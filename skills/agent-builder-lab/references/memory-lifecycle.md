# Memory Lifecycle

Agent-builder memory should make future agent work better. It should not become a permanent pile of untested ideas.

## States

| Status | Meaning | Next Action |
| --- | --- | --- |
| `active` | Proven and currently useful | Reuse in the next similar build |
| `watch` | Plausible but under-evidenced | Revisit after more runs |
| `promote` | Evidence supports durable change | Prepare approval package |
| `archive` | No longer useful or too local | Keep only as history |
| `rejected` | Wrong or harmful | Do not reuse without new evidence |
| `superseded` | Replaced by a better rule | Link to replacement |

## Evaluation Questions

For each journal entry, ask:

1. Which future agent-building decision will this change?
2. What evidence supports it?
3. Is the lesson local to one product, or reusable across agents?
4. What is the cost of keeping it active?
5. What failure happens if the lesson is forgotten?

If the answer to question 1 is vague, archive or reject the entry.

## Forgetting Rules

Archive or reject a memory when:

- It has no future task effect.
- It only describes project-specific content.
- It was not reused after several relevant opportunities.
- New evidence contradicts it.
- It creates more routing or process burden than quality improvement.

## Promotion Thresholds

Use evidence, not excitement.

| Evidence | Promotion Strength |
| --- | --- |
| One low-impact observation | `watch` |
| One serious safety, trust, or risk failure | `promote` candidate |
| Three similar failures or repeated repairs | `promote` candidate |
| A passing eval catches a real regression | strong `promote` candidate |
| User explicitly states a durable preference | promote to the right layer |

Absorption into another skill, runtime, project rule, or template requires approval.
