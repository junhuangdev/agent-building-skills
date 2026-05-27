# Capability Integration

Use this reference when an agent needs a capability that could come from an open-source project, third-party service, framework, MCP server, SDK, or local package.

## Principle

Treat the scaffold as an assembly layer, not a hand-built platform.

Prefer mature third-party capabilities when they can be wrapped behind the scaffold's boundaries and verified with evals or contract tests.

## Decision Flow

```text
agent need
  -> capability category
  -> build vs integrate decision
  -> adapter boundary
  -> config/integrations.yaml
  -> eval or contract test
```

## Capability Categories

| Category | Examples | Scaffold Boundary |
| --- | --- | --- |
| Model provider | DeepSeek, OpenAI, Gemini, Claude, local models | `agent_app/providers/` |
| Retrieval / RAG | document loaders, vector DB, rerankers | `agent_app/integrations/` |
| Web / browser | search, scraping, browser automation | `agent_app/integrations/` + policy |
| Tool runtime | MCP tools, local tools, hosted tools | `agent_app/tools/` |
| Memory | session, project, long-term memory | `agent_app/memory/` |
| Workflow | graphs, queues, schedulers | `agent_app/integrations/` |
| Guardrails | PII filter, approval classifier, content policy | `agent_app/policy/` |
| Observability | traces, logs, token/cost tracking | `agent_app/integrations/` |
| Evaluation | golden cases, regression suites | `evals/` |
| Deployment | CLI, API server, worker, local app | project-specific app layer |

## Integration Rules

Before adopting a third-party capability, answer:

1. Which scaffold boundary owns it?
2. Can the project replace it without changing business logic?
3. What data, credentials, or external effects does it touch?
4. What capability flags or config does it require?
5. What eval or contract test proves it works?

If these answers are unclear, keep the integration behind a small adapter first.

## Manifest

Record optional third-party capabilities in `config/integrations.yaml`.

Each entry should include:

- `kind`: `adapter`, `service`, `framework`, `mcp`, or `local`
- `package`: package, service, or project name when known
- `enabled`: whether this integration is active
- `boundary`: scaffold boundary it belongs to
- `risk`: `low`, `external`, `destructive`, `permission`, or `money`
- `capabilities`: what it provides
- `recommended_for`: presets or agent types where this is a good default
- `alternatives`: replacement packages, services, or custom approaches
- `scaffold_ownership`: boundaries the scaffold still owns even when this integration is used
- `config`: project-specific configuration
- `evals`: eval cases that protect the integration

## What Not To Do

- Do not import a full framework when one adapter function would be enough.
- Do not let an integration own the agent loop unless the project explicitly chooses a framework-backed runtime.
- Do not hide external calls behind low-risk tools.
- Do not add project-specific data source details to the shared skill.
- Do not promote a third-party solution as default until at least one real project validates it.
