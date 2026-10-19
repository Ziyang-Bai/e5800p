"""Numbered native20 matrices. All movable storage belongs to E5BWORK/MCS."""

from kits import cpu


# Source descriptors are reopened after allocation; DD survives workspace lookup.
AD, BD, WD, DD = 0, 0, 0, 16
ARGS, RESULT, INPUT, OP = 32, 56, 58, 78
AR, AC, BR, BC, NR, NC = 80, 82, 84, 86, 88, 90
AZ, BZ, CZ, AB, BB, CB, SIZE = 92, 94, 96, 98, 100, 102, 104
STRIDE, RANK, COL, ROW, BEST = 106, 108, 110, 112, 114
I, J, K, P, Q, T, SIGN = 116, 118, 120, 122, 124, 126, 131
FRAME = 136
NUM = 4
ZERO, ONE, PIVOT, FACTOR, ACC, TEMP, ABS_A, ABS_B = range(848, 1008, 20)
DATA = 1008


def install(fw):
    @fw.function(native=True)
    def matrix_copy():
        # ER0/R2 source, ER4/R6 destination, ER12 byte count.
        cpu.er12 = cpu.er12
        if cpu.eq:
            cpu.ret()
        cpu.label('copy')
        cpu.r3 = cpu.mem8[cpu.r2, cpu.er0]
        cpu.mem8[cpu.r6, cpu.er4] = cpu.r3
        cpu.er0 += 1
        cpu.er4 += 1
        cpu.er12 += -1
        if cpu.ne:
            cpu.branch('copy')
        cpu.ret()

    @fw.function(native=True)
    def matrix_size():
        # Positive ER4 rows, ER6 cols -> ER12 native20 byte length.
        # Bound before every addition, including the final 8-byte header.
        cpu.er12 = 0
        cpu.er4 = cpu.er4
        if cpu.eq:
            cpu.branch('bad')
        cpu.er6 = cpu.er6
        if cpu.eq:
            cpu.branch('bad')
        cpu.er2 = 3276
        cpu.compare(cpu.er4, cpu.er2)
        if cpu.gt:
            cpu.branch('bad')
        cpu.compare(cpu.er6, cpu.er2)
        if cpu.gt:
            cpu.branch('bad')
        cpu.er0 = cpu.er4
        cpu.label('rows')
        cpu.er12 += cpu.er6
        cpu.compare(cpu.er12, cpu.er2)
        if cpu.gt:
            cpu.branch('bad')
        cpu.er0 += -1
        if cpu.ne:
            cpu.branch('rows')
        cpu.er0 = cpu.er12
        cpu.er12 += cpu.er12
        cpu.er12 += cpu.er12
        cpu.er12 += cpu.er0
        cpu.er12 += cpu.er12
        cpu.er12 += cpu.er12
        cpu.er0 = 0
        cpu.ret()
        cpu.label('bad')
        cpu.er0 = 4
        cpu.ret()

    @fw.function(native=True)
    def matrix_shape():
        cpu.push(cpu.lr)
        cpu.push(cpu.er0)
        cpu.r2 = 0
        cpu.r3 = 0
        cpu.er6 = 0
        cpu.call('fn_object_open')
        cpu.pop(cpu.er12)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er12, 14)]
        cpu.compare(cpu.r0, 8)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.lt:
            cpu.er0 = 4
            cpu.jump('out')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er12, 10)]
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er12, 12)]
        cpu.er4 = cpu.mem16[cpu.r2, cpu.offset(cpu.er0, 4)]
        cpu.er6 = cpu.mem16[cpu.r2, cpu.offset(cpu.er0, 6)]
        cpu.push(cpu.er12)
        cpu.call('fn_matrix_size')
        cpu.pop(cpu.er2)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er2, 14)]
        cpu.er2 = cpu.er12
        cpu.er2 += 8
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.er0 = 4
        else:
            cpu.er0 = 0
        cpu.label('out')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_work():
        cpu.push(cpu.lr)
        cpu.er0 = cpu.er14
        cpu.er6 = 0
        cpu.r3 = 0
        cpu.call('fn_object_work')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.er8 = cpu.mem16[0, cpu.offset(cpu.er14, WD + 10)]
            cpu.r10 = cpu.mem8[0, cpu.offset(cpu.er14, WD + 12)]
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_move():
        cpu.push(cpu.lr)
        cpu.er0 += cpu.er8
        cpu.er4 += cpu.er8
        cpu.r2 = cpu.r10
        cpu.r6 = cpu.r10
        cpu.er12 = 20
        cpu.call('fn_matrix_copy')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_math():
        cpu.push(cpu.lr)
        cpu.push(cpu.er12)
        cpu.er4 += cpu.er8
        cpu.er6 += cpu.er8
        cpu.er0 = cpu.er8
        cpu.er0 += NUM
        cpu.r2 = cpu.r10
        cpu.call('fn_graph_arithmetic')
        cpu.pop(cpu.er4)
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.er0 = 4
            cpu.pop(cpu.pc)
        cpu.er0 = NUM + 24
        cpu.call('fn_matrix_move')
        cpu.er0 = 0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_number():
        # Reuse BASIC's exact unsigned integer -> native20 conversion.
        cpu.push(cpu.lr)
        cpu.mem16[0, cpu.offset(cpu.er14, INPUT)] = cpu.er0
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er14, INPUT + 2)] = cpu.er0
        cpu.er0 = cpu.er14
        cpu.er0 += INPUT
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, RESULT)]
        cpu.call(0xFB538)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_cell():
        # ER0 row, ER2 col, zero based; STRIDE bytes per row, AB base.
        cpu.er4 = 0
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, STRIDE)]
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('column')
        cpu.label('row')
        cpu.er4 += cpu.er6
        cpu.er0 += -1
        if cpu.ne:
            cpu.branch('row')
        cpu.label('column')
        cpu.er0 = cpu.er2
        cpu.er0 += cpu.er0
        cpu.er0 += cpu.er0
        cpu.er0 += cpu.er2
        cpu.er0 += cpu.er0
        cpu.er0 += cpu.er0
        cpu.er4 += cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, AB)]
        cpu.er0 += cpu.er4
        cpu.ret()

    @fw.function(native=True)
    def matrix():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er12 = cpu.er2
        cpu.r11 = cpu.r0
        cpu.sp += -128
        cpu.sp += -8
        cpu.er14 = cpu.sp
        cpu.mem16[0, cpu.offset(cpu.er14, RESULT)] = cpu.er4
        cpu.mem8[0, cpu.offset(cpu.er14, OP)] = cpu.r11
        cpu.er0 = cpu.er12
        cpu.er4 = cpu.er14
        cpu.er4 += ARGS
        cpu.r2 = 0
        cpu.r6 = 0
        cpu.er12 = 24
        cpu.call('fn_matrix_copy')
        # Input is copied before any allocation and before RESULT is cleared.
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, FRAME + 10)]
        # Saved XR4 contains incoming ER6 at its high word.
        cpu.er4 = cpu.er14
        cpu.er4 += INPUT
        cpu.er12 = 20
        cpu.call('fn_matrix_copy')
        cpu.compare(cpu.r11, 12)
        if cpu.ge:
            cpu.jump('bad')
        cpu.compare(cpu.r11, 5)
        if cpu.ge:
            cpu.call('fn_matrix_calc')
        else:
            cpu.call('fn_matrix_access')
        cpu.jump('out')
        cpu.label('bad')
        cpu.er0 = 4
        cpu.label('out')
        cpu.sp += 127
        cpu.sp += 9
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_access():
        cpu.push(cpu.lr)
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, ARGS + 4)]
            cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, ARGS + 8)]
            cpu.call('fn_matrix_size')
            cpu.er0 = cpu.er0
            if cpu.ne:
                cpu.jump('out')
            cpu.mem16[0, cpu.offset(cpu.er14, NR)] = cpu.er4
            cpu.mem16[0, cpu.offset(cpu.er14, NC)] = cpu.er6
            cpu.er6 = cpu.er12
            cpu.er6 += 8
            cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, ARGS)]
            cpu.er0 = cpu.er14
            cpu.er0 += DD
            cpu.r2 = 0
            cpu.r3 = 1
            cpu.call('fn_object_open')
            cpu.er0 = cpu.er0
            if cpu.ne:
                cpu.jump('out')
            cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, DD + 10)]
            cpu.r6 = cpu.mem8[0, cpu.offset(cpu.er14, DD + 12)]
            cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, NR)]
            cpu.mem16[cpu.r6, cpu.offset(cpu.er4, 4)] = cpu.er0
            cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, NC)]
            cpu.mem16[cpu.r6, cpu.offset(cpu.er4, 6)] = cpu.er0
            cpu.er4 += 8
            cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er14, DD + 14)]
            cpu.er12 += -8
            cpu.r0 = 0
            cpu.label('zero')
            cpu.mem8[cpu.r6, cpu.er4] = cpu.r0
            cpu.er4 += 1
            cpu.er12 += -1
            if cpu.ne:
                cpu.branch('zero')
            cpu.jump('statement')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, ARGS)]
        cpu.er0 = cpu.er14
        cpu.call('fn_matrix_shape')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.mem16[0, cpu.offset(cpu.er14, AR)] = cpu.er4
        cpu.mem16[0, cpu.offset(cpu.er14, AC)] = cpu.er6
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
        cpu.compare(cpu.r0, 3)
        if cpu.ge:
            cpu.compare(cpu.r0, 3)
            if cpu.eq:
                cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, AR)]
            else:
                cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, AC)]
            cpu.call('fn_matrix_number')
            cpu.jump('out')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, ARGS + 4)]
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.jump('bad')
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, AR)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.gt:
            cpu.jump('bad')
        cpu.er0 += -1
        cpu.mem16[0, cpu.offset(cpu.er14, ROW)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, ARGS + 8)]
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.jump('bad')
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, AC)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.gt:
            cpu.jump('bad')
        cpu.er0 += -1
        cpu.mem16[0, cpu.offset(cpu.er14, COL)] = cpu.er0
        cpu.er4 = 1
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, AC)]
        cpu.call('fn_matrix_size')
        cpu.mem16[0, cpu.offset(cpu.er14, STRIDE)] = cpu.er12
        cpu.er0 = 8
        cpu.mem16[0, cpu.offset(cpu.er14, AB)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, ROW)]
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, COL)]
        cpu.call('fn_matrix_cell')
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, AD + 10)]
        cpu.er0 += cpu.er2
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
        cpu.compare(cpu.r0, 1)
        if cpu.eq:
            cpu.er0 = cpu.er14
            cpu.er0 += INPUT
            cpu.r2 = 0
            cpu.call('fn_graph_scalar')
            cpu.compare(cpu.r0, 0)
            if cpu.ne:
                cpu.jump('bad')
            cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
            cpu.r6 = cpu.mem8[0, cpu.offset(cpu.er14, AD + 12)]
            cpu.er0 = cpu.er14
            cpu.er0 += INPUT
            cpu.r2 = 0
        else:
            cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
            cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, AD + 12)]
            cpu.call('fn_graph_scalar')
            cpu.compare(cpu.r0, 0)
            if cpu.ne:
                cpu.jump('bad')
            cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
            cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, AD + 12)]
            cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, RESULT)]
            cpu.r6 = 0
        cpu.er12 = 20
        cpu.call('fn_matrix_copy')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
        cpu.compare(cpu.r0, 1)
        if cpu.ne:
            cpu.er0 = 0
            cpu.jump('out')
        cpu.label('statement')
        cpu.er0 = 0
        cpu.call('fn_matrix_number')
        cpu.jump('out')
        cpu.label('bad')
        cpu.er0 = 4
        cpu.label('out')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_calc():
        cpu.push(cpu.lr)
        cpu.call('fn_matrix_prepare')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
        cpu.compare(cpu.r0, 9)
        if cpu.ge:
            cpu.call('fn_matrix_eliminate')
        else:
            cpu.call('fn_matrix_product')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
        cpu.compare(cpu.r0, 10)
        if cpu.eq:
            cpu.er0 = ACC
            cpu.er0 += cpu.er8
            cpu.r2 = cpu.r10
            cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, RESULT)]
            cpu.r6 = 0
            cpu.er12 = 20
            cpu.call('fn_matrix_copy')
        else:
            cpu.call('fn_matrix_commit')
            cpu.er0 = cpu.er0
            if cpu.ne:
                cpu.jump('out')
            cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
            cpu.compare(cpu.r0, 9)
            if cpu.eq:
                cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, RANK)]
            else:
                cpu.er0 = 0
            cpu.call('fn_matrix_number')
            cpu.er0 = cpu.er0
            if cpu.ne:
                cpu.jump('out')
        cpu.er0 = 0
        cpu.label('out')
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er6 = 0
        cpu.r3 = 2
        cpu.call('fn_object_work')
        cpu.pop(cpu.er2)
        cpu.er2 = cpu.er2
        if cpu.ne:
            cpu.er0 = cpu.er2
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_prepare():
        cpu.push(cpu.lr)
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
        cpu.compare(cpu.r0, 9)
        if cpu.lt:
            cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, ARGS + 4)]
        else:
            cpu.compare(cpu.r0, 11)
            if cpu.eq:
                cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, ARGS + 4)]
            else:
                cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, ARGS)]
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er4
        cpu.er0 = cpu.er14
        cpu.call('fn_matrix_shape')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.mem16[0, cpu.offset(cpu.er14, AR)] = cpu.er4
        cpu.mem16[0, cpu.offset(cpu.er14, AC)] = cpu.er6
        cpu.mem16[0, cpu.offset(cpu.er14, NR)] = cpu.er4
        cpu.mem16[0, cpu.offset(cpu.er14, NC)] = cpu.er6
        cpu.mem16[0, cpu.offset(cpu.er14, AZ)] = cpu.er12
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er14, BZ)] = cpu.er0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
        cpu.compare(cpu.r0, 8)
        if cpu.lt:
            cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, ARGS + 8)]
            cpu.er0 = cpu.er14
            cpu.call('fn_matrix_shape')
            cpu.er0 = cpu.er0
            if cpu.ne:
                cpu.jump('out')
            cpu.mem16[0, cpu.offset(cpu.er14, BR)] = cpu.er4
            cpu.mem16[0, cpu.offset(cpu.er14, BC)] = cpu.er6
            cpu.mem16[0, cpu.offset(cpu.er14, BZ)] = cpu.er12
            cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
            cpu.compare(cpu.r0, 7)
            if cpu.eq:
                cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, AC)]
                cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, BR)]
                cpu.compare(cpu.er0, cpu.er2)
                if cpu.ne:
                    cpu.jump('bad')
                cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, BC)]
                cpu.mem16[0, cpu.offset(cpu.er14, NC)] = cpu.er0
            else:
                cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, AR)]
                cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, BR)]
                cpu.compare(cpu.er0, cpu.er2)
                if cpu.ne:
                    cpu.jump('bad')
                cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, AC)]
                cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, BC)]
                cpu.compare(cpu.er0, cpu.er2)
                if cpu.ne:
                    cpu.jump('bad')
        else:
            cpu.compare(cpu.r0, 8)
            if cpu.eq:
                cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, AR)]
                cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, AC)]
                cpu.mem16[0, cpu.offset(cpu.er14, NR)] = cpu.er2
                cpu.mem16[0, cpu.offset(cpu.er14, NC)] = cpu.er0
            else:
                cpu.compare(cpu.r0, 10)
                if cpu.ge:
                    cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, AR)]
                    cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, AC)]
                    cpu.compare(cpu.er0, cpu.er2)
                    if cpu.ne:
                        cpu.jump('bad')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, NR)]
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, NC)]
        cpu.call('fn_matrix_size')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.mem16[0, cpu.offset(cpu.er14, CZ)] = cpu.er12
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
        cpu.compare(cpu.r0, 9)
        if cpu.ge:
            cpu.compare(cpu.r0, 11)
            if cpu.eq:
                cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, CZ)]
                cpu.er2 = 32262
                cpu.compare(cpu.er0, cpu.er2)
                if cpu.gt:
                    cpu.jump('memory')
                cpu.er0 += cpu.er0
                cpu.mem16[0, cpu.offset(cpu.er14, CZ)] = cpu.er0
            else:
                cpu.er0 = 0
                cpu.mem16[0, cpu.offset(cpu.er14, CZ)] = cpu.er0
        cpu.er0 = DATA
        cpu.mem16[0, cpu.offset(cpu.er14, AB)] = cpu.er0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, AZ)]
        cpu.er0 += cpu.er2
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.jump('memory')
        cpu.mem16[0, cpu.offset(cpu.er14, BB)] = cpu.er0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, BZ)]
        cpu.er0 += cpu.er2
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.jump('memory')
        cpu.mem16[0, cpu.offset(cpu.er14, CB)] = cpu.er0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, CZ)]
        cpu.er0 += cpu.er2
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.jump('memory')
        cpu.er2 = 65534
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.gt:
            cpu.jump('memory')
        cpu.mem16[0, cpu.offset(cpu.er14, SIZE)] = cpu.er0
        cpu.er6 = cpu.er0
        cpu.er0 = cpu.er14
        cpu.r3 = 1
        cpu.call('fn_object_work')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.call('fn_matrix_work')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er4 = cpu.er8
        cpu.er4 += 4
        cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er14, SIZE)]
        cpu.er12 += -4
        cpu.r0 = 0
        cpu.label('clear')
        cpu.mem8[cpu.r10, cpu.er4] = cpu.r0
        cpu.er4 += 1
        cpu.er12 += -1
        if cpu.ne:
            cpu.branch('clear')
        cpu.er4 = ONE
        cpu.er4 += cpu.er8
        cpu.r0 = 1
        cpu.mem8[cpu.r10, cpu.er4] = cpu.r0
        cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 9)] = cpu.r0
        cpu.er0 = ONE
        cpu.er4 = ACC
        cpu.call('fn_matrix_move')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
        cpu.er0 = cpu.er14
        cpu.call('fn_matrix_shape')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er0 = cpu.er14
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, AB)]
        cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er14, AZ)]
        cpu.call('fn_matrix_stage')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, BZ)]
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, ARGS + 8)]
            cpu.er0 = cpu.er14
            cpu.call('fn_matrix_shape')
            cpu.er0 = cpu.er0
            if cpu.ne:
                cpu.jump('out')
            cpu.er0 = cpu.er14
            cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, BB)]
            cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er14, BZ)]
            cpu.call('fn_matrix_stage')
            cpu.er0 = cpu.er0
            if cpu.ne:
                cpu.jump('out')
        cpu.er4 = 1
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, AC)]
        cpu.call('fn_matrix_size')
        cpu.mem16[0, cpu.offset(cpu.er14, STRIDE)] = cpu.er12
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
        cpu.compare(cpu.r0, 11)
        if cpu.eq:
            cpu.call('fn_matrix_augment')
        else:
            cpu.compare(cpu.r0, 9)
            if cpu.ge:
                cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, AB)]
                cpu.mem16[0, cpu.offset(cpu.er14, CB)] = cpu.er0
        cpu.er0 = 0
        cpu.jump('out')
        cpu.label('bad')
        cpu.er0 = 4
        cpu.jump('out')
        cpu.label('memory')
        cpu.er0 = 6
        cpu.label('out')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_stage():
        # Descriptor ER0, work-relative destination ER4, bytes ER12.
        cpu.push(cpu.lr)
        cpu.er4 += cpu.er8
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er0, 12)]
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er0, 10)]
        cpu.er0 += 8
        cpu.r6 = cpu.r10
        cpu.push(cpu.er4)
        cpu.push(cpu.er12)
        cpu.call('fn_matrix_copy')
        cpu.pop(cpu.er6)
        cpu.pop(cpu.er4)
        cpu.label('scalar')
        cpu.er0 = cpu.er4
        cpu.r2 = cpu.r10
        cpu.call('fn_graph_scalar')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.er0 = 4
            cpu.jump('out')
        cpu.er4 += 20
        cpu.er6 += -20
        if cpu.ne:
            cpu.branch('scalar')
        cpu.er0 = 0
        cpu.label('out')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_augment():
        cpu.push(cpu.lr)
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, AB)]
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, CB)]
        cpu.mem16[0, cpu.offset(cpu.er14, Q)] = cpu.er0
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er14, I)] = cpu.er0
        cpu.label('row')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, Q)]
        cpu.er0 += cpu.er8
        cpu.er4 += cpu.er8
        cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er14, STRIDE)]
        cpu.r2 = cpu.r10
        cpu.r6 = cpu.r10
        cpu.call('fn_matrix_copy')
        cpu.r0 -= cpu.r8
        cpu.sub_carry(cpu.r1, cpu.r9)
        cpu.r4 -= cpu.r8
        cpu.sub_carry(cpu.r5, cpu.r9)
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, STRIDE)]
        cpu.er4 += cpu.er2
        cpu.mem16[0, cpu.offset(cpu.er14, Q)] = cpu.er4
        # Right half is already zero; set its diagonal to native one.
        cpu.er0 = 0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, I)]
        cpu.push(cpu.er4)
        cpu.call('fn_matrix_cell')
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, AB)]
        cpu.r0 -= cpu.r2
        cpu.sub_carry(cpu.r1, cpu.r3)
        cpu.pop(cpu.er4)
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, STRIDE)]
        cpu.r4 -= cpu.r2
        cpu.sub_carry(cpu.r5, cpu.r3)
        cpu.er4 += cpu.er0
        cpu.er0 = ONE
        cpu.call('fn_matrix_move')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, I)]
        cpu.er0 += 1
        cpu.mem16[0, cpu.offset(cpu.er14, I)] = cpu.er0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, AR)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.jump('row')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, CB)]
        cpu.mem16[0, cpu.offset(cpu.er14, AB)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, STRIDE)]
        cpu.er0 += cpu.er0
        cpu.mem16[0, cpu.offset(cpu.er14, STRIDE)] = cpu.er0
        cpu.er0 = 0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_product():
        cpu.push(cpu.lr)
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, CB)]
        cpu.mem16[0, cpu.offset(cpu.er14, BEST)] = cpu.er0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
        cpu.compare(cpu.r0, 7)
        if cpu.eq:
            cpu.call('fn_matrix_multiply')
            cpu.jump('out')
        cpu.compare(cpu.r0, 8)
        if cpu.eq:
            cpu.call('fn_matrix_transpose')
            cpu.jump('out')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, AB)]
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, BB)]
        cpu.mem16[0, cpu.offset(cpu.er14, Q)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, AZ)]
        cpu.mem16[0, cpu.offset(cpu.er14, K)] = cpu.er0
        cpu.label('cell')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, Q)]
        cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er14, BEST)]
        cpu.r3 = 0x89
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
        cpu.compare(cpu.r0, 6)
        if cpu.eq:
            cpu.r3 = 0x99
        cpu.call('fn_matrix_math')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
        cpu.er0 += 20
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, Q)]
        cpu.er0 += 20
        cpu.mem16[0, cpu.offset(cpu.er14, Q)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, BEST)]
        cpu.er0 += 20
        cpu.mem16[0, cpu.offset(cpu.er14, BEST)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, K)]
        cpu.er0 += -20
        cpu.mem16[0, cpu.offset(cpu.er14, K)] = cpu.er0
        if cpu.ne:
            cpu.jump('cell')
        cpu.er0 = 0
        cpu.label('out')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_transpose():
        cpu.push(cpu.lr)
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er14, I)] = cpu.er0
        cpu.label('row')
        cpu.call('fn_graph_cancel')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.er0 = 4
            cpu.pop(cpu.pc)
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er14, J)] = cpu.er0
        cpu.label('column')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, J)]
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, I)]
        cpu.call('fn_matrix_cell')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, BEST)]
        cpu.call('fn_matrix_move')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, BEST)]
        cpu.er0 += 20
        cpu.mem16[0, cpu.offset(cpu.er14, BEST)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, J)]
        cpu.er0 += 1
        cpu.mem16[0, cpu.offset(cpu.er14, J)] = cpu.er0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, NC)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.jump('column')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, I)]
        cpu.er0 += 1
        cpu.mem16[0, cpu.offset(cpu.er14, I)] = cpu.er0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, NR)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.jump('row')
        cpu.er0 = 0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_multiply():
        cpu.push(cpu.lr)
        cpu.er4 = 1
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, BC)]
        cpu.call('fn_matrix_size')
        cpu.mem16[0, cpu.offset(cpu.er14, ROW)] = cpu.er12
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er14, I)] = cpu.er0
        cpu.label('row')
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er14, J)] = cpu.er0
        cpu.label('column')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, I)]
        cpu.er2 = 0
        cpu.call('fn_matrix_cell')
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.er0 = 0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, J)]
        cpu.call('fn_matrix_cell')
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, AB)]
        cpu.r0 -= cpu.r2
        cpu.sub_carry(cpu.r1, cpu.r3)
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, BB)]
        cpu.er0 += cpu.er2
        cpu.mem16[0, cpu.offset(cpu.er14, Q)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, AC)]
        cpu.mem16[0, cpu.offset(cpu.er14, K)] = cpu.er0
        cpu.er0 = ZERO
        cpu.er4 = ACC
        cpu.call('fn_matrix_move')
        cpu.label('dot')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, Q)]
        cpu.er12 = TEMP
        cpu.r3 = 0xA9
        cpu.call('fn_matrix_math')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.r3 = 0x89
        cpu.er4 = ACC
        cpu.er6 = TEMP
        cpu.er12 = ACC
        cpu.call('fn_matrix_math')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
        cpu.er0 += 20
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, Q)]
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, ROW)]
        cpu.er0 += cpu.er2
        cpu.mem16[0, cpu.offset(cpu.er14, Q)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, K)]
        cpu.er0 += -1
        cpu.mem16[0, cpu.offset(cpu.er14, K)] = cpu.er0
        if cpu.ne:
            cpu.jump('dot')
        cpu.er0 = ACC
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, BEST)]
        cpu.call('fn_matrix_move')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, BEST)]
        cpu.er0 += 20
        cpu.mem16[0, cpu.offset(cpu.er14, BEST)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, J)]
        cpu.er0 += 1
        cpu.mem16[0, cpu.offset(cpu.er14, J)] = cpu.er0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, NC)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.jump('column')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, I)]
        cpu.er0 += 1
        cpu.mem16[0, cpu.offset(cpu.er14, I)] = cpu.er0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, NR)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.jump('row')
        cpu.er0 = 0
        cpu.label('out')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_commit():
        cpu.push(cpu.lr)
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, NR)]
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, NC)]
        cpu.call('fn_matrix_size')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er6 = cpu.er12
        cpu.er6 += 8
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, ARGS)]
        cpu.er0 = cpu.er14
        cpu.er0 += DD
        cpu.r2 = 0
        cpu.r3 = 1
        cpu.call('fn_object_open')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        # Destination creation can move the workspace. Reopen both descriptors.
        cpu.call('fn_matrix_work')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, DD + 10)]
        cpu.r6 = cpu.mem8[0, cpu.offset(cpu.er14, DD + 12)]
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, NR)]
        cpu.mem16[cpu.r6, cpu.offset(cpu.er4, 4)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, NC)]
        cpu.mem16[cpu.r6, cpu.offset(cpu.er4, 6)] = cpu.er0
        cpu.er4 += 8
        cpu.mem16[0, cpu.offset(cpu.er14, Q)] = cpu.er4
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, CB)]
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, NR)]
        cpu.mem16[0, cpu.offset(cpu.er14, I)] = cpu.er0
        cpu.er4 = 1
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er14, NC)]
        cpu.call('fn_matrix_size')
        cpu.mem16[0, cpu.offset(cpu.er14, T)] = cpu.er12
        cpu.label('row')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
        cpu.compare(cpu.r2, 11)
        if cpu.eq:
            cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, T)]
            cpu.er0 += cpu.er2
        cpu.er0 += cpu.er8
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, Q)]
        cpu.r2 = cpu.r10
        cpu.r6 = cpu.mem8[0, cpu.offset(cpu.er14, DD + 12)]
        cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er14, T)]
        cpu.call('fn_matrix_copy')
        cpu.mem16[0, cpu.offset(cpu.er14, Q)] = cpu.er4
        cpu.r0 -= cpu.r8
        cpu.sub_carry(cpu.r1, cpu.r9)
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, I)]
        cpu.er0 += -1
        cpu.mem16[0, cpu.offset(cpu.er14, I)] = cpu.er0
        if cpu.ne:
            cpu.jump('row')
        cpu.er0 = 0
        cpu.label('out')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_pivot():
        cpu.push(cpu.lr)
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, RANK)]
        cpu.mem16[0, cpu.offset(cpu.er14, BEST)] = cpu.er0
        cpu.mem16[0, cpu.offset(cpu.er14, I)] = cpu.er0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, COL)]
        cpu.call('fn_matrix_cell')
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.label('next')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, I)]
        cpu.er0 += 1
        cpu.mem16[0, cpu.offset(cpu.er14, I)] = cpu.er0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, AR)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.jump('done')
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, COL)]
        cpu.call('fn_matrix_cell')
        cpu.mem16[0, cpu.offset(cpu.er14, Q)] = cpu.er0
        cpu.er4 = ABS_A
        cpu.call('fn_matrix_move')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
        cpu.er4 = ABS_B
        cpu.call('fn_matrix_move')
        cpu.er4 = ABS_A
        cpu.er4 += cpu.er8
        cpu.er6 = ABS_B
        cpu.er6 += cpu.er8
        cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 9)]
        cpu.compare(cpu.r0, 5)
        if cpu.ge:
            cpu.r0 += 251
            cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 9)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er6, 9)]
        cpu.compare(cpu.r0, 5)
        if cpu.ge:
            cpu.r0 += 251
            cpu.mem8[cpu.r10, cpu.offset(cpu.er6, 9)] = cpu.r0
        cpu.call('fn_graph_compare')
        cpu.compare(cpu.r0, 4)
        if cpu.eq:
            cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, I)]
            cpu.mem16[0, cpu.offset(cpu.er14, BEST)] = cpu.er0
            cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, Q)]
            cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.jump('next')
        cpu.label('done')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
        cpu.er4 += cpu.er8
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.r1 = 0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_swap():
        cpu.push(cpu.lr)
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, RANK)]
        cpu.er2 = 0
        cpu.call('fn_matrix_cell')
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, BEST)]
        cpu.er2 = 0
        cpu.call('fn_matrix_cell')
        cpu.er4 = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
        cpu.er0 += cpu.er8
        cpu.er4 += cpu.er8
        cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er14, STRIDE)]
        cpu.label('byte')
        cpu.r2 = cpu.mem8[cpu.r10, cpu.er0]
        cpu.r3 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.mem8[cpu.r10, cpu.er0] = cpu.r3
        cpu.mem8[cpu.r10, cpu.er4] = cpu.r2
        cpu.er0 += 1
        cpu.er4 += 1
        cpu.er12 += -1
        if cpu.ne:
            cpu.branch('byte')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, SIGN)]
        cpu.r0 ^= 1
        cpu.mem8[0, cpu.offset(cpu.er14, SIGN)] = cpu.r0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_eliminate():
        cpu.push(cpu.lr)
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er14, RANK)] = cpu.er0
        cpu.mem16[0, cpu.offset(cpu.er14, COL)] = cpu.er0
        cpu.mem8[0, cpu.offset(cpu.er14, SIGN)] = cpu.r0
        cpu.label('column')
        cpu.call('fn_graph_cancel')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.jump('bad')
        cpu.call('fn_matrix_pivot')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
            cpu.compare(cpu.r0, 9)
            if cpu.ne:
                cpu.compare(cpu.r0, 11)
                if cpu.eq:
                    cpu.jump('bad')
                cpu.er0 = ZERO
                cpu.er4 = ACC
                cpu.call('fn_matrix_move')
                cpu.jump('done')
            cpu.jump('next')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, BEST)]
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, RANK)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.call('fn_matrix_swap')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, RANK)]
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, COL)]
        cpu.call('fn_matrix_cell')
        cpu.mem16[0, cpu.offset(cpu.er14, BEST)] = cpu.er0
        cpu.er4 = PIVOT
        cpu.call('fn_matrix_move')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
        cpu.compare(cpu.r0, 10)
        if cpu.eq:
            cpu.r3 = 0xa9
            cpu.er4 = ACC
            cpu.er6 = PIVOT
            cpu.er12 = ACC
            cpu.call('fn_matrix_math')
            cpu.er0 = cpu.er0
            if cpu.ne:
                cpu.jump('out')
        cpu.call('fn_matrix_reduce')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, RANK)]
        cpu.er0 += 1
        cpu.mem16[0, cpu.offset(cpu.er14, RANK)] = cpu.er0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, AR)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.jump('done')
        cpu.label('next')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, COL)]
        cpu.er0 += 1
        cpu.mem16[0, cpu.offset(cpu.er14, COL)] = cpu.er0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, AC)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.jump('column')
        cpu.label('done')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, OP)]
        cpu.compare(cpu.r0, 10)
        if cpu.eq:
            cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, SIGN)]
            cpu.compare(cpu.r0, 0)
            if cpu.ne:
                cpu.r3 = 0x99
                cpu.er4 = ZERO
                cpu.er6 = ACC
                cpu.er12 = ACC
                cpu.call('fn_matrix_math')
                cpu.er0 = cpu.er0
                if cpu.ne:
                    cpu.jump('out')
        cpu.er0 = 0
        cpu.jump('out')
        cpu.label('bad')
        cpu.er0 = 4
        cpu.label('out')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def matrix_reduce():
        cpu.push(cpu.lr)
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, RANK)]
        cpu.er2 = 0
        cpu.call('fn_matrix_cell')
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, STRIDE)]
        cpu.mem16[0, cpu.offset(cpu.er14, K)] = cpu.er0
        cpu.label('normalize')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
        cpu.er6 = PIVOT
        cpu.er12 = cpu.er4
        cpu.r3 = 0xB9
        cpu.call('fn_matrix_math')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
        cpu.er0 += 20
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, K)]
        cpu.er0 += -20
        cpu.mem16[0, cpu.offset(cpu.er14, K)] = cpu.er0
        if cpu.ne:
            cpu.jump('normalize')
        cpu.er0 = ONE
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, BEST)]
        cpu.call('fn_matrix_move')
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er14, I)] = cpu.er0
        cpu.label('row')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, I)]
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, RANK)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.eq:
            cpu.jump('next')
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, COL)]
        cpu.call('fn_matrix_cell')
        cpu.mem16[0, cpu.offset(cpu.er14, T)] = cpu.er0
        cpu.er4 = cpu.er0
        cpu.er4 += cpu.er8
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.jump('next')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, T)]
        cpu.er4 = FACTOR
        cpu.call('fn_matrix_move')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, I)]
        cpu.er2 = 0
        cpu.call('fn_matrix_cell')
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, RANK)]
        cpu.er2 = 0
        cpu.call('fn_matrix_cell')
        cpu.mem16[0, cpu.offset(cpu.er14, Q)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, STRIDE)]
        cpu.mem16[0, cpu.offset(cpu.er14, K)] = cpu.er0
        cpu.label('cell')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, Q)]
        cpu.er6 = FACTOR
        cpu.er12 = TEMP
        cpu.r3 = 0xA9
        cpu.call('fn_matrix_math')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
        cpu.er6 = TEMP
        cpu.er12 = cpu.er4
        cpu.r3 = 0x99
        cpu.call('fn_matrix_math')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('out')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, P)]
        cpu.er0 += 20
        cpu.mem16[0, cpu.offset(cpu.er14, P)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, Q)]
        cpu.er0 += 20
        cpu.mem16[0, cpu.offset(cpu.er14, Q)] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, K)]
        cpu.er0 += -20
        cpu.mem16[0, cpu.offset(cpu.er14, K)] = cpu.er0
        if cpu.ne:
            cpu.jump('cell')
        cpu.er0 = ZERO
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, T)]
        cpu.call('fn_matrix_move')
        cpu.label('next')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, I)]
        cpu.er0 += 1
        cpu.mem16[0, cpu.offset(cpu.er14, I)] = cpu.er0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, AR)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.jump('row')
        cpu.er0 = 0
        cpu.label('out')
        cpu.pop(cpu.pc)
