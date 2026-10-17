; journal_crc
; Return nonoverlapping (physical S0 offset, machine-code bytes) spans.
; CPU 0x83A00, physical 0x03A00, 46 bytes

journal_crc:
MOV ER4,ER0
MOV ER6,ER2
MOV R8,#0xFF
MOV R9,#0xFF
byte:
L R0,0x08:[ER4]
XOR R9,R0
MOV R2,#0x08
bit:
MOV R0,R9
AND R0,#0x80
SLLC R9,#0x01
SLL R8,#0x01
CMP R0,#0x00
BEQ no_poly
XOR R8,#0x21
XOR R9,#0x10
no_poly:
ADD R2,#0xFF
BNE bit
ADD ER4,#0x01
ADD ER6,#0x7F
BNE byte
MOV ER0,ER8
RET
