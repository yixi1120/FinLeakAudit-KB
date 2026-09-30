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

## 三模型结果

2026-09-06 完成三个模型、五事件共 15 个 Backfilled 调用，0 错误：

- 6 个初始翻转：Sparse 与 Backfilled 均恢复 6/6。
- 9 个非翻转：Sparse drift 1/9，Backfilled drift 0/9。
- Backfilled 与 Clean 方向一致 15/15，Wilson 95% CI 为 79.6%–100%。
- Backfilled evidence sequence 与 Clean 完全相同 12/15。
- 15 个输出均有引用，共 53 个 evidence ID，53/53 有效。

唯一被纠正的 drift 是 Qwen `natural_007`。由于只有一个 discordant pair，且多数
Backfilled 输入与 Clean 完全相同，不进行统计显著性或总体优越性声明。完整报告见
[`natural_revision_refill_three_model_results_2026_09_06.md`](natural_revision_refill_three_model_results_2026_09_06.md)。

## 十事件扩展结果

同日完成后五事件并与首批冻结结果合并，共得到 30 个 model-event pairs：

- 13 个初始翻转：Sparse 恢复 11/13，Backfilled 恢复 13/13。
- 17 个非翻转：Sparse drift 1/17，Backfilled drift 0/17。
- Backfilled 与 Clean 方向一致 30/30，Wilson 95% CI 为 88.6%–100%。
- Backfilled evidence sequence 与 Clean 完全相同 24/30。
- Backfill 修正 DeepSeek `natural_005`、Qwen `natural_006` 和 Qwen
  `natural_007` 三处 Sparse 不一致。
- 配对 exact McNemar `p=0.25`，未达到统计显著。

该扩展支持 Backfill 作为上下文稀疏诊断和 revision consistency baseline，但仍不支持
一般优越性结论。完整报告见
[`natural_pit_10event_three_model_results_2026_09_06.md`](natural_pit_10event_three_model_results_2026_09_06.md)。

## 后续消融：Novel-safe Backfill（计划中）

### 研究动机

十事件实验中，24/30 个 Backfilled evidence sequence 与 Clean 完全相同。因此，
Backfilled 与 Clean 方向一致 30/30 的结果部分来自相同输入在 temperature 0 下被重新
运行，而不能单独证明“补足任意合规上下文”具有稳定效果。

2026-09-15 决定保留当前 Rank-Preserving Backfill 作为主 revision baseline，同时新增
Novel-safe Backfill 作为消融。两者回答不同问题：

- Standard Backfill 模拟正确执行 cutoff filtering 后，检索系统本应返回的高排名安全
  evidence；允许重新选入 Clean top-k 中的 evidence。
- Novel-safe Backfill 检查恢复是否只是因为重建了 Clean 输入，还是补足不同的 cutoff-safe
  evidence 后仍能维持 revision consistency。

Novel-safe 不是推荐的生产检索策略，因为它会主动跳过部分排名更高的合法 evidence；
它只用于压力测试和识别输入重合这一混杂因素。

### 构造规则

1. 从实际 Unfiltered top-k 删除全部 cutoff 后 evidence，得到 surviving safe evidence。
2. 保留 surviving evidence 的原始相对顺序。即使某个 survivor 也出现在 Clean top-k，
   也不得为了制造不重合而删除它。
3. 新补入的 evidence 必须满足 `available_at <= prediction_cutoff`。
4. 新补入的 evidence ID 不得出现在 surviving evidence 或 Clean top-k 中。
5. 从满足条件的候选中按照冻结的 cutoff-time retrieval score 和既有 tie-break 规则依次
   选择，并沿用 parent-document cap。
6. 不得使用 outcome、人工 sentiment、模型预测方向或 evaluator label 选择回填内容。
7. 若合格候选不足以补到 k 条，保留实际数量并将该 run 标记为
   `novel_safe_backfill_incomplete`，不得临时放宽规则。

示例：

```text
Clean top-4:            [A, B, C, D]
Unfiltered top-4:       [A, B, F_future, G_future]
Sparse:                 [A, B]
Standard Backfill:      [A, B, C, D]
Novel-safe Backfill:    [A, B, H, I]
```

### 新增指标

- `novel_safe_backfilled_matches_clean_direction`
- `novel_safe_recovery_on_initial_flips`
- `novel_safe_revision_drift_without_initial_flip`
- `novel_safe_backfill_complete`
- `novel_safe_backfill_count`
- `novel_safe_clean_id_overlap`，按构造规则只统计 survivors 造成的重合
- Standard 与 Novel-safe 各自的 evidence-sequence overlap、invalid citation、tokens 和 runtime

除总体指标外，应分别报告：

