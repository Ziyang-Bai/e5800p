"""Assemble, stage firmware images, and operate an explicitly selected emulator."""

import argparse
import hashlib
import json
import os
import shutil
import socket
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

from casio_emulator import MCPClient


def number(text):
    """Accept decimal, 0x hex, or a hexadecimal segment:offset address."""
    if ':' in text:
        segment, offset = text.split(':', 1)
        segment, offset = int(segment, 16), int(offset, 16)
        if segment < 0 or not 0 <= offset <= 0xffff:
            raise ValueError('Invalid segment:offset address')
        return (segment << 16) | offset
    return int(text, 16 if text.lower().startswith(('0x', '-0x')) else 10)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def emit(value):
    print(json.dumps(value, indent=2, ensure_ascii=False))


def write_json(path, value):
    text = json.dumps(value, indent=2, ensure_ascii=False) + '\n'
    Path(path).write_text(text, encoding='utf-8')


def output_paths(inputs, outputs):
    inputs = [Path(path).resolve() for path in inputs if path is not None]
    outputs = [Path(path).resolve() for path in outputs if path is not None]
    def same_file(left, right):
        return left == right or (left.exists() and right.exists() and left.samefile(right))

    for index, path in enumerate(outputs):
        if any(same_file(path, other) for other in outputs[index + 1:]):
            raise ValueError('Output paths must be different')
        if any(same_file(path, source) for source in inputs):
            raise ValueError(f'Output would replace an input: {path}')
        if path.exists() and not path.is_file():
            raise ValueError(f'Output is not a file: {path}')
        if not path.parent.is_dir():
            raise ValueError(f'Output directory does not exist: {path.parent}')


def write_binary(path, data):
    with Path(path).open('wb') as stream:
        stream.write(data)


def image_range(data, *, offset=None, cpu_address=None, image_base=None, size=None):
    if (offset is None) == (cpu_address is None):
        raise ValueError('Select exactly one file offset or CPU address')
    if cpu_address is not None:
        if image_base is None:
            raise ValueError('--cpu-address requires --image-base')
        if not 0 <= image_base <= cpu_address <= 0xffffff:
            raise ValueError('CPU address/base is outside the 24-bit data address space')
        offset = cpu_address - image_base
    elif image_base is not None:
        raise ValueError('--image-base is only used with --cpu-address')
    size = len(data) - offset if size is None else size
    if offset < 0 or size < 0 or offset + size > len(data):
        raise ValueError(f'Range [{offset:#x}, {offset + size:#x}) exceeds {len(data):#x} bytes')
    if cpu_address is not None and cpu_address + size > 0x1000000:
        raise ValueError('Range exceeds the 24-bit data address space')
    return offset, size


def flash_checksum(data):
    if len(data) != 0x80000:
        raise ValueError('Native checksum requires a complete 512 KiB flash image')
    return sum(data[0x40000:0x7fffe]) & 0xffff


def patch_image(image, payload, *, offset=None, cpu_address=None, image_base=None,
                native_checksum=False):
    start, size = image_range(image, offset=offset, cpu_address=cpu_address,
                              image_base=image_base, size=len(payload))
    result = bytearray(image)
    result[start:start + size] = payload
    if native_checksum:
        result[0x7fffe:0x80000] = flash_checksum(result).to_bytes(2, 'little')
    return bytes(result)


def assemble_file(source, output, origin=0, listing=None, symbols=None):
    from nxu8_asm import assemble

    output_paths([source], [output, listing, symbols])
    data, names, lines = assemble(Path(source).read_text(encoding='utf-8-sig'), origin)
    write_binary(output, data)
    if listing:
        write_json(listing, lines)
    if symbols:
        write_json(symbols, names)
    return {'output': str(output), 'origin': origin, 'size': len(data),
            'sha256': digest(data), 'symbols': names}


def build_image(base, output, *, project=None, clean=None, map_path=None):
    from build_e5800p import load_project

    fw = load_project(project)
    result = fw.build(base, output, clean=clean, map_path=map_path)
    return {'output': str(output), 'size': 0x80000, 'sha256': result['sha256'],
            'map': str(map_path) if map_path else None}


