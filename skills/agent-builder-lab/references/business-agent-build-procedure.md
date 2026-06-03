# Business Agent Build Procedure

## 一句话结论

构建 Composite Business Agent 时，不要从抽象能力开始；先把一个业务目标落成可检查的 agent package，再用一次真实业务 run 验证它是否有价值。

## 适用场景

当目标是用 Codex、OpenCode、Hermes、OpenClaw 或类似宿主 Agent，加上 Skill、项目 CLI、数据、报告和人工验收，构建一个业务 Agent 时，使用这份规程。

如果目标是自建完整 runtime loop、planner、dispatcher、memory engine 和 trace system，这份规程只能作为业务层参考。

## 输入

开始前必须能回答四个问题：

| 问题 | 如果答不出 |
| --- | --- |
| 这个 Agent 服务哪个业务目标 | 停下来澄清 mission |
| 它创造什么可观察业务价值 | 停下来定义 business_value |
| 它能做哪些动作 | 先只定义 3 到 5 个核心 actions |
| 哪些动作必须人审 | 先定义 risk_class 和 human_gates |
| 工作台承载什么 | 默认只承载展示、提示、模板、产物和人审入口 |

不要用“提高效率”“辅助分析”作为最终答案。要写成可验收的业务结果，例如“把候选视频整理成可人工采纳的候选池记录”。

## 输出

第一版输出是一个 business-agent package：

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

可以从模板复制：

```bash
cp -R ~/.codex/skills/agent-builder-lab/assets/templates/business-agent ./business-agent
```

复制后先改内容，不要先扩展目录。

## 构建步骤

### 1. 定义 Agent Contract

填写 `agent.yaml`。先填这些字段：

| 字段 | 写法 |
| --- | --- |
| `id` | 稳定短名，例如 `dubforge-candidate-agent` |
| `mission` | 这个 Agent 要稳定完成的业务使命 |
| `business_value` | 它带来的可观察业务价值 |
| `non_goals` | 明确不做什么，防止能力膨胀 |
| `allowed_actions` | 只列第一版真实需要的动作 |
| `risk_classes` | 把动作按风险分层 |
| `human_gates` | 定义哪些风险必须人审 |
| `runtime_targets` | 第一版通常先放 `codex` |

如果 `mission` 和 `business_value` 写不清楚，不要继续写 actions。

### 1.5 定义 Interaction Surfaces

对混合型或 Composite Business Agent，先在 `agent.yaml` 写清楚三个交互表面：

| 表面 | 第一版默认 |
| --- | --- |
| AI 对话 / 宿主 Agent | 探索、判断、综合、调用工具、生成候选产物 |
| 工作台 | 展示状态、产物、证据、人工闸门、可复制 prompt、固定模板、导入导出包 |
| 固定应用流程 | 只承载已稳定、可审计、输入输出清楚的动作 |

第一版不要把还在变化的 AI 协作过程做成复杂 UI workflow。先让 AI 在对话里完成高变动工作，把结果、提示、模板、审核点和 handoff package 回写到工作台。某个动作经过真实 run 证明稳定后，再提升为工作台按钮或固定流程。

### 2. 定义 3 到 5 个 Actions

每个 action 放在 `actions/*.yaml`。第一版优先选择窄动作：

| 动作类型 | 示例 |
| --- | --- |
| Inspect | 读取项目状态、外部来源、候选记录 |
| Write record | 写入结构化业务记录 |
| Generate report | 生成可人工验收的报告 |
| Propose change | 提出变更建议但不直接执行高风险动作 |
| Execute gated action | 只有在人审后执行外部可见动作 |

每个 action 必须写清楚输入、输出、风险、审批、产物和禁止条件。

### 3. 定义 Artifacts

每个重要结果都应该有 artifact contract。不要只依赖聊天回答。

第一版至少有一个 artifact，例如：

| Artifact | 用途 |
| --- | --- |
| candidate_record | 业务记录 |
| review_summary | 人类验收报告 |
| run_report | 一次任务的执行证据 |

每个 artifact 必须说明 evidence_required。没有证据链的输出只能是观察，不能作为高置信业务结论。

### 4. 定义 Memory

业务记忆属于项目，不属于宿主 runtime。

第一版只需要两类文件：

