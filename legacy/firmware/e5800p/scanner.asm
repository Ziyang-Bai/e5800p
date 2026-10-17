; scanner
; Return ER0=event; R0=FA..FF for cancel/EXE/left/right/down/up.
; CPU 0x80800, physical 0x00800, 76 bytes
rom_read_key EQU 0x1234E
rom_normalize_key EQU 0x1249C

scanner:
PUSH LR
ADD SP,#0xFE
MOV ER0,SP
CALL rom_read_key
MOV ER0,SP
CALL rom_normalize_key
MOV ER0,SP
L ER0,[ER0]
CMP R1,#0x75
BNE next_66
CMP R0,#0x32
BNE next_50
MOV R0,#0xFA
BAL next_66
next_50:
CMP R0,#0x34
BNE next_52
MOV R0,#0xFB
BAL next_66
next_52:
CMP R0,#0x44
BNE next_68
MOV R0,#0xFC
BAL next_66
next_68:
CMP R0,#0x45
BNE next_69
MOV R0,#0xFD
BAL next_66
next_69:
CMP R0,#0x47
BNE next_71
MOV R0,#0xFE
BAL next_66
next_71:
CMP R0,#0x42
BNE next_66
MOV R0,#0xFF
BAL next_66
next_66:
done:
ADD SP,#0x02
POP PC
