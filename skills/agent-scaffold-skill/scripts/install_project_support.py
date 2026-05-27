#!/usr/bin/env python3

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path


START_MARKER = "<!-- agent-scaffold-skill:start -->"
END_MARKER = "<!-- agent-scaffold-skill:end -->"


@dataclass(frozen=True)
class InstallResult:
    project_root: Path
    agents_path: Path
    harvest_path: Path
    report_script_path: Path


def install_project_support(project_root: Path, skill_root: Path) -> InstallResult:
    project_root = project_root.expanduser().resolve()
    skill_root = skill_root.expanduser().resolve()

    if not project_root.exists():
        raise SystemExit(f"Project root does not exist: {project_root}")
    if not (skill_root / "SKILL.md").exists():
        raise SystemExit(f"Skill root missing SKILL.md: {skill_root}")

    agents_path = project_root / "AGENTS.md"
    harvest_path = project_root / "docs" / "agent-scaffold-harvest.md"
    report_script_path = project_root / "scripts" / "harvest_report.py"

    _upsert_agents_block(agents_path)
    _copy_if_missing(skill_root / "assets" / "scaffold-template" / "docs" / "agent-scaffold-harvest.md", harvest_path)
    _copy_if_missing(skill_root / "assets" / "scaffold-template" / "scripts" / "harvest_report.py", report_script_path)
    report_script_path.chmod(0o755)

    return InstallResult(
        project_root=project_root,
        agents_path=agents_path,
        harvest_path=harvest_path,
        report_script_path=report_script_path,
    )


def _upsert_agents_block(path: Path) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    block = _agents_block()

    if START_MARKER in existing and END_MARKER in existing:
        before, rest = existing.split(START_MARKER, 1)
        _, after = rest.split(END_MARKER, 1)
        text = before.rstrip() + "\n\n" + block + "\n" + after.lstrip()
    else:
        text = existing.rstrip()
        if text:
            text += "\n\n"
        text += block + "\n"

    path.write_text(text, encoding="utf-8")


def _agents_block() -> str:
    return f"""{START_MARKER}
## Agent Scaffold Skill

This project uses `agent-scaffold-skill` for agent runtime scaffolding, provider adapters, tool policy, memory boundaries, evals, and scaffold harvest.

When work changes provider, tool, policy, memory, capability, eval, or test boundaries, check `docs/agent-scaffold-harvest.md` for reusable scaffold lessons.

Use `python scripts/harvest_report.py` to list entries marked `promote_to_skill: yes`.

Project-specific prompts, business rules, and data source details stay in this project unless the user explicitly approves promotion back to the shared skill.
{END_MARKER}"""


def _copy_if_missing(source: Path, target: Path) -> None:
    if target.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install agent-scaffold-skill support into one project that wants to depend on it."
    )
    parser.add_argument("project_root", help="Existing project root to receive local support files.")
    parser.add_argument(
        "--skill-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to the self-contained agent-scaffold-skill directory.",
    )
    args = parser.parse_args()

    result = install_project_support(Path(args.project_root), Path(args.skill_root))
    print(f"Installed agent-scaffold-skill support into {result.project_root}")
    print(f"- {result.agents_path}")
    print(f"- {result.harvest_path}")
    print(f"- {result.report_script_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
