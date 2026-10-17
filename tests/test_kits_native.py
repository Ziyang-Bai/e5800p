"""Native entry encoding and ABI boundaries."""

import unittest

from kits import Firmware, cpu


class NativeTests(unittest.TestCase):
    def setUp(self):
        self.fw = Firmware('native', regions=((0x84000, 0x86000),))

    def test_return(self):
        @self.fw.function(native=True)
        def main():
            cpu.r0 = 42
            cpu.r1 = 0
            cpu.ret()

        self.assertEqual(self.fw.link()['blocks'][0]['data'], bytes.fromhex('2a0000011ffe'))

    def test_flag_branch(self):
        @self.fw.function(native=True)
        def main():
            cpu.r0 = 255
            cpu.r0 += 1
            if cpu.eq:
                cpu.branch('zero')
            cpu.r1 = 99
            cpu.label('zero')
            cpu.r1 = 7
            cpu.ret()

        self.assertEqual(self.fw.link()['blocks'][0]['data'],
                         bytes.fromhex('ff00011001c9630107011ffe'))

    def test_register_segment(self):
        @self.fw.function(native=True)
        def main():
            cpu.r11 = cpu.mem8[cpu.r10, cpu.er8]
            cpu.ret()

        self.assertEqual(self.fw.link()['blocks'][0]['data'], bytes.fromhex('af90809b1ffe'))

    def test_signed_steps(self):
        @self.fw.function(native=True)
        def main():
            cpu.er4 += -1
            cpu.sp += -8
            cpu.sp += 8
            cpu.ret()

        self.assertEqual(self.fw.link()['blocks'][0]['data'], bytes.fromhex('ffe4f8e108e11ffe'))

    def test_branch_boundary(self):
        for count in (254, 256):
            with self.subTest(count=count):
                fw = Firmware('branch', regions=((0x84000, 0x86000),))
                padding = bytes(count)

                @fw.function(native=True)
                def main():
                    if cpu.eq:
                        cpu.branch('end')
                    cpu.data(padding)
                    cpu.label('end')
                    cpu.ret()

                if count == 254:
                    self.assertEqual(fw.link()['blocks'][0]['data'],
                                     b'\x7f\xc9' + padding + b'\x1f\xfe')
                else:
                    with self.assertRaises(ValueError):
                        fw.link()

    def test_memory_width(self):
        @self.fw.function(native=True)
        def main():
            cpu.r0 = cpu.mem16[cpu.er2]
            cpu.ret()

        with self.assertRaises(ValueError):
            self.fw.link()

    def test_register_alignment(self):
        @self.fw.function(native=True)
        def main():
            cpu.er3 = cpu.er0
            cpu.ret()

        with self.assertRaises(ValueError):
            self.fw.link()

    def test_host_call(self):
        calls = []

        def host():
            calls.append(1)
            return 42

        @self.fw.function(native=True)
        def main():
            cpu.r0 = host()
            cpu.ret()

        with self.assertRaises(ValueError):
            self.fw.link()
        self.assertEqual(calls, [])

    def test_label_input(self):
        @self.fw.function(native=True)
        def main():
            cpu.label('end\nMOV R0,#1')
            cpu.ret()

        with self.assertRaises(ValueError):
            self.fw.link()

    def test_call_requires_explicit_abi(self):
        @self.fw.function(native=True)
        def native():
            cpu.er14 = 0
            cpu.ret()

        @self.fw.function
        def main():
            return native()

        with self.assertRaises(ValueError):
            self.fw.link()


if __name__ == '__main__':
    unittest.main()