def app(args):
    from build_e5800p import load_project
    from kits.app import (
        S4_ADDRESS, S4_OFFSET, S4_SIZE, build_app, init_image, install_app,
        read_apps, remove_app, restore_s4,
    )

    if args.action == 'build':
        fw = load_project(args.project)
        output_paths([args.project, *fw.source_inputs()], [args.output, args.listing])
        data, listing = build_app(fw, entry=args.entry, work_bytes=args.work_bytes,
                                  stack_bytes=args.stack_bytes)
        write_binary(args.output, data)
        if args.listing:
            args.listing.write_text(listing, encoding='utf-8')
        return {'output': str(args.output), 'size': len(data), 'sha256': digest(data)}

    data = args.image.read_bytes()
    if args.action == 'list':
        return [
            {**{key: row[key] for key in ('name', 'load_address', 'payload_size',
                                          'work_bytes', 'stack_bytes', 'modified')},
             'entry_address': row['load_address'] + row['entry_offset']}
            for row in read_apps(data)
        ]

    inputs = [args.image]
    outputs = [args.output]
    if args.action == 'init':
        outputs.append(args.backup_s4)
    elif args.action == 'install':
        inputs.append(args.package)
    elif args.action == 'restore':
        inputs.append(args.backup)
    output_paths(inputs, outputs)
    result = {'input': str(args.image), 'output': str(args.output),
              'input_sha256': digest(data)}
    if args.action == 'init':
        changed = init_image(data)
        backup = data[S4_OFFSET:S4_OFFSET + S4_SIZE]
        with args.backup_s4.open('xb') as stream:
            stream.write(backup)
        result.update(backup_s4=str(args.backup_s4), backup_sha256=digest(backup))
    elif args.action == 'install':
        changed = install_app(data, args.package.read_bytes(), replace=args.replace)
    elif args.action == 'remove':
        changed = remove_app(data, args.name)
    else:
        backup = args.backup.read_bytes()
        changed = restore_s4(data, backup)
        result.update(backup=str(args.backup), backup_sha256=digest(backup),
                      regions=[dict(file_offset=S4_OFFSET, cpu_start=S4_ADDRESS, size=S4_SIZE)])
        print(f'Restore S4 SHA-256 {digest(backup)}; '
              f'CPU [{S4_ADDRESS:#x}, {S4_ADDRESS + S4_SIZE:#x}), '
              f'image [{S4_OFFSET:#x}, {S4_OFFSET + S4_SIZE:#x})', file=sys.stderr)
    write_binary(args.output, changed)
    result.update(size=len(changed), sha256=digest(changed))
    return result


def _powershell(command):
    result = subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-Command',
                             "$ErrorActionPreference='Stop'; "
                             "[Console]::OutputEncoding=[Text.UTF8Encoding]::new($false); " + command],
                            check=True, capture_output=True, encoding='utf-8')
    return json.loads(result.stdout.strip() or '[]')


def _processes():
    if os.name == 'nt':
        rows = _powershell('Get-CimInstance Win32_Process | '
                           'Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress')
        return rows if isinstance(rows, list) else [rows]
    proc = Path('/proc')
    if not proc.is_dir():
        raise RuntimeError('Model process checks require Windows or Linux /proc')
    rows = []
    for entry in proc.iterdir():
        if not entry.name.isdigit():
            continue
        try:
            arguments = entry.joinpath('cmdline').read_bytes().rstrip(b'\0').split(b'\0')
            rows.append({'ProcessId': int(entry.name),
                         'Arguments': [arg.decode(errors='replace') for arg in arguments],
                         'ExecutablePath': str(entry.joinpath('exe').resolve())})
        except (FileNotFoundError, PermissionError, ProcessLookupError):
            continue
    return rows


def _uses_model(row, model, *, conservative=False):
    arguments = row.get('Arguments')
    if arguments is None:
        import ctypes
        from ctypes import wintypes

        count = ctypes.c_int()
        split = ctypes.windll.shell32.CommandLineToArgvW
        split.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_int)]
        split.restype = ctypes.POINTER(wintypes.LPWSTR)
        pointer = split(row.get('CommandLine') or '', ctypes.byref(count))
        if not pointer:
            return False
        try:
            arguments = [pointer[index] for index in range(count.value)]
        finally:
            free = ctypes.windll.kernel32.LocalFree
            free.argtypes = [ctypes.c_void_p]
            free(pointer)
    path = str(Path(model).resolve()).replace('\\', '/').casefold()
    for argument in arguments[1:]:
        argument = argument.replace('\\', '/').rstrip('/').casefold()
        if argument == path:
            return True
        # A relative model argument has no reliable cwd in Win32_Process.
        if conservative and argument.rsplit('/', 1)[-1] == Path(model).name.casefold():
            return True
    return False


