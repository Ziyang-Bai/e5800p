"""S4 application directory, Devlop menu and fixed-address launcher."""

from kits import cpu

from .memory import CALL_BRIDGE_ADDRESS
from .ui import ROM_DRAW_TEXT, ROM_REFRESH, SCANNER_ADDRESS

STACK_LOW = 0x8292
NATIVE_STACK_MARGIN = 900
APP_HEADER_SIZE = 44
DIRECTORY_HEADER = 0xFFF0
MAX_APPS = 1483
# Snapshot: math, workspace pointer, display fields and selected record.
LAUNCH_FRAME = 126
LAUNCH_RESERVE = LAUNCH_FRAME + 2 + 4 + NATIVE_STACK_MARGIN


def install(fw):
    @fw.function(native=True)
    def apps_copy_text():
        """Copy inline NUL text to ER0; skip its even-sized data on return."""
        cpu.er4 = cpu.er0
        cpu.push(cpu.lr)
        cpu.pop(cpu.xr0)
        cpu.label('copy')
        cpu.r3 = cpu.mem8[cpu.r2, cpu.er0]
        cpu.mem8[0, cpu.er4] = cpu.r3
        cpu.er0 += 1
        cpu.er4 += 1
        cpu.compare(cpu.r3, 0)
        if cpu.ne:
            cpu.branch('copy')
        cpu.r3 = cpu.r0
        cpu.r3 &= 1
        if cpu.ne:
            cpu.er0 += 1
        cpu.r3 = 0
        cpu.push(cpu.xr0)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def apps_owned():
        """Return ER0=1 for the app magic, even when the directory is damaged."""
        cpu.er0 = cpu.mem16[9, DIRECTORY_HEADER]
        cpu.er2 = 0x3545
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.branch('no')
        cpu.er0 = cpu.mem16[9, DIRECTORY_HEADER + 2]
        cpu.er2 = 0x4441
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.branch('no')
        cpu.er0 = 1
        cpu.ret()
        cpu.label('no')
        cpu.er0 = 0
        cpu.ret()

    @fw.function(native=True)
    def apps_erase_confirm():
        """EXE returns ER0=1, EXIT returns 0; restore the native screen/font."""
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er0 = cpu.sp
        cpu.er2 = 460
        cpu.r0 -= cpu.r2
        cpu.sub_carry(cpu.r1, cpu.r3)
        cpu.sp = cpu.er0
        cpu.er14 = cpu.er0
        cpu.er0 += 32
        cpu.er0 += 32
        cpu.call(0xCFA66)
        cpu.er2 = cpu.er14
        cpu.r0 = 0
        cpu.r4 = 64
        cpu.label('clear')
        cpu.mem8[0, cpu.er2] = cpu.r0
        cpu.er2 += 1
        cpu.r4 += 0xFF
        if cpu.ne:
            cpu.branch('clear')
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_copy_text')
        cpu.data(b'ERASE APPS?\0')
        cpu.er0 = cpu.er14
        cpu.er0 += 32
        cpu.call('fn_apps_copy_text')
        cpu.data(b'EXE:ERASE\0')
        cpu.er0 = cpu.er14
        cpu.er0 += 48
        cpu.call('fn_apps_copy_text')
        cpu.data(b'EXIT:BACK\0')
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_screen')
        cpu.label('key')
        cpu.call(SCANNER_ADDRESS)
        cpu.compare(cpu.r0, 0xFB)
        if cpu.eq:
            cpu.branch('yes')
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('key')
        cpu.er0 = 0
        cpu.branch('restore')
        cpu.label('yes')
        cpu.er0 = 1
        cpu.label('restore')
        cpu.mem16[0, cpu.offset(cpu.er14, 62)] = cpu.er0
        cpu.er0 = cpu.er14
        cpu.er0 += 32
        cpu.er0 += 32
        cpu.call(0xCFAB4)
        cpu.call(ROM_REFRESH)
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 62)]
        cpu.er2 = 460
        cpu.er14 += cpu.er2
        cpu.sp = cpu.er14
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def apps_crc():
        """Update uncomplemented CRC32 in XR4 over ER2 bytes at 9:ER0."""
        cpu.push(cpu.er8)
        cpu.push(cpu.er10)
        cpu.er2 = cpu.er2
        if cpu.eq:
            cpu.branch('done')
        cpu.label('byte')
        cpu.r8 = cpu.mem8[9, cpu.er0]
        cpu.r4 ^= cpu.r8
        cpu.r8 = 8
        cpu.label('bit')
        cpu.r9 = cpu.r4
        cpu.r9 &= 1
        cpu.r10 = cpu.r5
        cpu.r10 <<= 7
        cpu.r4 >>= 1
        cpu.r4 |= cpu.r10
        cpu.r10 = cpu.r6
        cpu.r10 <<= 7
        cpu.r5 >>= 1
        cpu.r5 |= cpu.r10
        cpu.r10 = cpu.r7
        cpu.r10 <<= 7
        cpu.r6 >>= 1
        cpu.r6 |= cpu.r10
        cpu.r7 >>= 1
        cpu.compare(cpu.r9, 0)
        if cpu.eq:
            cpu.branch('next')
        cpu.r4 ^= 0x20
        cpu.r5 ^= 0x83
        cpu.r6 ^= 0xB8
        cpu.r7 ^= 0xED
        cpu.label('next')
        cpu.r8 += 0xFF
        if cpu.ne:
            cpu.branch('bit')
        cpu.er0 += 1
        cpu.er2 += -1
        if cpu.ne:
            cpu.branch('byte')
        cpu.label('done')
        cpu.pop(cpu.er10)
        cpu.pop(cpu.er8)
        cpu.ret()

    @fw.function(native=True)
    def apps_header():
        """Check record ER0 against directory start ER2; return status/end."""
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.er12 = cpu.er2
        cpu.er0 = cpu.mem16[9, cpu.er8]
        cpu.er2 = 0x3545
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.jump('bad')
        cpu.er0 = cpu.mem16[9, cpu.offset(cpu.er8, 2)]
        cpu.er2 = 0x5041
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.jump('bad')
        cpu.er0 = cpu.mem16[9, cpu.offset(cpu.er8, 4)]
        cpu.er2 = 1
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.jump('bad')
        cpu.er0 = cpu.mem16[9, cpu.offset(cpu.er8, 6)]
        cpu.er2 = APP_HEADER_SIZE
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.jump('bad')
        cpu.er0 = cpu.mem16[9, cpu.offset(cpu.er8, 10)]
        cpu.er2 = 9
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.jump('bad')
        cpu.er0 = cpu.mem16[9, cpu.offset(cpu.er8, 14)]
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('bad')
        cpu.er0 = cpu.mem16[9, cpu.offset(cpu.er8, 18)]
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('bad')
        cpu.er4 = cpu.mem16[9, cpu.offset(cpu.er8, 8)]
        cpu.er0 = 0x0100
        cpu.compare(cpu.er4, cpu.er0)
        if cpu.lt:
            cpu.jump('bad')
        cpu.er6 = cpu.mem16[9, cpu.offset(cpu.er8, 16)]
        cpu.er6 = cpu.er6
        if cpu.eq:
            cpu.jump('bad')
        cpu.er10 = cpu.er4
        cpu.er10 += cpu.er6
        cpu.er0 = 0
        cpu.add_carry(cpu.r0, 0)
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('bad')
        cpu.compare(cpu.er10, cpu.er12)
        if cpu.gt:
            cpu.jump('bad')
        cpu.er0 = cpu.mem16[9, cpu.offset(cpu.er8, 12)]
        cpu.compare(cpu.er0, cpu.er6)
        if cpu.ge:
            cpu.jump('bad')
        cpu.er0 += cpu.er4
        cpu.r0 &= 1
        if cpu.ne:
            cpu.jump('bad')
        cpu.r0 = cpu.mem8[9, cpu.offset(cpu.er8, 25)]
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.jump('bad')
        cpu.er0 = cpu.mem16[9, cpu.offset(cpu.er8, 26)]
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('bad')
        cpu.r4 = cpu.mem8[9, cpu.offset(cpu.er8, 24)]
        cpu.compare(cpu.r4, 1)
        if cpu.lt:
            cpu.jump('bad')
        cpu.compare(cpu.r4, 12)
        if cpu.gt:
            cpu.jump('bad')
        cpu.er8 += 28
        cpu.r5 = 12
        cpu.label('name')
        cpu.r0 = cpu.mem8[9, cpu.er8]
        cpu.compare(cpu.r0, 0x20)
        if cpu.lt:
            cpu.jump('bad')
        cpu.compare(cpu.r0, 0x5F)
        if cpu.gt:
            cpu.jump('bad')
        cpu.er8 += 1
        cpu.r5 += 0xFF
        cpu.r4 += 0xFF
        if cpu.ne:
            cpu.branch('name')
        cpu.compare(cpu.r5, 0)
        if cpu.eq:
            cpu.branch('good')
        cpu.label('padding')
        cpu.r0 = cpu.mem8[9, cpu.er8]
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('bad')
        cpu.er8 += 1
        cpu.r5 += 0xFF
        if cpu.ne:
            cpu.branch('padding')
        cpu.label('good')
        cpu.er2 = cpu.er10
        cpu.er0 = 0
        cpu.branch('out')
        cpu.label('bad')
        cpu.er0 = 2
        cpu.label('out')
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.ret()

    @fw.function(native=True)
    def apps_check():
        """R0=0/1 not apps/2 bad; ER2=start, ER4=count; preserve R6..R15."""
        cpu.push(cpu.lr)
        cpu.push(cpu.er6)
        cpu.push(cpu.qr8)
        cpu.er0 = cpu.mem16[9, DIRECTORY_HEADER]
        cpu.er2 = 0x3545
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.jump('not_apps')
        cpu.er0 = cpu.mem16[9, DIRECTORY_HEADER + 2]
        cpu.er2 = 0x4441
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.jump('not_apps')
        cpu.er0 = cpu.mem16[9, DIRECTORY_HEADER + 4]
        cpu.er2 = 1
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.jump('bad')
        cpu.er10 = cpu.mem16[9, DIRECTORY_HEADER + 6]
        cpu.er0 = MAX_APPS
        cpu.compare(cpu.er10, cpu.er0)
        if cpu.gt:
            cpu.jump('bad')
        cpu.er0 = cpu.mem16[9, DIRECTORY_HEADER + 10]
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('bad')
        cpu.er6 = 16
        cpu.er8 = cpu.er10
        cpu.er8 = cpu.er8
        if cpu.eq:
            cpu.branch('size')
        cpu.label('count')
        cpu.er6 += APP_HEADER_SIZE
        cpu.er8 += -1
        if cpu.ne:
            cpu.branch('count')
        cpu.label('size')
        cpu.er0 = cpu.mem16[9, DIRECTORY_HEADER + 8]
        cpu.compare(cpu.er0, cpu.er6)
        if cpu.ne:
            cpu.jump('bad')
        cpu.er12 = 0
        cpu.r12 -= cpu.r6
        cpu.sub_carry(cpu.r13, cpu.r7)
        cpu.er0 = 0
        cpu.label('prefix')
        cpu.r2 = cpu.mem8[9, cpu.er0]
        cpu.compare(cpu.r2, 0xFF)
        if cpu.ne:
            cpu.jump('bad')
        cpu.er0 += 1
        cpu.compare(cpu.r1, 1)
        if cpu.ne:
            cpu.branch('prefix')
        cpu.er4 = 0xFFFF
        cpu.er6 = 0xFFFF
        cpu.er0 = DIRECTORY_HEADER
        cpu.er2 = 12
        cpu.call('fn_apps_crc')
        cpu.er0 = cpu.er12
        cpu.er2 = DIRECTORY_HEADER
        cpu.r2 -= cpu.r12
        cpu.sub_carry(cpu.r3, cpu.r13)
        cpu.call('fn_apps_crc')
        cpu.r4 ^= 0xFF
        cpu.r5 ^= 0xFF
        cpu.r6 ^= 0xFF
        cpu.r7 ^= 0xFF
        cpu.er0 = cpu.mem16[9, DIRECTORY_HEADER + 12]
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.ne:
            cpu.jump('bad')
        cpu.er0 = cpu.mem16[9, DIRECTORY_HEADER + 14]
        cpu.compare(cpu.er0, cpu.er6)
        if cpu.ne:
            cpu.jump('bad')
        cpu.er8 = cpu.er12
        cpu.er14 = 0x0100
        cpu.label('record')
        cpu.er0 = DIRECTORY_HEADER
        cpu.compare(cpu.er8, cpu.er0)
        if cpu.eq:
            cpu.jump('good')
        cpu.er0 = cpu.er8
        cpu.er2 = cpu.er12
        cpu.call('fn_apps_header')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.jump('bad')
        cpu.er0 = cpu.mem16[9, cpu.offset(cpu.er8, 8)]
        cpu.compare(cpu.er0, cpu.er14)
        if cpu.lt:
            cpu.jump('bad')
        cpu.er14 = cpu.er2
        cpu.er4 = cpu.er12
        cpu.label('prior')
        cpu.compare(cpu.er4, cpu.er8)
        if cpu.eq:
            cpu.branch('next_record')
        cpu.er0 = cpu.er4
        cpu.er0 += 28
        cpu.er2 = cpu.er8
        cpu.er2 += 28
        cpu.r6 = 12
        cpu.label('same_name')
        cpu.r7 = cpu.mem8[9, cpu.er0]
        cpu.r11 = cpu.mem8[9, cpu.er2]
        cpu.compare(cpu.r7, cpu.r11)
        if cpu.ne:
            cpu.branch('next_prior')
        cpu.er0 += 1
        cpu.er2 += 1
        cpu.r6 += 0xFF
        if cpu.ne:
            cpu.branch('same_name')
        cpu.jump('bad')
        cpu.label('next_prior')
        cpu.er4 += APP_HEADER_SIZE
        cpu.branch('prior')
        cpu.label('next_record')
        cpu.er8 += APP_HEADER_SIZE
        cpu.jump('record')
        cpu.label('good')
        cpu.er2 = cpu.er12
        cpu.er4 = cpu.mem16[9, DIRECTORY_HEADER + 6]
        cpu.er0 = 0
        cpu.branch('out')
        cpu.label('not_apps')
        cpu.er0 = 1
        cpu.branch('out')
        cpu.label('bad')
        cpu.er0 = 2
        cpu.label('out')
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.er6)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def apps_modified():
        """ER0 is a checked record; return R0=1 if its code CRC changed."""
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.er8)
        cpu.er8 = cpu.er0
        cpu.er4 = 0xFFFF
        cpu.er6 = 0xFFFF
        cpu.er2 = 40
        cpu.call('fn_apps_crc')
        cpu.er0 = cpu.mem16[9, cpu.offset(cpu.er8, 8)]
        cpu.er2 = cpu.mem16[9, cpu.offset(cpu.er8, 16)]
        cpu.call('fn_apps_crc')
        cpu.r4 ^= 0xFF
        cpu.r5 ^= 0xFF
        cpu.r6 ^= 0xFF
        cpu.r7 ^= 0xFF
        cpu.er0 = cpu.mem16[9, cpu.offset(cpu.er8, 40)]
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.ne:
            cpu.branch('changed')
        cpu.er0 = cpu.mem16[9, cpu.offset(cpu.er8, 42)]
        cpu.compare(cpu.er0, cpu.er6)
        if cpu.ne:
            cpu.branch('changed')
        cpu.er0 = 0
        cpu.branch('out')
        cpu.label('changed')
        cpu.er0 = 1
        cpu.label('out')
        cpu.pop(cpu.er8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def apps_launch():
        """Checked record ER0; ER0=application return, ER2=0 or 1 (no RAM)."""
        cpu.push(cpu.lr)
        cpu.push(cpu.qr0)
        cpu.push(cpu.qr8)
        cpu.push(cpu.ea)
        cpu.r2 = cpu.psw
        cpu.push(cpu.er2)
        cpu.er8 = cpu.er0
        # Carry is retained in ER6: a 65535-byte request must not wrap to zero.
        cpu.er4 = cpu.mem16[9, cpu.offset(cpu.er8, 20)]
        cpu.er6 = 0
        cpu.er4 += 1
        cpu.add_carry(cpu.r6, 0)
        cpu.r4 &= 0xFE
        cpu.er10 = cpu.er4
        cpu.er0 = cpu.mem16[9, cpu.offset(cpu.er8, 22)]
        cpu.er4 += cpu.er0
        cpu.add_carry(cpu.r6, 0)
        cpu.r0 &= 1
        cpu.r1 = 0
        cpu.er4 += cpu.er0
        cpu.add_carry(cpu.r6, 0)
        cpu.er0 = STACK_LOW + LAUNCH_RESERVE
        cpu.er4 += cpu.er0
        cpu.add_carry(cpu.r6, 0)
        cpu.er6 = cpu.er6
        if cpu.ne:
            cpu.jump('memory')
        cpu.er0 = cpu.sp
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.lt:
            cpu.jump('memory')
        cpu.er2 = LAUNCH_FRAME
        cpu.r0 -= cpu.r2
        cpu.sub_carry(cpu.r1, cpu.r3)
        cpu.sp = cpu.er0
        cpu.er14 = cpu.er0
        cpu.mem16[0, cpu.offset(cpu.er14, 124)] = cpu.er8
        cpu.er2 = cpu.er14
        cpu.er0 = 0x8000
        cpu.r4 = 0x70
        cpu.label('save_math')
        cpu.r5 = cpu.mem8[0, cpu.er0]
        cpu.mem8[0, cpu.er2] = cpu.r5
        cpu.er0 += 1
        cpu.er2 += 1
        cpu.r4 += 0xFF
        if cpu.ne:
            cpu.branch('save_math')
        cpu.er0 = cpu.mem16[0, 0x8086]
        cpu.mem16[0, cpu.offset(cpu.er14, 112)] = cpu.er0
        cpu.er0 = cpu.mem16[0, 0x807E]
        cpu.mem16[0, cpu.offset(cpu.er14, 114)] = cpu.er0
        cpu.r0 = cpu.mem8[0, 0x808B]
        cpu.mem8[0, cpu.offset(cpu.er14, 116)] = cpu.r0
        cpu.er0 = 0x80A0
        cpu.er2 = cpu.er14
        cpu.er2 += 60
        cpu.er2 += 57
        cpu.r4 = 7
        cpu.label('save_font')
        cpu.r5 = cpu.mem8[0, cpu.er0]
        cpu.mem8[0, cpu.er2] = cpu.r5
        cpu.er0 += 1
        cpu.er2 += 1
        cpu.r4 += 0xFF
        if cpu.ne:
            cpu.branch('save_font')
        cpu.er0 = cpu.er14
        cpu.r0 -= cpu.r10
        cpu.sub_carry(cpu.r1, cpu.r11)
        cpu.sp = cpu.er0
        cpu.er2 = cpu.er0
        cpu.er4 = cpu.er10
        cpu.er4 = cpu.er4
        if cpu.eq:
            cpu.branch('invoke')
        cpu.r6 = 0
        cpu.label('zero_work')
        cpu.mem8[0, cpu.er2] = cpu.r6
        cpu.er2 += 1
        cpu.er4 += -1
        if cpu.ne:
            cpu.branch('zero_work')
        cpu.label('invoke')
        # The anchor survives even applications which clobber every register.
        cpu.push(cpu.er14)
        cpu.er8 = cpu.mem16[0, cpu.offset(cpu.er14, 124)]
        cpu.er4 = cpu.mem16[9, cpu.offset(cpu.er8, 20)]
        cpu.er4 = cpu.er4
        if cpu.eq:
            cpu.er0 = 0
        cpu.er2 = 0
        cpu.er6 = 0
        cpu.er10 = cpu.mem16[9, cpu.offset(cpu.er8, 12)]
        cpu.er8 = cpu.mem16[9, cpu.offset(cpu.er8, 8)]
        cpu.er8 += cpu.er10
        cpu.er10 = 9
        cpu.call(CALL_BRIDGE_ADDRESS)
        cpu.pop(cpu.er14)
        cpu.sp = cpu.er14
        cpu.mem16[0, cpu.offset(cpu.er14, LAUNCH_FRAME + 12)] = cpu.er0
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er14, LAUNCH_FRAME + 14)] = cpu.er0
        cpu.er2 = cpu.er14
        cpu.er0 = 0x8000
        cpu.r4 = 0x70
        cpu.label('restore_math')
        cpu.r5 = cpu.mem8[0, cpu.er2]
        cpu.mem8[0, cpu.er0] = cpu.r5
        cpu.er0 += 1
        cpu.er2 += 1
        cpu.r4 += 0xFF
        if cpu.ne:
            cpu.branch('restore_math')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 112)]
        cpu.mem16[0, 0x8086] = cpu.er0
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 114)]
        cpu.mem16[0, 0x807E] = cpu.er0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 116)]
        cpu.mem8[0, 0x808B] = cpu.r0
        cpu.er0 = 0x80A0
        cpu.er2 = cpu.er14
        cpu.er2 += 60
        cpu.er2 += 57
        cpu.r4 = 7
        cpu.label('restore_font')
        cpu.r5 = cpu.mem8[0, cpu.er2]
        cpu.mem8[0, cpu.er0] = cpu.r5
        cpu.er0 += 1
        cpu.er2 += 1
        cpu.r4 += 0xFF
        if cpu.ne:
            cpu.branch('restore_font')
        cpu.er0 = LAUNCH_FRAME
        cpu.er14 += cpu.er0
        cpu.sp = cpu.er14
        cpu.branch('out')
        cpu.label('memory')
        cpu.er14 = cpu.sp
        cpu.er0 = 1
        cpu.mem16[0, cpu.offset(cpu.er14, 14)] = cpu.er0
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er14, 12)] = cpu.er0
        cpu.label('out')
        cpu.pop(cpu.er2)
        cpu.pop(cpu.ea)
        cpu.pop(cpu.qr8)
        cpu.psw = cpu.r2
        cpu.pop(cpu.qr0)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def apps_screen():
        """Draw four NUL-terminated 16-byte near lines at ER0."""
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.r0 = 8
        cpu.mem8[0, 0x80A0] = cpu.r0
        cpu.r0 = 1
        cpu.mem8[0, 0x80A2] = cpu.r0
        cpu.call(0x0409A)
        cpu.er10 = 1
        cpu.label('row')
        cpu.er2 = cpu.er8
        cpu.r0 = 0
        cpu.r1 = cpu.r10
        cpu.call(ROM_DRAW_TEXT)
        cpu.er8 += 16
        cpu.er10 += 8
        cpu.er0 = 33
        cpu.compare(cpu.er10, cpu.er0)
        if cpu.lt:
            cpu.branch('row')
        cpu.call(ROM_REFRESH)
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def apps_message():
        """ER0=64-byte screen; R2=1 not apps/2 bad/3 empty/4 changed/5 RAM/6 run."""
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.er8)
        cpu.er8 = cpu.er0
        cpu.r4 = cpu.r2
        cpu.er2 = cpu.er0
        cpu.r0 = 0
        cpu.r5 = 64
        cpu.label('clear')
        cpu.mem8[0, cpu.er2] = cpu.r0
        cpu.er2 += 1
        cpu.r5 += 0xFF
        if cpu.ne:
            cpu.branch('clear')
        cpu.er0 = cpu.er8
        cpu.compare(cpu.r4, 1)
        if cpu.eq:
            cpu.jump('not_apps')
        cpu.compare(cpu.r4, 2)
        if cpu.eq:
            cpu.jump('bad')
        cpu.compare(cpu.r4, 3)
        if cpu.eq:
            cpu.jump('not_apps')
        cpu.compare(cpu.r4, 4)
        if cpu.eq:
            cpu.jump('modified')
        cpu.compare(cpu.r4, 6)
        if cpu.eq:
            cpu.jump('run')
        cpu.call('fn_apps_copy_text')
        cpu.data(b'NO APP RAM\0\0')
        cpu.er0 = cpu.er8
        cpu.er0 += 16
        cpu.call('fn_apps_copy_text')
        cpu.data(b'FREE PROG RAM\0')
        cpu.jump('back')
        cpu.label('not_apps')
        cpu.call('fn_apps_copy_text')
        cpu.data(b'NO APPS\0')
        cpu.er0 = cpu.er8
        cpu.er0 += 16
        cpu.call('fn_apps_copy_text')
        cpu.data(b'INSTALL VIA PC\0\0')
        cpu.jump('toolchain')
        cpu.label('bad')
        cpu.call('fn_apps_copy_text')
        cpu.data(b'BAD APP DATA\0\0')
        cpu.er0 = cpu.er8
        cpu.er0 += 16
        cpu.call('fn_apps_copy_text')
        cpu.data(b'RECOVER VIA PC\0\0')
        cpu.label('toolchain')
        cpu.er0 = cpu.er8
        cpu.er0 += 32
        cpu.call('fn_apps_copy_text')
        cpu.data(b'TOOLCHAIN\0')
        cpu.jump('back')
        cpu.label('run')
        cpu.call('fn_apps_copy_text')
        cpu.data(b'RUN APP?\0\0')
        cpu.jump('confirm')
        cpu.label('modified')
        cpu.call('fn_apps_copy_text')
        cpu.data(b'APP MODIFIED\0\0')
        cpu.label('confirm')
        cpu.er0 = cpu.er8
        cpu.er0 += 16
        cpu.call('fn_apps_copy_text')
        cpu.data(b'EXE:RUN\0')
        cpu.label('back')
        cpu.er0 = cpu.er8
        cpu.er0 += 48
        cpu.call('fn_apps_copy_text')
        cpu.data(b'EXIT:BACK\0')
        cpu.label('draw')
        cpu.er0 = cpu.er8
        cpu.call('fn_apps_screen')
        cpu.pop(cpu.er8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def apps_return():
        """Format unsigned ER2 at near ER0 without using native math or variables."""
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er8 = cpu.er0
        cpu.er10 = cpu.er2
        cpu.er2 = cpu.er0
        cpu.r0 = 0
        cpu.r4 = 64
        cpu.label('clear')
        cpu.mem8[0, cpu.er2] = cpu.r0
        cpu.er2 += 1
        cpu.r4 += 0xFF
        if cpu.ne:
            cpu.branch('clear')
        cpu.er0 = cpu.er8
        cpu.call('fn_apps_copy_text')
        cpu.data(b'RETURN \0')
        cpu.er0 = cpu.er8
        cpu.er0 += 7
        cpu.er2 = cpu.er10
        cpu.call('fn_apps_number')
        cpu.er0 = cpu.er8
        cpu.er0 += 48
        cpu.call('fn_apps_copy_text')
        cpu.data(b'EXE/EXIT:BACK\0')
        cpu.er0 = cpu.er8
        cpu.call('fn_apps_screen')
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def apps_number():
        """Append unsigned ER2 at near ER0; return ER0 at the terminating NUL."""
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.er10 = cpu.er2
        cpu.er12 = cpu.er0
        cpu.er6 = 10000
        cpu.r4 = 0
        cpu.label('digit')
        cpu.r5 = 0x30
        cpu.label('subtract')
        cpu.compare(cpu.er10, cpu.er6)
        if cpu.lt:
            cpu.branch('emit')
        cpu.r10 -= cpu.r6
        cpu.sub_carry(cpu.r11, cpu.r7)
        cpu.r5 += 1
        cpu.branch('subtract')
        cpu.label('emit')
        cpu.compare(cpu.r5, 0x30)
        if cpu.ne:
            cpu.branch('write')
        cpu.compare(cpu.r4, 0)
        if cpu.ne:
            cpu.branch('write')
        cpu.er0 = 1
        cpu.compare(cpu.er6, cpu.er0)
        if cpu.ne:
            cpu.branch('next')
        cpu.label('write')
        cpu.mem8[0, cpu.er12] = cpu.r5
        cpu.er12 += 1
        cpu.r4 = 1
        cpu.label('next')
        cpu.er0 = 10000
        cpu.compare(cpu.er6, cpu.er0)
        if cpu.eq:
            cpu.er6 = 1000
            cpu.jump('digit')
        cpu.er0 = 1000
        cpu.compare(cpu.er6, cpu.er0)
        if cpu.eq:
            cpu.er6 = 100
            cpu.jump('digit')
        cpu.er0 = 100
        cpu.compare(cpu.er6, cpu.er0)
        if cpu.eq:
            cpu.er6 = 10
            cpu.jump('digit')
        cpu.er0 = 10
        cpu.compare(cpu.er6, cpu.er0)
        if cpu.eq:
            cpu.er6 = 1
            cpu.jump('digit')
        cpu.er0 = cpu.er12
        cpu.r2 = 0
        cpu.mem8[0, cpu.er0] = cpu.r2
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.ret()

    @fw.function(native=True)
    def apps_page_number():
        cpu.push(cpu.er4)
        cpu.push(cpu.er6)
        cpu.er6 = 3
        cpu.er4 = 1
        cpu.label('page')
        cpu.compare(cpu.er2, cpu.er6)
        if cpu.lt:
            cpu.branch('done')
        cpu.er2 += -3
        cpu.er4 += 1
        cpu.branch('page')
        cpu.label('done')
        cpu.er2 = cpu.er4
        cpu.pop(cpu.er6)
        cpu.pop(cpu.er4)
        cpu.jump('fn_apps_number')

    @fw.function(native=True)
    def apps():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.sp += -64
        cpu.sp += -16
        cpu.er14 = cpu.sp
        cpu.er0 = cpu.mem16[0, 0x80A0]
        cpu.mem16[0, cpu.offset(cpu.er14, 76)] = cpu.er0
        cpu.r0 = cpu.mem8[0, 0x80A2]
        cpu.mem8[0, cpu.offset(cpu.er14, 78)] = cpu.r0
        cpu.r0 = 0
        cpu.mem8[0, 0x80A1] = cpu.r0
        cpu.er0 = 0
        cpu.mem16[0, cpu.offset(cpu.er14, 64)] = cpu.er0
        cpu.label('reload')
        cpu.call('fn_apps_check')
        cpu.er0 = cpu.er0
        if cpu.ne:
            cpu.r2 = cpu.r0
            cpu.jump('error')
        cpu.mem16[0, cpu.offset(cpu.er14, 66)] = cpu.er2
        cpu.mem16[0, cpu.offset(cpu.er14, 68)] = cpu.er4
        cpu.er4 = cpu.er4
        if cpu.eq:
            cpu.r2 = 3
            cpu.jump('error')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 64)]
        cpu.compare(cpu.er0, cpu.er4)
        if cpu.ge:
            cpu.er0 = 0
            cpu.mem16[0, cpu.offset(cpu.er14, 64)] = cpu.er0
        cpu.er8 = cpu.er2
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('page_ready')
        cpu.label('page_offset')
        cpu.er8 += APP_HEADER_SIZE
        cpu.er0 += -1
        if cpu.ne:
            cpu.branch('page_offset')
        cpu.label('page_ready')
        cpu.mem16[0, cpu.offset(cpu.er14, 70)] = cpu.er8
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 64)]
        cpu.r4 -= cpu.r0
        cpu.sub_carry(cpu.r5, cpu.r1)
        cpu.er0 = 3
        cpu.compare(cpu.er4, cpu.er0)
        if cpu.gt:
            cpu.er4 = 3
        cpu.mem16[0, cpu.offset(cpu.er14, 72)] = cpu.er4
        cpu.er2 = cpu.er14
        cpu.r0 = 0
        cpu.r4 = 64
        cpu.label('clear')
        cpu.mem8[0, cpu.er2] = cpu.r0
        cpu.er2 += 1
        cpu.r4 += 0xFF
        if cpu.ne:
            cpu.branch('clear')
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_copy_text')
        cpu.data(b'APPS \0')
        cpu.er0 = cpu.er14
        cpu.er0 += 5
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, 64)]
        cpu.call('fn_apps_page_number')
        cpu.r2 = 0x2F
        cpu.mem8[0, cpu.er0] = cpu.r2
        cpu.er0 += 1
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, 68)]
        cpu.er2 += -1
        cpu.call('fn_apps_page_number')
        cpu.call('fn_apps_copy_text')
        cpu.data(b' <>\0')
        cpu.er10 = cpu.er14
        cpu.er10 += 16
        cpu.er12 = cpu.mem16[0, cpu.offset(cpu.er14, 72)]
        cpu.r4 = 0x31
        cpu.label('row')
        cpu.mem8[0, cpu.er10] = cpu.r4
        cpu.r0 = 0x3A
        cpu.mem8[0, cpu.offset(cpu.er10, 1)] = cpu.r0
        cpu.er0 = cpu.er8
        cpu.er0 += 28
        cpu.er2 = cpu.er10
        cpu.er2 += 2
        cpu.r5 = cpu.mem8[9, cpu.offset(cpu.er8, 24)]
        cpu.label('copy_name')
        cpu.r6 = cpu.mem8[9, cpu.er0]
        cpu.mem8[0, cpu.er2] = cpu.r6
        cpu.er0 += 1
        cpu.er2 += 1
        cpu.r5 += 0xFF
        if cpu.ne:
            cpu.branch('copy_name')
        cpu.er8 += APP_HEADER_SIZE
        cpu.er10 += 16
        cpu.r4 += 1
        cpu.er12 += -1
        if cpu.ne:
            cpu.branch('row')
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_screen')
        cpu.label('key')
        cpu.call(SCANNER_ADDRESS)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.jump('out')
        cpu.compare(cpu.r0, 0xFC)
        if cpu.eq:
            cpu.jump('left')
        cpu.compare(cpu.r0, 0xFD)
        if cpu.eq:
            cpu.jump('right')
        cpu.compare(cpu.r0, 0x31)
        if cpu.lt:
            cpu.jump('key')
        cpu.compare(cpu.r0, 0x33)
        if cpu.gt:
            cpu.jump('key')
        cpu.r0 += 0xCF
        cpu.r1 = 0
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, 72)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.jump('key')
        cpu.er8 = cpu.mem16[0, cpu.offset(cpu.er14, 70)]
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('selected')
        cpu.label('select_offset')
        cpu.er8 += APP_HEADER_SIZE
        cpu.er0 += -1
        if cpu.ne:
            cpu.branch('select_offset')
        cpu.label('selected')
        cpu.mem16[0, cpu.offset(cpu.er14, 74)] = cpu.er8
        cpu.er0 = cpu.er8
        cpu.call('fn_apps_modified')
        cpu.r2 = 4
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.r2 = 6
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_message')
        cpu.label('modified_key')
        cpu.call(SCANNER_ADDRESS)
        cpu.compare(cpu.r0, 0xFB)
        if cpu.eq:
            cpu.branch('run')
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.jump('reload')
        cpu.jump('modified_key')
        cpu.label('run')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 74)]
        cpu.call('fn_apps_launch')
        cpu.er2 = cpu.er2
        if cpu.ne:
            cpu.er0 = cpu.er14
            cpu.r2 = 5
            cpu.call('fn_apps_message')
            cpu.jump('acknowledge')
        cpu.er2 = cpu.er0
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_return')
        cpu.label('acknowledge')
        cpu.call(SCANNER_ADDRESS)
        cpu.compare(cpu.r0, 0xFB)
        if cpu.eq:
            cpu.jump('reload')
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.jump('reload')
        cpu.jump('acknowledge')
        cpu.label('left')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 64)]
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.jump('key')
        cpu.er0 += -3
        cpu.mem16[0, cpu.offset(cpu.er14, 64)] = cpu.er0
        cpu.jump('reload')
        cpu.label('right')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 64)]
        cpu.er0 += 3
        cpu.er2 = cpu.mem16[0, cpu.offset(cpu.er14, 68)]
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.jump('key')
        cpu.mem16[0, cpu.offset(cpu.er14, 64)] = cpu.er0
        cpu.jump('reload')
        cpu.label('error')
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_message')
        cpu.label('error_key')
        cpu.call(SCANNER_ADDRESS)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('error_key')
        cpu.label('out')
        cpu.er0 = cpu.mem16[0, cpu.offset(cpu.er14, 76)]
        cpu.mem16[0, 0x80A0] = cpu.er0
        cpu.r0 = cpu.mem8[0, cpu.offset(cpu.er14, 78)]
        cpu.mem8[0, 0x80A2] = cpu.r0
        cpu.sp += 64
        cpu.sp += 16
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def develop_menu():
        """Called after native CFA66 save and 1210A; return to the owning hook."""
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.label('draw')
        cpu.er2 = 15
        cpu.push(cpu.er2)
        cpu.er0 = 0x3B14
        cpu.push(cpu.er0)
        cpu.push(cpu.er2)
        cpu.er0 = 0x3B03
        cpu.push(cpu.er0)
        cpu.push(cpu.er2)
        cpu.er0 = 0x3AF2
        cpu.push(cpu.er0)
        cpu.er0 = 0x3AE6
        cpu.call(0x19F12)
        cpu.sp += 12
        cpu.label('key')
        cpu.er0 = 0
        cpu.push(cpu.er0)
        cpu.r0 = 0x31
        cpu.r1 = 0x36
        cpu.er2 = 0x7532
        cpu.call(0x125FC)
        cpu.sp += 2
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.jump('out')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.eq:
            cpu.jump('out')
        cpu.compare(cpu.r0, 1)
        if cpu.eq:
            cpu.call(0xDA60E)
            cpu.jump('draw')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.call(0xD9D52)
            cpu.jump('draw')
        cpu.compare(cpu.r0, 3)
        if cpu.eq:
            cpu.call(0x07660)
            cpu.jump('draw')
        cpu.compare(cpu.r0, 4)
        if cpu.eq:
            cpu.call(0x07480)
            cpu.jump('draw')
        cpu.compare(cpu.r0, 5)
        if cpu.eq:
            cpu.call(0x07354)
            cpu.jump('draw')
        cpu.compare(cpu.r0, 6)
        if cpu.eq:
            cpu.call('fn_apps')
            cpu.jump('draw')
        cpu.jump('key')
        cpu.label('out')
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
