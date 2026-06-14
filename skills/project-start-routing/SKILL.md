---
name: project-start-routing
description: Use when starting, scaffolding, or materially reshaping a project, tool, app, Skill, Agent, prototype, workbench, automation, or local service where the technology stack, runtime, package manager, or project template is not already fixed by local instructions.
---

# Project Start Routing

Use this skill before choosing or changing a project's default stack. The goal is controlled variety: let the agent choose the right lane for the work, but require an explicit reason, commands, and environment boundary.

## Workflow

1. Read the nearest project instructions, existing files, and user constraints first.
2. If the stack is already fixed by the user, `AGENTS.md`, a spec, or an existing project structure, follow that source of truth.
3. If the stack is not fixed, classify the work using `references/stack-routing.md`.
4. Produce a compact project-start decision using `references/startup-checklist.md`.
5. Apply the Design System Adoption Gate before implementation when the work includes a product page, workbench, dashboard, settings screen, detail page, local tool UI, or browser-facing prototype.
6. Ask the user only when two lanes are genuinely close, the wrong choice would add meaningful maintenance cost, or the Design System Adoption Gate requires Jun's choice.
7. When creating a durable project, write the final decision into the new project's README, AGENTS file, or design note so future agents do not re-litigate the stack.

## Design System Adoption Gate

This is a mandatory decision gate, not a mandatory adoption rule.

When a project start or major reshape includes a UI surface, ask Jun whether to use `jun-ui-design-system` before choosing page implementation details. Use this shape:

> This project has a UI surface. It appears suitable / not suitable for `jun-ui-design-system` because `<short reason>`. Should I enable it for this project now?

Accepted answers:

- `adopted`: use `jun-ui-design-system` from now on.
- `deferred`: continue without it for this slice, but ask again before the next UI surface change.
- `not-suitable`: do not use it because the project has a stronger local design system or a non-Jun-facing UI requirement.

Record the answer as `jun-ui adoption decision: adopted`, `jun-ui adoption decision: deferred`, or `jun-ui adoption decision: not-suitable`.

If the answer is `adopted`, add the project-level `jun-ui-design-system` contract and run:

```bash
jun-ui doctor --strict --consumer-root <project-root>
```

If the answer is `deferred` or `not-suitable`, record `Reason:` and `Reopen path:` so the project can later switch to adopted without re-litigating the original decision. A later page/workbench/tool request may reopen the gate and change the decision to `adopted`.

## Rules

- Prefer the repo's existing package manager, runtime, test framework, and style over a new default.
- Do not add a new package manager or runtime just because it is familiar.
- Keep global runtime installs as outputs. The source of truth must live in a versioned project.
- Make install, start, and test commands explicit before implementation begins.
- Use hybrid stacks only when both sides are central to the product and the boundary is clear.
- Do not silently skip the Design System Adoption Gate for UI-capable projects. It is acceptable to continue without jun-ui only after Jun chooses `deferred` or `not-suitable` and the decision is recorded.
