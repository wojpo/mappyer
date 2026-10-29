from pathlib import Path

def get_from_dir(directory: Path) -> list[Path]:
    return list(directory.rglob("*.py"))
