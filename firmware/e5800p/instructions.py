"""Fixed-layout e5800p instructions routines and tables."""

from kits import cpu

HEX_KEY_ADDRESS = 0x825CA
CODEC_SOURCE_LENGTH_ADDRESS = 0x80444
CODEC_LENGTH_ADDRESS = 0x80440
CODEC_ENCODE_ADDRESS = 0x808E0
ROM_REFRESH = 0x043BE
ROM_DRAW_TEXT = 0x041DA
UI_TEXT_ADDRESS = 0x81E06
SMALL_TEXT_ADDRESS = 0xF9000

INSTRUCTION_RECORDS = bytes((
    0x00, 0x01, 0x00, 0x10, 0x01, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x91, 0x00, 0xF0,
    0x01, 0x01, 0x01, 0x80, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x91, 0x0F, 0xF0,
    0x00, 0x01, 0x00, 0x60, 0x01, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x91, 0x00, 0xF0,
    0x01, 0x01, 0x06, 0x80, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x19, 0x91, 0x0F, 0xF0,
    0x03, 0x01, 0x80, 0xE0, 0x02, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x22, 0x91, 0x80, 0xF1,
    0x02, 0x01, 0x06, 0xF0, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2B, 0x91, 0x0F, 0xF1,
    0x01, 0x01, 0x08, 0x80, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x35, 0x91, 0x0F, 0xF0,
    0x01, 0x01, 0x09, 0x80, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3D, 0x91, 0x0F, 0xF0,
    0x17, 0x00, 0x08, 0x80, 0x01, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x46, 0x91, 0xFF, 0xFF,
    0x01, 0x01, 0x02, 0x80, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x4E, 0x91, 0x0F, 0xF0,
    0x00, 0x01, 0x00, 0x20, 0x01, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x56, 0x91, 0x00, 0xF0,
    0x01, 0x01, 0x03, 0x80, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5E, 0x91, 0x0F, 0xF0,
    0x00, 0x01, 0x00, 0x30, 0x01, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x65, 0x91, 0x00, 0xF0,
    0x01, 0x01, 0x04, 0x80, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x6C, 0x91, 0x0F, 0xF0,
    0x00, 0x01, 0x00, 0x40, 0x01, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x74, 0x91, 0x00, 0xF0,
    0x01, 0x01, 0x0A, 0x80, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7C, 0x91, 0x0F, 0xF0,
    0x04, 0x01, 0x0A, 0x90, 0x01, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x84, 0x91, 0x0F, 0xF0,
    0x01, 0x01, 0x0B, 0x80, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x8C, 0x91, 0x0F, 0xF0,
    0x04, 0x01, 0x0B, 0x90, 0x01, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x95, 0x91, 0x0F, 0xF0,
    0x01, 0x01, 0x0C, 0x80, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x9E, 0x91, 0x0F, 0xF0,
    0x04, 0x01, 0x0C, 0x90, 0x01, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xA6, 0x91, 0x0F, 0xF0,
    0x01, 0x01, 0x0D, 0x80, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xAE, 0x91, 0x0F, 0xF0,
    0x04, 0x01, 0x0E, 0x90, 0x01, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xB7, 0x91, 0x0F, 0xF0,
    0x01, 0x01, 0x0E, 0x80, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xBF, 0x91, 0x0F, 0xF0,
    0x05, 0x01, 0x04, 0xF0, 0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC7, 0x91, 0x0F, 0xF1,
    0x05, 0x01, 0x09, 0xF0, 0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xD0, 0x91, 0x0F, 0xF1,
    0x00, 0x01, 0x00, 0x70, 0x01, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0xD9, 0x91, 0x00, 0xF0,
    0x01, 0x01, 0x07, 0x80, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xE1, 0x91, 0x0F, 0xF0,
    0x00, 0x01, 0x00, 0x50, 0x01, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0xE9, 0x91, 0x00, 0xF0,
    0x01, 0x01, 0x05, 0x80, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xF2, 0x91, 0x0F, 0xF0,
    0x02, 0x01, 0x07, 0xF0, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFB, 0x91, 0x0F, 0xF1,
    0x06, 0x01, 0x1F, 0x80, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x92, 0xFF, 0xF0,
    0x06, 0x01, 0x3F, 0x80, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0B, 0x92, 0xFF, 0xF0,
    0x06, 0x01, 0x5F, 0x80, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x11, 0x92, 0xFF, 0xF0,
    0x00, 0x01, 0x00, 0x00, 0x01, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x17, 0x92, 0x00, 0xF0,
    0x01, 0x01, 0x00, 0x80, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0x92, 0x0F, 0xF0,
    0x02, 0x01, 0x05, 0xF0, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x27, 0x92, 0x0F, 0xF1,
    0x15, 0x01, 0x1A, 0xA0, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x31, 0x92, 0xFF, 0xF1,
    0x16, 0x01, 0x0A, 0xA1, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3B, 0x92, 0x0F, 0xFF,
    0x0E, 0x01, 0x00, 0xC0, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x45, 0x92, 0x00, 0xFF,
    0x0E, 0x01, 0x00, 0xC1, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x49, 0x92, 0x00, 0xFF,
    0x0E, 0x01, 0x00, 0xC2, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x4D, 0x92, 0x00, 0xFF,
    0x0E, 0x01, 0x00, 0xC3, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x51, 0x92, 0x00, 0xFF,
    0x0E, 0x01, 0x00, 0xC4, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x55, 0x92, 0x00, 0xFF,
    0x0E, 0x01, 0x00, 0xC5, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x5A, 0x92, 0x00, 0xFF,
    0x0E, 0x01, 0x00, 0xC6, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x5F, 0x92, 0x00, 0xFF,
    0x0E, 0x01, 0x00, 0xC7, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x64, 0x92, 0x00, 0xFF,
    0x0E, 0x01, 0x00, 0xC8, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x69, 0x92, 0x00, 0xFF,
    0x0E, 0x01, 0x00, 0xC9, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x6D, 0x92, 0x00, 0xFF,
    0x0E, 0x01, 0x00, 0xCA, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x71, 0x92, 0x00, 0xFF,
    0x0E, 0x01, 0x00, 0xCB, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x75, 0x92, 0x00, 0xFF,
    0x0E, 0x01, 0x00, 0xCC, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x79, 0x92, 0x00, 0xFF,
    0x0E, 0x01, 0x00, 0xCD, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x7D, 0x92, 0x00, 0xFF,
    0x0F, 0x01, 0x00, 0xF8, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x81, 0x92, 0xFF, 0xF8,
    0x0F, 0x01, 0x01, 0xF8, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x85, 0x92, 0xFF, 0xF8,
    0x08, 0x01, 0x10, 0x90, 0x01, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x8A, 0x92, 0xFF, 0xF0,
    0x09, 0x01, 0x00, 0x90, 0x01, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x93, 0x92, 0x1F, 0xF0,
    0x0A, 0x01, 0x08, 0x90, 0x01, 0x02, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x9C, 0x92, 0x1F, 0xF0,
    0x0B, 0x01, 0x12, 0x90, 0x02, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0xA6, 0x92, 0xFF, 0xF1,
    0x0C, 0x01, 0x02, 0x90, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xB0, 0x92, 0x1F, 0xF1,
    0x0D, 0x01, 0x08, 0xA0, 0x02, 0x02, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0xBA, 0x92, 0x1F, 0xF1,
    0x08, 0x01, 0x11, 0x90, 0x01, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0xC5, 0x92, 0xFF, 0xF0,
    0x09, 0x01, 0x01, 0x90, 0x01, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xCF, 0x92, 0x1F, 0xF0,
    0x0A, 0x01, 0x09, 0x90, 0x01, 0x02, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0xD9, 0x92, 0x1F, 0xF0,
    0x0B, 0x01, 0x13, 0x90, 0x02, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0xE4, 0x92, 0xFF, 0xF1,
    0x0C, 0x01, 0x03, 0x90, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEF, 0x92, 0x1F, 0xF1,
    0x0D, 0x01, 0x09, 0xA0, 0x02, 0x02, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0xFA, 0x92, 0x1F, 0xF1,
    0x06, 0x01, 0x4E, 0xF0, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x93, 0xFF, 0xF0,
    0x07, 0x01, 0x5E, 0xF0, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0D, 0x93, 0xFF, 0xF1,
    0x06, 0x01, 0x0E, 0xF0, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x15, 0x93, 0xFF, 0xF0,
    0x07, 0x01, 0x1E, 0xF0, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1B, 0x93, 0xFF, 0xF1,
    0x18, 0x01, 0x6E, 0xF0, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x22, 0x93, 0xFF, 0xF3,
    0x19, 0x01, 0x7E, 0xF0, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2A, 0x93, 0xFF, 0xF7,
    0x18, 0x01, 0x2E, 0xF0, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x32, 0x93, 0xFF, 0xF3,
    0x19, 0x01, 0x3E, 0xF0, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x39, 0x93, 0xFF, 0xF7,
    0x13, 0x01, 0xCE, 0xF8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x93, 0xFF, 0xFF,
    0x13, 0x01, 0x8E, 0xF8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x48, 0x93, 0xFF, 0xFF,
    0x13, 0x01, 0xCE, 0xF1, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x4F, 0x93, 0xFF, 0xFF,
    0x13, 0x01, 0x8E, 0xF1, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x57, 0x93, 0xFF, 0xFF,
    0x13, 0x01, 0x8E, 0xF2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5E, 0x93, 0xFF, 0xFF,
    0x10, 0x01, 0x01, 0xF0, 0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x00, 0x65, 0x93, 0xFF, 0xF0,
    0x11, 0x01, 0x01, 0xA0, 0x01, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x6E, 0x93, 0x0F, 0xF0,
    0x14, 0x01, 0x0F, 0x81, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x75, 0x93, 0x0F, 0xF1,
    0x12, 0x01, 0x00, 0xE1, 0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7E, 0x93, 0x00, 0xFF,
    0x13, 0x01, 0x80, 0xED, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x87, 0x93, 0xFF, 0xFF,
    0x13, 0x01, 0x7F, 0xEB, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x8A, 0x93, 0xFF, 0xFF,
    0x13, 0x01, 0xCF, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x8D, 0x93, 0xFF, 0xFF,
    0x13, 0x01, 0x8F, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x92, 0x93, 0xFF, 0xFF,
    0x13, 0x01, 0x1F, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x96, 0x93, 0xFF, 0xFF,
    0x13, 0x00, 0x1F, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x9A, 0x93, 0xFF, 0xFF,
    0x22, 0x05, 0x10, 0x0C, 0x0D, 0x0A, 0x00, 0x22, 0x27, 0x37, 0x43, 0x50,
))

INSTRUCTION_RECORDS_LABELS = {
    'instruction_records': 0x0,
}

ISA_DATA_CATEGORY_ROW_0 = b'1:ARITH 2:MOVE\x00'

ISA_DATA_CATEGORY_ROW_1 = b'3:BR    4:LOADST\x00'

ISA_DATA_CATEGORY_ROW_2 = b'5:STACK 6:MISC\x00'

ISA_DATA_CATEGORY_TITLE = b'ASSEMBLE\x00'

ISA_DATA_OPERAND_BAD_TEXT = b'BAD OPERAND\x00'

ISA_DATA_BRANCH_ODD_TEXT = b'ODD BR TARGET\x00'

ISA_DATA_BRANCH_OUTSIDE_TEXT = b'NOT IN S1 PROG\x00'

ISA_DATA_BRANCH_RANGE_TEXT = b'BR OUT OF RANGE\x00'

ISA_DATA_TABLE = (
    ISA_DATA_CATEGORY_ROW_0 +
    ISA_DATA_CATEGORY_ROW_1 +
    ISA_DATA_CATEGORY_ROW_2 +
    ISA_DATA_CATEGORY_TITLE +
    ISA_DATA_OPERAND_BAD_TEXT +
    ISA_DATA_BRANCH_ODD_TEXT +
    ISA_DATA_BRANCH_OUTSIDE_TEXT +
    ISA_DATA_BRANCH_RANGE_TEXT
)

ISA_DATA_LABELS = {
    'isa_data': 0x0,
    'category_row_0': 0x0,
    'category_row_1': 0xF,
    'category_row_2': 0x20,
    'category_title': 0x2F,
    'operand_bad_text': 0x38,
    'branch_odd_text': 0x44,
    'branch_outside_text': 0x52,
    'branch_range_text': 0x61,
}

INSTRUCTION_NAMES = (
    b'ADD R,#\x00'
    b'ADD R,R\x00'
    b'ADDC R,#\x00'
    b'ADDC R,R\x00'
    b'ADD ER,#\x00'
    b'ADD ER,ER\x00'
    b'SUB R,R\x00'
    b'SUBC R,R\x00'
    b'SUB R,#\x00'
    b'AND R,R\x00'
    b'AND R,#\x00'
    b'OR R,R\x00'
    b'OR R,#\x00'
    b'XOR R,R\x00'
    b'XOR R,#\x00'
    b'SLL R,R\x00'
    b'SLL R,#\x00'
    b'SLLC R,R\x00'
    b'SLLC R,#\x00'
    b'SRL R,R\x00'
    b'SRL R,#\x00'
    b'SRLC R,R\x00'
    b'SRA R,#\x00'
    b'SRA R,R\x00'
    b'MUL ER,R\x00'
    b'DIV ER,R\x00'
    b'CMP R,#\x00'
    b'CMP R,R\x00'
    b'CMPC R,#\x00'
    b'CMPC R,R\x00'
    b'CMP ER,ER\x00'
    b'DAA R\x00'
    b'DAS R\x00'
    b'NEG R\x00'
    b'MOV R,#\x00'
    b'MOV R,R\x00'
    b'MOV ER,ER\x00'
    b'MOV ER,SP\x00'
    b'MOV SP,ER\x00'
    b'BGE\x00'
    b'BLT\x00'
    b'BGT\x00'
    b'BLE\x00'
    b'BGES\x00'
    b'BLTS\x00'
    b'BGTS\x00'
    b'BLES\x00'
    b'BNE\x00'
    b'BEQ\x00'
    b'BNV\x00'
    b'BOV\x00'
    b'BPS\x00'
    b'BNS\x00'
    b'JMP\x00'
    b'CALL\x00'
    b'L R,ADDR\x00'
    b'L R,[ER]\x00'
    b'L R,D[ER]\x00'
    b'L ER,ADDR\x00'
    b'L ER,[ER]\x00'
    b'L ER,D[ER]\x00'
    b'ST R,ADDR\x00'
    b'ST R,[ER]\x00'
    b'ST R,D[ER]\x00'
    b'ST ER,ADDR\x00'
    b'ST ER,[ER]\x00'
    b'ST ER,D[ER]\x00'
    b'PUSH R\x00'
    b'PUSH ER\x00'
    b'POP R\x00'
    b'POP ER\x00'
    b'PUSH XR\x00'
    b'PUSH QR\x00'
    b'POP XR\x00'
    b'POP QR\x00'
    b'PUSH LR\x00'
    b'POP LR\x00'
    b'PUSH EA\x00'
    b'POP EA\x00'
    b'POP PC\x00'
    b'CALL_SYS\x00'
    b'TB R.B\x00'
    b'EXTBW ER\x00'
    b'ADD SP,#\x00'
    b'SC\x00'
    b'RC\x00'
    b'CPLC\x00'
    b'NOP\x00'
    b'RET\x00'
    b'END\x00'
    b'ARITH\x00'
    b'MOVE\x00'
    b'BRANCH\x00'
    b'LOAD/ST\x00'
    b'STACK\x00'
    b'MISC\x00'
    b'DW\x00'
)

