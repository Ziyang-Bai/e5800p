"""Replace the native OFF bitmap while retaining screen save and AC wake."""

from pathlib import Path

from u8_emit import Code

SAVE_ENTRY = 0xcfa66
SAVE_PROLOGUE = bytes.fromhex('ce f8 5e f8')
from flash_layout import LOGO_ADDRESS, LOGO_BITMAP_ADDRESS


def read_logo():
    path = Path(__file__).resolve().parents[1] / 'assets' / 'ziyang_bai.pbm'
    words = path.read_text(encoding='ascii').split()
    if words[:3] != ['P1', '96', '32'] or len(words) != 3075 or any(p not in ('0', '1') for p in words[3:]):
        raise ValueError('Expected a 96x32 plain PBM logo')
    pixels = words[3:]
    return bytes(int(''.join(pixels[i:i + 8]), 2) for i in range(0, len(pixels), 8))


def logo_code(bitmap):
    if len(bitmap) != 384:
        raise ValueError('Shutdown bitmap must contain 96x32 packed pixels')
    c = Code(LOGO_ADDRESS)
    c.raw('ce f8 6e f0')  # Saved caller LR:CSR follows the four argument bytes.
    c.raw('1a a2 84 e2 22 90')
    c.raw('d6 70 59 51')  # Native OFF returns from screen save to ROM 0:59D6.
    c.branch('ne', 'ordinary')
    c.raw('82 e2 22 90 05 f0')
    c.branch('ne', 'ordinary')
    c.raw('2e f0')
    c.call('save')
    c.call(0x1210a)
    c.raw('6e f4')
    c.mov_er(2, LOGO_BITMAP_ADDRESS & 0xffff)
    c.mov_er(4, 0x80e0)
    c.mov_er(6, len(bitmap))
    c.label('copy')
    c.db(LOGO_BITMAP_ADDRESS >> 16, 0xe3)
    c.raw('20 90 41 90 81 e2 81 e4 ff e6')
    c.branch('ne', 'copy')
    c.raw('2e f4')
    c.call(0x043be)
    c.raw('8e f8')
    c.jump(0x059f6)  # Continue with native key release, STOP and wake restoration.
    c.label('ordinary')
    c.raw('2e f0 8e f8')
    c.label('save')
    c.data.extend(SAVE_PROLOGUE)
    c.jump(SAVE_ENTRY + len(SAVE_PROLOGUE))
    code = c.build()
    return ((LOGO_ADDRESS - 0x80000, code),
            (LOGO_BITMAP_ADDRESS - 0x80000, bitmap))
