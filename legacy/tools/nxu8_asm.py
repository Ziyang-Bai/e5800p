"""PC-side nX-U8 assembly using the firmware instruction catalogue.

Numbers are decimal, 0x hexadecimal, or hexadecimal with an H suffix. Symbols
are case-insensitive; expressions support integer + and -. DB accepts quoted
ASCII with doubled quotes. .equ NAME, expression (or NAME EQU expression),
.org address (zero padding), DB and DW do not impose instruction alignment.
Memory operands accept immediate, register and reused DSR prefixes, e.g.
4:[ER2], R3:0x8000 and DSR:4[ER2]. Code addresses are 20-bit; a numeric branch
operand below 0x10000 means an offset in the current code segment. Symbolic
branch operands and CALL_SYS operands are absolute addresses.
Numeric MOV ER immediates use the native signed seven-bit form when possible;
other uint16 values and symbolic immediates use two byte-register MOVs. Keeping
symbolic immediates wide makes forward-label layout independent of their values.
"""

import re

from instruction_table import (ENTRIES, opcode_mask, IMM, RR, EE, EI7, SHIFT,
                               ER_R, ONE_R, ONE_ER, R_ABS, R_IND, R_DISP,
                               ER_ABS, ER_IND, ER_DISP, BR, FAR, FAR_SYS, TB,
                               SP_IMM, FIXED, EXTBW, ER_SP, SP_ER, SUB_IMM,
                               ONE_XR, ONE_QR)

# Host-only forms; the on-device catalogue and its firmware layout stay unchanged.
R_BASE, ER_BASE, R_EA, ER_EA, XR_EA, QR_EA, BR_REG, LEA_IND, LEA_DISP, LEA_ABS = range(26, 36)
R_CTRL, CTRL_R = range(36, 38)
_ENTRIES = ENTRIES + (
    (EI7, 0xe000, 'MOV ER,#'), (SHIFT, 0x900d, 'SRLC R,#'),
    (BR, 0xce00, 'BAL'), (BR_REG, 0xf002, 'B ER'), (BR_REG, 0xf003, 'BL ER'),
    (R_BASE, 0xd000, 'L R,D[BP]'), (R_BASE, 0xd040, 'L R,D[FP]'),
    (R_BASE, 0xd080, 'ST R,D[BP]'), (R_BASE, 0xd0c0, 'ST R,D[FP]'),
    (ER_BASE, 0xb000, 'L ER,D[BP]'), (ER_BASE, 0xb040, 'L ER,D[FP]'),
    (ER_BASE, 0xb080, 'ST ER,D[BP]'), (ER_BASE, 0xb0c0, 'ST ER,D[FP]'),
    (R_EA, 0x9030, 'L R,[EA]'), (R_EA, 0x9050, 'L R,[EA+]'),
    (R_EA, 0x9031, 'ST R,[EA]'), (R_EA, 0x9051, 'ST R,[EA+]'),
    (ER_EA, 0x9032, 'L ER,[EA]'), (ER_EA, 0x9052, 'L ER,[EA+]'),
    (ER_EA, 0x9033, 'ST ER,[EA]'), (ER_EA, 0x9053, 'ST ER,[EA+]'),
    (XR_EA, 0x9034, 'L XR,[EA]'), (XR_EA, 0x9054, 'L XR,[EA+]'),
    (XR_EA, 0x9035, 'ST XR,[EA]'), (XR_EA, 0x9055, 'ST XR,[EA+]'),
    (QR_EA, 0x9036, 'L QR,[EA]'), (QR_EA, 0x9056, 'L QR,[EA+]'),
    (QR_EA, 0x9037, 'ST QR,[EA]'), (QR_EA, 0x9057, 'ST QR,[EA+]'),
    (LEA_IND, 0xf00a, 'LEA [ER]'), (LEA_DISP, 0xf00b, 'LEA D[ER]'),
    (LEA_ABS, 0xf00c, 'LEA ADDR'),
    (TB, 0xa000, 'SB R.B'), (TB, 0xa002, 'RB R.B'),
    (FIXED, 0xed08, 'EI'), (FIXED, 0xebf7, 'DI'),
    (FIXED, 0xfe2f, 'INC [EA]'), (FIXED, 0xfe3f, 'DEC [EA]'),
    (R_CTRL, 0xa003, 'MOV R,PSW'), (CTRL_R, 0xa00b, 'MOV PSW,R'),
    (FIXED, 0xfe0f, 'RTI'),
)
_MEMORY = (R_ABS, R_IND, R_DISP, ER_ABS, ER_IND, ER_DISP,
           R_BASE, ER_BASE, R_EA, ER_EA, XR_EA, QR_EA)
