; basic_memory
; BASIC integer, hardware-mapped memory and returning far CALL primitives.
; CPU 0xFB530, physical 0x7B530, 1758 bytes
call_bridge_address EQU 0x80400

basic_memory:
JMP dispatch
JMP to_integer
JMP to_number
JMP read_range
read_range:
PUSH ER4
MOV ER4,ER4
BEQ range_ok
ADD ER4,#0x7F
ADD ER0,ER4
ADDC R2,#0x00
BLT range_bad
range_ok:
MOV ER0,#0x00
BAL range_out
range_bad:
MOV ER0,#0x04
range_out:
POP ER4
RET
dispatch:
PUSH LR
PUSH XR4
PUSH QR8
MOV R6,PSW
PUSH EA
PUSH ER6
MOV ER8,ER2
MOV ER12,ER4
MOV R10,R0
MOV ER0,SP
MOV R2,#0x92
MOV R3,#0x83
CMP ER0,ER2
BGE skip_1
JMP entry_memory
skip_1:
ADD SP,#0xF8
MOV ER14,SP
CMP R10,#0x00
BNE skip_2
JMP peek
skip_2:
CMP R10,#0x01
BNE skip_3
JMP peek
skip_3:
CMP R10,#0x02
BNE skip_4
JMP poke
skip_4:
CMP R10,#0x03
BNE skip_5
JMP poke
skip_5:
CMP R10,#0x04
BNE skip_6
JMP call
skip_6:
CMP R10,#0x05
BNE skip_7
JMP bit_and
skip_7:
CMP R10,#0x06
BNE skip_8
JMP bit_or
skip_8:
CMP R10,#0x07
BNE skip_9
JMP bit_xor
skip_9:
CMP R10,#0x08
BNE skip_10
JMP shift_left
skip_10:
CMP R10,#0x09
BNE skip_11
JMP shift_right
skip_11:
CMP R10,#0x0A
BNE skip_12
JMP inkey
skip_12:
CMP R10,#0x0B
BNE skip_13
JMP ticks
skip_13:
CMP R10,#0x0D
BNE skip_14
JMP copy
skip_14:
CMP R10,#0x0E
BNE skip_15
JMP fill
skip_15:
JMP argument
peek:
MOV R11,R10
AND R11,#0x01
ADD R11,#0x01
L ER0,0x00:0x0000[ER8]
L ER2,0x00:0x0002[ER8]
MOV R4,#0x00
MOV R4,R11
MOV R5,#0x00
CALL read_range
MOV ER0,ER0
BEQ skip_16
JMP argument
skip_16:
L ER4,0x00:0x0000[ER8]
L ER6,0x00:0x0002[ER8]
MOV ER0,#0x00
L R0,R6:[ER4]
CMP R11,#0x01
BEQ peek_done
ADD ER4,#0x01
ADDC R6,#0x00
L R1,R6:[ER4]
peek_done:
JMP word_result
poke:
MOV R11,R10
AND R11,#0x01
ADD R11,#0x01
L ER0,0x00:0x0000[ER8]
L ER2,0x00:0x0002[ER8]
MOV R4,#0x00
MOV R4,R11
MOV R5,#0x00
CALL read_range
MOV ER0,ER0
BEQ skip_17
JMP argument
skip_17:
L ER4,0x00:0x0000[ER8]
L ER6,0x00:0x0002[ER8]
L ER0,0x00:0x0004[ER8]
ST R0,R6:[ER4]
CMP R11,#0x01
BEQ poke_done
ADD ER4,#0x01
ADDC R6,#0x00
ST R1,R6:[ER4]
poke_done:
JMP zero
copy:
L ER10,0x00:0x0008[ER8]
MOV ER10,ER10
BNE skip_18
JMP zero
skip_18:
L ER0,0x00:0x0004[ER8]
L ER2,0x00:0x0006[ER8]
MOV ER4,ER10
CALL read_range
MOV ER0,ER0
BEQ skip_19
JMP argument
skip_19:
L ER0,0x00:0x0000[ER8]
L ER2,0x00:0x0002[ER8]
CALL read_range
MOV ER0,ER0
BEQ skip_20
JMP argument
skip_20:
L ER4,0x00:0x0000[ER8]
L ER6,0x00:0x0002[ER8]
L ER0,0x00:0x0004[ER8]
L ER2,0x00:0x0006[ER8]
MOV R7,R2
MOV ER8,ER0
MOV R3,#0x00
CMP R6,R7
BLT copy_loop
BNE copy_reverse
CMP ER4,ER8
BLT copy_loop
copy_reverse:
ADD ER10,#0x7F
ADD ER4,ER10
ADDC R6,#0x00
ADD ER8,ER10
ADDC R7,#0x00
ADD ER10,#0x01
MOV R3,#0x01
copy_loop:
L R0,R7:[ER8]
ST R0,R6:[ER4]
ADD ER10,#0x7F
BNE skip_21
JMP zero
skip_21:
CMP R3,#0x00
BNE copy_back
ADD ER4,#0x01
ADDC R6,#0x00
ADD ER8,#0x01
ADDC R7,#0x00
BAL copy_loop
copy_back:
ADD ER4,#0x7F
ADDC R6,#0xFF
ADD ER8,#0x7F
ADDC R7,#0xFF
BAL copy_loop
fill:
L ER10,0x00:0x0004[ER8]
MOV ER10,ER10
BNE skip_22
JMP zero
skip_22:
L ER0,0x00:0x0000[ER8]
L ER2,0x00:0x0002[ER8]
MOV ER4,ER10
CALL read_range
MOV ER0,ER0
BEQ skip_23
JMP argument
skip_23:
L ER4,0x00:0x0000[ER8]
L ER6,0x00:0x0002[ER8]
L ER0,0x00:0x0008[ER8]
fill_loop:
ST R0,R6:[ER4]
ADD ER4,#0x01
ADDC R6,#0x00
ADD ER10,#0x7F
BNE fill_loop
JMP zero
bit_and:
L ER0,0x00:0x0000[ER8]
L ER2,0x00:0x0004[ER8]
AND R0,R2
AND R1,R3
JMP word_result
bit_or:
L ER0,0x00:0x0000[ER8]
L ER2,0x00:0x0004[ER8]
OR R0,R2
OR R1,R3
JMP word_result
bit_xor:
L ER0,0x00:0x0000[ER8]
L ER2,0x00:0x0004[ER8]
XOR R0,R2
XOR R1,R3
JMP word_result
shift_left:
L ER0,0x00:0x0000[ER8]
L ER2,0x00:0x0004[ER8]
CMP R3,#0x00
BEQ skip_24
JMP argument
skip_24:
CMP R2,#0x10
BLT skip_25
JMP argument
skip_25:
CMP R2,#0x00
BNE skip_26
JMP word_result
skip_26:
shift_left_loop:
SLLC R1,#0x01
SLL R0,#0x01
ADD R2,#0xFF
BNE skip_26
JMP word_result
shift_right:
L ER0,0x00:0x0000[ER8]
L ER2,0x00:0x0004[ER8]
CMP R3,#0x00
BEQ skip_27
JMP argument
skip_27:
CMP R2,#0x10
BLT skip_28
JMP argument
skip_28:
CMP R2,#0x00
BNE skip_29
JMP word_result
skip_29:
shift_right_loop:
SRLC R0,#0x01
SRL R1,#0x01
ADD R2,#0xFF
BNE skip_29
JMP word_result
ticks:
MOV ER0,#0x00
L R0,0x00:0xF00C
JMP word_result
inkey:
MOV ER0,#0x00
ST ER0,0x00:0x0000[ER14]
MOV R0,PSW
ST R0,0x00:0x0002[ER14]
AND R0,#0xF7
MOV PSW,R0
L R0,0x00:0xF044
ST R0,0x00:0x0003[ER14]
MOV ER0,ER14
CALL 0x1:0x2864
L R0,0x00:0x0003[ER14]
ST R0,0x00:0xF044
L R0,0x00:0x0002[ER14]
MOV PSW,R0
L ER2,0x00:0x0000[ER14]
MOV ER0,#0x00
CMP R2,#0x00
BNE skip_30
JMP word_result
skip_30:
MOV R0,#0x01
key_column:
MOV R4,R3
AND R4,#0x01
BNE key_row
SRL R3,#0x01
ADD R0,#0x10
BAL key_column
key_row:
MOV R4,R2
AND R4,#0x01
BEQ skip_31
JMP word_result
skip_31:
SRL R2,#0x01
ADD R0,#0x01
BAL key_row
call:
L ER0,0x00:0x0002[ER8]
CMP R1,#0x00
BEQ skip_32
JMP argument
skip_32:
CMP R0,#0x10
BLT skip_33
JMP argument
skip_33:
L ER0,0x00:0x0000[ER8]
MOV R2,R0
AND R2,#0x01
BEQ skip_34
JMP argument
skip_34:
PUSH QR0
PUSH QR8
ADD SP,#0x88
MOV ER2,SP
MOV R0,#0x00
MOV R1,#0x80
MOV R5,#0x70
call_save_8000:
L R4,0x00:[ER0]
ST R4,0x00:[ER2]
ADD ER0,#0x01
ADD ER2,#0x01
ADD R5,#0xFF
BNE call_save_8000
MOV R0,#0x86
MOV R1,#0x80
MOV R5,#0x02
call_save_8086:
L R4,0x00:[ER0]
ST R4,0x00:[ER2]
ADD ER0,#0x01
ADD ER2,#0x01
ADD R5,#0xFF
BNE call_save_8086
MOV R0,#0xA0
MOV R1,#0x80
MOV R5,#0x03
call_save_80a0:
L R4,0x00:[ER0]
ST R4,0x00:[ER2]
ADD ER0,#0x01
ADD ER2,#0x01
ADD R5,#0xFF
BNE call_save_80a0
L ER0,0x00:0x0004[ER8]
L ER2,0x00:0x0008[ER8]
L ER4,0x00:0x000C[ER8]
L ER6,0x00:0x0010[ER8]
L ER10,0x00:0x0002[ER8]
L ER8,0x00:0x0000[ER8]
CALL call_bridge_address
MOV ER2,SP
ADD ER2,#0x3F
ADD ER2,#0x3F
ADD ER2,#0x0A
ST ER0,0x00:[ER2]
MOV ER2,SP
MOV R0,#0x00
MOV R1,#0x80
MOV R5,#0x70
call_restore_8000:
L R4,0x00:[ER2]
ST R4,0x00:[ER0]
ADD ER0,#0x01
ADD ER2,#0x01
ADD R5,#0xFF
BNE call_restore_8000
MOV R0,#0x86
MOV R1,#0x80
MOV R5,#0x02
call_restore_8086:
L R4,0x00:[ER2]
ST R4,0x00:[ER0]
ADD ER0,#0x01
ADD ER2,#0x01
ADD R5,#0xFF
BNE call_restore_8086
MOV R0,#0xA0
MOV R1,#0x80
MOV R5,#0x03
call_restore_80a0:
L R4,0x00:[ER2]
ST R4,0x00:[ER0]
ADD ER0,#0x01
ADD ER2,#0x01
ADD R5,#0xFF
BNE call_restore_80a0
ADD SP,#0x78
POP QR8
POP QR0
L ER0,0x00:0x0000[ER14]
JMP word_result
zero:
MOV ER0,#0x00
word_result:
MOV ER2,#0x00
ST ER0,0x00:[ER12]
ST ER2,0x00:0x0002[ER12]
MOV ER0,#0x00
JMP dispatch_out
argument:
MOV ER0,#0x04
JMP dispatch_out
memory:
MOV ER0,#0x06
dispatch_out:
ADD SP,#0x08
entry_out:
POP ER2
POP EA
POP QR8
POP XR4
MOV PSW,R2
POP PC
entry_memory:
MOV ER0,#0x06
JMP entry_out
to_integer:
PUSH LR
PUSH XR4
PUSH QR8
MOV ER8,ER0
MOV ER12,ER4
MOV ER10,ER2
MOV ER0,SP
MOV R2,#0xC2
MOV R3,#0x82
CMP ER0,ER2
BGE skip_35
JMP conv_memory
skip_35:
ADD SP,#0xF0
MOV ER14,SP
ST R10,0x00:0x0000[ER14]
CMP R11,#0x00
BEQ skip_36
JMP conv_argument
skip_36:
CMP R10,#0x05
BLT skip_37
JMP conv_argument
skip_37:
MOV ER2,ER8
ADD ER2,#0x0A
MOV R6,#0x0A
imaginary:
L R0,0x00:[ER2]
CMP R0,#0x00
BEQ skip_38
JMP conv_argument
skip_38:
ADD ER2,#0x01
ADD R6,#0xFF
BNE imaginary
MOV ER4,#0x00
MOV ER6,#0x00
L R0,0x00:[ER8]
CMP R0,#0x00
BNE nonzero
MOV ER2,ER8
MOV R6,#0x0A
native_zero:
L R0,0x00:[ER2]
CMP R0,#0x00
BEQ skip_39
JMP conv_argument
skip_39:
ADD ER2,#0x01
ADD R6,#0xFF
BNE native_zero
JMP integer_result
nonzero:
CMP R0,#0x0A
BLT skip_40
JMP conv_argument
skip_40:
L R0,0x00:0x0009[ER8]
MOV R1,#0x00
CMP R0,#0x05
BLT positive
ADD R0,#0xFB
MOV R1,#0x01
positive:
ST R1,0x00:0x0001[ER14]
CMP R0,#0x01
BEQ skip_41
JMP conv_argument
skip_41:
L R7,0x00:0x0008[ER8]
CMP R7,#0x08
BLT skip_42
JMP conv_argument
skip_42:
MOV R10,#0x00
digit:
CMP R10,#0x00
BEQ digit_low
MOV R0,R10
AND R0,#0x01
BEQ digit_low
ADD ER8,#0x01
L R3,0x00:[ER8]
SRL R3,#0x04
BAL digit_ready
digit_low:
L R3,0x00:[ER8]
AND R3,#0x0F
digit_ready:
CMP R3,#0x0A
BLT skip_43
JMP conv_argument
skip_43:
MOV R0,R7
ADD R0,#0x01
CMP R10,R0
BLT accumulate
CMP R3,#0x00
BEQ skip_44
JMP conv_argument
skip_44:
JMP digit_next
accumulate:
CMP R4,#0x99
CMPC R5,#0x99
CMPC R6,#0x19
BLT skip_46
BEQ skip_45
JMP conv_argument
skip_45:
CMP R3,#0x06
BLT skip_46
JMP conv_argument
skip_46:
multiply:
MOV ER0,ER4
MOV R2,R6
SLLC R6,#0x01
SLLC R5,#0x01
SLL R4,#0x01
SLLC R2,#0x03
SLLC R1,#0x03
SLL R0,#0x03
ADD R4,R0
ADDC R5,R1
ADDC R6,R2
ADD R4,R3
ADDC R5,#0x00
ADDC R6,#0x00
digit_next:
ADD R10,#0x01
CMP R10,#0x0F
BGE skip_47
JMP digit
skip_47:
MOV R7,#0x00
L R0,0x00:0x0000[ER14]
CMP R0,#0x04
BEQ skip_50
CMP R0,#0x02
BNE narrow_result
CMP R6,#0x10
BLT skip_48
JMP conv_argument
skip_48:
JMP skip_50
narrow_result:
CMP R6,#0x00
BEQ skip_49
JMP conv_argument
skip_49:
CMP R0,#0x03
BEQ signed_result
CMP R0,#0x01
BEQ skip_50
CMP R5,#0x00
BEQ skip_50
JMP conv_argument
skip_50:
unsigned_result:
L R0,0x00:0x0001[ER14]
CMP R0,#0x00
BEQ skip_51
JMP conv_argument
skip_51:
JMP integer_result
signed_result:
L R0,0x00:0x0001[ER14]
CMP R0,#0x00
BNE negative_result
CMP R5,#0x80
BLT skip_52
JMP conv_argument
skip_52:
JMP integer_result
negative_result:
CMP R4,#0x00
CMPC R5,#0x80
BLT skip_53
BEQ skip_53
JMP conv_argument
skip_53:
negate:
XOR R4,#0xFF
XOR R5,#0xFF
ADD ER4,#0x01
MOV R6,#0xFF
MOV R7,#0xFF
integer_result:
ST ER4,0x00:[ER12]
ST ER6,0x00:0x0002[ER12]
MOV ER0,#0x00
JMP conv_out
to_number:
PUSH LR
PUSH XR4
PUSH QR8
MOV ER8,ER0
MOV ER12,ER2
MOV ER0,SP
MOV R2,#0xC2
MOV R3,#0x82
CMP ER0,ER2
BGE skip_54
JMP conv_memory
skip_54:
ADD SP,#0xF0
MOV ER14,SP
L ER4,0x00:[ER8]
L ER6,0x00:0x0002[ER8]
MOV ER8,ER14
MOV R10,#0x00
decimal_divide:
MOV R1,#0x00
MOV R0,R7
MOV R2,#0x0A
DIV ER0,R2
MOV R7,R0
MOV R1,R2
MOV R0,R6
MOV R2,#0x0A
DIV ER0,R2
MOV R6,R0
MOV R1,R2
MOV R0,R5
MOV R2,#0x0A
DIV ER0,R2
MOV R5,R0
MOV R1,R2
MOV R0,R4
MOV R2,#0x0A
DIV ER0,R2
MOV R4,R0
MOV R1,R2
ST R2,0x00:[ER8]
ADD ER8,#0x01
ADD R10,#0x01
MOV R0,R4
OR R0,R5
OR R0,R6
OR R0,R7
BNE decimal_divide
MOV ER2,ER12
MOV R0,#0x00
MOV R1,#0x14
number_clear:
ST R0,0x00:[ER2]
ADD ER2,#0x01
ADD R1,#0xFF
BNE number_clear
MOV R0,R10
ADD R0,#0xFF
ST R0,0x00:0x0008[ER12]
ADD ER8,#0x7F
L R0,0x00:[ER8]
CMP R0,#0x00
BEQ number_done
MOV R1,#0x01
ST R1,0x00:0x0009[ER12]
ST R0,0x00:[ER12]
ADD R10,#0xFF
BEQ number_done
number_pair:
ADD ER12,#0x01
ADD ER8,#0x7F
L R3,0x00:[ER8]
SLL R3,#0x04
ADD R10,#0xFF
BEQ number_last
ADD ER8,#0x7F
L R0,0x00:[ER8]
OR R3,R0
ADD R10,#0xFF
number_last:
ST R3,0x00:[ER12]
CMP R10,#0x00
BNE number_pair
number_done:
MOV ER0,#0x00
JMP conv_out
conv_argument:
MOV ER0,#0x04
conv_out:
ADD SP,#0x10
POP QR8
POP XR4
POP PC
conv_memory:
MOV ER0,#0x06
POP QR8
POP XR4
POP PC
