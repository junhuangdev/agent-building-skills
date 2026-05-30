# Promotion Contract

## Conclusion

Promotion is the act of turning experience into durable behavior such as a Skill, rule, template, eval, project process, Agent behavior, or runtime change. AI may recommend promotion, but shared-layer promotion needs human approval.

## Promotion Targets

| Target | Use when |
| --- | --- |
| Project memory | Business facts, domain rules, project-local preference |
| User memory | Durable personal preference across projects |
| Agent package | Agent-specific method, business rule, eval, or tool behavior |
| Eval template | A test shape catches a reusable failure mode |
| Skill | A procedure should guide future AI behavior |
| Project rule | A local workflow or boundary should become default |
| Runtime/tooling | Execution mechanics need deterministic support |
| Reference only | Useful knowledge without rule status |

## Evidence Thresholds

| Evidence | Default state |
| --- | --- |
| One weak observation | `watch` |
| One low-risk success | `watch` |
| Repeated similar failures | `promote` candidate |
| One serious safety/trust failure | `promote` candidate |
| Eval catches real regression | strong `promote` candidate |
| User states durable preference | scoped promotion candidate |
| Skill self-eval proves a repeated defect | owning-skill promotion candidate |

## Approval Package

Every shared promotion package must include:

```text
Recommendation: What should change?
Evidence: Which trace, feedback, eval, or repeated pattern supports it?
Impact: What future tasks improve?
Risk if changed: What could become worse?
Risk if not changed: What failure may repeat?
Target: Which Skill, rule, template, eval, project, or runtime should change?
Decision needed: accept / revise / defer / reject
```

## Anti-Promotion Rules

- Do not promote private data, raw chat, credentials, or one-project facts into shared artifacts.
- Do not promote a business rubric as a universal rubric.
- Do not turn every useful memory into a Skill.
- Do not let AI approve its own shared-layer promotion.
- Do not let a Skill approve its own self-evolution package.
- Do not promote without a concrete future task effect.
