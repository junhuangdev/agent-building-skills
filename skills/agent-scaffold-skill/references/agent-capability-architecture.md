# Agent 能力架构全览

本文档基于对 OpenClaw、Hermes Agent、Codex 等成熟 AI Agent 产品的深度分析，系统梳理一个完整 AI Agent 需要具备的全部能力。

## 核心理念

**Agent 不是"调一次大模型就完"。** Agent 的本质是一个持续运行的 orchestration 循环，模型负责决策，框架负责执行、记忆、安全、观测。

大模型是**纯函数**（无状态 HTTP 请求），不记得任何事。Agent 系统替模型维护一切状态和记忆。

---

## 能力全景图

```
                     ┌──────── Observability (trace + cost) ────────┐
                     │                                               │
   User / Channel ──→│  Agent Loop ──→ Tool Calls ──→ Sandbox       │
                     │      │                                        │
                     │      ├─ Streaming (逐字输出)                   │
                     │      ├─ Structured Output (JSON Schema 约束)   │
                     │      ├─ Error Recovery (错误喂回模型自修复)     │
                     │      └─ Sub-agent Spawn (并行子 agent)        │
                     │                                               │
                     └── Memory System ──────────────────────────────┘
                          ├─ MEMORY.md (push, 硬上限强制蒸馏)
                          ├─ Daily Notes (pull, 自然过期)
                          ├─ Vector Search (语义检索)
                          ├─ Dreaming (后台自动提炼)
                          ├─ Memory Wiki (结构化编译知识库)
                          ├─ Session Search (全文回放历史对话)
                          └─ Compaction (对话压缩防止 token 爆炸)

                     ┌── Skill System (程序性记忆) ──────────────────┐
                     │   SKILL.md × 渐进披露 × Hub 分发              │
                     │   Agent 自建 × 条件激活 × Bundles             │
                     └──────────────────────────────────────────────┘
```

---

## 1. Agent Loop（运行时核心）

### 1.1 基本形态

Loop 就是一个 `for` 循环：

```
调模型 → 模型说要调工具？ → 执行工具 → 结果塞回上下文 → 再调模型 → ...
                                                   ↑                │
                                                   └──循环───────────┘
```

模型不调工具了（`finish_reason: stop`）= 循环终止。这不是模型说"结束"，是模型的下一个动作不是调工具。

### 1.2 动态控制

Loop 控制不当纯靠硬编码。应该给模型注册控制类工具，让模型参与决策：

| 控制工具 | 含义 |
|---|---|
| `finish_task` | 任务完成，返回最终结果 |
| `abandon_task` | 遇到无法解决的问题，放弃 |
| `request_human_help` | 需要人工介入 |
| `sessions_yield` | 主动暂停当前 turn，等子 agent 完成事件 |

三个终止条件：模型主动结束（`finish_reason: stop`）/ 轮次上限兜底 / policy gate 拦截。

### 1.3 与子 Agent 的关系

子 agent 对主 agent 而言只是一个 tool handler，内部跑了一个完整的 agent loop。区别仅在于输入来源和输出去向不同，loop 代码是一样的。

---

## 2. Provider Adapter（模型适配层）

### 2.1 OpenAI-compatible 协议

OpenAI 的 Chat Completions API 已经成为事实标准。国内 DeepSeek、Kimi、豆包、通义千问等只要说"OpenAI-compatible"就是完全兼容这套协议。

协议约定内容：
- 端点：`POST /chat/completions`
- 鉴权：`Authorization: Bearer <key>`
- 角色：`system` / `user` / `assistant` / `tool`
- 工具定义：`{"type": "function", "function": {"name", "description", "parameters"}}`
- 工具调用返回：`tool_calls` 数组，参数为 JSON 字符串
- 结束信号：`finish_reason`: `stop` / `tool_calls` / `length`
- 用量：`usage.prompt_tokens` / `completion_tokens`

### 2.2 适配器架构

不同 provider 的协议格式不同（Claude 不是 OpenAI 格式，Gemini 原生也不一样）。每个 provider 有自己的 adapter 类，负责把内部的 `ToolSpec` 翻译成对应格式。Agent loop 不碰这些差异。

Capability flag（`config/capabilities.yaml`）标记每个 provider 的能力：`tool_calling` / `streaming` / `json_schema` / `reasoning` 等。未知能力标记为 `false` 或 `experimental`。

---

## 3. Memory 系统（多层叠加，不只是"存文件"）

### 3.1 两层根本区别

对所有记忆内容，模型**不是主动去文件系统找东西**。模型是纯函数，接收 prompt，产出文本。所有"模型读了文件"都是运行时代码在发请求前先读了文件塞进 prompt。

### 3.2 加载方式

- **push**：运行时主动注入 prompt（MEMORY.md、AGENTS.md、skill 索引、provider auto-prefetch）。模型被动接收
- **pull**：模型通过工具调用获取（`memory_search`、`skill_view`、`session_search`）

