from pathlib import Path

excluded = {'.venv', 'venv', '.git', '__pycache__', 'node_modules'}

def get_filtered_from_dir(directory: Path) -> list[Path]:
    temp = list(directory.rglob("*.py"))
    return [path for path in temp if not any([part in excluded for part in path.parts])]