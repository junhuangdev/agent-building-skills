# Agent Scaffold Runtime Notes

This project was generated from `agent-scaffold-skill`.

## Default Behavior

When working in this project, keep the agent scaffold thin and provider-aware:

- Keep provider-specific behavior inside `agent_app/providers/`.
- Keep optional third-party capability wrappers inside `agent_app/integrations/`.
- Keep tool contracts inside `agent_app/tools/`.
- Keep approval and side-effect policy inside `agent_app/policy/`.
- Keep session or task state inside `agent_app/memory/`.
- Keep provider capability assumptions in `config/capabilities.yaml`.
- Keep third-party capability choices in `config/integrations.yaml`.
- Keep regression checks in `tests/` or `evals/`.

## Harvest Check

At the end of any task that changes these areas, check whether the work exposed a reusable scaffold lesson:

- `agent_app/providers/`
- `agent_app/integrations/`
- `agent_app/tools/`
- `agent_app/policy/`
- `agent_app/memory/`
- `config/capabilities.yaml`
- `config/integrations.yaml`
- `evals/`
- `tests/`

If the lesson is reusable across agent projects, add an entry to `docs/agent-scaffold-harvest.md`.

Do not promote project-specific prompts, business rules, or data source details into the shared scaffold.

Use `python scripts/harvest_report.py` to list entries marked `promote_to_skill: yes`.
