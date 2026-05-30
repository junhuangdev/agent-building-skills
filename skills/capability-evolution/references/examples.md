# Examples

## Example 1: The Capability Evolution Skill Improves Itself

`$capability-evolution` notices that callers repeatedly forget to route learned content to the correct owner.

| Step | Artifact |
| --- | --- |
| Target | `skill_improvement` |
| Sink | `owning_skill_package` for local package changes; `shared_skill_candidate` for shared behavior |
| Eval | Caller-routing case checks `evolution_target` and `storage_sink` |
| Use | Apply the new routing rule in the next task and record `use_result` |
| Promotion | Human approval before the changed Skill becomes the shared default |

Correct decision: self-reference is allowed, self-approval is not. Storage is not enough; the revised rule must be used and evaluated.

## Example 2: Another Skill Uses Learning

A document-editing Skill sees repeated failures in visual QA.

| Step | Artifact |
| --- | --- |
| Target | `skill_improvement` |
| Sink | `owning_skill_package` |
| Memory | Under-evidenced failure pattern in `watch` |
| Eval | Regression case that checks rendered pages before delivery |

Correct decision: `$capability-evolution` supplies the loop, use evaluation, and templates; the document Skill owns the content.

## Example 3: Agent Method Vs Agent Business

An Agent learns both a better candidate-ranking method and a business-specific evidence threshold.

| Learned item | Target | Sink |
| --- | --- | --- |
| Reusable ranking method | `agent_method` | `shared_skill_candidate` or owning Agent repo |
| Business evidence threshold | `agent_business` | owning Agent repo or current project |

Correct decision: the same loop handles both, but they should not be stored as the same kind of knowledge.

## Example 4: Software Project Learning

A project accumulates knowledge about its architecture, local commands, and delivery process.

| Learned item | Target | Sink |
| --- | --- | --- |
| Project architecture fact | `software_project` | `current_project` |
| Development workflow improvement | `workflow_process` | `current_project` first |
| Cross-project engineering method | `agent_method` or `workflow_process` | `shared_skill_candidate` only with evidence |

Correct decision: keep project knowledge in the project. Promote only the method that truly transfers.

## Example 5: Trace Violation

Final answer is correct, but the AI skipped a required approval gate.

Correct decision: outcome passes, policy fails. Create a policy eval case and do not mark the evolution run as passed.
