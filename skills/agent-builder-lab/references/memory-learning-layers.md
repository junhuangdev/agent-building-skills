# Memory And Learning Layers

## 一句话结论

记忆、学习和评估必须分层：runtime 可以记住怎么执行，业务 Agent 必须记住业务怎么变好，评估系统必须记住什么变化导致能力变强或变弱。

## 为什么要分层

如果把所有记忆都放进 runtime，业务经验会被锁在某个宿主 Agent 里，换到 Codex、OpenCode、Hermes、OpenClaw 或自建 runtime 时会丢失。

如果把所有记忆都放进业务项目，执行层的通用经验会被业务噪音污染，很难跨项目复用。

正确做法是按所有权和用途分层。

## 记忆和学习层级

| 层 | 记忆什么 | 学习什么 | 所有者 |
| --- | --- | --- | --- |
| Runtime memory | 会话状态、工具结果、执行上下文、调度线索 | 怎么更好计划、调用工具、恢复、压缩上下文 | Codex / OpenCode / Hermes / 自建 runtime |
| Agent method memory | 构建 Agent 的原则、模板、边界、反模式 | 怎么构建更好的 Agent | `agent-builder-lab` / scaffold |
| Business memory | 业务事实、历史决策、领域 profile、用户业务偏好 | 怎么更好完成该业务目标 | 具体业务 Agent 项目 |
| Collaboration memory | 人机边界、交付偏好、风险习惯 | 什么时候问人、怎么交付、怎么验收 | project instructions / `vibeflow` |
| Eval memory | cases、baselines、失败模式、能力趋势 | 哪些变化让能力变好或变坏 | 项目 eval 系统 |

业务 Agent 不能把学习能力完全交给 runtime。Runtime 帮助“怎么执行”，业务层负责“这个业务怎么变好”。

## 机制层和内容层

判断一项能力是否应通用，先分清 mechanism 和 content。

| 能力 | 通用机制 | 业务内容 |
| --- | --- | --- |
| 记忆 | schema、生命周期、检索、写入审批、过期、提升流程 | 业务事实、领域 profile、用户偏好、历史判断 |
| 学习 | feedback intake、归因、promotion、archive、supersede | 什么反馈算好、哪些经验可复用、业务策略怎么变 |
| 评估 | case schema、runner、scorer interface、report、baseline diff | 任务集、rubric、阈值、业务成功标准 |
| 风险 | risk classes、approval gate、audit log | 哪些业务动作高风险、谁能批准 |
| 报告 | report layout、evidence fields、status taxonomy | 业务指标、字段、解释语言 |

因此，通用框架应该做机制，不应该吞掉业务内容。

## 通用能力应该做到哪一层

| 层 | 是否通用 | 建议 |
| --- | --- | --- |
| 文件布局 | 是 | 提供默认目录和命名 |
| schema | 是 | 定义最小字段，可扩展 |
| lifecycle | 是 | keep/promote/archive/reject/supersede |
| runner | 是 | 读取 case、执行命令、收集产物 |
| scorer interface | 是 | 统一输入输出，不统一评分逻辑 |
| report format | 是 | 统一摘要、证据、风险、回归 |
| business case | 否 | 每个 Agent 自己维护 |
| business rubric | 否 | 每个 Agent 自己维护 |
| business memory content | 否 | 留在业务项目 |
| promotion decision | 半通用 | 框架给流程，人决定是否提升 |

## 推荐架构

```text
business-agent/
  agent.yaml
  memory/
    profile.yaml
    decisions.jsonl
    feedback.jsonl
  learning/
    journal.md
    harvests/
  evals/
    cases/
    rubrics/
    baselines/
    reports/
  runtime-adapters/
    codex/
    opencode/
    hermes/
```

通用框架可以提供模板、schema、runner 和报告生成器。业务项目填入自己的 profile、decisions、cases、rubrics 和 thresholds。

## 业务记忆的典型类型

| 类型 | 例子 | 生命周期 |
| --- | --- | --- |
| Domain facts | 视频平台限制、宏观框架、数据源说明 | 可更新 |
| User taste | 喜欢的候选视频风格、报告偏好 | 可编辑 |
| Decisions | 为什么采用某个流程、为什么拒绝某个方案 | 长期保留 |
| Feedback | 采纳、拒绝、修改、人工原因 | 聚合后提升 |
| Profiles | `candidate_discovery_profile`、MacroPhase watchlist | 持续演化 |
| Baselines | 评估稳定版本、成功样例、失败样例 | 版本化 |

业务记忆不应默认进入宿主 Agent 的全局记忆。它应该在项目内可读、可改、可导出。

## 学习闭环

```text
business run
  -> structured result
  -> human feedback
  -> business memory update
  -> eval case or baseline update
  -> build journal entry
  -> harvest review
  -> project fix or shared promotion
```

只有跨项目可复用、证据足够、会改善未来 Agent 构建的经验，才提升到共享层。

## 是否要做通用框架

需要，但不要先做大平台。先做小框架。

| 阶段 | 目标 |
| --- | --- |
| Phase 1 | 文件化 schema + 模板 + 手动流程 |
| Phase 2 | 本地 CLI runner + report generator |
| Phase 3 | 通用 scorer interface + project scorer plugins |
| Phase 4 | runtime adapter + scenario regression |
| Phase 5 | 可选 UI / SaaS / 长期自动运行 |

不要一开始做完整 memory platform、workflow engine 或 universal agent runtime。先让 DubForge 和 MacroPhase 的真实业务闭环跑起来。

## 设计原则

1. 业务记忆留在业务项目，runtime 记忆只做执行辅助。
2. 通用框架提供机制，不拥有业务真相。
3. 业务学习必须能导出、迁移、评估，不能锁在某个宿主 Agent。
4. 评估 case 和 baseline 是学习系统的一部分，不只是测试。
5. 反馈先进入项目层，跨项目经验再经证据和审批提升。
6. 先做本地、文件化、可版本控制，再做自动化和平台化。

## 对当前项目的建议

| 项目 | 第一层落地 |
| --- | --- |
| DubForge | `candidate_discovery_profile` + feedback log + candidate eval cases |
| MacroPhase | structured notes + watchlist + brief baseline + financial-advice boundary cases |
| TradingAgents-CN | research report baselines + agent role feedback + risk disclaimer cases |
| agent-builder-lab | 记忆/学习/评估分层认知和 promotion 规则 |
| agent-scaffold-skill | schema、runner、adapter 和 eval 模板候选 |

当前最合适的路线是：先把通用机制沉淀成模板和小 CLI，再由每个业务 Agent 填入业务内容。
