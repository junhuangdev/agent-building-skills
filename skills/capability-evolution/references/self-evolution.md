# Self-Evolution

## Conclusion

The capability-evolution skill can use itself as a capability, but self-evolution must be evidence-backed, bounded, and require external approval when it changes shared behavior.

## Loop

| Stage | Action |
| --- | --- |
| Observe | Capture a defect, repeated friction, feedback, or eval result |
| Classify | Set `evolution_target: skill_improvement` |
| Route | Use `storage_sink: owning_skill_package` or `shared_skill_candidate` |
| Draft | Create memory, eval, template change, or promotion package |
| Use | Apply the candidate change in a realistic task or example |
| Evaluate | Run the relevant checker or eval case and record use result |
| Decide | Human or owning maintainer approves shared or risky changes |
| Record | Keep evidence, counterexamples, and review trigger |

## Allowed Self-Reference

The term self-reference means `$capability-evolution` can treat its own behavior as an evolution target.

`$capability-evolution` may:

- create an eval case for its own behavior;
- draft a memory item about a recurring learning failure;
- draft a promotion package for a template, rule, or checker update;
- validate an evolution package with its own checker;
- archive or reject weak self-improvement candidates when there is no future effect.

## Not Allowed

`$capability-evolution` must not:

- approve its own shared-layer promotion;
- turn one self-observation into an active shared rule;
- hide failed self-evolution attempts by deleting history;
- write private project content into its own shared package;
- keep looping until it invents a change.

## Anti-Loop Limits

- At most one self-evolution promotion package per task unless the user asks for a dedicated review.
- A no-op is a valid evolution result.
- Self-improvement needs either repeated evidence, a serious trust/safety failure, or a failing eval that the change fixes.
- A checker passing proves shape, not usefulness. Human feedback or realistic evals are still needed for shared behavior.

## Other Skills And Agents

Other Skills and Agents use the same loop. They should call `$capability-evolution` for classification, routing, eval shape, and promotion packaging, while keeping their domain content in their own package or project.
