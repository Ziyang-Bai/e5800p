"""Owned GRAPH and numbered BASIC objects in the native main folder.

ER0 points to a segment-0 descriptor. All entries preserve R4..R15; R0 is
0=OK, 1=full, 2=name used, 3=native error, 4=not found. Returned length is
allocated (even) length; logical lengths belong in the caller's payload header.
Names and lookup outputs are copied to the near stack before a moving call.
"""

from kits import cpu

FOLDER = 0
FOLDER_BANK = 2
NAME = 4
NAME_BANK = 6
FLAGS = 7
REQUEST_SIZE = 8
PAYLOAD = 10
PAYLOAD_BANK = 12
ACTUAL_SIZE = 14
DESCRIPTOR_SIZE = 16

MAIN_FOLDER = b'main\0'
GRAPH_NAME = b'E5GRAPH\0'
WORK_NAME = b'E5GWORK\0'
GRAPH_OWNER = b'EGS1'
WORK_OWNER = b'EGW1'

SUCCESS = 0
MEMORY_FULL = 1
NAME_USED = 2
NATIVE_ERROR = 3
NOT_FOUND = 4

NATIVE_LOOKUP = 0x1A574
NATIVE_CREATE = 0x1A6C6
NATIVE_GROW = 0x1B1C2
NATIVE_SHRINK = 0x1B408
NATIVE_REMOVE = 0x1AFCE

# Descriptor, main[6], name[8], type[2], record[4], payload[4], size[4].
FRAME_SIZE = 44


