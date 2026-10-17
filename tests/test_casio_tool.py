"""Offline toolchain checks; no running emulator is contacted."""

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from casio_emulator import MCPClient
from casio_tool import (
    build_image, clone_model, deploy_image, flash_checksum, image_range, number, output_paths,
    parser, patch_image, run, schema_call, start_emulator, write_binary,
)


class ImageTests(unittest.TestCase):
    def test_addresses(self):
        self.assertEqual(number('F:1234'), 0xf1234)
        self.assertEqual(number('FF:F000'), 0xfff000)
        self.assertEqual(number('1048575'), 0xfffff)
        self.assertEqual(number('0x84000'), 0x84000)
        with self.assertRaises(ValueError):
            number('1:10000')

    def test_explicit_mapping(self):
        data = bytes(range(16))
        self.assertEqual(image_range(data, cpu_address=0xff0004, image_base=0xff0000, size=2), (4, 2))
        self.assertEqual(patch_image(data, b'XY', cpu_address=0xff0004, image_base=0xff0000),
                         data[:4] + b'XY' + data[6:])
        for values in ({'cpu_address': 4}, {'offset': -1}, {'offset': 15, 'size': 2},
                       {'offset': 0, 'cpu_address': 0},
                       {'cpu_address': 0xfffffe, 'image_base': 0xfffffe, 'size': 3}):
            with self.subTest(values=values), self.assertRaises(ValueError):
                image_range(data, **values)

    def test_checksum_is_opt_in(self):
        data = bytes(0x80000)
        raw = patch_image(data, b'\x12', offset=0x40000)
        checked = patch_image(data, b'\x12', offset=0x40000, native_checksum=True)
        self.assertEqual(raw[-2:], b'\0\0')
        self.assertEqual(checked[-2:], b'\x12\0')
        self.assertEqual(flash_checksum(checked), 0x12)
        with self.assertRaises(ValueError):
            patch_image(b'abc', b'x', offset=0, native_checksum=True)

    def test_output_preserves_inputs(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder, 'source.bin')
            source.write_bytes(b'original')
            with self.assertRaises(ValueError):
                output_paths([source], [source])
            output_paths([], [source])
            output_paths([source], [Path(folder, 'new.bin')])
            self.assertEqual(source.read_bytes(), b'original')
            destination = Path(folder, 'output.bin')
            destination.write_bytes(b'old')
            output_paths([source], [destination])
            write_binary(destination, b'new')
            self.assertEqual(destination.read_bytes(), b'new')


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = self.root / 'original.bin'
        self.output = self.root / 'built.bin'
        self.map = self.root / 'built.map.json'
        self.project = self.root / 'project.py'
        self.original = bytes(range(256)) * 2048
        self.base.write_bytes(self.original)
        fingerprint = hashlib.sha256(self.original[:0x4000] + self.original[0x40000:]).hexdigest()
        rows = []
        for name, address, size, kind in (('answer', 0x80200, 6, 'code'),
                                          ('caption', 0x80210, 3, 'data')):
            offset = address - 0x80000
            rows.append(dict(name=name, cpu_start=address, physical_start=offset,
                             size=size, reserved_stop=address + 16, kind=kind,
                             original_sha256=hashlib.sha256(
                                 self.original[offset:offset + size]).hexdigest()))
        self.project.write_text(
            "from kits import Firmware, cpu\n"
            f"fw = Firmware('synthetic', regions=((0x80200,0x80220),), "
            f"original_firmware_sha256={fingerprint!r}, original_regions={rows!r})\n"
            "@fw.function(native=True, address=0x80200)\n"
            "def answer():\n"
            "    cpu.r0 = 42\n"
            "    cpu.r1 = 0\n"
            "    cpu.ret()\n"
            "fw.data('caption', b'OK\\0', address=0x80210, labels={'end': 2})\n",
            encoding='utf-8')

    def test_build_and_inspect_python_project(self):
        args = parser().parse_args(['build', str(self.base), '-o', str(self.output),
                                    '--project', str(self.project), '--map', str(self.map)])
        result = run(args)
        image = self.output.read_bytes()
        self.assertEqual(image[0x200:0x206], bytes.fromhex('2a 00 00 01 1f fe'))
        self.assertEqual(image[0x210:0x213], b'OK\0')
        self.assertEqual(image[0x4000:0x40000], self.original[0x4000:0x40000])
        self.assertEqual(image[0x7ffe0:0x7fffe], self.original[0x7ffe0:0x7fffe])
        self.assertEqual(result['sha256'], hashlib.sha256(image).hexdigest())
        report = run(parser().parse_args(['inspect', str(self.output),
                                         '--native-checksum', '--map', str(self.map)]))
        self.assertTrue(report['native_checksum']['valid'])
        rows = report['map']['regions']
        self.assertEqual([row['name'] for row in rows], ['answer', 'caption', 'native_checksum'])
        self.assertEqual(rows[0], dict(name='answer', cpu_start=0x80200,
                                      physical_start=0x200, size=6,
                                      reserved_stop=0x80210, kind='code'))
        self.assertEqual(rows[1]['size'], 3)

    def test_clean_upgrade_preserves_user_banks_and_footer(self):
        clean = self.root / 'clean.bin'
        clean.write_bytes(self.original)
        upgraded = bytearray(self.original)
        upgraded[0x300:0x304] = b'OLD!'
        upgraded[0x4000:0x40000] = b'U' * 0x3c000
        upgraded[0x7ffe0:0x7fffe] = b'F' * 30
        self.base.write_bytes(upgraded)
        build_image(self.base, self.output, project=self.project, clean=clean, map_path=self.map)
        image = self.output.read_bytes()
        self.assertEqual(image[0x300:0x304], self.original[0x300:0x304])
        self.assertEqual(image[0x4000:0x40000], upgraded[0x4000:0x40000])
        self.assertEqual(image[0x7ffe0:0x7fffe], upgraded[0x7ffe0:0x7fffe])
        self.assertEqual(int.from_bytes(image[-2:], 'little'), flash_checksum(image))

    def test_invalid_original_leaves_outputs_untouched(self):
        self.base.write_bytes(bytes(0x80000))
        self.output.write_bytes(b'previous')
        self.map.write_text('previous', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'version mismatch'):
            build_image(self.base, self.output, project=self.project, map_path=self.map)
        self.assertEqual(self.output.read_bytes(), b'previous')
        self.assertEqual(self.map.read_text(encoding='utf-8'), 'previous')

    def test_region_signature_and_layout_are_checked(self):
        from build_e5800p import load_project

        fw = load_project(self.project)
        fw.original_firmware_sha256 = None
        with self.assertRaisesRegex(ValueError, 'region hash mismatch'):
            fw.image(bytes(0x80000))
        fw.original_regions[0]['size'] += 2
        fw.original_regions[0]['original_sha256'] = hashlib.sha256(
            self.original[0x200:0x208]).hexdigest()
        with self.assertRaisesRegex(ValueError, 'fixed layout'):
            fw.image(self.original)

    def test_module_cli_builds_external_project(self):
        from kits.__main__ import main

        listing = self.root / 'output.asm'
        with patch.object(sys, 'argv', ['kits', str(self.project), str(self.base),
                                       '-o', str(self.output), '--map', str(self.map),
                                       '--listing', str(listing)]):
            self.assertEqual(main(), 0)
        self.assertEqual(self.output.read_bytes()[0x200:0x206],
                         bytes.fromhex('2a 00 00 01 1f fe'))

    def test_data_symbols_and_code_alignment(self):
        from build_e5800p import load_project
        from kits import Firmware, cpu

        linked = load_project(self.project).link()
        self.assertEqual(linked['symbols']['caption__end'], 0x80212)
        fw = Firmware('odd', regions=((0x80200, 0x80220),))

        @fw.function(native=True, address=0x80200)
        def odd():
            cpu.ret()
            cpu.data(b'X')

        with self.assertRaisesRegex(ValueError, 'invalid compiled code size'):
            fw.link()

    def test_source_and_output_aliases_are_rejected(self):
        source = self.project.read_bytes()
        for output, map_path in ((self.project, None), (self.output, self.project),
                                 (self.output, self.output), (self.base, None)):
            with self.subTest(output=output, map_path=map_path):
                with self.assertRaises(ValueError):
                    build_image(self.base, output, project=self.project, map_path=map_path)
        self.assertEqual(self.project.read_bytes(), source)
        self.assertEqual(self.base.read_bytes(), self.original)

    def test_standalone_assembly_remains_available(self):
        source = self.root / 'user.asm'
        source.write_text('MOV R0,#42\nMOV R1,#0\nRET\n', encoding='utf-8')
        run(parser().parse_args(['asm', str(source), '--origin', '8:4000',
                                 '-o', str(self.output)]))
        self.assertEqual(self.output.read_bytes(), bytes.fromhex('2a 00 00 01 1f fe'))


