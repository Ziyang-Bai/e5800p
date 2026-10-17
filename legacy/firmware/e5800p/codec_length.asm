; codec_length
; Return independent encoder and length/prefix/SUB clusters.
; CPU 0x80440, physical 0x00440, 588 bytes

codec_length:
JMP s1_length
JMP source_length
s1_length:
PUSH LR
PUSH ER2
PUSH XR4
MOV ER0,ER2
AND R0,#0x01
BEQ skip_1
JMP s1_bad
skip_1:
MOV ER0,ER2
MOV R4,#0x00
MOV R5,#0x40
CMP ER0,ER4
BGE skip_2
JMP s1_bad
skip_2:
MOV R4,#0xF0
MOV R5,#0x5F
MOV R2,#0x08
CALL source_length
JMP s1_exit
s1_bad:
MOV R0,#0xFF
MOV R1,#0xFF
s1_exit:
POP XR4
POP ER2
POP PC
source_length:
PUSH LR
PUSH XR4
PUSH QR8
MOV ER8,ER0
MOV ER10,ER4
MOV R12,R2
MOV R13,#0x00
MOV R14,#0x00
MOV R7,#0x02
CALL fits
CMP R0,#0x00
BEQ skip_3
JMP source_bad
skip_3:
MOV R6,#0x00
CALL read
MOV R4,R0
MOV R6,#0x01
CALL read
MOV R5,R0
CMP R5,#0xE3
BNE skip_4
JMP prefixed
skip_4:
CMP R5,#0xFE
BNE skip_5
CMP R4,#0x9F
BNE skip_5
JMP prefixed
skip_5:
prefix_register:
CMP R5,#0x90
BNE skip_6
MOV R0,R4
AND R0,#0x0F
CMP R0,#0x0F
BNE skip_6
JMP prefixed
skip_6:
unprefixed:
CALL word_length
CMP R4,#0x4E
BEQ skip_7
JMP source_span
skip_7:
MOV R0,R5
AND R0,#0xFE
CMP R0,#0xF0
BEQ skip_8
JMP source_span
skip_8:
MOV R7,#0x08
CALL fits
CMP R0,#0x00
BEQ skip_9
JMP source_two
skip_9:
MOV R15,R5
AND R15,#0x01
MOV R6,#0x03
CALL read
CMP R0,R15
BEQ skip_10
JMP source_two
skip_10:
MOV R6,#0x04
CALL read
MOV R6,R15
SLL R6,#0x04
OR R6,#0x08
CMP R0,R6
BEQ skip_11
JMP source_two
skip_11:
MOV R6,#0x05
CALL read
MOV R6,R0
AND R6,#0xF0
CMP R6,#0x80
BEQ skip_12
JMP source_two
skip_12:
AND R0,#0x0F
CMP R0,#0x00
BEQ macro_r0
CMP R15,#0x00
BEQ skip_13
JMP source_two
skip_13:
JMP skip_14
macro_r0:
CMP R15,#0x01
BEQ skip_14
JMP source_two
skip_14:
macro_pop:
MOV R6,#0x06
CALL read
CMP R0,#0x0E
BEQ skip_15
JMP source_two
skip_15:
MOV R6,#0x07
CALL read
OR R15,#0xF0
CMP R0,R15
BEQ skip_16
JMP source_two
skip_16:
MOV R14,#0x01
MOV R7,#0x08
JMP source_span
source_two:
MOV R7,#0x02
JMP source_span
prefixed:
MOV R7,#0x04
CALL fits
CMP R0,#0x00
BEQ skip_17
JMP source_bad
skip_17:
MOV R6,#0x02
CALL read
MOV R4,R0
MOV R6,#0x03
CALL read
MOV R5,R0
MOV R0,R5
AND R0,#0xF0
CMP R0,#0x90
BEQ prefix_memory
CMP R0,#0xA0
BEQ skip_18
JMP source_bad
skip_18:
MOV R0,R4
AND R0,#0x0E
CMP R0,#0x08
BEQ skip_19
JMP source_bad
skip_19:
JMP skip_21
prefix_memory:
MOV R0,R4
AND R0,#0x0F
CMP R0,#0x04
BLT skip_21
CMP R0,#0x08
BLT prefix_ea
CMP R0,#0x0A
BLT skip_20
JMP source_bad
skip_20:
JMP skip_21
prefix_ea:
MOV R0,R4
AND R0,#0xC0
BEQ skip_21
JMP source_bad
skip_21:
prefix_length:
MOV R13,#0x02
CALL word_length
ADD R7,#0x02
source_span:
CALL fits
CMP R0,#0x00
BEQ skip_22
JMP source_bad
skip_22:
MOV R0,R7
MOV R1,#0x00
MOV R2,R13
MOV R3,R14
JMP source_exit
source_bad:
MOV R0,#0xFF
MOV R1,#0xFF
MOV R2,#0x00
MOV R3,#0x00
source_exit:
POP QR8
POP XR4
POP PC
fits:
MOV ER0,ER8
MOV R2,R7
MOV R3,#0x00
ADD ER0,ER2
CMP ER0,ER8
BLT fits_bad
CMP ER0,ER10
BLT fits_ok
BEQ fits_ok
fits_bad:
MOV R0,#0x01
RET
fits_ok:
MOV R0,#0x00
RET
read:
MOV ER2,ER8
MOV R7,#0x00
ADD ER2,ER6
L R0,R12:[ER2]
RET
word_length:
MOV R7,#0x02
MOV R0,R5
AND R0,#0xF0
CMP R0,#0x90
BEQ word_load
CMP R0,#0xA0
BEQ word_aload
CMP R0,#0xF0
BNE word_done
MOV R0,R4
AND R0,#0x0F
CMP R0,#0x02
BLT word_four
CMP R5,#0xF0
BNE word_done
CMP R0,#0x0B
BEQ word_four
CMP R4,#0x0C
BEQ word_four
JMP word_done
word_load:
MOV R0,R4
AND R0,#0x0E
CMP R0,#0x08
BEQ word_four
MOV R0,R4
AND R0,#0xFE
CMP R0,#0x10
BEQ word_four
CMP R0,#0x12
BEQ word_four
JMP word_done
word_aload:
MOV R0,R4
AND R0,#0x0E
CMP R0,#0x08
BEQ word_four
CMP R5,#0xA0
BNE word_done
MOV R0,R4
AND R0,#0x8F
CMP R0,#0x80
BEQ word_four
CMP R0,#0x81
BEQ word_four
CMP R0,#0x82
BEQ word_four
word_done:
RET
word_four:
MOV R7,#0x04
RET
