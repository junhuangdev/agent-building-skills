# Eval Contract

## Conclusion

Capability evolution cannot be evaluated by final output alone. A valid eval checks outcome, trace, memory behavior, use result, policy behavior, and human feedback.

## Evaluation Layers

| Layer | Question | Fail signal |
| --- | --- | --- |
| Outcome | Did the task result satisfy the goal? | missing or wrong result |
| Trace | Did the AI use a defensible path? | skipped verification or repeated failed path |
| Memory | Did it read/write/update memory correctly? | pollution, stale reuse, bad scope |
| Use result | Did the learned artifact improve this task? | retrieved but unused, partial, stale, or misleading reuse |
| Policy | Did it respect risk and approval gates? | bypassed gate or unsafe action |
| Human feedback | Was it actually useful? | rejected, partial, or preference mismatch |

Policy failures and serious memory pollution are blocking even if the final output looks correct.

## Eval Case Types

| Type | Use when |
| --- | --- |
| Smoke case | Prove the evolution loop can run on a simple task |
| Regression case | A past failure should not repeat |
| Transfer case | A lesson should work in a nearby or different scenario |
| Policy case | A gate or risk boundary must hold |
| Memory case | Retrieval, write, staleness, or promotion behavior is under test |
| Use case | A learned artifact must prove value when applied |
| Self-evolution case | A Skill or Agent changes itself and must prove the change improves behavior |

## Trace Invariants

Good eval cases include invariants such as:

- verify freshness before using drift-prone facts;
- never promote one-off success to Skill without evidence;
- never write private or project-specific content to shared memory;
- never let a Skill approve its own shared promotion;
- route `evolution_target` and `storage_sink` before writing memory;
- record use result when a learned artifact affects a task;
- stop for approval before high-risk external actions;
- do not call the same failing tool path repeatedly without classification;
- preserve `success_no_result` when empty output is valid.

## Human Feedback Shape

Keep feedback simple:

```text
human_feedback:
  result_useful: yes | no | partial
  reason: direction_wrong | weak_evidence | too_verbose | not_specific | risk_unacceptable | other
  durable_preference: yes | no | only_this_project
  notes: optional short explanation
```

AI converts this into memory, eval, or promotion candidates. The human should not need to inspect internal trace unless risk, trust, or shared promotion requires it.
