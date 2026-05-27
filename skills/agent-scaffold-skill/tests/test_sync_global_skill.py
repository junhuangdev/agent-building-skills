import importlib.util
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_sync_module():
    module_path = ROOT / "scripts" / "sync_global_skill.py"
    spec = importlib.util.spec_from_file_location("sync_global_skill", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def git(cwd: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def create_source_repo(path: Path, description: str) -> None:
    path.mkdir()
    git(path, "init", "-b", "main")
    git(path, "config", "user.email", "test@example.com")
    git(path, "config", "user.name", "Test User")
    skill_root = path / "skills" / "agent-scaffold-skill"
    skill_root.mkdir(parents=True)
    (skill_root / "SKILL.md").write_text(
        f"---\nname: agent-scaffold-skill\ndescription: {description}\n---\n\n# Agent Scaffold Skill\n",
        encoding="utf-8",
    )
    git(path, "add", "skills/agent-scaffold-skill/SKILL.md")
    git(path, "commit", "-m", "initial")


def test_sync_replaces_symlink_with_git_clone(tmp_path):
    sync = load_sync_module()
    source = tmp_path / "source"
    create_source_repo(source, "test skill")
    target = tmp_path / "skills" / "agent-scaffold-skill"
    symlink_source = tmp_path / "workspace-copy"
    symlink_source.mkdir()
    target.parent.mkdir()
    target.symlink_to(symlink_source, target_is_directory=True)

    source_root = tmp_path / "suite-source"
    result = sync.sync_skill(str(source), target, branch="main", source_root=source_root)

    assert result == target
    assert target.is_symlink()
    assert "test skill" in (target / "SKILL.md").read_text(encoding="utf-8")


def test_sync_updates_existing_clone_to_latest_commit(tmp_path):
    sync = load_sync_module()
    source = tmp_path / "source"
    create_source_repo(source, "old description")
    target = tmp_path / "skills" / "agent-scaffold-skill"
    source_root = tmp_path / "suite-source"

    sync.sync_skill(str(source), target, branch="main", source_root=source_root)
    (source / "skills" / "agent-scaffold-skill" / "SKILL.md").write_text(
        "---\nname: agent-scaffold-skill\ndescription: new description\n---\n\n# Agent Scaffold Skill\n",
        encoding="utf-8",
    )
    git(source, "add", "skills/agent-scaffold-skill/SKILL.md")
    git(source, "commit", "-m", "update")

    sync.sync_skill(str(source), target, branch="main", source_root=source_root)

    assert "new description" in (target / "SKILL.md").read_text(encoding="utf-8")