def install(fw):
    @fw.function(native=True)
    def mcs_open():
        """Find an owned object; flags bit0 permits creation with REQUEST_SIZE."""
        cpu.r3 = 0
        cpu.jump('fn_mcs_native')

    @fw.function(native=True)
    def mcs_resize():
        """Preserve the prefix, round REQUEST_SIZE up, and reopen after moving."""
        cpu.r3 = 1
        cpu.jump('fn_mcs_native')

    @fw.function(native=True)
    def mcs_remove():
        """Remove only an object with its name's matching owner header."""
        cpu.r3 = 2
        cpu.jump('fn_mcs_native')

    @fw.function(native=True)
    def mcs_native():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.r12 = cpu.r3
        cpu.sp += -FRAME_SIZE
        cpu.er14 = cpu.sp
        cpu.er4 = cpu.er8
        cpu.er0 = cpu.er14
        cpu.r2 = DESCRIPTOR_SIZE
        cpu.label('descriptor')
        cpu.r3 = cpu.mem8[0, cpu.er4]
        cpu.mem8[0, cpu.er0] = cpu.r3
        cpu.er4 += 1
        cpu.er0 += 1
        cpu.r2 += 255
        if cpu.ne:
            cpu.branch('descriptor')
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er8, PAYLOAD)] = cpu.er0
        cpu.mem16[0, cpu.offset(cpu.er8, PAYLOAD_BANK)] = cpu.er0
        cpu.mem16[0, cpu.offset(cpu.er8, ACTUAL_SIZE)] = cpu.er0

        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, FOLDER)]
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, FOLDER_BANK)]
        cpu.er4 = cpu.er14
        cpu.er4 += 16
        cpu.r3 = 5
        cpu.label('folder')
        cpu.r7 = cpu.mem8[cpu.r2, cpu.er0]
        cpu.mem8[0, cpu.er4] = cpu.r7
        cpu.er0 += 1
        cpu.er4 += 1
        cpu.r3 += 255
        if cpu.ne:
            cpu.branch('folder')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, NAME)]
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, NAME_BANK)]
        cpu.er4 = cpu.er14
        cpu.er4 += 22
        cpu.r3 = 8
        cpu.label('name')
        cpu.r7 = cpu.mem8[cpu.r2, cpu.er0]
        cpu.mem8[0, cpu.er4] = cpu.r7
        cpu.er0 += 1
        cpu.er4 += 1
        cpu.r3 += 255
        if cpu.ne:
            cpu.branch('name')

        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 16)]
        cpu.er4 = 0x616D
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.ne:
            cpu.jump('collision')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 18)]
        cpu.er4 = 0x6E69
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.ne:
            cpu.jump('collision')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 20)]
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.jump('collision')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 22)]
        cpu.er4 = 0x3545
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.ne:
            cpu.jump('collision')
        cpu.call('fn_mcs_object_name')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.jump('lookup')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 24)]
        cpu.er4 = 0x5247
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.ne:
            cpu.branch('work')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 26)]
        cpu.er4 = 0x5041
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.ne:
            cpu.jump('collision')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 28)]
        cpu.er4 = 0x0048
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.ne:
            cpu.jump('collision')
        cpu.er6 = 0x3153
        cpu.jump('lookup')
        cpu.label('work')
        cpu.er4 = 0x5747
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.ne:
            cpu.er4 = 0x5742
            cpu.compare(cpu.er0, cpu.er4)
            if cpu.ne:
                cpu.jump('collision')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 26)]
        cpu.er4 = 0x524F
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.ne:
            cpu.jump('collision')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 28)]
        cpu.er4 = 0x004B
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.ne:
            cpu.jump('collision')
        cpu.er6 = 0x3157

        cpu.label('lookup')
        cpu.call('fn_mcs_lookup')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.jump('found')
        cpu.compare(cpu.r1, 0)
        if cpu.ne:
            cpu.jump('native_error')
        cpu.compare(cpu.r0, 0x30)
        if cpu.ne:
            cpu.jump('status')
        cpu.compare(cpu.r12, 0)
        if cpu.ne:
            cpu.jump('missing')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, FLAGS)]
        cpu.r0 &= 1
        if cpu.eq:
            cpu.jump('missing')
        cpu.call('size')
        # A null source does not clear the allocation in the native allocator.
        cpu.er0 = 0
        cpu.push(cpu.er0)
        cpu.push(cpu.er0)
        cpu.push(cpu.er0)
        cpu.push(cpu.er10)
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 22
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.r2 = 0
        cpu.r3 = 0x0C
        cpu.call(NATIVE_CREATE)
        cpu.sp += 12
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('status')
        cpu.call('fn_mcs_lookup')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('status')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 42)]
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('native_error')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 40)]
        cpu.compare(cpu.er0, cpu.er10)
        if cpu.ne:
            cpu.jump('native_error')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, 36)]
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, 38)]
        cpu.er0 = cpu.er10
        cpu.r3 = 0
        cpu.label('clear')
        cpu.mem8[cpu.r2, cpu.er4] = cpu.r3
        cpu.er4 += 1
        cpu.er0 += -1
        if cpu.ne:
            cpu.branch('clear')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, 36)]
        cpu.er0 = 0x4745
        cpu.mem16[cpu.r2, cpu.er4] = cpu.er0
        cpu.mem16[cpu.r2, cpu.offset(cpu.er4, 2)] = cpu.er6
        cpu.jump('publish')

        cpu.label('found')
        cpu.call('fn_mcs_owned')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.compare(cpu.r12, 0)
        if cpu.eq:
            cpu.jump('publish')
        cpu.compare(cpu.r12, 2)
        if cpu.eq:
            cpu.jump('remove')
        cpu.call('size')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 40)]
        cpu.compare(cpu.er10, cpu.er0)
        if cpu.eq:
            cpu.jump('publish')
        if cpu.gt:
            cpu.branch('grow')
        cpu.er4 = cpu.er0
        cpu.r4 -= cpu.r10
        cpu.sub_carry(cpu.r5, cpu.r11)
        cpu.er0 = cpu.er10
        cpu.r13 = 0
        cpu.jump('resize')
        cpu.label('grow')
        cpu.er4 = cpu.er10
        cpu.r4 -= cpu.r0
        cpu.sub_carry(cpu.r5, cpu.r1)
        cpu.r13 = 1
        cpu.label('resize')
        cpu.er2 = 0
        cpu.push(cpu.er2)
        cpu.push(cpu.er4)
        cpu.push(cpu.er2)
        cpu.push(cpu.er0)
        cpu.push(cpu.er2)
        cpu.er0 = cpu.er14
        cpu.er0 += 22
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.r2 = 0
        cpu.r3 = 0
        cpu.compare(cpu.r13, 0)
        if cpu.eq:
            cpu.call(NATIVE_SHRINK)
        else:
            cpu.call(NATIVE_GROW)
        cpu.sp += 12
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('status')
        cpu.call('fn_mcs_lookup')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('status')
        cpu.call('fn_mcs_owned')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.jump('publish')

        cpu.label('remove')
        cpu.er0 = 0
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 22
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.r2 = 0
        cpu.call(NATIVE_REMOVE)
        cpu.sp += 4
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('status')
        cpu.call('fn_mcs_lookup')
        cpu.compare(cpu.r1, 0)
        if cpu.ne:
            cpu.jump('native_error')
        cpu.compare(cpu.r0, 0x30)
        if cpu.ne:
            cpu.jump('native_error')
        cpu.jump('success')

        cpu.label('publish')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 36)]
        cpu.mem16[0, cpu.offset(cpu.er8, PAYLOAD)] = cpu.er0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 38)]
        cpu.mem8[0, cpu.offset(cpu.er8, PAYLOAD_BANK)] = cpu.r0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 40)]
        cpu.mem16[0, cpu.offset(cpu.er8, ACTUAL_SIZE)] = cpu.er0
        cpu.label('success')
        cpu.er0 = SUCCESS
        cpu.jump('out')
        cpu.label('status')
        cpu.compare(cpu.r1, 0)
        if cpu.ne:
            cpu.jump('native_error')
        cpu.compare(cpu.r0, 0x11)
        if cpu.eq:
            cpu.branch('full')
        cpu.compare(cpu.r0, 0x30)
        if cpu.eq:
            cpu.branch('missing')
        cpu.label('native_error')
        cpu.er0 = NATIVE_ERROR
        cpu.jump('out')
        cpu.label('full')
        cpu.er0 = MEMORY_FULL
        cpu.jump('out')
        cpu.label('missing')
        cpu.er0 = NOT_FOUND
        cpu.jump('out')
        cpu.label('collision')
        cpu.er0 = NAME_USED
        cpu.label('out')
        cpu.sp += FRAME_SIZE
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

        cpu.label('size')
        cpu.er10 = cpu.mem16[0, cpu.offset(cpu.er14, REQUEST_SIZE)]
        cpu.er0 = 4
        cpu.compare(cpu.er10, cpu.er0)
        if cpu.lt:
            cpu.jump('native_error')
        cpu.er10 += 1
        cpu.er10 = cpu.er10
        if cpu.eq:
            cpu.jump('full')
        cpu.r10 &= 0xFE
        cpu.ret()

    @fw.function(native=True)
    def mcs_lookup():
        """Private: ER14 is the near frame; exact native 20-byte argument list."""
        cpu.push(cpu.lr)
        cpu.er2 = 0
        cpu.push(cpu.er2)
        cpu.er0 = cpu.er14
        cpu.er0 += 40
        cpu.push(cpu.er0)
        cpu.push(cpu.er2)
        cpu.er0 = cpu.er14
        cpu.er0 += 36
        cpu.push(cpu.er0)
        cpu.push(cpu.er2)
        cpu.er0 = cpu.er14
        cpu.er0 += 32
        cpu.push(cpu.er0)
        cpu.push(cpu.er2)
        cpu.er0 = cpu.er14
        cpu.er0 += 30
        cpu.push(cpu.er0)
        cpu.push(cpu.er2)
        cpu.er0 = cpu.er14
        cpu.er0 += 22
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.r2 = 0
        cpu.call(NATIVE_LOOKUP)
        cpu.sp += 20
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def mcs_owned():
        """Private: check lookup output against ER6's owner suffix; clobber ER4."""
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 30)]
        cpu.compare(cpu.r0, 0x0C)
        if cpu.ne:
            cpu.jump('collision')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 42)]
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('collision')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 40)]
        cpu.er4 = 4
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.lt:
            cpu.jump('collision')
        cpu.r0 &= 1
        if cpu.ne:
            cpu.jump('collision')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, 36)]
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, 38)]
        cpu.er0 = cpu.mem16[cpu.r2, cpu.er4]
        cpu.compare(cpu.r0, 0x45)
        if cpu.ne:
            cpu.jump('collision')
        cpu.compare(cpu.r1, 0x47)
        if cpu.ne:
            cpu.jump('collision')
        cpu.er0 = cpu.mem16[cpu.r2, cpu.offset(cpu.er4, 2)]
        cpu.compare(cpu.er0, cpu.er6)
        if cpu.ne:
            cpu.jump('collision')
        cpu.er0 = SUCCESS
        cpu.ret()
        cpu.label('collision')
        cpu.er0 = NAME_USED
        cpu.ret()

    @fw.function(native=True)
    def mcs_object_name():
        # E5Mhhhh / E5Shhhh; the payload tag follows the namespace, not flags.
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 24)]
        cpu.er6 = 0x314D
        cpu.compare(cpu.r0, 0x4D)
        if cpu.ne:
            cpu.compare(cpu.r0, 0x53)
            if cpu.ne:
                cpu.jump('bad')
            cpu.er6 = 0x3154
        cpu.er4 = cpu.er14
        cpu.er4 += 25
        cpu.r3 = 4
        cpu.label('hex')
        cpu.r0 = cpu.mem8[0, cpu.er4]
        cpu.compare(cpu.r0, 0x30)
        if cpu.lt:
            cpu.jump('bad')
        cpu.compare(cpu.r0, 0x39)
        if cpu.le:
            cpu.branch('next')
        cpu.compare(cpu.r0, 0x41)
        if cpu.lt:
            cpu.jump('bad')
        cpu.compare(cpu.r0, 0x46)
        if cpu.gt:
            cpu.jump('bad')
        cpu.label('next')
        cpu.er4 += 1
        cpu.r3 += 255
        if cpu.ne:
            cpu.branch('hex')
        cpu.r0 = cpu.mem8[0, cpu.er4]
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.jump('bad')
        cpu.er0 = 0
        cpu.ret()
        cpu.label('bad')
        cpu.er0 = NAME_USED
        cpu.ret()
