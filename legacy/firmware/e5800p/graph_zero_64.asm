; graph_zero_64
; CPU 0x82400, physical 0x02400, 20 bytes

graph_zero_64:
MOV ER10,ER14
ADD ER10,#0x50
MOV R9,#0x08
MOV R0,#0x00
branch_0008:
ST R0,[ER10]
ADD ER10,#0x01
ADD R9,#0xFF
CMP R9,#0x00
BNE branch_0008
RET
