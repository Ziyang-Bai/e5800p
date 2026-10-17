"""Fixed-layout e5800p basic routines and tables."""

from kits import cpu

NATIVE_TOKEN_ADMISSION = 0xC30D8
NATIVE_EVALUATE = 0xC7B6E
BASIC_MEMORY = 0xFB530
BASIC_GRAPHICS = 0xFC530
NATIVE_ERROR_WRITE = 0xE8FBA
NATIVE_EVALUATE_CORE = 0xC701E
NATIVE_TOKEN_FETCH = 0xC3794
NATIVE_NUMBER_COPY = 0x19B72
BASIC_ASM = 0xF9530
NATIVE_PROGRAM_LOOKUP = 0xE2F86
NATIVE_LIBRARY_LOOKUP = 0xF0484
HOOK_SPELL_DFC02 = 0xDFC02
NATIVE_TOKEN_DECODE = 0x10B7E
NATIVE_PROGRAM_FUNCTION = 0xDF3FA
ROM_DRAW_TEXT = 0x041DA
ROM_REFRESH = 0x043BE
HEX_KEY_ADDRESS = 0x825CA
NATIVE_PROGRAM_INSERT = 0xE302E

BASIC_DATA_NAMES = bytes((
    0x9B, 0x5B, 0xA0, 0x5B, 0xA7, 0x5B, 0xAC, 0x5B, 0xB3, 0x5B, 0xB8, 0x5B, 0xBD, 0x5B, 0xC1, 0x5B,
    0xC6, 0x5B, 0xCA, 0x5B, 0xCE, 0x5B, 0xD4, 0x5B, 0xDA, 0x5B, 0xE0, 0x5B, 0xE5, 0x5B, 0xEA, 0x5B,
    0xF5, 0x5B, 0xF9, 0x5B, 0xFE, 0x5B, 0x03, 0x5C, 0x08, 0x5C, 0x0D, 0x5C, 0x12, 0x5C, 0x1A, 0x5C,
    0x1E, 0x5C,
))

BASIC_DATA_ARG_COUNTS = bytes((
    0x01, 0x01, 0x02, 0x02, 0x05, 0x02, 0x02, 0x02, 0x02, 0x02, 0x00, 0x00, 0x02, 0x03, 0x03, 0x03,
    0x00, 0x03, 0x05, 0x05, 0x06, 0x04, 0x00, 0x00, 0x00,
))

BASIC_DATA_ARG_TYPES = bytes((
    0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x04, 0x01, 0x00, 0x00, 0x00, 0x00, 0x02, 0x01, 0x01, 0x01, 0x01, 0x00, 0x01, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00,
    0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x03, 0x00, 0x00, 0x00, 0x00, 0x04, 0x04,
    0x01, 0x00, 0x00, 0x00, 0x04, 0x01, 0x00, 0x00, 0x00, 0x00, 0x02, 0x04, 0x01, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x03, 0x00, 0x00, 0x00, 0x00, 0x03, 0x03, 0x03, 0x03,
    0x00, 0x00, 0x03, 0x03, 0x03, 0x03, 0x00, 0x00, 0x03, 0x03, 0x00, 0x00, 0x04, 0x00, 0x03, 0x03,
    0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
))

BASIC_DATA_NX_PAGE_NAME = b'%\\'

BASIC_DATA_NX_CATEGORY_NAMES = bytes((
    0x28, 0x5C, 0x1A, 0x5C, 0x2C, 0x5C, 0x30, 0x5C,
))

BASIC_DATA_NX_ITEMS_0 = bytes((
    0x9B, 0x5B, 0xA0, 0x5B, 0xA7, 0x5B, 0xAC, 0x5B, 0xE0, 0x5B, 0xE5, 0x5B, 0xEA, 0x5B,
))

BASIC_DATA_NX_TOKENS_0 = bytes((
    0xE0, 0xE1, 0xE2, 0xE3, 0xED, 0xEE, 0xEF, 0x00,
))

BASIC_DATA_NX_ITEMS_1 = bytes((
    0xB3, 0x5B, 0x1A, 0x5C, 0x1E, 0x5C,
))

BASIC_DATA_NX_TOKENS_1 = bytes((
    0xE4, 0xF7, 0xF8, 0x00,
))

BASIC_DATA_NX_ITEMS_2 = bytes((
    0xF5, 0x5B, 0xF9, 0x5B, 0xDA, 0x5B, 0xFE, 0x5B, 0x03, 0x5C, 0x08, 0x5C, 0x0D, 0x5C, 0x12, 0x5C,
))

BASIC_DATA_NX_TOKENS_2 = bytes((
    0xF0, 0xF1, 0xEC, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6,
))

BASIC_DATA_NX_ITEMS_3 = bytes((
    0xB8, 0x5B, 0xBD, 0x5B, 0xC1, 0x5B, 0xC6, 0x5B, 0xCA, 0x5B, 0xCE, 0x5B, 0xD4, 0x5B,
))

BASIC_DATA_NX_TOKENS_3 = bytes((
    0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEA, 0xEB, 0x00,
))

BASIC_DATA_BLOCK_CATEGORIES_NAMES = b'6\\9\\=\\A\\'

BASIC_DATA_OP_CATEGORIES = b'G\\M\\R\\Y\\a\\g\\'

BASIC_DATA_BLOCK_REGS = bytes((
    0x6C, 0x5C, 0x6F, 0x5C, 0x72, 0x5C, 0x75, 0x5C, 0x78, 0x5C, 0x7B, 0x5C, 0x7E, 0x5C, 0x81, 0x5C,
    0x84, 0x5C, 0x87, 0x5C, 0x8A, 0x5C, 0x8E, 0x5C, 0x92, 0x5C, 0x96, 0x5C, 0x9A, 0x5C, 0x9E, 0x5C,
    0xA2, 0x5C, 0xA6, 0x5C, 0xAA, 0x5C, 0xAE, 0x5C, 0xB2, 0x5C, 0xB6, 0x5C, 0xBB, 0x5C, 0xC0, 0x5C,
    0xC5, 0x5C, 0xC9, 0x5C, 0xCD, 0x5C, 0xD1, 0x5C, 0xD6, 0x5C, 0xDA, 0x5C, 0xDE, 0x5C, 0xE1, 0x5C,
    0xE4, 0x5C,
))

BASIC_DATA_BLOCK_REGS_TEXT = bytes((
    0x6C, 0x5C, 0x6F, 0x5C, 0x72, 0x5C, 0x75, 0x5C, 0x78, 0x5C, 0x7B, 0x5C, 0x7E, 0x5C, 0x81, 0x5C,
    0x84, 0x5C, 0x87, 0x5C, 0x8A, 0x5C, 0x8E, 0x5C, 0x92, 0x5C, 0x96, 0x5C, 0x9A, 0x5C, 0x9E, 0x5C,
    0xA2, 0x5C, 0xA6, 0x5C, 0xAA, 0x5C, 0xAE, 0x5C, 0xB2, 0x5C, 0xB6, 0x5C, 0xBB, 0x5C, 0xC0, 0x5C,
    0xC5, 0x5C, 0xC9, 0x5C, 0xCD, 0x5C, 0xD1, 0x5C, 0xD6, 0x5C, 0xDA, 0x5C, 0xDE, 0x5C, 0xE1, 0x5C,
    0xE4, 0x5C,
))

BASIC_DATA_BLOCK_SYMBOLS = bytes((
    0xE7, 0x5C, 0xED, 0x5C, 0xEF, 0x5C, 0xF1, 0x5C, 0xF3, 0x5C, 0xF5, 0x5C, 0xF7, 0x5C, 0xF9, 0x5C,
    0xFB, 0x5C, 0xFD, 0x5C, 0xFF, 0x5C, 0x01, 0x5D, 0x03, 0x5D, 0x05, 0x5D, 0x07, 0x5D, 0x09, 0x5D,
    0x0B, 0x5D, 0x0D, 0x5D, 0x0F, 0x5D, 0x11, 0x5D,
))

BASIC_DATA_BLOCK_SYMBOLS_TEXT = bytes((
    0x13, 0x5D, 0xED, 0x5C, 0xEF, 0x5C, 0xF1, 0x5C, 0xF3, 0x5C, 0xF5, 0x5C, 0xF7, 0x5C, 0xF9, 0x5C,
    0xFB, 0x5C, 0xFD, 0x5C, 0xFF, 0x5C, 0x01, 0x5D, 0x03, 0x5D, 0x05, 0x5D, 0x07, 0x5D, 0x09, 0x5D,
    0x0B, 0x5D, 0x0D, 0x5D, 0x0F, 0x5D, 0x11, 0x5D,
))

BASIC_DATA_BLOCK_DIRECTIVES = bytes((
    0x15, 0x5D, 0x18, 0x5D, 0x1E, 0x5C,
))

BASIC_DATA_BLOCK_DIRECTIVES_TEXT = bytes((
    0x1B, 0x5D, 0x1F, 0x5D, 0x23, 0x5D,
))

BASIC_DATA_OP_0 = bytes((
    0x27, 0x5D, 0x2F, 0x5D, 0x37, 0x5D, 0x40, 0x5D, 0x49, 0x5D, 0x52, 0x5D, 0x5C, 0x5D, 0x64, 0x5D,
    0x6D, 0x5D, 0x75, 0x5D, 0x7D, 0x5D, 0x85, 0x5D, 0x8C, 0x5D, 0x93, 0x5D, 0x9B, 0x5D, 0xA3, 0x5D,
    0xAB, 0x5D, 0xB3, 0x5D, 0xBC, 0x5D, 0xC5, 0x5D, 0xCD, 0x5D, 0xD5, 0x5D, 0xDE, 0x5D, 0xE6, 0x5D,
    0xEE, 0x5D, 0xF7, 0x5D, 0x00, 0x5E, 0x08, 0x5E, 0x10, 0x5E, 0x19, 0x5E, 0x22, 0x5E, 0x2C, 0x5E,
    0x32, 0x5E, 0x38, 0x5E,
))

BASIC_DATA_OP_0_TEXT = bytes((
    0x3E, 0x5E, 0x48, 0x5E, 0x52, 0x5E, 0x5D, 0x5E, 0x68, 0x5E, 0x73, 0x5E, 0x7F, 0x5E, 0x89, 0x5E,
    0x94, 0x5E, 0x9E, 0x5E, 0xA8, 0x5E, 0xB2, 0x5E, 0xBB, 0x5E, 0xC4, 0x5E, 0xCE, 0x5E, 0xD8, 0x5E,
    0xE2, 0x5E, 0xEC, 0x5E, 0xF7, 0x5E, 0x02, 0x5F, 0x0C, 0x5F, 0x16, 0x5F, 0x21, 0x5F, 0x2B, 0x5F,
    0x35, 0x5F, 0x40, 0x5F, 0x4B, 0x5F, 0x55, 0x5F, 0x5F, 0x5F, 0x6A, 0x5F, 0x75, 0x5F, 0x81, 0x5F,
    0x88, 0x5F, 0x8F, 0x5F,
))

BASIC_DATA_OP_1 = bytes((
    0x96, 0x5F, 0x9E, 0x5F, 0xA6, 0x5F, 0xB0, 0x5F, 0xBA, 0x5F, 0xC4, 0x5F,
))

BASIC_DATA_OP_1_TEXT = bytes((
    0xCD, 0x5F, 0xD7, 0x5F, 0xE1, 0x5F, 0xED, 0x5F, 0xF8, 0x5F, 0x03, 0x60,
))

BASIC_DATA_OP_2 = bytes((
    0x0E, 0x60, 0x12, 0x60, 0x16, 0x60, 0x1A, 0x60, 0x1E, 0x60, 0x23, 0x60, 0x28, 0x60, 0x2D, 0x60,
    0x32, 0x60, 0x36, 0x60, 0x3A, 0x60, 0x3E, 0x60, 0x42, 0x60, 0x46, 0x60, 0x4A, 0x60, 0xB3, 0x5B,
))

BASIC_DATA_OP_2_TEXT = bytes((
    0x4E, 0x60, 0x58, 0x60, 0x62, 0x60, 0x6C, 0x60, 0x76, 0x60, 0x81, 0x60, 0x8C, 0x60, 0x97, 0x60,
    0xA2, 0x60, 0xAC, 0x60, 0xB6, 0x60, 0xC0, 0x60, 0xCA, 0x60, 0xD4, 0x60, 0xDE, 0x60, 0xE8, 0x60,
))

BASIC_DATA_OP_3 = bytes((
    0xF3, 0x60, 0xFC, 0x60, 0x05, 0x61, 0x0F, 0x61, 0x19, 0x61, 0x23, 0x61, 0x2E, 0x61, 0x38, 0x61,
    0x42, 0x61, 0x4D, 0x61, 0x58, 0x61, 0x63, 0x61,
))

BASIC_DATA_OP_3_TEXT = bytes((
    0x6F, 0x61, 0x76, 0x61, 0x81, 0x61, 0x8D, 0x61, 0x95, 0x61, 0xA1, 0x61, 0xAE, 0x61, 0xB6, 0x61,
    0xC2, 0x61, 0xCF, 0x61, 0xD8, 0x61, 0xE5, 0x61,
))

BASIC_DATA_OP_4 = bytes((
    0xF3, 0x61, 0xFA, 0x61, 0x02, 0x62, 0x08, 0x62, 0x0F, 0x62, 0x17, 0x62, 0x1F, 0x62, 0x26, 0x62,
    0x2D, 0x62, 0x35, 0x62, 0x3C, 0x62, 0x44, 0x62, 0x4B, 0x62,
))

BASIC_DATA_OP_4_TEXT = bytes((
    0x52, 0x62, 0x5A, 0x62, 0x63, 0x62, 0x6A, 0x62, 0x72, 0x62, 0x7B, 0x62, 0x84, 0x62, 0x8C, 0x62,
    0x2D, 0x62, 0x35, 0x62, 0x3C, 0x62, 0x44, 0x62, 0x4B, 0x62,
))

BASIC_DATA_OP_5 = bytes((
    0x94, 0x62, 0x9D, 0x62, 0xA4, 0x62, 0xAD, 0x62, 0xB6, 0x62, 0xB9, 0x62, 0xBC, 0x62, 0xC1, 0x62,
    0xC5, 0x62, 0xC9, 0x62,
))

BASIC_DATA_OP_5_TEXT = bytes((
    0xCD, 0x62, 0xD8, 0x62, 0xE0, 0x62, 0xEA, 0x62, 0xB6, 0x62, 0xB9, 0x62, 0xBC, 0x62, 0xC1, 0x62,
    0xC5, 0x62, 0xC9, 0x62,
))

BASIC_DATA_ASM_REASONS = bytes((
    0xF4, 0x62, 0x00, 0x63, 0x0A, 0x63, 0x13, 0x63, 0x1C, 0x63, 0x2A, 0x63,
))

BASIC_DATA_WRITE_ERROR = b'WRITE ERROR\x00'

BASIC_DATA_ASM_ERROR_TITLE = b'ASM ERROR\x00'

BASIC_DATA_ERROR_EXIT = b'EXIT\x00'

BASIC_DATA_TEXT_0 = b'PEEK\x00'

BASIC_DATA_TEXT_1 = b'PEEK16\x00'

BASIC_DATA_TEXT_2 = b'POKE\x00'

BASIC_DATA_TEXT_3 = b'POKE16\x00'

BASIC_DATA_TEXT_4 = b'CALL\x00'

BASIC_DATA_TEXT_5 = b'BAND\x00'

BASIC_DATA_TEXT_6 = b'BOR\x00'

BASIC_DATA_TEXT_7 = b'BXOR\x00'

BASIC_DATA_TEXT_8 = b'SHL\x00'

BASIC_DATA_TEXT_9 = b'SHR\x00'

BASIC_DATA_TEXT_10 = b'INKEY\x00'

BASIC_DATA_TEXT_11 = b'TICKS\x00'

BASIC_DATA_TEXT_12 = b'POINT\x00'

BASIC_DATA_TEXT_13 = b'COPY\x00'

BASIC_DATA_TEXT_14 = b'FILL\x00'

BASIC_DATA_TEXT_15 = b'FLASHWRITE\x00'

BASIC_DATA_TEXT_16 = b'CLS\x00'

BASIC_DATA_TEXT_17 = b'PSET\x00'

BASIC_DATA_TEXT_18 = b'LINE\x00'

BASIC_DATA_TEXT_19 = b'RECT\x00'

BASIC_DATA_TEXT_20 = b'BLIT\x00'

BASIC_DATA_TEXT_21 = b'TEXT\x00'

BASIC_DATA_TEXT_22 = b'REFRESH\x00'

BASIC_DATA_TEXT_23 = b'ASM\x00'

BASIC_DATA_TEXT_24 = b'ENDASM\x00'

BASIC_DATA_TEXT_25 = b'NX\x00'

BASIC_DATA_TEXT_26 = b'MEM\x00'

BASIC_DATA_TEXT_27 = b'GFX\x00'

BASIC_DATA_TEXT_28 = b'TOOLS\x00'

BASIC_DATA_TEXT_29 = b'OP\x00'

BASIC_DATA_TEXT_30 = b'REG\x00'

BASIC_DATA_TEXT_31 = b'SYM\x00'

BASIC_DATA_TEXT_32 = b'BLOCK\x00'

BASIC_DATA_TEXT_33 = b'ARITH\x00'

BASIC_DATA_TEXT_34 = b'MOVE\x00'

BASIC_DATA_TEXT_35 = b'BRANCH\x00'

BASIC_DATA_TEXT_36 = b'LOAD/ST\x00'

BASIC_DATA_TEXT_37 = b'STACK\x00'

BASIC_DATA_TEXT_38 = b'MISC\x00'

BASIC_DATA_TEXT_39 = b'R0\x00'

BASIC_DATA_TEXT_40 = b'R1\x00'

