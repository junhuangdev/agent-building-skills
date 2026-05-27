# Business Agent Package Contract

## 一句话结论

Business Agent package 是给 AI 和人共同使用的机器契约：它把使命、动作、产物、评估、记忆和运行时适配固定成可检查文件。

## 最小目录

```text
business-agent/
  agent.yaml
  actions/*.yaml
  artifacts/*.yaml
  memory/*.yaml
  evals/*.yaml
  reports/delivery-package.md
  runtime-adapters/*.yaml
```

模板位置：

```text
~/.codex/skills/agent-builder-lab/assets/templates/business-agent/
```

结构检查：

```bash
python ~/.codex/skills/agent-builder-lab/scripts/check_business_agent_package.py ./business-agent
```

## agent.yaml

`agent.yaml` 是 canonical contract。其他文件都应能回到它。

| 字段 | 必填 | 含义 |
| --- | --- | --- |
| `id` | yes | 稳定机器名 |
| `name` | yes | 人类可读名称 |
| `agent_shape` | yes | `composite_business_agent` 或 `self_built_runtime_agent` |
| `mission` | yes | 长期业务使命 |
| `business_value` | yes | 可观察业务价值 |
| `non_goals` | yes | 明确不做什么 |
| `allowed_actions` | yes | 允许动作清单 |
| `risk_classes` | yes | 风险分级 |
| `human_gates` | yes | 人审规则 |
| `runtime_targets` | yes | 支持的宿主或运行时 |
| `memory_policy` | yes | 业务记忆归属和提升规则 |
| `eval_policy` | yes | eval 场景和阻断规则 |
| `delivery_contract` | yes | 交付格式 |

语义规则：

- `business_value` 必须能被人判断，不要写成泛泛愿望。
- `allowed_actions` 里的 action 必须在 `actions/` 中存在。
- 每个 external、irreversible、money、publish、delete 类型风险必须有 human gate。
- runtime target 必须有对应 adapter。

## actions/*.yaml

Action 是 AI 可以调用、建议或驱动的业务动作。

| 字段 | 必填 | 含义 |
| --- | --- | --- |
| `id` | yes | 动作机器名 |
| `description` | yes | 动作做什么 |
| `input_contract` | yes | 输入要求 |
| `output_contract` | yes | 输出要求 |
| `risk_class` | yes | 风险等级 |
| `requires_approval` | yes | 是否需要人审 |
| `side_effects` | yes | 副作用 |
| `forbidden_when` | yes | 禁止条件 |
| `produces_artifacts` | yes | 产物 |

动作设计规则：

- 一个 action 做一类业务动作。
- 能读就不要写，能建议就不要直接执行。
- 高风险动作要拆成 `propose_*` 和 `execute_*` 两步。
- 所有动作都要能被测试或人工验收。

## artifacts/*.yaml

Artifact 是业务 Agent 产出的可验收结果，不是聊天内容。

| 字段 | 必填 | 含义 |
| --- | --- | --- |
| `id` | yes | 产物机器名 |
| `type` | yes | 产物类型 |
| `owner` | yes | 归属 Agent |
| `schema` | yes | 字段契约 |
| `evidence_required` | yes | 必须证据 |
| `status_values` | yes | 状态枚举 |
| `human_summary_fields` | yes | 人类验收字段 |

产物设计规则：

- 重要业务结论必须有 evidence。
- 产物状态至少覆盖 draft、verified、rejected、superseded。
- 产物要能被后续 run 读取，而不是只给当前对话看。

## memory/*.yaml

Memory 保存业务项目拥有的长期知识。

建议最小文件：

| 文件 | 用途 |
| --- | --- |
| `business-memory.yaml` | mission、偏好、长期决策 |
| `feedback-log.yaml` | 反馈、失败、沉淀去向 |

记忆规则：

- runtime memory 可以辅助执行，但业务记忆必须归项目所有。
- 反馈先进入 log，再决定提升到 memory、eval、action、artifact 或 archive。
- 过期、冲突、局部的一次性经验不要直接提升。

## evals/*.yaml

Eval scenario 评估业务闭环，而不是宿主 Agent 的隐藏推理。

| 字段 | 必填 | 含义 |
| --- | --- | --- |
| `id` | yes | 场景机器名 |
| `goal` | yes | 业务目标 |
| `initial_state` | yes | 初始条件 |
| `expected_artifacts` | yes | 期望产物 |
| `rubric` | yes | 评分标准 |
| `blocking_failures` | yes | 阻断失败 |
| `human_gate_expectations` | yes | 人审期望 |

第一版至少有一个 smoke scenario。它应覆盖 outcome、artifact、evidence、boundary。

## runtime-adapters/*.yaml

Runtime adapter 描述业务 Agent 如何跑在不同宿主上。

| 字段 | 必填 | 含义 |
| --- | --- | --- |
| `runtime` | yes | runtime 名称 |
| `invocation` | yes | 启动或触发方式 |
| `skill_trigger` | yes | 需要的 Skill 或规则 |
| `capability_map` | yes | 能力映射 |
| `unsupported_actions` | yes | 不支持或不应依赖的能力 |
| `handoff_rules` | yes | 状态和证据交还规则 |

不要把业务状态绑定在某个 runtime 的隐藏上下文里。

## reports/delivery-package.md

Delivery package 是每次 run 的交付契约。

必须包含：

```text
Result
Evidence
Risks
Human Gates
Artifacts
Next Action
```

如果一个结果不能放进 delivery package，说明它还不是可验收业务产出。

## Contract Invariants

这些规则比文件格式更重要：

| 不变量 | 影响 |
| --- | --- |
| mission 驱动 action | 防止工具堆砌 |
| action 产生 artifact | 防止只有聊天答案 |
| artifact 需要 evidence | 防止不可验证结论 |
| risk 触发 gate | 防止高风险自动化失控 |
| eval 覆盖 boundary | 防止只看结果不看风险 |
| memory 归项目所有 | 防止业务知识丢在宿主上下文 |
| adapter 明确 unsupported | 防止误用 runtime 黑盒能力 |

## 当前自动检查范围

`check_business_agent_package.py` 检查：

- `agent.yaml` 是否存在并包含必填顶层字段。
- `actions/`、`artifacts/`、`evals/`、`runtime-adapters/` 是否存在并至少有一个 YAML。
- 每类 YAML 是否包含必填顶层字段。
- `reports/delivery-package.md` 是否存在。

它不检查：

- YAML 深层语义是否完全一致。
- 业务价值是否真的成立。
- action 是否真的能运行。
- eval rubric 是否足够严格。

这些需要通过人工 review 和真实业务 run 验证。
