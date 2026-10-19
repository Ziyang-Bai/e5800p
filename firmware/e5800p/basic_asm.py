"""Fixed-layout e5800p basic asm routines and tables."""

from kits import cpu

BASIC_FLASH = 0xF6E68
BASIC_MEMORY = 0xFB530
CODEC_ENCODE_ADDRESS = 0x808E0

BASIC_ASM_DATA_CATALOGUE = bytes((
    0x00, 0x91, 0x9A, 0xA7, 0x3C, 0x11, 0x08, 0x91, 0x9E, 0xA7, 0x4C, 0x11, 0x10, 0x91, 0x9A, 0xA7,
    0x5C, 0x11, 0x19, 0x91, 0x9E, 0xA7, 0x6C, 0x11, 0x22, 0x91, 0xA2, 0xA7, 0x7C, 0x11, 0x2B, 0x91,
    0xA6, 0xA7, 0x8C, 0x11, 0x35, 0x91, 0x9E, 0xA7, 0x9C, 0x11, 0x3D, 0x91, 0x9E, 0xA7, 0xAC, 0x11,
    0x46, 0x91, 0x9A, 0xA7, 0xBC, 0x11, 0x4E, 0x91, 0x9E, 0xA7, 0xCC, 0x11, 0x56, 0x91, 0x9A, 0xA7,
    0xDC, 0x11, 0x5E, 0x91, 0x9E, 0xA7, 0xEC, 0x11, 0x65, 0x91, 0x9A, 0xA7, 0xFC, 0x11, 0x6C, 0x91,
    0x9E, 0xA7, 0x0C, 0x12, 0x74, 0x91, 0x9A, 0xA7, 0x1C, 0x12, 0x7C, 0x91, 0x9E, 0xA7, 0x2C, 0x12,
    0x84, 0x91, 0xAA, 0xA7, 0x3C, 0x12, 0x8C, 0x91, 0x9E, 0xA7, 0x4C, 0x12, 0x95, 0x91, 0xAA, 0xA7,
    0x5C, 0x12, 0x9E, 0x91, 0x9E, 0xA7, 0x6C, 0x12, 0xA6, 0x91, 0xAA, 0xA7, 0x7C, 0x12, 0xAE, 0x91,
    0x9E, 0xA7, 0x8C, 0x12, 0xB7, 0x91, 0xAA, 0xA7, 0x9C, 0x12, 0xBF, 0x91, 0x9E, 0xA7, 0xAC, 0x12,
    0xC7, 0x91, 0xAE, 0xA7, 0xBC, 0x12, 0xD0, 0x91, 0xAE, 0xA7, 0xCC, 0x12, 0xD9, 0x91, 0x9A, 0xA7,
    0xDC, 0x12, 0xE1, 0x91, 0x9E, 0xA7, 0xEC, 0x12, 0xE9, 0x91, 0x9A, 0xA7, 0xFC, 0x12, 0xF2, 0x91,
    0x9E, 0xA7, 0x0C, 0x13, 0xFB, 0x91, 0xA6, 0xA7, 0x1C, 0x13, 0x05, 0x92, 0xB2, 0xA7, 0x2C, 0x13,
    0x0B, 0x92, 0xB2, 0xA7, 0x3C, 0x13, 0x11, 0x92, 0xB2, 0xA7, 0x4C, 0x13, 0x17, 0x92, 0x9A, 0xA7,
    0x5C, 0x13, 0x1F, 0x92, 0x9E, 0xA7, 0x6C, 0x13, 0x27, 0x92, 0xA6, 0xA7, 0x7C, 0x13, 0x31, 0x92,
    0xB4, 0xA7, 0x8C, 0x13, 0x3B, 0x92, 0xB9, 0xA7, 0x9C, 0x13, 0x45, 0x92, 0xBE, 0xA7, 0xAC, 0x13,
    0x49, 0x92, 0xBE, 0xA7, 0xBC, 0x13, 0x4D, 0x92, 0xBE, 0xA7, 0xCC, 0x13, 0x51, 0x92, 0xBE, 0xA7,
    0xDC, 0x13, 0x55, 0x92, 0xBE, 0xA7, 0xEC, 0x13, 0x5A, 0x92, 0xBE, 0xA7, 0xFC, 0x13, 0x5F, 0x92,
    0xBE, 0xA7, 0x0C, 0x14, 0x64, 0x92, 0xBE, 0xA7, 0x1C, 0x14, 0x69, 0x92, 0xBE, 0xA7, 0x2C, 0x14,
    0x6D, 0x92, 0xBE, 0xA7, 0x3C, 0x14, 0x71, 0x92, 0xBE, 0xA7, 0x4C, 0x14, 0x75, 0x92, 0xBE, 0xA7,
    0x5C, 0x14, 0x79, 0x92, 0xBE, 0xA7, 0x6C, 0x14, 0x7D, 0x92, 0xBE, 0xA7, 0x7C, 0x14, 0x81, 0x92,
    0xBE, 0xA7, 0x8C, 0x14, 0x85, 0x92, 0xBE, 0xA7, 0x9C, 0x14, 0x8A, 0x92, 0xC0, 0xA7, 0xAC, 0x14,
    0x93, 0x92, 0xC5, 0xA7, 0xBC, 0x14, 0x9C, 0x92, 0xCC, 0xA7, 0xCC, 0x14, 0xA6, 0x92, 0xD4, 0xA7,
    0xDC, 0x14, 0xB0, 0x92, 0xD9, 0xA7, 0xEC, 0x14, 0xBA, 0x92, 0xE0, 0xA7, 0xFC, 0x14, 0xC5, 0x92,
    0xC0, 0xA7, 0x0C, 0x15, 0xCF, 0x92, 0xC5, 0xA7, 0x1C, 0x15, 0xD9, 0x92, 0xCC, 0xA7, 0x2C, 0x15,
    0xE4, 0x92, 0xD4, 0xA7, 0x3C, 0x15, 0xEF, 0x92, 0xD9, 0xA7, 0x4C, 0x15, 0xFA, 0x92, 0xE0, 0xA7,
    0x5C, 0x15, 0x06, 0x93, 0xB2, 0xA7, 0x6C, 0x15, 0x0D, 0x93, 0xE8, 0xA7, 0x7C, 0x15, 0x15, 0x93,
    0xB2, 0xA7, 0x8C, 0x15, 0x1B, 0x93, 0xE8, 0xA7, 0x9C, 0x15, 0x22, 0x93, 0xEA, 0xA7, 0xAC, 0x15,
    0x2A, 0x93, 0xEC, 0xA7, 0xBC, 0x15, 0x32, 0x93, 0xEA, 0xA7, 0xCC, 0x15, 0x39, 0x93, 0xEC, 0xA7,
    0xDC, 0x15, 0x40, 0x93, 0xEE, 0xA7, 0xEC, 0x15, 0x48, 0x93, 0xEE, 0xA7, 0xFC, 0x15, 0x4F, 0x93,
    0xF1, 0xA7, 0x0C, 0x16, 0x57, 0x93, 0xF1, 0xA7, 0x1C, 0x16, 0x5E, 0x93, 0xF4, 0xA7, 0x2C, 0x16,
    0x65, 0x93, 0xF7, 0xA7, 0x3C, 0x16, 0x6E, 0x93, 0xF9, 0xA7, 0x4C, 0x16, 0x75, 0x93, 0xE8, 0xA7,
    0x5C, 0x16, 0x7E, 0x93, 0xFD, 0xA7, 0x6C, 0x16, 0x87, 0x93, 0x02, 0xA8, 0x7C, 0x16, 0x8A, 0x93,
    0x02, 0xA8, 0x8C, 0x16, 0x8D, 0x93, 0x02, 0xA8, 0x9C, 0x16, 0x92, 0x93, 0x02, 0xA8, 0xAC, 0x16,
    0x96, 0x93, 0x02, 0xA8, 0xBC, 0x16, 0x9A, 0x93, 0x02, 0xA8, 0xCC, 0x16, 0x27, 0x92, 0x03, 0xA8,
    0x00, 0x00, 0x00, 0x00,
))

