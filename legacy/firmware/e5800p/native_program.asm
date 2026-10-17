; native_program
; CPU 0xCA05A, physical 0x4A05A, 4 bytes
selector_address EQU 0x80200

native_program:
JMP selector_address
