# 第三方 Agent Runtime 下的能力演化边界

状态：工作版讨论笔记，不是最终总结。

结论：如果不自研 Agent Runtime，而是在第三方 Runtime 上构建混合型 Agent，我们控制不了内部认知机制，但仍然可以控制外部能力包；因此 `capability-evolution` 的默认落点应该是 `Skill + AGENTS.md + 项目文件 + 工具/CLI + eval + use record`，而不是假设能修改 Runtime 内部。

## 为什么这个问题重要

“能力演化系统”里的“能力”不能直接等同于 Skill。Skill 是重要载体，但 Agent 能力还可能落在 memory、policy、eval、tool、runtime adapter、业务模板和项目规则里。

但当我们使用第三方 Agent Runtime 时，可控面会变小。Runtime 内部的 planner、memory、context compression、tool scheduling、权限机制和 trace 机制通常不由我们直接控制。

因此需要区分两种架构：

| 架构 | 可控重点 | 风险 |
|---|---|---|
| 自研 Runtime | loop、memory、policy、tool、eval、trace 全链路 | 维护成本高，容易被基础设施拖住 |
| 第三方 Runtime + 外部能力包 | Skill、docs、项目文件、tools、eval、wrapper | 无法保证内部机制按我们的方式运行 |

## 第三方 Runtime 下仍然可控的层

| 层 | 是否可控 | 说明 |
|---|---|---|
| `Skill` | 高 | 最强的 procedural capability 入口，用来约束“怎么做” |
| `AGENTS.md` / 指导文件 | 高 | 轻量 bootstrap 和路由入口，不适合放复杂记忆 |
| 项目 memory 文件 | 高 | 保存业务事实、偏好、决策、反馈、use record |
| 项目 eval 文件 | 高 | 保存 cases、rubrics、baselines、reports |
| CLI / MCP / tools | 高 | 可以把确定性逻辑和业务动作放到工具侧 |
| wrapper / adapter | 中 | 可以在 Runtime 外层做前后处理、记录、校验 |
| Runtime 原生 memory | 低到中 | 取决于 Runtime 暴露能力，不能默认依赖 |
| Runtime 内部 loop | 低 | 通常不可控，除非 fork 或自研 |
| Runtime 内部 policy | 低到中 | 可用其配置，但难以完全定义自己的政策层 |
| Runtime change | 低 | 只能提 issue、fork、等待上游或更换 Runtime |

## 使用第三方 Runtime 的理由是否成立

这个理由成立，而且适合作为默认策略。

Agent Runtime 是高维护成本层，包含模型适配、工具调用、上下文管理、权限、沙箱、流式输出、恢复、UI、trace、供应商变化和生态集成。个人或小团队自研 Runtime，长期很难追上成熟开源项目或商业产品。

更务实的方式是：

```text
第三方 Runtime 负责执行 Agent
我们负责能力包和演化闭环
```

也就是借用 Runtime 的执行能力，但把长期资产留在我们可迁移、可审计、可版本控制的位置。

## 为什么很多 Agent 仍然自写 Runtime

大量 Agent 项目自写 Runtime，并不说明它们都能写出比 Codex、Claude Code 或其他官方 Agent 更强的通用执行层。更常见的原因是：Runtime 本身就是产品边界。

| 原因 | 说明 |
|---|---|
| 产品形态不同 | Coding Agent、个人助理、网关、自动化、研究 Agent 的 loop 不一样 |
| 工具和权限不同 | shell、浏览器、消息、文件、云任务等动作需要不同授权模型 |
| UX 不同 | TUI、IDE、Web、Slack、Telegram、Feishu、后台任务需要不同交互层 |
| 商业控制 | Runtime 是平台入口，产品通常不愿完全交给外部 SDK |
| 标准未稳定 | Agent loop、memory、skills、eval 还没有统一事实标准 |
| 生态适配 | MCP、provider、sandbox、plugin、channels 都需要胶水层 |
| 差异化能力 | 不同项目会把 memory、automation、code execution、gateway 或 collaboration 做成核心卖点 |

