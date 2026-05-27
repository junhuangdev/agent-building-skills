# Harvest Loop

Use this reference when a real agent project exposes lessons that might improve this skill.

## Rule

Promote only lessons that change reusable scaffold structure or runtime behavior.

Keep project-specific business logic in the generated agent project.

## Trigger Model

Generated agent projects should include:

- `AGENTS.md`: project-local reminder to check scaffold harvest after provider, tool, policy, memory, capability, eval, or test changes.
- `docs/agent-scaffold-harvest.md`: append-only record of reusable scaffold lessons.
- `scripts/harvest_report.py`: report entries marked `promote_to_skill: yes`.

The harvest loop is not a background automation. It is an automatic checkpoint inside normal agent-project work, followed by human confirmation before updating the shared skill.

## Ownership Direction

Projects depend on this skill. This skill does not depend on projects.

Do not add global project registries, workspace crawlers, or automatic project discovery. Existing projects opt in by installing project-local support. New projects opt in by being generated from the scaffold template.

## Classification

| Signal | Promote To Skill | Keep In Project |
| --- | --- | --- |
| Provider response shape differs | Yes | No |
| Tool schema pattern repeats | Yes | No |
| Third-party integration adapter pattern repeats | Yes | No |
| Approval gate risk class is missing | Yes | No |
| Memory bucket boundary changes | Yes | No |
| Eval case catches scaffold regression | Yes | No |
| Business prompt works well | No | Yes |
| Project data source detail | Usually no | Yes |
| User preference for one project | No | Yes |

## Promotion Targets

| Lesson Type | Target |
| --- | --- |
| Module boundary | `references/architecture.md` |
| Provider behavior | `references/provider-adapters.md` |
| Integration pattern | `references/capability-integration.md` |
| Capability flag | `references/capabilities.md` or template `config/capabilities.yaml` |
| Agent quality rule | `references/good-agent-principles.md` |
| Usage process | `references/scaffold-usage.md` |
| Runtime contract | `assets/scaffold-template/agent_app/` |
| Regression guard | `assets/scaffold-template/tests/` or `assets/scaffold-template/evals/` |

## Before Updating The Skill

Answer these questions:

1. What user-visible or developer-visible failure did the real agent expose?
2. Is the lesson reusable across at least one other plausible agent project?
3. Which scaffold boundary should own the change?
4. What eval or test proves the change works?
5. What project-specific detail should stay out of this skill?

If the answer is unclear, keep the lesson in the agent project first.
