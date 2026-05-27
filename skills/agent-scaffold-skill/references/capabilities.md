# Capability Matrix

Use a capability matrix because model providers do not expose the same behavior.

## Required Capability Groups

| Group | Examples | Why It Matters |
| --- | --- | --- |
| Text | chat, instruction following | Base agent behavior |
| Tools | tool calls, parallel calls | Action execution |
| Structure | JSON object, JSON schema | Reliable machine-readable output |
| Streaming | token stream, event stream | UI and long tasks |
| Reasoning | thinking, effort, traces | Planning and cost controls |
| Multimodal | image, audio, file | Input/output scope |
| Hosted tools | web/file search | Provider-native features |
| Limits | context, output tokens | Planning and chunking |
| Operations | retries, rate limits, usage | Reliability and cost |

## Policy

When a capability is unknown, mark it as `false` or `experimental`.

Do not silently emulate a feature in the adapter without documenting the behavior. Emulation can be useful, but it changes reliability and test coverage requirements.
