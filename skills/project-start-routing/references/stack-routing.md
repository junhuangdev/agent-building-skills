# Stack Routing

Choose the narrowest lane that can carry the project without creating avoidable environment drift.

## Priority Order

1. User instruction for this task.
2. Nearest `AGENTS.md`, spec, README, or existing project structure.
3. Existing package manager, runtime, test framework, and deploy path.
4. The routing table below.

## Lanes

| Lane | Use when | Default shape | Avoid when |
| --- | --- | --- | --- |
| TS App | Product UI, browser-heavy app, Electron app, workbench, frontend prototype that will grow, or full-stack TypeScript service. | TypeScript, npm, Vite or Next.js, Vitest or Playwright as needed. | The core value is Python-only tooling, data processing, or backend automation. |
| Python Engine | Agent core, automation, CLI, data pipeline, ML/AI integration, backend process, or integration with Python-first libraries. | Python, uv when available, unittest or pytest, Typer or FastAPI only when useful. | The main surface is a rich browser UI and Python is only incidental. |
| No-build Tool | Static local dashboard, one-page report, small utility UI, quick internal workbench, or HTML-first prototype. | HTML, CSS, vanilla JavaScript, existing local static UI kit when available. | State, routing, build-time composition, or shared frontend components are central. |
| Hybrid | TS frontend and Python backend are both central, and each side has a strong reason to exist. | TS app plus Python service with explicit boundary, one start command, and separate tests. | The split exists only from habit or because the agent is undecided. |

## Defaults

- Prefer No-build Tool over TS App when the page can stay static and local.
- Prefer TS App for interactive product UI, repeated UI components, or browser-native workflows.
- Prefer Python Engine for agent runtime, automation, data, ML, scripts, and Python-first upstream ecosystems.
- Prefer Hybrid only when the UI and Python engine would both be worse if forced into one language.
- For any lane with product UI, browser UI, local dashboard, workbench, settings screen, detail page, or HTML-first prototype, run the Design System adoption gate for `jun-ui-design-system` before implementation. The gate asks Jun whether to use the Design System; it does not force adoption by default.

## Required Decision Fields

Every unfixed project start must state:

- project type
- selected lane
- rejected alternatives
- Design System adoption
- Design System reason
- Design System reopen path
- runtime and package manager
- install command
- start command
- test command
- external services or tools
- environment boundary and why the choice will not increase global drift

## Management Rules

- Do not introduce pnpm, yarn, uv, Poetry, Bun, Docker, or a database unless the project already uses it or the need is explicit.
- Pin or document the runtime when reproducibility matters.
- Keep generated runtime installs, symlinks, and global configuration separate from canonical source files.
- Keep Python-heavy upstream dependencies isolated in the project environment.
- Keep TypeScript apps on one package manager per repo.
- Do not create or switch git worktrees unless the user approves that isolation.
- If the agent chooses a non-default lane, include the tradeoff in one sentence.
