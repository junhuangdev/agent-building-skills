# Agent Scaffold Architecture

An agent scaffold should be small enough to understand and strict enough to prevent model/provider drift.

## MVP Modules

| Module | Purpose | MVP |
| --- | --- | --- |
| Agent loop | Owns the task cycle and final response | Yes |
| Provider adapters | Normalize model requests and responses | Yes |
| Tool runtime | Registers and executes tools | Yes |
| Stack catalog | Maps agent modules to recommended SDKs, libraries, presets, and ownership boundaries | Yes |
| Capability matrix | Declares provider-specific support | Yes |
| Policy gates | Controls risky or external actions | Yes |
| Config | Centralizes model and runtime settings | Yes |
| Integrations | Wraps optional third-party capabilities | Optional first, needed for assembly |
| Memory/state | Stores session and task state | Optional first, needed soon |
| Observability | Logs usage, errors, and traces | Optional first, needed soon |
| Evals | Protects behavior during provider changes | Optional first, recommended |
| Skills/plugins | Adds installable capability packages | Later |
| Schedulers/channels | Adds cron, Slack, Telegram, web UI | Later |

## Runtime Shape

```text
User or channel
  -> agent loop
    -> policy gates
  -> provider adapter
    -> integrations
    -> tool runtime
    -> memory/state
    -> final response
```

## Design Rules

- Keep provider-specific behavior out of the agent loop.
- Treat tool calling and structured output as capabilities, not assumptions.
- Put approval policy before external effects.
- Keep model IDs and base URLs in config.
- Keep third-party packages behind integration adapters.
- Add eval cases before changing provider behavior.
- Do not copy a full platform before the first agent proves the need.

## Minimum Acceptance

A generated scaffold is usable when it can:

1. Load model configuration from `config/models.yaml`.
2. Select one provider adapter.
3. Register at least one typed tool.
4. Run one agent loop without provider-specific code in the loop.
5. Block or surface approval for external/destructive actions.
6. Run at least one eval case.
7. Record optional third-party capabilities in `config/integrations.yaml` when used.
