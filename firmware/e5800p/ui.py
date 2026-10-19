"""Fixed-layout e5800p ui routines and tables."""

from kits import cpu

UI_TEXT_ADDRESS = 0x81E06
ROM_DRAW_TEXT = 0x041DA
ROM_REFRESH = 0x043BE
SCANNER_ADDRESS = 0x80800
PROGRAM_ADDRESS = 0xFE000
ROM_READ_KEY = 0x1234E
ROM_NORMALIZE_KEY = 0x1249C

SMALL_TABLE = bytes((
    0x2E, 0x3F, 0x80, 0x94, 0x85, 0x94, 0x8A, 0x94, 0x8F, 0x94, 0x94, 0x94, 0x99, 0x94, 0x9E, 0x94,
    0x33, 0x3F, 0x38, 0x3F, 0x86, 0x90, 0x42, 0x3F, 0x47, 0x3F, 0x4C, 0x3F, 0x51, 0x3F, 0x56, 0x3F,
    0x5B, 0x3F, 0x60, 0x3F, 0x65, 0x3F, 0x6A, 0x3F, 0x6F, 0x3F, 0x74, 0x3F, 0x79, 0x3F, 0x7E, 0x3F,
    0x83, 0x3F, 0x88, 0x3F, 0xA3, 0x94, 0xA8, 0x94, 0xAD, 0x94, 0xB2, 0x94, 0xB7, 0x94, 0xBC, 0x94,
    0xC1, 0x94, 0x8D, 0x3F, 0x92, 0x3F, 0x97, 0x3F, 0x9C, 0x3F, 0xA1, 0x3F, 0xA6, 0x3F, 0xC6, 0x94,
    0xCB, 0x94, 0xD0, 0x94, 0xD5, 0x94, 0xDA, 0x94, 0xDF, 0x94, 0xE4, 0x94, 0xE9, 0x94, 0xAB, 0x3F,
    0xEE, 0x94, 0xB5, 0x3F, 0xBA, 0x3F, 0xF3, 0x94, 0xF8, 0x94, 0xFD, 0x94, 0x02, 0x95, 0x07, 0x95,
    0xBF, 0x3F, 0xC4, 0x3F, 0x0C, 0x95, 0x11, 0x95, 0x16, 0x95, 0x1B, 0x95, 0x20, 0x95, 0x25, 0x95,
))

SMALL_TABLE_LABELS = {
    'small_table': 0x0,
}

SMALL_GLYPHS = bytes((
    0x20, 0x20, 0x20, 0x00, 0x20, 0x50, 0x50, 0x00, 0x00, 0x00, 0x20, 0x70, 0x20, 0x70, 0x20, 0x30,
    0x60, 0x30, 0x60, 0x20, 0x50, 0x10, 0x20, 0x40, 0x50, 0x20, 0x50, 0x20, 0x50, 0x30, 0x20, 0x20,
    0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x20, 0x00, 0x00, 0x20, 0x00, 0x20, 0x40, 0x10, 0x20, 0x40,
    0x20, 0x10, 0x00, 0x70, 0x00, 0x70, 0x00, 0x40, 0x20, 0x10, 0x20, 0x40, 0x60, 0x10, 0x20, 0x00,
    0x20, 0x70, 0x50, 0x70, 0x40, 0x70, 0x70, 0x40, 0x50, 0x50, 0x70, 0x50, 0x50, 0x70, 0x50, 0x50,
    0x70, 0x20, 0x20, 0x20, 0x70, 0x30, 0x10, 0x10, 0x50, 0x20, 0x50, 0x50, 0x60, 0x50, 0x50, 0x40,
    0x40, 0x40, 0x40, 0x70, 0x50, 0x70, 0x70, 0x50, 0x50, 0x50, 0x70, 0x70, 0x70, 0x50, 0x60, 0x50,
    0x60, 0x40, 0x40, 0x70, 0x40, 0x70, 0x10, 0x70, 0x70, 0x20, 0x20, 0x20, 0x20, 0x50, 0x50, 0x50,
    0x50, 0x70, 0x50, 0x50, 0x50, 0x50, 0x20, 0x50, 0x50, 0x70, 0x70, 0x50, 0x70, 0x10, 0x20, 0x40,
    0x70, 0x60, 0x40, 0x40, 0x40, 0x60, 0x40, 0x40, 0x20, 0x10, 0x10, 0x30, 0x10, 0x10, 0x10, 0x30,
    0x20, 0x50, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x70,
))

SMALL_GLYPHS_LABELS = {
    'small_glyphs': 0x0,
}


