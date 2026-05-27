# Runtime Portable Business Agent

## 一句话结论

可移植的 Business Agent 不把业务能力绑定在某个宿主 Agent 里，而是把业务契约、状态、产物、评估和人审留在项目内，再用 adapter 映射到不同 runtime。

## 核心判断

Runtime 可以替换，业务契约不能漂移。

```text
business-agent package
  -> runtime adapter
  -> host runtime
  -> external collaboration trace
  -> project-owned artifacts / memory / evals
```

对于 Composite Business Agent，Codex、OpenCode、Hermes、OpenClaw 或自建 runtime 都只是执行宿主。真正的业务 Agent 由项目内的 contract、actions、artifacts、memory、evals、reports 和 human gates 共同定义。

## 所有权边界

| 能力 | Runtime 所有 | 业务项目所有 |
| --- | --- | --- |
| 模型推理 | yes | no |
| 隐藏规划过程 | usually yes | no |
| 文件和命令执行 | runtime 提供能力 | project 定义允许范围 |
| 业务状态 | no | yes |
| 业务记忆 | no | yes |
| 业务产物 | no | yes |
| 人审规则 | no | yes |
| eval 场景 | no | yes |
| 交付格式 | no | yes |

如果一个业务能力只能靠某个 runtime 的隐藏上下文维持，它就还不可移植。

## Adapter Contract

每个 runtime target 都需要一个 adapter：

```text
runtime-adapters/
  codex.yaml
  opencode.yaml
  hermes.yaml
  self-built.yaml
```

每个 adapter 至少回答：

| 字段 | 问题 |
| --- | --- |
| `runtime` | 运行在哪个宿主上 |
| `invocation` | 人或系统如何启动 |
| `skill_trigger` | 需要加载哪些 Skill、AGENTS.md 或规则 |
| `capability_map` | 这个 runtime 稳定支持什么 |
| `unsupported_actions` | 不能依赖什么 |
| `handoff_rules` | 状态、证据和风险如何回写项目 |

## Capability Map

建议按这些能力描述 runtime：

| 能力 | 判断 |
| --- | --- |
| file_read | 能否稳定读取项目文件 |
| file_write | 能否在项目范围内写文件 |
| command_run | 能否运行本地命令 |
| browser_use | 能否操作或检查浏览器 |
| external_api | 能否调用外部 API |
| long_running | 能否长期无人值守运行 |
| scheduled_run | 能否定时触发 |
| hidden_trace | 能否拿到内部完整 trace |
| external_trace | 能否记录外部协作轨迹 |
| persistent_memory | 是否有可靠持久记忆 |
| human_gate | 能否在风险点停下来等人 |

不要把 unknown 写成 supported。写清楚 unsupported 比假设能力存在更重要。

## Codex Adapter 第一版

Codex 适合第一版 Composite Business Agent，因为它能稳定完成项目文件、命令、编辑、报告和交付协作。

但 Codex adapter 要明确：

| 项 | 结论 |
| --- | --- |
| hidden trace | 不可依赖 |
| business memory | 必须写入项目文件 |
| eval | 用 scenario、脚本、人工 rubric 评估外部行为 |
| human gate | 通过对话和项目规则触发 |
| portability risk | 不要把能力写死成 Codex 独有命令 |

## 添加一个新 Runtime

按这个顺序做：

1. 复制 `runtime-adapters/codex.yaml` 为新 runtime。
2. 填写 invocation。
3. 填写 capability_map。
4. 明确 unsupported_actions。
5. 写 handoff_rules。
6. 用同一个 smoke scenario 跑一次。
7. 比较 delivery package 和 artifacts 是否等价。
8. 把差异写入 adapter，不要改业务 contract 来迁就 runtime。

只有当业务 contract 本身错了，才修改 `agent.yaml`、actions、artifacts 或 evals。

## 自建 Runtime 的位置

当出现这些情况，可以考虑自建 runtime：

| 信号 | 原因 |
| --- | --- |
| 需要长期无人值守 | 宿主对话式 runtime 不稳定 |
| 需要完整 trace | 黑盒宿主不足以审计 |
| 需要多租户产品化 | 项目级 package 不够 |
| 需要严格 tool dispatch | 宿主调度不可控 |
| 需要可重复自动 eval | 手工协作成本过高 |

即使自建 runtime，业务层 contract 仍应保留。自建 runtime 是执行层替换，不是业务 Agent 重新定义。

## Portability Check

一个 Business Agent 具备初步可移植性，至少满足：

| 检查 | 通过标准 |
| --- | --- |
| 状态归属 | 业务状态写入项目文件或系统 |
| 产物归属 | artifact 不只存在聊天里 |
| 记忆归属 | business memory 不依赖宿主隐藏记忆 |
| 评估归属 | eval scenarios 在项目里 |
| 风险归属 | human gates 在 contract 里 |
| adapter | runtime 支持和不支持都明确 |
| smoke | 同一业务目标可在至少一个 runtime 上跑通 |

## 反模式

- 把 Codex 当前对话当成业务 Agent 的唯一状态。
- 把宿主 Agent 的强能力当成业务 contract。
- 为了迁就 runtime，弱化业务 evidence、artifact 或 human gate。
- 只写 Skill，不写 action、artifact、eval 和 delivery。
- 只评估最终聊天回答，不评估外部 trace 和项目产物。
