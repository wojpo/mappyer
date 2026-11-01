import ast
import sys
from pathlib import Path


def get_imports(p: Path):
    try:
        tree = ast.parse(p.read_text(encoding="utf-8"))
    except SyntaxError:
        sys.stderr(f"Syntax error in file {p}")
        return []
    except OSError:
        sys.stderr(f"Unreadable file {p}")
        return []
    except UnicodeDecodeError:
        sys.stderr(f"Unicode decode error {p}")
        return []
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
