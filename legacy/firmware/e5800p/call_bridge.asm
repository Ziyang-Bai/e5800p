; call_bridge
; BASIC integer, hardware-mapped memory and returning far CALL primitives.
; CPU 0x80400, physical 0x00400, 6 bytes

call_bridge:
PUSH ER10
PUSH ER8
POP PC
