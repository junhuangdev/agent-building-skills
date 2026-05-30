# Memory Lifecycle

## Conclusion

Memory items are not permanent notes. They are evolution artifacts with scope, evidence, future use, use history, and a lifecycle state.

## Required Fields

| Field | Purpose |
| --- | --- |
| `id` | Stable identifier |
| `evolution_target` | What kind of capability or knowledge should change |
| `storage_sink` | Which owner should store and maintain this item |
| `scope` | `project`, `user`, `shared_candidate`, or `runtime` |
| `status` | Lifecycle state |
| `source` | Why the item exists |
| `context` | Task or situation that produced it |
| `content` | The reusable lesson |
| `future_use` | When future AI should use it |
| `use_history` | Evidence from actual reuse |
| `last_use_result` | Most recent reuse result |
| `evidence` | Trace, feedback, eval, or repeated pattern |
| `counterexamples` | Where it must not apply |
| `risk` | Failure caused by misuse |
| `last_confirmed` | Freshness anchor |
| `review_trigger` | When to re-check it |

## States

| Status | Meaning | AI action |
| --- | --- | --- |
| `watch` | Plausible but under-evidenced | Revisit after more evidence |
| `active` | Proven and currently useful | Retrieve for matching tasks and record use result |
| `promote` | Evidence supports a durable change | Prepare approval package |
| `archive` | No future task effect or too local | Keep only as history |
| `rejected` | Wrong or harmful | Do not reuse without new evidence |
| `superseded` | Replaced by a better item | Link to replacement |

## Scope Rules

| Scope | Use when | Promotion rule |
| --- | --- | --- |
| `project` | Business facts, project preferences, domain rules | Keep local unless cross-project evidence exists |
| `user` | Durable personal preference across projects | Confirm durable preference |
| `shared_candidate` | Method likely useful across agents/projects | Requires promotion package |
| `runtime` | Host execution behavior | Do not write unless runtime owner approves |

`scope` controls reuse authority. `storage_sink` controls ownership and location. Do not use one field to mean both.

See `references/storage-routing.md` for target and sink values.

## Write Gate

Write memory only if all answers are concrete:

1. Which future task changes?
2. What evidence supports it?
3. What is the evolution target?
4. Which owner should store it?
5. How will future use be evaluated?
6. Where does it apply?
7. Where does it not apply?
8. What goes wrong if reused incorrectly?

If answer 1 is vague, do not store. If evidence is weak but plausible, use `watch`.

## Use Result Lifecycle

| Use result | Action |
| --- | --- |
| `helped` | update `last_confirmed`; add use evidence |
| `partial` | revise wording or narrow scope |
| `misled` | reject or supersede |
| `stale` | verify current fact; supersede or archive |
| `not_applicable` | add counterexample or narrow future use |
| `not_used` | leave in `watch` unless no future use remains |

## Staleness And Conflict

When facts may drift, verify before reuse. If current evidence conflicts with memory:

| Case | Action |
| --- | --- |
| Old item still mostly true | update `last_confirmed` |
| New fact replaces old fact | mark old `superseded` |
| Old item has no future use | mark `archive` |
| Old item is harmful | mark `rejected` |

Never delete useful history just to hide a bad prior memory.
