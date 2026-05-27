import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_checker():
    module_path = ROOT / "scripts" / "check_business_agent_package.py"
    spec = importlib.util.spec_from_file_location("check_business_agent_package", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["check_business_agent_package"] = module
    spec.loader.exec_module(module)
    return module


class BusinessAgentTemplateTests(unittest.TestCase):
    def test_business_agent_template_is_a_valid_minimum_package(self):
        checker = load_checker()
        template_root = ROOT / "assets" / "templates" / "business-agent"

        with tempfile.TemporaryDirectory() as temp_dir:
            package_root = Path(temp_dir) / "business-agent"
            shutil.copytree(template_root, package_root)

            result = checker.check_package(package_root)

        self.assertTrue(result.ok, "\n".join(result.issues))


if __name__ == "__main__":
    unittest.main()
