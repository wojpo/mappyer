from pathlib import Path

from resolver import resolve_import
from scanner import get_filtered_from_dir
from parser import get_imports
import graphviz


def unique_module_id(p: Path, f: Path):
    p = p.relative_to(f).with_suffix('').parts
    if p[-1] == '__init__':
        return '.'.join(p[:-1])
    return '.'.join(p)

if __name__ == "__main__":
    folder = Path(".")


    all_paths = get_filtered_from_dir(folder)

    modules_to_files = {}
    dependencies = {}

    for path in all_paths:
        uniq = unique_module_id(path, folder)
        modules_to_files[uniq] = path
        dependencies[uniq] = get_imports(path)

    dot = graphviz.Digraph()

    for source, imports in dependencies.items():
        dot.node(source)

        for imp in imports:
            resolved = resolve_import(
                source,
                imp,
                modules_to_files
            )

            for target in resolved:
                dot.node(target)
                dot.edge(source, target)

    dot.render()