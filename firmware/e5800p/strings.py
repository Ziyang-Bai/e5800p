"""Numbered byte strings. Lengths include embedded NULs; display maps NUL to space."""

from kits import cpu

from .graph_math import TEXT, Y

FRAME_SIZE = 88
STACK_MIN = 0x8492
MAX_LENGTH = 65525  # Header, terminator and native even allocation fit in u16.
NATIVE_DECIMAL = 0xC3F3C


def install(fw):
    @fw.function(native=True)
    def strings():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er2
        cpu.er10 = cpu.er4
        cpu.er12 = cpu.er6
        cpu.r6 = cpu.r0
        cpu.er0 = cpu.sp
        cpu.er2 = STACK_MIN + FRAME_SIZE
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.jump('memory')
        cpu.sp += -FRAME_SIZE
        cpu.er14 = cpu.sp
        cpu.mem8[0, cpu.offset(cpu.er14, 72)] = cpu.r6
        cpu.mem16[0, cpu.offset(cpu.er14, 68)] = cpu.er8
        cpu.mem16[0, cpu.offset(cpu.er14, 70)] = cpu.er10
        cpu.er0 = cpu.er12
        cpu.r2 = 0
        cpu.r3 = 20
        cpu.er4 = cpu.er14
        cpu.er4 += 48
        cpu.r6 = 0
        cpu.call('fn_graph_copy')
        cpu.er4 = cpu.er10
        cpu.r2 = 20
        cpu.r0 = 0
        cpu.label('zero')
        cpu.mem8[0, cpu.er4] = cpu.r0
        cpu.er4 += 1
        cpu.r2 += 255
        if cpu.ne:
            cpu.branch('zero')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 72)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.call('fn_string_set')
            cpu.jump('out')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.call('fn_string_join')
            cpu.jump('out')
        cpu.compare(cpu.r0, 3)
        if cpu.eq:
            cpu.call('fn_string_join')
            cpu.jump('out')
        cpu.compare(cpu.r0, 5)
        if cpu.eq:
            cpu.call('fn_string_convert')
            cpu.jump('out')
        cpu.compare(cpu.r0, 6)
        if cpu.eq:
            cpu.call('fn_string_convert')
            cpu.jump('out')
        cpu.compare(cpu.r0, 8)
        if cpu.eq:
            cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er8, 4)]
            cpu.compare(cpu.r1, 0)
            if cpu.ne:
                cpu.jump('argument')
            cpu.mem8[0, cpu.offset(cpu.er14, 82)] = cpu.r0
            cpu.er6 = cpu.er14
            cpu.er6 += 63
            cpu.er6 += 19
            cpu.er12 = 1
            cpu.er4 = cpu.mem16[0, cpu.er8]
            cpu.call('fn_string_put')
            cpu.jump('out')
        cpu.call('fn_string_read')
        cpu.jump('out')
        cpu.label('argument')
        cpu.er0 = 4
        cpu.label('out')
        cpu.sp = cpu.er14
        cpu.sp += FRAME_SIZE
        cpu.label('restore')
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('memory')
        cpu.er0 = 6
        cpu.jump('restore')

    @fw.function(native=True)
    def string_open():
        # ER0 descriptor, ER4 ID. +8 returns logical length, +10 still header.
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.er8)
        cpu.er8 = cpu.er0
        cpu.r2 = 1
        cpu.r3 = 0
        cpu.er6 = 0
        cpu.call('fn_object_open')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er8, 14)]
        cpu.er4 = 10
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.lt:
            cpu.jump('bad')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er8, 10)]
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er8, 12)]
        cpu.er6 = cpu.mem16[cpu.r2, cpu.offset(cpu.er4, 4)]
        cpu.mem16[0, cpu.offset(cpu.er8, 8)] = cpu.er6
        cpu.er4 = cpu.mem16[cpu.r2, cpu.offset(cpu.er4, 6)]
        cpu.er4 = cpu.er4
        if cpu.ne:
            cpu.jump('bad')
        cpu.er4 = MAX_LENGTH
        cpu.compare(cpu.er6, cpu.er4)
        if cpu.gt:
            cpu.jump('bad')
        cpu.er6 += 9
        cpu.compare(cpu.er6, cpu.er0)
        if cpu.gt:
            cpu.jump('bad')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er8, 10)]
        cpu.er4 += cpu.er6
        cpu.er4 += -1
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.jump('bad')
        cpu.er0 = 0
        cpu.jump('out')
        cpu.label('bad')
        cpu.er0 = 4
        cpu.label('out')
        cpu.pop(cpu.er8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def string_copy():
        # ER0/R2 -> ER4/R6, ER12 bytes, including NULs. Preserve R4..R15.
        cpu.push(cpu.xr4)
        cpu.push(cpu.er12)
        cpu.er12 = cpu.er12
        if cpu.eq:
            cpu.jump('out')
        cpu.label('byte')
        cpu.r7 = cpu.mem8[cpu.r2, cpu.er0]
        cpu.mem8[cpu.r6, cpu.er4] = cpu.r7
        cpu.er0 += 1
        cpu.er4 += 1
        cpu.er12 += -1
        if cpu.ne:
            cpu.branch('byte')
        cpu.label('out')
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr4)
        cpu.ret()

    @fw.function(native=True)
    def string_put():
        # ER4 ID, ER6 near snapshot, ER12 length. No moving source survives.
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er6
        cpu.er10 = cpu.er12
        cpu.er0 = MAX_LENGTH
        cpu.compare(cpu.er10, cpu.er0)
        if cpu.gt:
            cpu.jump('memory')
        cpu.sp += -16
        cpu.er14 = cpu.sp
        cpu.er6 = cpu.er10
        cpu.er6 += 9
        cpu.er0 = cpu.er14
        cpu.r2 = 1
        cpu.r3 = 1
        cpu.call('fn_object_open')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, 10)]
        cpu.r6 = cpu.mem8[0, cpu.offset(cpu.er14, 12)]
        cpu.mem16[cpu.r6, cpu.offset(cpu.er4, 4)] = cpu.er10
        cpu.er0 = 0
        cpu.mem16[cpu.r6, cpu.offset(cpu.er4, 6)] = cpu.er0
        cpu.er4 += 8
        cpu.er0 = cpu.er8
        cpu.r2 = 0
        cpu.er12 = cpu.er10
        cpu.call('fn_string_copy')
        cpu.er4 += cpu.er10
        cpu.r0 = 0
        cpu.mem8[cpu.r6, cpu.er4] = cpu.r0
        cpu.er0 = 0
        cpu.label('out')
        cpu.sp += 16
        cpu.label('restore')
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('memory')
        cpu.er0 = 6
        cpu.jump('restore')

    @fw.function(native=True)
    def string_alloc():
        # Internal: reserve an even near snapshot; the entry restores SP at exit.
        cpu.mem16[0, cpu.offset(cpu.er14, 80)] = cpu.er6
        cpu.er0 = cpu.er6
        cpu.er2 = MAX_LENGTH
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.gt:
            cpu.jump('memory')
        cpu.er0 += 1
        cpu.r0 &= 0xFE
        cpu.er2 = cpu.sp
        cpu.r2 -= cpu.r0
        cpu.sub_carry(cpu.r3, cpu.r1)
        if cpu.lt:
            cpu.jump('memory')
        cpu.er0 = STACK_MIN
        cpu.compare(cpu.er2, cpu.er0)
        if cpu.lt:
            cpu.jump('memory')
        cpu.sp = cpu.er2
        cpu.mem16[0, cpu.offset(cpu.er14, 78)] = cpu.er2
        cpu.er0 = 0
        cpu.ret()
        cpu.label('memory')
        cpu.er0 = 6
        cpu.ret()

    @fw.function(native=True)
    def string_set():
        cpu.push(cpu.lr)
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er8, 8)]
        cpu.call('fn_string_alloc')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er8, 4)]
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er8, 6)]
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, 78)]
        cpu.r6 = 0
        cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er14, 80)]
        cpu.call('fn_string_copy')
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, 78)]
        cpu.er4 = cpu.mem16[0, cpu.er8]
        cpu.call('fn_string_put')
        cpu.label('out')
        # The variable snapshot lies below the saved return address.
        cpu.er2 = cpu.er14
        cpu.er2 += -4
        cpu.sp = cpu.er2
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def string_join():
        cpu.push(cpu.lr)
        cpu.er0 = cpu.er14
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er8, 4)]
        cpu.call('fn_string_open')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, 8)]
        cpu.mem16[0, cpu.offset(cpu.er14, 74)] = cpu.er6
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er14, 76)] = cpu.er0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 72)]
        cpu.compare(cpu.r0, 3)
        if cpu.eq:
            cpu.jump('concat')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er8, 8)]
        cpu.er4 = cpu.er4
        if cpu.eq:
            cpu.jump('argument')
        cpu.er4 += -1
        cpu.compare(cpu.er4, cpu.er6)
        if cpu.ge:
            cpu.er6 = 0
            cpu.jump('substring')
        cpu.r6 -= cpu.r4
        cpu.sub_carry(cpu.r7, cpu.r5)
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er8, 12)]
        cpu.compare(cpu.er6, cpu.er0)
        if cpu.gt:
            cpu.er6 = cpu.er0
        cpu.label('substring')
        cpu.mem16[0, cpu.offset(cpu.er14, 74)] = cpu.er6
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 10)]
        cpu.er0 += cpu.er4
        cpu.mem16[0, cpu.offset(cpu.er14, 10)] = cpu.er0
        cpu.jump('snapshot')
        cpu.label('concat')
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er8, 8)]
        cpu.call('fn_string_open')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, 24)]
        cpu.mem16[0, cpu.offset(cpu.er14, 76)] = cpu.er6
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 74)]
        cpu.er6 += cpu.er0
        if cpu.lt:
            cpu.jump('memory')
        cpu.label('snapshot')
        cpu.call('fn_string_alloc')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 10)]
        cpu.er0 += 8
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, 12)]
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, 78)]
        cpu.r6 = 0
        cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er14, 74)]
        cpu.call('fn_string_copy')
        cpu.er4 += cpu.er12
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 26)]
        cpu.er0 += 8
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, 28)]
        cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er14, 76)]
        cpu.call('fn_string_copy')
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, 78)]
        cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er14, 80)]
        cpu.er4 = cpu.mem16[0, cpu.er8]
        cpu.call('fn_string_put')
        cpu.jump('out')
        cpu.label('argument')
        cpu.er0 = 4
        cpu.jump('out')
        cpu.label('memory')
        cpu.er0 = 6
        cpu.label('out')
        cpu.er2 = cpu.er14
        cpu.er2 += -4
        cpu.sp = cpu.er2
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def string_number():
        # Internal u16 ER0 -> entry's native20 result.
        cpu.push(cpu.lr)
        cpu.mem16[0, cpu.offset(cpu.er14, 82)] = cpu.er0
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er14, 84)] = cpu.er0
        cpu.er0 = cpu.er14
        cpu.er0 += 63
        cpu.er0 += 19
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, 70)]
        cpu.call(0xFB538)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def string_read():
        cpu.push(cpu.lr)
        cpu.er4 = cpu.mem16[0, cpu.er8]
        cpu.er0 = cpu.er14
        cpu.call('fn_string_open')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 72)]
        cpu.compare(cpu.r0, 1)
        if cpu.eq:
            cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 8)]
            cpu.call('fn_string_number')
            cpu.jump('out')
        cpu.compare(cpu.r0, 4)
        if cpu.eq:
            cpu.call('fn_string_find')
            cpu.jump('out')
        cpu.compare(cpu.r0, 7)
        if cpu.eq:
            cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 10)]
            cpu.er0 += 8
            cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, 12)]
            cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, 8)]
            cpu.call('fn_string_print')
            cpu.jump('out')
        cpu.compare(cpu.r0, 9)
        if cpu.ne:
            cpu.jump('argument')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er8, 4)]
        cpu.er4 = cpu.er4
        if cpu.eq:
            cpu.jump('argument')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 8)]
        cpu.compare(cpu.er4, cpu.er0)
        if cpu.gt:
            cpu.jump('argument')
        cpu.er4 += 7
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 10)]
        cpu.er4 += cpu.er0
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, 12)]
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.r1 = 0
        cpu.call('fn_string_number')
        cpu.jump('out')
        cpu.label('argument')
        cpu.er0 = 4
        cpu.label('out')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def string_find():
        cpu.push(cpu.lr)
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er8, 4)]
        cpu.call('fn_string_open')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er10 = cpu.mem16[0, cpu.offset(cpu.er14, 24)]
        cpu.er0 = 1
        cpu.er10 = cpu.er10
        if cpu.eq:
            cpu.jump('number')
        cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er14, 8)]
        cpu.compare(cpu.er10, cpu.er12)
        if cpu.gt:
            cpu.jump('missing')
        cpu.r12 -= cpu.r10
        cpu.sub_carry(cpu.r13, cpu.r11)
        cpu.er12 += 1
        cpu.mem16[0, cpu.offset(cpu.er14, 82)] = cpu.er0
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, 10)]
        cpu.er4 += 8
        cpu.r8 = cpu.mem8[0, cpu.offset(cpu.er14, 12)]
        cpu.r9 = cpu.mem8[0, cpu.offset(cpu.er14, 28)]
        cpu.label('candidate')
        cpu.push(cpu.er4)
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, 26)]
        cpu.er6 += 8
        cpu.er2 = cpu.er10
        cpu.label('compare')
        cpu.r0 = cpu.mem8[cpu.r8, cpu.er4]
        cpu.r1 = cpu.mem8[cpu.r9, cpu.er6]
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.ne:
            cpu.jump('next')
        cpu.er4 += 1
        cpu.er6 += 1
        cpu.er2 += -1
        if cpu.ne:
            cpu.branch('compare')
        cpu.pop(cpu.er4)
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 82)]
        cpu.jump('number')
        cpu.label('next')
        cpu.pop(cpu.er4)
        cpu.er4 += 1
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 82)]
        cpu.er0 += 1
        cpu.mem16[0, cpu.offset(cpu.er14, 82)] = cpu.er0
        cpu.er12 += -1
        if cpu.ne:
            cpu.branch('candidate')
        cpu.label('missing')
        cpu.er0 = 0
        cpu.label('number')
        cpu.call('fn_string_number')
        cpu.label('out')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def string_convert():
        cpu.push(cpu.lr)
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 72)]
        cpu.compare(cpu.r0, 5)
        if cpu.eq:
            cpu.call('fn_string_value')
            cpu.jump('out')
        cpu.sp += -128
        cpu.er12 = cpu.sp
        cpu.er0 = cpu.er14
        cpu.er0 += 48
        cpu.r2 = 0
        cpu.r3 = 20
        cpu.er4 = cpu.er12
        cpu.er4 += Y
        cpu.r6 = 0
        cpu.call('fn_graph_copy')
        cpu.er0 = cpu.er12
        cpu.r2 = 0
        cpu.call('fn_graph_format')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.er0 = 4
            cpu.jump('out')
        cpu.er6 = cpu.er12
        cpu.er6 += 63
        cpu.er6 += TEXT - 63
        cpu.er4 = cpu.er6
        cpu.er12 = 0
        cpu.label('length')
        cpu.r0 = cpu.mem8[0, cpu.er4]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.jump('put')
        cpu.er4 += 1
        cpu.er12 += 1
        cpu.jump('length')
        cpu.label('put')
        cpu.er8 = cpu.mem16[0, cpu.offset(cpu.er14, 68)]
        cpu.er4 = cpu.mem16[0, cpu.er8]
        cpu.call('fn_string_put')
        cpu.label('out')
        cpu.er2 = cpu.er14
        cpu.er2 += -4
        cpu.sp = cpu.er2
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def string_value():
        cpu.push(cpu.lr)
        cpu.er0 = cpu.er14
        cpu.er4 = cpu.mem16[0, cpu.er8]
        cpu.call('fn_string_open')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, 8)]
        cpu.er6 += 1
        cpu.call('fn_string_alloc')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, 10)]
        cpu.er4 += 8
        cpu.r6 = cpu.mem8[0, cpu.offset(cpu.er14, 12)]
        cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er14, 8)]
        cpu.er10 = cpu.mem16[0, cpu.offset(cpu.er14, 78)]
        cpu.r8 = 0
        cpu.label('leading')
        cpu.er12 = cpu.er12
        if cpu.eq:
            cpu.jump('bad')
        cpu.r0 = cpu.mem8[cpu.r6, cpu.er4]
        cpu.er4 += 1
        cpu.er12 += -1
        cpu.compare(cpu.r0, 0x20)
        if cpu.eq:
            cpu.branch('leading')
        cpu.compare(cpu.r0, 0x2D)
        if cpu.eq:
            cpu.r8 = 1
            cpu.jump('signed')
        cpu.compare(cpu.r0, 0x2B)
        if cpu.ne:
            cpu.jump('initial')
        cpu.label('signed')
        cpu.er12 = cpu.er12
        if cpu.eq:
            cpu.jump('bad')
        cpu.r0 = cpu.mem8[cpu.r6, cpu.er4]
        cpu.er4 += 1
        cpu.er12 += -1
        cpu.label('initial')
        cpu.mem8[0, cpu.offset(cpu.er14, 86)] = cpu.r8
        cpu.r7 = 0
        cpu.r9 = 0
        cpu.label('character')
        cpu.compare(cpu.r0, 0x30)
        if cpu.lt:
            cpu.jump('punctuation')
        cpu.compare(cpu.r0, 0x39)
        if cpu.gt:
            cpu.jump('punctuation')
        cpu.r1 = cpu.r7
        cpu.r1 &= 4
        if cpu.eq:
            cpu.r7 |= 1
            cpu.jump('write')
        cpu.r7 |= 8
        cpu.compare(cpu.r9, 0)
        if cpu.ne:
            cpu.jump('write')
        cpu.compare(cpu.r0, 0x30)
        if cpu.eq:
            cpu.jump('next')
        cpu.r9 = 1
        cpu.jump('write')
        cpu.label('punctuation')
        cpu.compare(cpu.r0, 0x20)
        if cpu.eq:
            cpu.jump('trailing')
        cpu.compare(cpu.r0, 0x2E)
        if cpu.eq:
            cpu.r1 = cpu.r7
            cpu.r1 &= 6
            if cpu.ne:
                cpu.jump('bad')
            cpu.r7 |= 2
            cpu.jump('write')
        cpu.r0 &= 0xDF
        cpu.compare(cpu.r0, 0x45)
        if cpu.ne:
            cpu.jump('bad')
        cpu.r1 = cpu.r7
        cpu.r1 &= 5
        cpu.compare(cpu.r1, 1)
        if cpu.ne:
            cpu.jump('bad')
        cpu.r7 |= 4
        cpu.r0 = 0x0F
        cpu.mem8[0, cpu.er10] = cpu.r0
        cpu.er10 += 1
        cpu.er12 = cpu.er12
        if cpu.eq:
            cpu.jump('bad')
        cpu.r0 = cpu.mem8[cpu.r6, cpu.er4]
        cpu.compare(cpu.r0, 0x2B)
        if cpu.eq:
            cpu.jump('exponent_sign')
        cpu.compare(cpu.r0, 0x2D)
        if cpu.ne:
            cpu.jump('next')
        cpu.r0 = 0x87
        cpu.mem8[0, cpu.er10] = cpu.r0
        cpu.er10 += 1
        cpu.label('exponent_sign')
        cpu.er4 += 1
        cpu.er12 += -1
        cpu.jump('next')
        cpu.label('write')
        cpu.mem8[0, cpu.er10] = cpu.r0
        cpu.er10 += 1
        cpu.label('next')
        cpu.er12 = cpu.er12
        if cpu.eq:
            cpu.jump('end')
        cpu.r0 = cpu.mem8[cpu.r6, cpu.er4]
        cpu.er4 += 1
        cpu.er12 += -1
        cpu.jump('character')
        cpu.label('trailing')
        cpu.er12 = cpu.er12
        if cpu.eq:
            cpu.jump('end')
        cpu.r0 = cpu.mem8[cpu.r6, cpu.er4]
        cpu.er4 += 1
        cpu.er12 += -1
        cpu.compare(cpu.r0, 0x20)
        if cpu.eq:
            cpu.branch('trailing')
        cpu.jump('bad')
        cpu.label('end')
        cpu.r0 = cpu.r7
        cpu.r0 &= 1
        if cpu.eq:
            cpu.jump('bad')
        cpu.r0 = cpu.r7
        cpu.r0 &= 4
        if cpu.eq:
            cpu.jump('parse')
        cpu.r0 = cpu.r7
        cpu.r0 &= 8
        if cpu.eq:
            cpu.jump('bad')
        cpu.compare(cpu.r9, 0)
        if cpu.eq:
            cpu.r0 = 0x30
            cpu.mem8[0, cpu.er10] = cpu.r0
            cpu.er10 += 1
        cpu.label('parse')
        cpu.r0 = 0
        cpu.mem8[0, cpu.er10] = cpu.r0
        cpu.mem8[0, cpu.offset(cpu.er14, 18)] = cpu.r0
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, 78)]
        cpu.r0 = cpu.mem8[0, cpu.er4]
        cpu.mem8[0, cpu.offset(cpu.er14, 20)] = cpu.r0
        cpu.er4 += 1
        cpu.mem16[0, cpu.offset(cpu.er14, 16)] = cpu.er4
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 70)]
        cpu.push(cpu.er0)
        cpu.er0 = 0
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 20
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.r2 = 0
        cpu.call(NATIVE_DECIMAL)
        cpu.sp += 6
        cpu.compare(cpu.r0, 1)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.ne:
            cpu.jump('bad')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 20)]
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.jump('bad')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, 70)]
        cpu.r0 = cpu.mem8[0, cpu.er4]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.jump('success')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 86)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.jump('success')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er4, 9)]
        cpu.r0 += 5
        cpu.mem8[0, cpu.offset(cpu.er4, 9)] = cpu.r0
        cpu.label('success')
        cpu.er0 = 0
        cpu.jump('out')
        cpu.label('bad')
        cpu.er0 = 4
        cpu.label('out')
        cpu.er2 = cpu.er14
        cpu.er2 += -8
        cpu.sp = cpu.er2
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def string_print():
        # Native text and key pause, four 16-character lines per page.
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er12 = cpu.er0
        cpu.r8 = cpu.r2
        cpu.er10 = cpu.er4
        cpu.sp += -40
        cpu.er14 = cpu.sp
        cpu.r0 = cpu.mem8[0, 0x80A0]
        cpu.mem8[0, cpu.offset(cpu.er14, 26)] = cpu.r0
        cpu.r0 = cpu.mem8[0, 0x80A1]
        cpu.mem8[0, cpu.offset(cpu.er14, 27)] = cpu.r0
        cpu.r0 = cpu.mem8[0, 0x80A2]
        cpu.mem8[0, cpu.offset(cpu.er14, 28)] = cpu.r0
        cpu.r0 = 7
        cpu.mem8[0, 0x80A0] = cpu.r0
        cpu.r0 = 0
        cpu.mem8[0, 0x80A1] = cpu.r0
        cpu.r0 = 1
        cpu.mem8[0, 0x80A2] = cpu.r0
        cpu.label('page')
        cpu.call(0x0409A)
        cpu.r9 = 0
        cpu.label('line')
        cpu.er4 = cpu.er14
        cpu.r3 = 16
        cpu.label('character')
        cpu.er10 = cpu.er10
        if cpu.eq:
            cpu.jump('draw')
        cpu.r0 = cpu.mem8[cpu.r8, cpu.er12]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.r0 = 0x20
        cpu.mem8[0, cpu.er4] = cpu.r0
        cpu.er4 += 1
        cpu.er12 += 1
        cpu.er10 += -1
        cpu.r3 += 255
        if cpu.ne:
            cpu.branch('character')
        cpu.label('draw')
        cpu.r0 = 0
        cpu.mem8[0, cpu.er4] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.r0 = 0
        cpu.r1 = cpu.r9
        cpu.r1 <<= 3
        cpu.r1 += 1
        cpu.call(0x041DA)
        cpu.r9 += 1
        cpu.er10 = cpu.er10
        if cpu.eq:
            cpu.jump('pause')
        cpu.compare(cpu.r9, 4)
        if cpu.lt:
            cpu.branch('line')
        cpu.label('pause')
        cpu.call(0x043BE)
        cpu.er0 = cpu.er14
        cpu.er0 += 30
        cpu.call(0x12576)
        cpu.er10 = cpu.er10
        if cpu.ne:
            cpu.jump('page')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 26)]
        cpu.mem8[0, 0x80A0] = cpu.r0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 27)]
        cpu.mem8[0, 0x80A1] = cpu.r0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 28)]
        cpu.mem8[0, 0x80A2] = cpu.r0
        cpu.er0 = 0
        cpu.sp += 40
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
