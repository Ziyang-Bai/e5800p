; journal_program
; Return nonoverlapping (physical S0 offset, machine-code bytes) spans.
; CPU 0x83D80, physical 0x03D80, 100 bytes
journal_program_ram EQU 0x83CC0

journal_program:
PUSH LR
PUSH XR4
PUSH XR8
PUSH ER12
PUSH ER14
ADD SP,#0xF0
MOV ER8,ER0
MOV ER10,ER4
MOV ER12,ER6
MOV ER14,SP
chunk:
MOV ER12,ER12
BEQ done
MOV ER0,ER12
MOV ER2,#0x10
CMP ER0,ER2
BLT short
MOV ER6,#0x10
BAL copy
short:
MOV ER6,ER12
copy:
MOV ER0,ER14
MOV R3,R6
copy_byte:
L R2,0x08:[ER10]
ST R2,[ER0]
ADD ER10,#0x01
ADD ER0,#0x01
ADD R3,#0xFF
BNE copy_byte
MOV ER0,ER8
MOV ER4,ER14
PUSH ER6
CALL journal_program_ram
POP ER6
MOV ER0,ER0
BNE bad
ADD ER8,ER6
SUB R12,R6
SUBC R13,R7
BAL chunk
done:
MOV ER0,#0x00
BAL out
bad:
MOV R0,#0xFF
MOV R1,#0xFF
out:
ADD SP,#0x10
POP ER14
POP ER12
POP XR8
POP XR4
POP PC
