"""Fixed-layout e5800p hooks routines and tables."""

from kits import cpu

BASIC = 0xF3E68
BASIC__FUNCTION = 0xF3F3A
BASIC__EDITOR_INPUT = 0xF5486
BASIC__PROGRAM_MENU = 0xF50EA
SELECTOR_ADDRESS = 0x80200
BASIC__DISPLAY_CC7DE = 0xF4F4E
BASIC__DISPLAY_CC878 = 0xF4F88
BASIC__DISPLAY_CC94A = 0xF4FC4
BASIC__DISPLAY_CCB16 = 0xF4FFE
BASIC__DISPLAY_CCF82 = 0xF5072
BASIC__DISPLAY_CD268 = 0xF5038
BASIC__STATEMENT = 0xF3FB2
LOGO_ADDRESS = 0x81A86
BASIC__DISPLAY_DECODE = 0xF50B4
BASIC__NATIVE_MENU_KEY = 0xF5116
BASIC__SPELL = 0xF3EE4
GRAPH_TABLE_GATE = 0x81100
BASIC__SCAN_IF = 0xF4952
BASIC__SCAN_ELSE = 0xF496C
BASIC__SCAN_FOR = 0xF49A0
BASIC__SCAN_WHILE = 0xF49DA
BASIC__SCAN_BREAK = 0xF4986
BASIC__SCAN_GOTO = 0xF4A14

ADDIN_LABEL = b'Add-in'

ADDIN_LABEL_LABELS = {
    'addin_label': 0x0,
}


def install(fw):
    fw.data('addin_label', ADDIN_LABEL, address=0xF3B1E, labels=ADDIN_LABEL_LABELS)

    @fw.function(native=True, address=0xC70EC)
    def hook_admit_c70ec():
        cpu.label('hook_admit_c70ec')
        cpu.call(BASIC)


    @fw.function(native=True, address=0xC71FE)
    def hook_function_c71fe():
        cpu.label('hook_function_c71fe')
        cpu.jump(BASIC__FUNCTION)


    @fw.function(native=True, address=0xC75F2)
    def hook_admit_c75f2():
        cpu.label('hook_admit_c75f2')
        cpu.call(BASIC)


    @fw.function(native=True, address=0xC884E)
    def hook_editor_input_c884e():
        cpu.label('hook_editor_input_c884e')
        cpu.jump(BASIC__EDITOR_INPUT)


    @fw.function(native=True, address=0xC8936)
    def hook_program_menu_c8936():
        cpu.label('hook_program_menu_c8936')
        cpu.call(BASIC__PROGRAM_MENU)


    @fw.function(native=True, address=0xCA05A)
    def native_program():
        cpu.label('native_program')
        cpu.jump(SELECTOR_ADDRESS)


    @fw.function(native=True, address=0xCC7DE)
    def hook_display_cc7de_cc7de():
        cpu.label('hook_display_cc7de_cc7de')
        cpu.call(BASIC__DISPLAY_CC7DE)


    @fw.function(native=True, address=0xCC878)
    def hook_display_cc878_cc878():
        cpu.label('hook_display_cc878_cc878')
        cpu.call(BASIC__DISPLAY_CC878)


    @fw.function(native=True, address=0xCC94A)
    def hook_display_cc94a_cc94a():
        cpu.label('hook_display_cc94a_cc94a')
        cpu.call(BASIC__DISPLAY_CC94A)


    @fw.function(native=True, address=0xCCB16)
    def hook_display_ccb16_ccb16():
        cpu.label('hook_display_ccb16_ccb16')
        cpu.call(BASIC__DISPLAY_CCB16)


    @fw.function(native=True, address=0xCCF82)
    def hook_display_ccf82_ccf82():
        cpu.label('hook_display_ccf82_ccf82')
        cpu.call(BASIC__DISPLAY_CCF82)


    @fw.function(native=True, address=0xCD268)
    def hook_display_cd268_cd268():
        cpu.label('hook_display_cd268_cd268')
        cpu.call(BASIC__DISPLAY_CD268)


    @fw.function(native=True, address=0xCD696)
    def hook_statement_cd696():
        cpu.label('hook_statement_cd696')
        cpu.jump(BASIC__STATEMENT)


    @fw.function(native=True, address=0xCFA66)
    def native_screen_save():
        cpu.label('native_screen_save')
        cpu.jump(LOGO_ADDRESS)


    @fw.function(native=True, address=0xD60C4)
    def hook_display_decode_d60c4():
        cpu.label('hook_display_decode_d60c4')
        cpu.call(BASIC__DISPLAY_DECODE)


    @fw.function(native=True, address=0xD60FC)
    def hook_display_decode_d60fc():
        cpu.label('hook_display_decode_d60fc')
        cpu.call(BASIC__DISPLAY_DECODE)


    @fw.function(native=True, address=0xD6248)
    def hook_display_decode_d6248():
        cpu.label('hook_display_decode_d6248')
        cpu.call(BASIC__DISPLAY_DECODE)


    @fw.function(native=True, address=0xD6994)
    def hook_display_decode_d6994():
        cpu.label('hook_display_decode_d6994')
        cpu.call(BASIC__DISPLAY_DECODE)


    @fw.function(native=True, address=0xD6B1E)
    def hook_display_decode_d6b1e():
        cpu.label('hook_display_decode_d6b1e')
        cpu.call(BASIC__DISPLAY_DECODE)


    @fw.function(native=True, address=0xD7104)
    def hook_display_decode_d7104():
        cpu.label('hook_display_decode_d7104')
        cpu.call(BASIC__DISPLAY_DECODE)


    @fw.function(native=True, address=0xD7236)
    def hook_display_decode_d7236():
        cpu.label('hook_display_decode_d7236')
        cpu.call(BASIC__DISPLAY_DECODE)


    @fw.function(native=True, address=0xDF550)
    def hook_native_menu_key_df550():
        cpu.label('hook_native_menu_key_df550')
        cpu.jump(BASIC__NATIVE_MENU_KEY)


    @fw.function(native=True, address=0xDFC02)
    def hook_spell_dfc02():
        cpu.label('hook_spell_dfc02')
        cpu.jump(BASIC__SPELL)


    @fw.function(native=True, address=0xE3694)
    def native_table():
        cpu.label('native_table')
        cpu.jump(GRAPH_TABLE_GATE)


    @fw.function(native=True, address=0xE5FCE)
    def hook_scan_if_e5fce():
        cpu.label('hook_scan_if_e5fce')
        cpu.jump(BASIC__SCAN_IF)


    @fw.function(native=True, address=0xE6060)
    def hook_scan_else_e6060():
        cpu.label('hook_scan_else_e6060')
        cpu.jump(BASIC__SCAN_ELSE)


    @fw.function(native=True, address=0xE662C)
    def hook_scan_for_e662c():
        cpu.label('hook_scan_for_e662c')
        cpu.jump(BASIC__SCAN_FOR)


    @fw.function(native=True, address=0xE6876)
    def hook_scan_while_e6876():
        cpu.label('hook_scan_while_e6876')
        cpu.jump(BASIC__SCAN_WHILE)


    @fw.function(native=True, address=0xE6BC4)
    def hook_scan_break_e6bc4():
        cpu.label('hook_scan_break_e6bc4')
        cpu.jump(BASIC__SCAN_BREAK)


    @fw.function(native=True, address=0xE6F9C)
    def hook_scan_goto_e6f9c():
        cpu.label('hook_scan_goto_e6f9c')
        cpu.jump(BASIC__SCAN_GOTO)
