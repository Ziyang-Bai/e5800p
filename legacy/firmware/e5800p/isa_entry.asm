; isa_entry
; Return the picker payload at its layout-owned Flash address.
; CPU 0xF7E68, physical 0x77E68, 3324 bytes
hex_key_address EQU 0x825CA
codec_source_length_address EQU 0x80444
codec_length_address EQU 0x80440
codec_encode_address EQU 0x808E0
rom_refresh EQU 0x043BE
rom_draw_text EQU 0x041DA
ui_text_address EQU 0x81E06

isa_entry:
entry:
PUSH LR
PUSH XR4
PUSH ER6
PUSH QR8
PUSH ER12
PUSH ER14
MOV ER8,ER6
MOV ER10,ER0
MOV R7,R5
MOV ER12,ER2
ADD SP,#0xE0
ADD SP,#0xE0
ADD SP,#0xE0
MOV ER14,SP
MOV ER2,ER14
ADD ER2,#0x20
ST R10,[ER2]
ADD ER2,#0x01
ST R11,[ER2]
MOV ER2,ER14
ADD ER2,#0x22
ST R8,[ER2]
ADD ER2,#0x01
ST R9,[ER2]
MOV ER2,ER14
ADD ER2,#0x24
ST R12,[ER2]
ADD ER2,#0x01
ST R13,[ER2]
MOV ER2,ER14
ADD ER2,#0x26
ST R7,[ER2]
MOV R0,#0x00
MOV ER2,ER14
ADD ER2,#0x31
ST R0,[ER2]
MOV R0,#0x00
MOV ER2,ER14
ADD ER2,#0x2D
ST R0,[ER2]
MOV R0,#0x00
MOV ER2,ER14
ADD ER2,#0x2E
ST R0,[ER2]
MOV R0,#0x00
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x20
ST R0,[ER2]
MOV R0,#0x00
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x21
ST R0,[ER2]
MOV R0,#0x00
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x22
ST R0,[ER2]
MOV R0,#0x00
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x23
ST R0,[ER2]
MOV R0,#0x00
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x24
ST R0,[ER2]
MOV R0,#0x00
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x25
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x26
L R0,[ER2]
CMP R0,#0x10
BLT skip_1
JMP cancel
skip_1:
MOV ER2,ER14
ADD ER2,#0x26
L R0,[ER2]
AND R0,#0x01
BEQ skip_2
JMP cancel
skip_2:
categories:
CALL draw_categories
CALL key
CMP R0,#0xFA
BNE skip_3
JMP cancel
skip_3:
CMP R0,#0x31
BGE skip_4
JMP skip_2
skip_4:
CMP R0,#0x37
BLT skip_5
JMP skip_2
skip_5:
ADD R0,#0xCF
MOV ER2,ER14
ADD ER2,#0x27
ST R0,[ER2]
MOV R0,#0x00
MOV ER2,ER14
ADD ER2,#0x3C
ST R0,[ER2]
JMP browse
browse:
CALL draw_menu
CALL key
CMP R0,#0xFA
BNE skip_6
JMP skip_2
skip_6:
CMP R0,#0xFC
BNE skip_7
JMP page_left
skip_7:
CMP R0,#0xFD
BNE skip_8
JMP page_right
skip_8:
CMP R0,#0x31
BGE skip_9
JMP browse
skip_9:
CMP R0,#0x35
BLT skip_10
JMP browse
skip_10:
ADD R0,#0xCF
MOV ER2,ER14
ADD ER2,#0x3C
L R8,[ER2]
ADD R0,R8
MOV R8,R0
CALL item_count
MOV R0,R8
CMP R0,R7
BLT skip_11
JMP browse
skip_11:
MOV ER2,ER14
ADD ER2,#0x28
ST R0,[ER2]
JMP selected
page_left:
MOV ER2,ER14
ADD ER2,#0x3C
L R0,[ER2]
CMP R0,#0x04
BGE skip_12
JMP page_end
skip_12:
ADD R0,#0xFC
JMP skip_13
page_right:
MOV ER2,ER14
ADD ER2,#0x3C
L R0,[ER2]
ADD R0,#0x04
MOV R8,R0
CALL item_count
MOV R0,R8
CMP R0,R7
BLT skip_13
JMP page_begin
skip_13:
page_store:
MOV ER2,ER14
ADD ER2,#0x3C
ST R0,[ER2]
JMP browse
page_begin:
MOV R0,#0x00
JMP skip_13
page_end:
CALL item_count
MOV R0,R7
ADD R0,#0xFF
AND R0,#0xFC
JMP skip_13
selected:
CALL record
MOV ER2,ER14
ADD ER2,#0x29
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x2A
L R1,[ER2]
MOV R0,#0x00
MOV ER2,ER14
ADD ER2,#0x31
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x2D
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x2E
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x34
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x35
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x36
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x37
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x20
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x21
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x22
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x23
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x24
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x25
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x26
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x27
ST R0,[ER2]
MOV R0,#0xFF
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x27
ST R0,[ER2]
CALL old_length
MOV ER2,ER14
ADD ER2,#0x2B
ST R0,[ER2]
operand:
CALL field_kind
CMP R0,#0x00
BNE skip_14
JMP segment
skip_14:
MOV ER2,ER14
ADD ER2,#0x32
ST R0,[ER2]
CALL draw_operand
operand_key:
CALL key
CMP R0,#0xFA
BNE skip_15
JMP browse
skip_15:
CMP R0,#0xFC
BNE skip_16
JMP operand_prev
skip_16:
CMP R0,#0xFD
BNE skip_17
JMP operand_next
skip_17:
CMP R0,#0xFE
BNE skip_18
JMP operand_down
skip_18:
CMP R0,#0xFF
BNE skip_19
JMP operand_up
skip_19:
CMP R0,#0xFB
BNE skip_20
JMP operand_next
skip_20:
CMP R0,#0x30
BGE skip_21
JMP operand_key
skip_21:
CMP R0,#0x3A
BLT skip_22
JMP operand_letter
skip_22:
ADD R0,#0xD0
JMP operand_digit
operand_letter:
CMP R0,#0x41
BGE skip_23
JMP operand_key
skip_23:
CMP R0,#0x47
BLT skip_24
JMP operand_key
skip_24:
ADD R0,#0xC9
operand_digit:
CALL set_field
CMP R0,#0x00
BEQ skip_25
JMP operand_key
skip_25:
MOV ER2,ER14
ADD ER2,#0x31
L R0,[ER2]
ADD R0,#0x01
MOV ER2,ER14
ADD ER2,#0x31
ST R0,[ER2]
CALL field_kind
CMP R0,#0x00
BEQ skip_26
JMP operand
skip_26:
MOV ER2,ER14
ADD ER2,#0x31
L R0,[ER2]
ADD R0,#0xFF
MOV ER2,ER14
ADD ER2,#0x31
ST R0,[ER2]
CALL draw_operand
JMP operand_key
operand_down:
MOV R1,#0xFF
JMP operand_change
operand_up:
MOV R1,#0x01
operand_change:
CALL change_field
CALL draw_operand
JMP operand_key
operand_prev:
MOV ER2,ER14
ADD ER2,#0x31
L R0,[ER2]
CMP R0,#0x00
BNE skip_27
JMP operand_key
skip_27:
ADD R0,#0xFF
MOV ER2,ER14
ADD ER2,#0x31
ST R0,[ER2]
JMP operand
operand_next:
MOV ER2,ER14
ADD ER2,#0x31
L R0,[ER2]
ADD R0,#0x01
MOV ER2,ER14
ADD ER2,#0x31
ST R0,[ER2]
JMP operand
segment:
MOV ER2,ER14
ADD ER2,#0x29
L R0,[ER2]
CMP R0,#0x08
BGE skip_28
JMP encode
skip_28:
CMP R0,#0x0E
BLT skip_29
JMP encode
skip_29:
segment_draw:
CALL draw_segment
segment_key:
CALL key
CMP R0,#0xFA
BNE skip_30
JMP browse
skip_30:
CMP R0,#0xFB
BNE skip_31
JMP encode
skip_31:
CMP R0,#0x49
CMPC R1,#0x75
BNE skip_32
JMP segment_clear
skip_32:
CMP R0,#0x30
BGE skip_33
JMP segment_key
skip_33:
CMP R0,#0x3A
BLT skip_34
JMP segment_letter
skip_34:
ADD R0,#0xD0
JMP segment_store
segment_letter:
CMP R0,#0x41
BGE skip_35
JMP segment_key
skip_35:
CMP R0,#0x47
BLT skip_36
JMP segment_key
skip_36:
ADD R0,#0xC9
JMP segment_store
segment_clear:
MOV R0,#0xFF
segment_store:
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x27
ST R0,[ER2]
JMP skip_29
encode:
CALL assemble
CMP R0,#0x00
BEQ skip_37
JMP bad_target
skip_37:
CALL draw_result
confirm:
CALL key
CMP R0,#0xFA
BNE skip_38
JMP browse
skip_38:
CMP R0,#0xFC
BNE skip_39
JMP result_back
skip_39:
CMP R0,#0xFB
BNE skip_40
JMP commit
skip_40:
JMP confirm
result_back:
MOV ER2,ER14
ADD ER2,#0x31
L R0,[ER2]
CMP R0,#0x00
BNE skip_41
JMP confirm
skip_41:
ADD R0,#0xFF
MOV ER2,ER14
ADD ER2,#0x31
ST R0,[ER2]
JMP operand
bad_target:
CALL draw_bad_target
bad_target_key:
CALL key
CMP R0,#0x00
BNE skip_42
JMP bad_target_key
skip_42:
MOV ER2,ER14
ADD ER2,#0x31
L R0,[ER2]
ADD R0,#0xFF
MOV ER2,ER14
ADD ER2,#0x31
ST R0,[ER2]
JMP operand
commit:
MOV ER2,ER14
ADD ER2,#0x22
L R8,[ER2]
ADD ER2,#0x01
L R9,[ER2]
MOV ER2,ER14
ADD ER2,#0x2B
L R0,[ER2]
ST R0,[ER8]
ADD ER8,#0x01
MOV ER2,ER14
ADD ER2,#0x2C
L R0,[ER2]
ST R0,[ER8]
ADD ER8,#0x01
MOV R7,#0x08
MOV ER2,ER14
ADD ER2,#0x34
commit_loop:
L R0,[ER2]
ST R0,[ER8]
ADD ER8,#0x01
ADD ER2,#0x01
ADD R7,#0xFF
CMP R7,#0x00
BEQ skip_43
JMP commit_loop
skip_43:
MOV ER0,#0x00
JMP exit
cancel:
MOV R0,#0xFF
MOV R1,#0xFF
exit:
ADD SP,#0x20
ADD SP,#0x20
ADD SP,#0x20
POP ER14
POP ER12
POP QR8
POP ER6
POP XR4
POP PC
key:
PUSH LR
PUSH ER4
CALL hex_key_address
POP ER4
POP PC
item_count:
MOV R0,#0xDC
MOV R1,#0x16
MOV ER2,ER14
ADD ER2,#0x27
L R6,[ER2]
MOV R7,#0x00
ADD ER0,ER6
L R7,0x08:[ER0]
RET
record:
MOV R0,#0xE2
MOV R1,#0x16
MOV ER2,ER14
ADD ER2,#0x27
L R6,[ER2]
MOV R7,#0x00
ADD ER0,ER6
L R6,0x08:[ER0]
MOV ER2,ER14
ADD ER2,#0x28
L R7,[ER2]
ADD R6,R7
MOV R2,R6
MOV R3,#0x00
MOV R0,#0x10
MUL ER2,R0
MOV R0,#0x3C
MOV R1,#0x11
ADD ER0,ER2
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x2E
ST R0,[ER2]
ADD ER2,#0x01
ST R1,[ER2]
L R6,0x08:[ER0]
ADD ER0,#0x02
L R7,0x08:[ER0]
MOV ER2,ER14
ADD ER2,#0x29
ST R6,[ER2]
MOV ER2,ER14
ADD ER2,#0x2A
ST R7,[ER2]
ADD ER0,#0x01
L R7,0x08:[ER0]
MOV ER2,ER14
ADD ER2,#0x2F
ST R7,[ER2]
ADD ER0,#0x09
L R6,0x08:[ER0]
ADD ER0,#0x01
L R7,0x08:[ER0]
MOV R0,R6
MOV R1,R7
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x30
ST R0,[ER2]
ADD ER2,#0x01
ST R1,[ER2]
MOV ER2,ER14
ADD ER2,#0x29
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x2A
L R1,[ER2]
RET
field_kind:
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x2E
L R0,[ER2]
ADD ER2,#0x01
L R1,[ER2]
ADD ER0,#0x04
MOV ER2,ER14
ADD ER2,#0x31
L R6,[ER2]
MOV R7,#0x00
ADD ER0,ER6
L R0,0x08:[ER0]
RET
set_field:
MOV R1,R0
MOV ER2,ER14
ADD ER2,#0x32
L R7,[ER2]
CMP R7,#0x05
BEQ skip_44
JMP skip_45
skip_44:
AND R0,#0x03
BEQ skip_45
JMP set_invalid
skip_45:
set_not_xr:
CMP R7,#0x06
BEQ skip_46
JMP skip_47
skip_46:
MOV R0,R1
AND R0,#0x07
BEQ skip_47
JMP set_invalid
skip_47:
set_not_qr:
CMP R7,#0x02
BEQ skip_48
JMP skip_49
skip_48:
MOV R0,R1
AND R0,#0x01
BEQ skip_49
JMP set_invalid
skip_49:
set_not_er:
CMP R7,#0x03
BEQ skip_50
JMP skip_51
skip_50:
CMP R1,#0x08
BLT skip_51
JMP set_invalid
skip_51:
set_hex_check:
MOV ER2,ER14
ADD ER2,#0x31
L R6,[ER2]
CMP R7,#0x04
BEQ skip_52
JMP set_register
skip_52:
ADD R6,#0x40
MOV ER2,ER14
ADD ER2,#0x29
L R7,[ER2]
CMP R7,#0x03
BEQ skip_53
JMP skip_55
skip_53:
CMP R6,#0x41
BEQ skip_54
JMP skip_55
skip_54:
CMP R1,#0x08
BLT skip_55
JMP set_invalid
skip_55:
set_far:
CMP R7,#0x0F
BEQ skip_56
JMP skip_58
skip_56:
CMP R6,#0x43
BEQ skip_57
JMP skip_58
skip_57:
MOV R0,R1
AND R0,#0x01
BEQ skip_58
JMP set_invalid
skip_58:
set_even_15:
CMP R7,#0x10
BEQ skip_59
JMP skip_61
skip_59:
CMP R6,#0x44
BEQ skip_60
JMP skip_61
skip_60:
MOV R0,R1
AND R0,#0x01
BEQ skip_61
JMP set_invalid
skip_61:
set_even_16:
CMP R7,#0x0B
BEQ skip_62
JMP skip_64
skip_62:
CMP R6,#0x44
BEQ skip_63
JMP skip_64
skip_63:
MOV R0,R1
AND R0,#0x01
BEQ skip_64
JMP set_invalid
skip_64:
set_even_11:
JMP set_store
set_register:
CMP R6,#0x00
BNE skip_65
JMP set_a
skip_65:
MOV R6,#0x2E
JMP set_store
set_a:
MOV R6,#0x2D
set_store:
MOV R7,#0x00
MOV ER2,ER14
ADD ER2,ER6
ST R1,[ER2]
MOV R0,#0x00
RET
set_invalid:
MOV R0,#0xFF
RET
change_field:
MOV ER2,ER14
ADD ER2,#0x32
L R7,[ER2]
CMP R7,#0x04
BNE skip_66
JMP change_hex
skip_66:
MOV ER2,ER14
ADD ER2,#0x31
L R6,[ER2]
CMP R6,#0x00
BNE skip_67
JMP change_a
skip_67:
MOV R6,#0x2E
JMP change_loaded
change_a:
MOV R6,#0x2D
JMP change_loaded
change_hex:
MOV ER2,ER14
ADD ER2,#0x31
L R6,[ER2]
ADD R6,#0x40
change_loaded:
MOV R7,#0x00
MOV ER2,ER14
ADD ER2,ER6
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x32
L R7,[ER2]
CMP R7,#0x05
BEQ skip_68
JMP change_not_xr
skip_68:
SLL R1,#0x02
JMP change_byte
change_not_xr:
CMP R7,#0x06
BEQ skip_69
JMP change_not_qr
skip_69:
SLL R1,#0x03
JMP change_byte
change_not_qr:
CMP R7,#0x02
BEQ skip_70
JMP change_byte
skip_70:
SLL R1,#0x01
change_byte:
CMP R7,#0x04
BEQ skip_71
JMP change_step_done
skip_71:
MOV ER2,ER14
ADD ER2,#0x29
L R7,[ER2]
CMP R7,#0x0F
BEQ skip_72
JMP skip_73
skip_72:
CMP R6,#0x43
BNE skip_73
JMP skip_77
skip_73:
change_step_sys:
CMP R7,#0x10
BEQ skip_74
JMP skip_75
skip_74:
CMP R6,#0x44
BNE skip_75
JMP skip_77
skip_75:
change_step_abs:
CMP R7,#0x0B
BEQ skip_76
JMP change_step_done
skip_76:
CMP R6,#0x44
BEQ skip_77
JMP change_step_done
skip_77:
change_step_even:
SLL R1,#0x01
change_step_done:
MOV ER2,ER14
ADD ER2,#0x32
L R7,[ER2]
ADD R0,R1
CMP R7,#0x03
BNE skip_78
JMP change_bit
skip_78:
CMP R7,#0x02
BNE skip_79
JMP change_er
skip_79:
CMP R7,#0x05
BNE skip_80
JMP change_xr
skip_80:
CMP R7,#0x06
BNE skip_81
JMP change_qr
skip_81:
AND R0,#0x0F
MOV ER2,ER14
ADD ER2,#0x29
L R7,[ER2]
CMP R7,#0x03
BEQ skip_82
JMP skip_83
skip_82:
CMP R6,#0x41
BNE skip_83
JMP change_seven
skip_83:
change_far:
CMP R7,#0x0F
BEQ skip_84
JMP skip_85
skip_84:
CMP R6,#0x43
BNE skip_85
JMP skip_89
skip_85:
change_sys:
CMP R7,#0x10
BEQ skip_86
JMP skip_87
skip_86:
CMP R6,#0x44
BNE skip_87
JMP skip_89
skip_87:
change_abs_er:
CMP R7,#0x0B
BEQ skip_88
JMP store_field
skip_88:
CMP R6,#0x44
BEQ skip_89
JMP store_field
skip_89:
change_even:
AND R0,#0x0E
JMP store_field
change_seven:
AND R0,#0x07
JMP store_field
change_bit:
AND R0,#0x07
JMP store_field
change_er:
AND R0,#0x0E
JMP store_field
change_xr:
AND R0,#0x0C
JMP store_field
change_qr:
AND R0,#0x08
store_field:
MOV R7,#0x00
MOV ER2,ER14
ADD ER2,ER6
ST R0,[ER2]
RET
old_length:
PUSH LR
PUSH XR4
MOV ER2,ER14
ADD ER2,#0x20
L R0,[ER2]
ADD ER2,#0x01
L R1,[ER2]
MOV ER4,ER0
ADD ER4,#0x10
MOV ER2,ER14
ADD ER2,#0x26
L R6,[ER2]
MOV R7,#0x00
ADD ER0,ER6
MOV R2,#0x00
CALL codec_source_length_address
CMP R1,#0xFF
BEQ skip_90
JMP old_length_done
skip_90:
MOV ER2,ER14
ADD ER2,#0x24
L R0,[ER2]
ADD ER2,#0x01
L R1,[ER2]
MOV ER2,ER14
ADD ER2,#0x26
L R6,[ER2]
MOV R7,#0x00
ADD ER0,ER6
MOV ER2,ER0
CALL codec_length_address
CMP R1,#0xFF
BEQ skip_91
JMP old_length_done
skip_91:
MOV ER0,#0x02
old_length_done:
POP XR4
POP PC
assemble:
PUSH LR
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x2E
L R0,[ER2]
ADD ER2,#0x01
L R1,[ER2]
ADD ER0,#0x04
L R0,0x08:[ER0]
CMP R0,#0x04
BNE skip_92
JMP codec_nibble_0
skip_92:
MOV ER2,ER14
ADD ER2,#0x2D
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x20
ST R0,[ER2]
codec_nibble_0:
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x2E
L R0,[ER2]
ADD ER2,#0x01
L R1,[ER2]
ADD ER0,#0x05
L R0,0x08:[ER0]
CMP R0,#0x04
BNE skip_93
JMP codec_nibble_1
skip_93:
MOV ER2,ER14
ADD ER2,#0x2E
L R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x21
ST R0,[ER2]
codec_nibble_1:
MOV R0,#0x00
MOV ER2,ER14
ADD ER2,#0x34
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x35
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x36
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x37
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x38
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x39
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x3A
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x3B
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x24
L R0,[ER2]
ADD ER2,#0x01
L R1,[ER2]
MOV ER2,ER14
ADD ER2,#0x26
L R6,[ER2]
MOV R7,#0x00
ADD ER0,ER6
MOV ER8,ER0
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x2E
L R0,[ER2]
ADD ER2,#0x01
L R1,[ER2]
MOV ER2,ER0
MOV ER4,ER14
ADD ER4,#0x20
ADD ER4,#0x20
MOV ER6,ER14
ADD ER6,#0x34
MOV ER0,ER8
CALL codec_encode_address
MOV R7,R2
MOV ER2,ER14
ADD ER2,#0x30
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x2C
ST R7,[ER2]
POP PC
draw_segment:
PUSH LR
CALL 0x0:0x409A
CALL old_line
CALL name_line
MOV ER10,ER14
MOV R0,#0x53
ST R0,[ER10]
ADD ER10,#0x01
MOV R0,#0x45
ST R0,[ER10]
ADD ER10,#0x01
MOV R0,#0x47
ST R0,[ER10]
ADD ER10,#0x01
MOV R0,#0x20
ST R0,[ER10]
ADD ER10,#0x01
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x27
L R0,[ER2]
CMP R0,#0xFF
BEQ skip_94
JMP segment_value
skip_94:
MOV R0,#0x2D
ST R0,[ER10]
ADD ER10,#0x01
JMP segment_char
segment_value:
CALL hexchar
segment_char:
ST R0,[ER10]
ADD ER10,#0x01
MOV R0,#0x00
ST R0,[ER10]
MOV R1,#0x11
CALL lcd
CALL rom_refresh
POP PC
lcd:
MOV R0,#0x07
JMP lcd_font
menu_lcd:
MOV R0,#0x08
lcd_font:
PUSH LR
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x2C
ST R0,[ER2]
L R0,0x80A0
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x2A
ST R0,[ER2]
L R0,0x80A2
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x2B
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x2C
L R0,[ER2]
ST R0,0x80A0
MOV R0,#0x01
ST R0,0x80A2
MOV ER2,ER14
ADD ER2,#0x33
ST R1,[ER2]
MOV R0,#0x00
MOV ER2,ER14
ADD ER2,#0x33
L R1,[ER2]
MOV ER2,ER14
PUSH ER4
CALL rom_draw_text
POP ER4
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x2B
L R0,[ER2]
ST R0,0x80A2
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x2A
L R0,[ER2]
ST R0,0x80A0
POP PC
show:
MOV R0,#0x07
JMP show_font
menu_show:
MOV R0,#0x08
show_font:
PUSH LR
MOV ER8,ER2
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x2C
ST R0,[ER2]
MOV ER2,ER14
ADD ER2,#0x33
ST R1,[ER2]
MOV ER0,ER14
MOV ER2,ER8
MOV ER6,#0x11
CALL ui_text_address
MOV ER2,ER14
ADD ER2,#0x33
L R1,[ER2]
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x2C
L R0,[ER2]
CALL lcd_font
POP PC
hexchar:
CMP R0,#0x0A
BLT skip_95
JMP hex_letter
skip_95:
ADD R0,#0x30
RET
hex_letter:
ADD R0,#0x37
RET
hexbyte:
PUSH LR
MOV R7,R0
SRL R0,#0x04
CALL hexchar
ST R0,[ER10]
ADD ER10,#0x01
MOV R0,R7
AND R0,#0x0F
CALL hexchar
ST R0,[ER10]
ADD ER10,#0x01
POP PC
old_line:
PUSH LR
MOV ER10,ER14
CALL old_length
MOV ER2,ER14
ADD ER2,#0x2B
ST R0,[ER2]
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
MOV R8,R0
MOV R0,R1
CALL hexbyte
MOV R0,R8
CALL hexbyte
MOV R0,#0x20
ST R0,[ER10]
ADD ER10,#0x01
MOV R9,#0x00
old_bytes:
MOV ER2,ER14
ADD ER2,#0x26
L R0,[ER2]
ADD R0,R9
CMP R0,#0x10
BLT skip_96
JMP skip_97
skip_96:
MOV ER2,ER14
ADD ER2,#0x20
L R0,[ER2]
ADD ER2,#0x01
L R1,[ER2]
MOV ER2,ER14
ADD ER2,#0x26
L R6,[ER2]
ADD R6,R9
MOV R7,#0x00
ADD ER0,ER6
L R0,[ER0]
CALL hexbyte
ADD R9,#0x01
MOV ER2,ER14
ADD ER2,#0x2B
L R0,[ER2]
CMP R9,R0
BGE skip_97
JMP old_bytes
skip_97:
old_bytes_done:
MOV R0,#0x00
ST R0,[ER10]
MOV R1,#0x01
CALL lcd
POP PC
name_line:
PUSH LR
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x30
L R0,[ER2]
ADD ER2,#0x01
L R1,[ER2]
MOV ER2,ER0
MOV R1,#0x09
CALL show
POP PC
menu_copy:
PUSH LR
MOV ER0,ER10
MOV ER2,ER6
MOV ER6,#0x0F
CALL ui_text_address
POP PC
menu_row:
PUSH LR
MOV ER8,ER2
MOV ER2,ER14
ADD ER2,#0x33
ST R1,[ER2]
MOV ER10,ER14
MOV R0,R6
ADD R0,#0x30
ST R0,[ER10]
ADD ER10,#0x01
MOV R0,#0x3A
ST R0,[ER10]
ADD ER10,#0x01
MOV ER6,ER8
MOV R9,#0x0E
CALL menu_copy
MOV ER2,ER14
ADD ER2,#0x33
L R1,[ER2]
CALL menu_lcd
POP PC
draw_categories:
PUSH LR
CALL 0x0:0x409A
MOV R2,#0x93
MOV R3,#0x8B
MOV R1,#0x01
CALL menu_show
MOV R2,#0x64
MOV R3,#0x8B
MOV R1,#0x09
CALL menu_show
MOV R2,#0x73
MOV R3,#0x8B
MOV R1,#0x11
CALL menu_show
MOV R2,#0x84
MOV R3,#0x8B
MOV R1,#0x19
CALL menu_show
CALL rom_refresh
POP PC
draw_menu:
PUSH LR
CALL 0x0:0x409A
MOV ER2,ER14
ADD ER2,#0x3C
L R0,[ER2]
ADD R0,#0x00
MOV R8,R0
CALL item_count
MOV R0,R8
CMP R0,R7
BLT skip_98
JMP menu_row_skip_0
skip_98:
MOV ER2,ER14
ADD ER2,#0x28
ST R0,[ER2]
CALL record
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x30
L R0,[ER2]
ADD ER2,#0x01
L R1,[ER2]
MOV ER2,ER0
MOV R6,#0x01
MOV R1,#0x01
CALL menu_row
menu_row_skip_0:
MOV ER2,ER14
ADD ER2,#0x3C
L R0,[ER2]
ADD R0,#0x01
MOV R8,R0
CALL item_count
MOV R0,R8
CMP R0,R7
BLT skip_99
JMP menu_row_skip_1
skip_99:
MOV ER2,ER14
ADD ER2,#0x28
ST R0,[ER2]
CALL record
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x30
L R0,[ER2]
ADD ER2,#0x01
L R1,[ER2]
MOV ER2,ER0
MOV R6,#0x02
MOV R1,#0x09
CALL menu_row
menu_row_skip_1:
MOV ER2,ER14
ADD ER2,#0x3C
L R0,[ER2]
ADD R0,#0x02
MOV R8,R0
CALL item_count
MOV R0,R8
CMP R0,R7
BLT skip_100
JMP menu_row_skip_2
skip_100:
MOV ER2,ER14
ADD ER2,#0x28
ST R0,[ER2]
CALL record
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x30
L R0,[ER2]
ADD ER2,#0x01
L R1,[ER2]
MOV ER2,ER0
MOV R6,#0x03
MOV R1,#0x11
CALL menu_row
menu_row_skip_2:
MOV ER2,ER14
ADD ER2,#0x3C
L R0,[ER2]
ADD R0,#0x03
MOV R8,R0
CALL item_count
MOV R0,R8
CMP R0,R7
BLT skip_101
JMP menu_row_skip_3
skip_101:
MOV ER2,ER14
ADD ER2,#0x28
ST R0,[ER2]
CALL record
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x30
L R0,[ER2]
ADD ER2,#0x01
L R1,[ER2]
MOV ER2,ER0
MOV R6,#0x04
MOV R1,#0x19
CALL menu_row
menu_row_skip_3:
CALL rom_refresh
POP PC
draw_operand:
PUSH LR
CALL 0x0:0x409A
CALL old_line
CALL name_line
MOV ER10,ER14
MOV ER2,ER14
ADD ER2,#0x32
L R7,[ER2]
MOV R0,#0x52
CMP R7,#0x02
BEQ skip_102
JMP operand_not_er
skip_102:
MOV R0,#0x45
operand_not_er:
CMP R7,#0x03
BEQ skip_103
JMP operand_not_bit
skip_103:
MOV R0,#0x42
operand_not_bit:
CMP R7,#0x04
BEQ skip_104
JMP operand_label
skip_104:
MOV R0,#0x48
MOV ER2,ER14
ADD ER2,#0x29
L R7,[ER2]
CMP R7,#0x0E
BEQ skip_105
JMP operand_label
skip_105:
MOV R0,#0x54
operand_label:
ST R0,[ER10]
ADD ER10,#0x01
MOV ER2,ER14
ADD ER2,#0x31
L R9,[ER2]
MOV R0,R9
ADD R0,#0x01
CALL hexchar
ST R0,[ER10]
ADD ER10,#0x01
MOV R0,#0x3D
ST R0,[ER10]
ADD ER10,#0x01
MOV ER2,ER14
ADD ER2,#0x32
L R7,[ER2]
CMP R7,#0x04
BNE skip_106
JMP operand_hex
skip_106:
CMP R9,#0x00
BNE skip_107
JMP operand_a
skip_107:
MOV ER2,ER14
ADD ER2,#0x2E
L R0,[ER2]
JMP operand_value
operand_a:
MOV ER2,ER14
ADD ER2,#0x2D
L R0,[ER2]
JMP operand_value
operand_hex:
MOV ER2,ER14
ADD ER2,#0x20
ADD ER2,#0x20
MOV R0,R9
MOV R1,#0x00
ADD ER2,ER0
L R0,[ER2]
operand_value:
CALL hexchar
ST R0,[ER10]
ADD ER10,#0x01
MOV R0,#0x20
ST R0,[ER10]
ADD ER10,#0x01
MOV R0,#0x45
ST R0,[ER10]
ADD ER10,#0x01
MOV R0,#0x58
ST R0,[ER10]
ADD ER10,#0x01
MOV R0,#0x45
ST R0,[ER10]
ADD ER10,#0x01
MOV R0,#0x00
ST R0,[ER10]
MOV R1,#0x11
CALL lcd
CALL rom_refresh
POP PC
draw_bad_target:
PUSH LR
CALL 0x0:0x409A
CALL old_line
CALL name_line
MOV ER2,ER14
ADD ER2,#0x30
L R0,[ER2]
CMP R0,#0x01
BEQ skip_108
JMP bad_target_text
skip_108:
MOV R2,#0x9C
MOV R3,#0x8B
JMP bad_show
bad_target_text:
CMP R0,#0x02
BEQ skip_109
JMP bad_outside_text
skip_109:
MOV R2,#0xA8
MOV R3,#0x8B
JMP bad_show
bad_outside_text:
CMP R0,#0x03
BEQ skip_110
JMP bad_range_text
skip_110:
MOV R2,#0xB6
MOV R3,#0x8B
JMP bad_show
bad_range_text:
MOV R2,#0xC5
MOV R3,#0x8B
bad_show:
MOV R1,#0x11
CALL show
CALL rom_refresh
POP PC
draw_result:
PUSH LR
CALL 0x0:0x409A
CALL old_line
CALL name_line
CALL rom_refresh
MOV ER10,ER14
MOV R9,#0x00
result_bytes:
MOV ER2,ER14
ADD ER2,#0x34
MOV R0,R9
MOV R1,#0x00
ADD ER2,ER0
L R0,[ER2]
CALL hexbyte
MOV R0,#0x20
ST R0,[ER10]
ADD ER10,#0x01
ADD R9,#0x01
MOV ER2,ER14
ADD ER2,#0x2C
L R0,[ER2]
CMP R9,R0
BLT skip_111
JMP result_end
skip_111:
CMP R9,#0x04
BEQ skip_112
JMP result_bytes
skip_112:
MOV R0,#0x00
ST R0,[ER10]
MOV R1,#0x11
CALL lcd
MOV ER10,ER14
MOV R9,#0x04
JMP result_bytes
result_end:
MOV R0,#0x45
ST R0,[ER10]
ADD ER10,#0x01
MOV R0,#0x58
ST R0,[ER10]
ADD ER10,#0x01
MOV R0,#0x45
ST R0,[ER10]
ADD ER10,#0x01
MOV R0,#0x00
ST R0,[ER10]
MOV ER2,ER14
ADD ER2,#0x2C
L R0,[ER2]
CMP R0,#0x05
BLT skip_113
JMP result_second
skip_113:
MOV R1,#0x11
JMP result_show
result_second:
MOV R1,#0x19
result_show:
CALL lcd
CALL rom_refresh
POP PC
