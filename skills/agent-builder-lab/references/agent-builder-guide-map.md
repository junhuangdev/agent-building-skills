# Agent Builder Guide Map

## 一句话结论

构建我们需要的 Agent 时，先判断 Agent 形态，再定义业务操作模型，然后补齐记忆学习、评估、运行时适配和经验沉淀。

## 阅读顺序

| 顺序 | 文档 | 回答的问题 |
| --- | --- | --- |
| 1 | `composite-business-agent.md` | 这是自建 runtime Agent，还是组合型业务 Agent |
| 2 | `business-agent-operating-model.md` | 业务 Agent 应该有哪些固定操作能力 |
| 3 | `capability-reference-and-output-mining.md` | 怎么从外部 Agent 的过程和产出提炼本地契约 |
| 4 | `business-agent-build-procedure.md` | 按什么步骤构建第一版可执行业务 Agent |
| 5 | `business-agent-package-contract.md` | 每个文件和字段应该怎么写、怎么检查 |
| 6 | `runtime-portable-business-agent.md` | 怎么避免绑定在某一个 runtime 上 |
| 7 | `memory-learning-layers.md` | 记忆、学习、评估分别归哪一层 |
| 8 | `agent-evaluation-cognition.md` | 怎么评估 Agent 和业务闭环是否变强 |
| 9 | `build-journal.md` | 构建过程中哪些经验要记录 |
| 10 | `memory-lifecycle.md` | 经验如何保留、提升、归档、遗忘 |
| 11 | `harvest-and-promotion.md` | 哪些经验能提升到项目、scaffold、vibeflow 或 eval 模板 |

## 构建流程

```text
agent idea
  -> choose agent shape
  -> define operating model
  -> mine external capability outputs when capability design is uncertain
  -> copy business-agent package template
  -> fill agent contract / actions / artifacts / evals / adapter
  -> check package contract
  -> define business memory and learning loop
  -> define eval scenarios and rubrics
  -> choose runtime adapter
  -> build first real workflow
  -> record lessons
  -> harvest and promote
```

## 形态判断

| 问题 | 倾向 |
| --- | --- |
| 需要完整控制 loop、tool dispatch、memory、trace | 自建 runtime Agent |
| 主要依赖 Codex/OpenCode 等宿主完成调度 | Composite Business Agent |
| 业务状态、CLI、报告、人工验收更重要 | Composite Business Agent |
| 需要长期无人值守、多租户、平台化交付 | 自建 runtime Agent |
| 还在验证业务闭环 | Composite Business Agent 优先 |

## 必须定义的业务 Agent 资产

| 资产 | 最小要求 |
| --- | --- |
| Agent contract | mission、non-goals、allowed actions、risk boundary |
| Business run | run_id、goal、stage、status、artifacts、decisions |
| Action registry | action schema、risk、permission、input/output |
| Artifact contract | type、source、status、evidence、summary |
| Human gate | action、risk、decision、reason |
| Memory | profile、decisions、feedback |
| Eval | scenarios、rubrics、baselines、reports |
| Delivery | result、evidence、risks、gates、next action |

## 第一版构建命令

```bash
cp -R ~/.codex/skills/agent-builder-lab/assets/templates/business-agent ./business-agent
python ~/.codex/skills/agent-builder-lab/scripts/check_business_agent_package.py ./business-agent
```

复制后先填写模板内容，再扩展目录。结构检查通过只代表具备第一版实现入口，不代表业务质量已经通过。

## 外部能力参照命令

```bash
cp ~/.codex/skills/agent-builder-lab/assets/templates/capability-reference-study.yaml ./capability-reference-study.yaml
```

研究 memory、eval、tool、risk、runtime state 等基础能力时，先填这份 study。重点不是摘录资料，而是拆出外部系统的 output objects、字段、生命周期、所有权、验证方式和可迁移性。

## 通用和业务自有边界

| 层 | 通用 | 业务自有 |
| --- | --- | --- |
| Operating model | run/action/artifact/gate 流程 | 具体状态、动作、产物 |
| Memory | schema、lifecycle、promotion | 业务事实、profile、偏好 |
| Evaluation | case schema、runner、report | scenario、rubric、threshold |
| Risk | risk classes、approval format | 风险标准、批准人 |
| Runtime | adapter contract | runtime 选择和限制 |

## 当前文档缺口

| 缺口 | 说明 | 建议 |
| --- | --- | --- |
| Concrete project example | DubForge 或 MacroPhase 的最小实例 | 先选一个项目试点 |
| Semantic checker | 当前脚本只检查最低结构，不检查跨文件语义 | 等真实样例跑完后扩展 |
| HTML reading layer | 人类友好的阅读版 | 内容稳定后从 Markdown 生成 |

## 当前推荐路线

1. 先用 `business-agent-build-procedure.md` 创建第一套业务 Agent package。
2. 用 `check_business_agent_package.py` 做结构检查。
3. 对不确定的通用能力，用 `capability-reference-and-output-mining.md` 做外部参照。
4. 选择 DubForge 或 MacroPhase 跑一次真实业务任务。
5. 把真实摩擦写入 `agent-build-journal.md`。
6. 根据真实摩擦扩展 semantic checker、模板或 runtime adapter。
7. 内容稳定后再决定是否生成 HTML 阅读版。

## 使用原则

不要先设计万能平台。先让一个真实业务 Agent 用这套文档跑通：

```text
one real business workflow
  -> business-agent package
  -> structured run
  -> artifact
  -> human gate
  -> eval scenario
  -> feedback
  -> journal
```

当这个闭环跑通后，再决定哪些机制需要提升成通用框架。
