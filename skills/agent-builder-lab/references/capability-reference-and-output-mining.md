# Capability Reference And Output Mining

## 一句话结论

研究 Agent 能力时，不只参考别人怎么做，更要抽取别人最终沉淀了什么对象，再把稳定相似的对象转成我们的 schema、template、checker、eval 或 memory rule。

## 使用场景

当我们要研究或改进某个 Agent 基础能力时使用这份方法：

| 能力 | 示例问题 |
| --- | --- |
| Memory | 记忆应该分几层，怎么写入、召回、过期 |
| Learning | 经验怎么从运行结果提升成长期规则 |
| Evaluation | 怎么评估分项能力和整体结果 |
| Tool use | tool/action 怎么注册、授权、验证 |
| Runtime state | run、session、checkpoint、trace 怎么保存 |
| Risk | 风险怎么分级，哪些动作要人审 |
| Collaboration | 人机协作结果怎么交付、验收、回写 |

不要把这份方法用于一次性资料摘录。它只用于会影响未来 Agent 构建方式的能力研究。

## 核心方法

```text
external concrete systems
  -> process observation
  -> output anatomy
  -> invariant extraction
  -> local contract
  -> field trial
  -> validated lesson
  -> promoted artifact
```

关键点：`output anatomy` 和 `local contract` 是中心。没有产出对象，就没有可复用沉淀。

## 为什么产出比过程更重要

过程容易受 runtime、模型、UI、团队习惯影响。产出更稳定，更容易比较。

| 只看过程的问题 | 看产出的价值 |
| --- | --- |
| 容易模仿表面流程 | 能看到真正被系统保存和复用的对象 |
| 难以判断通用性 | 可以比较字段、生命周期、所有权 |
| 难以转成 AI 可执行指南 | 可以直接变成 schema、template、checker |
| 容易停在认知总结 | 可以进入真实项目验证 |

例如 memory 能力，不要只看“它什么时候写记忆”。还要看它最终保存的是 memory block、checkpoint、state snapshot、memory content、namespace store，还是 feedback log。

## 参考对象选择

每次研究至少选择 3 个参考对象。优先使用官方文档、源码或可运行示例。

| 类型 | 用途 |
| --- | --- |
| Runtime / SDK | 看执行循环、trace、state、tool、eval |
| Memory-first agent | 看长期记忆、分层、召回、编辑、遗忘 |
| Workflow framework | 看 checkpoint、resume、human-in-loop、state |
| Business agent product | 看协作、交付、人审、业务产物 |

如果某个参考对象没有清楚产出，只能作为弱证据。

## 采集模板

每个参考对象都按同一结构记录：

```yaml
reference:
  name:
  source:
  capability:
  observed_process:
    - trigger:
      action:
      decision:
      stop_condition:
  output_objects:
    - name:
      purpose:
      owner:
      fields:
        - name:
          meaning:
      lifecycle:
        - created
        - updated
        - retrieved
        - archived
      quality_signal:
      portability_note:
  useful_patterns:
    - pattern:
      evidence:
      reusable_scope:
  rejected_patterns:
    - pattern:
      reason:
```

模板文件见 `assets/templates/capability-reference-study.yaml`。

## Output Anatomy

对每个外部系统，至少拆这几项：

| 维度 | 要问的问题 |
| --- | --- |
| Object | 它最终保存了什么对象 |
| Field | 对象有哪些关键字段 |
| Owner | 谁拥有这个对象，runtime、项目、用户还是 agent |
| Lifecycle | 什么时候创建、更新、读取、归档、删除 |
| Trigger | 什么事件触发这个对象变化 |
| Validator | 怎么判断对象有效 |
| Consumer | 后续谁会读取它 |
| Failure | 如果对象丢失或错误，会造成什么失败 |
| Portability | 换 runtime 后这个对象还能不能成立 |

只有能回答这些问题的产出，才适合进入我们的契约层。

## Invariant Extraction

比较多个参考对象后，只提炼稳定相似点。

| 稳定相似 | 可以提升 |
| --- | --- |
| 多个系统都有 run/session/thread 概念 | 抽成 `business run` 或 `runtime session` |
| 多个系统都有 checkpoint/state snapshot | 抽成 `state checkpoint` 或 `run snapshot` |
| 多个系统都把记忆分 active/context 和 long-term/store | 抽成 memory layer contract |
| 多个系统都有 trace/grader/eval report | 抽成 eval evidence contract |
| 多个系统都有 action/tool schema 和 risk gate | 抽成 action registry 和 human gate |

不要提升：

- 某个产品的 UI 习惯。
- 某个 provider 的私有字段。
- 只出现一次、没有真实价值证据的技巧。
- 只适合某个业务的 taste 或私有数据。

## Local Contract

把外部相似点转成我们的本地契约时，只能落到这些位置：

| 落点 | 用途 |
| --- | --- |
| `references/*.md` | 方法、判断规则、能力边界 |
| `assets/templates/*.yaml` | 可复制结构化对象 |
| `scripts/*.py` | 可自动检查或汇总的规则 |
| `evals/*.yaml` | 可重复验证的 scenario |
| `docs/agent-build-journal.md` | 真实项目试点经验 |
| project-local memory | 业务自有经验 |
| approval package | 准备提升到全局 Skill 或其他系统 |

