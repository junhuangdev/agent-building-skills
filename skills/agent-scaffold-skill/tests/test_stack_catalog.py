from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_skill_references_stack_catalog():
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    assert "`references/stack-catalog.md`" in skill_text


def test_stack_catalog_defines_presets_and_ownership():
    catalog = (ROOT / "references" / "stack-catalog.md").read_text(encoding="utf-8")

    assert "deepseek-basic" in catalog
    assert "multi-provider" in catalog
    assert "OpenAI SDK client" in catalog
    assert "scaffold ownership" in catalog.lower()


def test_skill_references_open_source_agent_survey():
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    assert "`references/open-source-agent-survey.md`" in skill_text


def test_open_source_agent_survey_covers_capability_assembly():
    survey = (ROOT / "references" / "open-source-agent-survey.md").read_text(
        encoding="utf-8"
    )

    for project in ["Hermes Agent", "OpenClaw", "OpenHands", "Aider"]:
        assert project in survey

    for capability in [
        "agent loop",
        "model provider",
        "tool system",
        "memory",
        "browser",
        "code execution",
        "workflow",
        "security",
    ]:
        assert capability in survey.lower()

    assert "self-built" in survey
    assert "external dependency" in survey
    assert "scaffold harvest" in survey.lower()
