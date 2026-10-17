; codec_encode
; Return independent encoder and length/prefix/SUB clusters.
; CPU 0x808E0, physical 0x008E0, 1536 bytes

codec_encode:
PUSH LR
PUSH XR4
PUSH QR8
MOV ER8,ER0
MOV ER10,ER2
MOV ER12,ER4
ADD SP,#0xE0
ADD SP,#0xE0
ADD SP,#0xE0
MOV ER14,SP
MOV ER2,ER14
ADD ER2,#0x22
ST R6,[ER2]
ADD ER2,#0x01
ST R7,[ER2]
MOV ER2,ER14
ADD ER2,#0x24
ST R8,[ER2]
ADD ER2,#0x01
ST R9,[ER2]
MOV R0,#0x00
MOV ER2,ER14
ADD ER2,#0x26
ST R0,[ER2]
MOV R0,R8
AND R0,#0x01
BEQ skip_1
JMP enc_odd
skip_1:
MOV ER0,ER10
MOV R2,#0x3C
MOV R3,#0x11
CMP ER0,ER2
BGE skip_2
JMP enc_operand
skip_2:
MOV R2,#0xDC
MOV R3,#0x16
CMP ER0,ER2
BLT skip_3
JMP enc_operand
skip_3:
ADD R0,#0xF4
AND R0,#0x0F
BEQ skip_4
JMP enc_operand
skip_4:
L R0,0x08:[ER10]
MOV ER2,ER14
ADD ER2,#0x29
ST R0,[ER2]
ADD ER10,#0x02
L R0,0x08:[ER10]
MOV ER2,ER14
ADD ER2,#0x2A
ST R0,[ER2]
ADD ER10,#0x01
L R0,0x08:[ER10]
MOV ER2,ER14
ADD ER2,#0x2F
ST R0,[ER2]
ADD ER10,#0x01
MOV ER8,ER14
ADD ER8,#0x20
ADD ER8,#0x20
MOV R6,#0x00
enc_fields:
L R0,0x00:[ER12]
ST R0,0x00:[ER8]
CMP R6,#0x07
BNE skip_5
JMP enc_fields_done
skip_5:
L R7,0x08:[ER10]
CMP R7,#0x00
BNE skip_6
JMP skip_15
skip_6:
CMP R0,#0x10
BLT skip_7
JMP enc_operand
skip_7:
CMP R7,#0x02
BEQ skip_8
JMP skip_9
skip_8:
AND R0,#0x01
BEQ skip_9
JMP enc_operand
skip_9:
enc_not_er:
CMP R7,#0x03
BEQ skip_10
JMP skip_11
skip_10:
CMP R0,#0x08
BLT skip_11
JMP enc_operand
skip_11:
enc_not_bit:
CMP R7,#0x05
BEQ skip_12
JMP skip_13
skip_12:
AND R0,#0x03
BEQ skip_13
JMP enc_operand
skip_13:
enc_not_xr:
CMP R7,#0x06
BEQ skip_14
JMP skip_15
skip_14:
AND R0,#0x07
BEQ skip_15
JMP enc_operand
skip_15:
enc_field_next:
ADD ER8,#0x01
ADD ER10,#0x01
ADD ER12,#0x01
ADD R6,#0x01
JMP enc_fields
enc_fields_done:
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x20
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x2D
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x21
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x2E
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x29
L R0,[ER2]
CMP R0,#0x03
BEQ skip_16
JMP skip_17
skip_16:
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x21
L R0,[ER2]
CMP R0,#0x08
BLT skip_17
JMP enc_operand
skip_17:
enc_target:
MOV ER2,ER14
ADD ER2,#0x29
L R0,[ER2]
CMP R0,#0x0E
BEQ skip_18
JMP enc_far_check
skip_18:
CALL branch_target
CMP R0,#0x00
BEQ skip_19
JMP enc_failed
skip_19:
JMP skip_23
enc_far_check:
CMP R0,#0x0F
BEQ skip_20
JMP enc_sys_check
skip_20:
MOV R0,#0x00
CALL pack
MOV R9,R0
MOV R0,#0x02
CALL pack
MOV R8,R0
AND R0,#0x01
BEQ skip_21
JMP enc_odd
skip_21:
JMP skip_23
enc_sys_check:
CMP R0,#0x10
BEQ skip_22
JMP skip_23
skip_22:
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x24
L R0,[ER2]
AND R0,#0x01
BEQ skip_23
JMP enc_odd
skip_23:
enc_assemble:
CALL assemble
MOV R9,#0x02
MOV ER2,ER14
ADD ER2,#0x29
L R0,[ER2]
CMP R0,#0x17
BEQ skip_24
JMP enc_size_normal
skip_24:
MOV R9,#0x08
JMP enc_segment
enc_size_normal:
CMP R0,#0x08
BNE skip_25
JMP enc_size_four
skip_25:
CMP R0,#0x0A
BNE skip_26
JMP enc_size_four
skip_26:
CMP R0,#0x0B
BNE skip_27
JMP enc_size_four
skip_27:
CMP R0,#0x0D
BNE skip_28
JMP enc_size_four
skip_28:
CMP R0,#0x0F
BNE skip_29
JMP enc_size_four
skip_29:
CMP R0,#0x10
BNE skip_30
JMP enc_size_four
skip_30:
JMP enc_segment
enc_size_four:
MOV R9,#0x04
enc_segment:
MOV ER2,ER14
ADD ER2,#0x29
L R0,[ER2]
CMP R0,#0x08
BGE skip_31
JMP enc_copy
skip_31:
CMP R0,#0x0E
BLT skip_32
JMP enc_copy
skip_32:
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x27
L R0,[ER2]
CMP R0,#0xFF
BNE skip_33
JMP enc_copy
skip_33:
CMP R0,#0x10
BLT skip_34
JMP enc_operand
skip_34:
MOV ER2,ER14
ADD ER2,#0x37
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x39
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x36
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x38
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x35
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x37
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x34
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x36
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x27
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x34
ST R0,[ER2]
MOV R0,#0xE3
MOV ER2,ER14
ADD ER2,#0x35
ST R0,[ER2]
ADD R9,#0x02
enc_copy:
MOV ER2,ER14
ADD ER2,#0x24
L R0,[ER2]
ADD ER2,#0x01
L R1,[ER2]
MOV R2,R9
MOV R3,#0x00
ADD ER0,ER2
BGE skip_35
MOV ER0,ER0
BEQ skip_35
JMP enc_outside
skip_35:
enc_copy_ready:
MOV ER2,ER14
ADD ER2,#0x22
L R10,[ER2]
ADD ER2,#0x01
L R11,[ER2]
MOV R5,R9
MOV ER8,ER14
ADD ER8,#0x34
MOV R6,R5
enc_copy_byte:
L R0,0x00:[ER8]
ST R0,0x00:[ER10]
ADD ER8,#0x01
ADD ER10,#0x01
ADD R6,#0xFF
CMP R6,#0x00
BEQ skip_36
JMP enc_copy_byte
skip_36:
MOV R2,R5
MOV ER0,#0x00
JMP enc_exit
enc_operand:
MOV R0,#0x01
JMP enc_failed
enc_odd:
MOV R0,#0x02
JMP enc_failed
enc_outside:
MOV R0,#0x03
JMP enc_failed
enc_failed:
MOV R1,#0x00
MOV R2,#0x00
enc_exit:
ADD SP,#0x20
ADD SP,#0x20
ADD SP,#0x20
POP QR8
POP XR4
POP PC
pack:
MOV R6,R0
MOV R7,#0x00
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x20
ADD ER2,ER6
L R8,[ER2]
SLL R8,#0x04
ADD R6,#0x01
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x20
ADD ER2,ER6
L R0,[ER2]
OR R0,R8
RET
branch_target:
PUSH LR
MOV R0,#0x00
CALL pack
MOV ER2,ER14
ADD ER2,#0x30
ST R0,[ER2]
MOV R0,#0x02
CALL pack
MOV R8,R0
MOV ER2,ER14
ADD ER2,#0x30
L R9,[ER2]
MOV R0,R8
AND R0,#0x01
BEQ skip_37
JMP branch_odd
skip_37:
MOV ER2,ER14
ADD ER2,#0x24
L R0,[ER2]
ADD ER2,#0x01
L R1,[ER2]
MOV ER2,ER14
ADD ER2,#0x26
L R6,[ER2]
ADD R0,R6
ADDC R1,#0x00
ADD ER0,#0x02
SUB R8,R0
SUBC R9,R1
CMP R9,#0x00
BNE skip_38
JMP branch_forward
skip_38:
CMP R9,#0xFF
BEQ skip_39
JMP branch_range
skip_39:
SRL R8,#0x01
OR R8,#0x80
JMP branch_ready
branch_forward:
CMP R8,#0xFF
BNE skip_40
JMP branch_range
skip_40:
SRL R8,#0x01
branch_ready:
MOV ER2,ER14
ADD ER2,#0x30
ST R8,[ER2]
MOV R0,#0x00
POP PC
branch_odd:
MOV R0,#0x02
JMP branch_fail
branch_range:
MOV R0,#0x04
branch_fail:
MOV ER2,ER14
ADD ER2,#0x30
ST R0,[ER2]
POP PC
assemble:
PUSH LR
MOV ER2,ER14
ADD ER2,#0x2A
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x34
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x2F
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x35
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x29
L R6,[ER2]
CMP R6,#0x00
BNE skip_41
JMP asm_imm
skip_41:
CMP R6,#0x17
BNE skip_42
JMP asm_sub_imm
skip_42:
CMP R6,#0x01
BNE skip_43
JMP asm_pair
skip_43:
CMP R6,#0x02
BNE skip_44
JMP asm_pair
skip_44:
CMP R6,#0x03
BNE skip_45
JMP asm_ei7
skip_45:
CMP R6,#0x04
BNE skip_46
JMP asm_shift
skip_46:
CMP R6,#0x05
BNE skip_47
JMP asm_er_r
skip_47:
CMP R6,#0x06
BNE skip_48
JMP asm_one
skip_48:
CMP R6,#0x07
BNE skip_49
JMP asm_one
skip_49:
CMP R6,#0x18
BNE skip_50
JMP asm_one
skip_50:
CMP R6,#0x19
BNE skip_51
JMP asm_one
skip_51:
CMP R6,#0x08
BNE skip_52
JMP asm_abs
skip_52:
CMP R6,#0x0B
BNE skip_53
JMP asm_abs
skip_53:
CMP R6,#0x09
BNE skip_54
JMP asm_pair
skip_54:
CMP R6,#0x0C
BNE skip_55
JMP asm_pair
skip_55:
CMP R6,#0x0A
BNE skip_56
JMP asm_disp
skip_56:
CMP R6,#0x0D
BNE skip_57
JMP asm_disp
skip_57:
CMP R6,#0x0E
BNE skip_58
JMP asm_branch
skip_58:
CMP R6,#0x0F
BNE skip_59
JMP asm_far
skip_59:
CMP R6,#0x10
BNE skip_60
JMP asm_sys
skip_60:
CMP R6,#0x11
BNE skip_61
JMP asm_shift
skip_61:
CMP R6,#0x12
BNE skip_62
JMP asm_sp_imm
skip_62:
CMP R6,#0x14
BNE skip_63
JMP asm_extbw
skip_63:
CMP R6,#0x15
BNE skip_64
JMP asm_one
skip_64:
CMP R6,#0x16
BNE skip_65
JMP asm_sp_er
skip_65:
JMP asm_done
asm_imm:
MOV ER2,ER14
ADD ER2,#0x2D
L R7,[ER2]
MOV ER2,ER14
ADD ER2,#0x35
L R0,[ER2]
OR R0,R7
MOV ER2,ER14
ADD ER2,#0x35
ST R0,[ER2]
MOV R0,#0x01
JMP asm_pack_imm
asm_sp_imm:
MOV R0,#0x00
asm_pack_imm:
CALL pack
MOV ER2,ER14
ADD ER2,#0x34
ST R0,[ER2]
JMP asm_done
asm_sub_imm:
MOV R0,#0x01
CALL pack
MOV ER2,ER14
ADD ER2,#0x36
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x2D
L R7,[ER2]
CMP R7,#0x00
BEQ skip_66
JMP sub_tmp_zero
skip_66:
MOV R6,#0x01
JMP sub_tmp_ready
sub_tmp_zero:
MOV R6,#0x00
sub_tmp_ready:
MOV R0,#0x4E
MOV ER2,ER14
ADD ER2,#0x34
ST R0,[ER2]
MOV R0,R6
OR R0,#0xF0
MOV ER2,ER14
ADD ER2,#0x35
ST R0,[ER2]
MOV R0,R6
MOV ER2,ER14
ADD ER2,#0x37
ST R0,[ER2]
MOV R0,R6
SLL R0,#0x04
OR R0,#0x08
MOV ER2,ER14
ADD ER2,#0x38
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x2D
L R0,[ER2]
OR R0,#0x80
MOV ER2,ER14
ADD ER2,#0x39
ST R0,[ER2]
MOV R0,#0x0E
MOV ER2,ER14
ADD ER2,#0x3A
ST R0,[ER2]
MOV R0,R6
OR R0,#0xF0
MOV ER2,ER14
ADD ER2,#0x3B
ST R0,[ER2]
JMP asm_done
asm_pair:
CALL asm_dest
MOV ER2,ER14
ADD ER2,#0x2A
L R7,[ER2]
MOV ER2,ER14
ADD ER2,#0x2E
L R0,[ER2]
SLL R0,#0x04
OR R7,R0
MOV ER2,ER14
ADD ER2,#0x34
ST R7,[ER2]
JMP asm_done
asm_ei7:
CALL asm_dest
MOV R0,#0x01
CALL pack
OR R0,#0x80
MOV ER2,ER14
ADD ER2,#0x34
ST R0,[ER2]
JMP asm_done
asm_shift:
CALL asm_dest
MOV ER2,ER14
ADD ER2,#0x2A
L R7,[ER2]
MOV ER2,ER14
ADD ER2,#0x2E
L R0,[ER2]
SLL R0,#0x04
OR R7,R0
MOV ER2,ER14
ADD ER2,#0x34
ST R7,[ER2]
JMP asm_done
asm_er_r:
CALL asm_dest
MOV ER2,ER14
ADD ER2,#0x2A
L R7,[ER2]
MOV ER2,ER14
ADD ER2,#0x2E
L R0,[ER2]
SLL R0,#0x04
OR R7,R0
MOV ER2,ER14
ADD ER2,#0x34
ST R7,[ER2]
JMP asm_done
asm_one:
CALL asm_dest
JMP asm_done
asm_sp_er:
MOV ER2,ER14
ADD ER2,#0x2A
L R7,[ER2]
MOV ER2,ER14
ADD ER2,#0x2D
L R0,[ER2]
SLL R0,#0x04
OR R7,R0
MOV ER2,ER14
ADD ER2,#0x34
ST R7,[ER2]
JMP asm_done
asm_extbw:
CALL asm_dest
JMP asm_sp_er
asm_abs:
CALL asm_dest
MOV R0,#0x01
JMP asm_word
asm_disp:
CALL asm_dest
MOV ER2,ER14
ADD ER2,#0x2A
L R7,[ER2]
MOV ER2,ER14
ADD ER2,#0x2E
L R0,[ER2]
SLL R0,#0x04
OR R7,R0
MOV ER2,ER14
ADD ER2,#0x34
ST R7,[ER2]
MOV R0,#0x02
asm_word:
MOV R9,R0
CALL pack
MOV ER2,ER14
ADD ER2,#0x37
ST R0,[ER2]
MOV R0,R9
ADD R0,#0x02
CALL pack
MOV ER2,ER14
ADD ER2,#0x36
ST R0,[ER2]
JMP asm_done
asm_branch:
MOV ER2,ER14
ADD ER2,#0x30
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x34
ST R0,[ER2]
JMP asm_done
asm_far:
MOV R0,#0x00
JMP asm_word
asm_sys:
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x20
L R0,[ER2]
OR R0,#0xF0
MOV ER2,ER14
ADD ER2,#0x35
ST R0,[ER2]
MOV R0,#0x01
JMP asm_word
asm_dest:
MOV ER2,ER14
ADD ER2,#0x2D
L R7,[ER2]
MOV ER2,ER14
ADD ER2,#0x2F
L R0,[ER2]
OR R0,R7
MOV ER2,ER14
ADD ER2,#0x35
ST R0,[ER2]
RET
asm_done:
POP PC
