#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import NamedTuple


START_MARKER = "<!-- agent-builder-lab:start -->"
END_MARKER = "<!-- agent-builder-lab:end -->"


class InstallResult(NamedTuple):
    project_root: Path
    agents_path: Path
    journal_path: Path
    report_script_path: Path


def install_project_support(project_root: Path, skill_root: Path) -> InstallResult:
    project_root = project_root.expanduser().resolve()
    skill_root = skill_root.expanduser().resolve()

    if not project_root.exists():
        raise SystemExit(f"Project root does not exist: {project_root}")
    if not (skill_root / "SKILL.md").exists():
        raise SystemExit(f"Skill root missing SKILL.md: {skill_root}")

    agents_path = project_root / "AGENTS.md"
    journal_path = project_root / "docs" / "agent-build-journal.md"
    report_script_path = project_root / "scripts" / "agent_builder_report.py"

    _upsert_agents_block(agents_path)
    _copy_if_missing(skill_root / "assets" / "templates" / "agent-build-journal.md", journal_path)
    _copy_if_missing(skill_root / "scripts" / "agent_builder_report.py", report_script_path)
    report_script_path.chmod(0o755)

    return InstallResult(
        project_root=project_root,
        agents_path=agents_path,
        journal_path=journal_path,
        report_script_path=report_script_path,
    )


def _upsert_agents_block(path: Path) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    block = _agents_block()

    if START_MARKER in existing and END_MARKER in existing:
        before, rest = existing.split(START_MARKER, 1)
        _, after = rest.split(END_MARKER, 1)
        text = _join_sections(before.rstrip(), block, after.lstrip())
    else:
        text = _join_sections(existing.rstrip(), block)

    path.write_text(text, encoding="utf-8")


def _join_sections(*sections: str) -> str:
    return "\n\n".join(section for section in sections if section) + "\n"


def _agents_block() -> str:
    return f"""{START_MARKER}
## Agent Builder Lab

This project uses `agent-builder-lab` to learn how to build better agents through real agent-building work.

When work changes agent goals, loops, tools, memory, policy, evals, workflow, collaboration, or Agent UX, use `$agent-builder-lab`.

Record meaningful lessons in `docs/agent-build-journal.md`: decisions, failures, reusable patterns, normalized constraints, missing capabilities, risk mismatches, and durable taste signals.

Use `python scripts/agent_builder_report.py docs/agent-build-journal.md` to list entries marked for promotion, watch, archive, rejection, or supersession.

Project-specific prompts, business rules, credentials, private data, and taste stay in this project unless the user explicitly approves a broader lesson.
{END_MARKER}"""


def _copy_if_missing(source: Path, target: Path) -> None:
    if target.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install agent-builder-lab support into one agent-building project."
    )
    parser.add_argument("project_root", help="Existing project root to receive local support files.")
    parser.add_argument(
        "--skill-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to the self-contained agent-builder-lab skill directory.",
    )
    args = parser.parse_args()

    result = install_project_support(Path(args.project_root), Path(args.skill_root))
    print(f"Installed agent-builder-lab support into {result.project_root}")
    print(f"- {result.agents_path}")
    print(f"- {result.journal_path}")
    print(f"- {result.report_script_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
