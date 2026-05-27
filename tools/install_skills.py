#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


SUITE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_ROOT = Path.home() / ".codex" / "skills"


def iter_skill_roots(suite_root: Path) -> list[Path]:
    skills_dir = suite_root / "skills"
    if not skills_dir.exists():
        raise SystemExit(f"Missing skills directory: {skills_dir}")
    return sorted(path for path in skills_dir.iterdir() if (path / "SKILL.md").exists())


def install_all(skills_root: Path, replace_existing: bool = False) -> list[tuple[str, Path]]:
    skills_root = skills_root.expanduser().resolve()
    skills_root.mkdir(parents=True, exist_ok=True)
    installed: list[tuple[str, Path]] = []

    for skill_root in iter_skill_roots(SUITE_ROOT):
        target = skills_root / skill_root.name
        install_one(skill_root, target, replace_existing=replace_existing)
        installed.append((skill_root.name, target))

    return installed


def install_one(skill_root: Path, target: Path, replace_existing: bool = False) -> None:
    skill_root = skill_root.resolve()

    if target.is_symlink():
        if target.resolve() == skill_root:
            return
        if not replace_existing:
            raise SystemExit(f"Refusing to replace existing symlink: {target} -> {target.resolve()}")
        target.unlink()
    elif target.exists():
        if not replace_existing:
            raise SystemExit(f"Refusing to replace existing path: {target}")
        backup = _backup_path(target)
        target.rename(backup)
        print(f"Backed up {target} -> {backup}")

    target.symlink_to(skill_root, target_is_directory=True)


def _backup_path(target: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_root = target.parent / ".backups" / "agent-building-skills"
    backup_root.mkdir(parents=True, exist_ok=True)
    backup = backup_root / f"{target.name}-{stamp}"
    counter = 1
    while backup.exists():
        backup = backup_root / f"{target.name}-{stamp}-{counter}"
        counter += 1
    return backup


def main() -> int:
    parser = argparse.ArgumentParser(description="Install all suite-managed skills into a Codex skills directory.")
    parser.add_argument("--skills-root", default=str(DEFAULT_SKILLS_ROOT), help="Codex skills directory.")
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="Move existing skill directories to a timestamped backup before installing symlinks.",
    )
    args = parser.parse_args()

    installed = install_all(Path(args.skills_root), replace_existing=args.replace_existing)
    for name, target in installed:
        print(f"Installed {name} -> {target.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
