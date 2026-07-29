---
title: Semantic claim-evidence attribution annotation protocol v1
date: 2026-07-29
status: ready-for-analysis-line
---

# 目标

为 v4 三模型输出建立人工 gold labels，判断每条 rationale claim 是否在语义上依赖
cutoff 后证据。标注单位是一个 `claim × post-cutoff evidence` pair，不是整个 case。

当前共有 30 个 model-case、79 条 leaky rationale claims。第一轮由两名标注者分别
独立完成同一批 79 条样本。

# 重要边界

- 没有引用未来 evidence ID，不等于发生了语义泄漏。
- 引用了未来 evidence ID，也不自动证明该 evidence 对 claim 必不可少。
- 方向发生变化属于 marginal sensitivity，不等于 claim-level semantic attribution。
- 标注者不得查看 Clean/Audited 预测、outcome label、自动审计结果、模型名称或
  leave-one-out 结果。

# 标注字段

## `label_semantic_dependency`

- `yes`：claim 的核心事实或判断明显来自 post-cutoff evidence。
- `no`：claim 可由 pre-cutoff evidence 支持，或与 post-cutoff evidence 无关。
- `uncertain`：两边都可能解释，证据不足以判断。

## `label_relation`

- `support`：post-cutoff evidence 支持 claim 或预测方向。
- `contradict`：post-cutoff evidence 反驳 claim 或预测方向。
- `irrelevant`：二者没有实质关系。
- `uncertain`：关系不明确。

## `label_exclusive_to_post_cutoff`

- `yes`：claim 的核心事实无法从任何 pre-cutoff evidence 得到。
- `no`：pre-cutoff evidence 已包含同一核心事实或足够支持该概括。
- `uncertain`：只能做弱推断。

## `label_should_remove`

- `yes`：如果目标是恢复 point-in-time 合规输入，应删除该 post-cutoff evidence。
- `no`：该 pair 没有构成应删除的语义依赖。
- `uncertain`：交给 adjudication。

## 其他字段

- `matched_claim_span`：复制最能体现依赖的 claim 片段；没有则留空。
- `confidence_1_to_5`：1 表示非常不确定，5 表示非常确定。
- `notes`：简述依据，不写模型优劣评价。

# 判定示例

Post-cutoff evidence：

> The company reported Q4 revenue of $302.6 million and continued
> inventory-related shipment reductions.

### `yes`

Claim：

> Q4 revenue was $302.6 million and shipments were reduced because of
> inventory.

理由：包含只有未来证据提供的精确季度数值与事实。

### `no`

Claim：

> The company faces an inventory glut and analysts expect weak guidance.

若 pre-cutoff evidence 已明确写有 inventory glut 和 weak guidance，则该 claim
不应仅因措辞相似被标成未来语义依赖。

### `uncertain`

Claim：

> Near-term demand remains weak.

如果 pre-cutoff 和 post-cutoff evidence 都能支持这一概括，标记 `uncertain`，
不要强行二选一。

# 标注流程

1. 工程线运行 `experiments/prepare_semantic_annotations.py`。
2. 两名标注者分别复制 blind batch，填写自己的 `annotator_id`。
3. 标注期间不得打开 key 文件或讨论单条答案。
4. 合并后计算三分类 agreement 和 Cohen's kappa；同时报告 `yes` 对其他标签的
   二分类 agreement。
5. 只对分歧样本进行 adjudication，并保留两份原始标注。
6. 人工标签冻结后，才运行 lexical/embedding/LLM-judge baselines。

# 验收规则

- 79 行全部填写；
- label 只能使用协议列出的枚举；
- confidence 必须为 1–5；
- `yes` 必须填写 `matched_claim_span`；
- 不允许根据模型名称或预测是否翻转倒推标签；
- `case_005` 中未显式引用未来 ID 的输出必须逐条判断，不能批量标成 `yes`。

# 交付物

- `semantic_annotations_annotator_a_v1.csv`
- `semantic_annotations_annotator_b_v1.csv`
- `semantic_annotation_disagreements_v1.csv`
- `semantic_annotation_adjudicated_v1.csv`
