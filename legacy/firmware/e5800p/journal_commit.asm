; journal_commit
; Return nonoverlapping (physical S0 offset, machine-code bytes) spans.
; CPU 0x83000, physical 0x03000, 296 bytes
journal_backup EQU 0x83E00
journal_program EQU 0x83D80
journal_program_ram EQU 0x83CC0
journal_compare EQU 0x83A80
journal_compare_ram EQU 0x83C40
journal_crc EQU 0x83A00
journal_finish EQU 0x83F00

journal_commit:
PUSH LR
PUSH XR4
PUSH XR8
PUSH ER12
PUSH ER14
MOV ER14,ER0
MOV ER12,ER2
AND R0,#0x1F
BNE fail_near
CMP R1,#0x40
BLT fail_near
CMP R1,#0x5F
BLT page_ok
BNE fail_near
MOV R0,R14
CMP R0,#0xF0
BLT page_ok
fail_near:
JMP fail
page_ok:
CALL journal_backup
MOV ER0,ER0
BEQ backup_ready
JMP fail
backup_ready:
MOV ER6,ER14
ADD R7,#0xC0
MOV R4,#0x00
MOV R5,#0x60
MOV R0,#0x00
MOV R1,#0x40
CALL journal_program
MOV ER0,ER0
BEQ prefix_written
JMP fail
prefix_written:
MOV ER0,ER14
MOV ER4,ER12
MOV ER6,#0x20
MOV R2,#0xE0
MOV R3,#0x5F
CMP ER0,ER2
BNE full_page
MOV ER6,#0x10
full_page:
CALL journal_program_ram
MOV ER0,ER0
BEQ page_written
JMP fail
page_written:
MOV ER4,ER14
MOV R2,#0xE0
MOV R3,#0x5F
CMP ER4,ER2
BNE full_suffix
ADD ER4,#0x10
MOV R6,#0xF0
MOV R7,#0x5F
SUB R6,R14
SUBC R7,R15
ADD ER6,#0x70
MOV ER0,ER14
ADD ER0,#0x10
BAL write_suffix
full_suffix:
ADD ER4,#0x20
MOV R6,#0xF0
MOV R7,#0x5F
SUB R6,R14
SUBC R7,R15
ADD ER6,#0x60
MOV ER0,ER14
ADD ER0,#0x20
write_suffix:
ADD R5,#0x20
CALL journal_program
MOV ER0,ER0
BEQ suffix_written
JMP fail
suffix_written:
MOV R0,#0x00
MOV R1,#0x40
MOV R2,#0x00
MOV R3,#0x60
MOV ER4,ER14
ADD R5,#0xC0
CALL journal_compare
MOV ER0,ER0
BEQ prefix_compared
JMP fail
prefix_compared:
MOV ER0,ER14
MOV ER2,ER12
MOV ER4,#0x20
MOV R6,#0xE0
MOV R7,#0x5F
CMP ER0,ER6
BNE full_compare
MOV ER4,#0x10
full_compare:
CALL journal_compare_ram
MOV ER0,ER0
BEQ page_compared
JMP fail
page_compared:
MOV ER0,ER14
MOV R2,#0xE0
MOV R3,#0x5F
CMP ER0,ER2
BNE full_compare_suffix
ADD ER0,#0x10
BAL compare_suffix
full_compare_suffix:
ADD ER0,#0x20
compare_suffix:
MOV ER2,ER0
ADD R3,#0x20
MOV R4,#0xF0
MOV R5,#0x5F
SUB R4,R0
SUBC R5,R1
CALL journal_compare
MOV ER0,ER0
BEQ suffix_compared
JMP fail
suffix_compared:
MOV R0,#0x00
MOV R1,#0x40
MOV R2,#0xF0
MOV R3,#0x1F
CALL journal_crc
CALL journal_finish
MOV ER0,ER0
BEQ s1_checked
JMP fail
s1_checked:
MOV ER0,#0x00
JMP done
fail:
MOV R0,#0xFF
MOV R1,#0xFF
done:
POP ER14
POP ER12
POP XR8
POP XR4
POP PC
