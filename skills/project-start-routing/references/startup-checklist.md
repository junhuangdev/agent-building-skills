# Startup Checklist

Use this template in the project README, AGENTS file, design note, or delivery summary when the stack was not already fixed.

```markdown
## Project Start Decision

- Project type:
- Existing local rule:
- Selected lane:
- Rejected alternatives:
- Design System adoption:
- Design System reason:
- Design System reopen path:
- Runtime/package manager:
- Install:
- Start:
- Test:
- External services/tools:
- Environment boundary:
- Escalation:
```

Use exactly one Design System adoption value:

- `jun-ui adoption decision: adopted`
- `jun-ui adoption decision: deferred`
- `jun-ui adoption decision: not-suitable`

When the decision is `deferred` or `not-suitable`, fill `Design System reason` and `Design System reopen path`. The reopen path should say when to ask Jun again and how to switch to `adopted`.

## Escalation Triggers

Ask the user before continuing when:

- two lanes are equally valid and the wrong choice would add long-term maintenance cost
- a project has a UI surface and the Design System adoption decision has not been made
- the project would require a new global runtime, daemon, database, or paid external service
- the project needs a hybrid stack but no clear process boundary exists
- local instructions conflict with the user's current request
