; graph_zero_axis_pixel
; CPU 0x82420, physical 0x02420, 12 bytes
graph_zero_64 EQU 0x82400

graph_zero_axis_pixel:
PUSH LR
PUSH ER12
CALL graph_zero_64
JMP 0x8:0x238C
