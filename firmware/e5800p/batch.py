"""Fixed-layout e5800p batch routines and tables."""

from kits import cpu

JOURNAL_CRC_UPDATE = 0x83F80
JOURNAL_PROGRAM_RAM = 0x83CC0
BATCH_RELOCATE_ADDRESS = 0x81EE0
JOURNAL_BACKUP = 0x83E00
BATCH_EMIT_ADDRESS = 0x81AE0
JOURNAL_FINISH = 0x83F00
JOURNAL_RECOVER = 0x83800
CODEC_SOURCE_LENGTH_ADDRESS = 0x80444


def install(fw):
    @fw.function(native=True, address=0x81AE0)
    def batch_emit():
        cpu.label('batch_emit')
        cpu.label('emit')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.r5 = cpu.r0
        cpu.r0 = 0xF0
        cpu.r1 = 0x5F
        cpu.compare(cpu.er10, cpu.er0)
        if cpu.lt:
            cpu.branch('skip_63')
        cpu.jump('emit_bad')
        cpu.label('skip_63')
        cpu.er2 = cpu.er14
        cpu.r0 = cpu.r10
        cpu.r0 &= 0x0F
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.mem8[cpu.er2] = cpu.r5
        cpu.er2 = cpu.er14
        cpu.er2 += 0x10
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x11
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.r2 = cpu.r5
        cpu.call(JOURNAL_CRC_UPDATE)
        cpu.er2 = cpu.er14
        cpu.er2 += 0x10
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x11
        cpu.mem8[cpu.er2] = cpu.r1
        cpu.er10 += 0x01
        cpu.r0 = cpu.r10
        cpu.r0 &= 0x0F
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_64')
        cpu.jump('emit_good')
        cpu.label('skip_64')
        cpu.er0 = cpu.er10
        cpu.er0 += -16
        cpu.er4 = cpu.er14
        cpu.er6 = 0x10
        cpu.call(JOURNAL_PROGRAM_RAM)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_65')
        cpu.jump('emit_bad')
        cpu.label('skip_65')
        cpu.er4 = cpu.er14
        cpu.er6 = cpu.er10
        cpu.er6 += -16
        cpu.r3 = 0x10
        cpu.label('verify')
        cpu.r0 = cpu.mem8[0x08, cpu.er6]
        cpu.r1 = cpu.mem8[cpu.er4]
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.eq:
            cpu.branch('skip_66')
        cpu.jump('emit_bad')
        cpu.label('skip_66')
        cpu.er4 += 0x01
        cpu.er6 += 0x01
        cpu.r3 += 0xFF
        if cpu.ne:
            cpu.branch('verify')
        cpu.label('emit_good')
        cpu.er0 = 0x00
        cpu.jump('emit_exit')
        cpu.label('emit_bad')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.label('emit_exit')
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0x81EE0)
    def batch_relocate():
        cpu.label('batch_relocate')
        cpu.label('relocate')
        cpu.r6 = 0x00
        cpu.r0 = cpu.r5
        cpu.compare(cpu.r0, 0xC0)
        if cpu.ge:
            cpu.branch('skip_69')
        cpu.jump('relocate_ok')
        cpu.label('skip_69')
        cpu.compare(cpu.r0, 0xCF)
        if cpu.ge:
            cpu.branch('skip_70')
        cpu.jump('relative_target')
        cpu.label('skip_70')
        cpu.compare(cpu.r0, 0xF8)
        if cpu.eq:
            cpu.branch('skip_71')
        cpu.jump('relocate_ok')
        cpu.label('skip_71')
        cpu.r0 = cpu.r4
        cpu.r0 &= 0x0F
        cpu.compare(cpu.r0, 0x02)
        if cpu.lt:
            cpu.branch('skip_72')
        cpu.jump('relocate_ok')
        cpu.label('skip_72')
        cpu.r6 = 0x02
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1E
        cpu.r7 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er8
        cpu.compare(cpu.r7, 0x00)
        if cpu.eq:
            cpu.branch('skip_73')
        cpu.jump('far_source')
        cpu.label('skip_73')
        cpu.r3 += 0xE0
        cpu.label('far_source')
        cpu.er2 += 0x02
        cpu.r4 = cpu.mem8[0x08, cpu.er2]
        cpu.er2 += 0x01
        cpu.r5 = cpu.mem8[0x08, cpu.er2]
        cpu.r5 += 0x20
        cpu.r0 = cpu.r4
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_74')
        cpu.jump('relocate_bad')
        cpu.label('skip_74')
        cpu.jump('target_check')
        cpu.label('relative_target')
        cpu.r6 = 0x01
        cpu.r0 = cpu.r4
        cpu.r5 = 0x00
        cpu.r0 &= 0x80
        if cpu.ne:
            cpu.branch('skip_75')
        cpu.jump('relative_sign')
        cpu.label('skip_75')
        cpu.r5 = 0xFF
        cpu.label('relative_sign')
        cpu.er4 += cpu.er4
        cpu.er0 = cpu.er8
        cpu.er0 += 0x02
        cpu.er4 += cpu.er0
        cpu.label('target_check')
        cpu.er0 = cpu.er4
        cpu.r2 = 0x00
        cpu.r3 = 0x60
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_76')
        cpu.jump('skip_82')
        cpu.label('skip_76')
        cpu.r2 = 0xF0
        cpu.r3 = 0x7F
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('skip_77')
        cpu.jump('skip_82')
        cpu.label('skip_77')
        cpu.er0 = cpu.er12
        cpu.compare(cpu.er4, cpu.er0)
        if cpu.ge:
            cpu.branch('skip_78')
        cpu.jump('skip_82')
        cpu.label('skip_78')
        if cpu.ne:
            cpu.branch('skip_79')
        cpu.jump('skip_82')
        cpu.label('skip_79')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x16
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.compare(cpu.er4, cpu.er0)
        if cpu.ge:
            cpu.branch('skip_80')
        cpu.jump('relocate_bad')
        cpu.label('skip_80')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x18
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.r0 = cpu.r2
        cpu.r0 &= 0x80
        if cpu.ne:
            cpu.branch('skip_81')
        cpu.jump('target_delta')
        cpu.label('skip_81')
        cpu.r3 = 0xFF
        cpu.label('target_delta')
        cpu.er4 += cpu.er2
        cpu.er0 = cpu.er4
        cpu.r2 = 0xF0
        cpu.r3 = 0x7F
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('skip_82')
        cpu.jump('relocate_bad')
        cpu.label('skip_82')
        cpu.label('target_ready')
        cpu.compare(cpu.r6, 0x02)
        if cpu.eq:
            cpu.branch('skip_83')
        cpu.jump('relative_finish')
        cpu.label('skip_83')
        cpu.r5 += 0xE0
        cpu.jump('relocate_ok')
        cpu.label('relative_finish')
        cpu.er0 = cpu.er12
        cpu.er2 = cpu.er14
        cpu.er2 += 0x16
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.compare(cpu.er8, cpu.er0)
        if cpu.ge:
            cpu.branch('skip_84')
        cpu.jump('source_ready_rel')
        cpu.label('skip_84')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x18
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.r0 = cpu.r2
        cpu.r0 &= 0x80
        if cpu.ne:
            cpu.branch('skip_85')
        cpu.jump('source_delta')
        cpu.label('skip_85')
        cpu.r3 = 0xFF
        cpu.label('source_delta')
        cpu.er0 = cpu.er8
        cpu.er0 += cpu.er2
        cpu.jump('source_done_rel')
        cpu.label('source_ready_rel')
        cpu.er0 = cpu.er8
        cpu.label('source_done_rel')
        cpu.er0 += 0x02
        cpu.r4 -= cpu.r0
        cpu.sub_carry(cpu.r5, cpu.r1)
        cpu.r0 = cpu.r4
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_86')
        cpu.jump('relocate_bad')
        cpu.label('skip_86')
        cpu.compare(cpu.r5, 0x00)
        if cpu.ne:
            cpu.branch('skip_87')
        cpu.jump('relative_low')
        cpu.label('skip_87')
        cpu.compare(cpu.r5, 0xFF)
        if cpu.eq:
            cpu.branch('skip_88')
        cpu.jump('relocate_bad')
        cpu.label('skip_88')
        cpu.r4 >>= 0x01
        cpu.r4 |= 0x80
        cpu.jump('relocate_ok')
        cpu.label('relative_low')
        cpu.r4 >>= 0x01
        cpu.label('relocate_ok')
        cpu.er0 = 0x00
        cpu.ret()
        cpu.label('relocate_bad')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.ret()


    @fw.function(native=True, address=0xFF900)
    def batch():
        cpu.label('batch')
        cpu.push(cpu.lr)
        cpu.push(cpu.er2)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.push(cpu.er14)
        cpu.sp += -32
        cpu.er14 = cpu.sp
        cpu.er8 = cpu.er2
        cpu.er12 = cpu.er8
        cpu.r0 = 0x00
        cpu.r1 = 0x20
        cpu.er12 += cpu.er0
        cpu.er0 = cpu.er6
        cpu.er2 = cpu.er14
        cpu.er2 += 0x12
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x13
        cpu.mem8[cpu.er2] = cpu.r1
        cpu.er0 = cpu.er12
        cpu.er2 = cpu.er14
        cpu.er2 += 0x14
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x15
        cpu.mem8[cpu.er2] = cpu.r1
        cpu.er2 = cpu.er6
        cpu.er2 += 0x01
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x02)
        if cpu.ge:
            cpu.branch('skip_1')
        cpu.jump('invalid')
        cpu.label('skip_1')
        cpu.compare(cpu.r0, 0x41)
        if cpu.lt:
            cpu.branch('skip_2')
        cpu.jump('invalid')
        cpu.label('skip_2')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x17
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_3')
        cpu.jump('invalid')
        cpu.label('skip_3')
        cpu.er2 = cpu.er6
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x02)
        if cpu.ge:
            cpu.branch('skip_4')
        cpu.jump('invalid')
        cpu.label('skip_4')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x16
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_5')
        cpu.jump('invalid')
        cpu.label('skip_5')
        cpu.er0 = cpu.er12
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_6')
        cpu.jump('invalid')
        cpu.label('skip_6')
        cpu.er0 = cpu.er12
        cpu.r1 += 0xE0
        cpu.r2 = 0x00
        cpu.r3 = 0x40
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_7')
        cpu.jump('invalid')
        cpu.label('skip_7')
        cpu.r2 = 0xF0
        cpu.r3 = 0x5F
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('skip_8')
        cpu.jump('invalid')
        cpu.label('skip_8')
        cpu.er10 = cpu.er0
        cpu.r8 = 0x00
        cpu.r9 = 0x40
        cpu.label('boundary')
        cpu.compare(cpu.er8, cpu.er10)
        if cpu.ne:
            cpu.branch('skip_9')
        cpu.jump('boundary_ready')
        cpu.label('skip_9')
        if cpu.lt:
            cpu.branch('skip_10')
        cpu.jump('invalid')
        cpu.label('skip_10')
        cpu.call('s1_length')
        cpu.compare(cpu.r7, 0xFF)
        if cpu.ne:
            cpu.branch('skip_11')
        cpu.jump('invalid')
        cpu.label('skip_11')
        cpu.r2 = cpu.r7
        cpu.r3 = 0x00
        cpu.er8 += cpu.er2
        cpu.jump('boundary')
        cpu.label('boundary_ready')
        cpu.call('s1_length')
        cpu.compare(cpu.r7, 0xFF)
        if cpu.ne:
            cpu.branch('skip_12')
        cpu.jump('invalid')
        cpu.label('skip_12')
        cpu.er0 = cpu.er8
        cpu.er2 = cpu.er14
        cpu.er2 += 0x16
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.r2 = 0xF0
        cpu.r3 = 0x5F
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_13')
        cpu.jump('skip_14')
        cpu.label('skip_13')
        if cpu.eq:
            cpu.branch('skip_14')
        cpu.jump('invalid')
        cpu.label('skip_14')
        cpu.label('old_inside')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x16
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r2 = cpu.r0
        cpu.r3 = 0x00
        cpu.er10 = cpu.er8
        cpu.er10 += cpu.er2
        cpu.label('old_span')
        cpu.compare(cpu.er8, cpu.er10)
        if cpu.ne:
            cpu.branch('skip_15')
        cpu.jump('old_ready')
        cpu.label('skip_15')
        if cpu.lt:
            cpu.branch('skip_16')
        cpu.jump('invalid')
        cpu.label('skip_16')
        cpu.call('s1_length')
        cpu.compare(cpu.r7, 0xFF)
        if cpu.ne:
            cpu.branch('skip_17')
        cpu.jump('invalid')
        cpu.label('skip_17')
        cpu.r2 = cpu.r7
        cpu.r3 = 0x00
        cpu.er8 += cpu.er2
        cpu.jump('old_span')
        cpu.label('old_ready')
        cpu.er8 = cpu.er12
        cpu.r9 += 0xE0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x17
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x16
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r0 -= cpu.r2
        cpu.er2 = cpu.er14
        cpu.er2 += 0x18
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er0 = cpu.er8
        cpu.er2 = cpu.er14
        cpu.er2 += 0x16
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.r2 = 0xF0
        cpu.r3 = 0x5F
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_18')
        cpu.jump('skip_19')
        cpu.label('skip_18')
        if cpu.eq:
            cpu.branch('skip_19')
        cpu.jump('invalid')
        cpu.label('skip_19')
        cpu.label('span_valid')
        cpu.r0 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1F
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.label('staged_loop')
        cpu.call('staged_length')
        cpu.compare(cpu.r7, 0xFF)
        if cpu.ne:
            cpu.branch('skip_20')
        cpu.jump('invalid')
        cpu.label('skip_20')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x19
        cpu.mem8[cpu.er2] = cpu.r7
        cpu.label('staged_opcode')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x19
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x04)
        if cpu.eq:
            cpu.branch('skip_21')
        cpu.jump('skip_24')
        cpu.label('skip_21')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1F
        cpu.r7 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x12
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x13
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.r0 = cpu.r7
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.er2 += 0x03
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 &= 0xF0
        cpu.compare(cpu.r0, 0xF0)
        if cpu.eq:
            cpu.branch('skip_22')
        cpu.jump('skip_24')
        cpu.label('skip_22')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1F
        cpu.r7 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x12
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x13
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.r0 = cpu.r7
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.er2 += 0x02
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 &= 0x0F
        cpu.compare(cpu.r0, 0x02)
        if cpu.lt:
            cpu.branch('skip_23')
        cpu.jump('skip_24')
        cpu.label('skip_23')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1F
        cpu.r7 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x12
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x13
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.r0 = cpu.r7
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.er2 += 0x05
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_24')
        cpu.jump('invalid')
        cpu.label('skip_24')
        cpu.label('staged_ready')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1F
        cpu.r7 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x12
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x13
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.r0 = cpu.r7
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.er2 += 0x03
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r1, 0xC0)
        if cpu.ge:
            cpu.branch('skip_25')
        cpu.jump('skip_29')
        cpu.label('skip_25')
        cpu.compare(cpu.r1, 0xCF)
        if cpu.lt:
            cpu.branch('skip_26')
        cpu.jump('skip_29')
        cpu.label('skip_26')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1F
        cpu.r7 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x12
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x13
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.r0 = cpu.r7
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.er2 += 0x02
        cpu.r4 = cpu.mem8[cpu.er2]
        cpu.r0 = cpu.r4
        cpu.r5 = 0x00
        cpu.r0 &= 0x80
        if cpu.ne:
            cpu.branch('skip_27')
        cpu.jump('staged_sign')
        cpu.label('skip_27')
        cpu.r5 = 0xFF
        cpu.label('staged_sign')
        cpu.er4 += cpu.er4
        cpu.er0 = cpu.er12
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1F
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.er0 += 0x02
        cpu.er4 += cpu.er0
        cpu.r2 = 0x00
        cpu.r3 = 0x60
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_28')
        cpu.jump('invalid')
        cpu.label('skip_28')
        cpu.r2 = 0xF0
        cpu.r3 = 0x7F
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('skip_29')
        cpu.jump('invalid')
        cpu.label('skip_29')
        cpu.label('staged_branch_ready')
        cpu.label('staged_step')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1F
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x19
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.r0 += cpu.r1
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1F
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x17
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.ge:
            cpu.branch('skip_30')
        cpu.jump('staged_loop')
        cpu.label('skip_30')
        if cpu.eq:
            cpu.branch('skip_31')
        cpu.jump('invalid')
        cpu.label('skip_31')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x18
        cpu.r3 = cpu.mem8[cpu.er2]
        cpu.r0 = cpu.r3
        cpu.r0 &= 0x80
        if cpu.eq:
            cpu.branch('skip_32')
        cpu.jump('no_growth')
        cpu.label('skip_32')
        cpu.compare(cpu.r3, 0x00)
        if cpu.ne:
            cpu.branch('skip_33')
        cpu.jump('no_growth')
        cpu.label('skip_33')
        cpu.r8 = 0xF0
        cpu.r9 = 0x5F
        cpu.r2 = cpu.r3
        cpu.r3 = 0x00
        cpu.r8 -= cpu.r2
        cpu.sub_carry(cpu.r9, cpu.r3)
        cpu.er2 = cpu.er14
        cpu.er2 += 0x18
        cpu.r3 = cpu.mem8[cpu.er2]
        cpu.label('tail')
        cpu.r0 = cpu.mem8[0x08, cpu.er8]
        cpu.compare(cpu.r0, 0xFF)
        if cpu.eq:
            cpu.branch('skip_34')
        cpu.jump('invalid')
        cpu.label('skip_34')
        cpu.er8 += 0x01
        cpu.r3 += 0xFF
        if cpu.ne:
            cpu.branch('tail')
        cpu.label('no_growth')
        cpu.r8 = 0xF0
        cpu.r9 = 0x7F
        cpu.er2 = cpu.er14
        cpu.er2 += 0x18
        cpu.r3 = cpu.mem8[cpu.er2]
        cpu.r0 = cpu.r3
        cpu.r0 &= 0x80
        if cpu.eq:
            cpu.branch('skip_35')
        cpu.jump('limit_ready')
        cpu.label('skip_35')
        cpu.compare(cpu.r3, 0x00)
        if cpu.ne:
            cpu.branch('skip_36')
        cpu.jump('limit_ready')
        cpu.label('skip_36')
        cpu.r2 = cpu.r3
        cpu.r3 = 0x00
        cpu.r8 -= cpu.r2
        cpu.sub_carry(cpu.r9, cpu.r3)
        cpu.label('limit_ready')
        cpu.er0 = cpu.er8
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1A
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1B
        cpu.mem8[cpu.er2] = cpu.r1
        cpu.er0 = cpu.er12
        cpu.er2 = cpu.er14
        cpu.er2 += 0x16
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.er4 = cpu.er0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1A
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1B
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.er4, cpu.er0)
        if cpu.ge:
            cpu.branch('skip_37')
        cpu.jump('skip_38')
        cpu.label('skip_37')
        if cpu.eq:
            cpu.branch('skip_38')
        cpu.jump('invalid')
        cpu.label('skip_38')
        cpu.label('source_ready')
        cpu.r0 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1E
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r8 = 0x00
        cpu.r9 = 0x60
        cpu.label('preflight')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1A
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1B
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.er8, cpu.er0)
        if cpu.lt:
            cpu.branch('skip_39')
        cpu.jump('preflight_done')
        cpu.label('skip_39')
        cpu.compare(cpu.er8, cpu.er12)
        if cpu.ne:
            cpu.branch('skip_40')
        cpu.jump('preflight_skip')
        cpu.label('skip_40')
        cpu.er2 = cpu.er8
        cpu.r3 += 0xE0
        cpu.r0 = cpu.mem8[0x08, cpu.er2]
        cpu.r4 = cpu.r0
        cpu.er2 += 0x01
        cpu.r1 = cpu.mem8[0x08, cpu.er2]
        cpu.r5 = cpu.r1
        cpu.call('preflight_length')
        cpu.compare(cpu.r7, 0xFF)
        if cpu.ne:
            cpu.branch('skip_41')
        cpu.jump('invalid')
        cpu.label('skip_41')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x19
        cpu.mem8[cpu.er2] = cpu.r7
        cpu.call('source_span')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_42')
        cpu.jump('invalid')
        cpu.label('skip_42')
        cpu.call(BATCH_RELOCATE_ADDRESS)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_43')
        cpu.jump('invalid')
        cpu.label('skip_43')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x19
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.er8 += cpu.er2
        cpu.jump('preflight')
        cpu.label('preflight_skip')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x16
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.er8 += cpu.er2
        cpu.jump('preflight')
        cpu.label('preflight_done')
        cpu.r0 = 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1E
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.call(JOURNAL_BACKUP)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_44')
        cpu.jump('recover')
        cpu.label('skip_44')
        cpu.r8 = 0x00
        cpu.r9 = 0x60
        cpu.r10 = 0x00
        cpu.r11 = 0x40
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.er2 = cpu.er14
        cpu.er2 += 0x10
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x11
        cpu.mem8[cpu.er2] = cpu.r1
        cpu.label('instruction')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1A
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1B
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.er8, cpu.er0)
        if cpu.lt:
            cpu.branch('skip_45')
        cpu.jump('padding')
        cpu.label('skip_45')
        cpu.compare(cpu.er8, cpu.er12)
        if cpu.eq:
            cpu.branch('skip_46')
        cpu.jump('ordinary')
        cpu.label('skip_46')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x12
        cpu.r4 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x13
        cpu.r5 = cpu.mem8[cpu.er2]
        cpu.er4 += 0x02
        cpu.er2 = cpu.er14
        cpu.er2 += 0x17
        cpu.r7 = cpu.mem8[cpu.er2]
        cpu.label('replacement')
        cpu.r0 = cpu.mem8[cpu.er4]
        cpu.er4 += 0x01
        cpu.call(BATCH_EMIT_ADDRESS)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_47')
        cpu.jump('recover')
        cpu.label('skip_47')
        cpu.r7 += 0xFF
        if cpu.ne:
            cpu.branch('replacement')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x16
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r1 = 0x00
        cpu.er8 += cpu.er0
        cpu.jump('instruction')
        cpu.label('ordinary')
        cpu.r0 = cpu.mem8[0x08, cpu.er8]
        cpu.r4 = cpu.r0
        cpu.er2 = cpu.er8
        cpu.er2 += 0x01
        cpu.r1 = cpu.mem8[0x08, cpu.er2]
        cpu.r5 = cpu.r1
        cpu.call('backup_length')
        cpu.compare(cpu.r7, 0xFF)
        if cpu.ne:
            cpu.branch('skip_48')
        cpu.jump('recover')
        cpu.label('skip_48')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x19
        cpu.mem8[cpu.er2] = cpu.r7
        cpu.call('source_span')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_49')
        cpu.jump('recover')
        cpu.label('skip_49')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1C
        cpu.mem8[cpu.er2] = cpu.r4
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1D
        cpu.mem8[cpu.er2] = cpu.r5
        cpu.call(BATCH_RELOCATE_ADDRESS)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_50')
        cpu.jump('recover')
        cpu.label('skip_50')
        cpu.compare(cpu.r6, 0x00)
        if cpu.ne:
            cpu.branch('skip_51')
        cpu.jump('plain')
        cpu.label('skip_51')
        cpu.compare(cpu.r6, 0x01)
        if cpu.eq:
            cpu.branch('skip_52')
        cpu.jump('far_instruction')
        cpu.label('skip_52')
        cpu.r0 = cpu.r4
        cpu.call(BATCH_EMIT_ADDRESS)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_53')
        cpu.jump('recover')
        cpu.label('skip_53')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1D
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.call(BATCH_EMIT_ADDRESS)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_54')
        cpu.jump('recover')
        cpu.label('skip_54')
        cpu.er8 += 0x02
        cpu.jump('instruction')
        cpu.label('far_instruction')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1C
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.call(BATCH_EMIT_ADDRESS)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_55')
        cpu.jump('recover')
        cpu.label('skip_55')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1D
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.call(BATCH_EMIT_ADDRESS)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_56')
        cpu.jump('recover')
        cpu.label('skip_56')
        cpu.r0 = cpu.r4
        cpu.call(BATCH_EMIT_ADDRESS)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_57')
        cpu.jump('recover')
        cpu.label('skip_57')
        cpu.r0 = cpu.r5
        cpu.call(BATCH_EMIT_ADDRESS)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_58')
        cpu.jump('recover')
        cpu.label('skip_58')
        cpu.er8 += 0x04
        cpu.jump('instruction')
        cpu.label('plain')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x19
        cpu.r7 = cpu.mem8[cpu.er2]
        cpu.label('plain_byte')
        cpu.r0 = cpu.mem8[0x08, cpu.er8]
        cpu.er8 += 0x01
        cpu.call(BATCH_EMIT_ADDRESS)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_59')
        cpu.jump('recover')
        cpu.label('skip_59')
        cpu.r7 += 0xFF
        if cpu.ne:
            cpu.branch('plain_byte')
        cpu.jump('instruction')
        cpu.label('padding')
        cpu.r0 = 0xF0
        cpu.r1 = 0x5F
        cpu.compare(cpu.er10, cpu.er0)
        if cpu.ne:
            cpu.branch('skip_60')
        cpu.jump('finish')
        cpu.label('skip_60')
        cpu.r0 = 0xFF
        cpu.call(BATCH_EMIT_ADDRESS)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_61')
        cpu.jump('recover')
        cpu.label('skip_61')
        cpu.jump('padding')
        cpu.label('finish')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x10
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x11
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.call(JOURNAL_FINISH)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_62')
        cpu.jump('recover')
        cpu.label('skip_62')
        cpu.jump('success')
        cpu.label('recover')
        cpu.call(JOURNAL_RECOVER)
        cpu.label('invalid')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.jump('exit')
        cpu.label('success')
        cpu.er0 = 0x00
        cpu.label('exit')
        cpu.sp = cpu.er14
        cpu.sp += 0x20
        cpu.pop(cpu.er14)
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.er2)
        cpu.pop(cpu.pc)
        cpu.label('source_span')
        cpu.er0 = cpu.er8
        cpu.er2 = cpu.er14
        cpu.er2 += 0x19
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.er6 = cpu.er0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1A
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1B
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.er6, cpu.er0)
        if cpu.ge:
            cpu.branch('skip_67')
        cpu.jump('skip_68')
        cpu.label('skip_67')
        if cpu.eq:
            cpu.branch('skip_68')
        cpu.jump('span_bad')
        cpu.label('skip_68')
        cpu.label('span_ok')
        cpu.er0 = 0x00
        cpu.ret()
        cpu.label('span_bad')
        cpu.r0 = 0xFF
        cpu.r1 = 0xFF
        cpu.ret()
        cpu.label('s1_length')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.er0 = cpu.er8
        cpu.r4 = 0xF0
        cpu.r5 = 0x5F
        cpu.jump('source_length')
        cpu.label('preflight_length')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.er0 = cpu.er8
        cpu.r1 += 0xE0
        cpu.r4 = 0xF0
        cpu.r5 = 0x5F
        cpu.jump('source_length')
        cpu.label('backup_length')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.er0 = cpu.er8
        cpu.r4 = 0xF0
        cpu.r5 = 0x7F
        cpu.label('source_length')
        cpu.r2 = 0x08
        cpu.jump('probe_length')
        cpu.label('staged_length')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.er2 = cpu.er14
        cpu.er2 += 0x12
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x13
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er0 += 0x02
        cpu.er4 = cpu.er0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x17
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.er4 += cpu.er2
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1F
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.r2 = 0x00
        cpu.label('probe_length')
        cpu.call(CODEC_SOURCE_LENGTH_ADDRESS)
        cpu.r3 = cpu.r0
        cpu.pop(cpu.xr4)
        cpu.r7 = cpu.r3
        cpu.pop(cpu.pc)
