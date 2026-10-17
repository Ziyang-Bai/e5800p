"""Emit the instruction viewer's native mnemonic and operand formatter.

PC, length, kind and name are frame slots 40..45; 52..63 are scratch.
operand_text appends ASCII at ER10 without a NUL and keeps ER14 unchanged.
"""

from instruction_table import (IMM, RR, EE, EI7, SHIFT, ER_R, ONE_R, ONE_ER,
                               R_ABS, R_IND, R_DISP, ER_ABS, ER_IND, ER_DISP,
                               BR, FAR, FAR_SYS, TB, SP_IMM, FIXED, EXTBW,
                               ER_SP, SP_ER, SUB_IMM, ONE_XR, ONE_QR, NAME_SEGMENT)


def emit_text(c):
    """Append formatter routines to the viewer's code segment."""
    seq = 0

    def goto_if(condition, target):
        nonlocal seq
        seq += 1
        skip = f"operand_skip_{seq}"
        c.branch({"eq": "ne", "ne": "eq", "lt": "ge", "ge": "lt"}[condition], skip)
        c.jump(target)
        c.label(skip)

    def done():
        c.jump("operand_done")

    c.label("operand_text")
    c.raw("ce f8")
    c.slot(8, 40)
    c.slot(9, 41)
    c.slot(6, 78)
    c.mov(7, 0)
    c.raw("66 f8")  # Operand bytes follow the DSR word, if present.
    c.flash(0, 4)
    c.flash(1, 5)
    c.slot(4, 52, True)
    c.slot(5, 53, True)
    c.copy(0, 5)
    c.db(0x0f, 0x20)
    c.slot(0, 54, True)  # Destination register index.
    c.copy(0, 4)
    c.db(0x4c, 0x90)
    c.slot(0, 55, True)  # Source register index or shift/bit count.
    c.slot(0, 43)
    c.db(0xff, 0x70)
    goto_if("eq", "operand_unknown")
    c.slot(6, 44)
    c.slot(7, 45)
    c.label("operand_name")
    c.pair(2, 6)
    c.ram(0, 0x20, segment=NAME_SEGMENT)
    c.db(0, 0x70)
    c.branch("eq", "operand_name_done")
    c.db(32, 0x70)
    c.branch("ne", "operand_name_char")
    c.slot(1, 43)
    c.db(FIXED, 0x71)
    c.branch("ne", "operand_name_done")
    c.label("operand_name_char")
    c.char(0)
    c.add_er(6, 1)
    c.jump("operand_name")
    c.label("operand_name_done")
    c.slot(6, 43)
    c.db(FIXED, 0x76)
    goto_if("eq", "operand_done")
    c.char(" ")
    for kind, label in (
        (IMM, "imm"), (RR, "rr"), (EE, "ee"), (EI7, "ei7"),
        (SHIFT, "shift"), (ER_R, "er_r"), (ONE_R, "one_r"),
        (ONE_ER, "one_er"), (R_ABS, "r_abs"), (R_IND, "r_ind"),
        (ONE_XR, "one_xr"), (ONE_QR, "one_qr"),
        (R_DISP, "r_disp"), (ER_ABS, "er_abs"), (ER_IND, "er_ind"),
        (ER_DISP, "er_disp"), (BR, "branch"), (FAR, "far"),
        (FAR_SYS, "far"), (TB, "tb"), (SP_IMM, "sp_imm"),
        (EXTBW, "one_er"), (ER_SP, "er_sp"), (SP_ER, "sp_er"),
        (SUB_IMM, "sub_imm"),
    ):
        c.db(kind, 0x76)
        goto_if("eq", "operand_" + label)
    done()

    c.label("operand_imm")
    c.call("operand_rdest")
    c.text(",#")
    c.slot(0, 52)
    c.call("hexbyte")
    done()

    for label, dst, src in (
        ("rr", "rdest", "rsrc"), ("ee", "edest", "esrc"),
        ("er_r", "edest", "rsrc"),
    ):
        c.label("operand_" + label)
        c.call("operand_" + dst)
        c.char(",")
        c.call("operand_" + src)
        done()

    c.label("operand_ei7")
    c.call("operand_edest")
    c.text(",#")
    c.slot(0, 52)
    c.db(0x7f, 0x20)  # imm7 occupies bits 0..6; bit 7 selects the opcode.
    c.call("hexbyte")
    done()

    c.label("operand_shift")
    c.call("operand_rdest")
    c.text(",#")
    c.slot(0, 55)
    c.db(7, 0x20)
    c.call("hexbyte")
    done()

    for label, reg in (("one_r", "rdest"), ("one_er", "edest")):
        c.label("operand_" + label)
        c.call("operand_" + reg)
        done()

    for label, prefix in (("one_xr", "X"), ("one_qr", "Q")):
        c.label("operand_" + label)
        c.char(prefix)
        c.char("R")
        c.slot(0, 54)
        c.call("operand_decimal")
        done()

    for label, reg in (("r_abs", "rdest"), ("er_abs", "edest")):
        c.label("operand_" + label)
        c.call("operand_" + reg)
        c.char(",")
        c.call("operand_segment")
        c.call("operand_word")
        done()

    for label, reg in (("r_ind", "rdest"), ("er_ind", "edest")):
        c.label("operand_" + label)
        c.call("operand_" + reg)
        c.char(",")
        c.call("operand_segment")
        c.char("[")
        c.call("operand_esrc")
        c.char("]")
        done()

    for label, reg in (("r_disp", "rdest"), ("er_disp", "edest")):
        c.label("operand_" + label)
        c.call("operand_" + reg)
        c.char(",")
        c.call("operand_segment")
        c.call("operand_word")
        c.char("[")
        c.call("operand_esrc")
        c.char("]")
        done()

    c.label("operand_branch")
    c.slot(6, 52)
    c.mov(7, 0)
    c.db(0x80, 0x76)
    c.branch("lt", "operand_branch_positive")
    c.mov(7, 0xff)
    c.label("operand_branch_positive")
    c.raw("66 f6")  # Sign-extended word displacement * 2.
    c.add_er(6, 2)
    c.raw("86 f6")  # Absolute target = PC + 2 + displacement * 2.
    c.slot(6, 58, True)
    c.copy(0, 7)
    c.call("hexbyte")
    c.slot(0, 58)
    c.call("hexbyte")
    done()

    c.label("operand_far")
    c.slot(0, 53)
    c.db(0x0f, 0x20)
    c.call("nibble")
    c.char(0)
    c.char(":")
    c.call("operand_word")
    done()

    c.label("operand_tb")
    c.call("operand_rdest")
    c.char(".")
    c.slot(0, 55)
    c.db(7, 0x20)
    c.call("operand_decimal")
    done()

    c.label("operand_sp_imm")
    c.text("SP,#")
    c.slot(0, 52)
    c.call("hexbyte")
    done()

    c.label("operand_er_sp")
    c.call("operand_edest")
    c.text(",SP")
    done()

    c.label("operand_sp_er")
    c.text("SP,")
    c.call("operand_esrc")
    done()

    c.label("operand_sub_imm")
    # PUSH scratch; MOV scratch,#imm; SUB destination,scratch; POP scratch.
    c.char("R")
    c.flash(5, 0)
    c.db(0x0f, 0x20)
    c.call("operand_decimal")
    c.text(",#")
    c.flash(2, 0)
    c.call("hexbyte")
    done()

    c.label("operand_unknown")
    c.text("DW ")
    c.slot(0, 53)
    c.call("hexbyte")
    c.slot(0, 52)
    c.call("hexbyte")
    c.label("operand_done")
    c.slot(8, 40)
    c.slot(9, 41)
    c.raw("8e f2")

    # These leaf routines tail-call the decimal register index formatter.
    c.label("operand_edest")
    c.char("E")
    c.char("R")
    c.slot(0, 54)
    c.db(0x0e, 0x20)  # EXTBW's odd encoded index names the even ER pair.
    c.jump("operand_decimal")
    c.label("operand_rdest")
    c.char("R")
    c.slot(0, 54)
    c.jump("operand_decimal")
    c.label("operand_esrc")
    c.char("E")
    c.label("operand_rsrc")
    c.char("R")
    c.slot(0, 55)
    c.jump("operand_decimal")

    c.label("operand_decimal")
    c.copy(6, 0)
    c.db(10, 0x76)
    c.branch("lt", "operand_decimal_digit")
    c.char("1")
    c.db(0xf6, 0x16)
    c.label("operand_decimal_digit")
    c.copy(0, 6)
    c.db(48, 0x10)
    c.char(0)
    c.raw("1f fe")

    c.label("operand_word")
    c.raw("ce f8")
    c.flash(3, 0)
    c.call("hexbyte")
    c.flash(2, 0)
    c.call("hexbyte")
    c.raw("8e f2")

    c.label("operand_segment")
    c.raw("ce f8")
    c.slot(0, 78)
    c.db(0, 0x70)
    c.branch("eq", "operand_segment_done")
    c.slot(6, 40)
    c.slot(7, 41)
    c.pair(2, 6)
    c.ram(4, 0x20, segment=8)
    c.add_er(2, 1)
    c.ram(0, 0x20, segment=8)
    c.db(0xe3, 0x70)
    c.branch("ne", "operand_segment_register")
    c.copy(0, 4)
    c.call("hexbyte")
    c.jump("operand_segment_colon")
    c.label("operand_segment_register")
    c.db(0xfe, 0x70)
    c.branch("ne", "operand_segment_r")
    c.text("DSR")
    c.jump("operand_segment_colon")
    c.label("operand_segment_r")
    c.copy(0, 4)
    c.db(0x4c, 0x90)
    c.copy(4, 0)
    c.char("R")
    c.copy(0, 4)
    c.call("operand_decimal")
    c.label("operand_segment_colon")
    c.char(":")
    c.label("operand_segment_done")
    c.raw("8e f2")
