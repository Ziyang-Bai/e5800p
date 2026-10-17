; hook_display_decode_d6248
; CPU 0xD6248, physical 0x56248, 4 bytes
basic__display_decode EQU 0xF50B4

hook_display_decode_d6248:
CALL basic__display_decode
