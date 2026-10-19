"""Fixed-layout e5800p editing routines and tables."""

from kits import cpu

SCANNER_ADDRESS = 0x80800
UI_TEXT_ADDRESS = 0x81E06
ROM_DRAW_TEXT = 0x041DA
ROM_REFRESH = 0x043BE
JOURNAL_RECOVER = 0x83800
SMALL_TEXT_ADDRESS = 0xF9000
JOURNAL_COMMIT = 0x83000
MEMORY_GOTO_ADDRESS = 0x825CE
HEX_KEY_ADDRESS = 0x825CA
VIEW_ADDRESS = 0xFEC00
DETAIL_ADDRESS = 0xFEC04
GOTO_ADDRESS = 0x825C6
CODEC_LENGTH_ADDRESS = 0x80440
ISA_ENTRY_ADDRESS = 0xF7E68
BATCH_ADDRESS = 0xFF900

UI_STRINGS = (
    b'PROGRAM\x00'
    b'1:PROG\x00'
    b'2:ASM\x00'
    b'WRITE ERROR\x00'
    b'READ ONLY\x00'
    b'EXE SAVE FIRST\x00'
    b'RECOVER ERROR\x00'
    b'EMPTY PROGRAM\x00'
    b'EXE SAVE EXIT NO\x00'
    b'BAD OPCODE\x00'
    b'SAVE FIRST\x00'
    b'PROGRAM FULL\x00'
    b'NEXT \x00'
    b' Q\x00'
    b' \x00'
    b'GOTO ADDRESS\x00'
    b'8:\x00'
    b'4000..5FEF\x00'
    b'EVEN ADDRESS\x00'
    b'HEX 4 DIGITS\x00'
    b'EXE OK EXIT BACK\x00'
    b'1:FLASH\x00'
    b'2:SRAM\x00'
    b'3:RAM\x00'
    b'EXIT BACK\x00'
    b'GOTO FLASH\x00'
    b'GOTO SRAM\x00'
    b'GOTO RAM\x00'
    b'ADDRESS RANGE\x00'
    b'8:0000..F:FFFF\x00'
    b'0000..7FFF\x00'
    b'8000..8DFF\x00'
)

UI_STRINGS_LABELS = {
    'ui_strings': 0x0,
}


