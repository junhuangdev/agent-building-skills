# Open Source Agent Survey

Use this reference when comparing well-known open-source agents to decide what the scaffold should build, wrap, or avoid copying.

The goal is not to rank products. The goal is to learn how mature agents assemble capabilities across self-built runtime logic and external dependencies.

## Survey Rule

Use official repositories, official docs, and package manifests as sources. Treat blog posts, mirrors, social posts, and secondary summaries as context only.

## Capability Assembly Matrix

| Project | Product Shape | Self-built | external dependency | Scaffold harvest |
| --- | --- | --- | --- | --- |
| Hermes Agent | Long-lived personal agent across CLI and messaging channels | agent loop, toolsets, skills, memory loop, session search, cron, delegation, gateway | OpenAI SDK, optional Anthropic SDK, MCP, Docker/SSH/Singularity/Modal/Daytona/Vercel Sandbox, messaging SDKs | split core runtime from optional backends; lazy-load risky/provider-specific integrations |
| OpenClaw | Local-first personal assistant and gateway | gateway, sessions, channels, tools, skills, plugins, sandbox policy, multi-agent routing | model providers, Docker/SSH/OpenShell sandboxes, channel services, browser CDP, plugin ecosystem | expose tools through policy; keep channels and gateway outside domain agent business logic |
| OpenHands | Software-development agent platform and SDK | software agent SDK, code/workspace loop, task planning, context compression, security analysis | LiteLLM, OpenAI SDK, Docker/process/remote sandboxes, Playwright, MCP, OpenTelemetry, Redis/Postgres/Kubernetes integrations | code execution and workspace lifecycle are a mature reusable layer, but domain agents should not inherit coding-specific assumptions |
| Aider | Terminal pair-programming agent | coding loop, repo map, edit formats, git workflow, lint/test repair flow | LiteLLM, OpenAI SDK, tree-sitter language pack, GitPython, prompt-toolkit | repo context and git safety are specialized reusable patterns for coding agents, not generic agent-core defaults |

## Capability Findings

| Capability | Mature Shape | Common Pattern | Scaffold Decision |
| --- | --- | --- | --- |
| agent loop | message loop with tool rounds, interrupts, compaction, retry, final answer | self-built in serious products | keep thin shared agent-core loop unless a framework is explicitly selected |
| model provider | provider adapter or gateway with model config and fallback | OpenAI SDK, LiteLLM, provider SDKs, OpenRouter | wrap behind `agent_app/providers/` and capability matrix |
| tool system | typed tool registry with policy-filtered exposure | built-in tools plus plugin/MCP/toolset layers | scaffold owns registry, schema, risk metadata, and tool result shape |
| memory | session search, durable notes, skills, project context, checkpoints | often self-built over SQLite/DB/vector stores | scaffold defines memory buckets and write rules; storage is pluggable |
| browser | browser session controlled by tool API or CDP | Playwright/CDP/cloud browser services | use external browser control, but keep source logging and action policy |
| code execution | isolated shell/container/remote workspace | Docker, SSH, cloud sandbox, process mode | use sandbox integrations; scaffold owns approval and workspace access rules |
| workflow | cron, background tasks, sessions, subagents, state graph | built-in scheduler or external workflow runtime | use explicit integration; scaffold owns state contract and approval checkpoints |
| channels | CLI, web, Slack, Discord, Telegram, WhatsApp, IDE | product-specific gateway/channel adapters | keep out of default agent-core; add only in product shell |
| observability | trace, usage, logs, replay, trajectory export | OpenTelemetry, product logs, research exports | scaffold owns event schema and redaction; backend is replaceable |
| security | permission gates, sandbox policy, channel allowlists, command approvals | self-built policy with external sandboxing | scaffold owns risk classes and approval gate; never delegate final policy to a tool library |

## Project Notes

### Hermes Agent

Hermes is a strong example of a self-built runtime with optional external capability backends. Its official docs describe memory, skills, MCP, messaging, command approval, container isolation, scheduled automation, subagent delegation, and many terminal backends. Its package manifest shows a small core dependency set with provider-specific and backend-specific extras.

Useful scaffold lessons:

- Keep model/provider code replaceable.
- Keep optional capabilities in extras or integration records, not in the core runtime.
- Treat terminal/code execution as a backend choice: local, Docker, SSH, or cloud sandbox.
- Treat skills and memory as first-class reusable agent behavior, but keep business truth outside them.

