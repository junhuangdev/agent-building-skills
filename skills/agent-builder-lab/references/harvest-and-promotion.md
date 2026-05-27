# Harvest And Promotion

Run a harvest review at meaningful milestones: first working run, failed prototype, provider switch, tool integration, memory design change, approval policy change, or user acceptance/rejection.

## Milestone Review

1. List journal entries since the last review.
2. Group entries by root cause or design layer.
3. Mark each group as `keep`, `promote`, `archive`, `reject`, or `supersede`.
4. Decide the correct promotion target.
5. Require evidence and an approval package before changing durable systems.

## Promotion Targets

| Target | Use When |
| --- | --- |
| Agent project | Business rules, product taste, data sources, UI, channel behavior |
| `agent-core` | Loop, state, tool dispatch, provider routing, recovery, durable runtime contracts |
| `agent-scaffold-skill` | Starter structure, reusable module boundary, provider/tool/memory/eval templates |
| `vibeflow` | Collaboration boundary, human participation, risk authorization, delivery contract |
| Eval template | A test shape catches a general agent-quality failure |
| Tool strategy | Tool schema, sandbox, approval, or integration pattern repeats |
| Memory rule | What to store, retrieve, summarize, expire, or forget changes future quality |
| Reference only | Useful learning, but not a rule or implementation change |
| Archive | No material future value |

## Approval Package

For any promotion outside the current project, present:

```text
Recommendation: What should change?
Evidence: Which runs, tests, user feedback, or repeated failures support it?
Impact: What future agent-building work improves?
Risk if changed: What could become worse?
Risk if not changed: What failure will likely repeat?
Target: Which file, skill, template, runtime, or project should change?
Decision needed: accept / revise / defer / reject
```

## Guardrails

- Do not promote business prompts, private data, or one-project taste into global rules.
- Do not make a scaffold absorb every good idea.
- Do not turn a weak lesson into a workflow step.
- Do not let an automation directly rewrite global skills or user-level runtime files.
- Do not keep dead memories active for politeness.

## Dry-Run Prompt

Use this compact prompt when reviewing a journal:

```text
Use $agent-builder-lab to review this agent build journal. Identify entries to keep, promote, archive, reject, or supersede. For each promotion candidate, name the correct target and the evidence gap, if any.
```
