"""Native20 graph evaluation and numerical analysis.

The small instruction stream keeps the analysis loops in Flash without expanding
hundreds of copies of the native evaluator's calling sequence. Its operands are
20-byte values in GWORK, never host or fixed-point approximations.

ER0/R2 address the calculation descriptor; public entries preserve R4..R15.
Descriptor +128 holds the repeated-evaluation value, +160 the original X,
+512 the sample/candidate bits, and +640..843 the evaluator saves and A/B
expression. The first 3072 GWORK bytes are reused by the numerical algorithms.
The VM's 128-byte near frame holds its code origin, counters and return stack;
no allocator or MCS service is called from this module.
"""

from decimal import Decimal

from kits import cpu


# Formula/numeric editors can clear 8086. This wrapper owns a fresh 328-byte
# workspace; graph_native restores the caller's saved 8086 afterward.
EVALUATE = 0xC7C12
VARIABLE_A = 0x7086
VARIABLE_B = 0x709A
VARIABLE_X = 0x7252
VARIABLE_ANS = 0x728E

# Public descriptor, relative to the last 1024 bytes of the calculation area.
FORMULA_LENGTH = 0
OPERATION = 2
STATUS = 3
X = 4
Y = 24
A = 44
B = 64
FLAGS = 84
TEXT = 96
FORMULA = 1024

SUCCESS = 0
UNDEFINED = 1
CANCELLED = 2
NATIVE_ERROR = 3
NO_CONVERGENCE = 4
NO_ROOT = 5
UNCONFIRMED = 6
UNSTABLE = 7


