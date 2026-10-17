; journal_recover
; Return nonoverlapping (physical S0 offset, machine-code bytes) spans.
; CPU 0x83800, physical 0x03800, 162 bytes
journal_check EQU 0x83B00
journal_erased EQU 0x83C00
journal_crc EQU 0x83A00
rom_flash_erase EQU 0x04EF4
journal_program EQU 0x83D80
journal_compare EQU 0x83A80
journal_meta EQU 0x83D00

journal_recover:
PUSH LR
PUSH XR4
PUSH XR8
PUSH ER12
PUSH ER14
MOV R0,#0x00
MOV R1,#0x40
CALL journal_check
MOV ER0,ER0
BEQ good
MOV R0,#0x00
MOV R1,#0x60
CALL journal_check
MOV ER0,ER0
BEQ restore
MOV R0,#0x00
MOV R1,#0x40
MOV R2,#0x00
MOV R3,#0x20
CALL journal_erased
MOV ER0,ER0
BEQ good
JMP bad
restore:
MOV R0,#0x00
MOV R1,#0x60
MOV R2,#0xF0
MOV R3,#0x1F
CALL journal_crc
MOV ER12,ER0
MOV R0,#0x01
CALL rom_flash_erase
MOV ER0,ER0
BNE bad
MOV R0,#0x00
MOV R1,#0x40
MOV R4,#0x00
MOV R5,#0x60
MOV R6,#0xF0
MOV R7,#0x1F
CALL journal_program
MOV ER0,ER0
BNE bad
MOV R0,#0x00
MOV R1,#0x40
MOV R2,#0x00
MOV R3,#0x60
MOV R4,#0xF0
MOV R5,#0x1F
CALL journal_compare
MOV ER0,ER0
BNE bad
MOV R0,#0xF0
MOV R1,#0x5F
MOV ER2,ER12
CALL journal_meta
MOV ER0,ER0
BNE bad
MOV R0,#0x00
MOV R1,#0x40
CALL journal_check
MOV ER0,ER0
BNE bad
good:
MOV ER0,#0x00
BAL out
bad:
MOV R0,#0xFF
MOV R1,#0xFF
out:
POP ER14
POP ER12
POP XR8
POP XR4
POP PC
