"""Owned native MCS objects for BASIC; descriptors and names live on the stack."""

from kits import cpu


def install(fw):
    @fw.function(native=True)
    def object_work():
        # ER0 descriptor, ER6 allocation, R3 lookup/upsert/delete; EGW1 workspace.
        cpu.r2 = 2
        cpu.jump('fn_object_open')

    @fw.function(native=True)
    def object_open():
        # ER0 descriptor, R2 matrix/string/work, ER4 ID, ER6 bytes, R3 mode.
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.er12 = cpu.er4
        cpu.r10 = cpu.r3
        cpu.r11 = cpu.r2
        cpu.sp += -16
        cpu.er14 = cpu.sp
        cpu.compare(cpu.r10, 2)
        if cpu.gt:
            cpu.jump('argument')
        cpu.compare(cpu.r11, 2)
        if cpu.gt:
            cpu.jump('argument')
        cpu.compare(cpu.r10, 1)
        if cpu.eq:
            cpu.er0 = 8
            cpu.compare(cpu.r11, 2)
            if cpu.eq:
                cpu.er0 = 4
            cpu.compare(cpu.er6, cpu.er0)
            if cpu.lt:
                cpu.jump('argument')
        cpu.mem16[0, cpu.offset(cpu.er8, 8)] = cpu.er6
        cpu.er0 = 0
        cpu.er4 = cpu.er8
        cpu.r2 = 8
        cpu.label('clear')
        cpu.mem8[0, cpu.er4] = cpu.r0
        cpu.er4 += 1
        cpu.r2 += 255
        if cpu.ne:
            cpu.branch('clear')
        cpu.er0 = cpu.er14
        cpu.mem16[0, cpu.er8] = cpu.er0
        cpu.er0 += 6
        cpu.mem16[0, cpu.offset(cpu.er8, 4)] = cpu.er0
        cpu.er0 = 0x616D
        cpu.mem16[0, cpu.er14] = cpu.er0
        cpu.er0 = 0x6E69
        cpu.mem16[0, cpu.offset(cpu.er14, 2)] = cpu.er0
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er14, 4)] = cpu.er0
        cpu.mem16[0, cpu.offset(cpu.er14, 12)] = cpu.er0
        cpu.er0 = 0x3545
        cpu.mem16[0, cpu.offset(cpu.er14, 6)] = cpu.er0
        cpu.r0 = 0x4D
        cpu.compare(cpu.r11, 0)
        if cpu.ne:
            cpu.r0 = 0x53
        cpu.mem8[0, cpu.offset(cpu.er14, 8)] = cpu.r0
        cpu.er4 = cpu.er14
        cpu.er4 += 9
        cpu.r2 = 4
        cpu.label('hex')
        cpu.r0 = cpu.r13
        cpu.r0 >>= 4
        cpu.compare(cpu.r0, 10)
        if cpu.ge:
            cpu.r0 += 7
        cpu.r0 += 0x30
        cpu.mem8[0, cpu.er4] = cpu.r0
        cpu.er4 += 1
        cpu.shift_left_carry(cpu.r13, 4)
        cpu.r12 <<= 4
        cpu.r2 += 255
        if cpu.ne:
            cpu.branch('hex')
        cpu.compare(cpu.r11, 2)
        if cpu.eq:
            cpu.er0 = 0x5742
            cpu.mem16[0, cpu.offset(cpu.er14, 8)] = cpu.er0
            cpu.er0 = 0x524F
            cpu.mem16[0, cpu.offset(cpu.er14, 10)] = cpu.er0
            cpu.er0 = 0x004B
            cpu.mem16[0, cpu.offset(cpu.er14, 12)] = cpu.er0
        cpu.er0 = cpu.er8
        cpu.compare(cpu.r10, 2)
        if cpu.eq:
            cpu.call('fn_mcs_remove')
            cpu.jump('status')
        cpu.r0 = cpu.r10
        cpu.mem8[0, cpu.offset(cpu.er8, 7)] = cpu.r0
        cpu.er0 = cpu.er8
        cpu.call('fn_mcs_open')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('status')
        cpu.compare(cpu.r10, 1)
        if cpu.ne:
            cpu.jump('out')
        cpu.er0 = cpu.er8
        cpu.call('fn_mcs_resize')
        cpu.label('status')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.jump('out')
        cpu.compare(cpu.r0, 1)
        if cpu.eq:
            cpu.er0 = 6
        else:
            cpu.er0 = 4
        cpu.jump('out')
        cpu.label('argument')
        cpu.er0 = 4
        cpu.label('out')
        cpu.sp += 16
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
