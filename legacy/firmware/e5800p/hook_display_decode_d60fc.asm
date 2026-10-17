; hook_display_decode_d60fc
; CPU 0xD60FC, physical 0x560FC, 4 bytes
basic__display_decode EQU 0xF50B4

hook_display_decode_d60fc:
CALL basic__display_decode
