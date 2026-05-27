# Good Agent Principles

Use this reference to keep the scaffold focused on building useful agents, not only generating files.

## Definition

A good agent reliably turns a user goal into verified progress while respecting capability limits, tool risks, and human approval boundaries.

This file is not a general agent philosophy document. Add principles here only when they change scaffold structure, runtime behavior, provider adaptation, tool design, memory, approval gates, or eval design.

## Core Capabilities

| Capability | Good Behavior | Failure Mode |
| --- | --- | --- |
| Goal alignment | Restates goal, scope, and acceptance when needed | Solves the wrong task confidently |
| Planning | Chooses a small next step and updates when facts change | Produces long plans without execution |
| Tool use | Calls tools only when they improve evidence or action | Calls tools because they are available |
| State handling | Keeps task state compact and recoverable | Dumps all history into context |
| Uncertainty | Surfaces high-cost ambiguity | Hides guesses until final failure |
| Policy | Stops before risky external effects | Treats all tools as equally safe |
| Recovery | Classifies failure and retries with a changed tactic | Repeats the same failing call |
| Evaluation | Has cases that catch regressions | Relies on vibes after provider changes |

## Design Checks

Before adding a module or abstraction, answer:

1. What user-visible failure does this prevent?
2. What agent decision does this make clearer?
3. What provider difference does this isolate?
4. What eval proves it works?

If none of these has a concrete answer, keep the scaffold smaller.

## Assembly Design

Good agents can be assembled from mature third-party capabilities, but the scaffold must keep the boundaries explicit.

- Prefer proven libraries, services, MCP servers, or frameworks when they reduce real implementation risk.
- Wrap third-party capabilities behind adapters in `agent_app/integrations/` unless they belong in a more specific boundary.
- Record choices in `config/integrations.yaml`.
- Keep project-specific prompts, data sources, and credentials out of the shared skill.
- Add evals or contract tests before treating an integration as stable.

## Tool Design

Good tools are narrow, typed, and observable.

- Give each tool one job.
- Define JSON schema strictly.
- Return structured results plus concise human-readable summaries.
- Mark tool risk as `low`, `external`, `destructive`, `permission`, or `money`.
- Keep side-effecting tools behind approval gates.
- Log inputs, outputs, duration, and errors.

## Memory Design

Memory should improve future decisions without polluting the current context.

Use three buckets:

| Bucket | Examples | Lifetime |
| --- | --- | --- |
| Session state | current goal, tool results, pending approvals | current run |
| Project memory | repo conventions, provider decisions, eval baselines | project |
| User preference | language, output style, risk tolerance | cross project only when explicitly durable |

Do not store raw transcripts as default memory. Store decisions, constraints, and reusable facts.

## Provider Design

Model switching should not change the agent loop.

Provider adapters own:

- request normalization
- streaming normalization
- tool call parsing
- structured output behavior
- usage accounting
- retryable error classification
- capability flags

The agent loop reads capabilities and adapts behavior. It should not branch on provider names except for logging or diagnostics.

## Evaluation

Every serious agent scaffold needs small evals before it needs a plugin system.

Start with:

- golden task cases
- tool-call expected cases
- no-tool expected cases
- refusal or approval-gate cases
- provider-switch smoke cases
- structured-output contract cases

Track both correctness and process quality:

- Did the agent call the right tool?
- Did it avoid unsafe actions?
- Did it ask for approval only when needed?
- Did it recover from a tool error?
- Did output remain stable across providers?

## Practical Standard

An agent is ready to use when it can:

1. Explain what it is trying to do.
2. Use tools with typed inputs and outputs.
3. Stop before high-risk actions.
4. Recover from common tool/model failures.
5. Run repeatable evals.
6. Swap at least one provider without changing business logic.
