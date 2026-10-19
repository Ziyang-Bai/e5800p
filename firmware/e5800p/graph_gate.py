"""Caller-limited MODE7 selector and native TABLE continuation."""

from kits import cpu

from .ui import ROM_REFRESH, SCANNER_ADDRESS

SELECT_FRAME = 464


def install(fw):
    @fw.function(native=True)
    def mode_screen_save():
        """Extend regular MODE only; leave the caller-sensitive logo hook intact."""
        cpu.push(cpu.lr)
        cpu.push(cpu.xr0)
        cpu.er2 = cpu.sp
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er2, 4)]
        cpu.compare(cpu.r0, 0xC4)
        cpu.compare_carry(cpu.r1, 0x78)
        if cpu.ne:
            cpu.branch('forward')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er2, 6)]
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.branch('forward')
        cpu.pop(cpu.xr0)
        cpu.call('fn_logo__save')
        cpu.call(0x1210A)
        cpu.label('menu')
        cpu.call('fn_mode_select')
        cpu.compare(cpu.r0, 0x39)
        if cpu.eq:
            cpu.call('fn_apps')
            cpu.branch('menu')
        cpu.compare(cpu.r0, 0xFD)
        if cpu.eq:
            cpu.branch('more')
        cpu.compare(cpu.r0, 0xFE)
        if cpu.eq:
            cpu.branch('more')
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.er0 = 0
            cpu.branch('done')
        cpu.r0 += 0xCF
        cpu.r1 = 0
        cpu.er2 = 0xFF96
        cpu.er2 += cpu.er0
        cpu.r0 = cpu.mem8[12, cpu.er2]
        cpu.branch('done')
        cpu.label('more')
        cpu.call('more_select')
        cpu.label('done')
        cpu.pop(cpu.lr)
        cpu.jump(0x078CC)
        cpu.label('forward')
        cpu.pop(cpu.xr0)
        cpu.pop(cpu.lr)
        cpu.jump('fn_logo')

        # Enter native MODE's second page with its original saved-register frame.
        cpu.label('more_select')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.er12)
        cpu.push(cpu.er8)
        cpu.r5 = 1
        cpu.jump(0x0777E)

    @fw.function(native=True)
    def mode_select():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.sp += -64
        cpu.sp += -4
        cpu.er14 = cpu.sp
        cpu.er0 = cpu.mem16[0, 0x80A0]
        cpu.mem16[0, cpu.offset(cpu.er14, 64)] = cpu.er0
        cpu.r0 = cpu.mem8[0, 0x80A2]
        cpu.mem8[0, cpu.offset(cpu.er14, 66)] = cpu.r0
        cpu.r0 = 0
        cpu.mem8[0, 0x80A1] = cpu.r0
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_copy_text')
        cpu.data(b'MODE 1CMP 2BASE\0')
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.call('fn_apps_copy_text')
        cpu.data(b'3SD 4REG 5PROG\0\0')
        cpu.er0 = cpu.er14
        cpu.er0 += 32
        cpu.call('fn_apps_copy_text')
        cpu.data(b'6REC 7TBL 8EQN\0\0')
        cpu.er0 = cpu.er14
        cpu.er0 += 48
        cpu.call('fn_apps_copy_text')
        cpu.data(b'9APPS v>:MORE\0')
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_screen')
        cpu.label('key')
        cpu.call(SCANNER_ADDRESS)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.branch('out')
        cpu.compare(cpu.r0, 0xFD)
        if cpu.eq:
            cpu.branch('out')
        cpu.compare(cpu.r0, 0xFE)
        if cpu.eq:
            cpu.branch('out')
        cpu.compare(cpu.r0, 0x31)
        if cpu.lt:
            cpu.branch('key')
        cpu.compare(cpu.r0, 0x39)
        if cpu.gt:
            cpu.branch('key')
        cpu.label('out')
        cpu.mem8[0, cpu.offset(cpu.er14, 67)] = cpu.r0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 64)]
        cpu.mem16[0, 0x80A0] = cpu.er0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 66)]
        cpu.mem8[0, 0x80A2] = cpu.r0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 67)]
        cpu.sp += 64
        cpu.sp += 4
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def graph_mode_gate():
        cpu.push(cpu.lr)
        cpu.push(cpu.qr0)
        cpu.push(cpu.qr8)
        cpu.er2 = cpu.sp
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er2, 16)]
        cpu.compare(cpu.r0, 0xB2)
        cpu.compare_carry(cpu.r1, 0x7D)
        if cpu.ne:
            cpu.jump('table')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er2, 18)]
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('table')
        cpu.label('select')
        cpu.call('fn_graph_mode_select')
        cpu.compare(cpu.r0, 0x32)
        if cpu.eq:
            cpu.jump('table')
        cpu.compare(cpu.r0, 0x31)
        if cpu.ne:
            cpu.jump('cancel')

        # Keep the entry snapshot for TABLE even after a GRAPH session.
        cpu.er2 = cpu.sp
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er2, 8)]
        cpu.er4 = cpu.mem16[0, cpu.offset(cpu.er2, 12)]
        cpu.er6 = cpu.mem16[0, cpu.offset(cpu.er2, 14)]
        cpu.er8 = cpu.mem16[0, cpu.er2]
        cpu.er10 = cpu.mem16[0, cpu.offset(cpu.er2, 2)]
        cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er2, 4)]
        cpu.er14 = cpu.mem16[0, cpu.offset(cpu.er2, 6)]
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er2, 10)]
        cpu.call('original')
        cpu.call('fn_graph')
        cpu.jump('select')

        cpu.label('cancel')
        cpu.r0 = 0x81
        cpu.mem8[0, 0x8091] = cpu.r0
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.qr0)
        cpu.pop(cpu.lr)
        # TABLE's saved registers precede its 0x36-byte local frame.
        cpu.pop(cpu.er8)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr4)
        cpu.sp = cpu.er14
        cpu.pop(cpu.er14)
        cpu.pop(cpu.pc)

        cpu.label('table')
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.qr0)
        cpu.pop(cpu.lr)
        cpu.label('original')
        cpu.push(cpu.lr)
        cpu.push(cpu.er8)
        cpu.jump(0xCFA12)

    @fw.function(native=True)
    def graph_mode_select():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er0 = cpu.sp
        cpu.er2 = SELECT_FRAME
        cpu.r0 -= cpu.r2
        cpu.sub_carry(cpu.r1, cpu.r3)
        cpu.sp = cpu.er0
        cpu.er14 = cpu.er0
        cpu.r0 = cpu.mem8[0, 0x80A0]
        cpu.mem8[0, cpu.offset(cpu.er14, 460)] = cpu.r0
        cpu.r0 = cpu.mem8[0, 0x80A1]
        cpu.mem8[0, cpu.offset(cpu.er14, 461)] = cpu.r0
        cpu.r0 = cpu.mem8[0, 0x80A2]
        cpu.mem8[0, cpu.offset(cpu.er14, 462)] = cpu.r0
        cpu.r0 = cpu.mem8[0, 0x8091]
        cpu.mem8[0, cpu.offset(cpu.er14, 463)] = cpu.r0
        cpu.er0 = cpu.er14
        cpu.er0 += 32
        cpu.er0 += 32
        cpu.call(0xCFA66)
        cpu.call('fn_ui_menu')
        cpu.data(b'GRAPH/TBL\0GRAPH\0TABLE\0\0\0')
        cpu.compare(cpu.r0, 0xFF)
        if cpu.eq:
            cpu.r0 = 0xFA
        else:
            cpu.r0 += 0x31
        cpu.mem8[0, cpu.offset(cpu.er14, 63)] = cpu.r0
        cpu.er0 = cpu.er14
        cpu.er0 += 32
        cpu.er0 += 32
        cpu.call(0xCFAB4)
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 460)]
        cpu.mem8[0, 0x80A0] = cpu.r0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 461)]
        cpu.mem8[0, 0x80A1] = cpu.r0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 462)]
        cpu.mem8[0, 0x80A2] = cpu.r0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 463)]
        cpu.mem8[0, 0x8091] = cpu.r0
        cpu.call(ROM_REFRESH)
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 63)]
        cpu.er2 = SELECT_FRAME
        cpu.er14 += cpu.er2
        cpu.sp = cpu.er14
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
