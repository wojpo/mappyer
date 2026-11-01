from pathlib import Path

from parser import get_imports

def test_simple_import(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("import os", encoding="utf-8")

    result = get_imports(file)

    assert result == [{
        "type": "import",
        'module': 'os',
        'level': 0,
        'names': []
    }]

def test_multiple_imports(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("import os, sys", encoding="utf-8")

    result = get_imports(file)

    assert result == [{
        "type": "import",
        'module': 'os',
        'level': 0,
        'names': []
    },
    {
        "type": "import",
        'module': 'sys',
        'level': 0,
        'names': []
    }]

def test_from_import(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("from pathlib import Path", encoding="utf-8")

    result = get_imports(file)

    assert result == [{
        "type": "from",
        "module": 'pathlib',
        "level": 0,
        'names': ['Path']
    }]

def test_syntax_error(tmp_path, capsys):
    file = tmp_path / "example.py"
    file.write_text(
        """import os
            l = list(""", encoding="utf-8")

    result = get_imports(file)
    captured = capsys.readouterr()

    assert captured.err == f'Syntax error in file {file}'
    assert result == []

def test_relative_import(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("from . import utils")

    result = get_imports(file)

    assert result == [{
        "type": "from",
        "module": None,
        "level": 1,
        'names': ['utils']
    }]

def test_parent_import(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("from ..core import config")

    result = get_imports(file)

    assert result == [{
        "type": "from",
        "module": 'core',
        "level": 2,
        'names': ['config']
    }]

def test_aliased_import(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("import numpy as np")

    result = get_imports(file)

    assert result == [{
        "type": "import",
        "module": 'numpy',
        "level": 0,
        'names': []
    }]

def test_no_imports(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("print(\"hello\")")

    result = get_imports(file)

    assert result == []

def test_empty_file(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("", encoding="utf-8")

    result = get_imports(file)

    assert result == []

def test_multiple_names(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("from os import path, getcwd", encoding="utf-8")

    result = get_imports(file)

    assert result == [{
        "type": "from",
        "module": 'os',
        "level": 0,
        'names': ['path', 'getcwd']
    }]

def test_dotted_imports(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("import os.path", encoding="utf-8")

    result = get_imports(file)

    assert result == [{
        "type": "import",
        "module": 'os.path',
        "level": 0,
        'names': []
    }]

def test_wildcard_imports(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("from math import *", encoding="utf-8")

    result = get_imports(file)

    assert result == [{
        "type": "from",
        "module": 'math',
        "level": 0,
        'names': ['*']
    }]

def test_nested_import(tmp_path):
    file = tmp_path / "example.py"
    file.write_text("def foo(): import os", encoding="utf-8")

    result = get_imports(file)

    assert result == [{
        "type": "import",
        "module": 'os',
        "level": 0,
        'names': []
    }]

def test_missing_file(tmp_path, capsys):
    file = tmp_path / "example.py"

    result = get_imports(file)
    captured = capsys.readouterr()

    assert captured.err == f'Unreadable file {file}'
    assert result == []

def test_unicode_decode_error(tmp_path, capsys):
    file = tmp_path / "example.py"
    file.write_bytes(b"\xff\xfe\xfa")

    result = get_imports(file)
    captured = capsys.readouterr()

    assert captured.err == f"Unicode decode error {file}"
    assert result == []