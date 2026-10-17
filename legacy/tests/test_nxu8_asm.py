"""Host-only tests; no simulator or firmware files are modified."""

import random
import unittest

from nxu8_asm import assemble, disassemble


class AssemblerTests(unittest.TestCase):
    def roundtrip(self, data, origin=0):
        records = disassemble(data, origin)
        self.assertEqual(b''.join(bytes.fromhex(row['bytes']) for row in records), data)
        encoded, _, _ = assemble('\n'.join(row['text'] for row in records), origin)
        self.assertEqual(encoded, data)
        address = origin
        for row in records:
            self.assertEqual(row['address'], address)
            address += len(bytes.fromhex(row['bytes']))
        return records

    def test_known_machine_code(self):
        data, symbols, listing = assemble('entry: MOV R0,#42\nMOV R1,#0\nRT', 0xc4000)
        self.assertEqual(data.hex(), '2a0000011ffe')
        self.assertEqual(symbols, {'ENTRY': 0xc4000})
        self.assertEqual([row['line'] for row in listing], [1, 2, 3])
        self.assertEqual([row['address'] for row in listing], [0xc4000, 0xc4002, 0xc4004])
        self.roundtrip(data, 0xc4000)

    def test_catalogue_forms(self):
        source = '''
ADD R3,#42
ADD R3,R5
ADDC R3,#42
ADDC R3,R5
ADD ER2,#-64
ADD ER2,ER4
SUB R3,R5
SUBC R3,R5
SUB R3,#42
AND R3,R5
AND R3,#42
OR R3,R5
OR R3,#42
XOR R3,R5
XOR R3,#42
SLL R3,R5
SLL R3,#7
SLLC R3,R5
SLLC R3,#7
SRL R3,R5
SRL R3,#7
SRLC R3,R5
SRA R3,#7
SRA R3,R5
MUL ER2,R5
DIV ER2,R5
CMP R3,#42
CMP R3,R5
CMPC R3,#42
CMPC R3,R5
CMP ER2,ER4
DAA R3
DAS R3
NEG R3
MOV R3,#42
MOV R3,R5
MOV ER2,ER4
MOV ER2,SP
MOV SP,ER4
here:
BGE here
BLT here
BGT here
BLE here
BGES here
BLTS here
BGTS here
BLES here
BNE here
BEQ here
BNV here
BOV here
BPS here
BNS here
JMP here
CALL here
L R3,0x0101
L R3,[ER4]
L R3,-32768[ER4]
L ER2,0x0100
L ER2,[ER4]
L ER2,0xFFFF[ER4]
ST R3,0x0101
ST R3,[ER4]
ST R3,32767[ER4]
ST ER2,0x0100
ST ER2,[ER4]
ST ER2,0x8000[ER4]
PUSH R3
PUSH ER2
POP R3
POP ER2
PUSH XR4
PUSH QR8
POP XR12
POP QR0
PUSH LR
POP LR
PUSH EA
POP EA
POP PC
CALL_SYS 0x1:0x2340
TB R3.7
EXTBW ER2
ADD SP,#-128
SC
RC
CPLC
NOP
RET
END
'''
        data, _, _ = assemble(source, 0xa0000)
        self.roundtrip(data, 0xa0000)

    def test_macros(self):
        data, _, _ = assemble('MOV ER14,#0x1234\nSUB R0,#255\nSUB R7,#42')
        self.assertEqual(data.hex(), '340e120f4ef1ff0118800ef14ef02a0008870ef0')
        records = self.roundtrip(data)
        self.assertEqual(records[-2]['text'], 'SUB R0,#0xFF')
        self.assertEqual(records[-1]['text'], 'SUB R7,#0x2A')

    def test_native_word_immediates(self):
        cases = [
            ('MOV ER0,#1', '01e0'), ('MOV ER14,#63', '3fee'),
            ('MOV ER2,#-64', '40e2'), ('MOV ER4,#-1', '7fe4'),
            ('MOV ER6,#0xFFC0', '40e6'), ('MOV ER8,#65535', '7fe8'),
            ('MOV ER0,#64', '40000001'), ('MOV ER2,#0x7F', '7f020003'),
            ('MOV ER4,#0xFFBF', 'bf04ff05'),
        ]
        for source, raw in cases:
            with self.subTest(source=source):
                data = bytes.fromhex(raw)
                self.assertEqual(assemble(source)[0], data)
                records = self.roundtrip(data)
                self.assertTrue(all(row['text'].startswith('MOV ') for row in records))

    def test_symbolic_word_immediates_keep_layout(self):
        source = 'MOV ER0,#end\nMOV ER2,#small\nMOV ER4,#0\nend: NOP\nsmall EQU 1'
        data, symbols, _ = assemble(source)
        self.assertEqual(data.hex(), '0a0000010102000300e48ffe')
        self.assertEqual(symbols['END'], 10)
        self.roundtrip(data)

    def test_native_control_and_arithmetic(self):
        # Opcode fixtures from CPU.cpp and the nX-U8/100 instruction formats.
        cases = [
            ('BAL 0x4006', '02ce'), ('B ER0', '02f0'), ('BL ER14', 'e3f0'),
            ('JMP ER2', '22f0'), ('CALL ER8', '83f0'),
            ('SRLC R15,#7', '7d9f'), ('SRLC R0,#0', '0d90'),
            ('SB R3.7', '70a3'), ('RB R8.0', '02a8'),
            ('EI', '08ed'), ('DI', 'f7eb'), ('INC [EA]', '2ffe'),
            ('DEC [EA]', '3ffe'), ('RTI', '0ffe'),
            ('LEA [ER2]', '2af0'), ('LEA -32768[ER14]', 'ebf00080'),
            ('LEA 32767[ER0]', '0bf0ff7f'), ('LEA 0xFFFF', '0cf0ffff'),
            ('MOV R0,PSW', '03a0'), ('MOV R15,PSW', '03af'),
            ('MOV PSW,R0', '0ba0'), ('MOV PSW,R15', 'fba0'),
        ]
        for source, raw in cases:
            with self.subTest(source=source):
                data = bytes.fromhex(raw)
                self.assertEqual(assemble(source, 0x4000)[0], data)
                records = self.roundtrip(data, 0x4000)
                self.assertEqual(len(records), 1)
                self.assertNotIn(records[0]['text'].split()[0], ('DB', 'DW'))

    def test_base_pointer_load_store(self):
        cases = [
            ('L R0,-32[BP]', '20d0'), ('L R15,31[FP]', '5fdf'),
            ('ST R3,-1[BP]', 'bfd3'), ('ST R4,0[FP]', 'c0d4'),
            ('L ER0,-32[BP]', '20b0'), ('L ER14,31[FP]', '5fbe'),
            ('ST ER2,-1[BP]', 'bfb2'), ('ST ER4,0[FP]', 'c0b4'),
            ('L R2,[BP]', '00d2'), ('ST ER6,0x3F[FP]', 'ffb6'),
            ('L R0,4:-32[BP]', '04e320d0'),
            ('ST ER14,R3:31[FP]', '3f90dfbe'),
            ('L ER2,DSR:0[BP]', '9ffe00b2'),
        ]
        for source, raw in cases:
            with self.subTest(source=source):
                data = bytes.fromhex(raw)
                self.assertEqual(assemble(source)[0], data)
                records = self.roundtrip(data)
                self.assertEqual(len(records), 1)
                self.assertTrue(records[0]['text'].startswith(('L ', 'ST ')))

    def test_effective_address_load_store(self):
        cases = [
            ('L R15,[EA]', '309f'), ('L R15,[EA+]', '509f'),
            ('ST R15,[EA]', '319f'), ('ST R15,[EA+]', '519f'),
            ('L ER14,[EA]', '329e'), ('L ER14,[EA+]', '529e'),
            ('ST ER14,[EA]', '339e'), ('ST ER14,[EA+]', '539e'),
            ('L XR12,[EA]', '349c'), ('L XR12,[EA+]', '549c'),
            ('ST XR12,[EA]', '359c'), ('ST XR12,[EA+]', '559c'),
            ('L QR8,[EA]', '3698'), ('L QR8,[EA+]', '5698'),
            ('ST QR8,[EA]', '3798'), ('ST QR8,[EA+]', '5798'),
            ('L QR0,4:[EA+]', '04e35690'),
            ('ST XR4,R7:[EA]', '7f903594'),
            ('L ER0,DSR:[EA]', '9ffe3290'),
        ]
        for source, raw in cases:
            with self.subTest(source=source):
                data = bytes.fromhex(raw)
                self.assertEqual(assemble(source)[0], data)
                records = self.roundtrip(data)
                self.assertEqual(len(records), 1)
                self.assertTrue(records[0]['text'].startswith(('L ', 'ST ')))

    def test_unconditional_relative_limits(self):
        for source, origin, raw in [
            ('BAL 0x4100', 0x4000, '7fce'),
            ('BAL 0x4000', 0x40fe, '80ce'),
            ('BAL 0x8:0', 0x8fffe, '00ce'),
        ]:
            with self.subTest(source=source):
                data = bytes.fromhex(raw)
                self.assertEqual(assemble(source, origin)[0], data)
                self.assertEqual(self.roundtrip(data, origin)[0]['text'].split()[0], 'BAL')

    def test_native_operand_boundaries(self):
        cases = [
            'MOV ER0,#-65', 'MOV ER16,#0', 'MOV ER3,#1',
            'BAL 0x102', 'BAL 0xFFF00', 'BAL 0x1:0', 'BAL 1',
            'B ER1', 'BL ER16', 'SRLC R0,#8', 'SRLC R0,#-1',
            'SB R0.8', 'RB R16.0', 'RB R0.-1',
            'MOV R16,PSW', 'MOV PSW,R16', 'MOV PSW,ER0',
            'L R0,-33[BP]', 'L R0,32[FP]', 'ST ER0,0x40[BP]',
            'ST ER1,0[FP]', 'L XR0,0[BP]',
            'L ER1,[EA]', 'ST XR2,[EA+]', 'L QR4,[EA]', 'L R16,[EA+]',
            'LEA [ER1]', 'LEA 32768[ER0]', 'LEA -32769[ER0]', 'LEA 65536',
        ]
        for source in cases:
            with self.subTest(source=source):
                with self.assertRaisesRegex(ValueError, r'line \d+:'):
                    assemble(source)

    def test_native_alternate_and_truncated_encodings(self):
        # Nonzero ignored branch bits and unaligned register fields stay data.
        for raw in ('83f1', '02f8', '3491', '3694', '00b1',
                    '0bf0', '0bf034', '0cf0', '04e356', '8d90'):
            with self.subTest(raw=raw):
                data = bytes.fromhex(raw)
                self.roundtrip(data)
                self.assertTrue(disassemble(data)[0]['text'].startswith('DW '))

    def test_data_symbols_and_padding(self):
        source = '''.equ value, other+1
other EQU 0x20
start: DB "a; b,""c""", 0, value ; unmatched " in comment
DW finish-start, 1234H
.org 0x1012
finish: DW start
'''
        data, symbols, listing = assemble(source, 0x1000)
        self.assertEqual(data[:10], b'a; b,"c"\x00!')
        self.assertEqual(data[10:14], bytes.fromhex('12003412'))
        self.assertEqual(data[14:18], bytes(4))
        self.assertEqual(data[18:], bytes.fromhex('0010'))
        self.assertEqual(symbols['VALUE'], 33)
        self.assertEqual(symbols['FINISH'], 0x1012)
        self.assertEqual(listing[2]['bytes'], '00000000')
        self.roundtrip(data, 0x1000)

    def test_forward_backward_and_data_targets(self):
        source = 'BNE later\nback: DW 0\nlater: BEQ back\nJMP later+2\nCALL 0x1:0x0120'
        data, symbols, _ = assemble(source, 0xc8000)
        self.assertEqual(data[:6].hex(), '01c80000fec9')
        self.assertEqual(data[6:].hex(), '00fc068001f12001')
        self.assertEqual(symbols['LATER'], 0xc8004)
        self.roundtrip(data, 0xc8000)

    def test_segment_targets(self):
        for segment in range(16):
            data, _, _ = assemble('JMP 0x1234\nCALL 0x5678\nBL 0x2:0\nB 0x3:0', segment << 16)
            self.assertEqual(data[:8], bytes((0, 0xf0 | segment, 0x34, 0x12, 1, 0xf0 | segment, 0x78, 0x56)))
            self.roundtrip(data, segment << 16)
        data, _, _ = assemble('CALL_SYS 0x1234', 0xf8000)
        self.assertEqual(data.hex(), '01f03412')

    def test_prefixes(self):
        data, _, _ = assemble('L R3,4:[ER2]\nST ER4,R7:0x8000\nL R0,DSR:-1[ER14]\nL R1,255:[ER0]')
        self.assertEqual(data.hex(), '04e320937f90139400809ffe e890ffff ffe30091'.replace(' ', ''))
        records = self.roundtrip(data)
        self.assertEqual(len(records), 4)
        self.assertIn('R7:', records[1]['text'])
        self.assertIn('DSR:', records[2]['text'])

    def test_relative_limits_and_wrap(self):
        positive, _, _ = assemble('BNE target\n.org 0x4100\ntarget: NOP', 0x4000)
        self.assertEqual(positive[:2].hex(), '7fc8')
        negative, _, _ = assemble('target: NOP\n.org 0x40FE\nBNE target', 0x4000)
        self.assertEqual(negative[-2:].hex(), '80c8')
        wrapped, _, _ = assemble('BNE 0x8:0', 0x8fffe)
        self.assertEqual(wrapped.hex(), '00c8')
        self.roundtrip(wrapped, 0x8fffe)

    def test_no_firmware_source_limits(self):
        source = '\n'.join(f'label_{i}: DW {i}' for i in range(64))
        source += '\nDB "' + 'X' * 100 + '"'
        data, symbols, _ = assemble(source, 0x20100)
        self.assertEqual(len(symbols), 64)
        self.assertEqual(len(data), 228)
        self.assertEqual(assemble('DB 1', 0xfffff)[0], b'\x01')
        self.assertEqual(assemble('DW 0x1234', 1)[0], b'\x34\x12')

    def test_signed_immediates(self):
        data, _, _ = assemble('ADD ER2,#-64\nADD ER2,#63\nADD ER2,#0x7F\nADD SP,#-128\nADD SP,#127\nADD SP,#0xFF')
        self.assertEqual(data.hex(), 'c0e2bfe2ffe280e17fe1ffe1')
        self.roundtrip(data)

    def test_errors_have_source_lines(self):
        cases = [
            'MOV R16,#0', 'MOV ER1,#0', 'PUSH XR2', 'POP QR4',
            'MOV R0,#256', 'MOV ER0,#65536', 'SLL R0,#8', 'TB R0.8',
            'ADD ER0,#64', 'ADD ER0,#-65', 'ADD SP,#128', 'ADD SP,#-129',
            'L R0,32768[ER2]', 'L R0,-32769[ER2]', 'L R0,65536',
            'ST ER0,[ER1]', 'L R0,256:[ER0]', 'JMP 3', 'CALL_SYS 0x100000',
            'BEQ absent', 'BEQ 0x102', 'BNE 0xFFEFE', 'BEQ 0x1:0',
            'DB 256', 'DW 65536', 'DB "unterminated', 'DB "é"', 'DB 1,',
            '.org -1', 'wat R0', '.equ A,B\n.equ B,A',
            'label: NOP\nlabel: NOP', 'DB 1\nNOP', 'DB 0\n.org 0',
        ]
        for source in cases:
            with self.subTest(source=source):
                with self.assertRaisesRegex(ValueError, r'line \d+:'):
                    assemble(source)
        for source, origin in [('NOP', 1), ('CALL 0', 0xffffe), ('DB 1,2', 0xfffff)]:
            with self.subTest(source=source, origin=origin):
                with self.assertRaisesRegex(ValueError, r'line \d+:'):
                    assemble(source, origin)

    def test_unknown_truncated_and_alternate_encodings(self):
        for raw in ('ff', 'ffff', '00f8', '00f834', '04e3', '7f90', '9ffe',
                    '04e31ffe', '04e304e30090', 'ff90', '2f81', '8a90', '00f80100'):
            with self.subTest(raw=raw):
                self.roundtrip(bytes.fromhex(raw), 0x80000)
        self.assertEqual(disassemble(bytes.fromhex('2f81'))[0]['text'], 'DW 0x812F')
        self.roundtrip(bytes(range(255)), 1)

    def test_arbitrary_binary_roundtrip(self):
        rng = random.Random(5800)
        for origin in (0, 1, 0x8fffc, 0xc1234, 0xfff00):
            for size in (0, 1, 2, 3, 7, 64, 255):
                self.roundtrip(bytes(rng.randrange(256) for _ in range(size)), origin)
        words = b''.join(word.to_bytes(2, 'little') for word in range(65536))
        self.roundtrip(words, 0x80000)


if __name__ == '__main__':
    unittest.main()