Sources:

- [Hermes Agent docs](https://hermes-agent.nousresearch.com/docs/)
- [Hermes tools and toolsets](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools/)
- [Hermes pyproject](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/pyproject.toml)

### OpenClaw

OpenClaw is a strong example of a local-first assistant platform. Its official repository describes a gateway control plane for sessions, channels, tools, and events. Its docs distinguish tools, skills, plugins, channel permissions, provider restrictions, sandbox state, and policy filtering before tool schemas reach the model.

Useful scaffold lessons:

- Tool visibility should be policy-filtered before the model call.
- Channels and gateway surfaces should stay outside domain business logic.
- Skills are instruction packages, while plugins add runtime capability.
- Sandbox policy and elevated execution need separate controls.

Sources:

- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [OpenClaw capabilities overview](https://docs.openclaw.ai/tools)
- [OpenClaw sandboxing](https://docs.openclaw.ai/gateway/sandboxing)

### OpenHands

OpenHands is a strong example of a coding-agent runtime that extracted reusable agent SDK concepts. Its SDK docs describe agents, tools, workspaces, pre-defined tools, REST agent server, MCP, custom tools, persistence, action confirmation, metrics, and tracing. Its sandbox docs make Docker the recommended provider and distinguish process and remote providers.

Useful scaffold lessons:

- Code execution and workspace lifecycle are mature enough to integrate instead of rebuild.
- Sandbox provider should be explicit because safety and reproducibility change by provider.
- Coding-agent assumptions should not become generic domain-agent defaults.
- Observability and security analysis belong in the shared layer when actions affect files or systems.

Sources:

- [OpenHands Software Agent SDK](https://docs.openhands.dev/sdk/index)
- [OpenHands sandbox overview](https://docs.openhands.dev/openhands/usage/sandboxes/overview)
- [OpenHands Docker sandbox](https://docs.openhands.dev/openhands/usage/sandboxes/docker)
- [OpenHands pyproject](https://raw.githubusercontent.com/All-Hands-AI/OpenHands/main/pyproject.toml)

### Aider

Aider is a strong example of a narrow domain agent. It owns the coding loop, repo map, edit strategy, git workflow, lint/test integration, and user control model. It uses external dependencies for multi-provider model access, code parsing, git operations, and terminal UX.

Useful scaffold lessons:

- Domain-specific context engineering can be more valuable than a generic agent framework.
- Git safety is part of the coding-agent business layer, not generic agent-core.
- Tree-sitter-based code context is a mature reusable pattern for coding agents.
- Provider access can be delegated to LiteLLM while the agent owns edit semantics.

Sources:

- [Aider README](https://raw.githubusercontent.com/Aider-AI/aider/main/README.md)
- [Aider LLM docs](https://aider.chat/docs/llms.html)
- [Aider repository map](https://aider.chat/docs/repomap.html)
- [Aider git integration](https://aider.chat/docs/git.html)
- [Aider requirements](https://raw.githubusercontent.com/Aider-AI/aider/main/requirements.txt)

## Cross-project Lessons

1. Build the shared agent-core around boundaries, not around a specific third-party framework.
2. Reuse mature external capabilities behind adapters: provider gateways, MCP, browser automation, sandboxes, vector search, tracing, and eval backends.
3. Keep tool policy, approval gates, memory write rules, and eval pass criteria inside the scaffold or project shell.
4. Treat channels, product UI, and domain workflows as business agent shell concerns.
5. Promote a third-party dependency into the default stack only after a real generated agent validates the fit.

## Scaffold Harvest

Promote these items into `references/stack-catalog.md` or `config/integrations.yaml` when validated by a real agent project:

| Candidate | Why |
| --- | --- |
| `shared-agent-core` preset | Matches the cross-project pattern: self-built thin loop plus external integrations |
| `sandbox` integration category | Hermes, OpenClaw, and OpenHands all treat execution backend as a distinct concern |
| `channel` as product-shell category | OpenClaw and Hermes show channels are important but not core business logic |
| `tool_policy` metadata | OpenClaw shows tool visibility should be filtered before model exposure |
| `coding-agent` specialized preset | Aider and OpenHands show code agents need repo map, git safety, sandbox, and tests |
