from pathlib import Path


def resolve_import(
    source: str,
    imp: dict,
    modules_to_files: dict[str, Path]
) -> list[str]:

    module = imp["module"]
    level = imp["level"]

    if level == 0:
        base = module

    else:
        source_path = modules_to_files[source]

        if source_path.stem == "__init__":
            package = source
        else:
            package = source.rpartition(".")[0]

        if not package:
            return []

        parts = package.split(".")

        if level > len(parts):
            return []

        parent = ".".join(parts[:len(parts) - level + 1])
        base = f"{parent}.{module}" if module else parent

    if not base:
        return []

    resolved = set()

    if imp["type"] == "import":
        if base in modules_to_files and base != source:
            resolved.add(base)

    elif imp["type"] == "from":
        for name in imp["names"]:
            candidate = f"{base}.{name}" if name != "*" else None

            if candidate and candidate in modules_to_files:
                if candidate != source:
                    resolved.add(candidate)

            elif base in modules_to_files and base != source:
                resolved.add(base)

    return sorted(resolved)