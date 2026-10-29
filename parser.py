import ast
from pathlib import Path


def get_imports(p: Path):
    tree = ast.parse(p.read_text(encoding="utf-8"))
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    {
                        "type": "import",
                        'module': alias.name,
                        'level': 0,
                        'names': []
                    }
                )

        elif isinstance(node, ast.ImportFrom):
            mod = {
                "type": "from",
                'module': node.module,
                'level': node.level,
                'names': [i.name for i in node.names]
            }
            imports.append(mod)

    return imports
