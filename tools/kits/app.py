"""Fixed-address application packages and the S4 application directory."""

import struct
import zlib

from .firmware import FLASH_BASE, FLASH_SIZE


S4_OFFSET = 0x10000
S4_SIZE = 0x10000
S4_ADDRESS = 0x90000
APP_START = 0x90100
APP_STOP = 0x9fff0
HEADER_SIZE = 44
DIRECTORY_SIZE = 16
_HEADER = struct.Struct('<4sHHIIIHHB3s12sI')
_DIRECTORY = struct.Struct('<4sHHII')


def _crc(header, payload):
    return zlib.crc32(payload, zlib.crc32(header[:40]))


def _read_header(header):
    if len(header) != HEADER_SIZE:
        raise ValueError('Truncated application header')
    (magic, version, size, address, entry, length, work, stack,
     name_len, reserved, name, crc) = _HEADER.unpack(header)
    if magic != b'E5AP' or version != 1 or size != HEADER_SIZE:
        raise ValueError('Invalid application format')
    if (reserved != b'\0' * 3 or not 1 <= name_len <= 12
            or any(byte < 0x20 or byte > 0x5f for byte in name[:name_len])
            or name[name_len:] != b'\0' * (12 - name_len)):
        raise ValueError('Invalid application name or reserved bytes')
    name = name[:name_len].decode('ascii')
    if not length or not APP_START <= address < address + length <= APP_STOP:
        raise ValueError(f'{name}: payload must fit in [{APP_START:#07x}, {APP_STOP:#07x})')
    if entry >= length or (address + entry) & 1:
        raise ValueError(f'{name}: entry must be even and inside the payload')
    return dict(name=name, format=version, header_size=size, load_address=address,
                entry_offset=entry, payload_size=length, work_bytes=work,
                stack_bytes=stack, name_len=name_len, crc32=crc, header=bytes(header))


def read_app(data):
    """Decode a complete package, rejecting changed headers or payloads."""
    row = _read_header(data[:HEADER_SIZE])
    if len(data) != HEADER_SIZE + row['payload_size']:
        raise ValueError(f"{row['name']}: package size does not match its header")
    row['payload'] = bytes(data[HEADER_SIZE:])
    if _crc(row['header'], row['payload']) != row['crc32']:
        raise ValueError(f"{row['name']}: application CRC mismatch")
    return row


def build_app(fw, *, entry='main', work_bytes=0, stack_bytes):
    """Link a Firmware project without a base image and return package and listing."""
    for name, value in (('work_bytes', work_bytes), ('stack_bytes', stack_bytes)):
        if type(value) is not int or not 0 <= value <= 0xffff:
            raise ValueError(f'{name} must be an integer from 0 to 65535')
    if (not 1 <= len(fw.name) <= 12
            or any(not 0x20 <= ord(char) <= 0x5f for char in fw.name)):
        raise ValueError('Application name must be 1 to 12 ASCII characters from 20 to 5F')
    linked = fw.link()
    blocks = linked['blocks']
    address = linked['symbols'].get(entry)
    if address is None or not any(block['kind'] == 'code'
                                  and block['address'] <= address
                                  < block['address'] + len(block['data'])
                                  for block in blocks):
        raise ValueError(f'{entry}: entry must name linked code')
    start = min(block['address'] for block in blocks)
    stop = max(block['address'] + len(block['data']) for block in blocks)
    if not APP_START <= start < stop <= APP_STOP:
        raise ValueError(f'{fw.name}: linked blocks must fit in [{APP_START:#07x}, {APP_STOP:#07x})')
    payload = bytearray(b'\xff' * (stop - start))
    text = f'; {fw.name}: diagnostic assembly, not a build input\n'
    for block in blocks:
        offset = block['address'] - start
        payload[offset:offset + len(block['data'])] = block['data']
        text += (f'\n; {block["name"]}, {len(block["data"])} bytes\n'
                 f'ORG 0x{block["address"]:05x}\n{block["source"].rstrip()}\n')
    header = _HEADER.pack(b'E5AP', 1, HEADER_SIZE, start, address - start,
                          len(payload), work_bytes, stack_bytes, len(fw.name),
                          b'\0' * 3, fw.name.encode('ascii'), 0)
    _read_header(header)
    header = header[:40] + struct.pack('<I', _crc(header, payload))
    return header + payload, text


def _check_image(image):
    if len(image) != FLASH_SIZE:
        raise ValueError('Application input must be a complete 512 KiB Flash image')


