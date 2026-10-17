"""Route MODE 5:PROG to the original program mode or the nX-U8 ASM editor."""

from program_mode import PROGRAM_ADDRESS
from u8_emit import Code

from flash_layout import SELECTOR_ADDRESS, SCANNER_ADDRESS
from ui_text import text_copy
PROG_ENTRY = 0x4a05a
PROG_RESUME = 0xca05e
ORIGINAL_PROLOGUE = bytes.fromhex("ce f8 5e fe")


def selector_code():
    c = Code(SELECTOR_ADDRESS)

    def ptr(offset):
        c.raw("e5 f2")  # ER2 = ER14
        if offset:
            c.mov_er(10, offset)
            c.raw("a6 f2")

    def save_font():
        c.raw("10 90 a0 80")  # ROM font height
        ptr(24)
        c.raw("21 90")
        c.raw("10 90 a2 80")  # ROM font width
        ptr(25)
        c.raw("21 90")
        c.mov(0, 7)
        c.raw("11 90 a0 80")
        c.mov(0, 1)
        c.raw("11 90 a2 80")

    def restore_font():
        ptr(25)
        c.raw("20 90 11 90 a2 80")
        ptr(24)
        c.raw("20 90 11 90 a0 80")

    def line(text, y):
        ptr(0)
        text_copy(c, text, 24)
        ptr(0)
        c.mov(0, 0)
        c.mov(1, y)
        c.call(0x041da)

    c.label("entry")
    c.raw(ORIGINAL_PROLOGUE.hex(" "))
    c.raw("e0 e1 1a ae")  # 32-byte line buffer; ER14=SP
    save_font()
    c.label("draw")
    c.call(0x0409a)
    line("PROGRAM", 1)
    line("1:PROG", 9)
    line("2:ASM", 17)
    c.call(0x043be)
    c.label("key")
    c.call(SCANNER_ADDRESS)
    c.raw("31 70")
    c.branch("eq", "prog")
    c.raw("32 70")
    c.branch("eq", "asm")
    c.raw("fa 70")
    c.branch("ne", "key")
    restore_font()
    c.mov(0, 0x81)
    c.raw("11 90 91 80")  # Return to native COMP dispatch on EXIT.
    c.raw("20 e1 1e fe 8e f8 1f fe")
    c.label("prog")
    restore_font()
    c.raw("20 e1")  # Discard selector frame; keep native PROG prologue pushes.
    c.jump(PROG_RESUME)
    c.label("asm")
    c.mov_er(12, 0x4000)
    c.mov(5, 0)
    c.call(PROGRAM_ADDRESS)
    c.jump("draw")
    return (SELECTOR_ADDRESS - 0x80000, c.build())
