from __future__ import annotations

from agent_app.config import ModelsConfig
from agent_app.providers.base import ModelProvider
from agent_app.providers.openai_compatible import OpenAICompatibleProvider


def build_provider(
    models: ModelsConfig,
    capabilities: dict,
    provider_name: str | None = None,
) -> ModelProvider:
    name = provider_name or models.default_provider
    config = models.providers[name]
    provider_capabilities = capabilities.get("providers", {}).get(name, {})

    if config.kind == "openai_compatible":
        return OpenAICompatibleProvider(name, config, provider_capabilities)

    raise ValueError(f"Unsupported provider kind: {config.kind}")
