"""Fixed-layout e5800p storage routines and tables."""

from kits import cpu

JOURNAL_BACKUP = 0x83E00
JOURNAL_PROGRAM = 0x83D80
JOURNAL_PROGRAM_RAM = 0x83CC0
JOURNAL_COMPARE = 0x83A80
JOURNAL_COMPARE_RAM = 0x83C40
JOURNAL_CRC = 0x83A00
JOURNAL_FINISH = 0x83F00
JOURNAL_CHECK = 0x83B00
JOURNAL_ERASED = 0x83C00
ROM_FLASH_ERASE = 0x04EF4
JOURNAL_META = 0x83D00
ROM_FLASH_PROGRAM = 0x04E86
JOURNAL_RECOVER = 0x83800


def install(fw):
    @fw.function(native=True, address=0x83000)
    def journal_commit():
        cpu.label('journal_commit')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.xr8)
        cpu.push(cpu.er12)
        cpu.push(cpu.er14)
        cpu.er14 = cpu.er0
        cpu.er12 = cpu.er2
        cpu.r0 &= 0x1F
        if cpu.ne:
            cpu.branch('fail_near')
        cpu.compare(cpu.r1, 0x40)
        if cpu.lt:
            cpu.branch('fail_near')
        cpu.compare(cpu.r1, 0x5F)
        if cpu.lt:
            cpu.branch('page_ok')
        if cpu.ne:
            cpu.branch('fail_near')
        cpu.r0 = cpu.r14
        cpu.compare(cpu.r0, 0xF0)
        if cpu.lt:
            cpu.branch('page_ok')
        cpu.label('fail_near')
        cpu.jump('fail')
        cpu.label('page_ok')
        cpu.call(JOURNAL_BACKUP)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('backup_ready')
        cpu.jump('fail')
        cpu.label('backup_ready')
        cpu.er6 = cpu.er14
        cpu.r7 += 0xC0
        cpu.r4 = 0x00
        cpu.r5 = 0x60
        cpu.r0 = 0x00
        cpu.r1 = 0x40
        cpu.call(JOURNAL_PROGRAM)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('prefix_written')
        cpu.jump('fail')
        cpu.label('prefix_written')
        cpu.er0 = cpu.er14
        cpu.er4 = cpu.er12
        cpu.er6 = 0x20
        cpu.r2 = 0xE0
        cpu.r3 = 0x5F
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.branch('full_page')
        cpu.er6 = 0x10
        cpu.label('full_page')
        cpu.call(JOURNAL_PROGRAM_RAM)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('page_written')
        cpu.jump('fail')
        cpu.label('page_written')
        cpu.er4 = cpu.er14
        cpu.r2 = 0xE0
        cpu.r3 = 0x5F
        cpu.compare(cpu.er4, cpu.er2)
        if cpu.ne:
            cpu.branch('full_suffix')
        cpu.er4 += 0x10
        cpu.r6 = 0xF0
        cpu.r7 = 0x5F
        cpu.r6 -= cpu.r14
        cpu.sub_carry(cpu.r7, cpu.r15)
        cpu.er6 += -16
        cpu.er0 = cpu.er14
        cpu.er0 += 0x10
        cpu.branch('write_suffix')
        cpu.label('full_suffix')
        cpu.er4 += 0x20
        cpu.r6 = 0xF0
        cpu.r7 = 0x5F
        cpu.r6 -= cpu.r14
        cpu.sub_carry(cpu.r7, cpu.r15)
        cpu.er6 += -32
        cpu.er0 = cpu.er14
        cpu.er0 += 0x20
        cpu.label('write_suffix')
        cpu.r5 += 0x20
        cpu.call(JOURNAL_PROGRAM)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('suffix_written')
        cpu.jump('fail')
        cpu.label('suffix_written')
        cpu.r0 = 0x00
        cpu.r1 = 0x40
        cpu.r2 = 0x00
        cpu.r3 = 0x60
        cpu.er4 = cpu.er14
        cpu.r5 += 0xC0
        cpu.call(JOURNAL_COMPARE)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('prefix_compared')
        cpu.jump('fail')
        cpu.label('prefix_compared')
        cpu.er0 = cpu.er14
        cpu.er2 = cpu.er12
        cpu.er4 = 0x20
        cpu.r6 = 0xE0
        cpu.r7 = 0x5F
        cpu.compare(cpu.er0, cpu.er6)
        if cpu.ne:
            cpu.branch('full_compare')
        cpu.er4 = 0x10
        cpu.label('full_compare')
        cpu.call(JOURNAL_COMPARE_RAM)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('page_compared')
        cpu.jump('fail')
        cpu.label('page_compared')
        cpu.er0 = cpu.er14
        cpu.r2 = 0xE0
        cpu.r3 = 0x5F
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.branch('full_compare_suffix')
        cpu.er0 += 0x10
        cpu.branch('compare_suffix')
        cpu.label('full_compare_suffix')
        cpu.er0 += 0x20
        cpu.label('compare_suffix')
        cpu.er2 = cpu.er0
        cpu.r3 += 0x20
        cpu.r4 = 0xF0
        cpu.r5 = 0x5F
        cpu.r4 -= cpu.r0
        cpu.sub_carry(cpu.r5, cpu.r1)
        cpu.call(JOURNAL_COMPARE)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('suffix_compared')
        cpu.jump('fail')
        cpu.label('suffix_compared')
        cpu.r0 = 0x00
        cpu.r1 = 0x40
        cpu.r2 = 0xF0
        cpu.r3 = 0x1F
        cpu.call(JOURNAL_CRC)
        cpu.call(JOURNAL_FINISH)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('s1_checked')
        cpu.jump('fail')
        cpu.label('s1_checked')
        cpu.er0 = 0x00
        cpu.jump('done')
        cpu.label('fail')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.label('done')
        cpu.pop(cpu.er14)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0x83800)
    def journal_recover():
        cpu.label('journal_recover')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.xr8)
        cpu.push(cpu.er12)
        cpu.push(cpu.er14)
        cpu.r0 = 0x00
        cpu.r1 = 0x40
        cpu.call(JOURNAL_CHECK)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('good')
        cpu.r0 = 0x00
        cpu.r1 = 0x60
        cpu.call(JOURNAL_CHECK)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('restore')
        cpu.r0 = 0x00
        cpu.r1 = 0x40
        cpu.r2 = 0x00
        cpu.r3 = 0x20
        cpu.call(JOURNAL_ERASED)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('good')
        cpu.jump('bad')
        cpu.label('restore')
        cpu.r0 = 0x00
        cpu.r1 = 0x60
        cpu.r2 = 0xF0
        cpu.r3 = 0x1F
        cpu.call(JOURNAL_CRC)
        cpu.er12 = cpu.er0
        cpu.r0 = 0x01
        cpu.call(ROM_FLASH_ERASE)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.r0 = 0x00
        cpu.r1 = 0x40
        cpu.r4 = 0x00
        cpu.r5 = 0x60
        cpu.r6 = 0xF0
        cpu.r7 = 0x1F
        cpu.call(JOURNAL_PROGRAM)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.r0 = 0x00
        cpu.r1 = 0x40
        cpu.r2 = 0x00
        cpu.r3 = 0x60
        cpu.r4 = 0xF0
        cpu.r5 = 0x1F
        cpu.call(JOURNAL_COMPARE)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.r0 = 0xF0
        cpu.r1 = 0x5F
        cpu.er2 = cpu.er12
        cpu.call(JOURNAL_META)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.r0 = 0x00
        cpu.r1 = 0x40
        cpu.call(JOURNAL_CHECK)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.label('good')
        cpu.er0 = 0x00
        cpu.branch('out')
        cpu.label('bad')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.label('out')
        cpu.pop(cpu.er14)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0x83A00)
    def journal_crc():
        cpu.label('journal_crc')
        cpu.er4 = cpu.er0
        cpu.er6 = cpu.er2
        cpu.r8 = 0xFF
        cpu.r9 = 0xFF
        cpu.label('byte')
        cpu.r0 = cpu.mem8[0x08, cpu.er4]
        cpu.r9 ^= cpu.r0
        cpu.r2 = 0x08
        cpu.label('bit')
        cpu.r0 = cpu.r9
        cpu.r0 &= 0x80
        cpu.shift_left_carry(cpu.r9, 0x01)
        cpu.r8 <<= 0x01
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('no_poly')
        cpu.r8 ^= 0x21
        cpu.r9 ^= 0x10
        cpu.label('no_poly')
        cpu.r2 += 0xFF
        if cpu.ne:
            cpu.branch('bit')
        cpu.er4 += 0x01
        cpu.er6 += -1
        if cpu.ne:
            cpu.branch('byte')
        cpu.er0 = cpu.er8
        cpu.ret()


    @fw.function(native=True, address=0x83A80)
    def journal_compare():
        cpu.label('journal_compare')
        cpu.er6 = cpu.er0
        cpu.er8 = cpu.er2
        cpu.er10 = cpu.er4
        cpu.label('loop')
        cpu.er10 = cpu.er10
        if cpu.eq:
            cpu.branch('equal')
        cpu.r0 = cpu.mem8[0x08, cpu.er6]
        cpu.r1 = cpu.mem8[0x08, cpu.er8]
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.ne:
            cpu.branch('different')
        cpu.er6 += 0x01
        cpu.er8 += 0x01
        cpu.er10 += -1
        cpu.branch('loop')
        cpu.label('equal')
        cpu.er0 = 0x00
        cpu.ret()
        cpu.label('different')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.ret()


    @fw.function(native=True, address=0x83B00)
    def journal_check():
        cpu.label('journal_check')
        cpu.push(cpu.lr)
        cpu.push(cpu.er12)
        cpu.push(cpu.er14)
        cpu.push(cpu.er4)
        cpu.er12 = cpu.er0
        cpu.r2 = 0xF0
        cpu.r3 = 0x1F
        cpu.call(JOURNAL_CRC)
        cpu.er14 = cpu.er0
        cpu.er4 = cpu.er12
        cpu.r4 += 0xF0
        cpu.add_carry(cpu.r5, 0x1F)
        cpu.r0 = cpu.mem8[0x08, cpu.er4]
        cpu.compare(cpu.r0, cpu.r14)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er4 += 0x01
        cpu.r0 = cpu.mem8[0x08, cpu.er4]
        cpu.compare(cpu.r0, cpu.r15)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er4 += 0x01
        cpu.r0 = cpu.mem8[0x08, cpu.er4]
        cpu.r0 ^= 0xFF
        cpu.compare(cpu.r0, cpu.r14)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er4 += 0x01
        cpu.r0 = cpu.mem8[0x08, cpu.er4]
        cpu.r0 ^= 0xFF
        cpu.compare(cpu.r0, cpu.r15)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er4 += 0x01
        cpu.r0 = cpu.mem8[0x08, cpu.er4]
        cpu.compare(cpu.r0, 0x4A)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er4 += 0x01
        cpu.r0 = cpu.mem8[0x08, cpu.er4]
        cpu.compare(cpu.r0, 0xB6)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er4 += 0x01
        cpu.er0 = 0x00
        cpu.branch('out')
        cpu.label('bad')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.label('out')
        cpu.pop(cpu.er4)
        cpu.pop(cpu.er14)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0x83C00)
    def journal_erased():
        cpu.label('journal_erased')
        cpu.er4 = cpu.er0
        cpu.er6 = cpu.er2
        cpu.label('loop')
        cpu.r0 = cpu.mem8[0x08, cpu.er4]
        cpu.compare(cpu.r0, 0xFF)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er4 += 0x01
        cpu.er6 += -1
        if cpu.ne:
            cpu.branch('loop')
        cpu.er0 = 0x00
        cpu.ret()
        cpu.label('bad')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.ret()


    @fw.function(native=True, address=0x83C40)
    def journal_compare_ram():
        cpu.label('journal_compare_ram')
        cpu.er6 = cpu.er0
        cpu.er8 = cpu.er2
        cpu.er10 = cpu.er4
        cpu.label('loop')
        cpu.er10 = cpu.er10
        if cpu.eq:
            cpu.branch('equal')
        cpu.r0 = cpu.mem8[0x08, cpu.er6]
        cpu.r1 = cpu.mem8[cpu.er8]
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.ne:
            cpu.branch('different')
        cpu.er6 += 0x01
        cpu.er8 += 0x01
        cpu.er10 += -1
        cpu.branch('loop')
        cpu.label('equal')
        cpu.er0 = 0x00
        cpu.ret()
        cpu.label('different')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.ret()


    @fw.function(native=True, address=0x83CC0)
    def journal_program_ram():
        cpu.label('journal_program_ram')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.push(cpu.er6)
        cpu.r8 = 0x00
        cpu.push(cpu.r8)
        cpu.push(cpu.er4)
        cpu.er2 = 0x08
        cpu.call(ROM_FLASH_PROGRAM)
        cpu.sp += 0x06
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0x83D00)
    def journal_meta():
        cpu.label('journal_meta')
        cpu.push(cpu.lr)
        cpu.push(cpu.er12)
        cpu.push(cpu.er6)
        cpu.er12 = cpu.er0
        cpu.er0 = cpu.er2
        cpu.r0 ^= 0xFF
        cpu.r1 ^= 0xFF
        cpu.push(cpu.er0)
        cpu.push(cpu.er2)
        cpu.er4 = cpu.sp
        cpu.er6 = 0x04
        cpu.er0 = cpu.er12
        cpu.call(JOURNAL_PROGRAM_RAM)
        cpu.sp += 0x04
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.r0 = 0x4A
        cpu.r1 = 0xB6
        cpu.push(cpu.er0)
        cpu.er4 = cpu.sp
        cpu.er6 = 0x02
        cpu.er0 = cpu.er12
        cpu.er0 += 0x04
        cpu.call(JOURNAL_PROGRAM_RAM)
        cpu.sp += 0x02
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.er0 = 0x00
        cpu.branch('out')
        cpu.label('bad')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.label('out')
        cpu.pop(cpu.er6)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0x83D80)
    def journal_program():
        cpu.label('journal_program')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.xr8)
        cpu.push(cpu.er12)
        cpu.push(cpu.er14)
        cpu.sp += -16
        cpu.er8 = cpu.er0
        cpu.er10 = cpu.er4
        cpu.er12 = cpu.er6
        cpu.er14 = cpu.sp
        cpu.label('chunk')
        cpu.er12 = cpu.er12
        if cpu.eq:
            cpu.branch('done')
        cpu.er0 = cpu.er12
        cpu.er2 = 0x10
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('short')
        cpu.er6 = 0x10
        cpu.branch('copy')
        cpu.label('short')
        cpu.er6 = cpu.er12
        cpu.label('copy')
        cpu.er0 = cpu.er14
        cpu.r3 = cpu.r6
        cpu.label('copy_byte')
        cpu.r2 = cpu.mem8[0x08, cpu.er10]
        cpu.mem8[cpu.er0] = cpu.r2
        cpu.er10 += 0x01
        cpu.er0 += 0x01
        cpu.r3 += 0xFF
        if cpu.ne:
            cpu.branch('copy_byte')
        cpu.er0 = cpu.er8
        cpu.er4 = cpu.er14
        cpu.push(cpu.er6)
        cpu.call(JOURNAL_PROGRAM_RAM)
        cpu.pop(cpu.er6)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.er8 += cpu.er6
        cpu.r12 -= cpu.r6
        cpu.sub_carry(cpu.r13, cpu.r7)
        cpu.branch('chunk')
        cpu.label('done')
        cpu.er0 = 0x00
        cpu.branch('out')
        cpu.label('bad')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.label('out')
        cpu.sp += 0x10
        cpu.pop(cpu.er14)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0x83E00)
    def journal_backup():
        cpu.label('journal_backup')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.xr8)
        cpu.push(cpu.er12)
        cpu.push(cpu.er14)
        cpu.call(JOURNAL_RECOVER)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.r0 = 0x02
        cpu.call(ROM_FLASH_ERASE)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.r0 = 0x00
        cpu.r1 = 0x60
        cpu.r4 = 0x00
        cpu.r5 = 0x40
        cpu.r6 = 0xF0
        cpu.r7 = 0x1F
        cpu.call(JOURNAL_PROGRAM)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.r0 = 0x00
        cpu.r1 = 0x40
        cpu.r2 = 0x00
        cpu.r3 = 0x60
        cpu.r4 = 0xF0
        cpu.r5 = 0x1F
        cpu.call(JOURNAL_COMPARE)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.r0 = 0x00
        cpu.r1 = 0x60
        cpu.r2 = 0xF0
        cpu.r3 = 0x1F
        cpu.call(JOURNAL_CRC)
        cpu.er2 = cpu.er0
        cpu.r0 = 0xF0
        cpu.r1 = 0x7F
        cpu.call(JOURNAL_META)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.r0 = 0x00
        cpu.r1 = 0x60
        cpu.call(JOURNAL_CHECK)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.r0 = 0x01
        cpu.call(ROM_FLASH_ERASE)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.er0 = 0x00
        cpu.branch('out')
        cpu.label('bad')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.label('out')
        cpu.pop(cpu.er14)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0x83F00)
    def journal_finish():
        cpu.label('journal_finish')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.xr8)
        cpu.push(cpu.er12)
        cpu.push(cpu.er14)
        cpu.er12 = cpu.er0
        cpu.r0 = 0x00
        cpu.r1 = 0x60
        cpu.call(JOURNAL_CHECK)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.r0 = 0x00
        cpu.r1 = 0x40
        cpu.r2 = 0xF0
        cpu.r3 = 0x1F
        cpu.call(JOURNAL_CRC)
        cpu.compare(cpu.er0, cpu.er12)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er2 = cpu.er12
        cpu.r0 = 0xF0
        cpu.r1 = 0x5F
        cpu.call(JOURNAL_META)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.r0 = 0x00
        cpu.r1 = 0x40
        cpu.call(JOURNAL_CHECK)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('bad')
        cpu.er0 = 0x00
        cpu.branch('out')
        cpu.label('bad')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.label('out')
        cpu.pop(cpu.er14)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0x83F80)
    def journal_crc_update():
        cpu.label('journal_crc_update')
        cpu.r1 ^= cpu.r2
        cpu.r3 = 0x08
        cpu.label('bit')
        cpu.r2 = cpu.r1
        cpu.r2 &= 0x80
        cpu.shift_left_carry(cpu.r1, 0x01)
        cpu.r0 <<= 0x01
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('next')
        cpu.r0 ^= 0x21
        cpu.r1 ^= 0x10
        cpu.label('next')
        cpu.r3 += 0xFF
        if cpu.ne:
            cpu.branch('bit')
        cpu.ret()


    @fw.function(native=True, address=0xF6E68)
    def basic_flash():
        cpu.label('basic_flash')
        cpu.jump('replace')
        cpu.jump('write')
        cpu.label('replace')
        cpu.push(cpu.lr)
        cpu.push(cpu.er2)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.sp += -32
        cpu.er14 = cpu.sp
        cpu.mem16[cpu.offset(cpu.er14, 0x0000)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 0x0002)] = cpu.er2
        cpu.mem16[cpu.offset(cpu.er14, 0x0004)] = cpu.er4
        cpu.mem16[cpu.offset(cpu.er14, 0x0006)] = cpu.er6
        cpu.mem8[cpu.offset(cpu.er14, 0x0008)] = cpu.r8
        cpu.er0 = cpu.sp
        cpu.r2 = 0x92
        cpu.r3 = 0x83
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('near_2')
        cpu.jump('failed')
        cpu.label('near_2')
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er14, 0x0002)]
        cpu.er2 = cpu.er2
        if cpu.ne:
            cpu.branch('near_4')
        cpu.jump('near_48')
        cpu.label('near_4')
        cpu.compare(cpu.r8, 0x08)
        if cpu.ge:
            cpu.branch('near_6')
        cpu.jump('failed')
        cpu.label('near_6')
        cpu.compare(cpu.r8, 0x10)
        if cpu.lt:
            cpu.branch('near_8')
        cpu.jump('failed')
        cpu.label('near_8')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0000)]
        cpu.er2 += -1
        cpu.er0 += cpu.er2
        cpu.r2 = cpu.r8
        cpu.add_carry(cpu.r2, 0x00)
        cpu.compare(cpu.r2, 0x10)
        if cpu.lt:
            cpu.branch('near_10')
        cpu.jump('failed')
        cpu.label('near_10')
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 0x0009)] = cpu.r0
        cpu.r2 = 0x00
        cpu.call('reader')
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('near_13')
        cpu.jump('failed')
        cpu.label('near_13')
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x0000)]
        cpu.er10 = cpu.mem16[cpu.offset(cpu.er14, 0x0002)]
        cpu.r12 = cpu.mem8[cpu.offset(cpu.er14, 0x0008)]
        cpu.label('preflight')
        cpu.r2 = 0x01
        cpu.call('reader')
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('near_16')
        cpu.jump('failed')
        cpu.label('near_16')
        cpu.r4 = cpu.r0
        cpu.r2 = cpu.mem8[cpu.r12, cpu.er8]
        cpu.compare(cpu.r2, cpu.r4)
        if cpu.eq:
            cpu.branch('same')
        cpu.r0 = 0x01
        cpu.mem8[cpu.offset(cpu.er14, 0x0009)] = cpu.r0
        cpu.label('same')
        cpu.r2 &= cpu.r4
        cpu.compare(cpu.r2, cpu.r4)
        if cpu.eq:
            cpu.branch('near_19')
        cpu.jump('failed')
        cpu.label('near_19')
        cpu.er8 += 0x01
        if cpu.ne:
            cpu.branch('preflight_next')
        cpu.r12 += 0x01
        cpu.label('preflight_next')
        cpu.er10 += -1
        cpu.er10 = cpu.er10
        if cpu.eq:
            cpu.branch('near_22')
        cpu.jump('preflight')
        cpu.label('near_22')
        cpu.call('reader_end')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('near_25')
        cpu.jump('failed')
        cpu.label('near_25')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0009)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('near_27')
        cpu.jump('near_48')
        cpu.label('near_27')
        cpu.r2 = 0x00
        cpu.call('reader')
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('near_30')
        cpu.jump('failed')
        cpu.label('near_30')
        cpu.label('chunk')
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x0000)]
        cpu.er10 = cpu.mem16[cpu.offset(cpu.er14, 0x0002)]
        cpu.er12 = cpu.er14
        cpu.er12 += 0x10
        cpu.er6 = 0x00
        cpu.label('fill')
        cpu.r2 = 0x01
        cpu.call('reader')
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('near_33')
        cpu.jump('failed')
        cpu.label('near_33')
        cpu.mem8[cpu.er12] = cpu.r0
        cpu.er12 += 0x01
        cpu.er6 += 0x01
        cpu.er8 += 0x01
        cpu.er10 += -1
        cpu.er10 = cpu.er10
        if cpu.eq:
            cpu.branch('program_chunk')
        cpu.er8 = cpu.er8
        if cpu.eq:
            cpu.branch('program_chunk')
        cpu.compare(cpu.r6, 0x10)
        if cpu.lt:
            cpu.branch('fill')
        cpu.label('program_chunk')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0000)]
        cpu.r2 = cpu.mem8[cpu.offset(cpu.er14, 0x0008)]
        cpu.r3 = 0x00
        cpu.er4 = cpu.er14
        cpu.er4 += 0x10
        cpu.call('program')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('near_39')
        cpu.jump('failed')
        cpu.label('near_39')
        cpu.mem16[cpu.offset(cpu.er14, 0x0002)] = cpu.er10
        cpu.er10 = cpu.mem16[cpu.offset(cpu.er14, 0x0000)]
        cpu.mem16[cpu.offset(cpu.er14, 0x0000)] = cpu.er8
        cpu.r12 = cpu.mem8[cpu.offset(cpu.er14, 0x0008)]
        cpu.er8 = cpu.er8
        if cpu.ne:
            cpu.branch('verify')
        cpu.r0 = cpu.r12
        cpu.r0 += 0x01
        cpu.mem8[cpu.offset(cpu.er14, 0x0008)] = cpu.r0
        cpu.label('verify')
        cpu.r0 = cpu.mem8[cpu.er4]
        cpu.r2 = cpu.mem8[cpu.r12, cpu.er10]
        cpu.compare(cpu.r0, cpu.r2)
        if cpu.eq:
            cpu.branch('near_42')
        cpu.jump('failed')
        cpu.label('near_42')
        cpu.er4 += 0x01
        cpu.er10 += 0x01
        cpu.er6 += -1
        cpu.er6 = cpu.er6
        if cpu.ne:
            cpu.branch('verify')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0002)]
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('near_45')
        cpu.jump('near_30')
        cpu.label('near_45')
        cpu.call('reader_end')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('near_48')
        cpu.jump('failed')
        cpu.label('near_48')
        cpu.label('success')
        cpu.er0 = 0x00
        cpu.jump('exit')
        cpu.label('failed')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.label('exit')
        cpu.sp += 0x20
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.er2)
        cpu.pop(cpu.pc)
        cpu.label('reader')
        cpu.push(cpu.lr)
        cpu.push(cpu.er8)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0006)]
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x0004)]
        cpu.call(cpu.er8)
        cpu.pop(cpu.er8)
        cpu.pop(cpu.pc)
        cpu.label('reader_end')
        cpu.push(cpu.lr)
        cpu.r2 = 0x01
        cpu.call('reader')
        cpu.compare(cpu.r1, 0x01)
        if cpu.ne:
            cpu.branch('reader_long')
        cpu.er0 = 0x00
        cpu.pop(cpu.pc)
        cpu.label('reader_long')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.pop(cpu.pc)
        cpu.label('program')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.push(cpu.er6)
        cpu.r8 = 0x00
        cpu.push(cpu.r8)
        cpu.push(cpu.er4)
        cpu.call(ROM_FLASH_PROGRAM)
        cpu.sp += 0x06
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('write')
        cpu.push(cpu.lr)
        cpu.push(cpu.er2)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er2
        cpu.er0 = cpu.sp
        cpu.r2 = 0x12
        cpu.r3 = 0x84
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('near_53')
        cpu.jump('write_stack')
        cpu.label('near_53')
        cpu.sp += -24
        cpu.er14 = cpu.sp
        cpu.mem16[cpu.offset(cpu.er14, 0x0010)] = cpu.er4
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er8, 0x000A)]
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('near_55')
        cpu.jump('write_arg')
        cpu.label('near_55')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er8, 0x0002)]
        cpu.er2 = 0x10
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('near_57')
        cpu.jump('write_arg')
        cpu.label('near_57')
        cpu.mem16[cpu.offset(cpu.er14, 0x000E)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.er8]
        cpu.mem16[cpu.offset(cpu.er14, 0x000C)] = cpu.er0
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er8, 0x0006)]
        cpu.r0 = 0x00
        cpu.r1 = 0x01
        cpu.compare(cpu.er2, cpu.er0)
        if cpu.lt:
            cpu.branch('near_59')
        cpu.jump('write_arg')
        cpu.label('near_59')
        cpu.mem16[cpu.offset(cpu.er14, 0x0002)] = cpu.er2
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er8, 0x0004)]
        cpu.mem16[cpu.offset(cpu.er14, 0x0000)] = cpu.er0
        cpu.er4 = cpu.mem16[cpu.offset(cpu.er8, 0x0008)]
        cpu.mem16[cpu.offset(cpu.er14, 0x0004)] = cpu.er4
        cpu.call(0xFB53C)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('near_61')
        cpu.jump('write_arg')
        cpu.label('near_61')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x000C)]
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er14, 0x0004)]
        cpu.r4 = 0x02
        cpu.r5 = 0x71
        cpu.er6 = cpu.er14
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x000E)]
        cpu.call('basic_flash')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('near_63')
        cpu.jump('write_failed')
        cpu.label('near_63')
        cpu.er4 = cpu.mem16[cpu.offset(cpu.er14, 0x0010)]
        cpu.er0 = 0x00
        cpu.mem8[cpu.er4] = cpu.r0
        cpu.er4 += 0x01
        cpu.mem8[cpu.er4] = cpu.r0
        cpu.er4 += 0x01
        cpu.mem8[cpu.er4] = cpu.r0
        cpu.er4 += 0x01
        cpu.mem8[cpu.er4] = cpu.r0
        cpu.jump('write_exit')
        cpu.label('write_arg')
        cpu.er0 = 0x04
        cpu.jump('write_exit')
        cpu.label('write_failed')
        cpu.r0 = 0x00
        cpu.r1 = 0x01
        cpu.label('write_exit')
        cpu.sp += 0x18
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.er2)
        cpu.pop(cpu.pc)
        cpu.label('write_stack')
        cpu.er0 = 0x06
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.er2)
        cpu.pop(cpu.pc)
        cpu.label('ram_reader')
        cpu.push(cpu.xr4)
        cpu.er4 = cpu.er0
        cpu.compare(cpu.r2, 0x00)
        if cpu.ne:
            cpu.branch('ram_next')
        cpu.er0 = cpu.mem16[cpu.er4]
        cpu.mem16[cpu.offset(cpu.er4, 0x0006)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er4, 0x0002)]
        cpu.mem16[cpu.offset(cpu.er4, 0x0008)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er4, 0x0004)]
        cpu.mem16[cpu.offset(cpu.er4, 0x000A)] = cpu.er0
        cpu.er0 = 0x00
        cpu.jump('ram_out')
        cpu.label('ram_next')
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er4, 0x000A)]
        cpu.er2 = cpu.er2
        if cpu.eq:
            cpu.branch('ram_end')
        cpu.er6 = cpu.mem16[cpu.offset(cpu.er4, 0x0006)]
        cpu.r3 = cpu.mem8[cpu.offset(cpu.er4, 0x0008)]
        cpu.r0 = cpu.mem8[cpu.r3, cpu.er6]
        cpu.er6 += 0x01
        cpu.mem16[cpu.offset(cpu.er4, 0x0006)] = cpu.er6
        if cpu.ne:
            cpu.branch('ram_count')
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er4, 0x0008)]
        cpu.er2 += 0x01
        cpu.mem16[cpu.offset(cpu.er4, 0x0008)] = cpu.er2
        cpu.label('ram_count')
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er4, 0x000A)]
        cpu.er2 += -1
        cpu.mem16[cpu.offset(cpu.er4, 0x000A)] = cpu.er2
        cpu.r1 = 0x00
        cpu.jump('ram_out')
        cpu.label('ram_end')
        cpu.r0 = 0x00
        cpu.r1 = 0x01
        cpu.label('ram_out')
        cpu.pop(cpu.xr4)
        cpu.ret()
