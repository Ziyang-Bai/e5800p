; batch_emit
; Journaled S1 replacement and branch relocation, with bounded shared decoding.
; CPU 0x81AE0, physical 0x01AE0, 138 bytes
journal_crc_update EQU 0x83F80
journal_program_ram EQU 0x83CC0

batch_emit:
emit:
PUSH LR
PUSH XR4
MOV R5,R0
MOV R0,#0xF0
MOV R1,#0x5F
CMP ER10,ER0
BLT skip_63
JMP emit_bad
skip_63:
MOV ER2,ER14
MOV R0,R10
AND R0,#0x0F
MOV R1,#0x00
ADD ER2,ER0
ST R5,[ER2]
MOV ER2,ER14
ADD ER2,#0x10
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x11
L R1,[ER2]
MOV R2,R5
CALL journal_crc_update
MOV ER2,ER14
ADD ER2,#0x10
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x11
ST R1,[ER2]
ADD ER10,#0x01
MOV R0,R10
AND R0,#0x0F
CMP R0,#0x00
BEQ skip_64
JMP emit_good
skip_64:
MOV ER0,ER10
ADD ER0,#0x70
MOV ER4,ER14
MOV ER6,#0x10
CALL journal_program_ram
CMP R0,#0x00
BEQ skip_65
JMP emit_bad
skip_65:
MOV ER4,ER14
MOV ER6,ER10
ADD ER6,#0x70
MOV R3,#0x10
verify:
L R0,0x08:[ER6]
L R1,[ER4]
CMP R0,R1
BEQ skip_66
JMP emit_bad
skip_66:
ADD ER4,#0x01
ADD ER6,#0x01
ADD R3,#0xFF
BNE verify
emit_good:
MOV ER0,#0x00
JMP emit_exit
emit_bad:
MOV R0,#0xFF
MOV R1,#0xFF
emit_exit:
POP XR4
POP PC
