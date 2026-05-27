import importlib.util
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


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class CheckBusinessAgentPackageTests(unittest.TestCase):
    def test_valid_minimum_package_passes(self):
        checker = load_checker()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write(
                root / "agent.yaml",
                """id: candidate-review-agent
name: Candidate Review Agent
agent_shape: composite_business_agent
mission: Prepare candidate records for human review.
business_value: Reduce candidate triage time.
non_goals: []
allowed_actions: []
risk_classes: []
human_gates: []
runtime_targets: []
memory_policy: {}
eval_policy: {}
delivery_contract: {}
""",
            )
            write(
                root / "actions" / "write_candidate.yaml",
                """id: write_candidate
description: Write a candidate record.
input_contract: {}
output_contract: {}
risk_class: low
requires_approval: false
side_effects: []
forbidden_when: []
produces_artifacts: []
""",
            )
            write(
                root / "artifacts" / "candidate_record.yaml",
                """id: candidate_record
type: candidate_record
owner: candidate-review-agent
schema: {}
evidence_required: []
status_values: []
human_summary_fields: []
""",
            )
            write(
                root / "evals" / "candidate_review.yaml",
                """id: candidate-review-smoke
goal: Verify candidate review package.
initial_state: {}
expected_artifacts: []
rubric: {}
blocking_failures: []
human_gate_expectations: []
""",
            )
            write(
                root / "runtime-adapters" / "codex.yaml",
                """runtime: codex
invocation: Use Codex with project AGENTS.md.
skill_trigger: agent-builder-lab
capability_map: {}
unsupported_actions: []
handoff_rules: []
""",
            )
            write(root / "reports" / "delivery-package.md", "# Delivery Package\n")

            result = checker.check_package(root)

        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_missing_required_agent_key_fails(self):
        checker = load_checker()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write(root / "agent.yaml", "id: candidate-review-agent\nname: Candidate Review Agent\n")

            result = checker.check_package(root)

        self.assertFalse(result.ok)
        self.assertTrue(any("agent.yaml missing key: mission" in issue for issue in result.issues))

    def test_missing_required_package_parts_fail(self):
        checker = load_checker()

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write(
                root / "agent.yaml",
                """id: candidate-review-agent
name: Candidate Review Agent
agent_shape: composite_business_agent
mission: Prepare candidate records for human review.
business_value: Reduce candidate triage time.
non_goals: []
allowed_actions: []
risk_classes: []
human_gates: []
runtime_targets: []
memory_policy: {}
eval_policy: {}
delivery_contract: {}
""",
            )

            result = checker.check_package(root)

        self.assertFalse(result.ok)
        self.assertTrue(any("missing directory: actions" in issue for issue in result.issues))
        self.assertTrue(any("missing directory: evals" in issue for issue in result.issues))


if __name__ == "__main__":
    unittest.main()
