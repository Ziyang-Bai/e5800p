; isa_data
; Return the picker payload at its layout-owned Flash address.
; CPU 0xF8B64, physical 0x78B64, 113 bytes

isa_data:
category_row_0:
DB "1:ARITH 2:MOVE", 0x00
category_row_1:
DB "3:BR    4:LOADST"
DB 0x00
category_row_2:
DB "5:STACK 6:MISC", 0x00
category_title:
DB "FUNCTION", 0x00
operand_bad_text:
DB "BAD OPERAND", 0x00
branch_odd_text:
DB "ODD BR TARGET", 0x00
branch_outside_text:
DB "NOT IN S1 PROG", 0x00
branch_range_text:
DB "BR OUT OF RANGE", 0x00
