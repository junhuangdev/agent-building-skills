from __future__ import annotations

from dataclasses import dataclass, field

from agent_app.types import Message


@dataclass
class SessionStore:
    messages: list[Message] = field(default_factory=list)

    def add(self, message: Message) -> None:
        self.messages.append(message)

    def history(self) -> list[Message]:
        return list(self.messages)
