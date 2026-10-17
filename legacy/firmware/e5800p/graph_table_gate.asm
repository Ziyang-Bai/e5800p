; graph_table_gate
; CPU 0x81100, physical 0x01100, 60 bytes
graph EQU 0x81800

graph_table_gate:
PUSH LR
PUSH XR0
PUSH ER14
MOV ER14,SP
L ER0,6[FP]
CMP R0,#0xA4
CMPC R1,#0x7E
BEQ branch_0016
CMP R0,#0xD2
CMPC R1,#0x7E
BNE branch_002c
branch_0016:
L R0,0x8091
CMP R0,#0x85
BNE branch_002c
POP ER14
CALL graph
CMP R0,#0x01
BEQ branch_0038
JMP branch_002e
branch_002c:
POP ER14
branch_002e:
POP XR0
PUSH ER14
MOV ER14,SP
JMP 0xE:0x369A
branch_0038:
POP XR0
POP PC
