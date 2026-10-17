"""Source-only, fixed-layout e5800p firmware patches.

patchset.py defines PATCHSET, a dictionary containing:
  firmware (``e5800p``), flash_base, flash_size;
  original_image_sha256: whole original image, for identification only;
  original_firmware_sha256, result_firmware_sha256: SHA256 of physical
    [0, 0x4000) + [0x40000, 0x80000), excluding native user banks;
  regions: changed owned intervals, each with name, cpu_start, physical_start,
    size, reserved_stop (exclusive CPU address), kind (code/data), source
    (relative .asm path), and original_sha256 (original interval bytes).

The module is trusted executable Python, loaded with runpy.run_path.
Native user banks are fixed at [0x4000, 0x40000), and the checksum at physical
0x7fffe: the unsigned byte sum of [0x40000, 0x7fffe), modulo 65536, stored
little-endian. Neither original bytes nor checksum bytes are exported.
Each ASM file is an actual build input;
its assembled size must stay fixed (use explicit DB padding if needed).
The release result digest is informational so valid source edits are accepted.

export_patchset returns the written PATCHSET dictionary. Optional region labels
are absolute CPU addresses; symbols supplies named external addresses for EQU.
build_patchset returns bytes and, if supplied, extends map_regions with the
existing six-field region records, including native_checksum. Unchanged
intervals are not included in that map. patchset_inputs returns absolute
patchset.py/ASM paths for output collision checks using the same validation.
"""

import hashlib
import re
import runpy
from pathlib import Path

from nxu8_asm import assemble, disassemble


FLASH_BASE = 0x80000
FLASH_SIZE = 0x80000
MAP_FIELDS = ('name', 'cpu_start', 'physical_start', 'size', 'reserved_stop', 'kind')
CHECKSUM_REGION = dict(name='native_checksum', cpu_start=0xffffe,
                       physical_start=0x7fffe, size=2, reserved_stop=0x100000,
                       kind='data')


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _fingerprint(image):
    return _sha(image[:0x4000] + image[0x40000:])


def _checksum(image):
    return (sum(image[0x40000:0x7fffe]) & 0xffff).to_bytes(2, 'little')


def _digest(value):
    if (not isinstance(value, str) or len(value) != 64
            or any(c not in '0123456789abcdef' for c in value)):
        raise ValueError('Invalid SHA256 digest')
    return value


def _identifier(name):
    return isinstance(name, str) and re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', name)


def _regions(regions):
    if not isinstance(regions, list):
        raise ValueError('Expected a region list')
    result = []
    names = set()
    for row in regions:
        if not isinstance(row, dict) or any(key not in row for key in MAP_FIELDS):
            raise ValueError('Incomplete region record')
        name = row['name']
        if (not _identifier(name) or name.casefold() in names
                or name.upper() in {'CON', 'PRN', 'AUX', 'NUL'}
                or re.fullmatch(r'(?:COM|LPT)[1-9]', name, re.I)):
            raise ValueError('Invalid or duplicate region name')
        names.add(name.casefold())
        if any(type(row[key]) is not int for key in MAP_FIELDS[1:5]):
            raise ValueError(f'Invalid region address or size: {name}')
        cpu, start, size, stop = (row[key] for key in MAP_FIELDS[1:5])
        if (size <= 0 or start < 0 or start + size > FLASH_SIZE
                or cpu != FLASH_BASE + start
                or not cpu + size <= stop <= FLASH_BASE + FLASH_SIZE):
            raise ValueError(f'Region out of bounds: {name}')
        if row['kind'] not in ('code', 'data'):
            raise ValueError(f'Invalid region kind: {name}')
        if row['kind'] == 'code':
            if cpu & 1:
                raise ValueError(f'Odd code address: {name}')
            if cpu >> 16 != (cpu + size - 1) >> 16:
                raise ValueError(f'Code crosses a segment: {name}')
        if start < 0x40000 and start + size > 0x4000:
            raise ValueError(f'Region overlaps native user banks: {name}')
        if name == 'native_checksum':
            if any(row[key] != CHECKSUM_REGION[key] for key in MAP_FIELDS):
                raise ValueError('Invalid native checksum region')
        elif start + size > 0x7fffe:
            raise ValueError(f'Region overlaps native checksum: {name}')
        if not isinstance(row.get('description', ''), str):
            raise ValueError(f'Invalid region description: {name}')
        labels = row.get('labels', {})
        if not isinstance(labels, dict):
            raise ValueError(f'Invalid region labels: {name}')
        local = {name.casefold(): cpu}
        for label, address in labels.items():
            if (not _identifier(label) or type(address) is not int
                    or not cpu <= address <= cpu + size
                    or (label.casefold() in local
                        and (label != name or address != cpu))):
                raise ValueError(f'Invalid or duplicate label in {name}: {label}')
            local[label.casefold()] = address
        result.append(dict(row))
    result.sort(key=lambda row: row['physical_start'])
    for left, right in zip(result, result[1:]):
        if left['physical_start'] + left['size'] > right['physical_start']:
            raise ValueError(f"Region overlap: {left['name']} and {right['name']}")
    return result


