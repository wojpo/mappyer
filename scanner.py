from pathlib import Path

excluded = {'.venv', 'venv', '.git', '__pycache__', 'node_modules'}

def get_filtered_from_dir(directory: Path) -> list[Path]:
    temp = list(directory.rglob("*.py"))
    return [i for i in temp if not any([j in excluded for j in i.parts])]