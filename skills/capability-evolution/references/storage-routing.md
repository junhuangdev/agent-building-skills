# Storage Routing

## Conclusion

Keep one evolution mechanism, but store learned content with the owner that will use and maintain it.

## Field Meanings

| Field | Meaning |
| --- | --- |
| `evolution_target` | What kind of future behavior or knowledge should change |
| `storage_sink` | Where the artifact should live and who owns it |
| `scope` | How broadly the artifact may be reused |

`scope` is not the same as `storage_sink`. A project may hold a `shared_candidate`, and an owning Skill may hold an under-evidenced `watch` item.

## Targets

| `evolution_target` | Use when |
| --- | --- |
| `agent_method` | General Agent-building or Agent-operation method |
| `agent_business` | Agent-specific business/domain behavior |
| `software_project` | Project architecture, commands, domain facts, local codebase knowledge |
| `workflow_process` | Development process, review flow, delivery habit, collaboration pattern |
| `skill_improvement` | A Skill should change its own procedure, examples, templates, or evals |
| `user_preference` | Durable user preference across or within projects |
| `runtime_behavior` | Host runtime, tool, permission, adapter, or execution behavior |

## Storage Sinks

| `storage_sink` | Use when |
| --- | --- |
| `current_project` | The content is local to the active repo or project |
| `owning_agent_repo` | The content belongs to a specific Agent package |
| `owning_skill_package` | The content belongs to a specific Skill package |
| `shared_skill_candidate` | The content may become shared behavior but still needs evidence or approval |
| `user_memory` | The content is a confirmed user preference or durable user-level fact |
| `runtime_candidate` | The content concerns runtime behavior and needs runtime-owner approval |

## Default Routing

| Target | Default sink | Default scope |
| --- | --- | --- |
| `agent_method` | `owning_agent_repo` or `shared_skill_candidate` | `project` or `shared_candidate` |
| `agent_business` | `owning_agent_repo` | `project` |
| `software_project` | `current_project` | `project` |
| `workflow_process` | `current_project` | `project` |
| `skill_improvement` | `owning_skill_package` | `project` or `shared_candidate` |
| `user_preference` | `user_memory` | `user` |
| `runtime_behavior` | `runtime_candidate` | `runtime` |

## Rules

- If the owner is unclear, use `current_project` with `status: watch` rather than shared promotion.
- If content contains project facts, business details, raw conversation, credentials, or private data, keep it out of shared artifacts.
- If a method appears reusable across projects, store it as `shared_skill_candidate`, not `active`.
- If a Skill learns about itself, prefer `owning_skill_package`; use `shared_skill_candidate` only when the change affects shared behavior.
- If an Agent learns both method and business behavior, split them into separate memory items.
- If runtime behavior is involved, use `runtime_candidate` until the runtime owner approves.