如果一个外部经验不能落到任何位置，先作为 reference only，不要强行吸收。

## Field Evolution

字段本身也是学习对象。不要一次性固定最终字段，也不要让字段自由漂移。

使用三层成熟度：

| 成熟度 | 含义 | 允许动作 |
| --- | --- | --- |
| `observed` | 单次研究中发现某字段可能有用 | 留在本次 study，不改模板 |
| `candidate` | 多来源相似或一次高影响失败证明字段缺失 | 加到模板的 candidate section，或起 approval package |
| `stable` | 经过 field trial 或重复使用证明能改善后续构建 | 进入核心模板、schema 或 checker |

字段闭环：

```text
field gap
  -> observed field
  -> candidate field
  -> field trial
  -> stable field or rejected field
  -> template / schema / checker update
  -> next study uses the improved contract
```

每个新增字段必须回答：

| 问题 | 目的 |
| --- | --- |
| 解决哪个判断缺口 | 防止字段装饰化 |
| 哪些参考或试点支持它 | 防止单点泛化 |
| 属于核心、能力、项目还是实验字段 | 防止层级混乱 |
| 谁会读取这个字段 | 防止无人消费 |
| 如何验证它改善了学习或构建 | 防止不可证伪 |
| 如果不保留会重复什么失败 | 防止字段堆积 |

字段变更审批：

| 变更 | 等级 | 处理 |
| --- | --- | --- |
| study 内新增 `observed` 字段 | auto | 当前 study 自主记录 |
| 模板新增可选 `candidate` 字段 | propose | AI 提建议，用户确认后改模板 |
| checker / schema 新增必填字段 | approval | 必须说明迁移和兼容 |
| 删除或合并 stable 字段 | approval | 必须说明替代和影响 |
| 项目专属字段 | project-only | 不提升到全局模板，除非有跨项目证据 |

如果字段变更影响 vibeflow、runtime、agent-core 或其他全局系统，必须走对应系统的审批边界。

## Field Trial

任何新契约都要用真实项目试点验证。

| 试点前 | 试点中 | 试点后 |
| --- | --- | --- |
| 写清 capability hypothesis | 收集产物、证据、人类反馈 | 分类 lesson 和 promotion target |
| 定义成功/失败信号 | 记录 friction 和 failure | 更新模板、checker、eval 或归档 |
| 选低风险真实任务 | 保留 delivery package | 必要时再次运行 |

没有 field trial 的外部学习只能是 `watch`，不能直接 `promote`。

## Promotion Rules

把学习结果提升到更高层时，按这个顺序判断：

| 问题 | 结论 |
| --- | --- |
| 只服务当前业务项目 | 留在项目内 |
| 改变 Composite Business Agent 构建方式 | 候选提升到 `agent-builder-lab` |
| 改变 runtime loop、tool dispatch、state | 候选提升到 runtime / agent-core |
| 改变协作、人审、交付边界 | 候选提升到 `vibeflow` |
| 改变 eval 形状 | 候选提升到 eval template |
| 只有资料价值 | reference only |

跨项目、跨 Skill、跨 runtime 的吸收必须有人批准。

## 最小可用产出

一次能力参照研究至少产出：

```text
1 capability hypothesis
3 external references
1 output anatomy table
1 invariant list
1 local contract recommendation
1 field trial proposal
1 promotion decision
```

如果少于这些，说明还只是资料阅读，不是 Agent 能力学习。

## 示例：Memory 能力

外部产出可以这样对照：

| 系统 | 产出对象 | 可借鉴点 |
| --- | --- | --- |
| Letta | memory block、archival memory | active context 与 long-term store 分层 |
| LangGraph | thread、checkpoint、StateSnapshot、store item | runtime state 和跨 thread memory 分离 |
| AutoGen | MemoryContent、Memory protocol、agent/team state | memory 接口和 save/load state 分离 |
| OpenAI Agents SDK | trace、span、eval dataset、grader | 运行轨迹和评估证据分离 |

本地契约可以落成：

```text
memory/
  business-memory.yaml
  feedback-log.yaml
evals/
  memory-recall-scenario.yaml
reports/
  memory-change-report.md
```

并新增规则：

```text
runtime memory helps execution
business memory belongs to the project
eval memory records whether changes improved ability
promotion memory records what should change future agents
```

## Red Flags

- 只总结“这个系统很强”，没有拆产出对象。
- 只学习流程，没有字段、生命周期和所有权。
- 把某个产品的特殊实现当成通用原则。
- 没有 field trial 就修改全局 skill。
- 学习结果只存在聊天里，没有进入模板、schema、eval、checker 或 journal。
- 把项目 taste、业务数据、私有 prompt 提升成通用规则。

## Source Notes

这份方法来自对 Agent runtime、memory、eval、state 和 trace 系统的产出层对比。当前参考包括：

- OpenAI Agents SDK tracing: https://openai.github.io/openai-agents-python/tracing/
- OpenAI agent evals: https://developers.openai.com/api/docs/guides/agent-evals
- LangGraph persistence/checkpoint/store: https://docs.langchain.com/oss/python/langgraph/persistence
- Letta memory blocks: https://docs.letta.com/guides/core-concepts/memory/memory-blocks
- AutoGen memory: https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/memory.html
- AutoGen state: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/state.html
