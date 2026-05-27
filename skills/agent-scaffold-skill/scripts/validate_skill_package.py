#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


REFERENCE_RE = re.compile(r"`((?:references|scripts|assets)/[^`]+)`")
ABSOLUTE_USER_PATH_RE = re.compile("/" + "Users" + r"/[^\s`)]+")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []

    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        errors.append("missing SKILL.md")
    else:
        text = skill_md.read_text(encoding="utf-8")
        for relative in REFERENCE_RE.findall(text):
            target = root / relative
            if not target.exists():
                errors.append(f"SKILL.md references missing path: {relative}")

    checked_suffixes = {".md", ".py", ".yaml", ".yml", ".toml", ".example"}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if ".venv" in path.parts or "__pycache__" in path.parts:
            continue
        if path.suffix not in checked_suffixes and path.name != ".env.example":
            continue
        text = path.read_text(encoding="utf-8")
        for match in ABSOLUTE_USER_PATH_RE.findall(text):
            errors.append(f"{path.relative_to(root)} contains absolute user path: {match}")

    if errors:
        print("Skill package validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Skill package validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
