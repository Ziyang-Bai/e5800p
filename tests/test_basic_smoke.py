"""Offline native-memory parsing checks for the emulator smoke runner."""

import unittest
from unittest.mock import Mock

from tools.basic_smoke import Emulator


class RecordsTests(unittest.TestCase):
    def test_program_source_after_directory(self):
        data = bytearray(0x8000)
        data[0x60:0x66] = b'system'
        data[0x6c:0x70] = (0x40128).to_bytes(4, 'little')
        data[0x70:0x74] = (1).to_bytes(4, 'little')
        source = b'123456789ABCDEG\0'
        payload = b'\x01\0' + len(source).to_bytes(4, 'little') + source
        record = (b'ONE'.ljust(12, b'\0') + (24).to_bytes(4, 'little')
                  + len(payload).to_bytes(4, 'little') + b'\x47\0\0\x0a')
        data[0x128:0x140] = record
        data[0x140:0x140 + len(payload)] = payload
        emu = Emulator.__new__(Emulator)
        emu.call = Mock(return_value={'bytes': list(data)})
        records = emu.records()
        self.assertEqual(list(records), ['ONE'])
        self.assertEqual(bytes.fromhex(records['ONE']['source']), source)


if __name__ == '__main__':
    unittest.main()
