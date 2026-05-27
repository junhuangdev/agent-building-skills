# Build Journal

Use a build journal while constructing a real agent. Record only events that can change a future agent-building decision.

## When To Record

Record an entry when one of these happens:

- A design decision affects the agent goal, loop, tools, memory, policy, evaluation, or user experience.
- A failure causes rework, unsafe behavior, weak output, excessive human involvement, or unclear evidence.
- A reusable pattern appears in implementation or evaluation.
- A limitation repeats and should become a normal constraint.
- A lesson might update a project, runtime, scaffold, workflow, skill, or collaboration rule.

Do not record routine implementation steps, one-off project data, or process narration.

## Entry Schema

```text
### AB-NNNN Short title
date: YYYY-MM-DD
agent_project: <project or experiment name>
scope: product-agent | runtime | tool | memory | policy | eval | workflow | collaboration | scaffold | reference
status: active | watch | promote | archive | rejected | superseded
quality_state: pass | repair | fail | human
signal: decision | failure | reusable-pattern | normalized-constraint | missing-capability | risk-mismatch | taste-signal
context: What was being built or tested?
decision: What changed or was chosen?
evidence: What proved the result, failure, or repeated pattern?
impact: What future agent-building work is affected?
next_task_effect: What should a future builder do differently?
promotion_target: project | agent-core | scaffold | vibeflow | eval-template | tool-strategy | memory-rule | policy-rule | docs | none
project_specific: What must not be generalized?
```

## Writing Rules

- Separate facts, inference, user preference, and AI judgment.
- Keep the title concrete enough to search later.
- Prefer observable evidence: tests, evals, run logs, user rejection, repeated rework, or explicit user preference.
- If evidence is weak, use `status: watch`.
- If an item has no clear next-task effect, do not keep it.

## Normalized Constraints

When the same limitation repeats but does not block delivery, make it a normalized constraint. The future agent should present it as a known limit or checklist item instead of treating it as a fresh defect every time.

Examples:

- A provider lacks strict JSON schema but works with JSON object mode.
- A research agent cannot prove real user adoption from vendor docs alone.
- A local tool requires manual auth refresh before external actions.
