"""Compiler tests use opcode fixtures, not a substitute CPU implementation."""

import linecache
import re
import textwrap
import unittest

from kits import Buffer, Firmware, Memory, ROM, u8, u16
from kits.compiler import compile_function
from nxu8_asm import disassemble


class CompilerTests(unittest.TestCase):
    def setUp(self):
        self.serial = 0
        self.sources = []

    def tearDown(self):
        for filename in self.sources:
            linecache.cache.pop(filename, None)

    def functions(self, source, **objects):
        self.serial += 1
        filename = f'<kits-compiler-{self.id()}-{self.serial}>'
        source = textwrap.dedent(source).lstrip('\n')
        linecache.cache[filename] = (len(source), None, source.splitlines(True), filename)
        self.sources.append(filename)
        fw = Firmware('test', regions=((0x84000, 0x86000),))
        namespace = dict(fw=fw, u8=u8, u16=u16, Buffer=Buffer, Memory=Memory, ROM=ROM)
        namespace.update(objects)
        exec(compile(source, filename, 'exec'), namespace)
        return fw, namespace, filename

    def compile(self, source, name='main', origin=0x84000, **objects):
        fw, namespace, filename = self.functions(source, **objects)
        addresses = {function.symbol: 0x85000 + index * 0x100
                     for index, function in enumerate(fw.functions)}
        data, assembly = compile_function(namespace[name], origin, addresses)
        return data, assembly

    def error(self, source, message, line=None, **objects):
        fw, namespace, filename = self.functions(source, **objects)
        addresses = {function.symbol: 0x85000 for function in fw.functions}
        with self.assertRaisesRegex(ValueError, message) as caught:
            compile_function(namespace['main'], 0x84000, addresses)
        location = f'{filename}:{line}:' if line is not None else filename + ':'
        self.assertIn(location, str(caught.exception))

    def test_known_return_and_frame_opcodes(self):
        data, _ = self.compile('''
            @fw.function
            def main():
                return 42
        ''')
        # PUSH LR / PUSH XR4 / PUSH QR8 / MOV ER14,SP, MOV ER0,#42,
        # far JMP 8:400E, MOV SP,ER14 / POP QR8 / POP XR4 / POP PC.
        self.assertEqual(data.hex(), 'cef86ef47ef81aae2ae000f80e40eaa13ef82ef48ef2')

    def test_known_argument_slot_and_subtraction(self):
        data, source = self.compile('''
            @fw.function
            def main(value: u16):
                return value - 1
        ''')
        self.assertIn(bytes.fromhex('fee100e3e9a0feff'), data)
        self.assertIn(bytes.fromhex('0882198325f0'), data)
        self.assertIn('L ER0,0:-2[ER14]', source)
        self.assertTrue(source.endswith('MOV SP,ER14\nPOP QR8\nPOP XR4\nPOP PC\n'))

    def test_word_and_byte_narrowing(self):
        data, source = self.compile('''
            @fw.function
            def main(value: u8) -> u8:
                small: u8 = value + 255
                small += 1
                wide: u16 = u16(small) + 65535
                return u8(wide)
        ''')
        self.assertGreaterEqual(source.count('MOV R1,#0'), 5)
        self.assertIn('ADD ER0,ER2', source)
        self.assertIn(bytes.fromhex('0001'), data)

    def test_runtime_arithmetic(self):
        _, source = self.compile('''
            @fw.function
            def main(a, b):
                product = a * b
                shifted = (product << b) | (product >> b)
                return (~shifted ^ -a) & (a + b - 1)
        ''')
        self.assertEqual(source.count('MUL '), 3)
        self.assertIn('MUL ER6,R0', source)
        self.assertIn('SRL R0,#1\nSRL R1,#1\nOR R0,R4', source)
        self.assertIn('MOV ER4,#16', source)
        self.assertIn('XOR R1,#255', source)

    def test_constant_division_and_modulo(self):
        for divisor in (1, 2, 3, 255, 256, 32768, 65535):
            with self.subTest(divisor=divisor):
                data, source = self.compile(f'''
                    @fw.function
                    def main(value):
                        quotient = value // {divisor}
                        remainder = value % {divisor}
                        quotient //= {divisor}
                        remainder %= {divisor}
                        return quotient + remainder
                ''')
                self.assertNotIn('DIV ', source)
                if divisor != 1:
                    self.assertIn('CMP ER2,ER4', source)
                    self.assertIn('SUB R2,R4\nSUBC R3,R5', source)

    def test_division_diagnostics(self):
        for rhs, message in [('other', 'compile-time'), ('0', '1..65535'),
                             ('-1', '1..65535'), ('65536', '1..65535')]:
            with self.subTest(rhs=rhs):
                self.error(f'''
                    @fw.function
                    def main(value, other):
                        return value // {rhs}
                ''', message, line=3)

    def test_long_branches_do_not_overflow(self):
        assignments = '\n'.join('        total += value' for _ in range(100))
        source = ('@fw.function\ndef main(value):\n    total = 0\n'
                  '    if value:\n' + assignments + '\n'
                  '    else:\n        total = 1\n'
                  '    while value:\n        value -= 1\n'
                  '        total += value\n    return total\n')
        data, assembly = self.compile(source)
        self.assertGreater(len(data), 1000)
        rows = disassemble(data, 0x84000)
        relative = [row for row in rows if re.match(r'B(?:EQ|NE|GE|LT|GT|LE) ', row['text'])]
        self.assertTrue(relative)
        # Every relative branch skips one four-byte far jump: displacement = 2.
        self.assertTrue(all(bytes.fromhex(row['bytes'])[0] == 2 for row in relative))
        self.assertIn('JMP _while_', assembly)

    def test_short_circuit_and_chained_comparison(self):
        data, source = self.compile('''
            @fw.function
            def main(value):
                if value and probe() or not value:
                    return 0 < probe() < 65535
                return 7
        ''', probe=ROM(0x12340))
        self.assertEqual(data.count(bytes.fromhex('01f14023')), 2)
        first_call = source.index('CALL_SYS')
        self.assertIn('JMP _boolean_', source[:first_call])
        self.assertIn('CMP ER2,ER0', source)

    def test_boolean_operators_keep_operand_values(self):
        for operator in ('and', 'or'):
            with self.subTest(operator=operator):
                _, source = self.compile(f'''
                    @fw.function
                    def main():
                        return 7 {operator} 3
                ''')
                self.assertIn('MOV ER0,#7', source)
                self.assertIn('MOV ER0,#3', source)
                self.assertNotIn('MOV ER0,#1', source)
                self.assertNotIn('MOV ER0,#0', source)

    def test_all_unsigned_comparisons(self):
        for comparison in ('==', '!=', '<', '<=', '>', '>='):
            with self.subTest(comparison=comparison):
                _, source = self.compile(f'''
                    @fw.function
                    def main(a, b):
                        return a {comparison} b
                ''')
                self.assertIn('CMP ER2,ER0', source)
                self.assertNotRegex(source, r'B(?:GE|LT|GT|LE)S ')

    def test_range_and_loop_control(self):
        _, source = self.compile('''
            @fw.function
            def main(bound):
                total = 0
                for i in range(bound):
                    if i == 2:
                        continue
                    for j in range(9, 0, -2):
                        if j < 3:
                            break
                        total += i + j
                for i in range(65534, 65535, 2):
                    total += i
                while total:
                    total -= 1
                    if total < 5:
                        break
                return total
        ''')
        self.assertIn('MOV ER2,#65534', source)
        self.assertIn('MOV ER2,#2', source)
        self.assertIn('MOV ER2,#65533', source)
        self.assertIn('JMP _next_', source)
        self.assertIn('JMP _endfor_', source)
        self.assertIn('JMP _endwhile_', source)

    def test_range_snapshots_bounds_and_preserves_target(self):
        _, source = self.compile('''
            @fw.function
            def main():
                i = 100
                for i in range(probe(), probe(), 2):
                    i = 17
                return i
        ''', probe=ROM(0x12340))
        self.assertEqual(source.count('CALL_SYS'), 2)
        self.assertLess(source.rindex('CALL_SYS'), source.index('_for_'))
        self.assertIn('ST ER0,0:-2[ER14]', source)

    def test_range_rejections(self):
        for args, message in [('0, 5, 0', 'nonzero'), ('0, 5, value', 'constant'),
                              ('5, -1, -1', 'signed ranges'), ('65536', 'signed ranges'),
                              ('-1, 5', 'signed ranges')]:
            with self.subTest(args=args):
                self.error(f'''
                    @fw.function
                    def main(value):
                        for i in range({args}):
                            pass
                        return 0
                ''', message, line=3)

    def test_buffer_explicit_segments_and_odd_words(self):
        data, source = self.compile('''
            @fw.function
            def main(index, value):
                bytes_[index] = u8(value)
                words[index] = value
                return words[index] + bytes_[index]
        ''', bytes_=Buffer(0x40001, 16), words=Buffer(0x40101, 16, u16))
        # Immediate DSR=4, ST R0,[ER2]; byte accesses avoid alignment loss.
        self.assertIn(bytes.fromhex('04e32190'), data)
        self.assertIn('ST R0,4:[ER2]\nADD ER2,#1\nST R1,4:[ER2]', source)
        self.assertIn('L R0,4:[ER2]\nADD ER2,#1\nL R1,4:[ER2]', source)
        self.assertNotIn('L ER0,4:', source)

    def test_memory_class_and_len(self):
        class LCD(Memory):
            body = Buffer(0x80EC, 31 * 12)

        data, source = self.compile('''
            @fw.function
            def main() -> None:
                for i in range(len(LCD.body)):
                    LCD.body[i] = 0
                refresh()
        ''', LCD=LCD, refresh=ROM(0x043BE, result=None))
        self.assertIn('MOV ER0,#372', source)
        self.assertIn(bytes.fromhex('01f0be43'), data)
        self.assertIn('ST R0,0:[ER2]', source)

    def test_aligned_buffer_word_opcodes(self):
        data, source = self.compile('''
            @fw.function
            def main(index, value):
                memory[index] = value
                return memory[index]
        ''', memory=Buffer(0x40000, 8, u16))
        self.assertIn(bytes.fromhex('04e32390'), data)
        self.assertIn(bytes.fromhex('04e32290'), data)
        self.assertIn('ST ER0,4:[ER2]', source)
        self.assertIn('L ER0,4:[ER2]', source)

    def test_buffer_augassign_evaluates_index_once(self):
        _, source = self.compile('''
            @fw.function
            def main() -> None:
                memory[probe()] += probe()
        ''', memory=Buffer(0x40001, 8, u16), probe=ROM(0x12340))
        self.assertEqual(source.count('CALL_SYS'), 2)
        self.assertIn('PUSH ER2', source)
        self.assertIn('POP ER2\nST R0,4:[ER2]', source)

    def test_constant_buffer_bounds(self):
        for index in ('-1', '8', '4 + 4'):
            with self.subTest(index=index):
                self.error(f'''
                    @fw.function
                    def main():
                        return memory[{index}]
                ''', 'Buffer index', line=3, memory=Buffer(0x40000, 8))

    def test_constant_and_closure_bindings(self):
        owner = Firmware('closure', regions=((0x84000, 0x86000),))
        limit = 27
        memory = Buffer(0x40000, 32)

        @owner.function
        def main():
            return memory[limit] + limit

        _, source = compile_function(main, 0x84000, {main.symbol: 0x84000})
        self.assertEqual(source.count('MOV ER0,#27'), 2)
        self.assertIn('L R0,4:[ER2]', source)

    def test_internal_call_arguments_and_stable_link_size(self):
        fw, namespace, _ = self.functions('''
            @fw.function
            def helper(a: u8, b: u16, c, d=17) -> u8:
                return u8(a + b + c + d)

            @fw.function
            def main(value):
                return helper(value, value + 1, value + 2)
        ''')
        main = namespace['main']
        small, source = compile_function(main, 0x84000, {'fn_main': 0, 'fn_helper': 0})
        final, linked = compile_function(main, 0x84000, {'fn_main': 0x84000, 'fn_helper': 0xA3456})
        self.assertEqual(len(small), len(final))
        self.assertIn(bytes.fromhex('01fa5634'), final)
        self.assertEqual(source.count('CALL_SYS'), 1)
        self.assertIn('MOV ER6,ER8', linked)
        self.assertIn('MOV ER4,ER8', linked)
        self.assertIn('MOV ER2,ER8', linked)
        self.assertIn('MOV ER0,ER8', linked)
        self.assertIn('MOV ER0,#17', linked)

    def test_rom_saves_frame_and_captures_result_first(self):
        data, source = self.compile('''
            @fw.function
            def main(a, b):
                value = native(a + 1, b)
                return value + a
        ''', native=ROM(0x12340, args=('r3', 'er4'), result='er6'))
        self.assertEqual(source.count('PUSH QR8'), 2)
        self.assertIn('MOV R3,R8', source)
        self.assertIn('MOV ER4,ER8', source)
        self.assertIn('CALL_SYS 0x12340\nMOV ER0,ER6\nPOP QR8\nPOP XR4', source)
        self.assertIn(bytes.fromhex('65f03ef82ef4'), data)

    def test_rom_byte_result_zero_extends(self):
        _, source = self.compile('''
            @fw.function
            def main():
                return native()
        ''', native=ROM(0x12340, result='r1'))
        self.assertIn('MOV R0,R1\nMOV R1,#0\nPOP QR8\nPOP XR4', source)

    def test_void_return(self):
        for statement in ('return', 'return None', 'pass'):
            with self.subTest(statement=statement):
                data, _ = self.compile(f'@fw.function\ndef main() -> None:\n    {statement}\n')
                self.assertTrue(data.endswith(bytes.fromhex('eaa13ef82ef48ef2')))
        self.error('''
            @fw.function
            def main():
                return native()
        ''', 'void call', line=3, native=ROM(0x12340, result=None))

    def test_definite_assignment(self):
        self.error('''
            @fw.function
            def main(flag):
                if flag:
                    value = 1
                return value
        ''', 'uninitialized', line=5)
        self.error('''
            @fw.function
            def main(flag):
                for i in range(flag):
                    value = i
                return value
        ''', 'uninitialized', line=5)
        self.error('''
            @fw.function
            def main():
                value += 1
                return value
        ''', 'uninitialized', line=3)
        _, source = self.compile('''
            @fw.function
            def main(flag):
                if flag:
                    return 7
                else:
                    value = 11
                return value
        ''')
        self.assertIn('MOV ER0,#11', source)

    def test_both_branch_definitions(self):
        data, _ = self.compile('''
            @fw.function
            def main(flag):
                if flag:
                    value = 1
                else:
                    value = 2
                return value
        ''')
        self.assertTrue(data)

    def test_original_source_lines(self):
        self.error('''
            sentinel = 1

            @fw.function
            def main():
                value = 1
                return [value]
        ''', 'unsupported expression: List', line=6)

    def test_unsupported_statements_and_calls(self):
        cases = [
            ('try:\n        pass\n    finally:\n        pass', 'unsupported statement'),
            ('items = [1, 2]', 'unsupported expression'),
            ('memory.address = 1', 'assignment requires'),
            ('native(value=1)', 'positional'),
            ('value = len()', 'one Buffer'),
            ('value = abs(1)', 'expected a constant'),
            ('global value', 'unsupported statement'),
            ('while 0:\n        pass\n    else:\n        pass', 'loop else'),
        ]
        for statement, message in cases:
            with self.subTest(statement=statement):
                source = '@fw.function\ndef main() -> None:\n    ' + statement + '\n'
                self.error(source, message, memory=Buffer(0x40000, 8), native=ROM(0x12340))

    def test_no_descriptor_execution(self):
        class Dangerous(Memory):
            class Descriptor:
                def __get__(self, instance, owner):
                    raise AssertionError('compiler executed a descriptor')
            field = Descriptor()

        self.error('''
            @fw.function
            def main():
                return Dangerous.field
        ''', 'expected a constant', line=3, Dangerous=Dangerous)

    def test_parameter_and_return_diagnostics(self):
        cases = [
            ('def main(a, b, c, d, e):\n    return 0', 'at most four'),
            ('def main(*args):\n    return 0', 'positional'),
            ('def main(a: str):\n    return 0', 'annotation'),
            ('def main(a):\n    if a:\n        return 1', 'fall through'),
            ('def main() -> None:\n    return 1', 'void function'),
            ('def main():\n    return', 'must return'),
        ]
        for definition, message in cases:
            with self.subTest(definition=definition):
                self.error('@fw.function\n' + definition + '\n', message)

    def test_function_call_diagnostics(self):
        self.error('''
            @fw.function
            def helper(value):
                return value
            @fw.function
            def main():
                return helper()
        ''', 'missing function argument', line=6)
        self.error('''
            @fw.function
            def helper():
                return 1
            @fw.function
            def main():
                return helper(1)
        ''', 'too many', line=6)
        fw, namespace, filename = self.functions('''
            @fw.function
            def helper():
                return 1
            @fw.function
            def main():
                return helper()
        ''')
        with self.assertRaisesRegex(ValueError, re.escape(filename) + ':6: unlinked'):
            compile_function(namespace['main'], 0x84000, {})

    def test_code_address_boundaries(self):
        fw, namespace, filename = self.functions('''
            @fw.function
            def main():
                return 42
        ''')
        for origin in (0x84001, -2, 0x100000, 0x40000):
            with self.subTest(origin=origin):
                with self.assertRaisesRegex(ValueError, 'origin must be'):
                    compile_function(namespace['main'], origin, {})
        with self.assertRaisesRegex(ValueError, 'crosses.*code'):
            compile_function(namespace['main'], 0x8FFF0, {})

    def test_large_frame_uses_bounded_sp_immediates(self):
        assignments = '\n'.join(f'    value{i} = {i}' for i in range(90))
        _, source = self.compile('@fw.function\ndef main():\n' + assignments + '\n    return value89\n')
        self.assertIn('ADD SP,#-128\nADD SP,#-52', source)
        self.assertIn('L ER0,0:-180[ER14]', source)


if __name__ == '__main__':
    unittest.main()
