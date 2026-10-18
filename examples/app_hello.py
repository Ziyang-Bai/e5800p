"""Display HELLO until EXIT, then return 42; build with --stack-bytes 512."""

from kits import Firmware, cpu


fw = Firmware('HELLO', regions=[(0x90100, 0x91000)])

# ROM-A27 interfaces used by firmware/e5800p/ui.py.
ROM_CLEAR = 0x0409A
ROM_DRAW_TEXT = 0x041DA
ROM_REFRESH = 0x043BE
ROM_READ_KEY = 0x1234E
ROM_NORMALIZE_KEY = 0x1249C


@fw.function(native=True, address=0x90100)
def main():
    cpu.push(cpu.lr)
    cpu.push(cpu.er14)
    cpu.sp += -10
    cpu.er14 = cpu.sp
    cpu.r0 = cpu.mem8[0x80A0]
    cpu.mem8[0x00, cpu.offset(cpu.er14, 8)] = cpu.r0
    cpu.r0 = cpu.mem8[0x80A2]
    cpu.mem8[0x00, cpu.offset(cpu.er14, 9)] = cpu.r0
    cpu.r0 = 0x07
    cpu.mem8[0x80A0] = cpu.r0
    cpu.r0 = 0x01
    cpu.mem8[0x80A2] = cpu.r0
    cpu.call(ROM_CLEAR)
    cpu.er0 = 0x4548
    cpu.mem16[cpu.er14] = cpu.er0
    cpu.er0 = 0x4C4C
    cpu.mem16[0x00, cpu.offset(cpu.er14, 2)] = cpu.er0
    cpu.er0 = 0x004F
    cpu.mem16[0x00, cpu.offset(cpu.er14, 4)] = cpu.er0
    cpu.er2 = cpu.er14
    cpu.r0 = 0x00
    cpu.r1 = 0x01
    cpu.call(ROM_DRAW_TEXT)
    cpu.call(ROM_REFRESH)
    cpu.label('key')
    cpu.er0 = cpu.er14
    cpu.er0 += 6
    cpu.call(ROM_READ_KEY)
    cpu.er0 = cpu.er14
    cpu.er0 += 6
    cpu.call(ROM_NORMALIZE_KEY)
    cpu.er0 = cpu.mem16[0x00, cpu.offset(cpu.er14, 6)]
    cpu.compare(cpu.r1, 0x75)
    if cpu.ne:
        cpu.branch('key')
    cpu.compare(cpu.r0, 0x32)
    if cpu.ne:
        cpu.branch('key')
    cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 8)]
    cpu.mem8[0x80A0] = cpu.r0
    cpu.r0 = cpu.mem8[0x00, cpu.offset(cpu.er14, 9)]
    cpu.mem8[0x80A2] = cpu.r0
    cpu.er0 = 42
    cpu.sp += 10
    cpu.pop(cpu.er14)
    cpu.pop(cpu.pc)
