# Agent Building Skills

This repository is the source workspace for skills, tools, and references used to build better AI agents.

It is a skill suite, not one universal agent runtime. Each skill under `skills/` must remain usable as a self-contained Codex skill. The repository root manages installation, validation, release, and shared project boundaries.

## Skills

| Skill | Responsibility |
| --- | --- |
| `agent-builder-lab` | Learn how to build better agents through real agent-building work, evidence, evaluation, and approved lesson promotion. |
| `agent-scaffold-skill` | Create and improve concrete agent scaffolds with provider adapters, tools, policy gates, memory/state, and eval hooks. |
| `capability-evolution` | Research and apply use-backed capability evolution in Agents, Skills, and projects: learning artifacts, retrieval, use, evaluation, improvement, forgetting, and promotion. |

## Boundaries

- This repository stores knowledge about building good agents.
- It does not store business-domain knowledge from generated agents.
- Business memories, user preferences, private data, project rules, and domain feedback stay in the concrete business agent project.
- Reusable meta-lessons may be proposed back into this suite only after review.
- A scaffold is one part of good agent construction, not the whole body of knowledge.
- Capability evolution is a reusable mechanism. It does not own every learned fact; it routes learned artifacts to the project, Agent, Skill, or shared layer that will use and maintain them.

## Layout

```text
agent-building-skills/
├── skills/
│   ├── agent-builder-lab/
│   ├── agent-scaffold-skill/
│   └── capability-evolution/
├── docs/
├── tools/
└── README.md
```

Topic research that supports `capability-evolution` lives under
`docs/topics/capability-evolution/`. The runnable skill lives under
`skills/capability-evolution/`.

## Local Install

Install every suite-managed skill into `~/.codex/skills` as symlinks:

```bash
python tools/install_skills.py
```

If an old install already exists, create a backup and replace it with a symlink:

```bash
python tools/install_skills.py --replace-existing
```

## Validate

Run the suite-level checks:

```bash
python tools/validate_suite.py
```

Then run skill-specific tests when changing scripts or templates:

```bash
python -m pytest skills/agent-builder-lab/tests skills/agent-scaffold-skill/tests
```

When changing `capability-evolution`, also run:

```bash
python skills/capability-evolution/scripts/validate_skill_package.py skills/capability-evolution
```
