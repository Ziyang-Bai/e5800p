"""Place Python functions and signature-checked patches in owned Flash areas."""

import hashlib
import sys
from pathlib import Path

from .model import Function


FLASH_BASE = 0x80000
FLASH_SIZE = 0x80000
FOOTER = 0xfffe0


def _span(address, size, name, *, code=False):
    if type(address) is not int or not FLASH_BASE <= address < FOOTER:
        raise ValueError(f'{name}: address must be in Flash below the native footer')
    if size <= 0 or address + size > FOOTER:
        raise ValueError(f'{name}: range overlaps the native footer or exceeds Flash')
    if code and (address & 1 or size & 1):
        raise ValueError(f'{name}: code address and size must be even')
    if code and address >> 16 != (address + size - 1) >> 16:
        raise ValueError(f'{name}: code crosses a bank boundary')


def _bytes(value, name):
    if not isinstance(value, (bytes, bytearray, memoryview)):
        raise TypeError(f'{name} must be bytes')
    return bytes(value)


def _digest(value):
    if (not isinstance(value, str) or len(value) != 64
            or any(c not in '0123456789abcdef' for c in value)):
        raise ValueError('Invalid SHA256 digest')


class Firmware:
    """A single Python source's functions, writable intervals and exact patches."""

    def __init__(self, name, *, regions=(), original_firmware_sha256=None,
                 original_regions=()):
        if not isinstance(name, str) or not name:
            raise ValueError('Firmware name must be a nonempty string')
        self.name = name
        self.functions = []
        self.original_firmware_sha256 = original_firmware_sha256
        if original_firmware_sha256 is not None:
            _digest(original_firmware_sha256)
        self.original_regions = tuple(dict(row) for row in original_regions)
        names = set()
        for row in self.original_regions:
            name = row['name']
            if not isinstance(name, str) or not name or name in names:
                raise ValueError('Invalid or duplicate original region name')
            names.add(name)
            if row['kind'] not in ('code', 'data'):
                raise ValueError(f'{name}: invalid region kind')
            _span(row['cpu_start'], row['size'], name, code=row['kind'] == 'code')
            if (row['physical_start'] != row['cpu_start'] - FLASH_BASE
                    or not row['cpu_start'] + row['size'] <= row['reserved_stop'] <= FOOTER):
                raise ValueError(f'{name}: invalid original region bounds')
            if row['cpu_start'] < 0xc0000 and row['cpu_start'] + row['size'] > 0x84000:
                raise ValueError(f'{name}: region overlaps native user banks')
            _digest(row['original_sha256'])
        ordered = sorted(self.original_regions, key=lambda row: row['cpu_start'])
        for left, right in zip(ordered, ordered[1:]):
            if left['cpu_start'] + left['size'] > right['cpu_start']:
                raise ValueError('Original regions overlap')
        intervals = []
        for start, stop in regions:
            if type(start) is not int or type(stop) is not int:
                raise ValueError('Region endpoints must be integer CPU addresses')
            _span(start, stop - start, 'region')
            intervals.append((start, stop))
        self.regions = tuple(sorted(intervals))
        for left, right in zip(self.regions, self.regions[1:]):
            if left[1] > right[0]:
                raise ValueError('Writable regions overlap')
        self._patches = []
        self._hooks = []
        self._data = []
        self._sources = {sys._getframe(1).f_code.co_filename}

    def function(self, fn=None, *, address=None, native=False):
        """Register a function, optionally at a fixed full CPU code address."""
        if type(native) is not bool:
            raise TypeError('Function native must be a bool')
        if address is not None:
            _span(address, 2, 'function', code=True)

        def register(fn):
            if not callable(fn) or not hasattr(fn, '__code__'):
                raise TypeError('Firmware functions must be Python functions')
            if (any(item.name == fn.__name__ for item in self.functions)
                    or any(item['name'] == fn.__name__ for item in self._data)):
                raise ValueError(f'Duplicate function name: {fn.__name__}')
            result = Function(fn, self, address, native=native)
            self.functions.append(result)
            self._sources.add(fn.__code__.co_filename)
            return result

        return register if fn is None else register(fn)

    def data(self, name, value, *, address, labels=None):
        """Place a named constant table at a fixed CPU data address."""
        if not isinstance(name, str) or not name:
            raise ValueError('Data name must be a nonempty string')
        if (any(fn.name == name for fn in self.functions)
                or any(item['name'] == name for item in self._data)):
            raise ValueError(f'Duplicate data name: {name}')
        value = _bytes(value, name)
        _span(address, len(value), name)
        labels = dict(labels or {})
        for label, offset in labels.items():
            if (not isinstance(label, str) or not label or type(offset) is not int
                    or not 0 <= offset <= len(value)):
                raise ValueError(f'{name}: invalid data label')
        self._data.append(dict(name=name, address=address, data=value, labels=labels))
        self._sources.add(sys._getframe(1).f_code.co_filename)

    def patch(self, address, data, *, expected):
        """Replace bytes only when the original image matches the signature."""
        data, expected = _bytes(data, 'data'), _bytes(expected, 'expected')
        _span(address, len(data), 'patch')
        if len(data) != len(expected):
            raise ValueError('Patch signature length must match replacement length')
        self._patches.append((address, data, expected))

    def hook(self, address, target, *, expected, call=True):
        """Install a four-byte far CALL or JMP to a function or CPU address."""
        _span(address, 4, 'hook', code=True)
        expected = _bytes(expected, 'expected')
        if len(expected) != 4:
            raise ValueError('Hook signature must contain exactly four bytes')
        if type(call) is not bool:
            raise TypeError('Hook call must be a bool')
        if isinstance(target, Function):
            if target.owner is not self or not any(target is fn for fn in self.functions):
                raise ValueError('Hook target must be registered in this firmware')
        elif (type(target) is not int or not 0 <= target <= 0xfffff
              or target & 1 or target >> 16 not in (0, 1, 8, 9, 10, 11, 12, 13, 14, 15)):
            raise ValueError('Hook target must be an even executable CPU address')
        self._hooks.append((address, target, expected, call))

    def link(self):
        """Size, place and compile functions without reading or writing an image."""
        occupied = []

        def reserve(address, size, name):
            stop = address + size
            for start, end, other in occupied:
                if address < end and start < stop:
                    raise ValueError(f'{name} overlaps {other}')
            occupied.append((address, stop, name))
            occupied.sort()

        def fits(address, size):
            return any(start <= address and address + size <= stop
                       for start, stop in self.regions)

        for address, data, _ in self._patches:
            reserve(address, len(data), f'patch_{address:05x}')
        for address, _, _, _ in self._hooks:
            reserve(address, 4, f'hook_{address:05x}')
        for item in self._data:
            if not fits(item['address'], len(item['data'])):
                raise ValueError(f"{item['name']}: fixed data is outside declared regions")
            reserve(item['address'], len(item['data']), item['name'])

        sizes, addresses = {}, {}
        if self.functions:
            from .compiler import compile_function

            dummy = {fn.symbol: fn.address if fn.address is not None else FLASH_BASE
                     for fn in self.functions}
            for fn in self.functions:
                data, _ = compile_function(fn, dummy[fn.symbol], dummy)
                if not data or len(data) & 1 or len(data) > 0x10000:
                    raise ValueError(f'{fn.name}: invalid compiled code size')
                sizes[fn.symbol] = len(data)

            # Fixed entries and patches occupy space before any first-fit allocation.
            for fn in self.functions:
                if fn.address is None:
                    continue
                size = sizes[fn.symbol]
                _span(fn.address, size, fn.name, code=True)
                if not fits(fn.address, size):
                    raise ValueError(f'{fn.name}: fixed function is outside declared regions')
                reserve(fn.address, size, fn.name)
                addresses[fn.symbol] = fn.address

            for fn in self.functions:
                if fn.address is not None:
                    continue
                size = sizes[fn.symbol]
                address = None
                for start, stop in self.regions:
                    candidate = (start + 1) & ~1
                    while candidate + size <= stop:
                        if candidate >> 16 != (candidate + size - 1) >> 16:
                            candidate = ((candidate >> 16) + 1) << 16
                            continue
                        conflict = next((end for left, end, _ in occupied
                                         if candidate < end and left < candidate + size), None)
                        if conflict is not None:
                            candidate = (conflict + 1) & ~1
                            continue
                        address = candidate
                        break
                    if address is not None:
                        break
                if address is None:
                    raise ValueError(f'{fn.name}: needs {size} bytes; no contiguous space in declared regions')
                reserve(address, size, fn.name)
                addresses[fn.symbol] = address

        blocks = []
        for fn in self.functions:
            address = addresses[fn.symbol]
            data, source = compile_function(fn, address, addresses)
            if len(data) != sizes[fn.symbol]:
                raise ValueError(f'{fn.name}: compiled size changed after placement')
            blocks.append(dict(name=fn.name, address=address, data=data, source=source,
                               kind='code'))
        for item in self._data:
            source = '\n'.join('DB ' + ','.join(f'0x{byte:02x}' for byte in item['data'][i:i + 16])
                               for i in range(0, len(item['data']), 16))
            blocks.append(dict(name=item['name'], address=item['address'],
                               data=item['data'], source=source, kind='data'))
        for address, data, _ in self._patches:
            source = '\n'.join('DB ' + ','.join(f'0x{byte:02x}' for byte in data[i:i + 16])
                               for i in range(0, len(data), 16))
            blocks.append(dict(name=f'patch_{address:05x}', address=address,
                               data=data, source=source, kind='data'))
        if self._hooks:
            from nxu8_asm import assemble

            for address, target, _, call in self._hooks:
                target = addresses[target.symbol] if isinstance(target, Function) else target
                # A symbol forces absolute addressing even for ROM0 targets below 0x10000.
                source = f'TARGET EQU 0x{target:05x}\n' + ('CALL' if call else 'JMP') + ' TARGET'
                data, _, _ = assemble(source, address)
                blocks.append(dict(name=f'hook_{address:05x}', address=address,
                                   data=data, source=source, kind='code'))
        symbols = {fn.name: addresses[fn.symbol] for fn in self.functions}
        for item in self._data:
            symbols[item['name']] = item['address']
            symbols.update({item['name'] + '__' + label: item['address'] + offset
                            for label, offset in item['labels'].items()})
        return dict(blocks=sorted(blocks, key=lambda block: block['address']),
                    symbols=symbols)

    def image(self, original):
        """Compile onto original bytes, checking version and owned-span signatures."""
        from casio_tool import flash_checksum

        if len(original) != FLASH_SIZE:
            raise ValueError('Firmware input must be a complete 512 KiB Flash image')
        if (self.original_firmware_sha256 is not None
                and hashlib.sha256(original[:0x4000] + original[0x40000:]).hexdigest()
                != self.original_firmware_sha256):
            raise ValueError('Source firmware version mismatch')
        for row in self.original_regions:
            start = row['physical_start']
            if hashlib.sha256(original[start:start + row['size']]).hexdigest() != row['original_sha256']:
                raise ValueError(f"Original region hash mismatch: {row['name']}")
        linked = self.link()
        metadata = {row['name']: row for row in self.original_regions}
        if metadata and set(metadata) != {block['name'] for block in linked['blocks']}:
            raise ValueError('Compiled blocks do not match original regions')
        regions = []
        for block in linked['blocks']:
            address, size = block['address'], len(block['data'])
            row = metadata.get(block['name'])
            if row is not None:
                if (address != row['cpu_start'] or size != row['size']
                        or block['kind'] != row['kind']):
                    raise ValueError(f"{block['name']}: compiled region does not match fixed layout")
                stop = row['reserved_stop']
            else:
                stop = next((end for start, end in self.regions
                             if start <= address and address + size <= end), address + size)
            regions.append(dict(name=block['name'], cpu_start=address,
                                physical_start=address - FLASH_BASE, size=size,
                                reserved_stop=stop, kind=block['kind']))
        signatures = [(address, expected) for address, _, expected in self._patches]
        signatures.extend((address, expected) for address, _, expected, _ in self._hooks)
        for address, expected in signatures:
            offset = address - FLASH_BASE
            if original[offset:offset + len(expected)] != expected:
                raise ValueError(f'Original signature mismatch at {address:#07x}')
        image = bytearray(original)
        for block in linked['blocks']:
            offset = block['address'] - FLASH_BASE
            image[offset:offset + len(block['data'])] = block['data']
        image[-2:] = flash_checksum(image).to_bytes(2, 'little')
        regions.append(dict(name='native_checksum', cpu_start=0xffffe,
                            physical_start=0x7fffe, size=2, reserved_stop=0x100000,
                            kind='data'))
        return bytes(image), dict(linked, regions=regions)

    def source_inputs(self):
        """Include sibling Python tables as well as registered function sources."""
        paths = {Path(path).resolve() for path in self._sources if not path.startswith('<')}
        for parent in {path.parent for path in paths}:
            paths.update(parent.glob('*.py'))
        return sorted(paths)

    def build(self, original, output, *, listing=None, clean=None, map_path=None):
        """Write an image; upgrades replace firmware while retaining native user banks."""
        from casio_tool import flash_checksum, output_paths, write_json

        for path in (output, listing, map_path):
            if path is not None:
                Path(path).parent.mkdir(parents=True, exist_ok=True)
        output_paths([original, clean, *self.source_inputs()], [output, listing, map_path])
        base = Path(original).read_bytes()
        if len(base) != FLASH_SIZE:
            raise ValueError('Firmware input must be a complete 512 KiB Flash image')
        image, linked = self.image(Path(clean).read_bytes() if clean is not None else base)
        if clean is not None:
            if any(row['physical_start'] < 0x40000
                   and row['physical_start'] + row['size'] > 0x4000
                   for row in linked['regions']):
                raise ValueError('Upgrade regions overlap native user banks')
            # Reconstruct all firmware-owned banks from clean, including retired spans.
            image = bytearray(image[:0x4000] + base[0x4000:0x40000] + image[0x40000:])
            image[0x7ffe0:0x7fffe] = base[0x7ffe0:0x7fffe]
            image[-2:] = flash_checksum(image).to_bytes(2, 'little')
        text = f'; {self.name}: diagnostic assembly, not a build input\n'
        if listing is not None:
            for block in linked['blocks']:
                text += (f'\n; {block["name"]}, {len(block["data"])} bytes\n'
                         f'ORG 0x{block["address"]:05x}\n{block["source"].rstrip()}\n')
        Path(output).write_bytes(image)
        if listing is not None:
            Path(listing).write_text(text, encoding='utf-8')
        if map_path is not None:
            write_json(map_path, {'regions': linked['regions']})
        return dict(linked, output=str(output), sha256=hashlib.sha256(image).hexdigest())
