; journal_erased
; Return nonoverlapping (physical S0 offset, machine-code bytes) spans.
; CPU 0x83C00, physical 0x03C00, 28 bytes

journal_erased:
MOV ER4,ER0
MOV ER6,ER2
loop:
L R0,0x08:[ER4]
CMP R0,#0xFF
BNE bad
ADD ER4,#0x01
ADD ER6,#0x7F
BNE loop
MOV ER0,#0x00
RET
bad:
MOV R0,#0xFF
MOV R1,#0xFF
RET