因此，“自写 Runtime”不等于“能力更强”。它只说明这个项目需要控制自己的产品执行层。真正需要评估的是这个 Runtime 在目标任务上的执行质量。

## 如何评估不同 Agent Runtime 的差距

不同 Agent Runtime 不能只按产品名气比较，也不能只看是否支持某个功能。更合理的方式是用同一组任务和同一套观测指标做评估。

| 评估层 | 看什么 | 为什么重要 |
|---|---|---|
| Task outcome | 同一任务是否完成 | 最终用户价值 |
| Tool execution | 工具选择、参数、错误恢复 | Runtime 核心差距 |
| Context control | 项目规则、文件、历史、压缩 | 长任务稳定性 |
| Memory / learning | 是否能正确复用和更新经验 | 长期能力 |
| Security / policy | 权限、沙箱、审批、隔离 | 是否能放心给它行动权 |
| Observability | trace、日志、diff、报告 | 能否调试和评估 |
| Extensibility | Skill、MCP、plugin、custom tool | 能否接入外部能力包 |
| Portability | 记忆、Skill、eval 能否导出 | 是否被 Runtime 锁死 |
| Maintenance | 社区、更新、模型适配 | 长期可用性 |

评估最好分两类：

| 评估方式 | 回答的问题 |
|---|---|
| Black-box product eval | 今天实际用哪个 Agent 更好 |
| Runtime-isolation eval | 尽量固定模型、任务和工具后，Runtime loop 本身强不强 |

第一类适合选工具。第二类适合判断某个 Runtime 是否值得作为长期基础层。

## 当前建议：不要押注单一 Runtime

当前更合理的策略不是“自己写一个通用 Runtime”，也不是“完全绑定某个第三方 Runtime”，而是：

```text
成熟第三方 Runtime 负责执行力
capability-evolution 负责可迁移的能力演化层
真实任务 eval 负责选择当前最适合的 Runtime
```

这意味着我们应该：

1. 先使用成熟 Runtime 承担执行层，例如 Codex、OpenCode、OpenClaw、Hermes 或其他同类系统。
2. 把长期能力资产放在 Runtime 外部，例如 Skill、AGENTS.md、项目 memory、eval cases、use records、lifecycle decisions、CLI / MCP hooks。
3. 为候选 Runtime 建同一套真实任务 eval，不靠感觉判断强弱。
4. 只在必要时写薄 wrapper，例如 context pack、use record、eval runner、artifact routing。
5. 只有当第三方 Runtime 无法满足关键能力，且 wrapper / Skill / tool 也补不了时，再考虑自研或 fork Runtime。

## 技术选型架构结论

当前结论：不自研完整通用 Agent Runtime。自研完整 Runtime 是庞大工程，涉及模型适配、tool calling、agent loop、context、memory、policy、trace、eval、UX、插件、沙箱、升级和安全维护。个人或小团队不适合把主精力放在这一层。

但“不自研 Runtime”不等于“不写任何 runtime 辅助代码”。我们仍然可以写薄 wrapper 和能力演化工具。

| 层 | 当前决策 | 说明 |
|---|---|---|
| 完整 Agent Runtime | 不自研 | 交给成熟第三方 Runtime |
| 通用 agent loop | 不自研 | 不做 planner、调度、工具回合、恢复全套机制 |
| 原生 memory 平台 | 不自研 | 不做 Runtime 内部黑盒记忆系统 |
| 权限 / 沙箱系统 | 不自研 | 使用 Runtime 或工具平台提供的能力 |
| context pack 生成 | 可以自研薄层 | 为第三方 Runtime 准备输入上下文 |
| use record 记录 | 可以自研薄层 | 记录学习产物是否被使用 |
| eval runner | 可以自研薄层 | 比较不同 Runtime 和能力包效果 |
| artifact router | 可以自研薄层 | 决定学习产物写到项目、Skill、全局候选或 runtime candidate |
| Skill / AGENTS 集成 | 应该自控 | 这是第三方 Runtime 下最可迁移的入口 |
| CLI / MCP hooks | 按需自控 | 承载确定性动作、校验和报告 |