def _source_path(directory, source):
    # Restrict to portable relative paths, including on non-Windows hosts.
    if (not isinstance(source, str) or not source or '\\' in source or ':' in source
            or any(ord(c) < 32 or ord(c) == 127 for c in source)
            or any(part in ('', '.', '..') or part.endswith((' ', '.'))
                   for part in source.split('/'))
            or not source.endswith('.asm')):
        raise ValueError('Invalid assembly source path')
    path = directory / source
    root = directory.resolve()
    if not path.resolve().is_relative_to(root):
        raise ValueError('Assembly source path escapes patch directory')
    current = path
    while current != directory:
        if current.is_symlink():
            raise ValueError('Assembly source path must not use symlinks')
        current = current.parent
    return path


def _data_lines(data):
    for pos in range(0, len(data), 16):
        block = data[pos:pos + 16]
        parts, index = [], 0
        while index < len(block):
            stop = index
            while stop < len(block) and 32 <= block[stop] <= 126:
                stop += 1
            if stop > index:
                text = block[index:stop].decode('ascii').replace('"', '""')
                parts.append(f'"{text}"')
                index = stop
            else:
                parts.append(f'0x{block[index]:02X}')
                index += 1
        yield 'DB ' + ', '.join(parts)


def _assembly_source(row, data, symbols):
    cpu = row['cpu_start']
    end = cpu + len(data)
    labels = {row['name']: cpu}
    labels.update(row.get('labels', {}))
    names = {name.casefold() for name in labels}
    external = {}
    # A split can expose another branch hidden in a macro, so collect targets
    # until every in-region target has its own instruction/data boundary.
    while True:
        boundaries = sorted({cpu, end, *labels.values()})
        records = []
        for start, stop in zip(boundaries, boundaries[1:]):
            block = data[start - cpu:stop - cpu]
            if row['kind'] == 'code':
                records.extend(disassemble(block, start))
            else:
                records.append(dict(address=start, text='\n'.join(_data_lines(block))))
        targets = {}
        for item in records:
            match = re.fullmatch(r'(\w+) 0x([0-9A-F]+):0x([0-9A-F]+)', item['text'])
            if match:
                targets[item['address']] = (match[1], int(match[2], 16) * 65536 + int(match[3], 16))
        added = False
        addresses = set(labels.values())
        for _, target in targets.values():
            if cpu <= target <= end and target not in addresses:
                name = f'branch_{target - cpu:04x}'
                while name.casefold() in names or name.casefold() in symbols:
                    name += '_'
                labels[name] = target
                names.add(name.casefold())
                addresses.add(target)
                added = True
        if not added:
            break
    by_address = {}
    for name, address in labels.items():
        by_address.setdefault(address, []).append(name)
    for item in records:
        if item['address'] not in targets:
            continue
        mnemonic, target = targets[item['address']]
        if target in by_address:
            item['text'] = f'{mnemonic} {by_address[target][0]}'
        else:
            for name, address in symbols.values():
                if address == target:
                    if name.casefold() in names:
                        raise ValueError(f"External symbol conflicts with label in {row['name']}: {name}")
                    external[name] = address
                    item['text'] = f'{mnemonic} {name}'
                    break
    lines = [f"; {row['name']}"]
    description = row.get('description', '').strip().split('\n\n', 1)[0]
    lines.extend(f'; {line.strip()}' for line in description.splitlines())
    lines.append(f"; CPU 0x{cpu:05X}, physical 0x{row['physical_start']:05X}, {len(data)} bytes")
    lines.extend(f'{name} EQU 0x{address:05X}' for name, address in external.items())
    lines.append('')
    for item in records:
        lines.extend(f'{name}:' for name in by_address.get(item['address'], []))
        lines.append(item['text'])
    lines.extend(f'{name}:' for name in by_address.get(end, []))
    return '\n'.join(lines) + '\n'


