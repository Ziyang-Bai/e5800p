"""Clear the LCD body and return 42 through the calculator calling convention."""

from kits import Buffer, Firmware, Memory, ROM, u16


fw = Firmware('python-demo', regions=[(0x84000, 0x86000)])


class LCD(Memory):
    body = Buffer(address=0x80EC, size=96 * 31 // 8)


refresh = ROM(0x043BE, result=None)


@fw.function
def add_two(value: u16) -> u16:
    return value + 2


@fw.function
def clear_screen() -> None:
    for i in range(len(LCD.body)):
        LCD.body[i] = 0
    refresh()


@fw.function(address=0x84000)
def main() -> u16:
    clear_screen()
    return add_two(40)
