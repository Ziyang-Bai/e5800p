; basic_asm
; Bounded, streaming BASIC ASM compiler for the nX-U8.
; CPU 0xF9530, physical 0x79530, 4166 bytes
basic_flash EQU 0xF6E68
basic_memory EQU 0xFB530
codec_encode_address EQU 0x808E0

basic_asm:
JMP execute
JMP skip
execute:
PUSH LR
PUSH XR4
PUSH QR8
MOV R7,#0x00
JMP entry
skip:
PUSH LR
PUSH XR4
PUSH QR8
MOV R7,#0x01
entry:
MOV ER8,ER0
MOV ER12,ER2
MOV ER0,SP
MOV R2,#0xD2
MOV R3,#0x83
CMP ER0,ER2
BGE near_1
JMP entry_memory
near_1:
ADD SP,#0x80
MOV ER14,SP
ST ER12,0x00:0x0000[ER14]
ST R7,0x00:0x0007[ER14]
MOV ER10,ER14
MOV R2,#0x7E
MOV R3,#0x00
MOV R0,#0x00
ADD ER10,#0x02
clear_frame:
ST R0,0x00:[ER10]
ADD ER10,#0x01
ADD ER2,#0x7F
BNE clear_frame
ST R7,0x00:0x0007[ER14]
ST ER14,0x00:0x0076[ER14]
MOV R6,#0x10
clear_output:
ST R0,0x00:[ER12]
ADD ER12,#0x01
ADD R6,#0xFF
BNE clear_output
L ER0,0x00:0x0000[ER8]
ST ER0,0x00:0x0002[ER14]
L ER0,0x00:0x0004[ER8]
ST ER0,0x00:0x0004[ER14]
L ER0,0x00:0x0008[ER8]
ST ER0,0x00:0x0008[ER14]
L ER0,0x00:0x0002[ER8]
CMP R1,#0x00
BEQ near_2
JMP bad_operand
near_2:
ST R0,0x00:0x0006[ER14]
L ER2,0x00:0x0006[ER8]
CMP ER0,ER2
BEQ near_3
JMP bad_operand
near_3:
L ER2,0x00:0x000A[ER8]
CMP ER0,ER2
BEQ near_4
JMP bad_operand
near_4:
L ER0,0x00:0x0002[ER14]
L ER2,0x00:0x0008[ER14]
CMP ER0,ER2
BLT near_5
JMP begin_equal
near_5:
JMP near_6
begin_equal:
BEQ near_6
JMP bad_operand
near_6:
begin_ok:
L ER0,0x00:0x0008[ER14]
ST ER0,0x00:0x000A[ER14]
ST ER0,0x00:0x000C[ER14]
L ER2,0x00:0x0004[ER14]
CMP ER0,ER2
BLT near_7
JMP no_endasm
near_7:
CALL measure
CALL get
CMP R0,#0xF9
BEQ near_8
JMP bad_operand
near_8:
CALL get
CMP R0,#0xF7
BEQ near_9
JMP bad_operand
near_9:
L R0,0x00:0x0007[ER14]
CMP R0,#0x00
BEQ near_10
JMP skip_header
near_10:
CALL spaces
MOV R0,#0x00
ST R0,0x00:0x003F[ER14]
CALL decimal
L R6,0x00:0x003F[ER14]
CMP R6,#0x00
BEQ near_11
JMP bad_operand
near_11:
CMP R2,#0x08
BGE near_12
JMP address_range
near_12:
CMP R2,#0x10
BLT near_13
JMP address_range
near_13:
CMP R3,#0x00
BEQ near_14
JMP address_range
near_14:
ST R2,0x00:0x007C[ER14]
ST ER0,0x00:0x0012[ER14]
CALL even_address
CALL line_tail
JMP header_done
skip_header:
CALL discard_line
header_done:
CALL peek
CMP R0,#0x0D
BEQ near_15
JMP no_endasm
near_15:
CALL get
L ER0,0x00:0x000A[ER14]
ST ER0,0x00:0x000E[ER14]
ST ER0,0x00:0x000C[ER14]
L R0,0x00:0x0007[ER14]
CMP R0,#0x00
BEQ near_16
JMP skip_loop
near_16:
MOV R0,#0x00
ST R0,0x00:0x0019[ER14]
CALL reset
label_pass:
CALL next
CMP R1,#0x03
BNE near_17
JMP add_label
near_17:
CMP R1,#0x01
BNE near_18
JMP labels_done
near_18:
CMP R1,#0x00
BEQ near_19
JMP failure
near_19:
JMP label_pass
add_label:
L R0,0x00:0x007D[ER14]
CMP R0,#0x00
BEQ near_20
JMP address_range
near_20:
CALL find_label
MOV ER2,#0x00
CMP ER0,ER2
BEQ near_21
JMP dup_label
near_21:
MOV ER0,SP
MOV R2,#0x5E
MOV R3,#0x83
CMP ER0,ER2
BGE near_22
JMP memory
near_22:
ADD SP,#0xF4
L ER8,0x00:0x0076[ER14]
ADD ER8,#0x74
ST ER8,0x00:0x0076[ER14]
L R0,0x00:0x0038[ER14]
ST R0,0x00:[ER8]
MOV ER10,ER14
ADD ER10,#0x30
ADD ER8,#0x02
MOV R6,#0x08
label_copy:
L R0,0x00:[ER10]
ST R0,0x00:[ER8]
ADD ER10,#0x01
ADD ER8,#0x01
ADD R6,#0xFF
BNE label_copy
L ER0,0x00:0x0014[ER14]
ST ER0,0x00:[ER8]
JMP label_pass
labels_done:
MOV R0,#0x01
ST R0,0x00:0x0019[ER14]
MOV R0,#0x00
ST R0,0x00:0x006D[ER14]
CALL reset
compare_pass:
CALL next
CMP R1,#0x01
BNE near_23
JMP compare_done
near_23:
CMP R1,#0x00
BEQ near_24
JMP failure
near_24:
MOV R4,R0
L ER2,0x00:0x0014[ER14]
ADD ER2,#0x7F
L R5,0x00:0x007C[ER14]
L R0,R5:[ER2]
CMP R0,R4
BEQ compare_pass
MOV R0,#0x01
ST R0,0x00:0x006D[ER14]
JMP compare_pass
compare_done:
L R0,0x00:0x006D[ER14]
CMP R0,#0x00
BNE near_25
JMP near_27
near_25:
MOV ER0,SP
MOV R2,#0xD4
MOV R3,#0x83
CMP ER0,ER2
BGE near_26
JMP memory
near_26:
L ER0,0x00:0x0012[ER14]
L ER2,0x00:0x0016[ER14]
MOV R4,#0x58
MOV R5,#0x9D
MOV ER6,ER14
L R8,0x00:0x007C[ER14]
CALL basic_flash
CMP R0,#0x00
BEQ near_27
JMP write_error
near_27:
call_block:
MOV ER8,ER14
ADD ER8,#0x3F
ADD ER8,#0x11
MOV R0,#0x00
MOV R6,#0x1C
clear_call:
ST R0,0x00:[ER8]
ADD ER8,#0x01
ADD R6,#0xFF
BNE clear_call
L ER0,0x00:0x0012[ER14]
ST ER0,0x00:0x0050[ER14]
L R0,0x00:0x007C[ER14]
ST R0,0x00:0x0052[ER14]
MOV ER0,#0x04
MOV ER2,ER14
ADD ER2,#0x3F
ADD ER2,#0x11
MOV ER4,ER14
ADD ER4,#0x3F
ADD ER4,#0x29
CALL basic_memory
CMP R0,#0x00
BEQ near_28
JMP call_error
near_28:
L ER8,0x00:0x0000[ER14]
L ER0,0x00:0x0068[ER14]
ST ER0,0x00:0x0008[ER8]
MOV ER0,#0x00
ST ER0,0x00:0x000A[ER8]
JMP success
skip_loop:
CALL line_start
CMP R0,#0x01
BNE near_29
JMP success
near_29:
CALL discard_line
CALL get
CMP R0,#0x0D
BEQ near_30
JMP no_endasm
near_30:
JMP skip_loop
success:
L ER8,0x00:0x0000[ER14]
L ER0,0x00:0x0010[ER14]
ST ER0,0x00:[ER8]
L R0,0x00:0x0006[ER14]
MOV R1,#0x00
ST ER0,0x00:0x0002[ER8]
MOV ER0,#0x00
ST ER0,0x00:0x000C[ER8]
JMP exit_status
bad_operand:
MOV ER0,#0x01
ST ER0,0x00:0x001A[ER14]
JMP failure
dup_label:
MOV ER0,#0x02
ST ER0,0x00:0x001A[ER14]
JMP failure
no_label:
MOV ER0,#0x03
ST ER0,0x00:0x001A[ER14]
JMP failure
br_range:
MOV ER0,#0x04
ST ER0,0x00:0x001A[ER14]
JMP failure
address_range:
MOV ER0,#0x05
ST ER0,0x00:0x001A[ER14]
JMP failure
no_endasm:
MOV ER0,#0x06
ST ER0,0x00:0x001A[ER14]
JMP failure
call_error:
MOV ER6,ER0
L ER0,0x00:0x0008[ER14]
ST ER0,0x00:0x000C[ER14]
MOV ER0,#0x00
ST ER0,0x00:0x001A[ER14]
MOV ER0,ER6
JMP error_output
write_error:
L ER0,0x00:0x0008[ER14]
ST ER0,0x00:0x000C[ER14]
MOV R0,#0x00
MOV R1,#0x01
JMP error_output
memory:
MOV ER0,#0x06
JMP error_output
failure:
MOV ER0,#0x02
error_output:
MOV ER6,ER0
L R0,0x00:0x006E[ER14]
CMP R0,#0x00
BEQ near_31
JMP reader_error
near_31:
L ER8,0x00:0x0000[ER14]
L ER0,0x00:0x000C[ER14]
ST ER0,0x00:0x0004[ER8]
L R0,0x00:0x0006[ER14]
MOV R1,#0x00
ST ER0,0x00:0x0006[ER8]
L ER0,0x00:0x001A[ER14]
ST ER0,0x00:0x000C[ER8]
MOV ER0,ER6
exit_status:
MOV ER2,ER14
ADD ER2,#0x3F
ADD ER2,#0x3F
ADD ER2,#0x02
MOV SP,ER2
POP QR8
POP XR4
POP PC
entry_memory:
MOV ER0,#0x06
POP QR8
POP XR4
POP PC
peek:
L ER2,0x00:0x000A[ER14]
L ER0,0x00:0x0004[ER14]
CMP ER2,ER0
BLT near_32
JMP no_endasm
near_32:
L ER0,0x00:0x0002[ER14]
CMP ER2,ER0
BGE near_33
JMP bad_operand
near_33:
L ER2,0x00:0x000A[ER14]
L R5,0x00:0x0006[ER14]
L R0,R5:[ER2]
RET
get:
PUSH LR
CALL peek
L ER2,0x00:0x000A[ER14]
ADD ER2,#0x01
ST ER2,0x00:0x000A[ER14]
POP PC
upper:
CMP R0,#0x61
BLT upper_done
CMP R0,#0x7B
BGE upper_done
ADD R0,#0xE0
upper_done:
RET
spaces:
PUSH LR
space_loop:
CALL peek
CMP R0,#0x20
BNE spaces_done
CALL get
JMP space_loop
spaces_done:
POP PC
discard_line:
PUSH LR
discard_byte:
CALL peek
CMP R0,#0x0D
BEQ discard_done
CMP R0,#0x00
BNE near_34
JMP no_endasm
near_34:
CALL get
JMP discard_byte
discard_done:
POP PC
line_tail:
PUSH LR
CALL spaces
CMP R0,#0x3B
BNE tail_check
comment_byte:
CALL get
CALL peek
CMP R0,#0x00
BEQ near_35
CMP R0,#0x0D
BNE comment_byte
tail_check:
CMP R0,#0x0D
BEQ near_35
CMP R0,#0x00
BEQ near_35
JMP operand_fail
near_35:
tail_done:
POP PC
measure:
L ER0,0x00:0x000A[ER14]
ST ER0,0x00:0x000C[ER14]
RET
line_start:
PUSH LR
CALL measure
CALL spaces
CMP R0,#0x00
BNE near_36
JMP no_endasm
near_36:
CMP R0,#0xF9
BNE ordinary_line
CALL get
CALL get
CMP R0,#0xF8
BEQ near_37
JMP bad_operand
near_37:
CALL line_tail
L ER0,0x00:0x000A[ER14]
ST ER0,0x00:0x0010[ER14]
MOV R0,#0x01
POP PC
ordinary_line:
MOV R0,#0x00
POP PC
identifier:
PUSH LR
MOV ER8,ER14
ADD ER8,#0x30
MOV R0,#0x00
ST R0,0x00:0x0000[ER8]
ST R0,0x00:0x0001[ER8]
ST R0,0x00:0x0002[ER8]
ST R0,0x00:0x0003[ER8]
ST R0,0x00:0x0004[ER8]
ST R0,0x00:0x0005[ER8]
ST R0,0x00:0x0006[ER8]
ST R0,0x00:0x0007[ER8]
MOV R6,#0x00
identifier_byte:
CALL peek
CALL upper
CMP R0,#0x5F
BEQ identifier_accept
CMP R0,#0x41
BLT identifier_digit
CMP R0,#0x5B
BLT identifier_accept
identifier_digit:
CMP R6,#0x00
BEQ identifier_end
CMP R0,#0x30
BLT identifier_end
CMP R0,#0x3A
BGE identifier_end
identifier_accept:
CMP R6,#0x08
BLT near_38
JMP operand_fail
near_38:
ST R0,0x00:[ER8]
ADD ER8,#0x01
ADD R6,#0x01
CALL get
JMP identifier_byte
identifier_end:
ST R6,0x00:0x0038[ER14]
CMP R6,#0x00
BNE near_39
JMP operand_fail
near_39:
POP PC
find_label:
PUSH LR
L ER8,0x00:0x0076[ER14]
find_record:
MOV ER0,ER8
MOV ER2,ER14
CMP ER0,ER2
BEQ find_missing
L R0,0x00:[ER8]
L R1,0x00:0x0038[ER14]
CMP R0,R1
BNE find_next
MOV ER10,ER14
ADD ER10,#0x30
MOV ER12,ER8
ADD ER12,#0x02
MOV R6,#0x08
find_char:
L R0,0x00:[ER10]
L R1,0x00:[ER12]
CMP R0,R1
BNE find_next
ADD ER10,#0x01
ADD ER12,#0x01
ADD R6,#0xFF
BNE find_char
MOV ER0,ER8
POP PC
find_next:
ADD ER8,#0x0C
JMP find_record
find_missing:
MOV ER0,#0x00
POP PC
even_address:
MOV R2,R0
AND R2,#0x01
BEQ near_40
JMP address_range
near_40:
RET
number:
PUSH LR
MOV R0,#0x00
ST R0,0x00:0x003E[ER14]
MOV R0,#0x00
ST R0,0x00:0x003F[ER14]
MOV R0,#0x00
ST R0,0x00:0x0039[ER14]
CALL spaces
CMP R0,#0x23
BNE number_sign
CALL get
CALL spaces
number_sign:
CMP R0,#0x2D
BNE number_plus
MOV R0,#0x01
ST R0,0x00:0x003E[ER14]
CALL get
JMP number_atom
number_plus:
CMP R0,#0x2B
BNE number_atom
CALL get
number_atom:
CALL peek
CMP R0,#0x30
BLT number_label
CMP R0,#0x3A
BGE number_label
CALL decimal
POP PC
number_label:
CALL identifier
CALL find_label
CMP R0,#0x00
BNE number_found
CMP R1,#0x00
BNE number_found
L R0,0x00:0x0019[ER14]
CMP R0,#0x00
BEQ near_41
JMP undefined_operand
near_41:
MOV R0,#0x02
ST R0,0x00:0x0039[ER14]
MOV ER0,#0x00
MOV R2,#0x00
JMP label_offset
number_found:
MOV ER8,ER0
MOV R0,#0x01
ST R0,0x00:0x0039[ER14]
L ER0,0x00:0x000A[ER8]
MOV R2,#0x00
label_offset:
ST ER0,0x00:0x003A[ER14]
ST R2,0x00:0x003C[ER14]
CALL spaces
CMP R0,#0x2B
BEQ offset_plus
CMP R0,#0x2D
BNE label_number_done
MOV R0,#0x01
ST R0,0x00:0x003D[ER14]
JMP offset_read
offset_plus:
MOV R0,#0x00
ST R0,0x00:0x003D[ER14]
offset_read:
CALL get
CALL spaces
CALL decimal
CMP R2,#0x00
BEQ near_42
JMP operand_fail
near_42:
L R3,0x00:0x0039[ER14]
CMP R3,#0x02
BEQ label_number_done
MOV ER4,ER0
L ER0,0x00:0x003A[ER14]
L R2,0x00:0x003D[ER14]
CMP R2,#0x00
BNE offset_subtract
ADD ER0,ER4
L ER2,0x00:0x003A[ER14]
CMP ER0,ER2
BGE near_43
JMP operand_fail
near_43:
JMP offset_applied
offset_subtract:
CMP ER0,ER4
BGE near_44
JMP operand_fail
near_44:
SUB R0,R4
SUBC R1,R5
offset_applied:
ST ER0,0x00:0x003A[ER14]
label_number_done:
L ER0,0x00:0x003A[ER14]
L R2,0x00:0x003C[ER14]
MOV R3,#0x00
POP PC
undefined_operand:
MOV ER0,#0x03
ST ER0,0x00:0x001A[ER14]
L R0,0x00:0x006C[ER14]
CMP R0,#0x00
BNE near_45
JMP failure
near_45:
JMP operand_fail
decimal:
PUSH LR
MOV ER10,#0x00
MOV R12,#0x00
MOV R7,#0x00
CALL peek
CMP R0,#0x30
BNE digit_loop
CALL get
MOV R7,#0x01
CALL peek
CALL upper
CMP R0,#0x58
BNE digit_loop
MOV R0,#0x01
ST R0,0x00:0x003F[ER14]
MOV R7,#0x00
CALL get
digit_loop:
CALL peek
CALL upper
ADD R0,#0xD0
CMP R0,#0x0A
BLT digit_valid
L R1,0x00:0x003F[ER14]
CMP R1,#0x00
BEQ digits_done
ADD R0,#0xF9
CMP R0,#0x0A
BLT digits_done
CMP R0,#0x10
BGE digits_done
digit_valid:
MOV R6,R0
L R0,0x00:0x003F[ER14]
CMP R0,#0x00
BNE hex_multiply
MOV ER0,ER10
MOV R2,R12
SLLC R2,#0x01
SLLC R1,#0x01
SLL R0,#0x01
SLLC R12,#0x01
SLLC R11,#0x01
SLL R10,#0x01
SLLC R12,#0x01
SLLC R11,#0x01
SLL R10,#0x01
SLLC R12,#0x01
SLLC R11,#0x01
SLL R10,#0x01
ADD R10,R0
ADDC R11,R1
ADDC R12,R2
JMP digit_add
hex_multiply:
SLLC R12,#0x01
SLLC R11,#0x01
SLL R10,#0x01
SLLC R12,#0x01
SLLC R11,#0x01
SLL R10,#0x01
SLLC R12,#0x01
SLLC R11,#0x01
SLL R10,#0x01
SLLC R12,#0x01
SLLC R11,#0x01
SLL R10,#0x01
digit_add:
ADD R10,R6
ADDC R11,#0x00
ADDC R12,#0x00
CMP R12,#0x10
BLT near_46
JMP operand_fail
near_46:
MOV R7,#0x01
CALL get
JMP digit_loop
digits_done:
CMP R7,#0x00
BNE near_47
JMP operand_fail
near_47:
MOV ER0,ER10
MOV R2,R12
MOV R3,#0x00
POP PC
reader:
PUSH LR
PUSH XR4
PUSH QR8
MOV ER14,ER0
MOV ER0,SP
ST ER0,0x00:0x0078[ER14]
MOV R0,#0x01
ST R0,0x00:0x006E[ER14]
CMP R2,#0x00
BNE reader_next
CALL reset
MOV ER0,#0x00
JMP reader_return
reader_next:
CALL next
reader_return:
MOV R2,#0x00
ST R2,0x00:0x006E[ER14]
POP QR8
POP XR4
POP PC
reader_error:
L ER2,0x00:0x0078[ER14]
MOV SP,ER2
MOV R0,#0x00
MOV R1,#0x02
JMP reader_return
reset:
L ER0,0x00:0x000E[ER14]
ST ER0,0x00:0x000A[ER14]
L ER0,0x00:0x0012[ER14]
ST ER0,0x00:0x0014[ER14]
MOV ER0,#0x00
ST ER0,0x00:0x0016[ER14]
MOV R0,#0x00
ST R0,0x00:0x007D[ER14]
MOV R0,#0x00
ST R0,0x00:0x0026[ER14]
ST R0,0x00:0x0027[ER14]
ST R0,0x00:0x0028[ER14]
ST R0,0x00:0x0029[ER14]
ST R0,0x00:0x002A[ER14]
ST R0,0x00:0x002B[ER14]
ST R0,0x00:0x006C[ER14]
RET
next:
PUSH LR
next_again:
L R0,0x00:0x0027[ER14]
L R1,0x00:0x0026[ER14]
CMP R0,R1
BGE near_48
JMP emit_byte
near_48:
MOV R0,#0x00
ST R0,0x00:0x0026[ER14]
MOV R0,#0x00
ST R0,0x00:0x0027[ER14]
L R0,0x00:0x0028[ER14]
CMP R0,#0x00
BEQ near_49
JMP data_next
near_49:
L R0,0x00:0x002A[ER14]
CMP R0,#0x02
BNE near_50
JMP next_line
near_50:
CMP R0,#0x00
BNE line_continue
CALL line_start
CMP R0,#0x01
BNE near_51
JMP stream_end
near_51:
MOV R0,#0x01
ST R0,0x00:0x002A[ER14]
line_continue:
CALL spaces
CMP R0,#0x0D
BNE near_52
JMP next_line
near_52:
CMP R0,#0x3B
BNE near_53
JMP finish_line
near_53:
CMP R0,#0x00
BNE near_54
JMP no_endasm
near_54:
CALL identifier
CALL spaces
CMP R0,#0x3A
BNE instruction_line
CALL get
L R0,0x00:0x0019[ER14]
CMP R0,#0x00
BNE line_continue
MOV R0,#0x00
MOV R1,#0x03
POP PC
instruction_line:
L R0,0x00:0x0038[ER14]
CMP R0,#0x02
BNE instruction_match
L R0,0x00:0x0030[ER14]
CMP R0,#0x44
BNE instruction_match
L R0,0x00:0x0031[ER14]
CMP R0,#0x42
BEQ db_begin
CMP R0,#0x57
BNE instruction_match
MOV R0,#0x02
ST R0,0x00:0x0028[ER14]
JMP data_begin
db_begin:
MOV R0,#0x01
ST R0,0x00:0x0028[ER14]
data_begin:
MOV R0,#0x01
ST R0,0x00:0x002B[ER14]
JMP data_next
instruction_match:
L R0,0x00:0x007D[ER14]
CMP R0,#0x00
BEQ near_55
JMP address_range
near_55:
L ER0,0x00:0x0014[ER14]
CALL even_address
CALL match
CALL line_tail
MOV R0,#0x02
ST R0,0x00:0x002A[ER14]
JMP next_again
data_next:
L R0,0x00:0x0029[ER14]
CMP R0,#0x00
BEQ near_56
JMP string_byte
near_56:
CALL spaces
L R1,0x00:0x002B[ER14]
CMP R1,#0x02
BNE data_value
CMP R0,#0x2C
BEQ near_57
JMP data_finish
near_57:
CALL get
CALL spaces
data_value:
MOV R0,#0x02
ST R0,0x00:0x002B[ER14]
CALL peek
CMP R0,#0x22
BNE data_number
L R0,0x00:0x0028[ER14]
CMP R0,#0x01
BEQ near_58
JMP bad_operand
near_58:
CALL get
MOV R0,#0x01
ST R0,0x00:0x0029[ER14]
string_byte:
CALL get
CMP R0,#0x22
BNE string_ascii
CALL peek
CMP R0,#0x22
BEQ escaped_quote
MOV R0,#0x00
ST R0,0x00:0x0029[ER14]
JMP data_next
escaped_quote:
CALL get
string_ascii:
CMP R0,#0x20
BGE near_59
JMP bad_operand
near_59:
CMP R0,#0x7F
BLT near_60
JMP bad_operand
near_60:
ST R0,0x00:0x0048[ER14]
MOV R0,#0x01
ST R0,0x00:0x0026[ER14]
JMP next_again
data_number:
CALL number
CMP R2,#0x00
BEQ near_61
JMP bad_operand
near_61:
L R2,0x00:0x003E[ER14]
CMP R2,#0x00
BEQ near_62
JMP bad_operand
near_62:
ST ER0,0x00:0x0048[ER14]
L R2,0x00:0x0028[ER14]
CMP R2,#0x01
BNE near_63
CMP R1,#0x00
BEQ near_63
JMP bad_operand
near_63:
data_word:
ST R2,0x00:0x0026[ER14]
JMP next_again
data_finish:
MOV R0,#0x00
ST R0,0x00:0x0028[ER14]
finish_line:
CALL line_tail
next_line:
CALL get
CMP R0,#0x0D
BEQ near_64
JMP no_endasm
near_64:
MOV R0,#0x00
ST R0,0x00:0x002A[ER14]
JMP next_again
emit_byte:
MOV R1,#0x00
MOV ER2,ER14
ADD ER2,#0x3F
ADD ER2,#0x09
ADD ER2,ER0
L R6,0x00:[ER2]
ADD R0,#0x01
ST R0,0x00:0x0027[ER14]
L R0,0x00:0x007D[ER14]
CMP R0,#0x00
BEQ near_65
JMP address_range
near_65:
L ER0,0x00:0x0016[ER14]
MOV R2,#0xFF
MOV R3,#0xFF
CMP ER0,ER2
BNE near_66
JMP address_range
near_66:
ADD ER0,#0x01
ST ER0,0x00:0x0016[ER14]
L ER0,0x00:0x0014[ER14]
ADD ER0,#0x01
ST ER0,0x00:0x0014[ER14]
MOV ER2,#0x00
CMP ER0,ER2
BNE emit_ready
MOV R0,#0x01
ST R0,0x00:0x007D[ER14]
emit_ready:
MOV R0,R6
MOV R1,#0x00
POP PC
stream_end:
MOV R0,#0x00
MOV R1,#0x01
POP PC
match:
PUSH LR
MOV ER8,ER14
ADD ER8,#0x30
MOV ER10,ER14
ADD ER10,#0x3F
ADD ER10,#0x11
MOV R6,#0x08
save_mnemonic:
L R0,0x00:[ER8]
ST R0,0x00:[ER10]
ADD ER8,#0x01
ADD ER10,#0x01
ADD R6,#0xFF
BNE save_mnemonic
MOV R0,#0x00
ST R0,0x00:0x0058[ER14]
L ER0,0x00:0x000A[ER14]
ST ER0,0x00:0x0022[ER14]
MOV ER0,SP
ST ER0,0x00:0x001C[ER14]
MOV R0,#0x01
ST R0,0x00:0x006C[ER14]
MOV ER0,#0x01
ST ER0,0x00:0x001A[ER14]
MOV R0,#0x76
MOV R1,#0xA5
ST ER0,0x00:0x001E[ER14]
candidate:
L ER8,0x00:0x001E[ER14]
MOV R7,#0x0F
L ER10,R7:[ER8]
MOV ER0,ER10
MOV ER2,#0x00
CMP ER0,ER2
BNE near_67
JMP match_missing
near_67:
MOV ER12,ER14
ADD ER12,#0x3F
ADD ER12,#0x11
mnemonic_char:
L R0,R7:[ER10]
L R1,0x00:[ER12]
CMP R0,#0x20
BEQ mnemonic_end
CMP R0,#0x00
BEQ mnemonic_end
CMP R0,R1
BEQ near_68
JMP candidate_next
near_68:
ADD ER10,#0x01
ADD ER12,#0x01
JMP mnemonic_char
mnemonic_end:
CMP R1,#0x00
BEQ near_69
JMP candidate_next
near_69:
L ER0,R7:0x0002[ER8]
ST ER0,0x00:0x0020[ER14]
L ER0,0x00:0x0022[ER14]
ST ER0,0x00:0x000A[ER14]
MOV R0,#0x00
ST R0,0x00:0x0024[ER14]
MOV R0,#0xFF
ST R0,0x00:0x0047[ER14]
grammar_token:
L ER8,0x00:0x0020[ER14]
MOV R7,#0x0F
L R0,R7:[ER8]
ADD ER8,#0x01
ST ER8,0x00:0x0020[ER14]
ST R0,0x00:0x006F[ER14]
CMP R0,#0x00
BNE near_70
JMP grammar_end
near_70:
CMP R0,#0x20
BLT grammar_control
MOV R6,R0
CALL literal
JMP grammar_token
grammar_control:
CMP R0,#0x0D
BNE near_71
JMP segment
near_71:
CMP R0,#0x05
BGE numeric_operand
CALL spaces
L R0,0x00:0x006F[ER14]
CMP R0,#0x01
BEQ register_r
MOV R6,#0x45
CMP R0,#0x02
BEQ register_prefix
MOV R6,#0x58
CMP R0,#0x03
BEQ register_prefix
MOV R6,#0x51
register_prefix:
CALL literal
register_r:
MOV R6,#0x52
CALL literal
MOV R0,#0x00
ST R0,0x00:0x003F[ER14]
CALL decimal
CMP R2,#0x00
BEQ near_72
JMP operand_fail
near_72:
CMP R1,#0x00
BEQ near_73
JMP operand_fail
near_73:
L R6,0x00:0x003F[ER14]
CMP R6,#0x00
BEQ near_74
JMP operand_fail
near_74:
CMP R0,#0x10
BLT near_75
JMP operand_fail
near_75:
ST R0,0x00:0x003A[ER14]
L R1,0x00:0x006F[ER14]
CMP R1,#0x02
BNE near_76
AND R0,#0x01
BEQ near_76
JMP operand_fail
near_76:
register_not_2:
CMP R1,#0x03
BNE near_77
AND R0,#0x03
BEQ near_77
JMP operand_fail
near_77:
register_not_3:
CMP R1,#0x04
BNE near_78
AND R0,#0x07
BEQ near_78
JMP operand_fail
near_78:
register_not_4:
L R0,0x00:0x003A[ER14]
CALL nibble
JMP grammar_token
numeric_operand:
CALL number
ST ER0,0x00:0x003A[ER14]
ST R2,0x00:0x003C[ER14]
L R6,0x00:0x006F[ER14]
CMP R6,#0x0B
BNE near_79
JMP target_operand
near_79:
CMP R6,#0x07
BEQ unsigned_twenty
CMP R2,#0x00
BEQ near_80
JMP operand_fail
near_80:
CMP R6,#0x08
BLT unsigned_operand
CMP R6,#0x0B
BLT signed_operand
unsigned_operand:
L R2,0x00:0x003E[ER14]
CMP R2,#0x00
BEQ near_81
JMP operand_fail
near_81:
CMP R6,#0x06
BNE near_82
JMP pack_four
near_82:
CMP R1,#0x00
BEQ near_83
JMP operand_fail
near_83:
CMP R6,#0x0C
BNE pack_two
CMP R0,#0x08
BLT near_84
JMP operand_fail
near_84:
CALL nibble
JMP grammar_token
unsigned_twenty:
L R3,0x00:0x0039[ER14]
CMP R3,#0x00
BEQ near_85
JMP operand_fail
near_85:
L R3,0x00:0x003E[ER14]
CMP R3,#0x00
BEQ near_86
JMP operand_fail
near_86:
MOV R0,R2
CALL nibble
JMP pack_four
signed_operand:
MOV R4,#0x00
MOV R5,#0x80
CMP R6,#0x0A
BEQ signed_limit
MOV R4,#0x80
MOV R5,#0x00
CMP R6,#0x09
BEQ signed_limit
MOV R4,#0x40
MOV R5,#0x00
signed_limit:
L R2,0x00:0x003E[ER14]
CMP R2,#0x00
BEQ signed_positive
CMP ER0,ER4
BLT near_87
JMP signed_equal
near_87:
JMP near_88
signed_equal:
BEQ near_88
JMP operand_fail
near_88:
signed_negate:
MOV ER2,ER0
MOV ER0,#0x00
SUB R0,R2
SUBC R1,R3
JMP near_89
signed_positive:
L R2,0x00:0x003F[ER14]
CMP R2,#0x00
BEQ signed_compare
ADD ER4,ER4
CMP R6,#0x0A
BEQ near_89
signed_compare:
CMP ER0,ER4
BLT near_89
JMP operand_fail
near_89:
signed_ready:
CMP R6,#0x08
BNE signed_store
AND R0,#0x7F
signed_store:
ST ER0,0x00:0x003A[ER14]
CMP R6,#0x0A
BEQ pack_four
pack_two:
MOV R0,#0x02
ST R0,0x00:0x0071[ER14]
JMP pack_number
pack_four:
MOV R0,#0x04
ST R0,0x00:0x0071[ER14]
pack_number:
L R0,0x00:0x0071[ER14]
CMP R0,#0x04
BNE pack_low
L R0,0x00:0x003B[ER14]
CALL pack_byte
pack_low:
L R0,0x00:0x003A[ER14]
CALL pack_byte
JMP grammar_token
target_operand:
L R3,0x00:0x003E[ER14]
CMP R3,#0x00
BEQ near_90
JMP operand_fail
near_90:
CMP R2,#0x00
BEQ near_91
L R3,0x00:0x007C[ER14]
CMP R2,R3
BEQ near_91
JMP operand_fail
near_91:
target_ready:
L R3,0x00:0x0039[ER14]
CMP R3,#0x02
BNE target_known
L ER0,0x00:0x0014[ER14]
ST ER0,0x00:0x003A[ER14]
target_known:
CALL even_address
JMP pack_four
segment:
L ER0,0x00:0x000A[ER14]
ST ER0,0x00:0x0072[ER14]
CALL spaces
CMP R0,#0x5B
BEQ segment_absent
CALL number
ST ER0,0x00:0x0074[ER14]
ST R2,0x00:0x0070[ER14]
CALL spaces
CMP R0,#0x3A
BNE segment_absent
CALL get
L ER0,0x00:0x0074[ER14]
L R2,0x00:0x0070[ER14]
CMP R2,#0x00
BEQ near_92
JMP operand_fail
near_92:
L R2,0x00:0x003E[ER14]
CMP R2,#0x00
BEQ near_93
JMP operand_fail
near_93:
CMP R1,#0x00
BEQ near_94
JMP operand_fail
near_94:
CMP R0,#0x10
BLT near_95
JMP operand_fail
near_95:
ST R0,0x00:0x0047[ER14]
JMP grammar_token
segment_absent:
L ER0,0x00:0x0072[ER14]
ST ER0,0x00:0x000A[ER14]
JMP grammar_token
grammar_end:
CALL line_tail
L ER8,0x00:0x001E[ER14]
MOV R7,#0x0F
L ER2,R7:0x0004[ER8]
CMP R2,#0x00
BNE near_96
CMP R3,#0x00
BNE near_96
JMP mov_word
near_96:
catalogue_encode:
MOV R7,#0x08
L R0,R7:[ER2]
CMP R0,#0x0A
BEQ reorder_displacement
CMP R0,#0x0D
BEQ reorder_displacement
JMP encode_ready
reorder_displacement:
L R6,0x00:0x0045[ER14]
L R0,0x00:0x0044[ER14]
ST R0,0x00:0x0045[ER14]
L R0,0x00:0x0043[ER14]
ST R0,0x00:0x0044[ER14]
L R0,0x00:0x0042[ER14]
ST R0,0x00:0x0043[ER14]
L R0,0x00:0x0041[ER14]
ST R0,0x00:0x0042[ER14]
ST R6,0x00:0x0041[ER14]
encode_ready:
ST ER2,0x00:0x0074[ER14]
L ER0,0x00:0x0014[ER14]
MOV ER4,ER14
ADD ER4,#0x3F
ADD ER4,#0x01
MOV ER6,ER14
ADD ER6,#0x3F
ADD ER6,#0x09
CALL codec_encode_address
CMP R0,#0x00
BEQ encoded
CMP R0,#0x04
BNE codec_operand
MOV ER0,#0x04
ST ER0,0x00:0x001A[ER14]
JMP operand_fail
codec_operand:
CMP R0,#0x03
BNE operand_fail
MOV ER0,#0x05
ST ER0,0x00:0x001A[ER14]
JMP operand_fail
encoded:
ST R2,0x00:0x0026[ER14]
L ER2,0x00:0x0074[ER14]
MOV R7,#0x08
L R0,R7:[ER2]
CMP R0,#0x0F
BNE match_done
L R0,0x00:0x007C[ER14]
OR R0,#0xF0
ST R0,0x00:0x0049[ER14]
match_done:
MOV R0,#0x00
ST R0,0x00:0x006C[ER14]
POP PC
mov_word:
L R0,0x00:0x0043[ER14]
L R1,0x00:0x0044[ER14]
SLL R0,#0x04
OR R0,R1
ST R0,0x00:0x0048[ER14]
L R0,0x00:0x0041[ER14]
L R1,0x00:0x0042[ER14]
SLL R0,#0x04
OR R0,R1
ST R0,0x00:0x004A[ER14]
L R0,0x00:0x0040[ER14]
ST R0,0x00:0x0049[ER14]
ADD R0,#0x01
ST R0,0x00:0x004B[ER14]
MOV R0,#0x04
ST R0,0x00:0x0026[ER14]
JMP match_done
operand_fail:
L R0,0x00:0x006C[ER14]
CMP R0,#0x00
BNE near_97
JMP bad_operand
near_97:
L ER0,0x00:0x001C[ER14]
MOV SP,ER0
candidate_next:
L ER0,0x00:0x001E[ER14]
ADD ER0,#0x06
ST ER0,0x00:0x001E[ER14]
JMP candidate
match_missing:
MOV R0,#0x00
ST R0,0x00:0x006C[ER14]
JMP failure
literal:
PUSH LR
CALL spaces
CALL get
CALL upper
CMP R0,R6
BEQ near_98
JMP operand_fail
near_98:
POP PC
nibble:
L R2,0x00:0x0024[ER14]
MOV R3,#0x00
MOV ER4,ER14
ADD ER4,#0x3F
ADD ER4,#0x01
ADD ER4,ER2
ST R0,0x00:[ER4]
ADD R2,#0x01
ST R2,0x00:0x0024[ER14]
RET
pack_byte:
PUSH LR
ST R0,0x00:0x0070[ER14]
SRL R0,#0x04
CALL nibble
L R0,0x00:0x0070[ER14]
AND R0,#0x0F
CALL nibble
POP PC
