"""Fixed-layout e5800p graphics routines and tables."""

from kits import cpu

ROM_REFRESH = 0x043BE
SMALL_TEXT_ADDRESS = 0xF9000
ROM_DRAW_TEXT = 0x041DA


def install(fw):
    @fw.function(native=True, address=0xFC530)
    def basic_graphics():
        cpu.label('basic_graphics')
        cpu.push(cpu.er0)
        cpu.er0 = cpu.sp
        cpu.compare(cpu.r0, 0x52)
        cpu.compare_carry(cpu.r1, 0x83)
        if cpu.ge:
            cpu.branch('stack_ok')
        cpu.pop(cpu.er0)
        cpu.er0 = 0x06
        cpu.ret()
        cpu.label('stack_ok')
        cpu.pop(cpu.er0)
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.sp += -80
        cpu.er14 = cpu.sp
        cpu.mem16[cpu.offset(cpu.er14, 0x0000)] = cpu.er4
        cpu.mem8[cpu.offset(cpu.er14, 0x0002)] = cpu.r0
        cpu.er12 = cpu.er2
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er12, 0x0000)]
        cpu.mem16[cpu.offset(cpu.er14, 0x0004)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er12, 0x0004)]
        cpu.mem16[cpu.offset(cpu.er14, 0x0006)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er12, 0x0008)]
        cpu.mem16[cpu.offset(cpu.er14, 0x0008)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er12, 0x000C)]
        cpu.mem16[cpu.offset(cpu.er14, 0x000A)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er12, 0x0010)]
        cpu.mem16[cpu.offset(cpu.er14, 0x000C)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er12, 0x0014)]
        cpu.mem16[cpu.offset(cpu.er14, 0x000E)] = cpu.er0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er12, 0x0012)]
        cpu.mem8[cpu.offset(cpu.er14, 0x001E)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0002)]
        cpu.compare(cpu.r0, 0x10)
        if cpu.ne:
            cpu.branch('skip_1')
        cpu.jump('cls')
        cpu.label('skip_1')
        cpu.compare(cpu.r0, 0x11)
        if cpu.ne:
            cpu.branch('skip_2')
        cpu.jump('pset')
        cpu.label('skip_2')
        cpu.compare(cpu.r0, 0x0C)
        if cpu.ne:
            cpu.branch('skip_3')
        cpu.jump('point')
        cpu.label('skip_3')
        cpu.compare(cpu.r0, 0x12)
        if cpu.ne:
            cpu.branch('skip_4')
        cpu.jump('line')
        cpu.label('skip_4')
        cpu.compare(cpu.r0, 0x13)
        if cpu.ne:
            cpu.branch('skip_5')
        cpu.jump('line')
        cpu.label('skip_5')
        cpu.compare(cpu.r0, 0x14)
        if cpu.ne:
            cpu.branch('skip_6')
        cpu.jump('blit')
        cpu.label('skip_6')
        cpu.compare(cpu.r0, 0x15)
        if cpu.ne:
            cpu.branch('skip_7')
        cpu.jump('text')
        cpu.label('skip_7')
        cpu.compare(cpu.r0, 0x16)
        if cpu.ne:
            cpu.branch('skip_8')
        cpu.jump('refresh')
        cpu.label('skip_8')
        cpu.jump('argument')
        cpu.label('cls')
        cpu.r8 = 0xEC
        cpu.r9 = 0x80
        cpu.r10 = 0x74
        cpu.r11 = 0x01
        cpu.r0 = 0x00
        cpu.label('cls_byte')
        cpu.mem8[cpu.er8] = cpu.r0
        cpu.er8 += 0x01
        cpu.er10 += -1
        if cpu.ne:
            cpu.branch('cls_byte')
        cpu.jump('success')
        cpu.label('refresh')
        cpu.call(ROM_REFRESH)
        cpu.jump('success')
        cpu.label('pset')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0008)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_9')
        cpu.jump('argument')
        cpu.label('skip_9')
        cpu.compare(cpu.r0, 0x03)
        if cpu.lt:
            cpu.branch('skip_10')
        cpu.jump('argument')
        cpu.label('skip_10')
        cpu.mem8[cpu.offset(cpu.er14, 0x0003)] = cpu.r0
        cpu.jump('point_bounds')
        cpu.label('point')
        cpu.r0 = 0x03
        cpu.mem8[cpu.offset(cpu.er14, 0x0003)] = cpu.r0
        cpu.label('point_bounds')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0004)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_11')
        cpu.jump('success')
        cpu.label('skip_11')
        cpu.compare(cpu.r0, 0x60)
        if cpu.lt:
            cpu.branch('skip_12')
        cpu.jump('success')
        cpu.label('skip_12')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0006)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_13')
        cpu.jump('success')
        cpu.label('skip_13')
        cpu.compare(cpu.r0, 0x1F)
        if cpu.lt:
            cpu.branch('skip_14')
        cpu.jump('success')
        cpu.label('skip_14')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0004)]
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, 0x0006)]
        cpu.r2 = cpu.mem8[cpu.offset(cpu.er14, 0x0003)]
        cpu.call('pixel')
        cpu.jump('value')
        cpu.label('line')
        cpu.label('rect')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x000C)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_15')
        cpu.jump('argument')
        cpu.label('skip_15')
        cpu.compare(cpu.r0, 0x03)
        if cpu.lt:
            cpu.branch('skip_16')
        cpu.jump('argument')
        cpu.label('skip_16')
        cpu.mem8[cpu.offset(cpu.er14, 0x0003)] = cpu.r0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0004)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_17')
        cpu.jump('argument')
        cpu.label('skip_17')
        cpu.compare(cpu.r0, 0x60)
        if cpu.lt:
            cpu.branch('skip_18')
        cpu.jump('argument')
        cpu.label('skip_18')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0006)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_19')
        cpu.jump('argument')
        cpu.label('skip_19')
        cpu.compare(cpu.r0, 0x1F)
        if cpu.lt:
            cpu.branch('skip_20')
        cpu.jump('argument')
        cpu.label('skip_20')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0008)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_21')
        cpu.jump('argument')
        cpu.label('skip_21')
        cpu.compare(cpu.r0, 0x60)
        if cpu.lt:
            cpu.branch('skip_22')
        cpu.jump('argument')
        cpu.label('skip_22')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x000A)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_23')
        cpu.jump('argument')
        cpu.label('skip_23')
        cpu.compare(cpu.r0, 0x1F)
        if cpu.lt:
            cpu.branch('skip_24')
        cpu.jump('argument')
        cpu.label('skip_24')
        cpu.r8 = cpu.mem8[cpu.offset(cpu.er14, 0x0004)]
        cpu.r9 = cpu.mem8[cpu.offset(cpu.er14, 0x0006)]
        cpu.r10 = cpu.mem8[cpu.offset(cpu.er14, 0x0008)]
        cpu.r11 = cpu.mem8[cpu.offset(cpu.er14, 0x000A)]
        cpu.r12 = cpu.mem8[cpu.offset(cpu.er14, 0x0003)]
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0002)]
        cpu.compare(cpu.r0, 0x13)
        if cpu.ne:
            cpu.branch('skip_25')
        cpu.jump('rectangle')
        cpu.label('skip_25')
        cpu.er4 = 0x00
        cpu.r4 = cpu.r10
        cpu.er0 = 0x00
        cpu.r0 = cpu.r8
        cpu.r4 -= cpu.r0
        cpu.sub_carry(cpu.r5, cpu.r1)
        cpu.er2 = 0x01
        if cpu.ge:
            cpu.branch('dx_ready')
        cpu.er4 = 0x00
        cpu.r4 = cpu.r8
        cpu.r0 = cpu.r10
        cpu.r4 -= cpu.r0
        cpu.sub_carry(cpu.r5, cpu.r1)
        cpu.r2 = 0xFF
        cpu.r3 = 0xFF
        cpu.label('dx_ready')
        cpu.mem16[cpu.offset(cpu.er14, 0x0016)] = cpu.er2
        cpu.er6 = 0x00
        cpu.r6 = cpu.r9
        cpu.er0 = 0x00
        cpu.r0 = cpu.r11
        cpu.r6 -= cpu.r0
        cpu.sub_carry(cpu.r7, cpu.r1)
        cpu.er2 = 0x01
        if cpu.lt:
            cpu.branch('dy_ready')
        cpu.er6 = 0x00
        cpu.r6 = cpu.r11
        cpu.r0 = cpu.r9
        cpu.r6 -= cpu.r0
        cpu.sub_carry(cpu.r7, cpu.r1)
        cpu.r2 = 0xFF
        cpu.r3 = 0xFF
        cpu.label('dy_ready')
        cpu.mem16[cpu.offset(cpu.er14, 0x0018)] = cpu.er2
        cpu.er0 = cpu.er4
        cpu.er0 += cpu.er6
        cpu.mem16[cpu.offset(cpu.er14, 0x001A)] = cpu.er0
        cpu.label('line_pixel')
        cpu.r0 = cpu.r8
        cpu.r1 = cpu.r9
        cpu.r2 = cpu.r12
        cpu.call('pixel')
        cpu.r0 = cpu.r8
        cpu.compare(cpu.r0, cpu.r10)
        if cpu.ne:
            cpu.branch('skip_26')
        cpu.r0 = cpu.r9
        cpu.compare(cpu.r0, cpu.r11)
        if cpu.ne:
            cpu.branch('skip_26')
        cpu.jump('success')
        cpu.label('skip_26')
        cpu.label('line_step')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x001A)]
        cpu.er0 += cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 0x001C)] = cpu.er0
        cpu.compare(cpu.er0, cpu.er6)
        if cpu.lts:
            cpu.branch('line_y')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x001A)]
        cpu.er0 += cpu.er6
        cpu.mem16[cpu.offset(cpu.er14, 0x001A)] = cpu.er0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0016)]
        cpu.r8 += cpu.r0
        cpu.label('line_y')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x001C)]
        cpu.compare(cpu.er4, cpu.er0)
        if cpu.lts:
            cpu.branch('line_pixel')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x001A)]
        cpu.er0 += cpu.er4
        cpu.mem16[cpu.offset(cpu.er14, 0x001A)] = cpu.er0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0018)]
        cpu.r9 += cpu.r0
        cpu.jump('line_pixel')
        cpu.label('rectangle')
        cpu.compare(cpu.r8, cpu.r10)
        if cpu.lt:
            cpu.branch('rect_x')
        cpu.r0 = cpu.r8
        cpu.r8 = cpu.r10
        cpu.r10 = cpu.r0
        cpu.label('rect_x')
        cpu.compare(cpu.r9, cpu.r11)
        if cpu.lt:
            cpu.branch('rect_y')
        cpu.r0 = cpu.r9
        cpu.r9 = cpu.r11
        cpu.r11 = cpu.r0
        cpu.label('rect_y')
        cpu.r13 = cpu.r8
        cpu.mem8[cpu.offset(cpu.er14, 0x0012)] = cpu.r9
        cpu.label('rect_horizontal')
        cpu.r0 = cpu.r8
        cpu.r1 = cpu.r9
        cpu.r2 = cpu.r12
        cpu.call('pixel')
        cpu.compare(cpu.r9, cpu.r11)
        if cpu.eq:
            cpu.branch('rect_next_x')
        cpu.r9 = cpu.r11
        cpu.r0 = cpu.r8
        cpu.r1 = cpu.r9
        cpu.r2 = cpu.r12
        cpu.call('pixel')
        cpu.r9 = cpu.mem8[cpu.offset(cpu.er14, 0x0012)]
        cpu.label('rect_next_x')
        cpu.compare(cpu.r8, cpu.r10)
        if cpu.eq:
            cpu.branch('rect_sides')
        cpu.r8 += 0x01
        cpu.jump('rect_horizontal')
        cpu.label('rect_sides')
        cpu.r9 += 0x01
        cpu.compare(cpu.r9, cpu.r11)
        if cpu.lt:
            cpu.branch('skip_27')
        cpu.jump('success')
        cpu.label('skip_27')
        cpu.r8 = cpu.r13
        cpu.r0 = cpu.r8
        cpu.r1 = cpu.r9
        cpu.r2 = cpu.r12
        cpu.call('pixel')
        cpu.compare(cpu.r8, cpu.r10)
        if cpu.eq:
            cpu.branch('rect_sides')
        cpu.r8 = cpu.r10
        cpu.r0 = cpu.r8
        cpu.r1 = cpu.r9
        cpu.r2 = cpu.r12
        cpu.call('pixel')
        cpu.jump('rect_sides')
        cpu.label('blit')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x000E)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_28')
        cpu.jump('argument')
        cpu.label('skip_28')
        cpu.compare(cpu.r0, 0x03)
        if cpu.lt:
            cpu.branch('skip_29')
        cpu.jump('argument')
        cpu.label('skip_29')
        cpu.mem8[cpu.offset(cpu.er14, 0x0003)] = cpu.r0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0004)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_30')
        cpu.jump('argument')
        cpu.label('skip_30')
        cpu.compare(cpu.r0, 0x60)
        if cpu.lt:
            cpu.branch('skip_31')
        cpu.jump('argument')
        cpu.label('skip_31')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0006)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_32')
        cpu.jump('argument')
        cpu.label('skip_32')
        cpu.compare(cpu.r0, 0x1F)
        if cpu.lt:
            cpu.branch('skip_33')
        cpu.jump('argument')
        cpu.label('skip_33')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0008)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_34')
        cpu.jump('argument')
        cpu.label('skip_34')
        cpu.compare(cpu.r0, 0x61)
        if cpu.lt:
            cpu.branch('skip_35')
        cpu.jump('argument')
        cpu.label('skip_35')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x000A)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_36')
        cpu.jump('argument')
        cpu.label('skip_36')
        cpu.compare(cpu.r0, 0x21)
        if cpu.lt:
            cpu.branch('skip_37')
        cpu.jump('argument')
        cpu.label('skip_37')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0008)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_38')
        cpu.jump('argument')
        cpu.label('skip_38')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x000A)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_39')
        cpu.jump('argument')
        cpu.label('skip_39')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0008)]
        cpu.r0 += 0x07
        cpu.r0 >>= 0x03
        cpu.r2 = cpu.mem8[cpu.offset(cpu.er14, 0x000A)]
        cpu.multiply(cpu.er0, cpu.r2)
        cpu.mem16[cpu.offset(cpu.er14, 0x0010)] = cpu.er0
        cpu.er4 = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x000C)]
        cpu.r2 = cpu.mem8[cpu.offset(cpu.er14, 0x001E)]
        cpu.call(0xFB53C)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_40')
        cpu.jump('argument')
        cpu.label('skip_40')
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x000C)]
        cpu.r10 = cpu.mem8[cpu.offset(cpu.er14, 0x001E)]
        cpu.compare(cpu.r10, 0x00)
        if cpu.ne:
            cpu.branch('blit_ready')
        cpu.r0 = 0x60
        cpu.r1 = 0x82
        cpu.compare(cpu.er8, cpu.er0)
        if cpu.ge:
            cpu.branch('blit_ready')
        cpu.er0 = cpu.er8
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er14, 0x0010)]
        cpu.er0 += cpu.er2
        cpu.r2 = 0xED
        cpu.r3 = 0x80
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('blit_ready')
        cpu.er0 = cpu.sp
        cpu.r2 = 0x36
        cpu.r3 = 0x84
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_41')
        cpu.jump('memory')
        cpu.label('skip_41')
        cpu.sp += -128
        cpu.sp += -128
        cpu.sp += -128
        cpu.er4 = cpu.sp
        cpu.er6 = cpu.mem16[cpu.offset(cpu.er14, 0x0010)]
        cpu.label('snapshot')
        cpu.r0 = cpu.mem8[cpu.er8]
        cpu.mem8[cpu.er4] = cpu.r0
        cpu.er8 += 0x01
        cpu.er4 += 0x01
        cpu.er6 += -1
        if cpu.ne:
            cpu.branch('snapshot')
        cpu.er8 = cpu.sp
        cpu.label('blit_ready')
        cpu.r13 = 0x00
        cpu.label('blit_row')
        cpu.r12 = 0x00
        cpu.label('blit_column')
        cpu.r0 = cpu.r12
        cpu.r0 &= 0x07
        if cpu.ne:
            cpu.branch('blit_bit')
        # The source bank must prefix each byte read, including SRAM snapshots.
        cpu.r11 = cpu.mem8[cpu.r10, cpu.er8]
        cpu.er8 += 0x01
        if cpu.ne:
            cpu.branch('blit_bit')
        cpu.r10 += 0x01
        cpu.label('blit_bit')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0004)]
        cpu.r0 += cpu.r12
        cpu.compare(cpu.r0, 0x60)
        if cpu.ge:
            cpu.branch('blit_next')
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, 0x0006)]
        cpu.r1 += cpu.r13
        cpu.compare(cpu.r1, 0x1F)
        if cpu.ge:
            cpu.branch('blit_next')
        cpu.r2 = cpu.mem8[cpu.offset(cpu.er14, 0x0003)]
        cpu.compare(cpu.r11, 0x80)
        if cpu.ge:
            cpu.branch('blit_set')
        cpu.compare(cpu.r2, 0x00)
        if cpu.ne:
            cpu.branch('blit_next')
        cpu.jump('blit_plot')
        cpu.label('blit_set')
        cpu.compare(cpu.r2, 0x00)
        if cpu.ne:
            cpu.branch('blit_plot')
        cpu.r2 = 0x01
        cpu.label('blit_plot')
        cpu.call('pixel')
        cpu.label('blit_next')
        cpu.r11 <<= 0x01
        cpu.r12 += 0x01
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0008)]
        cpu.compare(cpu.r12, cpu.r0)
        if cpu.lt:
            cpu.branch('blit_column')
        cpu.r13 += 0x01
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x000A)]
        cpu.compare(cpu.r13, cpu.r0)
        if cpu.lt:
            cpu.branch('blit_row')
        cpu.jump('success')
        cpu.label('text')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0004)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_42')
        cpu.jump('argument')
        cpu.label('skip_42')
        cpu.compare(cpu.r0, 0x60)
        if cpu.lt:
            cpu.branch('skip_43')
        cpu.jump('argument')
        cpu.label('skip_43')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x000A)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_44')
        cpu.jump('argument')
        cpu.label('skip_44')
        cpu.compare(cpu.r0, 0x02)
        if cpu.lt:
            cpu.branch('skip_45')
        cpu.jump('argument')
        cpu.label('skip_45')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x000A)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('text_regular_bounds')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0006)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_46')
        cpu.jump('argument')
        cpu.label('skip_46')
        cpu.compare(cpu.r0, 0x1B)
        if cpu.lt:
            cpu.branch('skip_47')
        cpu.jump('argument')
        cpu.label('skip_47')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0004)]
        cpu.r0 &= 0x03
        if cpu.eq:
            cpu.branch('skip_48')
        cpu.jump('argument')
        cpu.label('skip_48')
        cpu.jump('skip_50')
        cpu.label('text_regular_bounds')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 0x0006)]
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_49')
        cpu.jump('argument')
        cpu.label('skip_49')
        cpu.compare(cpu.r0, 0x19)
        if cpu.lt:
            cpu.branch('skip_50')
        cpu.jump('argument')
        cpu.label('skip_50')
        cpu.label('text_copy')
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, 0x0008)]
        cpu.er10 = cpu.er14
        cpu.er10 += 0x20
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, 0x000C)]
        cpu.compare(cpu.r6, 0x21)
        if cpu.lt:
            cpu.branch('skip_51')
        cpu.jump('argument')
        cpu.label('skip_51')
        cpu.compare(cpu.r6, 0x00)
        if cpu.eq:
            cpu.branch('text_nul')
        cpu.label('text_byte')
        cpu.r0 = cpu.mem8[cpu.er8]
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er8 += 0x01
        cpu.er10 += 0x01
        cpu.r6 += 0xFF
        if cpu.ne:
            cpu.branch('text_byte')
        cpu.label('text_nul')
        cpu.r0 = 0x00
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A0]
        cpu.mem8[cpu.offset(cpu.er14, 0x0042)] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A1]
        cpu.mem8[cpu.offset(cpu.er14, 0x0043)] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A2]
        cpu.mem8[cpu.offset(cpu.er14, 0x0044)] = cpu.r0
        cpu.r0 = 0x07
        cpu.mem8[0x80A0] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[0x80A1] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x80A2] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x000A)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('text_rom')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0004)]
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, 0x0006)]
        cpu.r1 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.call(SMALL_TEXT_ADDRESS)
        cpu.jump('text_restore')
        cpu.label('text_rom')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0004)]
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, 0x0006)]
        cpu.r1 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.call(ROM_DRAW_TEXT)
        cpu.r8 = cpu.r0
        cpu.r1 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += 0x20
        cpu.er2 += cpu.er0
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_52')
        cpu.jump('text_restore')
        cpu.label('skip_52')
        cpu.mem8[cpu.offset(cpu.er14, 0x0046)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 0x0047)] = cpu.r0
        cpu.r0 = cpu.r8
        cpu.r2 = 0x06
        cpu.multiply(cpu.er0, cpu.r2)
        cpu.r2 = cpu.mem8[cpu.offset(cpu.er14, 0x0004)]
        cpu.r0 += cpu.r2
        cpu.compare(cpu.r0, 0x60)
        if cpu.lt:
            cpu.branch('skip_53')
        cpu.jump('text_restore')
        cpu.label('skip_53')
        cpu.r12 = cpu.r0
        cpu.r12 &= 0x07
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0006)]
        cpu.r2 = 0x0C
        cpu.multiply(cpu.er0, cpu.r2)
        cpu.r8 = 0xEC
        cpu.r9 = 0x80
        cpu.er8 += cpu.er0
        cpu.er10 = cpu.er14
        cpu.er10 += 0x10
        cpu.r13 = 0x07
        cpu.label('text_save_edge')
        cpu.r0 = cpu.mem8[cpu.er8]
        cpu.mem8[cpu.er10] = cpu.r0
        cpu.er8 += 0x0C
        cpu.er10 += 0x01
        cpu.r13 += 0xFF
        if cpu.ne:
            cpu.branch('text_save_edge')
        cpu.r0 = 0x00
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, 0x0006)]
        cpu.r1 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 0x23
        cpu.er2 += 0x23
        cpu.call(ROM_DRAW_TEXT)
        cpu.er8 += -60
        cpu.er8 += -24
        cpu.er10 = cpu.er14
        cpu.er10 += 0x10
        cpu.r13 = 0x07
        cpu.label('text_merge_edge')
        cpu.r0 = cpu.mem8[cpu.er8]
        cpu.r1 = cpu.mem8[cpu.er10]
        cpu.mem8[cpu.er8] = cpu.r1
        cpu.r0 >>= cpu.r12
        cpu.r1 = 0xFF
        cpu.r1 >>= cpu.r12
        cpu.r1 ^= 0xFF
        cpu.er2 = cpu.er8
        cpu.er2 += 0x0B
        cpu.r3 = cpu.mem8[cpu.er2]
        cpu.r3 &= cpu.r1
        cpu.r0 |= cpu.r3
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er8 += 0x0C
        cpu.er10 += 0x01
        cpu.r13 += 0xFF
        if cpu.ne:
            cpu.branch('text_merge_edge')
        cpu.label('text_restore')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0042)]
        cpu.mem8[0x80A0] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0043)]
        cpu.mem8[0x80A1] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 0x0044)]
        cpu.mem8[0x80A2] = cpu.r0
        cpu.jump('success')
        cpu.label('argument')
        cpu.er0 = 0x04
        cpu.jump('exit')
        cpu.label('memory')
        cpu.er0 = 0x06
        cpu.jump('exit')
        cpu.label('success')
        cpu.r0 = 0x00
        cpu.label('value')
        cpu.r1 = 0x00
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er14, 0x0000)]
        cpu.mem16[cpu.er2] = cpu.er0
        cpu.er2 += 0x02
        cpu.er0 = 0x00
        cpu.mem16[cpu.er2] = cpu.er0
        cpu.label('exit')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x28
        cpu.er2 += 0x28
        cpu.sp = cpu.er2
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('pixel')
        cpu.push(cpu.xr4)
        cpu.r6 = cpu.r2
        cpu.r2 = cpu.r0
        cpu.r2 &= 0x07
        cpu.r3 = 0x80
        cpu.r3 >>= cpu.r2
        cpu.r4 = cpu.r1
        cpu.r1 = 0x00
        cpu.r0 >>= 0x03
        cpu.r2 = 0x0C
        cpu.multiply(cpu.er4, cpu.r2)
        cpu.er4 += cpu.er0
        cpu.r0 = 0xEC
        cpu.r1 = 0x80
        cpu.er4 += cpu.er0
        cpu.r0 = cpu.mem8[cpu.er4]
        cpu.compare(cpu.r6, 0x03)
        if cpu.eq:
            cpu.branch('pixel_query')
        cpu.compare(cpu.r6, 0x00)
        if cpu.eq:
            cpu.branch('pixel_clear')
        cpu.compare(cpu.r6, 0x01)
        if cpu.eq:
            cpu.branch('pixel_set')
        cpu.r0 ^= cpu.r3
        cpu.jump('pixel_write')
        cpu.label('pixel_set')
        cpu.r0 |= cpu.r3
        cpu.jump('pixel_write')
        cpu.label('pixel_clear')
        cpu.r3 ^= 0xFF
        cpu.r0 &= cpu.r3
        cpu.label('pixel_write')
        cpu.mem8[cpu.er4] = cpu.r0
        cpu.r0 = 0x00
        cpu.jump('pixel_done')
        cpu.label('pixel_query')
        cpu.r0 &= cpu.r3
        if cpu.eq:
            cpu.branch('pixel_done')
        cpu.r0 = 0x01
        cpu.label('pixel_done')
        cpu.pop(cpu.xr4)
        cpu.ret()
