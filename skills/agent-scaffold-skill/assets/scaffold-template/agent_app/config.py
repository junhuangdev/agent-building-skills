from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class ProviderConfig(BaseModel):
    kind: str
    base_url: str
    api_key_env: str
    model: str
    extra: dict[str, Any] = Field(default_factory=dict)


class ModelsConfig(BaseModel):
    default_provider: str
    providers: dict[str, ProviderConfig]


class IntegrationConfig(BaseModel):
    kind: str
    package: str | None = None
    enabled: bool = False
    boundary: str
    risk: str = "low"
    capabilities: list[str] = Field(default_factory=list)
    recommended_for: list[str] = Field(default_factory=list)
    alternatives: list[str] = Field(default_factory=list)
    scaffold_ownership: list[str] = Field(default_factory=list)
    config: dict[str, Any] = Field(default_factory=dict)
    evals: list[str] = Field(default_factory=list)


class IntegrationsConfig(BaseModel):
    integrations: dict[str, IntegrationConfig] = Field(default_factory=dict)


def load_models_config(path: str | Path = "config/models.yaml") -> ModelsConfig:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return ModelsConfig.model_validate(data)


def load_capabilities(path: str | Path = "config/capabilities.yaml") -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_integrations_config(path: str | Path = "config/integrations.yaml") -> IntegrationsConfig:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return IntegrationsConfig.model_validate(data or {})
