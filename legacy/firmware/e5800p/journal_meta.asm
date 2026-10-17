; journal_meta
; Return nonoverlapping (physical S0 offset, machine-code bytes) spans.
; CPU 0x83D00, physical 0x03D00, 72 bytes
journal_program_ram EQU 0x83CC0

journal_meta:
PUSH LR
PUSH ER12
PUSH ER6
MOV ER12,ER0
MOV ER0,ER2
XOR R0,#0xFF
XOR R1,#0xFF
PUSH ER0
PUSH ER2
MOV ER4,SP
MOV ER6,#0x04
MOV ER0,ER12
CALL journal_program_ram
ADD SP,#0x04
MOV ER0,ER0
BNE bad
MOV R0,#0x4A
MOV R1,#0xB6
PUSH ER0
MOV ER4,SP
MOV ER6,#0x02
MOV ER0,ER12
ADD ER0,#0x04
CALL journal_program_ram
ADD SP,#0x02
MOV ER0,ER0
BNE bad
MOV ER0,#0x00
BAL out
bad:
MOV R0,#0xFF
MOV R1,#0xFF
out:
POP ER6
POP ER12
POP PC
