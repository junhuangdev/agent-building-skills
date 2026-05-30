#!/usr/bin/env python3
"""Validate the capability-evolution skill package."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


DEFAULT_SKILL_ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/execution-contract.md",
    "references/integration-contract.md",
    "references/storage-routing.md",
    "references/use-contract.md",
    "references/self-evolution.md",
    "references/memory-lifecycle.md",
    "references/eval-contract.md",
    "references/promotion-contract.md",
    "references/examples.md",
    "assets/templates/memory-item.yaml",
    "assets/templates/eval-case.yaml",
    "assets/templates/feedback-record.yaml",
    "assets/templates/promotion-package.md",
    "assets/example-evolution-package/memory/agent-method.yaml",
    "assets/example-evolution-package/memory/agent-business.yaml",
    "assets/example-evolution-package/memory/software-project.yaml",
    "assets/example-evolution-package/memory/skill-improvement.yaml",
    "assets/example-evolution-package/evals/trace-policy.yaml",
    "assets/example-evolution-package/evals/use-feedback-loop.yaml",
    "assets/example-evolution-package/evals/skill-self-improvement.yaml",
    "assets/example-evolution-package/feedback/user-feedback.yaml",
    "assets/example-evolution-package/promotions/skill-promotion.md",
    "scripts/check_evolution_package.py",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(skill_root: Path, path: Path) -> str:
    if not path.exists():
        fail(f"missing {path.relative_to(skill_root)}")
    return path.read_text(encoding="utf-8")


def assert_contains(skill_root: Path, path: Path, patterns: list[str]) -> None:
    text = read(skill_root, path)
    for pattern in patterns:
        if not re.search(pattern, text, re.MULTILINE):
            fail(f"{path.relative_to(skill_root)} missing pattern: {pattern}")


def assert_not_contains(skill_root: Path, path: Path, patterns: list[str]) -> None:
    text = read(skill_root, path)
    for pattern in patterns:
        if re.search(pattern, text, re.MULTILINE):
            fail(f"{path.relative_to(skill_root)} should not contain pattern: {pattern}")


def main() -> int:
    skill_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_SKILL_ROOT

    for rel in REQUIRED_FILES:
        if not (skill_root / rel).exists():
            fail(f"missing {rel}")

    assert_contains(
        skill_root,
        skill_root / "SKILL.md",
        [
            r"^name:\s*capability-evolution$",
            r"Use when.*(learn|learning|capability|evolution)",
            r"learn.*store.*retrieve.*use.*evaluate.*improve.*learn_again",
            r"Skill",
            r"Agent",
            r"project",
            r"promotion",
            r"eval",
        ],
    )
    outdated_skill_ref = "$" + "learning"
    assert_not_contains(
        skill_root,
        skill_root / "SKILL.md",
        [r"name:\s*learning$", re.escape(outdated_skill_ref)],
    )

    assert_contains(
        skill_root,
        skill_root / "references" / "execution-contract.md",
        [
            r"Intake",
            r"Retrieve",
            r"Use",
            r"Evaluate",
            r"Improve",
            r"Learn",
            r"[Hh]uman",
        ],
    )

    assert_contains(
        skill_root,
        skill_root / "references" / "use-contract.md",
        [
            r"Use Contract",
            r"applied_artifact",
            r"use_result",
            r"confirm",
            r"narrow",
            r"revise",
            r"supersede",
            r"archive",
            r"learn_again",
        ],
    )

    assert_contains(
        skill_root,
        skill_root / "references" / "integration-contract.md",
        [r"caller", r"Skill", r"Agent", r"project", r"\$capability-evolution", r"return"],
    )

    assert_contains(
        skill_root,
        skill_root / "references" / "storage-routing.md",
        [
            r"evolution_target",
            r"storage_sink",
            r"agent_method",
            r"agent_business",
            r"software_project",
            r"workflow_process",
            r"skill_improvement",
            r"user_preference",
            r"runtime_behavior",
        ],
    )

    assert_contains(
        skill_root,
        skill_root / "assets" / "templates" / "memory-item.yaml",
        [
            r"evolution_target:",
            r"storage_sink:",
            r"use_history:",
            r"last_use_result:",
            r"agent_method",
            r"owning_agent_repo",
            r"owning_skill_package",
            r"current_project",
        ],
    )

    result = subprocess.run(
        [
            sys.executable,
            str(skill_root / "scripts" / "check_evolution_package.py"),
            str(skill_root / "assets" / "example-evolution-package"),
        ],
        cwd=skill_root,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        fail("example evolution package validation failed")

    print("capability-evolution skill package validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
