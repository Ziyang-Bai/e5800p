"""Compile physical-register Python without a frame or implicit return.

Operations have nX-U8 width and PSW semantics, not Python integer semantics.
Compare/test update flags without assigning the operand; carry arithmetic and
carry shifts consume the current carry. No flags are saved or normalized.
MOV ER,# may use two byte MOVs, as in the assembler, so its final flags are
those of the last MOV. Other arithmetic maps directly to its named instruction;
SUB immediate macros are excluded because they would use a hidden stack slot.
Memory prefixes, LEA, calls and stack operations likewise retain ISA semantics.

An if containing only cpu.branch emits exactly one short conditional branch.
Structured if/while use short branches where the target is reachable.
Only explicit return/cpu.ret/cpu.pop(cpu.pc) returns; fallthrough is intentional.
"""

import ast
import inspect
import operator
import re
import textwrap

from nxu8_asm import assemble

from .model import cpu


_CONDITIONS = {name.lower(): 'B' + name for name in
               ('EQ', 'NE', 'LT', 'GE', 'GT', 'LE', 'LTS', 'GES', 'GTS', 'LES',
                'OV', 'NV', 'PS', 'NS')}
_INVERSE = dict(zip(('BEQ', 'BNE', 'BLT', 'BGE', 'BGT', 'BLE', 'BLTS', 'BGES',
                     'BGTS', 'BLES', 'BOV', 'BNV', 'BPS', 'BNS'),
                    ('BNE', 'BEQ', 'BGE', 'BLT', 'BLE', 'BGT', 'BGES', 'BLTS',
                     'BLES', 'BGTS', 'BNV', 'BOV', 'BNS', 'BPS')))
_BINARY = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
           ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
           ast.BitAnd: operator.and_, ast.BitOr: operator.or_, ast.BitXor: operator.xor,
           ast.LShift: operator.lshift, ast.RShift: operator.rshift}
_AUGMENT = {ast.Add: 'ADD', ast.Sub: 'SUB', ast.BitAnd: 'AND', ast.BitOr: 'OR',
            ast.BitXor: 'XOR', ast.LShift: 'SLL', ast.RShift: 'SRL'}
_ZERO = {'ret': 'RET', 'rti': 'RTI', 'nop': 'NOP',
         'enable_interrupts': 'EI', 'disable_interrupts': 'DI',
         'set_carry': 'SC', 'clear_carry': 'RC', 'complement_carry': 'CPLC',
         'increment': 'INC [EA]', 'decrement': 'DEC [EA]'}
_ONE = {'push': 'PUSH', 'pop': 'POP', 'negate': 'NEG', 'extend': 'EXTBW',
        'decimal_adjust_add': 'DAA', 'decimal_adjust_sub': 'DAS'}
_TWO = {'compare': 'CMP', 'compare_carry': 'CMPC', 'add_carry': 'ADDC',
        'sub_carry': 'SUBC', 'multiply': 'MUL', 'divide': 'DIV',
        'shift_left_carry': 'SLLC', 'shift_right_carry': 'SRLC',
        'shift_right_signed': 'SRA'}
_BITS = {'test_bit': 'TB', 'set_bit': 'SB', 'reset_bit': 'RB'}
_SYMBOL = re.compile(r'[A-Za-z_][A-Za-z_0-9]*\Z')


