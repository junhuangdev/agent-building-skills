---
name: capability-evolution
description: Use when Codex, another Skill, an Agent, or a project needs capability evolution from task results, user feedback, evals, repeated failures, memory reuse, stale learned content, self-improvement, self-evolution, learning, or promotion/archive decisions without over-generalizing local knowledge.
---

# Capability Evolution

## Overview

Use this skill as the reusable capability-evolution loop for AI work. It can be called by itself, by another Skill, by an Agent, or by a project workflow.

The skill owns the evolution mechanism. It does not own every learned fact. Learned content should be routed to the owner that will use and maintain it.

## Core Rule

Do not treat learning or memory as the goal. Capability evolution requires a use-backed loop:

```text
learn -> store -> retrieve -> use -> evaluate -> improve -> learn_again
```

Before writing or promoting any evolution artifact, decide its `evolution_target`, `storage_sink`, `scope`, `evidence`, `future_use`, `use_history`, `last_use_result`, and `risk`.

Self-reference is allowed: `$capability-evolution` may use this same loop to improve itself. It may draft memory, evals, use records, and promotion packages for itself, but it must not approve its own shared-layer or high-risk promotion.

## Workflow

1. **Classify the evolution event.** Is this user feedback, task trace, eval result, repeated failure, stale memory, reuse result, self-improvement, or promotion request?
2. **Read the right reference.**
   - Task execution loop: `references/execution-contract.md`
   - Caller integration: `references/integration-contract.md`
   - Storage routing: `references/storage-routing.md`
   - Use and reuse loop: `references/use-contract.md`
   - Self-evolution: `references/self-evolution.md`
   - Memory write/update/forget: `references/memory-lifecycle.md`
   - Eval cases and scoring: `references/eval-contract.md`
   - Skill/rule/template promotion: `references/promotion-contract.md`
   - Examples: `references/examples.md`
3. **Choose the artifact.**
   - Memory item: `assets/templates/memory-item.yaml`
   - Eval case: `assets/templates/eval-case.yaml`
   - Feedback record: `assets/templates/feedback-record.yaml`
   - Promotion package: `assets/templates/promotion-package.md`
4. **Apply, then evaluate.** When a learned artifact is used, record whether it helped, partially helped, misled, was stale, or was not applicable.
5. **Improve the artifact.** Confirm, narrow, revise, supersede, archive, reject, or promote based on use evidence.
6. **Apply the human boundary.** AI may draft, classify, evaluate, archive low-value items, and prepare promotion packages. Humans decide final usefulness, durable preference, high-risk approval, and shared-layer promotion.
7. **Validate structure when files are produced.** Run:

```bash
python <capability-evolution-skill>/scripts/check_evolution_package.py <evolution-package-dir>
```

## Stop Conditions

Stop and ask or prepare a decision package when:

- the learning would change a shared Skill, global rule, approval gate, or runtime behavior;
- the capability-evolution skill is trying to approve or apply its own promotion;
- the memory contains private data, credentials, raw chat, or project-sensitive content;
- evidence is weak but the proposed rule would affect many future tasks;
- outcome looks correct but trace, policy, or memory behavior failed.

## Anti-Patterns

| Anti-pattern | Correct move |
| --- | --- |
| "User said remember, so write global memory" | Determine scope and future use first |
| "This worked once, make it a Skill" | Put in `watch` unless evidence threshold is met |
| "Final answer passed, so evolution succeeded" | Check use result, outcome, trace, memory, policy, and feedback |
| "Business lesson is generally useful" | Keep project-local unless cross-project evidence exists |
| "Learning owns all learned content" | Route content to the owner: project, Skill, Agent, user memory, or runtime candidate |
| "Stored means improved" | Reuse it, evaluate the use result, then improve or archive |
| "Self-evolution can approve itself" | Draft and evaluate only; shared promotion needs external approval |
| "Old memory says X" | Verify freshness when facts may drift |