### 3.3 存储分层

| 层 | 形态 | 用途 | 加载方式 |
|---|---|---|---|
| **MEMORY.md** | 纯文本，硬上限 2,200 字符 | 持久事实、偏好、决策 | push，每次 session 自动注入 |
| **Daily Notes** | `memory/YYYY-MM-DD.md` | 每日工作草稿 | push（今昨两天）+ pull（更早的按需搜索） |
| **向量语义搜索** | SQLite + sqlite-vec | 语义近似匹配（"网关机器" → "跑 OpenClaw 的服务器"） | pull，通过 `memory_search` |
| **Session Search** | SQLite FTS5 全文索引 | 搜历史对话原文 | pull |
| **Dreaming** | 后台子 agent 自动跑 | 从短期记忆提炼到长期 | 自动，不需人干预 |
| **Memory Wiki** | 编译后的结构化知识库 | claims/evidence/来源溯源/冲突检测 | pull |
| **Skills** | SKILL.md 文件 | 程序性记忆（工作流程） | push（索引）+ pull（完整内容按需加载） |

### 3.4 向量语义搜索原理

不是对话模型做搜索。是专门的 embedding 小模型把文本变成一串 1536 维数字（向量）。搜索时纯数学算向量夹角，不调 AI。向量搜索和文本搜索（BM25）两条路并行，结果加权合并。

### 3.5 遗忘机制

**遗忘不是 bug，是刻意的设计特征。**

| 机制 | 方式 |
|---|---|
| 硬上限 | MEMORY.md 硬限制字符数，满了必须合并/删除 |
| 自然过期 | Daily notes 只自动注入今昨两天，更早的不主动注入 |
| 自动淘汰 | Dreaming 后台打分，不够格的淘汰 |
| 压缩衰减 | 每轮 compaction 信息密度上升，信息量下降 |

### 3.6 对话压缩（Compaction）

不是模型自己会压缩。是你自己调一次 API："把上面对话压缩成一段摘要"，模型返回摘要，你把摘要替换掉旧内容。每压缩一次信息就丢失一层，所以需要在压缩前先把关键事实存到外置记忆（memory flush）。

---

## 4. Skill 系统（程序性记忆）

### 4.1 核心概念

Skill 是 `SKILL.md` 文件——一个带有 YAML frontmatter 的 Markdown 文档，描述**怎么做一个工作流程**。遵循 agentskills.io 开放标准，OpenClaw/Hermes/Codex 都兼容。

### 4.2 关键机制

- **渐进披露**：Level 0 只有 name + description 索引（~3k tokens），用到时才加载完整内容。100 个 skill 的 token 成本是**对数级**的
- **条件激活**：fallback skill 只在特定工具不可用时出现，`requires_toolsets` / `fallback_for_toolsets`
- **Agent 自建**：agent 完成任务后自己调 `skill_manage.create()` 把经验保存为 skill
- **多源分发**：skills.sh / ClawHub / LobeHub / OpenAI/Anthropic 官方仓库 / 自定义 GitHub tap
- **安全扫描**：安装时自动扫描数据泄露、prompt 注入、供应链攻击

---

## 5. 安全与沙箱

### 5.1 多层架构

安全不是单一机制，是四层叠加：

```
外层: OS/Docker Sandbox（物理隔离执行环境）
中层: Tool Policy（deny 危险工具，如 exec/browser/web_search）
内层: Exec Approvals（即使工具可用，高风险命令需人工确认）
底层: Channel Allowlist（谁能触发 agent）
```

### 5.2 Codex 做法

平台原生 sandbox：macOS Seatbelt / Linux bubblewrap / Windows Sandbox。三层模式：`read-only` → `workspace-write`（默认）→ `danger-full-access`。approvals：`on-request`（默认）、`never`、`untrusted`。

### 5.3 OpenClaw 做法

Docker/SSH/OpenShell 三种后端。scope 控制隔离粒度（session / agent / shared）。`workspaceAccess` 控制可见性（none / ro / rw）。子 agent 默认无 message 工具、无 session 工具。

---

## 6. Sub-agent 协作

### 6.1 基本模型

Sub-agent 就是一个独立的 agent session，通过 tool handler 启动。对主 agent 而言它只是一个名为 `sessions_spawn` 的工具。主 agent 传 task，子 agent 跑完回传 result。

### 6.2 关键设计

- **隔离**：子 agent 有独立 session、独立上下文、独立工具集（去掉了 messaging/session 类工具）
- **并发**：全局 lane 上限，父 session 最多活跃子数限制
- **嵌套**：支持 orchestrator → workers 二级嵌套
- **结果回传**：announce 机制，完成时推回父 session
- **模型选择**：通常给子 agent 用更便宜的模型
- **上下文污染控制**：子 agent 的 noisy 中间输出（日志、堆栈）不污染主 agent，只返回摘要

### 6.3 通信协议

