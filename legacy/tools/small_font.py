"""Draw 3x5 uppercase ASCII using ROM glyphs and Flash supplements.

R0=x (multiple of four), R1=y (1..27), ER2=NUL-terminated segment-zero
string. Draws into 80E0 with four-pixel cells; XR4 and R8..R15 preserved.
"""

from u8_emit import Code

from flash_layout import SMALL_TEXT_ADDRESS, SMALL_TABLE_ADDRESS, SMALL_GLYPHS_ADDRESS

# Five rows, each using bits 6..4 like the native compact glyphs.
_EXTRA = {
    '!': (2, 2, 2, 0, 2), '"': (5, 5, 0, 0, 0),
    '#': (2, 7, 2, 7, 2), '$': (3, 6, 3, 6, 2),
    '%': (5, 1, 2, 4, 5), '&': (2, 5, 2, 5, 3),
    "'": (2, 2, 0, 0, 0),
    ':': (0, 2, 0, 2, 0), ';': (0, 2, 0, 2, 4),
    '<': (1, 2, 4, 2, 1), '=': (0, 7, 0, 7, 0),
    '>': (4, 2, 1, 2, 4), '?': (6, 1, 2, 0, 2),
    '@': (7, 5, 7, 4, 7),
    'G': (7, 4, 5, 5, 7), 'H': (5, 5, 7, 5, 5),
    'I': (7, 2, 2, 2, 7), 'J': (3, 1, 1, 5, 2),
    'K': (5, 5, 6, 5, 5), 'L': (4, 4, 4, 4, 7),
    'M': (5, 7, 7, 5, 5), 'N': (5, 7, 7, 7, 5),
    'P': (6, 5, 6, 4, 4), 'S': (7, 4, 7, 1, 7),
    'T': (7, 2, 2, 2, 2), 'U': (5, 5, 5, 5, 7),
    'V': (5, 5, 5, 5, 2), 'W': (5, 5, 7, 7, 5),
    'Z': (7, 1, 2, 4, 7),
    '[': (6, 4, 4, 4, 6), '\\': (4, 4, 2, 1, 1),
    ']': (3, 1, 1, 1, 3), '^': (2, 5, 0, 0, 0),
    '_': (0, 0, 0, 0, 7),
}


def small_font_code():
    c = Code(SMALL_TEXT_ADDRESS)
    c.raw('ce f8 6e f4 7e f8 05 f8 25 fa')
    c.raw('90 80')
    c.mov(1, 12)
    c.raw('14 f0')
    c.mov_er(12, 0x80e0)
    c.raw('06 fc 80 80 3c 90 00 01 06 fc')
    c.label('char')
    c.db(96, 0x78)
    c.branch('ge', 'done')
    c.raw('a0 90 00 70')
    c.branch('eq', 'done')
    c.db(32, 0x70)
    c.branch('lt', 'unknown')
    c.db(96, 0x70)
    c.branch('lt', 'lookup')
    c.label('unknown')
    c.mov(0, ord('?'))
    c.label('lookup')
    c.raw('e0 10 1a 90 00 01')  # Two-byte glyph pointer per ASCII code.
    c.mov_er(2, SMALL_TABLE_ADDRESS & 0xffff)
    c.raw('06 f2')
    c.db(SMALL_TABLE_ADDRESS >> 16, 0xe3, 0x22, 0x9e)
    c.raw('80 84 04 24')
    c.mov(6, 5)
    c.label('row')
    c.db(0x71, 0xaf)  # Bit 15 distinguishes Flash supplement pointers from ROM.
    c.branch('eq', 'rom')
    c.db(SMALL_GLYPHS_ADDRESS >> 16, 0xe3, 0xe0, 0x90)
    c.branch('al', 'shift')
    c.label('rom')
    c.raw('e0 90')
    c.label('shift')
    c.raw('70 20 00 74')
    c.branch('eq', 'high')
    c.raw('4c 90 c0 91 f0 21')
    c.branch('al', 'store')
    c.label('high')
    c.raw('c0 91 0f 21')
    c.label('store')
    c.raw('13 80 c1 90 81 ee 8c ec ff 16')
    c.branch('ne', 'row')
    c.raw('c4 ec 00 74')  # Return to the line, then advance after the low nibble.
    c.branch('eq', 'next')
    c.raw('81 ec')
    c.label('next')
    c.raw('04 18 81 ea')
    c.branch('al', 'char')
    c.label('done')
    c.raw('3e f8 2e f4 8e f2')

    table = bytearray()
    glyphs = bytearray()
    for code in range(32, 96):
        ch = chr(code)
        if ch in _EXTRA:
            ptr = (SMALL_GLYPHS_ADDRESS + len(glyphs)) & 0xffff
            glyphs.extend(row << 4 for row in _EXTRA[ch])
        else:
            if code == 32:
                index = 0
            elif 0x28 <= code <= 0x39:
                index = code - 0x27
            elif 0x41 <= code <= 0x46:
                index = code - 0x2e
            elif 0x4f <= code <= 0x52:
                index = code - 0x36
            elif 0x58 <= code <= 0x59:
                index = code - 0x3b
            else:
                raise ValueError(f'Missing compact glyph: {ch!r}')
            ptr = 0x3f2e + 5 * index
        table.extend(ptr.to_bytes(2, 'little'))
    code = c.build()
    if len(code) > 0x100:
        raise ValueError('Compact renderer exceeds its allocation')
    if SMALL_GLYPHS_ADDRESS & 0x8000 == 0 or len(glyphs) > 0xb0:
        raise ValueError('Compact glyph pointers lose the Flash discriminator')
    return ((SMALL_TEXT_ADDRESS - 0x80000, code),
            (SMALL_TABLE_ADDRESS - 0x80000, bytes(table)),
            (SMALL_GLYPHS_ADDRESS - 0x80000, bytes(glyphs)))
