; logo
; Generate e5800p extensions from a matching original fx-5800P Flash image.
; CPU 0x81A86, physical 0x01A86, 86 bytes
rom_refresh EQU 0x043BE

logo:
PUSH LR
PUSH XR0
MOV ER2,SP
ADD ER2,#0x04
L ER0,[ER2]
CMP R0,#0xD6
CMPC R1,#0x59
BNE ordinary
ADD ER2,#0x02
L ER0,[ER2]
MOV ER0,ER0
BNE ordinary
POP XR0
CALL save
CALL 0x1:0x210A
PUSH XR4
MOV R2,#0x86
MOV R3,#0x1C
MOV R4,#0xE0
MOV R5,#0x80
MOV R6,#0x80
MOV R7,#0x01
copy:
L R0,0x08:[ER2]
ST R0,[ER4]
ADD ER2,#0x01
ADD ER4,#0x01
ADD ER6,#0x7F
BNE copy
POP XR4
CALL rom_refresh
POP LR
JMP 0x0:0x59F6
ordinary:
POP XR0
POP LR
save:
PUSH LR
PUSH ER8
JMP 0xC:0xFA6A
