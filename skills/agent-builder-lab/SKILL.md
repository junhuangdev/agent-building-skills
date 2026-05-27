---
name: agent-builder-lab
description: Use when learning how to build better AI agents through real agent-building work, agent design discussions, build journals, reusable lesson harvest, memory lifecycle decisions, forgetting/archiving, or deciding whether lessons should change an agent, runtime, scaffold, eval, policy, tool, workflow, or collaboration rule.
---

# Agent Builder Lab

## Overview

Use this skill to learn by building real agents. The goal is not only to ship one agent, but to extract evidence-backed knowledge about what makes an agent good.

The skill is a semi-automatic learning loop: reminders are automatic, sessions start manually or by user intent, evaluation can be automated, and absorption into durable systems requires approval.

## Core Loop

```text
build a real agent
  -> record decisions, friction, failures, and evidence
  -> classify the lesson
  -> evaluate whether it improves future agents
  -> keep, promote, archive, reject, or supersede it
```

## Scope

Capture lessons about any layer that affects agent quality:

| Layer | Examples |
| --- | --- |
| Product agent | goal, user experience, task boundary, result shape |
| Runtime | loop, state, tools, provider handling, recovery |
| Memory | what to remember, when to retrieve, when to forget |
| Policy | approval gates, risk classes, safe stopping |
| Evaluation | eval cases, quality states, evidence requirements |
| Workflow | build process, review, handoff, continuation |
| Collaboration | when to ask humans, when to proceed, how to present uncertainty |

Do not narrow promotion targets to one repository. A lesson may update an agent project, `agent-core`, `agent-scaffold-skill`, `vibeflow`, an eval template, a tool strategy, a memory rule, or no durable artifact at all.

## Workflow

1. Define the current agent-building goal and the decision being tested.
2. Keep the first agent concrete; avoid designing a universal platform first.
3. Use `references/agent-builder-guide-map.md` to choose the right reference path.
4. When studying a reusable capability, use `references/capability-reference-and-output-mining.md` before changing templates or rules.
5. For a composite business agent, define the operating model before implementation.
6. Use `references/business-agent-build-procedure.md` and `references/business-agent-package-contract.md` to create a first executable package.
7. Check the package with `scripts/check_business_agent_package.py` before treating it as ready for a first run.
8. Record meaningful build events using `references/build-journal.md`.
9. Classify each event with `references/memory-lifecycle.md`.
10. At milestones, run a harvest review using `references/harvest-and-promotion.md`.
11. Promote only evidence-backed lessons. Archive or reject stale, local, or unproven ideas.
12. If a lesson changes another skill, runtime, or project rule, present an approval package before applying it.

## Quality States

Use these states when reviewing an agent-building milestone:

| State | Meaning | Action |
| --- | --- | --- |
| `pass` | Agent behavior is usable with evidence | Keep or promote |
| `repair` | AI-fixable defect in the current build | Fix and re-check |
| `fail` | Wrong direction, unsafe, or unsupported | Stop or redesign |
| `human` | Needs product, taste, risk, or scope judgment | Ask or prepare options |

## Resources

- `references/agent-builder-guide-map.md`: reading order and decision map for building agent projects from these references.
- `references/capability-reference-and-output-mining.md`: method for studying external agent capabilities by comparing processes and output objects before promoting local contracts.
- `references/business-agent-build-procedure.md`: executable step-by-step procedure for creating a first Composite Business Agent package.
- `references/business-agent-package-contract.md`: machine-readable package structure, required fields, invariants, and checker scope.
- `references/runtime-portable-business-agent.md`: adapter rules for keeping business agents portable across Codex, OpenCode, Hermes, OpenClaw, or self-built runtimes.
- `references/build-journal.md`: journal schema and logging rules.
- `references/memory-lifecycle.md`: keep/promote/archive/reject/supersede decisions.
- `references/harvest-and-promotion.md`: milestone review and promotion targets.
- `references/agent-evaluation-cognition.md`: evaluation principles, trace/outcome/capability layers, trigger rules, and shared-vs-project boundaries.
- `references/composite-business-agent.md`: second agent shape where a host agent, skills, project system, CLI, reports, and human review jointly form a business agent.
- `references/business-agent-operating-model.md`: fixed business-agent operating capabilities such as runs, actions, artifacts, evidence, gates, delivery, and feedback.
- `references/memory-learning-layers.md`: layered ownership of runtime, business, collaboration, eval, and agent-building memory and learning systems.
- `assets/templates/agent-build-journal.md`: copy into real agent projects.
- `assets/templates/business-agent/`: copy to start a first business-agent package.
- `assets/templates/capability-reference-study.yaml`: structured study template for extracting external process, output objects, invariants, field-trial plans, and promotion decisions.
- `scripts/agent_builder_report.py`: summarize journal entries that need promotion, review, or forgetting.
- `scripts/check_business_agent_package.py`: check whether a business-agent package has the minimum executable contract.
- `scripts/install_project_support.py`: add the local journal, report script, and `AGENTS.md` trigger block to a real agent project.

## Existing Projects

Install project-local support before repeated work on an agent-building project:

```bash
python scripts/install_project_support.py /path/to/agent-project
```

This creates `docs/agent-build-journal.md`, copies the report script into `scripts/`, and adds an idempotent `AGENTS.md` block.

## Red Flags

- The agent project keeps changing but no lessons are recorded.
- Lessons are promoted because they sound smart, not because they have evidence.
- Every idea is pushed into a scaffold or core runtime.
- Project-specific prompts, data, or taste are treated as universal agent principles.
- Old lessons remain active after newer evidence contradicts them.
