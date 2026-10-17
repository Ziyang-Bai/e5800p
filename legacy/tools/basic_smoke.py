"""Exercise fx-5800P firmware in the isolated MCP validation model."""

import argparse
import hashlib
import json
import time
from pathlib import Path

from casio_emulator import MCPClient
from casio_tool import require_server_model

from basic_native import ROM_SHA256, VARIABLE_A, VARIABLE_ANS

LETTERS = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", (
    0x04, 0x14, 0x24, 0x34, 0x44, 0x54, 0x23, 0x33, 0x43,
    0x53, 0x02, 0x12, 0x22, 0x01, 0x11, 0x21, 0x31, 0x67,
    0x42, 0x52, 0x62, 0x66, 0x65, 0x41, 0x51, 0x61,
)))
DIGITS = (0x41, 0x42, 0x52, 0x62, 0x01, 0x11, 0x21, 0x02, 0x12, 0x22)


class Emulator(MCPClient):
    def __init__(self, model):
        self.model = model.resolve()
        require_server_model("http://127.0.0.1:3001/mcp", self.model)
        super().__init__()
        rom = self.model.joinpath("rom.bin").read_bytes()
        if hashlib.sha256(rom).hexdigest() != ROM_SHA256:
            raise ValueError("Unexpected ROM-A27 image")
        if self.memory(0, 0x8000) != rom[:0x8000] or self.memory(0x10000, 0x10000) != rom[0x10000:]:
            raise ValueError("Running ROM differs from the validation model")


    def records(self):
        data = self.memory(0x40000, 0x8000)
        records = {}
        # This isolated fixture's system folder array starts at0128.
        for off in range(0x128, 0x8000 - 24, 24):
            record = data[off:off + 24]
            if record[20] != 0x47:
                break
            name = record[:12].split(b"\0", 1)[0].decode("ascii")
            start = 0x128 + int.from_bytes(record[12:16], "little")
            size = int.from_bytes(record[16:20], "little")
            if not 6 <= size <= 0x8000 - start:
                raise ValueError("Unexpected native file allocation")
            length = int.from_bytes(data[start + 2:start + 6], "little")
            if not 1 <= length <= size - 6 or data[start + 5 + length] != 0:
                raise ValueError("Unexpected native source length")
            records[name] = {"record": record.hex(" "), "payload": start,
                             "header": data[start:start + 6].hex(" "),
                             "source": data[start + 6:start + 6 + length].hex(" ")}
        return records

    def create(self, name):
        # Reenter PROG from COMP so the native mode cache reaches the selector.
        self.keys(0x26, 0x26, 0x26, 0x70, 0x07, 0x42, 0x07, 0x11, 0x42, 0x42)
        self.keys(*(LETTERS[c] for c in name), 0x63, 0x42)
        assert name in self.records(), f"Native NEW did not create {name}"

    def prog(self, page, digit):
        self.keys(0x17, 0x62, *([0x47] * page), DIGITS[digit])

    def nx(self, name):
        from basic_native import NX_CATEGORIES

        category, index = next((category, names.index(name))
                               for category, (_, names) in enumerate(NX_CATEGORIES)
                               if name in names)
        self.keys(0x17, 0x57, DIGITS[1], DIGITS[category + 1],
                  *([0x57] * (index // 4)), DIGITS[index % 4 + 1])

    def assign(self, letter):
        self.keys(0x06, 0x03, LETTERS[letter])

    def run(self):
        self.keys(0x63, 0x26, 0x26, 0x52, 0x63)

    def evidence(self, out, name):
        out.joinpath(name + "-lcd.bin").write_bytes(self.memory(0xf800, 512))
        out.joinpath(name + "-frame.bin").write_bytes(self.memory(0x80e0, 384))
        record = {"status": self.call("get_status"), "registers": self.registers(),
                  "math": self.memory(0x8000, 0x70).hex(" "),
                  "workspace": self.memory(0x8086, 2).hex(" "),
                  "A": self.memory(VARIABLE_A, 20).hex(" "),
                  "Ans": self.memory(VARIABLE_ANS, 20).hex(" "),
                  "files": self.records()}
        out.joinpath(name + ".json").write_text(json.dumps(record, indent=2), encoding="utf-8")
        return record

    def active(self):
        status = self.call("get_status")
        if status["paused"] and status["run_status"] == 2:
            return
        self.call("resume")
        self.call("add_execution_breakpoint", address=0x1234e)
        self.keys(0x70)
        time.sleep(0.5)
        status = self.call("get_status")
        self.call("clear_execution_breakpoints")
        if not status["paused"] or status["run_status"] != 2:
            raise RuntimeError("Native keyboard entry did not reach an active CPU")

    def invoke(self, address, values, writes=(), reads=(), seconds=0.15, keep=False, input_keys=(), stop_at=0):
        snapshot = self.call("save_snapshot", label="Before CPU smoke case")["id"]
        self.call("pause")
        try:
            self.call("clear_execution_breakpoints")
            for at, data in writes:
                self.call("write_memory", address=at, bytes=list(data))
            registers = {"sp": 0x8c00, "psw": 0, "lr": 0}
            registers.update(values)
            for name, value in registers.items():
                self.call("write_register", name=name, value=value)
            self.call("write_register", name="pc", value=address)
            self.call("add_execution_breakpoint", address=0)
            if stop_at:
                self.call("add_execution_breakpoint", address=stop_at)
            self.call("resume")
            if input_keys:
                deadline = time.monotonic() + 10
                while True:
                    status = self.call("get_status")
                    if status["paused"] or status["run_status"] == 0:
                        break
                    if time.monotonic() >= deadline:
                        raise AssertionError(("CPU did not reach keyboard input", status))
                    time.sleep(0.05)
                if not status["paused"]:
                    self.keys(*input_keys)
            deadline = time.monotonic() + seconds
            while True:
                status = self.call("get_status")
                if status["paused"] or time.monotonic() >= deadline:
                    break
                time.sleep(0.05)
            if not status["paused"] or status["program_counter"] != stop_at:
                self.call("pause")
                raise AssertionError(("CPU call did not reach stop", hex(address), hex(stop_at), status, self.registers()))
            return self.registers(), [self.memory(at, size) for at, size in reads]
        finally:
            self.call("clear_execution_breakpoints")
            if not keep:
                self.call("load_snapshot", id=snapshot)

    def evaluate(self, source, writes=(), seconds=1, reads=()):
        from basic_native import EVALUATE

        self.active()
        return self.invoke(EVALUATE, pair(0, 0x80ec) | {"r2": 0, "r3": 1},
                           [(0x46000, source + b"\0"), (0x80ec, (0x46000).to_bytes(4, "little")),
                            (0x80f0, b"\x01\0"), (0x8100, b"\xa5" * 20),
                            (0x8c00, bytes.fromhex("f0800000008100000000")), *writes],
                           [(0x8100, 20), (0x80ec, 4), *reads], seconds=seconds)

    def dispatch(self, address, token, args, writes=(), reads=(), keep=False):
        data = b"".join((value & 0xffffffff).to_bytes(4, "little")
                        for value in (list(args) + [0] * 6)[:6])
        registers, result = self.invoke(
            address, pair(0, token) | pair(2, 0x8800) | pair(4, 0x8840),
            [(0x8800, data), (0x8840, b"\xa5" * 4), *writes],
            [(0x8840, 4), *reads], seconds=300 if token == 15 else 60 if token == 4 else 0.15, keep=keep)
        assert registers["sp"] == 0x8c00, "Unbalanced runtime stack"
        return registers["r0"] | registers["r1"] << 8, result, registers

    def erase_flash(self, sector):
        if not 0 <= sector <= 10:
            raise ValueError("Flash sector must be 0..10")
        self.active()
        self.invoke(0x4ef4, pair(0, sector), seconds=60)
        start, size = (((0, 0x4000), (0x4000, 0x2000), (0x6000, 0x2000),
                        (0x8000, 0x8000))[sector] if sector < 4
                       else ((sector - 3) * 0x10000, 0x10000))
        assert self.memory(0x80000 + start, size) == b"\xff" * size, (
            "ROM erase did not clear the complete sector", sector)

    def program_flash(self, address, data):
        from basic_flash import FLASH_WRITE_ADDRESS

        if not 0x80000 <= address <= address + len(data) <= 0x100000:
            raise ValueError("Flash range must be within banks 8..F")
        self.active()
        for offset in range(0, len(data), 32768):
            chunk = data[offset:offset + 32768]
            status, result, _ = self.dispatch(
                FLASH_WRITE_ADDRESS, 15, [address + offset, 0x40000, len(chunk)],
                [(0x40000, chunk)], [(address + offset, len(chunk))])
            assert status == 0 and result[1] == chunk, (
                "Raw Flash programming failed", hex(address + offset), len(chunk), status)


def pair(register, value):
    return {f"r{register}": value & 255, f"r{register + 1}": value >> 8}


def scalar_integer(value):
    result = bytearray(20)
    if value:
        digits = str(abs(value))
        result[0] = int(digits[0])
        for index in range(1, len(digits), 2):
            result[(index + 1) // 2] = int(digits[index:index + 2].ljust(2, "0"), 16)
        result[8] = len(digits) - 1
        result[9] = 6 if value < 0 else 1
    return bytes(result)


def native(emu, out):
    existing = emu.records()
    names = ("NX" + a + b for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for b in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    names = iter(name for name in names if name not in existing)
    results = []
    name = next(names)
    emu.create(name)
    emu.keys(DIGITS[1]); emu.assign("A"); emu.run()
    assert emu.memory(VARIABLE_A, 20) == scalar_integer(1), "Native assignment failed"
    results.append(emu.evidence(out, "assignment"))

    name = next(names)
    emu.create(name)
    emu.keys(0x17, 0x42, 0x47, 0x42, 0x64, DIGITS[1], 0x33)
    emu.assign("B"); emu.run()
    assert emu.memory(VARIABLE_A + 20, 20) == scalar_integer(1), "Native Abs failed"
    results.append(emu.evidence(out, "abs"))

    for title, opener, closer, expected in (
        ("if_false", (0, 3), (0, 6), 8),
        ("while_false", (3, 5), (3, 6), 7),
    ):
        name = next(names)
        emu.create(name); emu.prog(*opener); emu.keys(DIGITS[0], 0x63)
        if title == "if_false":
            emu.prog(0, 4)
        emu.keys(DIGITS[1], 0x67, DIGITS[0], 0x63)
        if title == "if_false":
            emu.prog(0, 5)
            emu.keys(DIGITS[expected]); emu.assign("B"); emu.keys(0x63)
        emu.prog(*closer); emu.keys(0x63)
        emu.keys(DIGITS[expected]); emu.assign("B"); emu.run()
        assert emu.memory(VARIABLE_A + 20, 20) == scalar_integer(expected), title
        results.append(emu.evidence(out, title))

    name = next(names)
    emu.create(name); emu.prog(3, 1); emu.keys(DIGITS[1]); emu.assign("A")
    emu.prog(3, 2); emu.keys(DIGITS[3], 0x63)
    emu.keys(0x16, LETTERS["A"]); emu.assign("B"); emu.keys(0x63)
    emu.prog(3, 4); emu.run()
    assert emu.memory(VARIABLE_A, 20) == scalar_integer(3), "For iterator"
    assert emu.memory(VARIABLE_A + 20, 20) == scalar_integer(3), "For body"
    results.append(emu.evidence(out, "for"))
    return results


def codec(emu, out):
    from instruction_codec import ENCODE_ADDRESS, SOURCE_LENGTH_ADDRESS
    from instruction_table import ENTRIES, INSTRUCTION_RECORDS_ADDRESS

    emu.active()
    results = []
    for name, fields, expected in (
        ("MOV R,#", [0, 2, 10], "2a00"), ("PUSH XR", [4], "6ef4"),
        ("POP QR", [8], "3ef8"), ("PUSH LR", [], "cef8"),
        ("POP PC", [], "8ef2"), ("L R,[ER]", [0, 2, 0, 0, 0, 0, 0, 4], "04e32090"),
        ("L R,[ER]", [4, 2, 0, 0, 0, 0, 0, 4], "04e32094"),
        ("L ER,[ER]", [4, 2, 0, 0, 0, 0, 0, 4], "04e32294"),
        ("ST R,[ER]", [6, 2, 0, 0, 0, 0, 0, 4], "04e32196"),
        ("ST ER,[ER]", [6, 2, 0, 0, 0, 0, 0, 4], "04e32396"),
        ("RET", [], "1ffe"),
    ):
        index = next(i for i, entry in enumerate(ENTRIES) if entry[2] == name)
        nibbles = bytearray(8)
        nibbles[7] = 255
        nibbles[:len(fields)] = bytes(fields)
        expected = bytes.fromhex(expected)
        registers, data = emu.invoke(
            ENCODE_ADDRESS, pair(0, 0x4000) | pair(2, (INSTRUCTION_RECORDS_ADDRESS + 16 * index) & 65535)
            | pair(4, 0x8800) | pair(6, 0x8810),
            [(0x8800, nibbles), (0x8810, b"\xa5" * 16)], [(0x8810, 16)])
        assert registers["r0"] == registers["r1"] == 0 and registers["r2"] == len(expected), name
        assert data[0] == expected + b"\xa5" * (16 - len(expected)), (name, "output overrun")
        results.append({"instruction": name, "bytes": data[0].hex(), "length": registers["r2"]})
    for source, expected in (("04e32090", 4), ("04e310903412", 6), ("04e3", 65535),
                             ("04e31ffe", 65535), ("6ef4", 2)):
        source = bytes.fromhex(source)
        registers, _ = emu.invoke(SOURCE_LENGTH_ADDRESS,
                                  pair(0, 0x8800) | {"r2": 0} | pair(4, 0x8800 + len(source)),
                                  [(0x8800, source)])
        length = registers["r0"] | registers["r1"] << 8
        assert length == expected, source.hex()
        results.append({"source": source.hex(), "length": length})
    return results


def memory_cases(emu, out):
    from basic_memory import MEMORY_ADDRESS, NUMBER_TO_INTEGER_ADDRESS, INTEGER_TO_NUMBER_ADDRESS

    emu.active()
    results = []
    for value, kind, real in (
        (0, 2, "00000000000000000000"), (255, 0, "02550000000000000201"),
        (65535, 1, "06553500000000000401"), (1048575, 2, "01048575000000000601"),
        (16777215, 4, "01677721500000000701"), (None, 4, "01677721600000000701"),
        (-32768, 3, "03276800000000000406"),
        (None, 0, "02560000000000000201"), (None, 1, "06553600000000000401"),
        (None, 1, "05000000000000009900"),
        (None, 1, "f3000000000000000000"),
    ):
        native_value = bytes.fromhex(real) + bytes(10)
        registers, data = emu.invoke(NUMBER_TO_INTEGER_ADDRESS,
                                     pair(0, 0x8800) | pair(2, kind) | pair(4, 0x8820),
                                     [(0x8800, native_value), (0x8820, b"\xa5" * 4)], [(0x8820, 4)])
        status = registers["r0"] | registers["r1"] << 8
        if value is None:
            assert status == 4 and data[0] == b"\xa5" * 4, "Invalid native scalar accepted"
        else:
            assert status == 0 and int.from_bytes(data[0], "little", signed=value < 0) == value
            if value >= 0:
                _, encoded = emu.invoke(INTEGER_TO_NUMBER_ADDRESS, pair(0, 0x8800) | pair(2, 0x8820),
                                         [(0x8800, value.to_bytes(4, "little"))], [(0x8820, 20)])
                assert encoded[0] == native_value, "Noncanonical native scalar"
        results.append({"native": native_value.hex(), "status": status, "integer": data[0].hex()})
    for token, args, expected, changed in (
        (0, [0x80ec], 0, bytes(range(8))),
        (1, [0x80ed], 513, bytes(range(8))),
        (2, [0x80ec, 65], 0, b"A" + bytes(range(1, 8))),
        (3, [0x80ed, 4660], 0, bytes.fromhex("0034120304050607")),
        (13, [0x80ee, 0x80ec, 6], 0, bytes.fromhex("0001000102030405")),
        (13, [0x80ec, 0x80ee, 6], 0, bytes.fromhex("0203040506070607")),
        (14, [0x80ee, 3, 85], 0, bytes.fromhex("0001555555050607")),
        (5, [65535, 255], 255, bytes(range(8))),
        (6, [256, 1], 257, bytes(range(8))),
        (7, [65535, 255], 65280, bytes(range(8))),
        (8, [32768, 1], 0, bytes(range(8))),
        (9, [32768, 15], 1, bytes(range(8))),
        (14, [0xffffff, 0, 0], 0, bytes(range(8))),
        (13, [0xffffff, 0xffffff, 0], 0, bytes(range(8))),
    ):
        status, data, _ = emu.dispatch(MEMORY_ADDRESS, token, args,
                                       [(0x80ec, bytes(range(8)))], [(0x80ec, 8)])
        assert status == 0 and int.from_bytes(data[0], "little") == expected, (token, args)
        assert data[1] == changed, (token, "incorrect write range")
        results.append({"token": token, "args": args, "result": expected})
    for token, args in ((1, [0xffffff]), (8, [1, 16])):
        status, data, _ = emu.dispatch(MEMORY_ADDRESS, token, args,
                                       [(0x80ec, bytes(range(8)))], [(0x80ec, 8)])
        assert status == 4 and data[1] == bytes(range(8)) and data[0] == b"\xa5" * 4, (token, args)
        results.append({"token": token, "args": args, "status": status})
    for address, width in ((0x7fff, 1), (0x8dff, 1), (0x10000, 1), (0x1ffff, 1),
                           (0x40000, 1), (0x47fff, 1), (0x80000, 1), (0xfffff, 1),
                           (0x7fff, 2), (0x8ffff, 2), (0xbffff, 2), (0xfffff, 2),
                           (0x100000, 1), (0xfffffe, 2), (0xffffff, 1)):
        expected = emu.memory(address, width)
        status, data, _ = emu.dispatch(MEMORY_ADDRESS, width - 1, [address])
        assert status == 0 and int.from_bytes(data[0], "little") == int.from_bytes(expected, "little")
        results.append({"address": address, "read_bytes": expected.hex()})
    expected = emu.memory(0xbffff, 3)
    status, data, _ = emu.dispatch(MEMORY_ADDRESS, 13, [0x80ec, 0xbffff, 3],
                                   [(0x80ec, b"\xa5" * 8)], [(0x80ec, 8)])
    assert status == 0 and data[1] == expected + b"\xa5" * 5
    results.append({"case": "copy_across_flash_segment", "bytes": data[1].hex()})
    for token, args, address in ((3, [0xffffff, 4660], 0x80ec),
                                 (14, [0xffffff, 2, 65], 0x80ec),
                                 (13, [0x80ec, 0xffffff, 2], 0x80ec)):
        status, data, _ = emu.dispatch(MEMORY_ADDRESS, token, args,
                                       [(address, b"\xa5\xa5")], [(address, 2)])
        assert status == 4 and data[1] == b"\xa5\xa5", "Range failure performed a partial write"
        results.append({"token": token, "args": args, "preserved": data[1].hex()})
    # KO is writable without reconfiguring clocks or the interrupt controller.
    ko = emu.memory(0xf044, 1)
    try:
        value = ko[0] ^ 1
        status, data, _ = emu.dispatch(MEMORY_ADDRESS, 2, [0xf044, value],
                                       reads=[(0xf044, 1)])
        assert status == 0 and data[1] == bytes((value,))
        status, data, _ = emu.dispatch(MEMORY_ADDRESS, 0, [0xf044],
                                       [(0xf044, bytes((value,)))])
        assert status == 0 and int.from_bytes(data[0], "little") == value
        results.append({"case": "sfr_peek_poke", "address": 0xf044, "value": value})
    finally:
        emu.call("write_memory", address=0xf044, bytes=list(ko))
    for code, expected in ((None, 0), (0x42, 67), (0x06, 7)):
        if code is not None:
            emu.call("keyboard_code", code=code, pressed=True)
        try:
            status, data, _ = emu.dispatch(MEMORY_ADDRESS, 10, [])
            assert status == 0 and int.from_bytes(data[0], "little") == expected
            results.append({"physical_key": code, "INKEY": expected})
        finally:
            if code is not None:
                emu.call("keyboard_code", code=code, pressed=False)
    return results


def graphics_cases(emu, out):
    from basic_graphics import GRAPHICS_ADDRESS

    emu.active()
    results = []
    for token, args, pixels in (
        (17, [0, 0, 1], {(0, 0)}), (17, [95, 30, 1], {(95, 30)}),
        (17, [-1, 0, 1], set()), (18, [0, 0, 3, 0, 1], {(x, 0) for x in range(4)}),
        (18, [0, 0, 3, 3, 1], {(x, x) for x in range(4)}),
        (18, [3, 0, 0, 3, 1], {(3 - y, y) for y in range(4)}),
        (19, [1, 1, 3, 3, 2], {(x, y) for x in range(1, 4) for y in range(1, 4)
                                if x in (1, 3) or y in (1, 3)}),
        (19, [2, 2, 2, 2, 2], {(2, 2)}),
    ):
        initial = b"\xa5" * 12 + bytes(372)
        expected = bytearray(initial)
        for x, y in pixels:
            expected[(y + 1) * 12 + x // 8] |= 128 >> (x & 7)
        before_lcd = emu.memory(0xf800, 512)
        status, data, _ = emu.dispatch(GRAPHICS_ADDRESS, token, args,
                                       [(0x80e0, initial)], [(0x80e0, 384), (0xf800, 512)])
        assert status == 0 and data[1] == expected and data[2] == before_lcd, (token, args)
        results.append({"token": token, "args": args, "frame": data[1].hex()})
    initial = bytearray(384)
    initial[:12] = b"\xa5" * 12
    initial[12:36] = bytes(range(24))
    expected = bytearray(initial)
    expected[24:48] = initial[12:36]
    status, data, _ = emu.dispatch(GRAPHICS_ADDRESS, 20, [0, 1, 96, 2, 0x80ec, 0],
                                   [(0x80e0, initial)], [(0x80e0, 384)])
    assert status == 0 and data[1] == expected, "Self-BLIT overwrote unread source"
    results.append({"self_blit": data[1].hex()})
    status, data, _ = emu.dispatch(GRAPHICS_ADDRESS, 16, [], [(0x80e0, b"\xff" * 384)],
                                   [(0x80e0, 384)])
    assert status == 0 and data[1] == b"\xff" * 12 + bytes(372), "CLS changed status row"
    results.append({"CLS": data[1].hex()})
    return results


def flash_cases(emu, out):
    from basic_flash import FLASH_WRITE_ADDRESS
    from basic_memory import MEMORY_ADDRESS

    emu.active()
    before = emu.memory(0x84000, 8192)
    other = emu.memory(0x90000, 65536)
    edge = emu.memory(0x88000, 32768)
    backup = emu.memory(0x86000, 8192)
    out.joinpath("before-s1.bin").write_bytes(before)
    out.joinpath("before-bank9.bin").write_bytes(other)
    results = []
    try:
        for sector, base, size in ((1, 0x84000, 8192), (4, 0x90000, 65536)):
            emu.erase_flash(sector)
            payload = bytes.fromhex("2a0000011ffe")
            emu.program_flash(base, payload)
            expected = payload + b"\xff" * (size - len(payload))
            assert emu.memory(base, size) == expected
            status, data, _ = emu.dispatch(MEMORY_ADDRESS, 4, [base])
            assert status == 0 and int.from_bytes(data[0], "little") == 42
            results.append({"case": "raw_write_and_call", "address": base, "return": 42})

            # Repeating a raw write needs no erase and never touches the journal.
            emu.program_flash(base, payload)
            assert emu.memory(base, size) == expected and emu.memory(0x86000, 8192) == backup
            # Byte zero could clear bits; byte one needs a forbidden 0->1 transition.
            status, data, _ = emu.dispatch(
                FLASH_WRITE_ADDRESS, 15, [base, 0x80ec, 2],
                [(0x80ec, b"\x20\x01")], [(base, size)])
            assert status != 0 and data[1] == expected, "Raw write partially programmed before failure"
            results.append({"case": "nor_preflight", "address": base, "status": status})

        emu.program_flash(0x85ff0, b"\x12\x34")
        assert emu.memory(0x85ff0, 2) == b"\x12\x34", "Legacy metadata is not reserved by raw writes"
        source = emu.memory(0x10000, 31)
        status, data, _ = emu.dispatch(
            FLASH_WRITE_ADDRESS, 15, [0x84101, 0x10000, len(source)],
            reads=[(0x84100, 33)])
        assert status == 0 and data[1] == b"\xff" + source + b"\xff"
        results.append({"case": "rom_source_odd_destination", "bytes": data[1].hex()})
        emu.erase_flash(3)
        emu.erase_flash(4)
        crossing = bytes(range(32))
        emu.program_flash(0x8fff0, crossing)
        assert emu.memory(0x8ffef, 34) == b"\xff" + crossing + b"\xff"
        emu.program_flash(0x9fff0, crossing[:16])
        source = emu.memory(0x9fff0, 32)
        status, data, _ = emu.dispatch(
            FLASH_WRITE_ADDRESS, 15, [0x84200, 0x9fff0, 32],
            reads=[(0x841ff, 34)])
        assert status == 0 and data[1] == b"\xff" + source + b"\xff"
        results.append({"case": "source_and_destination_bank_carry",
                        "destination_bytes": crossing.hex(), "source_bytes": source.hex()})
        for args in ([0x100000, 0x80ec, 1], [0x7ffff, 0x80ec, 1],
                     [0xfffff, 0x80ec, 2], [0x84200, 0xffffff, 2]):
            stable = emu.memory(0x84000, 8192)
            status, data, _ = emu.dispatch(FLASH_WRITE_ADDRESS, 15, args,
                                           reads=[(0x84000, 8192)])
            assert status != 0 and data[1] == stable, "Invalid raw range changed Flash"
            results.append({"args": args, "status": status})
        status, _, _ = emu.dispatch(FLASH_WRITE_ADDRESS, 15, [0xfffff, 0xffffff, 0])
        assert status == 0
        assert emu.memory(0x86000, 8192) == backup, "Raw Flash writes changed the legacy backup"
        return results
    finally:
        # CPU snapshots do not restore NOR; erase and program every changed sector.
        emu.erase_flash(1)
        emu.program_flash(0x84000, before)
        emu.erase_flash(3)
        emu.program_flash(0x88000, edge)
        emu.erase_flash(4)
        emu.program_flash(0x90000, other)


def asm_cases(emu, out):
    from basic_asm import ASM_EXEC_ADDRESS, ASM_SKIP_ADDRESS

    emu.call("resume")
    existing = emu.records()
    name = next("NXIND" + a + b for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                for b in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if "NXIND" + a + b not in existing)
    emu.create(name)
    emu.keys(DIGITS[4], DIGITS[2], 0x26)
    record = emu.records()[name]
    assert int.from_bytes(bytes.fromhex(record["record"])[16:20], "little") >= 8
    buffer = 0x40000 + record["payload"] + 6
    emu.active()
    before = emu.memory(0x84000, 8192)
    other = emu.memory(0x90000, 65536)
    out.joinpath("before-s1-s2.bin").write_bytes(emu.memory(0x84000, 16384))
    preserved = {f"r{r}": 16 + r for r in range(4, 16)}
    results = []

    def compile_source(source, *, skip=False, seconds=0.3, writes=(), reads=()):
        info = b"".join(value.to_bytes(4, "little")
                        for value in (0x46000, 0x46000 + len(source), 0x46000))
        registers, data = emu.invoke(
            ASM_SKIP_ADDRESS if skip else ASM_EXEC_ADDRESS,
            pair(0, 0x8800) | pair(2, 0x8820) | preserved,
            [(0x46000, source), (0x8800, info), (0x8820, b"\xa5" * 16), *writes],
            [(0x8820, 16), (0x84000, 16384), *reads], seconds=seconds)
        assert registers["sp"] == 0x8c00
        assert all(registers[name] == value for name, value in preserved.items()), "ASM register corruption"
        status = registers["r0"] | registers["r1"] << 8
        result = {"source": source.hex(), "status": status, "output": data[0].hex()}
        results.append(result)
        return status, data

    def check(lines, expected=None, reason=1, *, writes=(), reads=()):
        source = b"\xf9\xf7 540672\r" + lines + b"\r\xf9\xf8\r\0"
        if expected is not None:
            emu.erase_flash(1)
        stable = emu.memory(0x84000, 16384)
        status, data = compile_source(source, seconds=60, writes=writes, reads=reads)
        if expected is None:
            assert status == 2 and int.from_bytes(data[0][12:14], "little") == reason, lines
            assert data[1] == stable, "Rejected assembly modified Flash"
        else:
            assert status == 0 and int.from_bytes(data[0][8:12], "little") == 42, lines
            assert data[1][:len(expected)] == expected, lines
            assert data[1][len(expected):] == stable[len(expected):], "Assembly wrote outside its block"
        return data

    try:
        fixture = bytes.fromhex("2a0000011ffe")
        emu.erase_flash(1)
        emu.program_flash(0x84000, fixture)
        stable = emu.memory(0x84000, 16384)
        for source in (b"\xf9\xf7 540672\rMOV R0,42\rRET\r\xf9\xf8\r7\0",
                       b"\xf9\xf7 X\rBAD OPERANDS HERE\r\xf9\xf8\r\0"):
            status, data = compile_source(source, skip=True)
            assert status == 0 and data[1] == stable
            assert int.from_bytes(data[0][:4], "little") == 0x46000 + source.index(b"\xf9\xf8") + 2
        invalid = (
            (b"\xf9\xf7 540672\rMOV R16,0\rRET\r\xf9\xf8\r\0", 1),
            (b"\xf9\xf7 540672\rX:\rX:\rRET\r\xf9\xf8\r\0", 2),
            (b"\xf9\xf7 540672\rJMP MISSING\rRET\r\xf9\xf8\r\0", 3),
            (b"\xf9\xf7 540673\rRET\r\xf9\xf8\r\0", 5),
            (b"\xf9\xf7 1048574\rMOV R0,42\rRET\r\xf9\xf8\r\0", 5),
            (b"\xf9\xf7 540672\rRET\0", 6),
        )
        for source, reason in invalid:
            status, data = compile_source(source)
            assert status == 2 and int.from_bytes(data[0][12:14], "little") == reason
            assert data[1] == stable, "Rejected assembly modified Flash"
        source = b"\xf9\xf7 540672\rMOV R0,42\rMOV R1,0\rRET\r\xf9\xf8\r7\0"
        status, data = compile_source(source, seconds=60)
        assert status == 0 and int.from_bytes(data[0][8:12], "little") == 42
        assert data[1] == stable, "Unchanged assembly rewrote Flash"
        changed = source.replace(b"R0,42", b"R0,43")
        emu.erase_flash(1)
        stable = emu.memory(0x84000, 16384)
        status, data = compile_source(changed, seconds=60)
        assert status == 0 and int.from_bytes(data[0][8:12], "little") == 43
        assert data[1][:6] == bytes.fromhex("2b0000011ffe")
        assert data[1][6:] == stable[6:], "Assembly wrote outside its block"
        padding = (b"DB " + b",".join([b"0"] * 24) + b"\r") * 25
        check(b"JMP DONE\r" + padding + b"DONE:\rMOV ER0,42\rRET",
              bytes.fromhex("00f85c42") + bytes(600) + fixture)
        check(b"".join(f"L{n}:\r".encode() for n in range(40))
              + b" " * 96 + b"MOV ER0,#42\rRET", fixture)
        check(b"MOV ER0,#42\rRET\rDB 1", fixture + b"\x01")
        for count, reason in ((254, 0), (256, 4)):
            padding = b"\r".join(b"DB " + b",".join([b"0"] * min(24, count - n))
                                  for n in range(0, count, 24))
            lines = b"CMP R0,#0\rBEQ FORWARD\r" + padding + b"\rFORWARD: MOV ER0,#42\rRET"
            expected = bytes.fromhex("00707fc9") + bytes(count) + fixture
            check(lines, expected if not reason else None, reason)
        for count, reason in ((246, 0), (248, 4)):
            padding = b"\r".join(b"DB " + b",".join([b"0"] * min(24, count - n))
                                  for n in range(0, count, 24))
            lines = b"JMP CHECK\rBACK: MOV ER0,#42\rRET\r" + padding + b"\rCHECK: CMP R0,#0\rBEQ BACK\rRET"
            expected = bytes.fromhex("00f80041") + fixture + bytes(count) + bytes.fromhex("007080c91ffe")
            check(lines, expected if not reason else None, reason)

        lines = b'JMP DONE\rDATA: DB 0,"A;""B",255\rDW 0x1234,65535\rDONE: MOV ER0,#42\rRET'
        expected = bytes.fromhex("00f80e4000413b2242ff3412ffff") + fixture
        check(lines, expected)
        check(lines.replace(b"JMP DONE", b"JMP DONE+0"), expected)
        check(lines.replace(b"DW 0x1234,65535", b"DW DATA+2,DATA-4"),
              bytes.fromhex("00f80e4000413b2242ff06400040") + fixture)
        check(lines.replace(b"JMP DONE", b"JMP 0x400E"), expected)
        check(b"JMP DATA\rDATA: DW 0x002A,0x0100,0xFE1F",
              bytes.fromhex("00f80440") + fixture)
        check(b"JMP DATA+2\rDATA: DW 0,0x002A,0x0100,0xFE1F",
              bytes.fromhex("00f806400000") + fixture)
        check(b"JMP ENTRY\rDATA: DW 0xFE1F\rENTRY: MOV ER0,#42\rJMP DATA",
              bytes.fromhex("00f806401ffe2a00000100f80440"))
        check(b"JMP DONE\rCALL_SYS 0x10000\rCALL_SYS 0x84100\rDONE: MOV ER0,#42\rRET",
              bytes.fromhex("00f80c4001f1000001f80041") + fixture)
        check(b"JMP DONE\rCALL_SYS 0x20000\rCALL_SYS 0x70000\rDONE: MOV ER0,#42\rRET",
              bytes.fromhex("00f80c4001f2000001f70000") + fixture)
        for operand in (b"0x10001", b"0x100000"):
            check(b"CALL_SYS " + operand + b"\rRET")

        check(b"MOV ER0,#0\rADD ER0,#-64\rADD ER0,#63\rADD ER0,#43\rRET",
              bytes.fromhex("00000001c0e0bfe0abe01ffe"))
        check(b"ADD SP,#-128\rADD SP,#127\rADD SP,#1\rMOV ER0,#43\rADD ER0,#0x7F\rRET",
              bytes.fromhex("80e17fe101e12b000001ffe01ffe"))
        check(b"ADD SP,#0xFF\rADD SP,#1\rMOV ER0,#42\rRET",
              bytes.fromhex("ffe101e1") + fixture)
        for instruction, operands in (
            (b"ADD ER0,#", (b"-65", b"64", b"0x80")),
            (b"ADD SP,#", (b"-129", b"128", b"0x100")),
            (b"L R4,4:", (b"-32769[ER2]", b"32768[ER2]", b"0x10000[ER2]")),
        ):
            for operand in operands:
                check(instruction + operand + b"\rRET")
        check(b"JMP DONE\rL R4,4:-32768[ER2]\rL R4,4:0xFFFF[ER2]\rDONE: MOV ER0,#42\rRET",
              bytes.fromhex("00f8104004e32894008004e32894ffff") + fixture)

        check(b"PUSH LR\rPUSH EA\rPUSH XR4\rPUSH QR8\rPOP QR8\rPOP XR4\rPOP EA\rMOV ER0,#42\rPOP PC",
              bytes.fromhex("cef8cef16ef47ef83ef82ef48ef12a0000018ef2"))
        for instruction in (b"PUSH XR2", b"POP XR6", b"PUSH QR4", b"POP QR12", b"PUSH PC", b"POP PC,0"):
            check(instruction + b"\rRET")
        for instruction in (b'DW "A"', b"DB 256", b"DB -1", b'DB "A', b"DB 1,", b"DW 1,"):
            check(b"JMP DONE\r" + instruction + b"\rDONE: MOV ER0,#42\rRET")

        offset = buffer & 65535
        prefix = bytes((offset & 255, 2, offset >> 8, 3, 42, 6, 0, 7))
        for store, load, move, code, stored in (
            (b"R6", b"R4", b"R0,R4", "04e3219604e3209440801ffe", b"\x2a\xa5"),
            (b"ER6", b"ER4", b"ER0,ER4", "04e3239604e3229445f01ffe", b"\x2a\0"),
        ):
            lines = (f"MOV ER2,#{offset}\rMOV ER6,#42\r".encode()
                     + b"ST " + store + b",4:[ER2]\rL " + load + b",4:[ER2]\rMOV " + move + b"\rRET")
            data = check(lines, prefix + bytes.fromhex(code),
                         writes=[(buffer, b"\xa5\xa5")], reads=[(buffer, 2)])
            assert data[2] == stored, "Indirect store selected the wrong register"
        emu.erase_flash(4)
        source = (b"\xf9\xf7 606208\rJMP ENTRY\rDATA: DW 0xFE1F\r"
                  b"ENTRY: MOV ER0,#42\rJMP DATA\r\xf9\xf8\r\0")
        status, data = compile_source(source, seconds=60, reads=[(0x90000, 65536)])
        expected = bytes.fromhex("00f906401ffe2a00000100f90440")
        assert status == 0 and int.from_bytes(data[0][8:12], "little") == 42
        assert data[2] == b"\xff" * 0x4000 + expected + b"\xff" * (0xc000 - len(expected))
        return results
    finally:
        emu.erase_flash(1)
        emu.program_flash(0x84000, before)
        emu.erase_flash(4)
        emu.program_flash(0x90000, other)


def expression_cases(emu, out):
    results = []
    rom_byte = emu.memory(1, 1)[0]
    for title, source, value, error in (
        ("rom_peek", b"\xf9\xe0(1)", rom_byte, 0),
        ("address_above_20bit", b"\xf9\xe0(1048576)", emu.memory(0x100000, 1)[0], 0),
        ("address_24bit_last", b"\xf9\xe0(16777215)", emu.memory(0xffffff, 1)[0], 0),
        ("address_24bit_overflow", b"\xf9\xe0(16777216)", 0, 4),
        ("function_suffix", b"\xf9\xe0(1)\x892", rom_byte + 2, 0),
        ("nested_variable", b"\xf9\xe5(\xf9\xe0(A),255)", 65, 0),
        ("precedence", b"1\x892\xa9\xf9\xe5(\xf9\xe0(A),255)", 131, 0),
        ("native_nested", b"\x97\x87\xf9\xe5(\xf9\xe0(A),255))", 65, 0),
        ("band", b"\xf9\xe5(65535,255)", 255, 0),
        ("bor", b"\xf9\xe6(256,1)", 257, 0),
        ("bxor", b"\xf9\xe7(65535,255)", 65280, 0),
        ("shl", b"\xf9\xe8(32768,1)", 0, 0),
        ("shr", b"\xf9\xe9(32768,15)", 1, 0),
        ("inkey_released", b"\xf9\xea()", 0, 0),
        ("native_divide_zero", b"1\xb90", 0, 3),
        ("nested_divide_zero", b"\xf9\xe0(1\xb90)", 0, 3),
        ("first_argument_error", b"\xf9\xe5(1\xb90,255)", 0, 3),
        ("last_argument_error", b"\xf9\xe5(255,1\xb90)", 0, 3),
        ("fractional_address", b"\xf9\xe0(0.5)", 0, 4),
        ("missing_parenthesis", b"\xf9\xe0(1", 0, 2),
        ("too_many_arguments", b"\xf9\xe0(1,2)", 0, 2),
    ):
        registers, data = emu.evaluate(source, [(VARIABLE_A, scalar_integer(0x46100)), (0x46100, b"A")])
        expected = bytes((0xf0 | error,)) + bytes(19) if error else scalar_integer(value)
        record = {"case": title, "source": source.hex(), "registers": registers,
                  "number": data[0].hex(), "cursor": data[1].hex()}
        out.joinpath(title + ".json").write_text(json.dumps(record, indent=2), encoding="utf-8")
        assert registers["r0"] == int(not error) and data[0] == expected, record
        assert registers["sp"] == 0x8c00, title
        results.append(record)
    return results


def token_cases(emu, out):
    from basic_native import TOKEN_NAMES, TOKENS, FUNCTIONS

    emu.call("resume")
    existing = emu.records()
    name = next("NXLEX" + a + b for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                for b in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if "NXLEX" + a + b not in existing)
    emu.create(name)
    expected = bytearray()
    results = []
    for token in TOKEN_NAMES[:23]:
        emu.nx(token)
        expected.extend(TOKENS[token].to_bytes(2, "big"))
        if token in FUNCTIONS:
            emu.keys(0x33)
            expected.extend(b"()")
        else:
            expected.extend(b" ")
        emu.keys(0x63)
        expected.append(13)
        actual = bytes.fromhex(emu.records()[name]["source"])
        assert actual == expected + b"\0", (token, actual.hex(), expected.hex())
        results.append({"token": token, "stored_length": len(actual)})
    emu.nx("ASM")
    emu.keys(*(DIGITS[int(ch)] for ch in "540672"), 0x63)
    emu.keys(0x17, DIGITS[1], DIGITS[2], DIGITS[1])
    emu.keys(0x32, DIGITS[4], DIGITS[2], 0x63)
    emu.keys(0x17, DIGITS[1], 0x57, DIGITS[2], 0x57, 0x57, DIGITS[1], 0x63)
    emu.keys(0x17, DIGITS[4], DIGITS[3])
    expected.extend(b"\xf9\xf7 540672\rMOV R0,#42\rRET\r\xf9\xf8\r")
    assert bytes.fromhex(emu.records()[name]["source"]) == expected + b"\0"
    results.extend(({"token": "ASM"}, {"token": "ENDASM"}))
    emu.keys(0x26, 0x63)
    assert bytes.fromhex(emu.records()[name]["source"]) == expected + b"\0", "Editor reopen changed source"
    emu.evidence(out, "tokens-reopened")
    name = next("NXAT" + a + b for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                for b in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if "NXAT" + a + b not in existing)
    emu.create(name)
    emu.nx("PEEK")
    emu.keys(0x32)
    assert bytes.fromhex(emu.records()[name]["source"]) == b"\xf9\xe0\0"
    emu.keys(0x32)
    assert bytes.fromhex(emu.records()[name]["source"]) == b"\0"
    results.append({"case": "delete_whole_token"})
    emu.nx("CALL")
    emu.keys(0x27, 0x27, DIGITS[1], 0x57, 0x32)
    actual = bytes.fromhex(emu.records()[name]["source"])
    assert actual == b"1(\0", ("Token cursor edit", actual.hex())
    results.append({"case": "move_across_token_and_insert"})
    emu.keys(0x32, 0x57, 0x32)
    emu.nx("BAND")
    emu.keys(*(DIGITS[int(ch)] for ch in "65535"), 0x43,
             *(DIGITS[int(ch)] for ch in "255"), 0x33)
    emu.assign("A")
    emu.run()
    time.sleep(0.5)
    assert emu.memory(VARIABLE_A, 20) == scalar_integer(255)
    source = emu.records()[name]["source"]
    emu.keys(0x26, 0x17, DIGITS[2], LETTERS["R"], 0x63)
    assert name not in emu.records() and emu.records()["R" + name]["source"] == source
    results.append({"case": "rename_token_program", "name": "R" + name, "source": source})
    emu.evidence(out, "tokens-renamed")
    return results


def call_cases(emu, out):
    from basic_memory import MEMORY_ADDRESS

    emu.active()
    clobber = bytes.fromhex("000280035a04a50500e323948602800300e32394"
                           "a002800300e32394070400e31194a2802a0000011ffe")
    before = emu.memory(0x84000, 8192)
    other = emu.memory(0x90000, 65536)
    backup = emu.memory(0x86000, 8192)
    results = []
    try:
        registers, data = emu.evaluate(b"\xf9\xe4(26112)", seconds=60)
        assert registers["r0"] == 1 and data[0] == scalar_integer(1)
        assert registers["sp"] == 0x8c00
        results.append({"case": "rom_call", "address": 0x6600, "return": 1})
        registers, data = emu.evaluate(b"\xf9\xe4(20212,1)", seconds=60)
        assert registers["r0"] == 1 and emu.memory(0x84000, 8192) == b"\xff" * 8192
        assert registers["sp"] == 0x8c00
        results.append({"case": "rom_sector_erase_call", "number": data[0].hex()})
        emu.program_flash(0x84000, bytes.fromhex("26f046f066f01ffe"))
        for values, expected in (((), 0), ((1,), 1), ((1, 2), 3), ((1, 2, 3), 6), ((1, 2, 3, 4), 10)):
            source = b"\xf9\xe4(540672" + b"".join(b"," + str(x).encode() for x in values) + b")"
            registers, data = emu.evaluate(source, seconds=60)
            assert registers["r0"] == 1 and data[0] == scalar_integer(expected), (values, data)
            assert registers["sp"] == 0x8c00
            results.append({"args": values, "number": data[0].hex()})
        for bank in range(2, 8):
            target = bank << 16
            args = target.to_bytes(4, "little") + bytes(20)
            registers, _ = emu.invoke(
                MEMORY_ADDRESS, pair(0, 4) | pair(2, 0x8800) | pair(4, 0x8840),
                [(0x8800, args)], seconds=1, stop_at=target)
            results.append({"case": "unmapped_csr_call_target", "address": target,
                            "registers": registers})
        for source, error in ((b"\xf9\xe4(540673)", 4), (b"\xf9\xe4(1048576)", 4),
                              (b"\xf9\xe4(540672,1,2,3,4,5)", 2)):
            registers, data = emu.evaluate(source)
            assert registers["r0"] == 0 and data[0] == bytes((0xf0 | error,)) + bytes(19)
            results.append({"invalid": source.hex(), "number": data[0].hex()})
        counter = bytes.fromhex("8002400304e32090011004e3219000011ffe")
        emu.erase_flash(1)
        emu.program_flash(0x84000, counter)
        registers, data = emu.evaluate(b"\xf9\xe8(\xf9\xe4(540672),\xf9\xe4(540672))",
                                       [(0x44080, b"\x02")], seconds=60, reads=[(0x44080, 1)])
        assert registers["r0"] == 1 and data[0] == scalar_integer(48) and data[2] == b"\x04", data
        results.append({"case": "arguments_once_left_to_right", "result": 48, "counter": 4})
        emu.erase_flash(1)
        emu.program_flash(0x84000, clobber)
        math = bytes(range(112))
        fonts = b"\x07\0\x01"
        status, data, _ = emu.dispatch(MEMORY_ADDRESS, 4, [0x84000],
                                       [(0x8000, math), (0x8086, b"\x34\x12"), (0x80a0, fonts)],
                                       [(0x8000, 112), (0x8086, 2), (0x80a0, 3)])
        assert status == 0 and data == [(42).to_bytes(4, "little"), math, b"\x34\x12", fonts]
        results.append({"case": "math_workspace_fonts_restored", "return": 42})
        emu.erase_flash(4)
        fixture = bytes.fromhex("2a0000011ffe")
        emu.program_flash(0x92000, fixture)
        emu.program_flash(0x85ff0, fixture)
        stable = emu.memory(0x84000, 8192)
        for address in (0x92000, 0x85ff0):
            registers, data = emu.evaluate(b"\xf9\xe4(" + str(address).encode() + b")", seconds=60)
            assert registers["r0"] == 1 and data[0] == scalar_integer(42)
            assert registers["sp"] == 0x8c00
            assert emu.memory(0x84000, 8192) == stable and emu.memory(0x86000, 8192) == backup
            results.append({"case": "call_without_recovery", "address": address, "return": 42})
    finally:
        emu.erase_flash(1)
        emu.program_flash(0x84000, before)
        emu.erase_flash(4)
        emu.program_flash(0x90000, other)
    return results


def regression_cases(emu, out):
    emu.call("resume")
    existing = emu.records()
    fixture = next("NXHEX" + a + b for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                   for b in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if "NXHEX" + a + b not in existing)
    emu.create(fixture)
    emu.keys(*((DIGITS[4], DIGITS[2], 0x63) * 4), 0x26)
    emu.keys(0x70, 0x26, 0x26, 0x26, 0x70)
    for keys in ((0x07, 0x42), (0x07, 0x11), (0x52,), (0x06,), (0x57,)):
        emu.keys(*keys)
        time.sleep(0.5)
    results = []

    def page():
        deadline = time.monotonic() + 5
        while emu.call("get_status")["run_status"] != 0:
            if time.monotonic() >= deadline:
                raise AssertionError(("Hex did not finish drawing", emu.registers()))
            time.sleep(0.02)
        emu.call("pause")
        registers = emu.registers()
        emu.call("resume")
        return registers["r12"] | registers["r13"] << 8

    entry = page()
    assert entry == 0x4000, (entry, emu.evidence(out, "hex-entry-failure"))
    emu.keys(0x47, 0x47, 0x47, 0x47)
    assert page() == 0x4020, "Four downward moves did not cross the Hex page"
    results.append(emu.evidence(out, "hex-page"))
    emu.call("keyboard_code", code=0x47, pressed=True)
    try:
        time.sleep(2)
    finally:
        emu.call("keyboard_code", code=0x47, pressed=False)
    time.sleep(0.4)
    assert page() > 0x4020, "Held DOWN did not repeat across a page"
    results.append(emu.evidence(out, "hex-held-down"))

    def goto(kind, digits):
        keys = []
        for ch in digits:
            keys.extend((DIGITS[int(ch)],) if ch.isdigit() else (0x16, LETTERS[ch]))
        emu.keys(0x06, 0x17, DIGITS[kind], *keys, 0x63)

    goto(3, "8000")
    assert page() == 0x8000
    results.append(emu.evidence(out, "hex-ram"))
    records = emu.records()
    address = 0x40000 + records[fixture]["payload"] + 6
    before = emu.memory(address, 8)
    try:
        goto(2, f"{address & 65535:04X}")
        assert page() == (address & 0xffe0)
        emu.keys(0x63, DIGITS[4], DIGITS[1], 0x63)
        assert emu.memory(address, 8) == b"A" + before[1:], "Hex nibble edit changed adjacent bytes"
        results.append(emu.evidence(out, "hex-sram-write"))
    finally:
        emu.call("write_memory", address=address, bytes=list(before))
    goto(1, "84000")
    assert page() == 0x4000
    results.append(emu.evidence(out, "hex-flash"))
    emu.keys(0x26, 0x26, 0x70, 0x07, 0x42, 0x06, 0x70)
    # The logo is drawn before ROM 0:578E finishes saving SRAM to Flash.
    deadline = time.monotonic() + 60
    while emu.call("get_status")["run_status"] != 0:
        if time.monotonic() >= deadline:
            raise AssertionError(("Native OFF did not finish", emu.registers()))
        time.sleep(0.05)
    lcd = emu.memory(0xf800, 512)
    from shutdown_logo import read_logo
    assert b"".join(lcd[y * 16:y * 16 + 12] for y in range(32)) == read_logo()
    results.append(emu.evidence(out, "off-signature"))
    emu.call("reset")
    emu.call("resume")
    time.sleep(1)
    emu.keys(0x70)
    after = emu.records()
    out.joinpath("off-programs.json").write_text(
        json.dumps({"before": records, "after": after}, indent=2), encoding="utf-8")
    expected = {name: record["source"] for name, record in records.items()}
    actual = {name: record["source"] for name, record in after.items()}
    assert actual == expected, ("OFF changed program sources",
                               sorted(name for name in actual.keys() | expected.keys()
                                      if actual.get(name) != expected.get(name)))
    return results


def control_cases(emu, out):
    from basic_smoke_native import native_cases

    emu.active()
    before = emu.memory(0x84000, 8192)
    try:
        emu.erase_flash(1)
        emu.program_flash(0x84000, bytes.fromhex("2a0000011ffe"))
        return native_cases(emu, out)
    finally:
        emu.erase_flash(1)
        emu.program_flash(0x84000, before)


def main():
    # Create keyboard-driven fixtures before probes take over the CPU return path.
    cases = {"native": native, "tokens": token_cases, "control": control_cases,
             "regression": regression_cases, "asm": asm_cases,
             "expressions": expression_cases, "codec": codec, "memory": memory_cases,
             "call": call_cases, "graphics": graphics_cases, "flash": flash_cases}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=(*cases, "all"), required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error("Choose a new evidence directory")
    emu = Emulator(args.model)
    args.out.mkdir(parents=True)
    emu.call("reset")
    emu.call("resume")
    time.sleep(1)
    snapshot = emu.call("save_snapshot", label="Before BASIC smoke")["id"]
    flash = b"".join(emu.memory(0x80000 + offset, 32768)
                     for offset in range(0, 524288, 32768))
    args.out.joinpath("before-flash.bin").write_bytes(flash)
    try:
        results = {}
        for name in cases if args.case == "all" else (args.case,):
            destination = args.out / name if args.case == "all" else args.out
            destination.mkdir(exist_ok=True)
            result = cases[name](emu, destination)
            destination.joinpath("cases.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
            results[name] = len(result)
            print(f"PASS {name}: {len(result)} scenarios", flush=True)
        args.out.joinpath("result.json").write_text(json.dumps({
            "case": args.case, "passed": sum(results.values()), "cases": results,
            "model": str(emu.model), "rom_sha256": ROM_SHA256,
            "flash_sha256": hashlib.sha256(emu.model.joinpath("flash.bin").read_bytes()).hexdigest(),
        }, indent=2), encoding="utf-8")
    finally:
        try:
            emu.call("clear_execution_breakpoints")
            emu.call("clear_memory_breakpoints")
            # Native OFF can also update snapshot sectors, independently of raw fixtures.
            for sector, start, stop in ((1, 0x4000, 0x6000), (2, 0x6000, 0x8000),
                                         (3, 0x8000, 0x10000), (4, 0x10000, 0x20000),
                                         (5, 0x20000, 0x30000), (6, 0x30000, 0x40000)):
                if emu.memory(0x80000 + start, stop - start) != flash[start:stop]:
                    emu.erase_flash(sector)
                    emu.program_flash(0x80000 + start, flash[start:stop])
            assert b"".join(emu.memory(0x80000 + offset, 32768)
                            for offset in range(0, 524288, 32768)) == flash, "Flash fixture restoration failed"
        finally:
            emu.call("load_snapshot", id=snapshot)
            emu.session.close()


if __name__ == "__main__":
    main()