def _check_records(rows):
    start = S4_ADDRESS + S4_SIZE - DIRECTORY_SIZE - len(rows) * HEADER_SIZE
    if start < APP_START:
        raise ValueError('Application directory exceeds S4')
    names = set()
    previous = None
    for row in rows:
        name = row['name']
        left = row['load_address']
        right = left + row['payload_size']
        if name in names:
            raise ValueError(f'Duplicate application name: {name}')
        names.add(name)
        if right > start:
            raise ValueError(f'{name} [{left:#07x}, {right:#07x}) overlaps directory at {start:#07x}')
        if previous is not None:
            old_left = previous['load_address']
            old_right = old_left + previous['payload_size']
            if left < old_left:
                raise ValueError('Application directory is not sorted by load address')
            if left < old_right:
                raise ValueError(f'{previous["name"]} [{old_left:#07x}, {old_right:#07x}) '
                                 f'overlaps {name} [{left:#07x}, {right:#07x})')
        previous = row
    return start


def read_apps(image):
    """Read an S4 directory; changed payloads remain readable as modified records."""
    _check_image(image)
    end = S4_OFFSET + S4_SIZE
    header = image[end - DIRECTORY_SIZE:end]
    magic, version, count, size, crc = _DIRECTORY.unpack(header)
    if magic != b'E5AD':
        raise ValueError('S4 is not initialized for applications')
    if (version != 1 or size != DIRECTORY_SIZE + count * HEADER_SIZE
            or size > S4_SIZE - (APP_START - S4_ADDRESS)):
        raise ValueError('Invalid application directory format or size')
    records = image[end - size:end - DIRECTORY_SIZE]
    if zlib.crc32(records, zlib.crc32(header[:12])) != crc:
        raise ValueError('Application directory CRC mismatch')
    if image[S4_OFFSET:S4_OFFSET + 0x100] != b'\xff' * 0x100:
        raise ValueError('Application directory reserved S4 prefix is not erased')
    rows = [_read_header(records[offset:offset + HEADER_SIZE])
            for offset in range(0, len(records), HEADER_SIZE)]
    _check_records(rows)
    for row in rows:
        offset = row['load_address'] - FLASH_BASE
        row['payload'] = bytes(image[offset:offset + row['payload_size']])
        row['modified'] = _crc(row['header'], row['payload']) != row['crc32']
    return rows


def _write_directory(image, rows, old_count):
    start = _check_records(rows) - FLASH_BASE
    end = S4_OFFSET + S4_SIZE
    old_start = end - DIRECTORY_SIZE - old_count * HEADER_SIZE
    image[min(start, old_start):end] = b'\xff' * (end - min(start, old_start))
    records = b''.join(row['header'] for row in rows)
    header = _DIRECTORY.pack(b'E5AD', 1, len(rows), DIRECTORY_SIZE + len(records), 0)
    crc = zlib.crc32(records, zlib.crc32(header[:12]))
    image[start:end] = records + header[:12] + struct.pack('<I', crc)


def init_image(image):
    """Erase S4 and create an empty directory; the caller must save S4 first."""
    _check_image(image)
    end = S4_OFFSET + S4_SIZE
    if image[end - DIRECTORY_SIZE:end - DIRECTORY_SIZE + 4] == b'E5AD':
        raise ValueError('S4 is already initialized for applications')
    result = bytearray(image)
    result[S4_OFFSET:end] = b'\xff' * S4_SIZE
    _write_directory(result, [], 0)
    return bytes(result)


def install_app(image, data, *, replace=False):
    """Install a checked package, preserving other applications' actual payloads."""
    rows = read_apps(image)
    app = read_app(data)
    old = next((row for row in rows if row['name'] == app['name']), None)
    if old is not None and not replace:
        left = old['load_address']
        right = left + old['payload_size']
        raise ValueError(f'{app["name"]} already exists at [{left:#07x}, {right:#07x})')
    updated = sorted([row for row in rows if row is not old] + [app],
                     key=lambda row: row['load_address'])
    _check_records(updated)
    result = bytearray(image)
    if old is not None:
        offset = old['load_address'] - FLASH_BASE
        result[offset:offset + old['payload_size']] = b'\xff' * old['payload_size']
    _write_directory(result, updated, len(rows))
    offset = app['load_address'] - FLASH_BASE
    result[offset:offset + app['payload_size']] = app['payload']
    return bytes(result)


def remove_app(image, name):
    """Remove one named application, including a modified one."""
    rows = read_apps(image)
    old = next((row for row in rows if row['name'] == name), None)
    if old is None:
        raise ValueError(f'Application not found: {name}')
    result = bytearray(image)
    offset = old['load_address'] - FLASH_BASE
    result[offset:offset + old['payload_size']] = b'\xff' * old['payload_size']
    _write_directory(result, [row for row in rows if row is not old], len(rows))
    return bytes(result)


def restore_s4(image, backup):
    """Replace all of S4 with a complete backup, leaving other banks unchanged."""
    _check_image(image)
    if len(backup) != S4_SIZE:
        raise ValueError('S4 backup must contain exactly 65536 bytes')
    return bytes(image[:S4_OFFSET]) + bytes(backup) + bytes(image[S4_OFFSET + S4_SIZE:])