class ModelTests(unittest.TestCase):
    @patch('casio_tool.require_stopped')
    def test_clone_and_deploy(self, stopped):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, model = root / 'source', root / 'clone'
            source.mkdir()
            for name, data in {'model.lua': b'-- model', 'config.bin': b'config',
                               'rom.bin': b'rom', 'ram.dmp': b'ram',
                               'flash.bin': bytes(0x80000), 'flash.dmp': bytes(0x80000)}.items():
                source.joinpath(name).write_bytes(data)
            clone_model(source, model)
            self.assertEqual(model.joinpath('config.bin').read_bytes(), b'config')
            self.assertEqual(model.joinpath('ram.dmp').read_bytes(), b'ram')
            image = root / 'staged.bin'
            image.write_bytes(b'\x12' * 0x80000)
            deploy_image(image, model)
            self.assertEqual(model.joinpath('flash.bin').read_bytes(), image.read_bytes())
            self.assertEqual(model.joinpath('flash.dmp').read_bytes(), image.read_bytes())
            self.assertEqual(source.joinpath('flash.bin').read_bytes(), bytes(0x80000))
            self.assertEqual(model.joinpath('rom.bin').read_bytes(), b'rom')
            deploy_image(image, source)
            self.assertEqual(source.joinpath('flash.bin').read_bytes(), image.read_bytes())

    def test_live_model_not_deployed(self):
        with tempfile.TemporaryDirectory() as folder:
            model = Path(folder) / '计算器型号'
            model.mkdir()
            target = model / 'flash.bin'
            target.write_bytes(b'original')
            image = Path(folder) / 'new.bin'
            image.write_bytes(bytes(0x80000))
            process = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)', str(model)])
            try:
                with self.assertRaises(ValueError):
                    deploy_image(image, model)
                self.assertEqual(target.read_bytes(), b'original')
            finally:
                process.terminate()
                process.wait(timeout=10)

    @patch('casio_tool.subprocess.Popen')
    @patch('casio_tool.socket.create_connection')
    @patch('casio_tool.require_stopped')
    def test_occupied_port_not_started(self, stopped, connection, popen):
        with tempfile.TemporaryDirectory() as folder:
            exe = Path(folder, 'emulator.exe')
            exe.write_bytes(b'')
            with self.assertRaisesRegex(ValueError, 'occupied'):
                start_emulator(exe, folder)
        popen.assert_not_called()


