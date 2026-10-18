"""Application package and S4 tests using only synthetic images."""

import struct
import unittest
import zlib

from kits import cpu
from kits.app import (APP_START, APP_STOP, HEADER_SIZE,
                      S4_OFFSET, S4_SIZE, build_app, init_image, install_app,
                      read_app, read_apps, remove_app, restore_s4)
from kits.firmware import Firmware


def package(name='HELLO', address=APP_START, payload=b'\x2a\x00\x00\x01\x1f\xfe',
            entry=0, work=0, stack=512):
    header = struct.pack('<4sHHIIIHHB3s12s', b'E5AP', 1, 44, address, entry,
                         len(payload), work, stack, len(name), b'\0' * 3,
                         name.encode('ascii'))
    return header + struct.pack('<I', zlib.crc32(header + payload)) + payload


def change_header(data, offset, fmt, value):
    result = bytearray(data)
    struct.pack_into(fmt, result, offset, value)
    struct.pack_into('<I', result, 40, zlib.crc32(result[:40] + result[44:]))
    return bytes(result)


class PackageTests(unittest.TestCase):
    @staticmethod
    def firmware(name='HELLO', address=APP_START):
        fw = Firmware(name, regions=((address, address + 0x100),))

        @fw.function(native=True)
        def main():
            cpu.r0 = 42
            cpu.r1 = 0
            cpu.ret()

        return fw

    def test_build_without_image(self):
        data, listing = build_app(self.firmware(), work_bytes=3, stack_bytes=512)
        self.assertEqual(data, package(work=3))
        row = read_app(data)
        self.assertEqual(row['header'], data[:44])
        self.assertEqual(row['payload'], bytes.fromhex('2a 00 00 01 1f fe'))
        self.assertEqual(row['name'], 'HELLO')
        self.assertEqual(row['format'], 1)
        self.assertEqual(row['header_size'], 44)
        self.assertEqual(row['load_address'], APP_START)
        self.assertEqual(row['entry_offset'], 0)
        self.assertEqual(row['payload_size'], 6)
        self.assertEqual(row['work_bytes'], 3)
        self.assertEqual(row['stack_bytes'], 512)
        self.assertEqual(row['name_len'], 5)
        self.assertEqual(row['crc32'], zlib.crc32(data[:40] + data[44:]))

    def test_build_gaps_and_nondefault_entry(self):
        fw = Firmware('GAPS', regions=((APP_START, APP_START + 0x100),))
        fw.data('text', b'ABC', address=APP_START + 1)

        @fw.function(native=True, address=APP_START + 0x20)
        def run():
            cpu.r0 = 7
            cpu.r1 = 0
            cpu.ret()

        data, listing = build_app(fw, entry='run', stack_bytes=0)
        row = read_app(data)
        self.assertEqual(row['load_address'], APP_START + 1)
        self.assertEqual(row['entry_offset'], 0x1f)
        self.assertEqual(row['payload'], b'ABC' + b'\xff' * 28
                         + bytes.fromhex('07 00 00 01 1f fe'))
        self.assertEqual(row['payload_size'], 37)
        self.assertEqual(row['work_bytes'], 0)

    def test_build_entry_must_be_code(self):
        fw = self.firmware()
        fw.data('table', b'12', address=APP_START + 0x40)
        for entry in ('missing', 'table'):
            with self.subTest(entry=entry):
                with self.assertRaisesRegex(ValueError, 'linked code'):
                    build_app(fw, entry=entry, stack_bytes=0)
        with self.assertRaisesRegex(ValueError, 'linked code'):
            build_app(Firmware('EMPTY'), stack_bytes=0)

    def test_build_checks_all_blocks(self):
        for address in (0x90000, APP_STOP - 2, 0xa0100):
            with self.subTest(address=address):
                with self.assertRaises(ValueError):
                    build_app(self.firmware(address=address), stack_bytes=0)
        fw = self.firmware()
        fw.patch(0x80000, b'12', expected=b'34')
        with self.assertRaisesRegex(ValueError, 'linked blocks'):
            build_app(fw, stack_bytes=0)

    def test_build_names_and_budgets(self):
        for name in ('lower', 'ABCDEFGHIJKLM', 'A\x1f', 'A`', '\u00c9'):
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, 'name'):
                    build_app(self.firmware(name), stack_bytes=0)
        for key in ('work_bytes', 'stack_bytes'):
            for value in (-1, 65536, 1.5, True, '1'):
                with self.subTest(key=key, value=value):
                    kwargs = dict(work_bytes=0, stack_bytes=0)
                    kwargs[key] = value
                    with self.assertRaisesRegex(ValueError, key):
                        build_app(self.firmware(), **kwargs)
        row = read_app(build_app(self.firmware(' !012ABC[]^_'),
                                 work_bytes=65535, stack_bytes=65535)[0])
        self.assertEqual(row['name'], ' !012ABC[]^_')
        self.assertEqual(row['stack_bytes'], 65535)
        with self.assertRaises(TypeError):
            build_app(self.firmware())

    def test_read_exact_length_and_crc(self):
        data = package()
        for bad in (b'', data[:43], data[:-1], data + b'\xff',
                    data[:40] + b'\0' * 4 + data[44:],
                    data[:-1] + bytes([data[-1] ^ 1]),
                    data[:20] + b'\x01' + data[21:]):
            with self.subTest(data=bad):
                with self.assertRaises(ValueError):
                    read_app(bad)

    def test_read_structural_errors(self):
        changes = ((0, '4s', b'NOPE'), (4, 'H', 0), (6, 'H', 45),
                   (8, 'I', APP_START - 1), (8, 'I', APP_STOP),
                   (8, 'I', 0xffffffff), (12, 'I', 1), (12, 'I', 6),
                   (12, 'I', 0xffffffff), (16, 'I', 0),
                   (16, 'I', 0xffffffff), (24, 'B', 0), (24, 'B', 13),
                   (25, 'B', 1), (26, 'B', 1), (27, 'B', 1),
                   (28, 'B', 0x1f), (28, 'B', 0x60), (28, 'B', 0xff),
                   (33, 'B', 1), (39, 'B', 1))
        for offset, fmt, value in changes:
            with self.subTest(offset=offset, value=value):
                with self.assertRaises(ValueError):
                    read_app(change_header(package(), offset, '<' + fmt, value))

    def test_read_boundary_and_odd_load(self):
        row = read_app(package(address=APP_STOP - 6))
        self.assertEqual(row['load_address'] + row['payload_size'], APP_STOP)
        row = read_app(package(address=APP_START + 1, entry=1))
        self.assertEqual(row['load_address'] + row['entry_offset'], APP_START + 2)
        with self.assertRaises(ValueError):
            read_app(package(address=APP_START + 1))
        self.assertEqual(read_app(package(name='ABCDEFGHIJKL'))['name_len'], 12)


