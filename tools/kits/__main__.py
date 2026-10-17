"""Build a firmware project declared in a Python file."""

import argparse
from pathlib import Path
import sys

from build_e5800p import load_project


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path, help='Python file declaring one Firmware object')
    parser.add_argument('original', type=Path, help='input Flash image; a separate output is created')
    parser.add_argument('-o', '--output', type=Path, help='default: build/<firmware name>.bin')
    parser.add_argument('--listing', type=Path, help='optional generated assembly for inspection')
    parser.add_argument('--clean', type=Path, help='matching original image for an upgrade')
    parser.add_argument('--map', type=Path, help='optional firmware region map')
    args = parser.parse_args()
    try:
        fw = load_project(args.project)
        output = args.output or Path('build') / (fw.name + '.bin')
        result = fw.build(args.original, output, listing=args.listing,
                          clean=args.clean, map_path=args.map)
        print(f'Built {output} ({Path(output).stat().st_size} bytes)')
        for block in result['blocks']:
            address = block['address']
            print(f"  {block['name']}: {address >> 16:X}:{address & 0xffff:04X}  {len(block['data'])} bytes")
        return 0
    except (OSError, ValueError, TypeError, SyntaxError) as exc:
        print(f'kits: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
