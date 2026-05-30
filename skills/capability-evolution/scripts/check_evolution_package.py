#!/usr/bin/env python3
"""Validate a lightweight capability-evolution package.

The checker intentionally uses only the Python standard library. It validates the
schema surface that matters for AI handoff: evolution target, storage owner,
scope, status, future use, use history, evidence, trace expectations, feedback,
and promotion package headings.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


MEMORY_REQUIRED = {
    "id",
    "evolution_target",
    "storage_sink",
    "scope",
    "status",
    "source",
    "context",
    "content",
    "future_use",
    "use_history",
    "last_use_result",
    "evidence",
    "counterexamples",
    "risk",
    "last_confirmed",
    "review_trigger",
}
EVOLUTION_TARGETS = {
    "agent_method",
    "agent_business",
    "software_project",
    "workflow_process",
    "skill_improvement",
    "user_preference",
    "runtime_behavior",
}
STORAGE_SINKS = {
    "current_project",
    "owning_agent_repo",
    "owning_skill_package",
    "shared_skill_candidate",
    "user_memory",
    "runtime_candidate",
}
MEMORY_SCOPES = {"project", "user", "shared_candidate", "runtime"}
MEMORY_STATUSES = {"watch", "active", "promote", "archive", "rejected", "superseded"}
USE_RESULTS = {"helped", "partial", "misled", "stale", "not_applicable", "not_used"}
TARGET_ALLOWED_SINKS = {
    "agent_method": {"current_project", "owning_agent_repo", "shared_skill_candidate"},
    "agent_business": {"current_project", "owning_agent_repo"},
    "software_project": {"current_project"},
    "workflow_process": {"current_project", "owning_skill_package", "shared_skill_candidate"},
    "skill_improvement": {"current_project", "owning_skill_package", "shared_skill_candidate"},
    "user_preference": {"current_project", "user_memory"},
    "runtime_behavior": {"runtime_candidate", "shared_skill_candidate"},
}

EVAL_REQUIRED = {"id", "goal", "input", "expected_outcome", "expected_use", "expected_trace", "scorers"}
FEEDBACK_REQUIRED = {
    "id",
    "source_task",
    "result_useful",
    "reason",
    "durable_preference",
    "evolution_action",
    "use_feedback",
}
PROMOTION_HEADINGS = [
    "Recommendation:",
    "Evidence:",
    "Impact:",
    "Risk if changed:",
    "Risk if not changed:",
    "Target:",
    "Decision needed:",
]


def parse_top_level_keys(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().split("#", 1)[0].strip()
    return values


def fail(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path}: {message}")


def require_keys(errors: list[str], path: Path, values: dict[str, str], required: set[str]) -> None:
    missing = sorted(required - set(values))
    if missing:
        fail(errors, path, f"missing keys: {', '.join(missing)}")


def validate_memory(errors: list[str], path: Path) -> None:
    values = parse_top_level_keys(path)
    require_keys(errors, path, values, MEMORY_REQUIRED)
    evolution_target = values.get("evolution_target")
    if evolution_target and evolution_target not in EVOLUTION_TARGETS:
        fail(errors, path, f"invalid evolution_target {evolution_target!r}")
    storage_sink = values.get("storage_sink")
    if storage_sink and storage_sink not in STORAGE_SINKS:
        fail(errors, path, f"invalid storage_sink {storage_sink!r}")
    if evolution_target and storage_sink and storage_sink not in TARGET_ALLOWED_SINKS[evolution_target]:
        fail(errors, path, f"{evolution_target!r} cannot use storage_sink {storage_sink!r}")
    scope = values.get("scope")
    if scope and scope not in MEMORY_SCOPES:
        fail(errors, path, f"invalid scope {scope!r}")
    status = values.get("status")
    if status and status not in MEMORY_STATUSES:
        fail(errors, path, f"invalid status {status!r}")
    if values.get("scope") == "shared_candidate" and values.get("status") == "active":
        fail(errors, path, "shared_candidate memory cannot be active without promotion")
    if values.get("storage_sink") == "shared_skill_candidate" and values.get("status") == "active":
        fail(errors, path, "shared_skill_candidate memory cannot be active without promotion")
    if not values.get("future_use"):
        fail(errors, path, "future_use must be concrete")
    if values.get("last_use_result") and values["last_use_result"] not in USE_RESULTS:
        fail(errors, path, f"invalid last_use_result {values['last_use_result']!r}")
    text = path.read_text(encoding="utf-8")
    if "use_result:" not in text:
        fail(errors, path, "use_history must include use_result")
    if "follow_up:" not in text:
        fail(errors, path, "use_history must include follow_up")


def validate_eval(errors: list[str], path: Path) -> None:
    values = parse_top_level_keys(path)
    require_keys(errors, path, values, EVAL_REQUIRED)
    text = path.read_text(encoding="utf-8")
    if "must_do:" not in text:
        fail(errors, path, "expected_trace must include must_do")
    if "must_not_do:" not in text:
        fail(errors, path, "expected_trace must include must_not_do")
    if "use_result:" not in text:
        fail(errors, path, "expected_use must include use_result")
    if "use_result" not in text:
        fail(errors, path, "eval should include use_result scorer")
    if not re.search(r"policy_gate|trace_invariant|memory_scope", text):
        fail(errors, path, "eval should include at least one trace, memory, or policy scorer")


def validate_feedback(errors: list[str], path: Path) -> None:
    values = parse_top_level_keys(path)
    require_keys(errors, path, values, FEEDBACK_REQUIRED)
    if values.get("result_useful") not in {"yes", "no", "partial"}:
        fail(errors, path, "result_useful must be yes, no, or partial")
    if values.get("durable_preference") not in {"yes", "no", "only_this_project"}:
        fail(errors, path, "durable_preference must be yes, no, or only_this_project")
    text = path.read_text(encoding="utf-8")
    if "use_result:" not in text:
        fail(errors, path, "use_feedback must include use_result")
    if "follow_up:" not in text:
        fail(errors, path, "use_feedback must include follow_up")


def validate_promotion(errors: list[str], path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for heading in PROMOTION_HEADINGS:
        if heading not in text:
            fail(errors, path, f"missing heading {heading}")
    decision = re.search(r"Decision needed:\s*(.+)", text)
    if decision and decision.group(1).strip() not in {"accept", "revise", "defer", "reject"}:
        fail(errors, path, "decision must be accept, revise, defer, or reject")


def validate_package(root: Path) -> list[str]:
    errors: list[str] = []
    if not root.exists():
        return [f"{root}: package path does not exist"]
    for path in sorted((root / "memory").glob("*.yaml")):
        validate_memory(errors, path)
    for path in sorted((root / "evals").glob("*.yaml")):
        validate_eval(errors, path)
    for path in sorted((root / "feedback").glob("*.yaml")):
        validate_feedback(errors, path)
    for path in sorted((root / "promotions").glob("*.md")):
        validate_promotion(errors, path)
    if not any((root / name).exists() for name in ("memory", "evals", "feedback", "promotions")):
        errors.append(f"{root}: no evolution artifact directories found")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a capability-evolution package.")
    parser.add_argument("package", type=Path, help="Directory containing memory/evals/feedback/promotions")
    args = parser.parse_args()

    errors = validate_package(args.package)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.package} is a valid capability-evolution package")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
