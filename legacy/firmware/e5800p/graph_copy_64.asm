; graph_copy_64
; CPU 0x82100, physical 0x02100, 18 bytes

graph_copy_64:
MOV R9,#0x08
branch_0002:
L R0,[ER6]
ST R0,[ER10]
ADD ER6,#0x01
ADD ER10,#0x01
ADD R9,#0xFF
CMP R9,#0x00
BNE branch_0002
RET
