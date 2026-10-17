; goto
; Emit the ASM address prompt and hexadecimal key translation.
; CPU 0x825C6, physical 0x025C6, 1508 bytes
scanner_address EQU 0x80800
ui_text_address EQU 0x81E06
rom_draw_text EQU 0x041DA
rom_refresh EQU 0x043BE

goto:
JMP address
branch_0004:
JMP hex_key
JMP memory
hex_key:
PUSH LR
PUSH XR4
CALL scanner_address
CMP R0,#0xFA
BGE key_F
CMP R0,#0x02
CMPC R1,#0x7D
BEQ key_F
CMP R0,#0x49
CMPC R1,#0x75
BEQ key_F
CMP R1,#0x00
BEQ key_ascii
MOV ER0,#0x00
JMP key_F
key_ascii:
CMP R0,#0x53
BNE key_A
MOV R0,#0x41
JMP key_F
key_A:
CMP R0,#0x54
BNE key_B
MOV R0,#0x42
JMP key_F
key_B:
CMP R0,#0x55
BNE key_C
MOV R0,#0x43
JMP key_F
key_C:
CMP R0,#0x4E
BNE key_D
MOV R0,#0x44
JMP key_F
key_D:
CMP R0,#0x4F
BNE key_E
MOV R0,#0x45
JMP key_F
key_E:
CMP R0,#0x50
BNE key_F
MOV R0,#0x46
JMP key_F
key_F:
key_done:
POP XR4
POP PC
address:
PUSH LR
PUSH XR4
PUSH QR8
PUSH ER12
PUSH ER14
ADD SP,#0xE0
MOV ER14,SP
MOV ER8,ER0
MOV R12,R2
MOV R13,#0x00
L R0,0x80A0
MOV ER2,ER14
ADD ER2,#0x1C
ST R0,[ER2]
L R0,0x80A2
ADD ER2,#0x01
ST R0,[ER2]
MOV R0,#0x07
ST R0,0x80A0
MOV R0,#0x01
ST R0,0x80A2
MOV R6,#0x00
MOV R7,#0x00
draw:
CALL 0x0:0x409A
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0xC5
MOV R3,#0xD1
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x01
CALL rom_draw_text
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0xD2
MOV R3,#0xD1
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
ADD ER2,#0x02
MOV R0,R9
CALL hexbyte
MOV R0,R8
CALL hexbyte
MOV R0,#0x00
ST R0,[ER2]
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x09
CALL rom_draw_text
CMP R7,#0x00
BEQ hint
CMP R7,#0x01
BNE odd_hint
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0xD5
MOV R3,#0xD1
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x11
CALL rom_draw_text
JMP footer
odd_hint:
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0xE0
MOV R3,#0xD1
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x11
CALL rom_draw_text
JMP footer
hint:
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0xED
MOV R3,#0xD1
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x11
CALL rom_draw_text
footer:
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0xFA
MOV R3,#0xD1
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x19
CALL rom_draw_text
CALL rom_refresh
input:
CALL branch_0004
CMP R0,#0xFA
BNE skip_26
JMP cancel
skip_26:
CMP R0,#0xFB
BNE skip_28
JMP accept
skip_28:
CMP R0,#0xFC
BNE skip_30
JMP backspace
skip_30:
CMP R0,#0x30
BGE skip_32
JMP input
skip_32:
CMP R0,#0x3A
BGE letter
ADD R0,#0xD0
JMP digit
letter:
CMP R0,#0x41
BGE skip_36
JMP input
skip_36:
CMP R0,#0x47
BLT skip_38
JMP input
skip_38:
ADD R0,#0xC9
digit:
CMP R6,#0x04
BLT digit_count
MOV R6,#0x00
digit_count:
CMP R6,#0x00
BNE append
MOV ER8,#0x00
append:
MOV R3,R8
SRL R3,#0x04
SLL R8,#0x04
SLL R9,#0x04
OR R9,R3
OR R8,R0
ADD R6,#0x01
MOV R7,#0x00
JMP draw
backspace:
CMP R6,#0x00
BNE skip_43
JMP input
skip_43:
MOV R3,R9
SLL R3,#0x04
SRL R8,#0x04
SRL R9,#0x04
OR R8,R3
ADD R6,#0xFF
MOV R7,#0x00
JMP draw
accept:
CMP R6,#0x00
BEQ skip_47
CMP R6,#0x04
BEQ skip_47
JMP draw
skip_47:
check_range:
MOV ER0,ER8
MOV R2,#0x00
MOV R3,#0x40
CMP ER0,ER2
BGE skip_49
JMP range_error
skip_49:
MOV R2,#0xF0
MOV R3,#0x5F
CMP ER0,ER2
BLT skip_51
JMP range_error
skip_51:
CMP R12,#0x00
BEQ skip_54
MOV R0,R8
AND R0,#0x01
BEQ skip_54
JMP odd_error
skip_54:
accepted:
MOV R4,#0x01
JMP finish
range_error:
MOV R7,#0x01
JMP draw
odd_error:
MOV R7,#0x02
JMP draw
cancel:
MOV R4,#0x00
finish:
MOV ER2,ER14
ADD ER2,#0x1D
L R0,[ER2]
ST R0,0x80A2
MOV ER2,ER14
ADD ER2,#0x1C
L R0,[ER2]
ST R0,0x80A0
MOV ER0,ER8
MOV R2,R4
ADD SP,#0x20
POP ER14
POP ER12
POP QR8
POP XR4
POP PC
memory:
PUSH LR
PUSH XR4
PUSH QR8
PUSH ER12
PUSH ER14
ADD SP,#0xD0
MOV ER14,SP
MOV ER8,ER0
MOV R13,R2
L R0,0x80A0
MOV ER2,ER14
ADD ER2,#0x1C
ST R0,[ER2]
L R0,0x80A2
ADD ER2,#0x01
ST R0,[ER2]
MOV R0,#0x08
ST R0,0x80A0
MOV R0,#0x01
ST R0,0x80A2
memory_menu:
CALL 0x0:0x409A
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0x0B
MOV R3,#0xD2
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x01
CALL rom_draw_text
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0x13
MOV R3,#0xD2
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x09
CALL rom_draw_text
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0x1A
MOV R3,#0xD2
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x11
CALL rom_draw_text
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0x20
MOV R3,#0xD2
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x19
CALL rom_draw_text
CALL rom_refresh
memory_menu_key:
CALL branch_0004
CMP R0,#0xFA
BNE skip_59
JMP memory_cancel
skip_59:
CMP R0,#0x31
BNE skip_61
JMP memory_flash
skip_61:
CMP R0,#0x32
BNE skip_63
JMP memory_sram
skip_63:
CMP R0,#0x33
BNE skip_65
JMP memory_ram
skip_65:
JMP memory_menu_key
memory_flash:
MOV R12,#0x00
MOV R10,#0x05
CMP R13,#0x08
BGE memory_ready
MOV R13,#0x08
MOV R8,#0x00
MOV R9,#0x40
JMP memory_ready
memory_sram:
MOV R12,#0x01
MOV R10,#0x04
CMP R13,#0x04
BEQ memory_ready
MOV R13,#0x04
MOV ER8,#0x00
JMP memory_ready
memory_ram:
MOV R12,#0x02
MOV R10,#0x04
CMP R13,#0x00
BEQ memory_ready
MOV R13,#0x00
MOV R8,#0x00
MOV R9,#0x80
memory_ready:
MOV R6,#0x00
MOV R7,#0x00
memory_draw:
CALL 0x0:0x409A
CMP R12,#0x00
BNE memory_title_sram
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0x2A
MOV R3,#0xD2
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x01
CALL rom_draw_text
JMP memory_address
memory_title_sram:
CMP R12,#0x01
BNE memory_title_ram
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0x35
MOV R3,#0xD2
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x01
CALL rom_draw_text
JMP memory_address
memory_title_ram:
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0x3F
MOV R3,#0xD2
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x01
CALL rom_draw_text
memory_address:
MOV ER2,ER14
MOV R0,R13
CALL nibble
ST R0,[ER2]
ADD ER2,#0x01
MOV R0,#0x3A
ST R0,[ER2]
ADD ER2,#0x01
MOV R0,R9
CALL hexbyte
MOV R0,R8
CALL hexbyte
MOV R0,#0x00
ST R0,[ER2]
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x09
CALL rom_draw_text
CMP R7,#0x00
BEQ memory_range
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0x48
MOV R3,#0xD2
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x11
CALL rom_draw_text
JMP memory_footer
memory_range:
CMP R12,#0x00
BNE memory_range_sram
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0x56
MOV R3,#0xD2
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x11
CALL rom_draw_text
JMP memory_footer
memory_range_sram:
CMP R12,#0x01
BNE memory_range_ram
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0x65
MOV R3,#0xD2
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x11
CALL rom_draw_text
JMP memory_footer
memory_range_ram:
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0x70
MOV R3,#0xD2
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x11
CALL rom_draw_text
memory_footer:
MOV ER2,ER14
PUSH ER6
MOV ER0,ER2
MOV R2,#0xFA
MOV R3,#0xD1
MOV ER6,#0x1A
CALL ui_text_address
POP ER6
MOV ER2,ER14
MOV R0,#0x00
MOV R1,#0x19
CALL rom_draw_text
CALL rom_refresh
memory_input:
CALL branch_0004
CMP R0,#0xFA
BNE skip_86
JMP memory_cancel
skip_86:
CMP R0,#0xFB
BNE skip_88
JMP memory_accept
skip_88:
CMP R0,#0xFC
BNE skip_90
JMP memory_backspace
skip_90:
CMP R0,#0x30
BGE skip_92
JMP memory_input
skip_92:
CMP R0,#0x3A
BGE memory_letter
ADD R0,#0xD0
JMP memory_digit
memory_letter:
CMP R0,#0x41
BGE skip_96
JMP memory_input
skip_96:
CMP R0,#0x47
BLT skip_98
JMP memory_input
skip_98:
ADD R0,#0xC9
memory_digit:
CMP R6,R10
BLT memory_digit_count
MOV R6,#0x00
memory_digit_count:
CMP R6,#0x00
BNE memory_append
MOV ER8,#0x00
CMP R12,#0x00
BNE memory_append
MOV R13,#0x00
memory_append:
CMP R12,#0x00
BNE memory_append_word
MOV R3,R9
SRL R3,#0x04
SLL R13,#0x04
OR R13,R3
memory_append_word:
MOV R3,R8
SRL R3,#0x04
SLL R8,#0x04
SLL R9,#0x04
OR R9,R3
OR R8,R0
ADD R6,#0x01
MOV R7,#0x00
JMP memory_draw
memory_backspace:
CMP R6,#0x00
BNE skip_105
JMP memory_input
skip_105:
MOV R3,R9
SLL R3,#0x04
SRL R8,#0x04
SRL R9,#0x04
OR R8,R3
CMP R12,#0x00
BNE memory_backspace_done
MOV R3,R13
SLL R3,#0x04
OR R9,R3
SRL R13,#0x04
memory_backspace_done:
ADD R6,#0xFF
MOV R7,#0x00
JMP memory_draw
memory_accept:
CMP R6,#0x00
BEQ skip_110
CMP R6,R10
BEQ skip_110
JMP memory_draw
skip_110:
memory_check:
CMP R12,#0x00
BNE memory_check_sram
CMP R13,#0x08
BGE skip_113
JMP memory_error
skip_113:
CMP R13,#0x10
BLT skip_115
JMP memory_error
skip_115:
JMP skip_124
memory_check_sram:
MOV ER0,ER8
CMP R12,#0x01
BNE memory_check_ram
MOV R2,#0x00
MOV R3,#0x80
CMP ER0,ER2
BLT skip_119
JMP memory_error
skip_119:
JMP skip_124
memory_check_ram:
MOV R2,#0x00
MOV R3,#0x80
CMP ER0,ER2
BGE skip_122
JMP memory_error
skip_122:
MOV R2,#0x00
MOV R3,#0x8E
CMP ER0,ER2
BLT skip_124
JMP memory_error
skip_124:
memory_accepted:
MOV R4,#0x01
JMP memory_finish
memory_error:
MOV R7,#0x01
JMP memory_draw
memory_cancel:
MOV R4,#0x00
memory_finish:
MOV ER2,ER14
ADD ER2,#0x1D
L R0,[ER2]
ST R0,0x80A2
MOV ER2,ER14
ADD ER2,#0x1C
L R0,[ER2]
ST R0,0x80A0
MOV ER0,ER8
MOV R2,R13
MOV R3,R4
ADD SP,#0x30
POP ER14
POP ER12
POP QR8
POP XR4
POP PC
hexbyte:
PUSH LR
MOV R5,R0
SRL R0,#0x04
CALL nibble
ST R0,[ER2]
ADD ER2,#0x01
MOV R0,R5
AND R0,#0x0F
CALL nibble
ST R0,[ER2]
ADD ER2,#0x01
POP PC
nibble:
CMP R0,#0x0A
BLT number
ADD R0,#0x37
RET
number:
ADD R0,#0x30
RET
