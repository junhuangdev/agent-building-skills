import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallSkillsTests(unittest.TestCase):
    def test_cli_can_install_one_skill_without_touching_others(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skills_root = Path(tmp) / "skills"
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/install_skills.py",
                    "--skills-root",
                    str(skills_root),
                    "--skill",
                    "project-start-routing",
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((skills_root / "project-start-routing").is_symlink())
            self.assertFalse((skills_root / "agent-builder-lab").exists())


if __name__ == "__main__":
    unittest.main()
