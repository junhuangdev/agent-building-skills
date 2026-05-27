from __future__ import annotations

import inspect
import json
from typing import Any

from agent_app.memory.session_store import SessionStore
from agent_app.policy.approvals import check_tool_approval
from agent_app.providers.base import ModelProvider
from agent_app.tools.registry import ToolRegistry
from agent_app.types import Message


class AgentLoop:
    def __init__(
        self,
        provider: ModelProvider,
        tools: ToolRegistry,
        session: SessionStore | None = None,
        max_tool_rounds: int = 4,
    ) -> None:
        self.provider = provider
        self.tools = tools
        self.session = session or SessionStore()
        self.max_tool_rounds = max_tool_rounds

    async def run(self, user_input: str) -> str:
        self.session.add(Message(role="user", content=user_input))

        for _ in range(self.max_tool_rounds + 1):
            result = await self.provider.complete(
                messages=self.session.history(),
                tools=self.tools.specs(),
            )
            if not result.tool_calls:
                self.session.add(Message(role="assistant", content=result.content))
                return result.content

            for call in result.tool_calls:
                registered = self.tools.get(call.name)
                decision = check_tool_approval(registered.risk)
                if not decision.allowed:
                    return decision.reason
                tool_result = registered.handler(**call.arguments)
                if inspect.isawaitable(tool_result):
                    tool_result = await tool_result
                self.session.add(
                    Message(
                        role="tool",
                        name=call.name,
                        content=_stringify_tool_result(tool_result),
                    )
                )

        return "Stopped after reaching the tool-call round limit."


def _stringify_tool_result(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)
