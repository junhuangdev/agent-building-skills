from __future__ import annotations

import os
import json
from collections.abc import Sequence
from typing import Any

import httpx

from agent_app.config import ProviderConfig
from agent_app.providers.base import ModelProvider
from agent_app.types import Message, ModelResult, ToolCall, ToolSpec


class OpenAICompatibleProvider(ModelProvider):
    def __init__(self, name: str, config: ProviderConfig, capabilities: dict[str, Any]) -> None:
        self.name = name
        self.config = config
        self.capabilities = capabilities

    def supports(self, capability: str) -> bool | str:
        return self.capabilities.get(capability, False)

    async def complete(
        self,
        messages: Sequence[Message],
        tools: Sequence[ToolSpec] | None = None,
        response_format: dict[str, Any] | None = None,
        settings: dict[str, Any] | None = None,
    ) -> ModelResult:
        api_key = os.environ.get(self.config.api_key_env)
        if not api_key:
            raise RuntimeError(f"Missing API key env var: {self.config.api_key_env}")

        payload: dict[str, Any] = {
            "model": self.config.model,
            "messages": [message.__dict__ for message in messages],
        }
        if tools:
            payload["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    },
                }
                for tool in tools
            ]
        if response_format:
            payload["response_format"] = response_format
        if settings:
            payload.update(settings)

        endpoint = self.config.base_url.rstrip("/") + "/chat/completions"
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                endpoint,
                headers={"Authorization": f"Bearer {api_key}"},
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        choice = data["choices"][0]["message"]
        tool_calls: list[ToolCall] = []
        for item in choice.get("tool_calls", []) or []:
            raw_arguments = item["function"].get("arguments", {})
            if isinstance(raw_arguments, str):
                raw_arguments = json.loads(raw_arguments or "{}")
            tool_calls.append(
                ToolCall(
                    id=item.get("id", ""),
                    name=item["function"]["name"],
                    arguments=raw_arguments,
                )
            )
        return ModelResult(
            content=choice.get("content") or "",
            tool_calls=tool_calls,
            usage=data.get("usage", {}),
            raw=data,
        )