def require_stopped(model):
    for row in _processes():
        if row['ProcessId'] != os.getpid() and _uses_model(row, model, conservative=True):
            raise ValueError(f'PID {row["ProcessId"]} may be using this model; close it before copying/deploying')


def clone_model(source, destination):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if not source.is_dir() or not source.joinpath('model.lua').is_file():
        raise ValueError('Source must be a complete emulator model directory containing model.lua')
    if destination.exists() or destination.is_relative_to(source):
        raise ValueError('Choose a new clone directory outside the source model')
    require_stopped(source)
    # Dereference links: a clone must not share writable backing files with its source.
    shutil.copytree(source, destination, symlinks=False)
    return {'model': str(destination), 'source': str(source)}


def deploy_image(image, model):
    model = Path(model).resolve()
    require_stopped(model)
    image = Path(image).resolve()
    targets = [model / 'flash.bin', model / 'flash.dmp']
    if image in targets or any(path.exists() and path.samefile(image) for path in targets):
        raise ValueError('Deploy a separate staged image, not a model backing file')
    data = image.read_bytes()
    if len(data) != 0x80000:
        raise ValueError('fx-5800P deployment requires a complete 512 KiB image')
    if not targets[0].is_file() or targets[0].stat().st_size != len(data):
        raise ValueError('Model flash.bin is missing or has a different size')
    previous = [(path, path.read_bytes() if path.exists() else None) for path in targets]
    try:
        for path in targets:
            path.write_bytes(data)
    except BaseException:
        for path, old in previous:
            if old is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(old)
        raise
    return {'model': str(model), 'image': str(image), 'size': len(data),
            'sha256': digest(data), 'synchronized': [path.name for path in targets]}


def _endpoint(url):
    parsed = urlparse(url)
    if parsed.scheme != 'http' or parsed.hostname not in ('127.0.0.1', 'localhost', '::1'):
        raise ValueError('Model ownership checks require a local HTTP MCP URL')
    return parsed.hostname, parsed.port or 80


def start_emulator(exe, model, *, url='http://127.0.0.1:3001/mcp', log=None):
    model = Path(model).resolve()
    if not model.is_dir():
        raise ValueError(f'Model directory does not exist: {model}')
    exe = Path(exe).resolve()
    if not exe.is_file():
        raise ValueError(f'Emulator executable does not exist: {exe}')
    require_stopped(model)
    host, port = _endpoint(url)
    try:
        with socket.create_connection((host, port), timeout=1):
            raise ValueError(f'Port {port} is occupied; the existing process was not changed')
    except (ConnectionRefusedError, TimeoutError):
        pass
    if log:
        output_paths([exe, *(path for path in model.rglob('*') if path.is_file())], [log])
    with Path(log).open('wb') if log else open(os.devnull, 'wb') as stream:
        options = {'cwd': str(exe.parent), 'stdin': subprocess.DEVNULL,
                   'stdout': stream, 'stderr': subprocess.STDOUT}
        if os.name == 'nt':
            options['creationflags'] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        else:
            options['start_new_session'] = True
        process = subprocess.Popen([str(exe), str(model)], **options)
    return {'pid': process.pid, 'exe': str(exe), 'model': str(model), 'url': url,
            'log': str(log) if log else None}


def require_server_model(url, model):
    host, port = _endpoint(url)
    if os.name == 'nt':
        pids = _powershell(f'Get-NetTCPConnection -LocalPort {port} -State Listen | '
                           'Select-Object -ExpandProperty OwningProcess | ConvertTo-Json -Compress')
        pids = pids if isinstance(pids, list) else [pids]
    else:
        sockets = set()
        for name in ('tcp', 'tcp6'):
            for line in Path('/proc/net', name).read_text().splitlines()[1:]:
                fields = line.split()
                if int(fields[1].split(':')[1], 16) == port and fields[3] == '0A':
                    sockets.add('socket:[' + fields[9] + ']')
        pids = []
        for entry in Path('/proc').iterdir():
            if not entry.name.isdigit():
                continue
            try:
                if any(os.readlink(fd) in sockets for fd in entry.joinpath('fd').iterdir()):
                    pids.append(int(entry.name))
            except (FileNotFoundError, PermissionError, ProcessLookupError):
                continue
    owners = [row for row in _processes() if row['ProcessId'] in pids]
    if not owners or any(not _uses_model(row, model) for row in owners):
        raise ValueError('MCP listener does not belong to the explicitly selected model')