BASIC_DATA_TEXT_41 = b'R2\x00'

BASIC_DATA_TEXT_42 = b'R3\x00'

BASIC_DATA_TEXT_43 = b'R4\x00'

BASIC_DATA_TEXT_44 = b'R5\x00'

BASIC_DATA_TEXT_45 = b'R6\x00'

BASIC_DATA_TEXT_46 = b'R7\x00'

BASIC_DATA_TEXT_47 = b'R8\x00'

BASIC_DATA_TEXT_48 = b'R9\x00'

BASIC_DATA_TEXT_49 = b'R10\x00'

BASIC_DATA_TEXT_50 = b'R11\x00'

BASIC_DATA_TEXT_51 = b'R12\x00'

BASIC_DATA_TEXT_52 = b'R13\x00'

BASIC_DATA_TEXT_53 = b'R14\x00'

BASIC_DATA_TEXT_54 = b'R15\x00'

BASIC_DATA_TEXT_55 = b'ER0\x00'

BASIC_DATA_TEXT_56 = b'ER2\x00'

BASIC_DATA_TEXT_57 = b'ER4\x00'

BASIC_DATA_TEXT_58 = b'ER6\x00'

BASIC_DATA_TEXT_59 = b'ER8\x00'

BASIC_DATA_TEXT_60 = b'ER10\x00'

BASIC_DATA_TEXT_61 = b'ER12\x00'

BASIC_DATA_TEXT_62 = b'ER14\x00'

BASIC_DATA_TEXT_63 = b'XR0\x00'

BASIC_DATA_TEXT_64 = b'XR4\x00'

BASIC_DATA_TEXT_65 = b'XR8\x00'

BASIC_DATA_TEXT_66 = b'XR12\x00'

BASIC_DATA_TEXT_67 = b'QR0\x00'

BASIC_DATA_TEXT_68 = b'QR8\x00'

BASIC_DATA_TEXT_69 = b'SP\x00'

BASIC_DATA_TEXT_70 = b'LR\x00'

BASIC_DATA_TEXT_71 = b'EA\x00'

BASIC_DATA_TEXT_72 = b'SPACE\x00'

BASIC_DATA_TEXT_73 = b',\x00'

BASIC_DATA_TEXT_74 = b':\x00'

BASIC_DATA_TEXT_75 = b'[\x00'

BASIC_DATA_TEXT_76 = b']\x00'

BASIC_DATA_TEXT_77 = b'#\x00'

BASIC_DATA_TEXT_78 = b'_\x00'

BASIC_DATA_TEXT_79 = b'"\x00'

BASIC_DATA_TEXT_80 = b';\x00'

BASIC_DATA_TEXT_81 = b'+\x00'

BASIC_DATA_TEXT_82 = b'-\x00'

BASIC_DATA_TEXT_83 = b'*\x00'

BASIC_DATA_TEXT_84 = b'/\x00'

BASIC_DATA_TEXT_85 = b'$\x00'

BASIC_DATA_TEXT_86 = b'\\\x00'

BASIC_DATA_TEXT_87 = b'`\x00'

BASIC_DATA_TEXT_88 = b'|\x00'

BASIC_DATA_TEXT_89 = b'.\x00'

BASIC_DATA_TEXT_90 = b'(\x00'

BASIC_DATA_TEXT_91 = b')\x00'

BASIC_DATA_TEXT_92 = b' \x00'

BASIC_DATA_TEXT_93 = b'DB\x00'

BASIC_DATA_TEXT_94 = b'DW\x00'

BASIC_DATA_TEXT_95 = b'DB \x00'

BASIC_DATA_TEXT_96 = b'DW \x00'

BASIC_DATA_TEXT_97 = bytes((
    0xF9, 0xF8, 0x0D, 0x00,
))

BASIC_DATA_TEXT_98 = b'ADD R,#\x00'

BASIC_DATA_TEXT_99 = b'ADD R,R\x00'

BASIC_DATA_TEXT_100 = b'ADDC R,#\x00'

BASIC_DATA_TEXT_101 = b'ADDC R,R\x00'

BASIC_DATA_TEXT_102 = b'ADD ER,#\x00'

BASIC_DATA_TEXT_103 = b'ADD ER,ER\x00'

BASIC_DATA_TEXT_104 = b'SUB R,R\x00'

BASIC_DATA_TEXT_105 = b'SUBC R,R\x00'

BASIC_DATA_TEXT_106 = b'SUB R,#\x00'

BASIC_DATA_TEXT_107 = b'AND R,R\x00'

BASIC_DATA_TEXT_108 = b'AND R,#\x00'

BASIC_DATA_TEXT_109 = b'OR R,R\x00'

BASIC_DATA_TEXT_110 = b'OR R,#\x00'

BASIC_DATA_TEXT_111 = b'XOR R,R\x00'

BASIC_DATA_TEXT_112 = b'XOR R,#\x00'

BASIC_DATA_TEXT_113 = b'SLL R,R\x00'

BASIC_DATA_TEXT_114 = b'SLL R,#\x00'

BASIC_DATA_TEXT_115 = b'SLLC R,R\x00'

BASIC_DATA_TEXT_116 = b'SLLC R,#\x00'

BASIC_DATA_TEXT_117 = b'SRL R,R\x00'

BASIC_DATA_TEXT_118 = b'SRL R,#\x00'

BASIC_DATA_TEXT_119 = b'SRLC R,R\x00'

BASIC_DATA_TEXT_120 = b'SRA R,#\x00'

BASIC_DATA_TEXT_121 = b'SRA R,R\x00'

BASIC_DATA_TEXT_122 = b'MUL ER,R\x00'

BASIC_DATA_TEXT_123 = b'DIV ER,R\x00'

BASIC_DATA_TEXT_124 = b'CMP R,#\x00'

BASIC_DATA_TEXT_125 = b'CMP R,R\x00'

BASIC_DATA_TEXT_126 = b'CMPC R,#\x00'

BASIC_DATA_TEXT_127 = b'CMPC R,R\x00'

BASIC_DATA_TEXT_128 = b'CMP ER,ER\x00'

BASIC_DATA_TEXT_129 = b'DAA R\x00'

BASIC_DATA_TEXT_130 = b'DAS R\x00'

BASIC_DATA_TEXT_131 = b'NEG R\x00'

BASIC_DATA_TEXT_132 = b'ADD R0,#0\x00'

BASIC_DATA_TEXT_133 = b'ADD R0,R0\x00'

BASIC_DATA_TEXT_134 = b'ADDC R0,#0\x00'

BASIC_DATA_TEXT_135 = b'ADDC R0,R0\x00'

BASIC_DATA_TEXT_136 = b'ADD ER0,#0\x00'

BASIC_DATA_TEXT_137 = b'ADD ER0,ER0\x00'

BASIC_DATA_TEXT_138 = b'SUB R0,R0\x00'

BASIC_DATA_TEXT_139 = b'SUBC R0,R0\x00'

BASIC_DATA_TEXT_140 = b'SUB R0,#0\x00'

BASIC_DATA_TEXT_141 = b'AND R0,R0\x00'

BASIC_DATA_TEXT_142 = b'AND R0,#0\x00'

BASIC_DATA_TEXT_143 = b'OR R0,R0\x00'

BASIC_DATA_TEXT_144 = b'OR R0,#0\x00'

BASIC_DATA_TEXT_145 = b'XOR R0,R0\x00'

BASIC_DATA_TEXT_146 = b'XOR R0,#0\x00'

BASIC_DATA_TEXT_147 = b'SLL R0,R0\x00'

BASIC_DATA_TEXT_148 = b'SLL R0,#0\x00'

BASIC_DATA_TEXT_149 = b'SLLC R0,R0\x00'

BASIC_DATA_TEXT_150 = b'SLLC R0,#0\x00'

BASIC_DATA_TEXT_151 = b'SRL R0,R0\x00'

BASIC_DATA_TEXT_152 = b'SRL R0,#0\x00'

BASIC_DATA_TEXT_153 = b'SRLC R0,R0\x00'

BASIC_DATA_TEXT_154 = b'SRA R0,#0\x00'

BASIC_DATA_TEXT_155 = b'SRA R0,R0\x00'

BASIC_DATA_TEXT_156 = b'MUL ER0,R0\x00'

BASIC_DATA_TEXT_157 = b'DIV ER0,R0\x00'

BASIC_DATA_TEXT_158 = b'CMP R0,#0\x00'

BASIC_DATA_TEXT_159 = b'CMP R0,R0\x00'

BASIC_DATA_TEXT_160 = b'CMPC R0,#0\x00'

BASIC_DATA_TEXT_161 = b'CMPC R0,R0\x00'

BASIC_DATA_TEXT_162 = b'CMP ER0,ER0\x00'

BASIC_DATA_TEXT_163 = b'DAA R0\x00'

BASIC_DATA_TEXT_164 = b'DAS R0\x00'

BASIC_DATA_TEXT_165 = b'NEG R0\x00'

BASIC_DATA_TEXT_166 = b'MOV R,#\x00'

BASIC_DATA_TEXT_167 = b'MOV R,R\x00'

BASIC_DATA_TEXT_168 = b'MOV ER,ER\x00'

BASIC_DATA_TEXT_169 = b'MOV ER,SP\x00'

BASIC_DATA_TEXT_170 = b'MOV SP,ER\x00'

BASIC_DATA_TEXT_171 = b'MOV ER,#\x00'

BASIC_DATA_TEXT_172 = b'MOV R0,#0\x00'

BASIC_DATA_TEXT_173 = b'MOV R0,R0\x00'

BASIC_DATA_TEXT_174 = b'MOV ER0,ER0\x00'

BASIC_DATA_TEXT_175 = b'MOV ER0,SP\x00'

BASIC_DATA_TEXT_176 = b'MOV SP,ER0\x00'

BASIC_DATA_TEXT_177 = b'MOV ER0,#0\x00'

BASIC_DATA_TEXT_178 = b'BGE\x00'

BASIC_DATA_TEXT_179 = b'BLT\x00'

BASIC_DATA_TEXT_180 = b'BGT\x00'

BASIC_DATA_TEXT_181 = b'BLE\x00'

BASIC_DATA_TEXT_182 = b'BGES\x00'

BASIC_DATA_TEXT_183 = b'BLTS\x00'

BASIC_DATA_TEXT_184 = b'BGTS\x00'

BASIC_DATA_TEXT_185 = b'BLES\x00'

BASIC_DATA_TEXT_186 = b'BNE\x00'

BASIC_DATA_TEXT_187 = b'BEQ\x00'

BASIC_DATA_TEXT_188 = b'BNV\x00'

BASIC_DATA_TEXT_189 = b'BOV\x00'

BASIC_DATA_TEXT_190 = b'BPS\x00'

BASIC_DATA_TEXT_191 = b'BNS\x00'

BASIC_DATA_TEXT_192 = b'JMP\x00'

BASIC_DATA_TEXT_193 = b'BGE LABEL\x00'

BASIC_DATA_TEXT_194 = b'BLT LABEL\x00'

BASIC_DATA_TEXT_195 = b'BGT LABEL\x00'

BASIC_DATA_TEXT_196 = b'BLE LABEL\x00'

BASIC_DATA_TEXT_197 = b'BGES LABEL\x00'

BASIC_DATA_TEXT_198 = b'BLTS LABEL\x00'

BASIC_DATA_TEXT_199 = b'BGTS LABEL\x00'

BASIC_DATA_TEXT_200 = b'BLES LABEL\x00'

BASIC_DATA_TEXT_201 = b'BNE LABEL\x00'

BASIC_DATA_TEXT_202 = b'BEQ LABEL\x00'

BASIC_DATA_TEXT_203 = b'BNV LABEL\x00'

BASIC_DATA_TEXT_204 = b'BOV LABEL\x00'

BASIC_DATA_TEXT_205 = b'BPS LABEL\x00'

BASIC_DATA_TEXT_206 = b'BNS LABEL\x00'

BASIC_DATA_TEXT_207 = b'JMP LABEL\x00'

BASIC_DATA_TEXT_208 = b'CALL LABEL\x00'

BASIC_DATA_TEXT_209 = b'L R,ADDR\x00'

BASIC_DATA_TEXT_210 = b'L R,[ER]\x00'

BASIC_DATA_TEXT_211 = b'L R,D[ER]\x00'

BASIC_DATA_TEXT_212 = b'L ER,ADDR\x00'

BASIC_DATA_TEXT_213 = b'L ER,[ER]\x00'

BASIC_DATA_TEXT_214 = b'L ER,D[ER]\x00'

BASIC_DATA_TEXT_215 = b'ST R,ADDR\x00'

BASIC_DATA_TEXT_216 = b'ST R,[ER]\x00'

BASIC_DATA_TEXT_217 = b'ST R,D[ER]\x00'

BASIC_DATA_TEXT_218 = b'ST ER,ADDR\x00'

BASIC_DATA_TEXT_219 = b'ST ER,[ER]\x00'

BASIC_DATA_TEXT_220 = b'ST ER,D[ER]\x00'

BASIC_DATA_TEXT_221 = b'L R0,0\x00'

BASIC_DATA_TEXT_222 = b'L R0,[ER0]\x00'

BASIC_DATA_TEXT_223 = b'L R0,0[ER0]\x00'

BASIC_DATA_TEXT_224 = b'L ER0,0\x00'

BASIC_DATA_TEXT_225 = b'L ER0,[ER0]\x00'

BASIC_DATA_TEXT_226 = b'L ER0,0[ER0]\x00'

BASIC_DATA_TEXT_227 = b'ST R0,0\x00'

BASIC_DATA_TEXT_228 = b'ST R0,[ER0]\x00'

BASIC_DATA_TEXT_229 = b'ST R0,0[ER0]\x00'

BASIC_DATA_TEXT_230 = b'ST ER0,0\x00'

BASIC_DATA_TEXT_231 = b'ST ER0,[ER0]\x00'

BASIC_DATA_TEXT_232 = b'ST ER0,0[ER0]\x00'

BASIC_DATA_TEXT_233 = b'PUSH R\x00'

BASIC_DATA_TEXT_234 = b'PUSH ER\x00'

BASIC_DATA_TEXT_235 = b'POP R\x00'

BASIC_DATA_TEXT_236 = b'POP ER\x00'

BASIC_DATA_TEXT_237 = b'PUSH XR\x00'

BASIC_DATA_TEXT_238 = b'PUSH QR\x00'

BASIC_DATA_TEXT_239 = b'POP XR\x00'

BASIC_DATA_TEXT_240 = b'POP QR\x00'

BASIC_DATA_TEXT_241 = b'PUSH LR\x00'

BASIC_DATA_TEXT_242 = b'POP LR\x00'

BASIC_DATA_TEXT_243 = b'PUSH EA\x00'

BASIC_DATA_TEXT_244 = b'POP EA\x00'

BASIC_DATA_TEXT_245 = b'POP PC\x00'

BASIC_DATA_TEXT_246 = b'PUSH R0\x00'

BASIC_DATA_TEXT_247 = b'PUSH ER0\x00'

BASIC_DATA_TEXT_248 = b'POP R0\x00'

BASIC_DATA_TEXT_249 = b'POP ER0\x00'

BASIC_DATA_TEXT_250 = b'PUSH XR0\x00'

BASIC_DATA_TEXT_251 = b'PUSH QR0\x00'

BASIC_DATA_TEXT_252 = b'POP XR0\x00'

BASIC_DATA_TEXT_253 = b'POP QR0\x00'

BASIC_DATA_TEXT_254 = b'CALL_SYS\x00'

BASIC_DATA_TEXT_255 = b'TB R.B\x00'

BASIC_DATA_TEXT_256 = b'EXTBW ER\x00'

BASIC_DATA_TEXT_257 = b'ADD SP,#\x00'

BASIC_DATA_TEXT_258 = b'SC\x00'

BASIC_DATA_TEXT_259 = b'RC\x00'

BASIC_DATA_TEXT_260 = b'CPLC\x00'

BASIC_DATA_TEXT_261 = b'NOP\x00'

BASIC_DATA_TEXT_262 = b'RET\x00'

BASIC_DATA_TEXT_263 = b'END\x00'

BASIC_DATA_TEXT_264 = b'CALL_SYS 0\x00'

BASIC_DATA_TEXT_265 = b'TB R0.0\x00'

BASIC_DATA_TEXT_266 = b'EXTBW ER0\x00'

BASIC_DATA_TEXT_267 = b'ADD SP,#0\x00'

BASIC_DATA_TEXT_268 = b'BAD OPERAND\x00'

BASIC_DATA_TEXT_269 = b'DUP LABEL\x00'

BASIC_DATA_TEXT_270 = b'NO LABEL\x00'

BASIC_DATA_TEXT_271 = b'BR RANGE\x00'

BASIC_DATA_TEXT_272 = b'ADDRESS RANGE\x00'

BASIC_DATA_TEXT_273 = b'NO ENDASM\x00'