_LONG = (R_ABS, R_DISP, ER_ABS, ER_DISP, FAR, FAR_SYS, LEA_DISP, LEA_ABS)
_SYMBOL = r"[A-Za-z_][A-Za-z_0-9]*"
_NUMBER = r"(?:0[xX][0-9A-Fa-f]+|[0-9][0-9A-Fa-f]*[hH]|[0-9]+)"
_TOKEN = re.compile(rf"\s*({_NUMBER}|{_SYMBOL}|[+-])")


def _split(text, separator=','):
    """Split outside strings; a doubled quote is a literal quote."""
    parts, start, quoted, i = [], 0, False, 0
    while i < len(text):
        if text[i] == '"':
            if quoted and i + 1 < len(text) and text[i + 1] == '"':
                i += 2
                continue
            quoted = not quoted
        elif not quoted and text[i] == separator:
            parts.append(text[start:i].strip())
            if separator == ';':
                return parts
            start = i + 1
        i += 1
    if quoted:
        raise ValueError('unterminated string')
    parts.append(text[start:].strip())
    return parts


def _expression(text, resolve):
    text = text.strip().removeprefix('#').strip()
    value, sign, operand, symbolic, pos = 0, 1, True, False, 0
    while pos < len(text):
        match = _TOKEN.match(text, pos)
        if not match:
            raise ValueError(f'bad expression: {text}')
        token = match[1]
        pos = match.end()
        if token in ('+', '-'):
            if operand:
                sign *= -1 if token == '-' else 1
            else:
                sign = -1 if token == '-' else 1
                operand = True
            continue
        if not operand:
            raise ValueError(f'bad expression: {text}')
        if re.fullmatch(_NUMBER, token):
            number = (int(token[:-1], 16) if token[-1:].lower() == 'h'
                      else int(token, 16 if token.lower().startswith('0x') else 10))
        else:
            symbolic = True
            number = resolve(token.upper())
        value += sign * number
        sign, operand = 1, False
    if operand:
        raise ValueError(f'bad expression: {text}')
    return value, symbolic


def _range(value, low, high, what):
    if not low <= value <= high:
        raise ValueError(f'{what} outside {low}..{high}: {value}')
    return value


def _reg(text, prefix):
    match = re.fullmatch(prefix + r'(\d+)', text, re.I)
    if not match:
        raise ValueError(f'expected {prefix} register: {text}')
    number = int(match[1])
    alignment = {'R': 1, 'ER': 2, 'XR': 4, 'QR': 8}[prefix]
    if number > 16 - alignment or number % alignment:
        raise ValueError(f'invalid {prefix} register: {text}')
    return number


def _word(value):
    return (value & 0xffff).to_bytes(2, 'little')


def _signed(text, bits, resolve, sizing):
    value = _expression(text, resolve)[0]
    raw = bool(re.fullmatch(r'#?\s*(?:0[xX][0-9A-Fa-f]+|[0-9][0-9A-Fa-f]*[hH])', text))
    if not sizing:
        _range(value, 0 if raw else -(1 << (bits - 1)),
               (1 << bits) - 1 if raw else (1 << (bits - 1)) - 1, 'signed immediate')
    return value & ((1 << bits) - 1)


