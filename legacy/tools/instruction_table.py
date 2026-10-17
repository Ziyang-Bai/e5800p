"""Shared nX-U8 instruction records (bank 8) and ASCII names (bank F)."""

from flash_layout import INSTRUCTION_RECORDS_ADDRESS, INSTRUCTION_NAMES_ADDRESS

RECORD_SIZE = 16
RECORD_SEGMENT = INSTRUCTION_RECORDS_ADDRESS >> 16
NAME_SEGMENT = INSTRUCTION_NAMES_ADDRESS >> 16

IMM, RR, EE, EI7, SHIFT, ER_R, ONE_R, ONE_ER = range(8)
R_ABS, R_IND, R_DISP, ER_ABS, ER_IND, ER_DISP = range(8, 14)
BR, FAR, FAR_SYS, TB, SP_IMM, FIXED, EXTBW, ER_SP, SP_ER = range(14, 23)
SUB_IMM = 23
ONE_XR, ONE_QR = range(24, 26)
CATEGORIES = (
    ("ARITH", (
        (IMM, 0x1000, "ADD R,#"), (RR, 0x8001, "ADD R,R"),
        (IMM, 0x6000, "ADDC R,#"), (RR, 0x8006, "ADDC R,R"),
        (EI7, 0xe080, "ADD ER,#"), (EE, 0xf006, "ADD ER,ER"),
        (RR, 0x8008, "SUB R,R"), (RR, 0x8009, "SUBC R,R"),
        (SUB_IMM, 0x8008, "SUB R,#"), (RR, 0x8002, "AND R,R"),
        (IMM, 0x2000, "AND R,#"), (RR, 0x8003, "OR R,R"),
        (IMM, 0x3000, "OR R,#"), (RR, 0x8004, "XOR R,R"),
        (IMM, 0x4000, "XOR R,#"), (RR, 0x800a, "SLL R,R"),
        (SHIFT, 0x900a, "SLL R,#"), (RR, 0x800b, "SLLC R,R"),
        (SHIFT, 0x900b, "SLLC R,#"), (RR, 0x800c, "SRL R,R"),
        (SHIFT, 0x900c, "SRL R,#"), (RR, 0x800d, "SRLC R,R"),
        (SHIFT, 0x900e, "SRA R,#"),
        (RR, 0x800e, "SRA R,R"), (ER_R, 0xf004, "MUL ER,R"),
        (ER_R, 0xf009, "DIV ER,R"), (IMM, 0x7000, "CMP R,#"),
        (RR, 0x8007, "CMP R,R"), (IMM, 0x5000, "CMPC R,#"),
        (RR, 0x8005, "CMPC R,R"), (EE, 0xf007, "CMP ER,ER"),
        (ONE_R, 0x801f, "DAA R"), (ONE_R, 0x803f, "DAS R"),
        (ONE_R, 0x805f, "NEG R"),
    )),
    ("MOVE", (
        (IMM, 0x0000, "MOV R,#"), (RR, 0x8000, "MOV R,R"),
        (EE, 0xf005, "MOV ER,ER"), (ER_SP, 0xa01a, "MOV ER,SP"),
        (SP_ER, 0xa10a, "MOV SP,ER"),
    )),
    ("BRANCH", (
        (BR, 0xc000, "BGE"), (BR, 0xc100, "BLT"),
        (BR, 0xc200, "BGT"), (BR, 0xc300, "BLE"),
        (BR, 0xc400, "BGES"), (BR, 0xc500, "BLTS"),
        (BR, 0xc600, "BGTS"), (BR, 0xc700, "BLES"),
        (BR, 0xc800, "BNE"), (BR, 0xc900, "BEQ"),
        (BR, 0xca00, "BNV"), (BR, 0xcb00, "BOV"),
        (BR, 0xcc00, "BPS"), (BR, 0xcd00, "BNS"),
        (FAR, 0xf800, "JMP"), (FAR, 0xf801, "CALL"),
    )),
    ("LOAD/ST", (
        (R_ABS, 0x9010, "L R,ADDR"), (R_IND, 0x9000, "L R,[ER]"),
        (R_DISP, 0x9008, "L R,D[ER]"), (ER_ABS, 0x9012, "L ER,ADDR"),
        (ER_IND, 0x9002, "L ER,[ER]"), (ER_DISP, 0xa008, "L ER,D[ER]"),
        (R_ABS, 0x9011, "ST R,ADDR"), (R_IND, 0x9001, "ST R,[ER]"),
        (R_DISP, 0x9009, "ST R,D[ER]"), (ER_ABS, 0x9013, "ST ER,ADDR"),
        (ER_IND, 0x9003, "ST ER,[ER]"), (ER_DISP, 0xa009, "ST ER,D[ER]"),
    )),
    ("STACK", (
        (ONE_R, 0xf04e, "PUSH R"), (ONE_ER, 0xf05e, "PUSH ER"),
        (ONE_R, 0xf00e, "POP R"), (ONE_ER, 0xf01e, "POP ER"),
        # nX-U8/100 manual 3-83..3-87: general/control stack formats.
        (ONE_XR, 0xf06e, "PUSH XR"), (ONE_QR, 0xf07e, "PUSH QR"),
        (ONE_XR, 0xf02e, "POP XR"), (ONE_QR, 0xf03e, "POP QR"),
        (FIXED, 0xf8ce, "PUSH LR"), (FIXED, 0xf88e, "POP LR"),
        (FIXED, 0xf1ce, "PUSH EA"), (FIXED, 0xf18e, "POP EA"),
        (FIXED, 0xf28e, "POP PC"),
    )),
    ("MISC", (
        (FAR_SYS, 0xf001, "CALL_SYS"), (TB, 0xa001, "TB R.B"),
        (EXTBW, 0x810f, "EXTBW ER"), (SP_IMM, 0xe100, "ADD SP,#"),
        (FIXED, 0xed80, "SC"), (FIXED, 0xeb7f, "RC"),
        (FIXED, 0xfecf, "CPLC"), (FIXED, 0xfe8f, "NOP"),
        (FIXED, 0xfe1f, "RET"), (FIXED, 0xfe1f, "END"),
    )),
)

