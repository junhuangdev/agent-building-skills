from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from agent_app.types import ToolSpec


ToolHandler = Callable[..., Any]


@dataclass(frozen=True)
class RegisteredTool:
    spec: ToolSpec
    handler: ToolHandler
    risk: str = "low"


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, RegisteredTool] = {}

    def register(self, spec: ToolSpec, handler: ToolHandler, risk: str = "low") -> None:
        if spec.name in self._tools:
            raise ValueError(f"Tool already registered: {spec.name}")
        self._tools[spec.name] = RegisteredTool(spec=spec, handler=handler, risk=risk)

    def specs(self) -> list[ToolSpec]:
        return [tool.spec for tool in self._tools.values()]

    def get(self, name: str) -> RegisteredTool:
        return self._tools[name]
