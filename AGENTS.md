# Agent Building Skills Instructions

This repository manages a suite of Codex skills for building better AI agents.

## Scope

- Keep all durable knowledge in this repository focused on how to build, evaluate, operate, and improve agents.
- Do not store business-domain knowledge, private project memories, credentials, or customer data here.
- Business-agent learning templates may live here; business-agent learning content must live in the generated business project.
- Promote lessons into this repository only when they are reusable across agent projects or improve a suite-managed skill.

## Structure

- `skills/agent-builder-lab/` is the source of the `agent-builder-lab` skill.
- `skills/agent-scaffold-skill/` is the source of the `agent-scaffold-skill` skill.
- `skills/capability-evolution/` is the source of the `capability-evolution` skill.
- `skills/project-start-routing/` is the source of the `project-start-routing` skill.
- `tools/` contains suite-level install, sync, and validation utilities.
- `docs/` contains suite-level governance and architecture notes.

## Editing Rules

- Keep each skill self-contained: its `SKILL.md`, `agents/`, `references/`, `assets/`, `scripts/`, and `tests/` must work from that skill directory.
- Put cross-skill automation in `tools/`, not inside one skill.
- Prefer explicit validation over convention-only instructions.
- Before claiming the suite is ready, run `python tools/validate_suite.py`.
