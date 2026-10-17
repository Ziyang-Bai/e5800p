"""Fixed-layout e5800p graph routines and tables."""

from kits import cpu

GRAPH = 0x81800
GRAPH_VALID_EXPONENT = 0x81C40
GRAPH_BCD_15_TO_FIXED_64 = 0x82200
GRAPH_COPY_64 = 0x82100
GRAPH_COMPARE_64 = 0x82120
GRAPH_SUBTRACT_64 = 0x82180
GRAPH_ZERO_64 = 0x82400
GRAPH_ZERO_AXIS_PIXEL = 0x82420
GRAPH_Y_PIXEL_64 = 0x82380
GRAPH_PLOT_SAMPLE = 0x82500
ROM_REFRESH = 0x043BE
SCANNER_ADDRESS = 0x80800
GRAPH_EXPONENT = 0x81C00
GRAPH_DECIMAL_DIGIT = 0x82300
GRAPH_MULTIPLY_31 = 0x82340
GRAPH_INTER_SAMPLE_POLE = 0x82480
GRAPH_SAME_COLUMN_SPAN = 0x825A0
GRAPH_LINE = 0x81E80


def install(fw):
    @fw.function(native=True, address=0x81100)
    def graph_table_gate():
        cpu.label('graph_table_gate')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr0)
        cpu.push(cpu.er14)
        cpu.er14 = cpu.sp
        cpu.er0 = cpu.mem16[cpu.offset(cpu.fp, 6)]
        cpu.compare(cpu.r0, 0xA4)
        cpu.compare_carry(cpu.r1, 0x7E)
        if cpu.eq:
            cpu.branch('branch_0016')
        cpu.compare(cpu.r0, 0xD2)
        cpu.compare_carry(cpu.r1, 0x7E)
        if cpu.ne:
            cpu.branch('branch_002c')
        cpu.label('branch_0016')
        cpu.r0 = cpu.mem8[0x8091]
        cpu.compare(cpu.r0, 0x85)
        if cpu.ne:
            cpu.branch('branch_002c')
        cpu.pop(cpu.er14)
        cpu.call(GRAPH)
        cpu.compare(cpu.r0, 0x01)
        if cpu.eq:
            cpu.branch('branch_0038')
        cpu.jump('branch_002e')
        cpu.label('branch_002c')
        cpu.pop(cpu.er14)
        cpu.label('branch_002e')
        cpu.pop(cpu.xr0)
        cpu.push(cpu.er14)
        cpu.er14 = cpu.sp
        cpu.jump(0xE369A)
        cpu.label('branch_0038')
        cpu.pop(cpu.xr0)
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0x81800)
    def graph():
        cpu.label('graph')
        cpu.push(cpu.lr)
        cpu.push(cpu.er14)
        cpu.er14 = cpu.sp
        cpu.sp += -112
        cpu.push(cpu.xr4)
        cpu.push(cpu.xr8)
        cpu.push(cpu.er12)
        cpu.er0 = cpu.er14
        cpu.er0 += -8
        cpu.r2 = 0x00
        cpu.push(cpu.r2)
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += -4
        cpu.r2 = 0x00
        cpu.push(cpu.r2)
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += -12
        cpu.r2 = 0x00
        cpu.push(cpu.r2)
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += -13
        cpu.r2 = 0x00
        cpu.push(cpu.r2)
        cpu.push(cpu.er0)
        cpu.r2 = 0x01
        cpu.push(cpu.r2)
        cpu.r0 = 0x48
        cpu.r1 = 0xE7
        cpu.push(cpu.er0)
        cpu.r0 = 0x98
        cpu.r1 = 0xE7
        cpu.r2 = 0x01
        cpu.call(0x1A574)
        cpu.sp += 0x14
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('branch_0054')
        cpu.jump('branch_0278')
        cpu.label('branch_0054')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.fp, -2)]
        cpu.compare(cpu.r0, 0x04)
        if cpu.eq:
            cpu.branch('branch_005e')
        cpu.jump('branch_0278')
        cpu.label('branch_005e')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.fp, -6)]
        cpu.compare(cpu.r0, 0x00)
        cpu.compare_carry(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('branch_006a')
        cpu.jump('branch_0278')
        cpu.label('branch_006a')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.fp, -4)]
        cpu.er4 = cpu.er0
        cpu.r2 = 0x04
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('branch_007c')
        cpu.jump('branch_0278')
        cpu.label('branch_007c')
        cpu.jump('branch_0084')
        cpu.r0 = 0x00
        cpu.r0 = 0x00
        cpu.label('branch_0084')
        cpu.mem8[cpu.offset(cpu.fp, -14)] = cpu.r0
        cpu.r12 = cpu.r0
        cpu.er4 += 0x01
        cpu.r2 = 0x04
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.er4 += -1
        cpu.compare(cpu.r0, 0x02)
        if cpu.eq:
            cpu.branch('branch_009a')
        cpu.jump('branch_0278')
        cpu.label('branch_009a')
        cpu.r0 = cpu.r12
        cpu.r1 = 0x00
        cpu.r2 = 0x14
        cpu.multiply(cpu.er0, cpu.r2)
        cpu.er0 += 0x02
        cpu.er2 = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.fp, -8)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ges:
            cpu.branch('branch_00b0')
        cpu.jump('branch_0278')
        cpu.label('branch_00b0')
        cpu.r8 = 0x80
        cpu.er0 = cpu.mem16[cpu.offset(cpu.fp, -4)]
        cpu.er4 = cpu.er0
        cpu.er4 += 0x0C
        cpu.r12 = cpu.mem8[cpu.offset(cpu.fp, -14)]
        cpu.label('branch_00ba')
        cpu.call(GRAPH_VALID_EXPONENT)
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('branch_00c8')
        cpu.compare(cpu.r0, cpu.r8)
        if cpu.les:
            cpu.branch('branch_00c8')
        cpu.r8 = cpu.r0
        cpu.label('branch_00c8')
        cpu.er4 += 0x14
        cpu.r12 += 0xFF
        cpu.compare(cpu.r12, 0x00)
        if cpu.eq:
            cpu.branch('branch_00d4')
        cpu.jump('branch_00ba')
        cpu.label('branch_00d4')
        cpu.compare(cpu.r8, 0x80)
        if cpu.ne:
            cpu.branch('branch_00da')
        cpu.r8 = 0x00
        cpu.label('branch_00da')
        cpu.r13 = 0x00
        cpu.r4 = cpu.mem8[cpu.offset(cpu.fp, -4)]
        cpu.r5 = cpu.mem8[cpu.offset(cpu.fp, -3)]
        cpu.er4 += 0x0C
        cpu.r12 = cpu.mem8[cpu.offset(cpu.fp, -14)]
        cpu.label('branch_00e4')
        cpu.call(GRAPH_BCD_15_TO_FIXED_64)
        cpu.compare(cpu.r2, 0x00)
        if cpu.ne:
            cpu.branch('branch_00f0')
        cpu.jump('branch_014a')
        cpu.label('branch_00f0')
        cpu.compare(cpu.r13, 0x00)
        if cpu.ne:
            cpu.branch('branch_0112')
        cpu.er6 = cpu.er14
        cpu.er6 += -48
        cpu.er10 = cpu.er14
        cpu.er10 += -56
        cpu.call(GRAPH_COPY_64)
        cpu.er6 = cpu.er14
        cpu.er6 += -48
        cpu.er10 = cpu.er14
        cpu.er10 += -64
        cpu.call(GRAPH_COPY_64)
        cpu.r13 = 0x01
        cpu.jump('branch_014a')
        cpu.label('branch_0112')
        cpu.er6 = cpu.er14
        cpu.er6 += -48
        cpu.er10 = cpu.er14
        cpu.er10 += -56
        cpu.call(GRAPH_COMPARE_64)
        cpu.compare(cpu.r0, 0x00)
        if cpu.ges:
            cpu.branch('branch_012e')
        cpu.er6 = cpu.er14
        cpu.er6 += -48
        cpu.er10 = cpu.er14
        cpu.er10 += -56
        cpu.call(GRAPH_COPY_64)
        cpu.label('branch_012e')
        cpu.er6 = cpu.er14
        cpu.er6 += -48
        cpu.er10 = cpu.er14
        cpu.er10 += -64
        cpu.call(GRAPH_COMPARE_64)
        cpu.compare(cpu.r0, 0x00)
        if cpu.les:
            cpu.branch('branch_014a')
        cpu.er6 = cpu.er14
        cpu.er6 += -48
        cpu.er10 = cpu.er14
        cpu.er10 += -64
        cpu.call(GRAPH_COPY_64)
        cpu.label('branch_014a')
        cpu.er4 += 0x14
        cpu.r12 += 0xFF
        cpu.compare(cpu.r12, 0x00)
        if cpu.eq:
            cpu.branch('branch_0156')
        cpu.jump('branch_00e4')
        cpu.label('branch_0156')
        cpu.compare(cpu.r13, 0x00)
        if cpu.ne:
            cpu.branch('branch_015e')
        cpu.jump('branch_0278')
        cpu.label('branch_015e')
        cpu.er6 = cpu.er14
        cpu.er6 += -64
        cpu.er10 = cpu.er14
        cpu.er10 += -56
        cpu.call(GRAPH_COMPARE_64)
        cpu.mem8[cpu.offset(cpu.fp, -22)] = cpu.r0
        cpu.er6 = cpu.er14
        cpu.er6 += -64
        cpu.er10 = cpu.er14
        cpu.er10 += -48
        cpu.er10 += -24
        cpu.call(GRAPH_COPY_64)
        cpu.er6 = cpu.er14
        cpu.er6 += -48
        cpu.er6 += -24
        cpu.er10 = cpu.er14
        cpu.er10 += -56
        cpu.call(GRAPH_SUBTRACT_64)
        cpu.call(GRAPH_ZERO_64)
        cpu.call(0x0409A)
        cpu.er6 = cpu.er14
        cpu.er6 += -56
        cpu.er10 = cpu.er14
        cpu.er10 += -48
        cpu.call(GRAPH_COMPARE_64)
        cpu.compare(cpu.r0, 0x00)
        if cpu.les:
            cpu.branch('branch_01a4')
        cpu.jump('branch_01ce')
        cpu.label('branch_01a4')
        cpu.er6 = cpu.er14
        cpu.er6 += -64
        cpu.er10 = cpu.er14
        cpu.er10 += -48
        cpu.call(GRAPH_COMPARE_64)
        cpu.compare(cpu.r0, 0x00)
        if cpu.ges:
            cpu.branch('branch_01b8')
        cpu.jump('branch_01ce')
        cpu.label('branch_01b8')
        cpu.call(GRAPH_ZERO_AXIS_PIXEL)
        cpu.r6 = cpu.r0
        cpu.r7 = 0x00
        cpu.label('branch_01c0')
        cpu.r0 = cpu.r7
        cpu.r1 = cpu.r6
        cpu.call(0x0431C)
        cpu.r7 += 0x01
        cpu.compare(cpu.r7, 0x60)
        if cpu.lts:
            cpu.branch('branch_01c0')
        cpu.label('branch_01ce')
        cpu.r4 = cpu.mem8[cpu.offset(cpu.fp, -4)]
        cpu.r5 = cpu.mem8[cpu.offset(cpu.fp, -3)]
        cpu.er4 += 0x02
        cpu.r2 = 0x04
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('branch_01e2')
        cpu.jump('branch_01f4')
        cpu.label('branch_01e2')
        cpu.r6 = 0x00
        cpu.r7 = 0x00
        cpu.label('branch_01e6')
        cpu.r0 = cpu.r6
        cpu.r1 = cpu.r7
        cpu.call(0x0431C)
        cpu.r7 += 0x01
        cpu.compare(cpu.r7, 0x20)
        if cpu.lts:
            cpu.branch('branch_01e6')
        cpu.label('branch_01f4')
        cpu.r13 = 0x00
        cpu.r4 = cpu.mem8[cpu.offset(cpu.fp, -4)]
        cpu.r5 = cpu.mem8[cpu.offset(cpu.fp, -3)]
        cpu.er4 += 0x0C
        cpu.r12 = cpu.mem8[cpu.offset(cpu.fp, -14)]
        cpu.compare(cpu.r12, 0x01)
        if cpu.ne:
            cpu.branch('branch_020a')
        cpu.r0 = 0x30
        cpu.mem8[cpu.offset(cpu.fp, -28)] = cpu.r0
        cpu.jump('branch_0218')
        cpu.label('branch_020a')
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.fp, -28)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.fp, -30)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.fp, -31)] = cpu.r0
        cpu.r0 = cpu.r12
        cpu.r0 += 0xFF
        cpu.mem8[cpu.offset(cpu.fp, -24)] = cpu.r0
        cpu.label('branch_0218')
        cpu.call(GRAPH_Y_PIXEL_64)
        cpu.compare(cpu.r2, 0x00)
        if cpu.ne:
            cpu.branch('branch_0226')
        cpu.r13 = 0x00
        cpu.jump('branch_022e')
        cpu.label('branch_0226')
        cpu.call(GRAPH_PLOT_SAMPLE)
        cpu.jump('branch_022e')
        cpu.label('branch_022e')
        cpu.er4 += 0x14
        cpu.r12 += 0xFF
        cpu.compare(cpu.r12, 0x00)
        if cpu.ne:
            cpu.branch('branch_023a')
        cpu.jump('branch_0266')
        cpu.label('branch_023a')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.fp, -30)]
        cpu.r1 = cpu.mem8[cpu.offset(cpu.fp, -31)]
        cpu.r2 = 0x5F
        cpu.r0 += cpu.r2
        cpu.add_carry(cpu.r1, 0x00)
        cpu.r7 = cpu.mem8[cpu.offset(cpu.fp, -24)]
        cpu.label('branch_0246')
        cpu.compare(cpu.r1, 0x00)
        if cpu.ne:
            cpu.branch('branch_024e')
        cpu.compare(cpu.r0, cpu.r7)
        if cpu.lt:
            cpu.branch('branch_025e')
        cpu.label('branch_024e')
        cpu.r3 = 0x00
        cpu.r0 -= cpu.r7
        cpu.sub_carry(cpu.r1, cpu.r3)
        cpu.r2 = cpu.mem8[cpu.offset(cpu.fp, -28)]
        cpu.r2 += 0x01
        cpu.mem8[cpu.offset(cpu.fp, -28)] = cpu.r2
        cpu.jump('branch_0246')
        cpu.label('branch_025e')
        cpu.mem8[cpu.offset(cpu.fp, -30)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.fp, -31)] = cpu.r1
        cpu.jump('branch_0218')
        cpu.label('branch_0266')
        cpu.call(ROM_REFRESH)
        cpu.label('branch_026a')
        cpu.call(SCANNER_ADDRESS)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('branch_026a')
        cpu.r0 = 0x01
        cpu.jump('branch_027a')
        cpu.label('branch_0278')
        cpu.r0 = 0x00
        cpu.label('branch_027a')
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr8)
        cpu.pop(cpu.xr4)
        cpu.sp = cpu.er14
        cpu.pop(cpu.er14)
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0x81C00)
    def graph_exponent():
        cpu.label('graph_exponent')
        cpu.r3 = cpu.r0
        cpu.r0 >>= 0x04
        cpu.r1 = 0x00
        cpu.r2 = 0x0A
        cpu.multiply(cpu.er0, cpu.r2)
        cpu.r3 &= 0x0F
        cpu.r0 += cpu.r3
        cpu.compare(cpu.r7, 0x00)
        if cpu.eq:
            cpu.branch('branch_0016')
        cpu.compare(cpu.r7, 0x05)
        if cpu.ne:
            cpu.branch('branch_001c')
        cpu.label('branch_0016')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('branch_001c')
        cpu.r0 += 0x9C
        cpu.label('branch_001c')
        cpu.ret()


    @fw.function(native=True, address=0x81C40)
    def graph_valid_exponent():
        cpu.label('graph_valid_exponent')
        cpu.push(cpu.lr)
        cpu.er4 += 0x09
        cpu.r2 = 0x04
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.er4 += -9
        cpu.r7 = cpu.r0
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('branch_0022')
        cpu.compare(cpu.r0, 0x01)
        if cpu.eq:
            cpu.branch('branch_0022')
        cpu.compare(cpu.r0, 0x05)
        if cpu.eq:
            cpu.branch('branch_0022')
        cpu.compare(cpu.r0, 0x06)
        if cpu.eq:
            cpu.branch('branch_0022')
        cpu.jump('branch_0042')
        cpu.label('branch_0022')
        cpu.r2 = 0x04
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.r0 &= 0x0F
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('branch_0042')
        cpu.er4 += 0x08
        cpu.r2 = 0x04
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.er4 += -8
        cpu.call(GRAPH_EXPONENT)
        cpu.r2 = 0x01
        cpu.jump('branch_0044')
        cpu.label('branch_0042')
        cpu.r2 = 0x00
        cpu.label('branch_0044')
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0x81E80)
    def graph_line():
        cpu.label('graph_line')
        cpu.push(cpu.lr)
        cpu.r6 = cpu.r0
        cpu.r7 = cpu.r1
        cpu.call(0x0431C)
        cpu.compare(cpu.r13, 0x00)
        if cpu.eq:
            cpu.branch('branch_0058')
        cpu.r9 = cpu.mem8[cpu.offset(cpu.fp, -26)]
        cpu.r10 = cpu.mem8[cpu.offset(cpu.fp, -27)]
        cpu.r11 = cpu.r7
        cpu.r11 -= cpu.r10
        cpu.compare(cpu.r11, 0x00)
        if cpu.ges:
            cpu.branch('branch_0022')
        cpu.negate(cpu.r11)
        cpu.r0 = 0xFF
        cpu.jump('branch_0024')
        cpu.label('branch_0022')
        cpu.r0 = 0x01
        cpu.label('branch_0024')
        cpu.mem8[cpu.offset(cpu.fp, -16)] = cpu.r0
        cpu.r0 = cpu.r6
        cpu.r0 -= cpu.r9
        cpu.mem8[cpu.offset(cpu.fp, -15)] = cpu.r0
        cpu.r0 >>= 0x01
        cpu.mem8[cpu.offset(cpu.fp, -17)] = cpu.r0
        cpu.label('branch_0030')
        cpu.r9 += 0x01
        cpu.compare(cpu.r9, cpu.r6)
        if cpu.ges:
            cpu.branch('branch_0058')
        cpu.r3 = cpu.mem8[cpu.offset(cpu.fp, -17)]
        cpu.r3 -= cpu.r11
        cpu.label('branch_003a')
        cpu.compare(cpu.r3, 0x00)
        if cpu.ges:
            cpu.branch('branch_004a')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.fp, -16)]
        cpu.r10 += cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.fp, -15)]
        cpu.r3 += cpu.r0
        cpu.jump('branch_003a')
        cpu.label('branch_004a')
        cpu.mem8[cpu.offset(cpu.fp, -17)] = cpu.r3
        cpu.r0 = cpu.r9
        cpu.r1 = cpu.r10
        cpu.call(0x0431C)
        cpu.jump('branch_0030')
        cpu.label('branch_0058')
        cpu.mem8[cpu.offset(cpu.fp, -26)] = cpu.r6
        cpu.mem8[cpu.offset(cpu.fp, -27)] = cpu.r7
        cpu.r13 = 0x01
        cpu.pop(cpu.pc)


    @fw.function(native=True, address=0x82100)
    def graph_copy_64():
        cpu.label('graph_copy_64')
        cpu.r9 = 0x08
        cpu.label('branch_0002')
        cpu.r0 = cpu.mem8[cpu.er6]
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er6 += 0x01
        cpu.er10 += 0x01
        cpu.r9 += 0xFF
        cpu.compare(cpu.r9, 0x00)
        if cpu.ne:
            cpu.branch('branch_0002')
        cpu.ret()


    @fw.function(native=True, address=0x82120)
    def graph_compare_64():
        cpu.label('graph_compare_64')
        cpu.r3 = 0x01
        cpu.jump('branch_0008')
        cpu.r3 = 0x00
        cpu.label('branch_0008')
        cpu.push(cpu.er6)
        cpu.push(cpu.er10)
        cpu.er6 += 0x07
        cpu.er10 += 0x07
        cpu.r9 = 0x08
        cpu.label('branch_0012')
        cpu.r0 = cpu.mem8[cpu.er6]
        cpu.r1 = cpu.mem8[cpu.er10]
        cpu.compare(cpu.r3, 0x00)
        if cpu.eq:
            cpu.branch('branch_0020')
        cpu.r0 ^= 0x80
        cpu.r1 ^= 0x80
        cpu.r3 = 0x00
        cpu.label('branch_0020')
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.lt:
            cpu.branch('branch_0036')
        if cpu.gt:
            cpu.branch('branch_003c')
        cpu.er6 += -1
        cpu.er10 += -1
        cpu.r9 += 0xFF
        cpu.compare(cpu.r9, 0x00)
        if cpu.ne:
            cpu.branch('branch_0012')
        cpu.r0 = 0x00
        cpu.jump('branch_003e')
        cpu.label('branch_0036')
        cpu.r0 = 0xFF
        cpu.jump('branch_003e')
        cpu.label('branch_003c')
        cpu.r0 = 0x01
        cpu.label('branch_003e')
        cpu.pop(cpu.er10)
        cpu.pop(cpu.er6)
        cpu.ret()


    @fw.function(native=True, address=0x82180)
    def graph_subtract_64():
        cpu.label('graph_subtract_64')
        cpu.push(cpu.er6)
        cpu.push(cpu.er10)
        cpu.push(cpu.er12)
        cpu.r9 = 0x08
        cpu.r12 = 0x00
        cpu.label('branch_000a')
        cpu.r0 = cpu.mem8[cpu.er6]
        cpu.r1 = cpu.mem8[cpu.er10]
        cpu.r2 = cpu.r0
        cpu.r3 = 0x00
        cpu.r0 = cpu.r1
        cpu.r1 = 0x00
        cpu.r0 += cpu.r12
        cpu.add_carry(cpu.r1, 0x00)
        cpu.r2 -= cpu.r0
        cpu.sub_carry(cpu.r3, cpu.r1)
        cpu.r12 = cpu.r3
        cpu.r12 &= 0x01
        cpu.r0 = cpu.r2
        cpu.mem8[cpu.er6] = cpu.r0
        cpu.er6 += 0x01
        cpu.er10 += 0x01
        cpu.r9 += 0xFF
        cpu.compare(cpu.r9, 0x00)
        if cpu.ne:
            cpu.branch('branch_000a')
        cpu.pop(cpu.er12)
        cpu.pop(cpu.er10)
        cpu.pop(cpu.er6)
        cpu.ret()


    @fw.function(native=True, address=0x82200)
    def graph_bcd_15_to_fixed_64():
        cpu.label('graph_bcd_15_to_fixed_64')
        cpu.push(cpu.lr)
        cpu.push(cpu.er12)
        cpu.push(cpu.er4)
        cpu.er10 = cpu.er14
        cpu.er10 += -48
        cpu.r9 = 0x08
        cpu.r0 = 0x00
        cpu.label('branch_000e')
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r9 += 0xFF
        cpu.compare(cpu.r9, 0x00)
        if cpu.ne:
            cpu.branch('branch_000e')
        cpu.er4 += 0x09
        cpu.r2 = 0x04
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.er4 += -9
        cpu.r7 = cpu.r0
        cpu.compare(cpu.r7, 0x00)
        if cpu.eq:
            cpu.branch('branch_003a')
        cpu.compare(cpu.r7, 0x01)
        if cpu.eq:
            cpu.branch('branch_003a')
        cpu.compare(cpu.r7, 0x05)
        if cpu.eq:
            cpu.branch('branch_003a')
        cpu.compare(cpu.r7, 0x06)
        if cpu.eq:
            cpu.branch('branch_003a')
        cpu.r2 = 0x00
        cpu.jump('branch_00d0')
        cpu.label('branch_003a')
        cpu.er4 += 0x08
        cpu.r2 = 0x04
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.er4 += -8
        cpu.call(GRAPH_EXPONENT)
        cpu.compare(cpu.r8, 0x10)
        if cpu.lts:
            cpu.branch('branch_0050')
        cpu.compare(cpu.r0, 0x00)
        if cpu.lts:
            cpu.branch('branch_00ce')
        cpu.label('branch_0050')
        cpu.r9 = cpu.r8
        cpu.r9 -= cpu.r0
        cpu.compare(cpu.r9, 0x10)
        if cpu.ges:
            cpu.branch('branch_00ce')
        cpu.r12 = 0x10
        cpu.r12 -= cpu.r9
        cpu.compare(cpu.r9, 0x00)
        if cpu.ne:
            cpu.branch('branch_0062')
        cpu.r12 = 0x0F
        cpu.label('branch_0062')
        cpu.r13 = 0x00
        cpu.r2 = 0x04
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.r0 &= 0x0F
        cpu.call(GRAPH_DECIMAL_DIGIT)
        cpu.r12 += 0xFF
        cpu.compare(cpu.r12, 0x00)
        if cpu.eq:
            cpu.branch('branch_00a0')
        cpu.label('branch_0076')
        cpu.er4 += 0x01
        cpu.label('branch_0078')
        cpu.r2 = 0x04
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.compare(cpu.r13, 0x00)
        if cpu.ne:
            cpu.branch('branch_008a')
        cpu.r0 >>= 0x04
        cpu.r13 = 0x01
        cpu.jump('branch_008e')
        cpu.label('branch_008a')
        cpu.r0 &= 0x0F
        cpu.r13 = 0x00
        cpu.label('branch_008e')
        cpu.call(GRAPH_DECIMAL_DIGIT)
        cpu.r12 += 0xFF
        cpu.compare(cpu.r12, 0x00)
        if cpu.eq:
            cpu.branch('branch_00a0')
        cpu.compare(cpu.r13, 0x00)
        if cpu.eq:
            cpu.branch('branch_0076')
        cpu.jump('branch_0078')
        cpu.label('branch_00a0')
        cpu.compare(cpu.r9, 0x00)
        if cpu.ne:
            cpu.branch('branch_00aa')
        cpu.r0 = 0x00
        cpu.call(GRAPH_DECIMAL_DIGIT)
        cpu.label('branch_00aa')
        cpu.compare(cpu.r7, 0x05)
        if cpu.eq:
            cpu.branch('branch_00b2')
        cpu.compare(cpu.r7, 0x06)
        if cpu.ne:
            cpu.branch('branch_00ce')
        cpu.label('branch_00b2')
        cpu.er10 = cpu.er14
        cpu.er10 += -48
        cpu.r9 = 0x08
        cpu.r6 = 0x01
        cpu.label('branch_00ba')
        cpu.r0 = cpu.mem8[cpu.er10]
        cpu.r0 ^= 0xFF
        cpu.r0 += cpu.r6
        cpu.r6 = 0x00
        cpu.add_carry(cpu.r6, 0x00)
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r9 += 0xFF
        cpu.compare(cpu.r9, 0x00)
        if cpu.ne:
            cpu.branch('branch_00ba')
        cpu.label('branch_00ce')
        cpu.r2 = 0x01
        cpu.label('branch_00d0')
        cpu.pop(cpu.er4)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.lr)
        cpu.ret()


    @fw.function(native=True, address=0x82300)
    def graph_decimal_digit():
        cpu.label('graph_decimal_digit')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr8)
        cpu.r6 = cpu.r0
        cpu.er10 = cpu.er14
        cpu.er10 += -48
        cpu.r9 = 0x08
        cpu.r2 = 0x0A
        cpu.label('branch_000e')
        cpu.r0 = cpu.mem8[cpu.er10]
        cpu.r1 = 0x00
        cpu.multiply(cpu.er0, cpu.r2)
        cpu.r0 += cpu.r6
        cpu.add_carry(cpu.r1, 0x00)
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.r6 = cpu.r1
        cpu.er10 += 0x01
        cpu.r9 += 0xFF
        cpu.compare(cpu.r9, 0x00)
        if cpu.ne:
            cpu.branch('branch_000e')
        cpu.pop(cpu.xr8)
        cpu.pop(cpu.lr)
        cpu.ret()


    @fw.function(native=True, address=0x82340)
    def graph_multiply_31():
        cpu.label('graph_multiply_31')
        cpu.push(cpu.xr8)
        cpu.er10 = cpu.er14
        cpu.er10 += -48
        cpu.er10 += -40
        cpu.r9 = 0x08
        cpu.r6 = 0x00
        cpu.r2 = 0x1F
        cpu.label('branch_000e')
        cpu.r0 = cpu.mem8[cpu.er10]
        cpu.r1 = 0x00
        cpu.multiply(cpu.er0, cpu.r2)
        cpu.r0 += cpu.r6
        cpu.add_carry(cpu.r1, 0x00)
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.r6 = cpu.r1
        cpu.er10 += 0x01
        cpu.r9 += 0xFF
        cpu.compare(cpu.r9, 0x00)
        if cpu.ne:
            cpu.branch('branch_000e')
        cpu.pop(cpu.xr8)
        cpu.ret()


    @fw.function(native=True, address=0x82380)
    def graph_y_pixel_64():
        cpu.label('graph_y_pixel_64')
        cpu.push(cpu.lr)
        cpu.push(cpu.er12)
        cpu.call(GRAPH_BCD_15_TO_FIXED_64)
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('branch_006c')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.fp, -22)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('branch_0018')
        cpu.r0 = 0x10
        cpu.jump('branch_006a')
        cpu.label('branch_0018')
        cpu.er6 = cpu.er14
        cpu.er6 += -64
        cpu.er10 = cpu.er14
        cpu.er10 += -48
        cpu.er10 += -32
        cpu.call(GRAPH_COPY_64)
        cpu.er6 = cpu.er14
        cpu.er6 += -48
        cpu.er6 += -32
        cpu.er10 = cpu.er14
        cpu.er10 += -48
        cpu.call(GRAPH_SUBTRACT_64)
        cpu.er6 = cpu.er14
        cpu.er6 += -48
        cpu.er6 += -32
        cpu.er10 = cpu.er14
        cpu.er10 += -48
        cpu.er10 += -40
        cpu.call(GRAPH_COPY_64)
        cpu.call(GRAPH_MULTIPLY_31)
        cpu.r12 = 0x00
        cpu.label('branch_004a')
        cpu.er6 = cpu.er14
        cpu.er6 += -48
        cpu.er6 += -40
        cpu.er10 = cpu.er14
        cpu.er10 += -48
        cpu.er10 += -24
        cpu.call(0x82126)
        cpu.compare(cpu.r0, 0x00)
        if cpu.lts:
            cpu.branch('branch_0068')
        cpu.call(GRAPH_SUBTRACT_64)
        cpu.r12 += 0x01
        cpu.compare(cpu.r12, 0x1F)
        if cpu.lts:
            cpu.branch('branch_004a')
        cpu.label('branch_0068')
        cpu.r0 = cpu.r12
        cpu.label('branch_006a')
        cpu.r2 = 0x01
        cpu.label('branch_006c')
        cpu.pop(cpu.er12)
        cpu.pop(cpu.lr)
        cpu.ret()


    @fw.function(native=True, address=0x82400)
    def graph_zero_64():
        cpu.label('graph_zero_64')
        cpu.er10 = cpu.er14
        cpu.er10 += -48
        cpu.r9 = 0x08
        cpu.r0 = 0x00
        cpu.label('branch_0008')
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er10 += 0x01
        cpu.r9 += 0xFF
        cpu.compare(cpu.r9, 0x00)
        if cpu.ne:
            cpu.branch('branch_0008')
        cpu.ret()


    @fw.function(native=True, address=0x82420)
    def graph_zero_axis_pixel():
        cpu.label('graph_zero_axis_pixel')
        cpu.push(cpu.lr)
        cpu.push(cpu.er12)
        cpu.call(GRAPH_ZERO_64)
        cpu.jump(0x8238C)


    @fw.function(native=True, address=0x82480)
    def graph_inter_sample_pole():
        cpu.label('graph_inter_sample_pole')
        cpu.push(cpu.lr)
        cpu.push(cpu.er4)
        cpu.push(cpu.er12)
        cpu.r2 = 0x00
        cpu.compare(cpu.r13, 0x00)
        if cpu.eq:
            cpu.branch('branch_005e')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.fp, -19)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('branch_005e')
        cpu.compare(cpu.r12, 0x01)
        if cpu.eq:
            cpu.branch('branch_005e')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.fp, -27)]
        cpu.compare(cpu.r0, 0x1C)
        if cpu.lts:
            cpu.branch('branch_002e')
        cpu.r1 = cpu.mem8[cpu.offset(cpu.fp, -20)]
        cpu.compare(cpu.r1, 0x03)
        if cpu.gts:
            cpu.branch('branch_005e')
        cpu.r1 = cpu.mem8[cpu.offset(cpu.fp, -18)]
        cpu.compare(cpu.r1, cpu.r0)
        if cpu.ges:
            cpu.branch('branch_005e')
        cpu.r13 = 0x01
        cpu.jump('branch_0040')
        cpu.label('branch_002e')
        cpu.compare(cpu.r0, 0x03)
        if cpu.gts:
            cpu.branch('branch_005e')
        cpu.r1 = cpu.mem8[cpu.offset(cpu.fp, -20)]
        cpu.compare(cpu.r1, 0x1C)
        if cpu.lts:
            cpu.branch('branch_005e')
        cpu.r1 = cpu.mem8[cpu.offset(cpu.fp, -18)]
        cpu.compare(cpu.r1, cpu.r0)
        if cpu.les:
            cpu.branch('branch_005e')
        cpu.r13 = 0x02
        cpu.label('branch_0040')
        cpu.er4 += 0x14
        cpu.call(GRAPH_Y_PIXEL_64)
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('branch_005e')
        cpu.r1 = cpu.mem8[cpu.offset(cpu.fp, -20)]
        cpu.compare(cpu.r13, 0x01)
        if cpu.eq:
            cpu.branch('branch_0058')
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.ges:
            cpu.branch('branch_005e')
        cpu.jump('branch_005c')
        cpu.label('branch_0058')
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.les:
            cpu.branch('branch_005e')
        cpu.label('branch_005c')
        cpu.r2 = 0x01
        cpu.label('branch_005e')
        cpu.pop(cpu.er12)
        cpu.pop(cpu.er4)
        cpu.pop(cpu.lr)
        cpu.ret()


    @fw.function(native=True, address=0x82500)
    def graph_plot_sample():
        cpu.label('graph_plot_sample')
        cpu.push(cpu.lr)
        cpu.mem8[cpu.offset(cpu.fp, -20)] = cpu.r0
        cpu.compare(cpu.r13, 0x00)
        if cpu.eq:
            cpu.branch('branch_002e')
        cpu.call(GRAPH_INTER_SAMPLE_POLE)
        cpu.compare(cpu.r2, 0x00)
        if cpu.eq:
            cpu.branch('branch_0016')
        cpu.r13 = 0x00
        cpu.jump('branch_002e')
        cpu.label('branch_0016')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.fp, -27)]
        cpu.mem8[cpu.offset(cpu.fp, -18)] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[cpu.offset(cpu.fp, -19)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.fp, -26)]
        cpu.r1 = cpu.mem8[cpu.offset(cpu.fp, -28)]
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.ne:
            cpu.branch('branch_0032')
        cpu.call(GRAPH_SAME_COLUMN_SPAN)
        cpu.jump('branch_0032')
        cpu.label('branch_002e')
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.fp, -19)] = cpu.r0
        cpu.label('branch_0032')
        cpu.r1 = cpu.mem8[cpu.offset(cpu.fp, -20)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.fp, -28)]
        cpu.call(GRAPH_LINE)
        cpu.pop(cpu.lr)
        cpu.ret()


    @fw.function(native=True, address=0x825A0)
    def graph_same_column_span():
        cpu.label('graph_same_column_span')
        cpu.push(cpu.lr)
        cpu.r6 = cpu.mem8[cpu.offset(cpu.fp, -28)]
        cpu.r7 = cpu.mem8[cpu.offset(cpu.fp, -27)]
        cpu.r9 = cpu.mem8[cpu.offset(cpu.fp, -20)]
        cpu.label('branch_0008')
        cpu.compare(cpu.r7, cpu.r9)
        if cpu.eq:
            cpu.branch('branch_0022')
        if cpu.lts:
            cpu.branch('branch_0014')
        cpu.r7 += 0xFF
        cpu.jump('branch_0016')
        cpu.label('branch_0014')
        cpu.r7 += 0x01
        cpu.label('branch_0016')
        cpu.r0 = cpu.r6
        cpu.r1 = cpu.r7
        cpu.call(0x0431C)
        cpu.jump('branch_0008')
        cpu.label('branch_0022')
        cpu.pop(cpu.lr)
        cpu.ret()
