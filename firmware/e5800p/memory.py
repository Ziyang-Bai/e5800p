"""Fixed-layout e5800p memory routines and tables."""

from kits import cpu

CALL_BRIDGE_ADDRESS = 0x80400


def install(fw):
    @fw.function(native=True, address=0x80400)
    def call_bridge():
        cpu.label('call_bridge')
        cpu.push(cpu.er10)
        cpu.push(cpu.er8)
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0xFB530)
    def basic_memory():
        cpu.label('basic_memory')
        cpu.jump('dispatch')
        cpu.jump('to_integer')
        cpu.jump('to_number')
        cpu.jump('read_range')
        cpu.label('read_range')
        cpu.push(cpu.er4)
        cpu.er4 = cpu.er4
        if cpu.eq:
            cpu.branch('range_ok')
        cpu.er4 += -1
        cpu.er0 += cpu.er4
        cpu.add_carry(cpu.r2, 0x00)
        if cpu.lt:
            cpu.branch('range_bad')
        cpu.label('range_ok')
        cpu.er0 = 0x00
        cpu.branch('range_out')
        cpu.label('range_bad')
        cpu.er0 = 0x04
        cpu.label('range_out')
        cpu.pop(cpu.er4)
        cpu.ret()
        cpu.label('dispatch')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.r6 = cpu.psw
        cpu.push(cpu.ea)
        cpu.push(cpu.er6)
        cpu.er8 = cpu.er2
        cpu.er12 = cpu.er4
        cpu.r10 = cpu.r0
        cpu.er0 = cpu.sp
        cpu.r2 = 0x92
        cpu.r3 = 0x83
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_1')
        cpu.jump('entry_memory')
        cpu.label('skip_1')
        cpu.sp += -8
        cpu.er14 = cpu.sp
        cpu.compare(cpu.r10, 0x00)
        if cpu.ne:
            cpu.branch('skip_2')
        cpu.jump('peek')
        cpu.label('skip_2')
        cpu.compare(cpu.r10, 0x01)
        if cpu.ne:
            cpu.branch('skip_3')
        cpu.jump('peek')
        cpu.label('skip_3')
        cpu.compare(cpu.r10, 0x02)
        if cpu.ne:
            cpu.branch('skip_4')
        cpu.jump('poke')
        cpu.label('skip_4')
        cpu.compare(cpu.r10, 0x03)
        if cpu.ne:
            cpu.branch('skip_5')
        cpu.jump('poke')
        cpu.label('skip_5')
        cpu.compare(cpu.r10, 0x04)
        if cpu.ne:
            cpu.branch('skip_6')
        cpu.jump('call')
        cpu.label('skip_6')
        cpu.compare(cpu.r10, 0x05)
        if cpu.ne:
            cpu.branch('skip_7')
        cpu.jump('bit_and')
        cpu.label('skip_7')
        cpu.compare(cpu.r10, 0x06)
        if cpu.ne:
            cpu.branch('skip_8')
        cpu.jump('bit_or')
        cpu.label('skip_8')
        cpu.compare(cpu.r10, 0x07)
        if cpu.ne:
            cpu.branch('skip_9')
        cpu.jump('bit_xor')
        cpu.label('skip_9')
        cpu.compare(cpu.r10, 0x08)
        if cpu.ne:
            cpu.branch('skip_10')
        cpu.jump('shift_left')
        cpu.label('skip_10')
        cpu.compare(cpu.r10, 0x09)
        if cpu.ne:
            cpu.branch('skip_11')
        cpu.jump('shift_right')
        cpu.label('skip_11')
        cpu.compare(cpu.r10, 0x0A)
        if cpu.ne:
            cpu.branch('skip_12')
        cpu.jump('inkey')
        cpu.label('skip_12')
        cpu.compare(cpu.r10, 0x0B)
        if cpu.ne:
            cpu.branch('skip_13')
        cpu.jump('ticks')
        cpu.label('skip_13')
        cpu.compare(cpu.r10, 0x0D)
        if cpu.ne:
            cpu.branch('skip_14')
        cpu.jump('copy')
        cpu.label('skip_14')
        cpu.compare(cpu.r10, 0x0E)
        if cpu.ne:
            cpu.branch('skip_15')
        cpu.jump('fill')
        cpu.label('skip_15')
        cpu.jump('argument')
        cpu.label('peek')
        cpu.r11 = cpu.r10
        cpu.r11 &= 0x01
        cpu.r11 += 0x01
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0002)]
        cpu.r4 = 0x00
        cpu.r4 = cpu.r11
        cpu.r5 = 0x00
        cpu.call('read_range')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('skip_16')
        cpu.jump('argument')
        cpu.label('skip_16')
        cpu.er4 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.er6 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0002)]
        cpu.er0 = 0x00
        cpu.r0 = cpu.mem8[cpu.r6, cpu.er4]
        cpu.compare(cpu.r11, 0x01)
        if cpu.eq:
            cpu.branch('peek_done')
        cpu.er4 += 0x01
        cpu.add_carry(cpu.r6, 0x00)
        cpu.r1 = cpu.mem8[cpu.r6, cpu.er4]
        cpu.label('peek_done')
        cpu.jump('word_result')
        cpu.label('poke')
        cpu.r11 = cpu.r10
        cpu.r11 &= 0x01
        cpu.r11 += 0x01
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0002)]
        cpu.r4 = 0x00
        cpu.r4 = cpu.r11
        cpu.r5 = 0x00
        cpu.call('read_range')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('skip_17')
        cpu.jump('argument')
        cpu.label('skip_17')
        cpu.er4 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.er6 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0002)]
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0004)]
        cpu.mem8[cpu.r6, cpu.er4] = cpu.r0
        cpu.compare(cpu.r11, 0x01)
        if cpu.eq:
            cpu.branch('poke_done')
        cpu.er4 += 0x01
        cpu.add_carry(cpu.r6, 0x00)
        cpu.mem8[cpu.r6, cpu.er4] = cpu.r1
        cpu.label('poke_done')
        cpu.jump('zero')
        cpu.label('copy')
        cpu.er10 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0008)]
        cpu.er10 = cpu.er10
        if cpu.ne:
            cpu.branch('skip_18')
        cpu.jump('zero')
        cpu.label('skip_18')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0004)]
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0006)]
        cpu.er4 = cpu.er10
        cpu.call('read_range')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('skip_19')
        cpu.jump('argument')
        cpu.label('skip_19')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0002)]
        cpu.call('read_range')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('skip_20')
        cpu.jump('argument')
        cpu.label('skip_20')
        cpu.er4 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.er6 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0002)]
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0004)]
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0006)]
        cpu.r7 = cpu.r2
        cpu.er8 = cpu.er0
        cpu.r3 = 0x00
        cpu.compare(cpu.r6, cpu.r7)
        if cpu.lt:
            cpu.branch('copy_loop')
        if cpu.ne:
            cpu.branch('copy_reverse')
        cpu.compare(cpu.er4, cpu.er8)
        if cpu.lt:
            cpu.branch('copy_loop')
        cpu.label('copy_reverse')
        cpu.er10 += -1
        cpu.er4 += cpu.er10
        cpu.add_carry(cpu.r6, 0x00)
        cpu.er8 += cpu.er10
        cpu.add_carry(cpu.r7, 0x00)
        cpu.er10 += 0x01
        cpu.r3 = 0x01
        cpu.label('copy_loop')
        cpu.r0 = cpu.mem8[cpu.r7, cpu.er8]
        cpu.mem8[cpu.r6, cpu.er4] = cpu.r0
        cpu.er10 += -1
        if cpu.ne:
            cpu.branch('skip_21')
        cpu.jump('zero')
        cpu.label('skip_21')
        cpu.compare(cpu.r3, 0x00)
        if cpu.ne:
            cpu.branch('copy_back')
        cpu.er4 += 0x01
        cpu.add_carry(cpu.r6, 0x00)
        cpu.er8 += 0x01
        cpu.add_carry(cpu.r7, 0x00)
        cpu.branch('copy_loop')
        cpu.label('copy_back')
        cpu.er4 += -1
        cpu.add_carry(cpu.r6, 0xFF)
        cpu.er8 += -1
        cpu.add_carry(cpu.r7, 0xFF)
        cpu.branch('copy_loop')
        cpu.label('fill')
        cpu.er10 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0004)]
        cpu.er10 = cpu.er10
        if cpu.ne:
            cpu.branch('skip_22')
        cpu.jump('zero')
        cpu.label('skip_22')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0002)]
        cpu.er4 = cpu.er10
        cpu.call('read_range')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('skip_23')
        cpu.jump('argument')
        cpu.label('skip_23')
        cpu.er4 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.er6 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0002)]
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0008)]
        cpu.label('fill_loop')
        cpu.mem8[cpu.r6, cpu.er4] = cpu.r0
        cpu.er4 += 0x01
        cpu.add_carry(cpu.r6, 0x00)
        cpu.er10 += -1
        if cpu.ne:
            cpu.branch('fill_loop')
        cpu.jump('zero')
        cpu.label('bit_and')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0004)]
        cpu.r0 &= cpu.r2
        cpu.r1 &= cpu.r3
        cpu.jump('word_result')
        cpu.label('bit_or')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0004)]
        cpu.r0 |= cpu.r2
        cpu.r1 |= cpu.r3
        cpu.jump('word_result')
        cpu.label('bit_xor')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0004)]
        cpu.r0 ^= cpu.r2
        cpu.r1 ^= cpu.r3
        cpu.jump('word_result')
        cpu.label('shift_left')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0004)]
        cpu.compare(cpu.r3, 0x00)
        if cpu.eq:
            cpu.branch('skip_24')
        cpu.jump('argument')
        cpu.label('skip_24')
        cpu.compare(cpu.r2, 0x10)
        if cpu.lt:
            cpu.branch('skip_25')
        cpu.jump('argument')
        cpu.label('skip_25')
        cpu.compare(cpu.r2, 0x00)
        if cpu.ne:
            cpu.branch('skip_26')
        cpu.jump('word_result')
        cpu.label('skip_26')
        cpu.label('shift_left_loop')
        cpu.shift_left_carry(cpu.r1, 0x01)
        cpu.r0 <<= 0x01
        cpu.r2 += 0xFF
        if cpu.ne:
            cpu.branch('skip_26')
        cpu.jump('word_result')
        cpu.label('shift_right')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0004)]
        cpu.compare(cpu.r3, 0x00)
        if cpu.eq:
            cpu.branch('skip_27')
        cpu.jump('argument')
        cpu.label('skip_27')
        cpu.compare(cpu.r2, 0x10)
        if cpu.lt:
            cpu.branch('skip_28')
        cpu.jump('argument')
        cpu.label('skip_28')
        cpu.compare(cpu.r2, 0x00)
        if cpu.ne:
            cpu.branch('skip_29')
        cpu.jump('word_result')
        cpu.label('skip_29')
        cpu.label('shift_right_loop')
        cpu.shift_right_carry(cpu.r0, 0x01)
        cpu.r1 >>= 0x01
        cpu.r2 += 0xFF
        if cpu.ne:
            cpu.branch('skip_29')
        cpu.jump('word_result')
        cpu.label('ticks')
        cpu.er0 = 0x00
        cpu.r0 = cpu.mem8[0x00, 0xF00C]
        cpu.jump('word_result')
        cpu.label('inkey')
        cpu.er0 = 0x00
        cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0000)] = cpu.er0
        cpu.r0 = cpu.psw
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0002)] = cpu.r0
        cpu.r0 &= 0xF7
        cpu.psw = cpu.r0
        cpu.r0 = cpu.mem8[0x00, 0xF044]
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0003)] = cpu.r0
        cpu.er0 = cpu.er14
        cpu.call(0x12864)
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0003)]
        cpu.mem8[0x00, 0xF044] = cpu.r0
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0002)]
        cpu.psw = cpu.r0
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0000)]
        cpu.er0 = 0x00
        cpu.compare(cpu.r2, 0x00)
        if cpu.ne:
            cpu.branch('skip_30')
        cpu.jump('word_result')
        cpu.label('skip_30')
        cpu.r0 = 0x01
        cpu.label('key_column')
        cpu.r4 = cpu.r3
        cpu.r4 &= 0x01
        if cpu.ne:
            cpu.branch('key_row')
        cpu.r3 >>= 0x01
        cpu.r0 += 0x10
        cpu.branch('key_column')
        cpu.label('key_row')
        cpu.r4 = cpu.r2
        cpu.r4 &= 0x01
        if cpu.eq:
            cpu.branch('skip_31')
        cpu.jump('word_result')
        cpu.label('skip_31')
        cpu.r2 >>= 0x01
        cpu.r0 += 0x01
        cpu.branch('key_row')
        cpu.label('call')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0002)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_32')
        cpu.jump('argument')
        cpu.label('skip_32')
        cpu.compare(cpu.r0, 0x10)
        if cpu.lt:
            cpu.branch('skip_33')
        cpu.jump('argument')
        cpu.label('skip_33')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.r2 = cpu.r0
        cpu.r2 &= 0x01
        if cpu.eq:
            cpu.branch('skip_34')
        cpu.jump('argument')
        cpu.label('skip_34')
        cpu.push(cpu.qr0)
        cpu.push(cpu.qr8)
        cpu.sp += -120
        cpu.er2 = cpu.sp
        cpu.r0 = 0x00
        cpu.r1 = 0x80
        cpu.r5 = 0x70
        cpu.label('call_save_8000')
        cpu.r4 = cpu.mem8[0x00, cpu.er0]
        cpu.mem8[0x00, cpu.er2] = cpu.r4
        cpu.er0 += 0x01
        cpu.er2 += 0x01
        cpu.r5 += 0xFF
        if cpu.ne:
            cpu.branch('call_save_8000')
        cpu.r0 = 0x86
        cpu.r1 = 0x80
        cpu.r5 = 0x02
        cpu.label('call_save_8086')
        cpu.r4 = cpu.mem8[0x00, cpu.er0]
        cpu.mem8[0x00, cpu.er2] = cpu.r4
        cpu.er0 += 0x01
        cpu.er2 += 0x01
        cpu.r5 += 0xFF
        if cpu.ne:
            cpu.branch('call_save_8086')
        cpu.r0 = 0xA0
        cpu.r1 = 0x80
        cpu.r5 = 0x03
        cpu.label('call_save_80a0')
        cpu.r4 = cpu.mem8[0x00, cpu.er0]
        cpu.mem8[0x00, cpu.er2] = cpu.r4
        cpu.er0 += 0x01
        cpu.er2 += 0x01
        cpu.r5 += 0xFF
        if cpu.ne:
            cpu.branch('call_save_80a0')
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0004)]
        cpu.er2 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0008)]
        cpu.er4 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x000C)]
        cpu.er6 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0010)]
        cpu.er10 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0002)]
        cpu.er8 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0000)]
        cpu.call(CALL_BRIDGE_ADDRESS)
        cpu.er2 = cpu.sp
        cpu.er2 += 0x3F
        cpu.er2 += 0x3F
        cpu.er2 += 0x0A
        cpu.mem16[0x00, cpu.er2] = cpu.er0
        cpu.er2 = cpu.sp
        cpu.r0 = 0x00
        cpu.r1 = 0x80
        cpu.r5 = 0x70
        cpu.label('call_restore_8000')
        cpu.r4 = cpu.mem8[0x00, cpu.er2]
        cpu.mem8[0x00, cpu.er0] = cpu.r4
        cpu.er0 += 0x01
        cpu.er2 += 0x01
        cpu.r5 += 0xFF
        if cpu.ne:
            cpu.branch('call_restore_8000')
        cpu.r0 = 0x86
        cpu.r1 = 0x80
        cpu.r5 = 0x02
        cpu.label('call_restore_8086')
        cpu.r4 = cpu.mem8[0x00, cpu.er2]
        cpu.mem8[0x00, cpu.er0] = cpu.r4
        cpu.er0 += 0x01
        cpu.er2 += 0x01
        cpu.r5 += 0xFF
        if cpu.ne:
            cpu.branch('call_restore_8086')
        cpu.r0 = 0xA0
        cpu.r1 = 0x80
        cpu.r5 = 0x03
        cpu.label('call_restore_80a0')
        cpu.r4 = cpu.mem8[0x00, cpu.er2]
        cpu.mem8[0x00, cpu.er0] = cpu.r4
        cpu.er0 += 0x01
        cpu.er2 += 0x01
        cpu.r5 += 0xFF
        if cpu.ne:
            cpu.branch('call_restore_80a0')
        cpu.sp += 0x78
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.qr0)
        cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 0x0000)]
        cpu.jump('word_result')
        cpu.label('zero')
        cpu.er0 = 0x00
        cpu.label('word_result')
        cpu.er2 = 0x00
        cpu.mem16[0x00, cpu.er12] = cpu.er0
        cpu.mem16[0x00, cpu.offset(cpu.er12, 0x0002)] = cpu.er2
        cpu.er0 = 0x00
        cpu.jump('dispatch_out')
        cpu.label('argument')
        cpu.er0 = 0x04
        cpu.jump('dispatch_out')
        cpu.label('memory')
        cpu.er0 = 0x06
        cpu.label('dispatch_out')
        cpu.sp += 0x08
        cpu.label('entry_out')
        cpu.pop(cpu.er2)
        cpu.pop(cpu.ea)
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.psw = cpu.r2
        cpu.pop(cpu.pc)
        cpu.label('entry_memory')
        cpu.er0 = 0x06
        cpu.jump('entry_out')
        cpu.label('to_integer')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.er12 = cpu.er4
        cpu.er10 = cpu.er2
        cpu.er0 = cpu.sp
        cpu.r2 = 0xC2
        cpu.r3 = 0x82
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_35')
        cpu.jump('conv_memory')
        cpu.label('skip_35')
        cpu.sp += -16
        cpu.er14 = cpu.sp
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0000)] = cpu.r10
        cpu.compare(cpu.r11, 0x00)
        if cpu.eq:
            cpu.branch('skip_36')
        cpu.jump('conv_argument')
        cpu.label('skip_36')
        cpu.compare(cpu.r10, 0x05)
        if cpu.lt:
            cpu.branch('skip_37')
        cpu.jump('conv_argument')
        cpu.label('skip_37')
        cpu.er2 = cpu.er8
        cpu.er2 += 0x0A
        cpu.r6 = 0x0A
        cpu.label('imaginary')
        cpu.r0 = cpu.mem8[0x00, cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_38')
        cpu.jump('conv_argument')
        cpu.label('skip_38')
        cpu.er2 += 0x01
        cpu.r6 += 0xFF
        if cpu.ne:
            cpu.branch('imaginary')
        cpu.er4 = 0x00
        cpu.er6 = 0x00
        cpu.r0 = cpu.mem8[0x00, cpu.er8]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('nonzero')
        cpu.er2 = cpu.er8
        cpu.r6 = 0x0A
        cpu.label('native_zero')
        cpu.r0 = cpu.mem8[0x00, cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_39')
        cpu.jump('conv_argument')
        cpu.label('skip_39')
        cpu.er2 += 0x01
        cpu.r6 += 0xFF
        if cpu.ne:
            cpu.branch('native_zero')
        cpu.jump('integer_result')
        cpu.label('nonzero')
        cpu.compare(cpu.r0, 0x0A)
        if cpu.lt:
            cpu.branch('skip_40')
        cpu.jump('conv_argument')
        cpu.label('skip_40')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er8, 0x0009)]
        cpu.r1 = 0x00
        cpu.compare(cpu.r0, 0x05)
        if cpu.lt:
            cpu.branch('positive')
        cpu.r0 += 0xFB
        cpu.r1 = 0x01
        cpu.label('positive')
        cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0001)] = cpu.r1
        cpu.compare(cpu.r0, 0x01)
        if cpu.eq:
            cpu.branch('skip_41')
        cpu.jump('conv_argument')
        cpu.label('skip_41')
        cpu.r7 = cpu.mem8[0x00, cpu.offset(cpu.er8, 0x0008)]
        cpu.compare(cpu.r7, 0x08)
        if cpu.lt:
            cpu.branch('skip_42')
        cpu.jump('conv_argument')
        cpu.label('skip_42')
        cpu.r10 = 0x00
        cpu.label('digit')
        cpu.compare(cpu.r10, 0x00)
        if cpu.eq:
            cpu.branch('digit_low')
        cpu.r0 = cpu.r10
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('digit_low')
        cpu.er8 += 0x01
        cpu.r3 = cpu.mem8[0x00, cpu.er8]
        cpu.r3 >>= 0x04
        cpu.branch('digit_ready')
        cpu.label('digit_low')
        cpu.r3 = cpu.mem8[0x00, cpu.er8]
        cpu.r3 &= 0x0F
        cpu.label('digit_ready')
        cpu.compare(cpu.r3, 0x0A)
        if cpu.lt:
            cpu.branch('skip_43')
        cpu.jump('conv_argument')
        cpu.label('skip_43')
        cpu.r0 = cpu.r7
        cpu.r0 += 0x01
        cpu.compare(cpu.r10, cpu.r0)
        if cpu.lt:
            cpu.branch('accumulate')
        cpu.compare(cpu.r3, 0x00)
        if cpu.eq:
            cpu.branch('skip_44')
        cpu.jump('conv_argument')
        cpu.label('skip_44')
        cpu.jump('digit_next')
        cpu.label('accumulate')
        cpu.compare(cpu.r4, 0x99)
        cpu.compare_carry(cpu.r5, 0x99)
        cpu.compare_carry(cpu.r6, 0x19)
        if cpu.lt:
            cpu.branch('skip_46')
        if cpu.eq:
            cpu.branch('skip_45')
        cpu.jump('conv_argument')
        cpu.label('skip_45')
        cpu.compare(cpu.r3, 0x06)
        if cpu.lt:
            cpu.branch('skip_46')
        cpu.jump('conv_argument')
        cpu.label('skip_46')
        cpu.label('multiply')
        cpu.er0 = cpu.er4
        cpu.r2 = cpu.r6
        cpu.shift_left_carry(cpu.r6, 0x01)
        cpu.shift_left_carry(cpu.r5, 0x01)
        cpu.r4 <<= 0x01
        cpu.shift_left_carry(cpu.r2, 0x03)
        cpu.shift_left_carry(cpu.r1, 0x03)
        cpu.r0 <<= 0x03
        cpu.r4 += cpu.r0
        cpu.add_carry(cpu.r5, cpu.r1)
        cpu.add_carry(cpu.r6, cpu.r2)
        cpu.r4 += cpu.r3
        cpu.add_carry(cpu.r5, 0x00)
        cpu.add_carry(cpu.r6, 0x00)
        cpu.label('digit_next')
        cpu.r10 += 0x01
        cpu.compare(cpu.r10, 0x0F)
        if cpu.ge:
            cpu.branch('skip_47')
        cpu.jump('digit')
        cpu.label('skip_47')
        cpu.r7 = 0x00
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0000)]
        cpu.compare(cpu.r0, 0x04)
        if cpu.eq:
            cpu.branch('skip_50')
        cpu.compare(cpu.r0, 0x02)
        if cpu.ne:
            cpu.branch('narrow_result')
        cpu.compare(cpu.r6, 0x10)
        if cpu.lt:
            cpu.branch('skip_48')
        cpu.jump('conv_argument')
        cpu.label('skip_48')
        cpu.jump('skip_50')
        cpu.label('narrow_result')
        cpu.compare(cpu.r6, 0x00)
        if cpu.eq:
            cpu.branch('skip_49')
        cpu.jump('conv_argument')
        cpu.label('skip_49')
        cpu.compare(cpu.r0, 0x03)
        if cpu.eq:
            cpu.branch('signed_result')
        cpu.compare(cpu.r0, 0x01)
        if cpu.eq:
            cpu.branch('skip_50')
        cpu.compare(cpu.r5, 0x00)
        if cpu.eq:
            cpu.branch('skip_50')
        cpu.jump('conv_argument')
        cpu.label('skip_50')
        cpu.label('unsigned_result')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0001)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_51')
        cpu.jump('conv_argument')
        cpu.label('skip_51')
        cpu.jump('integer_result')
        cpu.label('signed_result')
        cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 0x0001)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('negative_result')
        cpu.compare(cpu.r5, 0x80)
        if cpu.lt:
            cpu.branch('skip_52')
        cpu.jump('conv_argument')
        cpu.label('skip_52')
        cpu.jump('integer_result')
        cpu.label('negative_result')
        cpu.compare(cpu.r4, 0x00)
        cpu.compare_carry(cpu.r5, 0x80)
        if cpu.lt:
            cpu.branch('skip_53')
        if cpu.eq:
            cpu.branch('skip_53')
        cpu.jump('conv_argument')
        cpu.label('skip_53')
        cpu.label('negate')
        cpu.r4 ^= 0xFF
        cpu.r5 ^= 0xFF
        cpu.er4 += 0x01
        cpu.r6 = 0xFF
        cpu.r7 = 0xFF
        cpu.label('integer_result')
        cpu.mem16[0x00, cpu.er12] = cpu.er4
        cpu.mem16[0x00, cpu.offset(cpu.er12, 0x0002)] = cpu.er6
        cpu.er0 = 0x00
        cpu.jump('conv_out')
        cpu.label('to_number')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.er12 = cpu.er2
        cpu.er0 = cpu.sp
        cpu.r2 = 0xC2
        cpu.r3 = 0x82
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_54')
        cpu.jump('conv_memory')
        cpu.label('skip_54')
        cpu.sp += -16
        cpu.er14 = cpu.sp
        cpu.er4 = cpu.mem16[0x00, cpu.er8]
        cpu.er6 = cpu.mem16[0x00, cpu.offset(cpu.er8, 0x0002)]
        cpu.er8 = cpu.er14
        cpu.r10 = 0x00
        cpu.label('decimal_divide')
        cpu.r1 = 0x00
        cpu.r0 = cpu.r7
        cpu.r2 = 0x0A
        cpu.divide(cpu.er0, cpu.r2)
        cpu.r7 = cpu.r0
        cpu.r1 = cpu.r2
        cpu.r0 = cpu.r6
        cpu.r2 = 0x0A
        cpu.divide(cpu.er0, cpu.r2)
        cpu.r6 = cpu.r0
        cpu.r1 = cpu.r2
        cpu.r0 = cpu.r5
        cpu.r2 = 0x0A
        cpu.divide(cpu.er0, cpu.r2)
        cpu.r5 = cpu.r0
        cpu.r1 = cpu.r2
        cpu.r0 = cpu.r4
        cpu.r2 = 0x0A
        cpu.divide(cpu.er0, cpu.r2)
        cpu.r4 = cpu.r0
        cpu.r1 = cpu.r2
        cpu.mem8[0x00, cpu.er8] = cpu.r2
        cpu.er8 += 0x01
        cpu.r10 += 0x01
        cpu.r0 = cpu.r4
        cpu.r0 |= cpu.r5
        cpu.r0 |= cpu.r6
        cpu.r0 |= cpu.r7
        if cpu.ne:
            cpu.branch('decimal_divide')
        cpu.er2 = cpu.er12
        cpu.r0 = 0x00
        cpu.r1 = 0x14
        cpu.label('number_clear')
        cpu.mem8[0x00, cpu.er2] = cpu.r0
        cpu.er2 += 0x01
        cpu.r1 += 0xFF
        if cpu.ne:
            cpu.branch('number_clear')
        cpu.r0 = cpu.r10
        cpu.r0 += 0xFF
        cpu.mem8[0x00, cpu.offset(cpu.er12, 0x0008)] = cpu.r0
        cpu.er8 += -1
        cpu.r0 = cpu.mem8[0x00, cpu.er8]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('number_done')
        cpu.r1 = 0x01
        cpu.mem8[0x00, cpu.offset(cpu.er12, 0x0009)] = cpu.r1
        cpu.mem8[0x00, cpu.er12] = cpu.r0
        cpu.r10 += 0xFF
        if cpu.eq:
            cpu.branch('number_done')
        cpu.label('number_pair')
        cpu.er12 += 0x01
        cpu.er8 += -1
        cpu.r3 = cpu.mem8[0x00, cpu.er8]
        cpu.r3 <<= 0x04
        cpu.r10 += 0xFF
        if cpu.eq:
            cpu.branch('number_last')
        cpu.er8 += -1
        cpu.r0 = cpu.mem8[0x00, cpu.er8]
        cpu.r3 |= cpu.r0
        cpu.r10 += 0xFF
        cpu.label('number_last')
        cpu.mem8[0x00, cpu.er12] = cpu.r3
        cpu.compare(cpu.r10, 0x00)
        if cpu.ne:
            cpu.branch('number_pair')
        cpu.label('number_done')
        cpu.er0 = 0x00
        cpu.jump('conv_out')
        cpu.label('conv_argument')
        cpu.er0 = 0x04
        cpu.label('conv_out')
        cpu.sp += 0x10
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('conv_memory')
        cpu.er0 = 0x06
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
