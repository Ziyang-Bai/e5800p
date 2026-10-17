"""Synthetic firmware tests; no original ROM or Flash files are needed."""

import copy
import hashlib
import os
import runpy
from pathlib import Path
import tempfile
import unittest

from firmware_patch import FLASH_BASE, FLASH_SIZE, build_patchset, export_patchset, patchset_inputs
from nxu8_asm import assemble


class PatchsetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.directory = self.root / 'e5800p'
        original = bytearray(bytes(range(256)) * (FLASH_SIZE // 256))
        self.original = self.checksum(original)
        self.code, _, _ = assemble('entry: MOV R0,#42\nMOV R1,#0\nJMP entry', 0x80200)
        self.rows = [self.region('entry', 0x200, len(self.code), 'code'),
                     self.region('caption', 0x40200, 5, 'data'),
                     self.region('unchanged', 0x300, 8, 'data'),
                     self.region('native_checksum', 0x7fffe, 2, 'data')]
        image = bytearray(self.original)
        image[0x200:0x200 + len(self.code)] = self.code
        image[0x40200:0x40205] = b'HELLO'
        self.image = self.checksum(image)

    @staticmethod
    def region(name, start, size, kind):
        return dict(name=name, physical_start=start, cpu_start=FLASH_BASE + start,
                    size=size, reserved_stop=FLASH_BASE + start + size, kind=kind)

    @staticmethod
    def checksum(image):
        result = bytearray(image)
        result[0x7fffe:] = (sum(result[0x40000:0x7fffe]) & 65535).to_bytes(2, 'little')
        return bytes(result)

    def export(self):
        return export_patchset(self.original, self.image, self.rows, self.directory)

    def manifest(self, manifest):
        (self.directory / 'patchset.py').write_text(f'PATCHSET = {manifest!r}\n', encoding='utf-8')

    def export_blocks(self, blocks, *, symbols=None):
        image = bytearray(self.original)
        for row, data in blocks:
            start = row['physical_start']
            image[start:start + len(data)] = data
        image = self.checksum(image)
        export_patchset(self.original, image, [row for row, _ in blocks], self.directory,
                        symbols=symbols)
        self.assertEqual(build_patchset(self.original, self.directory), image)
        return image

    def test_export_build_roundtrip(self):
        manifest = self.export()
        self.assertEqual(build_patchset(self.original, self.directory), self.image)
        self.assertEqual([row['name'] for row in manifest['regions']], ['entry', 'caption'])
        self.assertEqual(len(list(self.directory.glob('*.asm'))), 2)
        self.assertEqual(runpy.run_path(str(self.directory / 'patchset.py'))['PATCHSET'], manifest)
        self.assertFalse((self.directory / 'manifest.json').exists())
        self.assertEqual([row['source'] for row in manifest['regions']], ['entry.asm', 'caption.asm'])
        self.assertEqual(manifest['original_image_sha256'], hashlib.sha256(self.original).hexdigest())
        self.assertEqual(manifest['result_firmware_sha256'],
                         hashlib.sha256(self.image[:0x4000] + self.image[0x40000:]).hexdigest())
        for row in manifest['regions']:
            start, size = row['physical_start'], row['size']
            self.assertEqual(row['original_sha256'],
                             hashlib.sha256(self.original[start:start + size]).hexdigest())

    def test_editing_assembly_changes_output(self):
        manifest = self.export()
        row = manifest['regions'][0]
        source = 'MOV R0,#43\nMOV R1,#0\nJMP 0x80200\n'
        (self.directory / row['source']).write_text(source, encoding='utf-8')
        result = build_patchset(self.original, self.directory)
        code, _, _ = assemble(source, row['cpu_start'])
        expected = bytearray(self.image)
        expected[0x200:0x200 + len(code)] = code
        self.assertEqual(result, self.checksum(expected))
        self.assertNotEqual(result, self.image)
        self.assertNotEqual(hashlib.sha256(result[:0x4000] + result[0x40000:]).hexdigest(),
                            manifest['result_firmware_sha256'])

    def test_preserves_input_user_banks_and_unrelated_bytes(self):
        self.export()
        base = bytearray(self.original)
        base[0x4000:0x40000] = b'\x69' * (0x40000 - 0x4000)
        result = build_patchset(bytes(base), self.directory)
        expected = bytearray(self.image)
        expected[0x4000:0x40000] = base[0x4000:0x40000]
        self.assertEqual(result, bytes(expected))
        self.assertEqual(len(result), FLASH_SIZE)
        self.assertEqual(base[0x200:0x200 + len(self.code)],
                         self.original[0x200:0x200 + len(self.code)])

    def test_patchset_input_paths(self):
        manifest = self.export()
        self.assertEqual(patchset_inputs(self.directory),
                         [self.directory / 'patchset.py']
                         + [self.directory / row['source'] for row in manifest['regions']])
        manifest['regions'][0]['source'] = '../outside.asm'
        self.manifest(manifest)
        with self.assertRaises(ValueError):
            patchset_inputs(self.directory)

    def test_map_shape_and_checksum(self):
        self.export()
        records = []
        result = build_patchset(self.original, self.directory, map_regions=records)
        self.assertEqual(records, [self.rows[0], self.rows[1], self.rows[3]])
        self.assertEqual(int.from_bytes(result[-2:], 'little'),
                         sum(result[0x40000:0x7fffe]) & 65535)
        self.assertEqual(result[0x7ffe0:0x7fffe], self.original[0x7ffe0:0x7fffe])

    def test_data_edit_recalculates_checksum(self):
        manifest = self.export()
        row = manifest['regions'][1]
        (self.directory / row['source']).write_text('DB 1,2,3,4,5\n', encoding='utf-8')
        result = build_patchset(self.original, self.directory)
        self.assertEqual(result[0x40200:0x40205], bytes((1, 2, 3, 4, 5)))
        self.assertEqual(result, self.checksum(result))
        self.assertNotEqual(result[-2:], self.image[-2:])

    def test_source_version_checked_before_assembly(self):
        manifest = self.export()
        (self.directory / manifest['regions'][0]['source']).unlink()
        for offset in (0, 0x3fff, 0x40000, 0x7fffe):
            with self.subTest(offset=offset):
                base = bytearray(self.original)
                base[offset] ^= 1
                with self.assertRaisesRegex(ValueError, 'version mismatch'):
                    build_patchset(bytes(base), self.directory)

    def test_original_region_hash_rejected(self):
        manifest = self.export()
        manifest['regions'][0]['original_sha256'] = '0' * 64
        self.manifest(manifest)
        with self.assertRaisesRegex(ValueError, 'region hash mismatch'):
            build_patchset(self.original, self.directory)

    def test_fixed_region_size(self):
        manifest = self.export()
        source = self.directory / manifest['regions'][0]['source']
        for text in ('DB 1', 'DB ' + ','.join('1' for _ in range(len(self.code) + 1))):
            with self.subTest(text=text):
                source.write_text(text, encoding='utf-8')
                records = []
                with self.assertRaisesRegex(ValueError, 'size mismatch'):
                    build_patchset(self.original, self.directory, map_regions=records)
                self.assertEqual(records, [])
        source.write_text('not_an_instruction', encoding='utf-8')
        with self.assertRaises(ValueError):
            build_patchset(self.original, self.directory)

    def test_explicit_data_padding(self):
        manifest = self.export()
        row = manifest['regions'][0]
        text = 'RT\nDB ' + ','.join('0xFF' for _ in range(row['size'] - 2))
        (self.directory / row['source']).write_text(text, encoding='utf-8')
        result = build_patchset(self.original, self.directory)
        expected, _, _ = assemble(text, row['cpu_start'])
        self.assertEqual(result[0x200:0x200 + row['size']], expected)

    def test_bad_regions_rejected(self):
        original_manifest = self.export()
        bad_rows = [dict(physical_start=-1), dict(size=0), dict(size=True),
                    dict(reserved_stop=0x80201), dict(cpu_start=0x80201),
                    dict(cpu_start=0x80201, physical_start=0x201),
                    dict(cpu_start=0xffffe, physical_start=0x7fffe),
                    dict(cpu_start=0x100000, physical_start=0x80000),
                    dict(cpu_start=0x8fffe, physical_start=0xfffe),
                    dict(cpu_start=0x85000, physical_start=0x5000), dict(kind='other')]
        for changes in bad_rows:
            with self.subTest(changes=changes):
                manifest = copy.deepcopy(original_manifest)
                row = manifest['regions'][0]
                row.update(changes)
                if 'cpu_start' in changes and 'reserved_stop' not in changes:
                    row['reserved_stop'] = row['cpu_start'] + row['size']
                self.manifest(manifest)
                with self.assertRaises(ValueError):
                    build_patchset(self.original, self.directory)

    def test_overlap_rejected_by_export_and_build(self):
        overlapping = self.region('overlap', 0x202, 2, 'code')
        with self.assertRaisesRegex(ValueError, 'overlap'):
            export_patchset(self.original, self.image, self.rows + [overlapping], self.directory)
        self.assertFalse(self.directory.exists())
        manifest = self.export()
        row = dict(manifest['regions'][0])
        row.update(overlapping)
        manifest['regions'].append(row)
        self.manifest(manifest)
        with self.assertRaisesRegex(ValueError, 'overlap'):
            build_patchset(self.original, self.directory)

    def test_path_escape_rejected(self):
        manifest = self.export()
        paths = ['../outside.asm', '/outside.asm', 'sub/../../outside.asm',
                 'C:/outside.asm', 'C:outside.asm', '..\\outside.asm',
                 '//host/outside.asm', 'sub//entry.asm', './entry.asm',
                 'entry.asm:stream', 'patchset.py', 'sub./entry.asm']
        for source in paths:
            with self.subTest(source=source):
                manifest['regions'][0]['source'] = source
                self.manifest(manifest)
                with self.assertRaises(ValueError):
                    build_patchset(self.original, self.directory)

    def test_symlink_source_rejected(self):
        manifest = self.export()
        source = self.directory / manifest['regions'][0]['source']
        outside = self.root / 'outside.asm'
        source.rename(outside)
        try:
            source.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f'Symlinks unavailable: {exc}')
        with self.assertRaises(ValueError):
            build_patchset(self.original, self.directory)

    def test_duplicate_source_rejected(self):
        manifest = self.export()
        manifest['regions'][1]['source'] = manifest['regions'][0]['source']
        self.manifest(manifest)
        with self.assertRaisesRegex(ValueError, 'Duplicate assembly'):
            build_patchset(self.original, self.directory)

    def test_unexplained_changes_rejected_before_output(self):
        image = bytearray(self.image)
        image[0x500] ^= 1
        with self.assertRaisesRegex(ValueError, 'Unexplained'):
            export_patchset(self.original, self.checksum(image), self.rows, self.directory)
        self.assertFalse(self.directory.exists())

    def test_native_user_bank_changes_rejected(self):
        image = bytearray(self.image)
        image[0x4000] ^= 1
        with self.assertRaisesRegex(ValueError, 'user banks'):
            export_patchset(self.original, bytes(image), self.rows, self.directory)
        rows = self.rows + [self.region('user_data', 0x4000, 1, 'data')]
        with self.assertRaisesRegex(ValueError, 'user banks'):
            export_patchset(self.original, bytes(image), rows, self.directory)
        self.assertFalse(self.directory.exists())

    def test_incorrect_target_checksum_rejected(self):
        image = bytearray(self.image)
        image[-1] ^= 1
        with self.assertRaisesRegex(ValueError, 'checksum'):
            export_patchset(self.original, bytes(image), self.rows, self.directory)
        self.assertFalse(self.directory.exists())

    def test_checksum_is_implicit(self):
        rows = [row for row in self.rows if row['name'] != 'native_checksum']
        export_patchset(self.original, self.image, rows, self.directory)
        self.assertEqual(build_patchset(self.original, self.directory), self.image)

    def test_rejects_existing_outputs(self):
        self.directory.mkdir()
        source = self.directory / 'entry.asm'
        source.write_text('local input', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'already exists'):
            self.export()
        self.assertEqual(source.read_text(encoding='utf-8'), 'local input')
        self.assertFalse((self.directory / 'patchset.py').exists())
        source.unlink()
        self.export()
        with self.assertRaisesRegex(ValueError, 'already exists'):
            self.export()
        self.assertEqual(build_patchset(self.original, self.directory), self.image)

    def test_malformed_and_truncated_code_roundtrips(self):
        blocks = [b'\xff', b'\x00\xe3', b'\x01\xf0', b'\x00\xe3\xff',
                  b'\xff' * 11, bytes(range(256)) + b'\x01']
        for index, data in enumerate(blocks):
            with self.subTest(data=data):
                image = bytearray(self.original)
                image[0x200:0x200 + len(data)] = data
                image = self.checksum(image)
                directory = self.root / str(index)
                rows = [self.region('malformed_code', 0x200, len(data), 'code')]
                export_patchset(self.original, image, rows, directory)
                self.assertEqual(build_patchset(self.original, directory), image)

    def test_invalid_image_sizes(self):
        for image in (b'', self.original[:-1], self.original + b'\x00'):
            with self.subTest(size=len(image)):
                with self.assertRaises(ValueError):
                    export_patchset(image, self.image, self.rows, self.directory)
                with self.assertRaises(ValueError):
                    export_patchset(self.original, image, self.rows, self.directory)
                with self.assertRaises(ValueError):
                    build_patchset(image, self.directory)
        self.assertFalse(self.directory.exists())

    def test_invalid_patchset(self):
        original = self.export()
        for changes in ({'firmware': 'other'}, {'flash_base': None}, {'flash_size': 1},
                        {'original_image_sha256': 'not a hash'}, {'regions': None}):
            with self.subTest(changes=changes):
                manifest = dict(original)
                manifest.update(changes)
                self.manifest(manifest)
                with self.assertRaises(ValueError):
                    build_patchset(self.original, self.directory)

    def test_python_expressions(self):
        manifest = self.export()
        manifest['flash_base'] = None
        manifest['regions'][0]['cpu_start'] = None
        module = (
            'FLASH = 1 << 19\n'
            'CODE_OFFSET = 0x100 + 0x100\n'
            f'PATCHSET = {manifest!r}\n'
            "PATCHSET['flash_base'] = FLASH\n"
            "PATCHSET['regions'][0]['cpu_start'] = FLASH + CODE_OFFSET\n"
        )
        (self.directory / 'patchset.py').write_text(module, encoding='utf-8')
        self.assertEqual(build_patchset(self.original, self.directory), self.image)

    def test_requires_patchset_dictionary(self):
        self.export()
        for source in ('regions = []\n', 'PATCHSET = []\n', 'PATCHSET = None\n'):
            with self.subTest(source=source):
                (self.directory / 'patchset.py').write_text(source, encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'patch description'):
                    build_patchset(self.original, self.directory)

    def test_json_is_not_an_input(self):
        self.export()
        (self.directory / 'manifest.json').write_text('not a manifest', encoding='utf-8')
        self.assertEqual(build_patchset(self.original, self.directory), self.image)
        (self.directory / 'patchset.py').unlink()
        with self.assertRaises(FileNotFoundError):
            build_patchset(self.original, self.directory)

    def test_hardlink_inputs_remain_discoverable(self):
        self.export()
        for name in ('patchset.py', 'entry.asm'):
            path = self.directory / name
            alias = self.root / name
            try:
                os.link(path, alias)
            except OSError as exc:
                self.skipTest(f'Hardlinks unavailable: {exc}')
            self.assertTrue(any(path.samefile(alias) for path in patchset_inputs(self.directory)))

    def test_symlink_description_rejected(self):
        self.export()
        path = self.directory / 'patchset.py'
        outside = self.root / 'outside.py'
        path.rename(outside)
        try:
            path.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f'Symlinks unavailable: {exc}')
        with self.assertRaisesRegex(ValueError, 'symlink'):
            patchset_inputs(self.directory)

    def test_invalid_region_names(self):
        for name in ('bad name', '../entry', 'entry.asm', 'entry:stream', '', 'CON', 'lpt1'):
            with self.subTest(name=name):
                rows = copy.deepcopy(self.rows)
                rows[0]['name'] = name
                with self.assertRaisesRegex(ValueError, 'region name'):
                    export_patchset(self.original, self.image, rows, self.directory)
                self.assertFalse(self.directory.exists())
        rows = copy.deepcopy(self.rows)
        rows[1]['name'] = 'ENTRY'
        with self.assertRaisesRegex(ValueError, 'region name'):
            export_patchset(self.original, self.image, rows, self.directory)

    def test_case_insensitive_output_collision(self):
        self.directory.mkdir()
        path = self.directory / 'ENTRY.asm'
        path.write_text('local input', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'already exists'):
            self.export()
        self.assertEqual(path.read_text(encoding='utf-8'), 'local input')
        self.assertFalse((self.directory / 'patchset.py').exists())

    def test_authored_labels_and_external_symbols(self):
        source = ('CALL_SYS 0x041DA\nCALL 0xC0200\nCALL 0xC0202\n'
                  'BNE 0x80200\nJMP 0x80212\nRET\n')
        code, _, _ = assemble(source, 0x80200)
        helper, _, _ = assemble('NOP\nRET\n', 0xc0200)
        row = self.region('screen_entry', 0x200, len(code), 'code')
        row['labels'] = {'again': 0x80200, 'finished': 0x80212}
        other = self.region('screen_helper', 0x40200, len(helper), 'code')
        other['labels'] = {'return_value': 0xc0202}
        self.export_blocks([(row, code), (other, helper)],
                           symbols={'rom_draw': 0x041da, 'screen_helper__return_value': 0xc0202})
        text = (self.directory / 'screen_entry.asm').read_text(encoding='utf-8')
        encoded, symbols, listing = assemble(text, row['cpu_start'])
        self.assertEqual(encoded, code)
        for name, address in {'SCREEN_ENTRY': 0x80200, 'AGAIN': 0x80200,
                              'FINISHED': 0x80212, 'ROM_DRAW': 0x041da,
                              'SCREEN_HELPER': 0xc0200,
                              'SCREEN_HELPER__RETURN_VALUE': 0xc0202}.items():
            self.assertEqual(symbols[name], address)
        operands = [item['text'].split()[-1] for item in listing[:5]]
        self.assertEqual(operands, ['rom_draw', 'screen_helper',
                                    'screen_helper__return_value', 'screen_entry', 'finished'])
        helper_text = (self.directory / 'screen_helper.asm').read_text(encoding='utf-8')
        _, helper_symbols, _ = assemble(helper_text, other['cpu_start'])
        self.assertEqual(helper_symbols['RETURN_VALUE'], 0xc0202)

    def test_authored_macro_boundary(self):
        code, _, _ = assemble('SUB R0,#1\nJMP 0x80204\n', 0x80200)
        row = self.region('subtract', 0x200, len(code), 'code')
        row['labels'] = {'subtract_value': 0x80204}
        self.export_blocks([(row, code)])
        text = (self.directory / 'subtract.asm').read_text(encoding='utf-8')
        encoded, symbols, listing = assemble(text, 0x80200)
        self.assertEqual(encoded, code)
        self.assertEqual(symbols['SUBTRACT_VALUE'], 0x80204)
        self.assertIn(0x80204, [item['address'] for item in listing])
        self.assertEqual(listing[-1]['text'], 'JMP subtract_value')

    def test_discovered_macro_boundary(self):
        code, _, _ = assemble('SUB R0,#1\nJMP 0x80204\n', 0x80200)
        row = self.region('subtract', 0x200, len(code), 'code')
        self.export_blocks([(row, code)])
        text = (self.directory / 'subtract.asm').read_text(encoding='utf-8')
        encoded, symbols, listing = assemble(text, 0x80200)
        self.assertEqual(encoded, code)
        self.assertEqual(symbols['BRANCH_0004'], 0x80204)
        self.assertIn(0x80204, [item['address'] for item in listing])
        self.assertEqual(listing[-1]['text'], 'JMP branch_0004')

    def test_odd_and_end_labels(self):
        row = self.region('odd_labels', 0x200, len(self.code), 'code')
        row['labels'] = {'high_byte': 0x80201, 'code_end': 0x80200 + len(self.code)}
        self.export_blocks([(row, self.code)])
        text = (self.directory / 'odd_labels.asm').read_text(encoding='utf-8')
        encoded, symbols, listing = assemble(text, 0x80200)
        self.assertEqual(encoded, self.code)
        self.assertEqual(symbols['HIGH_BYTE'], 0x80201)
        self.assertEqual(symbols['CODE_END'], 0x80200 + len(self.code))
        self.assertIn(0x80201, [item['address'] for item in listing])

    def test_unknown_external_target_stays_numeric(self):
        code, _, _ = assemble('CALL_SYS 0x041DA\n', 0x80200)
        row = self.region('unknown_call', 0x200, len(code), 'code')
        self.export_blocks([(row, code)])
        text = (self.directory / 'unknown_call.asm').read_text(encoding='utf-8')
        encoded, symbols, listing = assemble(text, 0x80200)
        self.assertEqual(encoded, code)
        self.assertEqual(symbols, {'UNKNOWN_CALL': 0x80200})
        self.assertEqual(listing[0]['text'].split()[-1], '0x0:0x41DA')

    def test_data_strings_and_labels(self):
        data = b'Hello, "U8";\x00\xffA\x01'
        row = self.region('message', 0x40200, len(data), 'data')
        row['labels'] = {'terminator': 0xc020c}
        self.export_blocks([(row, data)])
        text = (self.directory / 'message.asm').read_text(encoding='utf-8')
        encoded, symbols, listing = assemble(text, 0xc0200)
        self.assertEqual(encoded, data)
        self.assertEqual(symbols['MESSAGE'], 0xc0200)
        self.assertEqual(symbols['TERMINATOR'], 0xc020c)
        self.assertTrue(listing[0]['text'].startswith('DB "'))
        self.assertIn('0x00', listing[1]['text'])

    def test_invalid_labels(self):
        for labels in ([], {'bad label': 0x80200}, {'early': 0x801ff},
                       {'late': 0x80300}, {'bad': True}, {'entry': 0x80202},
                       {'loop': 0x80202, 'LOOP': 0x80204}):
            with self.subTest(labels=labels):
                rows = copy.deepcopy(self.rows)
                rows[0]['labels'] = labels
                with self.assertRaisesRegex(ValueError, 'label'):
                    export_patchset(self.original, self.image, rows, self.directory)
                self.assertFalse(self.directory.exists())

    def test_invalid_external_symbols(self):
        for symbols in ([], {'bad name': 1}, {'rom': -1}, {'rom': 0x100000},
                        {'rom': True}, {'entry': 0}, {'rom': 1, 'ROM': 2}):
            with self.subTest(symbols=symbols):
                with self.assertRaisesRegex(ValueError, 'symbol'):
                    export_patchset(self.original, self.image, self.rows, self.directory,
                                    symbols=symbols)
                self.assertFalse(self.directory.exists())

    def test_symbol_label_collision(self):
        code, _, _ = assemble('CALL_SYS 0x041DA\n', 0x80200)
        row = self.region('screen', 0x200, len(code), 'code')
        row['labels'] = {'rom_draw': 0x80200}
        image = bytearray(self.original)
        image[0x200:0x200 + len(code)] = code
        with self.assertRaisesRegex(ValueError, 'conflicts with label'):
            export_patchset(self.original, self.checksum(image), [row], self.directory,
                            symbols={'rom_draw': 0x041da})
        self.assertFalse(self.directory.exists())


if __name__ == '__main__':
    unittest.main()
