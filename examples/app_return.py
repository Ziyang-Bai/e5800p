"""Return 7 from S4; build with --stack-bytes 512."""

from kits import Firmware, u16


fw = Firmware('RETURN', regions=[(0x91000, 0x92000)])


@fw.function(address=0x91000)
def main() -> u16:
    return 7