class _NativeCompiler:
    def __init__(self, function, origin, addresses):
        self.function = function
        self.origin = origin
        self.addresses = addresses
        self.filename = inspect.getsourcefile(function.fn) or '<unknown>'
        try:
            lines, self.first_line = inspect.getsourcelines(function.fn)
        except (OSError, TypeError) as exc:
            raise ValueError(f'{self.filename}:1: Python source is unavailable: {exc}') from None
        try:
            tree = ast.parse(textwrap.dedent(''.join(lines)))
        except SyntaxError as exc:
            raise ValueError(f'{self.filename}:{self.first_line + exc.lineno - 1}: {exc.msg}') from None
        self.node = next((node for node in tree.body if isinstance(node, ast.FunctionDef)), None)
        if self.node is None:
            self.fail(tree, 'expected an ordinary Python function')
        self.globals = dict(function.fn.__globals__)
        self.globals.update(inspect.getclosurevars(function.fn).nonlocals)
        self.lines = []
        self.locations = []
        self.current = self.node
        self.counter = 0
        self.loops = []
        self.short_jumps = []
        # Reserve source labels before introducing structural control-flow labels.
        self.labels = set()
        for node in ast.walk(self.node):
            if isinstance(node, ast.Call) and self.cpu_name(node.func) == 'label':
                self.arity(node, 1)
                self.labels.add(self.label_name(node.args[0]).upper())
        self.user_labels = {self.label_name(node.args[0])
                            for node in ast.walk(self.node)
                            if isinstance(node, ast.Call)
                            and self.cpu_name(node.func) == 'label'}

    def fail(self, node, message):
        line = self.first_line + getattr(node, 'lineno', 1) - 1
        raise ValueError(f'{self.filename}:{line}: {message}')

    def emit(self, *lines):
        self.lines.extend(lines)
        self.locations.extend([self.current] * len(lines))

    def cpu_name(self, node):
        if (isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name)
                and self.globals.get(node.value.id) is cpu):
            return node.attr
        return None

    def constant(self, node):
        if isinstance(node, ast.Constant):
            value = node.value
        elif isinstance(node, ast.Name) and node.id in self.globals:
            value = self.globals[node.id]
        elif isinstance(node, (ast.Tuple, ast.List)):
            value = tuple(self.constant(item) for item in node.elts)
        elif isinstance(node, ast.Call) and self.cpu_name(node.func) == 'address':
            self.arity(node, 1)
            symbol = self.label_name(node.args[0])
            value = self.addresses.get(symbol)
            if type(value) is not int:
                self.fail(node, 'unlinked code address: ' + symbol)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub, ast.Invert)):
            value = self.integer(node.operand)
            value = +value if isinstance(node.op, ast.UAdd) else -value if isinstance(node.op, ast.USub) else ~value
        elif isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
            left, right = self.integer(node.left), self.integer(node.right)
            if isinstance(node.op, (ast.LShift, ast.RShift)) and not 0 <= right <= 63:
                self.fail(node, 'constant shift count must be 0..63')
            try:
                value = _BINARY[type(node.op)](left, right)
            except ArithmeticError as exc:
                self.fail(node, str(exc))
        else:
            self.fail(node, 'expected a literal or named constant; host calls are not executed')
        if type(value) not in (int, str, bytes, tuple, list):
            self.fail(node, 'expected an integer, label or constant data')
        return value

    def integer(self, node):
        value = self.constant(node)
        if type(value) is not int:
            self.fail(node, 'expected an integer constant')
        return value

    def register(self, node, required=True):
        name = self.cpu_name(node)
        if name in ('sp', 'ea', 'lr', 'pc', 'psw', 'bp', 'fp', 'dsr'):
            return name.upper()
        match = re.fullmatch(r'(r|er|xr|qr)(\d+)', name or '')
        if match:
            index = int(match[2])
            width = {'r': 1, 'er': 2, 'xr': 4, 'qr': 8}[match[1]]
            if index > 16 - width or index % width:
                self.fail(node, f'invalid register: cpu.{name}')
            return name.upper()
        if required:
            self.fail(node, 'expected a physical CPU register')
        return None

    def immediate(self, node):
        value = self.integer(node)
        # Positive signed-field values may specify the raw field, as in the ISA.
        return hex(value) if value >= 0 else str(value)

    def operand(self, node):
        register = self.register(node, required=False)
        return register if register else '#' + self.immediate(node)

    def arity(self, node, count):
        if len(node.args) != count or node.keywords:
            self.fail(node, f'CPU operation requires {count} positional argument(s)')

    def label_name(self, node):
        value = self.constant(node)
        if type(value) is not str or not _SYMBOL.fullmatch(value):
            self.fail(node, 'label must be an identifier string')
        return value

    def target(self, node, relative=False):
        register = self.register(node, required=False)
        if register:
            if relative or not register.startswith('ER'):
                self.fail(node, 'indirect call/jump requires an ER register')
            return register
        value = self.constant(node)
        if type(value) is str:
            if _SYMBOL.fullmatch(value):
                if value.upper() in self.labels:
                    return value
                external = self.globals.get(value, self.addresses.get(value))
                if type(external) is int:
                    value = external
                else:
                    return value
            elif re.fullmatch(r'0[xX][0-9a-fA-F]+|[0-9]+', value):
                value = int(value, 16 if value.lower().startswith('0x') else 10)
            else:
                self.fail(node, 'target must be an identifier or full integer address')
        if type(value) is not int or not 0 <= value <= 0xfffff or value & 1:
            self.fail(node, 'target must be an even 20-bit code address')
        if value >> 16 not in (0, 1, 8, 9, 10, 11, 12, 13, 14, 15):
            self.fail(node, 'target must be in ROM or Flash')
        # Explicit segment prevents the assembler treating a ROM0 address as local.
        return f'{value >> 16}:{hex(value & 65535)}'

    def address(self, node):
        register = self.register(node, required=False)
        if register:
            if not (register.startswith('ER') or register in ('EA', 'BP', 'FP')):
                self.fail(node, 'memory address requires ER, EA, BP or FP')
            return f'[{register}]'
        if isinstance(node, ast.Call):
            name = self.cpu_name(node.func)
            if name == 'post':
                self.arity(node, 1)
                if self.register(node.args[0]) != 'EA':
                    self.fail(node, 'post-increment requires EA')
                return '[EA+]'
            if name == 'offset':
                self.arity(node, 2)
                base = self.register(node.args[0])
                if not (base.startswith('ER') or base in ('BP', 'FP')):
                    self.fail(node, 'displacement requires ER, BP or FP')
                return f'{self.immediate(node.args[1])}[{base}]'
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub)):
            left = self.register(node.left, required=False)
            right = self.register(node.right, required=False)
            if left or right:
                base = left or right
                if not (base.startswith('ER') or base in ('BP', 'FP')) or (right and isinstance(node.op, ast.Sub)):
                    self.fail(node, 'address requires register + displacement or register - displacement')
                displacement = self.integer(node.right if left else node.left)
                if isinstance(node.op, ast.Sub):
                    displacement = -displacement
                text = hex(displacement) if displacement >= 0 else str(displacement)
                return f'{text}[{base}]'
        value = self.constant(node)
        if type(value) is str:
            label = self.label_name(node)
            external = self.globals.get(label, self.addresses.get(label))
            if label.upper() not in self.labels and type(external) is int:
                value = external
            else:
                # A local data label denotes its bank-local offset.
                return f'{label}-{hex(self.origin & 0xf0000)}'
        if type(value) is not int:
            self.fail(node, 'memory address must be an integer or label')
        return hex(value) if value >= 0 else str(value)

    def memory(self, node):
        if not isinstance(node, ast.Subscript):
            return None
        name = self.cpu_name(node.value)
        if name not in ('mem8', 'mem16', 'mem32', 'mem64'):
            self.fail(node, 'expected cpu.mem8/mem16/mem32/mem64')
        address, prefix = node.slice, ''
        if isinstance(address, ast.Tuple):
            if len(address.elts) != 2:
                self.fail(node, 'banked memory requires (bank, address)')
            bank, address = address.elts
            register = self.register(bank, required=False)
            if register:
                if register != 'DSR' and not re.fullmatch(r'R\d+', register):
                    self.fail(bank, 'memory bank requires a byte register, cpu.dsr or integer')
                prefix = register + ':'
            else:
                prefix = self.immediate(bank) + ':'
        return int(name[3:]), prefix + self.address(address)

    def memory_register(self, node, width):
        register = self.register(node)
        prefix = {8: 'R', 16: 'ER', 32: 'XR', 64: 'QR'}[width]
        if not re.fullmatch(prefix + r'\d+', register):
            self.fail(node, f'mem{width} requires a {prefix} register')
        return register

    def assign(self, target, value):
        memory = self.memory(target)
        if memory:
            width, address = memory
            self.emit(f'ST {self.memory_register(value, width)},{address}')
            return
        register = self.register(target)
        memory = self.memory(value)
        if memory:
            width, address = memory
            self.memory_register(target, width)
            self.emit(f'L {register},{address}')
        elif register == 'EA':
            if isinstance(value, ast.Call) and self.cpu_name(value.func) == 'address':
                self.arity(value, 1)
                value = value.args[0]
            self.emit('LEA ' + self.address(value))
        elif isinstance(value, ast.UnaryOp) and isinstance(value.op, ast.USub) and self.register(value.operand, required=False):
            if self.register(value.operand) != register:
                self.fail(value, 'negation must assign the same physical register')
            self.emit('NEG ' + register)
        elif register.startswith('ER') and any(
                isinstance(node, ast.Call) and self.cpu_name(node.func) == 'address'
                for node in ast.walk(value)):
            # Symbolic word immediates must keep their width during placement.
            immediate = self.integer(value)
            if not 0 <= immediate <= 65535:
                self.fail(value, 'word immediate outside 0..65535')
            index = int(register[2:])
            self.emit(f'MOV R{index},#{hex(immediate & 255)}',
                      f'MOV R{index + 1},#{hex(immediate >> 8)}')
        else:
            self.emit(f'MOV {register},{self.operand(value)}')

    def operation(self, node):
        name = self.cpu_name(node.func)
        if name in _ZERO:
            self.arity(node, 0)
            self.emit(_ZERO[name])
        elif name in _ONE:
            self.arity(node, 1)
            self.emit(f'{_ONE[name]} {self.register(node.args[0])}')
        elif name in _TWO:
            self.arity(node, 2)
            self.emit(f'{_TWO[name]} {self.register(node.args[0])},{self.operand(node.args[1])}')
        elif name in _BITS:
            self.arity(node, 2)
            self.emit(f'{_BITS[name]} {self.register(node.args[0])}.{self.immediate(node.args[1])}')
        elif name in ('call', 'jump', 'branch'):
            self.arity(node, 1)
            mnemonic = {'call': 'CALL', 'jump': 'JMP', 'branch': 'BAL'}[name]
            self.emit(f'{mnemonic} {self.target(node.args[0], name == "branch")}')
        elif name == 'label':
            self.arity(node, 1)
            self.emit(self.label_name(node.args[0]) + ':')
        elif name == 'data':
            self.arity(node, 1)
            value = self.constant(node.args[0])
            if type(value) is str:
                try:
                    value = value.encode('ascii')
                except UnicodeEncodeError:
                    self.fail(node, 'data strings must be ASCII')
            if type(value) not in (bytes, tuple, list) or any(type(item) is not int or not 0 <= item <= 255 for item in value):
                self.fail(node, 'data requires constant bytes or a sequence of bytes')
            for start in range(0, len(value), 32):
                self.emit('DB ' + ','.join(hex(item) for item in value[start:start + 32]))
        else:
            self.fail(node, 'unknown CPU operation; native bodies cannot execute host calls')

    def label(self):
        while True:
            self.counter += 1
            name = f'_native_{self.counter}'
            if name.upper() not in self.labels:
                self.labels.add(name.upper())
                return name

    def condition(self, node):
        name = self.cpu_name(node)
        if name in _CONDITIONS:
            return _CONDITIONS[name]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return _INVERSE[self.condition(node.operand)]
        self.fail(node, 'native condition must test CPU flags (for example cpu.eq)')

    def conditional_jump(self, condition, target):
        skip = self.label()
        self.short_jumps.append(len(self.lines))
        self.emit(f'{_INVERSE[condition]} {skip}', f'JMP {target}', skip + ':')

    def block(self, statements):
        for node in statements:
            self.current = node
            if isinstance(node, ast.Assign):
                if len(node.targets) != 1:
                    self.fail(node, 'native assignment requires one physical destination')
                self.assign(node.targets[0], node.value)
            elif isinstance(node, ast.AugAssign):
                mnemonic = _AUGMENT.get(type(node.op))
                if mnemonic is None:
                    self.fail(node, 'unsupported native augmented operator')
                register = self.register(node.target)
                operand = self.operand(node.value)
                if mnemonic == 'SUB' and operand.startswith('#'):
                    self.fail(node, 'SUB immediate needs hidden stack storage; use explicit CPU operations')
                self.emit(f'{mnemonic} {register},{operand}')
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                self.operation(node.value)
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and type(node.value.value) is str:
                if node is not self.node.body[0]:
                    self.fail(node, 'only the function docstring may be a string statement')
            elif isinstance(node, ast.If):
                condition = self.condition(node.test)
                branch = node.body[0] if len(node.body) == 1 else None
                if (not node.orelse and isinstance(branch, ast.Expr)
                        and isinstance(branch.value, ast.Call)
                        and self.cpu_name(branch.value.func) == 'branch'):
                    self.current = branch
                    self.arity(branch.value, 1)
                    self.emit(f'{condition} {self.target(branch.value.args[0], True)}')
                    continue
                if (not node.orelse and isinstance(branch, ast.Expr)
                        and isinstance(branch.value, ast.Call)
                        and self.cpu_name(branch.value.func) == 'jump'):
                    self.arity(branch.value, 1)
                    self.conditional_jump(condition, self.target(branch.value.args[0]))
                    continue
                other, done = self.label(), self.label()
                self.conditional_jump(_INVERSE[condition], other)
                self.block(node.body)
                self.current = node
                if node.orelse:
                    self.emit('JMP ' + done)
                self.emit(other + ':')
                self.block(node.orelse)
                if node.orelse:
                    self.emit(done + ':')
            elif isinstance(node, ast.While):
                if node.orelse:
                    self.fail(node, 'native while-else is not supported')
                condition = self.condition(node.test)
                begin, done = self.label(), self.label()
                self.emit(begin + ':')
                self.conditional_jump(_INVERSE[condition], done)
                self.loops.append((begin, done))
                self.block(node.body)
                self.loops.pop()
                self.current = node
                self.emit('JMP ' + begin, done + ':')
            elif isinstance(node, (ast.Break, ast.Continue)):
                if not self.loops:
                    self.fail(node, 'break/continue requires a native while loop')
                self.emit('JMP ' + self.loops[-1][isinstance(node, ast.Break)])
            elif isinstance(node, ast.Return):
                if node.value is not None:
                    self.fail(node, 'native return has no value; assign result registers explicitly')
                self.emit('RET')
            elif not isinstance(node, ast.Pass):
                self.fail(node, f'unsupported native statement: {type(node).__name__}')

    def compile(self):
        args = self.node.args
        if args.posonlyargs or args.args or args.kwonlyargs or args.vararg or args.kwarg:
            self.fail(self.node, 'native functions must be parameterless')
        if (type(self.origin) is not int or self.origin & 1 or not 0 <= self.origin <= 0xfffff
                or self.origin >> 16 not in (0, 1, 8, 9, 10, 11, 12, 13, 14, 15)):
            self.fail(self.node, 'origin must be an even ROM/Flash code address')
        self.block(self.node.body)
        # Unprefixed memory uses bank 0, but leaves lastDSR unchanged.
        # Keep the first #0 prefix in each block to preserve DSR reads.
        zero_dsr = False
        for index, line in enumerate(self.lines):
            memory = re.match(r'((?:L|ST) \w+,)(#[^:]+|R\d+|DSR):(.*)\Z', line)
            if memory:
                prefix = memory[2]
                if prefix == '#0x0':
                    if zero_dsr:
                        self.lines[index] = memory[1] + memory[3]
                    zero_dsr = True
                else:
                    zero_dsr = False
            elif (line.endswith(':') or line.split()[0] in
                  {'CALL', 'JMP', 'BAL', 'RET', 'RTI', 'DB', *_INVERSE}
                  or 'DSR' in line or line == 'POP PC'):
                zero_dsr = False
        try:
            while True:
                source = '\n'.join(self.lines) + '\n'
                data, symbols, listing = assemble(source, self.origin)
                at = {row['line'] - 1: row['address'] for row in listing}
                shorten = set()
                for index in self.short_jumps:
                    target = symbols.get(self.lines[index + 1][4:].upper())
                    if target is not None and -256 <= target - at[index] - 2 <= 254:
                        shorten.add(index)
                inherited = set()
                for index in range(len(self.lines) - 2):
                    parts = self.lines[index].split()
                    if (len(parts) != 2 or parts[0] not in _INVERSE
                            or index in self.short_jumps or at[index] - self.origin < 16
                            or self.lines[index + 2].upper() != parts[1].upper() + ':'
                            or not self.lines[index + 1].startswith(('JMP ', 'BAL '))):
                        continue
                    target = symbols.get(self.lines[index + 1][4:].upper())
                    if target is not None and -256 <= target - at[index] - 2 <= 254:
                        inherited.add(index)
                long_conditionals = {index + 1 for index in self.short_jumps}
                short_unconditional = set()
                # Keep published entry jump-table slots at offsets 0, 4, 8 and 12.
                for index, line in enumerate(self.lines):
                    if (not line.startswith('JMP ') or index in long_conditionals
                            or at[index] - self.origin < 16):
                        continue
                    target = symbols.get(line[4:].upper())
                    if target is not None and -256 <= target - at[index] - 2 <= 254:
                        short_unconditional.add(index)
                if not shorten and not inherited and not short_unconditional:
                    break
                lines, locations, pending = [], [], []
                removed = {index + step for index in shorten for step in (1, 2)}
                # Source labels may be external entries, so retain them.
                removed.update(index + 1 for index in inherited)
                for index, line in enumerate(self.lines):
                    if index in removed:
                        continue
                    if index in shorten or index in inherited:
                        condition = _INVERSE[line.split()[0]]
                        line = condition + ' ' + self.lines[index + 1][4:]
                    elif index in self.short_jumps:
                        pending.append(len(lines))
                    elif index in short_unconditional:
                        line = 'BAL ' + line[4:]
                    lines.append(line)
                    locations.append(self.locations[index])
                self.lines, self.locations, self.short_jumps = lines, locations, pending
        except ValueError as exc:
            match = re.match(r'line (\d+): (.*)', str(exc))
            if match:
                self.fail(self.locations[int(match[1]) - 1], match[2])
            self.fail(self.node, str(exc))
        if (self.origin & 65535) + len(data) > 65536:
            self.fail(self.node, 'function crosses a code bank boundary')
        self.symbols = {self.function.symbol + '__' + label: symbols[label.upper()]
                        for label in self.user_labels}
        return data, source


def compile_native(function, origin, addresses):
    """Return machine bytes and assembly with Python-source-linked errors."""
    return _NativeCompiler(function, origin, addresses).compile()
