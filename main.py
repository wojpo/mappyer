from pathlib import Path
from scanner import get_from_dir
from parser import get_imports

if __name__ == "__main__":
    folder = Path(".")

    all_paths = get_from_dir(folder)

    dependencies = {}

    for path in all_paths:
        dependencies[path] = get_imports(path)
    print(dependencies)
