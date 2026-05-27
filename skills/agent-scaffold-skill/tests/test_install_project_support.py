import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_installer():
    module_path = ROOT / "scripts" / "install_project_support.py"
    spec = importlib.util.spec_from_file_location("install_project_support", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_install_project_support_adds_local_dependency_files(tmp_path):
    installer = load_installer()

    result = installer.install_project_support(tmp_path, ROOT)

    assert result.project_root == tmp_path
    assert (tmp_path / "AGENTS.md").exists()
    assert (tmp_path / "docs" / "agent-scaffold-harvest.md").exists()
    assert (tmp_path / "scripts" / "harvest_report.py").exists()
    assert "This project uses `agent-scaffold-skill`" in (tmp_path / "AGENTS.md").read_text(
        encoding="utf-8"
    )


def test_install_project_support_preserves_existing_agents_file(tmp_path):
    installer = load_installer()
    agents = tmp_path / "AGENTS.md"
    agents.write_text("# Existing Instructions\n\nKeep this.\n", encoding="utf-8")

    installer.install_project_support(tmp_path, ROOT)
    installer.install_project_support(tmp_path, ROOT)

    text = agents.read_text(encoding="utf-8")
    assert "# Existing Instructions" in text
    assert text.count("agent-scaffold-skill:start") == 1


def test_install_project_support_does_not_create_global_project_registry(tmp_path):
    installer = load_installer()

    installer.install_project_support(tmp_path, ROOT)

    assert not (ROOT / "projects").exists()
    assert not (ROOT / "project-registry.json").exists()
