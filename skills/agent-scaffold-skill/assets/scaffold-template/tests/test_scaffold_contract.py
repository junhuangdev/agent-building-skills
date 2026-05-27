import asyncio
import importlib.util
from pathlib import Path

from agent_app.config import ModelsConfig, IntegrationsConfig
from agent_app.agent.loop import AgentLoop
from agent_app.policy.approvals import check_tool_approval
from agent_app.providers.base import ModelProvider
from agent_app.tools.registry import ToolRegistry
from agent_app.types import Message, ModelResult, ToolCall, ToolSpec


ROOT = Path(__file__).resolve().parents[1]


class FakeProvider(ModelProvider):
    def __init__(self, results):
        self.results = list(results)
        self.calls = []

    async def complete(self, messages, tools=None, response_format=None, settings=None):
        self.calls.append(
            {
                "messages": list(messages),
                "tools": list(tools or []),
                "response_format": response_format,
                "settings": settings,
            }
        )
        return self.results.pop(0)

    def supports(self, capability: str):
        return True


def test_models_config_contract():
    config = ModelsConfig.model_validate(
        {
            "default_provider": "deepseek",
            "providers": {
                "deepseek": {
                    "kind": "openai_compatible",
                    "base_url": "https://api.deepseek.com",
                    "api_key_env": "DEEPSEEK_API_KEY",
                    "model": "deepseek-chat",
                }
            },
        }
    )
    assert config.providers["deepseek"].kind == "openai_compatible"


def test_tool_registry_rejects_duplicate_names():
    registry = ToolRegistry()
    spec = ToolSpec(name="echo", description="Echo input", parameters={"type": "object"})
    registry.register(spec, lambda **kwargs: kwargs)

    try:
        registry.register(spec, lambda **kwargs: kwargs)
    except ValueError as exc:
        assert "already registered" in str(exc)
    else:
        raise AssertionError("Expected duplicate tool registration to fail")


def test_high_risk_tool_requires_approval():
    decision = check_tool_approval("external", approved=False)
    assert decision.allowed is False


def test_agent_loop_executes_allowed_tool_and_returns_final_answer():
    provider = FakeProvider(
        [
            ModelResult(
                content="",
                tool_calls=[
                    ToolCall(id="call_1", name="echo", arguments={"text": "hello"})
                ],
            ),
            ModelResult(content="final: hello"),
        ]
    )
    registry = ToolRegistry()
    registry.register(
        ToolSpec(
            name="echo",
            description="Echo input",
            parameters={
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
            },
        ),
        lambda text: {"echo": text},
    )

    answer = asyncio.run(AgentLoop(provider=provider, tools=registry).run("say hello"))

    assert answer == "final: hello"
    assert len(provider.calls) == 2
    second_messages = provider.calls[1]["messages"]
    assert Message(role="tool", name="echo", content='{"echo": "hello"}') in second_messages


def test_template_includes_harvest_entrypoints():
    assert (ROOT / "AGENTS.md").exists()
    assert (ROOT / "docs" / "agent-scaffold-harvest.md").exists()
    assert (ROOT / "scripts" / "harvest_report.py").exists()

    instructions = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "agent-scaffold-harvest.md" in instructions
    assert "agent_app/providers/" in instructions
    assert "agent_app/integrations/" in instructions
    assert "config/integrations.yaml" in instructions


def test_harvest_report_finds_promotable_entries(tmp_path):
    module_path = ROOT / "scripts" / "harvest_report.py"
    spec = importlib.util.spec_from_file_location("harvest_report", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    harvest_path = tmp_path / "agent-scaffold-harvest.md"
    harvest_path.write_text(
        """# Agent Scaffold Harvest

## Entries

### H-0001 Provider mismatch
promote_to_skill: yes
boundary: provider
failure: DeepSeek returned a different tool-call shape.
lesson: Normalize tool call parsing in the provider adapter.
verification: Add provider adapter regression test.

### H-0002 Project prompt
promote_to_skill: no
boundary: prompt
failure: Project prompt was unclear.
lesson: Keep this in the project.
verification: Project eval only.
""",
        encoding="utf-8",
    )

    entries = module.parse_harvest(harvest_path)

    assert len(entries) == 1
    assert entries[0]["id"] == "H-0001"
    assert entries[0]["boundary"] == "provider"


def test_integrations_config_contract():
    config = IntegrationsConfig.model_validate(
        {
            "integrations": {
                "retrieval": {
                    "kind": "adapter",
                    "package": "example-retrieval",
                    "enabled": False,
                    "boundary": "retrieval",
                    "risk": "low",
                    "capabilities": ["document_loader", "vector_search"],
                    "recommended_for": ["rag-agent"],
                    "alternatives": ["langchain"],
                    "scaffold_ownership": ["data_boundary", "retrieval_eval"],
                    "config": {"index": "local-dev"},
                    "evals": ["retrieval-smoke"],
                }
            }
        }
    )

    retrieval = config.integrations["retrieval"]
    assert retrieval.kind == "adapter"
    assert retrieval.enabled is False
    assert retrieval.capabilities == ["document_loader", "vector_search"]
    assert retrieval.recommended_for == ["rag-agent"]
    assert retrieval.alternatives == ["langchain"]
    assert retrieval.scaffold_ownership == ["data_boundary", "retrieval_eval"]


def test_template_includes_capability_integration_files():
    assert (ROOT / "config" / "integrations.yaml").exists()
    assert (ROOT / "agent_app" / "integrations" / "__init__.py").exists()
    assert (ROOT / "agent_app" / "integrations" / "base.py").exists()


def test_template_records_default_stack_recommendations():
    config = IntegrationsConfig.model_validate(
        __import__("yaml").safe_load((ROOT / "config" / "integrations.yaml").read_text())
    )

    model_client = config.integrations["model_client"]
    assert model_client.package == "openai"
    assert "deepseek-basic" in model_client.recommended_for
    assert "provider_adapter" in model_client.scaffold_ownership

    agent_runtime = config.integrations["agent_runtime"]
    assert agent_runtime.package == "thin-runtime"
    assert "langgraph" in agent_runtime.alternatives
    assert "agent_loop" in agent_runtime.scaffold_ownership