| 文件 | 用途 |
| --- | --- |
| `memory/business-memory.yaml` | 稳定使命、偏好、长期决策 |
| `memory/feedback-log.yaml` | 人类反馈、失败、需要沉淀的规则 |

不要把一次性聊天内容直接提升为长期记忆。先记录 feedback，再决定进入 memory、eval、action、artifact 或 archive。

### 5. 定义 Evals

每个业务 Agent 至少需要一个 smoke scenario。

第一版 eval 不追求评估宿主模型内部推理，而是评估组合系统：

| 评估面 | 问题 |
| --- | --- |
| Outcome | 是否推进了真实业务目标 |
| Artifact | 是否产生可验收产物 |
| Evidence | 关键结论是否可追溯 |
| Boundary | 高风险动作是否停在人审点 |
| Rework | 用户是否要反复纠正同类问题 |

### 6. 定义 Runtime Adapter

每个 runtime target 都要有 `runtime-adapters/*.yaml`。

第一版只需说明：

| 字段 | 含义 |
| --- | --- |
| `runtime` | Codex、OpenCode、Hermes、OpenClaw 或 self-built |
| `invocation` | 如何启动或触发 |
| `skill_trigger` | 需要加载哪些 Skill 或项目规则 |
| `capability_map` | 这个 runtime 能稳定做什么 |
| `unsupported_actions` | 不应依赖什么能力 |
| `handoff_rules` | 状态、证据、风险如何交还给项目 |

详细规则见 `runtime-portable-business-agent.md`。

### 7. 定义 Delivery Package

每次业务运行结束时，都要按 `reports/delivery-package.md` 交付。

交付必须包含：

```text
result
evidence
risks
human gates
artifacts
next action
```

如果交付不能让人一次性判断是否接受，说明 artifact 或 evidence 还不够。

### 8. 运行结构检查

在 business-agent package 根目录运行：

```bash
python ~/.codex/skills/agent-builder-lab/scripts/check_business_agent_package.py .
```

这个检查只覆盖最低结构要求。通过不代表业务正确，只代表已经具备第一版实现入口。

### 9. 跑一次最小业务 Run

选择一个真实但低风险的业务任务：

```text
one business goal
  -> one allowed action
  -> one artifact
  -> one delivery package
  -> one feedback or eval note
```

如果第一次 run 不能产出 artifact，不要继续加功能。先修 contract、action 或 artifact。

### 10. 写入构建日志

把真实摩擦写入 `docs/agent-build-journal.md`：

| 情况 | 写入 |
| --- | --- |
| mission 不清 | decision 或 friction |
| action 太宽 | reusable pattern 或 risk mismatch |
| artifact 不可验收 | missing capability |
| 人类反复纠正 | durable taste signal 或 eval case |
| runtime 做不到 | runtime adapter limitation |

## Ready Check

一个第一版 Business Agent package 至少满足：

| 检查 | 通过标准 |
| --- | --- |
| Structure | `check_business_agent_package.py` 通过 |
| Business value | `business_value` 可观察，不是空泛表述 |
| Actions | 3 到 5 个窄动作，风险清楚 |
| Artifacts | 至少 1 个可人工验收产物 |
| Evidence | 关键结论有来源或验证方式 |
| Human gate | 外部、删除、发布、花钱、迁移等动作有人审 |
| Eval | 至少 1 个 smoke scenario |
| Runtime | 至少 1 个 adapter 明确支持和不支持什么 |
| Delivery | 有固定交付格式 |
| Workbench | 展示、验收、提示、模板和交接清楚，不过早承载探索性 AI 流程 |

## Stop Conditions

遇到这些情况要停止扩展，先修定义：

- 业务价值说不清。
- action 看起来像“让 AI 自己决定一切”。
- artifact 只是聊天摘要，没有结构和证据。
- risky action 没有人审。
- eval 只看最终回答，不看证据、边界和返工。
- 业务状态只存在聊天里，没有项目自有文件或系统记录。
- 工作台试图实现尚未稳定的 AI 推理或探索流程。

## 使用原则

第一版目标不是造平台，而是证明这套组合能完成一个有价值的业务闭环：

```text
business value
  -> constrained actions
  -> structured artifacts
  -> evidence
  -> human gates
  -> delivery
  -> feedback / eval / memory
```
