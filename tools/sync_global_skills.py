#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


DEFAULT_REPO_URL = "https://github.com/junhuangdev/agent-building-skills.git"
DEFAULT_BRANCH = "main"
DEFAULT_SOURCE_ROOT = Path.home() / ".codex" / "skills" / ".sources" / "agent-building-skills"
DEFAULT_SKILLS_ROOT = Path.home() / ".codex" / "skills"


def run(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=True)
    return result.stdout.strip()


def sync_repo(repo_url: str, branch: str, source_root: Path) -> Path:
    source_root = source_root.expanduser().resolve()
    source_root.parent.mkdir(parents=True, exist_ok=True)

    if not source_root.exists():
        run(["git", "clone", "--branch", branch, repo_url, str(source_root)])
    elif (source_root / ".git").exists():
        status = run(["git", "status", "--short"], cwd=source_root)
        if status:
            raise SystemExit(f"Refusing to update dirty suite checkout: {source_root}")
        current_origin = run(["git", "remote", "get-url", "origin"], cwd=source_root)
        if current_origin != repo_url:
            run(["git", "remote", "set-url", "origin", repo_url], cwd=source_root)
        run(["git", "fetch", "origin", branch], cwd=source_root)
        run(["git", "checkout", branch], cwd=source_root)
        run(["git", "pull", "--ff-only", "origin", branch], cwd=source_root)
    else:
        raise SystemExit(f"Refusing to replace non-git source path: {source_root}")

    return source_root


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync and install all agent-building skills from GitHub.")
    parser.add_argument("--repo-url", default=DEFAULT_REPO_URL)
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("--source-root", default=str(DEFAULT_SOURCE_ROOT))
    parser.add_argument("--skills-root", default=str(DEFAULT_SKILLS_ROOT))
    parser.add_argument("--replace-existing", action="store_true")
    args = parser.parse_args()

    source_root = sync_repo(args.repo_url, args.branch, Path(args.source_root))
    run([str(source_root / "tools" / "validate_suite.py")], cwd=source_root)

    install_args = [
        str(source_root / "tools" / "install_skills.py"),
        "--skills-root",
        str(Path(args.skills_root).expanduser()),
    ]
    if args.replace_existing:
        install_args.append("--replace-existing")
    run(install_args, cwd=source_root)

    head = run(["git", "rev-parse", "HEAD"], cwd=source_root)
    print(f"Synced agent-building-skills to {source_root}")
    print(f"HEAD {head}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