BASIC_DATA_TABLE = (
    BASIC_DATA_NAMES +
    BASIC_DATA_ARG_COUNTS +
    BASIC_DATA_ARG_TYPES +
    BASIC_DATA_NX_PAGE_NAME +
    BASIC_DATA_NX_CATEGORY_NAMES +
    BASIC_DATA_NX_ITEMS_0 +
    BASIC_DATA_NX_TOKENS_0 +
    BASIC_DATA_NX_ITEMS_1 +
    BASIC_DATA_NX_TOKENS_1 +
    BASIC_DATA_NX_ITEMS_2 +
    BASIC_DATA_NX_TOKENS_2 +
    BASIC_DATA_NX_ITEMS_3 +
    BASIC_DATA_NX_TOKENS_3 +
    BASIC_DATA_BLOCK_CATEGORIES_NAMES +
    BASIC_DATA_OP_CATEGORIES +
    BASIC_DATA_BLOCK_REGS +
    BASIC_DATA_BLOCK_REGS_TEXT +
    BASIC_DATA_BLOCK_SYMBOLS +
    BASIC_DATA_BLOCK_SYMBOLS_TEXT +
    BASIC_DATA_BLOCK_DIRECTIVES +
    BASIC_DATA_BLOCK_DIRECTIVES_TEXT +
    BASIC_DATA_OP_0 +
    BASIC_DATA_OP_0_TEXT +
    BASIC_DATA_OP_1 +
    BASIC_DATA_OP_1_TEXT +
    BASIC_DATA_OP_2 +
    BASIC_DATA_OP_2_TEXT +
    BASIC_DATA_OP_3 +
    BASIC_DATA_OP_3_TEXT +
    BASIC_DATA_OP_4 +
    BASIC_DATA_OP_4_TEXT +
    BASIC_DATA_OP_5 +
    BASIC_DATA_OP_5_TEXT +
    BASIC_DATA_ASM_REASONS +
    BASIC_DATA_WRITE_ERROR +
    BASIC_DATA_ASM_ERROR_TITLE +
    BASIC_DATA_ERROR_EXIT +
    BASIC_DATA_TEXT_0 +
    BASIC_DATA_TEXT_1 +
    BASIC_DATA_TEXT_2 +
    BASIC_DATA_TEXT_3 +
    BASIC_DATA_TEXT_4 +
    BASIC_DATA_TEXT_5 +
    BASIC_DATA_TEXT_6 +
    BASIC_DATA_TEXT_7 +
    BASIC_DATA_TEXT_8 +
    BASIC_DATA_TEXT_9 +
    BASIC_DATA_TEXT_10 +
    BASIC_DATA_TEXT_11 +
    BASIC_DATA_TEXT_12 +
    BASIC_DATA_TEXT_13 +
    BASIC_DATA_TEXT_14 +
    BASIC_DATA_TEXT_15 +
    BASIC_DATA_TEXT_16 +
    BASIC_DATA_TEXT_17 +
    BASIC_DATA_TEXT_18 +
    BASIC_DATA_TEXT_19 +
    BASIC_DATA_TEXT_20 +
    BASIC_DATA_TEXT_21 +
    BASIC_DATA_TEXT_22 +
    BASIC_DATA_TEXT_23 +
    BASIC_DATA_TEXT_24 +
    BASIC_DATA_TEXT_25 +
    BASIC_DATA_TEXT_26 +
    BASIC_DATA_TEXT_27 +
    BASIC_DATA_TEXT_28 +
    BASIC_DATA_TEXT_29 +
    BASIC_DATA_TEXT_30 +
    BASIC_DATA_TEXT_31 +
    BASIC_DATA_TEXT_32 +
    BASIC_DATA_TEXT_33 +
    BASIC_DATA_TEXT_34 +
    BASIC_DATA_TEXT_35 +
    BASIC_DATA_TEXT_36 +
    BASIC_DATA_TEXT_37 +
    BASIC_DATA_TEXT_38 +
    BASIC_DATA_TEXT_39 +
    BASIC_DATA_TEXT_40 +
    BASIC_DATA_TEXT_41 +
    BASIC_DATA_TEXT_42 +
    BASIC_DATA_TEXT_43 +
    BASIC_DATA_TEXT_44 +
    BASIC_DATA_TEXT_45 +
    BASIC_DATA_TEXT_46 +
    BASIC_DATA_TEXT_47 +
    BASIC_DATA_TEXT_48 +
    BASIC_DATA_TEXT_49 +
    BASIC_DATA_TEXT_50 +
    BASIC_DATA_TEXT_51 +
    BASIC_DATA_TEXT_52 +
    BASIC_DATA_TEXT_53 +
    BASIC_DATA_TEXT_54 +
    BASIC_DATA_TEXT_55 +
    BASIC_DATA_TEXT_56 +
    BASIC_DATA_TEXT_57 +
    BASIC_DATA_TEXT_58 +
    BASIC_DATA_TEXT_59 +
    BASIC_DATA_TEXT_60 +
    BASIC_DATA_TEXT_61 +
    BASIC_DATA_TEXT_62 +
    BASIC_DATA_TEXT_63 +
    BASIC_DATA_TEXT_64 +
    BASIC_DATA_TEXT_65 +
    BASIC_DATA_TEXT_66 +
    BASIC_DATA_TEXT_67 +
    BASIC_DATA_TEXT_68 +
    BASIC_DATA_TEXT_69 +
    BASIC_DATA_TEXT_70 +
    BASIC_DATA_TEXT_71 +
    BASIC_DATA_TEXT_72 +
    BASIC_DATA_TEXT_73 +
    BASIC_DATA_TEXT_74 +
    BASIC_DATA_TEXT_75 +
    BASIC_DATA_TEXT_76 +
    BASIC_DATA_TEXT_77 +
    BASIC_DATA_TEXT_78 +
    BASIC_DATA_TEXT_79 +
    BASIC_DATA_TEXT_80 +
    BASIC_DATA_TEXT_81 +
    BASIC_DATA_TEXT_82 +
    BASIC_DATA_TEXT_83 +
    BASIC_DATA_TEXT_84 +
    BASIC_DATA_TEXT_85 +
    BASIC_DATA_TEXT_86 +
    BASIC_DATA_TEXT_87 +
    BASIC_DATA_TEXT_88 +
    BASIC_DATA_TEXT_89 +
    BASIC_DATA_TEXT_90 +
    BASIC_DATA_TEXT_91 +
    BASIC_DATA_TEXT_92 +
    BASIC_DATA_TEXT_93 +
    BASIC_DATA_TEXT_94 +
    BASIC_DATA_TEXT_95 +
    BASIC_DATA_TEXT_96 +
    BASIC_DATA_TEXT_97 +
    BASIC_DATA_TEXT_98 +
    BASIC_DATA_TEXT_99 +
    BASIC_DATA_TEXT_100 +
    BASIC_DATA_TEXT_101 +
    BASIC_DATA_TEXT_102 +
    BASIC_DATA_TEXT_103 +
    BASIC_DATA_TEXT_104 +
    BASIC_DATA_TEXT_105 +
    BASIC_DATA_TEXT_106 +
    BASIC_DATA_TEXT_107 +
    BASIC_DATA_TEXT_108 +
    BASIC_DATA_TEXT_109 +
    BASIC_DATA_TEXT_110 +
    BASIC_DATA_TEXT_111 +
    BASIC_DATA_TEXT_112 +
    BASIC_DATA_TEXT_113 +
    BASIC_DATA_TEXT_114 +
    BASIC_DATA_TEXT_115 +
    BASIC_DATA_TEXT_116 +
    BASIC_DATA_TEXT_117 +
    BASIC_DATA_TEXT_118 +
    BASIC_DATA_TEXT_119 +
    BASIC_DATA_TEXT_120 +
    BASIC_DATA_TEXT_121 +
    BASIC_DATA_TEXT_122 +
    BASIC_DATA_TEXT_123 +
    BASIC_DATA_TEXT_124 +
    BASIC_DATA_TEXT_125 +
    BASIC_DATA_TEXT_126 +
    BASIC_DATA_TEXT_127 +
    BASIC_DATA_TEXT_128 +
    BASIC_DATA_TEXT_129 +
    BASIC_DATA_TEXT_130 +
    BASIC_DATA_TEXT_131 +
    BASIC_DATA_TEXT_132 +
    BASIC_DATA_TEXT_133 +
    BASIC_DATA_TEXT_134 +
    BASIC_DATA_TEXT_135 +
    BASIC_DATA_TEXT_136 +
    BASIC_DATA_TEXT_137 +
    BASIC_DATA_TEXT_138 +
    BASIC_DATA_TEXT_139 +
    BASIC_DATA_TEXT_140 +
    BASIC_DATA_TEXT_141 +
    BASIC_DATA_TEXT_142 +
    BASIC_DATA_TEXT_143 +
    BASIC_DATA_TEXT_144 +
    BASIC_DATA_TEXT_145 +
    BASIC_DATA_TEXT_146 +
    BASIC_DATA_TEXT_147 +
    BASIC_DATA_TEXT_148 +
    BASIC_DATA_TEXT_149 +
    BASIC_DATA_TEXT_150 +
    BASIC_DATA_TEXT_151 +
    BASIC_DATA_TEXT_152 +
    BASIC_DATA_TEXT_153 +
    BASIC_DATA_TEXT_154 +
    BASIC_DATA_TEXT_155 +
    BASIC_DATA_TEXT_156 +
    BASIC_DATA_TEXT_157 +
    BASIC_DATA_TEXT_158 +
    BASIC_DATA_TEXT_159 +
    BASIC_DATA_TEXT_160 +
    BASIC_DATA_TEXT_161 +
    BASIC_DATA_TEXT_162 +
    BASIC_DATA_TEXT_163 +
    BASIC_DATA_TEXT_164 +
    BASIC_DATA_TEXT_165 +
    BASIC_DATA_TEXT_166 +
    BASIC_DATA_TEXT_167 +
    BASIC_DATA_TEXT_168 +
    BASIC_DATA_TEXT_169 +
    BASIC_DATA_TEXT_170 +
    BASIC_DATA_TEXT_171 +
    BASIC_DATA_TEXT_172 +
    BASIC_DATA_TEXT_173 +
    BASIC_DATA_TEXT_174 +
    BASIC_DATA_TEXT_175 +
    BASIC_DATA_TEXT_176 +
    BASIC_DATA_TEXT_177 +
    BASIC_DATA_TEXT_178 +
    BASIC_DATA_TEXT_179 +
    BASIC_DATA_TEXT_180 +
    BASIC_DATA_TEXT_181 +
    BASIC_DATA_TEXT_182 +
    BASIC_DATA_TEXT_183 +
    BASIC_DATA_TEXT_184 +
    BASIC_DATA_TEXT_185 +
    BASIC_DATA_TEXT_186 +
    BASIC_DATA_TEXT_187 +
    BASIC_DATA_TEXT_188 +
    BASIC_DATA_TEXT_189 +
    BASIC_DATA_TEXT_190 +
    BASIC_DATA_TEXT_191 +
    BASIC_DATA_TEXT_192 +
    BASIC_DATA_TEXT_193 +
    BASIC_DATA_TEXT_194 +
    BASIC_DATA_TEXT_195 +
    BASIC_DATA_TEXT_196 +
    BASIC_DATA_TEXT_197 +
    BASIC_DATA_TEXT_198 +
    BASIC_DATA_TEXT_199 +
    BASIC_DATA_TEXT_200 +
    BASIC_DATA_TEXT_201 +
    BASIC_DATA_TEXT_202 +
    BASIC_DATA_TEXT_203 +
    BASIC_DATA_TEXT_204 +
    BASIC_DATA_TEXT_205 +
    BASIC_DATA_TEXT_206 +
    BASIC_DATA_TEXT_207 +
    BASIC_DATA_TEXT_208 +
    BASIC_DATA_TEXT_209 +
    BASIC_DATA_TEXT_210 +
    BASIC_DATA_TEXT_211 +
    BASIC_DATA_TEXT_212 +
    BASIC_DATA_TEXT_213 +
    BASIC_DATA_TEXT_214 +
    BASIC_DATA_TEXT_215 +
    BASIC_DATA_TEXT_216 +
    BASIC_DATA_TEXT_217 +
    BASIC_DATA_TEXT_218 +
    BASIC_DATA_TEXT_219 +
    BASIC_DATA_TEXT_220 +
    BASIC_DATA_TEXT_221 +
    BASIC_DATA_TEXT_222 +
    BASIC_DATA_TEXT_223 +
    BASIC_DATA_TEXT_224 +
    BASIC_DATA_TEXT_225 +
    BASIC_DATA_TEXT_226 +
    BASIC_DATA_TEXT_227 +
    BASIC_DATA_TEXT_228 +
    BASIC_DATA_TEXT_229 +
    BASIC_DATA_TEXT_230 +
    BASIC_DATA_TEXT_231 +
    BASIC_DATA_TEXT_232 +
    BASIC_DATA_TEXT_233 +
    BASIC_DATA_TEXT_234 +
    BASIC_DATA_TEXT_235 +
    BASIC_DATA_TEXT_236 +
    BASIC_DATA_TEXT_237 +
    BASIC_DATA_TEXT_238 +
    BASIC_DATA_TEXT_239 +
    BASIC_DATA_TEXT_240 +
    BASIC_DATA_TEXT_241 +
    BASIC_DATA_TEXT_242 +
    BASIC_DATA_TEXT_243 +
    BASIC_DATA_TEXT_244 +
    BASIC_DATA_TEXT_245 +
    BASIC_DATA_TEXT_246 +
    BASIC_DATA_TEXT_247 +
    BASIC_DATA_TEXT_248 +
    BASIC_DATA_TEXT_249 +
    BASIC_DATA_TEXT_250 +
    BASIC_DATA_TEXT_251 +
    BASIC_DATA_TEXT_252 +
    BASIC_DATA_TEXT_253 +
    BASIC_DATA_TEXT_254 +
    BASIC_DATA_TEXT_255 +
    BASIC_DATA_TEXT_256 +
    BASIC_DATA_TEXT_257 +
    BASIC_DATA_TEXT_258 +
    BASIC_DATA_TEXT_259 +
    BASIC_DATA_TEXT_260 +
    BASIC_DATA_TEXT_261 +
    BASIC_DATA_TEXT_262 +
    BASIC_DATA_TEXT_263 +
    BASIC_DATA_TEXT_264 +
    BASIC_DATA_TEXT_265 +
    BASIC_DATA_TEXT_266 +
    BASIC_DATA_TEXT_267 +
    BASIC_DATA_TEXT_268 +
    BASIC_DATA_TEXT_269 +
    BASIC_DATA_TEXT_270 +
    BASIC_DATA_TEXT_271 +
    BASIC_DATA_TEXT_272 +
    BASIC_DATA_TEXT_273
)

