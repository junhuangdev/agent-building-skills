# Project Boundaries

The suite has one durable purpose: improve how agents are built.

## What Belongs Here

- Agent-building principles.
- Scaffold templates and provider/runtime boundaries.
- Evaluation methods and reusable eval templates.
- Memory, learning, forgetting, risk, policy, workflow, and collaboration patterns for agents.
- Tools that install, validate, sync, or package suite-managed skills.
- Meta-lessons extracted from real agent-building work after review.

## What Does Not Belong Here

- Business facts learned by a generated agent.
- Project-specific user preferences.
- Customer or private data.
- Domain prompts that only apply to one business project.
- Operational run logs from a concrete business agent, except anonymized examples approved as reusable references.

## Ownership Split

| Layer | Owner | Stored Here |
| --- | --- | --- |
| Agent-building knowledge | This suite | Yes |
| Scaffold structure | `agent-scaffold-skill` | Yes |
| Agent learning mechanism | `agent-builder-lab` and scaffold templates | Yes |
| Business learning content | Concrete business agent project | No |
| Runtime internals | Codex, OpenCode, Hermes, OpenClaw, or custom runtime | No |
| Cross-project meta-lessons | This suite after review | Yes |

The suite teaches generated agents how to learn. It does not own what those agents learn about their business domain.

