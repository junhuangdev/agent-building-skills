#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


SUITE_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME_RE = re.compile(r"^name:\s*([A-Za-z0-9-]+)\s*$", re.MULTILINE)
ABSOLUTE_USER_PATH_RE = re.compile("/" + "Users" + r"/[^\s`)]+" )
CHECKED_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".toml", ".example"}


def main() -> int:
    errors: list[str] = []
    skills_dir = SUITE_ROOT / "skills"

    if not skills_dir.exists():
        errors.append("missing skills/ directory")
    else:
        skill_roots = sorted(path for path in skills_dir.iterdir() if path.is_dir())
        if not skill_roots:
            errors.append("no skill directories found under skills/")
        for skill_root in skill_roots:
            validate_skill(skill_root, errors)

    validate_no_absolute_user_paths(errors)

    if errors:
        print("Suite validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Suite validation passed.")
    return 0


def validate_skill(skill_root: Path, errors: list[str]) -> None:
    skill_md = skill_root / "SKILL.md"
    if not skill_md.exists():
        errors.append(f"{skill_root.relative_to(SUITE_ROOT)} missing SKILL.md")
        return

    text = skill_md.read_text(encoding="utf-8")
    match = SKILL_NAME_RE.search(text)
    if not match:
        errors.append(f"{skill_root.relative_to(SUITE_ROOT)} missing frontmatter name")
    elif match.group(1) != skill_root.name:
        errors.append(
            f"{skill_root.relative_to(SUITE_ROOT)} name {match.group(1)!r} does not match directory"
        )

    if not (skill_root / "agents" / "openai.yaml").exists():
        errors.append(f"{skill_root.relative_to(SUITE_ROOT)} missing agents/openai.yaml")

    validator = skill_root / "scripts" / "validate_skill_package.py"
    if validator.exists():
        result = subprocess.run(
            [sys.executable, str(validator), str(skill_root)],
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            output = (result.stdout + result.stderr).strip()
            errors.append(f"{skill_root.relative_to(SUITE_ROOT)} package validator failed: {output}")


def validate_no_absolute_user_paths(errors: list[str]) -> None:
    for path in SUITE_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts or ".venv" in path.parts or "__pycache__" in path.parts:
            continue
        if path.suffix not in CHECKED_SUFFIXES and path.name != ".env.example":
            continue
        text = path.read_text(encoding="utf-8")
        for match in ABSOLUTE_USER_PATH_RE.findall(text):
            errors.append(f"{path.relative_to(SUITE_ROOT)} contains absolute user path: {match}")


if __name__ == "__main__":
    raise SystemExit(main())
