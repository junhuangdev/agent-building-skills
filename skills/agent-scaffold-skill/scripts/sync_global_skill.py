#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_REPO_URL = "https://github.com/junhuangdev/agent-building-skills.git"
DEFAULT_BRANCH = "main"
DEFAULT_SOURCE_ROOT = Path.home() / ".codex" / "skills" / ".sources" / "agent-building-skills"
DEFAULT_SKILL_PATH = "skills/agent-scaffold-skill"
DEFAULT_TARGET = Path.home() / ".codex" / "skills" / "agent-scaffold-skill"


def run(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=True)
    return result.stdout.strip()


def sync_skill(
    repo_url: str = DEFAULT_REPO_URL,
    target: Path = DEFAULT_TARGET,
    branch: str = DEFAULT_BRANCH,
    source_root: Path = DEFAULT_SOURCE_ROOT,
    skill_path: str = DEFAULT_SKILL_PATH,
    replace_existing: bool = False,
) -> Path:
    target = target.expanduser().absolute()
    target.parent.mkdir(parents=True, exist_ok=True)
    source_root = _sync_source_repo(repo_url, branch, source_root)
    skill_root = (source_root / skill_path).resolve()

    if target.is_symlink():
        if target.resolve() == skill_root:
            _validate_skill(skill_root)
            return target
        target.unlink()
    elif target.exists():
        if not replace_existing:
            raise SystemExit(f"Refusing to replace existing path: {target}")
        backup = _backup_path(target)
        target.rename(backup)
        print(f"Backed up {target} -> {backup}")

    if not skill_root.exists():
        raise SystemExit(f"Synced suite is missing skill path: {skill_path}")

    target.symlink_to(skill_root, target_is_directory=True)
    _validate_skill(skill_root)
    return target


def _sync_source_repo(repo_url: str, branch: str, source_root: Path) -> Path:
    source_root = source_root.expanduser().absolute()
    source_root.parent.mkdir(parents=True, exist_ok=True)

    if not source_root.exists():
        run(["git", "clone", "--branch", branch, repo_url, str(source_root)])
    elif (source_root / ".git").exists():
        _pull_existing_clone(source_root, repo_url, branch)
    else:
        raise SystemExit(f"Refusing to replace non-git source path: {source_root}")

    return source_root


def _pull_existing_clone(source_root: Path, repo_url: str, branch: str) -> None:
    status = run(["git", "status", "--short"], cwd=source_root)
    if status:
        raise SystemExit(f"Refusing to update dirty suite checkout: {source_root}")

    current_origin = run(["git", "remote", "get-url", "origin"], cwd=source_root)
    if current_origin != repo_url:
        run(["git", "remote", "set-url", "origin", repo_url], cwd=source_root)

    run(["git", "fetch", "origin", branch], cwd=source_root)
    run(["git", "checkout", branch], cwd=source_root)
    run(["git", "pull", "--ff-only", "origin", branch], cwd=source_root)


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


def _validate_skill(target: Path) -> None:
    skill_md = target / "SKILL.md"
    if not skill_md.exists():
        raise SystemExit(f"Synced checkout is missing SKILL.md: {target}")

    package_validator = target / "scripts" / "validate_skill_package.py"
    if package_validator.exists():
        run(["python", str(package_validator), str(target)])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync the globally installed agent-scaffold-skill from the agent-building-skills suite."
    )
    parser.add_argument("--repo-url", default=DEFAULT_REPO_URL, help="Git repository URL to clone or pull.")
    parser.add_argument("--branch", default=DEFAULT_BRANCH, help="Branch to sync.")
    parser.add_argument("--source-root", default=str(DEFAULT_SOURCE_ROOT), help="Local suite checkout path.")
    parser.add_argument("--skill-path", default=DEFAULT_SKILL_PATH, help="Path to this skill inside the suite.")
    parser.add_argument("--target", default=str(DEFAULT_TARGET), help="Global skill install path.")
    parser.add_argument("--replace-existing", action="store_true", help="Back up and replace an existing target.")
    args = parser.parse_args()

    target = sync_skill(
        args.repo_url,
        Path(args.target),
        args.branch,
        Path(args.source_root),
        args.skill_path,
        args.replace_existing,
    )
    head = run(["git", "rev-parse", "HEAD"], cwd=Path(args.source_root).expanduser().absolute())
    print(f"Synced agent-scaffold-skill to {target}")
    print(f"HEAD {head}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
