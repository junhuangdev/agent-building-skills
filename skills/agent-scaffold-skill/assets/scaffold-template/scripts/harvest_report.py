#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


DEFAULT_HARVEST_PATH = Path("docs/agent-scaffold-harvest.md")


def parse_harvest(path: str | Path = DEFAULT_HARVEST_PATH) -> list[dict[str, str]]:
    text = Path(path).read_text(encoding="utf-8")
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("### "):
            if current and current.get("promote_to_skill", "").lower() == "yes":
                entries.append(current)
            title = line.removeprefix("### ").strip()
            entry_id, _, entry_title = title.partition(" ")
            current = {"id": entry_id, "title": entry_title.strip()}
            continue

        if current is None or ":" not in line or line.startswith("```"):
            continue

        key, value = line.split(":", 1)
        current[key.strip()] = value.strip()

    if current and current.get("promote_to_skill", "").lower() == "yes":
        entries.append(current)

    return entries


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_HARVEST_PATH
    if not path.exists():
        print(f"Harvest file not found: {path}")
        return 1

    entries = parse_harvest(path)
    if not entries:
        print("No scaffold harvest entries marked promote_to_skill: yes.")
        return 0

    print("Promotable scaffold harvest entries:")
    for entry in entries:
        print(f"- {entry.get('id', 'unknown')} [{entry.get('boundary', 'unknown')}]: {entry.get('title', '')}")
        if entry.get("lesson"):
            print(f"  lesson: {entry['lesson']}")
        if entry.get("verification"):
            print(f"  verification: {entry['verification']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
