"""Native PROGRAM control flow and runtime smoke cases for the isolated model."""

import time

from basic_native import TOKENS, VARIABLE_A
from basic_smoke import DIGITS, LETTERS, scalar_integer


def native_cases(emu, out):
    from basic_smoke_apps import _idle

    results = []
    existing = emu.records()
    flash = emu.memory(0x84000, 0x4000)
    assert flash[:6] == bytes.fromhex("2a 00 00 01 1f fe"), "Install the verified S1 return-42 fixture first"
    emu.call("resume")

    def create(prefix):
        names = emu.records()
        name = next(prefix + a + b for a in LETTERS for b in LETTERS
                    if prefix + a + b not in names)
        emu.create(name)
        emu.nx("ASM")
        emu.keys(*(DIGITS[int(ch)] for ch in "540672"), 0x63)
        for _ in range(12):
            emu.keys(0x17, DIGITS[1], DIGITS[2], DIGITS[1], 0x63)
        emu.keys(0x17, DIGITS[4], DIGITS[3], 0x26)
        return name

    def source(name, data):
        record = emu.records()[name]
        capacity = int.from_bytes(bytes.fromhex(record["record"])[16:20], "little") - 6
        data += b"\0"
        assert len(data) <= capacity, (name, len(data), capacity)
        address = 0x40000 + record["payload"]
        emu.call("write_memory", address=address + 6, bytes=list(data))
        emu.call("write_memory", address=address + 2, bytes=list(len(data).to_bytes(4, "little")))

    def run(data):
        emu.keys(0x26, 0x26, 0x26, 0x70)
        source(parent, data)
        for address in (VARIABLE_A, VARIABLE_A + 20):
            emu.call("write_memory", address=address, bytes=list(scalar_integer(99)))
        emu.keys(0x07, DIGITS[1], 0x07, DIGITS[5], DIGITS[1], DIGITS[2])
        index = list(emu.records()).index(parent)
        for code in (*([0x47] * index), 0x63):
            _idle(emu)
            emu.call("resume")
            emu.keys(code)

    def wait_value(address, value, finished=False):
        deadline = time.monotonic() + 20
        expected = scalar_integer(value)
        while True:
            actual = emu.memory(address, 20)
            status = emu.call("get_status")
            if actual == expected and (not finished or status["run_status"] == 0):
                return
            if time.monotonic() >= deadline:
                raise AssertionError(("Native PROGRAM did not reach result", value, actual.hex(), status))
            time.sleep(0.05)

    def unchanged():
        assert emu.memory(0x84000, 0x4000) == flash, "Native case changed S1/S2"

    def record(title, **values):
        unchanged()
        result = emu.evidence(out, "control-" + title)
        result.update(case=title, **values)
        results.append(result)

    def stop():
        emu.keys(0x70, 0x26)

    def token(name):
        return TOKENS[name].to_bytes(2, "big")

    parent = create("NXCTRL")
    child = create("NXCHLD")
    child_source = bytes.fromhex(emu.records()[child]["source"])
    block = b"\xf9\xf7 540672\rMOV ER0,#42\rRET\r\xf9\xf8\r"
    opaque = b'"\xf9\xf7\xf9\xf8"\r\x27\xf9\xf7\xf9\xf8\r'
    opaque += b"\xf9\xf7 540672\rNOT AN OPCODE\r\xf9\xf8\r"
    tail = b"9\x0eB\r"
    try:
        for title, data, a in (
            ("if_false", b"\xf7\x000\r\xf7\x01\r" + opaque + b"\xf7\x02\r7\x0eA\r\xf7\x03\r", 7),
            ("else_skip", b"\xf7\x001\r\xf7\x01\r1\x0eA\r\xf7\x02\r" + opaque + b"\xf7\x03\r", 1),
            ("for_empty", b"\xf7\x043\x0eI\xf7\x051\r" + opaque + b"\xf7\x07\r", 99),
            ("while_false", b"\xf7\x080\r" + opaque + b"\xf7\x09\r", 99),
            ("break_for", b"\xf7\x041\x0eI\xf7\x053\r\xf7\x0d\r" + opaque + b"\xf7\x07\r", 99),
            ("break_while", b"\xf7\x081\r\xf7\x0d\r" + opaque + b"\xf7\x09\r", 99),
            ("goto", b"\xec1\r" + opaque + b"\xe21\r", 99),
        ):
            run(data + tail)
            wait_value(VARIABLE_A + 20, 9, finished=True)
            assert emu.memory(VARIABLE_A, 20) == scalar_integer(a), title
            record(title, expected_a=a, expected_b=9)

        run(b"\xf7\x001\r\xf7\x01\r" + block + b"\xc0\x0eA\r\xf7\x03\r" + tail)
        wait_value(VARIABLE_A + 20, 9, finished=True)
        assert emu.memory(VARIABLE_A, 20) == scalar_integer(42), "True branch did not execute ASM"
        record("if_true", expected_a=42, expected_b=9)

        run(b"0\x0eB\r\xf7\x041\x0eI\xf7\x053\r" + block + b"B\x891\x0eB\r\xf7\x07\r")
        wait_value(VARIABLE_A + 20, 3, finished=True)
        assert emu.memory(VARIABLE_A, 20) == scalar_integer(99), "ASM loop changed A"
        record("for_asm", expected_a=99, expected_b=3)

        source(child, block + b"\xc0\x0eA\r")
        run(b'\xed"' + child.encode("ascii") + b'"\rA\x891\x0eB\r')
        wait_value(VARIABLE_A + 20, 43, finished=True)
        assert emu.memory(VARIABLE_A, 20) == scalar_integer(42), "Child PROGRAM did not execute ASM"
        record("nested_prog", expected_a=42, expected_b=43, child=child)

        scratch = 0x40000 + emu.records()[child]["payload"] + 6
        saved = emu.memory(scratch, 12)
        try:
            address = str(scratch).encode("ascii")
            odd = str(scratch + 1).encode("ascii")
            data = token("FILL") + b" " + address + b",8,85\r"
            data += token("POKE") + b" " + address + b",65\r"
            data += token("POKE16") + b" " + odd + b",4660\r"
            data += token("PEEK") + b"(" + address + b")\x0eA\r"
            data += token("PEEK16") + b"(" + odd + b")\x0eB\r"
            run(data)
            wait_value(VARIABLE_A + 20, 4660, finished=True)
            assert emu.memory(VARIABLE_A, 20) == scalar_integer(65), "Native PEEK result"
            actual = emu.memory(scratch, 12)
            assert actual == bytes.fromhex("41 34 12 55 55 55 55 55") + saved[8:], actual.hex()
            record("owned_memory", expected_a=65, expected_b=4660, bytes=actual.hex())
        finally:
            stop()
            scratch = 0x40000 + emu.records()[child]["payload"] + 6
            emu.call("write_memory", address=scratch, bytes=list(saved))

        try:
            run(b"\xf7\x081\r" + token("INKEY") + b"()\x0eA\r\xf7\x09\r")
            wait_value(VARIABLE_A, 0)
            samples = []
            for code, value in ((0x42, 67), (0x06, 7)):
                emu.call("keyboard_code", code=code, pressed=True)
                try:
                    wait_value(VARIABLE_A, value)
                    for _ in range(3):
                        time.sleep(0.15)
                        actual = emu.memory(VARIABLE_A, 20)
                        assert actual == scalar_integer(value), (code, actual.hex())
                    samples.append({"key": code, "value": value, "held_samples": 3})
                finally:
                    emu.call("keyboard_code", code=code, pressed=False)
                wait_value(VARIABLE_A, 0)
            record("inkey", samples=samples, released=0)
        finally:
            stop()

        try:
            run(b"\xf7\x081\r" + token("TICKS") + b"()\x0eA\r\xf7\x09\r")
            scalars = {scalar_integer(value): value for value in range(256)}
            samples = []
            high = False
            deadline = time.monotonic() + 20
            while True:
                actual = emu.memory(VARIABLE_A, 20)
                assert actual in scalars, ("TICKS outside uint8", actual.hex())
                value = scalars[actual]
                samples.append(value)
                if high and value < 50:
                    break
                high |= value >= 200
                if time.monotonic() >= deadline:
                    raise AssertionError(("TICKS did not wrap", samples))
                time.sleep(0.03)
            record("ticks", samples=samples)
        finally:
            stop()

        scratch = 0x40000 + emu.records()[child]["payload"] + 6
        saved = emu.memory(scratch, 12)
        try:
            data = token("COPY") + b" " + str(scratch).encode("ascii") + b",32992,12\r"
            data += token("CLS") + b"\r" + token("PSET") + b" 0,0,1\r"
            data += token("LINE") + b" 0,15,95,15,1\r"
            data += token("RECT") + b" 0,17,95,30,1\r"
            data += token("TEXT") + b' 0,2,"BASIC",0\r'
            data += token("TEXT") + b' 24,18,"NX",1\r'
            data += token("REFRESH") + b"\r1\x0eA\r\xf7\x081\r\xf7\x09\r"
            run(data)
            wait_value(VARIABLE_A, 1)
            frame = emu.memory(0x80e0, 384)
            assert frame[:12] == emu.memory(scratch, 12), "BASIC graphics changed status row"
            assert frame[12:24] == b"\x80" + bytes(11), "PSET/CLS top row"
            for y in (15, 17, 30):
                assert frame[(y + 1) * 12:(y + 2) * 12] == b"\xff" * 12, ("Missing horizontal edge", y)
            for y in range(18, 30):
                assert frame[(y + 1) * 12] & 0x80 and frame[(y + 2) * 12 - 1] & 1, ("Missing rectangle edge", y)
            record("graphics", status_row=frame[:12].hex())
        finally:
            stop()
            scratch = 0x40000 + emu.records()[child]["payload"] + 6
            emu.call("write_memory", address=scratch, bytes=list(saved))
    finally:
        stop()
        source(child, child_source[:-1])
        current = emu.records()
        for name, old in existing.items():
            assert current[name]["source"] == old["source"], ("Existing PROGRAM changed", name)
        unchanged()
    return results
