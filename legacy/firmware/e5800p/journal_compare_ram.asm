; journal_compare_ram
; Return nonoverlapping (physical S0 offset, machine-code bytes) spans.
; CPU 0x83C40, physical 0x03C40, 38 bytes

journal_compare_ram:
MOV ER6,ER0
MOV ER8,ER2
MOV ER10,ER4
loop:
MOV ER10,ER10
BEQ equal
L R0,0x08:[ER6]
L R1,[ER8]
CMP R0,R1
BNE different
ADD ER6,#0x01
ADD ER8,#0x01
ADD ER10,#0x7F
BAL loop
equal:
MOV ER0,#0x00
RET
different:
MOV R0,#0xFF
MOV R1,#0xFF
RET
