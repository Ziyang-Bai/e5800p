"""Offline toolchain checks; no running emulator is contacted."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from casio_emulator import MCPClient
from casio_tool import (
    clone_model, deploy_image, flash_checksum, image_range, number, output_paths,
    patch_image, schema_call, start_emulator, write_binary,
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
