"""Fixed-layout e5800p logo routines and tables."""

from pathlib import Path

from kits import cpu

ROM_REFRESH = 0x043BE
PBM_PATH = Path(__file__).resolve().with_name('ziyang_bai.pbm')


def read_logo():
    words = PBM_PATH.read_text(encoding='ascii').split()
    if words[:3] != ['P1', '96', '32'] or len(words) != 3075 or any(p not in ('0', '1') for p in words[3:]):
        raise ValueError('Expected a 96x32 plain PBM logo')
    pixels = words[3:]
    return bytes(int(''.join(pixels[i:i + 8]), 2) for i in range(0, len(pixels), 8))


LOGO_BITMAP_LABELS = {
    'logo_bitmap': 0x0,
}


def install(fw):
    fw._sources.add(str(PBM_PATH))
    fw.data('logo_bitmap', read_logo(), address=0x81C86, labels=LOGO_BITMAP_LABELS)

    @fw.function(native=True, address=0x81800)
    def logo():
        cpu.label('logo')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr0)
        cpu.er2 = cpu.sp
        cpu.er2 += 0x04
        cpu.er0 = cpu.mem16[cpu.er2]
        cpu.compare(cpu.r0, 0x58)
        cpu.compare_carry(cpu.r1, 0x77)
        if cpu.eq:
            cpu.branch('develop')
        cpu.compare(cpu.r0, 0xD6)
        cpu.compare_carry(cpu.r1, 0x59)
        if cpu.ne:
            cpu.branch('ordinary')
        cpu.er2 += 0x02
        cpu.er0 = cpu.mem16[cpu.er2]
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('ordinary')
        cpu.pop(cpu.xr0)
        cpu.call('save')
        cpu.call(0x1210A)
        cpu.push(cpu.xr4)
        cpu.r2 = 0x86
        cpu.r3 = 0x1C
        cpu.r4 = 0xE0
        cpu.r5 = 0x80
        cpu.r6 = 0x80
        cpu.r7 = 0x01
        cpu.label('copy')
        cpu.r0 = cpu.mem8[0x08, cpu.er2]
        cpu.mem8[cpu.er4] = cpu.r0
        cpu.er2 += 0x01
        cpu.er4 += 0x01
        cpu.er6 += -1
        if cpu.ne:
            cpu.branch('copy')
        cpu.pop(cpu.xr4)
        cpu.call(ROM_REFRESH)
        cpu.pop(cpu.lr)
        cpu.jump(0x059F6)
        cpu.label('develop')
        cpu.er2 += 0x02
        cpu.er0 = cpu.mem16[cpu.er2]
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('ordinary')
        cpu.pop(cpu.xr0)
        cpu.call('save')
        cpu.push(cpu.er14)
        cpu.call(0x1210A)
        cpu.call('fn_develop_menu')
        cpu.pop(cpu.er14)
        cpu.pop(cpu.lr)
        cpu.jump(0x07760)
        cpu.label('ordinary')
        cpu.pop(cpu.xr0)
        cpu.pop(cpu.lr)
        cpu.label('save')
        cpu.push(cpu.lr)
        cpu.push(cpu.er8)
        cpu.jump(0xCFA6A)