BASIC_ASM_DATA_PATTERN_0 = bytes((
    0x01, 0x2C, 0x05, 0x00,
))

BASIC_ASM_DATA_PATTERN_1 = bytes((
    0x01, 0x2C, 0x01, 0x00,
))

BASIC_ASM_DATA_PATTERN_2 = bytes((
    0x02, 0x2C, 0x08, 0x00,
))

BASIC_ASM_DATA_PATTERN_3 = bytes((
    0x02, 0x2C, 0x02, 0x00,
))

BASIC_ASM_DATA_PATTERN_4 = bytes((
    0x01, 0x2C, 0x0C, 0x00,
))

BASIC_ASM_DATA_PATTERN_5 = bytes((
    0x02, 0x2C, 0x01, 0x00,
))

BASIC_ASM_DATA_PATTERN_6 = bytes((
    0x01, 0x00,
))

BASIC_ASM_DATA_PATTERN_7 = bytes((
    0x02, 0x2C, 0x53, 0x50, 0x00,
))

BASIC_ASM_DATA_PATTERN_8 = bytes((
    0x53, 0x50, 0x2C, 0x02, 0x00,
))

BASIC_ASM_DATA_PATTERN_9 = bytes((
    0x0B, 0x00,
))

BASIC_ASM_DATA_PATTERN_10 = bytes((
    0x01, 0x2C, 0x0D, 0x06, 0x00,
))

BASIC_ASM_DATA_PATTERN_11 = bytes((
    0x01, 0x2C, 0x0D, 0x5B, 0x02, 0x5D, 0x00,
))

BASIC_ASM_DATA_PATTERN_12 = bytes((
    0x01, 0x2C, 0x0D, 0x0A, 0x5B, 0x02, 0x5D, 0x00,
))

BASIC_ASM_DATA_PATTERN_13 = bytes((
    0x02, 0x2C, 0x0D, 0x06, 0x00,
))

BASIC_ASM_DATA_PATTERN_14 = bytes((
    0x02, 0x2C, 0x0D, 0x5B, 0x02, 0x5D, 0x00,
))

BASIC_ASM_DATA_PATTERN_15 = bytes((
    0x02, 0x2C, 0x0D, 0x0A, 0x5B, 0x02, 0x5D, 0x00,
))

BASIC_ASM_DATA_PATTERN_16 = bytes((
    0x02, 0x00,
))

BASIC_ASM_DATA_PATTERN_17 = bytes((
    0x03, 0x00,
))

BASIC_ASM_DATA_PATTERN_18 = bytes((
    0x04, 0x00,
))

BASIC_ASM_DATA_PATTERN_19 = b'LR\x00'

BASIC_ASM_DATA_PATTERN_20 = b'EA\x00'

BASIC_ASM_DATA_PATTERN_21 = b'PC\x00'

BASIC_ASM_DATA_PATTERN_22 = bytes((
    0x07, 0x00,
))

BASIC_ASM_DATA_PATTERN_23 = bytes((
    0x01, 0x2E, 0x0C, 0x00,
))

BASIC_ASM_DATA_PATTERN_24 = bytes((
    0x53, 0x50, 0x2C, 0x09, 0x00,
))

BASIC_ASM_DATA_PATTERN_25 = b'\x00'

BASIC_ASM_DATA_PATTERN_26 = bytes((
    0x02, 0x2C, 0x06, 0x00,
))

BASIC_ASM_DATA_TABLE = (
    BASIC_ASM_DATA_CATALOGUE +
    BASIC_ASM_DATA_PATTERN_0 +
    BASIC_ASM_DATA_PATTERN_1 +
    BASIC_ASM_DATA_PATTERN_2 +
    BASIC_ASM_DATA_PATTERN_3 +
    BASIC_ASM_DATA_PATTERN_4 +
    BASIC_ASM_DATA_PATTERN_5 +
    BASIC_ASM_DATA_PATTERN_6 +
    BASIC_ASM_DATA_PATTERN_7 +
    BASIC_ASM_DATA_PATTERN_8 +
    BASIC_ASM_DATA_PATTERN_9 +
    BASIC_ASM_DATA_PATTERN_10 +
    BASIC_ASM_DATA_PATTERN_11 +
    BASIC_ASM_DATA_PATTERN_12 +
    BASIC_ASM_DATA_PATTERN_13 +
    BASIC_ASM_DATA_PATTERN_14 +
    BASIC_ASM_DATA_PATTERN_15 +
    BASIC_ASM_DATA_PATTERN_16 +
    BASIC_ASM_DATA_PATTERN_17 +
    BASIC_ASM_DATA_PATTERN_18 +
    BASIC_ASM_DATA_PATTERN_19 +
    BASIC_ASM_DATA_PATTERN_20 +
    BASIC_ASM_DATA_PATTERN_21 +
    BASIC_ASM_DATA_PATTERN_22 +
    BASIC_ASM_DATA_PATTERN_23 +
    BASIC_ASM_DATA_PATTERN_24 +
    BASIC_ASM_DATA_PATTERN_25 +
    BASIC_ASM_DATA_PATTERN_26
)

BASIC_ASM_DATA_LABELS = {
    'basic_asm_data': 0x0,
    'catalogue': 0x0,
    'pattern_0': 0x224,
    'pattern_1': 0x228,
    'pattern_2': 0x22C,
    'pattern_3': 0x230,
    'pattern_4': 0x234,
    'pattern_5': 0x238,
    'pattern_6': 0x23C,
    'pattern_7': 0x23E,
    'pattern_8': 0x243,
    'pattern_9': 0x248,
    'pattern_10': 0x24A,
    'pattern_11': 0x24F,
    'pattern_12': 0x256,
    'pattern_13': 0x25E,
    'pattern_14': 0x263,
    'pattern_15': 0x26A,
    'pattern_16': 0x272,
    'pattern_17': 0x274,
    'pattern_18': 0x276,
    'pattern_19': 0x278,
    'pattern_20': 0x27B,
    'pattern_21': 0x27E,
    'pattern_22': 0x281,
    'pattern_23': 0x283,
    'pattern_24': 0x287,
    'pattern_25': 0x28C,
    'pattern_26': 0x28D,
}


