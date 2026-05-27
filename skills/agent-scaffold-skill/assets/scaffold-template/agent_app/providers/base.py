from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from agent_app.types import Message, ModelResult, ToolSpec


class ModelProvider(ABC):
    @abstractmethod
    async def complete(
        self,
        messages: Sequence[Message],
        tools: Sequence[ToolSpec] | None = None,
        response_format: dict[str, Any] | None = None,
        settings: dict[str, Any] | None = None,
    ) -> ModelResult:
        raise NotImplementedError

    @abstractmethod
    def supports(self, capability: str) -> bool | str:
        raise NotImplementedError
