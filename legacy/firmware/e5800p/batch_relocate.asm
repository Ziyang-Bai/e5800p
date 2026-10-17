; batch_relocate
; Journaled S1 replacement and branch relocation, with bounded shared decoding.
; CPU 0x81EE0, physical 0x01EE0, 324 bytes

batch_relocate:
relocate:
MOV R6,#0x00
MOV R0,R5
CMP R0,#0xC0
BGE skip_69
JMP relocate_ok
skip_69:
CMP R0,#0xCF
BGE skip_70
JMP relative_target
skip_70:
CMP R0,#0xF8
BEQ skip_71
JMP relocate_ok
skip_71:
MOV R0,R4
AND R0,#0x0F
CMP R0,#0x02
BLT skip_72
JMP relocate_ok
skip_72:
MOV R6,#0x02
MOV ER2,ER14
ADD ER2,#0x1E
L R7,[ER2]
MOV ER2,ER8
CMP R7,#0x00
BEQ skip_73
JMP far_source
skip_73:
ADD R3,#0xE0
far_source:
ADD ER2,#0x02
L R4,0x08:[ER2]
ADD ER2,#0x01
L R5,0x08:[ER2]
ADD R5,#0x20
MOV R0,R4
AND R0,#0x01
BEQ skip_74
JMP relocate_bad
skip_74:
JMP target_check
relative_target:
MOV R6,#0x01
MOV R0,R4
MOV R5,#0x00
AND R0,#0x80
BNE skip_75
JMP relative_sign
skip_75:
MOV R5,#0xFF
relative_sign:
ADD ER4,ER4
MOV ER0,ER8
ADD ER0,#0x02
ADD ER4,ER0
target_check:
MOV ER0,ER4
MOV R2,#0x00
MOV R3,#0x60
CMP ER0,ER2
BGE skip_76
JMP skip_82
skip_76:
MOV R2,#0xF0
MOV R3,#0x7F
CMP ER0,ER2
BLT skip_77
JMP skip_82
skip_77:
MOV ER0,ER12
CMP ER4,ER0
BGE skip_78
JMP skip_82
skip_78:
BNE skip_79
JMP skip_82
skip_79:
MOV ER2,ER14
ADD ER2,#0x16
L R2,[ER2]
MOV R3,#0x00
ADD ER0,ER2
CMP ER4,ER0
BGE skip_80
JMP relocate_bad
skip_80:
MOV ER2,ER14
ADD ER2,#0x18
L R2,[ER2]
MOV R3,#0x00
MOV R0,R2
AND R0,#0x80
BNE skip_81
JMP target_delta
skip_81:
MOV R3,#0xFF
target_delta:
ADD ER4,ER2
MOV ER0,ER4
MOV R2,#0xF0
MOV R3,#0x7F
CMP ER0,ER2
BLT skip_82
JMP relocate_bad
skip_82:
target_ready:
CMP R6,#0x02
BEQ skip_83
JMP relative_finish
skip_83:
ADD R5,#0xE0
JMP relocate_ok
relative_finish:
MOV ER0,ER12
MOV ER2,ER14
ADD ER2,#0x16
L R2,[ER2]
MOV R3,#0x00
ADD ER0,ER2
CMP ER8,ER0
BGE skip_84
JMP source_ready_rel
skip_84:
MOV ER2,ER14
ADD ER2,#0x18
L R2,[ER2]
MOV R3,#0x00
MOV R0,R2
AND R0,#0x80
BNE skip_85
JMP source_delta
skip_85:
MOV R3,#0xFF
source_delta:
MOV ER0,ER8
ADD ER0,ER2
JMP source_done_rel
source_ready_rel:
MOV ER0,ER8
source_done_rel:
ADD ER0,#0x02
SUB R4,R0
SUBC R5,R1
MOV R0,R4
AND R0,#0x01
BEQ skip_86
JMP relocate_bad
skip_86:
CMP R5,#0x00
BNE skip_87
JMP relative_low
skip_87:
CMP R5,#0xFF
BEQ skip_88
JMP relocate_bad
skip_88:
SRL R4,#0x01
OR R4,#0x80
JMP relocate_ok
relative_low:
SRL R4,#0x01
relocate_ok:
MOV ER0,#0x00
RET
relocate_bad:
MOV R0,#0xFF
MOV R1,#0xFF
RET