BASIC_DATA_LABELS = {
    'basic_data': 0x0,
    'names': 0x0,
    'arg_counts': 0x32,
    'arg_types': 0x4B,
    'nx_page_name': 0xE2,
    'nx_category_names': 0xE4,
    'nx_items_0': 0xEC,
    'nx_tokens_0': 0xFA,
    'nx_items_1': 0x102,
    'nx_tokens_1': 0x108,
    'nx_items_2': 0x10C,
    'nx_tokens_2': 0x11C,
    'nx_items_3': 0x124,
    'nx_tokens_3': 0x132,
    'block_categories_names': 0x13A,
    'op_categories': 0x142,
    'block_regs': 0x14E,
    'block_regs_text': 0x190,
    'block_symbols': 0x1D2,
    'block_symbols_text': 0x1FA,
    'block_directives': 0x222,
    'block_directives_text': 0x228,
    'op_0': 0x22E,
    'op_0_text': 0x272,
    'op_1': 0x2B6,
    'op_1_text': 0x2C2,
    'op_2': 0x2CE,
    'op_2_text': 0x2EE,
    'op_3': 0x30E,
    'op_3_text': 0x326,
    'op_4': 0x33E,
    'op_4_text': 0x358,
    'op_5': 0x372,
    'op_5_text': 0x386,
    'asm_reasons': 0x39A,
    'write_error': 0x3A6,
    'asm_error_title': 0x3B2,
    'error_exit': 0x3BC,
    'text_0': 0x3C1,
    'text_1': 0x3C6,
    'text_2': 0x3CD,
    'text_3': 0x3D2,
    'text_4': 0x3D9,
    'text_5': 0x3DE,
    'text_6': 0x3E3,
    'text_7': 0x3E7,
    'text_8': 0x3EC,
    'text_9': 0x3F0,
    'text_10': 0x3F4,
    'text_11': 0x3FA,
    'text_12': 0x400,
    'text_13': 0x406,
    'text_14': 0x40B,
    'text_15': 0x410,
    'text_16': 0x41B,
    'text_17': 0x41F,
    'text_18': 0x424,
    'text_19': 0x429,
    'text_20': 0x42E,
    'text_21': 0x433,
    'text_22': 0x438,
    'text_23': 0x440,
    'text_24': 0x444,
    'text_25': 0x44B,
    'text_26': 0x44E,
    'text_27': 0x452,
    'text_28': 0x456,
    'text_29': 0x45C,
    'text_30': 0x45F,
    'text_31': 0x463,
    'text_32': 0x467,
    'text_33': 0x46D,
    'text_34': 0x473,
    'text_35': 0x478,
    'text_36': 0x47F,
    'text_37': 0x487,
    'text_38': 0x48D,
    'text_39': 0x492,
    'text_40': 0x495,
    'text_41': 0x498,
    'text_42': 0x49B,
    'text_43': 0x49E,
    'text_44': 0x4A1,
    'text_45': 0x4A4,
    'text_46': 0x4A7,
    'text_47': 0x4AA,
    'text_48': 0x4AD,
    'text_49': 0x4B0,
    'text_50': 0x4B4,
    'text_51': 0x4B8,
    'text_52': 0x4BC,
    'text_53': 0x4C0,
    'text_54': 0x4C4,
    'text_55': 0x4C8,
    'text_56': 0x4CC,
    'text_57': 0x4D0,
    'text_58': 0x4D4,
    'text_59': 0x4D8,
    'text_60': 0x4DC,
    'text_61': 0x4E1,
    'text_62': 0x4E6,
    'text_63': 0x4EB,
    'text_64': 0x4EF,
    'text_65': 0x4F3,
    'text_66': 0x4F7,
    'text_67': 0x4FC,
    'text_68': 0x500,
    'text_69': 0x504,
    'text_70': 0x507,
    'text_71': 0x50A,
    'text_72': 0x50D,
    'text_73': 0x513,
    'text_74': 0x515,
    'text_75': 0x517,
    'text_76': 0x519,
    'text_77': 0x51B,
    'text_78': 0x51D,
    'text_79': 0x51F,
    'text_80': 0x521,
    'text_81': 0x523,
    'text_82': 0x525,
    'text_83': 0x527,
    'text_84': 0x529,
    'text_85': 0x52B,
    'text_86': 0x52D,
    'text_87': 0x52F,
    'text_88': 0x531,
    'text_89': 0x533,
    'text_90': 0x535,
    'text_91': 0x537,
    'text_92': 0x539,
    'text_93': 0x53B,
    'text_94': 0x53E,
    'text_95': 0x541,
    'text_96': 0x545,
    'text_97': 0x549,
    'text_98': 0x54D,
    'text_99': 0x555,
    'text_100': 0x55D,
    'text_101': 0x566,
    'text_102': 0x56F,
    'text_103': 0x578,
    'text_104': 0x582,
    'text_105': 0x58A,
    'text_106': 0x593,
    'text_107': 0x59B,
    'text_108': 0x5A3,
    'text_109': 0x5AB,
    'text_110': 0x5B2,
    'text_111': 0x5B9,
    'text_112': 0x5C1,
    'text_113': 0x5C9,
    'text_114': 0x5D1,
    'text_115': 0x5D9,
    'text_116': 0x5E2,
    'text_117': 0x5EB,
    'text_118': 0x5F3,
    'text_119': 0x5FB,
    'text_120': 0x604,
    'text_121': 0x60C,
    'text_122': 0x614,
    'text_123': 0x61D,
    'text_124': 0x626,
    'text_125': 0x62E,
    'text_126': 0x636,
    'text_127': 0x63F,
    'text_128': 0x648,
    'text_129': 0x652,
    'text_130': 0x658,
    'text_131': 0x65E,
    'text_132': 0x664,
    'text_133': 0x66E,
    'text_134': 0x678,
    'text_135': 0x683,
    'text_136': 0x68E,
    'text_137': 0x699,
    'text_138': 0x6A5,
    'text_139': 0x6AF,
    'text_140': 0x6BA,
    'text_141': 0x6C4,
    'text_142': 0x6CE,
    'text_143': 0x6D8,
    'text_144': 0x6E1,
    'text_145': 0x6EA,
    'text_146': 0x6F4,
    'text_147': 0x6FE,
    'text_148': 0x708,
    'text_149': 0x712,
    'text_150': 0x71D,
    'text_151': 0x728,
    'text_152': 0x732,
    'text_153': 0x73C,
    'text_154': 0x747,
    'text_155': 0x751,
    'text_156': 0x75B,
    'text_157': 0x766,
    'text_158': 0x771,
    'text_159': 0x77B,
    'text_160': 0x785,
    'text_161': 0x790,
    'text_162': 0x79B,
    'text_163': 0x7A7,
    'text_164': 0x7AE,
    'text_165': 0x7B5,
    'text_166': 0x7BC,
    'text_167': 0x7C4,
    'text_168': 0x7CC,
    'text_169': 0x7D6,
    'text_170': 0x7E0,
    'text_171': 0x7EA,
    'text_172': 0x7F3,
    'text_173': 0x7FD,
    'text_174': 0x807,
    'text_175': 0x813,
    'text_176': 0x81E,
    'text_177': 0x829,
    'text_178': 0x834,
    'text_179': 0x838,
    'text_180': 0x83C,
    'text_181': 0x840,
    'text_182': 0x844,
    'text_183': 0x849,
    'text_184': 0x84E,
    'text_185': 0x853,
    'text_186': 0x858,
    'text_187': 0x85C,
    'text_188': 0x860,
    'text_189': 0x864,
    'text_190': 0x868,
    'text_191': 0x86C,
    'text_192': 0x870,
    'text_193': 0x874,
    'text_194': 0x87E,
    'text_195': 0x888,
    'text_196': 0x892,
    'text_197': 0x89C,
    'text_198': 0x8A7,
    'text_199': 0x8B2,
    'text_200': 0x8BD,
    'text_201': 0x8C8,
    'text_202': 0x8D2,
    'text_203': 0x8DC,
    'text_204': 0x8E6,
    'text_205': 0x8F0,
    'text_206': 0x8FA,
    'text_207': 0x904,
    'text_208': 0x90E,
    'text_209': 0x919,
    'text_210': 0x922,
    'text_211': 0x92B,
    'text_212': 0x935,
    'text_213': 0x93F,
    'text_214': 0x949,
    'text_215': 0x954,
    'text_216': 0x95E,
    'text_217': 0x968,
    'text_218': 0x973,
    'text_219': 0x97E,
    'text_220': 0x989,
    'text_221': 0x995,
    'text_222': 0x99C,
    'text_223': 0x9A7,
    'text_224': 0x9B3,
    'text_225': 0x9BB,
    'text_226': 0x9C7,
    'text_227': 0x9D4,
    'text_228': 0x9DC,
    'text_229': 0x9E8,
    'text_230': 0x9F5,
    'text_231': 0x9FE,
    'text_232': 0xA0B,
    'text_233': 0xA19,
    'text_234': 0xA20,
    'text_235': 0xA28,
    'text_236': 0xA2E,
    'text_237': 0xA35,
    'text_238': 0xA3D,
    'text_239': 0xA45,
    'text_240': 0xA4C,
    'text_241': 0xA53,
    'text_242': 0xA5B,
    'text_243': 0xA62,
    'text_244': 0xA6A,
    'text_245': 0xA71,
    'text_246': 0xA78,
    'text_247': 0xA80,
    'text_248': 0xA89,
    'text_249': 0xA90,
    'text_250': 0xA98,
    'text_251': 0xAA1,
    'text_252': 0xAAA,
    'text_253': 0xAB2,
    'text_254': 0xABA,
    'text_255': 0xAC3,
    'text_256': 0xACA,
    'text_257': 0xAD3,
    'text_258': 0xADC,
    'text_259': 0xADF,
    'text_260': 0xAE2,
    'text_261': 0xAE7,
    'text_262': 0xAEB,
    'text_263': 0xAEF,
    'text_264': 0xAF3,
    'text_265': 0xAFE,
    'text_266': 0xB06,
    'text_267': 0xB10,
    'text_268': 0xB1A,
    'text_269': 0xB26,
    'text_270': 0xB30,
    'text_271': 0xB39,
    'text_272': 0xB42,
    'text_273': 0xB50,
}


