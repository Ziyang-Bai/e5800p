; graph_valid_exponent
; CPU 0x81C40, physical 0x01C40, 70 bytes
graph_exponent EQU 0x81C00

graph_valid_exponent:
PUSH LR
ADD ER4,#0x09
MOV R2,#0x04
L R0,R2:[ER4]
ADD ER4,#0x77
MOV R7,R0
CMP R0,#0x00
BEQ branch_0022
CMP R0,#0x01
BEQ branch_0022
CMP R0,#0x05
BEQ branch_0022
CMP R0,#0x06
BEQ branch_0022
JMP branch_0042
branch_0022:
MOV R2,#0x04
L R0,R2:[ER4]
AND R0,#0x0F
CMP R0,#0x00
BEQ branch_0042
ADD ER4,#0x08
MOV R2,#0x04
L R0,R2:[ER4]
ADD ER4,#0x78
CALL graph_exponent
MOV R2,#0x01
JMP branch_0044
branch_0042:
MOV R2,#0x00
branch_0044:
POP PC
