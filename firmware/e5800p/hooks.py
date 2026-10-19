"""Fixed-layout e5800p hooks routines and tables."""

from kits import cpu


ADDIN_LABEL = b'Add-in'

ADDIN_LABEL_LABELS = {
    'addin_label': 0x0,
}


def install(fw):
    fw.data('addin_label', ADDIN_LABEL, address=0xF3B1E, labels=ADDIN_LABEL_LABELS)

    @fw.function(native=True, address=0xC70EC)
    def hook_admit_c70ec():
        cpu.label('hook_admit_c70ec')
        cpu.call('fn_basic')


    @fw.function(native=True, address=0xC71FE)
    def hook_function_c71fe():
        cpu.label('hook_function_c71fe')
        cpu.jump('fn_basic__function')


    @fw.function(native=True, address=0xC75F2)
    def hook_admit_c75f2():
        cpu.label('hook_admit_c75f2')
        cpu.call('fn_basic')


    @fw.function(native=True, address=0xC884E)
    def hook_editor_input_c884e():
        cpu.label('hook_editor_input_c884e')
        cpu.jump('fn_basic__editor_input')


    @fw.function(native=True, address=0xC8936)
    def hook_program_menu_c8936():
        cpu.label('hook_program_menu_c8936')
        cpu.call('fn_basic_menu')


    @fw.function(native=True, address=0xCA05A)
    def native_program():
        cpu.label('native_program')
        cpu.jump('fn_selector')


    @fw.function(native=True, address=0xCC7DE)
    def hook_display_cc7de_cc7de():
        cpu.label('hook_display_cc7de_cc7de')
        cpu.call('fn_basic__display_cc7de')


    @fw.function(native=True, address=0xCC878)
    def hook_display_cc878_cc878():
        cpu.label('hook_display_cc878_cc878')
        cpu.call('fn_basic__display_cc878')


    @fw.function(native=True, address=0xCC94A)
    def hook_display_cc94a_cc94a():
        cpu.label('hook_display_cc94a_cc94a')
        cpu.call('fn_basic__display_cc94a')


    @fw.function(native=True, address=0xCCB16)
    def hook_display_ccb16_ccb16():
        cpu.label('hook_display_ccb16_ccb16')
        cpu.call('fn_basic__display_ccb16')


    @fw.function(native=True, address=0xCCF82)
    def hook_display_ccf82_ccf82():
        cpu.label('hook_display_ccf82_ccf82')
        cpu.call('fn_basic__display_ccf82')


    @fw.function(native=True, address=0xCD268)
    def hook_display_cd268_cd268():
        cpu.label('hook_display_cd268_cd268')
        cpu.call('fn_basic__display_cd268')


    @fw.function(native=True, address=0xCD696)
    def hook_statement_cd696():
        cpu.label('hook_statement_cd696')
        cpu.jump('fn_basic__statement')


    @fw.function(native=True, address=0xCFA66)
    def native_screen_save():
        cpu.label('native_screen_save')
        cpu.jump('fn_mode_screen_save')


    @fw.function(native=True, address=0xD60C4)
    def hook_display_decode_d60c4():
        cpu.label('hook_display_decode_d60c4')
        cpu.call('fn_basic__display_decode')


    @fw.function(native=True, address=0xD60FC)
    def hook_display_decode_d60fc():
        cpu.label('hook_display_decode_d60fc')
        cpu.call('fn_basic__display_decode')


    @fw.function(native=True, address=0xD6248)
    def hook_display_decode_d6248():
        cpu.label('hook_display_decode_d6248')
        cpu.call('fn_basic__display_decode')


    @fw.function(native=True, address=0xD6994)
    def hook_display_decode_d6994():
        cpu.label('hook_display_decode_d6994')
        cpu.call('fn_basic__display_decode')


    @fw.function(native=True, address=0xD6B1E)
    def hook_display_decode_d6b1e():
        cpu.label('hook_display_decode_d6b1e')
        cpu.call('fn_basic__display_decode')


    @fw.function(native=True, address=0xD7104)
    def hook_display_decode_d7104():
        cpu.label('hook_display_decode_d7104')
        cpu.call('fn_basic__display_decode')


    @fw.function(native=True, address=0xD7236)
    def hook_display_decode_d7236():
        cpu.label('hook_display_decode_d7236')
        cpu.call('fn_basic__display_decode')


    @fw.function(native=True, address=0xDF550)
    def hook_native_menu_key_df550():
        cpu.label('hook_native_menu_key_df550')
        cpu.jump('fn_basic__native_menu_key')


    @fw.function(native=True, address=0xDFC02)
    def hook_spell_dfc02():
        cpu.label('hook_spell_dfc02')
        cpu.jump('fn_basic__spell')


    @fw.function(native=True, address=0xCFA0E)
    def hook_graph_mode_cfa0e():
        cpu.jump('fn_graph_mode_gate')


    @fw.function(native=True, address=0xE5FCE)
    def hook_scan_if_e5fce():
        cpu.label('hook_scan_if_e5fce')
        cpu.jump('fn_basic__scan_if')


    @fw.function(native=True, address=0xE6060)
    def hook_scan_else_e6060():
        cpu.label('hook_scan_else_e6060')
        cpu.jump('fn_basic__scan_else')


    @fw.function(native=True, address=0xE662C)
    def hook_scan_for_e662c():
        cpu.label('hook_scan_for_e662c')
        cpu.jump('fn_basic__scan_for')


    @fw.function(native=True, address=0xE6876)
    def hook_scan_while_e6876():
        cpu.label('hook_scan_while_e6876')
        cpu.jump('fn_basic__scan_while')


    @fw.function(native=True, address=0xE6BC4)
    def hook_scan_break_e6bc4():
        cpu.label('hook_scan_break_e6bc4')
        cpu.jump('fn_basic__scan_break')


    @fw.function(native=True, address=0xE6F9C)
    def hook_scan_goto_e6f9c():
        cpu.label('hook_scan_goto_e6f9c')
        cpu.jump('fn_basic__scan_goto')