def install(fw):
    fw.data('ui_strings', UI_STRINGS, address=0xFD130, labels=UI_STRINGS_LABELS)

    @fw.function(native=True, address=0x825C6)
    def goto():
        cpu.label('goto')
        cpu.jump('address')
        cpu.label('branch_0004')
        cpu.jump('hex_key')
        cpu.jump('memory')
        cpu.label('hex_key')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.call(SCANNER_ADDRESS)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ge:
            cpu.branch('key_F')
        cpu.compare(cpu.r0, 0x02)
        cpu.compare_carry(cpu.r1, 0x7D)
        if cpu.eq:
            cpu.branch('key_F')
        cpu.compare(cpu.r0, 0x49)
        cpu.compare_carry(cpu.r1, 0x75)
        if cpu.eq:
            cpu.branch('key_F')
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('key_ascii')
        cpu.er0 = 0x00
        cpu.jump('key_F')
        cpu.label('key_ascii')
        cpu.compare(cpu.r0, 0x53)
        if cpu.ne:
            cpu.branch('key_A')
        cpu.r0 = 0x41
        cpu.jump('key_F')
        cpu.label('key_A')
        cpu.compare(cpu.r0, 0x54)
        if cpu.ne:
            cpu.branch('key_B')
        cpu.r0 = 0x42
        cpu.jump('key_F')
        cpu.label('key_B')
        cpu.compare(cpu.r0, 0x55)
        if cpu.ne:
            cpu.branch('key_C')
        cpu.r0 = 0x43
        cpu.jump('key_F')
        cpu.label('key_C')
        cpu.compare(cpu.r0, 0x4E)
        if cpu.ne:
            cpu.branch('key_D')
        cpu.r0 = 0x44
        cpu.jump('key_F')
        cpu.label('key_D')
        cpu.compare(cpu.r0, 0x4F)
        if cpu.ne:
            cpu.branch('key_E')
        cpu.r0 = 0x45
        cpu.jump('key_F')
        cpu.label('key_E')
        cpu.compare(cpu.r0, 0x50)
        if cpu.ne:
            cpu.branch('key_F')
        cpu.r0 = 0x46
        cpu.jump('key_F')
        cpu.label('key_F')
        cpu.label('key_done')
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('address')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.push(cpu.er12)
        cpu.push(cpu.er14)
        cpu.sp += -32
        cpu.er14 = cpu.sp
        cpu.er8 = cpu.er0
        cpu.r12 = cpu.r2
        cpu.r13 = 0x00
        cpu.r0 = cpu.mem8[0x80A0]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1C
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A2]
        cpu.er2 += 0x01
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = 0x07
        cpu.mem8[0x80A0] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x80A2] = cpu.r0
        cpu.r6 = 0x00
        cpu.r7 = 0x00
        cpu.label('draw')
        cpu.call(0x0409A)
        cpu.er2 = cpu.er14
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0xC5
        cpu.r3 = 0xD1
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x01
        cpu.call(ROM_DRAW_TEXT)
        cpu.er2 = cpu.er14
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0xD2
        cpu.r3 = 0xD1
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.er2 += 0x02
        cpu.r0 = cpu.r9
        cpu.call('hexbyte')
        cpu.r0 = cpu.r8
        cpu.call('hexbyte')
        cpu.r0 = 0x00
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x09
        cpu.call(ROM_DRAW_TEXT)
        cpu.compare(cpu.r7, 0x00)
        if cpu.eq:
            cpu.branch('hint')
        cpu.compare(cpu.r7, 0x01)
        if cpu.ne:
            cpu.branch('odd_hint')
        cpu.er2 = cpu.er14
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0xD5
        cpu.r3 = 0xD1
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x11
        cpu.call(ROM_DRAW_TEXT)
        cpu.jump('footer')
        cpu.label('odd_hint')
        cpu.er2 = cpu.er14
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0xE0
        cpu.r3 = 0xD1
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x11
        cpu.call(ROM_DRAW_TEXT)
        cpu.jump('footer')
        cpu.label('hint')
        cpu.er2 = cpu.er14
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0xED
        cpu.r3 = 0xD1
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x11
        cpu.call(ROM_DRAW_TEXT)
        cpu.label('footer')
        cpu.er2 = cpu.er14
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0xFA
        cpu.r3 = 0xD1
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x19
        cpu.call(ROM_DRAW_TEXT)
        cpu.call(ROM_REFRESH)
        cpu.label('input')
        cpu.call('branch_0004')
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('skip_26')
        cpu.jump('cancel')
        cpu.label('skip_26')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.ne:
            cpu.branch('skip_28')
        cpu.jump('accept')
        cpu.label('skip_28')
        cpu.compare(cpu.r0, 0xFC)
        if cpu.ne:
            cpu.branch('skip_30')
        cpu.jump('backspace')
        cpu.label('skip_30')
        cpu.compare(cpu.r0, 0x30)
        if cpu.ge:
            cpu.branch('skip_32')
        cpu.jump('input')
        cpu.label('skip_32')
        cpu.compare(cpu.r0, 0x3A)
        if cpu.ge:
            cpu.branch('letter')
        cpu.r0 += 0xD0
        cpu.jump('digit')
        cpu.label('letter')
        cpu.compare(cpu.r0, 0x41)
        if cpu.ge:
            cpu.branch('skip_36')
        cpu.jump('input')
        cpu.label('skip_36')
        cpu.compare(cpu.r0, 0x47)
        if cpu.lt:
            cpu.branch('skip_38')
        cpu.jump('input')
        cpu.label('skip_38')
        cpu.r0 += 0xC9
        cpu.label('digit')
        cpu.compare(cpu.r6, 0x04)
        if cpu.lt:
            cpu.branch('digit_count')
        cpu.r6 = 0x00
        cpu.label('digit_count')
        cpu.compare(cpu.r6, 0x00)
        if cpu.ne:
            cpu.branch('append')
        cpu.er8 = 0x00
        cpu.label('append')
        cpu.r3 = cpu.r8
        cpu.r3 >>= 0x04
        cpu.r8 <<= 0x04
        cpu.r9 <<= 0x04
        cpu.r9 |= cpu.r3
        cpu.r8 |= cpu.r0
        cpu.r6 += 0x01
        cpu.r7 = 0x00
        cpu.jump('draw')
        cpu.label('backspace')
        cpu.compare(cpu.r6, 0x00)
        if cpu.ne:
            cpu.branch('skip_43')
        cpu.jump('input')
        cpu.label('skip_43')
        cpu.r3 = cpu.r9
        cpu.r3 <<= 0x04
        cpu.r8 >>= 0x04
        cpu.r9 >>= 0x04
        cpu.r8 |= cpu.r3
        cpu.r6 += 0xFF
        cpu.r7 = 0x00
        cpu.jump('draw')
        cpu.label('accept')
        cpu.compare(cpu.r6, 0x00)
        if cpu.eq:
            cpu.branch('skip_47')
        cpu.compare(cpu.r6, 0x04)
        if cpu.eq:
            cpu.branch('skip_47')
        cpu.jump('draw')
        cpu.label('skip_47')
        cpu.label('check_range')
        cpu.er0 = cpu.er8
        cpu.r2 = 0x00
        cpu.r3 = 0x40
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_49')
        cpu.jump('range_error')
        cpu.label('skip_49')
        cpu.r2 = 0xF0
        cpu.r3 = 0x5F
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('skip_51')
        cpu.jump('range_error')
        cpu.label('skip_51')
        cpu.compare(cpu.r12, 0x00)
        if cpu.eq:
            cpu.branch('skip_54')
        cpu.r0 = cpu.r8
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('skip_54')
        cpu.jump('odd_error')
        cpu.label('skip_54')
        cpu.label('accepted')
        cpu.r4 = 0x01
        cpu.jump('finish')
        cpu.label('range_error')
        cpu.r7 = 0x01
        cpu.jump('draw')
        cpu.label('odd_error')
        cpu.r7 = 0x02
        cpu.jump('draw')
        cpu.label('cancel')
        cpu.r4 = 0x00
        cpu.label('finish')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1D
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.mem8[0x80A2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1C
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.mem8[0x80A0] = cpu.r0
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r4
        cpu.sp += 0x20
        cpu.pop(cpu.er14)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('memory')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.push(cpu.er12)
        cpu.push(cpu.er14)
        cpu.sp += -48
        cpu.er14 = cpu.sp
        cpu.er8 = cpu.er0
        cpu.r13 = cpu.r2
        cpu.r0 = cpu.mem8[0x80A0]
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1C
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A2]
        cpu.er2 += 0x01
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = 0x08
        cpu.mem8[0x80A0] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x80A2] = cpu.r0
        cpu.label('memory_menu')
        cpu.call('fn_ui_menu')
        cpu.data(b'REGION\0FLASH\0SRAM\0RAM\0\0\0')
        cpu.compare(cpu.r0, 0)
        if cpu.eq:
            cpu.branch('memory_flash')
        cpu.compare(cpu.r0, 1)
        if cpu.eq:
            cpu.branch('memory_sram')
        cpu.compare(cpu.r0, 2)
        if cpu.eq:
            cpu.branch('memory_ram')
        cpu.jump('memory_cancel')
        cpu.label('memory_flash')
        cpu.r12 = 0x00
        cpu.r10 = 0x05
        cpu.compare(cpu.r13, 0x08)
        if cpu.ge:
            cpu.branch('memory_ready')
        cpu.r13 = 0x08
        cpu.r8 = 0x00
        cpu.r9 = 0x40
        cpu.jump('memory_ready')
        cpu.label('memory_sram')
        cpu.r12 = 0x01
        cpu.r10 = 0x04
        cpu.compare(cpu.r13, 0x04)
        if cpu.eq:
            cpu.branch('memory_ready')
        cpu.r13 = 0x04
        cpu.er8 = 0x00
        cpu.jump('memory_ready')
        cpu.label('memory_ram')
        cpu.r12 = 0x02
        cpu.r10 = 0x04
        cpu.compare(cpu.r13, 0x00)
        if cpu.eq:
            cpu.branch('memory_ready')
        cpu.r13 = 0x00
        cpu.r8 = 0x00
        cpu.r9 = 0x80
        cpu.label('memory_ready')
        cpu.r6 = 0x00
        cpu.r7 = 0x00
        cpu.label('memory_draw')
        cpu.call(0x0409A)
        cpu.compare(cpu.r12, 0x00)
        if cpu.ne:
            cpu.branch('memory_title_sram')
        cpu.er2 = cpu.er14
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0x2A
        cpu.r3 = 0xD2
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x01
        cpu.call(ROM_DRAW_TEXT)
        cpu.jump('memory_address')
        cpu.label('memory_title_sram')
        cpu.compare(cpu.r12, 0x01)
        if cpu.ne:
            cpu.branch('memory_title_ram')
        cpu.er2 = cpu.er14
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0x35
        cpu.r3 = 0xD2
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x01
        cpu.call(ROM_DRAW_TEXT)
        cpu.jump('memory_address')
        cpu.label('memory_title_ram')
        cpu.er2 = cpu.er14
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0x3F
        cpu.r3 = 0xD2
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x01
        cpu.call(ROM_DRAW_TEXT)
        cpu.label('memory_address')
        cpu.er2 = cpu.er14
        cpu.r0 = cpu.r13
        cpu.call('nibble')
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 += 0x01
        cpu.r0 = 0x3A
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 += 0x01
        cpu.r0 = cpu.r9
        cpu.call('hexbyte')
        cpu.r0 = cpu.r8
        cpu.call('hexbyte')
        cpu.r0 = 0x00
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x09
        cpu.call(ROM_DRAW_TEXT)
        cpu.compare(cpu.r7, 0x00)
        if cpu.eq:
            cpu.branch('memory_range')
        cpu.er2 = cpu.er14
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0x48
        cpu.r3 = 0xD2
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x11
        cpu.call(ROM_DRAW_TEXT)
        cpu.jump('memory_footer')
        cpu.label('memory_range')
        cpu.compare(cpu.r12, 0x00)
        if cpu.ne:
            cpu.branch('memory_range_sram')
        cpu.er2 = cpu.er14
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0x56
        cpu.r3 = 0xD2
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x11
        cpu.call(ROM_DRAW_TEXT)
        cpu.jump('memory_footer')
        cpu.label('memory_range_sram')
        cpu.compare(cpu.r12, 0x01)
        if cpu.ne:
            cpu.branch('memory_range_ram')
        cpu.er2 = cpu.er14
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0x65
        cpu.r3 = 0xD2
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x11
        cpu.call(ROM_DRAW_TEXT)
        cpu.jump('memory_footer')
        cpu.label('memory_range_ram')
        cpu.er2 = cpu.er14
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0x70
        cpu.r3 = 0xD2
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x11
        cpu.call(ROM_DRAW_TEXT)
        cpu.label('memory_footer')
        cpu.er2 = cpu.er14
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0xFA
        cpu.r3 = 0xD1
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x19
        cpu.call(ROM_DRAW_TEXT)
        cpu.call(ROM_REFRESH)
        cpu.label('memory_input')
        cpu.call('branch_0004')
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('skip_86')
        cpu.jump('memory_cancel')
        cpu.label('skip_86')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.ne:
            cpu.branch('skip_88')
        cpu.jump('memory_accept')
        cpu.label('skip_88')
        cpu.compare(cpu.r0, 0xFC)
        if cpu.ne:
            cpu.branch('skip_90')
        cpu.jump('memory_backspace')
        cpu.label('skip_90')
        cpu.compare(cpu.r0, 0x30)
        if cpu.ge:
            cpu.branch('skip_92')
        cpu.jump('memory_input')
        cpu.label('skip_92')
        cpu.compare(cpu.r0, 0x3A)
        if cpu.ge:
            cpu.branch('memory_letter')
        cpu.r0 += 0xD0
        cpu.jump('memory_digit')
        cpu.label('memory_letter')
        cpu.compare(cpu.r0, 0x41)
        if cpu.ge:
            cpu.branch('skip_96')
        cpu.jump('memory_input')
        cpu.label('skip_96')
        cpu.compare(cpu.r0, 0x47)
        if cpu.lt:
            cpu.branch('skip_98')
        cpu.jump('memory_input')
        cpu.label('skip_98')
        cpu.r0 += 0xC9
        cpu.label('memory_digit')
        cpu.compare(cpu.r6, cpu.r10)
        if cpu.lt:
            cpu.branch('memory_digit_count')
        cpu.r6 = 0x00
        cpu.label('memory_digit_count')
        cpu.compare(cpu.r6, 0x00)
        if cpu.ne:
            cpu.branch('memory_append')
        cpu.er8 = 0x00
        cpu.compare(cpu.r12, 0x00)
        if cpu.ne:
            cpu.branch('memory_append')
        cpu.r13 = 0x00
        cpu.label('memory_append')
        cpu.compare(cpu.r12, 0x00)
        if cpu.ne:
            cpu.branch('memory_append_word')
        cpu.r3 = cpu.r9
        cpu.r3 >>= 0x04
        cpu.r13 <<= 0x04
        cpu.r13 |= cpu.r3
        cpu.label('memory_append_word')
        cpu.r3 = cpu.r8
        cpu.r3 >>= 0x04
        cpu.r8 <<= 0x04
        cpu.r9 <<= 0x04
        cpu.r9 |= cpu.r3
        cpu.r8 |= cpu.r0
        cpu.r6 += 0x01
        cpu.r7 = 0x00
        cpu.jump('memory_draw')
        cpu.label('memory_backspace')
        cpu.compare(cpu.r6, 0x00)
        if cpu.ne:
            cpu.branch('skip_105')
        cpu.jump('memory_input')
        cpu.label('skip_105')
        cpu.r3 = cpu.r9
        cpu.r3 <<= 0x04
        cpu.r8 >>= 0x04
        cpu.r9 >>= 0x04
        cpu.r8 |= cpu.r3
        cpu.compare(cpu.r12, 0x00)
        if cpu.ne:
            cpu.branch('memory_backspace_done')
        cpu.r3 = cpu.r13
        cpu.r3 <<= 0x04
        cpu.r9 |= cpu.r3
        cpu.r13 >>= 0x04
        cpu.label('memory_backspace_done')
        cpu.r6 += 0xFF
        cpu.r7 = 0x00
        cpu.jump('memory_draw')
        cpu.label('memory_accept')
        cpu.compare(cpu.r6, 0x00)
        if cpu.eq:
            cpu.branch('skip_110')
        cpu.compare(cpu.r6, cpu.r10)
        if cpu.eq:
            cpu.branch('skip_110')
        cpu.jump('memory_draw')
        cpu.label('skip_110')
        cpu.label('memory_check')
        cpu.compare(cpu.r12, 0x00)
        if cpu.ne:
            cpu.branch('memory_check_sram')
        cpu.compare(cpu.r13, 0x08)
        if cpu.ge:
            cpu.branch('skip_113')
        cpu.jump('memory_error')
        cpu.label('skip_113')
        cpu.compare(cpu.r13, 0x10)
        if cpu.lt:
            cpu.branch('skip_115')
        cpu.jump('memory_error')
        cpu.label('skip_115')
        cpu.jump('skip_124')
        cpu.label('memory_check_sram')
        cpu.er0 = cpu.er8
        cpu.compare(cpu.r12, 0x01)
        if cpu.ne:
            cpu.branch('memory_check_ram')
        cpu.r2 = 0x00
        cpu.r3 = 0x80
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('skip_119')
        cpu.jump('memory_error')
        cpu.label('skip_119')
        cpu.jump('skip_124')
        cpu.label('memory_check_ram')
        cpu.r2 = 0x00
        cpu.r3 = 0x80
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_122')
        cpu.jump('memory_error')
        cpu.label('skip_122')
        cpu.r2 = 0x00
        cpu.r3 = 0x8E
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('skip_124')
        cpu.jump('memory_error')
        cpu.label('skip_124')
        cpu.label('memory_accepted')
        cpu.r4 = 0x01
        cpu.jump('memory_finish')
        cpu.label('memory_error')
        cpu.r7 = 0x01
        cpu.jump('memory_draw')
        cpu.label('memory_cancel')
        cpu.r4 = 0x00
        cpu.label('memory_finish')
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1D
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.mem8[0x80A2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 0x1C
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.mem8[0x80A0] = cpu.r0
        cpu.er0 = cpu.er8
        cpu.r2 = cpu.r13
        cpu.r3 = cpu.r4
        cpu.sp += 0x30
        cpu.pop(cpu.er14)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('hexbyte')
        cpu.push(cpu.lr)
        cpu.r5 = cpu.r0
        cpu.r0 >>= 0x04
        cpu.call('nibble')
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 += 0x01
        cpu.r0 = cpu.r5
        cpu.r0 &= 0x0F
        cpu.call('nibble')
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 += 0x01
        cpu.pop(cpu.pc)
        cpu.label('nibble')
        cpu.compare(cpu.r0, 0x0A)
        if cpu.lt:
            cpu.branch('number')
        cpu.r0 += 0x37
        cpu.ret()
        cpu.label('number')
        cpu.r0 += 0x30
        cpu.ret()


    @fw.function(native=True, address=0xFD330)
    def editor():
        cpu.label('editor')
        cpu.label('entry')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.push(cpu.er14)
        cpu.sp += -32
        cpu.sp += -32
        cpu.sp += -32
        cpu.er14 = cpu.sp
        cpu.er14 += 32
        cpu.r2 = 0xF0
        cpu.r3 = 0x5F
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('entry_address')
        cpu.r0 = 0xEF
        cpu.r1 = 0x5F
        cpu.label('entry_address')
        cpu.er8 = cpu.er0
        cpu.mem8[cpu.offset(cpu.er14, 46)] = cpu.r0
        cpu.r0 = cpu.r9
        cpu.mem8[cpu.offset(cpu.er14, 47)] = cpu.r0
        cpu.er0 = cpu.er8
        cpu.r5 = cpu.r0
        cpu.r5 &= 0x1F
        cpu.er12 = cpu.er0
        cpu.r12 &= 0xE0
        cpu.r0 = cpu.mem8[0x80A0]
        cpu.mem8[cpu.offset(cpu.er14, 33)] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A2]
        cpu.mem8[cpu.offset(cpu.er14, 34)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 38)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 39)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 53)] = cpu.r0
        cpu.r0 = 0x08
        cpu.mem8[cpu.offset(cpu.er14, 44)] = cpu.r0
        cpu.r0 = 0x00
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x4F
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.call(JOURNAL_RECOVER)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('load')
        cpu.jump('recover_error')
        cpu.label('load')
        cpu.call('can_write')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('load_mode')
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 38)] = cpu.r0
        cpu.label('load_mode')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 44)]
        cpu.r7 = cpu.r0
        cpu.er2 = cpu.sp
        cpu.ea = cpu.address(cpu.er2)
        cpu.er0 = cpu.er12
        cpu.r8 = 0x20
        cpu.label('read_byte')
        cpu.r2 = cpu.r7
        cpu.r3 = cpu.mem8[cpu.r2, cpu.er0]
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r3
        cpu.er0 += 0x01
        cpu.r8 += 0xFF
        if cpu.ne:
            cpu.branch('read_byte')
        cpu.er2 = cpu.sp
        cpu.r0 = 0x40
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.r0 = 0x00
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 48)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 49)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 50)] = cpu.r0
        cpu.r0 = 0x00
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x55
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('draw')
        cpu.label('draw')
        cpu.call(0x0409A)
        cpu.r0 = 0x07
        cpu.mem8[0x80A0] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x80A2] = cpu.r0
        cpu.r8 = 0x00
        cpu.r9 = 0x01
        cpu.label('row')
        cpu.er2 = cpu.sp
        cpu.er0 = 0x20
        cpu.er2 += cpu.er0
        cpu.ea = cpu.address(cpu.er2)
        cpu.er10 = cpu.sp
        cpu.r0 = cpu.r8
        cpu.r1 = 0x00
        cpu.er10 += cpu.er0
        cpu.r7 = 0x00
        cpu.label('byte')
        cpu.r0 = 0x20
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.er10]
        cpu.call('hexbyte')
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r1
        cpu.er10 += 0x01
        cpu.r7 += 0x01
        cpu.compare(cpu.r7, 0x08)
        if cpu.lt:
            cpu.branch('byte')
        cpu.r0 = 0x00
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.er2 = cpu.sp
        cpu.er0 = 0x20
        cpu.er2 += cpu.er0
        cpu.r0 = 0x00
        cpu.r1 = cpu.r9
        cpu.call(SMALL_TEXT_ADDRESS)
        cpu.r8 += 0x08
        cpu.r9 += 0x06
        cpu.compare(cpu.r9, 0x19)
        if cpu.lt:
            cpu.branch('row')
        cpu.er2 = cpu.sp
        cpu.er0 = 0x20
        cpu.er2 += cpu.er0
        cpu.ea = cpu.address(cpu.er2)
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x4E
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.call('nibble')
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.r0 = 0x3A
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.er8 = cpu.er12
        cpu.r0 = cpu.r5
        cpu.r1 = 0x00
        cpu.er8 += cpu.er0
        cpu.r0 = cpu.r9
        cpu.call('hexbyte')
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r1
        cpu.r0 = cpu.r8
        cpu.call('hexbyte')
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r1
        cpu.r0 = 0x20
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.er10 = cpu.sp
        cpu.r0 = cpu.r5
        cpu.r1 = 0x00
        cpu.er10 += cpu.er0
        cpu.r0 = cpu.mem8[cpu.er10]
        cpu.r7 = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 39
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('current_value')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 41)]
        cpu.r0 >>= 0x04
        cpu.call('nibble')
        cpu.r1 = 0x5F
        cpu.jump('current_print')
        cpu.label('current_value')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 39)]
        cpu.compare(cpu.r0, 0x02)
        if cpu.ne:
            cpu.branch('saved_value')
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 41)]
        cpu.label('saved_value')
        cpu.r0 = cpu.r7
        cpu.call('hexbyte')
        cpu.label('current_print')
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r1
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 32)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('clean')
        cpu.r0 = 0x2A
        cpu.jump('status_end')
        cpu.label('clean')
        cpu.r0 = 0x20
        cpu.label('status_end')
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.er2 = cpu.sp
        cpu.er0 = 0x20
        cpu.er2 += cpu.er0
        cpu.r0 = 0x00
        cpu.r1 = 0x19
        cpu.call(SMALL_TEXT_ADDRESS)
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 38)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('read_status')
        cpu.push(cpu.xr4)
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_copy_text')
        cpu.data(b'EDIT 2HEX EXE\0')
        cpu.pop(cpu.xr4)
        cpu.jump('mode_status')
        cpu.label('read_status')
        cpu.push(cpu.xr4)
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_copy_text')
        cpu.data(b'HEX EXE:EDIT F\0\0')
        cpu.pop(cpu.xr4)
        cpu.label('mode_status')
        cpu.er2 = cpu.er14
        cpu.r0 = 0x28
        cpu.r1 = 0x19
        cpu.call(SMALL_TEXT_ADDRESS)
        cpu.call('cursor')
        cpu.call(ROM_REFRESH)
        cpu.label('key')
        cpu.r0 = cpu.mem8[0x808D]
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x4A
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.call('read_key')
        cpu.compare(cpu.r0, 0x02)
        cpu.compare_carry(cpu.r1, 0x7D)
        if cpu.ne:
            cpu.branch('skip_far_23')
        cpu.jump('function')
        cpu.label('skip_far_23')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_far_25')
        cpu.jump('key')
        cpu.label('skip_far_25')
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('skip_far_27')
        cpu.jump('cancel')
        cpu.label('skip_far_27')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.ne:
            cpu.branch('skip_far_29')
        cpu.jump('confirm')
        cpu.label('skip_far_29')
        cpu.r7 = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 38)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('typed_key')
        cpu.r0 = cpu.r7
        cpu.compare(cpu.r0, 0xFC)
        if cpu.ne:
            cpu.branch('skip_far_31')
        cpu.jump('left')
        cpu.label('skip_far_31')
        cpu.compare(cpu.r0, 0xFD)
        if cpu.ne:
            cpu.branch('skip_far_33')
        cpu.jump('right')
        cpu.label('skip_far_33')
        cpu.compare(cpu.r0, 0xFF)
        if cpu.ne:
            cpu.branch('skip_far_35')
        cpu.jump('up')
        cpu.label('skip_far_35')
        cpu.compare(cpu.r0, 0xFE)
        if cpu.ne:
            cpu.branch('skip_far_37')
        cpu.jump('down')
        cpu.label('skip_far_37')
        cpu.r7 = cpu.r0
        cpu.label('typed_key')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 38)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_far_39')
        cpu.jump('key')
        cpu.label('skip_far_39')
        cpu.r0 = cpu.r7
        cpu.compare(cpu.r0, 0x30)
        if cpu.ge:
            cpu.branch('skip_far_41')
        cpu.jump('key')
        cpu.label('skip_far_41')
        cpu.compare(cpu.r0, 0x3A)
        if cpu.ge:
            cpu.branch('letter_key')
        cpu.r0 += 0xD0
        cpu.jump('typed_nibble')
        cpu.label('letter_key')
        cpu.compare(cpu.r0, 0x41)
        if cpu.ge:
            cpu.branch('skip_far_45')
        cpu.jump('key')
        cpu.label('skip_far_45')
        cpu.compare(cpu.r0, 0x47)
        if cpu.lt:
            cpu.branch('skip_far_47')
        cpu.jump('key')
        cpu.label('skip_far_47')
        cpu.r0 += 0xC9
        cpu.label('typed_nibble')
        cpu.r7 = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 39)]
        cpu.compare(cpu.r0, 0x01)
        if cpu.eq:
            cpu.branch('low_nibble')
        cpu.r0 = cpu.r7
        cpu.r0 <<= 0x04
        cpu.mem8[cpu.offset(cpu.er14, 41)] = cpu.r0
        cpu.r0 = 0x01
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x49
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('draw')
        cpu.label('low_nibble')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 41)]
        cpu.r0 |= cpu.r7
        cpu.mem8[cpu.offset(cpu.er14, 41)] = cpu.r0
        cpu.r0 = 0x02
        cpu.mem8[cpu.offset(cpu.er14, 39)] = cpu.r0
        cpu.jump('draw')
        cpu.label('write_hint')
        cpu.jump('draw')
        cpu.label('confirm')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 38)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('write_confirm')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 40)]
        cpu.test_bit(cpu.r0, 3)
        if cpu.ne:
            cpu.branch('save_page')
        cpu.test_bit(cpu.r0, 2)
        if cpu.ne:
            cpu.jump('run')
        cpu.call('can_write')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.jump('read_only')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 45)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('edit_byte')
        cpu.call('fn_ui_menu')
        cpu.data(b'SYS DATA!\0CONTINUE EDIT\0BACK\0\0')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.jump('draw')
        cpu.label('edit_byte')
        cpu.r0 = 0x01
        cpu.mem8[cpu.offset(cpu.er14, 38)] = cpu.r0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 39)] = cpu.r0
        cpu.jump('draw')
        cpu.label('write_confirm')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 39)]
        cpu.compare(cpu.r0, 0x02)
        if cpu.ne:
            cpu.branch('write_hint')
        cpu.er2 = cpu.sp
        cpu.r0 = cpu.r5
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 41)]
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[cpu.offset(cpu.er14, 32)] = cpu.r0
        cpu.r0 = cpu.r5
        cpu.r0 >>= 0x03
        cpu.r1 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += 48
        cpu.er2 += cpu.er0
        cpu.r6 = cpu.mem8[cpu.er2]
        cpu.r1 = cpu.r5
        cpu.r1 &= 0x07
        cpu.r0 = 0x01
        cpu.r0 <<= cpu.r1
        cpu.r0 |= cpu.r6
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('cancel_byte')
        cpu.label('save_page')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 32)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.jump('draw')
        cpu.push(cpu.er4)
        cpu.er0 = cpu.er12
        cpu.r2 = cpu.mem8[cpu.offset(cpu.er14, 44)]
        cpu.er4 = 0x20
        cpu.er6 = 0x00
        cpu.call('fn_memory_confirm')
        cpu.pop(cpu.er4)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.jump('draw')
        cpu.label('save_confirmed')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 45)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('write_memory')
        cpu.er0 = cpu.er12
        cpu.er2 = cpu.sp
        cpu.call(JOURNAL_COMMIT)
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.jump('write_error')
        cpu.jump('read_mode')
        cpu.label('write_memory')
        cpu.r0 = cpu.r5
        cpu.mem8[cpu.offset(cpu.er14, 52)] = cpu.r0
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x4E
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r7 = cpu.r0
        cpu.er8 = cpu.sp
        cpu.er10 = cpu.er12
        cpu.r6 = 0x00
        cpu.label('memory_byte')
        cpu.r0 = cpu.r6
        cpu.r0 &= 0x07
        if cpu.ne:
            cpu.branch('memory_bit')
        cpu.r0 = cpu.r6
        cpu.r0 >>= 0x03
        cpu.r1 = 0x00
        cpu.er2 = cpu.sp
        cpu.er2 += cpu.er0
        cpu.r0 = 0x50
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.r4 = cpu.mem8[cpu.er2]
        cpu.label('memory_bit')
        cpu.test_bit(cpu.r4, 0)
        if cpu.eq:
            cpu.branch('memory_next')
        cpu.r3 = cpu.mem8[cpu.er8]
        cpu.r2 = cpu.r7
        cpu.mem8[cpu.r2, cpu.er10] = cpu.r3
        cpu.label('memory_next')
        cpu.r4 >>= 0x01
        cpu.er8 += 0x01
        cpu.er10 += 0x01
        cpu.r6 += 0x01
        cpu.compare(cpu.r6, 0x20)
        if cpu.lt:
            cpu.branch('memory_byte')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 52)]
        cpu.r5 = cpu.r0
        cpu.label('read_mode')
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 38)] = cpu.r0
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x49
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('load')
        cpu.label('cancel')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 38)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('cancel_byte')
        cpu.call('pending')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.jump('draw')
        cpu.r0 = 0x01
        cpu.jump('finish')
        cpu.label('cancel_byte')
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 38)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 39)] = cpu.r0
        cpu.jump('draw')
        cpu.label('function')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 38)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.jump('draw')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 40)]
        cpu.test_bit(cpu.r0, 3)
        if cpu.ne:
            cpu.branch('goto')
        cpu.call('fn_ui_menu')
        cpu.data(b'HEX\0GOTO\0EDIT BYTE\0REGION\0VIEW\0ASSEMBLE\0SAVE\0RUN\0HELP\0\0\0')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('goto')
        cpu.compare(cpu.r0, 0x01)
        if cpu.eq:
            cpu.branch('edit_menu')
        cpu.compare(cpu.r0, 0x02)
        if cpu.eq:
            cpu.branch('goto')
        cpu.compare(cpu.r0, 0x03)
        if cpu.eq:
            cpu.branch('view_menu')
        cpu.compare(cpu.r0, 0x04)
        if cpu.eq:
            cpu.branch('assemble')
        cpu.compare(cpu.r0, 0x05)
        if cpu.eq:
            cpu.jump('save_page')
        cpu.compare(cpu.r0, 0x06)
        if cpu.eq:
            cpu.branch('run')
        cpu.compare(cpu.r0, 0x07)
        if cpu.ne:
            cpu.jump('draw')
        cpu.call('fn_ui_menu')
        cpu.data(b'HEX HELP\0EXE EDIT BYTE\0F MENU *DIRTY\0EXIT BACK\0\0')
        cpu.jump('draw')
        cpu.label('edit_menu')
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 40)] = cpu.r0
        cpu.jump('confirm')
        cpu.label('view_menu')
        cpu.call('fn_ui_menu')
        cpu.data(b'VIEW\0HEX\0DISASM\0\0\0')
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.jump('draw')
        cpu.jump('toggle')
        cpu.label('assemble')
        cpu.call('pending')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.jump('draw')
        cpu.r0 = 0x02
        cpu.jump('finish')
        cpu.label('run')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 32)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.jump('save_first')
        cpu.r0 = 0x03
        cpu.jump('finish')
        cpu.label('goto')
        cpu.call('pending')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.jump('draw')
        cpu.er0 = cpu.er12
        cpu.r2 = cpu.r5
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.er8 = cpu.er0
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x4E
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r2 = cpu.r0
        cpu.er0 = cpu.er8
        cpu.call(MEMORY_GOTO_ADDRESS)
        cpu.compare(cpu.r3, 0x00)
        if cpu.ne:
            cpu.branch('skip_far_81')
        cpu.jump('draw')
        cpu.label('skip_far_81')
        cpu.er8 = cpu.er0
        cpu.r7 = cpu.r2
        cpu.r0 = cpu.r7
        cpu.mem8[cpu.offset(cpu.er14, 44)] = cpu.r0
        cpu.compare(cpu.r7, 0x08)
        if cpu.lt:
            cpu.branch('goto_sram')
        cpu.r0 = 0x00
        cpu.jump('goto_kind')
        cpu.label('goto_sram')
        cpu.compare(cpu.r7, 0x04)
        if cpu.ne:
            cpu.branch('goto_ram')
        cpu.r0 = 0x01
        cpu.jump('goto_kind')
        cpu.label('goto_ram')
        cpu.r0 = 0x02
        cpu.label('goto_kind')
        cpu.mem8[cpu.offset(cpu.er14, 45)] = cpu.r0
        cpu.er0 = cpu.er8
        cpu.r5 = cpu.r0
        cpu.r5 &= 0x1F
        cpu.er12 = cpu.er0
        cpu.r12 &= 0xE0
        cpu.jump('read_mode')
        cpu.label('toggle')
        cpu.r0 = cpu.mem8[0x808D]
        cpu.r0 &= 0xF3
        cpu.mem8[0x808D] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 39
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('skip_far_88')
        cpu.jump('write_hint')
        cpu.label('skip_far_88')
        cpu.call('pending')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.jump('draw')
        cpu.r0 = 0x00
        cpu.jump('finish')
        cpu.label('left')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 40)]
        cpu.r0 &= 0x08
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_far_93')
        cpu.jump('toggle')
        cpu.label('skip_far_93')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 39)]
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('skip_far_95')
        cpu.jump('write_back')
        cpu.label('skip_far_95')
        cpu.r0 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += 39
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.compare(cpu.r5, 0x00)
        if cpu.eq:
            cpu.branch('left_page')
        cpu.r5 += 0xFF
        cpu.jump('draw')
        cpu.label('left_page')
        cpu.r4 = 0x1F
        cpu.jump('previous_page')
        cpu.label('right')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 40)]
        cpu.r0 &= 0x08
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_far_100')
        cpu.jump('toggle')
        cpu.label('skip_far_100')
        cpu.er2 = cpu.er14
        cpu.er2 += 39
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('skip_far_102')
        cpu.jump('write_hint')
        cpu.label('skip_far_102')
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 39)] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 38
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_far_108')
        cpu.er2 = cpu.er14
        cpu.er2 += 45
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_far_108')
        cpu.er2 = cpu.er14
        cpu.er2 += 44
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x08)
        if cpu.ne:
            cpu.branch('skip_far_108')
        cpu.r0 = 0xE0
        cpu.r1 = 0x5F
        cpu.compare(cpu.er12, cpu.er0)
        if cpu.ne:
            cpu.branch('skip_far_108')
        cpu.compare(cpu.r5, 0x0F)
        if cpu.lt:
            cpu.branch('skip_far_108')
        cpu.jump('draw')
        cpu.label('skip_far_108')
        cpu.label('right_data')
        cpu.compare(cpu.r5, 0x1F)
        if cpu.eq:
            cpu.branch('right_page')
        cpu.r5 += 0x01
        cpu.jump('draw')
        cpu.label('right_page')
        cpu.r4 = 0x00
        cpu.jump('next_page')
        cpu.label('write_back')
        cpu.r0 = 0x00
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x49
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.jump('draw')
        cpu.label('up')
        cpu.er2 = cpu.er14
        cpu.er2 += 39
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('skip_far_114')
        cpu.jump('write_hint')
        cpu.label('skip_far_114')
        cpu.r0 = 0x00
        cpu.er2 = cpu.er14
        cpu.er2 += 39
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.compare(cpu.r5, 0x08)
        if cpu.lt:
            cpu.branch('up_page')
        cpu.r5 += 0xF8
        cpu.jump('draw')
        cpu.label('up_page')
        cpu.r4 = cpu.r5
        cpu.r4 += 0x18
        cpu.jump('previous_page')
        cpu.label('down')
        cpu.er2 = cpu.er14
        cpu.er2 += 39
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('skip_far_119')
        cpu.jump('write_hint')
        cpu.label('skip_far_119')
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 39)] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er2 += 38
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_far_125')
        cpu.er2 = cpu.er14
        cpu.er2 += 45
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_far_125')
        cpu.er2 = cpu.er14
        cpu.er2 += 44
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x08)
        if cpu.ne:
            cpu.branch('skip_far_125')
        cpu.r0 = 0xE0
        cpu.r1 = 0x5F
        cpu.compare(cpu.er12, cpu.er0)
        if cpu.ne:
            cpu.branch('skip_far_125')
        cpu.compare(cpu.r5, 0x08)
        if cpu.lt:
            cpu.branch('skip_far_125')
        cpu.jump('draw')
        cpu.label('skip_far_125')
        cpu.label('down_data')
        cpu.compare(cpu.r5, 0x18)
        if cpu.ge:
            cpu.branch('down_page')
        cpu.r5 += 0x08
        cpu.jump('draw')
        cpu.label('down_page')
        cpu.r4 = cpu.r5
        cpu.r4 += 0xE8
        cpu.jump('next_page')
        cpu.label('previous_page')
        cpu.call('at_begin')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_far_131')
        cpu.jump('draw')
        cpu.label('skip_far_131')
        cpu.er2 = cpu.er14
        cpu.er2 += 32
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_far_133')
        cpu.jump('save_first')
        cpu.label('skip_far_133')
        cpu.er0 = 0x00
        cpu.compare(cpu.er12, cpu.er0)
        if cpu.ne:
            cpu.branch('previous_offset')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 44)]
        cpu.r0 += 0xFF
        cpu.er2 = cpu.er14
        cpu.er2 += 44
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.label('previous_offset')
        cpu.er12 += -32
        cpu.r5 = cpu.r4
        cpu.jump('load')
        cpu.label('next_page')
        cpu.call('at_end')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_far_138')
        cpu.jump('draw')
        cpu.label('skip_far_138')
        cpu.er2 = cpu.er14
        cpu.er2 += 32
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_far_140')
        cpu.jump('save_first')
        cpu.label('skip_far_140')
        cpu.r0 = 0xE0
        cpu.r1 = 0xFF
        cpu.compare(cpu.er12, cpu.er0)
        if cpu.ne:
            cpu.branch('next_offset')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 44)]
        cpu.r0 += 0x01
        cpu.er2 = cpu.er14
        cpu.er2 += 44
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.label('next_offset')
        cpu.er12 += 0x20
        cpu.r5 = cpu.r4
        cpu.jump('load')
        cpu.label('write_error')
        cpu.er2 = cpu.sp
        cpu.er0 = 0x20
        cpu.er2 += cpu.er0
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0x45
        cpu.r3 = 0xD1
        cpu.er6 = 0x20
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.call('newline')
        cpu.jump('key')
        cpu.label('read_only')
        cpu.er2 = cpu.sp
        cpu.er0 = 0x20
        cpu.er2 += cpu.er0
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0x51
        cpu.r3 = 0xD1
        cpu.er6 = 0x20
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.call('newline')
        cpu.jump('key')
        cpu.label('save_first')
        cpu.call('pending')
        cpu.jump('draw')
        cpu.label('pending')
        cpu.push(cpu.lr)
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 32)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('pending_done')
        cpu.call('fn_ui_menu')
        cpu.data(b'UNSAVED\0SAVE\0DISCARD\0BACK\0\0\0')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('pending_discard')
        cpu.pop(cpu.lr)
        cpu.jump('save_page')
        cpu.label('pending_discard')
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('pending_back')
        cpu.er8 = cpu.er12
        cpu.er2 = cpu.er14
        cpu.er2 += -32
        cpu.r6 = 0x20
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 44)]
        cpu.label('discard_byte')
        cpu.r0 = cpu.mem8[cpu.r7, cpu.er8]
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 += 0x01
        cpu.er8 += 0x01
        cpu.r6 += 0xFF
        if cpu.ne:
            cpu.branch('discard_byte')
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 32)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 48)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 49)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 50)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 51)] = cpu.r0
        cpu.label('pending_done')
        cpu.pop(cpu.pc)
        cpu.label('pending_back')
        cpu.r0 = 0x01
        cpu.pop(cpu.pc)
        cpu.label('recover_error')
        cpu.er2 = cpu.sp
        cpu.er0 = 0x20
        cpu.er2 += cpu.er0
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0x6A
        cpu.r3 = 0xD1
        cpu.er6 = 0x20
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.call('newline')
        cpu.label('error_key')
        cpu.call(HEX_KEY_ADDRESS)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('error_key')
        cpu.r0 = 0x01
        cpu.label('finish')
        cpu.mem8[cpu.offset(cpu.er14, 42)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 34)]
        cpu.mem8[0x80A2] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 33)]
        cpu.mem8[0x80A0] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 44)]
        cpu.compare(cpu.r0, 0x08)
        if cpu.ne:
            cpu.branch('return_pc')
        cpu.er0 = cpu.er12
        cpu.r6 = cpu.r5
        cpu.r7 = 0x00
        cpu.er0 += cpu.er6
        cpu.r2 = 0x00
        cpu.r3 = 0x40
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('return_pc')
        cpu.r2 = 0xF0
        cpu.r3 = 0x5F
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('return_pc')
        cpu.er8 = cpu.er0
        cpu.jump('return_action')
        cpu.label('return_pc')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 46)]
        cpu.r8 = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 47)]
        cpu.r9 = cpu.r0
        cpu.label('return_action')
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x4C
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r2 = cpu.r0
        cpu.er0 = cpu.er8
        cpu.sp += 0x20
        cpu.sp += 0x20
        cpu.sp += 0x20
        cpu.pop(cpu.er14)
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('can_write')
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x4F
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('probe_yes')
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x4E
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x08)
        if cpu.ne:
            cpu.branch('probe_no')
        cpu.er0 = cpu.er12
        cpu.r2 = 0x00
        cpu.r3 = 0x40
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('probe_no')
        cpu.r2 = 0x00
        cpu.r3 = 0x60
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('probe_no')
        cpu.r0 = 0xE0
        cpu.r1 = 0x5F
        cpu.compare(cpu.er12, cpu.er0)
        if cpu.ne:
            cpu.branch('probe_yes')
        cpu.compare(cpu.r5, 0x10)
        if cpu.ge:
            cpu.branch('probe_no')
        cpu.jump('probe_yes')
        cpu.label('at_begin')
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x4F
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x02)
        if cpu.ne:
            cpu.branch('begin_external')
        cpu.r0 = 0x00
        cpu.r1 = 0x80
        cpu.jump('probe_page')
        cpu.label('begin_external')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('begin_offset')
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x4E
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x08)
        if cpu.ne:
            cpu.branch('probe_no')
        cpu.label('begin_offset')
        cpu.er0 = 0x00
        cpu.jump('probe_page')
        cpu.label('at_end')
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x4F
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('end_memory')
        cpu.push(cpu.er0)
        cpu.er2 = cpu.sp
        cpu.r0 = 0x4E
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x0F)
        if cpu.ne:
            cpu.branch('probe_no')
        cpu.r0 = 0xE0
        cpu.r1 = 0xFF
        cpu.jump('probe_page')
        cpu.label('end_memory')
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.branch('end_ram')
        cpu.r0 = 0xE0
        cpu.r1 = 0x7F
        cpu.jump('probe_page')
        cpu.label('end_ram')
        cpu.r0 = 0xE0
        cpu.r1 = 0x8D
        cpu.label('probe_page')
        cpu.compare(cpu.er12, cpu.er0)
        if cpu.ne:
            cpu.branch('probe_no')
        cpu.label('probe_yes')
        cpu.r0 = 0x01
        cpu.ret()
        cpu.label('probe_no')
        cpu.r0 = 0x00
        cpu.ret()
        cpu.label('read_key')
        cpu.er8 = cpu.sp
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x55
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('new_key')
        cpu.call('same_held_key')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('new_key')
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x5A
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('repeat_initial_delay')
        cpu.r6 = 0x08
        cpu.jump('repeat_delay')
        cpu.label('repeat_initial_delay')
        cpu.r6 = 0x18
        cpu.label('repeat_delay')
        cpu.r0 = 0x80
        cpu.r1 = 0x00
        cpu.call(0x05CC6)
        cpu.call('same_held_key')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('new_key')
        cpu.r6 += 0xFF
        if cpu.ne:
            cpu.branch('repeat_delay')
        cpu.r0 = 0x01
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x5A
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x55
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.jump('key_return')
        cpu.label('new_key')
        cpu.r0 = 0x00
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x55
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.call(HEX_KEY_ADDRESS)
        cpu.compare(cpu.r0, 0xFC)
        if cpu.lt:
            cpu.branch('key_return')
        cpu.r4 = cpu.r0
        cpu.er0 = cpu.er8
        cpu.r2 = 0x56
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.call(0x12864)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('arrow_return')
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x56
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x58
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x57
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x59
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = 0x00
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x5A
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = cpu.r4
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x55
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.label('arrow_return')
        cpu.r0 = cpu.r4
        cpu.label('key_return')
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('same_held_key')
        cpu.push(cpu.lr)
        cpu.er0 = cpu.er8
        cpu.r2 = 0x56
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.call(0x12864)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('held_no')
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x56
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r4 = cpu.r0
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x58
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, cpu.r4)
        if cpu.ne:
            cpu.branch('held_no')
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x57
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r4 = cpu.r0
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x59
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, cpu.r4)
        if cpu.ne:
            cpu.branch('held_no')
        cpu.r0 = 0x01
        cpu.pop(cpu.pc)
        cpu.label('held_no')
        cpu.r0 = 0x00
        cpu.pop(cpu.pc)
        cpu.label('hexbyte')
        cpu.push(cpu.lr)
        cpu.r3 = cpu.r0
        cpu.r0 >>= 0x04
        cpu.call('nibble')
        cpu.r2 = cpu.r0
        cpu.r0 = cpu.r3
        cpu.r0 &= 0x0F
        cpu.call('nibble')
        cpu.r1 = cpu.r0
        cpu.r0 = cpu.r2
        cpu.pop(cpu.pc)
        cpu.label('nibble')
        cpu.compare(cpu.r0, 0x0A)
        if cpu.lt:
            cpu.branch('digit')
        cpu.r0 += 0x37
        cpu.ret()
        cpu.label('digit')
        cpu.r0 += 0x30
        cpu.ret()
        cpu.label('cursor')
        cpu.r8 = cpu.r5
        cpu.r8 &= 0x18
        cpu.r9 = 0x00
        cpu.r1 = 0x09
        cpu.multiply(cpu.er8, cpu.r1)
        cpu.r0 = cpu.r5
        cpu.r0 &= 0x07
        cpu.r2 = cpu.r0
        cpu.r0 += cpu.r0
        cpu.r0 += cpu.r2
        cpu.r0 >>= 0x01
        cpu.r1 = 0x00
        cpu.er0 += cpu.er8
        cpu.r2 = 0xEC
        cpu.r3 = 0x80
        cpu.er2 += cpu.er0
        cpu.r0 = cpu.r5
        cpu.r0 &= 0x01
        if cpu.eq:
            cpu.branch('cursor_even')
        cpu.r6 = 0x0F
        cpu.r7 = 0xFF
        cpu.jump('cursor_start')
        cpu.label('cursor_even')
        cpu.r6 = 0xFF
        cpu.r7 = 0xF0
        cpu.label('cursor_start')
        cpu.r4 = 0x06
        cpu.label('cursor_line')
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 ^= cpu.r6
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 += 0x01
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 ^= cpu.r7
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 += 0x0B
        cpu.r4 += 0xFF
        if cpu.ne:
            cpu.branch('cursor_line')
        cpu.ret()
        cpu.label('newline')
        cpu.push(cpu.xr8)
        cpu.er8 = cpu.sp
        cpu.er8 += 0x04
        cpu.push(cpu.lr)
        cpu.r0 = cpu.mem8[0x80A0]
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x44
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A2]
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x45
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = 0x07
        cpu.mem8[0x80A0] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x80A2] = cpu.r0
        cpu.call(0x0409A)
        cpu.er2 = cpu.er8
        cpu.er0 = 0x20
        cpu.er2 += cpu.er0
        cpu.r0 = 0x00
        cpu.r1 = 0x01
        cpu.call(ROM_DRAW_TEXT)
        cpu.call(ROM_REFRESH)
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x45
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.mem8[0x80A2] = cpu.r0
        cpu.push(cpu.er0)
        cpu.er2 = cpu.er8
        cpu.r0 = 0x44
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.pop(cpu.er0)
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.mem8[0x80A0] = cpu.r0
        cpu.pop(cpu.lr)
        cpu.pop(cpu.xr8)
        cpu.ret()


    @fw.function(native=True, address=0xFE000)
    def program():
        cpu.label('program')
        cpu.label('entry')
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.push(cpu.er12)
        cpu.push(cpu.er14)
        cpu.sp += -32
        cpu.sp += -32
        cpu.sp += -32
        cpu.sp += -32
        cpu.sp += -32
        cpu.er14 = cpu.sp
        cpu.er0 = cpu.er12
        cpu.r2 = cpu.r5
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.mem16[cpu.offset(cpu.er14, 42)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 44)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 46)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 130)] = cpu.er0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 48)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 64)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 65)] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.r10 = 0x84
        cpu.r11 = 0x00
        cpu.er2 += cpu.er10
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.call(JOURNAL_RECOVER)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.jump('switch_view')
        cpu.er2 = cpu.er14
        cpu.er10 = 0x10
        cpu.er2 += cpu.er10
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0x6A
        cpu.r3 = 0xD1
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.call('message')
        cpu.label('recover_key')
        cpu.call(SCANNER_ADDRESS)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('recover_key')
        cpu.jump('exit')
        cpu.label('draw')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 132)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_4')
        cpu.jump('draw_detail')
        cpu.label('skip_4')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 130)]
        cpu.er8 = cpu.er0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 42)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x2B
        cpu.er2 += cpu.er10
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.er0 = cpu.er8
        cpu.call(VIEW_ADDRESS)
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('skip_6')
        cpu.jump('bad_instruction')
        cpu.label('skip_6')
        cpu.er0 = cpu.er2
        cpu.mem16[cpu.offset(cpu.er14, 130)] = cpu.er0
        cpu.jump('skip_9')
        cpu.label('draw_detail')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 42)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x2B
        cpu.er2 += cpu.er10
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.call(DETAIL_ADDRESS)
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('skip_9')
        cpu.jump('bad_instruction')
        cpu.label('skip_9')
        cpu.label('drawn')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 132)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_11')
        cpu.jump('input')
        cpu.label('skip_11')
        cpu.er2 = cpu.er14
        cpu.r10 = 0x41
        cpu.r11 = 0x00
        cpu.er2 += cpu.er10
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_13')
        cpu.jump('input')
        cpu.label('skip_13')
        cpu.call('queue_line')
        cpu.label('input')
        cpu.er2 = cpu.er14
        cpu.er10 = 0x30
        cpu.er2 += cpu.er10
        cpu.r0 = cpu.mem8[0x808D]
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.call(SCANNER_ADDRESS)
        cpu.compare(cpu.r0, 0x02)
        cpu.compare_carry(cpu.r1, 0x7D)
        if cpu.ne:
            cpu.branch('skip_16')
        cpu.jump('function')
        cpu.label('skip_16')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('input')
        cpu.compare(cpu.r0, 0xFC)
        if cpu.ne:
            cpu.branch('skip_19')
        cpu.jump('view_key')
        cpu.label('skip_19')
        cpu.compare(cpu.r0, 0xFD)
        if cpu.ne:
            cpu.branch('skip_21')
        cpu.jump('view_key')
        cpu.label('skip_21')
        cpu.compare(cpu.r0, 0xFA)
        if cpu.ne:
            cpu.branch('skip_23')
        cpu.jump('exit_key')
        cpu.label('skip_23')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.ne:
            cpu.branch('skip_25')
        cpu.jump('confirm')
        cpu.label('skip_25')
        cpu.compare(cpu.r0, 0xFF)
        if cpu.ne:
            cpu.branch('skip_27')
        cpu.jump('previous')
        cpu.label('skip_27')
        cpu.compare(cpu.r0, 0xFE)
        if cpu.ne:
            cpu.branch('skip_29')
        cpu.jump('following')
        cpu.label('skip_29')
        cpu.jump('input')
        cpu.label('function')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 48)]
        cpu.r0 &= 0x08
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_32')
        cpu.jump('goto')
        cpu.label('skip_32')
        cpu.call('fn_ui_menu')
        cpu.data(b'CODE\0GOTO\0HEX EDIT\0REGION IN HEX\0VIEW\0ASSEMBLE\0SAVE\0RUN\0HELP\0\0')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('goto')
        cpu.compare(cpu.r0, 0x01)
        if cpu.eq:
            cpu.branch('switch_view')
        cpu.compare(cpu.r0, 0x02)
        if cpu.eq:
            cpu.branch('switch_view')
        cpu.compare(cpu.r0, 0x03)
        if cpu.eq:
            cpu.branch('choose_view')
        cpu.compare(cpu.r0, 0x04)
        if cpu.eq:
            cpu.jump('select')
        cpu.compare(cpu.r0, 0x05)
        if cpu.eq:
            cpu.jump('commit')
        cpu.compare(cpu.r0, 0x06)
        if cpu.eq:
            cpu.jump('run')
        cpu.compare(cpu.r0, 0x07)
        if cpu.ne:
            cpu.jump('draw')
        cpu.call('fn_ui_menu')
        cpu.data(b'CODE HELP\0EXE ASSEMBLE\0RIGHT EXPAND\0EXIT HEX\0\0')
        cpu.jump('draw')
        cpu.label('choose_view')
        cpu.call('fn_ui_menu')
        cpu.data(b'VIEW\0HEX\0DISASM\0\0\0')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('switch_view')
        cpu.jump('draw')
        cpu.label('view_key')
        cpu.r6 = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 48)]
        cpu.r0 &= 0x08
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_35')
        cpu.jump('switch_view')
        cpu.label('skip_35')
        cpu.compare(cpu.r6, 0xFC)
        if cpu.ne:
            cpu.branch('skip_37')
        cpu.jump('detail_back')
        cpu.label('skip_37')
        cpu.r0 = 0x01
        cpu.mem8[cpu.offset(cpu.er14, 132)] = cpu.r0
        cpu.jump('draw')
        cpu.label('detail_back')
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 132)] = cpu.r0
        cpu.jump('draw')
        cpu.label('switch_view')
        cpu.r0 = cpu.mem8[0x808D]
        cpu.r0 &= 0xF3
        cpu.mem8[0x808D] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 65)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_41')
        cpu.jump('save_first')
        cpu.label('skip_41')
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 132)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 44)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x2D
        cpu.er2 += cpu.er10
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.call('fn_editor')
        cpu.r7 = cpu.r2
        cpu.mem16[cpu.offset(cpu.er14, 44)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 42)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 130)] = cpu.er0
        cpu.compare(cpu.r7, 0x01)
        if cpu.ne:
            cpu.branch('skip_43')
        cpu.jump('exit')
        cpu.label('skip_43')
        cpu.compare(cpu.r7, 0x02)
        if cpu.ne:
            cpu.branch('skip_45')
        cpu.jump('select')
        cpu.label('skip_45')
        cpu.compare(cpu.r7, 0x03)
        if cpu.eq:
            cpu.branch('run')
        cpu.jump('draw')
        cpu.label('goto')
        cpu.r0 = cpu.mem8[0x808D]
        cpu.r0 &= 0xF3
        cpu.mem8[0x808D] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 65)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_48')
        cpu.jump('save_first')
        cpu.label('skip_48')
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 132)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 44)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x2D
        cpu.er2 += cpu.er10
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.r2 = 0x01
        cpu.call(GOTO_ADDRESS)
        cpu.compare(cpu.r2, 0x00)
        if cpu.ne:
            cpu.branch('skip_50')
        cpu.jump('draw')
        cpu.label('skip_50')
        cpu.mem16[cpu.offset(cpu.er14, 44)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 42)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 130)] = cpu.er0
        cpu.jump('draw')
        cpu.label('confirm')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 48)]
        cpu.r0 &= 0x08
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_53')
        cpu.jump('check_alpha')
        cpu.label('skip_53')
        cpu.jump('commit')
        cpu.label('check_alpha')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 48)]
        cpu.r0 &= 0x04
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_56')
        cpu.jump('select')
        cpu.label('skip_56')
        cpu.label('run')
        cpu.er2 = cpu.er14
        cpu.r10 = 0x41
        cpu.r11 = 0x00
        cpu.er2 += cpu.er10
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_58')
        cpu.jump('save_first')
        cpu.label('skip_58')
        cpu.r0 = 0x00
        cpu.r1 = 0x40
        cpu.r2 = 0x08
        cpu.r0 = cpu.mem8[cpu.r2, cpu.er0]
        cpu.compare(cpu.r0, 0xFF)
        if cpu.ne:
            cpu.branch('skip_60')
        cpu.jump('empty')
        cpu.label('skip_60')
        cpu.er0 = 0x4000
        cpu.r2 = 0x08
        cpu.er4 = 0x1FF0
        cpu.er6 = 0x01
        cpu.call('fn_memory_confirm')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.jump('draw')
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.call(0x84000)
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.jump('draw')
        cpu.label('empty')
        cpu.er2 = cpu.er14
        cpu.er10 = 0x10
        cpu.er2 += cpu.er10
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0x78
        cpu.r3 = 0xD1
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.call('message')
        cpu.jump('input')
        cpu.label('previous')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 65)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_65')
        cpu.jump('save_first')
        cpu.label('skip_65')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 44)]
        cpu.r2 = 0x00
        cpu.r3 = 0x40
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ne:
            cpu.branch('skip_67')
        cpu.jump('draw')
        cpu.label('skip_67')
        cpu.r0 = 0x00
        cpu.r1 = 0x40
        cpu.mem16[cpu.offset(cpu.er14, 46)] = cpu.er0
        cpu.label('scan_back')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 46)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x2F
        cpu.er2 += cpu.er10
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.call(CODEC_LENGTH_ADDRESS)
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('skip_69')
        cpu.jump('bad_instruction')
        cpu.label('skip_69')
        cpu.r6 = cpu.r0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 46)]
        cpu.r2 = cpu.r6
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.er4 = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 44)]
        cpu.compare(cpu.er4, cpu.er0)
        if cpu.lt:
            cpu.branch('skip_71')
        cpu.jump('back_ready')
        cpu.label('skip_71')
        cpu.er0 = cpu.er4
        cpu.mem16[cpu.offset(cpu.er14, 46)] = cpu.er0
        cpu.jump('scan_back')
        cpu.label('back_ready')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 46)]
        cpu.mem16[cpu.offset(cpu.er14, 44)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 42)] = cpu.er0
        cpu.jump('draw')
        cpu.label('following')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 65)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_75')
        cpu.jump('save_first')
        cpu.label('skip_75')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 44)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x2D
        cpu.er2 += cpu.er10
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.call(CODEC_LENGTH_ADDRESS)
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('skip_77')
        cpu.jump('bad_instruction')
        cpu.label('skip_77')
        cpu.r6 = cpu.r0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 44)]
        cpu.r2 = cpu.r6
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.r2 = 0xF0
        cpu.r3 = 0x5F
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.lt:
            cpu.branch('skip_79')
        cpu.jump('draw')
        cpu.label('skip_79')
        cpu.mem16[cpu.offset(cpu.er14, 44)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 42)] = cpu.er0
        cpu.jump('draw')
        cpu.label('select')
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 132)] = cpu.r0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 42)]
        cpu.mem16[cpu.offset(cpu.er14, 130)] = cpu.er0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 65)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_82')
        cpu.jump('selected_source')
        cpu.label('skip_82')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 42)]
        cpu.mem16[cpu.offset(cpu.er14, 46)] = cpu.er0
        cpu.label('selected_source')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 42)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x2B
        cpu.er2 += cpu.er10
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.call(CODEC_LENGTH_ADDRESS)
        cpu.compare(cpu.r1, 0xFF)
        if cpu.ne:
            cpu.branch('skip_84')
        cpu.jump('bad_instruction')
        cpu.label('skip_84')
        cpu.mem8[cpu.offset(cpu.er14, 49)] = cpu.r0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 44)]
        cpu.r7 = cpu.r0
        cpu.r7 &= 0x0F
        cpu.er2 = cpu.er14
        cpu.r0 = 0x10
        cpu.label('clear_page')
        cpu.r6 = 0xFF
        cpu.mem8[cpu.er2] = cpu.r6
        cpu.er2 += 0x01
        cpu.r0 += 0xFF
        if cpu.ne:
            cpu.branch('clear_page')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 42)]
        cpu.er8 = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 44)]
        cpu.r7 = cpu.r0
        cpu.r7 &= 0x0F
        cpu.r6 = 0x02
        cpu.label('fill_page')
        cpu.er2 = cpu.er14
        cpu.r0 = cpu.r7
        cpu.r1 = 0x00
        cpu.er2 += cpu.er0
        cpu.r0 = cpu.mem8[0x08, cpu.er8]
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er8 += 0x01
        cpu.r7 += 0x01
        cpu.r6 += 0xFF
        if cpu.ne:
            cpu.branch('fill_page')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 44)]
        cpu.r0 &= 0xF0
        cpu.er2 = cpu.er0
        cpu.er2 = cpu.er14
        cpu.er10 = 0x20
        cpu.er2 += cpu.er10
        cpu.er6 = cpu.er2
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 44)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x2D
        cpu.er2 += cpu.er10
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.r5 = cpu.r0
        cpu.r5 &= 0x0F
        cpu.r0 &= 0xF0
        cpu.er2 = cpu.er0
        cpu.er0 = cpu.er14
        cpu.call(ISA_ENTRY_ADDRESS)
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_88')
        cpu.jump('draw')
        cpu.label('skip_88')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 44)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x21
        cpu.er2 += cpu.er10
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.r2 = 0xF0
        cpu.r3 = 0x5F
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_90')
        cpu.jump('skip_92')
        cpu.label('skip_90')
        if cpu.eq:
            cpu.branch('skip_92')
        cpu.jump('space_error')
        cpu.label('skip_92')
        cpu.label('new_space')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 42)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x31
        cpu.er2 += cpu.er10
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.r2 = 0xF0
        cpu.r3 = 0x5F
        cpu.compare(cpu.er0, cpu.er2)
        if cpu.ge:
            cpu.branch('skip_94')
        cpu.jump('skip_96')
        cpu.label('skip_94')
        if cpu.eq:
            cpu.branch('skip_96')
        cpu.jump('space_error')
        cpu.label('skip_96')
        cpu.label('source_space')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 33)]
        cpu.r7 = cpu.r0
        cpu.er2 = cpu.er14
        cpu.r10 = 0x41
        cpu.r11 = 0x00
        cpu.er2 += cpu.er10
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.r0 += cpu.r7
        cpu.compare(cpu.r0, 0x41)
        if cpu.lt:
            cpu.branch('skip_98')
        cpu.jump('commit_then_append')
        cpu.label('skip_98')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 64)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x31
        cpu.er2 += cpu.er10
        cpu.r7 = cpu.mem8[cpu.er2]
        cpu.r1 = 0x00
        cpu.r0 += cpu.r7
        cpu.add_carry(cpu.r1, 0x00)
        cpu.compare(cpu.r1, 0x00)
        if cpu.eq:
            cpu.branch('skip_100')
        cpu.jump('commit_then_append')
        cpu.label('skip_100')
        cpu.compare(cpu.r0, 0xFF)
        if cpu.ge:
            cpu.branch('skip_102')
        cpu.jump('append')
        cpu.label('skip_102')
        cpu.jump('commit_then_append')
        cpu.label('commit_then_append')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 46)]
        cpu.r2 = 0x08
        cpu.r4 = cpu.mem8[cpu.offset(cpu.er14, 65)]
        cpu.r5 = 0x00
        cpu.er6 = 0x00
        cpu.call('fn_memory_confirm')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.jump('draw')
        cpu.call('write_batch')
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.jump('write_error')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 44)]
        cpu.mem16[cpu.offset(cpu.er14, 42)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 46)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 130)] = cpu.er0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 64)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 65)] = cpu.r0
        cpu.label('append')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 64)]
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 49)]
        cpu.r0 += cpu.r7
        cpu.mem8[cpu.offset(cpu.er14, 64)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 65)]
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 33)]
        cpu.r0 += cpu.r7
        cpu.mem8[cpu.offset(cpu.er14, 65)] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 65)]
        cpu.r7 = cpu.mem8[cpu.offset(cpu.er14, 33)]
        cpu.r0 -= cpu.r7
        cpu.r6 = cpu.r0
        cpu.er8 = cpu.er14
        cpu.er0 = 0x22
        cpu.er8 += cpu.er0
        cpu.er10 = cpu.er14
        cpu.r0 = 0x42
        cpu.r1 = 0x00
        cpu.er10 += cpu.er0
        cpu.r0 = cpu.r6
        cpu.r1 = 0x00
        cpu.er10 += cpu.er0
        cpu.label('copy_instruction')
        cpu.er2 = cpu.er8
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er10
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er8 += 0x01
        cpu.er10 += 0x01
        cpu.r7 += 0xFF
        if cpu.ne:
            cpu.branch('copy_instruction')
        cpu.label('copied')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 42)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x31
        cpu.er2 += cpu.er10
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.mem16[cpu.offset(cpu.er14, 42)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 130)] = cpu.er0
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 44)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x21
        cpu.er2 += cpu.er10
        cpu.r2 = cpu.mem8[cpu.er2]
        cpu.r3 = 0x00
        cpu.er0 += cpu.er2
        cpu.mem16[cpu.offset(cpu.er14, 44)] = cpu.er0
        cpu.jump('draw')
        cpu.label('commit')
        cpu.er2 = cpu.er14
        cpu.r10 = 0x41
        cpu.r11 = 0x00
        cpu.er2 += cpu.er10
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_110')
        cpu.jump('draw')
        cpu.label('skip_110')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 46)]
        cpu.r2 = 0x08
        cpu.r4 = cpu.mem8[cpu.offset(cpu.er14, 65)]
        cpu.r5 = 0x00
        cpu.er6 = 0x00
        cpu.call('fn_memory_confirm')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.jump('draw')
        cpu.call('write_batch')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_113')
        cpu.jump('write_error')
        cpu.label('skip_113')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 44)]
        cpu.mem16[cpu.offset(cpu.er14, 42)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 46)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 130)] = cpu.er0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 64)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 65)] = cpu.r0
        cpu.jump('draw')
        cpu.label('write_batch')
        cpu.push(cpu.lr)
        cpu.er2 = cpu.er14
        cpu.r10 = 0x40
        cpu.r11 = 0x00
        cpu.er2 += cpu.er10
        cpu.er6 = cpu.er2
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 46)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x2F
        cpu.er2 += cpu.er10
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.call(BATCH_ADDRESS)
        cpu.pop(cpu.pc)
        cpu.label('exit_key')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 132)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('skip_116')
        cpu.jump('detail_back')
        cpu.label('skip_116')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 65)]
        cpu.compare(cpu.r0, 0x00)
        if cpu.ne:
            cpu.branch('skip_118')
        cpu.jump('switch_view')
        cpu.label('skip_118')
        cpu.call('fn_ui_menu')
        cpu.data(b'UNSAVED\0SAVE\0DISCARD\0BACK\0\0\0')
        cpu.compare(cpu.r0, 0x00)
        if cpu.eq:
            cpu.branch('commit')
        cpu.compare(cpu.r0, 0x01)
        if cpu.ne:
            cpu.jump('draw')
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 46)]
        cpu.mem16[cpu.offset(cpu.er14, 44)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 42)] = cpu.er0
        cpu.mem16[cpu.offset(cpu.er14, 130)] = cpu.er0
        cpu.r0 = 0x00
        cpu.mem8[cpu.offset(cpu.er14, 64)] = cpu.r0
        cpu.mem8[cpu.offset(cpu.er14, 65)] = cpu.r0
        cpu.jump('switch_view')
        cpu.label('bad_instruction')
        cpu.er2 = cpu.er14
        cpu.er10 = 0x10
        cpu.er2 += cpu.er10
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0x97
        cpu.r3 = 0xD1
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.call('message')
        cpu.call('queue_line')
        cpu.jump('input')
        cpu.label('save_first')
        cpu.er2 = cpu.er14
        cpu.er10 = 0x10
        cpu.er2 += cpu.er10
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0xA2
        cpu.r3 = 0xD1
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.call('message')
        cpu.jump('input')
        cpu.label('write_error')
        cpu.er2 = cpu.er14
        cpu.er10 = 0x10
        cpu.er2 += cpu.er10
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0x45
        cpu.r3 = 0xD1
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.call('message')
        cpu.jump('input')
        cpu.label('space_error')
        cpu.er2 = cpu.er14
        cpu.er10 = 0x10
        cpu.er2 += cpu.er10
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0xAD
        cpu.r3 = 0xD1
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.call('message')
        cpu.jump('input')
        cpu.label('queue_line')
        cpu.push(cpu.lr)
        cpu.er0 = cpu.mem16[cpu.offset(cpu.er14, 44)]
        cpu.r8 = cpu.r0
        cpu.r9 = cpu.r1
        cpu.r6 = cpu.mem8[cpu.offset(cpu.er14, 65)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x10
        cpu.er2 += cpu.er10
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0xBA
        cpu.r3 = 0xD1
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.er10 = 0x15
        cpu.er2 += cpu.er10
        cpu.r0 = cpu.r9
        cpu.r0 >>= 0x04
        cpu.r0 &= 0x0F
        cpu.call('hex_digit')
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 += 0x01
        cpu.r0 = cpu.r9
        cpu.r0 &= 0x0F
        cpu.call('hex_digit')
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 += 0x01
        cpu.r0 = cpu.r8
        cpu.r0 >>= 0x04
        cpu.r0 &= 0x0F
        cpu.call('hex_digit')
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 += 0x01
        cpu.r0 = cpu.r8
        cpu.r0 &= 0x0F
        cpu.call('hex_digit')
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 += 0x01
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0xC0
        cpu.r3 = 0xD1
        cpu.er6 = 0x11
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.er10 = 0x1B
        cpu.er2 += cpu.er10
        cpu.r8 = cpu.r6
        cpu.r0 = cpu.r8
        cpu.r0 >>= 0x04
        cpu.r0 &= 0x0F
        cpu.call('hex_digit')
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 += 0x01
        cpu.r0 = cpu.r8
        cpu.r0 &= 0x0F
        cpu.call('hex_digit')
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.er2 += 0x01
        cpu.r0 = 0x00
        cpu.mem8[cpu.er2] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A0]
        cpu.mem8[cpu.offset(cpu.er14, 50)] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A2]
        cpu.mem8[cpu.offset(cpu.er14, 51)] = cpu.r0
        cpu.r0 = 0x07
        cpu.mem8[0x80A0] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x80A2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er10 = 0x10
        cpu.er2 += cpu.er10
        cpu.r0 = 0x00
        cpu.r1 = 0x19
        cpu.call(ROM_DRAW_TEXT)
        cpu.push(cpu.xr4)
        cpu.er0 = cpu.er14
        cpu.er0 += 16
        cpu.call('fn_apps_copy_text')
        cpu.data(b'ASM\0')
        cpu.pop(cpu.xr4)
        cpu.er2 = cpu.er14
        cpu.er2 += 16
        cpu.r0 = 0x4E
        cpu.r1 = 0x19
        cpu.call(ROM_DRAW_TEXT)
        cpu.call(ROM_REFRESH)
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 51)]
        cpu.mem8[0x80A2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er10 = 0x32
        cpu.er2 += cpu.er10
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.mem8[0x80A0] = cpu.r0
        cpu.pop(cpu.pc)
        cpu.label('hex_digit')
        cpu.compare(cpu.r0, 0x0A)
        if cpu.lt:
            cpu.branch('skip_144')
        cpu.jump('hex_letter')
        cpu.label('skip_144')
        cpu.r0 += 0x30
        cpu.ret()
        cpu.label('hex_letter')
        cpu.r0 += 0x37
        cpu.ret()
        cpu.label('message')
        cpu.push(cpu.lr)
        cpu.call(0x0409A)
        cpu.r0 = cpu.mem8[0x80A0]
        cpu.mem8[cpu.offset(cpu.er14, 50)] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A2]
        cpu.mem8[cpu.offset(cpu.er14, 51)] = cpu.r0
        cpu.r0 = 0x07
        cpu.mem8[0x80A0] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x80A2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er10 = 0x10
        cpu.er2 += cpu.er10
        cpu.r0 = 0x00
        cpu.r1 = 0x09
        cpu.call(ROM_DRAW_TEXT)
        cpu.er2 = cpu.er14
        cpu.er10 = 0x10
        cpu.er2 += cpu.er10
        cpu.push(cpu.er6)
        cpu.er0 = cpu.er2
        cpu.r2 = 0xC3
        cpu.r3 = 0xD1
        cpu.er6 = 0x1A
        cpu.call(UI_TEXT_ADDRESS)
        cpu.pop(cpu.er6)
        cpu.er2 = cpu.er14
        cpu.er10 = 0x10
        cpu.er2 += cpu.er10
        cpu.r0 = 0x5A
        cpu.r1 = 0x19
        cpu.call(ROM_DRAW_TEXT)
        cpu.call(ROM_REFRESH)
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 51)]
        cpu.mem8[0x80A2] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.er10 = 0x32
        cpu.er2 += cpu.er10
        cpu.r0 = cpu.mem8[cpu.er2]
        cpu.mem8[0x80A0] = cpu.r0
        cpu.pop(cpu.pc)
        cpu.label('exit')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 44)]
        cpu.er2 = cpu.er14
        cpu.er10 = 0x2D
        cpu.er2 += cpu.er10
        cpu.r1 = cpu.mem8[cpu.er2]
        cpu.er2 = cpu.er0
        cpu.sp += 0x20
        cpu.sp += 0x20
        cpu.sp += 0x20
        cpu.sp += 0x20
        cpu.sp += 0x20
        cpu.pop(cpu.er14)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)


    @fw.function(native=True)
    def memory_confirm():
        cpu.push(cpu.lr)
        cpu.push(cpu.xr4)
        cpu.push(cpu.qr8)
        cpu.push(cpu.er12)
        cpu.push(cpu.er14)
        cpu.sp += -32
        cpu.er14 = cpu.sp
        cpu.er8 = cpu.er0
        cpu.r10 = cpu.r2
        cpu.r11 = cpu.r6
        cpu.er12 = cpu.er4
        cpu.r0 = cpu.mem8[0x80A0]
        cpu.mem8[cpu.offset(cpu.er14, 30)] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A2]
        cpu.mem8[cpu.offset(cpu.er14, 31)] = cpu.r0
        cpu.r0 = cpu.mem8[0x80A1]
        cpu.mem8[cpu.offset(cpu.er14, 29)] = cpu.r0
        cpu.r0 = 0
        cpu.mem8[0x80A1] = cpu.r0
        cpu.r0 = 0x07
        cpu.mem8[0x80A0] = cpu.r0
        cpu.r0 = 0x01
        cpu.mem8[0x80A2] = cpu.r0
        cpu.call(0x0409A)
        cpu.compare(cpu.r11, 0x00)
        if cpu.ne:
            cpu.branch('run')
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_copy_text')
        cpu.data(b'SAVE\0\0')
        cpu.jump('title')
        cpu.label('run')
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_copy_text')
        cpu.data(b'RUN S1 RANGE\0\0')
        cpu.label('title')
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x01
        cpu.call(ROM_DRAW_TEXT)
        cpu.ea = cpu.address(cpu.er14)
        cpu.r0 = cpu.r10
        cpu.call('digit')
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.r0 = 0x3A
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.er4 = cpu.er8
        cpu.call('word')
        cpu.r0 = 0x20
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.r0 = 0x2B
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.er4 = cpu.er12
        cpu.call('word')
        cpu.r0 = 0x00
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x09
        cpu.call(ROM_DRAW_TEXT)
        cpu.er0 = cpu.er14
        cpu.call('fn_apps_copy_text')
        cpu.data(b'EXE OK EXIT BACK\0\0')
        cpu.er2 = cpu.er14
        cpu.r0 = 0x00
        cpu.r1 = 0x19
        cpu.call(ROM_DRAW_TEXT)
        cpu.call(ROM_REFRESH)
        cpu.r0 = cpu.mem8[0x808D]
        cpu.r0 &= 0xF3
        cpu.mem8[0x808D] = cpu.r0
        cpu.label('key')
        cpu.call(SCANNER_ADDRESS)
        cpu.compare(cpu.r0, 0xFA)
        if cpu.eq:
            cpu.branch('cancel')
        cpu.compare(cpu.r0, 0xFB)
        if cpu.ne:
            cpu.branch('key')
        cpu.er6 = 0x01
        cpu.jump('return')
        cpu.label('cancel')
        cpu.er6 = 0x00
        cpu.label('return')
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 29)]
        cpu.mem8[0x80A1] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 30)]
        cpu.mem8[0x80A0] = cpu.r0
        cpu.r0 = cpu.mem8[cpu.offset(cpu.er14, 31)]
        cpu.mem8[0x80A2] = cpu.r0
        cpu.er0 = cpu.er6
        cpu.sp += 32
        cpu.pop(cpu.er14)
        cpu.pop(cpu.er12)
        cpu.pop(cpu.qr8)
        cpu.pop(cpu.xr4)
        cpu.pop(cpu.pc)
        cpu.label('word')
        cpu.push(cpu.lr)
        cpu.r6 = 0x04
        cpu.label('word_digit')
        cpu.r0 = cpu.r5
        cpu.r0 >>= 0x04
        cpu.call('digit')
        cpu.mem8[cpu.post(cpu.ea)] = cpu.r0
        cpu.r0 = cpu.r4
        cpu.r0 >>= 0x04
        cpu.r5 <<= 0x04
        cpu.r5 |= cpu.r0
        cpu.r4 <<= 0x04
        cpu.r6 += 0xFF
        if cpu.ne:
            cpu.branch('word_digit')
        cpu.pop(cpu.pc)
        cpu.label('digit')
        cpu.compare(cpu.r0, 0x0A)
        if cpu.lt:
            cpu.branch('decimal')
        cpu.r0 += 0x37
        cpu.ret()
        cpu.label('decimal')
        cpu.r0 += 0x30
        cpu.ret()
