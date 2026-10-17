"""Copy NUL-terminated bank-F UI constants to an existing near line buffer."""

from flash_layout import UI_STRINGS_ADDRESS, UI_TEXT_ADDRESS
from u8_emit import Code

DATA_SPANS = []


class TextPool:
    def __init__(self, address=None):
        self.address = address
        self.data = bytearray()
        self.strings = {}
        self.fixups = []

    def copy(self, c, text, capacity):
        value = text.encode('ascii') + b'\0'
        if len(value) > capacity:
            raise ValueError(f'UI text exceeds its buffer: {text!r}')
        if value not in self.strings:
            self.strings[value] = len(self.data)
            self.data.extend(value)
        offset = self.strings[value]
        c.raw('5e f6 25 f0')  # Preserve the caller's ER6; ER0 = destination ER2.
        pos = len(c.data)
        c.mov(2, 0)
        c.mov(3, 0)
        if self.address is None:
            self.fixups.append((c, pos, offset))
        else:
            c.data[pos] = (self.address + offset) & 255
            c.data[pos + 2] = ((self.address + offset) >> 8) & 255
        c.mov_er(6, capacity)
        c.call(UI_TEXT_ADDRESS)
        c.raw('1e f6')

    def finish(self, c):
        if self.address is not None:
            raise ValueError('Fixed UI pool must be emitted separately')
        if c.address >> 16 != 15:
            raise ValueError('UI constants must be in bank F')
        if len(c.data) & 1:
            c.db(0xff)
        address = c.address + len(c.data)
        if (address & 0xffff) + len(self.data) > 0x10000:
            raise ValueError('UI constants cross bank F')
        for emitter, pos, offset in self.fixups:
            emitter.data[pos] = (address + offset) & 255
            emitter.data[pos + 2] = ((address + offset) >> 8) & 255
        DATA_SPANS.append((address, len(self.data)))
        c.data.extend(self.data)


TEXT = TextPool(UI_STRINGS_ADDRESS)


def text_copy(c, text, capacity):
    TEXT.copy(c, text, capacity)


def ui_text_code():
    # ER0=near destination, ER2=bank-F source, ER6=capacity including NUL.
    # Return length or FFFF; preserve XR4 and R8..15.
    c = Code(UI_TEXT_ADDRESS)
    c.raw('6e f4 6e f8 05 f4 65 f8')
    c.mov_er(6, 0)
    c.label('next')
    c.raw('85 f8')
    c.branch('eq', 'fail')
    c.raw('ff e8 0f e3 20 90')
    c.raw('00 70')
    c.branch('eq', 'nul')
    c.raw('85 f8')
    c.branch('eq', 'truncate')
    c.raw('41 90 81 e4 81 e2 81 e6')
    c.branch('al', 'next')
    c.label('truncate')
    c.mov(0, 0)
    c.raw('41 90')
    c.label('fail')
    c.mov_er(0, 0xffff)
    c.branch('al', 'done')
    c.label('nul')
    c.raw('41 90 65 f0')
    c.label('done')
    c.raw('2e f8 2e f4 1f fe')
    return ((UI_TEXT_ADDRESS - 0x80000, c.build()),
            (UI_STRINGS_ADDRESS - 0x80000, bytes(TEXT.data)))
