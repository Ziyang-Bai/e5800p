"""Independent GRAPH numerical and keyboard acceptance in the isolated model."""

import json
import time
from decimal import Decimal

from basic_native import VARIABLE_A, VARIABLE_ANS, VARIABLE_X
from basic_smoke import DIGITS, LETTERS, pair
from basic_smoke_graph import scalar_decimal


PI = Decimal('3.141592653589793238462643383')
TOL = Decimal('1e-8')
WORK = 0x44000
STATE = WORK + 3072
STACK = 0x8300
STACK_SIZE = 0x8c00 - STACK


def _save(out, record):
    out.joinpath(record['case'] + '.json').write_text(
        json.dumps(record, indent=2), encoding='utf-8')
    return record


def _until(emu, addresses, keys=(), seconds=30):
    if isinstance(addresses, int):
        addresses = (addresses,)
    emu.call('clear_execution_breakpoints')
    if keys:
        emu.call('resume')
        deadline = time.monotonic() + 10
        while True:
            status = emu.call('get_status')
            if status['run_status'] == 0:
                break
            if time.monotonic() >= deadline:
                raise AssertionError(('GRAPH input wait not reached', status))
            time.sleep(0.01)
    for address in addresses:
        emu.call('add_execution_breakpoint', address=address)
    emu.call('resume')
    if keys:
        emu.keys(*keys)
    deadline = time.monotonic() + seconds
    while True:
        status = emu.call('get_status')
        if status['paused'] or time.monotonic() >= deadline:
            break
        time.sleep(0.05)
    if not status['paused'] or status['program_counter'] not in addresses:
        emu.call('pause')
        raise AssertionError(('GRAPH breakpoint not reached', list(addresses),
                              status, emu.registers()))
    return status['program_counter'], emu.registers()


def _descriptor(emu, registers):
    frame = registers['r14'] | registers['r15'] << 8
    pointer = emu.memory(frame + 128, 3)
    address = int.from_bytes(pointer[:2], 'little') | pointer[2] << 16
    return frame, address, emu.memory(address, 1024)


def _frame_cases(emu, out, symbols):
    initial = b'\xa5' * 12 + bytes(372) + b'\x5a' * 16
    results = []
    for x, y, mode in ((0, 0, 1), (95, 30, 1), (96, 0, 1), (0, 31, 1), (7, 15, 2)):
        before = bytearray(initial)
        expected = bytearray(initial)
        if x < 96 and y < 31:
            at = (y + 1) * 12 + x // 8
            if mode == 2:
                before[at] = 0xff
                expected[at] = 0xff ^ (0x80 >> (x % 8))
            else:
                expected[at] = 0x80 >> (x % 8)
        registers, data = emu.invoke(
            symbols['graph_pixel'], {'r0': x, 'r1': y, 'r2': mode},
            [(0x80e0, before)], [(0x80e0, 400)], seconds=2)
        record = _save(out, dict(case=f'graph-pixel-{x}-{y}-{mode}',
                                passed=data[0] == expected, registers=registers))
        assert record['passed'], record
        results.append(record)
    registers, data = emu.invoke(
        symbols['graph_clear'], {}, [(0x80e0, b'\xa5' * 384 + b'\x5a' * 16)],
        [(0x80e0, 400)], seconds=2)
    record = _save(out, dict(case='graph-clear-bounds', passed=data[0] == initial,
                            registers=registers))
    assert record['passed'], record
    results.append(record)
    return results


