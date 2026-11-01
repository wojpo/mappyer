from pathlib import Path
from scanner import get_from_dir
from parser import get_imports
import graphviz


def unique_module_id(p: Path, f: Path):
    p = p.relative_to(f).with_suffix('').parts
    if p[-1] == '__init__':
        return '.'.join(p[:-1])
    return '.'.join(p)

if __name__ == "__main__":
    folder = Path(".")

    all_paths = [i for i in get_from_dir(folder) if str(i)[0] != '.']

    dependencies = {}

    for path in all_paths:
        dependencies[unique_module_id(path, folder)] = get_imports(path)

    dot = graphviz.Digraph()

    for i in dependencies.keys():
        dot.node(i)
        for j in dependencies[i]:
            dot.node(str(j['module']))
            print(i, j)
            dot.edge(i, str(j['module']))


    dot.render()