def schema_call(client, tools, name, args):
    if name not in tools:
        raise ValueError(f'Server does not advertise {name!r}; use debug tools to inspect its schema')
    schema = tools[name].get('inputSchema', {})
    missing = set(schema.get('required', [])) - args.keys()
    if missing:
        raise ValueError(f'{name} requires arguments: {", ".join(sorted(missing))}')
    if schema.get('additionalProperties') is False:
        extra = args.keys() - schema.get('properties', {}).keys()
        if extra:
            raise ValueError(f'{name} does not accept: {", ".join(sorted(extra))}')
    return client.call(name, **args)


def debug(args):
    action = args.action
    if action not in ('tools', 'status', 'registers', 'read'):
        if args.model is None:
            raise ValueError('Mutating/generic debug commands require --model to check MCP process ownership')
        require_server_model(args.url, args.model)
    with MCPClient(args.url) as client:
        tools = {item['name']: item for item in client.tools()}
        if action == 'tools':
            return list(tools.values())
        if action == 'call':
            values = json.loads(args.args)
            if not isinstance(values, dict):
                raise ValueError('--args must be a JSON object')
            return schema_call(client, tools, args.tool, values)
        if action == 'keys':
            if 'keyboard_code' not in tools:
                raise ValueError('Server does not advertise keyboard_code')
            client.keys(*args.codes)
            return {'keys': args.codes}
        if action in ('read', 'write'):
            payload = Path(args.data).read_bytes() if action == 'write' else None
            size = len(payload) if payload is not None else args.size
            if args.address < 0 or size < 0 or args.address + size > 0x1000000:
                raise ValueError('Memory range exceeds the 24-bit data address space')
            if action == 'write':
                return schema_call(client, tools, 'write_memory',
                                   {'address': args.address, 'bytes': list(payload)})
            if args.output:
                output_paths([], [args.output])
            value = schema_call(client, tools, 'read_memory', {'address': args.address, 'size': size})
            data = bytes(value['bytes'])
            if len(data) != size:
                raise RuntimeError('Server returned a short memory read')
            if args.output:
                write_binary(args.output, data)
            return {'address': args.address, 'size': len(data), 'bytes': data.hex(' '),
                    'sha256': digest(data)}
        if action == 'breakpoint':
            name, values = ('clear_execution_breakpoints', {}) if args.clear else (
                'add_execution_breakpoint', {'address': args.address})
        else:
            name = {'status': 'get_status', 'registers': 'list_registers',
                    'pause': 'pause', 'resume': 'resume', 'reset': 'reset',
                    'step': 'step_into'}[action]
            values = {}
        return schema_call(client, tools, name, values)


def verify(model, out, *, case='all', suite='basic', exe=None, original=None):
    script = Path(__file__).with_name('basic_smoke.py' if suite == 'basic' else 'basic_smoke_power.py')
    command = [sys.executable, str(script), '--model', str(Path(model).resolve()),
               '--out', str(Path(out).resolve())]
    if suite == 'basic':
        command.extend(['--case', case])
        if original is not None:
            command.extend(['--original', str(Path(original).resolve())])
    else:
        if exe is None:
            raise ValueError('--suite power requires --exe')
        command.extend(['--exe', str(Path(exe).resolve())])
    return subprocess.run(command, cwd=script.parent).returncode


