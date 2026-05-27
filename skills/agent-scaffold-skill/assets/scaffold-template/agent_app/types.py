from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


Role = Literal["system", "user", "assistant", "tool"]


@dataclass(frozen=True)
class Message:
    role: Role
    content: str
    name: str | None = None


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    parameters: dict[str, Any]


@dataclass(frozen=True)
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class ModelResult:
    content: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    usage: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)