def _number(text):
    value = Decimal(text)
    result = bytearray(20)
    if value:
        sign, digits, exponent = value.as_tuple()
        exponent += len(digits) - 1
        if len(digits) > 15 or not -99 <= exponent <= 99:
            raise ValueError('Graph constant is outside native20 precision')
        digits = ''.join(str(d) for d in digits).ljust(15, '0')
        result[0] = int(digits[0])
        for i in range(1, 15, 2):
            result[(i + 1) // 2] = int(digits[i:i + 2], 16)
        result[8] = int(f'{exponent % 100:02d}', 16)
        result[9] = 5 * sign + (exponent >= 0)
    return bytes(result)


class _Program:
    def __init__(self):
        self.code = bytearray()
        self.labels = {}
        self.links = []

    def emit(self, *args):
        self.code.extend(args)

    def label(self, name):
        if name in self.labels:
            raise ValueError('Duplicate graph label: ' + name)
        self.labels[name] = len(self.code)

    def target(self, name):
        self.links.append((len(self.code), name))
        self.code.extend(b'\0\0')

    def end(self, status=SUCCESS):
        self.emit(0, status)

    def const(self, dst, value):
        self.emit(1, dst)
        # The VM restores the zero imaginary component.
        self.code.extend(_number(value)[:10])

    def mov(self, dst, src):
        self.emit(2, dst, src)

    def math(self, op, dst, a, b):
        self.emit({'+': 3, '-': 4, '*': 5, '/': 6}[op], dst, a, b)

    def abs(self, dst, src):
        self.emit(7, dst, src)

    def neg(self, dst, src):
        self.emit(8, dst, src)

    def eval(self, dst, src, domain='domain'):
        self.emit(9, dst, src)
        self.target(domain)

    def cmp(self, a, relation, b, target):
        self.emit(10, a, b, {'==': 1, '<': 2, '>': 4,
                            '<=': 3, '>=': 5, '!=': 6}[relation])
        self.target(target)

    def jump(self, target):
        self.emit(11)
        self.target(target)

    def call(self, target):
        self.emit(12)
        self.target(target)

    def ret(self):
        self.emit(13)

    def get(self, dst, offset):
        self.emit(14, dst, offset)

    def put(self, offset, src):
        self.emit(15, offset, src)

    def flags(self, value):
        self.emit(16, value)

    def set(self, index, value):
        self.emit(17, index, value)

    def inc(self, index, value=1):
        self.emit(18, index, value & 255)

    def test(self, index, relation, value, target):
        self.emit(19, index, value, {'==': 1, '<': 2, '>': 4,
                                    '<=': 3, '>=': 5, '!=': 6}[relation])
        self.target(target)

    def index(self, dst, src):
        self.emit(20, dst, src)

    def load(self, dst, base, index):
        self.emit(21, dst, base, index)

    def store(self, base, index, src):
        self.emit(22, base, index, src)

    def mark(self, index, mask):
        self.emit(23, index, mask)

    def marked(self, index, mask, target):
        self.emit(24, index, mask)
        self.target(target)

    def push(self):
        self.emit(25)

    def pop(self, empty):
        self.emit(26)
        self.target(empty)

    def depth(self, operation, target='convergence'):
        self.emit(27, operation)
        if operation == 2:
            self.target(target)

    def mode(self, value, target):
        self.emit(28, value)
        self.target(target)

    def loop(self, index, target):
        self.emit(29, index)
        self.target(target)

    def finish(self):
        for offset, name in self.links:
            self.code[offset:offset + 2] = self.labels[name].to_bytes(2, 'little')
        if len(self.code) & 1:
            self.code.append(0)
        return bytes(self.code)


def _program():
    p = _Program()
    p.mode(5, 'integral')
    p.const(0, '0')
    p.const(1, '1')
    p.const(2, '2')
    p.const(3, '1e-10')
    p.const(4, '1e-8')
    p.get(5, X)
    p.eval(10, 5, 'initial_checked')
    p.label('initial_checked')
    p.mode(4, 'slope')
    p.get(6, A)
    p.get(7, B)
    p.cmp(6, '>=', 7, 'domain')
    p.const(11, '32')
    p.math('-', 8, 7, 6)
    p.math('/', 8, 8, 11)
    p.cmp(8, '==', 0, 'convergence')
    p.mov(9, 6)
    p.set(0, 0)
    p.set(12, 1)
    p.set(13, 0)
    p.label('sample')
    p.test(0, '!=', 32, 'sample_eval')
    p.mov(9, 7)
    p.label('sample_eval')
    p.store(64, 0, 9)
    p.eval(10, 9, 'sample_undefined')
    p.store(97, 0, 10)
    p.inc(13)
    p.test(0, '!=', 0, 'sample_flat')
    p.mov(55, 10)
    p.jump('sample_next')
    p.label('sample_flat')
    p.cmp(10, '==', 55, 'sample_next')
    p.set(12, 0)
    p.jump('sample_next')
    p.label('sample_undefined')
    p.mark(0, 128)
    p.set(12, 0)
    p.label('sample_next')
    p.inc(0)
    p.test(0, '==', 33, 'sample_done')
    p.mov(11, 9)
    p.math('+', 9, 9, 8)
    p.cmp(9, '==', 11, 'convergence')
    p.jump('sample')
    p.label('sample_done')
    p.test(13, '==', 0, 'domain')
    p.mode(1, 'candidates')
    p.test(12, '==', 0, 'candidates')
    p.mov(9, 5)
    p.cmp(9, '>=', 6, 'flat_upper')
    p.mov(9, 6)
    p.label('flat_upper')
    p.cmp(9, '<=', 7, 'flat_value')
    p.mov(9, 7)
    p.label('flat_value')
    p.eval(10, 9)
    p.flags(2)
    p.jump('point')
    p.label('candidates')
    p.set(8, 0)
    p.set(9, 0)
    p.label('select')
    p.set(0, 0)
    p.set(5, 0)
    p.label('select_sample')
    p.marked(0, 128, 'select_next')
    p.load(9, 64, 0)
    p.load(10, 97, 0)
    p.mode(1, 'select_root')
    p.call('objective')
    p.mov(15, 10)
    p.test(0, '==', 0, 'left_endpoint')
    p.test(0, '==', 32, 'right_endpoint')
    p.marked(0, 4, 'select_next')
    p.index(1, 0)
    p.inc(1, -1)
    p.marked(1, 128, 'select_next')
    p.load(10, 97, 1)
    p.call('objective')
    p.mov(13, 10)
    p.index(1, 0)
    p.inc(1)
    p.marked(1, 128, 'select_next')
    p.load(10, 97, 1)
    p.call('objective')
    p.cmp(15, '>', 13, 'select_next')
    p.cmp(15, '>', 10, 'select_next')
    p.cmp(15, '<', 13, 'minimum_candidate')
    p.cmp(15, '==', 10, 'select_next')
    p.label('minimum_candidate')
    p.set(2, 4)
    p.call('consider')
    p.jump('select_next')
    p.label('left_endpoint')
    p.marked(0, 1, 'select_next')
    p.set(1, 1)
    p.jump('endpoint_neighbor')
    p.label('right_endpoint')
    p.marked(0, 1, 'select_next')
    p.set(1, 31)
    p.label('endpoint_neighbor')
    p.marked(1, 128, 'select_next')
    p.load(10, 97, 1)
    p.call('objective')
    p.cmp(15, '>', 10, 'select_next')
    p.set(2, 1)
    p.call('consider')
    p.jump('select_next')
    p.label('select_root')
    p.cmp(10, '!=', 0, 'select_sign')
    p.marked(0, 1, 'select_sign')
    p.set(2, 1)
    p.call('consider')
    p.label('select_sign')
    p.test(0, '==', 32, 'select_next')
    p.marked(0, 2, 'select_tangent')
    p.index(1, 0)
    p.inc(1)
    p.marked(1, 128, 'select_tangent')
    p.load(14, 97, 1)
    p.cmp(10, '<', 0, 'sign_negative')
    p.cmp(10, '==', 0, 'select_tangent')
    p.cmp(14, '>=', 0, 'select_tangent')
    p.jump('sign_candidate')
    p.label('sign_negative')
    p.cmp(14, '<=', 0, 'select_tangent')
    p.label('sign_candidate')
    p.load(13, 64, 1)
    p.math('-', 11, 13, 9)
    p.math('/', 11, 11, 2)
    p.math('+', 9, 9, 11)
    p.set(2, 2)
    p.call('consider')
    p.label('select_tangent')
    p.test(0, '==', 0, 'select_next')
    p.marked(0, 4, 'select_next')
    p.index(1, 0)
    p.inc(1, -1)
    p.marked(1, 128, 'select_next')
    p.load(13, 97, 1)
    p.abs(13, 13)
    p.index(1, 0)
    p.inc(1)
    p.marked(1, 128, 'select_next')
    p.load(14, 97, 1)
    p.abs(14, 14)
    p.load(10, 97, 0)
    p.abs(10, 10)
    p.cmp(10, '>', 13, 'select_next')
    p.cmp(10, '>', 14, 'select_next')
    p.cmp(10, '<', 13, 'tangent_candidate')
    p.cmp(10, '==', 14, 'select_next')
    p.label('tangent_candidate')
    p.load(9, 64, 0)
    p.set(2, 4)
    p.call('consider')
    p.label('select_next')
    p.inc(0)
    p.test(0, '<', 33, 'select_sample')
    p.test(5, '==', 0, 'exhausted')
    p.index(0, 3)
    p.test(4, '==', 1, 'selected_point')
    p.test(4, '==', 2, 'selected_root')
    p.mark(0, 4)
    p.load(20, 64, 0)
    p.index(1, 0)
    p.inc(1, -1)
    p.load(16, 64, 1)
    p.inc(1, 2)
    p.load(18, 64, 1)
    p.jump('minimum')
    p.label('selected_point')
    p.mark(0, 1)
    p.load(9, 64, 0)
    p.eval(10, 9, 'candidate_failed')
    p.mode(1, 'point')
    p.flags(1)
    p.jump('point')
    p.label('selected_root')
    p.mark(0, 2)
    p.load(16, 64, 0)
    p.load(17, 97, 0)
    p.index(1, 0)
    p.inc(1)
    p.load(18, 64, 1)
    p.load(19, 97, 1)
    p.jump('root')
    p.label('consider')
    p.math('-', 11, 9, 5)
    p.abs(11, 11)
    p.test(5, '==', 0, 'consider_save')
    p.cmp(11, '>=', 12, 'consider_done')
    p.label('consider_save')
    p.mov(12, 11)
    p.index(3, 0)
    p.index(4, 2)
    p.set(5, 1)
    p.label('consider_done')
    p.ret()
    p.label('objective')
    p.mode(1, 'objective_root')
    p.mode(3, 'objective_max')
    p.ret()
    p.label('objective_root')
    p.abs(10, 10)
    p.ret()
    p.label('objective_max')
    p.neg(10, 10)
    p.ret()
    p.label('candidate_failed')
    p.set(8, 1)
    p.jump('select')
    p.label('exhausted')
    p.test(9, '==', 1, 'unconfirmed')
    p.test(8, '==', 1, 'convergence')
    p.mode(1, 'no_root')
    p.jump('convergence')
    p.label('unconfirmed')
    p.put(X, 58)
    p.put(Y, 59)
    p.end(UNCONFIRMED)
    p.label('no_root')
    p.end(NO_ROOT)
    p.label('point')
    p.put(X, 9)
    p.put(Y, 10)
    p.end()

    # Brent-Dekker: [b,c] remains a sign bracket; b has the smaller residual.
    p.label('root')
    p.mov(20, 16)                 # c, fc, d, e
    p.mov(21, 17)
    p.math('-', 22, 18, 16)
    p.mov(23, 22)
    p.abs(40, 17)
    p.abs(41, 19)
    p.cmp(40, '>=', 41, 'root_scale')
    p.mov(40, 41)
    p.label('root_scale')
    p.mov(44, 40)
    p.math('*', 40, 40, 3)
    p.abs(43, 19)
    p.set(6, 128)
    p.set(10, 0)
    p.label('root_loop')
    p.cmp(19, '==', 0, 'root_point')
    p.cmp(19, '<', 0, 'root_negative')
    p.cmp(21, '<', 0, 'root_bracket')
    p.jump('root_reset')
    p.label('root_negative')
    p.cmp(21, '>', 0, 'root_bracket')
    p.label('root_reset')
    p.mov(20, 16)
    p.mov(21, 17)
    p.math('-', 22, 18, 16)
    p.mov(23, 22)
    p.label('root_bracket')
    p.abs(24, 21)
    p.abs(25, 19)
    p.cmp(24, '>=', 25, 'root_tolerance')
    p.mov(16, 18)
    p.mov(17, 19)
    p.mov(18, 20)
    p.mov(19, 21)
    p.mov(20, 16)
    p.mov(21, 17)
    p.label('root_tolerance')
    p.abs(26, 18)
    p.cmp(26, '>=', 1, 'root_tolerance_scale')
    p.mov(26, 1)
    p.label('root_tolerance_scale')
    p.math('*', 26, 26, 3)
    p.math('-', 27, 20, 18)
    p.abs(24, 27)
    p.cmp(24, '>', 26, 'root_step')
    p.abs(24, 19)
    p.cmp(24, '>', 40, 'candidate_failed')
    # A final interior sample must remain defined and not grow past the
    # original local scale. A narrow interval alone does not certify a pole.
    p.math('/', 9, 27, 2)
    p.math('+', 9, 18, 9)
    p.eval(10, 9, 'candidate_failed')
    p.abs(24, 10)
    p.cmp(24, '>', 44, 'candidate_failed')
    p.jump('root_point')
    p.label('root_step')
    p.math('/', 26, 26, 2)
    p.math('/', 27, 27, 2)
    p.abs(24, 23)
    p.cmp(24, '<', 26, 'root_bisect')
    p.abs(24, 17)
    p.abs(25, 19)
    p.cmp(24, '<=', 25, 'root_bisect')
    p.math('/', 28, 19, 17)       # s
    p.cmp(16, '!=', 20, 'root_quadratic')
    p.math('*', 29, 27, 28)       # p
    p.math('*', 29, 29, 2)
    p.math('-', 30, 1, 28)        # q
    p.jump('root_accept_interpolation')
    p.label('root_quadratic')
    p.math('/', 30, 17, 21)
    p.math('/', 31, 19, 21)       # r
    p.math('-', 32, 30, 31)
    p.math('*', 32, 32, 30)
    p.math('*', 32, 32, 27)
    p.math('*', 32, 32, 2)
    p.math('-', 33, 18, 16)
    p.math('-', 34, 31, 1)
    p.math('*', 33, 33, 34)
    p.math('-', 29, 32, 33)
    p.math('*', 29, 29, 28)
    p.math('-', 30, 30, 1)
    p.math('*', 30, 30, 34)
    p.math('-', 34, 28, 1)
    p.math('*', 30, 30, 34)
    p.label('root_accept_interpolation')
    p.cmp(29, '<=', 0, 'root_positive_p')
    p.neg(30, 30)
    p.label('root_positive_p')
    p.abs(29, 29)
    p.math('*', 32, 27, 30)
    p.math('*', 33, 32, 2)
    p.math('+', 32, 32, 33)       # 3*m*q - |tol*q|
    p.math('*', 33, 26, 30)
    p.abs(33, 33)
    p.math('-', 32, 32, 33)
    p.math('*', 33, 23, 30)
    p.abs(33, 33)
    p.cmp(32, '<=', 33, 'root_bound')
    p.mov(32, 33)
    p.label('root_bound')
    p.math('*', 33, 29, 2)
    p.cmp(33, '>=', 32, 'root_bisect')
    p.cmp(30, '==', 0, 'root_bisect')
    p.mov(23, 22)
    p.math('/', 22, 29, 30)
    p.jump('root_advance')
    p.label('root_bisect')
    p.mov(22, 27)
    p.mov(23, 27)
    p.label('root_advance')
    p.mov(16, 18)
    p.mov(17, 19)
    p.abs(24, 22)
    p.cmp(24, '>', 26, 'root_full_step')
    p.mov(22, 26)
    p.cmp(27, '>=', 0, 'root_full_step')
    p.neg(22, 22)
    p.label('root_full_step')
    p.math('+', 18, 18, 22)
    p.cmp(18, '==', 16, 'candidate_failed')
    p.eval(19, 18, 'candidate_failed')
    p.abs(24, 19)
    p.cmp(24, '<', 43, 'root_improving')
    p.inc(10)
    p.test(10, '>=', 12, 'candidate_failed')
    p.jump('root_continue')
    p.label('root_improving')
    p.mov(43, 24)
    p.set(10, 0)
    p.label('root_continue')
    p.loop(6, 'root_loop')
    p.jump('candidate_failed')
    p.label('root_point')
    p.mov(9, 18)
    p.eval(10, 9, 'candidate_failed')
    p.cmp(10, '!=', 19, 'unstable')
    p.jump('point')

    # Bounded Brent minimization is also the non-sign-changing ROOT search.
    p.label('minimum')
    p.mov(50, 16)
    p.mov(51, 18)
    p.mov(9, 20)
    p.eval(10, 9, 'candidate_failed')
    p.call('objective')
    p.mov(21, 10)
    p.mov(22, 20)
    p.mov(24, 20)
    p.mov(23, 21)
    p.mov(25, 21)
    p.mov(26, 0)
    p.mov(27, 0)
    p.const(41, '0.381966011250105')
    p.const(42, '4')
    p.set(6, 160)
    p.label('minimum_loop')
    p.abs(28, 20)
    p.cmp(28, '>=', 1, 'minimum_scale')
    p.mov(28, 1)
    p.label('minimum_scale')
    p.math('*', 28, 28, 3)
    p.math('-', 35, 18, 16)
    p.cmp(35, '<=', 28, 'minimum_done')
    p.math('/', 28, 28, 42)
    p.math('/', 29, 35, 2)
    p.math('+', 29, 16, 29)
    p.abs(35, 27)
    p.cmp(35, '<=', 28, 'minimum_golden')
    p.math('-', 35, 20, 22)
    p.math('-', 36, 21, 25)
    p.math('*', 32, 35, 36)       # r
    p.math('-', 36, 20, 24)
    p.math('-', 37, 21, 23)
    p.math('*', 31, 36, 37)       # q
    p.math('*', 30, 36, 31)
    p.math('*', 35, 35, 32)
    p.math('-', 30, 30, 35)       # p
    p.math('-', 31, 31, 32)
    p.math('*', 31, 31, 2)
    p.cmp(31, '<=', 0, 'minimum_q')
    p.neg(30, 30)
    p.label('minimum_q')
    p.abs(31, 31)
    p.mov(35, 27)
    p.mov(27, 26)
    p.abs(36, 30)
    p.math('*', 35, 35, 31)
    p.math('/', 35, 35, 2)
    p.abs(35, 35)
    p.cmp(36, '>=', 35, 'minimum_golden')
    p.math('-', 35, 16, 20)
    p.math('*', 35, 35, 31)
    p.cmp(30, '<=', 35, 'minimum_golden')
    p.math('-', 35, 18, 20)
    p.math('*', 35, 35, 31)
    p.cmp(30, '>=', 35, 'minimum_golden')
    p.cmp(31, '==', 0, 'minimum_golden')
    p.math('/', 26, 30, 31)
    p.math('+', 33, 20, 26)
    p.math('*', 35, 28, 2)
    p.math('-', 36, 33, 16)
    p.cmp(36, '<', 35, 'minimum_margin')
    p.math('-', 36, 18, 33)
    p.cmp(36, '>=', 35, 'minimum_step')
    p.label('minimum_margin')
    p.mov(26, 28)
    p.cmp(29, '>=', 20, 'minimum_step')
    p.neg(26, 26)
    p.jump('minimum_step')
    p.label('minimum_golden')
    p.cmp(20, '<', 29, 'minimum_right')
    p.math('-', 27, 16, 20)
    p.jump('minimum_golden_step')
    p.label('minimum_right')
    p.math('-', 27, 18, 20)
    p.label('minimum_golden_step')
    p.math('*', 26, 41, 27)
    p.label('minimum_step')
    p.abs(35, 26)
    p.cmp(35, '>=', 28, 'minimum_trial')
    p.cmp(26, '<', 0, 'minimum_negative_step')
    p.mov(26, 28)
    p.jump('minimum_trial')
    p.label('minimum_negative_step')
    p.neg(26, 28)
    p.label('minimum_trial')
    p.math('+', 33, 20, 26)
    p.cmp(33, '==', 20, 'candidate_failed')
    p.mov(9, 33)
    p.eval(10, 9, 'candidate_failed')
    p.call('objective')
    p.mov(34, 10)
    p.cmp(34, '>=', 21, 'minimum_worse')
    p.cmp(33, '<', 20, 'minimum_move_right')
    p.mov(16, 20)
    p.jump('minimum_replace')
    p.label('minimum_move_right')
    p.mov(18, 20)
    p.label('minimum_replace')
    p.mov(24, 22)
    p.mov(25, 23)
    p.mov(22, 20)
    p.mov(23, 21)
    p.mov(20, 33)
    p.mov(21, 34)
    p.jump('minimum_continue')
    p.label('minimum_worse')
    p.cmp(33, '<', 20, 'minimum_lower')
    p.mov(18, 33)
    p.jump('minimum_update_w')
    p.label('minimum_lower')
    p.mov(16, 33)
    p.label('minimum_update_w')
    p.cmp(34, '<=', 23, 'minimum_replace_w')
    p.cmp(22, '==', 20, 'minimum_replace_w')
    p.cmp(34, '<=', 25, 'minimum_replace_v')
    p.cmp(24, '==', 20, 'minimum_replace_v')
    p.cmp(24, '!=', 22, 'minimum_continue')
    p.label('minimum_replace_v')
    p.mov(24, 33)
    p.mov(25, 34)
    p.jump('minimum_continue')
    p.label('minimum_replace_w')
    p.mov(24, 22)
    p.mov(25, 23)
    p.mov(22, 33)
    p.mov(23, 34)
    p.label('minimum_continue')
    p.loop(6, 'minimum_loop')
    p.jump('candidate_failed')
    p.label('minimum_done')
    p.mov(9, 20)
    p.eval(10, 9, 'candidate_failed')
    p.mode(1, 'tangent_done')
    # Classify using values on both sides, not just a stationary point.
    p.mov(45, 10)
    p.call('objective')
    p.mov(46, 10)
    p.math('-', 47, 20, 50)
    p.math('/', 47, 47, 2)
    p.math('-', 48, 20, 47)
    p.cmp(48, '==', 20, 'candidate_failed')
    p.eval(10, 48, 'candidate_failed')
    p.call('objective')
    p.cmp(10, '<', 46, 'candidate_failed')
    p.mov(49, 10)
    p.math('-', 47, 51, 20)
    p.math('/', 47, 47, 2)
    p.math('+', 48, 20, 47)
    p.cmp(48, '==', 20, 'candidate_failed')
    p.eval(10, 48, 'candidate_failed')
    p.call('objective')
    p.cmp(10, '<', 46, 'candidate_failed')
    p.cmp(10, '!=', 46, 'minimum_point')
    p.cmp(49, '!=', 46, 'minimum_point')
    p.flags(2)
    p.label('minimum_point')
    p.mov(9, 20)
    p.mov(10, 45)
    p.jump('point')
    p.label('tangent_done')
    p.cmp(10, '==', 0, 'point')
    p.test(9, '==', 1, 'select')
    p.mov(58, 9)
    p.mov(59, 10)
    p.set(9, 1)
    p.jump('select')

    p.label('slope')
    p.eval(6, 5)
    p.abs(7, 5)
    p.cmp(7, '>=', 1, 'slope_scale')
    p.mov(7, 1)
    p.label('slope_scale')
    p.const(23, '0.001')
    p.math('*', 7, 7, 23)
    p.const(24, '4')
    p.const(25, '3')
    p.const(26, '0.9')
    p.set(0, 0)
    p.set(6, 48)
    p.label('slope_loop')
    p.math('+', 8, 5, 7)
    p.math('-', 9, 5, 7)
    p.cmp(8, '==', 5, 'convergence')
    p.cmp(9, '==', 5, 'convergence')
    p.eval(10, 8)
    p.eval(11, 9)
    p.cmp(10, '==', 6, 'slope_resolution')
    p.cmp(11, '==', 6, 'slope_resolution')
    p.jump('slope_difference')
    p.label('slope_resolution')
    p.cmp(6, '!=', 0, 'convergence')
    p.cmp(10, '!=', 0, 'slope_difference')
    p.cmp(11, '!=', 0, 'slope_difference')
    p.put(X, 5)
    p.put(Y, 0)
    p.end()
    p.label('slope_difference')
    p.math('-', 12, 10, 11)
    p.math('/', 12, 12, 7)
    p.math('/', 12, 12, 2)
    p.math('-', 16, 6, 11)
    p.math('/', 16, 16, 7)
    p.math('-', 17, 10, 6)
    p.math('/', 17, 17, 7)
    p.math('-', 20, 17, 16)
    p.abs(20, 20)
    p.test(0, '==', 0, 'slope_first')
    p.math('*', 14, 12, 24)
    p.math('-', 14, 14, 13)
    p.math('/', 14, 14, 25)
    p.abs(22, 14)
    p.cmp(22, '>=', 1, 'slope_tolerance')
    p.mov(22, 1)
    p.label('slope_tolerance')
    p.math('*', 22, 22, 4)
    p.test(0, '==', 1, 'slope_second')
    p.math('-', 18, 14, 15)
    p.abs(18, 18)
    p.cmp(18, '>', 22, 'slope_not_ready')
    p.math('*', 29, 16, 2)
    p.math('-', 29, 29, 27)
    p.math('-', 29, 29, 14)
    p.abs(29, 29)
    p.cmp(29, '>', 22, 'slope_not_ready')
    p.math('*', 29, 17, 2)
    p.math('-', 29, 29, 28)
    p.math('-', 29, 29, 14)
    p.abs(29, 29)
    p.cmp(29, '>', 22, 'slope_not_ready')
    p.put(X, 5)
    p.put(Y, 14)
    p.end()
    p.label('slope_not_ready')
    p.test(0, '<', 4, 'slope_remember')
    p.cmp(20, '<=', 22, 'slope_error')
    p.math('*', 23, 21, 26)
    p.cmp(20, '>=', 23, 'domain')
    p.label('slope_error')
    p.cmp(18, '<', 19, 'slope_remember')
    p.cmp(18, '>', 22, 'convergence')
    p.label('slope_remember')
    p.mov(19, 18)
    p.label('slope_second')
    p.mov(15, 14)
    p.label('slope_first')
    p.mov(13, 12)
    p.mov(21, 20)
    p.mov(27, 16)
    p.mov(28, 17)
    p.inc(0)
    p.math('/', 7, 7, 2)
    p.loop(6, 'slope_loop')
    p.jump('convergence')

    # Seven native20 fields followed by depth/padding form each 144-byte node.
    # The first 624 bytes hold registers; the remaining 2448 hold 17 nodes.
    p.label('integral')
    p.const(7, '0')
    p.const(8, '1')
    p.const(9, '2')
    p.const(10, '4')
    p.const(11, '6')
    p.const(12, '15')
    p.get(17, A)
    p.get(18, B)
    p.mov(30, 8)
    p.cmp(17, '==', 18, 'integral_zero')
    p.cmp(17, '<', 18, 'integral_ordered')
    p.mov(19, 17)
    p.mov(17, 18)
    p.mov(18, 19)
    p.neg(30, 8)
    p.label('integral_ordered')
    p.mov(0, 17)
    p.mov(1, 18)
    p.call('simpson_initial')
    p.abs(15, 5)
    p.cmp(15, '>=', 8, 'integral_budget')
    p.mov(15, 8)
    p.label('integral_budget')
    p.const(16, '1e-8')
    p.math('*', 15, 15, 16)
    p.set(6, 32)
    p.label('integral_restart')
    p.depth(0)
    p.mov(13, 7)                 # integral and accumulated absolute error
    p.mov(14, 7)
    p.mov(0, 17)
    p.mov(1, 18)
    p.call('simpson_initial')
    p.mov(6, 15)
    p.label('integral_node')
    p.math('-', 19, 1, 0)
    p.math('/', 19, 19, 9)
    p.math('+', 19, 0, 19)        # midpoint
    p.math('-', 20, 19, 0)
    p.math('/', 20, 20, 9)
    p.math('+', 20, 0, 20)
    p.math('-', 21, 1, 19)
    p.math('/', 21, 21, 9)
    p.math('+', 21, 19, 21)
    p.cmp(20, '==', 0, 'convergence')
    p.cmp(20, '==', 19, 'convergence')
    p.cmp(21, '==', 19, 'convergence')
    p.cmp(21, '==', 1, 'convergence')
    p.eval(22, 20)
    p.eval(23, 21)
    p.math('*', 24, 22, 10)
    p.math('+', 24, 24, 2)
    p.math('+', 24, 24, 3)
    p.math('-', 28, 19, 0)
    p.math('*', 24, 24, 28)
    p.math('/', 24, 24, 11)
    p.math('*', 25, 23, 10)
    p.math('+', 25, 25, 3)
    p.math('+', 25, 25, 4)
    p.math('-', 28, 1, 19)
    p.math('*', 25, 25, 28)
    p.math('/', 25, 25, 11)
    p.math('+', 26, 24, 25)
    p.math('-', 27, 26, 5)
    p.math('/', 27, 27, 12)
    p.abs(28, 27)
    p.cmp(28, '>', 6, 'integral_split')
    p.math('+', 26, 26, 27)
    p.math('+', 13, 13, 26)
    p.math('+', 14, 14, 28)
    p.pop('integral_complete')
    p.jump('integral_node')
    p.label('integral_split')
    p.depth(2)
    p.depth(1)
    p.math('/', 6, 6, 9)
    p.cmp(6, '==', 7, 'convergence')
    p.mov(29, 0)
    p.mov(20, 2)
    p.mov(21, 3)
    p.mov(0, 19)
    p.mov(2, 3)
    p.mov(3, 23)
    p.mov(5, 25)
    p.push()
    p.mov(0, 29)
    p.mov(1, 19)
    p.mov(2, 20)
    p.mov(3, 22)
    p.mov(4, 21)
    p.mov(5, 24)
    p.jump('integral_node')
    p.label('integral_complete')
    p.abs(16, 13)
    p.cmp(16, '>=', 8, 'integral_global_target')
    p.mov(16, 8)
    p.label('integral_global_target')
    p.const(28, '1e-8')
    p.math('*', 16, 16, 28)
    p.cmp(14, '<=', 16, 'integral_result')
    p.math('/', 15, 15, 9)
    p.math('/', 16, 16, 9)
    p.cmp(15, '<=', 16, 'integral_new_budget')
    p.mov(15, 16)
    p.label('integral_new_budget')
    p.cmp(15, '==', 7, 'convergence')
    p.loop(6, 'integral_restart')
    p.jump('convergence')
    p.label('integral_result')
    p.math('*', 13, 13, 30)
    p.put(Y, 13)
    p.end()
    p.label('integral_zero')
    p.put(Y, 7)
    p.end()
    p.label('simpson_initial')
    p.math('-', 19, 1, 0)
    p.math('/', 19, 19, 9)
    p.math('+', 19, 0, 19)
    p.cmp(19, '==', 0, 'convergence')
    p.cmp(19, '==', 1, 'convergence')
    p.eval(2, 0)
    p.eval(3, 19)
    p.eval(4, 1)
    p.math('*', 5, 3, 10)
    p.math('+', 5, 5, 2)
    p.math('+', 5, 5, 4)
    p.math('-', 19, 1, 0)
    p.math('*', 5, 5, 19)
    p.math('/', 5, 5, 11)
    p.ret()
    p.label('unstable')
    p.end(UNSTABLE)
    p.label('domain')
    p.end(UNDEFINED)
    p.label('convergence')
    p.end(NO_CONVERGENCE)
    return p.finish()


PROGRAM = _program()


def install(fw):
    @fw.function(native=True)
    def graph_copy():
        # ER0/R2 -> ER4/R6, R3 bytes. Preserve the destination registers.
        cpu.push(cpu.xr4)
        cpu.label('copy')
        cpu.r7 = cpu.mem8[cpu.r2, cpu.er0]
        cpu.mem8[cpu.r6, cpu.er4] = cpu.r7
        cpu.er0 += 1
        cpu.er4 += 1
        cpu.r3 += 255
        cpu.compare(cpu.r3, 0)
        if cpu.ne:
            cpu.branch('copy')
        cpu.pop(cpu.xr4)
        cpu.ret()

    @fw.function(native=True)
    def graph_scalar():
        # Real component: 15 BCD digits, BCD exponent and sign/exponent class.
        # A complex value is a scalar only when its entire imaginary half is 0.
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.er4 = cpu.er0
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.r0 &= 0xF0
        cpu.compare(cpu.r0, 0x80)
        if cpu.eq:
            cpu.er0 = cpu.er4
            cpu.call('fn_graph_normalize')
        cpu.r1 = cpu.mem8[cpu.r2, cpu.offset(cpu.er4, 9)]
        cpu.compare(cpu.r1, 6)
        if cpu.gt:
            cpu.jump('bad')
        cpu.compare(cpu.r1, 1)
        if cpu.gt:
            cpu.compare(cpu.r1, 5)
            if cpu.lt:
                cpu.jump('bad')
        cpu.r1 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.compare(cpu.r1, 9)
        if cpu.gt:
            cpu.jump('bad')
        cpu.r3 = 8
        cpu.label('bcd')
        cpu.er4 += 1
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.r1 = cpu.r0
        cpu.r1 &= 15
        cpu.compare(cpu.r1, 9)
        if cpu.gt:
            cpu.jump('bad')
        cpu.r0 >>= 4
        cpu.compare(cpu.r0, 9)
        if cpu.gt:
            cpu.jump('bad')
        cpu.r3 += 255
        cpu.compare(cpu.r3, 0)
        if cpu.ne:
            cpu.branch('bcd')
        cpu.er4 += 2
        cpu.r3 = 10
        cpu.label('imaginary')
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er4]
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.jump('bad')
        cpu.er4 += 1
        cpu.r3 += 255
        cpu.compare(cpu.r3, 0)
        if cpu.ne:
            cpu.branch('imaginary')
        cpu.r0 = SUCCESS
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('bad')
        cpu.r0 = UNDEFINED
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_eval():
        cpu.push(cpu.lr)
        cpu.push(cpu.er4)
        cpu.er4 = cpu.er0
        cpu.r4 += FORMULA & 255
        cpu.add_carry(cpu.r5, FORMULA >> 8)
        cpu.call('fn_graph_native')
        cpu.pop(cpu.er4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_native():
        # Internal entry: ER4 is the source offset in the descriptor's bank.
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.r10 = cpu.r2
        cpu.push(cpu.er4)
        cpu.er0 = 0x8000
        cpu.r2 = 0
        cpu.r3 = 112
        cpu.er4 = cpu.er8
        cpu.r4 += 128
        cpu.add_carry(cpu.r5, 2)
        cpu.r6 = cpu.r10
        cpu.call('fn_graph_copy')
        cpu.er0 = 0x8086
        cpu.r2 = 0
        cpu.r3 = 2
        cpu.er4 += 56
        cpu.er4 += 56
        cpu.call('fn_graph_copy')
        cpu.er0 = 0x8090
        cpu.r3 = 2
        cpu.er4 += 2
        cpu.call('fn_graph_copy')
        cpu.er0 = VARIABLE_X
        cpu.r2 = 4
        cpu.r3 = 20
        cpu.er4 += 2
        cpu.call('fn_graph_copy')
        cpu.er0 = VARIABLE_ANS
        cpu.r3 = 20
        cpu.er4 += 20
        cpu.call('fn_graph_copy')
        cpu.pop(cpu.er4)
        cpu.sp += -16
        cpu.er14 = cpu.sp
        cpu.mem16[0, cpu.er14] = cpu.er4
        cpu.mem8[0, cpu.offset(cpu.er14, 2)] = cpu.r10
        cpu.er0 = 1
        cpu.mem16[0, cpu.offset(cpu.er14, 4)] = cpu.er0
        cpu.er0 = cpu.er8
        cpu.er0 += X
        cpu.r2 = cpu.r10
        cpu.r3 = 20
        cpu.er4 = VARIABLE_X
        cpu.r6 = 4
        cpu.call('fn_graph_copy')
        cpu.er0 = 0
        cpu.push(cpu.er0)
        cpu.r0 = cpu.r10
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er8
        cpu.er0 += Y
        cpu.push(cpu.er0)
        cpu.er0 = 0
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.er0 += 4
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er14
        cpu.r2 = 0
        cpu.r3 = 1
        cpu.call(EVALUATE)
        cpu.sp += 10
        cpu.mem8[0, cpu.offset(cpu.er14, 8)] = cpu.r0
        cpu.er0 = cpu.er8
        cpu.r0 += 128
        cpu.add_carry(cpu.r1, 2)
        cpu.r2 = cpu.r10
        cpu.r3 = 112
        cpu.er4 = 0x8000
        cpu.r6 = 0
        cpu.call('fn_graph_copy')
        cpu.r3 = 2
        cpu.er4 = 0x8086
        cpu.call('fn_graph_copy')
        cpu.r3 = 2
        cpu.er4 = 0x8090
        cpu.call('fn_graph_copy')
        cpu.r3 = 20
        cpu.er4 = VARIABLE_X
        cpu.r6 = 4
        cpu.call('fn_graph_copy')
        cpu.r3 = 20
        cpu.er4 = VARIABLE_ANS
        cpu.call('fn_graph_copy')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 8)]
        cpu.compare(cpu.r0, 1)
        if cpu.eq:
            cpu.er0 = cpu.er8
            cpu.er0 += Y
            cpu.r2 = cpu.r10
            cpu.call('fn_graph_scalar')
        else:
            cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er8, Y)]
            cpu.compare(cpu.r0, 0xF1)
            if cpu.eq:
                cpu.r0 = CANCELLED
            else:
                cpu.compare(cpu.r0, 0xF3)
                if cpu.eq:
                    cpu.r0 = UNDEFINED
                else:
                    cpu.r0 = NATIVE_ERROR
        cpu.mem8[cpu.r10, cpu.offset(cpu.er8, STATUS)] = cpu.r0
        cpu.call('fn_graph_cancel')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.r0 = CANCELLED
            cpu.mem8[cpu.r10, cpu.offset(cpu.er8, STATUS)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er8, STATUS)]
        cpu.sp += 16
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_arithmetic():
        # ER0/R2 descriptor; R3 operator; ER4/ER6 input native20 offsets.
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.r10 = cpu.r2
        cpu.mem8[cpu.r10, cpu.offset(cpu.er8, 841)] = cpu.r3
        cpu.push(cpu.er4)
        cpu.push(cpu.er6)
        cpu.er0 = VARIABLE_A
        cpu.r2 = 4
        cpu.r3 = 40
        cpu.er4 = cpu.er8
        cpu.r4 += 32
        cpu.add_carry(cpu.r5, 3)
        cpu.r6 = cpu.r10
        cpu.call('fn_graph_copy')
        cpu.pop(cpu.er6)
        cpu.pop(cpu.er4)
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er4
        cpu.r2 = cpu.r10
        cpu.r3 = 20
        cpu.er4 = VARIABLE_A
        cpu.r6 = 4
        cpu.call('fn_graph_copy')
        cpu.pop(cpu.er0)
        cpu.r3 = 20
        cpu.er4 = VARIABLE_B
        cpu.call('fn_graph_copy')
        cpu.r0 = 0x41
        cpu.mem8[cpu.r10, cpu.offset(cpu.er8, 840)] = cpu.r0
        cpu.r0 = 0x42
        cpu.mem8[cpu.r10, cpu.offset(cpu.er8, 842)] = cpu.r0
        cpu.r0 = 0
        cpu.mem8[cpu.r10, cpu.offset(cpu.er8, 843)] = cpu.r0
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.er4 = cpu.er8
        cpu.r4 += 72
        cpu.add_carry(cpu.r5, 3)
        cpu.call('fn_graph_native')
        cpu.push(cpu.er0)
        cpu.er0 = cpu.er8
        cpu.r0 += 32
        cpu.add_carry(cpu.r1, 3)
        cpu.r2 = cpu.r10
        cpu.r3 = 40
        cpu.er4 = VARIABLE_A
        cpu.r6 = 4
        cpu.call('fn_graph_copy')
        cpu.pop(cpu.er0)
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_compare():
        # ER4/ER6 operands in R10's bank. Return 1 equal, 2 less, 4 greater.
        # Compare the encoding instead of subtracting values near overflow.
        cpu.push(cpu.xr4)
        cpu.push(cpu.er8)
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.r1 = cpu.mem8[cpu.r10, cpu.er6]
        cpu.r2 = cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 9)]
        cpu.r3 = cpu.mem8[cpu.r10, cpu.offset(cpu.er6, 9)]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.compare(cpu.r1, 0)
            if cpu.eq:
                cpu.jump('equal')
            cpu.compare(cpu.r3, 5)
            if cpu.ge:
                cpu.jump('greater')
            cpu.jump('less')
        cpu.compare(cpu.r1, 0)
        if cpu.eq:
            cpu.compare(cpu.r2, 5)
            if cpu.ge:
                cpu.jump('less')
            cpu.jump('greater')
        cpu.r8 = 0
        cpu.compare(cpu.r2, 5)
        if cpu.ge:
            cpu.compare(cpu.r3, 5)
            if cpu.lt:
                cpu.jump('less')
            cpu.r2 += 251
            cpu.r3 += 251
            cpu.r8 = 1
        else:
            cpu.compare(cpu.r3, 5)
            if cpu.ge:
                cpu.jump('greater')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 8)]
        cpu.r1 = cpu.mem8[cpu.r10, cpu.offset(cpu.er6, 8)]
        cpu.compare(cpu.r2, cpu.r3)
        if cpu.lt:
            cpu.jump('magnitude_less')
        if cpu.gt:
            cpu.jump('magnitude_greater')
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.lt:
            cpu.jump('magnitude_less')
        if cpu.gt:
            cpu.jump('magnitude_greater')
        cpu.r2 = 8
        cpu.label('digits')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.r1 = cpu.mem8[cpu.r10, cpu.er6]
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.lt:
            cpu.jump('magnitude_less')
        if cpu.gt:
            cpu.jump('magnitude_greater')
        cpu.er4 += 1
        cpu.er6 += 1
        cpu.r2 += 255
        cpu.compare(cpu.r2, 0)
        if cpu.ne:
            cpu.branch('digits')
        cpu.label('equal')
        cpu.r0 = 1
        cpu.pop(cpu.er8)
        cpu.pop(cpu.xr4)
        cpu.ret()
        cpu.label('magnitude_less')
        cpu.compare(cpu.r8, 0)
        if cpu.ne:
            cpu.jump('greater')
        cpu.label('less')
        cpu.r0 = 2
        cpu.pop(cpu.er8)
        cpu.pop(cpu.xr4)
        cpu.ret()
        cpu.label('magnitude_greater')
        cpu.compare(cpu.r8, 0)
        if cpu.ne:
            cpu.jump('less')
        cpu.label('greater')
        cpu.r0 = 4
        cpu.pop(cpu.er8)
        cpu.pop(cpu.xr4)
        cpu.ret()

    @fw.function(native=True)
    def graph_format():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.r10 = cpu.r2
        cpu.er0 += Y
        cpu.call('fn_graph_scalar')
        cpu.compare(cpu.r0, SUCCESS)
        if cpu.ne:
            cpu.jump('done')
        cpu.er4 = cpu.er8
        cpu.er4 += Y
        cpu.er6 = cpu.er8
        cpu.r6 += TEXT
        cpu.add_carry(cpu.r7, 0)
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.r0 = 0x30
            cpu.mem8[cpu.r10, cpu.er6] = cpu.r0
            cpu.er6 += 1
            cpu.jump('terminate')
        cpu.r11 = cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 9)]
        cpu.compare(cpu.r11, 5)
        if cpu.ge:
            cpu.r0 = 0x2D
            cpu.mem8[cpu.r10, cpu.er6] = cpu.r0
            cpu.er6 += 1
            cpu.r11 += 251
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.r0 += 0x30
        cpu.mem8[cpu.r10, cpu.er6] = cpu.r0
        cpu.er6 += 1
        cpu.r0 = 0x2E
        cpu.mem8[cpu.r10, cpu.er6] = cpu.r0
        cpu.er6 += 1
        cpu.r12 = 7
        cpu.label('digits')
        cpu.er4 += 1
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.r1 = cpu.r0
        cpu.r0 >>= 4
        cpu.r0 += 0x30
        cpu.mem8[cpu.r10, cpu.er6] = cpu.r0
        cpu.er6 += 1
        cpu.r1 &= 15
        cpu.r1 += 0x30
        cpu.mem8[cpu.r10, cpu.er6] = cpu.r1
        cpu.er6 += 1
        cpu.r12 += 255
        cpu.compare(cpu.r12, 0)
        if cpu.ne:
            cpu.branch('digits')
        cpu.r0 = 0x45
        cpu.mem8[cpu.r10, cpu.er6] = cpu.r0
        cpu.er6 += 1
        cpu.r0 = 0x2B
        cpu.compare(cpu.r11, 0)
        if cpu.eq:
            cpu.r0 = 0x2D
        cpu.mem8[cpu.r10, cpu.er6] = cpu.r0
        cpu.er6 += 1
        cpu.er4 += 1
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.r3 = cpu.r0
        cpu.r0 >>= 4
        cpu.r1 = 0
        cpu.r2 = 10
        cpu.multiply(cpu.er0, cpu.r2)
        cpu.r3 &= 15
        cpu.r0 += cpu.r3
        cpu.compare(cpu.r11, 0)
        if cpu.eq:
            cpu.er2 = 100
            cpu.r2 -= cpu.r0
            cpu.sub_carry(cpu.r3, cpu.r1)
            cpu.er0 = cpu.er2
        cpu.compare(cpu.r0, 100)
        if cpu.eq:
            cpu.r0 = 0x31
            cpu.mem8[cpu.r10, cpu.er6] = cpu.r0
            cpu.er6 += 1
            cpu.er0 = 0
        cpu.r2 = 10
        cpu.divide(cpu.er0, cpu.r2)
        cpu.r0 += 0x30
        cpu.mem8[cpu.r10, cpu.er6] = cpu.r0
        cpu.er6 += 1
        cpu.r2 += 0x30
        cpu.mem8[cpu.r10, cpu.er6] = cpu.r2
        cpu.er6 += 1
        cpu.label('terminate')
        cpu.r0 = 0
        cpu.mem8[cpu.r10, cpu.er6] = cpu.r0
        cpu.label('done')
        cpu.mem8[cpu.r10, cpu.offset(cpu.er8, STATUS)] = cpu.r0
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_calc():
        cpu.jump('fn_graph_program')

    @fw.function(native=True)
    def graph_program():
        cpu.push(cpu.lr)
        cpu.call('fn_graph_vm')
        cpu.data(PROGRAM)

    @fw.function(native=True)
    def graph_vm():
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.push(cpu.lr)
        cpu.pop(cpu.xr4)
        cpu.er8 = cpu.er0
        cpu.r10 = cpu.r2
        cpu.r11 = cpu.r6
        cpu.er12 = cpu.er4
        cpu.sp += -128
        cpu.er14 = cpu.sp
        cpu.mem16[0, cpu.er14] = cpu.er12
        cpu.er0 = cpu.er8
        cpu.er0 += X
        cpu.er4 = cpu.er8
        cpu.r4 += 160
        cpu.add_carry(cpu.r5, 0)
        cpu.r2 = cpu.r10
        cpu.r3 = 20
        cpu.r6 = cpu.r10
        cpu.call('fn_graph_copy')
        cpu.er0 = 0
        cpu.mem16[cpu.r10, cpu.offset(cpu.er8, FLAGS)] = cpu.er0
        cpu.mem16[0, cpu.offset(cpu.er14, 2)] = cpu.er0
        cpu.mem16[0, cpu.offset(cpu.er14, 4)] = cpu.er0
        cpu.er4 = cpu.er8
        cpu.r4 += 0
        cpu.add_carry(cpu.r5, 2)
        cpu.r1 = 33
        cpu.label('clear_marks')
        cpu.mem8[cpu.r10, cpu.er4] = cpu.r0
        cpu.er4 += 1
        cpu.r1 += 255
        cpu.compare(cpu.r1, 0)
        if cpu.ne:
            cpu.branch('clear_marks')
        cpu.label('next')
        cpu.call('byte')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.call('byte')
            cpu.jump('finish')
        cpu.compare(cpu.r0, 1)
        if cpu.eq:
            cpu.jump('constant')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.jump('move')
        cpu.compare(cpu.r0, 6)
        if cpu.le:
            cpu.jump('arithmetic')
        cpu.compare(cpu.r0, 8)
        if cpu.le:
            cpu.jump('sign')
        cpu.compare(cpu.r0, 9)
        if cpu.eq:
            cpu.jump('evaluate')
        cpu.compare(cpu.r0, 10)
        if cpu.eq:
            cpu.jump('compare')
        cpu.compare(cpu.r0, 11)
        if cpu.eq:
            cpu.call('word')
            cpu.jump('taken')
        cpu.compare(cpu.r0, 12)
        if cpu.eq:
            cpu.jump('call')
        cpu.compare(cpu.r0, 13)
        if cpu.eq:
            cpu.jump('return')
        cpu.compare(cpu.r0, 14)
        if cpu.eq:
            cpu.jump('get')
        cpu.compare(cpu.r0, 15)
        if cpu.eq:
            cpu.jump('put')
        cpu.compare(cpu.r0, 16)
        if cpu.eq:
            cpu.call('byte')
            cpu.mem16[cpu.r10, cpu.offset(cpu.er8, FLAGS)] = cpu.er0
            cpu.jump('next')
        cpu.compare(cpu.r0, 17)
        if cpu.eq:
            cpu.jump('set')
        cpu.compare(cpu.r0, 18)
        if cpu.eq:
            cpu.jump('increment')
        cpu.compare(cpu.r0, 19)
        if cpu.eq:
            cpu.jump('test')
        cpu.compare(cpu.r0, 20)
        if cpu.eq:
            cpu.jump('index')
        cpu.compare(cpu.r0, 21)
        if cpu.eq:
            cpu.jump('load')
        cpu.compare(cpu.r0, 22)
        if cpu.eq:
            cpu.jump('store')
        cpu.compare(cpu.r0, 23)
        if cpu.eq:
            cpu.jump('mark')
        cpu.compare(cpu.r0, 24)
        if cpu.eq:
            cpu.jump('marked')
        cpu.compare(cpu.r0, 25)
        if cpu.eq:
            cpu.jump('push_node')
        cpu.compare(cpu.r0, 26)
        if cpu.eq:
            cpu.jump('pop_node')
        cpu.compare(cpu.r0, 27)
        if cpu.eq:
            cpu.jump('depth')
        cpu.compare(cpu.r0, 28)
        if cpu.eq:
            cpu.jump('mode')
        cpu.compare(cpu.r0, 29)
        if cpu.eq:
            cpu.jump('loop')
        cpu.r0 = NATIVE_ERROR
        cpu.jump('finish')
        cpu.label('byte')
        cpu.r0 = cpu.mem8[cpu.r11, cpu.er12]
        cpu.r1 = 0
        cpu.er12 += 1
        cpu.ret()
        cpu.label('word')
        cpu.r0 = cpu.mem8[cpu.r11, cpu.er12]
        cpu.er12 += 1
        cpu.r1 = cpu.mem8[cpu.r11, cpu.er12]
        cpu.er12 += 1
        cpu.ret()
        cpu.label('slot')
        cpu.r2 = 20
        cpu.multiply(cpu.er0, cpu.r2)
        cpu.er0 += cpu.er8
        cpu.r0 += 0
        cpu.add_carry(cpu.r1, 244)
        cpu.ret()
        cpu.label('counter')
        cpu.r0 = cpu.mem8[cpu.r11, cpu.er12]
        cpu.r1 = 0
        cpu.er12 += 1
        cpu.er0 += cpu.er14
        cpu.er0 += 16
        cpu.ret()
        cpu.label('copy')
        cpu.r2 = cpu.r10
        cpu.r3 = 20
        cpu.r6 = cpu.r10
        cpu.call('fn_graph_copy')
        cpu.jump('next')
        cpu.label('constant')
        cpu.call('byte')
        cpu.call('slot')
        cpu.er4 = cpu.er0
        cpu.er0 = cpu.er12
        cpu.er12 += 10
        cpu.r2 = cpu.r11
        cpu.r3 = 10
        cpu.r6 = cpu.r10
        cpu.call('fn_graph_copy')
        cpu.er4 += 10
        cpu.r0 = 0
        cpu.r3 = 10
        cpu.label('constant_clear')
        cpu.mem8[cpu.r10, cpu.er4] = cpu.r0
        cpu.er4 += 1
        cpu.r3 += 255
        if cpu.ne:
            cpu.branch('constant_clear')
        cpu.jump('next')
        cpu.label('move')
        cpu.call('byte')
        cpu.call('slot')
        cpu.er4 = cpu.er0
        cpu.call('byte')
        cpu.call('slot')
        cpu.jump('copy')
        cpu.label('arithmetic')
        cpu.r0 += 253
        cpu.r0 <<= 4
        cpu.r0 += 0x89
        cpu.mem8[0, cpu.offset(cpu.er14, 6)] = cpu.r0
        cpu.call('byte')
        cpu.call('slot')
        cpu.mem16[0, cpu.offset(cpu.er14, 8)] = cpu.er0
        cpu.call('byte')
        cpu.call('slot')
        cpu.er4 = cpu.er0
        cpu.call('byte')
        cpu.call('slot')
        cpu.er6 = cpu.er0
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.r3 = cpu.mem8[0, cpu.offset(cpu.er14, 6)]
        cpu.call('fn_graph_arithmetic')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.jump('finish')
        cpu.er0 = cpu.er8
        cpu.er0 += Y
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, 8)]
        cpu.jump('copy')
        cpu.label('sign')
        cpu.mem8[0, cpu.offset(cpu.er14, 6)] = cpu.r0
        cpu.call('byte')
        cpu.call('slot')
        cpu.er4 = cpu.er0
        cpu.call('byte')
        cpu.call('slot')
        cpu.r2 = cpu.r10
        cpu.r3 = 20
        cpu.r6 = cpu.r10
        cpu.call('fn_graph_copy')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.jump('next')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 9)]
        cpu.compare(cpu.r0, 5)
        if cpu.ge:
            cpu.r0 += 251
        else:
            cpu.r1 = cpu.mem8[0, cpu.offset(cpu.er14, 6)]
            cpu.compare(cpu.r1, 8)
            if cpu.eq:
                cpu.r0 += 5
        cpu.mem8[cpu.r10, cpu.offset(cpu.er4, 9)] = cpu.r0
        cpu.jump('next')
        cpu.label('evaluate')
        cpu.call('byte')
        cpu.call('slot')
        cpu.mem16[0, cpu.offset(cpu.er14, 8)] = cpu.er0
        cpu.call('byte')
        cpu.call('slot')
        cpu.er4 = cpu.er8
        cpu.er4 += X
        cpu.r2 = cpu.r10
        cpu.r3 = 20
        cpu.r6 = cpu.r10
        cpu.call('fn_graph_copy')
        cpu.call('word')
        cpu.mem16[0, cpu.offset(cpu.er14, 10)] = cpu.er0
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.call('fn_graph_eval')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.jump('eval_error')
        cpu.er0 = cpu.er8
        cpu.er0 += Y
        cpu.er4 = cpu.er8
        cpu.r4 += 128
        cpu.add_carry(cpu.r5, 0)
        cpu.r2 = cpu.r10
        cpu.r3 = 20
        cpu.r6 = cpu.r10
        cpu.call('fn_graph_copy')
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r10
        cpu.call('fn_graph_eval')
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.compare(cpu.r0, UNDEFINED)
            if cpu.eq:
                cpu.er0 = cpu.er8
                cpu.r0 += 128
                cpu.add_carry(cpu.r1, 0)
                cpu.er4 = cpu.er8
                cpu.er4 += Y
                cpu.r2 = cpu.r10
                cpu.r3 = 20
                cpu.r6 = cpu.r10
                cpu.call('fn_graph_copy')
                cpu.r0 = UNSTABLE
            cpu.jump('finish')
        cpu.er4 = cpu.er8
        cpu.er4 += Y
        cpu.er6 = cpu.er8
        cpu.r6 += 128
        cpu.add_carry(cpu.r7, 0)
        cpu.call('fn_graph_compare')
        cpu.compare(cpu.r0, 1)
        if cpu.ne:
            cpu.r0 = UNSTABLE
            cpu.jump('finish')
        cpu.er0 = cpu.er8
        cpu.er0 += Y
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er14, 8)]
        cpu.jump('copy')
        cpu.label('eval_error')
        cpu.compare(cpu.r0, UNDEFINED)
        if cpu.ne:
            cpu.jump('finish')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 10)]
        cpu.jump('taken')
        cpu.label('compare')
        cpu.call('byte')
        cpu.call('slot')
        cpu.er4 = cpu.er0
        cpu.call('byte')
        cpu.call('slot')
        cpu.er6 = cpu.er0
        cpu.call('fn_graph_compare')
        cpu.mem8[0, cpu.offset(cpu.er14, 7)] = cpu.r0
        cpu.label('mask')
        cpu.call('byte')
        cpu.r1 = cpu.mem8[0, cpu.offset(cpu.er14, 7)]
        cpu.r0 &= cpu.r1
        cpu.label('conditional')
        cpu.mem8[0, cpu.offset(cpu.er14, 7)] = cpu.r0
        cpu.call('word')
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, 7)]
        cpu.compare(cpu.r2, 0)
        if cpu.eq:
            cpu.jump('next')
        cpu.label('taken')
        cpu.er12 = cpu.mem16[0, cpu.er14]
        cpu.er12 += cpu.er0
        cpu.jump('next')
        cpu.label('call')
        cpu.call('word')
        cpu.er4 = cpu.er0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 2)]
        cpu.r1 = 0
        cpu.er0 += cpu.er14
        cpu.er0 += 32
        cpu.mem16[0, cpu.er0] = cpu.er12
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 2)]
        cpu.r0 += 2
        cpu.mem8[0, cpu.offset(cpu.er14, 2)] = cpu.r0
        cpu.er0 = cpu.er4
        cpu.jump('taken')
        cpu.label('return')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 2)]
        cpu.r0 += 254
        cpu.mem8[0, cpu.offset(cpu.er14, 2)] = cpu.r0
        cpu.r1 = 0
        cpu.er0 += cpu.er14
        cpu.er0 += 32
        cpu.er12 = cpu.mem16[0, cpu.er0]
        cpu.jump('next')
        cpu.label('get')
        cpu.call('byte')
        cpu.call('slot')
        cpu.er4 = cpu.er0
        cpu.call('byte')
        cpu.er0 += cpu.er8
        cpu.jump('copy')
        cpu.label('put')
        cpu.call('byte')
        cpu.er0 += cpu.er8
        cpu.er4 = cpu.er0
        cpu.call('byte')
        cpu.call('slot')
        cpu.jump('copy')
        cpu.label('set')
        cpu.call('counter')
        cpu.er4 = cpu.er0
        cpu.call('byte')
        cpu.mem8[0, cpu.er4] = cpu.r0
        cpu.jump('next')
        cpu.label('increment')
        cpu.call('counter')
        cpu.er4 = cpu.er0
        cpu.call('byte')
        cpu.r1 = cpu.mem8[0, cpu.er4]
        cpu.r0 += cpu.r1
        cpu.mem8[0, cpu.er4] = cpu.r0
        cpu.jump('next')
        cpu.label('test')
        cpu.call('counter')
        cpu.er4 = cpu.er0
        cpu.call('byte')
        cpu.r1 = cpu.mem8[0, cpu.er4]
        cpu.compare(cpu.r1, cpu.r0)
        if cpu.eq:
            cpu.r0 = 1
        else:
            if cpu.lt:
                cpu.r0 = 2
            else:
                cpu.r0 = 4
        cpu.mem8[0, cpu.offset(cpu.er14, 7)] = cpu.r0
        cpu.jump('mask')
        cpu.label('index')
        cpu.call('counter')
        cpu.er4 = cpu.er0
        cpu.call('counter')
        cpu.r0 = cpu.mem8[0, cpu.er0]
        cpu.mem8[0, cpu.er4] = cpu.r0
        cpu.jump('next')
        cpu.label('indexed_slot')
        cpu.push(cpu.lr)
        cpu.call('byte')
        cpu.mem8[0, cpu.offset(cpu.er14, 6)] = cpu.r0
        cpu.call('counter')
        cpu.r0 = cpu.mem8[0, cpu.er0]
        cpu.r1 = cpu.mem8[0, cpu.offset(cpu.er14, 6)]
        cpu.r0 += cpu.r1
        cpu.r1 = 0
        cpu.call('slot')
        cpu.pop(cpu.pc)
        cpu.label('load')
        cpu.call('byte')
        cpu.call('slot')
        cpu.er4 = cpu.er0
        cpu.call('indexed_slot')
        cpu.jump('copy')
        cpu.label('store')
        cpu.call('indexed_slot')
        cpu.er4 = cpu.er0
        cpu.call('byte')
        cpu.call('slot')
        cpu.jump('copy')
        cpu.label('mark_address')
        cpu.push(cpu.lr)
        cpu.call('counter')
        cpu.r0 = cpu.mem8[0, cpu.er0]
        cpu.r1 = 0
        cpu.er0 += cpu.er8
        cpu.r0 += 0
        cpu.add_carry(cpu.r1, 2)
        cpu.er4 = cpu.er0
        cpu.pop(cpu.pc)
        cpu.label('mark')
        cpu.call('mark_address')
        cpu.call('byte')
        cpu.r1 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.r0 |= cpu.r1
        cpu.mem8[cpu.r10, cpu.er4] = cpu.r0
        cpu.jump('next')
        cpu.label('marked')
        cpu.call('mark_address')
        cpu.call('byte')
        cpu.r1 = cpu.mem8[cpu.r10, cpu.er4]
        cpu.r0 &= cpu.r1
        cpu.jump('conditional')
        cpu.label('node_address')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 4)]
        cpu.r1 = 0
        cpu.r2 = 144
        cpu.multiply(cpu.er0, cpu.r2)
        cpu.er0 += cpu.er8
        cpu.r0 += 112
        cpu.add_carry(cpu.r1, 246)
        cpu.ret()
        cpu.label('push_node')
        cpu.call('node_address')
        cpu.er4 = cpu.er0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 3)]
        cpu.r1 = 0
        cpu.mem16[cpu.r10, cpu.offset(cpu.er4, 140)] = cpu.er0
        cpu.er0 = 0
        cpu.mem16[cpu.r10, cpu.offset(cpu.er4, 142)] = cpu.er0
        cpu.er0 = cpu.er8
        cpu.r0 += 0
        cpu.add_carry(cpu.r1, 244)
        cpu.r2 = cpu.r10
        cpu.r3 = 140
        cpu.r6 = cpu.r10
        cpu.call('fn_graph_copy')
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 4)]
        cpu.r0 += 1
        cpu.mem8[0, cpu.offset(cpu.er14, 4)] = cpu.r0
        cpu.jump('next')
        cpu.label('pop_node')
        cpu.call('word')
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, 4)]
        cpu.compare(cpu.r2, 0)
        if cpu.eq:
            cpu.jump('taken')
        cpu.r2 += 255
        cpu.mem8[0, cpu.offset(cpu.er14, 4)] = cpu.r2
        cpu.call('node_address')
        cpu.r3 = cpu.mem8[cpu.r10, cpu.offset(cpu.er0, 140)]
        cpu.mem8[0, cpu.offset(cpu.er14, 3)] = cpu.r3
        cpu.er4 = cpu.er8
        cpu.r4 += 0
        cpu.add_carry(cpu.r5, 244)
        cpu.r2 = cpu.r10
        cpu.r3 = 140
        cpu.r6 = cpu.r10
        cpu.call('fn_graph_copy')
        cpu.jump('next')
        cpu.label('depth')
        cpu.call('byte')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.mem8[0, cpu.offset(cpu.er14, 3)] = cpu.r0
            cpu.mem8[0, cpu.offset(cpu.er14, 4)] = cpu.r0
            cpu.jump('next')
        cpu.compare(cpu.r0, 1)
        if cpu.eq:
            cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 3)]
            cpu.r0 += 1
            cpu.mem8[0, cpu.offset(cpu.er14, 3)] = cpu.r0
            cpu.jump('next')
        cpu.call('word')
        cpu.r2 = cpu.mem8[0, cpu.offset(cpu.er14, 3)]
        cpu.compare(cpu.r2, 16)
        if cpu.ge:
            cpu.jump('taken')
        cpu.jump('next')
        cpu.label('mode')
        cpu.call('byte')
        cpu.r1 = cpu.mem8[cpu.r10, cpu.offset(cpu.er8, OPERATION)]
        cpu.compare(cpu.r0, cpu.r1)
        if cpu.eq:
            cpu.r0 = 1
        else:
            cpu.r0 = 0
        cpu.jump('conditional')
        cpu.label('loop')
        cpu.call('counter')
        cpu.er4 = cpu.er0
        cpu.r0 = cpu.mem8[0, cpu.er4]
        cpu.r0 += 255
        cpu.mem8[0, cpu.er4] = cpu.r0
        cpu.jump('conditional')
        cpu.label('finish')
        cpu.mem8[cpu.r10, cpu.offset(cpu.er8, STATUS)] = cpu.r0
        cpu.r1 = cpu.mem8[cpu.r10, cpu.offset(cpu.er8, OPERATION)]
        cpu.compare(cpu.r1, 5)
        if cpu.eq:
            cpu.er0 = cpu.er8
            cpu.r0 += 160
            cpu.add_carry(cpu.r1, 0)
            cpu.er4 = cpu.er8
            cpu.er4 += X
            cpu.r2 = cpu.r10
            cpu.r3 = 20
            cpu.r6 = cpu.r10
            cpu.call('fn_graph_copy')
        cpu.r0 = cpu.mem8[cpu.r10, cpu.offset(cpu.er8, STATUS)]
        cpu.sp += 64
        cpu.sp += 64
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_cancel():
        # ROM12864 returns KI and KO masks without entering the key wait loop.
        # EXIT is KI bit 6, KO bit 2 (ROM591/5DA physical-key tables).
        cpu.push(cpu.lr)
        cpu.push(cpu.er14)
        cpu.sp += -4
        cpu.er14 = cpu.sp
        cpu.er0 = 0
        cpu.mem16[0, cpu.er14] = cpu.er0
        cpu.r0 = cpu.psw
        cpu.mem8[0, cpu.offset(cpu.er14, 2)] = cpu.r0
        cpu.r0 &= 0xF7
        cpu.psw = cpu.r0
        cpu.r0 = cpu.mem8[0, 0xF044]
        cpu.mem8[0, cpu.offset(cpu.er14, 3)] = cpu.r0
        cpu.er0 = cpu.er14
        cpu.call(0x12864)
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 3)]
        cpu.mem8[0, 0xF044] = cpu.r0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 2)]
        cpu.psw = cpu.r0
        cpu.er2 = cpu.mem16[0, cpu.er14]
        cpu.r0 = 0
        cpu.compare(cpu.r3, 4)
        if cpu.eq:
            cpu.r2 &= 0x40
            if cpu.ne:
                cpu.r0 = 1
        cpu.sp += 4
        cpu.pop(cpu.er14)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_normalize():
        # ER0/R2 addresses native20. ROM145C8 materializes the exact real
        # component in place; the imaginary component still undergoes the
        # scalar check. Preserve math state for callers outside graph_native.
        cpu.push(cpu.lr)
        cpu.push(cpu.qr0)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.r10 = cpu.r2
        cpu.sp += -128
        cpu.sp += -128
        cpu.sp += -128
        cpu.sp += -72
        cpu.er14 = cpu.sp
        cpu.er4 = cpu.er14
        cpu.r6 = 0
        cpu.r3 = 20
        cpu.call('fn_graph_copy')
        cpu.er0 = cpu.mem16[0, 0x8086]
        cpu.mem16[0, cpu.offset(cpu.er14, 20)] = cpu.er0
        cpu.er0 = 0x8000
        cpu.r2 = 0
        cpu.r3 = 112
        cpu.er4 = cpu.er14
        cpu.r4 += 88
        cpu.add_carry(cpu.r5, 1)
        cpu.call('fn_graph_copy')
        cpu.er0 = cpu.er14
        cpu.er0 += 24
        cpu.mem16[0, 0x8086] = cpu.er0
        cpu.er6 = cpu.er0
        cpu.er4 = 320
        cpu.er2 = 0
        cpu.r0 = 0
        cpu.label('clear_workspace')
        cpu.mem8[0, cpu.er6] = cpu.r0
        cpu.er6 += 1
        cpu.er4 += -1
        cpu.compare(cpu.er4, cpu.er2)
        if cpu.ne:
            cpu.branch('clear_workspace')
        cpu.er0 = cpu.er14
        cpu.call(0x145C8)
        cpu.er0 = cpu.er14
        cpu.r2 = 0
        cpu.r3 = 20
        cpu.er4 = cpu.er8
        cpu.r6 = cpu.r10
        cpu.call('fn_graph_copy')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 20)]
        cpu.mem16[0, 0x8086] = cpu.er0
        cpu.er0 = cpu.er14
        cpu.r0 += 88
        cpu.add_carry(cpu.r1, 1)
        cpu.r2 = 0
        cpu.r3 = 112
        cpu.er4 = 0x8000
        cpu.r6 = 0
        cpu.call('fn_graph_copy')
        cpu.sp += 120
        cpu.sp += 120
        cpu.sp += 120
        cpu.sp += 96
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.qr0)
        cpu.pop(cpu.pc)