最小架构可以表达为：

```text
third-party Agent Runtime
  <- reads / uses
capability package
  - Skill
  - AGENTS.md pointer
  - memory files
  - eval cases
  - use records
  - lifecycle decisions
  - optional CLI / MCP hooks
  - optional thin wrapper
```

这个架构的目标是避免两个风险：

1. 被自研 Runtime 的基础设施复杂度拖住。
2. 把长期学习资产锁进某个第三方 Runtime 的私有记忆或黑盒机制里。

因此，技术选型上的默认路线是：

```text
Use mature runtimes.
Own portable capability artifacts.
Evaluate runtime fit with real tasks.
Only build thin adapters where needed.
```

## 推荐架构

```text
capability package
  + Skill
  + AGENTS.md pointer
  + project memory files
  + use records
  + eval cases
  + lifecycle decisions
  + optional CLI / MCP hooks
  + optional runtime adapter
```

其中：

| 资产 | 默认 owner | 作用 |
|---|---|---|
| Skill | capability package 或具体 Skill 包 | 方法能力和触发规则 |
| AGENTS.md | 项目 | 引导 Runtime 发现能力入口 |
| memory items | 项目或 Agent 包 | 保存业务事实、偏好、经验、决策 |
| use records | 项目 | 记录哪些产物被使用，以及是否有效 |
| eval cases | 项目或共享模板 | 检查能力是否真的变强 |
| lifecycle decisions | 项目或全局候选区 | 管理 active、watch、archive、superseded、rejected |
| CLI / MCP | 项目或工具包 | 承载确定性动作、校验、报告和外部集成 |

## 对 capability-evolution 的设计含义

`capability-evolution` 不应该假设自己能修改 Runtime 内部。它应该优先支持外部可控面：

1. 识别这次运行产生了什么学习候选。
2. 判断候选属于 Skill、memory、policy、tool、eval、runtime candidate 还是 domain template。
3. 把产物写到可维护 owner 里。
4. 在后续任务中通过 Skill、AGENTS.md、context pack、tool 或 eval 使用它。
5. 记录 use result。
6. 用 eval 和反馈决定保留、更新、提升、归档或拒绝。

如果某个 Runtime 暴露更强 hooks，可以接入；但 v1 不应依赖这些 hooks。

## 当前开放问题

| 问题 | 为什么还没定 |
|---|---|
| `context_pack` 由谁生成 | 第三方 Runtime 可能没有 before_run hook，需要外部 wrapper 或 Skill 内部流程 |
| use record 如何自动化 | 不同 Runtime 的 trace 能力差异很大 |
| eval 是离线跑还是任务内跑 | 取决于 Agent 类型和成本 |
| Skill 能否足够约束行为 | 需要用具体 Runtime 做试验 |
| Runtime 原生 memory 是否接入 | 取决于是否可导出、可隔离、可审计 |

## 当前判断

当前应继续采用“第三方 Runtime 优先，外部能力包自控”的路线。自研 Runtime 只在第三方 Runtime 无法满足关键能力、或外部能力包无法表达必要边界时再考虑。

这篇笔记适合留在 `notes/`。等 `capability_artifact`、`memory_eval_case`、`use_record` 和 Runtime adapter 边界定稿后，再提升到 `docs/`。

## 参考来源

- DeepSeek AI, [awesome-deepseek-agent](https://github.com/deepseek-ai/awesome-deepseek-agent)
- OpenAI, [Codex cloud docs](https://developers.openai.com/codex/cloud)
- Nous Research, [Hermes Agent docs](https://hermes-agent.nousresearch.com/docs/)
- OpenClaw, [Capabilities overview](https://docs.openclaw.ai/tools)
- OpenClaw, [Gateway security](https://docs.openclaw.ai/gateway/security)
- OpenCode, [OpenCode docs](https://opencode.ai/docs/)
