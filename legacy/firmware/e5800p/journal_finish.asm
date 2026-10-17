; journal_finish
; Return nonoverlapping (physical S0 offset, machine-code bytes) spans.
; CPU 0x83F00, physical 0x03F00, 84 bytes
journal_check EQU 0x83B00
journal_crc EQU 0x83A00
journal_meta EQU 0x83D00

journal_finish:
PUSH LR
PUSH XR4
PUSH XR8
PUSH ER12
PUSH ER14
MOV ER12,ER0
MOV R0,#0x00
MOV R1,#0x60
CALL journal_check
MOV ER0,ER0
BNE bad
MOV R0,#0x00
MOV R1,#0x40
MOV R2,#0xF0
MOV R3,#0x1F
CALL journal_crc
CMP ER0,ER12
BNE bad
MOV ER2,ER12
MOV R0,#0xF0
MOV R1,#0x5F
CALL journal_meta
MOV ER0,ER0
BNE bad
MOV R0,#0x00
MOV R1,#0x40
CALL journal_check
MOV ER0,ER0
BNE bad
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