INSTRUCTION_NAMES_LABELS = {
    'instruction_names': 0x0,
}

VIEWER_DATA = b'DISASM EXE:ASM F:MENU\x00'

VIEWER_DATA_LABELS = {
    'viewer_data': 0x0,
}


def install(fw):
    fw.data('instruction_records', INSTRUCTION_RECORDS, address=0x8113C, labels=INSTRUCTION_RECORDS_LABELS)
    fw.data('isa_data', ISA_DATA_TABLE, address=0xF8B64, labels=ISA_DATA_LABELS)
    fw.data('instruction_names', INSTRUCTION_NAMES, address=0xF9100, labels=INSTRUCTION_NAMES_LABELS)
    fw.data('viewer_data', VIEWER_DATA, address=0xFF844, labels=VIEWER_DATA_LABELS)

    @fw.function(native=True, address=0x80440)
    def codec_length():
        cpu.label('codec_length')
        cpu.jump('s1_length')
        cpu.jump('source_length')
        cpu.label('s1_length')
        cpu.push(cpu.lr)
        cpu.push(cpu.er2)
        cpu.push(cpu.xr4)
        cpu.er0 = cpu.er2
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_1')
        cpu.jump('s1_bad')
        cpu.label('skip_1')
        cpu.er0 = cpu.er2
        cpu.r4 = 0x00
        cpu.r5 = 0x40
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.ge:
            cpu.branch('skip_2')
        cpu.jump('s1_bad')
        cpu.label('skip_2')
        cpu.r4 = 0xF0
        cpu.r5 = 0x5F
        cpu.r2 = 0x08
        cpu.call('source_length')
        cpu.jump('s1_exit')
        cpu.label('s1_bad')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.label('s1_exit')
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.er2)
        cpu.pop(cpu.pc)
        cpu.label('source_length')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.er10 = cpu.er4
        cpu.r12 = cpu.r2
        cpu.r13 = 0x00
        cpu.r14 = 0x00
        cpu.r7 = 0x02
        cpu.call('fits')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_3')
        cpu.jump('source_bad')
        cpu.label('skip_3')
        cpu.r6 = 0x00
        cpu.call('read')
        cpu.r4 = cpu.r0
        cpu.r6 = 0x01
        cpu.call('read')
        cpu.r5 = cpu.r0
        cpu.compare(cpu.r5, 0xE3)
        if cpu.ne:
            cpu.branch('skip_4')
        cpu.jump('prefixed')
        cpu.label('skip_4')
        cpu.compare(cpu.r5, 0xFE)
        if cpu.ne:
            cpu.branch('skip_5')
        cpu.compare(cpu.r4, 0x9F)
        if cpu.ne:
            cpu.branch('skip_5')
        cpu.jump('prefixed')
        cpu.label('skip_5')
        cpu.label('prefix_register')
        cpu.compare(cpu.r5, 0x90)
        if cpu.ne:
            cpu.branch('skip_6')
        cpu.r0 = cpu.r4
        cpu.r0 &= 0x0F
        cpu.compare(cpu.r0, 0x0F)
        if cpu.ne:
            cpu.branch('skip_6')
        cpu.jump('prefixed')
        cpu.label('skip_6')
        cpu.label('unprefixed')
        cpu.call('word_length')
        cpu.compare(cpu.r4, 0x4E)
        if cpu.eq:
            cpu.branch('skip_7')
        cpu.jump('source_span')
        cpu.label('skip_7')
        cpu.r0 = cpu.r5
        cpu.r0 &= 0xFE
        cpu.compare(cpu.r0, 0xF0)
        if cpu.eq:
            cpu.branch('skip_8')
        cpu.jump('source_span')
        cpu.label('skip_8')
        cpu.r7 = 0x08
        cpu.call('fits')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_9')
        cpu.jump('source_two')
        cpu.label('skip_9')
        cpu.r15 = cpu.r5
        cpu.r15 &= 0x01
        cpu.r6 = 0x03
        cpu.call('read')
        cpu.compare(cpu.r0, cpu.r15)
        if cpu.eq:
            cpu.branch('skip_10')
        cpu.jump('source_two')
        cpu.label('skip_10')
        cpu.r6 = 0x04
        cpu.call('read')
        cpu.r6 = cpu.r15
        cpu.r6 <<= 0x04
        cpu.r6 |= 0x08
        cpu.compare(cpu.r0, cpu.r6)
        if cpu.eq:
            cpu.branch('skip_11')
        cpu.jump('source_two')
        cpu.label('skip_11')
        cpu.r6 = 0x05
        cpu.call('read')
        cpu.r6 = cpu.r0
        cpu.r6 &= 0xF0
        cpu.compare(cpu.r6, 0x80)
        if cpu.eq:
            cpu.branch('skip_12')
        cpu.jump('source_two')
        cpu.label('skip_12')
        cpu.r0 &= 0x0F
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('macro_r0')
        cpu.compare(cpu.r15, 0x00)
        if cpu.eq:
            cpu.branch('skip_13')
        cpu.jump('source_two')
        cpu.label('skip_13')
        cpu.jump('skip_14')
        cpu.label('macro_r0')
        cpu.compare(cpu.r15, 0x01)
        if cpu.eq:
            cpu.branch('skip_14')
        cpu.jump('source_two')
        cpu.label('skip_14')
        cpu.label('macro_pop')
        cpu.r6 = 0x06
        cpu.call('read')
        cpu.compare(cpu.r0, 0x0E)
        if cpu.eq:
            cpu.branch('skip_15')
        cpu.jump('source_two')
        cpu.label('skip_15')
        cpu.r6 = 0x07
        cpu.call('read')
        cpu.r15 |= 0xF0
        cpu.compare(cpu.r0, cpu.r15)
        if cpu.eq:
            cpu.branch('skip_16')
        cpu.jump('source_two')
        cpu.label('skip_16')
        cpu.r14 = 0x01
        cpu.r7 = 0x08
        cpu.jump('source_span')
        cpu.label('source_two')
        cpu.r7 = 0x02
        cpu.jump('source_span')
        cpu.label('prefixed')
        cpu.r7 = 0x04
        cpu.call('fits')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_17')
        cpu.jump('source_bad')
        cpu.label('skip_17')
        cpu.r6 = 0x02
        cpu.call('read')
        cpu.r4 = cpu.r0
        cpu.r6 = 0x03
        cpu.call('read')
        cpu.r5 = cpu.r0
        cpu.r0 = cpu.r5
        cpu.r0 &= 0xF0
        cpu.compare(cpu.r0, 0x90)
        if cpu.eq:
            cpu.branch('prefix_memory')
        cpu.compare(cpu.r0, 0xA0)
        if cpu.eq:
            cpu.branch('skip_18')
        cpu.jump('source_bad')
        cpu.label('skip_18')
        cpu.r0 = cpu.r4
        cpu.r0 &= 0x0E
        cpu.compare(cpu.r0, 0x08)
        if cpu.eq:
            cpu.branch('skip_19')
        cpu.jump('source_bad')
        cpu.label('skip_19')
        cpu.jump('skip_21')
        cpu.label('prefix_memory')
        cpu.r0 = cpu.r4
        cpu.r0 &= 0x0F
        cpu.compare(cpu.r0, 0x04)
        if cpu.lt:
            cpu.branch('skip_21')
        cpu.compare(cpu.r0, 0x08)
        if cpu.lt:
            cpu.branch('prefix_ea')
        cpu.compare(cpu.r0, 0x0A)
        if cpu.lt:
            cpu.branch('skip_20')
        cpu.jump('source_bad')
        cpu.label('skip_20')
        cpu.jump('skip_21')
        cpu.label('prefix_ea')
        cpu.r0 = cpu.r4
        cpu.r0 &= 0xC0
        if cpu.eq:
            cpu.branch('skip_21')
        cpu.jump('source_bad')
        cpu.label('skip_21')
        cpu.label('prefix_length')
        cpu.r13 = 0x02
        cpu.call('word_length')
        cpu.r7 += 0x02
        cpu.label('source_span')
        cpu.call('fits')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_22')
        cpu.jump('source_bad')
        cpu.label('skip_22')
        cpu.r0 = cpu.r7
        cpu.r1 = 0x00
        cpu.r2 = cpu.r13
        cpu.r3 = cpu.r14
        cpu.jump('source_exit')
        cpu.label('source_bad')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.r2 = 0x00
        cpu.r3 = 0x00
        cpu.label('source_exit')
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('fits')
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r7
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.compare(cpu.er0, cpu.er8)
        if cpu.lt:
            cpu.branch('fits_bad')
        cpu.compare(cpu.er0, cpu.er10)
        if cpu.lt:
            cpu.branch('fits_ok')
        if cpu.eq:
            cpu.branch('fits_ok')
        cpu.label('fits_bad')
        cpu.r0 = 0x01
        cpu.ret()
        cpu.label('fits_ok')
        cpu.r0 = 0x00
        cpu.ret()
        cpu.label('read')
        cpu.er2 = cpu.er8
        cpu.r7 = 0x00
        cpu.er2 += cpu.er6
        cpu.r0 = cpu.mem8[cpu.r12, cpu.er2]
        cpu.ret()
        cpu.label('word_length')
        cpu.r7 = 0x02
        cpu.r0 = cpu.r5
        cpu.r0 &= 0xF0
        cpu.compare(cpu.r0, 0x90)
        if cpu.eq:
            cpu.branch('word_load')
        cpu.compare(cpu.r0, 0xA0)
        if cpu.eq:
            cpu.branch('word_aload')
        cpu.compare(cpu.r0, 0xF0)
        if cpu.ne:
            cpu.branch('word_done')
        cpu.r0 = cpu.r4
        cpu.r0 &= 0x0F
        cpu.compare(cpu.r0, 0x02)
        if cpu.lt:
            cpu.branch('word_four')
        cpu.compare(cpu.r5, 0xF0)
        if cpu.ne:
            cpu.branch('word_done')
        cpu.compare(cpu.r0, 0x0B)
        if cpu.eq:
            cpu.branch('word_four')
        cpu.compare(cpu.r4, 0x0C)
        if cpu.eq:
            cpu.branch('word_four')
        cpu.jump('word_done')
        cpu.label('word_load')
        cpu.r0 = cpu.r4
        cpu.r0 &= 0x0E
        cpu.compare(cpu.r0, 0x08)
        if cpu.eq:
            cpu.branch('word_four')
        cpu.r0 = cpu.r4
        cpu.r0 &= 0xFE
        cpu.compare(cpu.r0, 0x10)
        if cpu.eq:
            cpu.branch('word_four')
        cpu.compare(cpu.r0, 0x12)
        if cpu.eq:
            cpu.branch('word_four')
        cpu.jump('word_done')
        cpu.label('word_aload')
        cpu.r0 = cpu.r4
        cpu.r0 &= 0x0E
        cpu.compare(cpu.r0, 0x08)
        if cpu.eq:
            cpu.branch('word_four')
        cpu.compare(cpu.r5, 0xA0)
        if cpu.ne:
            cpu.branch('word_done')
        cpu.r0 = cpu.r4
        cpu.r0 &= 0x8F
        cpu.compare(cpu.r0, 0x80)
        if cpu.eq:
            cpu.branch('word_four')
        cpu.compare(cpu.r0, 0x81)
        if cpu.eq:
            cpu.branch('word_four')
        cpu.compare(cpu.r0, 0x82)
        if cpu.eq:
            cpu.branch('word_four')
        cpu.label('word_done')
        cpu.ret()
        cpu.label('word_four')
        cpu.r7 = 0x04
        cpu.ret()


    @fw.function(native=True, address=0x808E0)
    def codec_encode():
        cpu.label('codec_encode')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.er10 = cpu.er2
        cpu.er12 = cpu.er4
        cpu.sp += -96
        cpu.er14 = cpu.sp
        cpu.mem16[cpu.offset(cpu.er14, 0x22)] = cpu.er6
        cpu.mem16[cpu.offset(cpu.er14, 0x24)] = cpu.er8
        cpu.r0 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += 0x26
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = cpu.r8
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_1')
        cpu.jump('enc_odd')
        cpu.label('skip_1')
        cpu.er0 = cpu.er10
        cpu.r2 = 0x3C
        cpu.r3 = 0x11
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_2')
        cpu.jump('enc_operand')
        cpu.label('skip_2')
        cpu.r2 = 0xDC
        cpu.r3 = 0x16
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('skip_3')
        cpu.jump('enc_operand')
        cpu.label('skip_3')
        cpu.r0 += 0xF4
        cpu.r0 &= 0x0F
        if cpu.eq:
            cpu.branch('skip_4')
        cpu.jump('enc_operand')
        cpu.label('skip_4')
        cpu.r0 = cpu.mem8[0x08, cpu.er10]
        cpu.mem8[cpu.offset(cpu.er14, 0x29)] = cpu.r0
        cpu.er10 += 0x02
        cpu.r0 = cpu.mem8[0x08, cpu.er10]
        cpu.mem8[cpu.offset(cpu.er14, 0x2A)] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = cpu.mem8[0x08, cpu.er10]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2F
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er10 += 0x01
        cpu.er8 = cpu.er14
        cpu.er8 += 0x20
        cpu.er8 += 0x20
        cpu.r6 = 0x00
        cpu.label('enc_fields')
        cpu.r0 = cpu.mem8[0x00, cpu.er12]
        cpu.mem8[0x00, cpu.er8] = cpu.r0
        cpu.compare(cpu.r6, 0x07)
        if cpu.ne:
            cpu.branch('skip_5')
        cpu.jump('enc_fields_done')
        cpu.label('skip_5')
        cpu.r7 = cpu.mem8[0x08, cpu.er10]
        cpu.compare(cpu.r7, 0x00)
        if cpu.ne:
            cpu.branch('skip_6')
        cpu.jump('skip_15')
        cpu.label('skip_6')
        cpu.compare(cpu.r0, 0x10)
        if cpu.lt:
            cpu.branch('skip_7')
        cpu.jump('enc_operand')
        cpu.label('skip_7')
        cpu.compare(cpu.r7, 0x02)
        if cpu.eq:
            cpu.branch('skip_8')
        cpu.jump('skip_9')
        cpu.label('skip_8')
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_9')
        cpu.jump('enc_operand')
        cpu.label('skip_9')
        cpu.label('enc_not_er')
        cpu.compare(cpu.r7, 0x03)
        if cpu.eq:
            cpu.branch('skip_10')
        cpu.jump('skip_11')
        cpu.label('skip_10')
        cpu.compare(cpu.r0, 0x08)
        if cpu.lt:
            cpu.branch('skip_11')
        cpu.jump('enc_operand')
        cpu.label('skip_11')
        cpu.label('enc_not_bit')
        cpu.compare(cpu.r7, 0x05)
        if cpu.eq:
            cpu.branch('skip_12')
        cpu.jump('skip_13')
        cpu.label('skip_12')
        cpu.r0 &= 0x03
        if cpu.eq:
            cpu.branch('skip_13')
        cpu.jump('enc_operand')
        cpu.label('skip_13')
        cpu.label('enc_not_xr')
        cpu.compare(cpu.r7, 0x06)
        if cpu.eq:
            cpu.branch('skip_14')
        cpu.jump('skip_15')
        cpu.label('skip_14')
        cpu.r0 &= 0x07
        if cpu.eq:
            cpu.branch('skip_15')
        cpu.jump('enc_operand')
        cpu.label('skip_15')
        cpu.label('enc_field_next')
        cpu.er8 += 0x01
        cpu.er10 += 0x01
        cpu.er12 += 0x01
        cpu.r6 += 0x01
        cpu.jump('enc_fields')
        cpu.label('enc_fields_done')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x40)]
        cpu.mem8[cpu.offset(cpu.er14, 0x2D)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x41)]
        cpu.mem8[cpu.offset(cpu.er14, 0x2E)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x29)]
        cpu.compare(cpu.r0, 0x03)
        if cpu.eq:
            cpu.branch('skip_16')
        cpu.jump('skip_17')
        cpu.label('skip_16')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x21
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x08)
        if cpu.lt:
            cpu.branch('skip_17')
        cpu.jump('enc_operand')
        cpu.label('skip_17')
        cpu.label('enc_target')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x29
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x0E)
        if cpu.eq:
            cpu.branch('skip_18')
        cpu.jump('enc_far_check')
        cpu.label('skip_18')
        cpu.call('branch_target')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_19')
        cpu.jump('enc_failed')
        cpu.label('skip_19')
        cpu.jump('skip_23')
        cpu.label('enc_far_check')
        cpu.compare(cpu.r0, 0x0F)
        if cpu.eq:
            cpu.branch('skip_20')
        cpu.jump('enc_sys_check')
        cpu.label('skip_20')
        cpu.r0 = 0x00
        cpu.call('pack')
        cpu.r9 = cpu.r0
        cpu.r0 = 0x02
        cpu.call('pack')
        cpu.r8 = cpu.r0
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_21')
        cpu.jump('enc_odd')
        cpu.label('skip_21')
        cpu.jump('skip_23')
        cpu.label('enc_sys_check')
        cpu.compare(cpu.r0, 0x10)
        if cpu.eq:
            cpu.branch('skip_22')
        cpu.jump('skip_23')
        cpu.label('skip_22')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x24
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_23')
        cpu.jump('enc_odd')
        cpu.label('skip_23')
        cpu.label('enc_assemble')
        cpu.call('assemble')
        cpu.r9 = 0x02
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x29)]
        cpu.compare(cpu.r0, 0x17)
        if cpu.eq:
            cpu.branch('skip_24')
        cpu.jump('enc_size_normal')
        cpu.label('skip_24')
        cpu.r9 = 0x08
        cpu.jump('enc_segment')
        cpu.label('enc_size_normal')
        cpu.compare(cpu.r0, 0x08)
        if cpu.ne:
            cpu.branch('skip_25')
        cpu.jump('enc_size_four')
        cpu.label('skip_25')
        cpu.compare(cpu.r0, 0x0A)
        if cpu.ne:
            cpu.branch('skip_26')
        cpu.jump('enc_size_four')
        cpu.label('skip_26')
        cpu.compare(cpu.r0, 0x0B)
        if cpu.ne:
            cpu.branch('skip_27')
        cpu.jump('enc_size_four')
        cpu.label('skip_27')
        cpu.compare(cpu.r0, 0x0D)
        if cpu.ne:
            cpu.branch('skip_28')
        cpu.jump('enc_size_four')
        cpu.label('skip_28')
        cpu.compare(cpu.r0, 0x0F)
        if cpu.ne:
            cpu.branch('skip_29')
        cpu.jump('enc_size_four')
        cpu.label('skip_29')
        cpu.compare(cpu.r0, 0x10)
        if cpu.ne:
            cpu.branch('skip_30')
        cpu.jump('enc_size_four')
        cpu.label('skip_30')
        cpu.jump('enc_segment')
        cpu.label('enc_size_four')
        cpu.r9 = 0x04
        cpu.label('enc_segment')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x29)]
        cpu.compare(cpu.r0, 0x08)
        if cpu.ge:
            cpu.branch('skip_31')
        cpu.jump('enc_copy')
        cpu.label('skip_31')
        cpu.compare(cpu.r0, 0x0E)
        if cpu.lt:
            cpu.branch('skip_32')
        cpu.jump('enc_copy')
        cpu.label('skip_32')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x27
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0xFF)
        if cpu.ne:
            cpu.branch('skip_33')
        cpu.jump('enc_copy')
        cpu.label('skip_33')
        cpu.compare(cpu.r0, 0x10)
        if cpu.lt:
            cpu.branch('skip_34')
        cpu.jump('enc_operand')
        cpu.label('skip_34')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x37)]
        cpu.mem8[cpu.offset(cpu.er14, 0x39)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x36)]
        cpu.mem8[cpu.offset(cpu.er14, 0x38)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x35)]
        cpu.mem8[cpu.offset(cpu.er14, 0x37)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x34)]
        cpu.mem8[cpu.offset(cpu.er14, 0x36)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x47)]
        cpu.mem8[cpu.offset(cpu.er14, 0x34)] = cpu.r0
        cpu.r0 = 0xE3
        cpu.mem8[cpu.offset(cpu.er14, 0x35)] = cpu.r0
        cpu.r9 += 0x02
        cpu.label('enc_copy')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x24)]
        cpu.r2 = cpu.r9
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        if cpu.ge:
            cpu.branch('skip_35')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('skip_35')
        cpu.jump('enc_outside')
        cpu.label('skip_35')
        cpu.label('enc_copy_ready')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x22
        cpu.er10 = cpu.mem16[cpu.er2]
        cpu.er2 += 0x01
        cpu.r5 = cpu.r9
        cpu.er8 = cpu.er14
        cpu.er8 += 0x34
        cpu.r6 = cpu.r5
        cpu.label('enc_copy_byte')
        cpu.r0 = cpu.mem8[0x00, cpu.er8]
        cpu.mem8[0x00, cpu.er10] = cpu.r0
        cpu.er8 += 0x01
        cpu.er10 += 0x01
        cpu.r6 += 0xFF
        cpu.compare(cpu.r6, 0x00)
        if cpu.eq:
            cpu.branch('skip_36')
        cpu.jump('enc_copy_byte')
        cpu.label('skip_36')
        cpu.r2 = cpu.r5
        cpu.er0 = 0x00
        cpu.jump('enc_exit')
        cpu.label('enc_operand')
        cpu.r0 = 0x01
        cpu.jump('enc_failed')
        cpu.label('enc_odd')
        cpu.r0 = 0x02
        cpu.jump('enc_failed')
        cpu.label('enc_outside')
        cpu.r0 = 0x03
        cpu.jump('enc_failed')
        cpu.label('enc_failed')
        cpu.r1 = 0x00
        cpu.r2 = 0x00
        cpu.label('enc_exit')
        cpu.sp += 0x60
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('pack')
        cpu.r6 = cpu.r0
        cpu.r7 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x20
        cpu.er2 += cpu.er6
        cpu.r8 = cpu.mem8[cpu.er2]
        cpu.r8 <<= 0x04
        cpu.r6 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x20
        cpu.er2 += cpu.er6
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 |= cpu.r8
        cpu.ret()
        cpu.label('branch_target')
        cpu.push(cpu.lr)
        cpu.r0 = 0x00
        cpu.call('pack')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x30
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = 0x02
        cpu.call('pack')
        cpu.r8 = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x30
        cpu.r9 = cpu.mem8[cpu.er2]
        cpu.r0 = cpu.r8
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_37')
        cpu.jump('branch_odd')
        cpu.label('skip_37')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x24)]
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, 0x26)]
        cpu.r0 += cpu.r6
        cpu.add_carry(cpu.r1, 0x00)
        cpu.er0 += 0x02
        cpu.r8 -= cpu.r0
        cpu.sub_carry(cpu.r9, cpu.r1)
        cpu.compare(cpu.r9, 0x00)
        if cpu.ne:
            cpu.branch('skip_38')
        cpu.jump('branch_forward')
        cpu.label('skip_38')
        cpu.compare(cpu.r9, 0xFF)
        if cpu.eq:
            cpu.branch('skip_39')
        cpu.jump('branch_range')
        cpu.label('skip_39')
        cpu.r8 >>= 0x01
        cpu.r8 |= 0x80
        cpu.jump('branch_ready')
        cpu.label('branch_forward')
        cpu.compare(cpu.r8, 0xFF)
        if cpu.ne:
            cpu.branch('skip_40')
        cpu.jump('branch_range')
        cpu.label('skip_40')
        cpu.r8 >>= 0x01
        cpu.label('branch_ready')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x30
        cpu.mem8[cpu.er2] = cpu.r8
        cpu.r0 = 0x00
        cpu.pop(cpu.pc)
        cpu.label('branch_odd')
        cpu.r0 = 0x02
        cpu.jump('branch_fail')
        cpu.label('branch_range')
        cpu.r0 = 0x04
        cpu.label('branch_fail')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x30
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.pop(cpu.pc)
        cpu.label('assemble')
        cpu.push(cpu.lr)
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2A)]
        cpu.mem8[cpu.offset(cpu.er14, 0x34)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2F)]
        cpu.mem8[cpu.offset(cpu.er14, 0x35)] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x29
        cpu.r6 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r6, 0x00)
        if cpu.ne:
            cpu.branch('skip_41')
        cpu.jump('asm_imm')
        cpu.label('skip_41')
        cpu.compare(cpu.r6, 0x17)
        if cpu.ne:
            cpu.branch('skip_42')
        cpu.jump('asm_sub_imm')
        cpu.label('skip_42')
        cpu.compare(cpu.r6, 0x01)
        if cpu.ne:
            cpu.branch('skip_43')
        cpu.jump('asm_pair')
        cpu.label('skip_43')
        cpu.compare(cpu.r6, 0x02)
        if cpu.ne:
            cpu.branch('skip_44')
        cpu.jump('asm_pair')
        cpu.label('skip_44')
        cpu.compare(cpu.r6, 0x03)
        if cpu.ne:
            cpu.branch('skip_45')
        cpu.jump('asm_ei7')
        cpu.label('skip_45')
        cpu.compare(cpu.r6, 0x04)
        if cpu.ne:
            cpu.branch('skip_46')
        cpu.jump('asm_shift')
        cpu.label('skip_46')
        cpu.compare(cpu.r6, 0x05)
        if cpu.ne:
            cpu.branch('skip_47')
        cpu.jump('asm_er_r')
        cpu.label('skip_47')
        cpu.compare(cpu.r6, 0x06)
        if cpu.ne:
            cpu.branch('skip_48')
        cpu.jump('asm_one')
        cpu.label('skip_48')
        cpu.compare(cpu.r6, 0x07)
        if cpu.ne:
            cpu.branch('skip_49')
        cpu.jump('asm_one')
        cpu.label('skip_49')
        cpu.compare(cpu.r6, 0x18)
        if cpu.ne:
            cpu.branch('skip_50')
        cpu.jump('asm_one')
        cpu.label('skip_50')
        cpu.compare(cpu.r6, 0x19)
        if cpu.ne:
            cpu.branch('skip_51')
        cpu.jump('asm_one')
        cpu.label('skip_51')
        cpu.compare(cpu.r6, 0x08)
        if cpu.ne:
            cpu.branch('skip_52')
        cpu.jump('asm_abs')
        cpu.label('skip_52')
        cpu.compare(cpu.r6, 0x0B)
        if cpu.ne:
            cpu.branch('skip_53')
        cpu.jump('asm_abs')
        cpu.label('skip_53')
        cpu.compare(cpu.r6, 0x09)
        if cpu.ne:
            cpu.branch('skip_54')
        cpu.jump('asm_pair')
        cpu.label('skip_54')
        cpu.compare(cpu.r6, 0x0C)
        if cpu.ne:
            cpu.branch('skip_55')
        cpu.jump('asm_pair')
        cpu.label('skip_55')
        cpu.compare(cpu.r6, 0x0A)
        if cpu.ne:
            cpu.branch('skip_56')
        cpu.jump('asm_disp')
        cpu.label('skip_56')
        cpu.compare(cpu.r6, 0x0D)
        if cpu.ne:
            cpu.branch('skip_57')
        cpu.jump('asm_disp')
        cpu.label('skip_57')
        cpu.compare(cpu.r6, 0x0E)
        if cpu.ne:
            cpu.branch('skip_58')
        cpu.jump('asm_branch')
        cpu.label('skip_58')
        cpu.compare(cpu.r6, 0x0F)
        if cpu.ne:
            cpu.branch('skip_59')
        cpu.jump('asm_far')
        cpu.label('skip_59')
        cpu.compare(cpu.r6, 0x10)
        if cpu.ne:
            cpu.branch('skip_60')
        cpu.jump('asm_sys')
        cpu.label('skip_60')
        cpu.compare(cpu.r6, 0x11)
        if cpu.ne:
            cpu.branch('skip_61')
        cpu.jump('asm_shift')
        cpu.label('skip_61')
        cpu.compare(cpu.r6, 0x12)
        if cpu.ne:
            cpu.branch('skip_62')
        cpu.jump('asm_sp_imm')
        cpu.label('skip_62')
        cpu.compare(cpu.r6, 0x14)
        if cpu.ne:
            cpu.branch('skip_63')
        cpu.jump('asm_extbw')
        cpu.label('skip_63')
        cpu.compare(cpu.r6, 0x15)
        if cpu.ne:
            cpu.branch('skip_64')
        cpu.jump('asm_one')
        cpu.label('skip_64')
        cpu.compare(cpu.r6, 0x16)
        if cpu.ne:
            cpu.branch('skip_65')
        cpu.jump('asm_sp_er')
        cpu.label('skip_65')
        cpu.jump('asm_done')
        cpu.label('asm_imm')
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x2D)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x35)]
        cpu.r0 |= cpu.r7
        cpu.er2 = cpu.er14
        cpu.er2 += 0x35
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = 0x01
        cpu.jump('asm_pack_imm')
        cpu.label('asm_sp_imm')
        cpu.r0 = 0x00
        cpu.label('asm_pack_imm')
        cpu.call('pack')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x34
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('asm_done')
        cpu.label('asm_sub_imm')
        cpu.r0 = 0x01
        cpu.call('pack')
        cpu.mem8[cpu.offset(cpu.er14, 0x36)] = cpu.r0
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x2D)]
        cpu.compare(cpu.r7, 0x00)
        if cpu.eq:
            cpu.branch('skip_66')
        cpu.jump('sub_tmp_zero')
        cpu.label('skip_66')
        cpu.r6 = 0x01
        cpu.jump('sub_tmp_ready')
        cpu.label('sub_tmp_zero')
        cpu.r6 = 0x00
        cpu.label('sub_tmp_ready')
        cpu.r0 = 0x4E
        cpu.mem8[cpu.offset(cpu.er14, 0x34)] = cpu.r0
        cpu.r0 = cpu.r6
        cpu.r0 |= 0xF0
        cpu.mem8[cpu.offset(cpu.er14, 0x35)] = cpu.r0
        cpu.r0 = cpu.r6
        cpu.mem8[cpu.offset(cpu.er14, 0x37)] = cpu.r0
        cpu.r0 = cpu.r6
        cpu.r0 <<= 0x04
        cpu.r0 |= 0x08
        cpu.mem8[cpu.offset(cpu.er14, 0x38)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2D)]
        cpu.r0 |= 0x80
        cpu.mem8[cpu.offset(cpu.er14, 0x39)] = cpu.r0
        cpu.r0 = 0x0E
        cpu.mem8[cpu.offset(cpu.er14, 0x3A)] = cpu.r0
        cpu.r0 = cpu.r6
        cpu.r0 |= 0xF0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3B
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('asm_done')
        cpu.label('asm_pair')
        cpu.call('asm_dest')
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x2A)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2E)]
        cpu.r0 <<= 0x04
        cpu.r7 |= cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x34
        cpu.mem8[cpu.er2] = cpu.r7
        cpu.jump('asm_done')
        cpu.label('asm_ei7')
        cpu.call('asm_dest')
        cpu.r0 = 0x01
        cpu.call('pack')
        cpu.r0 |= 0x80
        cpu.er2 = cpu.er14
        cpu.er2 += 0x34
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('asm_done')
        cpu.label('asm_shift')
        cpu.call('asm_dest')
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x2A)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2E)]
        cpu.r0 <<= 0x04
        cpu.r7 |= cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x34
        cpu.mem8[cpu.er2] = cpu.r7
        cpu.jump('asm_done')
        cpu.label('asm_er_r')
        cpu.call('asm_dest')
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x2A)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2E)]
        cpu.r0 <<= 0x04
        cpu.r7 |= cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x34
        cpu.mem8[cpu.er2] = cpu.r7
        cpu.jump('asm_done')
        cpu.label('asm_one')
        cpu.call('asm_dest')
        cpu.jump('asm_done')
        cpu.label('asm_sp_er')
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x2A)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2D)]
        cpu.r0 <<= 0x04
        cpu.r7 |= cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x34
        cpu.mem8[cpu.er2] = cpu.r7
        cpu.jump('asm_done')
        cpu.label('asm_extbw')
        cpu.call('asm_dest')
        cpu.jump('asm_sp_er')
        cpu.label('asm_abs')
        cpu.call('asm_dest')
        cpu.r0 = 0x01
        cpu.jump('asm_word')
        cpu.label('asm_disp')
        cpu.call('asm_dest')
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x2A)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2E)]
        cpu.r0 <<= 0x04
        cpu.r7 |= cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x34
        cpu.mem8[cpu.er2] = cpu.r7
        cpu.r0 = 0x02
        cpu.label('asm_word')
        cpu.r9 = cpu.r0
        cpu.call('pack')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x37
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = cpu.r9
        cpu.r0 += 0x02
        cpu.call('pack')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x36
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('asm_done')
        cpu.label('asm_branch')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x30)]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x34
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('asm_done')
        cpu.label('asm_far')
        cpu.r0 = 0x00
        cpu.jump('asm_word')
        cpu.label('asm_sys')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x40)]
        cpu.r0 |= 0xF0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x35
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = 0x01
        cpu.jump('asm_word')
        cpu.label('asm_dest')
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x2D)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2F)]
        cpu.r0 |= cpu.r7
        cpu.er2 = cpu.er14
        cpu.er2 += 0x35
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.ret()
        cpu.label('asm_done')
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0xF7E68)
    def isa_entry():
        cpu.label('isa_entry')
        cpu.label('entry')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.er6)
        cpu.push(cpu.qr8)
        cpu.push(cpu.er12)
        cpu.push(cpu.er14)
        cpu.er8 = cpu.er6
        cpu.er10 = cpu.er0
        cpu.r7 = cpu.r5
        cpu.er12 = cpu.er2
        cpu.sp += -96
        cpu.er14 = cpu.sp
        cpu.mem16[cpu.offset(cpu.er14, 0x20)] = cpu.er10
        cpu.mem16[cpu.offset(cpu.er14, 0x22)] = cpu.er8
        cpu.mem16[cpu.offset(cpu.er14, 0x24)] = cpu.er12
        cpu.mem8[cpu.offset(cpu.er14, 0x26)] = cpu.r7
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 0x31)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 0x2D)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 0x2E)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 0x40)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 0x41)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 0x42)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 0x43)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 0x44)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 0x45)] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x26
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x10)
        if cpu.lt:
            cpu.branch('skip_1')
        cpu.jump('cancel')
        cpu.label('skip_1')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x26
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_2')
        cpu.jump('cancel')
        cpu.label('skip_2')
        cpu.label('categories')
        cpu.call('draw_categories')
        cpu.call('key')
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('skip_3')
        cpu.jump('cancel')
        cpu.label('skip_3')
        cpu.compare(cpu.r0, 0x31)
        if cpu.ge:
            cpu.branch('skip_4')
        cpu.jump('skip_2')
        cpu.label('skip_4')
        cpu.compare(cpu.r0, 0x37)
        if cpu.lt:
            cpu.branch('skip_5')
        cpu.jump('skip_2')
        cpu.label('skip_5')
        cpu.r0 += 0xCF
        cpu.mem8[cpu.offset(cpu.er14, 0x27)] = cpu.r0
        cpu.r0 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3C
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('browse')
        cpu.label('browse')
        cpu.call('draw_menu')
        cpu.call('key')
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('skip_6')
        cpu.jump('skip_2')
        cpu.label('skip_6')
        cpu.compare(cpu.r0, 0xFC)
        if cpu.ne:
            cpu.branch('skip_7')
        cpu.jump('page_left')
        cpu.label('skip_7')
        cpu.compare(cpu.r0, 0xFD)
        if cpu.ne:
            cpu.branch('skip_8')
        cpu.jump('page_right')
        cpu.label('skip_8')
        cpu.compare(cpu.r0, 0x31)
        if cpu.ge:
            cpu.branch('skip_9')
        cpu.jump('browse')
        cpu.label('skip_9')
        cpu.compare(cpu.r0, 0x35)
        if cpu.lt:
            cpu.branch('skip_10')
        cpu.jump('browse')
        cpu.label('skip_10')
        cpu.r0 += 0xCF
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3C
        cpu.r8 = cpu.mem8[cpu.er2]
        cpu.r0 += cpu.r8
        cpu.r8 = cpu.r0
        cpu.call('item_count')
        cpu.r0 = cpu.r8
        cpu.compare(cpu.r0, cpu.r7)
        if cpu.lt:
            cpu.branch('skip_11')
        cpu.jump('browse')
        cpu.label('skip_11')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x28
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('selected')
        cpu.label('page_left')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3C
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x04)
        if cpu.ge:
            cpu.branch('skip_12')
        cpu.jump('page_end')
        cpu.label('skip_12')
        cpu.r0 += 0xFC
        cpu.jump('skip_13')
        cpu.label('page_right')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3C
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 += 0x04
        cpu.r8 = cpu.r0
        cpu.call('item_count')
        cpu.r0 = cpu.r8
        cpu.compare(cpu.r0, cpu.r7)
        if cpu.lt:
            cpu.branch('skip_13')
        cpu.jump('page_begin')
        cpu.label('skip_13')
        cpu.label('page_store')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3C
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('browse')
        cpu.label('page_begin')
        cpu.r0 = 0x00
        cpu.jump('skip_13')
        cpu.label('page_end')
        cpu.call('item_count')
        cpu.r0 = cpu.r7
        cpu.r0 += 0xFF
        cpu.r0 &= 0xFC
        cpu.jump('skip_13')
        cpu.label('selected')
        cpu.call('record')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x29)]
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, 0x2A)]
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 0x31)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x2D)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x2E)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x34)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x35)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x36)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x37)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x40)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x41)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x42)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x43)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x44)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x45)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x46)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x47)] = cpu.r0
        cpu.r0 = 0xFF
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x27
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.call('old_length')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2B
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.label('operand')
        cpu.call('field_kind')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_14')
        cpu.jump('segment')
        cpu.label('skip_14')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x32
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.call('draw_operand')
        cpu.label('operand_key')
        cpu.call('key')
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('skip_15')
        cpu.jump('browse')
        cpu.label('skip_15')
        cpu.compare(cpu.r0, 0xFC)
        if cpu.ne:
            cpu.branch('skip_16')
        cpu.jump('operand_prev')
        cpu.label('skip_16')
        cpu.compare(cpu.r0, 0xFD)
        if cpu.ne:
            cpu.branch('skip_17')
        cpu.jump('operand_next')
        cpu.label('skip_17')
        cpu.compare(cpu.r0, 0xFE)
        if cpu.ne:
            cpu.branch('skip_18')
        cpu.jump('operand_down')
        cpu.label('skip_18')
        cpu.compare(cpu.r0, 0xFF)
        if cpu.ne:
            cpu.branch('skip_19')
        cpu.jump('operand_up')
        cpu.label('skip_19')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.ne:
            cpu.branch('skip_20')
        cpu.jump('operand_next')
        cpu.label('skip_20')
        cpu.compare(cpu.r0, 0x30)
        if cpu.ge:
            cpu.branch('skip_21')
        cpu.jump('operand_key')
        cpu.label('skip_21')
        cpu.compare(cpu.r0, 0x3A)
        if cpu.lt:
            cpu.branch('skip_22')
        cpu.jump('operand_letter')
        cpu.label('skip_22')
        cpu.r0 += 0xD0
        cpu.jump('operand_digit')
        cpu.label('operand_letter')
        cpu.compare(cpu.r0, 0x41)
        if cpu.ge:
            cpu.branch('skip_23')
        cpu.jump('operand_key')
        cpu.label('skip_23')
        cpu.compare(cpu.r0, 0x47)
        if cpu.lt:
            cpu.branch('skip_24')
        cpu.jump('operand_key')
        cpu.label('skip_24')
        cpu.r0 += 0xC9
        cpu.label('operand_digit')
        cpu.call('set_field')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_25')
        cpu.jump('operand_key')
        cpu.label('skip_25')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x31)]
        cpu.r0 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x31
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.call('field_kind')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_26')
        cpu.jump('operand')
        cpu.label('skip_26')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x31)]
        cpu.r0 += 0xFF
        cpu.er2 = cpu.er14
        cpu.er2 += 0x31
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.call('draw_operand')
        cpu.jump('operand_key')
        cpu.label('operand_down')
        cpu.r1 = 0xFF
        cpu.jump('operand_change')
        cpu.label('operand_up')
        cpu.r1 = 0x01
        cpu.label('operand_change')
        cpu.call('change_field')
        cpu.call('draw_operand')
        cpu.jump('operand_key')
        cpu.label('operand_prev')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x31
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_27')
        cpu.jump('operand_key')
        cpu.label('skip_27')
        cpu.r0 += 0xFF
        cpu.er2 = cpu.er14
        cpu.er2 += 0x31
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('operand')
        cpu.label('operand_next')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x31)]
        cpu.r0 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x31
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('operand')
        cpu.label('segment')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x29
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x08)
        if cpu.ge:
            cpu.branch('skip_28')
        cpu.jump('encode')
        cpu.label('skip_28')
        cpu.compare(cpu.r0, 0x0E)
        if cpu.lt:
            cpu.branch('skip_29')
        cpu.jump('encode')
        cpu.label('skip_29')
        cpu.label('segment_draw')
        cpu.call('draw_segment')
        cpu.label('segment_key')
        cpu.call('key')
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('skip_30')
        cpu.jump('browse')
        cpu.label('skip_30')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.ne:
            cpu.branch('skip_31')
        cpu.jump('encode')
        cpu.label('skip_31')
        cpu.compare(cpu.r0, 0x49)
        cpu.compare_carry(cpu.r1, 0x75)
        if cpu.ne:
            cpu.branch('skip_32')
        cpu.jump('segment_clear')
        cpu.label('skip_32')
        cpu.compare(cpu.r0, 0x30)
        if cpu.ge:
            cpu.branch('skip_33')
        cpu.jump('segment_key')
        cpu.label('skip_33')
        cpu.compare(cpu.r0, 0x3A)
        if cpu.lt:
            cpu.branch('skip_34')
        cpu.jump('segment_letter')
        cpu.label('skip_34')
        cpu.r0 += 0xD0
        cpu.jump('segment_store')
        cpu.label('segment_letter')
        cpu.compare(cpu.r0, 0x41)
        if cpu.ge:
            cpu.branch('skip_35')
        cpu.jump('segment_key')
        cpu.label('skip_35')
        cpu.compare(cpu.r0, 0x47)
        if cpu.lt:
            cpu.branch('skip_36')
        cpu.jump('segment_key')
        cpu.label('skip_36')
        cpu.r0 += 0xC9
        cpu.jump('segment_store')
        cpu.label('segment_clear')
        cpu.r0 = 0xFF
        cpu.label('segment_store')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x27
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('skip_29')
        cpu.label('encode')
        cpu.call('assemble')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_37')
        cpu.jump('bad_target')
        cpu.label('skip_37')
        cpu.call('draw_result')
        cpu.label('confirm')
        cpu.call('key')
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('skip_38')
        cpu.jump('browse')
        cpu.label('skip_38')
        cpu.compare(cpu.r0, 0xFC)
        if cpu.ne:
            cpu.branch('skip_39')
        cpu.jump('result_back')
        cpu.label('skip_39')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.ne:
            cpu.branch('skip_40')
        cpu.jump('commit')
        cpu.label('skip_40')
        cpu.jump('confirm')
        cpu.label('result_back')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x31
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_41')
        cpu.jump('confirm')
        cpu.label('skip_41')
        cpu.r0 += 0xFF
        cpu.er2 = cpu.er14
        cpu.er2 += 0x31
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('operand')
        cpu.label('bad_target')
        cpu.call('draw_bad_target')
        cpu.label('bad_target_key')
        cpu.call('key')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_42')
        cpu.jump('bad_target_key')
        cpu.label('skip_42')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x31)]
        cpu.r0 += 0xFF
        cpu.er2 = cpu.er14
        cpu.er2 += 0x31
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('operand')
        cpu.label('commit')
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x22)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2B)]
        cpu.mem8[cpu.er8] = cpu.r0
        cpu.er8 += 0x01
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2C)]
        cpu.mem8[cpu.er8] = cpu.r0
        cpu.er8 += 0x01
        cpu.r7 = 0x08
        cpu.er2 = cpu.er14
        cpu.er2 += 0x34
        cpu.label('commit_loop')
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.mem8[cpu.er8] = cpu.r0
        cpu.er8 += 0x01
        cpu.er2 += 0x01
        cpu.r7 += 0xFF
        cpu.compare(cpu.r7, 0x00)
        if cpu.eq:
            cpu.branch('skip_43')
        cpu.jump('commit_loop')
        cpu.label('skip_43')
        cpu.er0 = 0x00
        cpu.jump('exit')
        cpu.label('cancel')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.label('exit')
        cpu.sp += 0x60
        cpu.pop(cpu.er14)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.er6)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('key')
        cpu.push(cpu.lr)
        cpu.push(cpu.er4)
        cpu.call(HEX_KEY_ADDRESS)
        cpu.pop(cpu.er4)
        cpu.pop(cpu.pc)
        cpu.label('item_count')
        cpu.r0 = 0xDC
        cpu.r1 = 0x16
        cpu.er2 = cpu.er14
        cpu.er2 += 0x27
        cpu.r6 = cpu.mem8[cpu.er2]
        cpu.r7 = 0x00
        cpu.er0 += cpu.er6
        cpu.r7 = cpu.mem8[0x08, cpu.er0]
        cpu.ret()
        cpu.label('record')
        cpu.r0 = 0xE2
        cpu.r1 = 0x16
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, 0x27)]
        cpu.r7 = 0x00
        cpu.er0 += cpu.er6
        cpu.r6 = cpu.mem8[0x08, cpu.er0]
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x28)]
        cpu.r6 += cpu.r7
        cpu.r2 = cpu.r6
        cpu.r3 = 0x00
        cpu.r0 = 0x10
        cpu.multiply(cpu.er2, cpu.r0)
        cpu.r0 = 0x3C
        cpu.r1 = 0x11
        cpu.er0 += cpu.er2
        cpu.mem16[cpu.offset(cpu.er14, 0x4E)] = cpu.er0
        cpu.r6 = cpu.mem8[0x08, cpu.er0]
        cpu.er0 += 0x02
        cpu.r7 = cpu.mem8[0x08, cpu.er0]
        cpu.mem8[cpu.offset(cpu.er14, 0x29)] = cpu.r6
        cpu.mem8[cpu.offset(cpu.er14, 0x2A)] = cpu.r7
        cpu.er0 += 0x01
        cpu.r7 = cpu.mem8[0x08, cpu.er0]
        cpu.mem8[cpu.offset(cpu.er14, 0x2F)] = cpu.r7
        cpu.er0 += 0x09
        cpu.r6 = cpu.mem8[0x08, cpu.er0]
        cpu.er0 += 0x01
        cpu.r7 = cpu.mem8[0x08, cpu.er0]
        cpu.r0 = cpu.r6
        cpu.r1 = cpu.r7
        cpu.mem16[cpu.offset(cpu.er14, 0x50)] = cpu.er0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x29)]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2A
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.ret()
        cpu.label('field_kind')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x4E)]
        cpu.er0 += 0x04
        cpu.er2 = cpu.er14
        cpu.er2 += 0x31
        cpu.r6 = cpu.mem8[cpu.er2]
        cpu.r7 = 0x00
        cpu.er0 += cpu.er6
        cpu.r0 = cpu.mem8[0x08, cpu.er0]
        cpu.ret()
        cpu.label('set_field')
        cpu.r1 = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x32
        cpu.r7 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r7, 0x05)
        if cpu.eq:
            cpu.branch('skip_44')
        cpu.jump('skip_45')
        cpu.label('skip_44')
        cpu.r0 &= 0x03
        if cpu.eq:
            cpu.branch('skip_45')
        cpu.jump('set_invalid')
        cpu.label('skip_45')
        cpu.label('set_not_xr')
        cpu.compare(cpu.r7, 0x06)
        if cpu.eq:
            cpu.branch('skip_46')
        cpu.jump('skip_47')
        cpu.label('skip_46')
        cpu.r0 = cpu.r1
        cpu.r0 &= 0x07
        if cpu.eq:
            cpu.branch('skip_47')
        cpu.jump('set_invalid')
        cpu.label('skip_47')
        cpu.label('set_not_qr')
        cpu.compare(cpu.r7, 0x02)
        if cpu.eq:
            cpu.branch('skip_48')
        cpu.jump('skip_49')
        cpu.label('skip_48')
        cpu.r0 = cpu.r1
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_49')
        cpu.jump('set_invalid')
        cpu.label('skip_49')
        cpu.label('set_not_er')
        cpu.compare(cpu.r7, 0x03)
        if cpu.eq:
            cpu.branch('skip_50')
        cpu.jump('skip_51')
        cpu.label('skip_50')
        cpu.compare(cpu.r1, 0x08)
        if cpu.lt:
            cpu.branch('skip_51')
        cpu.jump('set_invalid')
        cpu.label('skip_51')
        cpu.label('set_hex_check')
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, 0x31)]
        cpu.compare(cpu.r7, 0x04)
        if cpu.eq:
            cpu.branch('skip_52')
        cpu.jump('set_register')
        cpu.label('skip_52')
        cpu.r6 += 0x40
        cpu.er2 = cpu.er14
        cpu.er2 += 0x29
        cpu.r7 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r7, 0x03)
        if cpu.eq:
            cpu.branch('skip_53')
        cpu.jump('skip_55')
        cpu.label('skip_53')
        cpu.compare(cpu.r6, 0x41)
        if cpu.eq:
            cpu.branch('skip_54')
        cpu.jump('skip_55')
        cpu.label('skip_54')
        cpu.compare(cpu.r1, 0x08)
        if cpu.lt:
            cpu.branch('skip_55')
        cpu.jump('set_invalid')
        cpu.label('skip_55')
        cpu.label('set_far')
        cpu.compare(cpu.r7, 0x0F)
        if cpu.eq:
            cpu.branch('skip_56')
        cpu.jump('skip_58')
        cpu.label('skip_56')
        cpu.compare(cpu.r6, 0x43)
        if cpu.eq:
            cpu.branch('skip_57')
        cpu.jump('skip_58')
        cpu.label('skip_57')
        cpu.r0 = cpu.r1
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_58')
        cpu.jump('set_invalid')
        cpu.label('skip_58')
        cpu.label('set_even_15')
        cpu.compare(cpu.r7, 0x10)
        if cpu.eq:
            cpu.branch('skip_59')
        cpu.jump('skip_61')
        cpu.label('skip_59')
        cpu.compare(cpu.r6, 0x44)
        if cpu.eq:
            cpu.branch('skip_60')
        cpu.jump('skip_61')
        cpu.label('skip_60')
        cpu.r0 = cpu.r1
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_61')
        cpu.jump('set_invalid')
        cpu.label('skip_61')
        cpu.label('set_even_16')
        cpu.compare(cpu.r7, 0x0B)
        if cpu.eq:
            cpu.branch('skip_62')
        cpu.jump('skip_64')
        cpu.label('skip_62')
        cpu.compare(cpu.r6, 0x44)
        if cpu.eq:
            cpu.branch('skip_63')
        cpu.jump('skip_64')
        cpu.label('skip_63')
        cpu.r0 = cpu.r1
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_64')
        cpu.jump('set_invalid')
        cpu.label('skip_64')
        cpu.label('set_even_11')
        cpu.jump('set_store')
        cpu.label('set_register')
        cpu.compare(cpu.r6, 0x00)
        if cpu.ne:
            cpu.branch('skip_65')
        cpu.jump('set_a')
        cpu.label('skip_65')
        cpu.r6 = 0x2E
        cpu.jump('set_store')
        cpu.label('set_a')
        cpu.r6 = 0x2D
        cpu.label('set_store')
        cpu.r7 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += cpu.er6
        cpu.mem8[cpu.er2] = cpu.r1
        cpu.r0 = 0x00
        cpu.ret()
        cpu.label('set_invalid')
        cpu.r0 = 0xFF
        cpu.ret()
        cpu.label('change_field')
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x32)]
        cpu.compare(cpu.r7, 0x04)
        if cpu.ne:
            cpu.branch('skip_66')
        cpu.jump('change_hex')
        cpu.label('skip_66')
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, 0x31)]
        cpu.compare(cpu.r6, 0x00)
        if cpu.ne:
            cpu.branch('skip_67')
        cpu.jump('change_a')
        cpu.label('skip_67')
        cpu.r6 = 0x2E
        cpu.jump('change_loaded')
        cpu.label('change_a')
        cpu.r6 = 0x2D
        cpu.jump('change_loaded')
        cpu.label('change_hex')
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, 0x31)]
        cpu.r6 += 0x40
        cpu.label('change_loaded')
        cpu.r7 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += cpu.er6
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x32)]
        cpu.compare(cpu.r7, 0x05)
        if cpu.eq:
            cpu.branch('skip_68')
        cpu.jump('change_not_xr')
        cpu.label('skip_68')
        cpu.r1 <<= 0x02
        cpu.jump('change_byte')
        cpu.label('change_not_xr')
        cpu.compare(cpu.r7, 0x06)
        if cpu.eq:
            cpu.branch('skip_69')
        cpu.jump('change_not_qr')
        cpu.label('skip_69')
        cpu.r1 <<= 0x03
        cpu.jump('change_byte')
        cpu.label('change_not_qr')
        cpu.compare(cpu.r7, 0x02)
        if cpu.eq:
            cpu.branch('skip_70')
        cpu.jump('change_byte')
        cpu.label('skip_70')
        cpu.r1 <<= 0x01
        cpu.label('change_byte')
        cpu.compare(cpu.r7, 0x04)
        if cpu.eq:
            cpu.branch('skip_71')
        cpu.jump('change_step_done')
        cpu.label('skip_71')
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x29)]
        cpu.compare(cpu.r7, 0x0F)
        if cpu.eq:
            cpu.branch('skip_72')
        cpu.jump('skip_73')
        cpu.label('skip_72')
        cpu.compare(cpu.r6, 0x43)
        if cpu.ne:
            cpu.branch('skip_73')
        cpu.jump('skip_77')
        cpu.label('skip_73')
        cpu.label('change_step_sys')
        cpu.compare(cpu.r7, 0x10)
        if cpu.eq:
            cpu.branch('skip_74')
        cpu.jump('skip_75')
        cpu.label('skip_74')
        cpu.compare(cpu.r6, 0x44)
        if cpu.ne:
            cpu.branch('skip_75')
        cpu.jump('skip_77')
        cpu.label('skip_75')
        cpu.label('change_step_abs')
        cpu.compare(cpu.r7, 0x0B)
        if cpu.eq:
            cpu.branch('skip_76')
        cpu.jump('change_step_done')
        cpu.label('skip_76')
        cpu.compare(cpu.r6, 0x44)
        if cpu.eq:
            cpu.branch('skip_77')
        cpu.jump('change_step_done')
        cpu.label('skip_77')
        cpu.label('change_step_even')
        cpu.r1 <<= 0x01
        cpu.label('change_step_done')
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x32)]
        cpu.r0 += cpu.r1
        cpu.compare(cpu.r7, 0x03)
        if cpu.ne:
            cpu.branch('skip_78')
        cpu.jump('change_bit')
        cpu.label('skip_78')
        cpu.compare(cpu.r7, 0x02)
        if cpu.ne:
            cpu.branch('skip_79')
        cpu.jump('change_er')
        cpu.label('skip_79')
        cpu.compare(cpu.r7, 0x05)
        if cpu.ne:
            cpu.branch('skip_80')
        cpu.jump('change_xr')
        cpu.label('skip_80')
        cpu.compare(cpu.r7, 0x06)
        if cpu.ne:
            cpu.branch('skip_81')
        cpu.jump('change_qr')
        cpu.label('skip_81')
        cpu.r0 &= 0x0F
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x29)]
        cpu.compare(cpu.r7, 0x03)
        if cpu.eq:
            cpu.branch('skip_82')
        cpu.jump('skip_83')
        cpu.label('skip_82')
        cpu.compare(cpu.r6, 0x41)
        if cpu.ne:
            cpu.branch('skip_83')
        cpu.jump('change_seven')
        cpu.label('skip_83')
        cpu.label('change_far')
        cpu.compare(cpu.r7, 0x0F)
        if cpu.eq:
            cpu.branch('skip_84')
        cpu.jump('skip_85')
        cpu.label('skip_84')
        cpu.compare(cpu.r6, 0x43)
        if cpu.ne:
            cpu.branch('skip_85')
        cpu.jump('skip_89')
        cpu.label('skip_85')
        cpu.label('change_sys')
        cpu.compare(cpu.r7, 0x10)
        if cpu.eq:
            cpu.branch('skip_86')
        cpu.jump('skip_87')
        cpu.label('skip_86')
        cpu.compare(cpu.r6, 0x44)
        if cpu.ne:
            cpu.branch('skip_87')
        cpu.jump('skip_89')
        cpu.label('skip_87')
        cpu.label('change_abs_er')
        cpu.compare(cpu.r7, 0x0B)
        if cpu.eq:
            cpu.branch('skip_88')
        cpu.jump('store_field')
        cpu.label('skip_88')
        cpu.compare(cpu.r6, 0x44)
        if cpu.eq:
            cpu.branch('skip_89')
        cpu.jump('store_field')
        cpu.label('skip_89')
        cpu.label('change_even')
        cpu.r0 &= 0x0E
        cpu.jump('store_field')
        cpu.label('change_seven')
        cpu.r0 &= 0x07
        cpu.jump('store_field')
        cpu.label('change_bit')
        cpu.r0 &= 0x07
        cpu.jump('store_field')
        cpu.label('change_er')
        cpu.r0 &= 0x0E
        cpu.jump('store_field')
        cpu.label('change_xr')
        cpu.r0 &= 0x0C
        cpu.jump('store_field')
        cpu.label('change_qr')
        cpu.r0 &= 0x08
        cpu.label('store_field')
        cpu.r7 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += cpu.er6
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.ret()
        cpu.label('old_length')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x20)]
        cpu.er4 = cpu.er0
        cpu.er4 += 0x10
        cpu.er2 = cpu.er14
        cpu.er2 += 0x26
        cpu.r6 = cpu.mem8[cpu.er2]
        cpu.r7 = 0x00
        cpu.er0 += cpu.er6
        cpu.r2 = 0x00
        cpu.call(CODEC_SOURCE_LENGTH_ADDRESS)
        cpu.compare(cpu.r1, 0xFF)
        if cpu.eq:
            cpu.branch('skip_90')
        cpu.jump('old_length_done')
        cpu.label('skip_90')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x24)]
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, 0x26)]
        cpu.r7 = 0x00
        cpu.er0 += cpu.er6
        cpu.er2 = cpu.er0
        cpu.call(CODEC_LENGTH_ADDRESS)
        cpu.compare(cpu.r1, 0xFF)
        if cpu.eq:
            cpu.branch('skip_91')
        cpu.jump('old_length_done')
        cpu.label('skip_91')
        cpu.er0 = 0x02
        cpu.label('old_length_done')
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('assemble')
        cpu.push(cpu.lr)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x4E)]
        cpu.er0 += 0x04
        cpu.r0 = cpu.mem8[0x08, cpu.er0]
        cpu.compare(cpu.r0, 0x04)
        if cpu.ne:
            cpu.branch('skip_92')
        cpu.jump('codec_nibble_0')
        cpu.label('skip_92')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2D)]
        cpu.mem8[cpu.offset(cpu.er14, 0x40)] = cpu.r0
        cpu.label('codec_nibble_0')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x4E)]
        cpu.er0 += 0x05
        cpu.r0 = cpu.mem8[0x08, cpu.er0]
        cpu.compare(cpu.r0, 0x04)
        if cpu.ne:
            cpu.branch('skip_93')
        cpu.jump('codec_nibble_1')
        cpu.label('skip_93')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2E)]
        cpu.mem8[cpu.offset(cpu.er14, 0x41)] = cpu.r0
        cpu.label('codec_nibble_1')
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 0x34)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x35)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x36)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x37)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x38)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x39)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x3A)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x3B)] = cpu.r0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x24)]
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, 0x26)]
        cpu.r7 = 0x00
        cpu.er0 += cpu.er6
        cpu.er8 = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x4E)]
        cpu.er2 = cpu.er0
        cpu.er4 = cpu.er14
        cpu.er4 += 0x20
        cpu.er4 += 0x20
        cpu.er6 = cpu.er14
        cpu.er6 += 0x34
        cpu.er0 = cpu.er8
        cpu.call(CODEC_ENCODE_ADDRESS)
        cpu.r7 = cpu.r2
        cpu.mem8[cpu.offset(cpu.er14, 0x30)] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2C
        cpu.mem8[cpu.er2] = cpu.r7
        cpu.pop(cpu.pc)
        cpu.label('draw_segment')
        cpu.push(cpu.lr)
        cpu.call(0x0409A)
        cpu.call('old_line')
        cpu.call('name_line')
        cpu.er10 = cpu.er14
        cpu.r0 = 0x53
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x45
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x47
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x20
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x27
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0xFF)
        if cpu.eq:
            cpu.branch('skip_94')
        cpu.jump('segment_value')
        cpu.label('skip_94')
        cpu.r0 = 0x2D
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.jump('segment_char')
        cpu.label('segment_value')
        cpu.call('hexchar')
        cpu.label('segment_char')
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x00
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.r1 = 0x11
        cpu.call('lcd')
        cpu.call(ROM_REFRESH)
        cpu.pop(cpu.pc)
        cpu.label('lcd')
        cpu.r0 = 0x07
        cpu.jump('lcd_font')
        cpu.label('menu_lcd')
        cpu.r0 = 0x08
        cpu.label('lcd_font')
        cpu.push(cpu.lr)
        cpu.mem8[cpu.offset(cpu.er14, 0x4C)] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A0]
        cpu.mem8[cpu.offset(cpu.er14, 0x4A)] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A2]
        cpu.mem8[cpu.offset(cpu.er14, 0x4B)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x4C)]
        cpu.mem8[0x80A0] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x80A2] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 0x33)] = cpu.r1
        cpu.r0 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += 0x33
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.push(cpu.er4)
        cpu.call(ROM_DRAW_TEXT)
        cpu.pop(cpu.er4)
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x4B)]
        cpu.mem8[0x80A2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x2A
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.mem8[0x80A0] = cpu.r0
        cpu.pop(cpu.pc)
        cpu.label('show')
        cpu.r0 = 0x07
        cpu.jump('show_font')
        cpu.label('menu_show')
        cpu.r0 = 0x08
        cpu.label('show_font')
        cpu.push(cpu.lr)
        cpu.er8 = cpu.er2
        cpu.mem8[cpu.offset(cpu.er14, 0x4C)] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x33
        cpu.mem8[cpu.er2] = cpu.r1
        cpu.er0 = cpu.er14
        cpu.er2 = cpu.er8
        cpu.er6 = 0x11
        cpu.call(UI_TEXT_ADDRESS)
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, 0x33)]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x2C
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.call('lcd_font')
        cpu.pop(cpu.pc)
        cpu.label('hexchar')
        cpu.compare(cpu.r0, 0x0A)
        if cpu.lt:
            cpu.branch('skip_95')
        cpu.jump('hex_letter')
        cpu.label('skip_95')
        cpu.r0 += 0x30
        cpu.ret()
        cpu.label('hex_letter')
        cpu.r0 += 0x37
        cpu.ret()
        cpu.label('hexbyte')
        cpu.push(cpu.lr)
        cpu.r7 = cpu.r0
        cpu.r0 >>= 0x04
        cpu.call('hexchar')
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = cpu.r7
        cpu.r0 &= 0x0F
        cpu.call('hexchar')
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.pop(cpu.pc)
        cpu.label('old_line')
        cpu.push(cpu.lr)
        cpu.er10 = cpu.er14
        cpu.call('old_length')
        cpu.mem8[cpu.offset(cpu.er14, 0x2B)] = cpu.r0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x24)]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x26
        cpu.r6 = cpu.mem8[cpu.er2]
        cpu.r0 += cpu.r6
        cpu.add_carry(cpu.r1, 0x00)
        cpu.r8 = cpu.r0
        cpu.r0 = cpu.r1
        cpu.call('hexbyte')
        cpu.r0 = cpu.r8
        cpu.call('hexbyte')
        cpu.r0 = 0x20
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r9 = 0x00
        cpu.label('old_bytes')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x26
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 += cpu.r9
        cpu.compare(cpu.r0, 0x10)
        if cpu.lt:
            cpu.branch('skip_96')
        cpu.jump('skip_97')
        cpu.label('skip_96')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x20)]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x26
        cpu.r6 = cpu.mem8[cpu.er2]
        cpu.r6 += cpu.r9
        cpu.r7 = 0x00
        cpu.er0 += cpu.er6
        cpu.r0 = cpu.mem8[cpu.er0]
        cpu.call('hexbyte')
        cpu.r9 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2B
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r9, cpu.r0)
        if cpu.ge:
            cpu.branch('skip_97')
        cpu.jump('old_bytes')
        cpu.label('skip_97')
        cpu.label('old_bytes_done')
        cpu.r0 = 0x00
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.r1 = 0x01
        cpu.call('lcd')
        cpu.pop(cpu.pc)
        cpu.label('name_line')
        cpu.push(cpu.lr)
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x30
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 += 0x01
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.r1 = 0x09
        cpu.call('show')
        cpu.pop(cpu.pc)
        cpu.label('menu_copy')
        cpu.push(cpu.lr)
        cpu.er0 = cpu.er10
        cpu.er2 = cpu.er6
        cpu.er6 = 0x0F
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.pc)
        cpu.label('menu_row')
        cpu.push(cpu.lr)
        cpu.er8 = cpu.er2
        cpu.er2 = cpu.er14
        cpu.er2 += 0x33
        cpu.mem8[cpu.er2] = cpu.r1
        cpu.er10 = cpu.er14
        cpu.r0 = cpu.r6
        cpu.r0 += 0x30
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x3A
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er6 = cpu.er8
        cpu.r9 = 0x0E
        cpu.call('menu_copy')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x33
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.call('menu_lcd')
        cpu.pop(cpu.pc)
        cpu.label('draw_categories')
        cpu.push(cpu.lr)
        cpu.call(0x0409A)
        cpu.r2 = 0x93
        cpu.r3 = 0x8B
        cpu.r1 = 0x01
        cpu.call('menu_show')
        cpu.r2 = 0x64
        cpu.r3 = 0x8B
        cpu.r1 = 0x09
        cpu.call('menu_show')
        cpu.r2 = 0x73
        cpu.r3 = 0x8B
        cpu.r1 = 0x11
        cpu.call('menu_show')
        cpu.r2 = 0x84
        cpu.r3 = 0x8B
        cpu.r1 = 0x19
        cpu.call('menu_show')
        cpu.call(ROM_REFRESH)
        cpu.pop(cpu.pc)
        cpu.label('draw_menu')
        cpu.push(cpu.lr)
        cpu.call(0x0409A)
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3C
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 += 0x00
        cpu.r8 = cpu.r0
        cpu.call('item_count')
        cpu.r0 = cpu.r8
        cpu.compare(cpu.r0, cpu.r7)
        if cpu.lt:
            cpu.branch('skip_98')
        cpu.jump('menu_row_skip_0')
        cpu.label('skip_98')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x28
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.call('record')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x30
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 += 0x01
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.r6 = 0x01
        cpu.r1 = 0x01
        cpu.call('menu_row')
        cpu.label('menu_row_skip_0')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3C
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 += 0x01
        cpu.r8 = cpu.r0
        cpu.call('item_count')
        cpu.r0 = cpu.r8
        cpu.compare(cpu.r0, cpu.r7)
        if cpu.lt:
            cpu.branch('skip_99')
        cpu.jump('menu_row_skip_1')
        cpu.label('skip_99')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x28
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.call('record')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x30
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 += 0x01
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.r6 = 0x02
        cpu.r1 = 0x09
        cpu.call('menu_row')
        cpu.label('menu_row_skip_1')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3C
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 += 0x02
        cpu.r8 = cpu.r0
        cpu.call('item_count')
        cpu.r0 = cpu.r8
        cpu.compare(cpu.r0, cpu.r7)
        if cpu.lt:
            cpu.branch('skip_100')
        cpu.jump('menu_row_skip_2')
        cpu.label('skip_100')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x28
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.call('record')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x30
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 += 0x01
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.r6 = 0x03
        cpu.r1 = 0x11
        cpu.call('menu_row')
        cpu.label('menu_row_skip_2')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3C
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 += 0x03
        cpu.r8 = cpu.r0
        cpu.call('item_count')
        cpu.r0 = cpu.r8
        cpu.compare(cpu.r0, cpu.r7)
        if cpu.lt:
            cpu.branch('skip_101')
        cpu.jump('menu_row_skip_3')
        cpu.label('skip_101')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x28
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.call('record')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x30
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 += 0x01
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.r6 = 0x04
        cpu.r1 = 0x19
        cpu.call('menu_row')
        cpu.label('menu_row_skip_3')
        cpu.call(ROM_REFRESH)
        cpu.pop(cpu.pc)
        cpu.label('draw_operand')
        cpu.push(cpu.lr)
        cpu.call(0x0409A)
        cpu.call('old_line')
        cpu.call('name_line')
        cpu.er10 = cpu.er14
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x32)]
        cpu.r0 = 0x52
        cpu.compare(cpu.r7, 0x02)
        if cpu.eq:
            cpu.branch('skip_102')
        cpu.jump('operand_not_er')
        cpu.label('skip_102')
        cpu.r0 = 0x45
        cpu.label('operand_not_er')
        cpu.compare(cpu.r7, 0x03)
        if cpu.eq:
            cpu.branch('skip_103')
        cpu.jump('operand_not_bit')
        cpu.label('skip_103')
        cpu.r0 = 0x42
        cpu.label('operand_not_bit')
        cpu.compare(cpu.r7, 0x04)
        if cpu.eq:
            cpu.branch('skip_104')
        cpu.jump('operand_label')
        cpu.label('skip_104')
        cpu.r0 = 0x48
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x29)]
        cpu.compare(cpu.r7, 0x0E)
        if cpu.eq:
            cpu.branch('skip_105')
        cpu.jump('operand_label')
        cpu.label('skip_105')
        cpu.r0 = 0x54
        cpu.label('operand_label')
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x31
        cpu.r9 = cpu.mem8[cpu.er2]
        cpu.r0 = cpu.r9
        cpu.r0 += 0x01
        cpu.call('hexchar')
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x3D
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 0x32)]
        cpu.compare(cpu.r7, 0x04)
        if cpu.ne:
            cpu.branch('skip_106')
        cpu.jump('operand_hex')
        cpu.label('skip_106')
        cpu.compare(cpu.r9, 0x00)
        if cpu.ne:
            cpu.branch('skip_107')
        cpu.jump('operand_a')
        cpu.label('skip_107')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2E
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.jump('operand_value')
        cpu.label('operand_a')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2D
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.jump('operand_value')
        cpu.label('operand_hex')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x20
        cpu.r0 = cpu.r9
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.label('operand_value')
        cpu.call('hexchar')
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x20
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x45
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x58
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x45
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x00
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.r1 = 0x11
        cpu.call('lcd')
        cpu.call(ROM_REFRESH)
        cpu.pop(cpu.pc)
        cpu.label('draw_bad_target')
        cpu.push(cpu.lr)
        cpu.call(0x0409A)
        cpu.call('old_line')
        cpu.call('name_line')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x30)]
        cpu.compare(cpu.r0, 0x01)
        if cpu.eq:
            cpu.branch('skip_108')
        cpu.jump('bad_target_text')
        cpu.label('skip_108')
        cpu.r2 = 0x9C
        cpu.r3 = 0x8B
        cpu.jump('bad_show')
        cpu.label('bad_target_text')
        cpu.compare(cpu.r0, 0x02)
        if cpu.eq:
            cpu.branch('skip_109')
        cpu.jump('bad_outside_text')
        cpu.label('skip_109')
        cpu.r2 = 0xA8
        cpu.r3 = 0x8B
        cpu.jump('bad_show')
        cpu.label('bad_outside_text')
        cpu.compare(cpu.r0, 0x03)
        if cpu.eq:
            cpu.branch('skip_110')
        cpu.jump('bad_range_text')
        cpu.label('skip_110')
        cpu.r2 = 0xB6
        cpu.r3 = 0x8B
        cpu.jump('bad_show')
        cpu.label('bad_range_text')
        cpu.r2 = 0xC5
        cpu.r3 = 0x8B
        cpu.label('bad_show')
        cpu.r1 = 0x11
        cpu.call('show')
        cpu.call(ROM_REFRESH)
        cpu.pop(cpu.pc)
        cpu.label('draw_result')
        cpu.push(cpu.lr)
        cpu.call(0x0409A)
        cpu.call('old_line')
        cpu.call('name_line')
        cpu.call(ROM_REFRESH)
        cpu.er10 = cpu.er14
        cpu.r9 = 0x00
        cpu.label('result_bytes')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x34
        cpu.r0 = cpu.r9
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.call('hexbyte')
        cpu.r0 = 0x20
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r9 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2C
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r9, cpu.r0)
        if cpu.lt:
            cpu.branch('skip_111')
        cpu.jump('result_end')
        cpu.label('skip_111')
        cpu.compare(cpu.r9, 0x04)
        if cpu.eq:
            cpu.branch('skip_112')
        cpu.jump('result_bytes')
        cpu.label('skip_112')
        cpu.r0 = 0x00
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.r1 = 0x11
        cpu.call('lcd')
        cpu.er10 = cpu.er14
        cpu.r9 = 0x04
        cpu.jump('result_bytes')
        cpu.label('result_end')
        cpu.r0 = 0x45
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x58
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x45
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x00
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2C
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x05)
        if cpu.lt:
            cpu.branch('skip_113')
        cpu.jump('result_second')
        cpu.label('skip_113')
        cpu.r1 = 0x11
        cpu.jump('result_show')
        cpu.label('result_second')
        cpu.r1 = 0x19
        cpu.label('result_show')
        cpu.call('lcd')
        cpu.call(ROM_REFRESH)
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0xFEC00)
    def instruction_view():
        cpu.label('instruction_view')
        cpu.jump('view')
        cpu.jump('detail')
        cpu.label('view')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.push(cpu.er12)
        cpu.push(cpu.er14)
        cpu.r6 = 0x01
        cpu.jump('entry')
        cpu.label('detail')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.push(cpu.er12)
        cpu.push(cpu.er14)
        cpu.r6 = 0x02
        cpu.jump('entry')
        cpu.label('entry')
        cpu.er12 = cpu.er0
        cpu.er8 = cpu.er2
        cpu.sp += -96
        cpu.er14 = cpu.sp
        cpu.mem16[cpu.offset(cpu.er14, 0x28)] = cpu.er8
        cpu.mem16[cpu.offset(cpu.er14, 0x40)] = cpu.er8
        cpu.mem16[cpu.offset(cpu.er14, 0x42)] = cpu.er12
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x25
        cpu.mem8[cpu.er2] = cpu.r6
        cpu.call('probe')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('skip_1')
        cpu.jump('entry_invalid')
        cpu.label('skip_1')
        cpu.mem8[cpu.offset(cpu.er14, 0x44)] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x25
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_2')
        cpu.jump('result')
        cpu.label('skip_2')
        cpu.compare(cpu.r0, 0x02)
        if cpu.ne:
            cpu.branch('skip_3')
        cpu.jump('detail_draw')
        cpu.label('skip_3')
        cpu.call('normalize')
        cpu.call('draw_list')
        cpu.jump('result')
        cpu.label('detail_draw')
        cpu.call('draw_detail')
        cpu.label('result')
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x40)]
        cpu.mem16[cpu.offset(cpu.er14, 0x28)] = cpu.er8
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x44)]
        cpu.mem8[cpu.offset(cpu.er14, 0x2A)] = cpu.r0
        cpu.r1 = 0x00
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, 0x45)]
        cpu.compare(cpu.r6, 0x01)
        if cpu.ne:
            cpu.branch('return_pc')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x22
        cpu.r6 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x23
        cpu.r7 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er6
        cpu.jump('exit')
        cpu.label('return_pc')
        cpu.er2 = cpu.er8
        cpu.jump('exit')
        cpu.label('entry_invalid')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x20
        cpu.r8 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x21
        cpu.r9 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er8
        cpu.label('exit')
        cpu.sp += 0x60
        cpu.pop(cpu.er14)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('probe')
        cpu.push(cpu.lr)
        cpu.r8 = cpu.mem8[cpu.offset(cpu.er14, 0x28)]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x29
        cpu.r9 = cpu.mem8[cpu.er2]
        cpu.r0 = cpu.r8
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_4')
        cpu.jump('probe_invalid')
        cpu.label('skip_4')
        cpu.er0 = cpu.er8
        cpu.r2 = 0x00
        cpu.r3 = 0x40
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_5')
        cpu.jump('probe_invalid')
        cpu.label('skip_5')
        cpu.er0 = cpu.er8
        cpu.r2 = 0x08
        cpu.r4 = 0xF0
        cpu.r5 = 0x5F
        cpu.call(CODEC_SOURCE_LENGTH_ADDRESS)
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('skip_6')
        cpu.jump('probe_invalid')
        cpu.label('skip_6')
        cpu.r6 = cpu.r2
        cpu.r7 = cpu.r3
        cpu.mem8[cpu.offset(cpu.er14, 0x2A)] = cpu.r0
        cpu.mem16[cpu.offset(cpu.er14, 0x4E)] = cpu.er6
        cpu.r7 = 0x00
        cpu.er8 += cpu.er6
        cpu.er2 = cpu.er8
        cpu.r4 = cpu.mem8[0x08, cpu.er2]
        cpu.er2 = cpu.er8
        cpu.er2 += 0x01
        cpu.r5 = cpu.mem8[0x08, cpu.er2]
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x28)]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2A
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r1 = 0x00
        cpu.pop(cpu.pc)
        cpu.label('probe_invalid')
        cpu.r0 = 0xFF
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2A
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.pop(cpu.pc)
        cpu.label('decode')
        cpu.push(cpu.lr)
        cpu.r0 = 0xC3
        cpu.r1 = 0x93
        cpu.mem16[cpu.offset(cpu.er14, 0x2C)] = cpu.er0
        cpu.r0 = 0xFF
        cpu.mem8[cpu.offset(cpu.er14, 0x2B)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2A)]
        cpu.compare(cpu.r0, 0x08)
        if cpu.eq:
            cpu.branch('skip_7')
        cpu.jump('scan')
        cpu.label('skip_7')
        cpu.r0 = 0x46
        cpu.r1 = 0x91
        cpu.mem16[cpu.offset(cpu.er14, 0x2C)] = cpu.er0
        cpu.r0 = 0x17
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2B
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('skip_8')
        cpu.label('scan')
        cpu.r10 = cpu.r4
        cpu.r11 = cpu.r5
        cpu.r6 = 0x3C
        cpu.r7 = 0x11
        cpu.r9 = 0x5A
        cpu.label('record')
        cpu.er2 = cpu.er6
        cpu.er2 += 0x01
        cpu.r0 = cpu.mem8[0x08, cpu.er2]
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('next_record')
        cpu.er2 += 0x01
        cpu.r0 = cpu.mem8[0x08, cpu.er2]
        cpu.er2 += 0x01
        cpu.r1 = cpu.mem8[0x08, cpu.er2]
        cpu.er2 += 0x01
        cpu.er2 += 0x0A
        cpu.r4 = cpu.mem8[0x08, cpu.er2]
        cpu.er2 += 0x01
        cpu.r5 = cpu.mem8[0x08, cpu.er2]
        cpu.er2 += 0x01
        cpu.r2 = cpu.r10
        cpu.r2 &= cpu.r4
        cpu.compare(cpu.r2, cpu.r0)
        if cpu.ne:
            cpu.branch('next_record')
        cpu.r3 = cpu.r11
        cpu.r3 &= cpu.r5
        cpu.compare(cpu.r3, cpu.r1)
        if cpu.ne:
            cpu.branch('next_record')
        cpu.er2 = cpu.er6
        cpu.er2 += 0x0C
        cpu.r0 = cpu.mem8[0x08, cpu.er2]
        cpu.mem8[cpu.offset(cpu.er14, 0x2C)] = cpu.r0
        cpu.er2 = cpu.er6
        cpu.er2 += 0x0D
        cpu.r0 = cpu.mem8[0x08, cpu.er2]
        cpu.mem8[cpu.offset(cpu.er14, 0x2D)] = cpu.r0
        cpu.er2 = cpu.er6
        cpu.r0 = cpu.mem8[0x08, cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2B
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('skip_8')
        cpu.label('next_record')
        cpu.er6 += 0x10
        cpu.r9 += 0xFF
        cpu.compare(cpu.r9, 0x00)
        if cpu.eq:
            cpu.branch('skip_8')
        cpu.jump('record')
        cpu.label('skip_8')
        cpu.label('decoded')
        cpu.pop(cpu.pc)
        cpu.label('normalize')
        cpu.push(cpu.lr)
        cpu.r8 = cpu.mem8[cpu.offset(cpu.er14, 0x42)]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x23
        cpu.r9 = cpu.mem8[cpu.er2]
        cpu.r0 = cpu.r8
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_9')
        cpu.jump('top_reset')
        cpu.label('skip_9')
        cpu.er0 = cpu.er8
        cpu.r2 = 0x00
        cpu.r3 = 0x40
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_10')
        cpu.jump('top_reset')
        cpu.label('skip_10')
        cpu.r2 = 0xF0
        cpu.r3 = 0x5F
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('skip_11')
        cpu.jump('top_reset')
        cpu.label('skip_11')
        cpu.label('top_scan')
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x42)]
        cpu.mem16[cpu.offset(cpu.er14, 0x28)] = cpu.er8
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 0x47)] = cpu.r0
        cpu.label('top_instruction')
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x28)]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x21
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er2, -1)]
        cpu.compare(cpu.er8, cpu.er0)
        if cpu.ne:
            cpu.branch('skip_12')
        cpu.jump('top_done')
        cpu.label('skip_12')
        if cpu.lt:
            cpu.branch('skip_13')
        cpu.jump('top_reset')
        cpu.label('skip_13')
        cpu.call('probe')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('skip_14')
        cpu.jump('top_reset')
        cpu.label('skip_14')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x47)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('top_advance')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2A)]
        cpu.mem8[cpu.offset(cpu.er14, 0x46)] = cpu.r0
        cpu.label('top_advance')
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x28)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2A)]
        cpu.r1 = 0x00
        cpu.er8 += cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 0x28)] = cpu.er8
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x47)]
        cpu.r0 += 0x01
        cpu.mem8[cpu.offset(cpu.er14, 0x47)] = cpu.r0
        cpu.compare(cpu.r0, 0x03)
        if cpu.ge:
            cpu.branch('skip_15')
        cpu.jump('top_instruction')
        cpu.label('skip_15')
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x42)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x46)]
        cpu.r1 = 0x00
        cpu.er8 += cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 0x42)] = cpu.er8
        cpu.jump('skip_11')
        cpu.label('top_reset')
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x40)]
        cpu.mem8[cpu.offset(cpu.er14, 0x42)] = cpu.r8
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x23
        cpu.mem8[cpu.er2] = cpu.r9
        cpu.label('top_done')
        cpu.pop(cpu.pc)
        cpu.label('draw_begin')
        cpu.push(cpu.lr)
        cpu.r0 = cpu.mem8[0x80A0]
        cpu.mem8[cpu.offset(cpu.er14, 0x2F)] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x30
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x80A2] = cpu.r0
        cpu.call(0x0409A)
        cpu.pop(cpu.pc)
        cpu.label('draw_end')
        cpu.push(cpu.lr)
        cpu.call(ROM_REFRESH)
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x30)]
        cpu.mem8[0x80A2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2F
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.mem8[0x80A0] = cpu.r0
        cpu.pop(cpu.pc)
        cpu.label('draw_list')
        cpu.push(cpu.lr)
        cpu.call('draw_begin')
        cpu.er10 = cpu.er14
        cpu.er2 = cpu.er10
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0x44
        cpu.r3 = 0xF8
        cpu.er6 = 0x16
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er10 += 0x15
        cpu.r0 = 0x00
        cpu.r0 = cpu.r0
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x01
        cpu.call(SMALL_TEXT_ADDRESS)
        cpu.r8 = 0xEC
        cpu.r9 = 0x80
        cpu.r6 = 0x03
        cpu.call('reverse_rows')
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x42)]
        cpu.mem16[cpu.offset(cpu.er14, 0x28)] = cpu.er8
        cpu.r0 = 0x07
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x2A
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.label('list_row')
        cpu.call('probe')
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('skip_16')
        cpu.jump('skip_17')
        cpu.label('skip_16')
        cpu.call('decode')
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x28)]
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x40)]
        cpu.compare(cpu.er8, cpu.er0)
        if cpu.ne:
            cpu.branch('row_not_selected')
        cpu.r0 = 0x01
        cpu.jump('row_selection')
        cpu.label('row_not_selected')
        cpu.r0 = 0x00
        cpu.label('row_selection')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x28
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er10 = cpu.er14
        cpu.r0 = cpu.r9
        cpu.call('hexbyte')
        cpu.r0 = cpu.r8
        cpu.call('hexbyte')
        cpu.r0 = 0x20
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('bytes')
        cpu.r0 = 0x20
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x00
        cpu.r0 = cpu.r0
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x2A
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.call(SMALL_TEXT_ADDRESS)
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2A)]
        cpu.r0 <<= 0x01
        cpu.r0 += 0x06
        cpu.r0 <<= 0x02
        cpu.mem8[cpu.offset(cpu.er14, 0x4B)] = cpu.r0
        cpu.r0 >>= 0x02
        cpu.r1 = 0x18
        cpu.r1 -= cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x2D
        cpu.mem8[cpu.er2] = cpu.r1
        cpu.call('text_begin')
        cpu.call('operand_text')
        cpu.r0 = 0x00
        cpu.r0 = cpu.r0
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x4D)]
        cpu.r1 = 0x00
        cpu.er8 = cpu.er14
        cpu.er8 += cpu.er0
        cpu.r0 = cpu.mem8[cpu.er8]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('row_text')
        cpu.r0 = 0x00
        cpu.mem8[cpu.er8] = cpu.r0
        cpu.er8 += -1
        cpu.r0 = 0x2B
        cpu.mem8[cpu.er8] = cpu.r0
        cpu.label('row_text')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x4B)]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x2A
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.call(SMALL_TEXT_ADDRESS)
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x48)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('row_next')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x2A
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r8 = cpu.r0
        cpu.r1 = 0x0C
        cpu.multiply(cpu.er8, cpu.r1)
        cpu.r0 = 0xE0
        cpu.r1 = 0x80
        cpu.er8 += cpu.er0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x2B
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 >>= 0x03
        cpu.r1 = 0x00
        cpu.er8 += cpu.er0
        cpu.r6 = cpu.r0
        cpu.r0 = 0x0C
        cpu.r0 -= cpu.r6
        cpu.r6 = cpu.r0
        cpu.call('reverse_rows')
        cpu.label('row_next')
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x28)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2A)]
        cpu.r1 = 0x00
        cpu.er8 += cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 0x28)] = cpu.er8
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x4A)]
        cpu.r0 += 0x06
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x2A
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.compare(cpu.r0, 0x19)
        if cpu.ge:
            cpu.branch('skip_17')
        cpu.jump('list_row')
        cpu.label('skip_17')
        cpu.label('list_footer')
        cpu.r0 = 0x07
        cpu.mem8[0x80A0] = cpu.r0
        cpu.call('address_text')
        cpu.r0 = 0x00
        cpu.r0 = cpu.r0
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x19
        cpu.call(ROM_DRAW_TEXT)
        cpu.call('draw_end')
        cpu.pop(cpu.pc)
        cpu.label('draw_detail')
        cpu.push(cpu.lr)
        cpu.call('draw_begin')
        cpu.r0 = 0x07
        cpu.mem8[0x80A0] = cpu.r0
        cpu.call('address_text')
        cpu.r0 = 0x00
        cpu.r0 = cpu.r0
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x01
        cpu.call(ROM_DRAW_TEXT)
        cpu.push(cpu.xr4)
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_copy_text')
        cpu.data(b'DISASM\0\0')
        cpu.pop(cpu.xr4)
        cpu.er2 = cpu.er14
        cpu.r0 = 0x3C
        cpu.r1 = 0x01
        cpu.call(ROM_DRAW_TEXT)
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x40)]
        cpu.mem8[cpu.offset(cpu.er14, 0x28)] = cpu.r8
        cpu.er2 = cpu.er14
        cpu.er2 += 0x29
        cpu.mem8[cpu.er2] = cpu.r9
        cpu.call('probe')
        cpu.call('decode')
        cpu.er10 = cpu.er14
        cpu.call('bytes')
        cpu.r0 = 0x00
        cpu.r0 = cpu.r0
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x09
        cpu.call(ROM_DRAW_TEXT)
        cpu.call('text_begin')
        cpu.call('operand_text')
        cpu.r0 = 0x00
        cpu.r0 = cpu.r0
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x10)]
        cpu.mem8[cpu.offset(cpu.er14, 0x50)] = cpu.r0
        cpu.r0 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += 0x10
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x11
        cpu.call(ROM_DRAW_TEXT)
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x50)]
        cpu.mem8[cpu.offset(cpu.er14, 0x10)] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x10
        cpu.r0 = 0x00
        cpu.r1 = 0x19
        cpu.call(ROM_DRAW_TEXT)
        cpu.call('draw_end')
        cpu.pop(cpu.pc)
        cpu.label('address_text')
        cpu.push(cpu.lr)
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x21
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er2, -1)]
        cpu.er10 = cpu.er14
        cpu.r0 = 0x38
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x3A
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = cpu.r9
        cpu.call('hexbyte')
        cpu.r0 = cpu.r8
        cpu.call('hexbyte')
        cpu.pop(cpu.pc)
        cpu.label('bytes')
        cpu.push(cpu.lr)
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x28)]
        cpu.r6 = 0x00
        cpu.label('byte')
        cpu.er2 = cpu.er8
        cpu.r0 = cpu.r6
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.r0 = cpu.mem8[0x08, cpu.er2]
        cpu.call('hexbyte')
        cpu.r6 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2A
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r6, cpu.r0)
        if cpu.lt:
            cpu.branch('byte')
        cpu.pop(cpu.pc)
        cpu.label('reverse_rows')
        cpu.r7 = 0x06
        cpu.label('reverse_line')
        cpu.er2 = cpu.er8
        cpu.r4 = cpu.r6
        cpu.label('reverse_byte')
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 ^= 0xFF
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 += 0x01
        cpu.r4 += 0xFF
        if cpu.ne:
            cpu.branch('reverse_byte')
        cpu.er8 += 0x0C
        cpu.r7 += 0xFF
        if cpu.ne:
            cpu.branch('reverse_line')
        cpu.ret()
        cpu.label('text_begin')
        cpu.er10 = cpu.er14
        cpu.r6 = 0x21
        cpu.label('text_clear')
        cpu.r0 = 0x00
        cpu.r0 = cpu.r0
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r6 += 0xFF
        if cpu.ne:
            cpu.branch('text_clear')
        cpu.er10 = cpu.er14
        cpu.ret()
        cpu.label('hexbyte')
        cpu.push(cpu.lr)
        cpu.r7 = cpu.r0
        cpu.r0 >>= 0x04
        cpu.call('nibble')
        cpu.r0 = cpu.r0
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = cpu.r7
        cpu.r0 &= 0x0F
        cpu.call('nibble')
        cpu.r0 = cpu.r0
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.pop(cpu.pc)
        cpu.label('nibble')
        cpu.compare(cpu.r0, 0x0A)
        if cpu.lt:
            cpu.branch('digit')
        cpu.r0 += 0x37
        cpu.ret()
        cpu.label('digit')
        cpu.r0 += 0x30
        cpu.ret()
        cpu.label('operand_text')
        cpu.push(cpu.lr)
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x28)]
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, 0x4E)]
        cpu.r7 = 0x00
        cpu.er8 += cpu.er6
        cpu.er2 = cpu.er8
        cpu.r4 = cpu.mem8[0x08, cpu.er2]
        cpu.er2 = cpu.er8
        cpu.er2 += 0x01
        cpu.r5 = cpu.mem8[0x08, cpu.er2]
        cpu.mem16[cpu.offset(cpu.er14, 0x34)] = cpu.er4
        cpu.r0 = cpu.r5
        cpu.r0 &= 0x0F
        cpu.mem8[cpu.offset(cpu.er14, 0x36)] = cpu.r0
        cpu.r0 = cpu.r4
        cpu.r0 >>= 0x04
        cpu.mem8[cpu.offset(cpu.er14, 0x37)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x2B)]
        cpu.compare(cpu.r0, 0xFF)
        if cpu.ne:
            cpu.branch('operand_skip_1')
        cpu.jump('operand_unknown')
        cpu.label('operand_skip_1')
        cpu.er6 = cpu.mem16[cpu.offset(cpu.er14, 0x2C)]
        cpu.label('operand_name')
        cpu.er2 = cpu.er6
        cpu.r0 = cpu.mem8[0x0F, cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('operand_name_done')
        cpu.compare(cpu.r0, 0x20)
        if cpu.ne:
            cpu.branch('operand_name_char')
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, 0x2B)]
        cpu.compare(cpu.r1, 0x13)
        if cpu.ne:
            cpu.branch('operand_name_done')
        cpu.label('operand_name_char')
        cpu.r0 = cpu.r0
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er6 += 0x01
        cpu.jump('operand_name')
        cpu.label('operand_name_done')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x2B
        cpu.r6 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r6, 0x13)
        if cpu.ne:
            cpu.branch('operand_skip_2')
        cpu.jump('operand_done')
        cpu.label('operand_skip_2')
        cpu.r0 = 0x20
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.compare(cpu.r6, 0x00)
        if cpu.ne:
            cpu.branch('operand_skip_3')
        cpu.jump('operand_imm')
        cpu.label('operand_skip_3')
        cpu.compare(cpu.r6, 0x01)
        if cpu.ne:
            cpu.branch('operand_skip_4')
        cpu.jump('operand_rr')
        cpu.label('operand_skip_4')
        cpu.compare(cpu.r6, 0x02)
        if cpu.ne:
            cpu.branch('operand_skip_5')
        cpu.jump('operand_ee')
        cpu.label('operand_skip_5')
        cpu.compare(cpu.r6, 0x03)
        if cpu.ne:
            cpu.branch('operand_skip_6')
        cpu.jump('operand_ei7')
        cpu.label('operand_skip_6')
        cpu.compare(cpu.r6, 0x04)
        if cpu.ne:
            cpu.branch('operand_skip_7')
        cpu.jump('operand_shift')
        cpu.label('operand_skip_7')
        cpu.compare(cpu.r6, 0x05)
        if cpu.ne:
            cpu.branch('operand_skip_8')
        cpu.jump('operand_er_r')
        cpu.label('operand_skip_8')
        cpu.compare(cpu.r6, 0x06)
        if cpu.ne:
            cpu.branch('operand_skip_9')
        cpu.jump('operand_one_r')
        cpu.label('operand_skip_9')
        cpu.compare(cpu.r6, 0x07)
        if cpu.ne:
            cpu.branch('operand_skip_10')
        cpu.jump('operand_one_er')
        cpu.label('operand_skip_10')
        cpu.compare(cpu.r6, 0x08)
        if cpu.ne:
            cpu.branch('operand_skip_11')
        cpu.jump('operand_r_abs')
        cpu.label('operand_skip_11')
        cpu.compare(cpu.r6, 0x09)
        if cpu.ne:
            cpu.branch('operand_skip_12')
        cpu.jump('operand_r_ind')
        cpu.label('operand_skip_12')
        cpu.compare(cpu.r6, 0x18)
        if cpu.ne:
            cpu.branch('operand_skip_13')
        cpu.jump('operand_one_xr')
        cpu.label('operand_skip_13')
        cpu.compare(cpu.r6, 0x19)
        if cpu.ne:
            cpu.branch('operand_skip_14')
        cpu.jump('operand_one_qr')
        cpu.label('operand_skip_14')
        cpu.compare(cpu.r6, 0x0A)
        if cpu.ne:
            cpu.branch('operand_skip_15')
        cpu.jump('operand_r_disp')
        cpu.label('operand_skip_15')
        cpu.compare(cpu.r6, 0x0B)
        if cpu.ne:
            cpu.branch('operand_skip_16')
        cpu.jump('operand_er_abs')
        cpu.label('operand_skip_16')
        cpu.compare(cpu.r6, 0x0C)
        if cpu.ne:
            cpu.branch('operand_skip_17')
        cpu.jump('operand_er_ind')
        cpu.label('operand_skip_17')
        cpu.compare(cpu.r6, 0x0D)
        if cpu.ne:
            cpu.branch('operand_skip_18')
        cpu.jump('operand_er_disp')
        cpu.label('operand_skip_18')
        cpu.compare(cpu.r6, 0x0E)
        if cpu.ne:
            cpu.branch('operand_skip_19')
        cpu.jump('operand_branch')
        cpu.label('operand_skip_19')
        cpu.compare(cpu.r6, 0x0F)
        if cpu.ne:
            cpu.branch('operand_skip_20')
        cpu.jump('operand_far')
        cpu.label('operand_skip_20')
        cpu.compare(cpu.r6, 0x10)
        if cpu.ne:
            cpu.branch('operand_skip_21')
        cpu.jump('operand_far')
        cpu.label('operand_skip_21')
        cpu.compare(cpu.r6, 0x11)
        if cpu.ne:
            cpu.branch('operand_skip_22')
        cpu.jump('operand_tb')
        cpu.label('operand_skip_22')
        cpu.compare(cpu.r6, 0x12)
        if cpu.ne:
            cpu.branch('operand_skip_23')
        cpu.jump('operand_sp_imm')
        cpu.label('operand_skip_23')
        cpu.compare(cpu.r6, 0x14)
        if cpu.ne:
            cpu.branch('operand_skip_24')
        cpu.jump('operand_one_er')
        cpu.label('operand_skip_24')
        cpu.compare(cpu.r6, 0x15)
        if cpu.ne:
            cpu.branch('operand_skip_25')
        cpu.jump('operand_er_sp')
        cpu.label('operand_skip_25')
        cpu.compare(cpu.r6, 0x16)
        if cpu.ne:
            cpu.branch('operand_skip_26')
        cpu.jump('operand_sp_er')
        cpu.label('operand_skip_26')
        cpu.compare(cpu.r6, 0x17)
        if cpu.ne:
            cpu.branch('operand_skip_27')
        cpu.jump('operand_sub_imm')
        cpu.label('operand_skip_27')
        cpu.jump('operand_done')
        cpu.label('operand_imm')
        cpu.call('operand_rdest')
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x23
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x34
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.call('hexbyte')
        cpu.jump('operand_done')
        cpu.label('operand_rr')
        cpu.call('operand_rdest')
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('operand_rsrc')
        cpu.jump('operand_done')
        cpu.label('operand_ee')
        cpu.call('operand_edest')
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('operand_esrc')
        cpu.jump('operand_done')
        cpu.label('operand_er_r')
        cpu.call('operand_edest')
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('operand_rsrc')
        cpu.jump('operand_done')
        cpu.label('operand_ei7')
        cpu.call('operand_edest')
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x23
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x34
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 &= 0x7F
        cpu.call('hexbyte')
        cpu.jump('operand_done')
        cpu.label('operand_shift')
        cpu.call('operand_rdest')
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x23
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x37
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 &= 0x07
        cpu.call('hexbyte')
        cpu.jump('operand_done')
        cpu.label('operand_one_r')
        cpu.call('operand_rdest')
        cpu.jump('operand_done')
        cpu.label('operand_one_er')
        cpu.call('operand_edest')
        cpu.jump('operand_done')
        cpu.label('operand_one_xr')
        cpu.r0 = 0x58
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x52
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x36
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.call('operand_decimal')
        cpu.jump('operand_done')
        cpu.label('operand_one_qr')
        cpu.r0 = 0x51
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x52
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x36
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.call('operand_decimal')
        cpu.jump('operand_done')
        cpu.label('operand_r_abs')
        cpu.call('operand_rdest')
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('operand_segment')
        cpu.call('operand_word')
        cpu.jump('operand_done')
        cpu.label('operand_er_abs')
        cpu.call('operand_edest')
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('operand_segment')
        cpu.call('operand_word')
        cpu.jump('operand_done')
        cpu.label('operand_r_ind')
        cpu.call('operand_rdest')
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('operand_segment')
        cpu.r0 = 0x5B
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('operand_esrc')
        cpu.r0 = 0x5D
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.jump('operand_done')
        cpu.label('operand_er_ind')
        cpu.call('operand_edest')
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('operand_segment')
        cpu.r0 = 0x5B
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('operand_esrc')
        cpu.r0 = 0x5D
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.jump('operand_done')
        cpu.label('operand_r_disp')
        cpu.call('operand_rdest')
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('operand_segment')
        cpu.call('operand_word')
        cpu.r0 = 0x5B
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('operand_esrc')
        cpu.r0 = 0x5D
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.jump('operand_done')
        cpu.label('operand_er_disp')
        cpu.call('operand_edest')
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('operand_segment')
        cpu.call('operand_word')
        cpu.r0 = 0x5B
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('operand_esrc')
        cpu.r0 = 0x5D
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.jump('operand_done')
        cpu.label('operand_branch')
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, 0x34)]
        cpu.r7 = 0x00
        cpu.compare(cpu.r6, 0x80)
        if cpu.lt:
            cpu.branch('operand_branch_positive')
        cpu.r7 = 0xFF
        cpu.label('operand_branch_positive')
        cpu.er6 += cpu.er6
        cpu.er6 += 0x02
        cpu.er6 += cpu.er8
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3A
        cpu.mem8[cpu.er2] = cpu.r6
        cpu.r0 = cpu.r7
        cpu.call('hexbyte')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3A
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.call('hexbyte')
        cpu.jump('operand_done')
        cpu.label('operand_far')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x35
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 &= 0x0F
        cpu.call('nibble')
        cpu.r0 = cpu.r0
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x3A
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('operand_word')
        cpu.jump('operand_done')
        cpu.label('operand_tb')
        cpu.call('operand_rdest')
        cpu.r0 = 0x2E
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x37
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 &= 0x07
        cpu.call('operand_decimal')
        cpu.jump('operand_done')
        cpu.label('operand_sp_imm')
        cpu.r0 = 0x53
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x50
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x23
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x34
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.call('hexbyte')
        cpu.jump('operand_done')
        cpu.label('operand_er_sp')
        cpu.call('operand_edest')
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x53
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x50
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.jump('operand_done')
        cpu.label('operand_sp_er')
        cpu.r0 = 0x53
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x50
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.call('operand_esrc')
        cpu.jump('operand_done')
        cpu.label('operand_sub_imm')
        cpu.r0 = 0x52
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er8
        cpu.er2 += 0x05
        cpu.r0 = cpu.mem8[0x08, cpu.er2]
        cpu.r0 &= 0x0F
        cpu.call('operand_decimal')
        cpu.r0 = 0x2C
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x23
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er8
        cpu.er2 += 0x02
        cpu.r0 = cpu.mem8[0x08, cpu.er2]
        cpu.call('hexbyte')
        cpu.jump('operand_done')
        cpu.label('operand_unknown')
        cpu.r0 = 0x44
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x57
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x20
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x35
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.call('hexbyte')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x34
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.call('hexbyte')
        cpu.label('operand_done')
        cpu.r8 = cpu.mem8[cpu.offset(cpu.er14, 0x28)]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x29
        cpu.r9 = cpu.mem8[cpu.er2]
        cpu.pop(cpu.pc)
        cpu.label('operand_edest')
        cpu.r0 = 0x45
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x52
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x36
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 &= 0x0E
        cpu.jump('operand_decimal')
        cpu.label('operand_rdest')
        cpu.r0 = 0x52
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x36
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.jump('operand_decimal')
        cpu.label('operand_esrc')
        cpu.r0 = 0x45
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.label('operand_rsrc')
        cpu.r0 = 0x52
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x37
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.jump('operand_decimal')
        cpu.label('operand_decimal')
        cpu.r6 = cpu.r0
        cpu.compare(cpu.r6, 0x0A)
        if cpu.lt:
            cpu.branch('operand_decimal_digit')
        cpu.r0 = 0x31
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r6 += 0xF6
        cpu.label('operand_decimal_digit')
        cpu.r0 = cpu.r6
        cpu.r0 += 0x30
        cpu.r0 = cpu.r0
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.ret()
        cpu.label('operand_word')
        cpu.push(cpu.lr)
        cpu.er2 = cpu.er8
        cpu.er2 += 0x03
        cpu.r0 = cpu.mem8[0x08, cpu.er2]
        cpu.call('hexbyte')
        cpu.er2 = cpu.er8
        cpu.er2 += 0x02
        cpu.r0 = cpu.mem8[0x08, cpu.er2]
        cpu.call('hexbyte')
        cpu.pop(cpu.pc)
        cpu.label('operand_segment')
        cpu.push(cpu.lr)
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += 0x2E
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('operand_segment_done')
        cpu.er6 = cpu.mem16[cpu.offset(cpu.er14, 0x28)]
        cpu.er2 = cpu.er6
        cpu.r4 = cpu.mem8[0x08, cpu.er2]
        cpu.er2 += 0x01
        cpu.r0 = cpu.mem8[0x08, cpu.er2]
        cpu.compare(cpu.r0, 0xE3)
        if cpu.ne:
            cpu.branch('operand_segment_register')
        cpu.r0 = cpu.r4
        cpu.call('hexbyte')
        cpu.jump('operand_segment_colon')
        cpu.label('operand_segment_register')
        cpu.compare(cpu.r0, 0xFE)
        if cpu.ne:
            cpu.branch('operand_segment_r')
        cpu.r0 = 0x44
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x53
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = 0x52
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.jump('operand_segment_colon')
        cpu.label('operand_segment_r')
        cpu.r0 = cpu.r4
        cpu.r0 >>= 0x04
        cpu.r4 = cpu.r0
        cpu.r0 = 0x52
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r0 = cpu.r4
        cpu.call('operand_decimal')
        cpu.label('operand_segment_colon')
        cpu.r0 = 0x3A
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.label('operand_segment_done')
        cpu.pop(cpu.pc)