def _target(text, pc, resolve, sizing, absolute=False):
    if ':' in text:
        segment, offset = text.split(':', 1)
        segment = _expression(segment, resolve)[0]
        offset = _expression(offset, resolve)[0]
        if not sizing:
            _range(segment, 0, 15, 'code segment')
            _range(offset, 0, 65535, 'code offset')
        value = segment * 65536 + offset
    else:
        value, symbolic = _expression(text, resolve)
        if not absolute and not symbolic and 0 <= value <= 65535:
            value |= pc & 0xf0000
    if not sizing:
        _range(value, 0, 0xfffff, 'code address')
        if value & 1:
            raise ValueError('odd branch target')
    return value


def _instruction(text, pc, resolve, sizing=False):
    parts = text.split(None, 1)
    mnemonic = {'RT': 'RET', 'B': 'JMP', 'BL': 'CALL'}.get(parts[0].upper(), parts[0].upper())
    args = _split(parts[1]) if len(parts) == 2 else []
    if mnemonic in ('JMP', 'CALL') and len(args) == 1 and re.fullmatch(r'ER\d+', args[0], re.I):
        mnemonic = 'B' if mnemonic == 'JMP' else 'BL'
    compact = mnemonic + (' ' + ','.join(arg.upper().replace(' ', '') for arg in args) if args else '')
    for kind, opcode, name in _ENTRIES:
        if kind == FIXED and compact == name:
            return _word(opcode)
    if mnemonic == 'MOV' and len(args) == 2 and re.fullmatch(r'ER\d+', args[0], re.I) and args[1].startswith('#'):
        reg = _reg(args[0], 'ER')
        value, symbolic = _expression(args[1], resolve)
        if not symbolic and (-64 <= value <= 63 or 0xffc0 <= value <= 0xffff):
            return _word(0xe000 | reg << 8 | (value & 127))
        if not sizing:
            _range(value, 0, 65535, 'word immediate')
        return bytes((value & 255, reg, (value >> 8) & 255, reg + 1))

    prefix, memory, mem_kind = b'', None, None
    if mnemonic in ('L', 'ST') and len(args) == 2:
        memory = args[1]
        if ':' in memory:
            segment, memory = (part.strip() for part in memory.split(':', 1))
            if segment.upper() == 'DSR':
                prefix = _word(0xfe9f)
            elif re.fullmatch(r'R\d+', segment, re.I):
                prefix = _word(0x900f | (_reg(segment, 'R') << 4))
            else:
                value = _expression(segment, resolve)[0]
                if not sizing:
                    _range(value, 0, 255, 'data segment')
                prefix = _word(0xe300 | (value & 255))
        indirect = re.fullmatch(r'(.*?)\[\s*(ER\d+|BP|FP)\s*\]', memory, re.I)
        pair = bool(re.fullmatch(r'ER\d+', args[0], re.I))
        if memory.upper().replace(' ', '') in ('[EA]', '[EA+]'):
            register = re.fullmatch(r'(R|ER|XR|QR)\d+', args[0], re.I)
            mem_kind = {'R': R_EA, 'ER': ER_EA, 'XR': XR_EA, 'QR': QR_EA}.get(
                register[1].upper() if register else '')
        elif indirect and indirect[2].upper() in ('BP', 'FP'):
            mem_kind = ER_BASE if pair else R_BASE
        else:
            mem_kind = ((ER_IND if pair else R_IND) if indirect and not indirect[1].strip()
                        else (ER_DISP if pair else R_DISP) if indirect
                        else (ER_ABS if pair else R_ABS))

    errors = []
    for kind, opcode, name in _ENTRIES:
        if name.split()[0] != mnemonic or kind == FIXED:
            continue
        try:
            word, extra = opcode, b''
            if kind in (IMM, SUB_IMM, EI7, SHIFT, SP_IMM):
                if len(args) != 2 or not args[1].startswith('#'):
                    continue
                if kind == SP_IMM:
                    if args[0].upper() != 'SP':
                        continue
                    word |= _signed(args[1], 8, resolve, sizing)
                else:
                    reg = _reg(args[0], 'ER' if kind == EI7 else 'R')
                    word |= reg << 8
                    if kind == EI7:
                        word |= _signed(args[1], 7, resolve, sizing)
                    else:
                        value = _expression(args[1], resolve)[0]
                        if not sizing:
                            _range(value, 0, 7 if kind == SHIFT else 255, 'immediate')
                        if kind == SUB_IMM:
                            tmp = 1 if reg == 0 else 0
                            return (_word(0xf04e | tmp << 8) + _word(tmp << 8 | (value & 255))
                                    + _word(0x8008 | reg << 8 | tmp << 4) + _word(0xf00e | tmp << 8))
                        word |= (value & 7) << 4 if kind == SHIFT else value & 255
            elif kind in (RR, EE, ER_R):
                if len(args) != 2:
                    continue
                word |= _reg(args[0], 'R' if kind == RR else 'ER') << 8
                word |= _reg(args[1], 'ER' if kind == EE else 'R') << 4
            elif kind in (ONE_R, ONE_ER, ONE_XR, ONE_QR, EXTBW):
                if len(args) != 1:
                    continue
                reg = _reg(args[0], {ONE_R: 'R', ONE_ER: 'ER', ONE_XR: 'XR', ONE_QR: 'QR', EXTBW: 'ER'}[kind])
                word |= reg << 8
                if kind == EXTBW:
                    word |= reg << 4
            elif kind in (ER_SP, SP_ER):
                if len(args) != 2 or args[1 if kind == ER_SP else 0].upper() != 'SP':
                    continue
                word |= _reg(args[0 if kind == ER_SP else 1], 'ER') << (8 if kind == ER_SP else 4)
            elif kind == TB:
                if len(args) != 1 or '.' not in args[0]:
                    continue
                reg, bit = args[0].split('.', 1)
                value = _expression(bit, resolve)[0]
                if not sizing:
                    _range(value, 0, 7, 'bit')
                word |= _reg(reg, 'R') << 8 | (value & 7) << 4
            elif kind in (R_CTRL, CTRL_R):
                if len(args) != 2 or args[1 if kind == R_CTRL else 0].upper() != 'PSW':
                    continue
                word |= _reg(args[0 if kind == R_CTRL else 1], 'R') << (8 if kind == R_CTRL else 4)
            elif kind == BR_REG:
                if len(args) != 1:
                    continue
                word |= _reg(args[0], 'ER') << 4
            elif kind in (LEA_IND, LEA_DISP, LEA_ABS):
                if len(args) != 1:
                    continue
                operand = re.fullmatch(r'(.*?)\[\s*(ER\d+)\s*\]', args[0], re.I)
                form = LEA_ABS if not operand else LEA_DISP if operand[1].strip() else LEA_IND
                if kind != form:
                    continue
                if operand:
                    word |= _reg(operand[2], 'ER') << 4
                if kind == LEA_DISP:
                    extra = _word(_signed(operand[1].strip(), 16, resolve, sizing))
                elif kind == LEA_ABS:
                    value = _expression(args[0], resolve)[0]
                    if not sizing:
                        _range(value, 0, 65535, 'data offset')
                    extra = _word(value)
            elif kind in _MEMORY:
                if kind != mem_kind:
                    continue
                register = {ER_ABS: 'ER', ER_IND: 'ER', ER_DISP: 'ER', ER_BASE: 'ER',
                            ER_EA: 'ER', XR_EA: 'XR', QR_EA: 'QR'}.get(kind, 'R')
                word |= _reg(args[0], register) << 8
                if kind in (R_BASE, ER_BASE):
                    if indirect[2].upper() != ('FP' if opcode & 0x40 else 'BP'):
                        continue
                    word |= _signed(indirect[1].strip() or '0', 6, resolve, sizing)
                elif kind in (R_EA, ER_EA, XR_EA, QR_EA):
                    if memory.upper().replace(' ', '') != name.split(',')[1]:
                        continue
                if kind in (R_IND, ER_IND, R_DISP, ER_DISP):
                    word |= _reg(indirect[2], 'ER') << 4
                if kind in (R_DISP, ER_DISP):
                    extra = _word(_signed(indirect[1].strip(), 16, resolve, sizing))
                elif kind in (R_ABS, ER_ABS):
                    value = _expression(memory, resolve)[0]
                    if not sizing:
                        _range(value, 0, 65535, 'data offset')
                    extra = _word(value)
            elif kind in (BR, FAR, FAR_SYS):
                if len(args) != 1:
                    continue
                target = _target(args[0], pc, resolve, sizing, kind == FAR_SYS)
                if kind == BR:
                    delta = ((target & 65535) - ((pc + 2) & 65535)) & 65535
                    if delta >= 32768:
                        delta -= 65536
                    if not sizing:
                        if target >> 16 != pc >> 16:
                            raise ValueError('relative branch crosses code segment')
                        _range(delta // 2, -128, 127, 'branch displacement')
                    word |= (delta // 2) & 255
                else:
                    word = (opcode & 0xf0ff) | ((target >> 16) & 15) << 8
                    extra = _word(target)
            else:
                continue
            return prefix + _word(word) + extra
        except ValueError as exc:
            errors.append(str(exc))
    raise ValueError('; '.join(dict.fromkeys(errors)) if errors else f'unknown instruction or operands: {text}')


def assemble(source: str, origin: int = 0) -> tuple[bytes, dict[str, int], list[dict]]:
    """Return contiguous bytes, absolute symbols and source-line listing records."""
    _range(origin, 0, 0xfffff, 'origin')
    lines, definitions, symbols = [], {}, {}
    for number, raw in enumerate(source.splitlines(), 1):
        try:
            text = _split(raw, ';')[0]
            label = None
            match = re.match(rf'^({_SYMBOL})\s*:\s*', text)
            if match:
                label, text = match[1].upper(), text[match.end():].strip()
            equ = re.fullmatch(rf'({_SYMBOL})\s+\.?EQU\s+(.+)', text, re.I)
            if not equ:
                equ = re.fullmatch(rf'\.?EQU\s+({_SYMBOL})\s*,\s*(.+)', text, re.I)
            if equ:
                if label:
                    raise ValueError('label before EQU')
                label, expression = equ[1].upper(), equ[2]
            else:
                expression = None
            if label:
                if label in definitions:
                    raise ValueError(f'duplicate symbol: {label}')
                definitions[label] = (expression, number)
            lines.append((number, label, text, expression))
        except ValueError as exc:
            raise ValueError(f'line {number}: {exc}') from None

    resolving = set()

    def resolve(name):
        if name in symbols:
            return symbols[name]
        if name not in definitions or definitions[name][0] is None:
            raise ValueError(f'undefined symbol: {name}')
        if name in resolving:
            raise ValueError(f'cyclic constant: {name}')
        resolving.add(name)
        try:
            return _expression(definitions[name][0], resolve)[0]
        finally:
            resolving.remove(name)

    def data(text, sizing):
        parts = text.split(None, 1)
        directive = parts[0].upper().lstrip('.')
        if directive not in ('DB', 'DW'):
            return None
        if len(parts) != 2:
            raise ValueError(f'{directive} needs data')
        result = bytearray()
        for item in _split(parts[1]):
            if item.startswith('"'):
                if directive != 'DB' or not re.fullmatch(r'"(?:[^"]|"")*"', item):
                    raise ValueError('bad DB string')
                try:
                    result.extend(item[1:-1].replace('""', '"').encode('ascii'))
                except UnicodeEncodeError:
                    raise ValueError('DB strings must be ASCII') from None
            else:
                value = _expression(item, (lambda name: 0) if sizing else resolve)[0]
                if not sizing:
                    _range(value, 0, 255 if directive == 'DB' else 65535, directive)
                result.extend(bytes((value & 255,)) if directive == 'DB' else _word(value))
        return bytes(result)

    # Instruction widths do not depend on symbol values; ORG must be resolvable
    # from constants and labels already encountered in the layout pass.
    output, listing = bytearray(), []
    for sizing in (True, False):
        pc = origin
        for number, label, text, expression in lines:
            try:
                if expression is not None:
                    if not sizing:
                        symbols[label] = resolve(label)
                    continue
                if sizing and label:
                    symbols[label] = pc
                if not text:
                    continue
                parts = text.split(None, 1)
                if parts[0].upper() in ('.ORG', 'ORG'):
                    if len(parts) != 2:
                        raise ValueError('ORG needs an address')
                    target = _expression(parts[1], resolve)[0]
                    _range(target, pc, 0x100000, 'ORG address')
                    encoded = bytes(target - pc)
                else:
                    encoded = data(text, sizing)
                    if encoded is None:
                        if pc & 1:
                            raise ValueError('instruction at odd address')
                        encoded = _instruction(text, pc, (lambda name: 0) if sizing else resolve, sizing)
                        if (pc & 65535) + len(encoded) > 65536:
                            raise ValueError('instruction crosses code segment')
                if pc + len(encoded) > 0x100000:
                    raise ValueError('output exceeds 20-bit address space')
                if not sizing:
                    output.extend(encoded)
                    listing.append({'address': pc, 'bytes': encoded.hex(), 'text': text, 'line': number})
                pc += len(encoded)
            except ValueError as exc:
                raise ValueError(f'line {number}: {exc}') from None
    return bytes(output), symbols, listing


def _decoded(kind, opcode, name, word, extra, pc):
    mnemonic = name.split()[0]
    reg, other = (word >> 8) & 15, (word >> 4) & 15
    if kind == FIXED:
        return name
    if kind in (IMM, EI7, SHIFT, SP_IMM):
        if kind == SP_IMM:
            return f'{mnemonic} SP,#0x{word & 255:02X}'
        value = (word & 127) if kind == EI7 else other if kind == SHIFT else word & 255
        if kind == EI7 and mnemonic == 'MOV' and value & 64:
            return f'MOV ER{reg},#{value - 128}'
        return f'{mnemonic} {"ER" if kind == EI7 else "R"}{reg},#0x{value:02X}'
    if kind in (RR, EE, ER_R):
        return f'{mnemonic} {"R" if kind == RR else "ER"}{reg},{"ER" if kind == EE else "R"}{other}'
    if kind in (ONE_R, ONE_ER, ONE_XR, ONE_QR, EXTBW):
        prefix = {ONE_R: 'R', ONE_ER: 'ER', ONE_XR: 'XR', ONE_QR: 'QR', EXTBW: 'ER'}[kind]
        return f'{mnemonic} {prefix}{reg & ~1 if kind == EXTBW else reg}'
    if kind == ER_SP:
        return f'{mnemonic} ER{reg},SP'
    if kind == SP_ER:
        return f'{mnemonic} SP,ER{other}'
    if kind == TB:
        return f'{mnemonic} R{reg}.{other}'
    if kind == R_CTRL:
        return f'MOV R{reg},PSW'
    if kind == CTRL_R:
        return f'MOV PSW,R{other}'
    if kind == BR_REG:
        return f'{mnemonic} ER{other}'
    if kind in (LEA_IND, LEA_DISP, LEA_ABS):
        operand = (f'[ER{other}]' if kind == LEA_IND else
                   f'0x{extra:04X}[ER{other}]' if kind == LEA_DISP else f'0x{extra:04X}')
        return f'LEA {operand}'
    if kind in (R_BASE, ER_BASE):
        value = word & 63
        if value & 32:
            value -= 64
        return f'{mnemonic} {"ER" if kind == ER_BASE else "R"}{reg},{value}[{"FP" if opcode & 64 else "BP"}]'
    if kind in (R_EA, ER_EA, XR_EA, QR_EA):
        register = {R_EA: 'R', ER_EA: 'ER', XR_EA: 'XR', QR_EA: 'QR'}[kind]
        return f'{mnemonic} {register}{reg},{name.split(",")[1]}'
    if kind in _MEMORY:
        prefix = 'ER' if kind in (ER_ABS, ER_IND, ER_DISP) else 'R'
        if kind in (R_IND, ER_IND):
            operand = f'[ER{other}]'
        elif kind in (R_DISP, ER_DISP):
            operand = f'0x{extra:04X}[ER{other}]'
        else:
            operand = f'0x{extra:04X}'
        return f'{mnemonic} {prefix}{reg},{operand}'
    if kind == BR:
        delta = word & 255
        if delta >= 128:
            delta -= 256
        target = (pc & 0xf0000) | ((pc + 2 + delta * 2) & 65535)
        return f'{mnemonic} 0x{target >> 16:X}:0x{target & 65535:04X}'
    if kind in (FAR, FAR_SYS):
        return f'{mnemonic} 0x{reg:X}:0x{extra:04X}'
    raise ValueError('unknown instruction kind')


def disassemble(data: bytes, origin: int = 0) -> list[dict]:
    """Decode catalogue instructions, preserving all other bytes as DW/DB.

    Noncanonical encodings use data directives rather than changing their bytes.
    Joining the returned text lines and assembling at origin is lossless.
    """
    _range(origin, 0, 0xfffff, 'origin')
    if origin + len(data) > 0x100000:
        raise ValueError('input exceeds 20-bit address space')
    records, pos = [], 0
    while pos < len(data):
        pc = origin + pos
        size, text = 1, f'DB 0x{data[pos]:02X}'
        if not pc & 1 and pos + 2 <= len(data):
            word = int.from_bytes(data[pos:pos + 2], 'little')
            size, text = 2, f'DW 0x{word:04X}'
            prefix, start = '', pos
            if word & 0xff00 == 0xe300:
                prefix = f'0x{word & 255:02X}:'
            elif word & 0xff0f == 0x900f:
                prefix = f'R{(word >> 4) & 15}:'
            elif word == 0xfe9f:
                prefix = 'DSR:'
            if prefix:
                start += 2
            if start + 2 <= len(data):
                code = int.from_bytes(data[start:start + 2], 'little')
                for kind, opcode, name in _ENTRIES:
                    if kind == SUB_IMM or name == 'END' or (prefix and kind not in _MEMORY):
                        continue
                    if kind in (R_BASE, ER_BASE):
                        mask = 0xf0c0 if kind == R_BASE else 0xf1c0
                    elif kind in (R_EA, ER_EA, XR_EA, QR_EA):
                        mask = {R_EA: 0xf0ff, ER_EA: 0xf1ff, XR_EA: 0xf3ff, QR_EA: 0xf7ff}[kind]
                    elif kind in (BR_REG, LEA_IND, LEA_DISP):
                        mask = 0xff1f
                    elif kind == LEA_ABS:
                        mask = 0xffff
                    elif kind in (R_CTRL, CTRL_R):
                        mask = 0xf0ff if kind == R_CTRL else 0xff0f
                    else:
                        mask = opcode_mask(kind, opcode)
                    if kind == FAR:
                        mask = 0xf0ff
                    if code & mask != opcode & mask:
                        continue
                    count = (4 if kind in _LONG else 2) + start - pos
                    if pos + count > len(data) or (pc & 65535) + count > 65536:
                        continue
                    extra = int.from_bytes(data[start + 2:start + 4], 'little')
                    candidate = _decoded(kind, opcode, name, code, extra, pc)
                    if prefix:
                        left, right = candidate.split(',', 1)
                        candidate = left + ',' + prefix + right
                    try:
                        encoded = _instruction(candidate, pc, lambda name: 0)
                    except ValueError:
                        continue
                    if encoded == data[pos:pos + count]:
                        size, text = count, candidate
                        break
            # Recognize only the exact scratch-preserving firmware SUB macro.
            if not prefix and pos + 8 <= len(data) and (pc & 65535) <= 65528:
                block = data[pos:pos + 8]
                reg = block[5] & 15
                candidate = f'SUB R{reg},#0x{block[2]:02X}'
                if _instruction(candidate, pc, lambda name: 0) == block:
                    size, text = 8, candidate
        records.append({'address': pc, 'bytes': data[pos:pos + size].hex(), 'text': text})
        pos += size
    return records
