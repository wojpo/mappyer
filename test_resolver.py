from pathlib import Path
import pytest

from resolver import resolve_import

@pytest.fixture
def modules_to_files():
    return {
        "main": Path("main.py"),
        "app": Path("app/__init__.py"),
        "app.utils": Path("app/utils.py"),
        "app.config": Path("app/config.py"),
        "app.auth": Path("app/auth.py"),
        "app.services": Path("app/services/__init__.py"),
        "app.services.tasks": Path("app/services/tasks.py"),
        "app.services.api": Path("app/services/api/__init__.py"),
        "app.services.api.routes": Path("app/services/api/routes.py"),
    }

def test_absolute_import(modules_to_files):
    imp = {
        "type": "import",
        "module": "app.utils",
        "level": 0,
        "names": []
    }

    result = resolve_import("main", imp, modules_to_files)

    assert result == ["app.utils"]

def test_external_import(modules_to_files):
    imp = {
        "type": "import",
        "module": "requests",
        "level": 0,
        "names": []
    }

    result = resolve_import("main", imp, modules_to_files)
    assert result == []

def test_nonexistent_module(modules_to_files):
    imp = {
        "type": "import",
        "module": "app.missing",
        "level": 0,
        "names": []
    }

    result = resolve_import("main", imp, modules_to_files)
    assert result == []

def test_from_import_function(modules_to_files):
    imp = {
        "type": "from",
        "module": "app.utils",
        "level": 0,
        "names": ['helper']
    }

    result = resolve_import("main", imp, modules_to_files)
    assert result == ['app.utils']

def test_from_import_submodule(modules_to_files):
    imp = {
        "type": "from",
        "module": "app",
        "level": 0,
        "names": ['utils']
    }

    result = resolve_import("main", imp, modules_to_files)
    assert result == ['app.utils']

def test_relative_import(modules_to_files):
    imp = {
        "type": "from",
        "module": None,
        "level": 1,
        "names": ['utils']
    }

    result = resolve_import("app.auth", imp, modules_to_files)
    assert result == ['app.utils']

def test_parent_import(modules_to_files):
    imp = {
        "type": "from",
        "module": None,
        "level": 2,
        "names": ['utils']
    }

    result = resolve_import("app.services.tasks", imp, modules_to_files)
    assert result == ['app.utils']

def test_deep_relative_import(modules_to_files):
    imp = {
        "type": "from",
        "module": None,
        "level": 3,
        "names": ['utils']
    }

    result = resolve_import("app.services.api.routes", imp, modules_to_files)
    assert result == ['app.utils']

def test_invalid_relative_level(modules_to_files):
    imp = {
        "type": "from",
        "module": None,
        "level": 3,
        "names": ['utils']
    }

    result = resolve_import("app.auth", imp, modules_to_files)
    assert result == []

def test_init_import(modules_to_files):
    imp = {
        "type": "from",
        "module": None,
        "level": 1,
        "names": ['utils']
    }

    result = resolve_import("app", imp, modules_to_files)
    assert result == ["app.utils"]

def test_self_import(modules_to_files):
    imp = {
        "type": "from",
        "module": None,
        "level": 1,
        "names": ['utils']
    }

    result = resolve_import("app.utils", imp, modules_to_files)
    assert result == []

def test_wildcard_import(modules_to_files):
    imp = {
        "type": "from",
        "module": 'utils',
        "level": 1,
        "names": ['*']
    }

    result = resolve_import("app.auth", imp, modules_to_files)
    assert result == ["app.utils"]

def test_multiple_names(modules_to_files):
    imp = {
        "type": "from",
        "module": 'app',
        "level": 0,
        "names": ['config', 'auth']
    }

    result = resolve_import("main", imp, modules_to_files)
    assert result == ["app.auth", "app.config"]

def test_nested_init_import(modules_to_files):
    imp = {
        "type": "from",
        "module": None,
        "level": 1,
        "names": ['tasks']
    }

    result = resolve_import("app.services", imp, modules_to_files)
    assert result == ["app.services.tasks"]

def test_relative_function_import(modules_to_files):
    imp = {
        "type": "from",
        "module": 'utils',
        "level": 1,
        "names": ['helper']
    }

    result = resolve_import("app.auth", imp, modules_to_files)
    assert result == ["app.utils"]

def test_root_relative_import(modules_to_files):
    imp = {
        "type": "from",
        "module": None,
        "level": 1,
        "names": ['utils']
    }

    result = resolve_import("main", imp, modules_to_files)
    assert result == []