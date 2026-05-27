import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_installer():
    module_path = ROOT / "scripts" / "install_local_skill.py"
    spec = importlib.util.spec_from_file_location("install_local_skill", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_install_creates_symlink_to_skill_root(tmp_path):
    installer = load_installer()
    target = installer.install_skill(ROOT, tmp_path, "agent-scaffold-skill")

    assert target.is_symlink()
    assert target.resolve() == ROOT


def test_install_is_idempotent_for_existing_same_symlink(tmp_path):
    installer = load_installer()
    first = installer.install_skill(ROOT, tmp_path, "agent-scaffold-skill")
    second = installer.install_skill(ROOT, tmp_path, "agent-scaffold-skill")

    assert first == second
    assert second.resolve() == ROOT
