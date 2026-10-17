"""e5800p firmware expressed in the native Python DSL."""

from kits import Firmware
from firmware.e5800p import (
    basic, basic_asm, batch, editing, graph, graphics, hooks,
    instructions, logo, memory, storage, ui,
)
from firmware.e5800p.layout import (
    ORIGINAL_FIRMWARE_SHA256, REGIONS, WRITABLE_REGIONS,
)

fw = Firmware(
    'e5800p',
    regions=WRITABLE_REGIONS,
    original_firmware_sha256=ORIGINAL_FIRMWARE_SHA256,
    original_regions=REGIONS,
)

for module in (
    basic, basic_asm, memory, graphics, graph, ui, editing,
    instructions, batch, storage, logo, hooks,
):
    module.install(fw)
