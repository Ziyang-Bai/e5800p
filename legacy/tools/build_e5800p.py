"""Generate e5800p extensions from a matching original fx-5800P Flash image."""

import hashlib
import sys

import basic_native
import flash_layout
import sector_journal

from graph_code import CODE
from address_input import address_code
from basic_mode import basic_code, basic_patches
from basic_memory import memory_code
from basic_graphics import graphics_code
from basic_flash import flash_code
from basic_asm import asm_code
from flash_layout import (
    BASIC_RESERVED, CHECKSUM_ADDRESS, FLASH_BASE, FLASH_SIZE, FOOTER_ADDRESS,
    INSTRUCTION_NAMES_ADDRESS, INSTRUCTION_RECORDS_ADDRESS, LEGACY_PAYLOAD_LIMIT,
    LOGO_BITMAP_ADDRESS, S0_GAPS, SMALL_GLYPHS_ADDRESS, SMALL_TABLE_ADDRESS,
    UI_STRINGS_ADDRESS, reserved_stop,
)
from isa_menu import isa_code
from instruction_codec import codec_code
from instruction_table import instruction_table_code
from instruction_insert import batch_code
from instruction_view import view_code
from page_editor import editor_code
from mode_selector import ORIGINAL_PROLOGUE, PROG_ENTRY, SELECTOR_ADDRESS, selector_code
from program_mode import program_code
from sector_journal import journal_code
from small_font import small_font_code
from shutdown_logo import LOGO_ADDRESS, SAVE_ENTRY, SAVE_PROLOGUE, logo_code, read_logo
from ui_text import DATA_SPANS, TEXT, ui_text_code
from scanner import scanner_code
from u8_emit import LABELS

SOURCE_FIRMWARE_SHA256 = '7a3fb0a93857de3fcd17fc146329409b027d755760e49093a3230a767f004567'
DATA_ADDRESSES = {
    INSTRUCTION_RECORDS_ADDRESS, INSTRUCTION_NAMES_ADDRESS,
    SMALL_TABLE_ADDRESS, SMALL_GLYPHS_ADDRESS, LOGO_BITMAP_ADDRESS, UI_STRINGS_ADDRESS,
}


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _payloads(payload):
    return (payload,) if isinstance(payload[0], int) else payload


