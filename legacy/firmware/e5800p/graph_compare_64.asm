; graph_compare_64
; CPU 0x82120, physical 0x02120, 68 bytes

graph_compare_64:
MOV R3,#0x01
JMP branch_0008
MOV R3,#0x00
branch_0008:
PUSH ER6
PUSH ER10
ADD ER6,#0x07
ADD ER10,#0x07
MOV R9,#0x08
branch_0012:
L R0,[ER6]
L R1,[ER10]
CMP R3,#0x00
BEQ branch_0020
XOR R0,#0x80
XOR R1,#0x80
MOV R3,#0x00
branch_0020:
CMP R0,R1
BLT branch_0036
BGT branch_003c
ADD ER6,#0x7F
ADD ER10,#0x7F
ADD R9,#0xFF
CMP R9,#0x00
BNE branch_0012
MOV R0,#0x00
JMP branch_003e
branch_0036:
MOV R0,#0xFF
JMP branch_003e
branch_003c:
MOV R0,#0x01
branch_003e:
POP ER10
POP ER6
RET
