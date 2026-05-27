from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IntegrationAdapter(ABC):
    """Boundary for optional third-party capability adapters."""

    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def capabilities(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    async def run(self, operation: str, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
