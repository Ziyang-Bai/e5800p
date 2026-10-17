; graph_bcd_15_to_fixed_64
; CPU 0x82200, physical 0x02200, 216 bytes
graph_exponent EQU 0x81C00
graph_decimal_digit EQU 0x82300

graph_bcd_15_to_fixed_64:
PUSH LR
PUSH ER12
PUSH ER4
MOV ER10,ER14
ADD ER10,#0x50
MOV R9,#0x08
MOV R0,#0x00
branch_000e:
ST R0,[ER10]
ADD ER10,#0x01
ADD R9,#0xFF
CMP R9,#0x00
BNE branch_000e
ADD ER4,#0x09
MOV R2,#0x04
L R0,R2:[ER4]
ADD ER4,#0x77
MOV R7,R0
CMP R7,#0x00
BEQ branch_003a
CMP R7,#0x01
BEQ branch_003a
CMP R7,#0x05
BEQ branch_003a
CMP R7,#0x06
BEQ branch_003a
MOV R2,#0x00
JMP branch_00d0
branch_003a:
ADD ER4,#0x08
MOV R2,#0x04
L R0,R2:[ER4]
ADD ER4,#0x78
CALL graph_exponent
CMP R8,#0x10
BLTS branch_0050
CMP R0,#0x00
BLTS branch_00ce
branch_0050:
MOV R9,R8
SUB R9,R0
CMP R9,#0x10
BGES branch_00ce
MOV R12,#0x10
SUB R12,R9
CMP R9,#0x00
BNE branch_0062
MOV R12,#0x0F
branch_0062:
MOV R13,#0x00
MOV R2,#0x04
L R0,R2:[ER4]
AND R0,#0x0F
CALL graph_decimal_digit
ADD R12,#0xFF
CMP R12,#0x00
BEQ branch_00a0
branch_0076:
ADD ER4,#0x01
branch_0078:
MOV R2,#0x04
L R0,R2:[ER4]
CMP R13,#0x00
BNE branch_008a
SRL R0,#0x04
MOV R13,#0x01
JMP branch_008e
branch_008a:
AND R0,#0x0F
MOV R13,#0x00
branch_008e:
CALL graph_decimal_digit
ADD R12,#0xFF
CMP R12,#0x00
BEQ branch_00a0
CMP R13,#0x00
BEQ branch_0076
JMP branch_0078
branch_00a0:
CMP R9,#0x00
BNE branch_00aa
MOV R0,#0x00
CALL graph_decimal_digit
branch_00aa:
CMP R7,#0x05
BEQ branch_00b2
CMP R7,#0x06
BNE branch_00ce
branch_00b2:
MOV ER10,ER14
ADD ER10,#0x50
MOV R9,#0x08
MOV R6,#0x01
branch_00ba:
L R0,[ER10]
XOR R0,#0xFF
ADD R0,R6
MOV R6,#0x00
ADDC R6,#0x00
ST R0,[ER10]
ADD ER10,#0x01
ADD R9,#0xFF
CMP R9,#0x00
BNE branch_00ba
branch_00ce:
MOV R2,#0x01
branch_00d0:
POP ER4
POP ER12
POP LR
RET
