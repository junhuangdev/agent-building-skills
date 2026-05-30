# Integration Contract

## Conclusion

`$capability-evolution` is a reusable capability. The caller owns the task and the learned content; `$capability-evolution` owns the evolution loop, artifact shape, routing rules, use evaluation, and promotion discipline.

## Caller Responsibilities

| Caller | Owns | Calls `$capability-evolution` when |
| --- | --- | --- |
| Capability Evolution Skill | Its own process, templates, evals | It finds a self-improvement signal |
| Other Skill | Skill-specific procedure and examples | A task reveals a reusable Skill defect or improvement |
| Agent | Agent method, business behavior, evals | A run should update future Agent behavior |
| Project | Project facts, dev process, local workflow | Work reveals durable project knowledge |

The caller should pass the task frame, relevant trace, feedback, owner, risk, privacy boundary, and likely storage owner. If the caller is unsure, `$capability-evolution` can propose a route.

## Invocation Moments

| Moment | Expected return |
| --- | --- |
| Task completed | no-op, memory item, or feedback record |
| Task failed | memory item plus eval case |
| User gave feedback | feedback record plus possible memory item |
| Learned artifact was used | use record plus confirm/narrow/revise/archive decision |
| Memory conflict found | update, supersede, archive, or reject recommendation |
| Repeated pattern found | promotion package candidate |
| Skill or Agent self-review | self-evolution package or eval case |

## Return Shape

`$capability-evolution` should return one of:

- `no-op`: no future behavior change.
- `memory`: structured memory item with `evolution_target` and `storage_sink`.
- `eval_case`: regression, transfer, policy, memory, or self-evolution case.
- `use_record`: applied artifact, use result, evidence, and follow-up action.
- `feedback_record`: normalized human feedback.
- `promotion_package`: recommendation awaiting approval.
- `decision_package`: human judgment is required before writing or promoting.

## Boundary

The caller may delegate classification, artifact drafting, and first-pass evaluation to `$capability-evolution`. The caller must not delegate final ownership, private data approval, shared-layer promotion, or high-risk action approval.

When the caller is itself a Skill or Agent, `$capability-evolution` can support self-evolution but cannot become the approver of that self-evolution.
