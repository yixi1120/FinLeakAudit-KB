# Natural Revision Refill Smoke: Qwen `natural_007`

## 目的

诊断 Qwen 在 Capital One 事件中的 revision drift：Clean 与 Unfiltered 都为 `UP`，
但直接删除两条 cutoff 后证据后，Sparse Audited 变为 `NEUTRAL`。本次只检验该变化
是否来自删除后上下文由 8 条缩减到 6 条。

## 冻结设置

- Event: `natural_007`
- Model: `qwen2.5-14b-instruct-q4_k_m`
- Temperature: `0.0`
- Top-k: `8`
- Policy: `remove_post_cutoff_then_rank_preserving_backfill_from_cutoff_top_k`
- 新增模型调用: `1`
- 运行错误: `0`
- Runtime: `107.242` seconds
- Tokens: `8,663` total, including `8,575` prompt and `88` completion

## 结果

| 条件 | 预测 | 置信度 | 证据数 |
|---|---:|---:|---:|
| Clean | `UP` | 0.65 | 8 |
| Unfiltered | `UP` | 0.65 | 8 |
| Sparse Audited | `NEUTRAL` | 0.50 | 6 |
| Backfilled Audited | `UP` | 0.65 | 8 |

被删除的两条证据均晚于 prediction cutoff。Backfill 加入两条 cutoff-safe evidence，
无重复、无未来证据，并且完整证据 ID 顺序与 Clean 完全一致。Backfilled 输出只引用
一个有效的、cutoff 前 evidence ID。

## 解释边界

这一结果支持该案例中的 drift 是上下文稀疏副作用：当模型重新看到与 Clean 完全相同
的证据序列时，方向也回到 Clean。它不证明 Backfill 在所有事件或模型上优于 Sparse
Audited，也不改变原始自然回放的 15-run 统计。下一步应在固定 runner 下完成三模型
五事件共 15 个 Backfilled 调用，再比较非翻转样本上的 revision drift rate。

原始机器可读结果：
`experiments/results/qwen_natural_refill_5event_v1_results.jsonl`。
