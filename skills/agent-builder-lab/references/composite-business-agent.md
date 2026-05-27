# Composite Business Agent

## 一句话结论

第二种 Agent 形态不是自建完整 AI runtime，而是用宿主 Agent、Skill、项目系统、CLI、结构化数据和人类验收共同组成一个业务 Agent。

## 定义

Composite Business Agent 是一种组合型业务 Agent。它不要求团队自建模型调度、工具选择、上下文管理和执行循环，而是把这些通用 AI 调度能力交给 Codex、OpenCode、Claude Code 等宿主 Agent，再用项目内的 Skill、规则、CLI、数据模型、报告和验收机制塑造业务行为。

```text
Host Agent
  + Skills / AGENTS.md
  + Project CLI / UI / scripts
  + Structured data / reports
  + Human review / approval
  + Build journal / evals
= Composite Business Agent
```

这不是“用 AI 辅助开发一个系统”这么简单。系统、Skill、宿主 Agent 和人共同构成了业务能力闭环。

## 与自建 Runtime Agent 的区别

| 维度 | 自建 runtime Agent | Composite Business Agent |
| --- | --- | --- |
| AI 调度 | 自己实现 loop / planner / dispatcher | 主要由宿主 Agent 提供 |
| 控制重点 | runtime、memory、policy、tool dispatch | Skill、项目系统、CLI、数据、报告、验收 |
| trace 能力 | 可记录内部完整轨迹 | 多数只能记录外部协作轨迹 |
| 适合场景 | 平台、SDK、长期自动运行 | 深入业务、人机共创、快速落地 |
| 主要风险 | runtime 复杂度、平台化过早 | 过度依赖宿主、边界和产物不清 |
| 评估重点 | 内部循环和能力分项 | 组合系统是否稳定完成业务目标 |

两种形态都成立。区别是控制边界不同，评估方法也不同。

## 为什么这种形态合理

| 理由 | 含义 |
| --- | --- |
| 宿主 Agent 已有强通用调度 | 不必从零实现计划、工具调用、代码编辑、文件操作 |
| 业务系统能结构化现实 | 数据、状态、报告、验证命令比纯对话更可控 |
| Skill 能塑造行为 | 可以固化方法、边界、风格、验收和学习循环 |
| 人类保留关键判断 | 业务品味、风险、发布、删除、花钱等动作由人确认 |
| 迭代成本低 | 先改 Skill、CLI、报告和 eval，而不是重写 runtime |

这种形态特别适合 DubForge、MacroPhase、个人研究助手、业务工作台、内容生产流水线、项目级 AI 操作台。

## 控制边界

| 层 | 谁负责 | 我们能否控制 |
| --- | --- | --- |
| 模型推理 | 宿主 Agent / provider | 低 |
| AI 调度 | 宿主 Agent | 低到中 |
| 指令和方法 | Skill / AGENTS.md | 高 |
| 业务动作 | CLI / API / scripts | 高 |
| 数据和状态 | 项目系统 | 高 |
| 可视化和报告 | 项目 UI / docs | 高 |
| 风险和审批 | Skill + 系统闸门 + 人 | 高 |
| 学习和沉淀 | journal + eval + harvest | 高 |

设计这种 Agent 时，不应把精力放在控制宿主内部调度，而应把精力放在可控层：输入清晰、工具窄、状态结构化、产物可验收、失败可沉淀。

第一版落地时，先按 `business-agent-build-procedure.md` 创建 package，并用 `business-agent-package-contract.md` 检查最小机器契约。

## 记忆和学习也是分层能力

Composite Business Agent 不应把业务记忆完全交给宿主 runtime。Runtime 可以帮助执行，但业务项目必须拥有自己的业务记忆、反馈、评估 baseline 和学习闭环。

| 层 | 作用 |
| --- | --- |
| Runtime memory | 服务执行质量，例如上下文、工具结果、短期状态 |
| Business memory | 服务业务质量，例如领域事实、profile、历史决策、用户业务偏好 |
| Eval memory | 服务能力判断，例如 cases、baselines、失败模式、回归趋势 |
| Collaboration memory | 服务人机效率，例如什么时候问人、怎么交付、怎么验收 |
| Agent-building memory | 服务跨项目方法沉淀，例如模板、原则、反模式 |

详细分层见 `references/memory-learning-layers.md`。

## 外部协作轨迹

Composite Business Agent 通常拿不到宿主 Agent 的完整内部 trace，但可以记录外部协作 trace。

```text
user goal
  -> loaded Skill / project instructions
  -> commands run
  -> files or records changed
  -> reports generated
  -> verification output
  -> delivery summary
  -> human acceptance / rejection
  -> build journal entry
```

这类 trace 不能解释模型内部所有选择，但足够评估业务 Agent 是否稳定完成任务。

## 评估重点

