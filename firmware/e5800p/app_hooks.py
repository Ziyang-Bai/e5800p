"""App-ownership warnings at native S4 destructive call sites.

APP_HOOKS describes CALL replacements; the project owns their placement.
Cancellation continuations follow the stock frames and require emulator proof.
"""

from kits import cpu


APP_HOOKS = (
    dict(address=0xC7EC6, expected=bytes.fromhex('01 FF 00 00'),
         symbol='fn_apps_trans_erase'),
    dict(address=0xE9614, expected=bytes.fromhex('01 FE BA 96'),
         symbol='fn_apps_protect'),
    dict(address=0xEA0E6, expected=bytes.fromhex('01 F0 F4 4E'),
         symbol='fn_apps_aging_erase'),
)

NATIVE_EXIT = 0x753F


def install(fw):
    @fw.function(native=True)
    def apps_trans_erase():
        """C7EC6: preserve preflight, warn only for S4, never fake erase success."""
        cpu.push(cpu.lr)
        cpu.push(cpu.xr0)
        cpu.r0 = cpu.mem8[0x80AD]
        cpu.compare(cpu.r0, 0)
        if cpu.ne:
            cpu.branch('forward')
        cpu.call('fn_apps_owned')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('forward')
        cpu.call('fn_apps_erase_confirm')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cancel')
        cpu.label('forward')
        cpu.pop(cpu.xr0)
        cpu.pop(cpu.lr)
        cpu.jump(0xF0000)

        cpu.label('cancel')
        cpu.pop(cpu.xr0)
        cpu.pop(cpu.lr)
        # Importer FP+2/+4 is its saved far return, not this gate's C7ECA.
        cpu.er0 = cpu.er14
        cpu.er0 += 2
        cpu.er2 = cpu.mem16[cpu.er0]
        cpu.compare(cpu.r2, 0xBE)
        cpu.compare_carry(cpu.r3, 0x73)
        if cpu.ne:
            cpu.branch('other_caller')
        cpu.er0 += 2
        cpu.er2 = cpu.mem16[cpu.er0]
        cpu.er2 = cpu.er2
        if cpu.ne:
            cpu.branch('other_caller')
        # C7DCC: FP-34 locals, then XR8/XR4/ER12; SP here is FP-44.
        cpu.pop(cpu.er12)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.xr8)
        cpu.sp = cpu.er14
        cpu.pop(cpu.er14)
        cpu.pop(cpu.lr)
        # Outer Trans SP is FP-4, pointing to saved ER4. Its native AC exit
        # skips both error4 and the success/delete-source continuation.
        cpu.jump(0x07460)

        cpu.label('other_caller')
        cpu.er4 = NATIVE_EXIT
        cpu.jump(0xC7FB6)

    @fw.function(native=True)
    def apps_protect():
        """E9614: app ownership selects native Release despite erased bank byte."""
        cpu.push(cpu.lr)
        cpu.push(cpu.xr0)
        cpu.call('fn_apps_owned')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('forward')
        cpu.call('fn_apps_erase_confirm')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cancel')
        cpu.pop(cpu.xr0)
        cpu.pop(cpu.lr)
        # Native E96BA keeps its own Release confirmation and SRAM cleanup.
        cpu.er0 = 1
        cpu.jump(0xE96BA)

        cpu.label('forward')
        cpu.pop(cpu.xr0)
        cpu.pop(cpu.lr)
        cpu.jump(0xE96BA)

        cpu.label('cancel')
        cpu.pop(cpu.xr0)
        cpu.pop(cpu.pc)

    @fw.function(native=True)
    def apps_aging_erase():
        """EA0E6: guard the separate native Aging/YAMAYO sector4 erase."""
        cpu.push(cpu.lr)
        cpu.push(cpu.xr0)
        cpu.call('fn_apps_owned')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('forward')
        cpu.call('fn_apps_erase_confirm')
        cpu.er0 = cpu.er0
        if cpu.eq:
            cpu.branch('cancel')
        cpu.label('forward')
        cpu.pop(cpu.xr0)
        cpu.pop(cpu.lr)
        cpu.jump(0x04EF4)

        cpu.label('cancel')
        cpu.pop(cpu.xr0)
        cpu.pop(cpu.lr)
        # E9F94 owns only a two-byte local frame; native epilogue restores it.
        cpu.jump(0xE9FD0)
