"""Independent GRAPH screen and world-coordinate MCS drawings."""

from kits import cpu

from .graph_math import _number


FRAME = 384
HEADER = 32
D = 128
BANK = 130
COL = 132
CX = 134
CY = 135
MODE = 136
PAGE = 137
KIND = 138
SIZE = 140
COUNT = 142
POS = 144
DEPTH = 146
PREV = 148
FONT = 348
TRACE_X = 352
TRACE_VALID = 372
OWN_WORK = 373

# Slots relative to the graph_math descriptor. The analysis union is scratch.
XMIN = 192
XMAX = 212
YMIN = 232
YMAX = 252
V = 272
T = 292
U = 312
W = 332
P = 352
Q = 372
DX = 392
DY = 412
N = 472
ZERO = 512
ONE = 532
XS = 432
YS = 452
TOL = 128
TWO = 552
FOUR = 572
WIDTH = 592
HEIGHT = 612
SAVED_Y = 844

INITIAL = b'EGS1' + (88).to_bytes(2, 'little') + _number('-10') + _number('10') + _number('-10') + _number('10') + b'\0\0'
CONSTANTS = _number('0') + _number('1') + _number('2') + _number('4') + _number('95') + _number('30')


def install(fw):
    @fw.function(native=True)
    def graph():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.sp += -128
        cpu.sp += -128
        cpu.sp += -128
        cpu.er14 = cpu.sp
        cpu.er0 = cpu.er14
        cpu.er2 = FRAME
        cpu.r4 = 0
        cpu.label('zero')
        cpu.mem8[cpu.er0] = cpu.r4
        cpu.er0 += 1
        cpu.er2 += -1
        if cpu.ne:
            cpu.branch('zero')
        cpu.r0 = cpu.mem8[0x80A0]
        cpu.mem8[cpu.offset(cpu.er14, FONT)] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A1]
        cpu.mem8[cpu.offset(cpu.er14, FONT + 1)] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A2]
        cpu.mem8[cpu.offset(cpu.er14, FONT + 2)] = cpu.r0
        cpu.r0 = 7
        cpu.mem8[0x80A0] = cpu.r0
        cpu.r0 = 0
        cpu.mem8[0x80A1] = cpu.r0
        cpu.r0 = 1
        cpu.mem8[0x80A2] = cpu.r0
        cpu.call('fn_graph_names')
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.call('fn_mcs_open')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.branch('name_used')
        cpu.compare(cpu.r0, 4)
        if cpu.eq:
            cpu.branch('create')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.jump('memory')
        cpu.call('fn_graph_load')
        cpu.compare(cpu.r0, 2)
        if cpu.ne:
            cpu.branch('skip_99')
        cpu.label('name_used')
        cpu.call('fn_graph_name_used')
        cpu.jump('leave')
        cpu.label('skip_99')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('ready')
        cpu.call('fn_graph_bad_data')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.ne:
            cpu.jump('leave')
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.call('fn_mcs_remove')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.jump('memory')
        cpu.label('create')
        cpu.r0 = 1
        cpu.mem8[cpu.offset(cpu.er14, 23)] = cpu.r0
        cpu.er0 = 88
        cpu.mem16[cpu.offset(cpu.er14, 24)] = cpu.er0
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.call('fn_mcs_open')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.branch('name_used')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.jump('memory')
        cpu.call('initial')
        cpu.data(INITIAL)
        cpu.label('initial')
        cpu.push(cpu.lr)
        cpu.pop(cpu.xr0)
        cpu.er4 = cpu.er14
        cpu.er4 += HEADER
        cpu.r6 = 0
        cpu.r3 = 88
        cpu.call('fn_graph_copy')
        cpu.call('fn_graph_save')
        cpu.label('ready')
        cpu.r0 = 47
        cpu.mem8[cpu.offset(cpu.er14, CX)] = cpu.r0
        cpu.r0 = 15
        cpu.mem8[cpu.offset(cpu.er14, CY)] = cpu.r0
        cpu.label('redraw')
        cpu.call('fn_graph_release')
        cpu.call('fn_graph_prepare')
        cpu.compare(cpu.r0, 4)
        if cpu.eq:
            cpu.branch('leave')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.branch('leave')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('memory')
        cpu.call('fn_graph_plot')
        cpu.call('fn_graph_record_replay')
        cpu.call(0x043BE)
        cpu.label('browse')
        cpu.call(0x80800)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.branch('leave')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.eq:
            cpu.branch('edit')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.compare(cpu.r1, 0x7D)
            if cpu.eq:
                cpu.branch('menu')
        cpu.compare(cpu.r0, 0x36)
        if cpu.eq:
            cpu.call(0x80800)
            cpu.compare(cpu.r0, 0xFF)
            if cpu.ne:
                cpu.branch('skip_174')
            cpu.r0 = 0x38
            cpu.label('skip_174')
            cpu.compare(cpu.r0, 0xFE)
            if cpu.ne:
                cpu.branch('skip_177')
            cpu.r0 = 0x32
            cpu.label('skip_177')
        cpu.call('fn_graph_pan_zoom')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('redraw')
        cpu.branch('browse')
        cpu.label('edit')
        cpu.call('fn_graph_formula_edit')
        cpu.compare(cpu.r0, 2)
        if cpu.ne:
            cpu.branch('edited')
        cpu.call('fn_graph_error')
        cpu.label('edited')
        cpu.branch('redraw')
        cpu.label('menu')
        cpu.call('fn_graph_menu')
        cpu.compare(cpu.r0, 0x31)
        if cpu.ne:
            cpu.branch('skip_190')
        cpu.call('fn_graph_trace')
        cpu.label('skip_190')
        cpu.compare(cpu.r0, 0x32)
        if cpu.ne:
            cpu.branch('skip_193')
        cpu.call('fn_graph_calculate')
        cpu.label('skip_193')
        cpu.compare(cpu.r0, 0x33)
        if cpu.ne:
            cpu.branch('skip_196')
        cpu.call('fn_graph_view_menu')
        cpu.label('skip_196')
        cpu.compare(cpu.r0, 0x34)
        if cpu.ne:
            cpu.branch('skip_199')
        cpu.call('fn_graph_sketch')
        cpu.label('skip_199')
        cpu.branch('redraw')
        cpu.label('memory')
        cpu.call('fn_graph_error')
        cpu.label('leave')
        cpu.call('fn_graph_close_work')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, FONT)]
        cpu.mem8[0x80A0] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, FONT + 1)]
        cpu.mem8[0x80A1] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, FONT + 2)]
        cpu.mem8[0x80A2] = cpu.r0
        cpu.sp += 127
        cpu.sp += 127
        cpu.sp += 127
        cpu.sp += 3
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_names():
        cpu.push(cpu.lr)
        cpu.call('names')
        cpu.data(b'main\0E5GWORK\0E5GRAPH\0\0')
        cpu.label('names')
        cpu.push(cpu.lr)
        cpu.pop(cpu.xr0)
        cpu.mem16[cpu.er14] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 16)] = cpu.er0
        cpu.mem8[cpu.offset(cpu.er14, 2)] = cpu.r2
        cpu.mem8[cpu.offset(cpu.er14, 18)] = cpu.r2
        cpu.er0 += 5
        cpu.mem16[cpu.offset(cpu.er14, 4)] = cpu.er0
        cpu.mem8[cpu.offset(cpu.er14, 6)] = cpu.r2
        cpu.er0 += 8
        cpu.mem16[cpu.offset(cpu.er14, 20)] = cpu.er0
        cpu.mem8[cpu.offset(cpu.er14, 22)] = cpu.r2
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_load():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_owner')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_245')
        cpu.pop(cpu.pc)
        cpu.label('skip_245')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 30)]
        cpu.compare(cpu.r0, 88)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.lt:
            cpu.branch('bad')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 26)]
        cpu.r2 = cpu.mem8[cpu.offset(cpu.er14, 28)]
        cpu.er4 = cpu.er14
        cpu.er4 += HEADER
        cpu.r6 = 0
        cpu.r3 = 88
        cpu.call('fn_graph_copy')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, HEADER)]
        cpu.compare(cpu.r0, 0x45)
        cpu.compare_carry(cpu.r1, 0x47)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, HEADER + 2)]
        cpu.compare(cpu.r0, 0x53)
        cpu.compare_carry(cpu.r1, 0x31)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, HEADER + 4)]
        cpu.er0 += 1
        cpu.r0 &= 0xFE
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er14, 30)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.branch('bad')
        cpu.call('fn_graph_records_check')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('skip_276')
        cpu.call('fn_graph_bounds_check')
        cpu.label('skip_276')
        cpu.pop(cpu.pc)
        cpu.label('bad')
        cpu.r0 = 1
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_save():
        cpu.push(cpu.lr)
        cpu.er0 = cpu.er14
        cpu.er0 += HEADER
        cpu.r2 = 0
        cpu.er4 = cpu.mem16[cpu.offset(cpu.er14, 26)]
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, 28)]
        cpu.r3 = 88
        cpu.call('fn_graph_copy')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_work():
        cpu.push(cpu.lr)
        cpu.r0 = 0
        cpu.mem8[cpu.offset(cpu.er14, 7)] = cpu.r0
        cpu.er0 = cpu.er14
        cpu.call('fn_mcs_open')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('end')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 10)]
        cpu.r0 += 4
        cpu.add_carry(cpu.r1, 12)
        cpu.mem16[cpu.offset(cpu.er14, D)] = cpu.er0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 12)]
        cpu.mem8[cpu.offset(cpu.er14, BANK)] = cpu.r0
        cpu.r0 = 0
        cpu.label('end')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_slots():
        cpu.er8 = cpu.mem16[cpu.offset(cpu.er14, D)]
        cpu.r10 = cpu.mem8[cpu.offset(cpu.er14, BANK)]
        cpu.ret()

    @fw.function(native=True)
    def graph_op():
        # Relative operands ER4/ER6, destination ER12; R3 is the native token.
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.er2)
        cpu.push(cpu.er4)
        cpu.er0 = 24
        cpu.er4 = SAVED_Y
        cpu.call('fn_graph_move')
        cpu.pop(cpu.er4)
        cpu.pop(cpu.er2)
        cpu.call('fn_graph_slots')
        cpu.er4 += cpu.er8
        cpu.er6 += cpu.er8
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.call('fn_graph_arithmetic')
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er8
        cpu.er0 += 24
        cpu.r2 = cpu.r10
        cpu.er4 = cpu.er8
        cpu.er4 += cpu.er12
        cpu.r6 = cpu.r10
        cpu.r3 = 20
        cpu.call('fn_graph_copy')
        cpu.er0 = SAVED_Y
        cpu.er4 = 24
        cpu.call('fn_graph_move')
        cpu.pop(cpu.er0)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_move():
        # Relative source ER0 and destination ER4, both native20.
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.call('fn_graph_slots')
        cpu.er0 += cpu.er8
        cpu.er4 += cpu.er8
        cpu.r2 = cpu.r10
        cpu.r6 = cpu.r10
        cpu.r3 = 20
        cpu.call('fn_graph_copy')
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_cmp():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.call('fn_graph_slots')
        cpu.er4 += cpu.er8
        cpu.er6 += cpu.er8
        cpu.call('fn_graph_compare')
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_integer():
        # R0 unsigned (0..99) -> native20 slot N.
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.er4 = cpu.mem16[cpu.offset(cpu.er14, D)]
        cpu.r4 += 216
        cpu.add_carry(cpu.r5, 1)
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, BANK)]
        cpu.r3 = 20
        cpu.r2 = 0
        cpu.label('clear')
        cpu.mem8[cpu.r6, cpu.er4] = cpu.r2
        cpu.er4 += 1
        cpu.r3 += 255
        if cpu.ne:
            cpu.branch('clear')
        cpu.er4 += -20
        cpu.r1 = 0
        cpu.label('tens')
        cpu.compare(cpu.r0, 10)
        if cpu.lt:
            cpu.branch('digits')
        cpu.r0 += 246
        cpu.r1 += 1
        cpu.branch('tens')
        cpu.label('digits')
        cpu.compare(cpu.r1, 0)
        if cpu.eq:
            cpu.mem8[cpu.r6, cpu.er4] = cpu.r0
            cpu.compare(cpu.r0, 0)
            if cpu.eq:
                cpu.branch('skip_402')
            cpu.r0 = 1
            cpu.mem8[cpu.r6, cpu.offset(cpu.er4, 9)] = cpu.r0
            cpu.label('skip_402')
        else:
            cpu.mem8[cpu.r6, cpu.er4] = cpu.r1
            cpu.r0 <<= 4
            cpu.mem8[cpu.r6, cpu.offset(cpu.er4, 1)] = cpu.r0
            cpu.r0 = 1
            cpu.mem8[cpu.r6, cpu.offset(cpu.er4, 8)] = cpu.r0
            cpu.mem8[cpu.r6, cpu.offset(cpu.er4, 9)] = cpu.r0
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_coord():
        # R0=column, R1=0 for X / 1 for Y; output V.
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.er12)
        cpu.mem8[cpu.offset(cpu.er14, 151)] = cpu.r1
        cpu.r4 = cpu.r1
        cpu.call('fn_graph_integer')
        cpu.er4 = XS
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 151)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_427')
        cpu.er4 = YS
        cpu.label('skip_427')
        cpu.er6 = N
        cpu.er12 = T
        cpu.r3 = 0xA9
        cpu.call('fn_graph_op')
        cpu.er6 = WIDTH
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 151)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_436')
        cpu.er6 = HEIGHT
        cpu.label('skip_436')
        cpu.er4 = T
        cpu.er12 = T
        cpu.r3 = 0xB9
        cpu.call('fn_graph_op')
        cpu.er4 = T
        cpu.er6 = XMIN
        cpu.r3 = 0x89
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 151)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_447')
        cpu.er4 = YMAX
        cpu.er6 = T
        cpu.r3 = 0x99
        cpu.label('skip_447')
        cpu.er12 = V
        cpu.call('fn_graph_op')
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_map():
        # V world value, R0 axis. Return clipped pixel in R0 (FF / 96 / 31).
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.er12)
        cpu.mem8[cpu.offset(cpu.er14, 151)] = cpu.r0
        cpu.er4 = V
        cpu.er6 = XMIN
        cpu.er12 = T
        cpu.r3 = 0x99
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_469')
        cpu.er4 = YMAX
        cpu.er6 = V
        cpu.label('skip_469')
        cpu.call('fn_graph_op')
        cpu.er4 = T
        cpu.er6 = ZERO
        cpu.call('fn_graph_cmp')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.branch('negative')
        cpu.er6 = XS
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 151)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_482')
        cpu.er6 = YS
        cpu.label('skip_482')
        cpu.er4 = T
        cpu.call('fn_graph_cmp')
        cpu.compare(cpu.r0, 4)
        if cpu.eq:
            cpu.branch('outside')
        cpu.er4 = T
        cpu.er12 = T
        cpu.r3 = 0xB9
        cpu.call('fn_graph_op')
        cpu.er4 = T
        cpu.er6 = WIDTH
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 151)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_497')
        cpu.er6 = HEIGHT
        cpu.label('skip_497')
        cpu.er12 = T
        cpu.r3 = 0xA9
        cpu.call('fn_graph_op')
        cpu.call('fn_graph_slots')
        cpu.er4 = cpu.er8
        cpu.r4 += 36
        cpu.add_carry(cpu.r5, 1)
        cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 9)]
        cpu.compare(cpu.r0, 1)
        if cpu.ne:
            cpu.branch('zero')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 8)]
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('skip_512')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.branch('done')
        cpu.label('skip_512')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.r1 = 10
        cpu.multiply(cpu.er0, cpu.r1)
        cpu.r1 = cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 1)]
        cpu.r1 >>= 4
        cpu.r0 += cpu.r1
        cpu.branch('done')
        cpu.label('zero')
        cpu.r0 = 0
        cpu.branch('done')
        cpu.label('negative')
        cpu.r0 = 255
        cpu.branch('done')
        cpu.label('outside')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 151)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.r0 = 96
        else:
            cpu.r0 = 31
        cpu.label('done')
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_pixel():
        # R0/R1 body coordinates, R2=1 set / 2 xor. Status row is untouched.
        cpu.push(cpu.xr4)
        cpu.compare(cpu.r0, 96)
        if cpu.ge:
            cpu.branch('done')
        cpu.compare(cpu.r1, 31)
        if cpu.ge:
            cpu.branch('done')
        cpu.r1 += 1
        cpu.r6 = cpu.r2
        cpu.r2 = cpu.r0
        cpu.r2 &= 7
        cpu.r3 = 0x80
        cpu.r3 >>= cpu.r2
        cpu.r4 = cpu.r1
        cpu.r1 = 0
        cpu.r0 >>= 3
        cpu.r2 = 12
        cpu.multiply(cpu.er4, cpu.r2)
        cpu.er4 += cpu.er0
        cpu.er0 = 0x80E0
        cpu.er4 += cpu.er0
        cpu.r0 = cpu.mem8[cpu.er4]
        cpu.compare(cpu.r6, 2)
        if cpu.eq:
            cpu.r0 ^= cpu.r3
        else:
            cpu.r0 |= cpu.r3
        cpu.mem8[cpu.er4] = cpu.r0
        cpu.label('done')
        cpu.pop(cpu.xr4)
        cpu.ret()

    @fw.function(native=True)
    def graph_clear():
        cpu.er0 = 0x80EC
        cpu.er2 = 372
        cpu.r4 = 0
        cpu.label('clear')
        cpu.mem8[cpu.er0] = cpu.r4
        cpu.er0 += 1
        cpu.er2 += -1
        if cpu.ne:
            cpu.branch('clear')
        cpu.ret()

    @fw.function(native=True)
    def graph_prepare():
        cpu.push(cpu.lr)
        cpu.er0 = cpu.er14
        cpu.r0 += 120
        cpu.add_carry(cpu.r1, 0)
        cpu.call('fn_graph_formula_get')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.call('fn_graph_formula_edit')
            cpu.compare(cpu.r0, 2)
            if cpu.ne:
                cpu.branch('edited')
            cpu.call('fn_graph_error')
            cpu.label('edited')
            cpu.er0 = cpu.er14
            cpu.r0 += 120
            cpu.add_carry(cpu.r1, 0)
            cpu.call('fn_graph_formula_get')
            cpu.compare(cpu.r0, 0)
            if cpu.ne:
                cpu.branch('end')
        cpu.er0 = cpu.er14
        cpu.call('fn_mcs_open')
        cpu.compare(cpu.r0, 4)
        if cpu.eq:
            cpu.branch('new')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.branch('used')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('end')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 124)]
        cpu.compare(cpu.r0, 0xFD)
        cpu.compare_carry(cpu.r1, 0x77)
        if cpu.gt:
            cpu.branch('full')
        cpu.er0 += cpu.er0
        cpu.r0 += 4
        cpu.add_carry(cpu.r1, 16)
        cpu.mem16[cpu.offset(cpu.er14, 8)] = cpu.er0
        cpu.er0 = cpu.er14
        cpu.call('fn_mcs_resize')
        cpu.branch('resized')
        cpu.label('new')
        cpu.r0 = 1
        cpu.mem8[cpu.offset(cpu.er14, 7)] = cpu.r0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 124)]
        cpu.compare(cpu.r0, 0xFD)
        cpu.compare_carry(cpu.r1, 0x77)
        if cpu.gt:
            cpu.branch('full')
        cpu.er0 += cpu.er0
        cpu.r0 += 4
        cpu.add_carry(cpu.r1, 16)
        cpu.mem16[cpu.offset(cpu.er14, 8)] = cpu.er0
        cpu.er0 = cpu.er14
        cpu.call('fn_mcs_open')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('end')
        cpu.er4 = cpu.mem16[cpu.offset(cpu.er14, 10)]
        cpu.r2 = cpu.mem8[cpu.offset(cpu.er14, 12)]
        cpu.er0 = 0x4745
        cpu.mem16[cpu.r2, cpu.er4] = cpu.er0
        cpu.er0 = 0x3157
        cpu.mem16[cpu.r2, cpu.offset(cpu.er4, 2)] = cpu.er0
        cpu.r0 = 0
        cpu.label('resized')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('end')
        cpu.r0 = 1
        cpu.mem8[cpu.offset(cpu.er14, OWN_WORK)] = cpu.r0
        cpu.er0 = cpu.er14
        cpu.r0 += 120
        cpu.add_carry(cpu.r1, 0)
        cpu.call('fn_graph_formula_get')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('end')
        cpu.call('fn_graph_work')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('end')
        cpu.call('fn_graph_slots')
        cpu.er4 = cpu.er8
        cpu.r4 += 0
        cpu.add_carry(cpu.r5, 4)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 120)]
        cpu.r2 = cpu.mem8[cpu.offset(cpu.er14, 122)]
        cpu.r6 = cpu.r10
        cpu.call('fn_graph_tokens_linear')
        cpu.mem16[cpu.r10, cpu.er8] = cpu.er0
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.call('fn_mcs_open')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('end')
        cpu.call('fn_graph_window_load')
        cpu.r0 = 0
        cpu.branch('end')
        cpu.label('used')
        cpu.call('fn_graph_name_used')
        cpu.r0 = 2
        cpu.branch('end')
        cpu.label('full')
        cpu.r0 = 1
        cpu.label('end')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_window_load():
        cpu.push(cpu.lr)
        cpu.er0 = 24
        cpu.er4 = 148
        cpu.call('fn_graph_move')
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.er14
        cpu.er0 += HEADER + 6
        cpu.r2 = 0
        cpu.er4 = cpu.er8
        cpu.r4 += 192
        cpu.add_carry(cpu.r5, 0)
        cpu.r6 = cpu.r10
        cpu.r3 = 80
        cpu.call('fn_graph_copy')
        cpu.call('constants')
        cpu.data(CONSTANTS)
        cpu.label('constants')
        cpu.push(cpu.lr)
        cpu.pop(cpu.xr0)
        cpu.er4 = cpu.er8
        cpu.r4 += 0
        cpu.add_carry(cpu.r5, 2)
        cpu.r6 = cpu.r10
        cpu.r3 = 120
        cpu.call('fn_graph_copy')
        cpu.er4 = XMAX
        cpu.er6 = XMIN
        cpu.er12 = XS
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.er4 = YMAX
        cpu.er6 = YMIN
        cpu.er12 = YS
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.er4 = YS
        cpu.er6 = HEIGHT
        cpu.er12 = TOL
        cpu.r3 = 0xB9
        cpu.call('fn_graph_op')
        cpu.er4 = TOL
        cpu.er6 = FOUR
        cpu.er12 = TOL
        cpu.r3 = 0xB9
        cpu.call('fn_graph_op')
        cpu.r0 = 3
        cpu.call('fn_graph_integer')
        cpu.er4 = TOL
        cpu.er6 = N
        cpu.er12 = TOL
        cpu.r3 = 0xA9
        cpu.call('fn_graph_op')
        cpu.er0 = 148
        cpu.er4 = 24
        cpu.call('fn_graph_move')
        cpu.r0 = 0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_plot():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_cancel_hint')
        cpu.call('fn_graph_clear')
        cpu.er0 = 0
        cpu.mem16[cpu.offset(cpu.er14, COL)] = cpu.er0
        cpu.mem8[cpu.offset(cpu.er14, MODE)] = cpu.r0
        cpu.label('column')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, COL)]
        cpu.r1 = 0
        cpu.call('fn_graph_coord')
        cpu.er0 = V
        cpu.er4 = 4
        cpu.call('fn_graph_move')
        cpu.er0 = V
        cpu.er4 = DX
        cpu.call('fn_graph_move')
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.call('fn_graph_eval')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.branch('done')
        cpu.mem8[cpu.offset(cpu.er14, 150)] = cpu.r0
        cpu.er0 = 24
        cpu.er4 = DY
        cpu.call('fn_graph_move')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 150)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.er0 = DY
            cpu.er4 = V
            cpu.call('fn_graph_move')
            cpu.r0 = 1
            cpu.call('fn_graph_map')
            cpu.r1 = cpu.r0
            cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, COL)]
            cpu.r2 = 1
            cpu.call('fn_graph_pixel')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, MODE)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('next')
        cpu.r0 = 0
        cpu.mem8[cpu.offset(cpu.er14, DEPTH)] = cpu.r0
        cpu.call('fn_graph_refine')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.branch('done')
        cpu.label('next')
        cpu.er0 = DX
        cpu.er4 = P
        cpu.call('fn_graph_move')
        cpu.er0 = DY
        cpu.er4 = Q
        cpu.call('fn_graph_move')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 150)]
        cpu.mem8[cpu.offset(cpu.er14, PREV)] = cpu.r0
        cpu.r0 = 1
        cpu.mem8[cpu.offset(cpu.er14, MODE)] = cpu.r0
        cpu.call(0x043BE)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, COL)]
        cpu.er0 += 1
        cpu.mem16[cpu.offset(cpu.er14, COL)] = cpu.er0
        cpu.compare(cpu.r0, 96)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.lt:
            cpu.branch('column')
        cpu.label('done')
        cpu.call('fn_graph_axes')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_refine():
        # Four endpoint native20s are stacked in the GWORK union, not near RAM.
        cpu.push(cpu.lr)
        cpu.call('fn_graph_slots')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, DEPTH)]
        cpu.r1 = 0
        cpu.r2 = 128
        cpu.multiply(cpu.er0, cpu.r2)
        cpu.er4 = cpu.er8
        cpu.r4 += 0
        cpu.add_carry(cpu.r5, 244)
        cpu.er4 += cpu.er0
        cpu.er0 = cpu.er8
        cpu.r0 += 96
        cpu.add_carry(cpu.r1, 1)
        cpu.r2 = cpu.r10
        cpu.r6 = cpu.r10
        cpu.r3 = 80
        cpu.call('fn_graph_copy')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, PREV)]
        cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 80)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 150)]
        cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 81)] = cpu.r0
        cpu.er4 = P
        cpu.er6 = DX
        cpu.er12 = W
        cpu.r3 = 0x89
        cpu.call('fn_graph_op')
        cpu.er4 = W
        cpu.er6 = TWO
        cpu.er12 = W
        cpu.r3 = 0xB9
        cpu.call('fn_graph_op')
        cpu.er0 = W
        cpu.er4 = 4
        cpu.call('fn_graph_move')
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.call('fn_graph_eval')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.jump('return')
        cpu.mem8[cpu.offset(cpu.er14, 152)] = cpu.r0
        cpu.er0 = 24
        cpu.er4 = V
        cpu.call('fn_graph_move')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, PREV)]
        cpu.compare(cpu.r0, 1)
        if cpu.eq:
            cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 150)]
            cpu.compare(cpu.r0, 1)
            if cpu.eq:
                cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 152)]
                cpu.compare(cpu.r0, 1)
                if cpu.ne:
                    cpu.branch('skip_899')
                cpu.r0 = 0
                cpu.jump('return')
                cpu.label('skip_899')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, PREV)]
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, 150)]
        cpu.r0 |= cpu.r1
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, 152)]
        cpu.r0 |= cpu.r1
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('split')
        cpu.er4 = Q
        cpu.er6 = DY
        cpu.er12 = T
        cpu.r3 = 0x89
        cpu.call('fn_graph_op')
        cpu.er4 = T
        cpu.er6 = TWO
        cpu.er12 = T
        cpu.r3 = 0xB9
        cpu.call('fn_graph_op')
        cpu.er4 = T
        cpu.er6 = V
        cpu.er12 = T
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.call('fn_graph_slots')
        cpu.er4 = cpu.er8
        cpu.r4 += 45
        cpu.add_carry(cpu.r5, 1)
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.compare(cpu.r0, 5)
        if cpu.lt:
            cpu.branch('skip_931')
        cpu.r0 += 251
        cpu.mem8[cpu.r10, cpu.er4] = cpu.r0
        cpu.label('skip_931')
        cpu.er4 = T
        cpu.er6 = TOL
        cpu.call('fn_graph_cmp')
        cpu.compare(cpu.r0, 4)
        if cpu.eq:
            cpu.branch('skip_938')
        cpu.call('fn_graph_line')
        cpu.r0 = 0
        cpu.jump('return')
        cpu.label('skip_938')
        cpu.label('split')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, DEPTH)]
        cpu.compare(cpu.r0, 8)
        if cpu.lt:
            cpu.branch('skip_945')
        cpu.r0 = 0
        cpu.branch('return')
        cpu.label('skip_945')
        # Save midpoint beside this level's endpoints.
        cpu.call('fn_graph_node')
        cpu.r4 += 82
        cpu.add_carry(cpu.r5, 0)
        cpu.er0 = cpu.er8
        cpu.r0 += 76
        cpu.add_carry(cpu.r1, 1)
        cpu.r2 = cpu.r10
        cpu.r6 = cpu.r10
        cpu.r3 = 20
        cpu.call('fn_graph_copy')
        cpu.er0 = cpu.er8
        cpu.r0 += 16
        cpu.add_carry(cpu.r1, 1)
        cpu.er4 += 20
        cpu.r3 = 20
        cpu.call('fn_graph_copy')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 152)]
        cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 20)] = cpu.r0
        cpu.er0 = W
        cpu.er4 = DX
        cpu.call('fn_graph_move')
        cpu.er0 = V
        cpu.er4 = DY
        cpu.call('fn_graph_move')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 152)]
        cpu.mem8[cpu.offset(cpu.er14, 150)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, DEPTH)]
        cpu.r0 += 1
        cpu.mem8[cpu.offset(cpu.er14, DEPTH)] = cpu.r0
        cpu.call('fn_graph_refine')
        cpu.push(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, DEPTH)]
        cpu.r0 += 255
        cpu.mem8[cpu.offset(cpu.er14, DEPTH)] = cpu.r0
        cpu.call('fn_graph_node')
        cpu.er0 = cpu.er4
        cpu.er4 = cpu.er8
        cpu.r4 += 96
        cpu.add_carry(cpu.r5, 1)
        cpu.r2 = cpu.r10
        cpu.r6 = cpu.r10
        cpu.r3 = 80
        cpu.call('fn_graph_copy')
        cpu.pop(cpu.er0)
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.branch('return')
        cpu.call('fn_graph_node')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 81)]
        cpu.mem8[cpu.offset(cpu.er14, 150)] = cpu.r0
        cpu.er0 = cpu.er4
        cpu.r0 += 82
        cpu.add_carry(cpu.r1, 0)
        cpu.er4 = cpu.er8
        cpu.r4 += 96
        cpu.add_carry(cpu.r5, 1)
        cpu.r2 = cpu.r10
        cpu.r6 = cpu.r10
        cpu.r3 = 20
        cpu.call('fn_graph_copy')
        cpu.er0 += 0
        cpu.er4 += 20
        cpu.r3 = 20
        cpu.call('fn_graph_copy')
        cpu.call('fn_graph_node')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 122)]
        cpu.mem8[cpu.offset(cpu.er14, PREV)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, DEPTH)]
        cpu.r0 += 1
        cpu.mem8[cpu.offset(cpu.er14, DEPTH)] = cpu.r0
        cpu.call('fn_graph_refine')
        cpu.push(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, DEPTH)]
        cpu.r0 += 255
        cpu.mem8[cpu.offset(cpu.er14, DEPTH)] = cpu.r0
        cpu.call('fn_graph_node')
        cpu.er0 = cpu.er4
        cpu.er4 = cpu.er8
        cpu.r4 += 96
        cpu.add_carry(cpu.r5, 1)
        cpu.r2 = cpu.r10
        cpu.r6 = cpu.r10
        cpu.r3 = 80
        cpu.call('fn_graph_copy')
        cpu.pop(cpu.er0)
        cpu.label('return')
        cpu.push(cpu.er0)
        cpu.call('fn_graph_node_restore')
        cpu.pop(cpu.er0)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_node():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_slots')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, DEPTH)]
        cpu.r1 = 0
        cpu.r2 = 128
        cpu.multiply(cpu.er0, cpu.r2)
        cpu.er4 = cpu.er8
        cpu.r4 += 0
        cpu.add_carry(cpu.r5, 244)
        cpu.er4 += cpu.er0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_node_restore():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_node')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 80)]
        cpu.mem8[cpu.offset(cpu.er14, PREV)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 81)]
        cpu.mem8[cpu.offset(cpu.er14, 150)] = cpu.r0
        cpu.er0 = cpu.er4
        cpu.er4 = cpu.er8
        cpu.r4 += P & 255
        cpu.add_carry(cpu.r5, P >> 8)
        cpu.r2 = cpu.r10
        cpu.r6 = cpu.r10
        cpu.r3 = 80
        cpu.call('fn_graph_copy')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_outcode():
        # Relative x/y slots ER4/ER6; R0 is Cohen-Sutherland outcode.
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.er12)
        cpu.er12 = cpu.er6
        cpu.r0 = 0
        cpu.mem8[cpu.offset(cpu.er14, 153)] = cpu.r0
        cpu.er6 = XMIN
        cpu.call('fn_graph_cmp')
        cpu.compare(cpu.r0, 2)
        if cpu.ne:
            cpu.branch('skip_1084')
        cpu.r0 = 1
        cpu.mem8[cpu.offset(cpu.er14, 153)] = cpu.r0
        cpu.label('skip_1084')
        cpu.er6 = XMAX
        cpu.call('fn_graph_cmp')
        cpu.compare(cpu.r0, 4)
        if cpu.ne:
            cpu.branch('skip_1090')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 153)]
        cpu.r0 |= 2
        cpu.mem8[cpu.offset(cpu.er14, 153)] = cpu.r0
        cpu.label('skip_1090')
        cpu.er4 = cpu.er12
        cpu.er6 = YMIN
        cpu.call('fn_graph_cmp')
        cpu.compare(cpu.r0, 2)
        if cpu.ne:
            cpu.branch('skip_1098')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 153)]
        cpu.r0 |= 4
        cpu.mem8[cpu.offset(cpu.er14, 153)] = cpu.r0
        cpu.label('skip_1098')
        cpu.er6 = YMAX
        cpu.call('fn_graph_cmp')
        cpu.compare(cpu.r0, 4)
        if cpu.ne:
            cpu.branch('skip_1105')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 153)]
        cpu.r0 |= 8
        cpu.mem8[cpu.offset(cpu.er14, 153)] = cpu.r0
        cpu.label('skip_1105')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 153)]
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_line():
        # P/Q -> DX/DY, in world coordinates. Clip before integer rasterization.
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.er12)
        cpu.r0 = 0
        cpu.mem8[cpu.offset(cpu.er14, 154)] = cpu.r0
        cpu.label('clip')
        cpu.er4 = P
        cpu.er6 = Q
        cpu.call('fn_graph_outcode')
        cpu.mem8[cpu.offset(cpu.er14, 155)] = cpu.r0
        cpu.er4 = DX
        cpu.er6 = DY
        cpu.call('fn_graph_outcode')
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, 155)]
        cpu.r2 = cpu.r0
        cpu.r2 &= cpu.r1
        if cpu.ne:
            cpu.jump('done')
        cpu.r0 |= cpu.r1
        if cpu.eq:
            cpu.jump('raster')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 154)]
        cpu.r0 += 1
        cpu.mem8[cpu.offset(cpu.er14, 154)] = cpu.r0
        cpu.compare(cpu.r0, 9)
        if cpu.ge:
            cpu.jump('done')
        cpu.compare(cpu.r1, 0)
        if cpu.eq:
            cpu.er0 = P
            cpu.er4 = T
            cpu.call('fn_graph_move')
            cpu.er0 = DX
            cpu.er4 = P
            cpu.call('fn_graph_move')
            cpu.er0 = T
            cpu.er4 = DX
            cpu.call('fn_graph_move')
            cpu.er0 = Q
            cpu.er4 = T
            cpu.call('fn_graph_move')
            cpu.er0 = DY
            cpu.er4 = Q
            cpu.call('fn_graph_move')
            cpu.er0 = T
            cpu.er4 = DY
            cpu.call('fn_graph_move')
            cpu.er4 = P
            cpu.er6 = Q
            cpu.call('fn_graph_outcode')
            cpu.mem8[cpu.offset(cpu.er14, 155)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 155)]
        cpu.r0 &= 3
        if cpu.eq:
            cpu.branch('horizontal')
        cpu.er0 = XMIN
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 155)]
        cpu.r0 &= 2
        if cpu.ne:
            cpu.er0 = XMAX
        else:
            cpu.er0 = XMIN
        cpu.er4 = W
        cpu.call('fn_graph_move')
        cpu.er4 = W
        cpu.er6 = P
        cpu.er12 = T
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.er4 = DX
        cpu.er6 = P
        cpu.er12 = U
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.er4 = T
        cpu.er6 = U
        cpu.er12 = T
        cpu.r3 = 0xB9
        cpu.call('fn_graph_op')
        cpu.er4 = DY
        cpu.er6 = Q
        cpu.er12 = U
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.er4 = T
        cpu.er6 = U
        cpu.er12 = T
        cpu.r3 = 0xA9
        cpu.call('fn_graph_op')
        cpu.er4 = Q
        cpu.er6 = T
        cpu.er12 = Q
        cpu.r3 = 0x89
        cpu.call('fn_graph_op')
        cpu.er0 = W
        cpu.er4 = P
        cpu.call('fn_graph_move')
        cpu.jump('clip')
        cpu.label('horizontal')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 155)]
        cpu.r0 &= 8
        if cpu.eq:
            cpu.er0 = YMIN
        else:
            cpu.er0 = YMAX
        cpu.er4 = W
        cpu.call('fn_graph_move')
        cpu.er4 = W
        cpu.er6 = Q
        cpu.er12 = T
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.er4 = DY
        cpu.er6 = Q
        cpu.er12 = U
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.er4 = T
        cpu.er6 = U
        cpu.er12 = T
        cpu.r3 = 0xB9
        cpu.call('fn_graph_op')
        cpu.er4 = DX
        cpu.er6 = P
        cpu.er12 = U
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.er4 = T
        cpu.er6 = U
        cpu.er12 = T
        cpu.r3 = 0xA9
        cpu.call('fn_graph_op')
        cpu.er4 = P
        cpu.er6 = T
        cpu.er12 = P
        cpu.r3 = 0x89
        cpu.call('fn_graph_op')
        cpu.er0 = W
        cpu.er4 = Q
        cpu.call('fn_graph_move')
        cpu.jump('clip')
        cpu.label('raster')
        cpu.er0 = P
        cpu.er4 = V
        cpu.call('fn_graph_move')
        cpu.r0 = 0
        cpu.call('fn_graph_map')
        cpu.mem8[cpu.offset(cpu.er14, 156)] = cpu.r0
        cpu.er0 = Q
        cpu.er4 = V
        cpu.call('fn_graph_move')
        cpu.r0 = 1
        cpu.call('fn_graph_map')
        cpu.mem8[cpu.offset(cpu.er14, 157)] = cpu.r0
        cpu.er0 = DX
        cpu.er4 = V
        cpu.call('fn_graph_move')
        cpu.r0 = 0
        cpu.call('fn_graph_map')
        cpu.mem8[cpu.offset(cpu.er14, 158)] = cpu.r0
        cpu.er0 = DY
        cpu.er4 = V
        cpu.call('fn_graph_move')
        cpu.r0 = 1
        cpu.call('fn_graph_map')
        cpu.r7 = cpu.r0
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, 158)]
        cpu.er4 = cpu.mem16[cpu.offset(cpu.er14, 156)]
        cpu.call('fn_graph_raster')
        cpu.label('done')
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_raster():
        # R4/R5 start, R6/R7 end. Integer Bresenham, clipped by graph_pixel.
        cpu.push(cpu.lr)
        cpu.push(cpu.qr8)
        cpu.r8 = cpu.r6
        cpu.r8 -= cpu.r4
        cpu.r10 = 1
        cpu.compare(cpu.r6, cpu.r4)
        if cpu.ge:
            cpu.branch('skip_1300')
        cpu.r8 = -cpu.r8
        cpu.r10 = 255
        cpu.label('skip_1300')
        cpu.r9 = cpu.r7
        cpu.r9 -= cpu.r5
        cpu.r11 = 1
        cpu.compare(cpu.r7, cpu.r5)
        if cpu.ge:
            cpu.branch('skip_1307')
        cpu.r9 = -cpu.r9
        cpu.r11 = 255
        cpu.label('skip_1307')
        cpu.r9 = -cpu.r9
        cpu.r12 = cpu.r8
        cpu.r12 += cpu.r9
        cpu.label('pixel')
        cpu.r0 = cpu.r4
        cpu.r1 = cpu.r5
        cpu.r2 = 1
        cpu.call('fn_graph_pixel')
        cpu.compare(cpu.r4, cpu.r6)
        if cpu.eq:
            cpu.compare(cpu.r5, cpu.r7)
            if cpu.eq:
                cpu.branch('done')
        cpu.er0 = 0
        cpu.r0 = cpu.r12
        cpu.extend(cpu.er0)
        cpu.er0 += cpu.er0
        cpu.er2 = 0
        cpu.r2 = cpu.r9
        cpu.extend(cpu.er2)
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lts:
            cpu.branch('skip_1331')
        cpu.r12 += cpu.r9
        cpu.r4 += cpu.r10
        cpu.label('skip_1331')
        cpu.er2 = 0
        cpu.r2 = cpu.r8
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.gts:
            cpu.branch('skip_1337')
        cpu.r12 += cpu.r8
        cpu.r5 += cpu.r11
        cpu.label('skip_1337')
        cpu.branch('pixel')
        cpu.label('done')
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_axes():
        cpu.push(cpu.lr)
        cpu.er0 = ZERO
        cpu.er4 = V
        cpu.call('fn_graph_move')
        cpu.r0 = 0
        cpu.call('fn_graph_map')
        cpu.r4 = cpu.r0
        cpu.r5 = 0
        cpu.label('vertical')
        cpu.r0 = cpu.r4
        cpu.r1 = cpu.r5
        cpu.r2 = 1
        cpu.call('fn_graph_pixel')
        cpu.r5 += 1
        cpu.compare(cpu.r5, 31)
        if cpu.lt:
            cpu.branch('vertical')
        cpu.er0 = ZERO
        cpu.er4 = V
        cpu.call('fn_graph_move')
        cpu.r0 = 1
        cpu.call('fn_graph_map')
        cpu.r5 = cpu.r0
        cpu.r4 = 0
        cpu.label('horizontal')
        cpu.r0 = cpu.r4
        cpu.r1 = cpu.r5
        cpu.r2 = 1
        cpu.call('fn_graph_pixel')
        cpu.r4 += 1
        cpu.compare(cpu.r4, 96)
        if cpu.lt:
            cpu.branch('horizontal')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_text():
        # Inline NUL text, row in R1; skip the data on return.
        cpu.mem8[cpu.offset(cpu.er14, 152)] = cpu.r1
        cpu.push(cpu.lr)
        cpu.pop(cpu.xr0)
        cpu.er4 = cpu.er0
        cpu.er6 = cpu.er2
        cpu.er2 = cpu.er14
        cpu.r2 += 0
        cpu.add_carry(cpu.r3, 1)
        cpu.label('copy')
        cpu.r0 = cpu.mem8[cpu.r6, cpu.er4]
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er4 += 1
        cpu.er2 += 1
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('copy')
        cpu.r0 = cpu.r4
        cpu.r0 &= 1
        if cpu.eq:
            cpu.branch('skip_1403')
        cpu.er4 += 1
        cpu.label('skip_1403')
        cpu.push(cpu.xr4)
        cpu.er2 = cpu.er14
        cpu.r2 += 0
        cpu.add_carry(cpu.r3, 1)
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, 152)]
        cpu.r0 = 0
        cpu.call(0x041DA)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_menu():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_clear')
        cpu.r1 = 1
        cpu.call('fn_graph_text')
        cpu.data(b'1:TRACE\0')
        cpu.r1 = 9
        cpu.call('fn_graph_text')
        cpu.data(b'2:CALC\0\0')
        cpu.r1 = 17
        cpu.call('fn_graph_text')
        cpu.data(b'3:VIEW\0\0')
        cpu.r1 = 25
        cpu.call('fn_graph_text')
        cpu.data(b'4:SKETCH\0\0')
        cpu.call(0x043BE)
        cpu.label('key')
        cpu.call(0x80800)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.branch('done')
        cpu.compare(cpu.r0, 0x31)
        if cpu.lt:
            cpu.branch('key')
        cpu.compare(cpu.r0, 0x34)
        if cpu.gt:
            cpu.branch('key')
        cpu.label('done')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_error():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_clear')
        cpu.r1 = 9
        cpu.call('fn_graph_text')
        cpu.data(b'MEMORY FULL\0')
        cpu.call('fn_graph_wait')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_name_used():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_clear')
        cpu.r1 = 9
        cpu.call('fn_graph_text')
        cpu.data(b'NAME USED\0')
        cpu.call('fn_graph_wait')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_bad_data():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_clear')
        cpu.r1 = 1
        cpu.call('fn_graph_text')
        cpu.data(b'BAD GRAPH DATA\0\0')
        cpu.r1 = 17
        cpu.call('fn_graph_text')
        cpu.data(b'RESET GRAPH?\0\0')
        cpu.r1 = 25
        cpu.call('fn_graph_text')
        cpu.data(b'EXE:YES EXIT:NO\0')
        cpu.call('fn_graph_wait')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_wait():
        cpu.push(cpu.lr)
        cpu.call(0x043BE)
        cpu.label('key')
        cpu.call(0x80800)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.branch('done')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.ne:
            cpu.branch('key')
        cpu.label('done')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_map_cursor():
        """V world value, R0 axis; return the nearest visible cursor pixel."""
        cpu.push(cpu.lr)
        cpu.push(cpu.er0)
        cpu.call('fn_graph_map')
        cpu.pop(cpu.er2)
        cpu.compare(cpu.r0, 255)
        if cpu.ne:
            cpu.branch('visible')
        cpu.r0 = 0
        cpu.label('visible')
        cpu.r1 = 95
        cpu.compare(cpu.r2, 0)
        if cpu.eq:
            cpu.branch('limit')
        cpu.r1 = 30
        cpu.label('limit')
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.lt:
            cpu.branch('done')
        cpu.r0 = cpu.r1
        cpu.label('done')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_cursor():
        cpu.push(cpu.lr)
        cpu.r4 = 0
        cpu.label('horizontal')
        cpu.r0 = cpu.r4
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, CY)]
        cpu.r2 = 2
        cpu.call('fn_graph_pixel')
        cpu.r4 += 1
        cpu.compare(cpu.r4, 96)
        if cpu.lt:
            cpu.branch('horizontal')
        cpu.r4 = 0
        cpu.label('vertical')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, CX)]
        cpu.r1 = cpu.r4
        cpu.r2 = 2
        cpu.call('fn_graph_pixel')
        cpu.r4 += 1
        cpu.compare(cpu.r4, 31)
        if cpu.lt:
            cpu.branch('vertical')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_cursor_key():
        cpu.compare(cpu.r0, 0xFC)
        if cpu.eq:
            cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, CX)]
            cpu.compare(cpu.r1, 0)
            if cpu.eq:
                cpu.branch('skip_1527')
            cpu.r1 += 255
            cpu.mem8[cpu.offset(cpu.er14, CX)] = cpu.r1
            cpu.label('skip_1527')
        cpu.compare(cpu.r0, 0xFD)
        if cpu.eq:
            cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, CX)]
            cpu.compare(cpu.r1, 95)
            if cpu.ge:
                cpu.branch('skip_1534')
            cpu.r1 += 1
            cpu.mem8[cpu.offset(cpu.er14, CX)] = cpu.r1
            cpu.label('skip_1534')
        cpu.compare(cpu.r0, 0xFF)
        if cpu.eq:
            cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, CY)]
            cpu.compare(cpu.r1, 0)
            if cpu.eq:
                cpu.branch('skip_1541')
            cpu.r1 += 255
            cpu.mem8[cpu.offset(cpu.er14, CY)] = cpu.r1
            cpu.label('skip_1541')
        cpu.compare(cpu.r0, 0xFE)
        if cpu.eq:
            cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, CY)]
            cpu.compare(cpu.r1, 30)
            if cpu.ge:
                cpu.branch('skip_1548')
            cpu.r1 += 1
            cpu.mem8[cpu.offset(cpu.er14, CY)] = cpu.r1
            cpu.label('skip_1548')
        cpu.ret()

    @fw.function(native=True)
    def graph_trace():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_plot')
        cpu.call('fn_graph_record_replay')
        cpu.label('at')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, CX)]
        cpu.r1 = 0
        cpu.call('fn_graph_coord')
        cpu.er0 = V
        cpu.er4 = 4
        cpu.call('fn_graph_move')
        cpu.label('evaluate')
        cpu.er0 = 4
        cpu.er4 = V
        cpu.call('fn_graph_move')
        cpu.r0 = 0
        cpu.call('fn_graph_map_cursor')
        cpu.mem8[cpu.offset(cpu.er14, CX)] = cpu.r0
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.call('fn_graph_eval')
        cpu.mem8[cpu.offset(cpu.er14, 153)] = cpu.r0
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('skip_1584')
        cpu.er0 = 24
        cpu.er4 = V
        cpu.call('fn_graph_move')
        cpu.r0 = 1
        cpu.call('fn_graph_map_cursor')
        cpu.mem8[cpu.offset(cpu.er14, CY)] = cpu.r0
        cpu.label('skip_1584')
        cpu.call('fn_graph_values')
        cpu.call('fn_graph_cursor')
        cpu.call(0x043BE)
        cpu.call(0x80800)
        cpu.push(cpu.er0)
        cpu.call('fn_graph_cursor')
        cpu.pop(cpu.er0)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.branch('done')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.eq:
            cpu.er0 = 4
            cpu.call('fn_graph_input_slot')
            cpu.compare(cpu.r0, 0)
            if cpu.ne:
                cpu.branch('evaluate')
            cpu.branch('at')
        cpu.call('fn_graph_cursor_key')
        cpu.branch('at')
        cpu.label('done')
        cpu.call('fn_graph_trace_save')
        cpu.r0 = 0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_values():
        cpu.push(cpu.lr)
        cpu.er0 = 0x81AC
        cpu.er2 = 180
        cpu.r4 = 0
        cpu.label('strip')
        cpu.mem8[cpu.er0] = cpu.r4
        cpu.er0 += 1
        cpu.er2 += -1
        if cpu.ne:
            cpu.branch('strip')
        cpu.er0 = 24
        cpu.er4 = P
        cpu.call('fn_graph_move')
        cpu.er0 = 4
        cpu.er4 = 24
        cpu.call('fn_graph_move')
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.call('fn_graph_format')
        cpu.r1 = 17
        cpu.call('fn_graph_number_text')
        cpu.er0 = P
        cpu.er4 = 24
        cpu.call('fn_graph_move')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 153)]
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.call('fn_graph_status_text')
            cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 153)]
            cpu.compare(cpu.r0, 6)
            if cpu.lt:
                cpu.branch('skip_1649')
            cpu.call('fn_graph_slots')
            cpu.er0 = cpu.er8
            cpu.r2 = cpu.r10
            cpu.call('fn_graph_format')
            cpu.r1 = 9
            cpu.call('fn_graph_number_text')
            cpu.label('skip_1649')
        else:
            cpu.er0 = cpu.er8
            cpu.r2 = cpu.r10
            cpu.call('fn_graph_format')
            cpu.r1 = 25
            cpu.call('fn_graph_number_text')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_number_text():
        cpu.push(cpu.lr)
        cpu.push(cpu.er0)
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.er8
        cpu.r0 += 96
        cpu.add_carry(cpu.r1, 0)
        cpu.r2 = cpu.r10
        cpu.er4 = cpu.er14
        cpu.r4 += 0
        cpu.add_carry(cpu.r5, 1)
        cpu.r6 = 0
        cpu.r3 = 32
        cpu.call('fn_graph_copy')
        cpu.pop(cpu.er0)
        cpu.er2 = cpu.er14
        cpu.r2 += 0
        cpu.add_carry(cpu.r3, 1)
        cpu.r0 = 0
        cpu.r1 += 1
        cpu.call('fn_small_text')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_status_text():
        cpu.push(cpu.lr)
        cpu.r1 = 25
        cpu.compare(cpu.r0, 1)
        if cpu.ne:
            cpu.branch('skip_1693')
        cpu.call('fn_graph_text')
        cpu.data(b'UNDEFINED\0')
        cpu.branch('done')
        cpu.label('skip_1693')
        cpu.compare(cpu.r0, 2)
        if cpu.ne:
            cpu.branch('skip_1698')
        cpu.call('fn_graph_text')
        cpu.data(b'CANCELLED\0')
        cpu.branch('done')
        cpu.label('skip_1698')
        cpu.compare(cpu.r0, 4)
        if cpu.ne:
            cpu.branch('skip_1703')
        cpu.call('fn_graph_text')
        cpu.data(b'NO CONVERGENCE\0\0')
        cpu.branch('done')
        cpu.label('skip_1703')
        cpu.compare(cpu.r0, 5)
        if cpu.ne:
            cpu.branch('skip_1708')
        cpu.call('fn_graph_text')
        cpu.data(b'NO ROOT\0')
        cpu.branch('done')
        cpu.label('skip_1708')
        cpu.compare(cpu.r0, 6)
        if cpu.ne:
            cpu.branch('skip_1713')
        cpu.call('fn_graph_text')
        cpu.data(b'UNCONFIRMED\0')
        cpu.branch('done')
        cpu.label('skip_1713')
        cpu.compare(cpu.r0, 7)
        if cpu.ne:
            cpu.branch('skip_1718')
        cpu.call('fn_graph_text')
        cpu.data(b'UNSTABLE\0\0')
        cpu.branch('done')
        cpu.label('skip_1718')
        cpu.call('fn_graph_text')
        cpu.data(b'NATIVE ERROR\0\0')
        cpu.label('done')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_calculate():
        cpu.push(cpu.lr)
        cpu.r0 = 0
        cpu.mem8[cpu.offset(cpu.er14, PAGE)] = cpu.r0
        cpu.label('menu')
        cpu.call('fn_graph_clear')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, PAGE)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.r1 = 1
            cpu.call('fn_graph_text')
            cpu.data(b'1:ROOT 2:MIN\0\0')
            cpu.r1 = 9
            cpu.call('fn_graph_text')
            cpu.data(b'3:MAX 4:SLOPE\0')
            cpu.r1 = 25
            cpu.call('fn_graph_text')
            cpu.data(b'RIGHT:MORE\0\0')
        else:
            cpu.r1 = 1
            cpu.call('fn_graph_text')
            cpu.data(b'1:INTEGRAL\0\0')
        cpu.call(0x043BE)
        cpu.label('key')
        cpu.call(0x80800)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.jump('done')
        cpu.compare(cpu.r0, 0xFC)
        if cpu.ne:
            cpu.branch('skip_1757')
        cpu.r0 = 0
        cpu.mem8[cpu.offset(cpu.er14, PAGE)] = cpu.r0
        cpu.branch('menu')
        cpu.label('skip_1757')
        cpu.compare(cpu.r0, 0xFD)
        if cpu.ne:
            cpu.branch('skip_1762')
        cpu.r0 = 1
        cpu.mem8[cpu.offset(cpu.er14, PAGE)] = cpu.r0
        cpu.branch('menu')
        cpu.label('skip_1762')
        cpu.compare(cpu.r0, 0x31)
        if cpu.lt:
            cpu.branch('key')
        cpu.compare(cpu.r0, 0x34)
        if cpu.gt:
            cpu.branch('key')
        cpu.r0 += 208
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, PAGE)]
        cpu.compare(cpu.r1, 0)
        if cpu.ne:
            cpu.compare(cpu.r0, 1)
            if cpu.ne:
                cpu.branch('key')
            cpu.r0 = 5
        cpu.mem8[cpu.offset(cpu.er14, KIND)] = cpu.r0
        cpu.call('fn_graph_prepare')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_1783')
        cpu.call('fn_graph_error')
        cpu.branch('done')
        cpu.label('skip_1783')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, TRACE_VALID)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_1788')
        cpu.call('fn_graph_trace_load')
        cpu.branch('position')
        cpu.label('skip_1788')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, CX)]
        cpu.r1 = 0
        cpu.call('fn_graph_coord')
        cpu.er0 = V
        cpu.er4 = 4
        cpu.call('fn_graph_move')
        cpu.label('position')
        cpu.er0 = XMIN
        cpu.er4 = 44
        cpu.call('fn_graph_move')
        cpu.er0 = XMAX
        cpu.er4 = 64
        cpu.call('fn_graph_move')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, KIND)]
        cpu.compare(cpu.r0, 4)
        if cpu.eq:
            cpu.er0 = 4
            cpu.call('fn_graph_input_slot')
            cpu.compare(cpu.r0, 0)
            if cpu.eq:
                cpu.branch('done')
        else:
            cpu.er0 = 44
            cpu.call('fn_graph_input_slot')
            cpu.compare(cpu.r0, 0)
            if cpu.eq:
                cpu.branch('done')
            cpu.er0 = 64
            cpu.call('fn_graph_input_slot')
            cpu.compare(cpu.r0, 0)
            if cpu.eq:
                cpu.branch('done')
        cpu.call('fn_graph_cancel_hint')
        cpu.call('fn_graph_slots')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, KIND)]
        cpu.mem8[cpu.r10, cpu.offset(cpu.er8, 2)] = cpu.r0
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.call('fn_graph_calc')
        cpu.mem8[cpu.offset(cpu.er14, 153)] = cpu.r0
        cpu.call('fn_graph_window_load')
        cpu.call('fn_graph_clear')
        cpu.call('fn_graph_values')
        cpu.call('fn_graph_result_flags')
        cpu.call('fn_graph_wait')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 153)]
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('done')
        cpu.call('fn_graph_trace_save')
        cpu.er0 = 4
        cpu.er4 = V
        cpu.call('fn_graph_move')
        cpu.r0 = 0
        cpu.call('fn_graph_map_cursor')
        cpu.mem8[cpu.offset(cpu.er14, CX)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, KIND)]
        cpu.compare(cpu.r0, 4)
        if cpu.ne:
            cpu.branch('skip_1848')
        cpu.call('fn_graph_tangent')
        cpu.label('skip_1848')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, KIND)]
        cpu.compare(cpu.r0, 5)
        if cpu.ne:
            cpu.branch('skip_1852')
        cpu.call('fn_graph_shade')
        cpu.label('skip_1852')
        cpu.label('done')
        cpu.r0 = 0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_input_slot():
        cpu.push(cpu.lr)
        cpu.mem16[cpu.offset(cpu.er14, 244)] = cpu.er0
        cpu.call('fn_graph_slots')
        cpu.er0 += cpu.er8
        cpu.r2 = cpu.r10
        cpu.er4 = cpu.er14
        cpu.r4 += 64
        cpu.add_carry(cpu.r5, 1)
        cpu.r6 = 0
        cpu.r3 = 20
        cpu.call('fn_graph_copy')
        cpu.er0 = cpu.er14
        cpu.r0 += 64
        cpu.add_carry(cpu.r1, 1)
        cpu.r2 = 0
        cpu.call('fn_graph_number_input')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('done')
        cpu.call('fn_graph_work')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_1881')
        cpu.r0 = 0
        cpu.branch('done')
        cpu.label('skip_1881')
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.call('fn_mcs_open')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_1888')
        cpu.r0 = 0
        cpu.branch('done')
        cpu.label('skip_1888')
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.er14
        cpu.r0 += 64
        cpu.add_carry(cpu.r1, 1)
        cpu.r2 = 0
        cpu.er4 = cpu.er8
        cpu.er6 = cpu.mem16[cpu.offset(cpu.er14, 244)]
        cpu.er4 += cpu.er6
        cpu.r6 = cpu.r10
        cpu.r3 = 20
        cpu.call('fn_graph_copy')
        cpu.r0 = 1
        cpu.label('done')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_view_menu():
        cpu.push(cpu.lr)
        cpu.label('menu')
        cpu.call('fn_graph_clear')
        cpu.r1 = 1
        cpu.call('fn_graph_text')
        cpu.data(b'1:XMIN 2:XMAX\0')
        cpu.r1 = 9
        cpu.call('fn_graph_text')
        cpu.data(b'3:YMIN 4:YMAX\0')
        cpu.r1 = 25
        cpu.call('fn_graph_text')
        cpu.data(b'RIGHT:RESET\0')
        cpu.call(0x043BE)
        cpu.label('key')
        cpu.call(0x80800)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.branch('done')
        cpu.compare(cpu.r0, 0xFD)
        if cpu.eq:
            cpu.call('fn_graph_clear')
            cpu.r1 = 1
            cpu.call('fn_graph_text')
            cpu.data(b'1:RESET\0')
            cpu.call(0x043BE)
            cpu.call(0x80800)
            cpu.compare(cpu.r0, 0x31)
            if cpu.ne:
                cpu.branch('menu')
            cpu.call('reset')
            cpu.data(INITIAL)
            cpu.label('reset')
            cpu.push(cpu.lr)
            cpu.pop(cpu.xr0)
            cpu.r0 += 6
            cpu.add_carry(cpu.r1, 0)
            cpu.er4 = cpu.er14
            cpu.er4 += HEADER + 6
            cpu.r6 = 0
            cpu.r3 = 80
            cpu.call('fn_graph_copy')
            cpu.call('fn_graph_save')
            cpu.branch('done')
        cpu.compare(cpu.r0, 0x31)
        if cpu.lt:
            cpu.branch('key')
        cpu.compare(cpu.r0, 0x34)
        if cpu.gt:
            cpu.branch('key')
        cpu.r0 += 207
        cpu.r1 = 20
        cpu.multiply(cpu.er0, cpu.r1)
        cpu.r0 += 192
        cpu.add_carry(cpu.r1, 0)
        cpu.mem16[cpu.offset(cpu.er14, POS)] = cpu.er0
        cpu.call('fn_graph_input_slot')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.jump('menu')
        cpu.call('fn_graph_window_valid')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('bad')
        cpu.call('fn_graph_window_save')
        cpu.jump('menu')
        cpu.label('bad')
        cpu.call('fn_graph_clear')
        cpu.r1 = 9
        cpu.call('fn_graph_text')
        cpu.data(b'BAD WINDOW\0\0')
        cpu.call('fn_graph_wait')
        cpu.jump('menu')
        cpu.label('done')
        cpu.r0 = 0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_window_save():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.er8
        cpu.r0 += XMIN
        cpu.add_carry(cpu.r1, 0)
        cpu.r2 = cpu.r10
        cpu.er4 = cpu.er14
        cpu.er4 += HEADER + 6
        cpu.r6 = 0
        cpu.r3 = 80
        cpu.call('fn_graph_copy')
        cpu.call('fn_graph_save')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_pan_zoom():
        cpu.push(cpu.lr)
        cpu.mem8[cpu.offset(cpu.er14, 153)] = cpu.r0
        cpu.compare(cpu.r0, 0xFC)
        if cpu.eq:
            cpu.branch('panx')
        cpu.compare(cpu.r0, 0xFD)
        if cpu.eq:
            cpu.branch('panx')
        cpu.compare(cpu.r0, 0xFF)
        if cpu.eq:
            cpu.branch('pany')
        cpu.compare(cpu.r0, 0xFE)
        if cpu.eq:
            cpu.branch('pany')
        cpu.compare(cpu.r0, 0x38)
        if cpu.eq:
            cpu.branch('zoom')
        cpu.compare(cpu.r0, 0x32)
        if cpu.eq:
            cpu.branch('zoom')
        cpu.r0 = 0
        cpu.pop(cpu.pc)
        cpu.label('panx')
        cpu.er4 = XMAX
        cpu.er6 = XMIN
        cpu.er12 = V
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.er4 = V
        cpu.er6 = FOUR
        cpu.er12 = V
        cpu.r3 = 0xB9
        cpu.call('fn_graph_op')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 153)]
        cpu.r3 = 0x89
        cpu.compare(cpu.r0, 0xFC)
        if cpu.ne:
            cpu.branch('skip_2038')
        cpu.r3 = 0x99
        cpu.label('skip_2038')
        cpu.mem8[cpu.offset(cpu.er14, 152)] = cpu.r3
        cpu.er4 = XMIN
        cpu.er6 = V
        cpu.er12 = XMIN
        cpu.call('fn_graph_op')
        cpu.er4 = XMAX
        cpu.er6 = V
        cpu.er12 = XMAX
        cpu.r3 = cpu.mem8[cpu.offset(cpu.er14, 152)]
        cpu.call('fn_graph_op')
        cpu.branch('save')
        cpu.label('pany')
        cpu.er4 = YMAX
        cpu.er6 = YMIN
        cpu.er12 = V
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.er4 = V
        cpu.er6 = FOUR
        cpu.er12 = V
        cpu.r3 = 0xB9
        cpu.call('fn_graph_op')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 153)]
        cpu.r3 = 0x89
        cpu.compare(cpu.r0, 0xFE)
        if cpu.ne:
            cpu.branch('skip_2065')
        cpu.r3 = 0x99
        cpu.label('skip_2065')
        cpu.mem8[cpu.offset(cpu.er14, 152)] = cpu.r3
        cpu.er4 = YMIN
        cpu.er6 = V
        cpu.er12 = YMIN
        cpu.call('fn_graph_op')
        cpu.er4 = YMAX
        cpu.er6 = V
        cpu.er12 = YMAX
        cpu.r3 = cpu.mem8[cpu.offset(cpu.er14, 152)]
        cpu.call('fn_graph_op')
        cpu.branch('save')
        cpu.label('zoom')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, CX)]
        cpu.r1 = 0
        cpu.call('fn_graph_coord')
        cpu.er0 = V
        cpu.er4 = P
        cpu.call('fn_graph_move')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, CY)]
        cpu.r1 = 1
        cpu.call('fn_graph_coord')
        cpu.er0 = V
        cpu.er4 = Q
        cpu.call('fn_graph_move')
        cpu.er4 = XMIN
        cpu.er6 = P
        cpu.er12 = XMIN
        cpu.call('fn_graph_zoom_bound')
        cpu.er4 = XMAX
        cpu.er6 = P
        cpu.er12 = XMAX
        cpu.call('fn_graph_zoom_bound')
        cpu.er4 = YMIN
        cpu.er6 = Q
        cpu.er12 = YMIN
        cpu.call('fn_graph_zoom_bound')
        cpu.er4 = YMAX
        cpu.er6 = Q
        cpu.er12 = YMAX
        cpu.call('fn_graph_zoom_bound')
        cpu.label('save')
        cpu.call('fn_graph_window_valid')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_2110')
        cpu.call('fn_graph_window_load')
        cpu.r0 = 1
        cpu.pop(cpu.pc)
        cpu.label('skip_2110')
        cpu.call('fn_graph_window_save')
        cpu.r0 = 1
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_zoom_bound():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.er12)
        cpu.er12 = T
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.er4 = T
        cpu.er6 = TWO
        cpu.er12 = T
        cpu.r3 = 0xB9
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 153)]
        cpu.compare(cpu.r0, 0x32)
        if cpu.ne:
            cpu.branch('skip_2132')
        cpu.r3 = 0xA9
        cpu.label('skip_2132')
        cpu.call('fn_graph_op')
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr4)
        cpu.er4 = T
        cpu.r3 = 0x89
        cpu.call('fn_graph_op')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_records_check():
        cpu.push(cpu.lr)
        cpu.er0 = 88
        cpu.mem16[cpu.offset(cpu.er14, POS)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, HEADER + 86)]
        cpu.mem16[cpu.offset(cpu.er14, COUNT)] = cpu.er0
        cpu.label('record')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, COUNT)]
        cpu.compare(cpu.r0, 0)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.eq:
            cpu.jump('last')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, HEADER + 4)]
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er14, POS)]
        cpu.r0 -= cpu.r2
        cpu.sub_carry(cpu.r1, cpu.r3)
        cpu.compare(cpu.r0, 3)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.lt:
            cpu.jump('bad')
        cpu.mem16[cpu.offset(cpu.er14, 158)] = cpu.er0
        cpu.call('fn_graph_record_address')
        cpu.er8 = cpu.er0
        cpu.r10 = cpu.r2
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er8]
        cpu.mem8[cpu.offset(cpu.er14, KIND)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er8, 1)]
        cpu.r1 = cpu.mem8[cpu.r10, cpu.offset(cpu.er8, 2)]
        cpu.mem16[cpu.offset(cpu.er14, SIZE)] = cpu.er0
        cpu.compare(cpu.r0, 3)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.lt:
            cpu.branch('bad')
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er14, 158)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.gt:
            cpu.branch('bad')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, KIND)]
        cpu.er12 = 3
        cpu.compare(cpu.r0, 1)
        if cpu.ne:
            cpu.branch('skip_2182')
        cpu.er2 = 43
        cpu.er6 = 2
        cpu.branch('fixed')
        cpu.label('skip_2182')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.branch('pair')
        cpu.compare(cpu.r0, 3)
        if cpu.eq:
            cpu.branch('pair')
        cpu.compare(cpu.r0, 4)
        if cpu.eq:
            cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, SIZE)]
            cpu.compare(cpu.r0, 44)
            cpu.compare_carry(cpu.r1, 0)
            if cpu.lt:
                cpu.branch('bad')
            cpu.er6 = 2
            cpu.branch('numbers')
        cpu.compare(cpu.r0, 5)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, SIZE)]
        cpu.compare(cpu.r0, 45)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.lt:
            cpu.branch('bad')
        cpu.r6 = cpu.mem8[cpu.r10, cpu.offset(cpu.er8, 3)]
        cpu.r7 = cpu.mem8[cpu.r10, cpu.offset(cpu.er8, 4)]
        cpu.compare(cpu.r6, 0)
        cpu.compare_carry(cpu.r7, 0)
        if cpu.eq:
            cpu.branch('bad')
        cpu.compare(cpu.r6, 0x66)
        cpu.compare_carry(cpu.r7, 6)
        if cpu.gt:
            cpu.branch('bad')
        cpu.er2 = 5
        cpu.er0 = cpu.er6
        cpu.label('length')
        cpu.er2 += 40
        cpu.er0 += -1
        if cpu.ne:
            cpu.branch('length')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, SIZE)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er6 += cpu.er6
        cpu.er12 = 5
        cpu.branch('numbers')
        cpu.label('pair')
        cpu.er2 = 83
        cpu.er6 = 4
        cpu.label('fixed')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, SIZE)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.branch('bad')
        cpu.label('numbers')
        cpu.er4 = cpu.er8
        cpu.er4 += cpu.er12
        cpu.label('number')
        cpu.er0 = cpu.er4
        cpu.r2 = cpu.r10
        cpu.call('fn_graph_scalar')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er4 += 20
        cpu.er6 += -1
        if cpu.ne:
            cpu.branch('number')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, KIND)]
        cpu.compare(cpu.r0, 4)
        if cpu.ne:
            cpu.branch('next')
        cpu.er6 = cpu.mem16[cpu.offset(cpu.er14, SIZE)]
        cpu.er6 += -43
        cpu.label('chars')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.compare(cpu.r0, 0x20)
        if cpu.lt:
            cpu.branch('bad')
        cpu.compare(cpu.r0, 0x5F)
        if cpu.gt:
            cpu.branch('bad')
        cpu.er4 += 1
        cpu.er6 += -1
        if cpu.ne:
            cpu.branch('chars')
        cpu.label('next')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, SIZE)]
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er14, POS)]
        cpu.er0 += cpu.er2
        cpu.mem16[cpu.offset(cpu.er14, POS)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, COUNT)]
        cpu.er0 += -1
        cpu.mem16[cpu.offset(cpu.er14, COUNT)] = cpu.er0
        cpu.jump('record')
        cpu.label('last')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, HEADER + 4)]
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er14, POS)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.branch('bad')
        cpu.r0 = 0
        cpu.pop(cpu.pc)
        cpu.label('bad')
        cpu.r0 = 1
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_record_address():
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 26)]
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er14, POS)]
        cpu.er0 += cpu.er2
        cpu.r2 = cpu.mem8[cpu.offset(cpu.er14, 28)]
        cpu.ret()

    @fw.function(native=True)
    def graph_record_point():
        # Relative record coordinate offset ER12 -> P/Q.
        cpu.push(cpu.lr)
        cpu.call('fn_graph_record_address')
        cpu.er0 += cpu.er12
        cpu.er4 = cpu.mem16[cpu.offset(cpu.er14, D)]
        cpu.r4 += P & 255
        cpu.add_carry(cpu.r5, P >> 8)
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, BANK)]
        cpu.r3 = 40
        cpu.call('fn_graph_copy')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_record_replay():
        cpu.push(cpu.lr)
        cpu.er0 = 88
        cpu.mem16[cpu.offset(cpu.er14, POS)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, HEADER + 86)]
        cpu.mem16[cpu.offset(cpu.er14, COUNT)] = cpu.er0
        cpu.label('record')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, COUNT)]
        cpu.compare(cpu.r0, 0)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.eq:
            cpu.jump('done')
        cpu.call('fn_graph_record_address')
        cpu.r3 = cpu.mem8[cpu.r2, cpu.er0]
        cpu.mem8[cpu.offset(cpu.er14, KIND)] = cpu.r3
        cpu.r4 = cpu.mem8[cpu.r2, cpu.offset(cpu.er0, 1)]
        cpu.r5 = cpu.mem8[cpu.r2, cpu.offset(cpu.er0, 2)]
        cpu.mem16[cpu.offset(cpu.er14, SIZE)] = cpu.er4
        cpu.er12 = 3
        cpu.compare(cpu.r3, 5)
        if cpu.ne:
            cpu.branch('skip_2335')
        cpu.er12 = 5
        cpu.label('skip_2335')
        cpu.call('fn_graph_record_point')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, KIND)]
        cpu.compare(cpu.r0, 1)
        if cpu.eq:
            cpu.branch('point')
        cpu.compare(cpu.r0, 4)
        if cpu.eq:
            cpu.branch('text')
        cpu.compare(cpu.r0, 5)
        if cpu.eq:
            cpu.branch('stroke')
        cpu.er0 = P
        cpu.er4 = DX
        cpu.call('fn_graph_move')
        cpu.er0 = Q
        cpu.er4 = DY
        cpu.call('fn_graph_move')
        cpu.er12 = 43
        cpu.call('fn_graph_record_point')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, KIND)]
        cpu.compare(cpu.r0, 3)
        if cpu.eq:
            cpu.call('fn_graph_rectangle')
        else:
            cpu.call('fn_graph_line')
        cpu.branch('next')
        cpu.label('point')
        cpu.call('fn_graph_point_pixel')
        cpu.r2 = 1
        cpu.call('fn_graph_pixel')
        cpu.branch('next')
        cpu.label('text')
        cpu.call('fn_graph_point_pixel')
        cpu.mem16[cpu.offset(cpu.er14, 156)] = cpu.er0
        cpu.call('fn_graph_record_address')
        cpu.er0 += 43
        cpu.er6 = cpu.mem16[cpu.offset(cpu.er14, SIZE)]
        cpu.er6 += -43
        cpu.er4 = cpu.er14
        cpu.r4 += 0
        cpu.add_carry(cpu.r5, 1)
        cpu.r3 = 0
        cpu.label('text_copy')
        cpu.compare(cpu.r6, 0)
        cpu.compare_carry(cpu.r7, 0)
        if cpu.eq:
            cpu.branch('text_end')
        cpu.compare(cpu.r3, 63)
        if cpu.ge:
            cpu.branch('text_end')
        cpu.r1 = cpu.mem8[cpu.r2, cpu.er0]
        cpu.mem8[cpu.er4] = cpu.r1
        cpu.er0 += 1
        cpu.er4 += 1
        cpu.er6 += -1
        cpu.r3 += 1
        cpu.branch('text_copy')
        cpu.label('text_end')
        cpu.r0 = 0
        cpu.mem8[cpu.er4] = cpu.r0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 156)]
        cpu.compare(cpu.r0, 96)
        if cpu.ge:
            cpu.branch('next')
        cpu.compare(cpu.r1, 31)
        if cpu.ge:
            cpu.branch('next')
        cpu.r1 += 1
        cpu.er2 = cpu.er14
        cpu.r2 += 0
        cpu.add_carry(cpu.r3, 1)
        cpu.call(0x041DA)
        cpu.branch('next')
        cpu.label('stroke')
        cpu.call('fn_graph_record_address')
        cpu.er4 = cpu.er0
        cpu.r0 = cpu.mem8[cpu.r2, cpu.offset(cpu.er4, 3)]
        cpu.r1 = cpu.mem8[cpu.r2, cpu.offset(cpu.er4, 4)]
        cpu.er0 += -1
        cpu.mem16[cpu.offset(cpu.er14, 246)] = cpu.er0
        cpu.compare(cpu.r0, 0)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.ne:
            cpu.branch('skip_2417')
        cpu.call('fn_graph_point_pixel')
        cpu.r2 = 1
        cpu.call('fn_graph_pixel')
        cpu.branch('next')
        cpu.label('skip_2417')
        cpu.er12 = 5
        cpu.label('stroke_point')
        cpu.call('fn_graph_record_point')
        cpu.er0 = P
        cpu.er4 = DX
        cpu.call('fn_graph_move')
        cpu.er0 = Q
        cpu.er4 = DY
        cpu.call('fn_graph_move')
        cpu.er12 += 40
        cpu.push(cpu.er12)
        cpu.call('fn_graph_record_point')
        cpu.call('fn_graph_line')
        cpu.pop(cpu.er12)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 246)]
        cpu.er0 += -1
        cpu.mem16[cpu.offset(cpu.er14, 246)] = cpu.er0
        cpu.compare(cpu.r0, 0)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.gt:
            cpu.branch('stroke_point')
        cpu.label('next')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, POS)]
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er14, SIZE)]
        cpu.er0 += cpu.er2
        cpu.mem16[cpu.offset(cpu.er14, POS)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, COUNT)]
        cpu.er0 += -1
        cpu.mem16[cpu.offset(cpu.er14, COUNT)] = cpu.er0
        cpu.jump('record')
        cpu.label('done')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_point_pixel():
        cpu.push(cpu.lr)
        cpu.er0 = P
        cpu.er4 = V
        cpu.call('fn_graph_move')
        cpu.r0 = 0
        cpu.call('fn_graph_map')
        cpu.mem8[cpu.offset(cpu.er14, 156)] = cpu.r0
        cpu.er0 = Q
        cpu.er4 = V
        cpu.call('fn_graph_move')
        cpu.r0 = 1
        cpu.call('fn_graph_map')
        cpu.r1 = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 156)]
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_rectangle():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.er8
        cpu.r0 += P & 255
        cpu.add_carry(cpu.r1, P >> 8)
        cpu.r2 = cpu.r10
        cpu.er4 = cpu.er14
        cpu.r4 += 160
        cpu.add_carry(cpu.r5, 0)
        cpu.r6 = 0
        cpu.r3 = 80
        cpu.call('fn_graph_copy')
        cpu.r0 = 0
        cpu.mem8[cpu.offset(cpu.er14, 159)] = cpu.r0
        cpu.label('edge')
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.er14
        cpu.r0 += 160
        cpu.add_carry(cpu.r1, 0)
        cpu.r2 = 0
        cpu.er4 = cpu.er8
        cpu.r4 += P & 255
        cpu.add_carry(cpu.r5, P >> 8)
        cpu.r6 = cpu.r10
        cpu.r3 = 80
        cpu.call('fn_graph_copy')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 159)]
        cpu.compare(cpu.r0, 2)
        if cpu.lt:
            cpu.er0 = Q
            cpu.er4 = DY
            cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, 159)]
            cpu.compare(cpu.r1, 0)
            if cpu.eq:
                cpu.branch('skip_2508')
            cpu.er0 = DY
            cpu.er4 = Q
            cpu.label('skip_2508')
        else:
            cpu.er0 = P
            cpu.er4 = DX
            cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, 159)]
            cpu.compare(cpu.r1, 2)
            if cpu.eq:
                cpu.branch('skip_2516')
            cpu.er0 = DX
            cpu.er4 = P
            cpu.label('skip_2516')
        cpu.call('fn_graph_move')
        cpu.call('fn_graph_line')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 159)]
        cpu.r0 += 1
        cpu.mem8[cpu.offset(cpu.er14, 159)] = cpu.r0
        cpu.compare(cpu.r0, 4)
        if cpu.lt:
            cpu.branch('edge')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_sketch():
        cpu.push(cpu.lr)
        cpu.r0 = 0
        cpu.mem8[cpu.offset(cpu.er14, PAGE)] = cpu.r0
        cpu.label('menu')
        cpu.call('fn_graph_clear')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, PAGE)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.r1 = 1
            cpu.call('fn_graph_text')
            cpu.data(b'1:POINT 2:LINE\0\0')
            cpu.r1 = 9
            cpu.call('fn_graph_text')
            cpu.data(b'3:RECT 4:TEXT\0')
            cpu.r1 = 25
            cpu.call('fn_graph_text')
            cpu.data(b'RIGHT:MORE\0\0')
        else:
            cpu.r1 = 1
            cpu.call('fn_graph_text')
            cpu.data(b'1:PEN 2:UNDO\0\0')
            cpu.r1 = 9
            cpu.call('fn_graph_text')
            cpu.data(b'3:CLEAR\0')
        cpu.call(0x043BE)
        cpu.label('key')
        cpu.call(0x80800)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.jump('done')
        cpu.compare(cpu.r0, 0xFC)
        if cpu.ne:
            cpu.branch('skip_2562')
        cpu.r0 = 0
        cpu.mem8[cpu.offset(cpu.er14, PAGE)] = cpu.r0
        cpu.branch('menu')
        cpu.label('skip_2562')
        cpu.compare(cpu.r0, 0xFD)
        if cpu.ne:
            cpu.branch('skip_2567')
        cpu.r0 = 1
        cpu.mem8[cpu.offset(cpu.er14, PAGE)] = cpu.r0
        cpu.branch('menu')
        cpu.label('skip_2567')
        cpu.compare(cpu.r0, 0x31)
        if cpu.lt:
            cpu.branch('key')
        cpu.compare(cpu.r0, 0x34)
        if cpu.gt:
            cpu.branch('key')
        cpu.r0 += 208
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, PAGE)]
        cpu.compare(cpu.r1, 0)
        if cpu.ne:
            cpu.compare(cpu.r0, 1)
            if cpu.eq:
                cpu.r0 = 5
            else:
                cpu.compare(cpu.r0, 2)
                if cpu.ne:
                    cpu.branch('skip_2586')
                cpu.call('fn_graph_undo')
                cpu.jump('done')
                cpu.label('skip_2586')
                cpu.compare(cpu.r0, 3)
                if cpu.ne:
                    cpu.branch('skip_2590')
                cpu.call('fn_graph_clear_sketch')
                cpu.jump('done')
                cpu.label('skip_2590')
                cpu.branch('key')
        cpu.mem8[cpu.offset(cpu.er14, KIND)] = cpu.r0
        cpu.push(cpu.er0)
        cpu.call('fn_graph_plot')
        cpu.call('fn_graph_record_replay')
        cpu.pop(cpu.er0)
        cpu.mem8[cpu.offset(cpu.er14, KIND)] = cpu.r0
        cpu.call('fn_graph_slots')
        cpu.er4 = cpu.er8
        cpu.r4 += (-3072) & 255
        cpu.add_carry(cpu.r5, ((-3072) >> 8) & 255)
        cpu.mem8[cpu.r10, cpu.er4] = cpu.r0
        cpu.er0 = 3
        cpu.mem16[cpu.offset(cpu.er14, SIZE)] = cpu.er0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, KIND)]
        cpu.compare(cpu.r0, 5)
        if cpu.eq:
            cpu.er0 = 5
            cpu.mem16[cpu.offset(cpu.er14, SIZE)] = cpu.er0
            cpu.er0 = 0
            cpu.mem16[cpu.offset(cpu.er14, COUNT)] = cpu.er0
            cpu.r0 = 0
            cpu.mem8[cpu.offset(cpu.er14, MODE)] = cpu.r0
            cpu.branch('pen')
        cpu.call('fn_graph_pick')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.jump('done')
        cpu.call('fn_graph_stage_point')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, KIND)]
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.branch('second')
        cpu.compare(cpu.r0, 3)
        if cpu.eq:
            cpu.branch('second')
        cpu.compare(cpu.r0, 4)
        if cpu.eq:
            cpu.er0 = cpu.er14
            cpu.r0 += 0
            cpu.add_carry(cpu.r1, 1)
            cpu.er2 = 63
            cpu.call('fn_graph_text_input')
            cpu.compare(cpu.r0, 0)
            if cpu.eq:
                cpu.branch('done')
            cpu.r1 = 0
            cpu.push(cpu.er0)
            cpu.call('fn_graph_work')
            cpu.er0 = cpu.er14
            cpu.er0 += 16
            cpu.call('fn_mcs_open')
            cpu.pop(cpu.er0)
            cpu.push(cpu.er0)
            cpu.er6 = cpu.er0
            cpu.call('fn_graph_slots')
            cpu.er4 = cpu.er8
            cpu.r4 += (-3029) & 255
            cpu.add_carry(cpu.r5, ((-3029) >> 8) & 255)
            cpu.er0 = cpu.er14
            cpu.r0 += 0
            cpu.add_carry(cpu.r1, 1)
            cpu.label('text')
            cpu.r3 = cpu.mem8[cpu.er0]
            cpu.compare(cpu.r3, 0x20)
            if cpu.lt:
                cpu.branch('text_bad')
            cpu.compare(cpu.r3, 0x5F)
            if cpu.gt:
                cpu.branch('text_bad')
            cpu.mem8[cpu.r10, cpu.er4] = cpu.r3
            cpu.er4 += 1
            cpu.er0 += 1
            cpu.er6 += -1
            if cpu.ne:
                cpu.branch('text')
            cpu.pop(cpu.er0)
            cpu.er0 += 43
            cpu.mem16[cpu.offset(cpu.er14, SIZE)] = cpu.er0
        cpu.branch('commit')
        cpu.label('text_bad')
        cpu.pop(cpu.er0)
        cpu.branch('done')
        cpu.label('second')
        cpu.call('fn_graph_pick')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('done')
        cpu.call('fn_graph_stage_point')
        cpu.branch('commit')
        cpu.label('pen')
        cpu.call('fn_graph_cursor')
        cpu.call(0x043BE)
        cpu.call(0x80800)
        cpu.push(cpu.er0)
        cpu.call('fn_graph_cursor')
        cpu.pop(cpu.er0)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.branch('pen_end')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.eq:
            cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, MODE)]
            cpu.r0 ^= 1
            cpu.mem8[cpu.offset(cpu.er14, MODE)] = cpu.r0
            cpu.compare(cpu.r0, 0)
            if cpu.eq:
                cpu.call('fn_graph_pen_commit')
                cpu.compare(cpu.r0, 0)
                if cpu.ne:
                    cpu.branch('full')
                cpu.branch('pen')
            cpu.call('fn_graph_stage_point')
            cpu.compare(cpu.r0, 0)
            if cpu.ne:
                cpu.branch('full')
            cpu.branch('pen')
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er14, CX)]
        cpu.push(cpu.er2)
        cpu.call('fn_graph_cursor_key')
        cpu.pop(cpu.er2)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, CX)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.eq:
            cpu.branch('pen')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, MODE)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('pen')
        cpu.call('fn_graph_stage_point')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('full')
        cpu.branch('pen')
        cpu.label('pen_end')
        cpu.call('fn_graph_pen_commit')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('full')
        cpu.branch('done')
        cpu.label('commit')
        cpu.call('fn_graph_append')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('done')
        cpu.label('full')
        cpu.call('fn_graph_error')
        cpu.label('done')
        cpu.r0 = 0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_pick():
        cpu.push(cpu.lr)
        cpu.label('key')
        cpu.call('fn_graph_cursor')
        cpu.call(0x043BE)
        cpu.call(0x80800)
        cpu.push(cpu.er0)
        cpu.call('fn_graph_cursor')
        cpu.pop(cpu.er0)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('skip_2755')
        cpu.r0 = 0
        cpu.pop(cpu.pc)
        cpu.label('skip_2755')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.ne:
            cpu.branch('skip_2759')
        cpu.r0 = 1
        cpu.pop(cpu.pc)
        cpu.label('skip_2759')
        cpu.call('fn_graph_cursor_key')
        cpu.branch('key')

    @fw.function(native=True)
    def graph_stage_point():
        cpu.push(cpu.lr)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, SIZE)]
        cpu.er0 += 40
        cpu.compare(cpu.r0, 0)
        cpu.compare_carry(cpu.r1, 12)
        if cpu.le:
            cpu.branch('skip_2772')
        cpu.r0 = 1
        cpu.pop(cpu.pc)
        cpu.label('skip_2772')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, CX)]
        cpu.r1 = 0
        cpu.call('fn_graph_coord')
        cpu.call('fn_graph_slots')
        cpu.er4 = cpu.er8
        cpu.r4 += (-3072) & 255
        cpu.add_carry(cpu.r5, ((-3072) >> 8) & 255)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, SIZE)]
        cpu.er4 += cpu.er0
        cpu.er0 = cpu.er8
        cpu.r0 += V & 255
        cpu.add_carry(cpu.r1, V >> 8)
        cpu.r2 = cpu.r10
        cpu.r6 = cpu.r10
        cpu.r3 = 20
        cpu.call('fn_graph_copy')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, CY)]
        cpu.r1 = 1
        cpu.call('fn_graph_coord')
        cpu.call('fn_graph_slots')
        cpu.er4 = cpu.er8
        cpu.r4 += (-3052) & 255
        cpu.add_carry(cpu.r5, ((-3052) >> 8) & 255)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, SIZE)]
        cpu.er4 += cpu.er0
        cpu.er0 = cpu.er8
        cpu.r0 += V & 255
        cpu.add_carry(cpu.r1, V >> 8)
        cpu.r2 = cpu.r10
        cpu.r6 = cpu.r10
        cpu.r3 = 20
        cpu.call('fn_graph_copy')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, SIZE)]
        cpu.er0 += 40
        cpu.mem16[cpu.offset(cpu.er14, SIZE)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, COUNT)]
        cpu.er0 += 1
        cpu.mem16[cpu.offset(cpu.er14, COUNT)] = cpu.er0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, KIND)]
        cpu.compare(cpu.r0, 5)
        if cpu.ne:
            cpu.branch('skip_2815')
        cpu.call('fn_graph_pen_preview')
        cpu.label('skip_2815')
        cpu.r0 = 0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_append():
        cpu.push(cpu.lr)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, HEADER + 86)]
        cpu.compare(cpu.r0, 255)
        cpu.compare_carry(cpu.r1, 255)
        if cpu.eq:
            cpu.branch('full')
        cpu.call('fn_graph_slots')
        cpu.er4 = cpu.er8
        cpu.r4 += (-3071) & 255
        cpu.add_carry(cpu.r5, ((-3071) >> 8) & 255)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, SIZE)]
        cpu.mem8[cpu.r10, cpu.er4] = cpu.r0
        cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 1)] = cpu.r1
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er14, HEADER + 4)]
        cpu.er0 += cpu.er2
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('full')
        cpu.mem16[cpu.offset(cpu.er14, 24)] = cpu.er0
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.call('fn_mcs_resize')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('done')
        cpu.call('fn_graph_work')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('done')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, D)]
        cpu.r0 += (-3072) & 255
        cpu.add_carry(cpu.r1, ((-3072) >> 8) & 255)
        cpu.r2 = cpu.mem8[cpu.offset(cpu.er14, BANK)]
        cpu.er4 = cpu.mem16[cpu.offset(cpu.er14, 26)]
        cpu.er6 = cpu.mem16[cpu.offset(cpu.er14, HEADER + 4)]
        cpu.er4 += cpu.er6
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, 28)]
        cpu.er12 = cpu.mem16[cpu.offset(cpu.er14, SIZE)]
        cpu.label('copy')
        cpu.r3 = cpu.mem8[cpu.r2, cpu.er0]
        cpu.mem8[cpu.r6, cpu.er4] = cpu.r3
        cpu.er0 += 1
        cpu.er4 += 1
        cpu.er12 += -1
        if cpu.ne:
            cpu.branch('copy')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 24)]
        cpu.mem16[cpu.offset(cpu.er14, HEADER + 4)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, HEADER + 86)]
        cpu.er0 += 1
        cpu.mem16[cpu.offset(cpu.er14, HEADER + 86)] = cpu.er0
        cpu.call('fn_graph_save')
        cpu.r0 = 0
        cpu.branch('done')
        cpu.label('full')
        cpu.r0 = 1
        cpu.label('done')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_undo():
        cpu.push(cpu.lr)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, HEADER + 86)]
        cpu.compare(cpu.r0, 0)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.eq:
            cpu.branch('done')
        cpu.er0 += -1
        cpu.mem16[cpu.offset(cpu.er14, COUNT)] = cpu.er0
        cpu.er0 = 88
        cpu.mem16[cpu.offset(cpu.er14, POS)] = cpu.er0
        cpu.label('scan')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, COUNT)]
        cpu.compare(cpu.r0, 0)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.eq:
            cpu.branch('truncate')
        cpu.call('fn_graph_record_address')
        cpu.er4 = cpu.er0
        cpu.r0 = cpu.mem8[cpu.r2, cpu.offset(cpu.er4, 1)]
        cpu.r1 = cpu.mem8[cpu.r2, cpu.offset(cpu.er4, 2)]
        cpu.er2 = cpu.mem16[cpu.offset(cpu.er14, POS)]
        cpu.er0 += cpu.er2
        cpu.mem16[cpu.offset(cpu.er14, POS)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, COUNT)]
        cpu.er0 += -1
        cpu.mem16[cpu.offset(cpu.er14, COUNT)] = cpu.er0
        cpu.branch('scan')
        cpu.label('truncate')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, POS)]
        cpu.mem16[cpu.offset(cpu.er14, 24)] = cpu.er0
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.call('fn_mcs_resize')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_2914')
        cpu.call('fn_graph_error')
        cpu.branch('done')
        cpu.label('skip_2914')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, POS)]
        cpu.mem16[cpu.offset(cpu.er14, HEADER + 4)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, HEADER + 86)]
        cpu.er0 += -1
        cpu.mem16[cpu.offset(cpu.er14, HEADER + 86)] = cpu.er0
        cpu.call('fn_graph_save')
        cpu.call('fn_graph_work')
        cpu.label('done')
        cpu.r0 = 0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_clear_sketch():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_clear')
        cpu.r1 = 9
        cpu.call('fn_graph_text')
        cpu.data(b'CLEAR SKETCH?\0')
        cpu.call('fn_graph_wait')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.ne:
            cpu.branch('done')
        cpu.er0 = 88
        cpu.mem16[cpu.offset(cpu.er14, 24)] = cpu.er0
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.call('fn_mcs_resize')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_2945')
        cpu.call('fn_graph_error')
        cpu.branch('done')
        cpu.label('skip_2945')
        cpu.er0 = 88
        cpu.mem16[cpu.offset(cpu.er14, HEADER + 4)] = cpu.er0
        cpu.er0 = 0
        cpu.mem16[cpu.offset(cpu.er14, HEADER + 86)] = cpu.er0
        cpu.call('fn_graph_save')
        cpu.call('fn_graph_work')
        cpu.label('done')
        cpu.r0 = 0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_tangent():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_clear')
        cpu.r1 = 9
        cpu.call('fn_graph_text')
        cpu.data(b'ADD TANGENT?\0\0')
        cpu.call('fn_graph_wait')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.ne:
            cpu.branch('done')
        cpu.er0 = 24
        cpu.er4 = 172
        cpu.call('fn_graph_move')
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.call('fn_graph_eval')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('done')
        cpu.er0 = 24
        cpu.er4 = 152
        cpu.call('fn_graph_move')
        cpu.er0 = XMIN
        cpu.er4 = P
        cpu.call('fn_graph_move')
        cpu.er0 = XMAX
        cpu.er4 = DX
        cpu.call('fn_graph_move')
        cpu.er4 = P
        cpu.er6 = 4
        cpu.er12 = T
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.er4 = T
        cpu.er6 = 172
        cpu.er12 = T
        cpu.r3 = 0xA9
        cpu.call('fn_graph_op')
        cpu.er4 = T
        cpu.er6 = 152
        cpu.er12 = Q
        cpu.r3 = 0x89
        cpu.call('fn_graph_op')
        cpu.er4 = DX
        cpu.er6 = 4
        cpu.er12 = T
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.er4 = T
        cpu.er6 = 172
        cpu.er12 = T
        cpu.r3 = 0xA9
        cpu.call('fn_graph_op')
        cpu.er4 = T
        cpu.er6 = 152
        cpu.er12 = DY
        cpu.r3 = 0x89
        cpu.call('fn_graph_op')
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.er8
        cpu.r0 += P & 255
        cpu.add_carry(cpu.r1, P >> 8)
        cpu.r2 = cpu.r10
        cpu.er4 = cpu.er8
        cpu.r4 += (-3069) & 255
        cpu.add_carry(cpu.r5, ((-3069) >> 8) & 255)
        cpu.r6 = cpu.r10
        cpu.r3 = 80
        cpu.call('fn_graph_copy')
        cpu.er4 += -3
        cpu.r0 = 2
        cpu.mem8[cpu.r10, cpu.er4] = cpu.r0
        cpu.er0 = 83
        cpu.mem16[cpu.offset(cpu.er14, SIZE)] = cpu.er0
        cpu.call('fn_graph_append')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_3036')
        cpu.call('fn_graph_error')
        cpu.label('skip_3036')
        cpu.label('done')
        cpu.r0 = 0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_shade():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_plot')
        cpu.r0 = 0
        cpu.mem8[cpu.offset(cpu.er14, COL)] = cpu.r0
        cpu.label('column')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, COL)]
        cpu.r1 = 0
        cpu.call('fn_graph_coord')
        cpu.er0 = V
        cpu.er4 = P
        cpu.call('fn_graph_move')
        cpu.er4 = 44
        cpu.er6 = 64
        cpu.call('fn_graph_cmp')
        cpu.compare(cpu.r0, 4)
        if cpu.eq:
            cpu.er4 = P
            cpu.er6 = 64
        else:
            cpu.er4 = P
            cpu.er6 = 44
        cpu.call('fn_graph_cmp')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.branch('next')
        cpu.er4 = 44
        cpu.er6 = 64
        cpu.call('fn_graph_cmp')
        cpu.compare(cpu.r0, 4)
        if cpu.eq:
            cpu.er4 = P
            cpu.er6 = 44
        else:
            cpu.er4 = P
            cpu.er6 = 64
        cpu.call('fn_graph_cmp')
        cpu.compare(cpu.r0, 4)
        if cpu.eq:
            cpu.branch('next')
        cpu.er0 = P
        cpu.er4 = 4
        cpu.call('fn_graph_move')
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.call('fn_graph_eval')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.branch('done')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('next')
        cpu.er0 = 24
        cpu.er4 = Q
        cpu.call('fn_graph_move')
        cpu.er0 = P
        cpu.er4 = DX
        cpu.call('fn_graph_move')
        cpu.er0 = ZERO
        cpu.er4 = DY
        cpu.call('fn_graph_move')
        cpu.call('fn_graph_line')
        cpu.label('next')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, COL)]
        cpu.r0 += 3
        cpu.mem8[cpu.offset(cpu.er14, COL)] = cpu.r0
        cpu.compare(cpu.r0, 96)
        if cpu.lt:
            cpu.branch('column')
        cpu.label('done')
        cpu.call('fn_graph_record_replay')
        cpu.call('fn_graph_wait')
        cpu.r0 = 0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_owner():
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 30)]
        cpu.compare(cpu.r0, 4)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.lt:
            cpu.branch('used')
        cpu.er4 = cpu.mem16[cpu.offset(cpu.er14, 26)]
        cpu.r2 = cpu.mem8[cpu.offset(cpu.er14, 28)]
        cpu.er0 = cpu.mem16[cpu.r2, cpu.er4]
        cpu.compare(cpu.r0, 0x45)
        cpu.compare_carry(cpu.r1, 0x47)
        if cpu.ne:
            cpu.branch('used')
        cpu.er0 = cpu.mem16[cpu.r2, cpu.offset(cpu.er4, 2)]
        cpu.compare(cpu.r0, 0x53)
        cpu.compare_carry(cpu.r1, 0x31)
        if cpu.ne:
            cpu.branch('used')
        cpu.r0 = 0
        cpu.ret()
        cpu.label('used')
        cpu.r0 = 2
        cpu.ret()

    @fw.function(native=True)
    def graph_bounds_check():
        cpu.push(cpu.lr)
        cpu.er4 = cpu.er14
        cpu.er4 += HEADER + 6
        cpu.er6 = 4
        cpu.label('number')
        cpu.er0 = cpu.er4
        cpu.r2 = 0
        cpu.call('fn_graph_scalar')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er4 += 20
        cpu.er6 += -1
        if cpu.ne:
            cpu.branch('number')
        cpu.er4 = cpu.er14
        cpu.er4 += HEADER + 6
        cpu.er6 = cpu.er4
        cpu.er6 += 20
        cpu.r10 = 0
        cpu.call('fn_graph_compare')
        cpu.compare(cpu.r0, 2)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er4 += 40
        cpu.er6 += 40
        cpu.call('fn_graph_compare')
        cpu.compare(cpu.r0, 2)
        if cpu.ne:
            cpu.branch('bad')
        cpu.r0 = 0
        cpu.pop(cpu.pc)
        cpu.label('bad')
        cpu.r0 = 1
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_trace_save():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.er8
        cpu.er0 += 4
        cpu.r2 = cpu.r10
        cpu.er4 = cpu.er14
        cpu.r4 += TRACE_X & 255
        cpu.add_carry(cpu.r5, TRACE_X >> 8)
        cpu.r6 = 0
        cpu.r3 = 20
        cpu.call('fn_graph_copy')
        cpu.r0 = 1
        cpu.mem8[cpu.offset(cpu.er14, TRACE_VALID)] = cpu.r0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_trace_load():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.er14
        cpu.r0 += TRACE_X & 255
        cpu.add_carry(cpu.r1, TRACE_X >> 8)
        cpu.r2 = 0
        cpu.er4 = cpu.er8
        cpu.er4 += 4
        cpu.r6 = cpu.r10
        cpu.r3 = 20
        cpu.call('fn_graph_copy')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_result_flags():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_slots')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er8, 84)]
        cpu.mem8[cpu.offset(cpu.er14, 151)] = cpu.r0
        cpu.r0 &= 1
        if cpu.eq:
            cpu.branch('skip_3221')
        cpu.r1 = 1
        cpu.call('fn_graph_text')
        cpu.data(b'ENDPOINT\0\0')
        cpu.label('skip_3221')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 151)]
        cpu.r0 &= 2
        if cpu.eq:
            cpu.branch('skip_3227')
        cpu.r1 = 9
        cpu.call('fn_graph_text')
        cpu.data(b'FLAT\0\0')
        cpu.label('skip_3227')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_window_valid():
        cpu.push(cpu.lr)
        cpu.er4 = XMIN
        cpu.er6 = XMAX
        cpu.call('fn_graph_cmp')
        cpu.compare(cpu.r0, 2)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er4 = YMIN
        cpu.er6 = YMAX
        cpu.call('fn_graph_cmp')
        cpu.compare(cpu.r0, 2)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er4 = XMAX
        cpu.er6 = XMIN
        cpu.er12 = T
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er4 = YMAX
        cpu.er6 = YMIN
        cpu.er12 = T
        cpu.r3 = 0x99
        cpu.call('fn_graph_op')
        cpu.pop(cpu.pc)
        cpu.label('bad')
        cpu.r0 = 1
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_pen_preview():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_slots')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, COUNT)]
        cpu.compare(cpu.r0, 1)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.ne:
            cpu.branch('skip_3273')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, CX)]
        cpu.r1 = cpu.mem8[cpu.offset(cpu.er14, CY)]
        cpu.r2 = 1
        cpu.call('fn_graph_pixel')
        cpu.branch('done')
        cpu.label('skip_3273')
        cpu.er0 += -2
        cpu.r2 = 40
        cpu.multiply(cpu.er0, cpu.r2)
        cpu.er0 += cpu.er8
        cpu.r0 += (-3067) & 255
        cpu.add_carry(cpu.r1, ((-3067) >> 8) & 255)
        cpu.r2 = cpu.r10
        cpu.er4 = cpu.er8
        cpu.r4 += P & 255
        cpu.add_carry(cpu.r5, P >> 8)
        cpu.r6 = cpu.r10
        cpu.r3 = 80
        cpu.call('fn_graph_copy')
        cpu.call('fn_graph_line')
        cpu.label('done')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_close_work():
        cpu.push(cpu.lr)
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, OWN_WORK)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('done')
        cpu.call('fn_graph_work')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('done')
        cpu.er4 = cpu.mem16[cpu.offset(cpu.er14, 10)]
        cpu.r2 = cpu.mem8[cpu.offset(cpu.er14, 12)]
        cpu.er0 = cpu.mem16[cpu.r2, cpu.er4]
        cpu.compare(cpu.r0, 0x45)
        cpu.compare_carry(cpu.r1, 0x47)
        if cpu.ne:
            cpu.branch('done')
        cpu.er0 = cpu.mem16[cpu.r2, cpu.offset(cpu.er4, 2)]
        cpu.compare(cpu.r0, 0x57)
        cpu.compare_carry(cpu.r1, 0x31)
        if cpu.ne:
            cpu.branch('done')
        cpu.er0 = cpu.er14
        cpu.call('fn_mcs_remove')
        cpu.label('done')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_release():
        cpu.push(cpu.lr)
        cpu.label('held')
        cpu.call('fn_graph_cancel')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('held')
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_pen_commit():
        cpu.push(cpu.lr)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, COUNT)]
        cpu.compare(cpu.r0, 0)
        cpu.compare_carry(cpu.r1, 0)
        if cpu.ne:
            cpu.branch('skip_3340')
        cpu.r0 = 0
        cpu.pop(cpu.pc)
        cpu.label('skip_3340')
        cpu.call('fn_graph_slots')
        cpu.er4 = cpu.er8
        cpu.r4 += (-3069) & 255
        cpu.add_carry(cpu.r5, ((-3069) >> 8) & 255)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, COUNT)]
        cpu.mem8[cpu.r10, cpu.er4] = cpu.r0
        cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 1)] = cpu.r1
        cpu.call('fn_graph_append')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('skip_3351')
        cpu.pop(cpu.pc)
        cpu.label('skip_3351')
        cpu.er0 = 5
        cpu.mem16[cpu.offset(cpu.er14, SIZE)] = cpu.er0
        cpu.er0 = 0
        cpu.mem16[cpu.offset(cpu.er14, COUNT)] = cpu.er0
        cpu.call('fn_graph_slots')
        cpu.er4 = cpu.er8
        cpu.r4 += (-3072) & 255
        cpu.add_carry(cpu.r5, ((-3072) >> 8) & 255)
        cpu.r0 = 5
        cpu.mem8[cpu.r10, cpu.er4] = cpu.r0
        cpu.r0 = 0
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_cancel_hint():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_clear')
        cpu.r1 = 25
        cpu.call('fn_graph_text')
        cpu.data(b'AC/EXIT:CANCEL\0\0')
        cpu.call(0x043BE)
        cpu.pop(cpu.pc)
