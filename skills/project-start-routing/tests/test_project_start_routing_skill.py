import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProjectStartRoutingSkillTests(unittest.TestCase):
    def test_skill_points_to_routing_references(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("`references/stack-routing.md`", skill)
        self.assertIn("`references/startup-checklist.md`", skill)
        self.assertIn("Design System Adoption Gate", skill)
        self.assertIn("ask Jun", skill)
        self.assertIn("jun-ui adoption decision", skill)

    def test_stack_routing_names_allowed_lanes_and_management_fields(self) -> None:
        routing = (ROOT / "references" / "stack-routing.md").read_text(encoding="utf-8")

        for lane in ["TS App", "Python Engine", "No-build Tool", "Hybrid"]:
            with self.subTest(lane=lane):
                self.assertIn(lane, routing)

        for phrase in [
            "project type",
            "selected lane",
            "rejected alternatives",
            "design system adoption",
            "jun-ui-design-system",
            "install",
            "start",
            "test",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, routing.lower())

    def test_startup_checklist_contains_decision_template(self) -> None:
        checklist = (ROOT / "references" / "startup-checklist.md").read_text(
            encoding="utf-8"
        )

        for field in [
            "Project type",
            "Selected lane",
            "Rejected alternatives",
            "Design System adoption",
            "Design System reason",
            "Design System reopen path",
            "Install",
            "Start",
            "Test",
            "Environment boundary",
        ]:
            with self.subTest(field=field):
                self.assertIn(field, checklist)

        for decision in [
            "jun-ui adoption decision: adopted",
            "jun-ui adoption decision: deferred",
            "jun-ui adoption decision: not-suitable",
        ]:
            with self.subTest(decision=decision):
                self.assertIn(decision, checklist)


if __name__ == "__main__":
    unittest.main()
