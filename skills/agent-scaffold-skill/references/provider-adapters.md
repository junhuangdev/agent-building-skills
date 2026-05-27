# Provider Adapter Guidance

Provider adapters isolate model-specific behavior from the agent runtime.

## Adapter Contract

Each adapter should expose the same core methods:

```text
complete(messages, tools, response_format, settings) -> ModelResult
stream(messages, tools, response_format, settings) -> events
supports(capability) -> bool
```

## Provider Families

| Family | Examples | Notes |
| --- | --- | --- |
| OpenAI-native | OpenAI Responses / Chat Completions | Best for OpenAI-first agents |
| OpenAI-compatible | DeepSeek, Gemini compatibility, local vLLM | Good for quick provider switching |
| Native vendor SDK | Claude, Gemini, Bedrock, Vertex | Better when provider-specific features matter |
| Gateway | LiteLLM, OpenRouter | Useful for routing and fallback |
| Local | Ollama, vLLM, LM Studio | Useful for privacy and cost control |

## DeepSeek-first Recommendation

For DeepSeek-first projects, start with an OpenAI-compatible adapter and keep DeepSeek settings explicit:

- `base_url`
- `api_key_env`
- `model`
- `supports_tool_calls`
- `supports_json_object`
- `supports_json_schema`
- `supports_reasoning`
- `reasoning_param`

## Gemini / Claude Recommendation

Use OpenAI-compatible APIs only for quick experiments.

For production behavior, prefer native adapters when the project depends on:

- strict tool calling
- multimodal inputs
- structured output guarantees
- vendor-specific reasoning controls
- accurate usage accounting

## Capability Flags

Provider adapters should not guess. Read flags from `config/capabilities.yaml` and validate at runtime.

Important flags:

- `tool_calling`
- `parallel_tool_calls`
- `json_object`
- `json_schema`
- `streaming`
- `vision`
- `audio`
- `file_input`
- `reasoning`
- `hosted_web_search`
- `hosted_file_search`
