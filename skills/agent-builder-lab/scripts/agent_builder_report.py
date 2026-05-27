#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path


ENTRY_RE = re.compile(r"^###\s+(AB-\d+)\s+(.+)$", re.MULTILINE)
FIELD_RE = re.compile(r"^([a-z_]+):\s*(.*)$")
INTERESTING_STATUSES = {"promote", "watch", "archive", "rejected", "superseded"}


def parse_entries(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(ENTRY_RE.finditer(text))
    entries: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end]
        entry = {"id": match.group(1), "title": match.group(2).strip(), "file": str(path)}
        for raw_line in body.splitlines():
            field_match = FIELD_RE.match(raw_line.strip())
            if field_match:
                entry[field_match.group(1)] = field_match.group(2).strip()
        entries.append(entry)
    return entries


def iter_markdown(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix == ".md":
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize agent build journal entries.")
    parser.add_argument("paths", nargs="*", type=Path, help="Markdown files or directories to scan.")
    args = parser.parse_args()

    paths = args.paths or [Path("docs/agent-build-journal.md"), Path(".agent-builder-lab")]
    entries: list[dict[str, str]] = []
    for path in iter_markdown(paths):
        entries.extend(parse_entries(path))

    if not entries:
        print("No agent-builder journal entries found.")
        return 0

    status_counts = Counter(entry.get("status", "missing") for entry in entries)
    target_counts = Counter(entry.get("promotion_target", "missing") for entry in entries)
    by_status: dict[str, list[dict[str, str]]] = defaultdict(list)
    for entry in entries:
        status = entry.get("status", "missing")
        if status in INTERESTING_STATUSES or status == "missing":
            by_status[status].append(entry)

    print("Agent builder journal report")
    print("============================")
    print(f"Entries: {len(entries)}")
    print("Statuses: " + ", ".join(f"{key}={value}" for key, value in sorted(status_counts.items())))
    print("Targets: " + ", ".join(f"{key}={value}" for key, value in sorted(target_counts.items())))

    for status in sorted(by_status):
        print(f"\n{status}")
        for entry in by_status[status]:
            target = entry.get("promotion_target", "missing")
            evidence = entry.get("evidence", "")
            marker = " evidence" if evidence else " missing-evidence"
            print(f"- {entry['id']} {entry['title']} [{target};{marker}] ({entry['file']})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
