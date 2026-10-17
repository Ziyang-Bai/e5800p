"""Compile the integer firmware subset of Python to nX-U8 assembly.

Locals are word slots below ER14. Expressions return ER0 and use the stack
for live operands; no Python body or user descriptor is executed by compilation.
"""

import ast
import inspect
import re
import textwrap

from nxu8_asm import assemble

from .model import Buffer, Function, Integer, Memory, ROM, u8, u16


_INVERSE = {'BEQ': 'BNE', 'BNE': 'BEQ', 'BLT': 'BGE', 'BGE': 'BLT',
            'BGT': 'BLE', 'BLE': 'BGT'}
_COMPARE = {ast.Eq: 'BEQ', ast.NotEq: 'BNE', ast.Lt: 'BLT',
            ast.LtE: 'BLE', ast.Gt: 'BGT', ast.GtE: 'BGE'}
_MISSING = object()


class _Compiler:
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
        closure = inspect.getclosurevars(function.fn)
        self.globals.update(closure.nonlocals)
        self.globals[function.name] = function
        self.lines = []
        self.locations = []
        self.current = self.node
        self.counter = 0
        self.slots = {}
        self.types = {}
        self.loops = []
        self.range_slots = {}
        self.params, self.result = self.signature(function, self.node)
        for name, dtype, default in self.params:
            self.slot(name)
            self.types[name] = dtype
        # Allocate once, including hidden range state. A local name shadows globals
        # throughout the body, even before its first assignment.
        for node in ast.walk(self.node):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                self.slot(node.id)
            if isinstance(node, ast.AnnAssign):
                if not isinstance(node.target, ast.Name):
                    self.fail(node, 'annotations require a local variable')
                dtype = self.annotation(node.annotation, node)
                if dtype is None:
                    self.fail(node, 'local variables must be u8 or u16')
                old = self.types.get(node.target.id)
                if old is not None and old is not dtype:
                    self.fail(node, 'conflicting local integer annotations')
                self.types[node.target.id] = dtype
            if isinstance(node, ast.For):
                self.range_slots[id(node)] = (self.slot(('range', id(node))),
                                              self.slot(('stop', id(node))))
        if len(self.slots) * 2 > 32768:
            self.fail(self.node, 'local frame exceeds signed 16-bit displacement')
        self.exit = self.label('return')

    def fail(self, node, message):
        line = self.first_line + getattr(node, 'lineno', 1) - 1
        raise ValueError(f'{self.filename}:{line}: {message}')

    def annotation(self, value, node):
        if isinstance(value, ast.Constant):
            value = value.value
        elif isinstance(value, (ast.Name, ast.Attribute)):
            value = self.object(value)
        if value is inspect.Signature.empty or value is u16 or (type(value) is str and value == 'u16'):
            return u16
        if value is u8 or (type(value) is str and value == 'u8'):
            return u8
        if value is None or (type(value) is str and value in ('None', 'NoneType')):
            return None
        self.fail(node, 'annotation must be u8, u16 or None')

    def signature(self, function, node):
        signature = inspect.signature(function.fn, eval_str=False)
        params = []
        for param in signature.parameters.values():
            if param.kind not in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):
                self.fail(node, 'only positional integer parameters are supported')
            dtype = self.annotation(param.annotation, node)
            if dtype is None:
                self.fail(node, 'parameter must be u8 or u16')
            default = param.default
            if default is not inspect.Signature.empty and type(default) not in (int, bool):
                self.fail(node, 'parameter defaults must be integer constants')
            params.append((param.name, dtype, default))
        if len(params) > 4:
            self.fail(node, 'at most four integer parameters are supported')
        return params, self.annotation(signature.return_annotation, node)

    def slot(self, name):
        if name not in self.slots:
            self.slots[name] = -2 * (len(self.slots) + 1)
        return self.slots[name]

    def emit(self, *lines):
        self.lines.extend(lines)
        self.locations.extend([self.current] * len(lines))

    def label(self, name):
        self.counter += 1
        return f'_{name}_{self.counter}'

    def mark(self, label):
        self.emit(label + ':')

    def jump(self, label):
        self.emit('JMP ' + label)

    def branch(self, condition, label):
        # Only this two-word skip uses the limited relative branch encoding.
        skip = self.label('skip')
        self.emit(f'{_INVERSE[condition]} {skip}', f'JMP {label}')
        self.mark(skip)

    def immediate(self, value, reg=0):
        self.emit(f'MOV ER{reg},#{value & 65535}')

    def load(self, slot, reg=0):
        self.emit(f'L ER{reg},0:{slot}[ER14]')

    def store(self, slot, reg=0):
        self.emit(f'ST ER{reg},0:{slot}[ER14]')

    def object(self, node):
        if isinstance(node, ast.Name):
            if node.id in self.slots:
                self.fail(node, 'local value is not a compile-time object')
            if node.id in self.globals:
                return self.globals[node.id]
            builtins = {'len': len, 'range': range, 'u8': u8, 'u16': u16}
            if node.id in builtins:
                return builtins[node.id]
        elif isinstance(node, ast.Attribute):
            owner = self.object(node.value)
            if isinstance(owner, type) and issubclass(owner, Memory):
                for cls in owner.__mro__:
                    if node.attr in vars(cls):
                        value = vars(cls)[node.attr]
                        if isinstance(value, (Buffer, ROM, Function, Integer)) or type(value) in (int, bool):
                            return value
                        break
        self.fail(node, 'expected a constant, Buffer, ROM or decorated function')

    def constant(self, node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, bool):
            return int(node.value)
        if isinstance(node, (ast.Name, ast.Attribute)):
            if isinstance(node, ast.Name) and node.id in self.slots:
                return _MISSING
            value = self.object(node)
            return int(value) if type(value) in (int, bool) else _MISSING
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub, ast.Invert)):
            value = self.constant(node.operand)
            if value is not _MISSING:
                return value if isinstance(node.op, ast.UAdd) else -value if isinstance(node.op, ast.USub) else ~value
        if isinstance(node, ast.BinOp):
            left, right = self.constant(node.left), self.constant(node.right)
            if left is _MISSING or right is _MISSING:
                return _MISSING
            operations = {ast.Add: lambda: left + right, ast.Sub: lambda: left - right,
                          ast.Mult: lambda: left * right, ast.BitAnd: lambda: left & right,
                          ast.BitOr: lambda: left | right, ast.BitXor: lambda: left ^ right}
            if type(node.op) in operations:
                return operations[type(node.op)]()
            if isinstance(node.op, (ast.LShift, ast.RShift)):
                count = right & 65535
                if count >= 16:
                    return 0
                return ((left << count) & 65535 if isinstance(node.op, ast.LShift)
                        else (left & 65535) >> count)
            if isinstance(node.op, (ast.FloorDiv, ast.Mod)):
                if not 1 <= right <= 65535:
                    self.fail(node.right, 'unsigned divisor must be in 1..65535')
                return ((left & 65535) // right if isinstance(node.op, ast.FloorDiv)
                        else (left & 65535) % right)
        if isinstance(node, ast.Call) and not node.keywords and len(node.args) == 1:
            callee = self.object(node.func)
            if callee is len:
                buffer = self.object(node.args[0])
                if not isinstance(buffer, Buffer):
                    self.fail(node, 'len requires a Buffer')
                return buffer.size
            if callee is u8 or callee is u16:
                value = self.constant(node.args[0])
                if value is not _MISSING:
                    return value & callee.mask
        return _MISSING

    def truth(self, label, positive=True):
        self.emit('MOV ER2,#0', 'CMP ER0,ER2')
        self.branch('BNE' if positive else 'BEQ', label)

    def expression(self, node, defined):
        self.current = node
        # Fold literals, immutable names and len only. Runtime arithmetic always
        # narrows each operation to 16 bits, rather than using Python big integers.
        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, bool):
                self.fail(node, 'only integer constants are supported')
            self.immediate(node.value)
        elif isinstance(node, ast.Name) and node.id in self.slots:
            if node.id not in defined:
                self.fail(node, f'local {node.id!r} may be uninitialized')
            self.load(self.slots[node.id])
        elif isinstance(node, (ast.Name, ast.Attribute)):
            value = self.object(node)
            if type(value) not in (int, bool):
                self.fail(node, 'object cannot be used as an integer')
            self.immediate(value)
        elif isinstance(node, ast.Subscript):
            buffer = self.buffer_pointer(node, defined)
            self.read_buffer(buffer)
        elif isinstance(node, ast.BinOp):
            self.expression(node.left, defined)
            if isinstance(node.op, (ast.FloorDiv, ast.Mod)):
                divisor = self.constant(node.right)
                if divisor is _MISSING:
                    self.fail(node.right, '// and % require a nonzero compile-time integer divisor')
                if not 1 <= divisor <= 65535:
                    self.fail(node.right, 'unsigned divisor must be in 1..65535')
                self.divide(divisor, isinstance(node.op, ast.Mod))
            else:
                self.emit('PUSH ER0')
                self.expression(node.right, defined)
                self.emit('POP ER2')
                self.binary(node.op, node)
        elif isinstance(node, ast.UnaryOp):
            self.expression(node.operand, defined)
            if isinstance(node.op, ast.USub):
                self.emit('XOR R0,#255', 'XOR R1,#255', 'ADD ER0,#1')
            elif isinstance(node.op, ast.Invert):
                self.emit('XOR R0,#255', 'XOR R1,#255')
            elif isinstance(node.op, ast.Not):
                yes, done = self.label('not'), self.label('done')
                self.truth(yes, False)
                self.immediate(0)
                self.jump(done)
                self.mark(yes)
                self.immediate(1)
                self.mark(done)
            elif not isinstance(node.op, ast.UAdd):
                self.fail(node, 'unsupported unary operator')
        elif isinstance(node, ast.BoolOp):
            done = self.label('boolean')
            for value in node.values[:-1]:
                self.expression(value, defined)
                self.truth(done, isinstance(node.op, ast.Or))
            self.expression(node.values[-1], defined)
            self.mark(done)
        elif isinstance(node, ast.Compare):
            self.compare(node, defined)
        elif isinstance(node, ast.Call):
            self.call(node, defined, value_required=True)
        else:
            self.fail(node, f'unsupported expression: {type(node).__name__}')

    def binary(self, op, node):
        if isinstance(op, ast.Add):
            self.emit('ADD ER0,ER2')
        elif isinstance(op, ast.Sub):
            self.emit('SUB R2,R0', 'SUBC R3,R1', 'MOV ER0,ER2')
        elif isinstance(op, (ast.BitAnd, ast.BitOr, ast.BitXor)):
            name = {ast.BitAnd: 'AND', ast.BitOr: 'OR', ast.BitXor: 'XOR'}[type(op)]
            self.emit(f'{name} R0,R2', f'{name} R1,R3')
        elif isinstance(op, ast.Mult):
            # 16x16 -> low word, using three native 8x8 products.
            self.emit('MOV ER4,ER0', 'MOV R6,R2',
                      'MUL ER6,R0', 'MOV R0,R3', 'MUL ER0,R4',
                      'ADD R7,R0', 'MOV R0,R2', 'MUL ER0,R5',
                      'ADD R7,R0', 'MOV ER0,ER6')
        elif isinstance(op, (ast.LShift, ast.RShift)):
            zero, loop, done = self.label('zero'), self.label('shift'), self.label('done')
            self.immediate(16, 4)
            self.emit('CMP ER0,ER4')
            self.branch('BGE', zero)
            self.emit('MOV R6,R0', 'MOV ER0,ER2')
            self.mark(loop)
            self.emit('CMP R6,#0')
            self.branch('BEQ', done)
            if isinstance(op, ast.LShift):
                self.emit('ADD ER0,ER0')
            else:
                self.emit('MOV R4,R1', 'AND R4,#1', 'SLL R4,#7',
                          'SRL R0,#1', 'SRL R1,#1', 'OR R0,R4')
            self.emit('ADD R6,#255')
            self.jump(loop)
            self.mark(zero)
            self.immediate(0)
            self.mark(done)
        else:
            self.fail(node, f'unsupported binary operator: {type(op).__name__}')

    def divide(self, divisor, remainder):
        if divisor == 1:
            if remainder:
                self.immediate(0)
            return
        self.emit('MOV ER2,ER0')
        if not remainder:
            self.immediate(0)
        for bit in range(15, -1, -1):
            shifted = divisor << bit
            if shifted > 65535:
                continue
            skip = self.label('divide')
            self.immediate(shifted, 4)
            self.emit('CMP ER2,ER4')
            self.branch('BLT', skip)
            self.emit('SUB R2,R4', 'SUBC R3,R5')
            if not remainder:
                self.emit(f'OR R{0 if bit < 8 else 1},#{1 << (bit % 8)}')
            self.mark(skip)
        if remainder:
            self.emit('MOV ER0,ER2')

    def compare(self, node, defined):
        failed, done = self.label('false'), self.label('done')
        self.expression(node.left, defined)
        for op, right in zip(node.ops, node.comparators):
            if type(op) not in _COMPARE:
                self.fail(node, 'only unsigned integer comparisons are supported')
            self.emit('PUSH ER0')
            self.expression(right, defined)
            self.emit('POP ER2', 'CMP ER2,ER0')
            self.branch(_INVERSE[_COMPARE[type(op)]], failed)
        self.immediate(1)
        self.jump(done)
        self.mark(failed)
        self.immediate(0)
        self.mark(done)

    def buffer_pointer(self, node, defined):
        buffer = self.object(node.value)
        if not isinstance(buffer, Buffer):
            self.fail(node, 'subscript requires a Buffer')
        index = self.constant(node.slice)
        if index is not _MISSING and not 0 <= index < buffer.size:
            self.fail(node.slice, f'Buffer index {index} outside 0..{buffer.size - 1}')
        self.expression(node.slice, defined)
        if buffer.dtype.bits == 16:
            self.emit('ADD ER0,ER0')
        self.immediate(buffer.address & 65535, 2)
        self.emit('ADD ER0,ER2', 'MOV ER2,ER0')
        return buffer

    def assign(self, target, defined):
        if isinstance(target, ast.Name):
            if self.types.get(target.id, u16).bits == 8:
                self.emit('MOV R1,#0')
            self.store(self.slots[target.id])
            defined.add(target.id)
        elif isinstance(target, ast.Subscript):
            self.emit('PUSH ER0')
            buffer = self.buffer_pointer(target, defined)
            self.emit('POP ER0')
            self.write_buffer(buffer)
        else:
            self.fail(target, 'assignment requires a local name or Buffer element')

    def read_buffer(self, buffer):
        segment = buffer.address >> 16
        if buffer.dtype.bits == 16 and not buffer.address & 1:
            self.emit(f'L ER0,{segment}:[ER2]')
        else:
            self.emit(f'L R0,{segment}:[ER2]')
            if buffer.dtype.bits == 16:
                self.emit('ADD ER2,#1', f'L R1,{segment}:[ER2]')
            else:
                self.emit('MOV R1,#0')

    def write_buffer(self, buffer):
        segment = buffer.address >> 16
        if buffer.dtype.bits == 16 and not buffer.address & 1:
            self.emit(f'ST ER0,{segment}:[ER2]')
        else:
            self.emit(f'ST R0,{segment}:[ER2]')
            if buffer.dtype.bits == 16:
                self.emit('ADD ER2,#1', f'ST R1,{segment}:[ER2]')

    def call(self, node, defined, value_required):
        callee = self.object(node.func)
        if node.keywords or any(isinstance(arg, ast.Starred) for arg in node.args):
            self.fail(node, 'calls require positional arguments without unpacking')
        if callee is u8 or callee is u16:
            if len(node.args) != 1:
                self.fail(node, 'integer cast requires one argument')
            self.expression(node.args[0], defined)
            if callee.bits == 8:
                self.emit('MOV R1,#0')
            return
        if callee is len:
            if len(node.args) != 1:
                self.fail(node, 'len requires one Buffer argument')
            value = self.constant(node)
            self.immediate(value)
            return
        args = list(node.args)
        if isinstance(callee, Function):
            if callee.native:
                self.fail(node, 'native calls require an explicit ROM(address, args, result) declaration')
            if callee.owner is not self.function.owner:
                self.fail(node, 'called function belongs to another Firmware')
            params, result = self.signature(callee, node)
            if len(args) > len(params):
                self.fail(node, 'too many function arguments')
            for name, dtype, default in params[len(args):]:
                if default is inspect.Signature.empty:
                    self.fail(node, 'missing function argument')
                args.append(ast.copy_location(ast.Constant(default), node))
            registers = [f'ER{i * 2}' for i in range(len(params))]
            if callee.symbol not in self.addresses:
                self.fail(node, f'unlinked function: {callee.name}')
            address = self.addresses[callee.symbol]
            result_reg = 'ER0' if result is not None else None
        elif isinstance(callee, ROM):
            registers = [reg.upper() for reg in callee.args]
            result_reg = callee.result.upper() if callee.result is not None else None
            if len(args) != len(registers):
                self.fail(node, 'wrong number of ROM arguments')
            self.rom_registers(registers, result_reg, node)
            address = callee.address
            result = u16
            self.emit('PUSH XR4', 'PUSH QR8')
        else:
            self.fail(node, 'call requires a decorated function, ROM, len or integer cast')
        if value_required and result_reg is None:
            self.fail(node, 'void call cannot be used as an integer')
        if type(address) is not int or address & 1 or not 0 <= address <= 0xfffff or address >> 16 not in (0, 1, 8, 9, 10, 11, 12, 13, 14, 15):
            self.fail(node, 'call target must be an even ROM/Flash code address')
        for arg in args:
            self.expression(arg, defined)
            self.emit('PUSH ER0')
        # ER8 is outside the argument register set, avoiding parallel-move cycles.
        for reg in reversed(registers):
            self.emit('POP ER8', f'MOV {reg},{"ER8" if reg.startswith("ER") else "R8"}')
        self.current = node
        self.emit(f'CALL_SYS 0x{address:05X}')
        if result_reg is not None:
            if result_reg.startswith('ER'):
                if result_reg != 'ER0':
                    self.emit(f'MOV ER0,{result_reg}')
            else:
                if result_reg != 'R0':
                    self.emit(f'MOV R0,{result_reg}')
                self.emit('MOV R1,#0')
        if isinstance(callee, ROM):
            self.emit('POP QR8', 'POP XR4')
        elif result is u8:
            self.emit('MOV R1,#0')

    def rom_registers(self, args, result, node):
        occupied = set()
        for reg in args + ([] if result is None else [result]):
            if not re.fullmatch(r'(?:R[0-7]|ER[0246])', reg):
                self.fail(node, 'ROM registers must be R0..R7 or ER0/2/4/6')
        for reg in args:
            number = int(reg[2:] if reg.startswith('ER') else reg[1:])
            used = {number, number + 1} if reg.startswith('ER') else {number}
            if occupied & used:
                self.fail(node, 'overlapping ROM argument registers')
            occupied.update(used)

    def block(self, nodes, defined):
        defined = set(defined)
        live = True
        for node in nodes:
            self.current = node
            state = self.statement(node, defined)
            if state is None:
                live = False
            else:
                defined = state
        return defined if live else None

    def statement(self, node, defined):
        if isinstance(node, ast.Assign):
            self.expression(node.value, defined)
            for index, target in enumerate(node.targets):
                if index < len(node.targets) - 1:
                    self.emit('PUSH ER0')
                self.assign(target, defined)
                if index < len(node.targets) - 1:
                    self.emit('POP ER0')
        elif isinstance(node, ast.AnnAssign):
            if node.value is not None:
                self.expression(node.value, defined)
                self.assign(node.target, defined)
        elif isinstance(node, ast.AugAssign):
            buffer = None
            if isinstance(node.target, ast.Subscript):
                buffer = self.buffer_pointer(node.target, defined)
                self.emit('PUSH ER2')
                self.read_buffer(buffer)
            else:
                self.expression(node.target, defined)
            if isinstance(node.op, (ast.FloorDiv, ast.Mod)):
                divisor = self.constant(node.value)
                if divisor is _MISSING or not 1 <= divisor <= 65535:
                    self.fail(node.value, '// and % require a compile-time divisor in 1..65535')
                self.divide(divisor, isinstance(node.op, ast.Mod))
            else:
                self.emit('PUSH ER0')
                self.expression(node.value, defined)
                self.emit('POP ER2')
                self.binary(node.op, node)
            if buffer is not None:
                self.emit('POP ER2')
                self.write_buffer(buffer)
            else:
                self.assign(node.target, defined)
        elif isinstance(node, ast.Return):
            if node.value is None or (isinstance(node.value, ast.Constant) and node.value.value is None):
                if self.result is not None:
                    self.fail(node, 'integer function must return an integer')
                self.immediate(0)
            else:
                if self.result is None:
                    self.fail(node, 'void function cannot return an integer')
                self.expression(node.value, defined)
                if self.result is u8:
                    self.emit('MOV R1,#0')
            self.jump(self.exit)
            return None
        elif isinstance(node, ast.If):
            other, done = self.label('else'), self.label('endif')
            self.expression(node.test, defined)
            self.truth(other, False)
            left = self.block(node.body, defined)
            self.jump(done)
            self.mark(other)
            right = self.block(node.orelse, defined)
            self.mark(done)
            return right if left is None else left if right is None else left & right
        elif isinstance(node, ast.While):
            if node.orelse:
                self.fail(node, 'loop else is not supported')
            start, done = self.label('while'), self.label('endwhile')
            self.mark(start)
            self.expression(node.test, defined)
            self.truth(done, False)
            self.loops.append((done, start))
            self.block(node.body, defined)
            self.loops.pop()
            self.jump(start)
            self.mark(done)
        elif isinstance(node, ast.For):
            self.for_loop(node, defined)
        elif isinstance(node, (ast.Break, ast.Continue)):
            if not self.loops:
                self.fail(node, 'break/continue requires a loop')
            self.jump(self.loops[-1][0 if isinstance(node, ast.Break) else 1])
            return None
        elif isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                # A function docstring does not generate code.
                if node is not self.node.body[0]:
                    self.fail(node, 'string expressions are only allowed as a docstring')
            elif isinstance(node.value, ast.Call):
                self.call(node.value, defined, value_required=False)
            else:
                self.expression(node.value, defined)
        elif not isinstance(node, ast.Pass):
            self.fail(node, f'unsupported statement: {type(node).__name__}')
        return defined

    def for_loop(self, node, defined):
        if node.orelse:
            self.fail(node, 'loop else is not supported')
        if not isinstance(node.target, ast.Name):
            self.fail(node.target, 'range target must be a local name')
        call = node.iter
        if not isinstance(call, ast.Call) or self.object(call.func) is not range or call.keywords or not 1 <= len(call.args) <= 3:
            self.fail(call, 'for requires range with one, two or three positional arguments')
        args = call.args
        start = ast.copy_location(ast.Constant(0), call) if len(args) == 1 else args[0]
        stop = args[0] if len(args) == 1 else args[1]
        step = 1 if len(args) < 3 else self.constant(args[2])
        if step is _MISSING or not -65535 <= step <= 65535 or step == 0:
            self.fail(call, 'range step must be a nonzero constant in -65535..65535')
        for bound in (start, stop):
            value = self.constant(bound)
            if value is not _MISSING and not 0 <= value <= 65535:
                self.fail(bound, 'range bounds must be unsigned 0..65535; signed ranges are unsupported')
        index_slot, stop_slot = self.range_slots[id(node)]
        self.expression(start, defined)
        self.store(index_slot)
        self.expression(stop, defined)
        self.store(stop_slot)
        begin, advance, done = self.label('for'), self.label('next'), self.label('endfor')
        self.mark(begin)
        self.load(index_slot)
        self.load(stop_slot, 2)
        self.emit('CMP ER0,ER2')
        self.branch('BGE' if step > 0 else 'BLE', done)
        body_defined = set(defined)
        self.assign(node.target, body_defined)
        self.loops.append((done, advance))
        self.block(node.body, body_defined)
        self.loops.pop()
        self.mark(advance)
        self.load(index_slot)
        # Do not wrap an induction variable at either unsigned boundary.
        self.immediate(65535 - step if step > 0 else -step, 2)
        self.emit('CMP ER0,ER2')
        self.branch('BGT' if step > 0 else 'BLT', done)
        self.immediate(step, 2)
        self.emit('ADD ER0,ER2')
        self.store(index_slot)
        self.jump(begin)
        self.mark(done)

    def compile(self):
        if type(self.origin) is not int or self.origin & 1 or not 0 <= self.origin <= 0xfffff or self.origin >> 16 not in (0, 1, 8, 9, 10, 11, 12, 13, 14, 15):
            self.fail(self.node, 'origin must be an even ROM/Flash code address')
        self.emit('PUSH LR', 'PUSH XR4', 'PUSH QR8', 'MOV ER14,SP')
        remaining = len(self.slots) * 2
        while remaining:
            chunk = min(remaining, 128)
            self.emit(f'ADD SP,#{-chunk}')
            remaining -= chunk
        for index, (name, dtype, default) in enumerate(self.params):
            if dtype is u8:
                self.emit(f'MOV R{index * 2 + 1},#0')
            self.store(self.slots[name], index * 2)
        end = self.block(self.node.body, {name for name, dtype, default in self.params})
        if end is not None and self.result is not None:
            self.fail(self.node, 'integer function may fall through without a return')
        if end is not None:
            self.immediate(0)
        self.mark(self.exit)
        self.emit('MOV SP,ER14', 'POP QR8', 'POP XR4', 'POP PC')
        source = '\n'.join(self.lines) + '\n'
        try:
            data, _, listing = assemble(source, self.origin)
        except ValueError as exc:
            match = re.match(r'line (\d+): (.*)', str(exc))
            if match:
                self.fail(self.locations[int(match[1]) - 1], match[2])
            self.fail(self.node, str(exc))
        if (self.origin & 65535) + len(data) > 65536:
            self.fail(self.node, 'function crosses a code bank boundary')
        return data, source


def compile_function(function, origin, addresses):
    """Return machine bytes and diagnostic assembly for one decorated function.

    Division/modulo accept constant divisors 1..65535. Shift counts >=16 give
    zero. Loop bounds are unsigned; loop-else and signed ranges are rejected.
    Definite assignment is conservative after loops (which may run zero times).
    """
    if function.native:
        from .native import compile_native
        return compile_native(function, origin, addresses)
    return _Compiler(function, origin, addresses).compile()