def install(fw):
    fw.data('basic_asm_data', BASIC_ASM_DATA_TABLE, address=0xFA576, labels=BASIC_ASM_DATA_LABELS)

    @fw.function(native=True, address=0xF9530)
    def basic_asm():
        cpu.label('basic_asm')
        cpu.jump('execute')
        cpu.jump('skip')
        cpu.label('execute')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.r7 = 0x00
        cpu.jump('entry')
        cpu.label('skip')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.r7 = 0x01
        cpu.label('entry')
        cpu.er8 = cpu.er0
        cpu.er12 = cpu.er2
        cpu.er0 = cpu.sp
        cpu.r2 = 0xD2
        cpu.r3 = 0x83
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('near_1')
        cpu.jump('entry_memory')
        cpu.label('near_1')
        cpu.sp += -128
        cpu.er14 = cpu.sp
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0000)] = cpu.er12
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0007)] = cpu.r7
        cpu.er10 = cpu.er14
        cpu.r2 = 0x7E
        cpu.r3 = 0x00
        cpu.r0 = 0x00
        cpu.er10 += 0x02
        cpu.label('clear_frame')
        cpu.mem8[0x00, cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.er2 += -1
        if cpu.ne:
            cpu.branch('clear_frame')
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0007)] = cpu.r7
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0076)] = cpu.er14
        cpu.r6 = 0x10
        cpu.label('clear_output')
        cpu.mem8[0x00, cpu.er12] = cpu.r0
        cpu.er12 += 0x01
        cpu.r6 += 0xFF
        if cpu.ne:
            cpu.branch('clear_output')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0002)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0004)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0004)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0008)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0008)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0002)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('near_2')
        cpu.jump('bad_operand')
        cpu.label('near_2')
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0006)] = cpu.r0
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0006)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.eq:
            cpu.branch('near_3')
        cpu.jump('bad_operand')
        cpu.label('near_3')
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x000A)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.eq:
            cpu.branch('near_4')
        cpu.jump('bad_operand')
        cpu.label('near_4')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0002)]
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0008)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('near_5')
        cpu.jump('begin_equal')
        cpu.label('near_5')
        cpu.jump('near_6')
        cpu.label('begin_equal')
        if cpu.eq:
            cpu.branch('near_6')
        cpu.jump('bad_operand')
        cpu.label('near_6')
        cpu.label('begin_ok')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0008)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)] = cpu.er0
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000C)] = cpu.er0
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0004)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('near_7')
        cpu.jump('no_endasm')
        cpu.label('near_7')
        cpu.call('measure')
        cpu.call('get')
        cpu.compare(cpu.r0, 0xF9)
        if cpu.eq:
            cpu.branch('near_8')
        cpu.jump('bad_operand')
        cpu.label('near_8')
        cpu.call('get')
        cpu.compare(cpu.r0, 0xF7)
        if cpu.eq:
            cpu.branch('near_9')
        cpu.jump('bad_operand')
        cpu.label('near_9')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0007)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('near_10')
        cpu.jump('skip_header')
        cpu.label('near_10')
        cpu.call('spaces')
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003F)] = cpu.r0
        cpu.call('decimal')
        cpu.r6 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003F)]
        cpu.compare(cpu.r6, 0x00)
        if cpu.eq:
            cpu.branch('near_11')
        cpu.jump('bad_operand')
        cpu.label('near_11')
        cpu.compare(cpu.r2, 0x08)
        if cpu.ge:
            cpu.branch('near_12')
        cpu.jump('address_range')
        cpu.label('near_12')
        cpu.compare(cpu.r2, 0x10)
        if cpu.lt:
            cpu.branch('near_13')
        cpu.jump('address_range')
        cpu.label('near_13')
        cpu.compare(cpu.r3, 0x00)
        if cpu.eq:
            cpu.branch('near_14')
        cpu.jump('address_range')
        cpu.label('near_14')
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x007C)] = cpu.r2
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0012)] = cpu.er0
        cpu.call('even_address')
        cpu.call('line_tail')
        cpu.jump('header_done')
        cpu.label('skip_header')
        cpu.call('discard_line')
        cpu.label('header_done')
        cpu.call('peek')
        cpu.compare(cpu.r0, 0x0D)
        if cpu.eq:
            cpu.branch('near_15')
        cpu.jump('no_endasm')
        cpu.label('near_15')
        cpu.call('get')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000E)] = cpu.er0
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000C)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0007)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('near_16')
        cpu.jump('skip_loop')
        cpu.label('near_16')
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0019)] = cpu.r0
        cpu.call('reset')
        cpu.label('label_pass')
        cpu.call('next')
        cpu.compare(cpu.r1, 0x03)
        if cpu.ne:
            cpu.branch('near_17')
        cpu.jump('add_label')
        cpu.label('near_17')
        cpu.compare(cpu.r1, 0x01)
        if cpu.ne:
            cpu.branch('near_18')
        cpu.jump('labels_done')
        cpu.label('near_18')
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('near_19')
        cpu.jump('failure')
        cpu.label('near_19')
        cpu.jump('label_pass')
        cpu.label('add_label')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x007D)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('near_20')
        cpu.jump('address_range')
        cpu.label('near_20')
        cpu.call('find_label')
        cpu.er2 = 0x00
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.eq:
            cpu.branch('near_21')
        cpu.jump('dup_label')
        cpu.label('near_21')
        cpu.er0 = cpu.sp
        cpu.r2 = 0x5E
        cpu.r3 = 0x83
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('near_22')
        cpu.jump('memory')
        cpu.label('near_22')
        cpu.sp += -12
        cpu.er8 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0076)]
        cpu.er8 += -12
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0076)] = cpu.er8
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0038)]
        cpu.mem8[0x00, cpu.er8] = cpu.r0
        cpu.er10 = cpu.er14
        cpu.er10 += 0x30
        cpu.er8 += 0x02
        cpu.r6 = 0x08
        cpu.label('label_copy')
        cpu.r0 = cpu.mem8[0x00, cpu.er10]
        cpu.mem8[0x00, cpu.er8] = cpu.r0
        cpu.er10 += 0x01
        cpu.er8 += 0x01
        cpu.r6 += 0xFF
        if cpu.ne:
            cpu.branch('label_copy')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0014)]
        cpu.mem16[0x00, cpu.er8] = cpu.er0
        cpu.jump('label_pass')
        cpu.label('labels_done')
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0019)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006D)] = cpu.r0
        cpu.call('reset')
        cpu.label('compare_pass')
        cpu.call('next')
        cpu.compare(cpu.r1, 0x01)
        if cpu.ne:
            cpu.branch('near_23')
        cpu.jump('compare_done')
        cpu.label('near_23')
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('near_24')
        cpu.jump('failure')
        cpu.label('near_24')
        cpu.r4 = cpu.r0
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0014)]
        cpu.er2 += -1
        cpu.r5 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x007C)]
        cpu.r0 = cpu.mem8[cpu.r5, cpu.er2]
        cpu.compare(cpu.r0, cpu.r4)
        if cpu.eq:
            cpu.branch('compare_pass')
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006D)] = cpu.r0
        cpu.jump('compare_pass')
        cpu.label('compare_done')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006D)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('near_25')
        cpu.jump('near_27')
        cpu.label('near_25')
        cpu.er0 = cpu.sp
        cpu.r2 = 0xD4
        cpu.r3 = 0x83
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('near_26')
        cpu.jump('memory')
        cpu.label('near_26')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0012)]
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0016)]
        cpu.er4 = cpu.address('fn_basic_asm__reader') & 0xFFFF
        cpu.er6 = cpu.er14
        cpu.r8 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x007C)]
        cpu.call(BASIC_FLASH)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('near_27')
        cpu.jump('write_error')
        cpu.label('near_27')
        cpu.label('call_block')
        cpu.er8 = cpu.er14
        cpu.er8 += 0x3F
        cpu.er8 += 0x11
        cpu.r0 = 0x00
        cpu.r6 = 0x1C
        cpu.label('clear_call')
        cpu.mem8[0x00, cpu.er8] = cpu.r0
        cpu.er8 += 0x01
        cpu.r6 += 0xFF
        if cpu.ne:
            cpu.branch('clear_call')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0012)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0050)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x007C)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0052)] = cpu.r0
        cpu.er0 = 0x04
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3F
        cpu.er2 += 0x11
        cpu.er4 = cpu.er14
        cpu.er4 += 0x3F
        cpu.er4 += 0x29
        cpu.call(BASIC_MEMORY)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('near_28')
        cpu.jump('call_error')
        cpu.label('near_28')
        cpu.er8 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0000)]
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0068)]
        cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0008)] = cpu.er0
        cpu.er0 = 0x00
        cpu.mem16[0x00, cpu.offset(cpu.er8, 0x000A)] = cpu.er0
        cpu.jump('success')
        cpu.label('skip_loop')
        cpu.call('line_start')
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('near_29')
        cpu.jump('success')
        cpu.label('near_29')
        cpu.call('discard_line')
        cpu.call('get')
        cpu.compare(cpu.r0, 0x0D)
        if cpu.eq:
            cpu.branch('near_30')
        cpu.jump('no_endasm')
        cpu.label('near_30')
        cpu.jump('skip_loop')
        cpu.label('success')
        cpu.er8 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0000)]
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0010)]
        cpu.mem16[0x00, cpu.er8] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0006)]
        cpu.r1 = 0x00
        cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0002)] = cpu.er0
        cpu.er0 = 0x00
        cpu.mem16[0x00, cpu.offset(cpu.er8, 0x000C)] = cpu.er0
        cpu.jump('exit_status')
        cpu.label('bad_operand')
        cpu.er0 = 0x01
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001A)] = cpu.er0
        cpu.jump('failure')
        cpu.label('dup_label')
        cpu.er0 = 0x02
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001A)] = cpu.er0
        cpu.jump('failure')
        cpu.label('no_label')
        cpu.er0 = 0x03
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001A)] = cpu.er0
        cpu.jump('failure')
        cpu.label('br_range')
        cpu.er0 = 0x04
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001A)] = cpu.er0
        cpu.jump('failure')
        cpu.label('address_range')
        cpu.er0 = 0x05
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001A)] = cpu.er0
        cpu.jump('failure')
        cpu.label('no_endasm')
        cpu.er0 = 0x06
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001A)] = cpu.er0
        cpu.jump('failure')
        cpu.label('call_error')
        cpu.er6 = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0008)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000C)] = cpu.er0
        cpu.er0 = 0x00
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001A)] = cpu.er0
        cpu.er0 = cpu.er6
        cpu.jump('error_output')
        cpu.label('write_error')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0008)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000C)] = cpu.er0
        cpu.r0 = 0x00
        cpu.r1 = 0x01
        cpu.jump('error_output')
        cpu.label('memory')
        cpu.er0 = 0x06
        cpu.jump('error_output')
        cpu.label('failure')
        cpu.er0 = 0x02
        cpu.label('error_output')
        cpu.er6 = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006E)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('near_31')
        cpu.jump('reader_error')
        cpu.label('near_31')
        cpu.er8 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0000)]
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000C)]
        cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0004)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0006)]
        cpu.r1 = 0x00
        cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0006)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001A)]
        cpu.mem16[0x00, cpu.offset(cpu.er8, 0x000C)] = cpu.er0
        cpu.er0 = cpu.er6
        cpu.label('exit_status')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3F
        cpu.er2 += 0x3F
        cpu.er2 += 0x02
        cpu.sp = cpu.er2
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('entry_memory')
        cpu.er0 = 0x06
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('peek')
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)]
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0004)]
        cpu.compare(cpu.er2, cpu.er0)
        if cpu.lt:
            cpu.branch('near_32')
        cpu.jump('no_endasm')
        cpu.label('near_32')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0002)]
        cpu.compare(cpu.er2, cpu.er0)
        if cpu.ge:
            cpu.branch('near_33')
        cpu.jump('bad_operand')
        cpu.label('near_33')
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)]
        cpu.r5 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0006)]
        cpu.r0 = cpu.mem8[cpu.r5, cpu.er2]
        cpu.ret()
        cpu.label('get')
        cpu.push(cpu.lr)
        cpu.call('peek')
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)]
        cpu.er2 += 0x01
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)] = cpu.er2
        cpu.pop(cpu.pc)
        cpu.label('upper')
        cpu.compare(cpu.r0, 0x61)
        if cpu.lt:
            cpu.branch('upper_done')
        cpu.compare(cpu.r0, 0x7B)
        if cpu.ge:
            cpu.branch('upper_done')
        cpu.r0 += 0xE0
        cpu.label('upper_done')
        cpu.ret()
        cpu.label('spaces')
        cpu.push(cpu.lr)
        cpu.label('space_loop')
        cpu.call('peek')
        cpu.compare(cpu.r0, 0x20)
        if cpu.ne:
            cpu.branch('spaces_done')
        cpu.call('get')
        cpu.jump('space_loop')
        cpu.label('spaces_done')
        cpu.pop(cpu.pc)
        cpu.label('discard_line')
        cpu.push(cpu.lr)
        cpu.label('discard_byte')
        cpu.call('peek')
        cpu.compare(cpu.r0, 0x0D)
        if cpu.eq:
            cpu.branch('discard_done')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('near_34')
        cpu.jump('no_endasm')
        cpu.label('near_34')
        cpu.call('get')
        cpu.jump('discard_byte')
        cpu.label('discard_done')
        cpu.pop(cpu.pc)
        cpu.label('line_tail')
        cpu.push(cpu.lr)
        cpu.call('spaces')
        cpu.compare(cpu.r0, 0x3B)
        if cpu.ne:
            cpu.branch('tail_check')
        cpu.label('comment_byte')
        cpu.call('get')
        cpu.call('peek')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('near_35')
        cpu.compare(cpu.r0, 0x0D)
        if cpu.ne:
            cpu.branch('comment_byte')
        cpu.label('tail_check')
        cpu.compare(cpu.r0, 0x0D)
        if cpu.eq:
            cpu.branch('near_35')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('near_35')
        cpu.jump('operand_fail')
        cpu.label('near_35')
        cpu.label('tail_done')
        cpu.pop(cpu.pc)
        cpu.label('measure')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000C)] = cpu.er0
        cpu.ret()
        cpu.label('line_start')
        cpu.push(cpu.lr)
        cpu.call('measure')
        cpu.call('spaces')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('near_36')
        cpu.jump('no_endasm')
        cpu.label('near_36')
        cpu.compare(cpu.r0, 0xF9)
        if cpu.ne:
            cpu.branch('ordinary_line')
        cpu.call('get')
        cpu.call('get')
        cpu.compare(cpu.r0, 0xF8)
        if cpu.eq:
            cpu.branch('near_37')
        cpu.jump('bad_operand')
        cpu.label('near_37')
        cpu.call('line_tail')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0010)] = cpu.er0
        cpu.r0 = 0x01
        cpu.pop(cpu.pc)
        cpu.label('ordinary_line')
        cpu.r0 = 0x00
        cpu.pop(cpu.pc)
        cpu.label('identifier')
        cpu.push(cpu.lr)
        cpu.er8 = cpu.er14
        cpu.er8 += 0x30
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er8, 0x0000)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er8, 0x0001)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er8, 0x0002)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er8, 0x0003)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er8, 0x0004)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er8, 0x0005)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er8, 0x0006)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er8, 0x0007)] = cpu.r0
        cpu.r6 = 0x00
        cpu.label('identifier_byte')
        cpu.call('peek')
        cpu.call('upper')
        cpu.compare(cpu.r0, 0x5F)
        if cpu.eq:
            cpu.branch('identifier_accept')
        cpu.compare(cpu.r0, 0x41)
        if cpu.lt:
            cpu.branch('identifier_digit')
        cpu.compare(cpu.r0, 0x5B)
        if cpu.lt:
            cpu.branch('identifier_accept')
        cpu.label('identifier_digit')
        cpu.compare(cpu.r6, 0x00)
        if cpu.eq:
            cpu.branch('identifier_end')
        cpu.compare(cpu.r0, 0x30)
        if cpu.lt:
            cpu.branch('identifier_end')
        cpu.compare(cpu.r0, 0x3A)
        if cpu.ge:
            cpu.branch('identifier_end')
        cpu.label('identifier_accept')
        cpu.compare(cpu.r6, 0x08)
        if cpu.lt:
            cpu.branch('near_38')
        cpu.jump('operand_fail')
        cpu.label('near_38')
        cpu.mem8[0x00, cpu.er8] = cpu.r0
        cpu.er8 += 0x01
        cpu.r6 += 0x01
        cpu.call('get')
        cpu.jump('identifier_byte')
        cpu.label('identifier_end')
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0038)] = cpu.r6
        cpu.compare(cpu.r6, 0x00)
        if cpu.ne:
            cpu.branch('near_39')
        cpu.jump('operand_fail')
        cpu.label('near_39')
        cpu.pop(cpu.pc)
        cpu.label('find_label')
        cpu.push(cpu.lr)
        cpu.er8 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0076)]
        cpu.label('find_record')
        cpu.er0 = cpu.er8
        cpu.er2 = cpu.er14
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.eq:
            cpu.branch('find_missing')
        cpu.r0 = cpu.mem8[0x00, cpu.er8]
        cpu.r1 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0038)]
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.ne:
            cpu.branch('find_next')
        cpu.er10 = cpu.er14
        cpu.er10 += 0x30
        cpu.er12 = cpu.er8
        cpu.er12 += 0x02
        cpu.r6 = 0x08
        cpu.label('find_char')
        cpu.r0 = cpu.mem8[0x00, cpu.er10]
        cpu.r1 = cpu.mem8[0x00, cpu.er12]
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.ne:
            cpu.branch('find_next')
        cpu.er10 += 0x01
        cpu.er12 += 0x01
        cpu.r6 += 0xFF
        if cpu.ne:
            cpu.branch('find_char')
        cpu.er0 = cpu.er8
        cpu.pop(cpu.pc)
        cpu.label('find_next')
        cpu.er8 += 0x0C
        cpu.jump('find_record')
        cpu.label('find_missing')
        cpu.er0 = 0x00
        cpu.pop(cpu.pc)
        cpu.label('even_address')
        cpu.r2 = cpu.r0
        cpu.r2 &= 0x01
        if cpu.eq:
            cpu.branch('near_40')
        cpu.jump('address_range')
        cpu.label('near_40')
        cpu.ret()
        cpu.label('number')
        cpu.push(cpu.lr)
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003E)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003F)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0039)] = cpu.r0
        cpu.call('spaces')
        cpu.compare(cpu.r0, 0x23)
        if cpu.ne:
            cpu.branch('number_sign')
        cpu.call('get')
        cpu.call('spaces')
        cpu.label('number_sign')
        cpu.compare(cpu.r0, 0x2D)
        if cpu.ne:
            cpu.branch('number_plus')
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003E)] = cpu.r0
        cpu.call('get')
        cpu.jump('number_atom')
        cpu.label('number_plus')
        cpu.compare(cpu.r0, 0x2B)
        if cpu.ne:
            cpu.branch('number_atom')
        cpu.call('get')
        cpu.label('number_atom')
        cpu.call('peek')
        cpu.compare(cpu.r0, 0x30)
        if cpu.lt:
            cpu.branch('number_label')
        cpu.compare(cpu.r0, 0x3A)
        if cpu.ge:
            cpu.branch('number_label')
        cpu.call('decimal')
        cpu.pop(cpu.pc)
        cpu.label('number_label')
        cpu.call('identifier')
        cpu.call('find_label')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('number_found')
        cpu.compare(cpu.r1, 0x00)
        if cpu.ne:
            cpu.branch('number_found')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0019)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('near_41')
        cpu.jump('undefined_operand')
        cpu.label('near_41')
        cpu.r0 = 0x02
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0039)] = cpu.r0
        cpu.er0 = 0x00
        cpu.r2 = 0x00
        cpu.jump('label_offset')
        cpu.label('number_found')
        cpu.er8 = cpu.er0
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0039)] = cpu.r0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x000A)]
        cpu.r2 = 0x00
        cpu.label('label_offset')
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x003A)] = cpu.er0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003C)] = cpu.r2
        cpu.call('spaces')
        cpu.compare(cpu.r0, 0x2B)
        if cpu.eq:
            cpu.branch('offset_plus')
        cpu.compare(cpu.r0, 0x2D)
        if cpu.ne:
            cpu.branch('label_number_done')
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003D)] = cpu.r0
        cpu.jump('offset_read')
        cpu.label('offset_plus')
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003D)] = cpu.r0
        cpu.label('offset_read')
        cpu.call('get')
        cpu.call('spaces')
        cpu.call('decimal')
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('near_42')
        cpu.jump('operand_fail')
        cpu.label('near_42')
        cpu.r3 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0039)]
        cpu.compare(cpu.r3, 0x02)
        if cpu.eq:
            cpu.branch('label_number_done')
        cpu.er4 = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x003A)]
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003D)]
        cpu.compare(cpu.r2, 0x00)
        if cpu.ne:
            cpu.branch('offset_subtract')
        cpu.er0 += cpu.er4
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x003A)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('near_43')
        cpu.jump('operand_fail')
        cpu.label('near_43')
        cpu.jump('offset_applied')
        cpu.label('offset_subtract')
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.ge:
            cpu.branch('near_44')
        cpu.jump('operand_fail')
        cpu.label('near_44')
        cpu.r0 -= cpu.r4
        cpu.sub_carry(cpu.r1, cpu.r5)
        cpu.label('offset_applied')
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x003A)] = cpu.er0
        cpu.label('label_number_done')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x003A)]
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003C)]
        cpu.r3 = 0x00
        cpu.pop(cpu.pc)
        cpu.label('undefined_operand')
        cpu.er0 = 0x03
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001A)] = cpu.er0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006C)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('near_45')
        cpu.jump('failure')
        cpu.label('near_45')
        cpu.jump('operand_fail')
        cpu.label('decimal')
        cpu.push(cpu.lr)
        cpu.er10 = 0x00
        cpu.r12 = 0x00
        cpu.r7 = 0x00
        cpu.call('peek')
        cpu.compare(cpu.r0, 0x30)
        if cpu.ne:
            cpu.branch('digit_loop')
        cpu.call('get')
        cpu.r7 = 0x01
        cpu.call('peek')
        cpu.call('upper')
        cpu.compare(cpu.r0, 0x58)
        if cpu.ne:
            cpu.branch('digit_loop')
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003F)] = cpu.r0
        cpu.r7 = 0x00
        cpu.call('get')
        cpu.label('digit_loop')
        cpu.call('peek')
        cpu.call('upper')
        cpu.r0 += 0xD0
        cpu.compare(cpu.r0, 0x0A)
        if cpu.lt:
            cpu.branch('digit_valid')
        cpu.r1 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003F)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('digits_done')
        cpu.r0 += 0xF9
        cpu.compare(cpu.r0, 0x0A)
        if cpu.lt:
            cpu.branch('digits_done')
        cpu.compare(cpu.r0, 0x10)
        if cpu.ge:
            cpu.branch('digits_done')
        cpu.label('digit_valid')
        cpu.r6 = cpu.r0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003F)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('hex_multiply')
        cpu.er0 = cpu.er10
        cpu.r2 = cpu.r12
        cpu.shift_left_carry(cpu.r2, 0x01)
        cpu.shift_left_carry(cpu.r1, 0x01)
        cpu.r0 <<= 0x01
        cpu.shift_left_carry(cpu.r12, 0x01)
        cpu.shift_left_carry(cpu.r11, 0x01)
        cpu.r10 <<= 0x01
        cpu.shift_left_carry(cpu.r12, 0x01)
        cpu.shift_left_carry(cpu.r11, 0x01)
        cpu.r10 <<= 0x01
        cpu.shift_left_carry(cpu.r12, 0x01)
        cpu.shift_left_carry(cpu.r11, 0x01)
        cpu.r10 <<= 0x01
        cpu.r10 += cpu.r0
        cpu.add_carry(cpu.r11, cpu.r1)
        cpu.add_carry(cpu.r12, cpu.r2)
        cpu.jump('digit_add')
        cpu.label('hex_multiply')
        cpu.shift_left_carry(cpu.r12, 0x01)
        cpu.shift_left_carry(cpu.r11, 0x01)
        cpu.r10 <<= 0x01
        cpu.shift_left_carry(cpu.r12, 0x01)
        cpu.shift_left_carry(cpu.r11, 0x01)
        cpu.r10 <<= 0x01
        cpu.shift_left_carry(cpu.r12, 0x01)
        cpu.shift_left_carry(cpu.r11, 0x01)
        cpu.r10 <<= 0x01
        cpu.shift_left_carry(cpu.r12, 0x01)
        cpu.shift_left_carry(cpu.r11, 0x01)
        cpu.r10 <<= 0x01
        cpu.label('digit_add')
        cpu.r10 += cpu.r6
        cpu.add_carry(cpu.r11, 0x00)
        cpu.add_carry(cpu.r12, 0x00)
        cpu.compare(cpu.r12, 0x10)
        if cpu.lt:
            cpu.branch('near_46')
        cpu.jump('operand_fail')
        cpu.label('near_46')
        cpu.r7 = 0x01
        cpu.call('get')
        cpu.jump('digit_loop')
        cpu.label('digits_done')
        cpu.compare(cpu.r7, 0x00)
        if cpu.ne:
            cpu.branch('near_47')
        cpu.jump('operand_fail')
        cpu.label('near_47')
        cpu.er0 = cpu.er10
        cpu.r2 = cpu.r12
        cpu.r3 = 0x00
        cpu.pop(cpu.pc)
        cpu.label('reader')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er14 = cpu.er0
        cpu.er0 = cpu.sp
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0078)] = cpu.er0
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006E)] = cpu.r0
        cpu.compare(cpu.r2, 0x00)
        if cpu.ne:
            cpu.branch('reader_next')
        cpu.call('reset')
        cpu.er0 = 0x00
        cpu.jump('reader_return')
        cpu.label('reader_next')
        cpu.call('next')
        cpu.label('reader_return')
        cpu.r2 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006E)] = cpu.r2
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('reader_error')
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0078)]
        cpu.sp = cpu.er2
        cpu.r0 = 0x00
        cpu.r1 = 0x02
        cpu.jump('reader_return')
        cpu.label('reset')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000E)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0012)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0014)] = cpu.er0
        cpu.er0 = 0x00
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0016)] = cpu.er0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x007D)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0026)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0027)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0028)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0029)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x002A)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x002B)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006C)] = cpu.r0
        cpu.ret()
        cpu.label('next')
        cpu.push(cpu.lr)
        cpu.label('next_again')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0027)]
        cpu.r1 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0026)]
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.ge:
            cpu.branch('near_48')
        cpu.jump('emit_byte')
        cpu.label('near_48')
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0026)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0027)] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0028)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('near_49')
        cpu.jump('data_next')
        cpu.label('near_49')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x002A)]
        cpu.compare(cpu.r0, 0x02)
        if cpu.ne:
            cpu.branch('near_50')
        cpu.jump('next_line')
        cpu.label('near_50')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('line_continue')
        cpu.call('line_start')
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('near_51')
        cpu.jump('stream_end')
        cpu.label('near_51')
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x002A)] = cpu.r0
        cpu.label('line_continue')
        cpu.call('spaces')
        cpu.compare(cpu.r0, 0x0D)
        if cpu.ne:
            cpu.branch('near_52')
        cpu.jump('next_line')
        cpu.label('near_52')
        cpu.compare(cpu.r0, 0x3B)
        if cpu.ne:
            cpu.branch('near_53')
        cpu.jump('finish_line')
        cpu.label('near_53')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('near_54')
        cpu.jump('no_endasm')
        cpu.label('near_54')
        cpu.call('identifier')
        cpu.call('spaces')
        cpu.compare(cpu.r0, 0x3A)
        if cpu.ne:
            cpu.branch('instruction_line')
        cpu.call('get')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0019)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('line_continue')
        cpu.r0 = 0x00
        cpu.r1 = 0x03
        cpu.pop(cpu.pc)
        cpu.label('instruction_line')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0038)]
        cpu.compare(cpu.r0, 0x02)
        if cpu.ne:
            cpu.branch('instruction_match')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0030)]
        cpu.compare(cpu.r0, 0x44)
        if cpu.ne:
            cpu.branch('instruction_match')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0031)]
        cpu.compare(cpu.r0, 0x42)
        if cpu.eq:
            cpu.branch('db_begin')
        cpu.compare(cpu.r0, 0x57)
        if cpu.ne:
            cpu.branch('instruction_match')
        cpu.r0 = 0x02
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0028)] = cpu.r0
        cpu.jump('data_begin')
        cpu.label('db_begin')
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0028)] = cpu.r0
        cpu.label('data_begin')
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x002B)] = cpu.r0
        cpu.jump('data_next')
        cpu.label('instruction_match')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x007D)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('near_55')
        cpu.jump('address_range')
        cpu.label('near_55')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0014)]
        cpu.call('even_address')
        cpu.call('match')
        cpu.call('line_tail')
        cpu.r0 = 0x02
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x002A)] = cpu.r0
        cpu.jump('next_again')
        cpu.label('data_next')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0029)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('near_56')
        cpu.jump('string_byte')
        cpu.label('near_56')
        cpu.call('spaces')
        cpu.r1 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x002B)]
        cpu.compare(cpu.r1, 0x02)
        if cpu.ne:
            cpu.branch('data_value')
        cpu.compare(cpu.r0, 0x2C)
        if cpu.eq:
            cpu.branch('near_57')
        cpu.jump('data_finish')
        cpu.label('near_57')
        cpu.call('get')
        cpu.call('spaces')
        cpu.label('data_value')
        cpu.r0 = 0x02
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x002B)] = cpu.r0
        cpu.call('peek')
        cpu.compare(cpu.r0, 0x22)
        if cpu.ne:
            cpu.branch('data_number')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0028)]
        cpu.compare(cpu.r0, 0x01)
        if cpu.eq:
            cpu.branch('near_58')
        cpu.jump('bad_operand')
        cpu.label('near_58')
        cpu.call('get')
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0029)] = cpu.r0
        cpu.label('string_byte')
        cpu.call('get')
        cpu.compare(cpu.r0, 0x22)
        if cpu.ne:
            cpu.branch('string_ascii')
        cpu.call('peek')
        cpu.compare(cpu.r0, 0x22)
        if cpu.eq:
            cpu.branch('escaped_quote')
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0029)] = cpu.r0
        cpu.jump('data_next')
        cpu.label('escaped_quote')
        cpu.call('get')
        cpu.label('string_ascii')
        cpu.compare(cpu.r0, 0x20)
        if cpu.ge:
            cpu.branch('near_59')
        cpu.jump('bad_operand')
        cpu.label('near_59')
        cpu.compare(cpu.r0, 0x7F)
        if cpu.lt:
            cpu.branch('near_60')
        cpu.jump('bad_operand')
        cpu.label('near_60')
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0048)] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0026)] = cpu.r0
        cpu.jump('next_again')
        cpu.label('data_number')
        cpu.call('number')
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('near_61')
        cpu.jump('bad_operand')
        cpu.label('near_61')
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003E)]
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('near_62')
        cpu.jump('bad_operand')
        cpu.label('near_62')
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0048)] = cpu.er0
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0028)]
        cpu.compare(cpu.r2, 0x01)
        if cpu.ne:
            cpu.branch('near_63')
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('near_63')
        cpu.jump('bad_operand')
        cpu.label('near_63')
        cpu.label('data_word')
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0026)] = cpu.r2
        cpu.jump('next_again')
        cpu.label('data_finish')
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0028)] = cpu.r0
        cpu.label('finish_line')
        cpu.call('line_tail')
        cpu.label('next_line')
        cpu.call('get')
        cpu.compare(cpu.r0, 0x0D)
        if cpu.eq:
            cpu.branch('near_64')
        cpu.jump('no_endasm')
        cpu.label('near_64')
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x002A)] = cpu.r0
        cpu.jump('next_again')
        cpu.label('emit_byte')
        cpu.r1 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += 0x3F
        cpu.er2 += 0x09
        cpu.er2 += cpu.er0
        cpu.r6 = cpu.mem8[0x00, cpu.er2]
        cpu.r0 += 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0027)] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x007D)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('near_65')
        cpu.jump('address_range')
        cpu.label('near_65')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0016)]
        cpu.r2 = 0xFF
        cpu.r3 = 0xFF
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.branch('near_66')
        cpu.jump('address_range')
        cpu.label('near_66')
        cpu.er0 += 0x01
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0016)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0014)]
        cpu.er0 += 0x01
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0014)] = cpu.er0
        cpu.er2 = 0x00
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.branch('emit_ready')
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x007D)] = cpu.r0
        cpu.label('emit_ready')
        cpu.r0 = cpu.r6
        cpu.r1 = 0x00
        cpu.pop(cpu.pc)
        cpu.label('stream_end')
        cpu.r0 = 0x00
        cpu.r1 = 0x01
        cpu.pop(cpu.pc)
        cpu.label('match')
        cpu.push(cpu.lr)
        cpu.er8 = cpu.er14
        cpu.er8 += 0x30
        cpu.er10 = cpu.er14
        cpu.er10 += 0x3F
        cpu.er10 += 0x11
        cpu.r6 = 0x08
        cpu.label('save_mnemonic')
        cpu.r0 = cpu.mem8[0x00, cpu.er8]
        cpu.mem8[0x00, cpu.er10] = cpu.r0
        cpu.er8 += 0x01
        cpu.er10 += 0x01
        cpu.r6 += 0xFF
        if cpu.ne:
            cpu.branch('save_mnemonic')
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0058)] = cpu.r0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0022)] = cpu.er0
        cpu.er0 = cpu.sp
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001C)] = cpu.er0
        cpu.r0 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006C)] = cpu.r0
        cpu.er0 = 0x01
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001A)] = cpu.er0
        cpu.r0 = 0x76
        cpu.r1 = 0xA5
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001E)] = cpu.er0
        cpu.label('candidate')
        cpu.er8 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001E)]
        cpu.r7 = 0x0F
        cpu.er10 = cpu.mem16[cpu.r7, cpu.er8]
        cpu.er0 = cpu.er10
        cpu.er2 = 0x00
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.branch('near_67')
        cpu.jump('match_missing')
        cpu.label('near_67')
        cpu.er12 = cpu.er14
        cpu.er12 += 0x3F
        cpu.er12 += 0x11
        cpu.label('mnemonic_char')
        cpu.r0 = cpu.mem8[cpu.r7, cpu.er10]
        cpu.r1 = cpu.mem8[0x00, cpu.er12]
        cpu.compare(cpu.r0, 0x20)
        if cpu.eq:
            cpu.branch('mnemonic_end')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('mnemonic_end')
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.eq:
            cpu.branch('near_68')
        cpu.jump('candidate_next')
        cpu.label('near_68')
        cpu.er10 += 0x01
        cpu.er12 += 0x01
        cpu.jump('mnemonic_char')
        cpu.label('mnemonic_end')
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('near_69')
        cpu.jump('candidate_next')
        cpu.label('near_69')
        cpu.er0 = cpu.mem16[cpu.r7, cpu.offset(cpu.er8, 0x0002)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0020)] = cpu.er0
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0022)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)] = cpu.er0
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0024)] = cpu.r0
        cpu.r0 = 0xFF
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0047)] = cpu.r0
        cpu.label('grammar_token')
        cpu.er8 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0020)]
        cpu.r7 = 0x0F
        cpu.r0 = cpu.mem8[cpu.r7, cpu.er8]
        cpu.er8 += 0x01
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0020)] = cpu.er8
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006F)] = cpu.r0
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('near_70')
        cpu.jump('grammar_end')
        cpu.label('near_70')
        cpu.compare(cpu.r0, 0x20)
        if cpu.lt:
            cpu.branch('grammar_control')
        cpu.r6 = cpu.r0
        cpu.call('literal')
        cpu.jump('grammar_token')
        cpu.label('grammar_control')
        cpu.compare(cpu.r0, 0x0D)
        if cpu.ne:
            cpu.branch('near_71')
        cpu.jump('segment')
        cpu.label('near_71')
        cpu.compare(cpu.r0, 0x05)
        if cpu.ge:
            cpu.branch('numeric_operand')
        cpu.call('spaces')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006F)]
        cpu.compare(cpu.r0, 0x01)
        if cpu.eq:
            cpu.branch('register_r')
        cpu.r6 = 0x45
        cpu.compare(cpu.r0, 0x02)
        if cpu.eq:
            cpu.branch('register_prefix')
        cpu.r6 = 0x58
        cpu.compare(cpu.r0, 0x03)
        if cpu.eq:
            cpu.branch('register_prefix')
        cpu.r6 = 0x51
        cpu.label('register_prefix')
        cpu.call('literal')
        cpu.label('register_r')
        cpu.r6 = 0x52
        cpu.call('literal')
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003F)] = cpu.r0
        cpu.call('decimal')
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('near_72')
        cpu.jump('operand_fail')
        cpu.label('near_72')
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('near_73')
        cpu.jump('operand_fail')
        cpu.label('near_73')
        cpu.r6 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003F)]
        cpu.compare(cpu.r6, 0x00)
        if cpu.eq:
            cpu.branch('near_74')
        cpu.jump('operand_fail')
        cpu.label('near_74')
        cpu.compare(cpu.r0, 0x10)
        if cpu.lt:
            cpu.branch('near_75')
        cpu.jump('operand_fail')
        cpu.label('near_75')
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003A)] = cpu.r0
        cpu.r1 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006F)]
        cpu.compare(cpu.r1, 0x02)
        if cpu.ne:
            cpu.branch('near_76')
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('near_76')
        cpu.jump('operand_fail')
        cpu.label('near_76')
        cpu.label('register_not_2')
        cpu.compare(cpu.r1, 0x03)
        if cpu.ne:
            cpu.branch('near_77')
        cpu.r0 &= 0x03
        if cpu.eq:
            cpu.branch('near_77')
        cpu.jump('operand_fail')
        cpu.label('near_77')
        cpu.label('register_not_3')
        cpu.compare(cpu.r1, 0x04)
        if cpu.ne:
            cpu.branch('near_78')
        cpu.r0 &= 0x07
        if cpu.eq:
            cpu.branch('near_78')
        cpu.jump('operand_fail')
        cpu.label('near_78')
        cpu.label('register_not_4')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003A)]
        cpu.call('nibble')
        cpu.jump('grammar_token')
        cpu.label('numeric_operand')
        cpu.call('number')
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x003A)] = cpu.er0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003C)] = cpu.r2
        cpu.r6 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006F)]
        cpu.compare(cpu.r6, 0x0B)
        if cpu.ne:
            cpu.branch('near_79')
        cpu.jump('target_operand')
        cpu.label('near_79')
        cpu.compare(cpu.r6, 0x07)
        if cpu.eq:
            cpu.branch('unsigned_twenty')
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('near_80')
        cpu.jump('operand_fail')
        cpu.label('near_80')
        cpu.compare(cpu.r6, 0x08)
        if cpu.lt:
            cpu.branch('unsigned_operand')
        cpu.compare(cpu.r6, 0x0B)
        if cpu.lt:
            cpu.branch('signed_operand')
        cpu.label('unsigned_operand')
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003E)]
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('near_81')
        cpu.jump('operand_fail')
        cpu.label('near_81')
        cpu.compare(cpu.r6, 0x06)
        if cpu.ne:
            cpu.branch('near_82')
        cpu.jump('pack_four')
        cpu.label('near_82')
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('near_83')
        cpu.jump('operand_fail')
        cpu.label('near_83')
        cpu.compare(cpu.r6, 0x0C)
        if cpu.ne:
            cpu.branch('pack_two')
        cpu.compare(cpu.r0, 0x08)
        if cpu.lt:
            cpu.branch('near_84')
        cpu.jump('operand_fail')
        cpu.label('near_84')
        cpu.call('nibble')
        cpu.jump('grammar_token')
        cpu.label('unsigned_twenty')
        cpu.r3 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0039)]
        cpu.compare(cpu.r3, 0x00)
        if cpu.eq:
            cpu.branch('near_85')
        cpu.jump('operand_fail')
        cpu.label('near_85')
        cpu.r3 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003E)]
        cpu.compare(cpu.r3, 0x00)
        if cpu.eq:
            cpu.branch('near_86')
        cpu.jump('operand_fail')
        cpu.label('near_86')
        cpu.r0 = cpu.r2
        cpu.call('nibble')
        cpu.jump('pack_four')
        cpu.label('signed_operand')
        cpu.r4 = 0x00
        cpu.r5 = 0x80
        cpu.compare(cpu.r6, 0x0A)
        if cpu.eq:
            cpu.branch('signed_limit')
        cpu.r4 = 0x80
        cpu.r5 = 0x00
        cpu.compare(cpu.r6, 0x09)
        if cpu.eq:
            cpu.branch('signed_limit')
        cpu.r4 = 0x40
        cpu.r5 = 0x00
        cpu.label('signed_limit')
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003E)]
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('signed_positive')
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.lt:
            cpu.branch('near_87')
        cpu.jump('signed_equal')
        cpu.label('near_87')
        cpu.jump('near_88')
        cpu.label('signed_equal')
        if cpu.eq:
            cpu.branch('near_88')
        cpu.jump('operand_fail')
        cpu.label('near_88')
        cpu.label('signed_negate')
        cpu.er2 = cpu.er0
        cpu.er0 = 0x00
        cpu.r0 -= cpu.r2
        cpu.sub_carry(cpu.r1, cpu.r3)
        cpu.jump('near_89')
        cpu.label('signed_positive')
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003F)]
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('signed_compare')
        cpu.er4 += cpu.er4
        cpu.compare(cpu.r6, 0x0A)
        if cpu.eq:
            cpu.branch('near_89')
        cpu.label('signed_compare')
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.lt:
            cpu.branch('near_89')
        cpu.jump('operand_fail')
        cpu.label('near_89')
        cpu.label('signed_ready')
        cpu.compare(cpu.r6, 0x08)
        if cpu.ne:
            cpu.branch('signed_store')
        cpu.r0 &= 0x7F
        cpu.label('signed_store')
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x003A)] = cpu.er0
        cpu.compare(cpu.r6, 0x0A)
        if cpu.eq:
            cpu.branch('pack_four')
        cpu.label('pack_two')
        cpu.r0 = 0x02
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0071)] = cpu.r0
        cpu.jump('pack_number')
        cpu.label('pack_four')
        cpu.r0 = 0x04
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0071)] = cpu.r0
        cpu.label('pack_number')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0071)]
        cpu.compare(cpu.r0, 0x04)
        if cpu.ne:
            cpu.branch('pack_low')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003B)]
        cpu.call('pack_byte')
        cpu.label('pack_low')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003A)]
        cpu.call('pack_byte')
        cpu.jump('grammar_token')
        cpu.label('target_operand')
        cpu.r3 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003E)]
        cpu.compare(cpu.r3, 0x00)
        if cpu.eq:
            cpu.branch('near_90')
        cpu.jump('operand_fail')
        cpu.label('near_90')
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('near_91')
        cpu.r3 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x007C)]
        cpu.compare(cpu.r2, cpu.r3)
        if cpu.eq:
            cpu.branch('near_91')
        cpu.jump('operand_fail')
        cpu.label('near_91')
        cpu.label('target_ready')
        cpu.r3 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0039)]
        cpu.compare(cpu.r3, 0x02)
        if cpu.ne:
            cpu.branch('target_known')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0014)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x003A)] = cpu.er0
        cpu.label('target_known')
        cpu.call('even_address')
        cpu.jump('pack_four')
        cpu.label('segment')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0072)] = cpu.er0
        cpu.call('spaces')
        cpu.compare(cpu.r0, 0x5B)
        if cpu.eq:
            cpu.branch('segment_absent')
        cpu.call('number')
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0074)] = cpu.er0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0070)] = cpu.r2
        cpu.call('spaces')
        cpu.compare(cpu.r0, 0x3A)
        if cpu.ne:
            cpu.branch('segment_absent')
        cpu.call('get')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0074)]
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0070)]
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('near_92')
        cpu.jump('operand_fail')
        cpu.label('near_92')
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x003E)]
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('near_93')
        cpu.jump('operand_fail')
        cpu.label('near_93')
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('near_94')
        cpu.jump('operand_fail')
        cpu.label('near_94')
        cpu.compare(cpu.r0, 0x10)
        if cpu.lt:
            cpu.branch('near_95')
        cpu.jump('operand_fail')
        cpu.label('near_95')
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0047)] = cpu.r0
        cpu.jump('grammar_token')
        cpu.label('segment_absent')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0072)]
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x000A)] = cpu.er0
        cpu.jump('grammar_token')
        cpu.label('grammar_end')
        cpu.call('line_tail')
        cpu.er8 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001E)]
        cpu.r7 = 0x0F
        cpu.er2 = cpu.mem16[cpu.r7, cpu.offset(cpu.er8, 0x0004)]
        cpu.compare(cpu.r2, 0x00)
        if cpu.ne:
            cpu.branch('near_96')
        cpu.compare(cpu.r3, 0x00)
        if cpu.ne:
            cpu.branch('near_96')
        cpu.jump('mov_word')
        cpu.label('near_96')
        cpu.label('catalogue_encode')
        cpu.r7 = 0x08
        cpu.r0 = cpu.mem8[cpu.r7, cpu.er2]
        cpu.compare(cpu.r0, 0x0A)
        if cpu.eq:
            cpu.branch('reorder_displacement')
        cpu.compare(cpu.r0, 0x0D)
        if cpu.eq:
            cpu.branch('reorder_displacement')
        cpu.jump('encode_ready')
        cpu.label('reorder_displacement')
        cpu.r6 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0045)]
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0044)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0045)] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0043)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0044)] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0042)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0043)] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0041)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0042)] = cpu.r0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0041)] = cpu.r6
        cpu.label('encode_ready')
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0074)] = cpu.er2
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0014)]
        cpu.er4 = cpu.er14
        cpu.er4 += 0x3F
        cpu.er4 += 0x01
        cpu.er6 = cpu.er14
        cpu.er6 += 0x3F
        cpu.er6 += 0x09
        cpu.call(CODEC_ENCODE_ADDRESS)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('encoded')
        cpu.compare(cpu.r0, 0x04)
        if cpu.ne:
            cpu.branch('codec_operand')
        cpu.er0 = 0x04
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001A)] = cpu.er0
        cpu.jump('operand_fail')
        cpu.label('codec_operand')
        cpu.compare(cpu.r0, 0x03)
        if cpu.ne:
            cpu.branch('operand_fail')
        cpu.er0 = 0x05
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001A)] = cpu.er0
        cpu.jump('operand_fail')
        cpu.label('encoded')
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0026)] = cpu.r2
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0074)]
        cpu.r7 = 0x08
        cpu.r0 = cpu.mem8[cpu.r7, cpu.er2]
        cpu.compare(cpu.r0, 0x0F)
        if cpu.ne:
            cpu.branch('match_done')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x007C)]
        cpu.r0 |= 0xF0
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0049)] = cpu.r0
        cpu.label('match_done')
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006C)] = cpu.r0
        cpu.pop(cpu.pc)
        cpu.label('mov_word')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0043)]
        cpu.r1 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0044)]
        cpu.r0 <<= 0x04
        cpu.r0 |= cpu.r1
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0048)] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0041)]
        cpu.r1 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0042)]
        cpu.r0 <<= 0x04
        cpu.r0 |= cpu.r1
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x004A)] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0040)]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0049)] = cpu.r0
        cpu.r0 += 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x004B)] = cpu.r0
        cpu.r0 = 0x04
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0026)] = cpu.r0
        cpu.jump('match_done')
        cpu.label('operand_fail')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006C)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('near_97')
        cpu.jump('bad_operand')
        cpu.label('near_97')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001C)]
        cpu.sp = cpu.er0
        cpu.label('candidate_next')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001E)]
        cpu.er0 += 0x06
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x001E)] = cpu.er0
        cpu.jump('candidate')
        cpu.label('match_missing')
        cpu.r0 = 0x00
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x006C)] = cpu.r0
        cpu.jump('failure')
        cpu.label('literal')
        cpu.push(cpu.lr)
        cpu.call('spaces')
        cpu.call('get')
        cpu.call('upper')
        cpu.compare(cpu.r0, cpu.r6)
        if cpu.eq:
            cpu.branch('near_98')
        cpu.jump('operand_fail')
        cpu.label('near_98')
        cpu.pop(cpu.pc)
        cpu.label('nibble')
        cpu.r2 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0024)]
        cpu.r3 = 0x00
        cpu.er4 = cpu.er14
        cpu.er4 += 0x3F
        cpu.er4 += 0x01
        cpu.er4 += cpu.er2
        cpu.mem8[0x00, cpu.er4] = cpu.r0
        cpu.r2 += 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0024)] = cpu.r2
        cpu.ret()
        cpu.label('pack_byte')
        cpu.push(cpu.lr)
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0070)] = cpu.r0
        cpu.r0 >>= 0x04
        cpu.call('nibble')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0070)]
        cpu.r0 &= 0x0F
        cpu.call('nibble')
        cpu.pop(cpu.pc)
