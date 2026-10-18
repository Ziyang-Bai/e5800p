"""e5800p firmware written in PL/e."""

from kits import Firmware
from firmware.e5800p import (
    app_hooks, apps, basic, basic_asm, batch, editing, graph_gate, graph_input,
    graph_math, graph_view, graphics, hooks, instructions, logo, mcs, memory,
    storage, ui,
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
    basic, basic_asm, memory, graphics, ui, editing, instructions, batch,
    storage, logo, graph_math, graph_input, graph_view, graph_gate, mcs,
    apps, app_hooks, hooks,
):
    module.install(fw)

addresses = {row['name']: row['cpu_start'] for row in REGIONS}
for fn in fw.functions:
    if fn.address is None:
        fn.address = addresses[fn.name]

functions = {fn.symbol: fn for fn in fw.functions}
for hook in app_hooks.APP_HOOKS:
    fw.hook(hook['address'], functions[hook['symbol']],
            expected=hook['expected'], call=True)
