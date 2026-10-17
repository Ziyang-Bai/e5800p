; journal_crc_update
; Return nonoverlapping (physical S0 offset, machine-code bytes) spans.
; CPU 0x83F80, physical 0x03F80, 26 bytes

journal_crc_update:
XOR R1,R2
MOV R3,#0x08
bit:
MOV R2,R1
AND R2,#0x80
SLLC R1,#0x01
SLL R0,#0x01
CMP R2,#0x00
BEQ next
XOR R0,#0x21
XOR R1,#0x10
next:
ADD R3,#0xFF
BNE bit
RET