def _range_options(parser, *, size=True):
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--offset', type=number, help='byte offset in the input file')
    group.add_argument('--cpu-address', type=number, help='full CPU data address')
    parser.add_argument('--image-base', type=number, help='CPU address represented by file offset zero')
    if size:
        parser.add_argument('--size', type=number, help='byte count; defaults to the rest of the file')


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest='command', required=True)
    asm = commands.add_parser('asm', help='assemble nXu8 source into a contiguous binary')
    asm.add_argument('source', type=Path)
    asm.add_argument('-o', '--output', type=Path, required=True)
    asm.add_argument('--origin', type=number, required=True)
    asm.add_argument('--listing', type=Path)
    asm.add_argument('--symbols', type=Path)
    disasm = commands.add_parser('disasm', help='disassemble an explicit image range')
    disasm.add_argument('image', type=Path)
    _range_options(disasm)
    disasm.add_argument('--origin', type=number, help='code address at selected range; required with --offset')
    disasm.add_argument('-o', '--output', type=Path, help='JSON listing (otherwise stdout)')
    build = commands.add_parser('build', help='compile a PL/e firmware project')
    build.add_argument('base', type=Path)
    build.add_argument('-o', '--output', type=Path, required=True)
    build.add_argument('--project', type=Path,
                       help='PL/e project; defaults to bundled e5800p')
    build.add_argument('--clean', type=Path,
                       help='original firmware for upgrading while preserving base native data banks')
    build.add_argument('--map', type=Path)
    application = commands.add_parser('app', help='build and manage standalone S4 applications')
    apps = application.add_subparsers(dest='action', required=True)
    app_build = apps.add_parser('build')
    app_build.add_argument('project', type=Path)
    app_build.add_argument('-o', '--output', type=Path, required=True)
    app_build.add_argument('--entry', default='main')
    app_build.add_argument('--work-bytes', type=number, default=0)
    app_build.add_argument('--stack-bytes', type=number, required=True)
    app_build.add_argument('--listing', type=Path)
    app_init = apps.add_parser('init')
    app_init.add_argument('image', type=Path)
    app_init.add_argument('-o', '--output', type=Path, required=True)
    app_init.add_argument('--backup-s4', type=Path, required=True)
    app_list = apps.add_parser('list')
    app_list.add_argument('image', type=Path)
    app_install = apps.add_parser('install')
    app_install.add_argument('image', type=Path)
    app_install.add_argument('package', type=Path)
    app_install.add_argument('-o', '--output', type=Path, required=True)
    app_install.add_argument('--replace', action='store_true')
    app_remove = apps.add_parser('remove')
    app_remove.add_argument('image', type=Path)
    app_remove.add_argument('name')
    app_remove.add_argument('-o', '--output', type=Path, required=True)
    app_restore = apps.add_parser('restore')
    app_restore.add_argument('image', type=Path)
    app_restore.add_argument('backup', type=Path)
    app_restore.add_argument('-o', '--output', type=Path, required=True)
    patch = commands.add_parser('patch', help='replace bytes in a separate staged image')
    patch.add_argument('image', type=Path)
    patch.add_argument('data', type=Path)
    patch.add_argument('-o', '--output', type=Path, required=True)
    _range_options(patch, size=False)
    patch.add_argument('--native-checksum', action='store_true')
    patch.add_argument('--map', type=Path, help='JSON patch ranges and image hashes')
    read = commands.add_parser('read', help='extract an explicit binary range')
    read.add_argument('image', type=Path)
    _range_options(read)
    read.add_argument('-o', '--output', type=Path)
    inspect = commands.add_parser('inspect', help='image size, SHA-256 and optional native checksum/map')
    inspect.add_argument('image', type=Path)
    inspect.add_argument('--native-checksum', action='store_true')
    inspect.add_argument('--map', type=Path)
    checksum = commands.add_parser('checksum', help='inspect or explicitly repair native flash checksum')
    checksum.add_argument('image', type=Path)
    checksum.add_argument('-o', '--output', type=Path, help='write a separate corrected image')
    model = commands.add_parser('model', help='clone, deploy or start an isolated full model')
    models = model.add_subparsers(dest='action', required=True)
    clone = models.add_parser('clone')
    clone.add_argument('source', type=Path)
    clone.add_argument('destination', type=Path)
    deploy = models.add_parser('deploy')
    deploy.add_argument('image', type=Path)
    deploy.add_argument('--model', type=Path, required=True)
    start = models.add_parser('start')
    start.add_argument('--exe', type=Path, required=True)
    start.add_argument('--model', type=Path, required=True)
    start.add_argument('--url', default='http://127.0.0.1:3001/mcp',
                       help='expected MCP endpoint; configure the emulator port separately')
    start.add_argument('--log', type=Path)
    debugger = commands.add_parser('debug', help='use the connected server\'s advertised MCP tools')
    debugger.add_argument('--url', default='http://127.0.0.1:3001/mcp')
    debugger.add_argument('--model', type=Path, help='required for mutation/generic calls')
    actions = debugger.add_subparsers(dest='action', required=True)
    for name in ('tools', 'status', 'registers', 'pause', 'resume', 'reset', 'step'):
        actions.add_parser(name)
    memory_read = actions.add_parser('read')
    memory_read.add_argument('address', type=number)
    memory_read.add_argument('size', type=number)
    memory_read.add_argument('-o', '--output', type=Path)
    memory_write = actions.add_parser('write')
    memory_write.add_argument('address', type=number)
    memory_write.add_argument('data', type=Path)
    keys = actions.add_parser('keys')
    keys.add_argument('codes', type=number, nargs='+')
    breakpoint = actions.add_parser('breakpoint')
    bp = breakpoint.add_mutually_exclusive_group(required=True)
    bp.add_argument('--address', type=number)
    bp.add_argument('--clear', action='store_true')
    call = actions.add_parser('call')
    call.add_argument('tool')
    call.add_argument('--args', default='{}', help='JSON object matching debug tools inputSchema')
    verification = commands.add_parser('verify', help='forward to the existing real-emulator smoke scripts')
    verification.add_argument('--model', type=Path, required=True)
    verification.add_argument('--out', type=Path, required=True)
    verification.add_argument('--case', default='all')
    verification.add_argument('--suite', choices=('basic', 'power'), default='basic')
    verification.add_argument('--exe', type=Path)
    verification.add_argument('--original', type=Path,
                              help='original Flash for Add-in native-library acceptance')
    return root


