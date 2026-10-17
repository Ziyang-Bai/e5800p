"""Firmware DSL linking and synthetic-image tests; no calculator images needed."""

import hashlib
import os
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

from kits.firmware import Firmware
from kits.model import Function


class FirmwareTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.original = bytes(range(256)) * 2048
        self.input = self.root / 'original.bin'
        self.output = self.root / 'firmware.bin'
        self.listing = self.root / 'firmware.asm'
        self.input.write_bytes(self.original)

    @staticmethod
    def firmware():
        fw = Firmware('test', regions=((0x84000, 0x85000),))

        @fw.function
        def answer():
            return 42

        return fw, answer

    def test_decorator_and_deterministic_link(self):
        fw, answer = self.firmware()
        self.assertIsInstance(answer, Function)
        self.assertIs(answer.owner, fw)
        self.assertEqual(fw.functions, [answer])
        first = fw.link()
        self.assertEqual(fw.link(), first)
        self.assertEqual(first['symbols'], {'answer': 0x84000})
        block = first['blocks'][0]
        self.assertEqual(block['name'], 'answer')
        self.assertEqual(block['address'], 0x84000)

    def test_fixed_entries_placed_before_dynamic(self):
        fw, answer = self.firmware()

        @fw.function(address=0x84000)
        def fixed():
            return 7

        linked = fw.link()
        fixed_block = next(block for block in linked['blocks'] if block['name'] == 'fixed')
        self.assertEqual(linked['symbols']['fixed'], 0x84000)
        self.assertEqual(linked['symbols']['answer'], 0x84000 + len(fixed_block['data']))

    def test_forward_calls_link_to_final_address(self):
        fw = Firmware('calls', regions=((0x84000, 0x85000),))

        @fw.function
        def caller():
            return callee()

        @fw.function(address=0x84400)
        def callee():
            return 42

        linked = fw.link()
        self.assertEqual(linked['symbols']['callee'], 0x84400)
        self.assertIn(b'\x01\xf8\x00\x44', linked['blocks'][0]['data'])

    def test_regions_are_sorted_first_fit(self):
        fw = Firmware('first fit', regions=((0x90000, 0x90100), (0x84001, 0x84100)))

        @fw.function
        def entry():
            return 42

        self.assertEqual(fw.regions, ((0x84001, 0x84100), (0x90000, 0x90100)))
        self.assertEqual(fw.link()['symbols']['entry'], 0x84002)

    def test_dynamic_function_skips_bank_boundary(self):
        fw = Firmware('bank', regions=((0x8fffe, 0x90100),))

        @fw.function
        def entry():
            return 42

        self.assertEqual(fw.link()['symbols']['entry'], 0x90000)

    def test_fixed_function_cannot_cross_bank(self):
        fw = Firmware('bank', regions=((0x8fffe, 0x90100),))

        @fw.function(address=0x8fffe)
        def entry():
            return 42

        with self.assertRaisesRegex(ValueError, 'bank boundary'):
            fw.link()

    def test_no_implicit_regions(self):
        for address in (None, 0x84000):
            with self.subTest(address=address):
                fw = Firmware('no ownership')

                @fw.function(address=address)
                def entry():
                    return 42

                with self.assertRaisesRegex(ValueError, 'declared regions'):
                    fw.link()

    def test_not_enough_space(self):
        fw = Firmware('small', regions=((0x84000, 0x84002),))

        @fw.function
        def entry():
            return 42

        with self.assertRaises(ValueError):
            fw.link()

    def test_duplicate_names(self):
        fw, answer = self.firmware()
        with self.assertRaisesRegex(ValueError, 'Duplicate function'):
            fw.function(answer.fn)

    def test_invalid_regions_and_addresses(self):
        for regions in (((0x7ffff, 0x80004),), ((0x84000, 0x84000),),
                        ((0xfffdf, 0xfffe1),), ((0xffffe, 0x100000),),
                        ((0x84000, 0x84100), (0x84080, 0x84200)),
                        ((0x84000, 1.0),)):
            with self.subTest(regions=regions):
                with self.assertRaises(ValueError):
                    Firmware('invalid', regions=regions)
        fw = Firmware('invalid')
        for address in (0x84001, 0x40000, 0xfffe0, True):
            with self.subTest(address=address):
                with self.assertRaises(ValueError):
                    fw.function(address=address)

    def test_patches_reserve_space_before_functions(self):
        fw, answer = self.firmware()
        fw.patch(0x84000, b'abc', expected=b'xyz')
        self.assertEqual(fw.link()['symbols']['answer'], 0x84004)

    def test_overlapping_patches_and_hooks(self):
        fw = Firmware('overlap')
        fw.patch(0x80200, b'1234', expected=b'0000')
        fw.hook(0x80202, 0x84000, expected=b'0000')
        with self.assertRaisesRegex(ValueError, 'overlaps'):
            fw.link()

    def test_fixed_function_overlaps_patch(self):
        fw = Firmware('overlap', regions=((0x84000, 0x84100),))
        fw.patch(0x84000, b'12', expected=b'00')

        @fw.function(address=0x84000)
        def entry():
            return 42

        with self.assertRaisesRegex(ValueError, 'overlaps'):
            fw.link()

    def test_fixed_functions_overlap(self):
        fw = Firmware('overlap', regions=((0x84000, 0x84100),))

        @fw.function(address=0x84000)
        def first():
            return 1

        @fw.function(address=0x84000)
        def second():
            return 2

        with self.assertRaisesRegex(ValueError, 'overlaps'):
            fw.link()

    def test_compiler_size_change_is_rejected(self):
        fw, answer = self.firmware()
        with patch('kits.compiler.compile_function', side_effect=[(b'\x1f\xfe', 'RET'),
                                                                 (b'\x00' * 4, 'RET')]):
            with self.assertRaisesRegex(ValueError, 'size changed'):
                fw.link()

    def test_hook_encodings(self):
        fw, answer = self.firmware()
        fw.hook(0x80200, answer, expected=b'\x00' * 4)
        fw.hook(0x80204, 0x84000, expected=b'\x00' * 4, call=False)
        fw.hook(0x80208, 0x1234, expected=b'\x00' * 4)
        linked = fw.link()
        self.assertEqual([block['data'] for block in linked['blocks'][:3]],
                         [b'\x01\xf8\x00\x40', b'\x00\xf8\x00\x40',
                          b'\x01\xf0\x34\x12'])

    def test_invalid_hooks(self):
        fw, answer = self.firmware()
        other = Firmware('other')
        with self.assertRaisesRegex(ValueError, 'registered'):
            other.hook(0x80200, answer, expected=b'1234')
        for address, target, expected in ((0x80201, 0x84000, b'1234'),
                                           (0x8fffe, 0x84000, b'1234'),
                                           (0x80200, 0x84001, b'1234'),
                                           (0x80200, 0x40000, b'1234'),
                                           (0x80200, 0x84000, b'123')):
            with self.subTest(address=address, target=target, expected=expected):
                with self.assertRaises(ValueError):
                    fw.hook(address, target, expected=expected)

    def test_patch_requires_exact_nonempty_bytes(self):
        fw = Firmware('patch')
        for address, data, expected in ((0x80200, b'12', b'1'),
                                        (0x80200, b'', b''),
                                        (0x7ffff, b'x', b'x'),
                                        (0xfffdf, b'12', b'12'),
                                        (0xfffe0, b'x', b'x'),
                                        (0xffffe, b'12', b'12')):
            with self.subTest(address=address, data=data):
                with self.assertRaises(ValueError):
                    fw.patch(address, data, expected=expected)
        with self.assertRaises(TypeError):
            fw.patch(0x80200, 2, expected=b'12')
        with self.assertRaises(TypeError):
            fw.patch(0x80200, b'12')

    def test_build_preserves_undeclared_bytes(self):
        fw, answer = self.firmware()
        fw.patch(0xc0201, b'hello', expected=self.original[0x40201:0x40206])
        fw.hook(0x80200, answer, expected=self.original[0x200:0x204])
        self.output = self.root / 'build' / 'firmware.bin'
        self.listing = self.root / 'listing' / 'firmware.asm'
        result = fw.build(self.input, self.output, listing=self.listing)
        expected = bytearray(self.original)
        for block in result['blocks']:
            offset = block['address'] - 0x80000
            expected[offset:offset + len(block['data'])] = block['data']
        expected[-2:] = (sum(expected[0x40000:0x7fffe]) & 65535).to_bytes(2, 'little')
        image = self.output.read_bytes()
        self.assertEqual(image, expected)
        self.assertEqual(len(image), 512 * 1024)
        self.assertEqual(image[0x7ffe0:0x7fffe], self.original[0x7ffe0:0x7fffe])
        self.assertEqual(self.input.read_bytes(), self.original)
        self.assertEqual(result['sha256'], hashlib.sha256(image).hexdigest())
        self.assertEqual(result['output'], str(self.output))
        self.assertEqual(fw.build(self.input, self.output)['sha256'], result['sha256'])

    def test_patches_without_functions_or_compiler(self):
        fw = Firmware('data only')
        data = bytearray(b'ABC')
        fw.patch(0x80201, data, expected=self.original[0x201:0x204])
        data[:] = b'XYZ'
        with patch.dict('sys.modules', {'kits.compiler': None}):
            fw.build(self.input, self.output)
        self.assertEqual(self.output.read_bytes()[0x201:0x204], b'ABC')

    def test_bad_signature_preserves_existing_outputs(self):
        for hook in (False, True):
            with self.subTest(hook=hook):
                fw = Firmware('signature')
                if hook:
                    fw.hook(0x80200, 0x84000, expected=b'fail')
                else:
                    fw.patch(0x80200, b'code', expected=b'fail')
                self.output.write_bytes(b'old image')
                self.listing.write_text('old listing', encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'signature mismatch'):
                    fw.build(self.input, self.output, listing=self.listing)
                self.assertEqual(self.output.read_bytes(), b'old image')
                self.assertEqual(self.listing.read_text(encoding='utf-8'), 'old listing')

    def test_invalid_input_size(self):
        for size in (0, 0x7ffff, 0x80001):
            with self.subTest(size=size):
                self.input.write_bytes(b'\x00' * size)
                with self.assertRaisesRegex(ValueError, '512 KiB'):
                    Firmware('size').build(self.input, self.output)
                self.assertFalse(self.output.exists())

    def test_input_and_output_aliases(self):
        fw = Firmware('paths')
        for output, listing in ((self.input, None), (self.output, self.input),
                                (self.output, self.output), (self.root, None)):
            with self.subTest(output=output, listing=listing):
                with self.assertRaises(ValueError):
                    fw.build(self.input, output, listing=listing)
        self.assertEqual(self.input.read_bytes(), self.original)
        self.assertFalse(self.output.exists())

    def test_source_script_is_protected_without_functions(self):
        source = self.root / 'source.py'
        text = "from kits import Firmware\nfw = Firmware('source')\n"
        source.write_text(text, encoding='utf-8')
        fw = runpy.run_path(str(source))['fw']
        for output, listing in ((source, None), (self.output, source)):
            with self.subTest(output=output):
                with self.assertRaisesRegex(ValueError, 'replace an input'):
                    fw.build(self.input, output, listing=listing)
        self.assertEqual(source.read_text(encoding='utf-8'), text)

    def test_decorated_source_file_is_protected(self):
        fw, answer = self.firmware()
        with self.assertRaisesRegex(ValueError, 'replace an input'):
            fw.build(self.input, Path(answer.fn.__code__.co_filename))

    def test_hardlinks_are_rejected(self):
        alias = self.root / 'alias.bin'
        try:
            os.link(self.input, alias)
        except OSError as exc:
            self.skipTest(f'Hardlinks unavailable: {exc}')
        fw = Firmware('hardlink')
        for output, listing in ((alias, None), (self.output, alias)):
            with self.subTest(output=output):
                with self.assertRaisesRegex(ValueError, 'replace an input'):
                    fw.build(self.input, output, listing=listing)
        self.assertEqual(self.input.read_bytes(), self.original)

    def test_output_and_listing_hardlinks_are_rejected(self):
        self.output.write_bytes(b'previous')
        try:
            os.link(self.output, self.listing)
        except OSError as exc:
            self.skipTest(f'Hardlinks unavailable: {exc}')
        with self.assertRaisesRegex(ValueError, 'different'):
            Firmware('hardlink').build(self.input, self.output, listing=self.listing)
        self.assertEqual(self.output.read_bytes(), b'previous')

    def test_source_hardlink_is_protected(self):
        source = self.root / 'source.py'
        source.write_text("from kits import Firmware\nfw = Firmware('source')\n", encoding='utf-8')
        fw = runpy.run_path(str(source))['fw']
        try:
            os.link(source, self.output)
        except OSError as exc:
            self.skipTest(f'Hardlinks unavailable: {exc}')
        with self.assertRaisesRegex(ValueError, 'replace an input'):
            fw.build(self.input, self.output)

    def test_symlink_input_alias_is_rejected(self):
        try:
            self.output.symlink_to(self.input)
        except OSError as exc:
            self.skipTest(f'Symlinks unavailable: {exc}')
        with self.assertRaisesRegex(ValueError, 'replace an input'):
            Firmware('symlink').build(self.input, self.output)
        self.assertEqual(self.input.read_bytes(), self.original)


if __name__ == '__main__':
    unittest.main()