- Standard Backfill 与 Clean 完全同序列的 runs；
- Standard Backfill 与 Clean 不同序列的 runs；
- Novel-safe 完整补足的 runs；
- Novel-safe 因候选不足未补足的 runs。

### 解释边界

- 若 Novel-safe 仍恢复 Clean 方向，说明恢复不完全依赖机械重建 Clean 输入，但不能证明
  任意安全 evidence 都等价。
- 若 Novel-safe 未恢复，说明 revision 对回填内容和检索构成敏感，而不自动推翻 Standard
  Backfill 作为正常 cutoff-safe retrieval baseline 的合理性。
- Novel-safe 结果衡量的是鲁棒性和输入重合敏感性，不衡量市场预测准确率。
- 当前 30 个 model-event pairs 不足以支持一般优越性结论；运行前应冻结候选资格、选择
  规则和统计比较，不根据结果调整回填内容。

### 2026-09-30 完成结果

模型调用前的离线资格检查显示，只有 6/10 个事件能在排除 Clean top-k 后仍使用不同的
cutoff-safe evidence 补满 8 条：`natural_002`、`natural_005`、`natural_006`、
`natural_007`、`natural_009`、`natural_010`。其余四个事件冻结为候选不足，不进入
完整回填比较。

在 6 个事件、3 个模型共 18 个 complete-case runs 上：

- Sparse 与 Clean 方向一致 15/18；
- Standard Backfill 与 Clean 方向一致 18/18；
- Novel-safe Backfill 与 Clean 方向一致 15/18；
- 6 个初始翻转中，Sparse、Standard、Novel-safe 分别恢复 4/6、6/6、4/6；
- 12 个非翻转中，三者 drift 分别为 1/12、0/12、1/12；
- Standard-only match 为 3，Novel-only match 为 0；配对 exact McNemar `p=0.25`；
- Novel-safe evidence sequence 与 Clean 完全相同 0/18。

Novel-safe 没有复现 Standard 对 DeepSeek Intel、Qwen Exxon 和 Qwen Capital One
三处 Sparse mismatch 的修正。它只在 DeepSeek Intel 上把 Sparse 的 `DOWN` 改成
`NEUTRAL`，仍未回到 Clean 的 `UP`。因此，当前结果支持 replacement evidence 的内容和
排序会影响 revision utility，而不支持“只要补足任意 cutoff-safe evidence 就能恢复”这一
更强结论。该比较仅适用于预先冻结的六事件合格子集，且差异不显著。

资格报告见
[`novel_safe_backfill_eligibility_2026_09_30.md`](novel_safe_backfill_eligibility_2026_09_30.md)，
三模型结果见
[`novel_safe_backfill_three_model_results_2026_09_30.md`](novel_safe_backfill_three_model_results_2026_09_30.md)。

## 最小验证顺序

1. [已完成] 对 Qwen `natural_007` 运行一次 Backfilled prediction，结果由 Sparse
   `NEUTRAL` 回到 Clean `UP`。
2. [已完成] 固定 runner 和指标后，扩展到三个模型的五事件，共 15 个新增调用。
3. [已完成] 扩展至完整十事件、三个模型，并进行 Sparse 与 Backfilled 配对比较。
4. [已完成] 实现并离线验证 Novel-safe Backfill，冻结 6/10 个完整回填事件并完成三个
   模型共 18 个调用。
5. 无论结果正负，保留所有失败与 citation-format errors。

## Citation ID 完整性门禁

从 2026-09-30 起，后续 Backfill 调用在写入正式结果前执行 evidence ID 白名单检查：

1. 所有 `rationale[].evidence_ids[]` 必须逐字匹配本次输入中的完整 evidence ID；
2. 首次出现缩写、变形或虚构 ID 时，向同一模型提供允许 ID 白名单并要求重新生成完整 JSON；
3. 默认最多进行 2 次 citation correction，即单个预测最多调用 3 次；
4. 三次均不合格时将该事件记为 `InvalidCitationError`，不得写入正式结果；
5. citation correction 已经耗尽后不再触发外层整事件重跑，避免把同一失败放大为 9 次调用；
6. 结果记录最终 citation validation、实际尝试次数和每次无效 ID，供成本与失败分析使用。

该门禁只适用于之后的新调用。已经冻结的 18 条 Novel-safe 输出保留原貌，不进行事后替换。

## 命令

```bash
python3 experiments/run_natural_refill_baseline.py --model qwen --minimal --dry-run

python3 experiments/run_natural_refill_baseline.py \
  --model qwen \
  --event natural_007 \
  --citation-retries 2
```

本地 Qwen 服务只在实际模型调用期间启动，运行完成后立即关闭。
