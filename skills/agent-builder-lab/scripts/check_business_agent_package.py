#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


REQUIRED_AGENT_KEYS = [
    "id",
    "name",
    "agent_shape",
    "mission",
    "business_value",
    "non_goals",
    "allowed_actions",
    "risk_classes",
    "human_gates",
    "runtime_targets",
    "memory_policy",
    "eval_policy",
    "delivery_contract",
]

REQUIRED_PARTS = {
    "actions": [
        "id",
        "description",
        "input_contract",
        "output_contract",
        "risk_class",
        "requires_approval",
        "side_effects",
        "forbidden_when",
        "produces_artifacts",
    ],
    "artifacts": [
        "id",
        "type",
        "owner",
        "schema",
        "evidence_required",
        "status_values",
        "human_summary_fields",
    ],
    "evals": [
        "id",
        "goal",
        "initial_state",
        "expected_artifacts",
        "rubric",
        "blocking_failures",
        "human_gate_expectations",
    ],
    "runtime-adapters": [
        "runtime",
        "invocation",
        "skill_trigger",
        "capability_map",
        "unsupported_actions",
        "handoff_rules",
    ],
}


@dataclass(frozen=True)
class CheckResult:
    ok: bool
    issues: list[str]


def check_package(package_root: Path) -> CheckResult:
    package_root = package_root.expanduser().resolve()
    issues: list[str] = []

    if not package_root.exists():
        return CheckResult(False, [f"package root does not exist: {package_root}"])

    agent_path = package_root / "agent.yaml"
    if not agent_path.exists():
        issues.append("missing file: agent.yaml")
    else:
        issues.extend(_missing_keys(agent_path, REQUIRED_AGENT_KEYS, "agent.yaml"))

    for directory, required_keys in REQUIRED_PARTS.items():
        part_dir = package_root / directory
        if not part_dir.exists():
            issues.append(f"missing directory: {directory}")
            continue
        files = sorted(part_dir.glob("*.yaml"))
        if not files:
            issues.append(f"missing yaml file in: {directory}")
            continue
        for file_path in files:
            issues.extend(_missing_keys(file_path, required_keys, str(file_path.relative_to(package_root))))

    delivery_path = package_root / "reports" / "delivery-package.md"
    if not delivery_path.exists():
        issues.append("missing file: reports/delivery-package.md")

    return CheckResult(not issues, issues)


def _missing_keys(path: Path, required_keys: list[str], label: str) -> list[str]:
    keys = _top_level_keys(path)
    return [f"{label} missing key: {key}" for key in required_keys if key not in keys]


def _top_level_keys(path: Path) -> set[str]:
    keys: set[str] = set()
    pattern = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            keys.add(match.group(1))
    return keys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether a business agent package has the minimum executable contract."
    )
    parser.add_argument("package_root", help="Path to a business-agent package directory.")
    args = parser.parse_args()

    result = check_package(Path(args.package_root))
    if result.ok:
        print("PASS: business agent package is ready for a first implementation pass.")
        return 0

    print("FAIL: business agent package is missing required parts.")
    for issue in result.issues:
        print(f"- {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
