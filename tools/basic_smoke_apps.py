"""Exercise S4 application validation, menus and the native launcher."""

import hashlib
import json
import runpy
import struct
import time
import zlib
from pathlib import Path

from basic_native import VARIABLE_A, VARIABLE_ANS, VARIABLE_X
from basic_smoke import DIGITS, LETTERS, pair, scalar_integer
from basic_smoke_graph import _comp, _er, _stop, scalar_decimal
from basic_smoke_graph_features import _until
from kits import Firmware, cpu
from kits.app import (S4_OFFSET, S4_SIZE, build_app, init_image, install_app,
                      read_app, read_apps)


_FIELDS = ((0x8000, 112), (0x8086, 2), (0x807e, 2), (0x808b, 1),
           (0x80a0, 7), (VARIABLE_A, 40), (VARIABLE_X, 20), (VARIABLE_ANS, 20))


def _record(out, name, **values):
    record = {"case": name, **values}
    out.joinpath(name + ".json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record


def _idle(emu, keys=()):
    emu.call("clear_execution_breakpoints")
    emu.call("resume")
    if keys:
        emu.keys(*keys)
    deadline = time.monotonic() + 10
    while True:
        status = emu.call("get_status")
        if status["run_status"] == 0:
            break
        if status["paused"] or time.monotonic() >= deadline:
            emu.call("pause")
            raise AssertionError(("Add-in did not reach keyboard input", status, emu.registers()))
        time.sleep(0.05)
    emu.call("pause")
    return emu.registers()


def _restore(emu, snapshot):
    """Pair saved native frames with a live RUN state and clock generator."""
    emu.call("reset")
    emu.call("resume")
    time.sleep(1)
    _comp(emu)
    emu.active()
    emu.call("load_snapshot", id=snapshot)


def _display(emu):
    return emu.memory(0x80e0, 384), emu.memory(0xf800, 512)




def _page(emu, out, name):
    frame, lcd = _display(emu)
    record = _record(out, name, registers=emu.registers(),
                     frame=frame.hex(), lcd=lcd.hex())
    out.joinpath(name + "-lcd.bin").write_bytes(lcd)
    return record


def _return_app(name, address, value, *, stack=512, marker=False):
    fw = Firmware(name, regions=((address, address + 0x100),))

    if marker:
        @fw.function(native=True, address=address)
        def main():
            cpu.r0 = 0x42
            cpu.mem8[0, 0x821e] = cpu.r0
            cpu.r0 = value
            cpu.r1 = 0
            cpu.ret()
    else:
        @fw.function(native=True, address=address)
        def main():
            cpu.r0 = value
            cpu.r1 = 0
            cpu.ret()

    return build_app(fw, stack_bytes=stack)[0]


def _work_app():
    fw = Firmware("WORK", regions=((0x92000, 0x93000),))

    @fw.function(native=True, address=0x92000)
    def main():
        cpu.mem16[0, 0x8200] = cpu.er0
        cpu.mem16[0, 0x8202] = cpu.er2
        cpu.mem16[0, 0x8204] = cpu.er4
        cpu.mem16[0, 0x8206] = cpu.er6
        cpu.er8 = cpu.sp
        cpu.mem16[0, 0x8208] = cpu.er8
        cpu.er8 = cpu.mem16[0, cpu.er0]
        cpu.mem16[0, 0x820a] = cpu.er8
        cpu.er8 = cpu.mem16[0, cpu.offset(cpu.er0, 2)]
        cpu.mem16[0, 0x820c] = cpu.er8
        cpu.er8 = 0x8000
        cpu.r0 = 0x5a
        cpu.r2 = 112
        cpu.label('math')
        cpu.mem8[0, cpu.er8] = cpu.r0
        cpu.er8 += 1
        cpu.r2 += 0xff
        if cpu.ne:
            cpu.branch('math')
        cpu.er0 = 0x5a5a
        cpu.mem16[0, 0x8086] = cpu.er0
        cpu.mem16[0, 0x807e] = cpu.er0
        cpu.mem8[0, 0x808b] = cpu.r0
        cpu.er8 = 0x80a0
        cpu.r2 = 7
        cpu.label('font')
        cpu.mem8[0, cpu.er8] = cpu.r0
        cpu.er8 += 1
        cpu.r2 += 0xff
        if cpu.ne:
            cpu.branch('font')
        cpu.r0 = 9
        cpu.mem8[VARIABLE_A >> 16, VARIABLE_A & 0xffff] = cpu.r0
        cpu.er2 = 0x1234
        cpu.ea = cpu.address(cpu.er2)
        cpu.er4 = 0x4567
        cpu.er6 = 0x6789
        cpu.er8 = 0x89ab
        cpu.er10 = 0xabcd
        cpu.er12 = 0xcdef
        cpu.er14 = 0xef01
        cpu.r2 = 0
        cpu.psw = cpu.r2
        cpu.er2 = 0x2345
        cpu.er0 = 93
        cpu.ret()

    return build_app(fw, work_bytes=3, stack_bytes=512)[0]


def _bad_header(image, offset, value):
    result = bytearray(image)
    end = S4_OFFSET + S4_SIZE
    count = int.from_bytes(result[end - 10:end - 8], "little")
    start = end - 16 - count * 44
    result[start + offset:start + offset + len(value)] = value
    crc = zlib.crc32(result[start:end - 16], zlib.crc32(result[end - 16:end - 4]))
    struct.pack_into("<I", result, end - 4, crc)
    return bytes(result)

def _native_protect(emu, out, symbols, title, *, owned, confirm=False):
    """Run the stock Protect menu and Release, without the serial startup handshake."""
    fields = ((0x807e, 2), (0x808b, 1), (0x80a0, 7))
    before = emu.memory(0x90000, S4_SIZE)
    # Let the native prologue allocate its real frame. E94A0 is its menu
    # re-entry after the cable-only Reset OK? handshake at E9628.
    prologue, _ = emu.invoke(0xe945e, {}, stop_at=0xe946e, keep=True, seconds=3)
    emu.call("write_register", name="pc", value=0xe94a0)
    _stop(emu, 0xe967c)
    _idle(emu)
    menu_frame, menu_lcd = _display(emu)
    out.joinpath("addin-protect-" + title + "-menu-lcd.bin").write_bytes(menu_lcd)
    entry = _stop(emu, 0xe9614, (DIGITS[1],))
    frame, lcd = _display(emu)
    fonts = [emu.memory(at, size) for at, size in fields]
    stack = emu.memory(entry["sp"], 0x8c00 - entry["sp"])
    pc, gated = _until(emu, (symbols["apps_erase_confirm"], 0xe96ba))
    record = _record(out, "addin-protect-" + title + "-entry",
                     native_entry="E945E prologue; E94A0 menu re-entry",
                     omitted="Serial cable Reset OK? handshake E9628",
                     prologue=prologue, registers=entry, next_pc=pc,
                     menu_frame=menu_frame.hex(), menu_lcd=menu_lcd.hex(),
                     frame=frame.hex(), fonts=[value.hex() for value in fonts],
                     s4_sha256=hashlib.sha256(before).hexdigest())
    assert entry["sp"] == prologue["sp"] and _er(entry, 14) == _er(prologue, 14), record
    assert pc == (symbols["apps_erase_confirm"] if owned else 0xe96ba), record
    results = [record]
    if owned:
        _idle(emu)
        results.append(_page(emu, out, "addin-protect-" + title + "-warning"))
        pc, gated = _until(emu, (0xe96ba, 0xe9618), (0x63 if confirm else 0x26,))
        record = _record(out, "addin-protect-" + title + "-approval", next_pc=pc,
                         registers=gated, frame=emu.memory(0x80e0, 384).hex(),
                         fonts=[emu.memory(at, size).hex() for at, size in fields],
                         s4_sha256=hashlib.sha256(emu.memory(0x90000, S4_SIZE)).hexdigest())
        assert pc == (0xe96ba if confirm else 0xe9618), record
        assert gated["sp"] == entry["sp"] and _er(gated, 14) == _er(entry, 14), record
        assert emu.memory(entry["sp"], len(stack)) == stack, record
        assert emu.memory(0x80e0, 384) == frame, record
        assert [emu.memory(at, size) for at, size in fields] == fonts, record
        assert emu.memory(0x90000, S4_SIZE) == before, record
        for index in range(2 if confirm else 0, 16):
            assert gated[f"r{index}"] == entry[f"r{index}"], record
        if confirm:
            assert _er(gated, 0) == 1, record
        results.append(record)

    if confirm:
        _idle(emu)
        native_frame, native_lcd = _display(emu)
        record = _record(out, "addin-protect-" + title + "-native-release",
                         registers=emu.registers(), frame=native_frame.hex(), lcd=native_lcd.hex())
        out.joinpath(record["case"] + "-lcd.bin").write_bytes(native_lcd)
        assert emu.memory(0x90000, S4_SIZE) == before, record
        results.append(record)
        _, erased = _until(emu, 0xe979e, (0x63,), seconds=30)
        after = emu.memory(0x90000, S4_SIZE)
        record = _record(out, "addin-protect-native-erase", registers=erased,
                         native_call="E979A -> 0:4EF4; stopped after return at E979E",
                         sector=4, before_sha256=hashlib.sha256(before).hexdigest(),
                         after_sha256=hashlib.sha256(after).hexdigest(),
                         changed_bytes=sum(a != b for a, b in zip(before, after)))
        assert _er(erased, 0) == 0 and after == b"\xff" * S4_SIZE and after != before, record
        results.append(record)
        _stop(emu, 0xe97b6)
        _idle(emu)
        restarted = _until(emu, 0x5c92, (0x26,))[1]
        results.append(_record(out, "addin-protect-native-restart",
                               native_call="E97E4 -> 0:5C92 soft reset", registers=restarted))
        _idle(emu)
        _comp(emu)
        emu.keys(DIGITS[1], 0x66, DIGITS[2], 0x63)
        answer = emu.memory(VARIABLE_ANS, 20)
        record = _record(out, "addin-protect-comp-after-release",
                         number=answer.hex(), decimal=str(scalar_decimal(answer)))
        assert scalar_decimal(answer) == 3, record
        results.append(record)
        assert emu.memory(0x90000, S4_SIZE) == b"\xff" * S4_SIZE
        return results
    elif not owned:
        assert _er(gated, 0) == _er(entry, 0), record
        assert gated["sp"] == entry["sp"] and _er(gated, 14) == _er(entry, 14), record
        _idle(emu)
        returned = _stop(emu, 0xe9618, (0x26,))
    else:
        returned = gated
    after = emu.memory(0x90000, S4_SIZE)
    record = _record(out, "addin-protect-" + title + "-return", registers=returned,
                     entry=entry, s4_sha256=hashlib.sha256(after).hexdigest())
    assert returned["sp"] == entry["sp"] and _er(returned, 14) == _er(entry, 14), record
    assert all(returned[f"r{i}"] == entry[f"r{i}"] for i in range(4, 16)), record
    assert after == (b"\xff" * S4_SIZE if confirm else before), record
    results.append(record)
    return results


def _native_aging(emu, out, symbols, *, receive=False, confirm=False, seconds=30):
    """Use Devlop 4 -> 2; receive=True waits for a real external transfer."""
    snapshot = emu.call("save_snapshot", label="Before native YAMAYO Aging")["id"]
    before = emu.memory(0x90000, S4_SIZE)
    results = []
    try:
        _comp(emu)
        entry = _stop(emu, 0xe9f94, (0x40, DIGITS[4], DIGITS[2]))
        _idle(emu)
        frame, lcd = _display(emu)
        out.joinpath("addin-aging-menu-lcd.bin").write_bytes(lcd)
        _, transfer = _until(emu, 0x1bfc2, (DIGITS[2],))
        record = _record(out, "addin-aging-native-receive", entry=entry,
                         registers=transfer, frame=frame.hex(), lcd=lcd.hex(),
                         connection_status=emu.memory(0xf050, 1).hex(),
                         next_native_erase=0xea0e6,
                         prerequisite="1:BFC2 must receive real YAMAYO data before EA0E6",
                         receive_path=["1:BFC2", "1:D2B8 handshake", "1:D39C data",
                                       "1:34F4 wait", "0:6604 receive-buffer status"],
                         handshake="1:D2B8 requires packet kind 05 and status 00 before data reception",
                         s4_sha256=hashlib.sha256(before).hexdigest())
        assert emu.memory(0x90000, S4_SIZE) == before, record
        results.append(record)
        if not receive:
            return results
        try:
            pc, registers = _until(emu, (0xea0e6, 0xcfb04), seconds=seconds)
        except AssertionError:
            _record(out, "addin-aging-transfer-incomplete", status=emu.call("get_status"),
                    registers=emu.registers(), candidate_breakpoints=[0x1d2b8, 0x1d39c, 0xea0e6, 0xcfb04],
                    prerequisite="Complete a real YAMAYO transfer; no cable state or result is synthesized")
            raise
        record = _record(out, "addin-aging-transfer-result", next_pc=pc, registers=registers)
        assert pc == 0xea0e6, record
        results.append(record)
        _stop(emu, symbols["apps_erase_confirm"])
        _idle(emu)
        _, returned = _until(emu, 0xea0ea if confirm else 0x7518,
                             (0x63 if confirm else 0x26,), seconds=30)
        after = emu.memory(0x90000, S4_SIZE)
        record = _record(out, "addin-aging-native-" + ("erase" if confirm else "cancel"),
                         registers=returned, entry=entry, gate=registers,
                         before_sha256=hashlib.sha256(before).hexdigest(),
                         after_sha256=hashlib.sha256(after).hexdigest())
        if confirm:
            assert _er(returned, 0) == 0 and after == b"\xff" * S4_SIZE and after != before, record
        else:
            assert returned["sp"] == entry["sp"] and _er(returned, 14) == _er(entry, 14), record
            assert after == before, record
        results.append(record)
        return results
    finally:
        emu.call("clear_execution_breakpoints")
        try:
            _restore(emu, snapshot)
            emu.erase_flash(4)
            emu.program_flash(0x90000, before)
            assert emu.memory(0x90000, S4_SIZE) == before, "Aging probe did not restore S4"
        finally:
            emu.call("load_snapshot", id=snapshot)


def _native_trans(emu, out, symbols, *, confirm=False):
    """Create a COMP source, then use the native Devlop 5 -> 1 importer."""
    title = "confirm" if confirm else "cancel"
    snapshot = emu.call("save_snapshot", label="Before native YAMAYO Trans " + title)["id"]
    before = emu.memory(0x90000, S4_SIZE)
    results = []
    try:
        _comp(emu)
        existing = emu.records()
        name = next("APTRANS" + a + b for a in LETTERS for b in LETTERS
                    if "APTRANS" + a + b not in existing)
        emu.create(name)
        emu.keys(DIGITS[4], DIGITS[2], 0x26)
        sources = emu.records()
        source = sources[name]
        header = bytes.fromhex(source["header"])
        tokens = bytes.fromhex(source["source"])
        payload = header + tokens
        record = _record(out, "addin-trans-" + title + "-source",
                         program=name, native_record=source,
                         source_count=len(sources), existing_names=list(existing),
                         types={key: bytes.fromhex(value["header"])[0]
                                for key, value in sources.items()})
        assert header[:2] == b"\x01\0" and tokens == b"42\0", record
        assert int.from_bytes(header[2:6], "little") == len(tokens), record
        assert 1 <= len(sources) <= 128, record
        assert all(bytes.fromhex(value["header"])[0] != 2 for value in sources.values()), record
        results.append(record)

        _comp(emu)
        entry = _stop(emu, 0xc7dcc, (0x40, DIGITS[5], DIGITS[1]))
        pc, registers = _until(emu, (0xc7ec6, 0xc7fb6), seconds=30)
        record = _record(out, "addin-trans-" + title + "-native-preflight", entry=entry,
                         registers=registers, next_pc=pc, selector=emu.memory(0x80ad, 1).hex(),
                         native_status=_er(registers, 4), fixture=name,
                         s4_sha256=hashlib.sha256(before).hexdigest())
        assert emu.memory(0x90000, S4_SIZE) == before, record
        assert emu.memory(0x80ad, 1) == b"\0" and pc == 0xc7ec6, record
        results.append(record)
        frame, _ = _display(emu)
        fields = ((0x807e, 2), (0x808b, 1), (0x80a0, 7))
        fonts = [emu.memory(at, size) for at, size in fields]
        _stop(emu, symbols["apps_erase_confirm"])
        _idle(emu)
        results.append(_page(emu, out, "addin-trans-" + title + "-native-warning"))
        _, returned = _until(emu, 0xc7eca if confirm else 0x7460,
                             (0x63 if confirm else 0x26,), seconds=30)
        after = emu.memory(0x90000, S4_SIZE)
        record = _record(out, "addin-trans-native-" + ("erase" if confirm else "cancel"),
                         registers=returned, entry=entry, gate=registers,
                         before_sha256=hashlib.sha256(before).hexdigest(),
                         after_sha256=hashlib.sha256(after).hexdigest())
        assert emu.memory(0x80e0, 384) == frame, record
        assert [emu.memory(at, size) for at, size in fields] == fonts, record
        assert emu.records() == sources, record
        if confirm:
            assert returned["sp"] == registers["sp"], record
            assert _er(returned, 0) == 0 and after == b"\xff" * S4_SIZE and after != before, record
        else:
            assert returned["sp"] == entry["sp"] and _er(returned, 14) == _er(entry, 14), record
            assert after == before, record
        results.append(record)
        if confirm:
            _, completed = _until(emu, 0x73be, seconds=60)
            written = emu.memory(0x90000, S4_SIZE)
            record = _record(out, "addin-trans-native-write-complete", registers=completed,
                             native_return="C7FB2 finalizes library, C7FC2 returns to 0:73BE",
                             fixture=name, source_count=len(sources),
                             s4_sha256=hashlib.sha256(written).hexdigest())
            assert _er(completed, 0) == 0 and completed["sp"] == entry["sp"], record
            assert _er(completed, 14) == _er(entry, 14) and written[0] == 0, record
            assert written != before and written != b"\xff" * S4_SIZE, record
            assert emu.records() == sources, record
            results.append(record)

            queried, data = emu.invoke(
                0xf0484, pair(0, 0x8200) | pair(2, 0x01c7),
                [(0x8200, name.encode("ascii") + b"\0"), (0x8220, b"\xa5" * 4),
                 (0x80ad, b"\0"), (0x8c00, (0x8220).to_bytes(2, "little"))],
                [(0x8220, 4)], seconds=3)
            directory = int.from_bytes(data[0][:3], "little")
            record = _record(out, "addin-trans-native-library-query",
                             registers=queried, fixture=name, output=data[0].hex(),
                             directory=directory, expected_payload=payload.hex())
            assert _er(queried, 0) == 0 and queried["sp"] == 0x8c00, record
            assert data[0][3] == 0xa5 and 0x90020 <= directory < 0x92000, record
            results.append(record)
            item = emu.memory(directory, 32)
            size, address = struct.unpack_from("<II", item, 16)
            record = _record(out, "addin-trans-native-library-record", fixture=name,
                             directory_record=item.hex(), payload_address=address, payload_size=size)
            assert item[:4] == b"\x0f\0\xc7\x01", record
            assert item[4:16].split(b"\0", 1)[0] == name.encode("ascii"), record
            assert len(payload) <= size and 0x92000 <= address < address + size <= 0xa0000, record
            results.append(record)
            actual = emu.memory(address, len(payload))
            record = _record(out, "addin-trans-native-library-payload", fixture=name,
                             payload=actual.hex(), expected_payload=payload.hex())
            assert actual == payload and emu.memory(0x90000, S4_SIZE) == written, record
            results.append(record)
            _idle(emu)
            success_frame, success_lcd = _display(emu)
            record = _record(out, "addin-trans-native-success-page", registers=emu.registers(),
                             frame=success_frame.hex(), lcd=success_lcd.hex(),
                             stopped_before="EXIT optionally deletes system sources and calls 0:578E persistence")
            out.joinpath(record["case"] + "-lcd.bin").write_bytes(success_lcd)
            assert emu.memory(0x90000, S4_SIZE) == written, record
            results.append(record)
        return results
    finally:
        emu.call("clear_execution_breakpoints")
        try:
            _restore(emu, snapshot)
            emu.erase_flash(4)
            emu.program_flash(0x90000, before)
            assert emu.memory(0x90000, S4_SIZE) == before, "Trans probe did not restore S4"
        finally:
            emu.call("load_snapshot", id=snapshot)



def addin_cases(emu, out):
    from firmware.e5800p.apps import LAUNCH_RESERVE, STACK_LOW
    from firmware.e5800p.project import fw

    linked = fw.link()
    symbols = linked["symbols"]
    for name in ("apps", "apps_check", "apps_modified", "apps_launch",
                 "apps_screen", "apps_erase_confirm"):
        address = symbols[name]
        block = next(block for block in linked["blocks"]
                     if block["address"] <= address < block["address"] + len(block["data"]))
        offset = address - block["address"]
        expected = block["data"][offset:offset + 8]
        assert emu.memory(address, len(expected)) == expected, ("Wrong Add-in firmware", name, hex(address))

    root = Path(__file__).resolve().parents[1]
    hello = build_app(runpy.run_path(str(root / "examples/app_hello.py"))["fw"], stack_bytes=512)[0]
    seven = build_app(runpy.run_path(str(root / "examples/app_return.py"))["fw"], stack_bytes=512)[0]
    # LR, QR0, QR8, EA and ER2 are saved before the launch budget check.
    budget = (0x8c00 - 24 - STACK_LOW - LAUNCH_RESERVE) & ~1
    packages = (hello, seven, _work_app(),
                _return_app("BUDGETOK", 0x93000, 11, stack=budget, marker=True),
                _return_app("BUDGETNO", 0x94000, 12, stack=budget + 2, marker=True),
                _return_app("PATCH", 0x95000, 42))
    empty = init_image(b"\xff" * 0x80000)
    image = empty
    for data in packages:
        read_app(data)
        image = install_app(image, data)
    rows = read_apps(image)
    names = [row["name"] for row in rows]
    assert names == ["HELLO", "RETURN", "WORK", "BUDGETOK", "BUDGETNO", "PATCH"]
    assert not any(row["modified"] for row in rows)
    directory = 0x10000 - 16 - len(rows) * 44
    addresses = {row["name"]: directory + index * 44 for index, row in enumerate(rows)}
    results = []
    snapshot = emu.call("save_snapshot", label="Before Add-in runtime smoke")["id"]
    s4 = emu.memory(0x90000, S4_SIZE)
    baseline = None

    def install(fixture):
        _restore(emu, baseline)
        emu.erase_flash(4)
        emu.program_flash(0x90000, fixture[S4_OFFSET:S4_OFFSET + S4_SIZE])
        emu.call("load_snapshot", id=baseline)

    def check(title, fixture, expected, count=None):
        install(fixture)
        preserved = {f"r{i}": 0x90 + i for i in range(6, 16)}
        registers, _ = emu.invoke(symbols["apps_check"], preserved, seconds=3)
        record = _record(out, title, registers=registers, status=_er(registers, 0),
                         directory=_er(registers, 2), count=_er(registers, 4),
                         s4_sha256=hashlib.sha256(emu.memory(0x90000, S4_SIZE)).hexdigest())
        assert _er(registers, 0) == expected and registers["sp"] == 0x8c00, record
        assert all(registers[key] == value for key, value in preserved.items()), record
        if count is not None:
            assert _er(registers, 4) == count, record
            assert _er(registers, 2) == 0x10000 - 16 - count * 44, record
        results.append(record)

    def enter():
        emu.call("load_snapshot", id=baseline)
        _stop(emu, symbols["apps"], (0x07, DIGITS[9]))
        return _idle(emu)

    def returned(value, keys):
        _, registers = _until(emu, symbols["apps_return"], keys)
        assert _er(registers, 2) == value, registers
        _idle(emu)

    try:
        _comp(emu)
        emu.active()
        baseline = emu.call("save_snapshot", label="Add-in native COMP baseline")["id"]
        for title, fixture, status, count in (
            ("uninitialized", b"\xff" * 0x80000, 1, None),
            ("empty", empty, 0, 0),
        ):
            check("addin-check-" + title, fixture, status, count)
            enter()
            assert emu.memory(0x90000, S4_SIZE) == fixture[S4_OFFSET:S4_OFFSET + S4_SIZE]
            results.append(_page(emu, out, "addin-menu-" + title))
            _idle(emu, (0x26, 0x26))

        broken = bytearray(image)
        broken[S4_OFFSET + S4_SIZE - 1] ^= 1
        invalid = (("directory-crc", bytes(broken)),
                   ("header-format", _bad_header(image, 4, b"\x02\0")),
                   ("header-odd-entry", _bad_header(image, 12, b"\x01\0\0\0")))
        for title, fixture in invalid:
            try:
                read_apps(fixture)
            except ValueError as error:
                reason = str(error)
            else:
                raise AssertionError(("Host accepted malformed Add-in fixture", title))
            check("addin-check-" + title, fixture, 2)
            enter()
            assert emu.memory(0x90000, S4_SIZE) == fixture[S4_OFFSET:S4_OFFSET + S4_SIZE]
            results.append(_page(emu, out, "addin-menu-" + title))
            results.append(_record(out, "addin-host-reject-" + title, reason=reason))
            _idle(emu, (0x26, 0x26))

        check("addin-check-valid", image, 0, len(rows))
        for row in rows:
            registers, _ = emu.invoke(symbols["apps_modified"], pair(0, addresses[row["name"]]), seconds=3)
            assert _er(registers, 0) == 0 and registers["sp"] == 0x8c00, registers
        results.append(_record(out, "addin-code-crc", names=names, modified=[False] * len(rows)))

        sentinels = {f"r{i}": 0x40 + i for i in range(4, 16)}
        values = sentinels | {"psw": 0x80, "ea": 0x4560}
        writes = [(0x8000, bytes(range(112))), (0x8086, b"\x34\x12"),
                  (0x807e, b"\x56\x34"), (0x808b, b"\x12"),
                  (0x80a0, b"\x07\0\x01\0\0\0\0"),
                  (VARIABLE_A, scalar_integer(1)), (VARIABLE_A + 20, scalar_integer(2)),
                  (VARIABLE_X, scalar_integer(3)), (VARIABLE_ANS, scalar_integer(4))]
        expected_fields = [bytes(range(112)), b"\x34\x12", b"\x56\x34", b"\x12",
                           b"\x07\0\x01\0\0\0\0", scalar_integer(1) + scalar_integer(2),
                           scalar_integer(3), scalar_integer(4)]
        for name, result in (("RETURN", 7), ("WORK", 93), ("BUDGETOK", 11), ("BUDGETNO", 0)):
            extra = [(0x8200, b"\xa5" * 32)]
            if name == "WORK":
                extra += [(STACK_LOW, b"\xa5" * (0x8c00 - STACK_LOW))]
            registers, data = emu.invoke(symbols["apps_launch"], values | pair(0, addresses[name]),
                                         [*extra, *writes], [*_FIELDS, (0x8200, 32)], seconds=3)
            record = _record(out, "addin-launch-" + name.lower(), registers=registers,
                             return_value=_er(registers, 0), status=_er(registers, 2),
                             fields=[value.hex() for value in data[:-1]], probe=data[-1].hex(),
                             stack_bytes=rows[names.index(name)]["stack_bytes"])
            assert registers["sp"] == 0x8c00 and _er(registers, 0) == result, record
            assert _er(registers, 2) == (1 if name == "BUDGETNO" else 0), record
            assert registers["psw"] == values["psw"] and registers["ea"] == values["ea"], record
            assert all(registers[key] == value for key, value in sentinels.items()), record
            expected = list(expected_fields)
            if name == "WORK":
                expected[5] = scalar_integer(9) + scalar_integer(2)
                probe = data[-1]
                pointer, segment, length, reserved, sp = struct.unpack_from("<5H", probe)
                assert pointer & 1 == 0 and STACK_LOW <= pointer < 0x8c00, record
                assert (segment, length, reserved) == (0, 3, 0), record
                assert STACK_LOW <= sp < pointer and probe[10:14] == bytes(4), record
            if name.startswith("BUDGET"):
                assert data[-1][30] == (0xa5 if name == "BUDGETNO" else 0x42), record
            assert data[:-1] == expected, record
            results.append(record)

        registers, _ = emu.invoke(symbols["apps_launch"], pair(0, addresses["RETURN"]),
                                  stop_at=read_app(seven)["load_address"], seconds=2)
        record = _record(out, "addin-zero-work-entry", registers=registers)
        assert all(_er(registers, index) == 0 for index in (0, 2, 4, 6)), record
        results.append(record)

        emu.call("load_snapshot", id=baseline)
        native_entry = _stop(emu, 0xcfa66, (0x40,))
        native_frame = emu.memory(0x80e0, 384)
        native_fields = ((0x807e, 2), (0x808b, 1), (0x80a0, 7))
        native_fonts = [emu.memory(at, size) for at, size in native_fields]
        _stop(emu, symbols["apps"], (DIGITS[6],))
        _idle(emu)
        results.append(_page(emu, out, "addin-devlop-six"))
        variables = [emu.memory(at, size) for at, size in _FIELDS[5:]]
        returned(7, (DIGITS[2], 0x63))
        results.append(_page(emu, out, "addin-return-seven"))
        _idle(emu, (0x63, DIGITS[1], 0x63))
        results.append(_page(emu, out, "addin-hello"))
        returned(42, (0x26,))
        results.append(_page(emu, out, "addin-return-forty-two"))
        assert [emu.memory(at, size) for at, size in _FIELDS[5:]] == variables
        _idle(emu, (0x63, 0x57))
        results.append(_page(emu, out, "addin-page-two"))
        _idle(emu, (0x27,))
        results.append(_page(emu, out, "addin-page-one"))
        native_return = _stop(emu, 0x776a, (0x26, 0x26))
        record = _record(out, "addin-native-frame-restored", entry=native_entry,
                         registers=native_return, frame=emu.memory(0x80e0, 384).hex(),
                         fonts=[emu.memory(at, size).hex() for at, size in native_fields])
        assert native_entry["lr"] == 0x7758 and native_entry["lcsr"] == 0, record
        assert native_return["sp"] == native_entry["sp"], record
        assert _er(native_return, 14) == _er(native_entry, 14), record
        assert emu.memory(0x80e0, 384) == native_frame, record
        assert [emu.memory(at, size) for at, size in native_fields] == native_fonts, record
        results.append(record)
        _comp(emu)
        emu.keys(DIGITS[1], 0x66, DIGITS[2], 0x63)
        ans = emu.memory(VARIABLE_ANS, 20)
        record = _record(out, "addin-comp-after-return", number=ans.hex(), decimal=str(scalar_decimal(ans)))
        assert scalar_decimal(ans) == 3, record
        results.append(record)

        patch = rows[names.index("PATCH")]
        at = patch["load_address"]
        assert patch["payload"] == bytes.fromhex("2a 00 00 01 1f fe"), patch
        # Program only a 1-to-0 change, without rewriting the directory CRC.
        emu.program_flash(at, b"\x28")
        changed = bytearray(image)
        changed[at - 0x80000] = 0x28
        changed_rows = read_apps(changed)
        assert [row["name"] for row in changed_rows if row["modified"]] == ["PATCH"]
        registers, _ = emu.invoke(symbols["apps_modified"], pair(0, addresses["PATCH"]), seconds=3)
        record = _record(out, "addin-manual-code-change", address=at, before=42, after=40,
                         registers=registers, modified_names=[row["name"] for row in changed_rows if row["modified"]])
        assert _er(registers, 0) == 1, record
        results.append(record)
        enter()
        _idle(emu, (0x57, DIGITS[3]))
        results.append(_page(emu, out, "addin-modified-approval"))
        _idle(emu, (0x26,))
        results.append(_page(emu, out, "addin-modified-back"))
        returned(40, (DIGITS[3], 0x63))
        results.append(_page(emu, out, "addin-modified-return-forty"))
        returned(7, (0x63, 0x27, DIGITS[2], 0x63))
        results.append(_page(emu, out, "addin-unmodified-neighbor"))
        assert emu.memory(0x90000, S4_SIZE) == changed[S4_OFFSET:S4_OFFSET + S4_SIZE]
        _idle(emu, (0x63, 0x26, 0x26))

        for title, key, value in (("cancel", 0x26, 0), ("confirm", 0x63, 1)):
            before = emu.memory(0x90000, S4_SIZE)
            frame = bytes(range(256)) + bytes(range(128))
            fields = ((0x807e, 2), (0x808b, 1), (0x80a0, 7))
            fonts = [emu.memory(at, size) for at, size in fields]
            saved = emu.call("save_snapshot", label="Before erase warning input")["id"]
            try:
                emu.invoke(symbols["apps_erase_confirm"], sentinels,
                           [(0x80e0, frame)], stop_at=0x80800, seconds=10, keep=True)
                _, registers = _until(emu, 0, (key,), seconds=10)
                data = [emu.memory(at, size) for at, size in ((0x80e0, 384), *fields)]
            finally:
                emu.call("clear_execution_breakpoints")
                emu.call("load_snapshot", id=saved)
            record = _record(out, "addin-erase-" + title, registers=registers,
                             frame=data[0].hex(), fonts=[item.hex() for item in data[1:]],
                             s4_sha256=hashlib.sha256(before).hexdigest())
            assert _er(registers, 0) == value and registers["sp"] == 0x8c00, record
            assert all(registers[name] == item for name, item in sentinels.items()), record
            assert data == [frame, *fonts] and emu.memory(0x90000, S4_SIZE) == before, record
            results.append(record)

        stock = emu.original
        for title, fixture, owned in (("apps", image, 1), ("stock", stock, 0)):
            install(fixture)
            before = emu.memory(0x90000, S4_SIZE)
            registers, _ = emu.invoke(symbols["apps_owned"], sentinels, seconds=2)
            record = _record(out, "addin-s4-owner-" + title, registers=registers,
                             owned=_er(registers, 0),
                             s4_sha256=hashlib.sha256(before).hexdigest())
            assert _er(registers, 0) == owned and registers["sp"] == 0x8c00, record
            assert all(registers[name] == item for name, item in sentinels.items()), record
            results.append(record)
            registers, data = emu.invoke(
                0xf0484, pair(0, 0x8200) | pair(2, 0x01c7),
                [(0x8200, b"E5ABIQUERY\0"), (0x8220, b"\xa5" * 4),
                 (0x80ad, b"\0"), (0x8c00, (0x8220).to_bytes(2, "little"))],
                [(0x8220, 4)], seconds=3)
            record = _record(out, "addin-native-s4-query-" + title, registers=registers,
                             status=_er(registers, 0), native_marker=before[0],
                             output=data[0].hex(),
                             s4_sha256=hashlib.sha256(before).hexdigest())
            assert _er(registers, 0) == (0xfff5 if before[0] else 0xffff), record
            assert registers["sp"] == 0x8c00 and data[0][3] == 0xa5, record
            assert emu.memory(0x90000, S4_SIZE) == before, record
            results.append(record)
        for title, fixture, owned, confirm in (
            ("cancel", image, True, False),
            ("confirm", image, True, True),
            ("stock", stock, False, False),
        ):
            install(fixture)
            results.extend(_native_protect(emu, out, symbols, title, owned=owned, confirm=confirm))
        install(image)
        restored = emu.memory(0x90000, S4_SIZE)
        record = _record(out, "addin-native-erase-fixture-restored",
                         s4_sha256=hashlib.sha256(restored).hexdigest())
        assert restored == image[S4_OFFSET:S4_OFFSET + S4_SIZE], record
        results.append(record)
        results.extend(_native_aging(emu, out, symbols))
        results.extend(_native_trans(emu, out, symbols))
        results.extend(_native_trans(emu, out, symbols, confirm=True))
        return results
    finally:
        emu.call("clear_execution_breakpoints")
        try:
            _restore(emu, snapshot)
            emu.erase_flash(4)
            emu.program_flash(0x90000, s4)
            assert emu.memory(0x90000, S4_SIZE) == s4, "Add-in smoke did not restore S4"
            _record(out, "addin-original-s4-restored", size=len(s4),
                    s4_sha256=hashlib.sha256(s4).hexdigest())
        finally:
            emu.call("load_snapshot", id=snapshot)