def _patchset_source(patchset):
    lines = ['"""e5800p fixed-layout firmware patch description.',
             '',
             'Trusted executable Python; load only sources you trust.',
             'Edit the named ASM files; each region must retain its declared size.',
             '"""', '', 'PATCHSET = {',
             f"    'firmware': {patchset['firmware']!r},",
             f"    'flash_base': 0x{patchset['flash_base']:X},",
             f"    'flash_size': 0x{patchset['flash_size']:X},",
             '    # Original firmware is required; native user banks are preserved.']
    for key in ('original_image_sha256', 'original_firmware_sha256'):
        lines.append(f'    {key!r}: {patchset[key]!r},')
    lines.append('    # Release reference only: edited assembly may change this digest.')
    lines.append(f"    'result_firmware_sha256': {patchset['result_firmware_sha256']!r},")
    lines.append("    'regions': [")
    for row in patchset['regions']:
        lines.append('        {')
        for key, value in row.items():
            text = f'0x{value:X}' if type(value) is int else repr(value)
            lines.append(f'            {key!r}: {text},')
        lines.append('        },')
    lines.extend(['    ],', '}', ''])
    return '\n'.join(lines)


def export_patchset(original: bytes, image: bytes, regions: list[dict], directory: Path,
                    *, symbols: dict[str, int] | None = None) -> dict:
    """Export named ASM and trusted patchset.py; refuse unexplained bytes/overwrites."""
    if len(original) != FLASH_SIZE or len(image) != FLASH_SIZE:
        raise ValueError('Expected 512 KiB firmware images')
    rows = _regions(regions)
    addresses = {}
    if symbols is not None and not isinstance(symbols, dict):
        raise ValueError('Expected a symbol dictionary')
    for name, address in (symbols or {}).items():
        if (not _identifier(name) or type(address) is not int
                or not 0 <= address <= 0xfffff or name.casefold() in addresses):
            raise ValueError(f'Invalid or duplicate external symbol: {name}')
        addresses[name.casefold()] = (name, address)
    for row in rows:
        name, address = row['name'], row['cpu_start']
        if name.casefold() in addresses and addresses[name.casefold()][1] != address:
            raise ValueError(f'Conflicting region symbol: {name}')
        addresses.setdefault(name.casefold(), (name, address))
    if image[0x7fffe:] != _checksum(image):
        raise ValueError('Incorrect native checksum in target image')
    if original[0x4000:0x40000] != image[0x4000:0x40000]:
        raise ValueError('Target changes native user banks')
    directory = Path(directory).absolute()
    manifest_path = directory / 'patchset.py'
    existing = {path.name.casefold() for path in directory.iterdir()} if directory.exists() else set()
    if manifest_path.name.casefold() in existing:
        raise ValueError('Patch description already exists')
    manifest = dict(firmware='e5800p', flash_base=FLASH_BASE,
                    flash_size=FLASH_SIZE, original_image_sha256=_sha(original),
                    original_firmware_sha256=_fingerprint(original),
                    result_firmware_sha256=_fingerprint(image), regions=[])
    covered = bytearray(FLASH_SIZE)
    covered[0x7fffe:] = b'\x01\x01'
    sources = []
    for row in rows:
        start, size = row['physical_start'], row['size']
        if row['name'] == 'native_checksum':
            continue
        old, data = original[start:start + size], image[start:start + size]
        if data == old:
            continue
        covered[start:start + size] = b'\x01' * size
        source = f"{row['name']}.asm"
        path = _source_path(directory, source)
        if source.casefold() in existing:
            raise ValueError(f'Assembly source already exists: {source}')
        cpu = row['cpu_start']
        text = _assembly_source(row, data, addresses)
        encoded, _, _ = assemble(text, cpu)
        if encoded != data:
            raise ValueError(f"Assembly roundtrip failed: {row['name']}")
        entry = {key: row[key] for key in MAP_FIELDS}
        entry.update(source=source, original_sha256=_sha(old))
        manifest['regions'].append(entry)
        sources.append((path, text))
    for pos, (old, new) in enumerate(zip(original, image)):
        if old != new and not covered[pos]:
            raise ValueError(f'Unexplained firmware change at physical 0x{pos:05x}')
    text = _patchset_source(manifest)
    directory.mkdir(parents=True, exist_ok=True)
    for path, source in sources:
        with path.open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(source)
    with manifest_path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(text)
    return manifest