def run(args):
    command = args.command
    if command == 'asm':
        return assemble_file(args.source, args.output, args.origin, args.listing, args.symbols)
    if command == 'build':
        return build_image(args.base, args.output, project=args.project,
                           clean=args.clean, map_path=args.map)
    if command == 'app':
        return app(args)
    if command == 'model':
        if args.action == 'clone':
            return clone_model(args.source, args.destination)
        if args.action == 'deploy':
            return deploy_image(args.image, args.model)
        return start_emulator(args.exe, args.model, url=args.url, log=args.log)
    if command == 'debug':
        return debug(args)
    data = args.image.read_bytes()
    if command in ('inspect', 'checksum'):
        result = {'image': str(args.image), 'size': len(data), 'sha256': digest(data)}
        if command == 'checksum' or args.native_checksum:
            expected = flash_checksum(data)
            stored = int.from_bytes(data[0x7fffe:0x80000], 'little')
            result['native_checksum'] = {'stored': stored, 'expected': expected, 'valid': stored == expected}
        if command == 'inspect' and args.map:
            result['map'] = json.loads(args.map.read_text(encoding='utf-8'))
        if command == 'checksum' and args.output:
            output_paths([args.image], [args.output])
            patched = data[:0x7fffe] + expected.to_bytes(2, 'little')
            write_binary(args.output, patched)
            result.update(output=str(args.output), output_sha256=digest(patched))
        return result
    if command == 'patch':
        output_paths([args.image, args.data], [args.output, args.map])
        payload = args.data.read_bytes()
        start, size = image_range(data, offset=args.offset, cpu_address=args.cpu_address,
                                  image_base=args.image_base, size=len(payload))
        patched = patch_image(data, payload, offset=args.offset, cpu_address=args.cpu_address,
                              image_base=args.image_base, native_checksum=args.native_checksum)
        result = {'input': str(args.image), 'output': str(args.output), 'size': len(patched),
                  'input_sha256': digest(data), 'sha256': digest(patched),
                  'regions': [{'file_offset': start, 'cpu_start': args.cpu_address, 'size': size}]}
        if args.native_checksum:
            result['regions'].append({'file_offset': 0x7fffe, 'size': 2, 'kind': 'native_checksum'})
        write_binary(args.output, patched)
        if args.map:
            write_json(args.map, result)
        return result
    start, size = image_range(data, offset=args.offset, cpu_address=args.cpu_address,
                              image_base=args.image_base, size=args.size)
    payload = data[start:start + size]
    if args.output:
        output_paths([args.image], [args.output])
    if command == 'disasm':
        from nxu8_asm import disassemble

        origin = args.origin if args.origin is not None else args.cpu_address
        if origin is None:
            raise ValueError('Disassembly with --offset requires --origin')
        result = disassemble(payload, origin)
        if args.output:
            write_json(args.output, result)
        return result
    if args.output:
        write_binary(args.output, payload)
    return {'file_offset': start, 'cpu_address': args.cpu_address, 'size': size,
            'bytes': payload.hex(' '), 'sha256': digest(payload)}


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == 'verify':
            return verify(args.model, args.out, case=args.case, suite=args.suite,
                          exe=args.exe, original=args.original)
        emit(run(args))
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f'casio_tool: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
