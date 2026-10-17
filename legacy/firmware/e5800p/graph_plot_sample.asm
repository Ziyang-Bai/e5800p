; graph_plot_sample
; CPU 0x82500, physical 0x02500, 62 bytes
graph_inter_sample_pole EQU 0x82480
graph_same_column_span EQU 0x825A0
graph_line EQU 0x81E80

graph_plot_sample:
PUSH LR
ST R0,-20[FP]
CMP R13,#0x00
BEQ branch_002e
CALL graph_inter_sample_pole
CMP R2,#0x00
BEQ branch_0016
MOV R13,#0x00
JMP branch_002e
branch_0016:
L R0,-27[FP]
ST R0,-18[FP]
MOV R0,#0x01
ST R0,-19[FP]
L R0,-26[FP]
L R1,-28[FP]
CMP R0,R1
BNE branch_0032
CALL graph_same_column_span
JMP branch_0032
branch_002e:
MOV R0,#0x00
ST R0,-19[FP]
branch_0032:
L R1,-20[FP]
L R0,-28[FP]
CALL graph_line
POP LR
RET