def operand_fields(kind):
    if kind in (IMM, SUB_IMM, SP_IMM):
        return (4, 4) if kind == SP_IMM else (1, 4, 4)
    if kind in (RR, ER_R, R_IND, R_DISP):
        first = 2 if kind == ER_R else 1
        return (first, 2 if kind in (R_IND, R_DISP) else 1) + ((4,) * 4 if kind == R_DISP else ())
    if kind in (EE, ER_IND, ER_DISP):
        return (2, 2) + ((4,) * 4 if kind == ER_DISP else ())
    if kind == EI7:
        return (2, 4, 4)
    if kind in (SHIFT, TB):
        return (1, 3)
    if kind in (ONE_XR, ONE_QR):
        return (5 if kind == ONE_XR else 6,)
    if kind in (ONE_R, ONE_ER, EXTBW, ER_SP, SP_ER):
        return (2 if kind in (ONE_ER, EXTBW, ER_SP, SP_ER) else 1,)
    if kind in (R_ABS, ER_ABS):
        return (2 if kind == ER_ABS else 1,) + (4,) * 4
    if kind == BR:
        return (4,) * 4
    if kind == FAR:
        return (4,) * 4
    if kind == FAR_SYS:
        return (4,) * 5
    return ()


def opcode_mask(kind, opcode):
    if kind == SUB_IMM:
        return 0xffff
    if kind in (ONE_XR, ONE_QR):
        return 0xf3ff if kind == ONE_XR else 0xf7ff
    if kind == IMM:
        return 0xf000
    if kind == EI7:
        return 0xf180
    if kind in (RR, SHIFT, TB):
        return 0xf00f
    if kind == R_DISP:
        return 0xf01f
    if kind in (EE, ER_R, ER_IND, ER_DISP):
        return 0xf11f if kind in (ER_IND, ER_DISP) else 0xf10f
    if kind in (R_IND,):
        return 0xf01f
    if kind in (ONE_R, R_ABS):
        return 0xf0ff
    if kind in (ONE_ER, ER_ABS, ER_SP):
        return 0xf1ff
    if kind == BR:
        return 0xff00
    if kind == FAR:
        return 0xf8ff
    if kind == FAR_SYS:
        return 0xf0ff
    if kind == SP_IMM:
        return 0xff00
    if kind == EXTBW:
        return 0xf10f
    if kind == SP_ER:
        return 0xff0f
    if kind == FIXED:
        return 0xffff
    raise ValueError(kind)


ENTRIES = tuple(entry for _, entries in CATEGORIES for entry in entries)
COUNTS_ADDRESS = INSTRUCTION_RECORDS_ADDRESS + RECORD_SIZE * len(ENTRIES)
STARTS_ADDRESS = COUNTS_ADDRESS + len(CATEGORIES)

# Strings are interned before pointers are assigned; all readers use NAME_SEGMENT.
_NAMES = tuple(dict.fromkeys([name for _, _, name in ENTRIES] +
                            [name for name, _ in CATEGORIES] + ["DW"]))
NAME_ADDRESSES = {}
_names = bytearray()
for _name in _NAMES:
    NAME_ADDRESSES[_name] = INSTRUCTION_NAMES_ADDRESS + len(_names)
    _names.extend(_name.encode("ascii") + b"\0")


def instruction_table_code():
    """Emit the sole fixed-width catalogue and its separate name pool."""
    records = bytearray()
    for kind, opcode, name in ENTRIES:
        fields = operand_fields(kind)
        mask = opcode_mask(kind, opcode)
        records.extend((kind, int(kind != SUB_IMM and name != "END")))
        records.extend(opcode.to_bytes(2, "little"))
        records.extend(fields + (0,) * (8 - len(fields)))
        records.extend((NAME_ADDRESSES[name] & 0xffff).to_bytes(2, "little"))
        records.extend(mask.to_bytes(2, "little"))
    records.extend(len(entries) for _, entries in CATEGORIES)
    start = 0
    for _, entries in CATEGORIES:
        records.append(start)
        start += len(entries)
    if INSTRUCTION_RECORDS_ADDRESS & 1 or len(records) > 0x1800 - (INSTRUCTION_RECORDS_ADDRESS & 0xffff):
        raise ValueError("Instruction records exceed bank 8 budget")
    if len(_names) > 0x9400 - (INSTRUCTION_NAMES_ADDRESS & 0xffff):
        raise ValueError("Instruction names exceed bank F budget")
    return ((INSTRUCTION_RECORDS_ADDRESS - 0x80000, bytes(records)),
            (INSTRUCTION_NAMES_ADDRESS - 0x80000, bytes(_names)))
