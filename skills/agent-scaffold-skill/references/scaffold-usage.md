# Scaffold Usage

Use the bundled template when the user wants a new agent project, not just architectural advice.

## Generate

From this skill directory:

```bash
python scripts/init_agent_project.py /path/to/new-agent --name my-agent
```

For local Codex discovery, install the skill once:

```bash
python scripts/install_local_skill.py
```

This creates a symlink in the local Codex skills directory, so future prompts can be natural language instead of path-based.

For a terminal-user-style update, sync the global install from GitHub:

```bash
python scripts/sync_global_skill.py
```

Use this when validating the public repository path. It replaces a local symlink install with a normal git checkout under the global Codex skills directory.

## Existing Project Adoption

For an existing agent project, install support into that project explicitly:

```bash
python scripts/install_project_support.py /path/to/existing-agent-project
```

This is project-local adoption:

- The existing project receives or updates its own `AGENTS.md`.
- The project receives `docs/agent-scaffold-harvest.md`.
- The project receives `scripts/harvest_report.py`.
- This skill does not keep a project registry or scan for projects.

After adoption, future work inside that project can trigger harvest checks through the project's own instructions.

## After Generation

1. Choose the closest preset from `references/stack-catalog.md`.
2. Edit `config/models.yaml`.
3. Edit `config/capabilities.yaml`.
4. Edit `config/integrations.yaml` to keep or replace the recommended SDKs/libraries.
5. Add provider API keys to the environment.
6. Add project-specific tools under `agent_app/tools/`.
7. Add eval cases under `evals/cases.yaml`.
8. Run the scaffold tests.

## Real Agent Build Loop

Use the scaffold as the first runnable slice of a real agent:

1. Generate the project.
2. Keep the first runtime thin: one provider, one safe tool, one approval-gated tool, and one eval.
3. Build the first real vertical slice.
4. Let the generated `AGENTS.md` remind future Codex sessions to check scaffold friction after relevant changes.
5. Record reusable friction in `docs/agent-scaffold-harvest.md`.
6. Run `python scripts/harvest_report.py` to list entries marked `promote_to_skill: yes`.
7. Promote only reusable lessons using `references/harvest-loop.md`.

Do not customize the scaffold by embedding one project's prompts, data contracts, or business rules into the shared template.

## Trigger Model

The scaffold does not run a background daemon. It uses project-local instructions and a harvest log:

| Trigger | Behavior |
| --- | --- |
| Normal agent work in generated project | `AGENTS.md` asks Codex to check harvest-worthy changes |
| Explicit harvest review | Run `python scripts/harvest_report.py` |
| Shared skill update | Human confirms which promotable lessons should update `agent-scaffold-skill` |

This keeps daily use simple while preventing project-specific business knowledge from leaking into the shared scaffold.

## First Provider Choice

Use this decision rule:

| Goal | Provider path |
| --- | --- |
| DeepSeek-first | OpenAI-compatible adapter first |
| OpenAI-first | OpenAI-native or OpenAI-compatible adapter |
| Gemini experiment | Gemini OpenAI-compatible adapter |
| Gemini production | Native Gemini adapter |
| Claude experiment | Claude compatibility or gateway |
| Claude production | Native Claude adapter |
| Many providers | LiteLLM/OpenRouter plus explicit capability matrix |

## First Stack Choice

Use the stack catalog before adding dependencies:

| Goal | Preset |
| --- | --- |
| DeepSeek-first basic agent | `deepseek-basic` |
| Kimi-first basic agent | `kimi-basic` |
| Provider switching | `multi-provider` |
| Documents or knowledge base | `rag-agent` |
| Explicit workflow graph | `workflow-agent` |
| Qwen-native tools | `qwen-agentic` |
| OpenAI hosted agent services | `openai-native` |