def install(fw):
    fw.data('basic_data', BASIC_DATA_TABLE, address=0xF57DA, labels=BASIC_DATA_LABELS)

    @fw.function(native=True, address=0xF3E68)
    def basic():
        cpu.label('basic')
        cpu.label('admit')
        cpu.push(cpu.lr)
        cpu.push(cpu.er4)
        cpu.er4 = cpu.er0
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.compare(cpu.r0, 0xF9)
        if cpu.ne:
            cpu.branch('cond_11')
        cpu.r0 = cpu.mem8[cpu.r2, cpu.offset(cpu.er4, 0x0001)]
        cpu.compare(cpu.r0, 0xE0)
        if cpu.ne:
            cpu.branch('cond_1')
        cpu.jump('admit_yes')
        cpu.label('cond_1')
        cpu.compare(cpu.r0, 0xE1)
        if cpu.ne:
            cpu.branch('cond_2')
        cpu.jump('admit_yes')
        cpu.label('cond_2')
        cpu.compare(cpu.r0, 0xE4)
        if cpu.ne:
            cpu.branch('cond_3')
        cpu.jump('admit_yes')
        cpu.label('cond_3')
        cpu.compare(cpu.r0, 0xE5)
        if cpu.ne:
            cpu.branch('cond_4')
        cpu.jump('admit_yes')
        cpu.label('cond_4')
        cpu.compare(cpu.r0, 0xE6)
        if cpu.ne:
            cpu.branch('cond_5')
        cpu.jump('admit_yes')
        cpu.label('cond_5')
        cpu.compare(cpu.r0, 0xE7)
        if cpu.ne:
            cpu.branch('cond_6')
        cpu.jump('admit_yes')
        cpu.label('cond_6')
        cpu.compare(cpu.r0, 0xE8)
        if cpu.ne:
            cpu.branch('cond_7')
        cpu.jump('admit_yes')
        cpu.label('cond_7')
        cpu.compare(cpu.r0, 0xE9)
        if cpu.ne:
            cpu.branch('cond_8')
        cpu.jump('admit_yes')
        cpu.label('cond_8')
        cpu.compare(cpu.r0, 0xEA)
        if cpu.ne:
            cpu.branch('cond_9')
        cpu.jump('admit_yes')
        cpu.label('cond_9')
        cpu.compare(cpu.r0, 0xEB)
        if cpu.ne:
            cpu.branch('cond_10')
        cpu.jump('admit_yes')
        cpu.label('cond_10')
        cpu.compare(cpu.r0, 0xEC)
        if cpu.ne:
            cpu.branch('cond_11')
        cpu.jump('admit_yes')
        cpu.label('cond_11')
        cpu.label('admit_native')
        cpu.er0 = cpu.er4
        cpu.call(NATIVE_TOKEN_ADMISSION)
        cpu.pop(cpu.er4)
        cpu.pop(cpu.pc)
        cpu.label('admit_yes')
        cpu.er0 = 0x01
        cpu.pop(cpu.er4)
        cpu.pop(cpu.pc)
        cpu.label('spell')
        cpu.compare(cpu.r1, 0xFE)
        if cpu.ne:
            cpu.branch('spell_token')
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er2, 0x0001)] = cpu.r0
        cpu.er0 = cpu.er2
        cpu.ret()
        cpu.label('spell_token')
        cpu.compare(cpu.r1, 0xF9)
        if cpu.ne:
            cpu.branch('spell_native')
        cpu.compare(cpu.r0, 0xE0)
        if cpu.lt:
            cpu.branch('spell_native')
        cpu.compare(cpu.r0, 0xF9)
        if cpu.ge:
            cpu.branch('spell_native')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.er4 = cpu.er2
        cpu.r0 += 0x20
        cpu.r1 = 0x00
        cpu.shift_left_carry(cpu.r1, 0x01)
        cpu.r0 <<= 0x01
        cpu.r6 = 0xDA
        cpu.r7 = 0x57
        cpu.er6 += cpu.er0
        cpu.er6 = cpu.mem16[0x0F, cpu.er6]
        cpu.label('spell_copy')
        cpu.r0 = cpu.mem8[0x0F, cpu.er6]
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.er6 += 0x01
        cpu.er2 += 0x01
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('spell_copy')
        cpu.er0 = cpu.er4
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('spell_native')
        cpu.push(cpu.lr)
        cpu.push(cpu.er12)
        cpu.jump(0xDFC06)
        cpu.label('function')
        cpu.compare(cpu.r1, 0xF9)
        if cpu.ne:
            cpu.branch('function_native')
        cpu.compare(cpu.r0, 0xE0)
        if cpu.lt:
            cpu.branch('function_native')
        cpu.compare(cpu.r0, 0xF9)
        if cpu.ge:
            cpu.branch('function_native')
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er12 = cpu.er14
        cpu.sp += -16
        cpu.er14 = cpu.sp
        cpu.r0 += 0x20
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x000C)] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x000D)] = cpu.r0
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0000)] = cpu.er8
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0002)] = cpu.r10
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er12, 0x0006)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0004)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er12, 0x0008)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0006)] = cpu.r0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er12, 0x000A)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0008)] = cpu.er0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x000A)] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.call('command')
        cpu.sp += 0x10
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.er4 = cpu.er0
        cpu.jump(0xC72CE)
        cpu.label('function_native')
        cpu.compare(cpu.r0, 0x5B)
        cpu.compare_carry(cpu.r1, 0x00)
        cpu.jump(0xC7202)
        cpu.label('statement')
        cpu.er0 = cpu.mem16[cpu.r10, cpu.er8]
        cpu.r2 = cpu.mem8[cpu.r10, cpu.offset(cpu.er8, 0x0002)]
        cpu.r3 = cpu.mem8[cpu.r2, cpu.er0]
        cpu.compare(cpu.r3, 0xF9)
        if cpu.eq:
            cpu.branch('cond_12')
        cpu.jump('statement_native')
        cpu.label('cond_12')
        cpu.r3 = cpu.mem8[cpu.r2, cpu.offset(cpu.er0, 0x0001)]
        cpu.compare(cpu.r3, 0xE0)
        if cpu.ge:
            cpu.branch('cond_13')
        cpu.jump('statement_native')
        cpu.label('cond_13')
        cpu.compare(cpu.r3, 0xF9)
        if cpu.lt:
            cpu.branch('cond_14')
        cpu.jump('statement_native')
        cpu.label('cond_14')
        cpu.compare(cpu.r3, 0xE0)
        if cpu.ne:
            cpu.branch('cond_15')
        cpu.jump('statement_expression')
        cpu.label('cond_15')
        cpu.compare(cpu.r3, 0xE1)
        if cpu.ne:
            cpu.branch('cond_16')
        cpu.jump('statement_expression')
        cpu.label('cond_16')
        cpu.compare(cpu.r3, 0xE4)
        if cpu.ne:
            cpu.branch('cond_17')
        cpu.jump('statement_expression')
        cpu.label('cond_17')
        cpu.compare(cpu.r3, 0xE5)
        if cpu.ne:
            cpu.branch('cond_18')
        cpu.jump('statement_expression')
        cpu.label('cond_18')
        cpu.compare(cpu.r3, 0xE6)
        if cpu.ne:
            cpu.branch('cond_19')
        cpu.jump('statement_expression')
        cpu.label('cond_19')
        cpu.compare(cpu.r3, 0xE7)
        if cpu.ne:
            cpu.branch('cond_20')
        cpu.jump('statement_expression')
        cpu.label('cond_20')
        cpu.compare(cpu.r3, 0xE8)
        if cpu.ne:
            cpu.branch('cond_21')
        cpu.jump('statement_expression')
        cpu.label('cond_21')
        cpu.compare(cpu.r3, 0xE9)
        if cpu.ne:
            cpu.branch('cond_22')
        cpu.jump('statement_expression')
        cpu.label('cond_22')
        cpu.compare(cpu.r3, 0xEA)
        if cpu.ne:
            cpu.branch('cond_23')
        cpu.jump('statement_expression')
        cpu.label('cond_23')
        cpu.compare(cpu.r3, 0xEB)
        if cpu.ne:
            cpu.branch('cond_24')
        cpu.jump('statement_expression')
        cpu.label('cond_24')
        cpu.compare(cpu.r3, 0xEC)
        if cpu.ne:
            cpu.branch('cond_25')
        cpu.jump('statement_expression')
        cpu.label('cond_25')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000E)]
        cpu.r2 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er0, 0x0026)] = cpu.r2
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er12 = cpu.er14
        cpu.sp += -16
        cpu.er14 = cpu.sp
        cpu.r3 += 0x20
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x000C)] = cpu.r3
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x000D)] = cpu.r0
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0000)] = cpu.er8
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0002)] = cpu.r10
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er12, 0x0006)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0004)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er12, 0x0008)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0006)] = cpu.r0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er12, 0x000A)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0008)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er12, 0x000C)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x000A)] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.call('command')
        cpu.sp += 0x10
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.r4 = cpu.r0
        cpu.jump(0xCD7CA)
        cpu.label('statement_expression')
        cpu.er0 = 0x02
        cpu.jump(0xCD69E)
        cpu.label('statement_native')
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.jump(0xCD69A)
        cpu.label('command')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er12 = cpu.er2
        cpu.er0 = cpu.sp
        cpu.r2 = 0x26
        cpu.r3 = 0x87
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('cond_26')
        cpu.jump('command_no_stack')
        cpu.label('cond_26')
        cpu.sp += -128
        cpu.sp += -128
        cpu.sp += -16
        cpu.er14 = cpu.sp
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er12, 0x0000)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00C6)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er12, 0x0002)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00C8)] = cpu.r0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er12, 0x0004)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00CA)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er12, 0x0006)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00CC)] = cpu.r0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er12, 0x0008)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00CE)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er12, 0x000A)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D0)] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er12, 0x000C)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D2)] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er12, 0x000D)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D3)] = cpu.r0
        cpu.r0 = 0x00
        cpu.r1 = 0x80
        cpu.er2 = cpu.er14
        cpu.r4 = 0x70
        cpu.r5 = 0x00
        cpu.call('near_copy')
        cpu.er0 = cpu.mem16[0x00, 0x8086]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0070)] = cpu.er0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3F
        cpu.er2 += 0x35
        cpu.er4 = 0x1C
        cpu.r0 = 0x00
        cpu.label('command_clear')
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.er2 += 0x01
        cpu.er4 += -1
        if cpu.ne:
            cpu.branch('command_clear')
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D4)] = cpu.r0
        cpu.call('cursor')
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00D6)] = cpu.er0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D8)] = cpu.r2
        cpu.r3 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D3)]
        cpu.compare(cpu.r3, 0x00)
        if cpu.ne:
            cpu.branch('command_cached')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00CA)]
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00CC)]
        cpu.r3 = 0x01
        cpu.mem8[cpu.r2, cpu.er0] = cpu.r3
        cpu.call('fetch')
        cpu.jump('command_ready')
        cpu.label('command_cached')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00D6)]
        cpu.er0 += -2
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00D6)] = cpu.er0
        cpu.label('command_ready')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D2)]
        cpu.compare(cpu.r0, 0x17)
        if cpu.ne:
            cpu.branch('cond_27')
        cpu.jump('command_asm')
        cpu.label('cond_27')
        cpu.compare(cpu.r0, 0x18)
        if cpu.ne:
            cpu.branch('cond_28')
        cpu.jump('syntax')
        cpu.label('cond_28')
        cpu.r1 = 0x00
        cpu.r2 = 0x0C
        cpu.r3 = 0x58
        cpu.er2 += cpu.er0
        cpu.r0 = cpu.mem8[0x0F, cpu.er2]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D5)] = cpu.r0
        cpu.call('fetch_spaces')
        cpu.r3 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D3)]
        cpu.compare(cpu.r3, 0x00)
        if cpu.eq:
            cpu.branch('command_arguments')
        cpu.compare(cpu.r0, 0x28)
        if cpu.eq:
            cpu.branch('cond_29')
        cpu.jump('syntax')
        cpu.label('cond_29')
        cpu.call('fetch_spaces')
        cpu.label('command_arguments')
        cpu.r3 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D5)]
        cpu.compare(cpu.r3, 0x00)
        if cpu.ne:
            cpu.branch('cond_30')
        cpu.jump('command_end_args')
        cpu.label('cond_30')
        cpu.label('argument')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D2)]
        cpu.compare(cpu.r0, 0x15)
        if cpu.ne:
            cpu.branch('cond_31')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D4)]
        cpu.compare(cpu.r0, 0x02)
        if cpu.ne:
            cpu.branch('cond_31')
        cpu.jump('argument_text')
        cpu.label('cond_31')
        cpu.label('argument_number')
        cpu.er0 = 0x00
        cpu.push(cpu.er0)
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x12
        cpu.push(cpu.er0)
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00CC)]
        cpu.r1 = 0x00
        cpu.push(cpu.er0)
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00CA)]
        cpu.push(cpu.er0)
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00C6)]
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00C8)]
        cpu.r3 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D3)]
        cpu.compare(cpu.r3, 0x00)
        if cpu.eq:
            cpu.branch('argument_statement')
        cpu.call('evaluate_argument')
        cpu.jump('argument_evaluated')
        cpu.label('argument_statement')
        cpu.call(NATIVE_EVALUATE)
        cpu.label('argument_evaluated')
        cpu.sp += 0x0A
        cpu.compare(cpu.r0, 0x01)
        if cpu.eq:
            cpu.branch('cond_32')
        cpu.jump('argument_native_error')
        cpu.label('cond_32')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D2)]
        cpu.r1 = 0x00
        cpu.er2 = 0x06
        cpu.multiply(cpu.er0, cpu.r2)
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D4)]
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.r2 = 0x25
        cpu.r3 = 0x58
        cpu.er2 += cpu.er0
        cpu.r2 = cpu.mem8[0x0F, cpu.er2]
        cpu.r3 = 0x00
        cpu.r4 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D4)]
        cpu.r5 = 0x00
        cpu.shift_left_carry(cpu.r5, 0x02)
        cpu.r4 <<= 0x02
        cpu.er0 = cpu.er14
        cpu.er0 += 0x3F
        cpu.er0 += 0x35
        cpu.er4 += cpu.er0
        cpu.er0 = cpu.er14
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x12
        cpu.call(0xFB534)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cond_33')
        cpu.jump('command_error')
        cpu.label('cond_33')
        cpu.label('argument_done')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D4)]
        cpu.r0 += 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D4)] = cpu.r0
        cpu.r1 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D5)]
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.ne:
            cpu.branch('cond_34')
        cpu.jump('command_end_args')
        cpu.label('cond_34')
        cpu.call('cached')
        cpu.compare(cpu.r0, 0x29)
        if cpu.ne:
            cpu.branch('cond_35')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D2)]
        cpu.compare(cpu.r0, 0x04)
        if cpu.ne:
            cpu.branch('cond_35')
        cpu.jump('command_end_args')
        cpu.label('cond_35')
        cpu.label('argument_comma')
        cpu.call('cached')
        cpu.compare(cpu.r0, 0x2C)
        if cpu.eq:
            cpu.branch('cond_36')
        cpu.jump('syntax')
        cpu.label('cond_36')
        cpu.call('fetch_spaces')
        cpu.jump('cond_30')
        cpu.label('command_end_args')
        cpu.call('cached')
        cpu.r3 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D3)]
        cpu.compare(cpu.r3, 0x00)
        if cpu.eq:
            cpu.branch('command_boundary')
        cpu.compare(cpu.r0, 0x29)
        if cpu.eq:
            cpu.branch('cond_37')
        cpu.jump('syntax')
        cpu.label('cond_37')
        cpu.call('fetch')
        cpu.jump('command_dispatch')
        cpu.label('command_boundary')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('cond_38')
        cpu.jump('command_dispatch')
        cpu.label('cond_38')
        cpu.compare(cpu.r0, 0x0C)
        if cpu.ne:
            cpu.branch('cond_39')
        cpu.jump('command_dispatch')
        cpu.label('cond_39')
        cpu.compare(cpu.r0, 0x0D)
        if cpu.ne:
            cpu.branch('cond_40')
        cpu.jump('command_dispatch')
        cpu.label('cond_40')
        cpu.compare(cpu.r0, 0x3A)
        if cpu.ne:
            cpu.branch('cond_41')
        cpu.jump('command_dispatch')
        cpu.label('cond_41')
        cpu.jump('syntax')
        cpu.label('command_dispatch')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D2)]
        cpu.r1 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3F
        cpu.er2 += 0x35
        cpu.er4 = cpu.er14
        cpu.er4 += 0x3F
        cpu.er4 += 0x3F
        cpu.er4 += 0x0E
        cpu.compare(cpu.r0, 0x0F)
        if cpu.ne:
            cpu.branch('dispatch_not_flash')
        cpu.call(0xF6E6C)
        cpu.jump('dispatch_return')
        cpu.label('dispatch_not_flash')
        cpu.compare(cpu.r0, 0x0C)
        if cpu.eq:
            cpu.branch('dispatch_graphics')
        cpu.compare(cpu.r0, 0x10)
        if cpu.ge:
            cpu.branch('dispatch_graphics')
        cpu.call(BASIC_MEMORY)
        cpu.jump('dispatch_return')
        cpu.label('dispatch_graphics')
        cpu.call(BASIC_GRAPHICS)
        cpu.label('dispatch_return')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cond_42')
        cpu.jump('command_error')
        cpu.label('cond_42')
        cpu.er0 = cpu.er14
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x0E
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3F
        cpu.er2 += 0x3F
        cpu.er2 += 0x12
        cpu.call(0xFB538)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cond_43')
        cpu.jump('command_error')
        cpu.label('cond_43')
        cpu.call('copy_result')
        cpu.er0 = 0x01
        cpu.jump('command_out')
        cpu.label('argument_text')
        cpu.call('cached')
        cpu.compare(cpu.r0, 0x22)
        if cpu.eq:
            cpu.branch('cond_44')
        cpu.jump('syntax')
        cpu.label('cond_44')
        cpu.er8 = 0x00
        cpu.label('text_char')
        cpu.call('fetch')
        cpu.compare(cpu.r0, 0x22)
        if cpu.eq:
            cpu.branch('text_end')
        cpu.compare(cpu.r0, 0x20)
        if cpu.ge:
            cpu.branch('cond_45')
        cpu.jump('syntax')
        cpu.label('cond_45')
        cpu.compare(cpu.r0, 0x60)
        if cpu.lt:
            cpu.branch('cond_46')
        cpu.jump('syntax')
        cpu.label('cond_46')
        cpu.compare(cpu.r8, 0x20)
        if cpu.lt:
            cpu.branch('cond_47')
        cpu.jump('syntax')
        cpu.label('cond_47')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3F
        cpu.er2 += 0x3F
        cpu.er2 += 0x26
        cpu.er2 += cpu.er8
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.er8 += 0x01
        cpu.jump('text_char')
        cpu.label('text_end')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3F
        cpu.er2 += 0x3F
        cpu.er2 += 0x26
        cpu.er2 += cpu.er8
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.er0 = cpu.er14
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x26
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x007C)] = cpu.er0
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0084)] = cpu.er8
        cpu.call('fetch_spaces')
        cpu.jump('cond_33')
        cpu.label('syntax')
        cpu.er0 = 0x02
        cpu.label('command_error')
        cpu.compare(cpu.r1, 0x01)
        if cpu.ne:
            cpu.branch('command_native_error')
        cpu.r0 = 0x80
        cpu.r1 = 0x5B
        cpu.call('error_screen')
        cpu.er0 = 0x06
        cpu.label('command_native_error')
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008C)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00D6)]
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D8)]
        cpu.call('set_cursor')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008C)]
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D0)]
        cpu.r3 = 0x00
        cpu.push(cpu.er2)
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00CE)]
        cpu.push(cpu.er2)
        cpu.call(NATIVE_ERROR_WRITE)
        cpu.sp += 0x04
        cpu.jump('command_out')
        cpu.label('argument_native_error')
        cpu.call('copy_result')
        cpu.er0 = 0x00
        cpu.label('command_out')
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008C)] = cpu.er0
        cpu.er0 = cpu.er14
        cpu.r2 = 0x00
        cpu.r3 = 0x80
        cpu.r4 = 0x70
        cpu.r5 = 0x00
        cpu.call('near_copy')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0070)]
        cpu.mem16[0x00, 0x8086] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008C)]
        cpu.sp += 0x7F
        cpu.sp += 0x7F
        cpu.sp += 0x12
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('command_no_stack')
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er12, 0x000A)]
        cpu.r3 = 0x00
        cpu.push(cpu.er2)
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er12, 0x0008)]
        cpu.push(cpu.er2)
        cpu.er0 = 0x06
        cpu.call(NATIVE_ERROR_WRITE)
        cpu.sp += 0x04
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('evaluate_argument')
        cpu.push(cpu.lr)
        cpu.push(cpu.er14)
        cpu.er14 = cpu.sp
        cpu.sp += -128
        cpu.sp += -6
        cpu.push(cpu.xr8)
        cpu.push(cpu.er12)
        cpu.push(cpu.er4)
        cpu.er8 = cpu.er0
        cpu.r10 = cpu.r2
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0xFF7E)] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0xFFE4)] = cpu.r0
        cpu.r0 = 0x95
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0xFFE6)] = cpu.r0
        cpu.er0 = cpu.er14
        cpu.er0 += -64
        cpu.er0 += -64
        cpu.er0 += -2
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0xFF7A)] = cpu.er0
        cpu.er0 = cpu.er14
        cpu.er0 += -28
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0xFF7C)] = cpu.er0
        cpu.call(0x06298)
        cpu.r0 = 0x00
        cpu.r1 = 0x0F
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += -64
        cpu.er0 += -64
        cpu.er0 += -6
        cpu.push(cpu.er0)
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)]
        cpu.push(cpu.er0)
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0008)]
        cpu.r1 = 0x00
        cpu.push(cpu.er0)
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0006)]
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.call(NATIVE_EVALUATE_CORE)
        cpu.sp += 0x0A
        cpu.r1 = 0x00
        cpu.pop(cpu.er4)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr8)
        cpu.sp = cpu.er14
        cpu.pop(cpu.er14)
        cpu.pop(cpu.pc)
        cpu.label('near_copy')
        cpu.r6 = cpu.mem8[0x00, cpu.er0]
        cpu.mem8[0x00, cpu.er2] = cpu.r6
        cpu.er0 += 0x01
        cpu.er2 += 0x01
        cpu.er4 += -1
        if cpu.ne:
            cpu.branch('near_copy')
        cpu.ret()
        cpu.label('cursor')
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00C8)]
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00C6)]
        cpu.r3 = cpu.mem8[cpu.r2, cpu.offset(cpu.er0, 0x0002)]
        cpu.er0 = cpu.mem16[cpu.r2, cpu.er0]
        cpu.r2 = cpu.r3
        cpu.ret()
        cpu.label('set_cursor')
        cpu.er4 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00C6)]
        cpu.r3 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00C8)]
        cpu.mem16[cpu.r3, cpu.er4] = cpu.er0
        cpu.mem8[cpu.r3, cpu.offset(cpu.er4, 0x0002)] = cpu.r2
        cpu.ret()
        cpu.label('fetch_spaces')
        cpu.push(cpu.lr)
        cpu.label('fetch_spaces_loop')
        cpu.call('fetch')
        cpu.compare(cpu.r0, 0x20)
        if cpu.eq:
            cpu.branch('fetch_spaces_loop')
        cpu.pop(cpu.pc)
        cpu.label('fetch')
        cpu.push(cpu.lr)
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00C8)]
        cpu.r1 = 0x00
        cpu.push(cpu.er0)
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00C6)]
        cpu.push(cpu.er0)
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00CA)]
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00CC)]
        cpu.call(NATIVE_TOKEN_FETCH)
        cpu.sp += 0x04
        cpu.call('cached')
        cpu.pop(cpu.pc)
        cpu.label('cached')
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00CC)]
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00CA)]
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er0]
        cpu.ret()
        cpu.label('copy_result')
        cpu.push(cpu.lr)
        cpu.er0 = 0x00
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x12
        cpu.push(cpu.er0)
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00CE)]
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D0)]
        cpu.call(NATIVE_NUMBER_COPY)
        cpu.sp += 0x04
        cpu.pop(cpu.pc)
        cpu.label('command_asm')
        cpu.call('source_bounds')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cond_48')
        cpu.jump('command_error')
        cpu.label('cond_48')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00D6)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00E2)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D8)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00E4)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00E5)] = cpu.r0
        cpu.er0 = cpu.er14
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x1D
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3F
        cpu.er2 += 0x3F
        cpu.er2 += 0x3F
        cpu.er2 += 0x29
        cpu.call(BASIC_ASM)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('asm_success')
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008C)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00EA)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00D6)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00EC)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D8)] = cpu.r0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008C)]
        cpu.compare(cpu.r1, 0x01)
        if cpu.ne:
            cpu.branch('cond_49')
        cpu.jump('command_error')
        cpu.label('cond_49')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00F2)]
        cpu.call('reason_screen')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008C)]
        cpu.jump('command_error')
        cpu.label('asm_success')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00E6)]
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00E8)]
        cpu.call('set_cursor')
        cpu.call('fetch')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00EE)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008C)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00F0)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008E)] = cpu.er0
        cpu.er0 = cpu.er14
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x0E
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3F
        cpu.er2 += 0x3F
        cpu.er2 += 0x12
        cpu.call(0xFB538)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cond_50')
        cpu.jump('command_error')
        cpu.label('cond_50')
        cpu.er0 = 0x00
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x12
        cpu.push(cpu.er0)
        cpu.r0 = 0x8E
        cpu.r1 = 0x72
        cpu.r2 = 0x04
        cpu.call(NATIVE_NUMBER_COPY)
        cpu.sp += 0x04
        cpu.call('copy_result')
        cpu.er0 = 0x01
        cpu.jump('command_out')
        cpu.label('source_bounds')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.xr8)
        cpu.push(cpu.er12)
        cpu.r0 = cpu.mem8[0x00, 0x80AB]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('cond_51')
        cpu.jump('bounds_bad')
        cpu.label('cond_51')
        cpu.compare(cpu.r0, 0x0C)
        if cpu.lt:
            cpu.branch('cond_52')
        cpu.jump('bounds_bad')
        cpu.label('cond_52')
        cpu.r0 += 0xFF
        cpu.r1 = 0x00
        cpu.r2 = 0x36
        cpu.multiply(cpu.er0, cpu.r2)
        cpu.r8 = 0x00
        cpu.r9 = 0x76
        cpu.er8 += cpu.er0
        cpu.r10 = 0x04
        cpu.er0 = cpu.mem16[cpu.r10, cpu.er8]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00DA)] = cpu.er0
        cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er8, 0x0002)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00DC)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00DD)] = cpu.r0
        cpu.er8 += 0x08
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3F
        cpu.er2 += 0x3F
        cpu.er2 += 0x3F
        cpu.er2 += 0x39
        cpu.r4 = 0x0D
        cpu.label('bounds_name')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er8]
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.er8 += 0x01
        cpu.er2 += 0x01
        cpu.r4 += 0xFF
        if cpu.ne:
            cpu.branch('bounds_name')
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0102)] = cpu.r0
        cpu.er0 = cpu.er14
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x0E
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x0C
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x39
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3F
        cpu.er2 += 0x3F
        cpu.er2 += 0x3F
        cpu.er2 += 0x3F
        cpu.er2 += 0x08
        cpu.call(NATIVE_PROGRAM_LOOKUP)
        cpu.sp += 0x04
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bounds_library')
        cpu.er8 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0108)]
        cpu.r10 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x010A)]
        cpu.compare(cpu.r10, 0x04)
        if cpu.ne:
            cpu.branch('bounds_library')
        cpu.er0 = cpu.er8
        cpu.er0 += 0x06
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00DA)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.branch('bounds_library')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00DC)]
        cpu.compare(cpu.r0, 0x04)
        if cpu.ne:
            cpu.branch('bounds_library')
        cpu.r12 = 0x00
        cpu.r13 = 0x80
        cpu.jump('bounds_allocation')
        cpu.label('bounds_library')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00DC)]
        cpu.compare(cpu.r0, 0x08)
        if cpu.eq:
            cpu.branch('bounds_s3')
        cpu.compare(cpu.r0, 0x09)
        if cpu.eq:
            cpu.branch('cond_53')
        cpu.jump('bounds_bad')
        cpu.label('cond_53')
        cpu.r2 = 0x00
        cpu.jump('bounds_lookup_library')
        cpu.label('bounds_s3')
        cpu.r2 = 0x01
        cpu.label('bounds_lookup_library')
        cpu.r0 = cpu.mem8[0x00, 0x80AD]
        cpu.r1 = 0x00
        cpu.push(cpu.er0)
        cpu.mem8[0x00, 0x80AD] = cpu.r2
        cpu.er0 = cpu.er14
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x0C
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x39
        cpu.r2 = 0xC7
        cpu.r3 = 0x01
        cpu.call(NATIVE_LIBRARY_LOOKUP)
        cpu.sp += 0x02
        cpu.pop(cpu.er2)
        cpu.mem8[0x00, 0x80AD] = cpu.r2
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cond_54')
        cpu.jump('bounds_bad')
        cpu.label('cond_54')
        cpu.er8 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0108)]
        cpu.r10 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x010A)]
        cpu.er0 = cpu.mem16[cpu.r10, cpu.offset(cpu.er8, 0x0010)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0104)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.r10, cpu.offset(cpu.er8, 0x0012)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0106)] = cpu.er0
        cpu.er2 = cpu.mem16[cpu.r10, cpu.offset(cpu.er8, 0x0016)]
        cpu.er8 = cpu.mem16[cpu.r10, cpu.offset(cpu.er8, 0x0014)]
        cpu.r10 = cpu.r2
        cpu.compare(cpu.r3, 0x00)
        if cpu.eq:
            cpu.branch('cond_55')
        cpu.jump('bounds_bad')
        cpu.label('cond_55')
        cpu.compare(cpu.r10, 0x08)
        if cpu.eq:
            cpu.branch('bounds_library_s3')
        cpu.compare(cpu.r10, 0x09)
        if cpu.eq:
            cpu.branch('cond_56')
        cpu.jump('bounds_bad')
        cpu.label('cond_56')
        cpu.r0 = 0x00
        cpu.r1 = 0x20
        cpu.compare(cpu.er8, cpu.er0)
        if cpu.ge:
            cpu.branch('cond_57')
        cpu.jump('bounds_bad')
        cpu.label('cond_57')
        cpu.er12 = 0x00
        cpu.jump('bounds_library_header')
        cpu.label('bounds_library_s3')
        cpu.r0 = 0x00
        cpu.r1 = 0xA0
        cpu.compare(cpu.er8, cpu.er0)
        if cpu.ge:
            cpu.branch('cond_58')
        cpu.jump('bounds_bad')
        cpu.label('cond_58')
        cpu.er12 = 0x00
        cpu.label('bounds_library_header')
        cpu.er0 = cpu.mem16[cpu.r10, cpu.offset(cpu.er8, 0x0002)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008C)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.r10, cpu.offset(cpu.er8, 0x0004)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008E)] = cpu.er0
        cpu.label('bounds_allocation')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0106)]
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cond_59')
        cpu.jump('bounds_bad')
        cpu.label('cond_59')
        cpu.er4 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0104)]
        cpu.er0 = 0x07
        cpu.compare(cpu.er4, cpu.er0)
        if cpu.ge:
            cpu.branch('cond_60')
        cpu.jump('bounds_bad')
        cpu.label('cond_60')
        cpu.er0 = cpu.er8
        cpu.er0 += cpu.er4
        cpu.compare(cpu.er0, cpu.er8)
        if cpu.ge:
            cpu.branch('bounds_owner_end')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cond_61')
        cpu.jump('bounds_bad')
        cpu.label('cond_61')
        cpu.er12 = cpu.er12
        if cpu.eq:
            cpu.branch('cond_62')
        cpu.jump('bounds_bad')
        cpu.label('cond_62')
        cpu.jump('cond_63')
        cpu.label('bounds_owner_end')
        cpu.er12 = cpu.er12
        if cpu.eq:
            cpu.branch('cond_63')
        cpu.compare(cpu.er12, cpu.er0)
        if cpu.ge:
            cpu.branch('cond_63')
        cpu.jump('bounds_bad')
        cpu.label('cond_63')
        cpu.label('bounds_length')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008E)]
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cond_64')
        cpu.jump('bounds_bad')
        cpu.label('cond_64')
        cpu.er6 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008C)]
        cpu.er6 = cpu.er6
        if cpu.ne:
            cpu.branch('cond_65')
        cpu.jump('bounds_bad')
        cpu.label('cond_65')
        cpu.er4 += -6
        cpu.compare(cpu.er4, cpu.er6)
        if cpu.ge:
            cpu.branch('cond_66')
        cpu.jump('bounds_bad')
        cpu.label('cond_66')
        cpu.er8 += 0x06
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00DA)]
        cpu.compare(cpu.er8, cpu.er0)
        if cpu.eq:
            cpu.branch('cond_67')
        cpu.jump('bounds_bad')
        cpu.label('cond_67')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00DC)]
        cpu.compare(cpu.r0, cpu.r10)
        if cpu.eq:
            cpu.branch('cond_68')
        cpu.jump('bounds_bad')
        cpu.label('cond_68')
        cpu.er6 += cpu.er8
        cpu.compare(cpu.er6, cpu.er8)
        if cpu.ge:
            cpu.branch('cond_69')
        cpu.jump('bounds_bad')
        cpu.label('cond_69')
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00DE)] = cpu.er6
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00E0)] = cpu.r10
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00E1)] = cpu.r0
        cpu.er6 += -1
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er6]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('cond_70')
        cpu.jump('bounds_bad')
        cpu.label('cond_70')
        cpu.er0 = 0x00
        cpu.jump('bounds_out')
        cpu.label('bounds_bad')
        cpu.er0 = 0x02
        cpu.label('bounds_out')
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('scan_if')
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.call('scan')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('scan_if_ok')
        cpu.er0 = 0x00
        cpu.jump(0xE5E90)
        cpu.label('scan_if_ok')
        cpu.er12 = cpu.mem16[cpu.offset(cpu.fp, 6)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.fp, 8)]
        cpu.jump(0xE5FD2)
        cpu.label('scan_else')
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.call('scan')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('scan_else_ok')
        cpu.er0 = 0x00
        cpu.jump(0xE5E90)
        cpu.label('scan_else_ok')
        cpu.er12 = cpu.mem16[cpu.offset(cpu.fp, 6)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.fp, 8)]
        cpu.jump(0xE6064)
        cpu.label('scan_break')
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.call('scan')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('scan_break_ok')
        cpu.er0 = 0x00
        cpu.jump(0xE6B44)
        cpu.label('scan_break_ok')
        cpu.er12 = cpu.mem16[cpu.offset(cpu.fp, 6)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.fp, 8)]
        cpu.jump(0xE6BC8)
        cpu.label('scan_for')
        cpu.push(cpu.xr0)
        cpu.call('scan')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_71')
        cpu.jump('scan_for_fail')
        cpu.label('cond_71')
        cpu.compare(cpu.r0, 0x01)
        if cpu.eq:
            cpu.branch('cond_72')
        cpu.pop(cpu.xr0)
        cpu.call(0xE5A42)
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.push(cpu.xr0)
        cpu.call('scan')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_72')
        cpu.jump('scan_for_fail')
        cpu.label('cond_72')
        cpu.label('scan_for_done')
        cpu.pop(cpu.xr0)
        cpu.jump(0xE6630)
        cpu.label('scan_for_fail')
        cpu.pop(cpu.xr0)
        cpu.sp += 0x04
        cpu.er0 = 0x00
        cpu.jump(0xE6290)
        cpu.label('scan_while')
        cpu.push(cpu.xr0)
        cpu.call('scan')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_73')
        cpu.jump('scan_while_fail')
        cpu.label('cond_73')
        cpu.compare(cpu.r0, 0x01)
        if cpu.eq:
            cpu.branch('cond_74')
        cpu.pop(cpu.xr0)
        cpu.call(0xE5A42)
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.push(cpu.xr0)
        cpu.call('scan')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_74')
        cpu.jump('scan_while_fail')
        cpu.label('cond_74')
        cpu.label('scan_while_done')
        cpu.pop(cpu.xr0)
        cpu.jump(0xE687A)
        cpu.label('scan_while_fail')
        cpu.pop(cpu.xr0)
        cpu.sp += 0x04
        cpu.er0 = 0x00
        cpu.jump(0xE67C2)
        cpu.label('scan_goto')
        cpu.push(cpu.xr0)
        cpu.call('scan')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_75')
        cpu.jump('scan_goto_fail')
        cpu.label('cond_75')
        cpu.compare(cpu.r0, 0x01)
        if cpu.eq:
            cpu.branch('cond_76')
        cpu.pop(cpu.xr0)
        cpu.call(0xE5A42)
        cpu.er0 = cpu.er14
        cpu.er0 += -4
        cpu.r2 = 0x00
        cpu.push(cpu.xr0)
        cpu.call('scan')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_76')
        cpu.jump('scan_goto_fail')
        cpu.label('cond_76')
        cpu.label('scan_goto_done')
        cpu.pop(cpu.xr0)
        cpu.jump(0xE6FA0)
        cpu.label('scan_goto_fail')
        cpu.pop(cpu.xr0)
        cpu.sp += 0x04
        cpu.er0 = 0x00
        cpu.jump(0xE6F04)
        cpu.label('scan')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.r10 = cpu.r2
        cpu.er12 = cpu.er14
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er12, 0x0006)]
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er12, 0x0008)]
        cpu.r3 = cpu.mem8[cpu.r2, cpu.er0]
        cpu.compare(cpu.r3, 0xF9)
        if cpu.eq:
            cpu.branch('cond_77')
        cpu.jump('scan_none')
        cpu.label('cond_77')
        cpu.r3 = cpu.mem8[cpu.r2, cpu.offset(cpu.er0, 0x0001)]
        cpu.compare(cpu.r3, 0xF7)
        if cpu.eq:
            cpu.branch('cond_78')
        cpu.jump('scan_none')
        cpu.label('cond_78')
        cpu.er0 = cpu.sp
        cpu.r2 = 0x22
        cpu.r3 = 0x86
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('cond_79')
        cpu.jump('scan_stack')
        cpu.label('cond_79')
        cpu.sp += -128
        cpu.sp += -128
        cpu.sp += -16
        cpu.er14 = cpu.sp
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00C6)] = cpu.er8
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00C8)] = cpu.r10
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er12, 0x0006)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00CA)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er12, 0x0008)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00CC)] = cpu.r0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er12, 0x000A)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00CE)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er12, 0x000C)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D0)] = cpu.r0
        cpu.er0 = 0x00
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00F2)] = cpu.er0
        cpu.call('cursor')
        cpu.er0 += -2
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00D6)] = cpu.er0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D8)] = cpu.r2
        cpu.call('source_bounds')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('scan_error')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00D6)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00E2)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D8)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00E4)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00E5)] = cpu.r0
        cpu.er0 = cpu.er14
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x3F
        cpu.er0 += 0x1D
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3F
        cpu.er2 += 0x3F
        cpu.er2 += 0x3F
        cpu.er2 += 0x29
        cpu.call(0xF9534)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('scan_success')
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008C)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00EA)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00D6)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00EC)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D8)] = cpu.r0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008C)]
        cpu.label('scan_error')
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008C)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00F2)]
        cpu.call('reason_screen')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00D6)]
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D8)]
        cpu.call('set_cursor')
        cpu.er4 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0110)]
        cpu.r3 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0112)]
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00D6)]
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D8)]
        cpu.mem16[cpu.r3, cpu.er4] = cpu.er0
        cpu.mem8[cpu.r3, cpu.offset(cpu.er4, 0x0002)] = cpu.r2
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00D0)]
        cpu.r3 = 0x00
        cpu.push(cpu.er2)
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00CE)]
        cpu.push(cpu.er2)
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x008C)]
        cpu.call(NATIVE_ERROR_WRITE)
        cpu.sp += 0x04
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.jump('scan_out')
        cpu.label('scan_success')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x00E6)]
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x00E8)]
        cpu.call('set_cursor')
        cpu.call('fetch')
        cpu.er0 = 0x01
        cpu.label('scan_out')
        cpu.sp += 0x7F
        cpu.sp += 0x7F
        cpu.sp += 0x12
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('scan_stack')
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er12, 0x000C)]
        cpu.r3 = 0x00
        cpu.push(cpu.er2)
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er12, 0x000A)]
        cpu.push(cpu.er2)
        cpu.er0 = 0x06
        cpu.call(NATIVE_ERROR_WRITE)
        cpu.sp += 0x04
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('scan_none')
        cpu.er0 = 0x00
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('source_context')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.r10 = cpu.r2
        cpu.er12 = cpu.er6
        cpu.sp += -4
        cpu.er14 = cpu.sp
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0000)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0001)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0003)] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0002)] = cpu.r0
        cpu.label('context_loop')
        cpu.compare(cpu.er8, cpu.er4)
        if cpu.lt:
            cpu.branch('cond_80')
        cpu.jump('context_out')
        cpu.label('cond_80')
        cpu.compare(cpu.er8, cpu.er12)
        if cpu.lt:
            cpu.branch('cond_81')
        cpu.jump('context_out')
        cpu.label('cond_81')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er8]
        cpu.er8 += 0x01
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('cond_82')
        cpu.jump('context_out')
        cpu.label('cond_82')
        cpu.compare(cpu.r0, 0x0D)
        if cpu.ne:
            cpu.branch('cond_83')
        cpu.jump('context_newline')
        cpu.label('cond_83')
        cpu.compare(cpu.r0, 0x0C)
        if cpu.ne:
            cpu.branch('cond_84')
        cpu.jump('context_newline')
        cpu.label('cond_84')
        cpu.compare(cpu.r0, 0x20)
        if cpu.eq:
            cpu.branch('context_loop')
        cpu.compare(cpu.r0, 0xF9)
        if cpu.ne:
            cpu.branch('context_byte')
        cpu.compare(cpu.er8, cpu.er12)
        if cpu.lt:
            cpu.branch('cond_85')
        cpu.jump('context_out')
        cpu.label('cond_85')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er8]
        cpu.er8 += 0x01
        cpu.r1 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0002)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('context_not_head')
        cpu.r1 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0003)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.ne:
            cpu.branch('context_not_head')
        cpu.compare(cpu.r0, 0xF7)
        if cpu.ne:
            cpu.branch('context_endasm')
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0001)] = cpu.r0
        cpu.jump('context_not_head')
        cpu.label('context_endasm')
        cpu.compare(cpu.r0, 0xF8)
        if cpu.ne:
            cpu.branch('context_not_head')
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0001)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0000)] = cpu.r0
        cpu.jump('context_not_head')
        cpu.label('context_byte')
        cpu.r1 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0000)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.ne:
            cpu.branch('context_not_head')
        cpu.r1 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0003)]
        cpu.compare(cpu.r1, 0x02)
        if cpu.eq:
            cpu.branch('context_not_head')
        cpu.compare(cpu.r0, 0x22)
        if cpu.ne:
            cpu.branch('context_comment')
        cpu.r1 ^= 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0003)] = cpu.r1
        cpu.jump('context_not_head')
        cpu.label('context_comment')
        cpu.compare(cpu.r1, 0x00)
        if cpu.ne:
            cpu.branch('context_not_head')
        cpu.compare(cpu.r0, 0x27)
        if cpu.ne:
            cpu.branch('context_prefix')
        cpu.r1 = 0x02
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0003)] = cpu.r1
        cpu.label('context_prefix')
        cpu.compare(cpu.r0, 0x7F)
        if cpu.eq:
            cpu.branch('context_second')
        cpu.compare(cpu.r0, 0xE5)
        if cpu.eq:
            cpu.branch('context_second')
        cpu.compare(cpu.r0, 0xE6)
        if cpu.eq:
            cpu.branch('context_second')
        cpu.compare(cpu.r0, 0xE7)
        if cpu.eq:
            cpu.branch('context_second')
        cpu.compare(cpu.r0, 0xF7)
        if cpu.eq:
            cpu.branch('context_second')
        cpu.jump('context_not_head')
        cpu.label('context_second')
        cpu.compare(cpu.er8, cpu.er12)
        if cpu.ge:
            cpu.branch('context_out')
        cpu.er8 += 0x01
        cpu.label('context_not_head')
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0002)] = cpu.r0
        cpu.jump('context_loop')
        cpu.label('context_newline')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0001)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0000)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0003)] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0002)] = cpu.r0
        cpu.jump('context_loop')
        cpu.label('context_out')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0000)]
        cpu.r1 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0002)]
        cpu.sp += 0x04
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('editor_context')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.er4 = cpu.mem16[0x00, cpu.offset(cpu.er0, 0xFFD6)]
        cpu.er6 = cpu.mem16[0x00, cpu.offset(cpu.er0, 0xFFE0)]
        cpu.er4 += cpu.er6
        cpu.call('program_extent')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('context_unowned')
        cpu.call('source_context')
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('display_context')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x000A)]
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er8, 0x000C)]
        cpu.call('header_context')
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('header_context')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.xr8)
        cpu.er8 = cpu.er0
        cpu.r10 = cpu.r2
        cpu.compare(cpu.r2, 0x04)
        if cpu.eq:
            cpu.branch('cond_86')
        cpu.jump('header_unowned')
        cpu.label('cond_86')
        cpu.call('program_frame')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('cond_87')
        cpu.jump('header_unowned')
        cpu.label('cond_87')
        cpu.call('program_extent')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('cond_88')
        cpu.jump('header_unowned')
        cpu.label('cond_88')
        cpu.compare(cpu.er0, cpu.er8)
        if cpu.eq:
            cpu.branch('cond_89')
        cpu.jump('header_unowned')
        cpu.label('cond_89')
        cpu.compare(cpu.r2, cpu.r10)
        if cpu.eq:
            cpu.branch('cond_90')
        cpu.jump('header_unowned')
        cpu.label('cond_90')
        cpu.call('source_context')
        cpu.pop(cpu.xr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('header_unowned')
        cpu.er0 = 0x00
        cpu.pop(cpu.xr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('context_unowned')
        cpu.er0 = 0x00
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('program_frame')
        cpu.push(cpu.xr4)
        cpu.er6 = cpu.er14
        cpu.label('program_frame_next')
        cpu.r0 = 0xE4
        cpu.r1 = 0x82
        cpu.compare(cpu.er6, cpu.er0)
        if cpu.ge:
            cpu.branch('cond_91')
        cpu.jump('program_frame_none')
        cpu.label('cond_91')
        cpu.r0 = 0xFA
        cpu.r1 = 0x8D
        cpu.compare(cpu.er0, cpu.er6)
        if cpu.ge:
            cpu.branch('cond_92')
        cpu.jump('program_frame_none')
        cpu.label('cond_92')
        cpu.r0 = cpu.r6
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('cond_93')
        cpu.jump('program_frame_none')
        cpu.label('cond_93')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er6, 0x0002)]
        cpu.r2 = 0xF2
        cpu.r3 = 0xA5
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.branch('program_frame_parent')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er6, 0x0004)]
        cpu.compare(cpu.r0, 0x0C)
        if cpu.ne:
            cpu.branch('program_frame_parent')
        cpu.er0 = cpu.er6
        cpu.pop(cpu.xr4)
        cpu.ret()
        cpu.label('program_frame_parent')
        cpu.er0 = cpu.mem16[0x00, cpu.er6]
        cpu.compare(cpu.er0, cpu.er6)
        if cpu.ge:
            cpu.branch('cond_94')
        cpu.jump('program_frame_none')
        cpu.label('cond_94')
        if cpu.ne:
            cpu.branch('cond_95')
        cpu.jump('program_frame_none')
        cpu.label('cond_95')
        cpu.er6 = cpu.er0
        cpu.jump('program_frame_next')
        cpu.label('program_frame_none')
        cpu.er0 = 0x00
        cpu.pop(cpu.xr4)
        cpu.ret()
        cpu.label('program_extent')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr8)
        cpu.push(cpu.er12)
        cpu.push(cpu.er14)
        cpu.er8 = cpu.er0
        cpu.er0 = cpu.sp
        cpu.r2 = 0x92
        cpu.r3 = 0x83
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('cond_96')
        cpu.jump('program_extent_stack')
        cpu.label('cond_96')
        cpu.sp += -12
        cpu.er14 = cpu.sp
        cpu.er0 = cpu.er14
        cpu.er0 += 0x08
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 0x04
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er14
        cpu.er0 = cpu.er8
        cpu.er0 += -64
        cpu.er0 += -4
        cpu.call(NATIVE_PROGRAM_LOOKUP)
        cpu.sp += 0x04
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cond_97')
        cpu.jump('program_extent_bad')
        cpu.label('cond_97')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0002)]
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cond_98')
        cpu.jump('program_extent_bad')
        cpu.label('cond_98')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)]
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cond_99')
        cpu.jump('program_extent_bad')
        cpu.label('cond_99')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0006)]
        cpu.compare(cpu.r0, 0x04)
        if cpu.eq:
            cpu.branch('cond_100')
        cpu.jump('program_extent_bad')
        cpu.label('cond_100')
        cpu.er10 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0004)]
        cpu.r0 = 0xFA
        cpu.r1 = 0x7F
        cpu.compare(cpu.er0, cpu.er10)
        if cpu.ge:
            cpu.branch('cond_101')
        cpu.jump('program_extent_bad')
        cpu.label('cond_101')
        cpu.er12 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0000)]
        cpu.er0 = 0x07
        cpu.compare(cpu.er12, cpu.er0)
        if cpu.ge:
            cpu.branch('cond_102')
        cpu.jump('program_extent_bad')
        cpu.label('cond_102')
        cpu.er0 = cpu.er10
        cpu.er0 += cpu.er12
        cpu.compare(cpu.er0, cpu.er10)
        if cpu.ge:
            cpu.branch('cond_103')
        cpu.jump('program_extent_bad')
        cpu.label('cond_103')
        cpu.r2 = 0x00
        cpu.r3 = 0x80
        cpu.compare(cpu.er2, cpu.er0)
        if cpu.ge:
            cpu.branch('cond_104')
        cpu.jump('program_extent_bad')
        cpu.label('cond_104')
        cpu.er6 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0008)]
        cpu.er6 = cpu.er6
        if cpu.ne:
            cpu.branch('cond_105')
        cpu.jump('program_extent_bad')
        cpu.label('cond_105')
        cpu.er12 += -6
        cpu.compare(cpu.er12, cpu.er6)
        if cpu.ge:
            cpu.branch('cond_106')
        cpu.jump('program_extent_bad')
        cpu.label('cond_106')
        cpu.er10 += 0x06
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0xFFE0)]
        cpu.compare(cpu.er0, cpu.er10)
        if cpu.eq:
            cpu.branch('cond_107')
        cpu.jump('program_extent_bad')
        cpu.label('cond_107')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er8, 0xFFE2)]
        cpu.compare(cpu.r0, 0x04)
        if cpu.eq:
            cpu.branch('cond_108')
        cpu.jump('program_extent_bad')
        cpu.label('cond_108')
        cpu.er6 += cpu.er10
        cpu.compare(cpu.er4, cpu.er10)
        if cpu.ge:
            cpu.branch('cond_109')
        cpu.jump('program_extent_bad')
        cpu.label('cond_109')
        cpu.compare(cpu.er4, cpu.er6)
        if cpu.lt:
            cpu.branch('cond_110')
        cpu.jump('program_extent_bad')
        cpu.label('cond_110')
        cpu.er0 = cpu.er6
        cpu.er0 += -1
        cpu.r2 = 0x04
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er0]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('cond_111')
        cpu.jump('program_extent_bad')
        cpu.label('cond_111')
        cpu.er0 = cpu.er10
        cpu.jump('program_extent_out')
        cpu.label('program_extent_bad')
        cpu.er0 = 0x00
        cpu.label('program_extent_out')
        cpu.sp += 0x0C
        cpu.pop(cpu.er14)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr8)
        cpu.pop(cpu.pc)
        cpu.label('program_extent_stack')
        cpu.er0 = 0x00
        cpu.pop(cpu.er14)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr8)
        cpu.pop(cpu.pc)
        cpu.label('display_cc7de')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.xr0)
        cpu.er4 = cpu.er12
        cpu.call('display_context')
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('display_cc7de_native')
        cpu.pop(cpu.xr0)
        cpu.compare(cpu.r1, 0x00)
        if cpu.ne:
            cpu.branch('display_cc7de_native_restored')
        cpu.compare(cpu.r0, 0x20)
        if cpu.lt:
            cpu.branch('display_cc7de_native_restored')
        cpu.compare(cpu.r0, 0x7F)
        if cpu.ge:
            cpu.branch('display_cc7de_native_restored')
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er2, 0x0001)] = cpu.r0
        cpu.er0 = 0x01
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('display_cc7de_native')
        cpu.pop(cpu.xr0)
        cpu.label('display_cc7de_native_restored')
        cpu.call(0xDFD00)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('display_cc878')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.xr0)
        cpu.r5 = 0x00
        cpu.er4 += cpu.er6
        cpu.call('display_context')
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('display_cc878_native')
        cpu.pop(cpu.xr0)
        cpu.compare(cpu.r1, 0x00)
        if cpu.ne:
            cpu.branch('display_cc878_native_restored')
        cpu.compare(cpu.r0, 0x20)
        if cpu.lt:
            cpu.branch('display_cc878_native_restored')
        cpu.compare(cpu.r0, 0x7F)
        if cpu.ge:
            cpu.branch('display_cc878_native_restored')
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er2, 0x0001)] = cpu.r0
        cpu.er0 = 0x01
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('display_cc878_native')
        cpu.pop(cpu.xr0)
        cpu.label('display_cc878_native_restored')
        cpu.call(0xDFD00)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('display_cc94a')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.xr0)
        cpu.er4 = cpu.er12
        cpu.call('display_context')
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('display_cc94a_native')
        cpu.pop(cpu.xr0)
        cpu.compare(cpu.r1, 0x00)
        if cpu.ne:
            cpu.branch('display_cc94a_native_restored')
        cpu.compare(cpu.r0, 0x20)
        if cpu.lt:
            cpu.branch('display_cc94a_native_restored')
        cpu.compare(cpu.r0, 0x7F)
        if cpu.ge:
            cpu.branch('display_cc94a_native_restored')
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er2, 0x0001)] = cpu.r0
        cpu.er0 = 0x01
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('display_cc94a_native')
        cpu.pop(cpu.xr0)
        cpu.label('display_cc94a_native_restored')
        cpu.call(0xDFD00)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('display_ccb16')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.xr0)
        cpu.er4 = cpu.er12
        cpu.call('display_context')
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('display_ccb16_native')
        cpu.pop(cpu.xr0)
        cpu.compare(cpu.r1, 0x00)
        if cpu.ne:
            cpu.branch('display_ccb16_native_restored')
        cpu.compare(cpu.r0, 0x20)
        if cpu.lt:
            cpu.branch('display_ccb16_native_restored')
        cpu.compare(cpu.r0, 0x7F)
        if cpu.ge:
            cpu.branch('display_ccb16_native_restored')
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er2, 0x0001)] = cpu.r0
        cpu.er0 = 0x01
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('display_ccb16_native')
        cpu.pop(cpu.xr0)
        cpu.label('display_ccb16_native_restored')
        cpu.call(0xDFD00)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('display_cd268')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.xr0)
        cpu.er4 = cpu.er12
        cpu.call('display_context')
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('display_cd268_native')
        cpu.pop(cpu.xr0)
        cpu.compare(cpu.r1, 0x00)
        if cpu.ne:
            cpu.branch('display_cd268_native_restored')
        cpu.compare(cpu.r0, 0x20)
        if cpu.lt:
            cpu.branch('display_cd268_native_restored')
        cpu.compare(cpu.r0, 0x7F)
        if cpu.ge:
            cpu.branch('display_cd268_native_restored')
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er2, 0x0001)] = cpu.r0
        cpu.er0 = 0x01
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('display_cd268_native')
        cpu.pop(cpu.xr0)
        cpu.label('display_cd268_native_restored')
        cpu.call(0xDFD00)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('display_ccf82')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.xr0)
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x000A)]
        cpu.er4 += cpu.er0
        cpu.er4 += -1
        cpu.call('display_context')
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('display_ccf82_native')
        cpu.pop(cpu.xr0)
        cpu.compare(cpu.r1, 0x00)
        if cpu.ne:
            cpu.branch('display_ccf82_native_restored')
        cpu.compare(cpu.r0, 0x20)
        if cpu.lt:
            cpu.branch('display_ccf82_native_restored')
        cpu.compare(cpu.r0, 0x7F)
        if cpu.ge:
            cpu.branch('display_ccf82_native_restored')
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er2, 0x0001)] = cpu.r0
        cpu.er0 = cpu.er2
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('display_ccf82_native')
        cpu.pop(cpu.xr0)
        cpu.label('display_ccf82_native_restored')
        cpu.call(HOOK_SPELL_DFC02)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('display_decode')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.er4 = cpu.er0
        cpu.call(NATIVE_TOKEN_DECODE)
        cpu.push(cpu.er0)
        cpu.er0 = cpu.mem16[0x00, 0x800A]
        cpu.r2 = cpu.mem8[0x00, 0x800C]
        cpu.call('header_context')
        cpu.pop(cpu.er2)
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('display_decode_native')
        cpu.compare(cpu.r3, 0x00)
        if cpu.ne:
            cpu.branch('display_decode_native')
        cpu.compare(cpu.r2, 0x20)
        if cpu.lt:
            cpu.branch('display_decode_native')
        cpu.compare(cpu.r2, 0x7F)
        if cpu.ge:
            cpu.branch('display_decode_native')
        cpu.r3 = 0xFE
        cpu.label('display_decode_native')
        cpu.er0 = cpu.er2
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('program_menu')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.er4 = cpu.er0
        cpu.push(cpu.er2)
        cpu.er0 = cpu.er14
        cpu.call('editor_context')
        cpu.pop(cpu.er2)
        cpu.compare(cpu.r0, 0x01)
        if cpu.eq:
            cpu.branch('program_block_menu')
        cpu.er0 = cpu.er4
        cpu.call(NATIVE_PROGRAM_FUNCTION)
        cpu.label('program_menu_return')
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('program_block_menu')
        cpu.er6 = cpu.er14
        cpu.call('block_menu')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('native_menu_key')
        cpu.call(0x125FC)
        cpu.compare(cpu.r0, 0xFD)
        if cpu.eq:
            cpu.branch('cond_112')
        cpu.jump('native_menu_key_return')
        cpu.label('cond_112')
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0002)]
        cpu.r0 = 0x04
        cpu.r1 = 0x51
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.eq:
            cpu.branch('cond_113')
        cpu.jump('native_menu_right')
        cpu.label('cond_113')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0xFE5E)]
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cond_114')
        cpu.jump('native_menu_right')
        cpu.label('cond_114')
        cpu.er0 = cpu.mem16[cpu.r11, cpu.offset(cpu.er6, 0x000C)]
        cpu.r2 = cpu.mem8[cpu.r11, cpu.offset(cpu.er6, 0x000E)]
        cpu.compare(cpu.r0, 0x00)
        cpu.compare_carry(cpu.r1, 0x00)
        cpu.compare_carry(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('cond_115')
        cpu.jump('native_menu_right')
        cpu.label('cond_115')
        cpu.call('nx_menu')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.eq:
            cpu.branch('native_menu_back')
        cpu.mem16[0x00, cpu.er8] = cpu.er0
        cpu.er0 = 0x01
        cpu.sp += 0x02
        cpu.jump(0xDF592)
        cpu.label('native_menu_back')
        cpu.sp += 0x02
        cpu.jump(0xDF49A)
        cpu.label('native_menu_right')
        cpu.r0 = 0xFD
        cpu.label('native_menu_key_return')
        cpu.jump(0xDF554)
        cpu.label('nx_menu')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.label('nx_page')
        cpu.r0 = 0xBC
        cpu.r1 = 0x58
        cpu.er2 = 0x01
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_116')
        cpu.jump('nx_next_3')
        cpu.label('cond_116')
        cpu.label('nx_categories')
        cpu.r0 = 0xBE
        cpu.r1 = 0x58
        cpu.er2 = 0x04
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_117')
        cpu.jump('nx_page')
        cpu.label('cond_117')
        cpu.er4 = cpu.er0
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('nx_next_0')
        cpu.r0 = 0xC6
        cpu.r1 = 0x58
        cpu.er2 = 0x07
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_118')
        cpu.jump('cond_116')
        cpu.label('cond_118')
        cpu.r2 = 0xD4
        cpu.r3 = 0x58
        cpu.er2 += cpu.er0
        cpu.r0 = cpu.mem8[0x0F, cpu.er2]
        cpu.r1 = 0xF9
        cpu.jump('nx_next_3')
        cpu.label('nx_next_0')
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('nx_next_1')
        cpu.r0 = 0xDC
        cpu.r1 = 0x58
        cpu.er2 = 0x03
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_119')
        cpu.jump('cond_116')
        cpu.label('cond_119')
        cpu.r2 = 0xE2
        cpu.r3 = 0x58
        cpu.er2 += cpu.er0
        cpu.r0 = cpu.mem8[0x0F, cpu.er2]
        cpu.r1 = 0xF9
        cpu.jump('nx_next_3')
        cpu.label('nx_next_1')
        cpu.compare(cpu.r0, 0x02)
        if cpu.ne:
            cpu.branch('nx_next_2')
        cpu.r0 = 0xE6
        cpu.r1 = 0x58
        cpu.er2 = 0x08
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_120')
        cpu.jump('cond_116')
        cpu.label('cond_120')
        cpu.r2 = 0xF6
        cpu.r3 = 0x58
        cpu.er2 += cpu.er0
        cpu.r0 = cpu.mem8[0x0F, cpu.er2]
        cpu.r1 = 0xF9
        cpu.jump('nx_next_3')
        cpu.label('nx_next_2')
        cpu.compare(cpu.r0, 0x03)
        if cpu.ne:
            cpu.branch('nx_next_3')
        cpu.r0 = 0xFE
        cpu.r1 = 0x58
        cpu.er2 = 0x07
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_121')
        cpu.jump('cond_116')
        cpu.label('cond_121')
        cpu.r2 = 0x0C
        cpu.r3 = 0x59
        cpu.er2 += cpu.er0
        cpu.r0 = cpu.mem8[0x0F, cpu.er2]
        cpu.r1 = 0xF9
        cpu.jump('nx_next_3')
        cpu.label('nx_next_3')
        cpu.label('nx_out')
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('choose')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.er10 = cpu.er2
        cpu.er12 = 0x00
        cpu.er0 = cpu.sp
        cpu.r2 = 0x32
        cpu.r3 = 0x83
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('cond_122')
        cpu.jump('choose_no_stack')
        cpu.label('cond_122')
        cpu.sp += -40
        cpu.er14 = cpu.sp
        cpu.r0 = cpu.mem8[0x00, 0x80A0]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0020)] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, 0x80A1]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0021)] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, 0x80A2]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0022)] = cpu.r0
        cpu.r0 = 0x08
        cpu.mem8[0x00, 0x80A0] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, 0x80A1] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x00, 0x80A2] = cpu.r0
        cpu.label('choose_page')
        cpu.call(0x0409A)
        cpu.er4 = 0x00
        cpu.label('choose_row')
        cpu.er0 = cpu.er12
        cpu.er0 += cpu.er4
        cpu.compare(cpu.er0, cpu.er10)
        if cpu.ge:
            cpu.branch('choose_key')
        cpu.shift_left_carry(cpu.r1, 0x01)
        cpu.r0 <<= 0x01
        cpu.er0 += cpu.er8
        cpu.er6 = cpu.mem16[0x0F, cpu.er0]
        cpu.r0 = cpu.r4
        cpu.r0 += 0x31
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0000)] = cpu.r0
        cpu.r0 = 0x3A
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0001)] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x02
        cpu.r1 = 0x0D
        cpu.label('choose_text')
        cpu.r0 = cpu.mem8[0x0F, cpu.er6]
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('choose_draw')
        cpu.er6 += 0x01
        cpu.er2 += 0x01
        cpu.r1 += 0xFF
        if cpu.ne:
            cpu.branch('choose_text')
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.label('choose_draw')
        cpu.r1 = cpu.r4
        cpu.r1 <<= 0x03
        cpu.r1 += 0x01
        cpu.r0 = 0x00
        cpu.er2 = cpu.er14
        cpu.push(cpu.er4)
        cpu.call(ROM_DRAW_TEXT)
        cpu.pop(cpu.er4)
        cpu.er4 += 0x01
        cpu.compare(cpu.r4, 0x04)
        if cpu.lt:
            cpu.branch('choose_row')
        cpu.label('choose_key')
        cpu.call(ROM_REFRESH)
        cpu.call(HEX_KEY_ADDRESS)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.branch('choose_cancel')
        cpu.compare(cpu.r0, 0xFC)
        if cpu.eq:
            cpu.branch('choose_left')
        cpu.compare(cpu.r0, 0xFD)
        if cpu.eq:
            cpu.branch('choose_right')
        cpu.compare(cpu.r0, 0x31)
        if cpu.ge:
            cpu.branch('cond_123')
        cpu.jump('choose_key')
        cpu.label('cond_123')
        cpu.compare(cpu.r0, 0x35)
        if cpu.lt:
            cpu.branch('cond_124')
        cpu.jump('choose_key')
        cpu.label('cond_124')
        cpu.r0 += 0xCF
        cpu.r1 = 0x00
        cpu.er0 += cpu.er12
        cpu.compare(cpu.er0, cpu.er10)
        if cpu.lt:
            cpu.branch('cond_125')
        cpu.jump('choose_key')
        cpu.label('cond_125')
        cpu.jump('choose_out')
        cpu.label('choose_left')
        cpu.compare(cpu.r12, 0x04)
        if cpu.ge:
            cpu.branch('cond_126')
        cpu.jump('choose_key')
        cpu.label('cond_126')
        cpu.er12 += -4
        cpu.jump('choose_page')
        cpu.label('choose_right')
        cpu.er0 = cpu.er12
        cpu.er0 += 0x04
        cpu.compare(cpu.er0, cpu.er10)
        if cpu.lt:
            cpu.branch('cond_127')
        cpu.jump('choose_key')
        cpu.label('cond_127')
        cpu.er12 = cpu.er0
        cpu.jump('choose_page')
        cpu.label('choose_cancel')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.label('choose_out')
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0024)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0020)]
        cpu.mem8[0x00, 0x80A0] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0021)]
        cpu.mem8[0x00, 0x80A1] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0022)]
        cpu.mem8[0x00, 0x80A2] = cpu.r0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0024)]
        cpu.sp += 0x28
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('choose_no_stack')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('reason_screen')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('reason_screen_show')
        cpu.ret()
        cpu.label('reason_screen_show')
        cpu.push(cpu.lr)
        cpu.compare(cpu.r0, 0x07)
        if cpu.lt:
            cpu.branch('reason_screen_index')
        cpu.er0 = 0x01
        cpu.label('reason_screen_index')
        cpu.er0 += -1
        cpu.shift_left_carry(cpu.r1, 0x01)
        cpu.r0 <<= 0x01
        cpu.r2 = 0x74
        cpu.r3 = 0x5B
        cpu.er2 += cpu.er0
        cpu.er0 = cpu.mem16[0x0F, cpu.er2]
        cpu.call('error_screen')
        cpu.pop(cpu.pc)
        cpu.label('error_screen')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.sp += -40
        cpu.er14 = cpu.sp
        cpu.r0 = cpu.mem8[0x00, 0x80A0]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0020)] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, 0x80A1]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0021)] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, 0x80A2]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0022)] = cpu.r0
        cpu.r0 = 0x08
        cpu.mem8[0x00, 0x80A0] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, 0x80A1] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x00, 0x80A2] = cpu.r0
        cpu.call(0x0409A)
        cpu.r6 = 0x8C
        cpu.r7 = 0x5B
        cpu.r1 = 0x01
        cpu.call('error_line')
        cpu.er6 = cpu.er8
        cpu.r1 = 0x09
        cpu.call('error_line')
        cpu.r6 = 0x96
        cpu.r7 = 0x5B
        cpu.r1 = 0x19
        cpu.call('error_line')
        cpu.call(ROM_REFRESH)
        cpu.label('error_wait')
        cpu.call(HEX_KEY_ADDRESS)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('error_wait')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0020)]
        cpu.mem8[0x00, 0x80A0] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0021)]
        cpu.mem8[0x00, 0x80A1] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0022)]
        cpu.mem8[0x00, 0x80A2] = cpu.r0
        cpu.sp += 0x28
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('error_line')
        cpu.push(cpu.lr)
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0023)] = cpu.r1
        cpu.er2 = cpu.er14
        cpu.label('error_line_copy')
        cpu.r0 = cpu.mem8[0x0F, cpu.er6]
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.er6 += 0x01
        cpu.er2 += 0x01
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('error_line_copy')
        cpu.r0 = 0x00
        cpu.r1 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0023)]
        cpu.er2 = cpu.er14
        cpu.call(ROM_DRAW_TEXT)
        cpu.pop(cpu.pc)
        cpu.label('editor_input')
        cpu.compare(cpu.r11, 0x03)
        if cpu.ne:
            cpu.branch('cond_128')
        cpu.jump('editor_input_native')
        cpu.label('cond_128')
        cpu.push(cpu.xr0)
        cpu.push(cpu.xr4)
        cpu.er0 = cpu.er14
        cpu.call('editor_context')
        cpu.r3 = cpu.r0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0xFFDC)]
        cpu.compare(cpu.r1, 0xF9)
        if cpu.ne:
            cpu.branch('editor_ascii')
        cpu.compare(cpu.r0, 0xE0)
        if cpu.lt:
            cpu.branch('editor_input_restore')
        cpu.compare(cpu.r0, 0xF9)
        if cpu.ge:
            cpu.branch('editor_input_restore')
        cpu.sp += -4
        cpu.er6 = cpu.sp
        cpu.mem8[0x00, cpu.er6] = cpu.r1
        cpu.mem8[0x00, cpu.offset(cpu.er6, 0x0001)] = cpu.r0
        cpu.r2 = 0x20
        cpu.compare(cpu.r0, 0xE0)
        if cpu.eq:
            cpu.branch('editor_parenthesis')
        cpu.compare(cpu.r0, 0xE1)
        if cpu.eq:
            cpu.branch('editor_parenthesis')
        cpu.compare(cpu.r0, 0xE4)
        if cpu.eq:
            cpu.branch('editor_parenthesis')
        cpu.compare(cpu.r0, 0xE5)
        if cpu.eq:
            cpu.branch('editor_parenthesis')
        cpu.compare(cpu.r0, 0xE6)
        if cpu.eq:
            cpu.branch('editor_parenthesis')
        cpu.compare(cpu.r0, 0xE7)
        if cpu.eq:
            cpu.branch('editor_parenthesis')
        cpu.compare(cpu.r0, 0xE8)
        if cpu.eq:
            cpu.branch('editor_parenthesis')
        cpu.compare(cpu.r0, 0xE9)
        if cpu.eq:
            cpu.branch('editor_parenthesis')
        cpu.compare(cpu.r0, 0xEA)
        if cpu.eq:
            cpu.branch('editor_parenthesis')
        cpu.compare(cpu.r0, 0xEB)
        if cpu.eq:
            cpu.branch('editor_parenthesis')
        cpu.compare(cpu.r0, 0xEC)
        if cpu.eq:
            cpu.branch('editor_parenthesis')
        cpu.jump('editor_token_text')
        cpu.label('editor_parenthesis')
        cpu.r2 = 0x28
        cpu.label('editor_token_text')
        cpu.mem8[0x00, cpu.offset(cpu.er6, 0x0002)] = cpu.r2
        cpu.er0 = cpu.er6
        cpu.er2 = 0x03
        cpu.jump('editor_insert_buffer')
        cpu.label('editor_ascii')
        cpu.compare(cpu.r3, 0x01)
        if cpu.ne:
            cpu.branch('editor_input_restore')
        cpu.compare(cpu.r1, 0x7D)
        if cpu.ne:
            cpu.branch('editor_ascii_byte')
        cpu.compare(cpu.r0, 0x15)
        if cpu.ne:
            cpu.branch('editor_input_restore')
        cpu.er0 = 0x0D
        cpu.jump('editor_ascii_ready')
        cpu.label('editor_ascii_byte')
        cpu.compare(cpu.r1, 0x00)
        if cpu.ne:
            cpu.branch('editor_input_restore')
        cpu.compare(cpu.r0, 0x0E)
        if cpu.ne:
            cpu.branch('editor_ascii_range')
        cpu.r0 = 0x0D
        cpu.jump('editor_ascii_ready')
        cpu.label('editor_ascii_range')
        cpu.compare(cpu.r0, 0x20)
        if cpu.lt:
            cpu.branch('editor_input_restore')
        cpu.compare(cpu.r0, 0x7F)
        if cpu.ge:
            cpu.branch('editor_input_restore')
        cpu.label('editor_ascii_ready')
        cpu.sp += -4
        cpu.er6 = cpu.sp
        cpu.mem8[0x00, cpu.er6] = cpu.r0
        cpu.er0 = cpu.er6
        cpu.er2 = 0x01
        cpu.label('editor_insert_buffer')
        cpu.r4 = 0x00
        cpu.er6 = cpu.er14
        cpu.call('editor_insert')
        cpu.sp += 0x04
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('editor_insert_failed')
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.xr0)
        cpu.jump(0xC877C)
        cpu.label('editor_insert_failed')
        cpu.pop(cpu.xr4)
        cpu.sp += 0x04
        cpu.er4 = cpu.er0
        cpu.jump(0xC8922)
        cpu.label('editor_input_restore')
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.xr0)
        cpu.label('editor_input_native')
        cpu.er2 = cpu.er2
        if cpu.ne:
            cpu.branch('editor_input_nonzero')
        cpu.jump(0xC8896)
        cpu.label('editor_input_nonzero')
        cpu.jump(0xC8852)
        cpu.label('editor_insert')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.er10 = cpu.er2
        cpu.er12 = cpu.er6
        cpu.er0 = cpu.sp
        cpu.r2 = 0x92
        cpu.r3 = 0x84
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('cond_129')
        cpu.jump('editor_insert_stack')
        cpu.label('cond_129')
        cpu.sp += -20
        cpu.er14 = cpu.sp
        cpu.r5 = 0x00
        cpu.push(cpu.er4)
        cpu.push(cpu.er8)
        cpu.er0 = 0x00
        cpu.push(cpu.er0)
        cpu.push(cpu.er10)
        cpu.push(cpu.er0)
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er12, 0xFFD6)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0010)] = cpu.er0
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er12
        cpu.er0 += -64
        cpu.er0 += -4
        cpu.call(NATIVE_PROGRAM_INSERT)
        cpu.sp += 0x0C
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('editor_insert_out')
        cpu.er0 = cpu.er14
        cpu.er0 += 0x08
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 0x04
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er14
        cpu.er0 = cpu.er12
        cpu.er0 += -64
        cpu.er0 += -4
        cpu.call(NATIVE_PROGRAM_LOOKUP)
        cpu.sp += 0x04
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('editor_insert_out')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0004)]
        cpu.er0 += 0x06
        cpu.mem16[0x00, cpu.offset(cpu.er12, 0xFFB4)] = cpu.er0
        cpu.mem16[0x00, cpu.offset(cpu.er12, 0xFFE0)] = cpu.er0
        cpu.mem16[0x00, cpu.offset(cpu.er12, 0xFFEC)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0006)]
        cpu.mem8[0x00, cpu.offset(cpu.er12, 0xFFB6)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er12, 0xFFE2)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er12, 0xFFEE)] = cpu.r0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0008)]
        cpu.er0 += -1
        cpu.mem16[0x00, cpu.offset(cpu.er12, 0xFFAE)] = cpu.er0
        cpu.mem16[0x00, cpu.offset(cpu.er12, 0xFFB8)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)]
        cpu.mem16[0x00, cpu.offset(cpu.er12, 0xFFBA)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0000)]
        cpu.mem16[0x00, cpu.offset(cpu.er12, 0xFFB0)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0002)]
        cpu.mem16[0x00, cpu.offset(cpu.er12, 0xFFB2)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0010)]
        cpu.er0 += cpu.er10
        cpu.mem16[0x00, cpu.offset(cpu.er12, 0xFFD6)] = cpu.er0
        cpu.er0 = 0x00
        cpu.label('editor_insert_out')
        cpu.sp += 0x14
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('editor_insert_stack')
        cpu.er0 = 0x06
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('block_menu')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er12 = cpu.er6
        cpu.label('block_categories')
        cpu.r0 = 0x14
        cpu.r1 = 0x59
        cpu.er2 = 0x04
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_130')
        cpu.jump('block_out')
        cpu.label('cond_130')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('cond_131')
        cpu.jump('block_next_3')
        cpu.label('cond_131')
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('block_next_1')
        cpu.r0 = 0x28
        cpu.r1 = 0x59
        cpu.er2 = 0x21
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_132')
        cpu.jump('block_categories')
        cpu.label('cond_132')
        cpu.r2 = 0x6A
        cpu.r3 = 0x59
        cpu.jump('block_op_next_5')
        cpu.label('block_next_1')
        cpu.compare(cpu.r0, 0x02)
        if cpu.ne:
            cpu.branch('block_next_2')
        cpu.r0 = 0xAC
        cpu.r1 = 0x59
        cpu.er2 = 0x14
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_133')
        cpu.jump('block_categories')
        cpu.label('cond_133')
        cpu.r2 = 0xD4
        cpu.r3 = 0x59
        cpu.jump('block_op_next_5')
        cpu.label('block_next_2')
        cpu.compare(cpu.r0, 0x03)
        if cpu.ne:
            cpu.branch('block_next_3')
        cpu.r0 = 0xFC
        cpu.r1 = 0x59
        cpu.er2 = 0x03
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_134')
        cpu.jump('block_categories')
        cpu.label('cond_134')
        cpu.r2 = 0x02
        cpu.r3 = 0x5A
        cpu.jump('block_op_next_5')
        cpu.label('block_next_3')
        cpu.label('block_op')
        cpu.r0 = 0x1C
        cpu.r1 = 0x59
        cpu.er2 = 0x06
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_135')
        cpu.jump('block_categories')
        cpu.label('cond_135')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('block_op_next_0')
        cpu.r0 = 0x08
        cpu.r1 = 0x5A
        cpu.er2 = 0x22
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_136')
        cpu.jump('block_next_3')
        cpu.label('cond_136')
        cpu.r2 = 0x4C
        cpu.r3 = 0x5A
        cpu.jump('block_op_next_5')
        cpu.label('block_op_next_0')
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('block_op_next_1')
        cpu.r0 = 0x90
        cpu.r1 = 0x5A
        cpu.er2 = 0x06
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_137')
        cpu.jump('block_next_3')
        cpu.label('cond_137')
        cpu.r2 = 0x9C
        cpu.r3 = 0x5A
        cpu.jump('block_op_next_5')
        cpu.label('block_op_next_1')
        cpu.compare(cpu.r0, 0x02)
        if cpu.ne:
            cpu.branch('block_op_next_2')
        cpu.r0 = 0xA8
        cpu.r1 = 0x5A
        cpu.er2 = 0x10
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_138')
        cpu.jump('block_next_3')
        cpu.label('cond_138')
        cpu.r2 = 0xC8
        cpu.r3 = 0x5A
        cpu.jump('block_op_next_5')
        cpu.label('block_op_next_2')
        cpu.compare(cpu.r0, 0x03)
        if cpu.ne:
            cpu.branch('block_op_next_3')
        cpu.r0 = 0xE8
        cpu.r1 = 0x5A
        cpu.er2 = 0x0C
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_139')
        cpu.jump('block_next_3')
        cpu.label('cond_139')
        cpu.r2 = 0x00
        cpu.r3 = 0x5B
        cpu.jump('block_op_next_5')
        cpu.label('block_op_next_3')
        cpu.compare(cpu.r0, 0x04)
        if cpu.ne:
            cpu.branch('block_op_next_4')
        cpu.r0 = 0x18
        cpu.r1 = 0x5B
        cpu.er2 = 0x0D
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_140')
        cpu.jump('block_next_3')
        cpu.label('cond_140')
        cpu.r2 = 0x32
        cpu.r3 = 0x5B
        cpu.jump('block_op_next_5')
        cpu.label('block_op_next_4')
        cpu.compare(cpu.r0, 0x05)
        if cpu.ne:
            cpu.branch('block_op_next_5')
        cpu.r0 = 0x4C
        cpu.r1 = 0x5B
        cpu.er2 = 0x0A
        cpu.call('choose')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('cond_141')
        cpu.jump('block_next_3')
        cpu.label('cond_141')
        cpu.r2 = 0x60
        cpu.r3 = 0x5B
        cpu.jump('block_op_next_5')
        cpu.label('block_op_next_5')
        cpu.label('block_selected')
        cpu.shift_left_carry(cpu.r1, 0x01)
        cpu.r0 <<= 0x01
        cpu.er2 += cpu.er0
        cpu.er8 = cpu.mem16[0x0F, cpu.er2]
        cpu.r0 = cpu.mem8[0x0F, cpu.er8]
        cpu.compare(cpu.r0, 0xF9)
        if cpu.ne:
            cpu.branch('cond_142')
        cpu.er0 = cpu.er12
        cpu.call('editor_context')
        cpu.compare(cpu.r1, 0x01)
        if cpu.eq:
            cpu.branch('cond_142')
        cpu.jump('block_categories')
        cpu.label('cond_142')
        cpu.label('block_length')
        cpu.er10 = 0x00
        cpu.er2 = cpu.er8
        cpu.label('block_count')
        cpu.r0 = cpu.mem8[0x0F, cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('block_insert')
        cpu.er2 += 0x01
        cpu.er10 += 0x01
        cpu.jump('block_count')
        cpu.label('block_insert')
        cpu.er0 = cpu.er8
        cpu.er2 = cpu.er10
        cpu.r4 = 0x0F
        cpu.er6 = cpu.er12
        cpu.call('editor_insert')
        cpu.label('block_out')
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
