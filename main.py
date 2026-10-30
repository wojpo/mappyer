from pathlib import Path
from scanner import get_from_dir
from parser import get_imports
import graphviz

if __name__ == "__main__":
    folder = Path(".")

    all_paths = [i for i in get_from_dir(folder) if str(i)[0] != '.']

    dependencies = {}

    for path in all_paths:
        dependencies[path.name] = get_imports(path)

    dot = graphviz.Digraph()

    for i in dependencies.keys():
        dot.node(i)
        for j in dependencies[i]:
            dot.node(str(j['module']))
            print(i, j)
            dot.edge(i, str(j['module']))


    dot.render()
