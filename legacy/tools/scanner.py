# SPDX-License-Identifier: GPL-3.0-only
"""Adapt native logical keyboard events to the ASM/Hex UI key codes."""

from flash_layout import SCANNER_ADDRESS
from u8_emit import Code


def scanner_code():
    """Return ER0=event; R0=FA..FF for cancel/EXE/left/right/down/up.

    No arguments. R1 remains 75h for translated navigation events; other
    native event words pass through, including FUNCTION (7D02h), DEL (7549h)
    and ASCII (R1=0). R0-R3 and flags are scratch; R4-R15 and SP are preserved.
    Native scanning owns SHIFT/ALPHA state, key repeat, idle and wake handling.
    """
    c = Code(SCANNER_ADDRESS)
    c.raw("ce f8 fe e1")  # PUSH LR; reserve a two-byte native event cell.
    c.raw("1a a0")  # ER0 = SP
    c.call(0x1234e)  # Blocking logical scan; writes the event through ER0.
    c.raw("1a a0")
    c.call(0x1249c)  # Normalize shifted up/down and EXE in the event cell.
    c.raw("1a a0 02 90")  # Load the event, not the scanner's status byte.

    # Only the native 75h class is translated. In particular, 7D01h is not EXE.
    c.db(0x75, 0x71)
    c.branch("ne", "done")
    for key, event in ((0x32, 0xfa), (0x34, 0xfb),
                       (0x44, 0xfc), (0x45, 0xfd),
                       (0x47, 0xfe), (0x42, 0xff)):
        c.db(key, 0x70)
        c.branch("ne", f"next_{key}")
        c.mov(0, event)
        c.branch("al", "done")
        c.label(f"next_{key}")

    c.label("done")
    c.raw("02 e1 8e f2")  # Discard event cell; POP PC restores the far return.
    data = c.build()
    if len(data) > 0xe0:
        raise ValueError("Scanner exceeds 8:0800..08DF")
    return SCANNER_ADDRESS - 0x80000, data
