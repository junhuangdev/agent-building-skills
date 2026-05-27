# Session Context

## Background

We discussed whether the OpenAI Developers plugin removes the need for a custom AI agent scaffold.

Current conclusion:

- The OpenAI Developers plugin is useful for OpenAI-first development, official docs, API key setup, Agents SDK scaffolding, and ChatGPT app work.
- It does not replace a DeepSeek-first or multi-provider agent scaffold.
- OpenAI Agents SDK can connect to non-OpenAI models through compatibility layers or custom providers, but its native path is still OpenAI-centered.
- There is no truly universal agent SDK. Frameworks such as LangGraph, Pydantic AI, LlamaIndex, Vercel AI SDK, Semantic Kernel, AutoGen, LiteLLM, MCP, and A2A cover different layers.

## Direction

Analyze agent products such as OpenClaw and Hermes, then extract reusable module boundaries:

- Agent loop
- Provider adapters
- Tool runtime
- Capability matrix
- Memory/state
- Policy and approval gates
- Config
- Observability
- Skills/plugins
- Evaluation

The selected project name is `agent-scaffold-skill` because it is more direct and more focused than `agent-kernel-skill`.

## Project Goal

Create a skill project under:

the skill project root

The project should become a reusable skill and template package for:

- Designing new agent projects.
- Generating lightweight agent scaffolds.
- Keeping provider adapters explicit.
- Supporting DeepSeek, OpenAI, Gemini, Claude, OpenRouter, LiteLLM, and local models.
- Accumulating practical principles for building good agents.
- Avoiding premature platform complexity.

## Current Recommendation

Use a thin runtime first:

```text
agent runtime
  + provider adapters
  + tool registry
  + policy gates
  + capability matrix
  + eval cases
```

Do not build a full platform until a concrete agent demo proves the need.

## Added Direction

The skill should accumulate principles for building good agents, but only where those principles affect scaffold structure, runtime behavior, provider adaptation, tool design, memory, approval gates, or evals.

It should not become a broad agent philosophy or research digest.
