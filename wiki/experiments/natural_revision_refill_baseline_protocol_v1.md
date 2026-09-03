# Natural Revision Refill Baseline v1

## 问题

自然回放中的 Clean 与 Audited 不是同一个证据构造过程：

- Clean：在 prediction cutoff 上重新检索 top-k。
- Sparse Audited：从 outcome-time Unfiltered top-k 中删除 cutoff 后证据。

如果 Unfiltered 有两条未来证据，Sparse Audited 删除后可能只剩六条。此时预测变化
既可能来自未来信息被移除，也可能来自上下文数量、覆盖面和排序发生变化。

Qwen 在 `natural_007` 中暴露了该问题：Clean 与 Unfiltered 都预测 `UP`，但 Sparse
Audited 变为 `NEUTRAL`。这不是 recovery failure，因为初始预测没有翻转；它是
revision instability。

## Baseline 定义

新增 Rank-Preserving Backfill：

1. 从实际 Unfiltered top-k 删除全部 cutoff 后证据。
2. 保留剩余证据的原始相对顺序。
3. 按 cutoff-time Clean retrieval 的排名顺序加入尚未出现的安全证据。
4. 补到 `k` 条或安全候选耗尽。
5. 用同一 predictor prompt 重新预测一次。

```text
Unfiltered top-k
      |
      +-- remove post-cutoff --> Sparse Audited (< k)
                                  |
                                  +-- add safe ranked fallbacks --> Backfilled Audited (= k)
```

Temporal operator 仍拥有删除权。Backfill 只改变删除后的输入重建策略，不使用 outcome、
人工 sentiment 或 evaluator label。

## 对照条件

| 条件 | 构造 | 回答的问题 |
|---|---|---|
| Clean | cutoff-time fresh top-k retrieval | cutoff 时正常可见的基准预测是什么 |
| Unfiltered | outcome-bounded top-k retrieval | 混入未来材料时预测怎样变化 |
| Sparse Audited | Unfiltered minus post-cutoff | 直接删除能否恢复，是否产生稀疏副作用 |
| Backfilled Audited | Sparse Audited plus safe fallbacks | 补齐上下文能否减少 revision instability |

## 预注册指标

- `backfilled_audited_matches_clean`
- `sparse_revision_drift_without_initial_flip`
- `backfilled_revision_drift_without_initial_flip`
- `backfill_changed_sparse_audited_direction`
- `backfilled_matches_clean_sequence`
- invalid citation count
- 每次调用 tokens 与 runtime

主要比较是非翻转样本上的 drift rate：

```text
drift = Clean == Unfiltered and Revised != Clean
```

不使用市场 outcome 选择 revision policy。Outcome accuracy 只作描述性报告。

## 当前离线检查

固定五事件中，Backfilled evidence sequence 在 `natural_001`、`natural_002`、
`natural_004` 和 `natural_007` 与 Clean 完全相同。`natural_010` 因候选集合中的父文档
限额和排序交互而不同，因此不能把 Backfilled 条件整体称为“重新运行 Clean”。

## Qwen 最小诊断结果

2026-09-03 对 `natural_007` 新增一次 Qwen Backfilled prediction：

| 条件 | 方向 | 证据数 |
|---|---:|---:|
| Clean | `UP` | 8 |
| Unfiltered | `UP` | 8 |
| Sparse Audited | `NEUTRAL` | 6 |
| Backfilled Audited | `UP` | 8 |

Backfilled evidence IDs 与 Clean 的顺序完全一致，新增的两条证据均早于 cutoff，
预测由 Sparse 的 `NEUTRAL` 回到 `UP`。该结果支持 `natural_007` 的异常主要来自
删除后的上下文稀疏，而不是 temporal removal 本身。但这是单事件、单模型 smoke，
不能据此断言 Backfill 在总体上优于 Sparse revision。

逐项运行记录见
[`natural_revision_refill_smoke_2026_09_03.md`](natural_revision_refill_smoke_2026_09_03.md)。

## 最小验证顺序

1. [已完成] 对 Qwen `natural_007` 运行一次 Backfilled prediction，结果由 Sparse
   `NEUTRAL` 回到 Clean `UP`。
2. 固定 runner 和指标后，扩展到三个模型的五事件，共 15 个新增调用。
3. 若 drift 降低，再在完整十事件集合上比较 Sparse 与 Backfilled。
4. 无论结果正负，保留所有失败与 citation-format errors。

## 命令

```bash
python3 experiments/run_natural_refill_baseline.py --model qwen --minimal --dry-run

python3 experiments/run_natural_refill_baseline.py \
  --model qwen \
  --event natural_007
```

本地 Qwen 服务只在实际模型调用期间启动，运行完成后立即关闭。
