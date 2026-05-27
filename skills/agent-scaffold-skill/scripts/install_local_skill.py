#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_SKILL_NAME = "agent-scaffold-skill"


def install_skill(skill_root: Path, skills_root: Path, name: str = DEFAULT_SKILL_NAME) -> Path:
    skill_root = skill_root.expanduser().resolve()
    skills_root = skills_root.expanduser().resolve()
    target = skills_root / name

    if not (skill_root / "SKILL.md").exists():
        raise SystemExit(f"SKILL.md not found in skill root: {skill_root}")

    skills_root.mkdir(parents=True, exist_ok=True)

    if target.is_symlink():
        if target.resolve() == skill_root:
            return target
        raise SystemExit(f"Refusing to replace existing symlink: {target} -> {target.resolve()}")

    if target.exists():
        raise SystemExit(f"Refusing to replace existing path: {target}")

    target.symlink_to(skill_root, target_is_directory=True)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Install this skill into a local Codex skill directory.")
    parser.add_argument(
        "--skill-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Path to this self-contained skill directory.",
    )
    parser.add_argument(
        "--skills-root",
        default=str(Path.home() / ".codex" / "skills"),
        help="Codex skills directory.",
    )
    parser.add_argument("--name", default=DEFAULT_SKILL_NAME, help="Installed skill directory name.")
    args = parser.parse_args()

    target = install_skill(Path(args.skill_root), Path(args.skills_root), args.name)
    print(f"Installed {args.name} -> {target.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
