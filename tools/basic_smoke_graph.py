"""Native GRAPH and Add-in ABI probes for the isolated ROM-A27 model."""

import hashlib
import json
import time
from decimal import Decimal

from basic_native import VARIABLE_A, VARIABLE_ANS, VARIABLE_X
from basic_smoke import DIGITS, pair, scalar_integer


def scalar_decimal(data):
    """Decode a real native20 value without binary floating-point rounding."""
    if len(data) != 20:
        raise ValueError("Native scalar must contain 20 bytes")
    if any(data[10:]):
        raise ValueError("Native value is not a real scalar")
    if not any(data):
        return Decimal(0)
    if data[9] not in (0, 1, 5, 6) or not 1 <= data[0] <= 9:
        raise ValueError("Unsupported native scalar class")
    digits = [data[0]]
    for byte in data[1:8]:
        hi, lo = byte >> 4, byte & 15
        if hi > 9 or lo > 9:
            raise ValueError("Invalid native mantissa BCD")
        digits.extend((hi, lo))
    hi, lo = data[8] >> 4, data[8] & 15
    if hi > 9 or lo > 9:
        raise ValueError("Invalid native exponent BCD")
    exponent = (data[9] % 5 - 1) * 100 + hi * 10 + lo
    return Decimal((int(data[9] >= 5), tuple(digits), exponent - 14))


