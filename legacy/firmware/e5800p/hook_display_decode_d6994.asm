; hook_display_decode_d6994
; CPU 0xD6994, physical 0x56994, 4 bytes
basic__display_decode EQU 0xF50B4

hook_display_decode_d6994:
CALL basic__display_decode
