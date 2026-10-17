; hook_display_decode_d7236
; CPU 0xD7236, physical 0x57236, 4 bytes
basic__display_decode EQU 0xF50B4

hook_display_decode_d7236:
CALL basic__display_decode
