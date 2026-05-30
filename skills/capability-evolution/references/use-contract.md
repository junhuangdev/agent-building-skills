# Use Contract

## Conclusion

Learned content only matters when it changes future work. Every active artifact should be reusable, and every meaningful reuse should feed the next improvement decision.

## Use Loop

```text
retrieve -> use -> evaluate_use -> improve -> learn_again
```

## Required Use Record

When a memory, eval, Skill rule, template, or promotion candidate affects a task, record:

```text
applied_artifact: Which learned artifact was used?
task_context: Where was it used?
use_result: helped | partial | misled | stale | not_applicable | not_used
evidence: What output, trace, eval, or feedback proves that result?
follow_up: confirm | narrow | revise | supersede | archive | reject | promote | none
```

## Result To Action

| `use_result` | Default action |
| --- | --- |
| `helped` | `confirm`; promote after repeated evidence |
| `partial` | `narrow` or `revise` |
| `misled` | `reject` or `supersede` |
| `stale` | `supersede` or `archive` |
| `not_applicable` | `narrow` scope or counterexamples |
| `not_used` | keep `watch`, archive if no future task exists |

## Use Evaluation Layers

| Layer | Question |
| --- | --- |
| Outcome | Did the task result improve? |
| Trace | Did the learned artifact guide the path correctly? |
| Scope | Was the artifact applied only where it fits? |
| Freshness | Did current evidence still support it? |
| Human feedback | Was the result useful in practice? |

## Anti-Patterns

- Do not count a stored artifact as an improvement until it has use evidence or strong risk evidence.
- Do not promote an artifact only because it was retrieved.
- Do not keep reusing an artifact that repeatedly produces `partial`, `misled`, or `stale` results without revision.
- Do not treat `not_used` as failure when the task did not match the artifact.
