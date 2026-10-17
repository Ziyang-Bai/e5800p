; journal_program_ram
; Return nonoverlapping (physical S0 offset, machine-code bytes) spans.
; CPU 0x83CC0, physical 0x03CC0, 28 bytes
rom_flash_program EQU 0x04E86

journal_program_ram:
PUSH LR
PUSH XR4
PUSH QR8
PUSH ER6
MOV R8,#0x00
PUSH R8
PUSH ER4
MOV ER2,#0x08
CALL rom_flash_program
ADD SP,#0x06
POP QR8
POP XR4
POP PC
