"""Objects shared by firmware declarations and the nXu8 compiler."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Integer:
    name: str
    bits: int

    @property
    def mask(self):
        return (1 << self.bits) - 1

    def __call__(self, value):
        return int(value) & self.mask


u8 = Integer('u8', 8)
u16 = Integer('u16', 16)


class Memory:
    """Group named buffers in calculator data memory."""


class Buffer:
    def __init__(self, address, size, dtype=u8):
        if dtype not in (u8, u16):
            raise ValueError('Buffer elements must be u8 or u16')
        if type(address) is not int or not 0 <= address <= 0xffffff:
            raise ValueError('Buffer address must fit a data segment and offset')
        if type(size) is not int or size <= 0:
            raise ValueError('Buffer size must be a positive element count')
        if (address & 0xffff) + size * (dtype.bits // 8) > 0x10000:
            raise ValueError('Buffer must fit one 64 KiB data segment')
        self.address = address
        self.size = size
        self.dtype = dtype

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        raise TypeError('Calculator memory is accessed inside @fw.function')

    def __setitem__(self, index, value):
        raise TypeError('Calculator memory is accessed inside @fw.function')


def _register(name):
    match = re.fullmatch(r'(er|r)([0-7])', name) if isinstance(name, str) else None
    if not match:
        raise ValueError('ROM registers must be r0..r7 or er0/er2/er4/er6')
    index = int(match[2])
    width = 2 if match[1] == 'er' else 1
    if width == 2 and index & 1:
        raise ValueError('ROM word registers must have an even index')
    return set(range(index, index + width))


class ROM:
    """A fixed code entry with explicit register arguments and result."""

    def __init__(self, address, args=(), result='er0'):
        if type(address) is not int or not 0 <= address <= 0xfffff or address & 1:
            raise ValueError('ROM entry must be an even 20-bit code address')
        self.args = tuple(args)
        if len(self.args) > 4:
            raise ValueError('ROM calls accept up to four arguments')
        used = set()
        for name in self.args:
            registers = _register(name)
            if used & registers:
                raise ValueError('ROM argument registers overlap')
            used.update(registers)
        if result is not None:
            _register(result)
        self.address = address
        self.result = result

    def __call__(self, *args, **kwargs):
        raise TypeError('ROM calls are compiled inside @fw.function')


class Function:
    def __init__(self, fn, owner, address=None, native=False):
        self.fn = fn
        self.owner = owner
        self.address = address
        self.native = native
        self.name = fn.__name__
        self.symbol = 'fn_' + self.name

    def __call__(self, *args, **kwargs):
        raise TypeError('Calculator functions run on the calculator; use fw.build()')


class _CPU:
    """Marker for native AST operations; never reads or mutates host state."""

    __slots__ = ()

    def __getattr__(self, name):
        raise TypeError('CPU operations are compiled inside @fw.function(native=True)')

    def __setattr__(self, name, value):
        raise TypeError('CPU operations are compiled inside @fw.function(native=True)')


cpu = _CPU()
