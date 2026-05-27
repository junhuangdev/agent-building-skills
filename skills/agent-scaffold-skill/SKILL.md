---
name: agent-scaffold-skill
description: Use when designing, generating, or using a lightweight multi-provider AI agent scaffold with explicit provider adapters, tool runtime, policy gates, memory/state, evaluation hooks, and capability matrices for OpenAI, DeepSeek, Gemini, Claude, OpenRouter, LiteLLM, or local models.
---

# Agent Scaffold Skill

Use this skill to create, use, and improve agent project scaffolds that are model-provider aware.

This skill does not assume a universal agent SDK. It treats agent development as a small runtime plus provider adapters, tools, policy, state, and evaluation.

The skill is self-contained. All runtime instructions, references, scripts, and starter assets needed by the skill live inside this directory. Do not depend on external project paths or prior session notes when using it.

## When To Use

- Create a new AI agent project scaffold.
- Compare whether to use OpenAI Agents SDK, LangGraph, Pydantic AI, LiteLLM, or a custom runtime.
- Add or review provider adapters for OpenAI, DeepSeek, Gemini, Claude, OpenRouter, LiteLLM, Ollama, vLLM, or LM Studio.
- Design tool calling, structured output, memory, approval gates, and evals for an agent.
- Audit whether an existing agent project has the right module boundaries.

## Workflow

1. Identify the target product shape:
   - CLI agent
   - local desktop helper
   - server API
   - workflow automation
   - ChatGPT app / MCP server
   - multi-agent platform
2. Choose the runtime style:
   - `thin-runtime`: custom loop, explicit provider adapters, minimal dependencies.
   - `framework-backed`: LangGraph, Pydantic AI, LlamaIndex, Vercel AI SDK, or OpenAI Agents SDK.
   - `gateway-backed`: LiteLLM or OpenRouter for provider routing.
3. Select a stack preset from `references/stack-catalog.md` when SDK/library choices matter.
4. Define the provider matrix before writing model-specific code.
5. Generate or adapt the scaffold template.
6. Add only the capabilities the first agent needs.
7. Add eval cases for provider switching and tool execution.
8. While building the real agent, record friction and reusable lessons.
9. Promote only reusable scaffold lessons back into this skill.

## Usage Loop

Use this loop when the user wants to build a real agent, not only discuss architecture:

```text
thin scaffold
  -> real agent implementation
  -> friction harvest
  -> reusable scaffold update
  -> eval-backed verification
```

Keep project-specific prompts, data sources, and business rules in the generated agent project. Promote lessons into this skill only when they affect scaffold structure, runtime behavior, provider adapters, tool design, memory, approval gates, or evals.

## Daily Use

For the most foolproof local setup, install this self-contained skill into the Codex skill directory as a symlink:

```bash
python scripts/install_local_skill.py
```

For end-user-style global updates, sync from GitHub instead of the working tree:

```bash
python scripts/sync_global_skill.py
```

After installation or sync, the user can ask naturally for a DeepSeek-first agent, a multi-provider agent scaffold, provider adapter work, tool approval gates, memory design, or eval setup. The generated agent project carries its own `AGENTS.md` harvest reminder, so future work in that project can record reusable scaffold lessons without repeating setup prompts.

For an existing agent project, install project-local support from this skill directory:

```bash
python scripts/install_project_support.py /path/to/existing-agent-project
```

This does not register the project in this skill. The project declares its dependency by receiving its own `AGENTS.md` block, harvest log, and harvest report script.

## Required Boundaries

Every scaffold should keep these concerns separate:

| Boundary | Responsibility |
| --- | --- |
| Agent loop | Plan, call model, dispatch tools, produce final answer |
| Provider adapter | Normalize model requests, streaming, tool calls, structured output |
| Tool runtime | Register tools, validate input, execute, return typed results |
| Policy | Human approval, risk classes, external actions, destructive actions |
| Memory/state | Session state, task state, user/project preferences |
| Config | Model IDs, API keys, base URLs, enabled tools, runtime flags |
| Observability | Logs, trace IDs, token usage, cost, errors |
| Evaluation | Regression cases, provider comparison, tool success checks |

## Reference Loading

Load only the files needed for the task:

- `references/architecture.md`: use for module boundaries and MVP scope.
- `references/provider-adapters.md`: use for OpenAI, DeepSeek, Gemini, Claude, OpenRouter, LiteLLM, and local model integration.
- `references/capabilities.md`: use when comparing model/provider features.
- `references/capability-integration.md`: use when choosing, wrapping, or evaluating third-party agent capabilities.
- `references/stack-catalog.md`: use when mapping agent modules to recommended SDKs, libraries, presets, and scaffold ownership.
- `references/open-source-agent-survey.md`: use when learning from well-known open-source agents and deciding what to build, wrap, or avoid copying.
- `references/good-agent-principles.md`: use when designing, reviewing, or improving agent behavior quality.
- `references/scaffold-usage.md`: use when creating a new project from the bundled template.
- `references/harvest-loop.md`: use when deciding whether lessons from a real agent should update this skill.

## Template

The bundled starter lives at `assets/scaffold-template/`.

Use `scripts/init_agent_project.py` to copy it into a target project:

```bash
python scripts/init_agent_project.py /path/to/new-agent --name my-agent
```

After generation, inspect `config/models.yaml` and `config/capabilities.yaml` before running the agent.
Inspect `config/integrations.yaml` to see which SDKs, libraries, presets, alternatives, and scaffold-owned boundaries were selected.

Validate this skill package from the skill directory with:

```bash
python scripts/validate_skill_package.py .
```

## Default Recommendation

For DeepSeek-first or multi-provider agents, start with `thin-runtime`:

```text
agent runtime
  + provider adapters
  + tool registry
  + policy gates
  + capability matrix
  + eval cases
```

Use OpenAI Agents SDK only when the project is OpenAI-first or needs OpenAI-native hosted tools, tracing, or ChatGPT app alignment.

For non-core capabilities, prefer assembly over hand-rolled implementations: choose mature third-party packages or services only when they can be wrapped behind provider/tool/memory/policy/integration boundaries and protected by evals.

For OpenAI-compatible providers like DeepSeek and Kimi, default to the OpenAI SDK as the model client inside the provider adapter, not as the agent architecture boundary.