def install(fw):
    fw.data('small_table', SMALL_TABLE, address=0xF9400, labels=SMALL_TABLE_LABELS)
    fw.data('small_glyphs', SMALL_GLYPHS, address=0xF9480, labels=SMALL_GLYPHS_LABELS)
    fw.data('small_star', bytes((0x50, 0x20, 0x70, 0x20, 0x50, 0)), address=0xF9086)

    @fw.function(native=True, address=0x80200)
    def selector():
        cpu.label('selector')
        cpu.label('entry')
        cpu.push(cpu.lr)
        cpu.push(cpu.er14)
        cpu.label('draw')
        cpu.call('fn_ui_menu')
        cpu.data(b'PROGRAM\0PROG\0ASM / HEX\0\0')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('prog')
        cpu.compare(cpu.r0, 1)
        if cpu.eq:
            cpu.branch('asm')
        cpu.r0 = 0x81
        cpu.mem8[0x8091] = cpu.r0
        cpu.pop(cpu.er14)
        cpu.pop(cpu.lr)
        cpu.ret()
        cpu.label('prog')
        cpu.jump(0xCA05E)
        cpu.label('asm')
        cpu.er12 = 0x4000
        cpu.r5 = 0
        cpu.call(PROGRAM_ADDRESS)
        cpu.jump('draw')


    @fw.function(native=True, address=0x80800)
    def scanner():
        cpu.label('scanner')
        cpu.push(cpu.lr)
        cpu.sp += -2
        cpu.er0 = cpu.sp
        cpu.call(ROM_READ_KEY)
        cpu.er0 = cpu.sp
        cpu.call(ROM_NORMALIZE_KEY)
        cpu.er0 = cpu.sp
        cpu.er0 = cpu.mem16[cpu.er0]
        cpu.compare(cpu.r1, 0x75)
        if cpu.ne:
            cpu.branch('next_66')
        cpu.compare(cpu.r0, 0x32)
        if cpu.ne:
            cpu.branch('next_50')
        cpu.r0 = 0xFA
        cpu.branch('next_66')
        cpu.label('next_50')
        cpu.compare(cpu.r0, 0x34)
        if cpu.ne:
            cpu.branch('next_52')
        cpu.r0 = 0xFB
        cpu.branch('next_66')
        cpu.label('next_52')
        cpu.compare(cpu.r0, 0x44)
        if cpu.ne:
            cpu.branch('next_68')
        cpu.r0 = 0xFC
        cpu.branch('next_66')
        cpu.label('next_68')
        cpu.compare(cpu.r0, 0x45)
        if cpu.ne:
            cpu.branch('next_69')
        cpu.r0 = 0xFD
        cpu.branch('next_66')
        cpu.label('next_69')
        cpu.compare(cpu.r0, 0x47)
        if cpu.ne:
            cpu.branch('next_71')
        cpu.r0 = 0xFE
        cpu.branch('next_66')
        cpu.label('next_71')
        cpu.compare(cpu.r0, 0x42)
        if cpu.ne:
            cpu.branch('next_66')
        cpu.r0 = 0xFF
        cpu.branch('next_66')
        cpu.label('next_66')
        cpu.label('done')
        cpu.sp += 0x02
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0x81E06)
    def ui_text():
        cpu.label('ui_text')
        cpu.push(cpu.xr4)
        cpu.push(cpu.xr8)
        cpu.er4 = cpu.er0
        cpu.er8 = cpu.er6
        cpu.er6 = 0x00
        cpu.label('next')
        cpu.er8 = cpu.er8
        if cpu.eq:
            cpu.branch('fail')
        cpu.er8 += -1
        cpu.r0 = cpu.mem8[0x0F, cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('nul')
        cpu.er8 = cpu.er8
        if cpu.eq:
            cpu.branch('truncate')
        cpu.mem8[cpu.er4] = cpu.r0
        cpu.er4 += 0x01
        cpu.er2 += 0x01
        cpu.er6 += 0x01
        cpu.branch('next')
        cpu.label('truncate')
        cpu.r0 = 0x00
        cpu.mem8[cpu.er4] = cpu.r0
        cpu.label('fail')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.branch('done')
        cpu.label('nul')
        cpu.mem8[cpu.er4] = cpu.r0
        cpu.er0 = cpu.er6
        cpu.label('done')
        cpu.pop(cpu.xr8)
        cpu.pop(cpu.xr4)
        cpu.ret()


    @fw.function(native=True, address=0xF9000)
    def small_text():
        cpu.label('small_text')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.er10 = cpu.er2
        cpu.r0 = cpu.r9
        cpu.r1 = 0x0C
        cpu.multiply(cpu.er0, cpu.r1)
        cpu.r12 = 0xE0
        cpu.r13 = 0x80
        cpu.er12 += cpu.er0
        cpu.r0 = cpu.r8
        cpu.r0 >>= 0x03
        cpu.r1 = 0x00
        cpu.er12 += cpu.er0
        cpu.label('char')
        cpu.compare(cpu.r8, 0x60)
        if cpu.ge:
            cpu.branch('done')
        cpu.r0 = cpu.mem8[cpu.er10]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('done')
        cpu.compare(cpu.r0, 0x20)
        if cpu.lt:
            cpu.branch('unknown')
        cpu.compare(cpu.r0, 0x60)
        if cpu.lt:
            cpu.branch('lookup')
        cpu.label('unknown')
        cpu.r0 = 0x3F
        cpu.label('lookup')
        cpu.r0 += 0xE0
        cpu.r0 <<= 0x01
        cpu.r1 = 0x00
        cpu.r2 = 0x00
        cpu.r3 = 0x94
        cpu.er2 += cpu.er0
        cpu.er14 = cpu.mem16[0x0F, cpu.er2]
        cpu.r4 = cpu.r8
        cpu.r4 &= 0x04
        cpu.r6 = 0x05
        cpu.label('row')
        cpu.test_bit(cpu.r15, 7)
        if cpu.eq:
            cpu.branch('rom')
        cpu.r0 = cpu.mem8[0x0F, cpu.er14]
        cpu.branch('shift')
        cpu.label('rom')
        cpu.r0 = cpu.mem8[cpu.er14]
        cpu.label('shift')
        cpu.r0 &= 0x70
        cpu.compare(cpu.r4, 0x00)
        if cpu.eq:
            cpu.branch('high')
        cpu.r0 >>= 0x04
        cpu.r1 = cpu.mem8[cpu.er12]
        cpu.r1 &= 0xF0
        cpu.branch('store')
        cpu.label('high')
        cpu.r1 = cpu.mem8[cpu.er12]
        cpu.r1 &= 0x0F
        cpu.label('store')
        cpu.r0 |= cpu.r1
        cpu.mem8[cpu.er12] = cpu.r0
        cpu.er14 += 0x01
        cpu.er12 += 0x0C
        cpu.r6 += 0xFF
        if cpu.ne:
            cpu.branch('row')
        cpu.er12 += -60
        cpu.compare(cpu.r4, 0x00)
        if cpu.eq:
            cpu.branch('next')
        cpu.er12 += 0x01
        cpu.label('next')
        cpu.r8 += 0x04
        cpu.er10 += 0x01
        cpu.branch('char')
        cpu.label('done')
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def ui_menu():
        # Inline title, items and an empty terminator; return a zero-based choice.
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.push(cpu.lr)
        cpu.pop(cpu.xr4)
        cpu.sp += -96
        cpu.er14 = cpu.sp
        cpu.mem16[0, cpu.offset(cpu.er14, 64)] = cpu.er4
        cpu.mem8[0, cpu.offset(cpu.er14, 66)] = cpu.r6
        cpu.r7 = 0
        cpu.label('count')
        cpu.r0 = cpu.mem8[cpu.r6, cpu.er4]
        cpu.er4 += 1
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('count')
        cpu.r7 += 1
        cpu.r0 = cpu.mem8[cpu.r6, cpu.er4]
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('count')
        cpu.er4 += 1
        cpu.r7 += 0xFF
        cpu.mem8[0, cpu.offset(cpu.er14, 67)] = cpu.r7
        cpu.r0 = cpu.r4
        cpu.r0 &= 1
        if cpu.ne:
            cpu.er4 += 1
        cpu.mem16[0, cpu.offset(cpu.er14, 108)] = cpu.er4
        cpu.er0 = 0
        cpu.r0 = cpu.r6
        cpu.mem16[0, cpu.offset(cpu.er14, 110)] = cpu.er0
        cpu.er0 = cpu.mem16[0, 0x80A0]
        cpu.mem16[0, cpu.offset(cpu.er14, 72)] = cpu.er0
        cpu.r0 = cpu.mem8[0, 0x80A2]
        cpu.mem8[0, cpu.offset(cpu.er14, 74)] = cpu.r0
        cpu.r0 = 0
        cpu.mem8[0, cpu.offset(cpu.er14, 68)] = cpu.r0
        cpu.mem8[0, 0x80A1] = cpu.r0
        cpu.label('draw')
        cpu.er2 = cpu.er14
        cpu.r0 = 0
        cpu.r4 = 64
        cpu.label('clear')
        cpu.mem8[0, cpu.er2] = cpu.r0
        cpu.er2 += 1
        cpu.r4 += 0xFF
        if cpu.ne:
            cpu.branch('clear')
        cpu.er8 = cpu.mem16[0, cpu.offset(cpu.er14, 64)]
        cpu.r10 = cpu.mem8[0, cpu.offset(cpu.er14, 66)]
        cpu.er12 = cpu.er14
        cpu.label('title')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er8]
        cpu.er8 += 1
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('page_title')
        cpu.mem8[0, cpu.er12] = cpu.r0
        cpu.er12 += 1
        cpu.branch('title')
        cpu.label('page_title')
        cpu.er0 = cpu.er12
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, 67)]
        cpu.compare(cpu.r2, 3)
        if cpu.gt:
            cpu.call('fn_apps_copy_text')
            cpu.data(b' <>EXIT\0')
        else:
            cpu.call('fn_apps_copy_text')
            cpu.data(b' EXIT\0')
        cpu.r4 = cpu.mem8[0, cpu.offset(cpu.er14, 68)]
        cpu.compare(cpu.r4, 0)
        if cpu.eq:
            cpu.branch('items')
        cpu.label('skip')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er8]
        cpu.er8 += 1
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('skip')
        cpu.r4 += 0xFF
        if cpu.ne:
            cpu.branch('skip')
        cpu.label('items')
        cpu.r4 = cpu.mem8[0, cpu.offset(cpu.er14, 67)]
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 68)]
        cpu.r4 -= cpu.r0
        cpu.compare(cpu.r4, 3)
        if cpu.gt:
            cpu.r4 = 3
        cpu.mem8[0, cpu.offset(cpu.er14, 71)] = cpu.r4
        cpu.r5 = 0
        cpu.label('row')
        cpu.compare(cpu.r5, cpu.r4)
        if cpu.ge:
            cpu.branch('refresh')
        cpu.er0 = 0
        cpu.r0 = cpu.r5
        cpu.r0 += 1
        cpu.r0 <<= 4
        cpu.er12 = cpu.er14
        cpu.er12 += cpu.er0
        cpu.r0 = cpu.r5
        cpu.r0 += 0x31
        cpu.mem8[0, cpu.er12] = cpu.r0
        cpu.er12 += 1
        cpu.r0 = 0x3A
        cpu.mem8[0, cpu.er12] = cpu.r0
        cpu.er12 += 1
        cpu.label('text')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er8]
        cpu.er8 += 1
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('row_done')
        cpu.mem8[0, cpu.er12] = cpu.r0
        cpu.er12 += 1
        cpu.branch('text')
        cpu.label('row_done')
        cpu.r5 += 1
        cpu.branch('row')
        cpu.label('refresh')
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_screen')
        cpu.label('key')
        cpu.call(SCANNER_ADDRESS)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.branch('cancel')
        cpu.compare(cpu.r0, 0xFC)
        if cpu.eq:
            cpu.branch('left')
        cpu.compare(cpu.r0, 0xFD)
        if cpu.eq:
            cpu.branch('right')
        cpu.compare(cpu.r0, 0x31)
        if cpu.lt:
            cpu.branch('key')
        cpu.r0 += 0xCF
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, 71)]
        cpu.compare(cpu.r0, cpu.r2)
        if cpu.ge:
            cpu.branch('key')
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, 68)]
        cpu.r0 += cpu.r2
        cpu.r1 = 0
        cpu.branch('done')
        cpu.label('left')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 68)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('key')
        cpu.r0 += 0xFD
        cpu.mem8[0, cpu.offset(cpu.er14, 68)] = cpu.r0
        cpu.jump('draw')
        cpu.label('right')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 68)]
        cpu.r0 += 3
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, 67)]
        cpu.compare(cpu.r0, cpu.r2)
        if cpu.ge:
            cpu.branch('key')
        cpu.mem8[0, cpu.offset(cpu.er14, 68)] = cpu.r0
        cpu.jump('draw')
        cpu.label('cancel')
        cpu.er0 = 0xFFFF
        cpu.label('done')
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, 72)]
        cpu.mem16[0, 0x80A0] = cpu.er2
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, 74)]
        cpu.mem8[0, 0x80A2] = cpu.r2
        cpu.sp += 96
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
