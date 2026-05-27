# Agent Scaffold Skill Design

## Readable Summary

This project creates a focused Codex skill for designing, generating, and using lightweight multi-provider AI agent scaffolds.

## Recommended Approach

Build a skill package rather than a full agent platform. The skill should teach Codex the scaffold boundaries, provide a reusable starter template, and include a deterministic script for creating new agent projects.

## Scope

Included:

- Skill entrypoint for scaffold design and generation.
- Architecture references for agent modules.
- Provider adapter guidance for OpenAI, DeepSeek, Gemini, Claude, OpenRouter, LiteLLM, and local models.
- Capability matrix guidance.
- Python starter scaffold.
- Initialization script.
- Session handoff prompt.

Excluded for now:

- Full OpenClaw/Hermes-style platform.
- Plugin marketplace.
- Multi-channel gateway.
- Long-running scheduler.
- Production tracing backend.

## Design

The skill treats agent systems as a thin runtime plus explicit provider adapters. It avoids assuming that OpenAI Agents SDK, LangGraph, Pydantic AI, or any other SDK is universally portable.

The bundled scaffold keeps these boundaries separate:

- Agent loop
- Provider adapter
- Tool runtime
- Policy gates
- Memory/session state
- Config
- Capabilities
- Evals

## Acceptance

The project is ready for the next discussion when:

1. `SKILL.md` exists at the skill project root.
2. The scaffold template exists under `assets/scaffold-template/`.
3. `scripts/init_agent_project.py` can copy the template into a target directory.
4. The project includes a concise prompt and session context for a follow-up session.
