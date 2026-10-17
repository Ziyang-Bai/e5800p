; graph_exponent
; CPU 0x81C00, physical 0x01C00, 30 bytes

graph_exponent:
MOV R3,R0
SRL R0,#0x04
MOV R1,#0x00
MOV R2,#0x0A
MUL ER0,R2
AND R3,#0x0F
ADD R0,R3
CMP R7,#0x00
BEQ branch_0016
CMP R7,#0x05
BNE branch_001c
branch_0016:
CMP R0,#0x00
BEQ branch_001c
ADD R0,#0x9C
branch_001c:
RET
