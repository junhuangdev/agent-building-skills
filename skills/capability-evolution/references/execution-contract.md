# Execution Contract

## Conclusion

Capability evolution starts as an execution discipline, not a storage action. Every evolution event must connect task context, learned content, use, evidence, evaluation, routing, and a lifecycle decision.

## Universal Loop

| Stage | AI action | Output |
| --- | --- | --- |
| Intake | Restate goal, scope, risk, and expected outcome | task frame |
| Learn | Extract a candidate lesson from feedback, trace, eval, or failure | candidate artifact |
| Store | Route the artifact to the owner that can maintain it | memory/eval/feedback/promotion |
| Retrieve | Read relevant project docs, memory, evals, and rules | context set |
| Use | Apply the retrieved artifact in a real task | applied artifact + result |
| Evaluate | Check outcome, trace, memory, policy, feedback, and use result | eval judgment |
| Improve | Confirm, narrow, revise, supersede, archive, reject, or promote | lifecycle decision |
| Learn again | Treat the use result as new evidence | updated artifact |

This loop applies to the capability-evolution skill itself, other Skills, Agents, and software projects. The mechanism is stable; only the owner, storage sink, and evaluation rubric change.

## Evolution Event Types

| Event | Default artifact |
| --- | --- |
| User says "remember this" | feedback record, then memory candidate |
| Repeated task failure | memory item + eval case |
| Trace or policy violation | eval case + possible promotion package |
| Stale or conflicting memory | memory update / supersede |
| Skill wants self-improvement | memory item or eval case in the owning Skill package |
| Learned artifact is reused | use record + confirm/narrow/revise/archive decision |
| Agent learns a reusable method | `agent_method` memory or shared candidate |
| Agent learns business behavior | owner-local `agent_business` memory or eval |
| Project learns dev/process knowledge | `software_project` or `workflow_process` memory |
| Reusable workflow discovery | memory item in `watch`; promotion package only with evidence |
| User accepts durable preference | scoped memory item, possibly promotion package |

## Decision Flow

```text
Does this change future behavior?
  no -> do not store
  yes -> identify evolution_target
    identify storage_sink owner
      local owner -> memory/eval/feedback in that owner
      shared candidate -> promotion package, not active rule
      runtime behavior -> runtime_candidate until owner approval

When the artifact is later used:
  record applied_artifact + use_result
  if helped repeatedly -> confirm or promote
  if partly helped -> narrow or revise
  if misled or stale -> supersede, archive, or reject
```

## Human Boundary

AI can draft and evaluate evolution artifacts. Humans decide:

- whether the result is useful;
- whether a preference is durable;
- whether a high-risk action is allowed;
- whether project-local evidence should become shared behavior.

## Completion Criteria

An evolution pass is complete only when:

1. the task result is delivered;
2. evidence has been checked beyond the final output;
3. any evolution artifact has a evolution target, storage sink, scope, future use, evidence, use history, last use result, and risk;
4. any reused artifact records whether it helped, partially helped, misled, was stale, or did not apply;
5. promotion beyond the current project is only a recommendation until approved.
