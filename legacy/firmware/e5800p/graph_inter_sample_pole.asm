; graph_inter_sample_pole
; CPU 0x82480, physical 0x02480, 102 bytes
graph_y_pixel_64 EQU 0x82380

graph_inter_sample_pole:
PUSH LR
PUSH ER4
PUSH ER12
MOV R2,#0x00
CMP R13,#0x00
BEQ branch_005e
L R0,-19[FP]
CMP R0,#0x00
BEQ branch_005e
CMP R12,#0x01
BEQ branch_005e
L R0,-27[FP]
CMP R0,#0x1C
BLTS branch_002e
L R1,-20[FP]
CMP R1,#0x03
BGTS branch_005e
L R1,-18[FP]
CMP R1,R0
BGES branch_005e
MOV R13,#0x01
JMP branch_0040
branch_002e:
CMP R0,#0x03
BGTS branch_005e
L R1,-20[FP]
CMP R1,#0x1C
BLTS branch_005e
L R1,-18[FP]
CMP R1,R0
BLES branch_005e
MOV R13,#0x02
branch_0040:
ADD ER4,#0x14
CALL graph_y_pixel_64
CMP R2,#0x00
BEQ branch_005e
L R1,-20[FP]
CMP R13,#0x01
BEQ branch_0058
CMP R0,R1
BGES branch_005e
JMP branch_005c
branch_0058:
CMP R0,R1
BLES branch_005e
branch_005c:
MOV R2,#0x01
branch_005e:
POP ER12
POP ER4
POP LR
RET