def _record(out, name, **values):
    record = {"case": name, **values}
    number = values.get("number", values.get("ans"))
    if number is not None:
        try:
            record["decimal"] = str(scalar_decimal(bytes.fromhex(number)))
        except ValueError as error:
            record["scalar_error"] = str(error)
    out.joinpath(name + ".json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record


def _comp(emu):
    emu.call("clear_execution_breakpoints")
    emu.call("resume")
    emu.keys(0x70, 0x07, DIGITS[1])


def _stop(emu, address, keys=()):
    emu.call("clear_execution_breakpoints")
    emu.call("add_execution_breakpoint", address=address)
    emu.call("resume")
    if keys:
        time.sleep(0.15)
        emu.keys(*keys)
    deadline = time.monotonic() + 5
    while True:
        status = emu.call("get_status")
        if status["paused"] or time.monotonic() >= deadline:
            break
        time.sleep(0.05)
    if not status["paused"] or status["program_counter"] != address:
        emu.call("pause")
        raise AssertionError(("Native ABI breakpoint not reached", hex(address), status, emu.registers()))
    return emu.registers()


def _er(registers, index):
    return registers[f"r{index}"] | registers[f"r{index + 1}"] << 8


def _mcs_cases(emu, out):
    # Names, source and output slots must not live in the movable MCS heap.
    folder, name, source, output = 0x8200, 0x8210, 0x8240, 0x8260
    sentinels = {f"r{i}": 0x90 + i for i in range(4, 16)}
    common = pair(0, folder) | {"r2": 0} | sentinels
    data = b"EGW1\0\x80\0\xff"
    emu.active()
    for at, value in ((folder, b"main\0"), (name, b"E5GWORK\0"), (source, data)):
        emu.call("write_memory", address=at, bytes=list(value))
    results = []

    def invoke(address, stack, extra=None, reads=()):
        registers, values = emu.invoke(address, common | (extra or {}),
                                      [(0x8c00, stack)], reads, seconds=2, keep=True)
        assert registers["sp"] == 0x8c00, (hex(address), registers)
        assert all(registers[key] == value for key, value in sentinels.items()), (hex(address), registers)
        return registers, values

    def lookup(title):
        # Guard each native 1/3/3/4-byte output independently.
        emu.call("write_memory", address=output, bytes=[0xa5] * 20)
        stack = b"".join(at.to_bytes(4, "little")
                         for at in (name, output, output + 4, output + 8, output + 12))
        registers, values = invoke(0x1a574, stack, reads=[(output, 20)])
        raw = values[0]
        status = _er(registers, 0)
        pointer = int.from_bytes(raw[8:11], "little")
        length = int.from_bytes(raw[12:16], "little")
        payload = emu.memory(pointer, length) if status == 0 and length <= 12 else b""
        record = _record(out, title, native_entry="1:A574", status=status,
                         registers=registers, outputs=raw.hex(), payload_address=pointer,
                         length=length, payload=payload.hex())
        assert raw[1:4] == b"\xa5" * 3 and raw[7] == raw[11] == 0xa5 and raw[16:] == b"\xa5" * 4, record
        if status == 0:
            assert raw[0] == 0x0c and 0x40000 <= pointer < pointer + length <= 0x48000, record
        return record

    record = lookup("graph-abi-mcs-before")
    assert record["status"] == 0x30, ("E5GWORK already exists; refusing to replace it", record)
    results.append(record)
    stack = name.to_bytes(4, "little") + (8).to_bytes(4, "little") + source.to_bytes(4, "little")
    registers, _ = invoke(0x1a6c6, stack, {"r3": 0x0c})
    record = _record(out, "graph-abi-mcs-create", native_entry="1:A6C6", registers=registers,
                     status=_er(registers, 0), requested_length=8, source=data.hex())
    assert record["status"] == 0, record
    results.append(record)
    record = lookup("graph-abi-mcs-created")
    assert record["status"] == 0 and record["length"] == 8 and record["payload"] == data.hex(), record
    results.append(record)
    for title, address, count, expected in (
        ("grow", 0x1b1c2, 4, data + bytes(4)),
        ("shrink", 0x1b408, 4, data),
    ):
        stack = name.to_bytes(4, "little") + (8).to_bytes(4, "little") + count.to_bytes(4, "little")
        registers, _ = invoke(address, stack, {"r3": 0})
        record = _record(out, "graph-abi-mcs-" + title, native_entry=f"{address >> 16:X}:{address & 65535:04X}",
                         registers=registers, status=_er(registers, 0), offset=8, count=count)
        assert record["status"] == 0, record
        results.append(record)
        record = lookup("graph-abi-mcs-" + title + "-readback")
        assert record["status"] == 0 and record["length"] == len(expected) and record["payload"] == expected.hex(), record
        results.append(record)
    registers, _ = invoke(0x1afce, name.to_bytes(4, "little"))
    record = _record(out, "graph-abi-mcs-remove", native_entry="1:AFCE", registers=registers,
                     status=_er(registers, 0))
    assert record["status"] == 0, record
    results.append(record)
    record = lookup("graph-abi-mcs-removed")
    assert record["status"] == 0x30, record
    results.append(record)
    return results


def _table_case(emu, out):
    _comp(emu)
    call = _stop(emu, 0x7dae, (0x07, DIGITS[7]))
    entry = _stop(emu, 0xcfa0e)
    fp = _er(entry, 14)
    sp = entry["sp"]
    saved = emu.memory(sp, 8)
    outer = emu.memory(fp, 6)
    record = _record(out, "graph-abi-table-entry", call=call, entry=entry,
                     saved_registers=saved.hex(), outer_frame=outer.hex(), frame_pointer=fp)
    assert entry["lr"] == 0x7db2 and entry["lcsr"] == 0 and sp == fp - 0x3e, record
    selector = emu.memory(0xcfa0e, 4) != bytes.fromhex("ce f8 5e f8")
    continuation = _stop(emu, 0x7db2, (DIGITS[2],) if selector else ())
    record = _record(out, "graph-abi-table-return", entry=entry, continuation=continuation,
                     saved_registers=emu.memory(sp, 8).hex())
    assert continuation["sp"] == sp and _er(continuation, 14) == fp, record
    assert emu.memory(sp, 8) == saved, record

    # Exercise the measured early-exit frame recipe, not the native editor.
    restored = {"r8": saved[0], "r9": saved[1], "r12": saved[2], "r13": saved[3],
                **{f"r{i + 4}": value for i, value in enumerate(saved[4:8])},
                **pair(14, int.from_bytes(outer[:2], "little")), "sp": fp + 6,
                "pc": int.from_bytes(outer[2:6], "little")}
    emu.call("write_memory", address=0x8091, bytes=[0x81])
    for name, value in restored.items():
        emu.call("write_register", name=name, value=value)
    after = emu.registers()
    assert all(after[name] == value for name, value in restored.items()), after
    emu.call("clear_execution_breakpoints")
    emu.call("resume")
    time.sleep(0.15)
    emu.keys(0x70, DIGITS[1], 0x66, DIGITS[2], 0x63)
    value = emu.memory(VARIABLE_ANS, 20)
    record = _record(out, "graph-abi-table-host-unwind", entry=entry, restored=after,
                     recipe="saved ER8, ER12, XR4; SP=FP; POP ER14/PC; 8091=81",
                     ans=value.hex())
    assert scalar_decimal(value) == Decimal(3), record
    return record


def graph_abi_cases(emu, out):
    snapshot = emu.call("save_snapshot", label="Before GRAPH ABI smoke")["id"]
    results = []
    try:
        _comp(emu)
        for title, keys, expected in (
            ("zero", (DIGITS[0],), "0"),
            ("negative-one", (0x64, DIGITS[1]), "-1"),
            ("fraction", (0x51, DIGITS[5]), "0.5"),
            ("positive-exponent", (DIGITS[1], 0x61, DIGITS[1], DIGITS[0]), "1e10"),
            ("negative-exponent", (DIGITS[1], 0x61, 0x64, DIGITS[1], DIGITS[0]), "1e-10"),
        ):
            emu.keys(0x70, *keys, 0x63)
            value = emu.memory(VARIABLE_ANS, 20)
            record = _record(out, "graph-abi-decimal-" + title, keys=list(keys) + [0x63],
                             number=value.hex(), expected=expected)
            assert scalar_decimal(value) == Decimal(expected), record
            results.append(record)
        for letter, number in (("A", "13"), ("B", "17"), ("X", "23")):
            emu.keys(0x70, *(DIGITS[int(ch)] for ch in number))
            emu.assign(letter)
            emu.keys(0x63)
        emu.keys(0x70, DIGITS[2], DIGITS[9], 0x63)
        variables = (("A", VARIABLE_A, 13), ("B", VARIABLE_A + 20, 17),
                     ("X", VARIABLE_X, 23), ("Ans", VARIABLE_ANS, 29))
        before = {name: emu.memory(address, 20) for name, address, _ in variables}
        record = _record(out, "graph-abi-keyboard-variables", addresses={name: address for name, address, _ in variables},
                         numbers={name: value.hex() for name, value in before.items()})
        assert all(scalar_decimal(before[name]) == Decimal(value) for name, _, value in variables), record
        results.append(record)
        for x, y in ((-2, 5), (0, 1), (3, 10)):
            registers, data = emu.evaluate(b"X\xa9X\x891", [(VARIABLE_X, scalar_integer(x))],
                                           reads=[(address, 20) for _, address, _ in variables])
            record = _record(out, "graph-abi-evaluate-" + str(x), source="58a9588931", x=x,
                             registers=registers, number=data[0].hex(), cursor=data[1].hex(),
                             variables={name: value.hex() for (name, _, _), value in zip(variables, data[2:])})
            assert registers["r0"] == 1 and registers["sp"] == 0x8c00 and scalar_decimal(data[0]) == Decimal(y), record
            assert all(scalar_decimal(value) == Decimal(x if name == "X" else expected)
                       for (name, _, expected), value in zip(variables, data[2:])), record
            assert all(emu.memory(address, 20) == before[name] for name, address, _ in variables), record
            results.append(record)
        for title, source, error in (("syntax", b"1\x89", 0xf2), ("domain", b"1\xb90", 0xf3)):
            registers, data = emu.evaluate(source)
            record = _record(out, "graph-abi-error-" + title, source=source.hex(),
                             registers=registers, number=data[0].hex(), cursor=data[1].hex())
            assert registers["r0"] == 0 and registers["sp"] == 0x8c00 and data[0] == bytes([error]) + bytes(19), record
            results.append(record)
        mcs_snapshot = emu.call("save_snapshot", label="Before GRAPH MCS lifecycle")["id"]
        try:
            results.extend(_mcs_cases(emu, out))
        finally:
            emu.call("load_snapshot", id=mcs_snapshot)
        results.append(_table_case(emu, out))
        return results
    finally:
        emu.call("clear_execution_breakpoints")
        emu.call("load_snapshot", id=snapshot)


def addin_abi_cases(emu, out):
    from basic_smoke_apps import _idle

    snapshot = emu.call("save_snapshot", label="Before Add-in ABI smoke")["id"]
    results = []
    s4 = emu.memory(0x90000, 65536)
    try:
        _comp(emu)
        entry = _stop(emu, 0xcfa66, (0x40,))
        fp, buffer = _er(entry, 14), _er(entry, 0)
        frame = emu.memory(0x80e0, 384)
        fields = ((0x180, 0x807e, 2), (0x182, 0x808b, 1), (0x183, 0x80a5, 1),
                  (0x184, 0x80a6, 1), (0x186, 0x80a0, 1), (0x187, 0x80a1, 1),
                  (0x188, 0x80a2, 1), (0x18a, 0x80a3, 1))
        fonts = {offset: emu.memory(address, size) for offset, address, size in fields}
        record = _record(out, "addin-abi-devlop-entry", registers=entry, buffer=buffer,
                         frame_pointer=fp, frame=frame.hex(),
                         fields={f"{offset:03x}": value.hex() for offset, value in fonts.items()})
        assert entry["lr"] == 0x7758 and entry["lcsr"] == 0 and buffer == entry["sp"] == fp - 0x18c, record
        hooked = emu.memory(0xcfa66, 2) != bytes.fromhex("ce f8")
        saved_at = 0x7758
        if hooked:
            from firmware.e5800p.project import fw
            saved_at = fw.link()["symbols"]["develop_menu"]
        saved = _stop(emu, saved_at)
        data = emu.memory(buffer, 0x18c)
        record = _record(out, "addin-abi-devlop-saved", registers=saved, buffer=data.hex())
        assert saved["sp"] == buffer - (6 if hooked else 0) and _er(saved, 14) == fp and data[:384] == frame, record
        assert all(data[offset:offset + len(value)] == value for offset, value in fonts.items()), record
        results.append(record)
        _idle(emu)
        exited = _stop(emu, 0x7760, (0x26,))
        record = _record(out, "addin-abi-devlop-exit", registers=exited, entry=entry,
                         saved_buffer=emu.memory(buffer, 0x18c).hex())
        assert exited["sp"] == buffer and _er(exited, 14) == fp, record
        results.append(record)
        restored = _stop(emu, 0x776a)
        actual_frame = emu.memory(0x80e0, 384)
        actual_fonts = {offset: emu.memory(address, size) for offset, address, size in fields}
        record = _record(out, "addin-abi-devlop-restored", registers=restored,
                         frame=actual_frame.hex(),
                         fields={f"{offset:03x}": value.hex() for offset, value in actual_fonts.items()})
        assert actual_frame == frame and actual_fonts == fonts, record
        assert restored["sp"] == buffer and _er(restored, 14) == fp, record
        results.append(record)
        _comp(emu)
        emu.keys(0x70, DIGITS[1], 0x66, DIGITS[2], 0x63)
        value = emu.memory(VARIABLE_ANS, 20)
        record = _record(out, "addin-abi-comp-after-exit", number=value.hex())
        assert scalar_decimal(value) == Decimal(3), record
        results.append(record)

        # F:0484 rejects a nonzero native S4 marker before directory scanning.
        emu.active()
        registers, values = emu.invoke(0xf0484, pair(0, 0x8200) | pair(2, 0x01c7),
                                      [(0x8200, b"E5ABIQUERY\0"), (0x8220, b"\xa5" * 4),
                                       (0x80ad, b"\0"), (0x8c00, (0x8220).to_bytes(2, "little"))],
                                      [(0x8220, 4)], seconds=2)
        record = _record(out, "addin-abi-s4-named-query", registers=registers, status=_er(registers, 0),
                         native_marker=s4[0], output=values[0].hex(),
                         s4_sha256=hashlib.sha256(s4).hexdigest())
        assert registers["sp"] == 0x8c00 and values[0][3] == 0xa5, record
        assert record["status"] == (0xfff5 if s4[0] else 0xffff), record
        assert emu.memory(0x90000, 65536) == s4, "Read-only Add-in ABI probes changed S4"
        results.append(record)
        return results
    finally:
        emu.call("clear_execution_breakpoints")
        emu.call("load_snapshot", id=snapshot)