def build(base, *, map_regions=None, symbols=None):
    if len(base) != FLASH_SIZE:
        raise ValueError('Expected a 512 KiB source image')
    if _sha(base[:0x4000] + base[0x40000:]) != SOURCE_FIRMWARE_SHA256:
        raise ValueError('Expected the matching original fx-5800P firmware')
    LABELS.clear()
    result = bytearray(base)
    for offset, name, code in CODE:
        result[offset:offset + len(code)] = code
    offset, code = scanner_code()
    if offset != 0x800 or len(code) > 0xe0:
        raise ValueError('Scanner exceeds its allocation')
    result[offset:offset + len(code)] = code

    regions = []

    def record(name, cpu, size, stop, kind):
        if size == 0:
            return
        if kind == 'code' and cpu & 1:
            raise ValueError(f'Odd code address: {name}')
        if cpu < FLASH_BASE or cpu + size > FLASH_BASE + FLASH_SIZE or cpu + size > stop:
            raise ValueError(f'Flash allocation exceeded: {name} at {cpu:05x}')
        if kind == 'code' and cpu >> 16 != (cpu + size - 1) >> 16:
            raise ValueError(f'Code crosses a segment: {name}')
        regions.append(dict(name=name, cpu_start=cpu, physical_start=cpu - FLASH_BASE,
                            size=size, reserved_stop=stop, kind=kind))

    def patch(name, offset, old, new, kind='code'):
        if result[offset:offset + len(old)] != old:
            raise ValueError(f'Unexpected {name} signature')
        result[offset:offset + len(new)] = new
        record(name, FLASH_BASE + offset, len(new), FLASH_BASE + offset + len(new), kind)

    patch('native_table', 0x63694, bytes.fromhex('ce f8 5e fe'), bytes.fromhex('00 f8 00 11'))
    patch('addin_label', 0x73b1e, b'      ', b'Add-in', kind='data')
    patch('native_program', PROG_ENTRY, ORIGINAL_PROLOGUE,
          bytes((0, 0xf0 | (SELECTOR_ADDRESS >> 16), SELECTOR_ADDRESS & 255, (SELECTOR_ADDRESS >> 8) & 255)))
    patch('native_screen_save', SAVE_ENTRY - FLASH_BASE, SAVE_PROLOGUE,
          bytes((0, 0xf0 | (LOGO_ADDRESS >> 16), LOGO_ADDRESS & 255, (LOGO_ADDRESS >> 8) & 255)))
    for address, expected, replacement in basic_patches():
        target = ((replacement[1] & 15) << 16) | int.from_bytes(replacement[2:4], 'little')
        label = next(name for name, value in LABELS[0xf3e68].items() if value == target)
        patch(f'hook_{label}_{address:05x}', address - FLASH_BASE, expected, replacement)
    bitmap = read_logo()
    DATA_SPANS.clear()
    TEXT.data.clear()
    TEXT.strings.clear()
    total = 0
    generators = (
        ('selector', selector_code), ('editor', editor_code), ('journal', journal_code),
        ('isa', isa_code), ('codec', codec_code), ('instructions', instruction_table_code),
        ('batch', batch_code), ('viewer', view_code), ('program', program_code),
        ('address', address_code), ('font', small_font_code), ('logo', lambda: logo_code(bitmap)),
        ('basic', basic_code), ('basic_memory', memory_code),
        ('basic_graphics', graphics_code), ('basic_flash', flash_code), ('basic_asm', asm_code),
    )
    entry_names = {address: name.removesuffix('_ADDRESS').lower()
                   for name, address in vars(flash_layout).items() if name.endswith('_ADDRESS')}
    entry_names[flash_layout.VIEW_ADDRESS] = 'instruction_view'
    entry_names.update({address: 'journal_' + name.strip('_').removesuffix('_ADDRESS').lower()
                        for name, address in vars(sector_journal).items()
                        if type(address) is int and 0x83000 <= address < 0x84000})
    descriptions = {name: generator.__doc__ or sys.modules[generator.__module__].__doc__
                    for name, generator in generators}
    payloads = [(name, offset, bytes(code)) for name, generator in generators
                for offset, code in _payloads(generator())]
    payloads.extend(('ui_text', offset, bytes(code)) for offset, code in ui_text_code())
    installed = []
    for name, offset, code in payloads:
        if not code:
            continue
        cpu = FLASH_BASE + offset
        stop = reserved_stop(cpu)
        if cpu + len(code) > stop:
            raise ValueError(f'{name} needs {len(code)} bytes at {cpu:05x}; limit {stop:05x}')
        is_basic = name == 'basic' or name.startswith('basic_')
        if is_basic:
            if not (any(start <= cpu and cpu + len(code) <= end for start, end in BASIC_RESERVED)
                    or 0x80400 <= cpu < 0x80440):
                raise ValueError(f'Unowned BASIC interval: {name} at {cpu:05x}')
        else:
            if any(start < cpu + len(code) and cpu < end for start, end in BASIC_RESERVED):
                raise ValueError(f'{name} occupies reserved BASIC space')
            if cpu != SELECTOR_ADDRESS and not (0x83000 <= cpu < 0x84000):
                if not (any(start <= cpu and cpu + len(code) <= end for start, end in S0_GAPS)
                        or 0xf7e68 <= cpu < FOOTER_ADDRESS):
                    raise ValueError(f'Unowned Flash interval: {name} at {cpu:05x}')
        if any(a < offset + len(code) and offset < b for a, b in installed):
            raise ValueError(f'Payload overlaps: {name} at {cpu:05x}')
        if any(byte != 0xff for byte in result[offset:offset + len(code)]):
            raise ValueError(f'Code area occupied: {name} at {cpu:05x}')
        installed.append((offset, offset + len(code)))
        result[offset:offset + len(code)] = code
        # Compare the same movable payload set as the old 24,306-byte S4 build.
        if not is_basic and name not in ('selector', 'journal'):
            total += len(code)
        spans = [(cpu, cpu + len(code), 'data' if cpu in DATA_ADDRESSES else 'code')]
        if name in ('basic', 'basic_asm'):
            data_start = LABELS[cpu]['names' if name == 'basic' else 'catalogue']
            spans = [(cpu, data_start, 'code'), (data_start, cpu + len(code), 'data')]
        for data_start, size in DATA_SPANS:
            if cpu <= data_start < cpu + len(code):
                if data_start + size != cpu + len(code):
                    raise ValueError(f'UI constants must end their payload: {name}')
                spans = [(cpu, data_start, 'code'), (data_start, data_start + size, 'data')]
        for index, (start, end, kind) in enumerate(spans):
            region_name = entry_names.get(start, name) if not index else f'{name}_data'
            record(region_name, start, end - start, stop, kind)
            regions[-1]['labels'] = {label: address for label, address in LABELS.get(cpu, {}).items()
                                     if start <= address < end}
            regions[-1]['description'] = descriptions.get(name) or ''
    if total > LEGACY_PAYLOAD_LIMIT:
        raise ValueError(f'Legacy payload {total} exceeds {LEGACY_PAYLOAD_LIMIT} bytes')

    for offset, name, code in CODE:
        record(name, FLASH_BASE + offset, len(code), FLASH_BASE + offset + len(code), 'code')
    offset, code = scanner_code()
    record('scanner', FLASH_BASE + offset, len(code), 0x808e0, 'code')
    regions[-1]['labels'] = LABELS[0x80800]
    regions[-1]['description'] = scanner_code.__doc__
    checksum = sum(result[0x40000:0x7fffe]) & 0xffff
    result[CHECKSUM_ADDRESS - FLASH_BASE:CHECKSUM_ADDRESS - FLASH_BASE + 2] = checksum.to_bytes(2, 'little')
    record('native_checksum', CHECKSUM_ADDRESS, 2, CHECKSUM_ADDRESS + 2, 'data')
    regions.sort(key=lambda r: r['cpu_start'])
    for left, right in zip(regions, regions[1:]):
        if left['cpu_start'] + left['size'] > right['cpu_start']:
            raise ValueError(f"Map overlap: {left['name']} and {right['name']}")
    if result[FOOTER_ADDRESS - FLASH_BASE:CHECKSUM_ADDRESS - FLASH_BASE] != base[FOOTER_ADDRESS - FLASH_BASE:CHECKSUM_ADDRESS - FLASH_BASE]:
        raise ValueError('Native footer changed')
    if symbols is not None:
        symbols.update({
            'rom_read_key': 0x1234e, 'rom_normalize_key': 0x1249c,
            'rom_draw_text': 0x041da, 'rom_refresh': 0x043be,
            'rom_flash_program': 0x04e86, 'rom_flash_erase': 0x04ef4,
        })
        for name in ('EVALUATE', 'EVALUATE_WORKSPACE', 'EVALUATE_CORE', 'TOKEN_FETCH',
                     'TOKEN_DECODE', 'TOKEN_ADMISSION', 'NUMBER_COPY', 'ERROR_WRITE',
                     'STATEMENT', 'STATEMENT_FINISH', 'SOURCE_OPEN', 'SOURCE_ACTIVATE',
                     'PROGRAM_EDITOR', 'PROGRAM_FUNCTION', 'PROGRAM_LOOKUP',
                     'PROGRAM_CREATE', 'PROGRAM_INSERT', 'PROGRAM_DELETE',
                     'PROGRAM_SERIALIZE', 'LIBRARY_LOOKUP'):
            symbols['native_' + name.lower()] = getattr(basic_native, name)
        symbols.update({name.lower(): value for name, value in vars(flash_layout).items()
                        if name.endswith('_ADDRESS')})
        for row in regions:
            symbols[row['name']] = row['cpu_start']
            symbols.update({row['name'] + '__' + name: address
                            for name, address in row.get('labels', {}).items()})
    if map_regions is not None:
        map_regions.extend(regions)
    return bytes(result)
