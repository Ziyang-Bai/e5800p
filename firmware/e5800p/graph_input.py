"""Native token editing and formula access for GRAPH."""

from kits import cpu


def install(fw):
    @fw.function(native=True)
    def graph_formula_get():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.sp += -16
        cpu.er10 = cpu.sp
        cpu.er0 = 0
        cpu.er2 = cpu.er10
        cpu.r4 = 8
        cpu.label('clear')
        cpu.mem16[0, cpu.er2] = cpu.er0
        cpu.er2 += 2
        cpu.r4 += 255
        if cpu.ne:
            cpu.branch('clear')
        cpu.er12 = cpu.er10
        cpu.er12 += 12
        cpu.r4 = 4
        cpu.label('outputs')
        cpu.er0 = 0
        cpu.push(cpu.er0)
        cpu.push(cpu.er12)
        cpu.er12 += -4
        cpu.r4 += 255
        if cpu.ne:
            cpu.branch('outputs')
        cpu.er0 = 1
        cpu.push(cpu.er0)
        cpu.er0 = 0xE736
        cpu.push(cpu.er0)
        cpu.er0 = 0xE798
        cpu.r2 = 1
        cpu.call(0x1A574)
        cpu.sp += 20
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('empty')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er10, 8)]
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er10, 10)]
        cpu.mem16[0, cpu.er8] = cpu.er0
        cpu.mem8[0, cpu.offset(cpu.er8, 2)] = cpu.r2
        cpu.r3 = 0
        cpu.mem8[0, cpu.offset(cpu.er8, 3)] = cpu.r3
        cpu.call(0x106DA)
        cpu.er0 += 1
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er10, 12)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.gt:
            cpu.branch('empty')
        cpu.mem16[0, cpu.offset(cpu.er8, 4)] = cpu.er0
        cpu.er0 = 0
        cpu.branch('out')
        cpu.label('empty')
        cpu.er0 = 0
        cpu.mem16[0, cpu.er8] = cpu.er0
        cpu.mem16[0, cpu.offset(cpu.er8, 2)] = cpu.er0
        cpu.mem16[0, cpu.offset(cpu.er8, 4)] = cpu.er0
        cpu.r0 = 4
        cpu.label('out')
        cpu.sp += 16
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_input_tokens():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        # ER6 is an optional bank-0 caption, outside the native edit frame.
        cpu.push(cpu.er6)
        cpu.er8 = cpu.er0
        cpu.r10 = cpu.r2
        cpu.sp += -44
        cpu.er14 = cpu.sp
        cpu.er0 = 0
        cpu.er2 = cpu.er14
        cpu.r4 = 22
        cpu.label('clear')
        cpu.mem16[0, cpu.er2] = cpu.er0
        cpu.er2 += 2
        cpu.r4 += 255
        if cpu.ne:
            cpu.branch('clear')
        cpu.er0 = cpu.mem16[0, 0x8086]
        cpu.mem16[0, cpu.offset(cpu.er14, 42)] = cpu.er0
        cpu.er0 = cpu.er14
        cpu.call(0x1ED76)
        cpu.er8 = cpu.er8
        if cpu.eq:
            cpu.branch('draw')
        cpu.r0 = cpu.r10
        cpu.r1 = 0
        cpu.push(cpu.er0)
        cpu.push(cpu.er8)
        cpu.er0 = 0x72A2
        cpu.r2 = 4
        cpu.call(0x108CA)
        cpu.sp += 4
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 17)]
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('length')
        cpu.er0 = 4
        cpu.push(cpu.er0)
        cpu.er0 = 0x73A2
        cpu.push(cpu.er0)
        cpu.er0 = 4
        cpu.push(cpu.er0)
        cpu.er0 = 0x72A2
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.r2 = 0
        cpu.r3 = 2
        cpu.call(0xD4C74)
        cpu.sp += 8
        cpu.er0 = 4
        cpu.push(cpu.er0)
        cpu.er0 = 0x73A2
        cpu.push(cpu.er0)
        cpu.er0 = 0x72A2
        cpu.r2 = 4
        cpu.call(0x108CA)
        cpu.sp += 4
        cpu.label('length')
        cpu.er0 = 0x72A2
        cpu.r2 = 4
        cpu.call(0x106DA)
        cpu.mem16[0, cpu.er14] = cpu.er0
        cpu.label('draw')
        cpu.call(0x0409A)
        cpu.er0 = cpu.er14
        cpu.call(0xCBF98)
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, 44)]
        cpu.er2 = cpu.er2
        if cpu.eq:
            cpu.branch('caption_done')
        cpu.r0 = 0
        cpu.r1 = 25
        cpu.call(0x041DA)
        cpu.label('caption_done')
        cpu.call(0x043BE)
        cpu.er0 = cpu.er14
        cpu.er0 += 6
        cpu.call(0x12576)
        cpu.r4 = cpu.r0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 6)]
        cpu.compare(cpu.r0, 0x32)
        cpu.compare_carry(cpu.r1, 0x75)
        if cpu.eq:
            cpu.branch('cancel')
        cpu.compare(cpu.r0, 0x34)
        cpu.compare_carry(cpu.r1, 0x75)
        if cpu.eq:
            cpu.branch('confirm')
        cpu.compare(cpu.r4, 0)
        if cpu.ne:
            cpu.branch('insert')
        cpu.compare(cpu.r1, 0x7D)
        if cpu.eq:
            cpu.compare(cpu.r0, 2)
            if cpu.ne:
                cpu.branch('draw')
            cpu.er0 = cpu.er14
            cpu.er0 += 6
            cpu.r2 = 1
            cpu.call(0xDF3FA)
            cpu.r4 = cpu.r0
            cpu.branch('insert')
        cpu.compare(cpu.r1, 0x75)
        if cpu.ne:
            cpu.branch('draw')
        cpu.compare(cpu.r0, 0x3F)
        if cpu.eq:
            cpu.er0 = cpu.er14
            cpu.call(0x1ED76)
            cpu.branch('draw')
        cpu.compare(cpu.r0, 0x42)
        if cpu.eq:
            cpu.branch('move')
        cpu.compare(cpu.r0, 0x44)
        if cpu.eq:
            cpu.branch('move')
        cpu.compare(cpu.r0, 0x45)
        if cpu.eq:
            cpu.branch('move')
        cpu.compare(cpu.r0, 0x47)
        if cpu.eq:
            cpu.branch('move')
        cpu.compare(cpu.r0, 0x49)
        if cpu.ne:
            cpu.branch('draw')
        cpu.label('move')
        cpu.er0 = cpu.er14
        cpu.call(0xD72E4)
        cpu.branch('draw')
        cpu.label('insert')
        cpu.r2 = cpu.r4
        cpu.r3 = 0
        cpu.er0 = cpu.er14
        cpu.er0 += 6
        cpu.call(0x0790E)
        cpu.compare(cpu.r0, 1)
        if cpu.ne:
            cpu.branch('draw')
        cpu.er0 = cpu.er14
        cpu.call(0xD5EAE)
        cpu.branch('draw')
        cpu.label('confirm')
        cpu.er0 = 0x72A2
        cpu.r2 = 4
        cpu.call(0x106DA)
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('draw')
        cpu.r3 = cpu.mem8[0, cpu.offset(cpu.er14, 17)]
        cpu.r3 <<= 1
        cpu.r3 |= 1
        cpu.branch('done')
        cpu.label('cancel')
        cpu.r3 = 0
        cpu.label('done')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 42)]
        cpu.mem16[0, 0x8086] = cpu.er0
        cpu.er0 = 0x72A2
        cpu.r2 = 4
        cpu.sp += 44
        cpu.pop(cpu.er6)
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_formula_edit():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.sp += -8
        cpu.er14 = cpu.sp
        cpu.er0 = cpu.er14
        cpu.call('fn_graph_formula_get')
        cpu.er0 = cpu.mem16[0, cpu.er14]
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, 2)]
        cpu.er6 = 0
        cpu.call('fn_graph_input_tokens')
        cpu.compare(cpu.r3, 0)
        if cpu.eq:
            cpu.branch('cancel')
        cpu.r3 >>= 1
        cpu.mem8[0, cpu.offset(cpu.er14, 6)] = cpu.r3
        cpu.r0 = cpu.r2
        cpu.r1 = 0
        cpu.push(cpu.er0)
        cpu.er0 = 0x72A2
        cpu.push(cpu.er0)
        cpu.r0 = 0x40
        cpu.call(0xE3CCC)
        cpu.sp += 4
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('full')
        cpu.er0 = cpu.er14
        cpu.call(0xE3D38)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('committed')
        cpu.er2 = cpu.mem16[0, cpu.er14]
        cpu.r1 = cpu.mem8[0, cpu.offset(cpu.er14, 2)]
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 6)]
        cpu.mem8[cpu.r1, cpu.er2] = cpu.r0
        cpu.label('committed')
        cpu.r0 = 1
        cpu.branch('out')
        cpu.label('full')
        cpu.r0 = 2
        cpu.branch('out')
        cpu.label('cancel')
        cpu.r0 = 0
        cpu.label('out')
        cpu.sp += 8
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_number_input():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.r10 = cpu.r2
        cpu.er12 = cpu.er4
        cpu.sp += -32
        cpu.er14 = cpu.sp
        cpu.er0 = cpu.mem16[0, 0x8086]
        cpu.mem16[0, cpu.offset(cpu.er14, 6)] = cpu.er0
        cpu.er0 = 0
        cpu.r2 = 0
        cpu.label('edit')
        cpu.er6 = cpu.er12
        cpu.call('fn_graph_input_tokens')
        cpu.compare(cpu.r3, 0)
        if cpu.eq:
            cpu.branch('cancel')
        cpu.er0 = 0x72A2
        cpu.r2 = 4
        cpu.er4 = 0x73A2
        cpu.r6 = 4
        cpu.call('fn_graph_tokens_linear')
        cpu.er0 = 0x73A2
        cpu.mem16[0, cpu.er14] = cpu.er0
        cpu.r0 = 4
        cpu.mem8[0, cpu.offset(cpu.er14, 2)] = cpu.r0
        cpu.er0 = 1
        cpu.mem16[0, cpu.offset(cpu.er14, 4)] = cpu.er0
        cpu.er0 = 0
        cpu.push(cpu.er0)
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 12
        cpu.push(cpu.er0)
        cpu.er0 = 0
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 4
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.r2 = 0
        cpu.r3 = 1
        cpu.call(0xC7C12)
        cpu.sp += 10
        cpu.compare(cpu.r0, 1)
        if cpu.ne:
            cpu.branch('retry')
        cpu.er0 = cpu.er14
        cpu.er0 += 12
        cpu.r2 = 0
        cpu.call('fn_graph_scalar')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('retry')
        cpu.er0 = cpu.er14
        cpu.er0 += 12
        cpu.r2 = 0
        cpu.r3 = 20
        cpu.er4 = cpu.er8
        cpu.r6 = cpu.r10
        cpu.call('fn_graph_copy')
        cpu.r0 = 1
        cpu.branch('out')
        cpu.label('retry')
        cpu.er0 = 4
        cpu.push(cpu.er0)
        cpu.er0 = 0x72A2
        cpu.push(cpu.er0)
        cpu.er0 = 0x73A2
        cpu.r2 = 4
        cpu.call(0x108CA)
        cpu.sp += 4
        cpu.er0 = 0x73A2
        cpu.r2 = 4
        cpu.branch('edit')
        cpu.label('cancel')
        cpu.r0 = 0
        cpu.label('out')
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, 6)]
        cpu.mem16[0, 0x8086] = cpu.er2
        cpu.sp += 32
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_text_input():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.er10 = cpu.er2
        cpu.er0 = 0
        cpu.r2 = 0
        cpu.er6 = 0
        cpu.call('fn_graph_input_tokens')
        cpu.compare(cpu.r3, 0)
        if cpu.eq:
            cpu.branch('cancel')
        cpu.er4 = 0x72A2
        cpu.er6 = 0
        cpu.label('copy')
        cpu.r0 = cpu.mem8[4, cpu.er4]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('finish')
        cpu.compare(cpu.r0, 0x20)
        if cpu.lt:
            cpu.branch('cancel')
        cpu.compare(cpu.r0, 0x60)
        if cpu.ge:
            cpu.branch('cancel')
        cpu.compare(cpu.er6, cpu.er10)
        if cpu.ge:
            cpu.branch('finish')
        cpu.mem8[0, cpu.er8] = cpu.r0
        cpu.er8 += 1
        cpu.er4 += 1
        cpu.er6 += 1
        cpu.branch('copy')
        cpu.label('finish')
        cpu.r0 = 0
        cpu.mem8[0, cpu.er8] = cpu.r0
        cpu.er0 = cpu.er6
        cpu.branch('out')
        cpu.label('cancel')
        cpu.er0 = 0
        cpu.label('out')
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_tokens_linear():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.r10 = cpu.r2
        cpu.er12 = cpu.er4
        cpu.r11 = cpu.r6
        cpu.sp += -128
        cpu.sp += -32
        cpu.er14 = cpu.sp
        cpu.er0 = 0
        cpu.er2 = cpu.er14
        cpu.r4 = 21
        cpu.label('clear')
        cpu.mem16[0, cpu.er2] = cpu.er0
        cpu.er2 += 2
        cpu.r4 += 255
        if cpu.ne:
            cpu.branch('clear')
        cpu.er0 = 0x8000
        cpu.er4 = cpu.er14
        cpu.er4 += 44
        cpu.r7 = 112
        cpu.label('save')
        cpu.r2 = cpu.mem8[0, cpu.er0]
        cpu.mem8[0, cpu.er4] = cpu.r2
        cpu.er0 += 1
        cpu.er4 += 1
        cpu.r7 += 255
        if cpu.ne:
            cpu.branch('save')
        cpu.r0 = cpu.mem8[0, 0x8090]
        cpu.mem8[0, cpu.er4] = cpu.r0
        cpu.r0 = 0
        cpu.mem8[0, 0x8090] = cpu.r0
        cpu.r0 = cpu.r11
        cpu.r1 = 0
        cpu.push(cpu.er0)
        cpu.push(cpu.er12)
        cpu.r0 = cpu.r10
        cpu.push(cpu.er0)
        cpu.push(cpu.er8)
        cpu.er0 = cpu.er14
        cpu.r2 = 0
        cpu.r3 = 1
        cpu.call(0xD4C74)
        cpu.sp += 8
        cpu.er0 = cpu.er12
        cpu.r2 = cpu.r11
        cpu.call(0x106DA)
        cpu.er8 = cpu.er0
        cpu.er8 += 1
        cpu.er0 = 0x8000
        cpu.er4 = cpu.er14
        cpu.er4 += 44
        cpu.r7 = 112
        cpu.label('restore')
        cpu.r2 = cpu.mem8[0, cpu.er4]
        cpu.mem8[0, cpu.er0] = cpu.r2
        cpu.er0 += 1
        cpu.er4 += 1
        cpu.r7 += 255
        if cpu.ne:
            cpu.branch('restore')
        cpu.r0 = cpu.mem8[0, cpu.er4]
        cpu.mem8[0, 0x8090] = cpu.r0
        cpu.er0 = cpu.er8
        cpu.sp += 64
        cpu.sp += 64
        cpu.sp += 32
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