class ImageTests(unittest.TestCase):
    def setUp(self):
        self.original = bytes(range(256)) * 2048
        self.empty = init_image(self.original)

    def assert_outside_s4(self, image):
        self.assertEqual(image[:S4_OFFSET], self.original[:S4_OFFSET])
        self.assertEqual(image[S4_OFFSET + S4_SIZE:],
                         self.original[S4_OFFSET + S4_SIZE:])
        self.assertEqual(len(image), len(self.original))

    def directory(self, packages):
        image = bytearray(self.empty)
        records = b''.join(data[:44] for data in packages)
        header = struct.pack('<4sHHI', b'E5AD', 1, len(packages), 16 + len(records))
        end = S4_OFFSET + S4_SIZE
        image[end - 16 - len(records):end] = records + header + struct.pack(
            '<I', zlib.crc32(header + records))
        for data in packages:
            address, _, size = struct.unpack_from('<III', data, 8)
            offset = address - 0x80000
            image[offset:offset + size] = data[44:]
        return bytes(image)

    def test_init_and_directory_encoding(self):
        self.assertEqual(read_apps(self.empty), [])
        end = S4_OFFSET + S4_SIZE
        self.assertEqual(self.empty[S4_OFFSET:end - 16], b'\xff' * (S4_SIZE - 16))
        header = struct.pack('<4sHHI', b'E5AD', 1, 0, 16)
        self.assertEqual(self.empty[end - 16:end], header + struct.pack('<I', zlib.crc32(header)))
        self.assert_outside_s4(self.empty)
        with self.assertRaisesRegex(ValueError, 'already initialized'):
            init_image(self.empty)
        with self.assertRaisesRegex(ValueError, 'not initialized'):
            read_apps(self.original)

    def test_install_sorted_directory(self):
        hello = package(work=3)
        other = package('RETURN', address=0x91000, payload=b'\x07\x00\x1f\xfe')
        image = install_app(install_app(self.empty, other), hello)
        self.assertEqual(image, self.directory([hello, other]))
        rows = read_apps(image)
        self.assertEqual([row['name'] for row in rows], ['HELLO', 'RETURN'])
        self.assertEqual([row['modified'] for row in rows], [False, False])
        self.assertEqual(rows[0]['header'] + rows[0]['payload'], hello)
        self.assertEqual(rows[0]['work_bytes'], 3)
        self.assertEqual(rows[1]['header'] + rows[1]['payload'], other)
        self.assert_outside_s4(image)

    def test_install_conflicts_preserve_input(self):
        image = bytearray(install_app(self.empty, package()))
        before = bytes(image)
        for data, replace in ((package(), False),
                              (package('OTHER', address=APP_START + 2), False),
                              (package('OTHER', address=APP_START + 2), True),
                              (package()[:-1], True)):
            with self.subTest(data=data, replace=replace):
                with self.assertRaises(ValueError):
                    install_app(image, data, replace=replace)
                self.assertEqual(image, before)
        with self.assertRaisesRegex(ValueError, r'HELLO.*0x90100.*OTHER.*0x90102'):
            install_app(image, package('OTHER', address=APP_START + 2))

    def test_adjacent_payloads(self):
        image = install_app(self.empty, package())
        image = install_app(image, package('NEXT', address=APP_START + 6))
        self.assertEqual(len(read_apps(image)), 2)

    def test_replace_erases_old_payload(self):
        image = install_app(self.empty, package(payload=b'\x12' * 32))
        image = install_app(image, package('OTHER', address=0x91000))
        new = package(address=APP_START + 16, payload=b'\x34' * 6)
        image = install_app(image, new, replace=True)
        rows = read_apps(image)
        self.assertEqual(rows[0]['header'] + rows[0]['payload'], new)
        offset = APP_START - 0x80000
        self.assertEqual(image[offset:offset + 16], b'\xff' * 16)
        self.assertEqual(image[offset + 22:offset + 32], b'\xff' * 10)
        self.assertEqual(rows[1]['payload'], package()[44:])
        self.assert_outside_s4(image)
        with self.assertRaisesRegex(ValueError, 'overlaps'):
            install_app(image, package(address=0x91000), replace=True)

    def test_replace_can_install_new_name(self):
        image = install_app(self.empty, package(), replace=True)
        self.assertEqual(read_apps(image)[0]['name'], 'HELLO')

    def test_modified_payload_survives_other_operations(self):
        image = bytearray(install_app(self.empty, package()))
        offset = APP_START - 0x80000
        image[offset] &= 0xfd
        modified = bytes(image[offset:offset + 6])
        self.assertNotEqual(modified, package()[44:])
        row = read_apps(image)[0]
        self.assertTrue(row['modified'])
        self.assertEqual(row['header'], package()[:44])
        self.assertEqual(row['payload'], modified)
        with self.assertRaisesRegex(ValueError, 'CRC'):
            read_app(row['header'] + row['payload'])
        image = install_app(image, package('OTHER', address=0x91000))
        image = install_app(image, package('OTHER', address=0x91200), replace=True)
        image = remove_app(image, 'OTHER')
        row = read_apps(image)[0]
        self.assertTrue(row['modified'])
        self.assertEqual(row['payload'], modified)
        self.assert_outside_s4(image)
        replaced = install_app(image, package(), replace=True)
        self.assertFalse(read_apps(replaced)[0]['modified'])
        self.assertEqual(remove_app(image, 'HELLO'), self.empty)

    def test_remove_reclaims_directory_and_payload(self):
        image = install_app(self.empty, package())
        image = install_app(image, package('OTHER', address=0x91000))
        image = remove_app(image, 'HELLO')
        self.assertEqual([row['name'] for row in read_apps(image)], ['OTHER'])
        offset = APP_START - 0x80000
        self.assertEqual(image[offset:offset + 6], b'\xff' * 6)
        end = S4_OFFSET + S4_SIZE
        self.assertEqual(image[end - 16 - 88:end - 16 - 44], b'\xff' * 44)
        self.assert_outside_s4(image)
        self.assertEqual(remove_app(image, 'OTHER'), self.empty)
        with self.assertRaisesRegex(ValueError, 'not found'):
            remove_app(image, 'MISSING')

    def test_directory_growth_checks_existing_payloads(self):
        address = APP_STOP - HEADER_SIZE - 6
        image = install_app(self.empty, package('HIGH', address=address))
        self.assertFalse(read_apps(image)[0]['modified'])
        with self.assertRaisesRegex(ValueError, 'HIGH.*overlaps directory'):
            install_app(image, package())
        with self.assertRaisesRegex(ValueError, 'overlaps directory'):
            install_app(self.empty, package(address=APP_STOP - 6))
        self.assertEqual(remove_app(image, 'HIGH'), self.empty)

    def test_corrupt_directory_crc_and_reserved_prefix(self):
        image = install_app(self.empty, package())
        end = S4_OFFSET + S4_SIZE
        for offset in (end - 1, end - 16 - 44 + 40, end - 16 - 44 + 28, S4_OFFSET):
            with self.subTest(offset=offset):
                bad = bytearray(image)
                bad[offset] ^= 1
                for operation in (read_apps, lambda data: install_app(data, package('NEW')),
                                  lambda data: remove_app(data, 'HELLO')):
                    with self.assertRaises(ValueError):
                        operation(bad)
        bad = bytearray(image)
        bad[end - 1] ^= 1
        with self.assertRaisesRegex(ValueError, 'already initialized'):
            init_image(bad)

    def test_directory_header_errors(self):
        end = S4_OFFSET + S4_SIZE
        for offset, fmt, value in ((0, '4s', b'BAD!'), (4, 'H', 2),
                                   (6, 'H', 1), (6, 'H', 65535),
                                   (8, 'I', 15), (8, 'I', 60),
                                   (8, 'I', 0xffffffff)):
            with self.subTest(offset=offset, value=value):
                bad = bytearray(self.empty)
                struct.pack_into('<' + fmt, bad, end - 16 + offset, value)
                struct.pack_into('<I', bad, end - 4, zlib.crc32(bad[end - 16:end - 4]))
                with self.assertRaises(ValueError):
                    read_apps(bad)

    def test_directory_rejects_invalid_records(self):
        cases = ([package(), package(address=0x91000)],
                 [package('HIGH', address=0x91000), package()],
                 [package(), package('OVERLAP', address=APP_START + 2)],
                 [change_header(package(), 12, '<I', 1)],
                 [change_header(package(), 33, '<B', 1)])
        for packages in cases:
            with self.subTest(packages=packages):
                with self.assertRaises(ValueError):
                    read_apps(self.directory(packages))

    def test_restore_exact_s4(self):
        backup = self.original[S4_OFFSET:S4_OFFSET + S4_SIZE]
        image = install_app(self.empty, package())
        self.assertEqual(restore_s4(image, backup), self.original)
        self.assertEqual(restore_s4(self.original, backup), self.original)
        corrupt = bytearray(image)
        corrupt[S4_OFFSET + S4_SIZE - 1] ^= 1
        self.assertEqual(restore_s4(corrupt, backup), self.original)
        for bad in (b'', backup[:-1], backup + b'\0'):
            with self.subTest(length=len(bad)):
                with self.assertRaisesRegex(ValueError, '65536'):
                    restore_s4(image, bad)

    def test_unallocated_s4_bytes_are_preserved(self):
        image = bytearray(self.empty)
        image[S4_OFFSET + 0x8000:S4_OFFSET + 0x8004] = b'USER'
        before = bytes(image)
        image = install_app(image, package())
        image = install_app(image, package(address=0x91000), replace=True)
        self.assertEqual(remove_app(image, 'HELLO'), before)

    def test_directory_cannot_consume_reserved_prefix(self):
        image = bytearray(self.empty)
        end = S4_OFFSET + S4_SIZE
        header = struct.pack('<4sHHI', b'E5AD', 1, 1484, 16 + 1484 * 44)
        image[end - 16:end] = header + struct.pack('<I', zlib.crc32(header))
        with self.assertRaisesRegex(ValueError, 'directory format or size'):
            read_apps(image)

    def test_operations_require_complete_images(self):
        for image in (b'', self.empty[:-1], self.empty + b'\0'):
            for operation in (read_apps, init_image,
                              lambda data: install_app(data, package()),
                              lambda data: remove_app(data, 'HELLO'),
                              lambda data: restore_s4(data, b'\xff' * S4_SIZE)):
                with self.subTest(length=len(image), operation=operation):
                    with self.assertRaisesRegex(ValueError, '512 KiB'):
                        operation(image)


if __name__ == '__main__':
    unittest.main()
