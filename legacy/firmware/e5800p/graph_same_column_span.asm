; graph_same_column_span
; CPU 0x825A0, physical 0x025A0, 38 bytes

graph_same_column_span:
PUSH LR
L R6,-28[FP]
L R7,-27[FP]
L R9,-20[FP]
branch_0008:
CMP R7,R9
BEQ branch_0022
BLTS branch_0014
ADD R7,#0xFF
JMP branch_0016
branch_0014:
ADD R7,#0x01
branch_0016:
MOV R0,R6
MOV R1,R7
CALL 0x0:0x431C
JMP branch_0008
branch_0022:
POP LR
RET
