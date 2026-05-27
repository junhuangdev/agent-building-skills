# Agent Evaluation Cognition

## 一句话结论

Agent 评估不是只给最终输出打分，而是用固定任务、执行轨迹、分项能力、风险规则和线上反馈来判断 Agent 是否真的变强。

## 当前认知

主流 Agent 的能力类别已经明显收敛，但没有一个可以直接替代所有 Agent 内部评估的统一标准。

| 判断 | 含义 |
| --- | --- |
| 能力类别收敛 | 模型、调度、工具、状态、记忆、策略、观测、评估基本都会出现 |
| 实现仍常自建 | 这些能力靠近产品控制权，不能完全交给外部库决定 |
| 评估没有统一标准 | 行业有通用方法，但不同 Agent 需要自己的任务、rubric 和风险阈值 |
| 最终输出不够 | Agent 的好坏经常藏在工具选择、调用顺序、恢复、停止和升级过程里 |
| trace 是核心证据 | 没有执行轨迹，就很难解释为什么变好或变坏 |

因此，我们需要一套统一评估骨架，而不是一套所有 Agent 共用的题库。

## Agent 形态影响评估边界

本文的评估模型同时适用于两类 Agent，但评估边界不同。

| Agent 形态 | 评估重点 |
| --- | --- |
| 自建 runtime Agent | 内部 loop、tool dispatch、memory、policy、trace、provider 行为 |
| Composite Business Agent | 宿主 Agent + Skill + 项目系统 + CLI + 报告 + 人类验收的整体业务效果 |

当 Agent 建立在 Codex、OpenCode、Claude Code 等宿主 Agent 之上时，不要假设可以控制或记录完整内部调度。此时应评估外部协作轨迹、Skill 触发、项目 CLI、结构化产物、人机边界和业务结果。

详细定义见 `references/composite-business-agent.md`。

## 评估和学习也要分机制与内容

评估、记忆和学习有一部分可以通用，但通用的是机制，不是业务真相。

| 项 | 通用机制 | 项目内容 |
| --- | --- | --- |
| Eval case | schema、runner、report | 业务任务、输入、期望输出 |
| Scorer | interface、result shape | 业务判断、阈值、权重 |
| Memory | lifecycle、存储格式、提升流程 | 业务事实、profile、用户偏好 |
| Learning | feedback intake、harvest、archive | 哪些反馈改变业务策略 |

详细分层见 `references/memory-learning-layers.md`。

## 为什么不能只看最终结果

最终输出只能回答“这次看起来是否完成了”。它不能稳定回答：

- 是否用了正确工具。
- 是否绕过了审批边界。
- 是否重复调用无效工具。
- 是否在失败后换了策略。
- 是否把项目特定信息错误提升为通用记忆。
- 是否用更高成本换来相同结果。
- 是否在应该报告 `success_no_candidates` 时编造了弱结果。

这些问题必须通过执行轨迹、工具记录、状态变化、风险事件和人工反馈来判断。

## 四层评估模型

| 层 | 评估对象 | 主要问题 | 产物 |
| --- | --- | --- | --- |
| Capability | 单项能力 | 这项能力是否按契约工作 | 单项 scorer |
| Trajectory | 执行过程 | 路径、工具、恢复、停止是否合理 | trace score |
| Task Outcome | 端到端任务 | 用户目标是否完成 | pass/fail/report |
| Operational | 真实运行 | 成本、延迟、人工介入、返工是否可接受 | trend/report |

这四层不能互相替代。端到端通过是验收入口，trajectory 是诊断入口，capability 是回归保护，operational 是长期质量信号。

## 能力评估拆分

| 能力 | 评估重点 | 示例信号 |
| --- | --- | --- |
| Goal alignment | 目标、范围、完成标准是否明确 | 错任务、过度扩张、遗漏验收 |
| Orchestration | 步骤选择、顺序、并行、停止 | 多余步骤、依赖倒置、过早停止 |
| Tool use | 工具选择、参数、结果处理 | 错工具、错参数、忽略工具错误 |
| Memory | 读取、写入、遗忘、提升 | 记忆污染、未复用、过度保存 |
| Policy | 风险分级、审批、拒绝 | 越权执行、过度打断、误拒绝 |
| Recovery | 失败分类、重试、降级 | 重复同一失败、静默掩盖错误 |
| Provider | 模型切换、能力差异、成本 | provider 分支泄漏、结构化输出破坏 |
| Product UX | 结果形态、解释、人工验收 | 用户无法验收、证据不足 |

## 统一什么，不统一什么

| 项 | 决策 |
| --- | --- |
| Trace schema | 统一 |
| Eval case schema | 统一骨架 |
| Runner CLI | 统一 |
| Scorer interface | 统一 |
| Report format | 统一 |
| Policy baseline | 统一最低线 |
| 业务任务集 | 每个 Agent 自己维护 |
| 业务 rubric | 每个 Agent 自己维护 |
| 分数权重 | 每个 Agent 自己维护 |
| 阈值和发布门禁 | 项目配置，必要时共享默认 |

统一骨架保证可比较、可自动化、可沉淀。项目自有内容保证评估真正贴近 Agent 的业务目标。

## 推荐落地形态

每个真实 Agent 项目应该有自己的评估资产：