def _load_patchset(directory):
    directory = Path(directory).absolute()
    manifest_path = directory / 'patchset.py'
    if manifest_path.is_symlink():
        raise ValueError('Patch description must not be a symlink')
    manifest = runpy.run_path(str(manifest_path)).get('PATCHSET')
    if (not isinstance(manifest, dict) or manifest.get('firmware') != 'e5800p'
            or type(manifest.get('flash_base')) is not int
            or type(manifest.get('flash_size')) is not int
            or manifest.get('flash_base') != FLASH_BASE
            or manifest.get('flash_size') != FLASH_SIZE):
        raise ValueError('Unsupported patch description')
    for key in ('original_image_sha256', 'original_firmware_sha256', 'result_firmware_sha256'):
        _digest(manifest.get(key))
    inputs = [manifest_path]
    rows = _regions(manifest.get('regions'))
    paths = {manifest_path.resolve().as_posix().casefold()}
    for row in rows:
        if row['name'] == 'native_checksum':
            raise ValueError('Native checksum must not have an assembly source')
        _digest(row.get('original_sha256'))
        path = _source_path(directory, row.get('source'))
        key = path.resolve().as_posix().casefold()
        if key in paths:
            raise ValueError('Duplicate assembly source path')
        paths.add(key)
        inputs.append(path)
    return manifest, rows, inputs


def patchset_inputs(directory: Path) -> list[Path]:
    """Return trusted Python description and ASM input paths after validation."""
    return _load_patchset(directory)[2]


def build_patchset(base: bytes, directory: Path, *, map_regions=None) -> bytes:
    """Assemble a patchset against its original firmware, preserving user banks."""
    if len(base) != FLASH_SIZE:
        raise ValueError('Expected a 512 KiB source image')
    manifest, rows, inputs = _load_patchset(directory)
    if _fingerprint(base) != manifest['original_firmware_sha256']:
        raise ValueError('Source firmware version mismatch')
    patches = []
    for row, path in zip(rows, inputs[1:]):
        start, size = row['physical_start'], row['size']
        if _sha(base[start:start + size]) != row['original_sha256']:
            raise ValueError(f"Original region hash mismatch: {row['name']}")
        data, _, _ = assemble(path.read_text(encoding='utf-8'), row['cpu_start'])
        if len(data) != size:
            raise ValueError(f"Assembly size mismatch: {row['name']} needs {size} bytes, got {len(data)}")
        patches.append((start, data))
    result = bytearray(base)
    for start, data in patches:
        result[start:start + len(data)] = data
    result[0x7fffe:] = _checksum(result)
    if map_regions is not None:
        map_regions.extend({key: row[key] for key in MAP_FIELDS} for row in rows)
        map_regions.append(dict(CHECKSUM_REGION))
    return bytes(result)
