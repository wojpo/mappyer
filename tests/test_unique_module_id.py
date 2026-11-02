from mappyer.main import unique_module_id


def test_package_root_module_id(tmp_path):
    package = tmp_path / "app"
    package.mkdir()

    init_file = package / "__init__.py"
    utils_file = package / "utils.py"

    init_file.write_text("", encoding="utf-8")
    utils_file.write_text("", encoding="utf-8")

    assert unique_module_id(init_file, package) == "app"
    assert unique_module_id(utils_file, package) == "app.utils"


def test_src_layout_module_id(tmp_path):
    src = tmp_path / "src"
    package = src / "app"
    package.mkdir(parents=True)

    init_file = package / "__init__.py"
    utils_file = package / "utils.py"

    init_file.write_text("", encoding="utf-8")
    utils_file.write_text("", encoding="utf-8")

    assert unique_module_id(init_file, src) == "app"
    assert unique_module_id(utils_file, src) == "app.utils"


def test_regular_module_id(tmp_path):
    main_file = tmp_path / "main.py"
    main_file.write_text("", encoding="utf-8")

    assert unique_module_id(main_file, tmp_path) == "main"