```text
evals/
  cases/
  scorers/
  rubrics/
  baselines/
traces/
docs/
  agent-eval-report.md
  agent-build-journal.md
```

| 资产 | 作用 |
| --- | --- |
| `evals/cases/*.yaml` | 固定任务和预期行为 |
| `evals/scorers/*` | 自动评分逻辑 |
| `evals/rubrics/*.md` | 人和 LLM judge 共用的评价标准 |
| `evals/baselines/*.json` | 稳定版本结果，用于比较退化 |
| `traces/*.jsonl` | 可审计执行轨迹 |
| `docs/agent-eval-report.md` | 人可读评估报告 |
| `docs/agent-build-journal.md` | 把评估暴露出的经验进入学习循环 |

`agent-builder-lab` 保存认知和学习循环。`agent-scaffold-skill` 可以保存可复用模板、schema 和 runner。具体 Agent 项目保存自己的 cases、rubrics、baseline 和报告。

## 触发机制

| 触发 | 跑什么 |
| --- | --- |
| 改 prompt | smoke outcome eval + trace spot check |
| 改 model/provider | provider smoke + structured output + cost diff |
| 改 tool schema | tool contract eval + relevant task eval |
| 改 orchestration loop | full trajectory regression |
| 改 memory rule | memory read/write eval + pollution check |
| 改 policy/approval | policy gate eval，一票否决 |
| 上线前 | full regression + human-readable report |
| 线上失败 | trace 转 case，补入回归集 |
| 人工驳回 | 记录原因，必要时补 scorer 或 rubric |

触发不是为了制造流程，而是为了让“Agent 是否变强”能被重复判断。

## Scorer 类型

| Scorer | 用途 |
| --- | --- |
| Deterministic | JSON schema、字段、状态、工具名、风险标签 |
| Trace invariant | 必须先查证再写入、不得跳过审批、不得重复失败工具 |
| LLM-as-judge | 开放文本质量、解释质量、证据充分性 |
| Human review | 品味、业务判断、高风险发布前验收 |
| Cost/latency | token、工具调用次数、耗时、失败率 |

安全和权限类 scorer 应该是一票否决。开放质量类 scorer 可以作为趋势或人工复核入口。

## 最小 Case Schema

```yaml
id: dubforge-candidate-001
agent: dubforge-candidate-discovery
goal: Find ingestible candidate videos for a target platform.
initial_state:
  profile: default
  existing_candidates: []
available_tools:
  - search_sources
  - inspect_video
  - write_candidate
risk_class: external
expected_outcome:
  completion_state: success_with_candidates
  min_candidates: 1
expected_trace:
  must_call:
    - search_sources
    - inspect_video
  must_not_call:
    - create_job
    - publish_video
scorers:
  - outcome_completion
  - tool_sequence
  - policy_gate
  - evidence_quality
budget:
  max_tool_calls: 12
  max_minutes: 5
```

这个 schema 是骨架示例，不是最终标准。真实项目应从 5 到 10 个高价值 case 开始，而不是一开始追求完整 benchmark。

## 评估结果怎么进入学习

```text
eval run
  -> report
  -> failure / regression / improvement
  -> agent-build-journal entry
  -> harvest review
  -> project fix or promotion target
```

只有可复用、可验证、会影响未来 Agent 构建的经验，才应该从项目日志提升到 `agent-builder-lab`、`agent-scaffold-skill`、`agent-core`、`vibeflow` 或 eval 模板。

## 对我们当前项目的含义

| 项目 | 第一批评估重点 |
| --- | --- |
| DubForge | 候选发现目标、`success_no_candidates`、风险边界、反馈进入 profile |
| MacroPhase | brief 质量、追问上下文、结构化沉淀、金融建议边界 |
| TradingAgents-CN | 多 Agent 分工、研究证据、风险声明、报告结构 |
| agent-scaffold-skill | provider 切换、tool policy、memory/eval 模板 |
| agent-builder-lab | 学习是否产生可复用、可验证的构建经验 |

## 行业参考

- [OpenAI Trace Grading](https://platform.openai.com/docs/guides/trace-grading): trace grading 将结构化分数或标签应用到 agent trace，用于评估 correctness、quality 和 adherence。
- [OpenAI Agent Evals](https://platform.openai.com/docs/guides/agent-evals): workflow-level 错误建议使用 trace grading。
- [LangChain Agent Evals](https://docs.langchain.com/oss/python/langchain/evals): agent evals 评估 execution trajectory，也就是消息和工具调用序列。
- [LangSmith Evaluate Complex Agent](https://docs.langchain.com/langsmith/evaluate-complex-agent): 同一 dataset 可以同时用于 final response 和 trajectory evaluation。
- [Langfuse Experiments via SDK](https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk): evaluator 接收 input、metadata、output、expected output，并把 metrics 写回 traces。
- [Braintrust Scorers](https://www.braintrust.dev/docs/evaluate/write-scorers): scorer 是评估输出质量的可复用函数。

## 当前原则

1. 先文件化、本地化、可版本控制，再接 SaaS 平台。
2. 先少量高价值 case，再扩展 benchmark。
3. 先保护安全、工具、记忆和调度边界，再追求复杂评分。
4. 结果评估用于验收，trace 评估用于诊断。
5. 项目经验先留在项目内，跨项目价值经证据和审批后再提升。
