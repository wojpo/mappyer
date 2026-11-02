import argparse
from pathlib import Path
from resolver import resolve_import
from scanner import get_filtered_from_dir
from parser import get_imports
from visualizer import visualize


def unique_module_id(p: Path, f: Path):
    p = p.relative_to(f).with_suffix('').parts
    if p[-1] == '__init__':
        return '.'.join(p[:-1])
    return '.'.join(p)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Mappyer',
        description='Python tool designed to analyze Python projects and visualize dependencies.')

    parser.add_argument(
        "directory",
        nargs="?",
        default=Path("."),
        type=Path,
        help="Python project directory to analyze"
    )

    parser.add_argument(
        "-o",
        "--output",
        default=Path("mappyer.html"),
        type=Path,
        help="Output HTML file path"
    )

    args = parser.parse_args()

    folder = Path(args.directory)

    if not folder.is_dir():
        parser.error(f"Invalid directory: {folder}")

    all_paths = get_filtered_from_dir(folder)

    modules_to_files = {}
    dependencies = {}

    for path in all_paths:
        uniq = unique_module_id(path, folder)
        modules_to_files[uniq] = path
        dependencies[uniq] = get_imports(path)

    edges = set()

    for source, imports in dependencies.items():

        for imp in imports:
            resolved = resolve_import(
                source,
                imp,
                modules_to_files
            )

            for target in resolved:
                edges.add((source, target))

    visualize(modules_to_files, edges, args.output)