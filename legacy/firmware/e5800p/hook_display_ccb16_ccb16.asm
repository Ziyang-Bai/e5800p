; hook_display_ccb16_ccb16
; CPU 0xCCB16, physical 0x4CB16, 4 bytes
basic__display_ccb16 EQU 0xF4FFE

hook_display_ccb16_ccb16:
CALL basic__display_ccb16
