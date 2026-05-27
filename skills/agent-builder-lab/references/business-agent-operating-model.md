# Business Agent Operating Model

## 一句话结论

Business Agent 的通用能力不是业务答案，而是让业务目标变成可执行、可追踪、可验收、可改进的操作模型。

## 定义

Business Agent Operating Model 是业务 Agent 的通用流程骨架。它不替代 Codex、OpenCode、Hermes、OpenClaw 或自建 runtime 的 AI 调度能力，而是固定业务层需要长期拥有的能力：

```text
business goal
  -> business run
  -> action registry
  -> artifact contract
  -> evidence chain
  -> human gate
  -> delivery package
  -> feedback / eval / memory loop
```

这套模型服务 Composite Business Agent，也可以服务未来自建 runtime Agent 的业务层。

## 核心分层

| 层 | 作用 | 典型资产 |
| --- | --- | --- |
| Core lifecycle | 定义任务如何开始、推进、结束 | run、stage、status |
| Execution surface | 定义能做什么、产出什么、凭什么判断 | actions、artifacts、evidence、gates |
| Improvement loop | 定义如何变好 | memory、feedback、eval、risk、recovery |
| Runtime portability | 定义如何跑在不同宿主上 | runtime adapters、capability matrix |

业务标准可以变化，但这些流程结构应该稳定。

## 能力清单

| 能力 | 固定流程 | 业务差异 |
| --- | --- | --- |
| Identity and boundary | mission、non-goals、allowed actions | 具体业务使命和边界 |
| Task intake | 收到目标、补上下文、建 run | 输入字段、来源、默认值 |
| Run lifecycle | created、running、blocked、done、failed | 业务状态枚举 |
| Workflow stage | stage、gate、transition | 业务流程步骤 |
| Action registry | action schema、risk、permission、result | 具体 CLI/API/tool |
| Artifact contract | 类型、来源、验证、展示、归档 | 报告字段和展示方式 |
| Evidence chain | source、action、result、evidence、decision | 证据充分标准 |
| Human gate | approve、reject、edit、escalate | 哪些点必须人审 |
| Delivery package | summary、evidence、risk、next step | 业务表达格式 |
| Observability | run log、event、artifact、decision log | 指标和审计要求 |
| Recovery | classify、retry、degrade、escalate | 可接受降级方式 |
| Portability | canonical contract、runtime adapter | runtime 能力差异 |

## 最小资产结构

```text
business-agent/
  agent.yaml
  actions/
  artifacts/
  memory/
  evals/
  reports/
  runtime-adapters/
```

详细字段和检查规则见 `business-agent-package-contract.md`。第一版构建步骤见 `business-agent-build-procedure.md`。

| 资产 | 用途 |
| --- | --- |
| `agent.yaml` | 业务 Agent 的 canonical contract |
| `actions/` | 可执行业务动作目录 |
| `artifacts/` | 产物 schema 和样例 |
| `memory/` | profile、decisions、feedback |
| `evals/` | scenarios、rubrics、baselines |
| `reports/` | 交付和评估报告 |
| `runtime-adapters/` | Codex、OpenCode、Hermes 等宿主映射 |

## Business Run

每次业务任务都应有一个 run。

```yaml
run_id: run_2026_05_27_001
goal: Find candidate videos for review.
status: running
stage: discovery
risk_class: external
artifacts: []
decisions: []
human_gates: []
started_at: 2026-05-27T10:00:00Z
```

Business Run 对应 runtime agent 的 session，但它属于业务项目，不属于宿主 runtime。

## Action Registry

所有业务动作都应先注册，再暴露给 AI 或 CLI。

```yaml
id: write_candidate
description: Write a candidate video record for human review.
input_schema: schemas/write_candidate.input.yaml
output_schema: schemas/candidate.output.yaml
risk_class: external
requires_approval: false
side_effects:
  - writes_project_data
forbidden_when:
  - missing_source_url
```

动作目录的价值是把“AI 可以做什么”变成可审计、可测试、可迁移的契约。

## Artifact Contract

业务 Agent 的产出不应只是聊天回答。重要结果应该变成 artifact。

```yaml
id: artifact_001
type: candidate_review_summary
source_run_id: run_2026_05_27_001
status: verified
evidence:
  - source_url
  - inspection_result
human_readable_summary: Generated candidate review summary.
```

Artifact Contract 让人能验收，也让后续 Agent 能继续接手。

## Evidence Chain

关键结论要能追到来源和验证。

```text
source
  -> action
  -> result
  -> evidence
  -> decision
```

缺少 evidence chain 的结论只能作为观察，不能作为高置信业务判断。

## Human Gate

人类参与点应结构化，而不是散落在对话里。

```yaml
gate_id: gate_publish_001
action: publish_video
risk_class: external
required_decision: approve | reject | edit | defer
reason: Publishing is externally visible.
```

Human Gate 的目标不是让人频繁确认，而是让必要判断发生在必要位置。

## Delivery Package

每次交付都应该让人一次性验收。

```text
Result: What changed or was produced.
Evidence: How to verify it.
Risks: What remains uncertain.
Human gates: What needs approval.
Artifacts: Where the structured outputs are.
Next action: What should happen next.
```

这是 Business Agent 版的 final answer contract。

## Improvement Loop

Business Agent 的学习闭环如下：

```text
business run
  -> artifact
  -> delivery
  -> human feedback
  -> memory update
  -> eval / baseline update
  -> journal entry
  -> harvest decision
```

这套流程借鉴 runtime agent 的 observe、evaluate、update loop，但所有权在业务项目。

## 与 Runtime Agent 的映射

| Runtime Agent | Business Agent |
| --- | --- |
| session | business run |
| tool registry | action registry |
| tool result | artifact / record |
| context state | business state |
| policy gate | human gate / business rule |
| trace | evidence chain / collaboration trace |
| final answer | delivery package |
| eval case | business scenario |
| memory update | profile / decision / feedback update |

## 第一版落地建议

第一版不要做大平台。先在一个真实业务项目里落最小闭环：

1. 从 `assets/templates/business-agent/` 复制第一版 package。
2. 定义 `agent.yaml`。
3. 定义 3 到 5 个核心 actions。
4. 定义 1 到 3 个 artifact contracts。
5. 定义必要 human gates。
6. 定义至少 1 个 smoke eval scenario。
7. 定义至少 1 个 runtime adapter。
8. 运行 `python ~/.codex/skills/agent-builder-lab/scripts/check_business_agent_package.py ./business-agent`。
9. 每次运行产出一个 delivery package。
10. 失败或人工驳回进入 `agent-build-journal.md`。

## 当前原则

1. 固定流程机制，不固定业务答案。
2. 业务状态和产物属于项目，不属于宿主 runtime。
3. 所有 AI 可执行动作都应可注册、可审计、可测试。
4. 所有关键结论都应有 evidence chain。
5. 人类参与点应结构化为 gate。
6. 交付必须有 artifact 和 evidence。
7. 改进必须进入 memory、eval 或 journal，而不是留在一次性对话里。
