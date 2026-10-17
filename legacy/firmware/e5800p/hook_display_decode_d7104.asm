; hook_display_decode_d7104
; CPU 0xD7104, physical 0x57104, 4 bytes
basic__display_decode EQU 0xF50B4

hook_display_decode_d7104:
CALL basic__display_decode