def _plot_cases(emu, out, symbols):
    from firmware.e5800p.graph_math import _number
    from firmware.e5800p.graph_view import FRAME, HEADER, D, INITIAL

    results = []
    for name, source, bounds in (
            ('large-offset', b'1\x0f10\x89X', ('-2', '5', '9999999998', '10000000005')),
            ('pole', b'1\xb9(X\x990.3)', ('-2', '5', '-10', '10')),
            ('integral-shade', b'X\xa9X', ('0', '1', '0', '1'))):
        record = dict(case='graph-plot-' + name, bounds=bounds, source=source.hex())
        snapshot = emu.call('save_snapshot', label=record['case'])['id']
        try:
            frame = bytearray(FRAME)
            frame[HEADER:HEADER + 88] = INITIAL
            frame[HEADER + 6:HEADER + 86] = b''.join(map(_number, bounds))
            frame[D:D + 3] = STATE.to_bytes(3, 'little')
            work = bytearray(4096 + len(source) + 1)
            work[3072:3074] = (len(source) + 1).to_bytes(2, 'little')
            if name == 'integral-shade':
                work[3072 + 44:3072 + 84] = _number('0') + _number('1')
            work[4096:4096 + len(source)] = source
            emu.invoke(symbols['graph_window_load'], pair(14, 0x8c00),
                       [(0x8c00, frame), (WORK, work), (0x80a0, b'\x07\0\x01')],
                       seconds=10, keep=True)
            registers, data = emu.invoke(
                symbols['graph_shade' if name == 'integral-shade' else 'graph_plot'],
                pair(14, 0x8c00),
                [(0x80e0, b'\xa5' * 12 + bytes(372) + b'\x5a' * 16)],
                [(0x80e0, 400)], stop_at=0x80800 if name == 'integral-shade' else 0,
                seconds=300)
            pixels = data[0]
            out.joinpath(record['case'] + '-frame.bin').write_bytes(pixels[:384])

            def pixel(x, y):
                return bool(pixels[(y + 1) * 12 + x // 8] & (0x80 >> (x % 8)))

            assert pixels[:12] == b'\xa5' * 12 and pixels[384:] == b'\x5a' * 16
            if name == 'large-offset':
                assert pixel(0, 30) and pixel(95, 0), 'Large-offset endpoints lost'
                samples = ((20, 30 - 30 * 20 // 95), (75, 30 - 30 * 75 // 95))
                assert all(any(pixel(x, y + delta) for delta in (-1, 0, 1))
                           for x, y in samples), 'Large-offset curve lost small differences'
                record['samples'] = samples
            elif name == 'pole':
                bridge = [y for y in range(4, 27) if y != 15 and pixel(31, y)]
                assert not bridge, ('Pole joined opposite branches', bridge)
                samples = ((24, 18), (38, 12))
                assert all(any(pixel(x, y + delta) for delta in (-1, 0, 1))
                           for x, y in samples), 'Pole curve branch missing'
                record.update(pole_column=31, bridge=bridge, samples=samples)
            else:
                rows = [y for y in range(24, 30) if pixel(48, y)]
                assert rows == list(range(24, 30)), ('Integral shading missing', rows)
                assert not any(pixel(49, y) for y in range(24, 30)), 'Integral shading lost its sparse columns'
                record.update(shaded_column=48, shaded_rows=rows, clear_column=49)
            record.update(passed=True, registers=registers)
        except Exception as error:
            record.update(passed=False, error=str(error), registers=emu.registers())
        finally:
            emu.call('clear_execution_breakpoints')
            emu.call('load_snapshot', id=snapshot)
        results.append(_save(out, record))
    return results


def _stored_cases(emu, out, symbols):
    from firmware.e5800p.graph_math import _number
    from firmware.e5800p.graph_view import INITIAL

    results = []
    point = b'\x01\x2b\0' + _number('1') + _number('2')
    for count in (0, 1, 2):
        payload = bytearray(INITIAL + point * count)
        logical = len(payload)
        payload[4:6] = logical.to_bytes(2, 'little')
        payload[86:88] = count.to_bytes(2, 'little')
        allocated = (logical + 1) & ~1
        payload.extend(bytes(allocated - logical))
        frame = bytearray(384)
        frame[26:28] = (WORK & 0xffff).to_bytes(2, 'little')
        frame[28] = WORK >> 16
        frame[30:32] = allocated.to_bytes(2, 'little')
        registers, data = emu.invoke(
            symbols['graph_load'], pair(14, 0x8500),
            [(0x8500, frame), (WORK, payload)], [(0x8520, 88)], seconds=3)
        record = _save(out, dict(case=f'graph-load-{count}-points',
                                logical=logical, allocated=allocated, registers=registers,
                                passed=registers['r0'] == 0 and data[0] == payload[:88]))
        assert record['passed'], record
        results.append(record)
    return results


def _cursor_cases(emu, out, symbols, record):
    observations = record['cursor_bounds'] = []

    def edit(keys):
        _until(emu, symbols['graph_input_tokens'], (0x63,))
        _until(emu, 0x12576)
        _until(emu, symbols['graph_plot'], (0x70, *keys, 0x63))
        _until(emu, 0x80800, seconds=180)

    def menu(digit, target):
        _until(emu, symbols['graph_menu'], (0x17,))
        _until(emu, 0x80800)
        _until(emu, symbols[target], (DIGITS[digit],))
        _until(emu, 0x80800)

    def point(item, key, axis, expected):
        menu(4, 'graph_sketch')
        _until(emu, symbols['graph_pick'], (DIGITS[1],), seconds=180)
        _until(emu, 0x80800, seconds=180)
        _until(emu, 0x80800, (key,))
        frame, _, _ = _descriptor(emu, emu.registers())
        item['moved'] = list(emu.memory(frame + 134, 2))
        assert item['moved'][axis] == expected, item
        _until(emu, symbols['graph_stage_point'], (0x63,))
        _until(emu, symbols['graph_plot'])
        _until(emu, 0x80800, seconds=180)
        frame, _, _ = _descriptor(emu, emu.registers())
        far = emu.memory(frame + 26, 3)
        address = int.from_bytes(far, 'little')
        header = emu.memory(address, 88)
        size = int.from_bytes(header[4:6], 'little')
        obj = emu.memory(address + size - 43, 43)
        assert obj[:3] == b'\x01\x2b\0', obj.hex()
        item['point'] = [str(scalar_decimal(obj[at:at + 20])) for at in (3, 23)]
        want = (Decimal(-10) + Decimal(expected) * 20 / 95 if axis == 0
                else Decimal(10) - Decimal(expected) * 20 / 30)
        assert abs(Decimal(item['point'][axis]) - want) < Decimal('1e-11'), item
        out.joinpath('graph-cursor-' + item['name'] + '-frame.bin').write_bytes(emu.memory(0x80e0, 384))

    for value, row, key in ((100, 0, 0x47), (-100, 30, 0x37)):
        edit(((0x64,) if value < 0 else ()) + (DIGITS[1], DIGITS[0], DIGITS[0]))
        menu(1, 'graph_trace')
        frame, _, state = _descriptor(emu, emu.registers())
        item = dict(name='above' if value > 0 else 'below', result=str(scalar_decimal(state[24:44])),
                    cursor=list(emu.memory(frame + 134, 2)))
        observations.append(item)
        assert state[3] == 0 and scalar_decimal(state[24:44]) == value, item
        assert item['cursor'][1] == row, item
        _until(emu, symbols['graph_plot'], (0x26,))
        _until(emu, 0x80800, seconds=180)
        point(item, key, 1, 1 if row == 0 else 29)

    edit((0x16, LETTERS['X'], 0x65, DIGITS[1], DIGITS[0], DIGITS[0]))
    menu(2, 'graph_calculate')
    _until(emu, symbols['graph_input_slot'], (DIGITS[1],))
    _until(emu, 0x12576)
    _until(emu, symbols['graph_input_slot'], (0x70, DIGITS[9], DIGITS[0], 0x63))
    _until(emu, 0x12576)
    _until(emu, symbols['graph_calc'], (0x70, DIGITS[1], DIGITS[1], DIGITS[0], 0x63))
    _until(emu, symbols['graph_wait'], seconds=300)
    _, _, state = _descriptor(emu, emu.registers())
    item = dict(name='root-right', x=str(scalar_decimal(state[4:24])), status=state[3])
    observations.append(item)
    assert state[3] == 0 and scalar_decimal(state[4:24]) == 100, item
    _until(emu, 0x80800)
    _until(emu, symbols['graph_plot'], (0x26,))
    _until(emu, 0x80800, seconds=180)
    frame, _, _ = _descriptor(emu, emu.registers())
    item['cursor'] = list(emu.memory(frame + 134, 2))
    assert item['cursor'][0] == 95, item
    point(item, 0x27, 0, 94)
    edit((0x16, LETTERS['X'], 0x25))
    record['steps'].append('Out-of-window TRACE and ROOT keep a visible SKETCH cursor; one inward key and EXE save the selected world point')


def _sketch_case(emu, out, symbols, record):
    observations = record['sketch'] = []
    formula = tokens = None

    def observe(name, kinds):
        nonlocal formula, tokens
        frame, address, state = _descriptor(emu, emu.registers())
        data = emu.memory(frame, 384)
        far = lambda at: int.from_bytes(data[at:at + 2], 'little') | data[at + 2] << 16
        graph = far(26)
        header = emu.memory(graph, 88)
        length = int.from_bytes(header[4:6], 'little')
        count = int.from_bytes(header[86:88], 'little')
        allocated = int.from_bytes(data[30:32], 'little')
        assert header[:4] == b'EGS1' and 88 <= length <= allocated, (name, header.hex())
        assert allocated == ((length + 1) & ~1), (name, length, allocated)
        payload = emu.memory(graph, length)
        objects, pos = [], 88
        for _ in range(count):
            kind = payload[pos]
            size = int.from_bytes(payload[pos + 1:pos + 3], 'little')
            assert kind in range(1, 6) and 3 <= size <= length - pos, (name, pos, size)
            raw = payload[pos:pos + size]
            start = 5 if kind == 5 else 3
            points = int.from_bytes(raw[3:5], 'little') if kind == 5 else (2 if kind in (2, 3) else 1)
            assert size >= start + points * 40, (name, raw.hex())
            if kind != 4:
                assert size == start + points * 40, (name, raw.hex())
            coords = [[str(scalar_decimal(raw[at:at + 20])),
                       str(scalar_decimal(raw[at + 20:at + 40]))]
                      for at in range(start, start + points * 40, 40)]
            objects.append(dict(kind=kind, size=size, points=coords, raw=raw.hex(),
                                text=raw[43:].decode('ascii') if kind == 4 else None))
            pos += size
        assert pos == length and (kinds is None or [obj['kind'] for obj in objects] == kinds), (name, objects)
        source = emu.memory(far(120), int.from_bytes(data[124:126], 'little'))
        linear = emu.memory(address + 1024, int.from_bytes(state[:2], 'little'))
        if formula is None:
            formula, tokens = source, linear
        assert source == formula and linear == tokens and linear.endswith(b'\0'), name
        assert emu.memory(address - 3076, 4) == b'EGW1', (name, address)
        window = [scalar_decimal(state[at:at + 20]) for at in (192, 212, 232, 252)]
        item = dict(name=name, graph=graph, descriptor=address, formula=far(120),
                    formula_bytes=source.hex(), tokens=linear.hex(), length=length,
                    allocated=allocated, count=count, window=list(map(str, window)),
                    objects=objects)
        observations.append(item)
        out.joinpath('graph-sketch-' + name + '.bin').write_bytes(payload)
        out.joinpath('graph-sketch-' + name + '-frame.bin').write_bytes(emu.memory(0x80e0, 384))
        return item, window

    def menu(more=False):
        _until(emu, symbols['graph_menu'], (0x17,))
        _until(emu, 0x80800)
        _until(emu, symbols['graph_sketch'], (DIGITS[4],))
        _until(emu, 0x80800)
        if more:
            _until(emu, 0x80800, (0x57,))

    def redraw(keys=()):
        _until(emu, symbols['graph_plot'], keys)
        _until(emu, 0x80800, seconds=180)

    def pick(x, y):
        frame, _, _ = _descriptor(emu, emu.registers())
        cx, cy = emu.memory(frame + 134, 2)
        for delta, negative, positive in ((x - cx, 0x27, 0x57), (y - cy, 0x37, 0x47)):
            for _ in range(abs(delta)):
                _until(emu, 0x80800, (negative if delta < 0 else positive,))
        assert emu.memory(frame + 134, 2) == bytes((x, y)), (x, y)
        _until(emu, symbols['graph_stage_point'], (0x63,))

    def coordinates(obj, pixels):
        expected = [[Decimal(-10) + Decimal(x) * 20 / 95,
                     Decimal(10) - Decimal(y) * 20 / 30] for x, y in pixels]
        assert all(abs(Decimal(actual) - want) < Decimal('1e-11')
                   for point, target in zip(obj['points'], expected)
                   for actual, want in zip(point, target)), (obj, expected)
        assert len(obj['points']) == len(expected), obj

    observe('before-clear', None)
    # Start from an empty sketch through the same confirmation used below.
    menu(True)
    _until(emu, symbols['graph_clear_sketch'], (DIGITS[3],))
    _until(emu, 0x80800)
    redraw((0x63,))
    empty, _ = observe('empty', [])
    menu()
    _until(emu, symbols['graph_pick'], (DIGITS[1],), seconds=180)
    _until(emu, 0x80800, seconds=180)
    pick(60, 10)
    redraw()
    point, window = observe('point', [1])
    coordinates(point['objects'][0], [(60, 10)])
    anchor = point['objects'][0]['raw']
    assert point['length'] == 131 and point['allocated'] == 132, point

    for name, keys in (('pan-right', (0x57,)), ('pan-left', (0x27,)),
                       ('pan-up', (0x37,)), ('pan-down', (0x47,)),
                       ('zoom-in', (0x06, 0x37)), ('zoom-out', (0x06, 0x47))):
        before = window
        frame, _, _ = _descriptor(emu, emu.registers())
        cx, cy = emu.memory(frame + 134, 2)
        if name.startswith('pan'):
            expected = list(before)
            at = 0 if name in ('pan-right', 'pan-left') else 2
            delta = (before[at + 1] - before[at]) / 4
            if name in ('pan-left', 'pan-down'):
                delta = -delta
            expected[at:at + 2] = [value + delta for value in before[at:at + 2]]
        else:
            focus = [before[0] + Decimal(cx) * (before[1] - before[0]) / 95,
                     before[3] - Decimal(cy) * (before[3] - before[2]) / 30]
            factor = Decimal('0.5') if name == 'zoom-in' else Decimal(2)
            expected = [focus[i // 2] + (value - focus[i // 2]) * factor
                        for i, value in enumerate(before)]
        redraw(keys)
        item, window = observe(name, [1])
        assert all(abs(a - b) < Decimal('1e-11') for a, b in zip(window, expected)), item
        assert item['objects'][0]['raw'] == anchor, item
        x, y = map(Decimal, item['objects'][0]['points'][0])
        px = int((x - window[0]) * 95 / (window[1] - window[0]))
        py = int((window[3] - y) * 30 / (window[3] - window[2]))
        pixels = emu.memory(0x80e0, 384)
        hits = [(col, row) for col in range(max(0, px - 1), min(95, px + 1) + 1)
                for row in range(max(0, py - 1), min(30, py + 1) + 1)
                if pixels[(row + 1) * 12 + col // 8] & (0x80 >> (col % 8))]
        item.update(anchor_pixel=[px, py], anchor_hits=hits)
        assert hits, item
    record['steps'].append('POINT world coordinates and pixels survive quarter-window pan and SHIFT zoom')

    _until(emu, symbols['graph_mode_select'], (0x26,))
    _until(emu, 0x80800)
    _until(emu, symbols['graph'], (DIGITS[1],))
    redraw()
    reopened, _ = observe('odd-reentry', [1])
    assert reopened['objects'][0]['raw'] == anchor and reopened['length'] == 131, reopened
    record['steps'].append('EXIT and GRAPH reentry accept the odd 131-byte EGS1 object')

    for digit, name, positions in ((2, 'line', [(30, 8), (35, 11)]),
                                    (3, 'rectangle', [(65, 18), (70, 21)]),
                                    (4, 'text', [(20, 5)])):
        menu()
        _until(emu, symbols['graph_pick'], (DIGITS[digit],), seconds=180)
        _until(emu, 0x80800, seconds=180)
        for index, position in enumerate(positions):
            if index:
                _until(emu, symbols['graph_pick'], seconds=180)
                _until(emu, 0x80800)
            pick(*position)
        if digit == 4:
            _until(emu, symbols['graph_text_input'])
            _until(emu, 0x12576)
            _until(emu, symbols['graph_append'],
                   (0x16, LETTERS['A'], 0x16, LETTERS['B'], 0x63))
        redraw()
        item, _ = observe(name, list(range(1, digit + 1)))
        coordinates(item['objects'][-1], positions)
        if digit == 4:
            assert item['objects'][-1]['text'] == 'AB', item
    before_pen = item
    menu(True)
    _until(emu, symbols['graph_plot'], (DIGITS[1],))
    _until(emu, 0x80800, seconds=180)
    pick(21, 5)
    _until(emu, 0x80800)
    for key in (0x57, 0x47):
        _until(emu, symbols['graph_stage_point'], (key,))
        _until(emu, 0x80800)
    _until(emu, symbols['graph_append'], (0x26,))
    redraw()
    stroke, _ = observe('pen-three-points', [1, 2, 3, 4, 5])
    coordinates(stroke['objects'][-1], [(21, 5), (22, 5), (22, 6)])
    assert stroke['objects'][-1]['size'] == 125, stroke
    menu(True)
    _until(emu, symbols['graph_undo'], (DIGITS[2],))
    redraw()
    undone, _ = observe('undo-stroke', [1, 2, 3, 4])
    assert undone['objects'] == before_pen['objects'] and undone['length'] == before_pen['length'], undone
    record['steps'].append('LINE, RECT, ASCII AB and three-point PEN stored in world coordinates; UNDO removes the whole stroke')

    for key, name, kinds in ((0x26, 'clear-cancel', [1, 2, 3, 4]),
                             (0x63, 'clear-confirm', [])):
        menu(True)
        _until(emu, symbols['graph_clear_sketch'], (DIGITS[3],))
        _until(emu, 0x80800)
        redraw((key,))
        item, _ = observe(name, kinds)
        if key == 0x26:
            assert item['objects'] == undone['objects'], item
        else:
            assert item['length'] == empty['length'] == 88, item
    record['steps'].append('CLEAR cancellation keeps objects; confirmation removes only sketches and keeps the shared formula')

    _until(emu, symbols['graph_menu'], (0x17,))
    _until(emu, 0x80800)
    _until(emu, symbols['graph_calculate'], (DIGITS[2],))
    _until(emu, 0x80800)
    _until(emu, symbols['graph_input_slot'], (DIGITS[4],))
    _until(emu, 0x12576)
    _until(emu, symbols['graph_calc'], (0x70, DIGITS[2], 0x63))
    _until(emu, symbols['graph_wait'], seconds=300)
    _, _, state = _descriptor(emu, emu.registers())
    record['slope'] = dict(x=str(scalar_decimal(state[4:24])),
                           y=str(scalar_decimal(state[24:44])), status=state[3])
    assert state[3] == 0 and scalar_decimal(state[4:24]) == 2 and scalar_decimal(state[24:44]) == 4, record['slope']
    _until(emu, symbols['graph_tangent'], (0x26,))
    _until(emu, 0x80800)
    _until(emu, symbols['graph_append'], (0x63,))
    redraw()
    item, _ = observe('slope-tangent', [2])
    points = [[Decimal(value) for value in point] for point in item['objects'][0]['points']]
    assert all(abs(actual - expected) < Decimal('1e-8')
               for point, pair in zip(points, ((-10, -44), (10, 36)))
               for actual, expected in zip(point, pair)), item
    menu(True)
    _until(emu, symbols['graph_undo'], (DIGITS[2],))
    redraw()
    observe('undo-tangent', [])
    record['steps'].append('SLOPE at X 2 gives 4; confirmed tangent is the world-coordinate line Y=4X-4 and UNDO removes it')

    _until(emu, symbols['graph_menu'], (0x17,))
    _until(emu, 0x80800)
    _until(emu, symbols['graph_view_menu'], (DIGITS[3],))
    _until(emu, 0x80800)
    for digit, keys in ((1, (0x70, 0x64, DIGITS[2], 0x63)),
                        (2, (0x70, DIGITS[5], 0x63))):
        _until(emu, symbols['graph_number_input'], (DIGITS[digit],))
        _until(emu, 0x12576)
        _until(emu, symbols['graph_window_save'], keys)
        _until(emu, 0x80800)
    redraw((0x26,))
    item, window = observe('asymmetric-view', [])
    assert all(abs(a - b) < Decimal('1e-11')
               for a, b in zip(window, map(Decimal, (-2, 5, -10, 10)))), item
    pixels = emu.memory(0x80e0, 384)
    axis = int(Decimal(2) * 95 / 7)
    columns = {col: sum(bool(pixels[(row + 1) * 12 + col // 8] & (0x80 >> (col % 8)))
                       for row in range(31)) for col in (axis - 1, axis, axis + 1, 47)}
    item.update(zero_axis_expected=axis, zero_axis_columns=columns)
    assert columns[axis] == 31 and columns[47] < 10, item
    record['steps'].append('VIEW [-2,5] maps the zero axis independently to column 27, not the screen center')

    _until(emu, symbols['graph_menu'], (0x17,))
    _until(emu, 0x80800)
    _until(emu, symbols['graph_trace'], (DIGITS[1],))
    _until(emu, 0x80800, seconds=180)
    _until(emu, symbols['graph_number_input'], (0x63,))
    _until(emu, 0x12576)
    _, registers = _until(emu, 0x80800, (DIGITS[2], 0x63), seconds=60)
    _, _, state = _descriptor(emu, registers)
    x, y = scalar_decimal(state[4:24]), scalar_decimal(state[24:44])
    record['sketch_trace'] = dict(x=str(x), y=str(y), status=state[3])
    assert state[3] == 0 and x == 2 and y == 4, record['sketch_trace']
    record['sketch_relocations'] = [
        dict(name=b['name'], work=a['descriptor'] != b['descriptor'],
             formula=a['formula'] != b['formula'], graph=a['graph'] != b['graph'])
        for a, b in zip(observations, observations[1:])
        if any(a[key] != b[key] for key in ('descriptor', 'formula', 'graph'))]
    assert any(item['work'] or item['formula'] for item in record['sketch_relocations']), (
        'Sketch growth did not exercise GWORK/formula relocation', record['sketch_relocations'])
    record['steps'].append('Fresh GWORK/formula consumers still trace X 2 to Y 4 after object growth, reentry and CLEAR')
    redraw((0x26,))


def _ui_case(emu, out, symbols):
    from basic_smoke_graph import _comp

    record = {'case': 'graph-ui', 'steps': []}
    snapshot = emu.call('save_snapshot', label='Before GRAPH keyboard acceptance')['id']
    s4 = emu.memory(0x90000, 65536)
    try:
        emu.call('reset')
        emu.call('resume')
        time.sleep(1)
        _comp(emu)
        font = emu.memory(0x80a0, 3)
        _until(emu, symbols['graph_mode_select'], (0x07, DIGITS[7]))
        _until(emu, 0x80800)
        out.joinpath('graph-selector-frame.bin').write_bytes(emu.memory(0x80e0, 384))
        record['steps'].append('MODE 7 selector')
        _until(emu, symbols['graph'], (DIGITS[1],))
        pc, _ = _until(emu, (0x12576, 0x80800), seconds=180)
        if pc == 0x80800:
            _until(emu, symbols['graph_input_tokens'], (0x63,))
            _until(emu, 0x12576)
        # The native editor receives real Math-input X-square keystrokes.
        _until(emu, symbols['graph_plot'], (0x70, 0x16, LETTERS['X'], 0x25, 0x63))
        _until(emu, 0x80800, seconds=180)
        record['steps'].append('GRAPH formula X squared confirmed and drawn')

        _until(emu, symbols['graph_menu'], (0x17,))
        _until(emu, 0x80800)
        _until(emu, symbols['graph_view_menu'], (DIGITS[3],))
        _until(emu, 0x80800)
        _until(emu, 0x80800, (0x57,))
        _until(emu, symbols['graph_plot'], (DIGITS[1],))
        _, registers = _until(emu, 0x80800, seconds=180)
        frame, address, state = _descriptor(emu, registers)
        window = [str(scalar_decimal(state[at:at + 20]))
                  for at in (192, 212, 232, 252)]
        assert [Decimal(value) for value in window] == list(map(Decimal, (-10, 10, -10, 10))), window
        pixels = emu.memory(0x80e0, 384)
        out.joinpath('graph-draw-frame.bin').write_bytes(pixels)
        out.joinpath('graph-draw-lcd.bin').write_bytes(emu.memory(0xf800, 512))

        def pixel(x, y):
            return bool(pixels[(y + 1) * 12 + x // 8] & (0x80 >> (x % 8)))

        # Both off-axis arms must be near the independently mapped parabola.
        arms = []
        for columns in (range(35, 43), range(53, 61)):
            hits = 0
            for x in columns:
                world = Decimal(-10) + Decimal(x) * 20 / 95
                y = int((Decimal(10) - world * world) * 30 / 20)
                if any(pixel(x, row) for row in range(max(0, y - 1), min(30, y + 1) + 1)):
                    hits += 1
            arms.append(hits)
        assert all(hits >= 5 for hits in arms), ('Missing parabola arms', arms)
        record.update(window=window, curve_columns=arms, frame=frame, descriptor=address)
        record['steps'].append('VIEW reset and off-axis parabola pixels')

        _until(emu, symbols['graph_menu'], (0x17,))
        _until(emu, 0x80800)
        _until(emu, symbols['graph_trace'], (DIGITS[1],))
        _until(emu, 0x80800, seconds=180)
        _until(emu, symbols['graph_number_input'], (0x63,))
        _until(emu, 0x12576)
        _, registers = _until(emu, 0x80800, (DIGITS[2], 0x63), seconds=60)
        _, address, state = _descriptor(emu, registers)
        x, y = scalar_decimal(state[4:24]), scalar_decimal(state[24:44])
        record.update(trace_x=str(x), trace_y=str(y), trace_status=state[3],
                      trace_descriptor=address, trace_registers=registers)
        out.joinpath('graph-trace-frame.bin').write_bytes(emu.memory(0x80e0, 384))
        assert state[3] == 0 and x == 2 and y == 4, record
        record['steps'].append('TRACE precise X 2 gives Y 4')

        _until(emu, symbols['graph_plot'], (0x26,))
        _until(emu, 0x80800, seconds=180)
        _cursor_cases(emu, out, symbols, record)
        _sketch_case(emu, out, symbols, record)
        _until(emu, symbols['graph_mode_select'], (0x26,))
        _until(emu, 0x80800)
        _until(emu, 0x1234e, (0x26,))
        assert emu.memory(0x8091, 1) == b'\x81', 'GRAPH exit did not restore COMP'
        assert emu.memory(0x80a0, 3) == font, 'GRAPH exit changed the native font state'
        emu.call('clear_execution_breakpoints')
        emu.call('resume')
        # Stop at native scanner entry only after EXE has evaluated the sum.
        emu.keys(0x70, DIGITS[1], 0x66, DIGITS[2])
        _until(emu, 0x1234e, (0x63,))
        ans = emu.memory(VARIABLE_ANS, 20)
        record['comp_ans'] = ans.hex()
        assert scalar_decimal(ans) == 3, record
        record['steps'].append('EXIT selector restores COMP and 1+2 gives 3')
        record['passed'] = True
    except Exception as error:
        record.update(passed=False, error=str(error), registers=emu.registers(),
                      status=emu.call('get_status'))
        out.joinpath('graph-ui-failure-frame.bin').write_bytes(emu.memory(0x80e0, 384))
    finally:
        record['s4_unchanged'] = emu.memory(0x90000, 65536) == s4
        if not record['s4_unchanged']:
            record.update(passed=False, error='GRAPH keyboard acceptance changed S4')
        emu.call('clear_execution_breakpoints')
        emu.call('load_snapshot', id=snapshot)
        _save(out, record)
    return record


def _table_lifecycle_case(emu, out, symbols):
    from basic_smoke_graph import _comp
    from basic_smoke_apps import _idle

    record = dict(case='graph-table-lifecycle', steps=[], observations=[])
    snapshot = emu.call('save_snapshot', label='Before native TABLE lifecycle')['id']
    s4 = emu.memory(0x90000, 65536)

    def formula():
        registers, data = emu.invoke(symbols['graph_formula_get'], pair(0, 0x8500),
                                     [(0x8500, bytes(6))], [(0x8500, 6)], seconds=3)
        assert registers['r0'] == 0, registers
        address = int.from_bytes(data[0][:2], 'little') | data[0][2] << 16
        size = int.from_bytes(data[0][4:6], 'little')
        assert 0 < size < 0x8000, data[0].hex()
        return address, emu.memory(address, size)

    def table():
        # ROM's lookup outputs are type, handle, far payload, allocated length.
        args = [0xe748, 1, 0x8500, 0, 0x8504, 0, 0x8508, 0, 0x850c, 0]
        registers, data = emu.invoke(
            0x1a574, pair(0, 0xe798) | {'r2': 1},
            [(0x8500, bytes(16)),
             (0x8c00, b''.join(value.to_bytes(2, 'little') for value in args))],
            [(0x8500, 16)], seconds=3)
        status = registers['r0'] | registers['r1'] << 8
        if status == 0x30:
            return None
        assert status == 0, registers
        meta = data[0]
        address = int.from_bytes(meta[8:10], 'little') | meta[10] << 16
        size = int.from_bytes(meta[12:16], 'little')
        assert meta[0] == 0x0c and 2 <= size <= 0x8000, meta.hex()
        payload = emu.memory(address, size)
        rows, columns = payload[:2]
        assert rows == 3 and columns == 2 and size >= 2 + rows * columns * 10, payload.hex()
        pairs = [[str(scalar_decimal(payload[at:at + 10] + bytes(10))),
                  str(scalar_decimal(payload[at + 10:at + 20] + bytes(10)))]
                 for at in range(2, 2 + rows * 20, 20)]
        assert [[Decimal(value) for value in pair] for pair in pairs] == [
            [Decimal(0), Decimal(1)], [Decimal(1), Decimal(2)], [Decimal(2), Decimal(5)]], pairs
        return dict(address=address, allocated=size, pairs=pairs, payload=payload.hex())

    def trace(name):
        _until(emu, symbols['graph_menu'], (0x17,))
        _until(emu, 0x80800)
        _until(emu, symbols['graph_trace'], (DIGITS[1],))
        _until(emu, 0x80800, seconds=180)
        _until(emu, symbols['graph_number_input'], (0x63,))
        _until(emu, 0x12576)
        _, registers = _until(emu, 0x80800, (DIGITS[2], 0x63), seconds=60)
        frame, address, state = _descriptor(emu, registers)
        x, y = scalar_decimal(state[4:24]), scalar_decimal(state[24:44])
        source, raw = formula()
        data = emu.memory(frame + 120, 6)
        current = int.from_bytes(data[:2], 'little') | data[2] << 16
        observation = dict(name=name, frame=frame, descriptor=address,
                           formula=source, formula_bytes=raw.hex(), x=str(x),
                           y=str(y), status=state[3], table=table())
        record['observations'].append(observation)
        assert state[3] == 0 and x == 2 and y == 5, observation
        assert current == source and int.from_bytes(data[4:6], 'little') == len(raw), observation
        actual = observation['table']
        assert (actual['payload'] if actual else None) == record['expected_table'], observation
        out.joinpath(name + '-frame.bin').write_bytes(emu.memory(0x80e0, 384))
        _until(emu, symbols['graph_plot'], (0x26,))
        _until(emu, 0x80800, seconds=180)
        return source, raw

    try:
        emu.call('reset')
        emu.call('resume')
        time.sleep(1)
        _comp(emu)
        _until(emu, symbols['graph_mode_select'], (0x07, DIGITS[7]))
        _until(emu, 0x80800)
        _until(emu, 0x7960, (DIGITS[2],))
        _until(emu, 0x12576)
        _until(emu, 0x7d5e,
               (0x70, 0x16, LETTERS['X'], 0x25, 0x66, DIGITS[1], 0x63))
        _idle(emu)
        for index, value in enumerate((0, 2, 1)):
            _until(emu, 0xef77e, (DIGITS[value],))
            _idle(emu)
            _until(emu, 0xef8c2, (0x63,))
            registers = _idle(emu)
            pc = registers['pc']
            result, data = emu.invoke(
                0xe3ea2, {'r0': 0x41, 'r1': index} | pair(2, 0x8500),
                [(0x8500, bytes(20))], [(0x8500, 20)], seconds=3)
            record['steps'].append(dict(field=('Start', 'End', 'Step')[index],
                                        value=value, native=data[0].hex(),
                                        continuation=pc, registers=registers))
            assert result['r0'] | result['r1'] << 8 == 0, result
            assert scalar_decimal(data[0]) == value, record['steps'][-1]
        _until(emu, 0xdc0c4, (0x63,))
        # 7EB0 opens the successful native TABLE viewer.
        _until(emu, 0x1fdf8, seconds=180)
        assert emu.registers()['r0'] == 0x42, emu.registers()
        _idle(emu)
        record['table'] = table()
        out.joinpath('graph-native-table-frame.bin').write_bytes(emu.memory(0x80e0, 384))
        record['steps'].append('Native TABLE viewer contains (0,1), (1,2), (2,5)')
        record['expected_table'] = record['table']['payload']
        live = emu.call('save_snapshot', label='Before nested GRAPH with live TABLE samples')['id']
        _until(emu, 0xe3694, (0x26,))
        _idle(emu)
        record['table_after_native_exit'] = table()
        assert record['table_after_native_exit'] is None, record
        record['expected_table'] = None
        _until(emu, 0x7960, (0x26,))
        _idle(emu)
        _idle(emu, (0x07, DIGITS[1]))
        assert emu.memory(0x8091, 1) == b'\x81'
        record['steps'].append('Native viewer EXIT deletes its temporary TABLE samples and retains the shared formula')
        _until(emu, symbols['graph_mode_select'], (0x07, DIGITS[7]))
        _until(emu, 0x80800)
        _until(emu, symbols['graph'], (DIGITS[1],))
        _until(emu, symbols['graph_plot'])
        _until(emu, 0x80800, seconds=180)
        before, shared = trace('graph-table-shared-trace')
        record['steps'].append('Physical GRAPH rereads TABLE formula and traces X 2 to Y 5 after native sample cleanup')

        _until(emu, symbols['graph_input_tokens'], (0x63,))
        _until(emu, 0x12576)
        _until(emu, symbols['graph_plot'], (0x70, DIGITS[9], 0x26))
        _until(emu, 0x80800, seconds=180)
        after, cancelled = formula()
        record['cancel'] = dict(before=before, after=after, formula=cancelled.hex())
        assert cancelled == shared, record['cancel']
        trace('graph-table-cancel-trace')
        record['steps'].append('Native formula editor cancellation preserves the previous exact shared source')

        _until(emu, symbols['graph_input_tokens'], (0x63,))
        _until(emu, 0x12576)
        keys = (0x70, 0x16, LETTERS['X'], 0x25, 0x66, DIGITS[1])
        keys += (0x66, DIGITS[0]) * 40
        _until(emu, symbols['graph_plot'], keys + (0x63,), seconds=180)
        _until(emu, 0x80800, seconds=180)
        moved, long_source = trace('graph-table-long-trace')
        record['long_edit'] = dict(before=after, after=moved, old_size=len(shared),
                                   size=len(long_source), source=long_source.hex())
        assert len(long_source) > len(shared) and moved != after, record['long_edit']
        record['steps'].append('Long native editor commit relocates shared source; fresh GRAPH lookup still gives Y 5')
        _until(emu, symbols['graph_mode_select'], (0x26,))
        _until(emu, 0x80800)
        _until(emu, 0x1234e, (0x26,))
        assert emu.memory(0x8091, 1) == b'\x81', 'TABLE lifecycle did not restore COMP'
        # End with the suspended-viewer probe so restored timers need no keyboard input.
        emu.call('load_snapshot', id=live)
        emu.invoke(symbols['graph'], {'sp': emu.registers()['sp']},
                   stop_at=symbols['graph_plot'], keep=True, seconds=10)
        _until(emu, 0x80800, seconds=180)
        _, address, _ = _descriptor(emu, emu.registers())
        from firmware.e5800p.graph_math import _number
        registers, data = emu.invoke(
            symbols['graph_eval'], pair(0, address & 0xffff) | {'r2': address >> 16},
            [(address + 4, _number('2'))], [(address, 44)], seconds=30)
        record['live_probe'] = dict(method='Diagnostic nested GRAPH with native TABLE frame alive',
                                    x=str(scalar_decimal(data[0][4:24])),
                                    y=str(scalar_decimal(data[0][24:44])),
                                    status=registers['r0'], table=table())
        assert registers['r0'] == 0 and scalar_decimal(data[0][24:44]) == 5, record['live_probe']
        assert record['live_probe']['table']['payload'] == record['table']['payload'], record['live_probe']
        record['steps'].append('Diagnostic nested GRAPH preserves live native TABLE samples during drawing and evaluation')
        record['passed'] = True
    except Exception as error:
        record.update(passed=False, error=str(error), registers=emu.registers(),
                      status=emu.call('get_status'))
        out.joinpath('graph-table-lifecycle-failure-frame.bin').write_bytes(emu.memory(0x80e0, 384))
    finally:
        record['s4_unchanged'] = emu.memory(0x90000, 65536) == s4
        if not record['s4_unchanged']:
            record.update(passed=False, error='TABLE lifecycle changed S4')
        emu.call('clear_execution_breakpoints')
        emu.call('load_snapshot', id=snapshot)
        _save(out, record)
    return record


def graph_cases(emu, out):
    """Run the full numerical matrix, then keyboard GRAPH; retain every failure."""
    from firmware.e5800p.graph_math import _number
    from firmware.e5800p.project import fw

    out.mkdir(parents=True, exist_ok=True)
    linked = fw.link()
    symbols = linked['symbols']
    required = ('graph_calc', 'graph_cancel', 'graph', 'graph_mode_select', 'graph_plot',
                'graph_menu', 'graph_view_menu', 'graph_trace',
                'graph_input_tokens', 'graph_number_input')
    for name in required:
        block = next(block for block in linked['blocks'] if block['name'] == name)
        size = min(16, len(block['data']))
        assert emu.memory(symbols[name], size) == block['data'][:size], (
            'Running firmware does not match GRAPH symbols', name, hex(symbols[name]))
    emu.active()
    results = (_frame_cases(emu, out, symbols) + _stored_cases(emu, out, symbols)
               + _plot_cases(emu, out, symbols))
    cases = []

    def add(name, source, op, x='0', a='-2', b='2', *, y=None, point=None,
            statuses=(0,), flags=0, angle=None, tolerance=TOL, cancel=False):
        cases.append(dict(case='graph-' + name, source=source, operation=op,
                          x=x, a=a, b=b, y=y, point=point, statuses=statuses,
                          flags=flags, angle=angle, tolerance=tolerance, cancel=cancel))

    square = b'X\xa9X'
    tangent = b'(X\x991)\xa9(X\x991)'
    sin = b'\x81X)'
    add('root-sqrt2', square + b'\x992', 1, x='1.5', a='1', b='2',
        point=(str(Decimal(2).sqrt()), '0'))
    add('root-tangent', tangent, 1, x='1', a='0', b='2', point=('1', '0'))
    add('root-positive-valley', b'1\x0f12\xa9' + tangent + b'\x891', 1,
        x='1', a='0', b='2', statuses=(6,))
    add('root-pole', b'1\xb9(X\x990.3)', 1, x='0.3', a='0', b='1',
        statuses=(1, 4, 5, 6))
    add('minimum', tangent + b'\x892', 2, x='1', a='-2', b='4', point=('1', '2'))
    add('maximum', b'0\x99(X\x892)\xa9(X\x892)\x893', 3,
        x='-2', a='-5', b='1', point=('-2', '3'))
    add('minimum-endpoint', b'X', 2, a='-2', b='5', point=('-2', '-2'), flags=1)
    add('maximum-endpoint', b'X', 3, a='-2', b='5', point=('5', '5'), flags=1)
    add('minimum-flat', b'7', 2, y='7', flags=2)
    add('maximum-flat', b'7', 3, y='7', flags=2)
    add('minimum-cubic', b'X\xa9X\xa9X', 2, a='-1', b='1', point=('-1', '-1'), flags=1)
    add('maximum-cubic', b'X\xa9X\xa9X', 3, a='-1', b='1', point=('1', '1'), flags=1)
    add('integral-square', square, 5, a='0', b='1', y=str(Decimal(1) / 3))
    add('integral-sin-rad', sin, 5, a='0', b='3.14159265358979', y='2', angle='rad')
    add('integral-reversed', square, 5, a='1', b='0', y=str(-Decimal(1) / 3))
    add('integral-same', square, 5, a='2', b='2', y='0')
    add('integral-singularity', b'1\xb9X', 5, a='-1', b='1', statuses=(1, 4))
    cancellation = Decimal(2) * PI * PI
    add('integral-cancellation', b'1000\xa9\x8120\xa9X)\x89X', 5,
        a='0', b='6.28318530717959', y=str(cancellation), angle='rad',
        tolerance=max(TOL, TOL * abs(cancellation)))
    add('integral-narrow-peak', b'1\xb9(1\x891\x0f6\xa9X\xa9X)', 5,
        a='-1', b='1', y='0.00313959265425646')
    add('integral-depth-limit', b'1\xb9(1\x891\x0f24\xa9X\xa9X)', 5,
        a='-1', b='1', statuses=(4,))
    add('integral-exit-cancel', b'\x8110000\xa9X)', 5, a='0', b='3',
        statuses=(2,), angle='rad', cancel=True)
    add('slope-square', square, 4, x='2', y='4')
    add('slope-sin-rad', sin, 4, y='1', angle='rad')
    add('slope-sin-deg', sin, 4, y=str(PI / 180), angle='deg')
    add('slope-cusp', b'\x97X)', 4, statuses=(1,))
    add('slope-large-offset', b'1\x0f10\x89X', 4, y='1', statuses=(0, 4))
    add('unstable-random', b'\xc1', 4, statuses=(7,))

    sentinels = {f'r{i}': 0x90 + i for i in range(4, 16)}
    variables = {'A': VARIABLE_A, 'B': VARIABLE_A + 20,
                 'X': VARIABLE_X, 'Ans': VARIABLE_ANS}
    numbers = {name: _number(str(value))
               for name, value in zip(variables, (13, 17, 23, 29))}
    for spec in cases:
        record = {key: value for key, value in spec.items()
                  if key not in ('source', 'tolerance')}
        record.update(source=spec['source'].hex(), tolerance=str(spec['tolerance']),
                      entry=symbols['graph_calc'], descriptor=STATE)
        try:
            state = bytearray(4096 + len(spec['source']) + 1)
            state[3072:3074] = (len(spec['source']) + 1).to_bytes(2, 'little')
            state[3074] = spec['operation']
            for offset, value in ((4, spec['x']), (44, spec['a']), (64, spec['b'])):
                assert scalar_decimal(_number(value)) == Decimal(value), ('Native20 fixture', value)
                state[3072 + offset:3072 + offset + 20] = _number(value)
            state[4096:] = spec['source'] + b'\0'
            math = emu.memory(0x8000, 112)
            mode = emu.memory(0x8090, 2)
            angle = emu.memory(0x8099, 1)
            writes = [(WORK, state), (0x8086, b'\0\0'), (STACK, b'\xa5' * STACK_SIZE)]
            writes.extend((variables[name], value) for name, value in numbers.items())
            if spec['angle'] is not None:
                # SHIFT MODE 4/3 changes only ROM-A27's RAD bit at 8099.
                angle = bytes([(angle[0] & ~1) | (spec['angle'] == 'rad')])
                writes.append((0x8099, angle))
            reads = [(STATE, 1024), (0x8000, 112), (0x8086, 2), (0x8090, 2)]
            reads.extend((address, 20) for address in variables.values())
            reads.extend(((STACK, STACK_SIZE), (0x8099, 1)))
            inputs = pair(0, STATE & 0xffff) | {'r2': STATE >> 16} | sentinels
            record['registers_before'] = inputs | {'sp': 0x8c00, 'psw': 0, 'lr': 0}
            if spec['cancel']:
                snapshot = emu.call('save_snapshot', label='Before GRAPH EXIT cancellation')['id']
                try:
                    emu.invoke(symbols['graph_calc'], inputs, writes, seconds=30,
                               keep=True, stop_at=symbols['graph_cancel'])
                    emu.call('keyboard_code', code=0x26, pressed=True)
                    _, registers = _until(emu, 0, seconds=10)
                    data = [emu.memory(address, size) for address, size in reads]
                finally:
                    emu.call('keyboard_code', code=0x26, pressed=False)
                    emu.call('clear_execution_breakpoints')
                    emu.call('load_snapshot', id=snapshot)
            else:
                registers, data = emu.invoke(
                    symbols['graph_calc'], inputs, writes, reads, seconds=300)
            result = data[0]
            status, flags = result[3], int.from_bytes(result[84:86], 'little')
            record.update(registers=registers, status=status, flags_actual=flags,
                          native_x=result[4:24].hex(), native_y=result[24:44].hex(),
                          math_before=math.hex(), math_after=data[1].hex(),
                          workspace_before='0000', workspace_after=data[2].hex(),
                          mode_before=mode.hex(), mode_after=data[3].hex(),
                          angle_before=angle.hex(), angle_after=data[9].hex(),
                          variables_before={name: value.hex() for name, value in numbers.items()},
                          variables_after={name: value.hex() for name, value in zip(variables, data[4:8])})
            changed = [index for index, byte in enumerate(data[8]) if byte != 0xa5]
            low = STACK + min(changed) if changed else 0x8c00
            record.update(stack_first_changed=low, stack_used_lower_bound=0x8c00 - low,
                          stack_guard_preserved=data[8][:32] == b'\xa5' * 32)
            errors = []
            if registers['sp'] != 0x8c00:
                errors.append('Unbalanced SP')
            if any(registers[name] != value for name, value in sentinels.items()):
                errors.append('R4..R15 not preserved')
            if registers['r0'] != status:
                errors.append('R0 disagrees with descriptor status')
            if data[1] != math or data[2] != b'\0\0' or data[3] != mode or data[9] != angle:
                errors.append('Native math/workspace/mode not preserved')
            if any(value != numbers[name] for name, value in zip(variables, data[4:8])):
                errors.append('A/B/X/Ans not preserved')
            if not record['stack_guard_preserved']:
                errors.append('Stack watermark reached the guard')
            if status not in spec['statuses']:
                errors.append('Unexpected analysis status')
            if flags & spec['flags'] != spec['flags']:
                errors.append('Missing ENDPOINT/FLAT flag')
            for name, offset in (('x', 4), ('y', 24)):
                try:
                    record['actual_' + name] = str(scalar_decimal(result[offset:offset + 20]))
                except ValueError as error:
                    record[name + '_decode_error'] = str(error)
            if status == 0:
                expected = spec['point'] or (None, spec['y'])
                for name, value in zip(('x', 'y'), expected):
                    if value is not None:
                        actual = Decimal(record['actual_' + name])
                        error = abs(actual - Decimal(value))
                        record[name + '_absolute_error'] = str(error)
                        if error > spec['tolerance']:
                            errors.append(name.upper() + ' outside numerical tolerance')
                if spec['flags'] & 2 and not Decimal(spec['a']) <= Decimal(record['actual_x']) <= Decimal(spec['b']):
                    errors.append('FLAT point outside interval')
            record.update(passed=not errors, errors=errors)
        except Exception as error:
            record.update(passed=False, error=str(error))
        results.append(_save(out, record))

    results.append(_ui_case(emu, out, symbols))
    results.append(_table_lifecycle_case(emu, out, symbols))
    out.joinpath('graph-cases.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    failures = [record for record in results if not record['passed']]
    assert not failures, [(record['case'], record.get('status'), record.get('errors', record.get('error')))
                          for record in failures]
    return results
