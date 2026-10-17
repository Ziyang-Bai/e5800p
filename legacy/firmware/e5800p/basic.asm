; basic
; Flash BASIC token, expression, statement and PROGRAM editor integration.
; CPU 0xF3E68, physical 0x73E68, 6514 bytes
native_token_admission EQU 0xC30D8
native_evaluate EQU 0xC7B6E
basic_memory EQU 0xFB530
basic_graphics EQU 0xFC530
native_error_write EQU 0xE8FBA
native_evaluate_core EQU 0xC701E
native_token_fetch EQU 0xC3794
native_number_copy EQU 0x19B72
basic_asm EQU 0xF9530
native_program_lookup EQU 0xE2F86
native_library_lookup EQU 0xF0484
hook_spell_dfc02 EQU 0xDFC02
native_token_decode EQU 0x10B7E
native_program_function EQU 0xDF3FA
rom_draw_text EQU 0x041DA
rom_refresh EQU 0x043BE
hex_key_address EQU 0x825CA
native_program_insert EQU 0xE302E

basic:
admit:
PUSH LR
PUSH ER4
MOV ER4,ER0
L R0,R2:[ER4]
CMP R0,#0xF9
BNE cond_11
L R0,R2:0x0001[ER4]
CMP R0,#0xE0
BNE cond_1
JMP admit_yes
cond_1:
CMP R0,#0xE1
BNE cond_2
JMP admit_yes
cond_2:
CMP R0,#0xE4
BNE cond_3
JMP admit_yes
cond_3:
CMP R0,#0xE5
BNE cond_4
JMP admit_yes
cond_4:
CMP R0,#0xE6
BNE cond_5
JMP admit_yes
cond_5:
CMP R0,#0xE7
BNE cond_6
JMP admit_yes
cond_6:
CMP R0,#0xE8
BNE cond_7
JMP admit_yes
cond_7:
CMP R0,#0xE9
BNE cond_8
JMP admit_yes
cond_8:
CMP R0,#0xEA
BNE cond_9
JMP admit_yes
cond_9:
CMP R0,#0xEB
BNE cond_10
JMP admit_yes
cond_10:
CMP R0,#0xEC
BNE cond_11
JMP admit_yes
cond_11:
admit_native:
MOV ER0,ER4
CALL native_token_admission
POP ER4
POP PC
admit_yes:
MOV ER0,#0x01
POP ER4
POP PC
spell:
CMP R1,#0xFE
BNE spell_token
ST R0,0x00:[ER2]
MOV R0,#0x00
ST R0,0x00:0x0001[ER2]
MOV ER0,ER2
RET
spell_token:
CMP R1,#0xF9
BNE spell_native
CMP R0,#0xE0
BLT spell_native
CMP R0,#0xF9
BGE spell_native
PUSH LR
PUSH XR4
MOV ER4,ER2
ADD R0,#0x20
MOV R1,#0x00
SLLC R1,#0x01
SLL R0,#0x01
MOV R6,#0xDA
MOV R7,#0x57
ADD ER6,ER0
L ER6,0x0F:[ER6]
spell_copy:
L R0,0x0F:[ER6]
ST R0,0x00:[ER2]
ADD ER6,#0x01
ADD ER2,#0x01
CMP R0,#0x00
BNE spell_copy
MOV ER0,ER4
POP XR4
POP PC
spell_native:
PUSH LR
PUSH ER12
JMP 0xD:0xFC06
function:
CMP R1,#0xF9
BNE function_native
CMP R0,#0xE0
BLT function_native
CMP R0,#0xF9
BGE function_native
PUSH XR4
PUSH QR8
MOV ER12,ER14
ADD SP,#0xF0
MOV ER14,SP
ADD R0,#0x20
ST R0,0x00:0x000C[ER14]
MOV R0,#0x01
ST R0,0x00:0x000D[ER14]
ST ER8,0x00:0x0000[ER14]
ST R10,0x00:0x0002[ER14]
L ER0,0x00:0x0006[ER12]
ST ER0,0x00:0x0004[ER14]
L R0,0x00:0x0008[ER12]
ST R0,0x00:0x0006[ER14]
L ER0,0x00:0x000A[ER12]
ST ER0,0x00:0x0008[ER14]
MOV R0,#0x00
ST R0,0x00:0x000A[ER14]
MOV ER2,ER14
CALL command
ADD SP,#0x10
POP QR8
POP XR4
MOV ER4,ER0
JMP 0xC:0x72CE
function_native:
CMP R0,#0x5B
CMPC R1,#0x00
JMP 0xC:0x7202
statement:
L ER0,R10:[ER8]
L R2,R10:0x0002[ER8]
L R3,R2:[ER0]
CMP R3,#0xF9
BEQ cond_12
JMP statement_native
cond_12:
L R3,R2:0x0001[ER0]
CMP R3,#0xE0
BGE cond_13
JMP statement_native
cond_13:
CMP R3,#0xF9
BLT cond_14
JMP statement_native
cond_14:
CMP R3,#0xE0
BNE cond_15
JMP statement_expression
cond_15:
CMP R3,#0xE1
BNE cond_16
JMP statement_expression
cond_16:
CMP R3,#0xE4
BNE cond_17
JMP statement_expression
cond_17:
CMP R3,#0xE5
BNE cond_18
JMP statement_expression
cond_18:
CMP R3,#0xE6
BNE cond_19
JMP statement_expression
cond_19:
CMP R3,#0xE7
BNE cond_20
JMP statement_expression
cond_20:
CMP R3,#0xE8
BNE cond_21
JMP statement_expression
cond_21:
CMP R3,#0xE9
BNE cond_22
JMP statement_expression
cond_22:
CMP R3,#0xEA
BNE cond_23
JMP statement_expression
cond_23:
CMP R3,#0xEB
BNE cond_24
JMP statement_expression
cond_24:
CMP R3,#0xEC
BNE cond_25
JMP statement_expression
cond_25:
L ER0,0x00:0x000E[ER14]
MOV R2,#0x01
ST R2,0x00:0x0026[ER0]
PUSH XR4
PUSH QR8
MOV ER12,ER14
ADD SP,#0xF0
MOV ER14,SP
ADD R3,#0x20
ST R3,0x00:0x000C[ER14]
MOV R0,#0x00
ST R0,0x00:0x000D[ER14]
ST ER8,0x00:0x0000[ER14]
ST R10,0x00:0x0002[ER14]
L ER0,0x00:0x0006[ER12]
ST ER0,0x00:0x0004[ER14]
L R0,0x00:0x0008[ER12]
ST R0,0x00:0x0006[ER14]
L ER0,0x00:0x000A[ER12]
ST ER0,0x00:0x0008[ER14]
L R0,0x00:0x000C[ER12]
ST R0,0x00:0x000A[ER14]
MOV ER2,ER14
CALL command
ADD SP,#0x10
POP QR8
POP XR4
MOV R4,R0
JMP 0xC:0xD7CA
statement_expression:
MOV ER0,#0x02
JMP 0xC:0xD69E
statement_native:
MOV ER0,ER8
MOV R2,R10
JMP 0xC:0xD69A
command:
PUSH LR
PUSH XR4
PUSH QR8
MOV ER12,ER2
MOV ER0,SP
MOV R2,#0x26
MOV R3,#0x87
CMP ER0,ER2
BGE cond_26
JMP command_no_stack
cond_26:
ADD SP,#0x80
ADD SP,#0x80
ADD SP,#0xF0
MOV ER14,SP
L ER0,0x00:0x0000[ER12]
ST ER0,0x00:0x00C6[ER14]
L R0,0x00:0x0002[ER12]
ST R0,0x00:0x00C8[ER14]
L ER0,0x00:0x0004[ER12]
ST ER0,0x00:0x00CA[ER14]
L R0,0x00:0x0006[ER12]
ST R0,0x00:0x00CC[ER14]
L ER0,0x00:0x0008[ER12]
ST ER0,0x00:0x00CE[ER14]
L R0,0x00:0x000A[ER12]
ST R0,0x00:0x00D0[ER14]
L R0,0x00:0x000C[ER12]
ST R0,0x00:0x00D2[ER14]
L R0,0x00:0x000D[ER12]
ST R0,0x00:0x00D3[ER14]
MOV R0,#0x00
MOV R1,#0x80
MOV ER2,ER14
MOV R4,#0x70
MOV R5,#0x00
CALL near_copy
L ER0,0x00:0x8086
ST ER0,0x00:0x0070[ER14]
MOV ER2,ER14
ADD ER2,#0x3F
ADD ER2,#0x35
MOV ER4,#0x1C
MOV R0,#0x00
command_clear:
ST R0,0x00:[ER2]
ADD ER2,#0x01
ADD ER4,#0x7F
BNE command_clear
ST R0,0x00:0x00D4[ER14]
CALL cursor
ST ER0,0x00:0x00D6[ER14]
ST R2,0x00:0x00D8[ER14]
L R3,0x00:0x00D3[ER14]
CMP R3,#0x00
BNE command_cached
L ER0,0x00:0x00CA[ER14]
L R2,0x00:0x00CC[ER14]
MOV R3,#0x01
ST R3,R2:[ER0]
CALL fetch
JMP command_ready
command_cached:
L ER0,0x00:0x00D6[ER14]
ADD ER0,#0x7E
ST ER0,0x00:0x00D6[ER14]
command_ready:
L R0,0x00:0x00D2[ER14]
CMP R0,#0x17
BNE cond_27
JMP command_asm
cond_27:
CMP R0,#0x18
BNE cond_28
JMP syntax
cond_28:
MOV R1,#0x00
MOV R2,#0x0C
MOV R3,#0x58
ADD ER2,ER0
L R0,0x0F:[ER2]
ST R0,0x00:0x00D5[ER14]
CALL fetch_spaces
L R3,0x00:0x00D3[ER14]
CMP R3,#0x00
BEQ command_arguments
CMP R0,#0x28
BEQ cond_29
JMP syntax
cond_29:
CALL fetch_spaces
command_arguments:
L R3,0x00:0x00D5[ER14]
CMP R3,#0x00
BNE cond_30
JMP command_end_args
cond_30:
argument:
L R0,0x00:0x00D2[ER14]
CMP R0,#0x15
BNE cond_31
L R0,0x00:0x00D4[ER14]
CMP R0,#0x02
BNE cond_31
JMP argument_text
cond_31:
argument_number:
MOV ER0,#0x00
PUSH ER0
PUSH ER0
MOV ER0,ER14
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x12
PUSH ER0
L R0,0x00:0x00CC[ER14]
MOV R1,#0x00
PUSH ER0
L ER0,0x00:0x00CA[ER14]
PUSH ER0
L ER0,0x00:0x00C6[ER14]
L R2,0x00:0x00C8[ER14]
L R3,0x00:0x00D3[ER14]
CMP R3,#0x00
BEQ argument_statement
CALL evaluate_argument
JMP argument_evaluated
argument_statement:
CALL native_evaluate
argument_evaluated:
ADD SP,#0x0A
CMP R0,#0x01
BEQ cond_32
JMP argument_native_error
cond_32:
L R0,0x00:0x00D2[ER14]
MOV R1,#0x00
MOV ER2,#0x06
MUL ER0,R2
L R2,0x00:0x00D4[ER14]
MOV R3,#0x00
ADD ER0,ER2
MOV R2,#0x25
MOV R3,#0x58
ADD ER2,ER0
L R2,0x0F:[ER2]
MOV R3,#0x00
L R4,0x00:0x00D4[ER14]
MOV R5,#0x00
SLLC R5,#0x02
SLL R4,#0x02
MOV ER0,ER14
ADD ER0,#0x3F
ADD ER0,#0x35
ADD ER4,ER0
MOV ER0,ER14
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x12
CALL 0xF:0xB534
MOV ER0,ER0
BEQ cond_33
JMP command_error
cond_33:
argument_done:
L R0,0x00:0x00D4[ER14]
ADD R0,#0x01
ST R0,0x00:0x00D4[ER14]
L R1,0x00:0x00D5[ER14]
CMP R0,R1
BNE cond_34
JMP command_end_args
cond_34:
CALL cached
CMP R0,#0x29
BNE cond_35
L R0,0x00:0x00D2[ER14]
CMP R0,#0x04
BNE cond_35
JMP command_end_args
cond_35:
argument_comma:
CALL cached
CMP R0,#0x2C
BEQ cond_36
JMP syntax
cond_36:
CALL fetch_spaces
JMP cond_30
command_end_args:
CALL cached
L R3,0x00:0x00D3[ER14]
CMP R3,#0x00
BEQ command_boundary
CMP R0,#0x29
BEQ cond_37
JMP syntax
cond_37:
CALL fetch
JMP command_dispatch
command_boundary:
CMP R0,#0x00
BNE cond_38
JMP command_dispatch
cond_38:
CMP R0,#0x0C
BNE cond_39
JMP command_dispatch
cond_39:
CMP R0,#0x0D
BNE cond_40
JMP command_dispatch
cond_40:
CMP R0,#0x3A
BNE cond_41
JMP command_dispatch
cond_41:
JMP syntax
command_dispatch:
L R0,0x00:0x00D2[ER14]
MOV R1,#0x00
MOV ER2,ER14
ADD ER2,#0x3F
ADD ER2,#0x35
MOV ER4,ER14
ADD ER4,#0x3F
ADD ER4,#0x3F
ADD ER4,#0x0E
CMP R0,#0x0F
BNE dispatch_not_flash
CALL 0xF:0x6E6C
JMP dispatch_return
dispatch_not_flash:
CMP R0,#0x0C
BEQ dispatch_graphics
CMP R0,#0x10
BGE dispatch_graphics
CALL basic_memory
JMP dispatch_return
dispatch_graphics:
CALL basic_graphics
dispatch_return:
MOV ER0,ER0
BEQ cond_42
JMP command_error
cond_42:
MOV ER0,ER14
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x0E
MOV ER2,ER14
ADD ER2,#0x3F
ADD ER2,#0x3F
ADD ER2,#0x12
CALL 0xF:0xB538
MOV ER0,ER0
BEQ cond_43
JMP command_error
cond_43:
CALL copy_result
MOV ER0,#0x01
JMP command_out
argument_text:
CALL cached
CMP R0,#0x22
BEQ cond_44
JMP syntax
cond_44:
MOV ER8,#0x00
text_char:
CALL fetch
CMP R0,#0x22
BEQ text_end
CMP R0,#0x20
BGE cond_45
JMP syntax
cond_45:
CMP R0,#0x60
BLT cond_46
JMP syntax
cond_46:
CMP R8,#0x20
BLT cond_47
JMP syntax
cond_47:
MOV ER2,ER14
ADD ER2,#0x3F
ADD ER2,#0x3F
ADD ER2,#0x26
ADD ER2,ER8
ST R0,0x00:[ER2]
ADD ER8,#0x01
JMP text_char
text_end:
MOV ER2,ER14
ADD ER2,#0x3F
ADD ER2,#0x3F
ADD ER2,#0x26
ADD ER2,ER8
MOV R0,#0x00
ST R0,0x00:[ER2]
MOV ER0,ER14
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x26
ST ER0,0x00:0x007C[ER14]
ST ER8,0x00:0x0084[ER14]
CALL fetch_spaces
JMP cond_33
syntax:
MOV ER0,#0x02
command_error:
CMP R1,#0x01
BNE command_native_error
MOV R0,#0x80
MOV R1,#0x5B
CALL error_screen
MOV ER0,#0x06
command_native_error:
ST ER0,0x00:0x008C[ER14]
L ER0,0x00:0x00D6[ER14]
L R2,0x00:0x00D8[ER14]
CALL set_cursor
L ER0,0x00:0x008C[ER14]
L R2,0x00:0x00D0[ER14]
MOV R3,#0x00
PUSH ER2
L ER2,0x00:0x00CE[ER14]
PUSH ER2
CALL native_error_write
ADD SP,#0x04
JMP command_out
argument_native_error:
CALL copy_result
MOV ER0,#0x00
command_out:
ST ER0,0x00:0x008C[ER14]
MOV ER0,ER14
MOV R2,#0x00
MOV R3,#0x80
MOV R4,#0x70
MOV R5,#0x00
CALL near_copy
L ER0,0x00:0x0070[ER14]
ST ER0,0x00:0x8086
L ER0,0x00:0x008C[ER14]
ADD SP,#0x7F
ADD SP,#0x7F
ADD SP,#0x12
POP QR8
POP XR4
POP PC
command_no_stack:
L R2,0x00:0x000A[ER12]
MOV R3,#0x00
PUSH ER2
L ER2,0x00:0x0008[ER12]
PUSH ER2
MOV ER0,#0x06
CALL native_error_write
ADD SP,#0x04
POP QR8
POP XR4
POP PC
evaluate_argument:
PUSH LR
PUSH ER14
MOV ER14,SP
ADD SP,#0x80
ADD SP,#0xFA
PUSH XR8
PUSH ER12
PUSH ER4
MOV ER8,ER0
MOV R10,R2
MOV R0,#0x00
ST R0,0x00:0xFF7E[ER14]
MOV R0,#0x01
ST R0,0x00:0xFFE4[ER14]
MOV R0,#0x95
ST R0,0x00:0xFFE6[ER14]
MOV ER0,ER14
ADD ER0,#0x40
ADD ER0,#0x40
ADD ER0,#0x7E
ST ER0,0x00:0xFF7A[ER14]
MOV ER0,ER14
ADD ER0,#0x64
ST ER0,0x00:0xFF7C[ER14]
CALL 0x0:0x6298
MOV R0,#0x00
MOV R1,#0x0F
PUSH ER0
MOV ER0,ER14
ADD ER0,#0x40
ADD ER0,#0x40
ADD ER0,#0x7A
PUSH ER0
L ER0,0x00:0x000A[ER14]
PUSH ER0
L R0,0x00:0x0008[ER14]
MOV R1,#0x00
PUSH ER0
L ER0,0x00:0x0006[ER14]
PUSH ER0
MOV ER0,ER8
MOV R2,R10
CALL native_evaluate_core
ADD SP,#0x0A
MOV R1,#0x00
POP ER4
POP ER12
POP XR8
MOV SP,ER14
POP ER14
POP PC
near_copy:
L R6,0x00:[ER0]
ST R6,0x00:[ER2]
ADD ER0,#0x01
ADD ER2,#0x01
ADD ER4,#0x7F
BNE near_copy
RET
cursor:
L R2,0x00:0x00C8[ER14]
L ER0,0x00:0x00C6[ER14]
L R3,R2:0x0002[ER0]
L ER0,R2:[ER0]
MOV R2,R3
RET
set_cursor:
L ER4,0x00:0x00C6[ER14]
L R3,0x00:0x00C8[ER14]
ST ER0,R3:[ER4]
ST R2,R3:0x0002[ER4]
RET
fetch_spaces:
PUSH LR
fetch_spaces_loop:
CALL fetch
CMP R0,#0x20
BEQ fetch_spaces_loop
POP PC
fetch:
PUSH LR
L R0,0x00:0x00C8[ER14]
MOV R1,#0x00
PUSH ER0
L ER0,0x00:0x00C6[ER14]
PUSH ER0
L ER0,0x00:0x00CA[ER14]
L R2,0x00:0x00CC[ER14]
CALL native_token_fetch
ADD SP,#0x04
CALL cached
POP PC
cached:
L R2,0x00:0x00CC[ER14]
L ER0,0x00:0x00CA[ER14]
L R0,R2:[ER0]
RET
copy_result:
PUSH LR
MOV ER0,#0x00
PUSH ER0
MOV ER0,ER14
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x12
PUSH ER0
L ER0,0x00:0x00CE[ER14]
L R2,0x00:0x00D0[ER14]
CALL native_number_copy
ADD SP,#0x04
POP PC
command_asm:
CALL source_bounds
MOV ER0,ER0
BEQ cond_48
JMP command_error
cond_48:
L ER0,0x00:0x00D6[ER14]
ST ER0,0x00:0x00E2[ER14]
L R0,0x00:0x00D8[ER14]
ST R0,0x00:0x00E4[ER14]
MOV R0,#0x00
ST R0,0x00:0x00E5[ER14]
MOV ER0,ER14
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x1D
MOV ER2,ER14
ADD ER2,#0x3F
ADD ER2,#0x3F
ADD ER2,#0x3F
ADD ER2,#0x29
CALL basic_asm
MOV ER0,ER0
BEQ asm_success
ST ER0,0x00:0x008C[ER14]
L ER0,0x00:0x00EA[ER14]
ST ER0,0x00:0x00D6[ER14]
L R0,0x00:0x00EC[ER14]
ST R0,0x00:0x00D8[ER14]
L ER0,0x00:0x008C[ER14]
CMP R1,#0x01
BNE cond_49
JMP command_error
cond_49:
L ER0,0x00:0x00F2[ER14]
CALL reason_screen
L ER0,0x00:0x008C[ER14]
JMP command_error
asm_success:
L ER0,0x00:0x00E6[ER14]
L R2,0x00:0x00E8[ER14]
CALL set_cursor
CALL fetch
L ER0,0x00:0x00EE[ER14]
ST ER0,0x00:0x008C[ER14]
L ER0,0x00:0x00F0[ER14]
ST ER0,0x00:0x008E[ER14]
MOV ER0,ER14
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x0E
MOV ER2,ER14
ADD ER2,#0x3F
ADD ER2,#0x3F
ADD ER2,#0x12
CALL 0xF:0xB538
MOV ER0,ER0
BEQ cond_50
JMP command_error
cond_50:
MOV ER0,#0x00
PUSH ER0
MOV ER0,ER14
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x12
PUSH ER0
MOV R0,#0x8E
MOV R1,#0x72
MOV R2,#0x04
CALL native_number_copy
ADD SP,#0x04
CALL copy_result
MOV ER0,#0x01
JMP command_out
source_bounds:
PUSH LR
PUSH XR4
PUSH XR8
PUSH ER12
L R0,0x00:0x80AB
CMP R0,#0x00
BNE cond_51
JMP bounds_bad
cond_51:
CMP R0,#0x0C
BLT cond_52
JMP bounds_bad
cond_52:
ADD R0,#0xFF
MOV R1,#0x00
MOV R2,#0x36
MUL ER0,R2
MOV R8,#0x00
MOV R9,#0x76
ADD ER8,ER0
MOV R10,#0x04
L ER0,R10:[ER8]
ST ER0,0x00:0x00DA[ER14]
L R0,R10:0x0002[ER8]
ST R0,0x00:0x00DC[ER14]
MOV R0,#0x00
ST R0,0x00:0x00DD[ER14]
ADD ER8,#0x08
MOV ER2,ER14
ADD ER2,#0x3F
ADD ER2,#0x3F
ADD ER2,#0x3F
ADD ER2,#0x39
MOV R4,#0x0D
bounds_name:
L R0,R10:[ER8]
ST R0,0x00:[ER2]
ADD ER8,#0x01
ADD ER2,#0x01
ADD R4,#0xFF
BNE bounds_name
MOV R0,#0x00
ST R0,0x00:0x0102[ER14]
MOV ER0,ER14
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x0E
PUSH ER0
MOV ER0,ER14
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x0C
PUSH ER0
MOV ER0,ER14
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x39
MOV ER2,ER14
ADD ER2,#0x3F
ADD ER2,#0x3F
ADD ER2,#0x3F
ADD ER2,#0x3F
ADD ER2,#0x08
CALL native_program_lookup
ADD SP,#0x04
MOV ER0,ER0
BNE bounds_library
L ER8,0x00:0x0108[ER14]
L R10,0x00:0x010A[ER14]
CMP R10,#0x04
BNE bounds_library
MOV ER0,ER8
ADD ER0,#0x06
L ER2,0x00:0x00DA[ER14]
CMP ER0,ER2
BNE bounds_library
L R0,0x00:0x00DC[ER14]
CMP R0,#0x04
BNE bounds_library
MOV R12,#0x00
MOV R13,#0x80
JMP bounds_allocation
bounds_library:
L R0,0x00:0x00DC[ER14]
CMP R0,#0x08
BEQ bounds_s3
CMP R0,#0x09
BEQ cond_53
JMP bounds_bad
cond_53:
MOV R2,#0x00
JMP bounds_lookup_library
bounds_s3:
MOV R2,#0x01
bounds_lookup_library:
L R0,0x00:0x80AD
MOV R1,#0x00
PUSH ER0
ST R2,0x00:0x80AD
MOV ER0,ER14
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x0C
PUSH ER0
MOV ER0,ER14
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x39
MOV R2,#0xC7
MOV R3,#0x01
CALL native_library_lookup
ADD SP,#0x02
POP ER2
ST R2,0x00:0x80AD
MOV ER0,ER0
BEQ cond_54
JMP bounds_bad
cond_54:
L ER8,0x00:0x0108[ER14]
L R10,0x00:0x010A[ER14]
L ER0,R10:0x0010[ER8]
ST ER0,0x00:0x0104[ER14]
L ER0,R10:0x0012[ER8]
ST ER0,0x00:0x0106[ER14]
L ER2,R10:0x0016[ER8]
L ER8,R10:0x0014[ER8]
MOV R10,R2
CMP R3,#0x00
BEQ cond_55
JMP bounds_bad
cond_55:
CMP R10,#0x08
BEQ bounds_library_s3
CMP R10,#0x09
BEQ cond_56
JMP bounds_bad
cond_56:
MOV R0,#0x00
MOV R1,#0x20
CMP ER8,ER0
BGE cond_57
JMP bounds_bad
cond_57:
MOV ER12,#0x00
JMP bounds_library_header
bounds_library_s3:
MOV R0,#0x00
MOV R1,#0xA0
CMP ER8,ER0
BGE cond_58
JMP bounds_bad
cond_58:
MOV ER12,#0x00
bounds_library_header:
L ER0,R10:0x0002[ER8]
ST ER0,0x00:0x008C[ER14]
L ER0,R10:0x0004[ER8]
ST ER0,0x00:0x008E[ER14]
bounds_allocation:
L ER0,0x00:0x0106[ER14]
MOV ER0,ER0
BEQ cond_59
JMP bounds_bad
cond_59:
L ER4,0x00:0x0104[ER14]
MOV ER0,#0x07
CMP ER4,ER0
BGE cond_60
JMP bounds_bad
cond_60:
MOV ER0,ER8
ADD ER0,ER4
CMP ER0,ER8
BGE bounds_owner_end
MOV ER0,ER0
BEQ cond_61
JMP bounds_bad
cond_61:
MOV ER12,ER12
BEQ cond_62
JMP bounds_bad
cond_62:
JMP cond_63
bounds_owner_end:
MOV ER12,ER12
BEQ cond_63
CMP ER12,ER0
BGE cond_63
JMP bounds_bad
cond_63:
bounds_length:
L ER0,0x00:0x008E[ER14]
MOV ER0,ER0
BEQ cond_64
JMP bounds_bad
cond_64:
L ER6,0x00:0x008C[ER14]
MOV ER6,ER6
BNE cond_65
JMP bounds_bad
cond_65:
ADD ER4,#0x7A
CMP ER4,ER6
BGE cond_66
JMP bounds_bad
cond_66:
ADD ER8,#0x06
L ER0,0x00:0x00DA[ER14]
CMP ER8,ER0
BEQ cond_67
JMP bounds_bad
cond_67:
L R0,0x00:0x00DC[ER14]
CMP R0,R10
BEQ cond_68
JMP bounds_bad
cond_68:
ADD ER6,ER8
CMP ER6,ER8
BGE cond_69
JMP bounds_bad
cond_69:
ST ER6,0x00:0x00DE[ER14]
ST R10,0x00:0x00E0[ER14]
MOV R0,#0x00
ST R0,0x00:0x00E1[ER14]
ADD ER6,#0x7F
L R0,R10:[ER6]
CMP R0,#0x00
BEQ cond_70
JMP bounds_bad
cond_70:
MOV ER0,#0x00
JMP bounds_out
bounds_bad:
MOV ER0,#0x02
bounds_out:
POP ER12
POP XR8
POP XR4
POP PC
scan_if:
MOV ER0,ER8
MOV R2,R10
CALL scan
CMP R1,#0xFF
BNE scan_if_ok
MOV ER0,#0x00
JMP 0xE:0x5E90
scan_if_ok:
L ER12,6[FP]
L R0,8[FP]
JMP 0xE:0x5FD2
scan_else:
MOV ER0,ER8
MOV R2,R10
CALL scan
CMP R1,#0xFF
BNE scan_else_ok
MOV ER0,#0x00
JMP 0xE:0x5E90
scan_else_ok:
L ER12,6[FP]
L R0,8[FP]
JMP 0xE:0x6064
scan_break:
MOV ER0,ER8
MOV R2,R10
CALL scan
CMP R1,#0xFF
BNE scan_break_ok
MOV ER0,#0x00
JMP 0xE:0x6B44
scan_break_ok:
L ER12,6[FP]
L R0,8[FP]
JMP 0xE:0x6BC8
scan_for:
PUSH XR0
CALL scan
CMP R1,#0xFF
BNE cond_71
JMP scan_for_fail
cond_71:
CMP R0,#0x01
BEQ cond_72
POP XR0
CALL 0xE:0x5A42
MOV ER0,ER8
MOV R2,R10
PUSH XR0
CALL scan
CMP R1,#0xFF
BNE cond_72
JMP scan_for_fail
cond_72:
scan_for_done:
POP XR0
JMP 0xE:0x6630
scan_for_fail:
POP XR0
ADD SP,#0x04
MOV ER0,#0x00
JMP 0xE:0x6290
scan_while:
PUSH XR0
CALL scan
CMP R1,#0xFF
BNE cond_73
JMP scan_while_fail
cond_73:
CMP R0,#0x01
BEQ cond_74
POP XR0
CALL 0xE:0x5A42
MOV ER0,ER8
MOV R2,R10
PUSH XR0
CALL scan
CMP R1,#0xFF
BNE cond_74
JMP scan_while_fail
cond_74:
scan_while_done:
POP XR0
JMP 0xE:0x687A
scan_while_fail:
POP XR0
ADD SP,#0x04
MOV ER0,#0x00
JMP 0xE:0x67C2
scan_goto:
PUSH XR0
CALL scan
CMP R1,#0xFF
BNE cond_75
JMP scan_goto_fail
cond_75:
CMP R0,#0x01
BEQ cond_76
POP XR0
CALL 0xE:0x5A42
MOV ER0,ER14
ADD ER0,#0x7C
MOV R2,#0x00
PUSH XR0
CALL scan
CMP R1,#0xFF
BNE cond_76
JMP scan_goto_fail
cond_76:
scan_goto_done:
POP XR0
JMP 0xE:0x6FA0
scan_goto_fail:
POP XR0
ADD SP,#0x04
MOV ER0,#0x00
JMP 0xE:0x6F04
scan:
PUSH LR
PUSH XR4
PUSH QR8
MOV ER8,ER0
MOV R10,R2
MOV ER12,ER14
L ER0,0x00:0x0006[ER12]
L R2,0x00:0x0008[ER12]
L R3,R2:[ER0]
CMP R3,#0xF9
BEQ cond_77
JMP scan_none
cond_77:
L R3,R2:0x0001[ER0]
CMP R3,#0xF7
BEQ cond_78
JMP scan_none
cond_78:
MOV ER0,SP
MOV R2,#0x22
MOV R3,#0x86
CMP ER0,ER2
BGE cond_79
JMP scan_stack
cond_79:
ADD SP,#0x80
ADD SP,#0x80
ADD SP,#0xF0
MOV ER14,SP
ST ER8,0x00:0x00C6[ER14]
ST R10,0x00:0x00C8[ER14]
L ER0,0x00:0x0006[ER12]
ST ER0,0x00:0x00CA[ER14]
L R0,0x00:0x0008[ER12]
ST R0,0x00:0x00CC[ER14]
L ER0,0x00:0x000A[ER12]
ST ER0,0x00:0x00CE[ER14]
L R0,0x00:0x000C[ER12]
ST R0,0x00:0x00D0[ER14]
MOV ER0,#0x00
ST ER0,0x00:0x00F2[ER14]
CALL cursor
ADD ER0,#0x7E
ST ER0,0x00:0x00D6[ER14]
ST R2,0x00:0x00D8[ER14]
CALL source_bounds
MOV ER0,ER0
BNE scan_error
L ER0,0x00:0x00D6[ER14]
ST ER0,0x00:0x00E2[ER14]
L R0,0x00:0x00D8[ER14]
ST R0,0x00:0x00E4[ER14]
MOV R0,#0x00
ST R0,0x00:0x00E5[ER14]
MOV ER0,ER14
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x3F
ADD ER0,#0x1D
MOV ER2,ER14
ADD ER2,#0x3F
ADD ER2,#0x3F
ADD ER2,#0x3F
ADD ER2,#0x29
CALL 0xF:0x9534
MOV ER0,ER0
BEQ scan_success
ST ER0,0x00:0x008C[ER14]
L ER0,0x00:0x00EA[ER14]
ST ER0,0x00:0x00D6[ER14]
L R0,0x00:0x00EC[ER14]
ST R0,0x00:0x00D8[ER14]
L ER0,0x00:0x008C[ER14]
scan_error:
ST ER0,0x00:0x008C[ER14]
L ER0,0x00:0x00F2[ER14]
CALL reason_screen
L ER0,0x00:0x00D6[ER14]
L R2,0x00:0x00D8[ER14]
CALL set_cursor
L ER4,0x00:0x0110[ER14]
L R3,0x00:0x0112[ER14]
L ER0,0x00:0x00D6[ER14]
L R2,0x00:0x00D8[ER14]
ST ER0,R3:[ER4]
ST R2,R3:0x0002[ER4]
L R2,0x00:0x00D0[ER14]
MOV R3,#0x00
PUSH ER2
L ER2,0x00:0x00CE[ER14]
PUSH ER2
L ER0,0x00:0x008C[ER14]
CALL native_error_write
ADD SP,#0x04
MOV R0,#0xFF
MOV R1,#0xFF
JMP scan_out
scan_success:
L ER0,0x00:0x00E6[ER14]
L R2,0x00:0x00E8[ER14]
CALL set_cursor
CALL fetch
MOV ER0,#0x01
scan_out:
ADD SP,#0x7F
ADD SP,#0x7F
ADD SP,#0x12
POP QR8
POP XR4
POP PC
scan_stack:
L R2,0x00:0x000C[ER12]
MOV R3,#0x00
PUSH ER2
L ER2,0x00:0x000A[ER12]
PUSH ER2
MOV ER0,#0x06
CALL native_error_write
ADD SP,#0x04
MOV R0,#0xFF
MOV R1,#0xFF
POP QR8
POP XR4
POP PC
scan_none:
MOV ER0,#0x00
POP QR8
POP XR4
POP PC
source_context:
PUSH LR
PUSH XR4
PUSH QR8
MOV ER8,ER0
MOV R10,R2
MOV ER12,ER6
ADD SP,#0xFC
MOV ER14,SP
MOV R0,#0x00
ST R0,0x00:0x0000[ER14]
ST R0,0x00:0x0001[ER14]
ST R0,0x00:0x0003[ER14]
MOV R0,#0x01
ST R0,0x00:0x0002[ER14]
context_loop:
CMP ER8,ER4
BLT cond_80
JMP context_out
cond_80:
CMP ER8,ER12
BLT cond_81
JMP context_out
cond_81:
L R0,R10:[ER8]
ADD ER8,#0x01
CMP R0,#0x00
BNE cond_82
JMP context_out
cond_82:
CMP R0,#0x0D
BNE cond_83
JMP context_newline
cond_83:
CMP R0,#0x0C
BNE cond_84
JMP context_newline
cond_84:
CMP R0,#0x20
BEQ context_loop
CMP R0,#0xF9
BNE context_byte
CMP ER8,ER12
BLT cond_85
JMP context_out
cond_85:
L R0,R10:[ER8]
ADD ER8,#0x01
L R1,0x00:0x0002[ER14]
CMP R1,#0x00
BEQ context_not_head
L R1,0x00:0x0003[ER14]
CMP R1,#0x00
BNE context_not_head
CMP R0,#0xF7
BNE context_endasm
MOV R0,#0x01
ST R0,0x00:0x0001[ER14]
JMP context_not_head
context_endasm:
CMP R0,#0xF8
BNE context_not_head
MOV R0,#0x00
ST R0,0x00:0x0001[ER14]
ST R0,0x00:0x0000[ER14]
JMP context_not_head
context_byte:
L R1,0x00:0x0000[ER14]
CMP R1,#0x00
BNE context_not_head
L R1,0x00:0x0003[ER14]
CMP R1,#0x02
BEQ context_not_head
CMP R0,#0x22
BNE context_comment
XOR R1,#0x01
ST R1,0x00:0x0003[ER14]
JMP context_not_head
context_comment:
CMP R1,#0x00
BNE context_not_head
CMP R0,#0x27
BNE context_prefix
MOV R1,#0x02
ST R1,0x00:0x0003[ER14]
context_prefix:
CMP R0,#0x7F
BEQ context_second
CMP R0,#0xE5
BEQ context_second
CMP R0,#0xE6
BEQ context_second
CMP R0,#0xE7
BEQ context_second
CMP R0,#0xF7
BEQ context_second
JMP context_not_head
context_second:
CMP ER8,ER12
BGE context_out
ADD ER8,#0x01
context_not_head:
MOV R0,#0x00
ST R0,0x00:0x0002[ER14]
JMP context_loop
context_newline:
L R0,0x00:0x0001[ER14]
ST R0,0x00:0x0000[ER14]
MOV R0,#0x00
ST R0,0x00:0x0003[ER14]
MOV R0,#0x01
ST R0,0x00:0x0002[ER14]
JMP context_loop
context_out:
L R0,0x00:0x0000[ER14]
L R1,0x00:0x0002[ER14]
ADD SP,#0x04
POP QR8
POP XR4
POP PC
editor_context:
PUSH LR
PUSH XR4
L ER4,0x00:0xFFD6[ER0]
L ER6,0x00:0xFFE0[ER0]
ADD ER4,ER6
CALL program_extent
MOV ER0,ER0
BEQ context_unowned
CALL source_context
POP XR4
POP PC
display_context:
PUSH LR
PUSH XR4
L ER0,0x00:0x000A[ER8]
L R2,0x00:0x000C[ER8]
CALL header_context
POP XR4
POP PC
header_context:
PUSH LR
PUSH XR4
PUSH XR8
MOV ER8,ER0
MOV R10,R2
CMP R2,#0x04
BEQ cond_86
JMP header_unowned
cond_86:
CALL program_frame
MOV ER0,ER0
BNE cond_87
JMP header_unowned
cond_87:
CALL program_extent
MOV ER0,ER0
BNE cond_88
JMP header_unowned
cond_88:
CMP ER0,ER8
BEQ cond_89
JMP header_unowned
cond_89:
CMP R2,R10
BEQ cond_90
JMP header_unowned
cond_90:
CALL source_context
POP XR8
POP XR4
POP PC
header_unowned:
MOV ER0,#0x00
POP XR8
POP XR4
POP PC
context_unowned:
MOV ER0,#0x00
POP XR4
POP PC
program_frame:
PUSH XR4
MOV ER6,ER14
program_frame_next:
MOV R0,#0xE4
MOV R1,#0x82
CMP ER6,ER0
BGE cond_91
JMP program_frame_none
cond_91:
MOV R0,#0xFA
MOV R1,#0x8D
CMP ER0,ER6
BGE cond_92
JMP program_frame_none
cond_92:
MOV R0,R6
AND R0,#0x01
BEQ cond_93
JMP program_frame_none
cond_93:
L ER0,0x00:0x0002[ER6]
MOV R2,#0xF2
MOV R3,#0xA5
CMP ER0,ER2
BNE program_frame_parent
L R0,0x00:0x0004[ER6]
CMP R0,#0x0C
BNE program_frame_parent
MOV ER0,ER6
POP XR4
RET
program_frame_parent:
L ER0,0x00:[ER6]
CMP ER0,ER6
BGE cond_94
JMP program_frame_none
cond_94:
BNE cond_95
JMP program_frame_none
cond_95:
MOV ER6,ER0
JMP program_frame_next
program_frame_none:
MOV ER0,#0x00
POP XR4
RET
program_extent:
PUSH LR
PUSH XR8
PUSH ER12
PUSH ER14
MOV ER8,ER0
MOV ER0,SP
MOV R2,#0x92
MOV R3,#0x83
CMP ER0,ER2
BGE cond_96
JMP program_extent_stack
cond_96:
ADD SP,#0xF4
MOV ER14,SP
MOV ER0,ER14
ADD ER0,#0x08
PUSH ER0
MOV ER0,ER14
ADD ER0,#0x04
PUSH ER0
MOV ER2,ER14
MOV ER0,ER8
ADD ER0,#0x40
ADD ER0,#0x7C
CALL native_program_lookup
ADD SP,#0x04
MOV ER0,ER0
BEQ cond_97
JMP program_extent_bad
cond_97:
L ER0,0x00:0x0002[ER14]
MOV ER0,ER0
BEQ cond_98
JMP program_extent_bad
cond_98:
L ER0,0x00:0x000A[ER14]
MOV ER0,ER0
BEQ cond_99
JMP program_extent_bad
cond_99:
L R0,0x00:0x0006[ER14]
CMP R0,#0x04
BEQ cond_100
JMP program_extent_bad
cond_100:
L ER10,0x00:0x0004[ER14]
MOV R0,#0xFA
MOV R1,#0x7F
CMP ER0,ER10
BGE cond_101
JMP program_extent_bad
cond_101:
L ER12,0x00:0x0000[ER14]
MOV ER0,#0x07
CMP ER12,ER0
BGE cond_102
JMP program_extent_bad
cond_102:
MOV ER0,ER10
ADD ER0,ER12
CMP ER0,ER10
BGE cond_103
JMP program_extent_bad
cond_103:
MOV R2,#0x00
MOV R3,#0x80
CMP ER2,ER0
BGE cond_104
JMP program_extent_bad
cond_104:
L ER6,0x00:0x0008[ER14]
MOV ER6,ER6
BNE cond_105
JMP program_extent_bad
cond_105:
ADD ER12,#0x7A
CMP ER12,ER6
BGE cond_106
JMP program_extent_bad
cond_106:
ADD ER10,#0x06
L ER0,0x00:0xFFE0[ER8]
CMP ER0,ER10
BEQ cond_107
JMP program_extent_bad
cond_107:
L R0,0x00:0xFFE2[ER8]
CMP R0,#0x04
BEQ cond_108
JMP program_extent_bad
cond_108:
ADD ER6,ER10
CMP ER4,ER10
BGE cond_109
JMP program_extent_bad
cond_109:
CMP ER4,ER6
BLT cond_110
JMP program_extent_bad
cond_110:
MOV ER0,ER6
ADD ER0,#0x7F
MOV R2,#0x04
L R0,R2:[ER0]
CMP R0,#0x00
BEQ cond_111
JMP program_extent_bad
cond_111:
MOV ER0,ER10
JMP program_extent_out
program_extent_bad:
MOV ER0,#0x00
program_extent_out:
ADD SP,#0x0C
POP ER14
POP ER12
POP XR8
POP PC
program_extent_stack:
MOV ER0,#0x00
POP ER14
POP ER12
POP XR8
POP PC
display_cc7de:
PUSH LR
PUSH XR4
PUSH XR0
MOV ER4,ER12
CALL display_context
CMP R0,#0x01
BNE display_cc7de_native
POP XR0
CMP R1,#0x00
BNE display_cc7de_native_restored
CMP R0,#0x20
BLT display_cc7de_native_restored
CMP R0,#0x7F
BGE display_cc7de_native_restored
ST R0,0x00:[ER2]
MOV R0,#0x00
ST R0,0x00:0x0001[ER2]
MOV ER0,#0x01
POP XR4
POP PC
display_cc7de_native:
POP XR0
display_cc7de_native_restored:
CALL 0xD:0xFD00
POP XR4
POP PC
display_cc878:
PUSH LR
PUSH XR4
PUSH XR0
MOV R5,#0x00
ADD ER4,ER6
CALL display_context
CMP R0,#0x01
BNE display_cc878_native
POP XR0
CMP R1,#0x00
BNE display_cc878_native_restored
CMP R0,#0x20
BLT display_cc878_native_restored
CMP R0,#0x7F
BGE display_cc878_native_restored
ST R0,0x00:[ER2]
MOV R0,#0x00
ST R0,0x00:0x0001[ER2]
MOV ER0,#0x01
POP XR4
POP PC
display_cc878_native:
POP XR0
display_cc878_native_restored:
CALL 0xD:0xFD00
POP XR4
POP PC
display_cc94a:
PUSH LR
PUSH XR4
PUSH XR0
MOV ER4,ER12
CALL display_context
CMP R0,#0x01
BNE display_cc94a_native
POP XR0
CMP R1,#0x00
BNE display_cc94a_native_restored
CMP R0,#0x20
BLT display_cc94a_native_restored
CMP R0,#0x7F
BGE display_cc94a_native_restored
ST R0,0x00:[ER2]
MOV R0,#0x00
ST R0,0x00:0x0001[ER2]
MOV ER0,#0x01
POP XR4
POP PC
display_cc94a_native:
POP XR0
display_cc94a_native_restored:
CALL 0xD:0xFD00
POP XR4
POP PC
display_ccb16:
PUSH LR
PUSH XR4
PUSH XR0
MOV ER4,ER12
CALL display_context
CMP R0,#0x01
BNE display_ccb16_native
POP XR0
CMP R1,#0x00
BNE display_ccb16_native_restored
CMP R0,#0x20
BLT display_ccb16_native_restored
CMP R0,#0x7F
BGE display_ccb16_native_restored
ST R0,0x00:[ER2]
MOV R0,#0x00
ST R0,0x00:0x0001[ER2]
MOV ER0,#0x01
POP XR4
POP PC
display_ccb16_native:
POP XR0
display_ccb16_native_restored:
CALL 0xD:0xFD00
POP XR4
POP PC
display_cd268:
PUSH LR
PUSH XR4
PUSH XR0
MOV ER4,ER12
CALL display_context
CMP R0,#0x01
BNE display_cd268_native
POP XR0
CMP R1,#0x00
BNE display_cd268_native_restored
CMP R0,#0x20
BLT display_cd268_native_restored
CMP R0,#0x7F
BGE display_cd268_native_restored
ST R0,0x00:[ER2]
MOV R0,#0x00
ST R0,0x00:0x0001[ER2]
MOV ER0,#0x01
POP XR4
POP PC
display_cd268_native:
POP XR0
display_cd268_native_restored:
CALL 0xD:0xFD00
POP XR4
POP PC
display_ccf82:
PUSH LR
PUSH XR4
PUSH XR0
L ER0,0x00:0x000A[ER8]
ADD ER4,ER0
ADD ER4,#0x7F
CALL display_context
CMP R0,#0x01
BNE display_ccf82_native
POP XR0
CMP R1,#0x00
BNE display_ccf82_native_restored
CMP R0,#0x20
BLT display_ccf82_native_restored
CMP R0,#0x7F
BGE display_ccf82_native_restored
ST R0,0x00:[ER2]
MOV R0,#0x00
ST R0,0x00:0x0001[ER2]
MOV ER0,ER2
POP XR4
POP PC
display_ccf82_native:
POP XR0
display_ccf82_native_restored:
CALL hook_spell_dfc02
POP XR4
POP PC
display_decode:
PUSH LR
PUSH XR4
MOV ER4,ER0
CALL native_token_decode
PUSH ER0
L ER0,0x00:0x800A
L R2,0x00:0x800C
CALL header_context
POP ER2
CMP R0,#0x01
BNE display_decode_native
CMP R3,#0x00
BNE display_decode_native
CMP R2,#0x20
BLT display_decode_native
CMP R2,#0x7F
BGE display_decode_native
MOV R3,#0xFE
display_decode_native:
MOV ER0,ER2
POP XR4
POP PC
program_menu:
PUSH LR
PUSH XR4
MOV ER4,ER0
PUSH ER2
MOV ER0,ER14
CALL editor_context
POP ER2
CMP R0,#0x01
BEQ program_block_menu
MOV ER0,ER4
CALL native_program_function
program_menu_return:
POP XR4
POP PC
program_block_menu:
MOV ER6,ER14
CALL block_menu
MOV R0,#0xFF
MOV R1,#0xFF
POP XR4
POP PC
native_menu_key:
CALL 0x1:0x25FC
CMP R0,#0xFD
BEQ cond_112
JMP native_menu_key_return
cond_112:
L ER2,0x00:0x0002[ER14]
MOV R0,#0x04
MOV R1,#0x51
CMP ER0,ER2
BEQ cond_113
JMP native_menu_right
cond_113:
L ER0,0x00:0xFE5E[ER14]
MOV ER0,ER0
BEQ cond_114
JMP native_menu_right
cond_114:
L ER0,R11:0x000C[ER6]
L R2,R11:0x000E[ER6]
CMP R0,#0x00
CMPC R1,#0x00
CMPC R2,#0x00
BEQ cond_115
JMP native_menu_right
cond_115:
CALL nx_menu
CMP R1,#0xFF
BEQ native_menu_back
ST ER0,0x00:[ER8]
MOV ER0,#0x01
ADD SP,#0x02
JMP 0xD:0xF592
native_menu_back:
ADD SP,#0x02
JMP 0xD:0xF49A
native_menu_right:
MOV R0,#0xFD
native_menu_key_return:
JMP 0xD:0xF554
nx_menu:
PUSH LR
PUSH XR4
nx_page:
MOV R0,#0xBC
MOV R1,#0x58
MOV ER2,#0x01
CALL choose
CMP R1,#0xFF
BNE cond_116
JMP nx_next_3
cond_116:
nx_categories:
MOV R0,#0xBE
MOV R1,#0x58
MOV ER2,#0x04
CALL choose
CMP R1,#0xFF
BNE cond_117
JMP nx_page
cond_117:
MOV ER4,ER0
CMP R0,#0x00
BNE nx_next_0
MOV R0,#0xC6
MOV R1,#0x58
MOV ER2,#0x07
CALL choose
CMP R1,#0xFF
BNE cond_118
JMP cond_116
cond_118:
MOV R2,#0xD4
MOV R3,#0x58
ADD ER2,ER0
L R0,0x0F:[ER2]
MOV R1,#0xF9
JMP nx_next_3
nx_next_0:
CMP R0,#0x01
BNE nx_next_1
MOV R0,#0xDC
MOV R1,#0x58
MOV ER2,#0x03
CALL choose
CMP R1,#0xFF
BNE cond_119
JMP cond_116
cond_119:
MOV R2,#0xE2
MOV R3,#0x58
ADD ER2,ER0
L R0,0x0F:[ER2]
MOV R1,#0xF9
JMP nx_next_3
nx_next_1:
CMP R0,#0x02
BNE nx_next_2
MOV R0,#0xE6
MOV R1,#0x58
MOV ER2,#0x08
CALL choose
CMP R1,#0xFF
BNE cond_120
JMP cond_116
cond_120:
MOV R2,#0xF6
MOV R3,#0x58
ADD ER2,ER0
L R0,0x0F:[ER2]
MOV R1,#0xF9
JMP nx_next_3
nx_next_2:
CMP R0,#0x03
BNE nx_next_3
MOV R0,#0xFE
MOV R1,#0x58
MOV ER2,#0x07
CALL choose
CMP R1,#0xFF
BNE cond_121
JMP cond_116
cond_121:
MOV R2,#0x0C
MOV R3,#0x59
ADD ER2,ER0
L R0,0x0F:[ER2]
MOV R1,#0xF9
JMP nx_next_3
nx_next_3:
nx_out:
POP XR4
POP PC
choose:
PUSH LR
PUSH XR4
PUSH QR8
MOV ER8,ER0
MOV ER10,ER2
MOV ER12,#0x00
MOV ER0,SP
MOV R2,#0x32
MOV R3,#0x83
CMP ER0,ER2
BGE cond_122
JMP choose_no_stack
cond_122:
ADD SP,#0xD8
MOV ER14,SP
L R0,0x00:0x80A0
ST R0,0x00:0x0020[ER14]
L R0,0x00:0x80A1
ST R0,0x00:0x0021[ER14]
L R0,0x00:0x80A2
ST R0,0x00:0x0022[ER14]
MOV R0,#0x08
ST R0,0x00:0x80A0
MOV R0,#0x00
ST R0,0x00:0x80A1
MOV R0,#0x01
ST R0,0x00:0x80A2
choose_page:
CALL 0x0:0x409A
MOV ER4,#0x00
choose_row:
MOV ER0,ER12
ADD ER0,ER4
CMP ER0,ER10
BGE choose_key
SLLC R1,#0x01
SLL R0,#0x01
ADD ER0,ER8
L ER6,0x0F:[ER0]
MOV R0,R4
ADD R0,#0x31
ST R0,0x00:0x0000[ER14]
MOV R0,#0x3A
ST R0,0x00:0x0001[ER14]
MOV ER2,ER14
ADD ER2,#0x02
MOV R1,#0x0D
choose_text:
L R0,0x0F:[ER6]
ST R0,0x00:[ER2]
CMP R0,#0x00
BEQ choose_draw
ADD ER6,#0x01
ADD ER2,#0x01
ADD R1,#0xFF
BNE choose_text
MOV R0,#0x00
ST R0,0x00:[ER2]
choose_draw:
MOV R1,R4
SLL R1,#0x03
ADD R1,#0x01
MOV R0,#0x00
MOV ER2,ER14
PUSH ER4
CALL rom_draw_text
POP ER4
ADD ER4,#0x01
CMP R4,#0x04
BLT choose_row
choose_key:
CALL rom_refresh
CALL hex_key_address
CMP R0,#0xFA
BEQ choose_cancel
CMP R0,#0xFC
BEQ choose_left
CMP R0,#0xFD
BEQ choose_right
CMP R0,#0x31
BGE cond_123
JMP choose_key
cond_123:
CMP R0,#0x35
BLT cond_124
JMP choose_key
cond_124:
ADD R0,#0xCF
MOV R1,#0x00
ADD ER0,ER12
CMP ER0,ER10
BLT cond_125
JMP choose_key
cond_125:
JMP choose_out
choose_left:
CMP R12,#0x04
BGE cond_126
JMP choose_key
cond_126:
ADD ER12,#0x7C
JMP choose_page
choose_right:
MOV ER0,ER12
ADD ER0,#0x04
CMP ER0,ER10
BLT cond_127
JMP choose_key
cond_127:
MOV ER12,ER0
JMP choose_page
choose_cancel:
MOV R0,#0xFF
MOV R1,#0xFF
choose_out:
ST ER0,0x00:0x0024[ER14]
L R0,0x00:0x0020[ER14]
ST R0,0x00:0x80A0
L R0,0x00:0x0021[ER14]
ST R0,0x00:0x80A1
L R0,0x00:0x0022[ER14]
ST R0,0x00:0x80A2
L ER0,0x00:0x0024[ER14]
ADD SP,#0x28
POP QR8
POP XR4
POP PC
choose_no_stack:
MOV R0,#0xFF
MOV R1,#0xFF
POP QR8
POP XR4
POP PC
reason_screen:
CMP R0,#0x00
BNE reason_screen_show
RET
reason_screen_show:
PUSH LR
CMP R0,#0x07
BLT reason_screen_index
MOV ER0,#0x01
reason_screen_index:
ADD ER0,#0x7F
SLLC R1,#0x01
SLL R0,#0x01
MOV R2,#0x74
MOV R3,#0x5B
ADD ER2,ER0
L ER0,0x0F:[ER2]
CALL error_screen
POP PC
error_screen:
PUSH LR
PUSH XR4
PUSH QR8
MOV ER8,ER0
ADD SP,#0xD8
MOV ER14,SP
L R0,0x00:0x80A0
ST R0,0x00:0x0020[ER14]
L R0,0x00:0x80A1
ST R0,0x00:0x0021[ER14]
L R0,0x00:0x80A2
ST R0,0x00:0x0022[ER14]
MOV R0,#0x08
ST R0,0x00:0x80A0
MOV R0,#0x00
ST R0,0x00:0x80A1
MOV R0,#0x01
ST R0,0x00:0x80A2
CALL 0x0:0x409A
MOV R6,#0x8C
MOV R7,#0x5B
MOV R1,#0x01
CALL error_line
MOV ER6,ER8
MOV R1,#0x09
CALL error_line
MOV R6,#0x96
MOV R7,#0x5B
MOV R1,#0x19
CALL error_line
CALL rom_refresh
error_wait:
CALL hex_key_address
CMP R0,#0xFA
BNE error_wait
L R0,0x00:0x0020[ER14]
ST R0,0x00:0x80A0
L R0,0x00:0x0021[ER14]
ST R0,0x00:0x80A1
L R0,0x00:0x0022[ER14]
ST R0,0x00:0x80A2
ADD SP,#0x28
POP QR8
POP XR4
POP PC
error_line:
PUSH LR
ST R1,0x00:0x0023[ER14]
MOV ER2,ER14
error_line_copy:
L R0,0x0F:[ER6]
ST R0,0x00:[ER2]
ADD ER6,#0x01
ADD ER2,#0x01
CMP R0,#0x00
BNE error_line_copy
MOV R0,#0x00
L R1,0x00:0x0023[ER14]
MOV ER2,ER14
CALL rom_draw_text
POP PC
editor_input:
CMP R11,#0x03
BNE cond_128
JMP editor_input_native
cond_128:
PUSH XR0
PUSH XR4
MOV ER0,ER14
CALL editor_context
MOV R3,R0
L ER0,0x00:0xFFDC[ER14]
CMP R1,#0xF9
BNE editor_ascii
CMP R0,#0xE0
BLT editor_input_restore
CMP R0,#0xF9
BGE editor_input_restore
ADD SP,#0xFC
MOV ER6,SP
ST R1,0x00:[ER6]
ST R0,0x00:0x0001[ER6]
MOV R2,#0x20
CMP R0,#0xE0
BEQ editor_parenthesis
CMP R0,#0xE1
BEQ editor_parenthesis
CMP R0,#0xE4
BEQ editor_parenthesis
CMP R0,#0xE5
BEQ editor_parenthesis
CMP R0,#0xE6
BEQ editor_parenthesis
CMP R0,#0xE7
BEQ editor_parenthesis
CMP R0,#0xE8
BEQ editor_parenthesis
CMP R0,#0xE9
BEQ editor_parenthesis
CMP R0,#0xEA
BEQ editor_parenthesis
CMP R0,#0xEB
BEQ editor_parenthesis
CMP R0,#0xEC
BEQ editor_parenthesis
JMP editor_token_text
editor_parenthesis:
MOV R2,#0x28
editor_token_text:
ST R2,0x00:0x0002[ER6]
MOV ER0,ER6
MOV ER2,#0x03
JMP editor_insert_buffer
editor_ascii:
CMP R3,#0x01
BNE editor_input_restore
CMP R1,#0x7D
BNE editor_ascii_byte
CMP R0,#0x15
BNE editor_input_restore
MOV ER0,#0x0D
JMP editor_ascii_ready
editor_ascii_byte:
CMP R1,#0x00
BNE editor_input_restore
CMP R0,#0x0E
BNE editor_ascii_range
MOV R0,#0x0D
JMP editor_ascii_ready
editor_ascii_range:
CMP R0,#0x20
BLT editor_input_restore
CMP R0,#0x7F
BGE editor_input_restore
editor_ascii_ready:
ADD SP,#0xFC
MOV ER6,SP
ST R0,0x00:[ER6]
MOV ER0,ER6
MOV ER2,#0x01
editor_insert_buffer:
MOV R4,#0x00
MOV ER6,ER14
CALL editor_insert
ADD SP,#0x04
MOV ER0,ER0
BNE editor_insert_failed
POP XR4
POP XR0
JMP 0xC:0x877C
editor_insert_failed:
POP XR4
ADD SP,#0x04
MOV ER4,ER0
JMP 0xC:0x8922
editor_input_restore:
POP XR4
POP XR0
editor_input_native:
MOV ER2,ER2
BNE editor_input_nonzero
JMP 0xC:0x8896
editor_input_nonzero:
JMP 0xC:0x8852
editor_insert:
PUSH LR
PUSH XR4
PUSH QR8
MOV ER8,ER0
MOV ER10,ER2
MOV ER12,ER6
MOV ER0,SP
MOV R2,#0x92
MOV R3,#0x84
CMP ER0,ER2
BGE cond_129
JMP editor_insert_stack
cond_129:
ADD SP,#0xEC
MOV ER14,SP
MOV R5,#0x00
PUSH ER4
PUSH ER8
MOV ER0,#0x00
PUSH ER0
PUSH ER10
PUSH ER0
L ER0,0x00:0xFFD6[ER12]
ST ER0,0x00:0x0010[ER14]
PUSH ER0
MOV ER0,ER12
ADD ER0,#0x40
ADD ER0,#0x7C
CALL native_program_insert
ADD SP,#0x0C
MOV ER0,ER0
BNE editor_insert_out
MOV ER0,ER14
ADD ER0,#0x08
PUSH ER0
MOV ER0,ER14
ADD ER0,#0x04
PUSH ER0
MOV ER2,ER14
MOV ER0,ER12
ADD ER0,#0x40
ADD ER0,#0x7C
CALL native_program_lookup
ADD SP,#0x04
MOV ER0,ER0
BNE editor_insert_out
L ER0,0x00:0x0004[ER14]
ADD ER0,#0x06
ST ER0,0x00:0xFFB4[ER12]
ST ER0,0x00:0xFFE0[ER12]
ST ER0,0x00:0xFFEC[ER12]
L R0,0x00:0x0006[ER14]
ST R0,0x00:0xFFB6[ER12]
ST R0,0x00:0xFFE2[ER12]
ST R0,0x00:0xFFEE[ER12]
L ER0,0x00:0x0008[ER14]
ADD ER0,#0x7F
ST ER0,0x00:0xFFAE[ER12]
ST ER0,0x00:0xFFB8[ER12]
L ER0,0x00:0x000A[ER14]
ST ER0,0x00:0xFFBA[ER12]
L ER0,0x00:0x0000[ER14]
ST ER0,0x00:0xFFB0[ER12]
L ER0,0x00:0x0002[ER14]
ST ER0,0x00:0xFFB2[ER12]
L ER0,0x00:0x0010[ER14]
ADD ER0,ER10
ST ER0,0x00:0xFFD6[ER12]
MOV ER0,#0x00
editor_insert_out:
ADD SP,#0x14
POP QR8
POP XR4
POP PC
editor_insert_stack:
MOV ER0,#0x06
POP QR8
POP XR4
POP PC
block_menu:
PUSH LR
PUSH XR4
PUSH QR8
MOV ER12,ER6
block_categories:
MOV R0,#0x14
MOV R1,#0x59
MOV ER2,#0x04
CALL choose
CMP R1,#0xFF
BNE cond_130
JMP block_out
cond_130:
CMP R0,#0x00
BNE cond_131
JMP block_next_3
cond_131:
CMP R0,#0x01
BNE block_next_1
MOV R0,#0x28
MOV R1,#0x59
MOV ER2,#0x21
CALL choose
CMP R1,#0xFF
BNE cond_132
JMP block_categories
cond_132:
MOV R2,#0x6A
MOV R3,#0x59
JMP block_op_next_5
block_next_1:
CMP R0,#0x02
BNE block_next_2
MOV R0,#0xAC
MOV R1,#0x59
MOV ER2,#0x14
CALL choose
CMP R1,#0xFF
BNE cond_133
JMP block_categories
cond_133:
MOV R2,#0xD4
MOV R3,#0x59
JMP block_op_next_5
block_next_2:
CMP R0,#0x03
BNE block_next_3
MOV R0,#0xFC
MOV R1,#0x59
MOV ER2,#0x03
CALL choose
CMP R1,#0xFF
BNE cond_134
JMP block_categories
cond_134:
MOV R2,#0x02
MOV R3,#0x5A
JMP block_op_next_5
block_next_3:
block_op:
MOV R0,#0x1C
MOV R1,#0x59
MOV ER2,#0x06
CALL choose
CMP R1,#0xFF
BNE cond_135
JMP block_categories
cond_135:
CMP R0,#0x00
BNE block_op_next_0
MOV R0,#0x08
MOV R1,#0x5A
MOV ER2,#0x22
CALL choose
CMP R1,#0xFF
BNE cond_136
JMP block_next_3
cond_136:
MOV R2,#0x4C
MOV R3,#0x5A
JMP block_op_next_5
block_op_next_0:
CMP R0,#0x01
BNE block_op_next_1
MOV R0,#0x90
MOV R1,#0x5A
MOV ER2,#0x06
CALL choose
CMP R1,#0xFF
BNE cond_137
JMP block_next_3
cond_137:
MOV R2,#0x9C
MOV R3,#0x5A
JMP block_op_next_5
block_op_next_1:
CMP R0,#0x02
BNE block_op_next_2
MOV R0,#0xA8
MOV R1,#0x5A
MOV ER2,#0x10
CALL choose
CMP R1,#0xFF
BNE cond_138
JMP block_next_3
cond_138:
MOV R2,#0xC8
MOV R3,#0x5A
JMP block_op_next_5
block_op_next_2:
CMP R0,#0x03
BNE block_op_next_3
MOV R0,#0xE8
MOV R1,#0x5A
MOV ER2,#0x0C
CALL choose
CMP R1,#0xFF
BNE cond_139
JMP block_next_3
cond_139:
MOV R2,#0x00
MOV R3,#0x5B
JMP block_op_next_5
block_op_next_3:
CMP R0,#0x04
BNE block_op_next_4
MOV R0,#0x18
MOV R1,#0x5B
MOV ER2,#0x0D
CALL choose
CMP R1,#0xFF
BNE cond_140
JMP block_next_3
cond_140:
MOV R2,#0x32
MOV R3,#0x5B
JMP block_op_next_5
block_op_next_4:
CMP R0,#0x05
BNE block_op_next_5
MOV R0,#0x4C
MOV R1,#0x5B
MOV ER2,#0x0A
CALL choose
CMP R1,#0xFF
BNE cond_141
JMP block_next_3
cond_141:
MOV R2,#0x60
MOV R3,#0x5B
JMP block_op_next_5
block_op_next_5:
block_selected:
SLLC R1,#0x01
SLL R0,#0x01
ADD ER2,ER0
L ER8,0x0F:[ER2]
L R0,0x0F:[ER8]
CMP R0,#0xF9
BNE cond_142
MOV ER0,ER12
CALL editor_context
CMP R1,#0x01
BEQ cond_142
JMP block_categories
cond_142:
block_length:
MOV ER10,#0x00
MOV ER2,ER8
block_count:
L R0,0x0F:[ER2]
CMP R0,#0x00
BEQ block_insert
ADD ER2,#0x01
ADD ER10,#0x01
JMP block_count
block_insert:
MOV ER0,ER8
MOV ER2,ER10
MOV R4,#0x0F
MOV ER6,ER12
CALL editor_insert
block_out:
POP QR8
POP XR4
POP PC