| 评估项 | 问题 |
| --- | --- |
| Skill 触发 | 该用的 Skill 是否被使用 |
| 任务对齐 | 是否明确目标、范围、验收和风险 |
| CLI 使用 | 是否调用正确命令，是否传入合理参数 |
| 结构化产物 | 是否生成数据、报告、diff、状态或可验收页面 |
| 人机边界 | 是否只在必要判断点询问人 |
| 业务结果 | 是否完成真实业务目标 |
| 返工成本 | 用户需要纠正几次，是否重复同类错误 |
| 沉淀能力 | 失败能否转成 case、rubric、Skill 或系统改进 |

评估对象是组合系统，不是宿主 Agent 本身。

## 推荐评估结构

```text
evals/
  scenarios/
  rubrics/
  fixtures/
  scorers/
  transcripts/
  reports/
docs/
  agent-eval-report.md
  agent-build-journal.md
scripts/
  eval_agent_scenario.py
```

| 资产 | 用途 |
| --- | --- |
| `scenarios/` | 人机协作业务场景 |
| `rubrics/` | 协作、产物、验收标准 |
| `fixtures/` | 固定输入、样例数据、初始状态 |
| `scorers/` | 自动检查脚本 |
| `transcripts/` | 真实或模拟协作记录 |
| `reports/` | 每轮评估结果 |

## Scenario 示例

```yaml
id: dubforge-candidate-console-001
agent_shape: composite
host_agent: codex
goal: Find and prepare candidate videos for review.
expected_skill:
  - agent-builder-lab
  - project AGENTS.md
expected_commands:
  - run candidate discovery CLI
expected_artifacts:
  - candidate records
  - review summary
  - risk notes
human_gate:
  must_ask_before:
    - create_job
    - publish
    - delete_candidate
score:
  outcome: required
  artifact_quality: required
  boundary_respect: blocking
  user_rework: tracked
```

这个 scenario 不评估宿主 Agent 内部如何思考，而评估组合系统能否把业务目标推进到可验收状态。

## 触发机制

| 变化 | 评估 |
| --- | --- |
| 改 Skill | Skill pressure scenario |
| 改 AGENTS.md | collaboration scenario |
| 改 CLI / API | deterministic test + scenario smoke |
| 改数据模型 | artifact schema eval |
| 改报告 | human-readable report rubric |
| 宿主 Agent 行为变化 | black-box scenario regression |
| 用户驳回交付 | 转成新 scenario 或 rubric |
| 业务流程成熟 | 更新 baseline 和验收阈值 |

## 设计原则

1. 借用宿主 Agent 的通用调度，不重复造完整 runtime。
2. 把业务知识和状态放进项目系统，而不是只放进 prompt。
3. 让 Skill 负责方法、边界、验收和学习循环。
4. 用 CLI、API、数据模型和报告把结果结构化。
5. 用人类验收守住风险、品味和业务判断。
6. 用 scenario、rubric 和外部协作 trace 评估整体效果。
7. 失败先留在项目内修正，跨项目价值再提升到共享 skill 或 eval 模板。

## 适用判断

优先选择 Composite Business Agent，当：

- 目标是深入一个业务领域，而不是卖一个通用 agent runtime。
- 宿主 Agent 已能完成大部分代码、文件、命令和工具操作。
- 业务系统可以提供结构化状态、CLI、报告或页面。
- 人类需要长期参与关键判断。
- 团队想先验证业务闭环，再决定是否自建 runtime。

优先选择自建 runtime Agent，当：

- 需要无人值守、长期运行、稳定调度。
- 需要完整控制 tool dispatch、memory、policy 和 trace。
- 需要作为 SDK、平台或多租户服务交付。
- 宿主 Agent 黑盒行为无法满足产品安全和可解释性要求。

## 与当前项目的关系

| 项目 | 形态判断 |
| --- | --- |
| DubForge | Composite Business Agent 优先：受限 Agent 控制台 + CLI/API + 候选池 + 人工采纳 |
| MacroPhase | Composite Business Agent 优先：Codex/Skill + 本地系统 + brief + note 沉淀 + 人类判断 |
| TradingAgents-CN | 可作为多 Agent 系统研究对象，也可被包装成 Composite Business Agent |
| agent-scaffold-skill | 负责沉淀自建 runtime 和复用模板 |
| agent-builder-lab | 负责沉淀两种形态的构建认知和评估认知 |

## 当前结论

Composite Business Agent 是有效且务实的第二种 Agent 形态。它不追求完全控制 AI 内部调度，而是把可控部分做扎实：Skill、系统、数据、CLI、报告、验收、eval 和学习闭环。

如果需要跨 Codex、OpenCode、Hermes、OpenClaw 或自建 runtime 运行，按 `runtime-portable-business-agent.md` 定义 adapter，不要把业务状态只留在宿主对话中。
