"""Build the e5800p Python firmware project."""

import argparse
from importlib.resources import files
from pathlib import Path
import runpy
import sys

from kits import Firmware


def default_project():
    source = Path(__file__).resolve().parents[1] / 'firmware' / 'e5800p' / 'project.py'
    if source.is_file():
        return source
    return Path(str(files('firmware.e5800p').joinpath('project.py')))


def load_project(project=None):
    project = Path(project if project is not None else default_project()).resolve()
    paths = [str(project.parent)]
    if project.parent.name == 'e5800p' and project.parent.parent.name == 'firmware':
        paths.append(str(project.parent.parent.parent))
    previous = sys.path[:]
    sys.path[:0] = paths
    try:
        namespace = runpy.run_path(str(project))
    finally:
        sys.path[:] = previous
    projects = {id(value): value for value in namespace.values() if isinstance(value, Firmware)}
    if len(projects) != 1:
        raise ValueError(f'{project}: declare one Firmware object')
    fw = next(iter(projects.values()))
    fw._sources.add(str(project))
    return fw


def build(base, *, project=None, map_regions=None, symbols=None):
    """Compile the Python project onto original Flash bytes."""
    image, linked = load_project(project).image(base)
    if map_regions is not None:
        map_regions.extend(linked['regions'])
    if symbols is not None:
        symbols.update(linked['symbols'])
    return image


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('base', type=Path)
    parser.add_argument('-o', '--output', type=Path, required=True)
    parser.add_argument('--project', type=Path, help='Python project; defaults to bundled e5800p')
    parser.add_argument('--clean', type=Path, help='matching original image for an upgrade')
    parser.add_argument('--map', type=Path)
    args = parser.parse_args(argv)
    try:
        result = load_project(args.project).build(args.base, args.output,
                                                 clean=args.clean, map_path=args.map)
        print(f"Built {args.output}: {result['sha256']}")
        return 0
    except (OSError, ValueError, TypeError, SyntaxError) as exc:
        print(f'build_e5800p: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
