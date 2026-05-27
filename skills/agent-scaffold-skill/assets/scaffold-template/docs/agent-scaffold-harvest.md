# Agent Scaffold Harvest

Use this file to record reusable scaffold lessons discovered while building this agent.

Project-specific prompts, business rules, and data sources should stay in this project.

## Entries

Copy this block when a scaffold-level lesson appears:

```text
### H-0001 Short title
promote_to_skill: no
boundary: runtime | provider | integration | tool | memory | approval | eval | config | docs
failure: What user-visible or developer-visible failure happened?
lesson: What reusable scaffold lesson did this expose?
verification: What test, eval, or check would prove the scaffold improvement works?
project_specific: What should stay in this project?
```

Set `promote_to_skill: yes` only when the lesson should update the shared `agent-scaffold-skill`.
