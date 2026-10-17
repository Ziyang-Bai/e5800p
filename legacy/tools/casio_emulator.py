"""Small MCP client for the Casio emulator's JSON/SSE endpoint."""

import json
import time

import requests


class MCPClient:
    def __init__(self, url='http://127.0.0.1:3001/mcp'):
        self.session = requests.Session()
        self.headers = {'Accept': 'application/json, text/event-stream'}
        self.sequence = 0
        self.url = url
        try:
            result = self.rpc('initialize', {
                'protocolVersion': '2024-11-05', 'capabilities': {},
                'clientInfo': {'name': 'casio-tool', 'version': '1'},
            })
            if result.get('protocolVersion'):
                self.headers['MCP-Protocol-Version'] = result['protocolVersion']
            with self.session.post(self.url, headers=self.headers, json={
                'jsonrpc': '2.0', 'method': 'notifications/initialized',
            }, timeout=30) as response:
                response.raise_for_status()
        except BaseException:
            self.close()
            raise

    @staticmethod
    def _events(response):
        data = []
        for line in response.iter_lines(decode_unicode=True):
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            line = line.lstrip('\ufeff')
            if not line:
                if data:
                    yield json.loads('\n'.join(data))
                    data.clear()
            elif line.startswith('data:'):
                data.append(line[5:].removeprefix(' '))
        if data:
            yield json.loads('\n'.join(data))

    def rpc(self, method, params):
        self.sequence += 1
        request_id = self.sequence
        with self.session.post(self.url, headers=self.headers, json={
            'jsonrpc': '2.0', 'id': request_id, 'method': method, 'params': params,
        }, timeout=30, stream=True) as response:
            response.raise_for_status()
            if response.headers.get('Mcp-Session-Id'):
                self.headers['Mcp-Session-Id'] = response.headers['Mcp-Session-Id']
            if 'text/event-stream' in response.headers.get('Content-Type', '').lower():
                messages = self._events(response)
            else:
                value = response.json()
                messages = value if isinstance(value, list) else (value,)
            for message in messages:
                if not isinstance(message, dict) or message.get('id') != request_id:
                    continue
                if 'error' in message:
                    raise RuntimeError(f'MCP {method}: {message["error"]}')
                if 'result' not in message:
                    raise RuntimeError(f'MCP {method}: response has no result')
                return message['result']
        raise RuntimeError(f'MCP {method}: no response for request {request_id}')

    def call(self, tool_name, **args):
        result = self.rpc('tools/call', {'name': tool_name, 'arguments': args})
        value = result.get('structuredContent')
        if value is None:
            content = result.get('content', [])
            text = '\n'.join(item['text'] for item in content if item.get('type') == 'text')
            try:
                value = json.loads(text)
            except (ValueError, TypeError):
                value = text if text else content
        if result.get('isError') or (isinstance(value, dict) and value.get('error')):
            raise RuntimeError(f'MCP tool {tool_name}: {value}')
        return value

    def tools(self):
        tools = []
        params = {}
        cursors = set()
        while True:
            result = self.rpc('tools/list', params)
            tools.extend(result['tools'])
            cursor = result.get('nextCursor')
            if not cursor:
                return tools
            if cursor in cursors:
                raise RuntimeError('MCP tools/list: repeated pagination cursor')
            cursors.add(cursor)
            params = {'cursor': cursor}

    def memory(self, address, size):
        data = bytes(self.call('read_memory', address=address, size=size)['bytes'])
        if len(data) != size:
            raise RuntimeError(f'MCP read_memory: expected {size} bytes, received {len(data)}')
        return data

    def registers(self):
        return {r['name']: r['value'] for r in self.call('list_registers')['registers']}

    def keys(self, *codes):
        for code in codes:
            self.call('keyboard_code', code=code, pressed=True)
            try:
                time.sleep(0.12)
            finally:
                self.call('keyboard_code', code=code, pressed=False)
            time.sleep(0.18)

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
