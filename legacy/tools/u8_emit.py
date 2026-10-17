"""Encode the nX-U8 instructions used by the fx-5800P Flash patches."""

LABELS = {}


class Code:
    def __init__(self, address):
        self.address = address
        self.data = bytearray()
        self.labels = {}
        self.fixups = []

    def label(self, name):
        if name in self.labels:
            raise ValueError(f"Duplicate label: {name}")
        self.labels[name] = self.address + len(self.data)

    def raw(self, hex_bytes):
        self.data.extend(bytes.fromhex(hex_bytes))

    def db(self, *values):
        self.data.extend(values)

    def word(self, value):
        self.data.extend((value & 255, (value >> 8) & 255))

    def mov(self, register, value):
        if not 0 <= register < 16 or not 0 <= value < 256:
            raise ValueError((register, value))
        self.db(value, register)

    def mov_er(self, register, value):
        if register not in range(0, 16, 2) or not 0 <= value < 65536:
            raise ValueError((register, value))
        if value <= 63:
            self.db(value, 0xe0 | register)
        else:
            self.mov(register, value & 255)
            self.mov(register + 1, value >> 8)

    def call(self, address):
        self._far(1, address)

    def jump(self, address):
        self._far(0, address)

    def _far(self, opcode, address):
        if isinstance(address, str):
            self.fixups.append((len(self.data) + 2, "far", address))
            address = self.address
        if address & 1 or not 0 <= address < 0x100000:
            raise ValueError(address)
        self.db(opcode, 0xf0 | (address >> 16), address & 255, (address >> 8) & 255)

    def branch(self, condition, label):
        codes = {"eq": 0xc9, "ne": 0xc8, "lt": 0xc1, "ge": 0xc0, "al": 0xce}
        if condition not in codes:
            raise ValueError(condition)
        self.fixups.append((len(self.data), "relative", label))
        self.db(0, codes[condition])

    def build(self):
        data = bytearray(self.data)
        for pos, kind, label in self.fixups:
            target = self.labels[label]
            if kind == "far":
                data[pos:pos + 2] = (target & 255, (target >> 8) & 255)
                data[pos - 1] = 0xf0 | (target >> 16)
            else:
                delta = target - (self.address + pos + 2)
                if delta & 1 or not -256 <= delta <= 254:
                    raise ValueError(f"Branch to {label} out of range: {delta}")
                data[pos] = (delta // 2) & 255
        LABELS[self.address] = dict(self.labels)
        return bytes(data)