class TransportTests(unittest.TestCase):
    def client(self):
        client = MCPClient.__new__(MCPClient)
        client.session = Mock()
        client.headers = {}
        client.sequence = 0
        client.url = 'http://localhost/mcp'
        return client

    def response(self, client, value=None, events=None):
        response = Mock()
        response.headers = {'Content-Type': 'text/event-stream' if events else 'application/json',
                            'Mcp-Session-Id': 'test-session'}
        response.json.return_value = value
        response.iter_lines.return_value = iter(events or [])
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        client.session.post.return_value = response
        return response

    def test_json_and_session(self):
        client = self.client()
        self.response(client, {'jsonrpc': '2.0', 'id': 1, 'result': {'ok': True}})
        self.assertEqual(client.rpc('get', {}), {'ok': True})
        self.assertEqual(client.headers['Mcp-Session-Id'], 'test-session')

    def test_sse_notifications_and_multiline(self):
        client = self.client()
        self.response(client, events=[
            ': keepalive', '', 'event: message',
            'data: {"jsonrpc":"2.0","method":"notifications/progress"}', '',
            'data: {"jsonrpc":"2.0","id":1,', 'data: "result":{"ok":true}}', '',
        ])
        self.assertEqual(client.rpc('get', {}), {'ok': True})

    def test_rpc_error(self):
        client = self.client()
        self.response(client, {'id': 1, 'error': {'code': -1, 'message': 'bad request'}})
        with self.assertRaisesRegex(RuntimeError, 'bad request'):
            client.rpc('get', {})

    def test_tool_results_and_errors(self):
        client = self.client()
        client.rpc = Mock(return_value={'content': [{'type': 'text', 'text': '{"answer":42}'}]})
        self.assertEqual(client.call('example'), {'answer': 42})
        client.rpc.return_value = {'content': [{'type': 'text', 'text': 'unsupported'}], 'isError': True}
        with self.assertRaisesRegex(RuntimeError, 'unsupported'):
            client.call('example')
        client.rpc.return_value = {'structuredContent': {'error': 'denied'}}
        with self.assertRaisesRegex(RuntimeError, 'denied'):
            client.call('example')


    def test_schema_guard(self):
        client = self.client()
        tools = {'write_memory': {'inputSchema': {'required': ['address', 'bytes']}}}
        with self.assertRaisesRegex(ValueError, 'advertise'):
            schema_call(client, tools, 'invented_tool', {})
        with self.assertRaisesRegex(ValueError, 'bytes'):
            schema_call(client, tools, 'write_memory', {'address': 0})
        client.session.post.assert_not_called()


if __name__ == '__main__':
    unittest.main()
