# Agent Stack Catalog

Use this reference when choosing the default stack for a generated agent project.

The scaffold should behave like an application starter: it names the modules an agent needs, recommends SDKs or libraries for each module, and keeps replacement boundaries explicit.

## Principle

Use SDKs and frameworks to reduce implementation risk, but keep scaffold ownership over the agent boundaries that affect portability, safety, memory, and evaluation.

```text
agent capability
  -> recommended SDK or library
  -> scaffold boundary
  -> eval or contract test
```

## Stack Layers

| Layer | Default | Good Fits | Scaffold Ownership |
| --- | --- | --- | --- |
| Model client | OpenAI SDK client | DeepSeek, Kimi, OpenAI-compatible APIs | provider adapter, retries, usage |
| Native provider SDK | Provider-specific SDK | Anthropic, Gemini, DashScope | adapter contract, capability matrix |
| Agent runtime | thin-runtime | DeepSeek-first, Kimi-first, multi-provider | loop, stop conditions, tool rounds |
| Workflow runtime | LangGraph | explicit graphs, checkpoints, multi-step flows | state contract, approval checkpoints |
| OpenAI-native runtime | OpenAI Agents SDK | OpenAI-first hosted tools, tracing, sandbox | project must accept OpenAI runtime coupling |
| Qwen-native runtime | Qwen-Agent | Qwen-heavy agents, code interpreter, MCP, RAG | adapter boundary, evals, exit path |
| Tool schema | Pydantic / JSON Schema | Python tools, strict input validation | registry, risk metadata, error shape |
| Tool protocol | MCP SDK | external reusable tools | approval policy, tool allowlist |
| Retrieval / RAG | LlamaIndex | document ingestion, indexes, RAG pipelines | data boundary, citations, retrieval evals |
| Provider routing | LiteLLM / OpenRouter | many providers, fallback, cost routing | capability flags, provider-specific tests |
| Observability | OpenTelemetry-compatible events | logs, traces, cost monitoring | event model, trace ids, redaction |
| Evals | pytest + golden cases | scaffold contracts, provider switching | acceptance gates, regression cases |

## Presets

| Preset | Use When | Default Stack |
| --- | --- | --- |
| `deepseek-basic` | DeepSeek-first agent with ordinary tools | thin-runtime, OpenAI SDK client, OpenAI-compatible adapter, scaffold tools |
| `kimi-basic` | Kimi-first agent with ordinary tools | thin-runtime, OpenAI SDK client, OpenAI-compatible adapter, Kimi-specific config |
| `multi-provider` | Provider switching matters | thin-runtime, provider matrix, OpenAI-compatible adapters, optional LiteLLM/OpenRouter |
| `rag-agent` | Documents or knowledge base matter | thin-runtime, retrieval adapter, LlamaIndex candidate, citation evals |
| `workflow-agent` | The process needs explicit states | LangGraph candidate behind integration boundary |
| `qwen-agentic` | Qwen-native tools matter | DashScope or Qwen-Agent candidate, explicit exit path |
| `openai-native` | OpenAI hosted tools, tracing, sandbox, or ChatGPT alignment matter | OpenAI Agents SDK |

## Selection Rules

1. Start with `thin-runtime` unless the project already needs graph state, hosted tools, or provider-native agent services.
2. Use OpenAI SDK client by default for DeepSeek, Kimi, and other OpenAI-compatible APIs.
3. Use native vendor SDKs when provider-specific features are central to the product.
4. Put every third-party package behind `agent_app/providers/`, `agent_app/integrations/`, or `agent_app/tools/`.
5. Record optional choices in `config/integrations.yaml` with `recommended_for`, `alternatives`, and `scaffold_ownership`.
6. Add evals or contract tests before treating an integration as stable.

Use `open-source-agent-survey.md` before promoting a new default dependency based on another agent project. Compare what that project builds itself, what it wraps, and what remains product-specific.

## Module Guidance

| Module | Recommended Package Class | Build In Scaffold |
| --- | --- | --- |
| Provider adapter | OpenAI SDK, Anthropic SDK, DashScope, Gemini SDK | normalized request/result, `supports()` |
| Agent loop | thin-runtime first; LangGraph when needed | tool loop, retry boundary, stop condition |
| Tool runtime | Pydantic, JSON Schema, MCP SDK | registry, execution, risk metadata |
| Policy gates | local policy module; guardrail libraries optional | approval rules, audit fields |
| Memory/state | SQLite/files first; Redis/Postgres/checkpoint libs later | memory buckets, lifecycle, export shape |
| RAG | LlamaIndex or similar | source boundary, citations, eval cases |
| Web/browser | search APIs, Playwright, browser MCP | source logs, external action controls |
| Observability | OpenTelemetry, LangSmith, Helicone, provider traces | common event schema, redaction |
| Evaluation | pytest, DeepEval, Ragas, provider eval APIs | golden cases, pass/fail gates |

## Default Interpretation

For OpenAI-compatible providers:

```text
OpenAI SDK client
  = model API transport inside the provider adapter

thin-runtime
  = default scaffold-owned agent runtime

OpenAI Agents SDK
  = optional framework-backed mode for OpenAI-native projects
```

This keeps model calls simple while avoiding provider lock-in at the agent architecture layer.
