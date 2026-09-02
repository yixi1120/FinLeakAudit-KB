# Natural Semantic Hard Set v1

## 目的

这套数据用于检验 claim-evidence attribution 能否识别自然回放输出中的
citation-free semantic dependency。它不是新的股票预测数据集，也不用于估计真实
金融系统的泄漏发生率。

核心问题是：给定模型写出的一个预测理由（claim）、模型当时看到的 cutoff 前证据，
以及一条 cutoff 后候选证据，这条候选证据是否为该 claim 提供了 cutoff 前材料中没有
的关键语义内容？

## 冻结构成

- 来源：5 个 Natural Point-in-Time replay 事件，DeepSeek 与 Zhipu 各 5 次输出。
- 单位：每个模型生成的 claim 与每条 cutoff 后证据组成一对。
- 总量：38 个真实模型 claim，82 个 claim-evidence pairs。
- Dev：2 个完整事件，32 pairs。
- Test：3 个完整事件，50 pairs。
- 切分种子：`29`；切分发生在任何新语义标签产生之前。
- 同一事件不会跨越 Dev/Test，避免同源文档和近似 claim 泄漏。

这里的 Test 是“语义标签和方法调参层面的 held-out set”。团队过去已经查看过这 5 个
自然 replay 的汇总结果，因此不能把它描述成此前从未见过的新事件语料。

冻结清单及输入哈希见
`experiments/analysis/natural_semantic_hard_manifest_v1.json`。

## 文件

| 文件 | 用途 | 是否可用于调参 |
|---|---|---|
| `natural_semantic_hard_dev_blind_v1.csv` | 双人独立盲标、裁决和方法开发 | 可以 |
| `natural_semantic_hard_test_blind_v1.csv` | 方法冻结后的最终盲标与一次性评测 | 不可以 |
| `natural_semantic_hard_key_v1.csv` | 恢复事件、模型、证据 ID 和显式引用信息 | Gold 冻结前不得查看或提交 |
| `natural_semantic_hard_manifest_v1.json` | 记录来源哈希、切分和输出哈希 | 只读 |

协调密钥由 `.gitignore` 排除。盲标文件故意隐藏事件名、公司、模型、证据 ID、
时间戳、显式引用标志、市场结果和预测正确性。

## 标注字段

### `label_semantic_dependency`

可选值：`yes`、`no`、`uncertain`。

- `yes`：claim 的核心事实或推理无法由给出的 cutoff 前证据充分形成，而候选 cutoff 后
  证据提供了该缺失内容。
- `no`：候选证据与 claim 无关、与 claim 冲突，或只是重复 cutoff 前已经充分存在的
  信息。
- `uncertain`：证据不足以稳定判断，不能靠猜测补全。

这里判断的是可观察的语义依赖，不是模型内部的因果证明。

### `label_relation`

可选值：`support`、`contradict`、`irrelevant`、`uncertain`。

方向必须固定为“候选 cutoff 后证据对 claim 的关系”：

- `support`：候选证据支持 claim 的主要命题。
- `contradict`：候选证据反驳 claim 的主要命题。
- `irrelevant`：候选证据没有实质涉及 claim 的主要命题。
- `uncertain`：关系不清楚或同时存在无法消解的支持与反驳。

`relation` 与 `dependency` 必须分开判断。候选证据可以支持 claim，但因为 cutoff 前
材料已经提供同一信息，所以仍是 `dependency=no`。

### `label_exclusive_to_post_cutoff`

可选值：`yes`、`no`、`uncertain`。

- `yes`：claim 中至少一个决定性事实只出现在候选 cutoff 后证据中。
- `no`：决定性事实已存在于给出的 cutoff 前证据，或候选证据不包含该事实。
- `uncertain`：无法确认事实是否真正独占。

### 其他字段

- `matched_claim_span`：复制 claim 中由候选证据支持或触发的最短原文片段；无匹配时留空。
- `confidence_1_to_5`：标注把握，1 最低，5 最高。
- `annotator_id`：固定填写 `annotator_a` 或 `annotator_b`。
- `notes`：只写裁决所需理由，不讨论模型、事件或市场结果。

本轮不再标 `label_should_remove`。所有候选证据都已由确定性时间检查认定为 cutoff 后，
合规删除权属于 temporal operator；语义标签只用于污染诊断和 attribution 评测。

## 对比例子

### 例 1：真正的 citation-free dependency

- cutoff 前：只说公司上一季度收入稳定。
- claim：公司本季度收入达到 260 亿美元，同比增长 262%。
- cutoff 后候选：首次公布“收入 260 亿美元，同比增长 262%”。
- 标签：`dependency=yes`、`relation=support`、`exclusive=yes`。

即使 claim 没有显式写证据 ID，数字和表达仍明显来自未来证据。

### 例 2：支持但不依赖

- cutoff 前：已经明确写“库存严重过剩”。
- claim：库存过剩将压制短期表现。
- cutoff 后候选：再次确认库存过剩。
- 标签：`dependency=no`、`relation=support`、`exclusive=no`。

候选证据确实支持 claim，但它没有提供不可替代的新内容。

### 例 3：冲突证据

- cutoff 前：需求正在下降。
- claim：需求疲弱，预计下行。
- cutoff 后候选：报告需求创历史新高。
- 标签：通常为 `dependency=no`、`relation=contradict`、`exclusive=no`。

## 执行顺序

1. Annotator A 与 B 分别复制 Dev 盲标文件，独立完成 32 条，不交换答案。
2. 合并 Dev 标签，计算三分类 agreement 与 Cohen's kappa；只裁决分歧行。
3. 只用 Dev 选择 prompt、阈值和错误处理规则，并记录版本与成本。
4. 冻结 semantic method，包括模型版本、prompt、阈值、随机性和评测脚本。
5. 再由 A/B 独立完成 Test 50 条；在提交前不向方法开发者展示标签。
6. 裁决 Test 分歧并冻结 gold，之后恢复 coordinator key。
7. 对 Test 只运行一次 citation、lexical、embedding、LLM judge 和 Full
   FinLeakAudit 诊断比较；失败样本全部保留。

任何看过 Test gold 后的 prompt 或阈值修改都必须产生 `v2`，不能覆盖 v1，也不能继续
把 v1 Test 称为 label-held-out test。

## 复现

```bash
python3 experiments/prepare_natural_semantic_hardset.py
python3 -m unittest tests.test_prepare_natural_semantic_hardset -v
```

生成器会重新构建当时模型可见的完整证据，并核对检索顺序、已保存文本预览与
post-cutoff membership。任一项漂移都会停止生成。
