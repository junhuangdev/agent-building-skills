import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_installer():
    module_path = ROOT / "scripts" / "install_project_support.py"
    spec = importlib.util.spec_from_file_location("install_project_support", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class InstallProjectSupportTests(unittest.TestCase):
    def test_install_project_support_adds_local_learning_files(self):
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            result = installer.install_project_support(tmp_path, ROOT)

            self.assertEqual(result.project_root, tmp_path.resolve())
            self.assertTrue((tmp_path / "AGENTS.md").exists())
            self.assertTrue((tmp_path / "docs" / "agent-build-journal.md").exists())
            self.assertTrue((tmp_path / "scripts" / "agent_builder_report.py").exists())
            agents_text = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("This project uses `agent-builder-lab`", agents_text)
            self.assertIn("docs/agent-build-journal.md", agents_text)

    def test_install_project_support_preserves_existing_agents_file(self):
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            agents = tmp_path / "AGENTS.md"
            agents.write_text("# Existing Instructions\n\nKeep this.\n", encoding="utf-8")

            installer.install_project_support(tmp_path, ROOT)
            installer.install_project_support(tmp_path, ROOT)

            text = agents.read_text(encoding="utf-8")
            self.assertIn("# Existing Instructions", text)
            self.assertIn("Keep this.", text)
            self.assertEqual(text.count("agent-builder-lab:start"), 1)

    def test_install_project_support_is_idempotent_for_empty_agents_file(self):
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)

            installer.install_project_support(tmp_path, ROOT)
            installer.install_project_support(tmp_path, ROOT)

            text = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
            self.assertFalse(text.startswith("\n"))
            self.assertEqual(text.count("agent-builder-lab:start"), 1)

    def test_install_project_support_does_not_create_global_project_registry(self):
        installer = load_installer()

        with tempfile.TemporaryDirectory() as temp_dir:
            installer.install_project_support(Path(temp_dir), ROOT)

        self.assertFalse((ROOT / "projects").exists())
        self.assertFalse((ROOT / "project-registry.json").exists())


if __name__ == "__main__":
    unittest.main()
