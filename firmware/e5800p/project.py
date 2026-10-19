"""e5800p firmware written in PL/e."""

from kits import Firmware
from firmware.e5800p import (
    app_hooks, apps, basic, basic_asm, batch, editing, graph_gate, graph_input,
    graph_math, graph_view, graphics, hooks, instructions, logo, matrix, mcs,
    memory, objects, storage, strings, ui,
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
    apps, objects, strings, matrix, app_hooks, hooks,
):
    module.install(fw)

addresses = {row['name']: row['cpu_start'] for row in REGIONS}
# Graph internals have symbolic callers; published entries and legacy tables stay fixed.
private_graph = {
    row['name'] for row in REGIONS
    if row['kind'] == 'code'
    and row['source'] in ('graph_math.py', 'graph_input.py', 'graph_view.py', 'graph_gate.py')
    and row['name'] not in ('graph', 'graph_calc', 'graph_eval', 'graph_format', 'graph_mode_gate')
}
for fn in fw.functions:
    if fn.address is None and fn.name not in private_graph:
        fn.address = addresses.get(fn.name)

functions = {fn.symbol: fn for fn in fw.functions}
for hook in app_hooks.APP_HOOKS:
    fw.hook(hook['address'], functions[hook['symbol']],
            expected=hook['expected'], call=True)
