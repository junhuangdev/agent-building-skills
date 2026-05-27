#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "scaffold-template"


def copy_template(target: Path, name: str) -> None:
    if target.exists() and any(target.iterdir()):
        raise SystemExit(f"Target exists and is not empty: {target}")

    shutil.copytree(TEMPLATE, target, dirs_exist_ok=True)

    pyproject = target / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")
    text = text.replace('name = "agent-scaffold"', f'name = "{name}"')
    pyproject.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a lightweight multi-provider agent project.")
    parser.add_argument("target", help="Target project directory")
    parser.add_argument("--name", default="agent-scaffold", help="Python project name")
    args = parser.parse_args()

    copy_template(Path(args.target).expanduser().resolve(), args.name)
    print(f"Created agent scaffold at {Path(args.target).expanduser().resolve()}")


if __name__ == "__main__":
    main()