Agent 间通信的**包装层**（status、runtime、tokens）由框架硬编码，**内容层**（task 描述、result 正文）由模型生成。模型只知道调了个 tool、拿到了字符串结果，不知道中间发生了什么。

---

## 7. 文件编辑

### 7.1 工具矩阵

| 工具 | 做什么 |
|---|---|
| `read` | 读文件，带行号前缀输出 |
| `write` | 创建或全量替换文件 |
| `edit` | search-and-replace——"找到这段文本，替换成那段" |
| `apply_patch` | 多文件 diff 格式批量编辑 |
| `exec` / `terminal` | 跑 shell 命令 |

### 7.2 核心设计

不是用行号编辑——是 search-and-replace。模型看到带行号的文件内容，决定改哪里，把**原文定片段**作为 `old_string` 传过去，框架做精确匹配替换。模型只改动了的那几行，不需要重新生成整个文件。

多 agent 并发写文件靠 sandbox 隔离和 `apply_patch` 原子化。

---

## 8. 可观测性

| 层 | 做什么 |
|---|---|
| **Trace id** | 贯穿 agent loop + 子 agent 的每次工具调用 |
| **Session transcript** | 完整对话记录存磁盘（`*.jsonl`） |
| **Token/cost 追踪** | 每轮 API 调用记录 usage |
| **OpenTelemetry** | 标准化的 trace + metrics 输出 |

---

## 9. 流式响应（Streaming）

模型不是等完整答案才返回，而是一个字一个字吐 SSE 事件流。Agent loop 里逐 chunk 接收——`delta.content` 逐字显示，`delta.tool_calls` 增量组装 tool call 参数。Provider adapter 归一化不同提供商的 chunk 格式差异。

---

## 10. 结构化输出（Structured Output）

强制模型按 JSON Schema 返回，不返回自由文本。capability flag 控制——OpenAI 用 `json_schema` strict 模式，DeepSeek 降级到 `json_object` 或 `experimental`。

---

## 11. 错误恢复

不是替模型做决策，是把错误信息原样喂回去让模型自己判断。四层处理：

| 层 | 策略 |
|---|---|
| 工具调用失败 | 错误信息作为 tool result 返回，模型读 stderr 决定重试还是换参数 |
| 模型 API 超时 | 重试 + 指数退避 |
| 子 agent 崩溃 | 孤儿恢复——重启后发 resume 消息 |
| loop 跑飞 | `max_tool_rounds` 硬上限兜底 |

---

## 完整能力清单

| # | 能力 | 核心要点 |
|---|---|---|
| 1 | Agent Loop | 调模型→工具→调模型的循环，控制信号可交还给模型决定 |
| 2 | Provider Adapter | 隔离 provider 差异，capability flag 抽象能力 |
| 3 | Tool Schema | JSON Schema 描述工具，OpenAI 格式是事实标准 |
| 4 | Policy Gate | 五级风险（low/external/destructive/permission/money），执行前拦截 |
| 5 | MEMORY.md（push 记忆） | 硬上限强制蒸馏，自动注入 prompt |
| 6 | Daily Notes（pull 记忆） | 今昨两天自动注入，更早的按需检索 |
| 7 | 向量语义搜索 | embedding 小模型向量化 + 纯数学算夹角，不调对话模型 |
| 8 | Dreaming（自动提炼） | 后台子 agent 打分筛选，自动从短期升级到长期记忆 |
| 9 | Memory Wiki（结构化知识库） | claims/evidence/来源溯源/冲突检测 |
| 10 | Session Search | SQLite FTS5 全文搜索历史对话 |
| 11 | Compaction（对话压缩） | 调模型总结旧对话，压缩前预存关键事实到外置记忆 |
| 12 | Skill 系统 | SKILL.md 程序性记忆，渐进披露控制 token |
| 13 | Sandbox（沙箱） | OS/Docker/SSH 多层隔离，workspace 访问控制 |
| 14 | Tool Policy | 全局/按 agent 禁止危险工具 |
| 15 | Exec Approvals | 高风险命令人工确认，allowlist 白名单 |
| 16 | Channel 网关 | pairing/allowlist 控制谁能触发 agent |
| 17 | Sub-agent 协作 | 独立 session，并行执行，结果回传 |
| 18 | 文件编辑 | read+edit(search-and-replace)+apply_patch(diff) |
| 19 | Streaming | SSE 逐字输出 + tool call 增量组装 |
| 20 | Structured Output | JSON Schema 强制约束模型输出 |
| 21 | Error Recovery | 错误信息喂回模型自修复 + 硬上限兜底 |
| 22 | Observability | trace + token/cost + session transcript |
| 23 | 遗忘机制 | 硬上限/自然过期/自动淘汰/压缩衰减 |

---

## 参考

本分析基于以下产品的官方文档和源码：
- OpenClaw（TypeScript，开源）：universal AI gateway + personal assistant
- Hermes Agent（Python，开源）：self-improving agent with skills + memory
- Codex（Rust，开源）：OpenAI coding agent with sandbox
