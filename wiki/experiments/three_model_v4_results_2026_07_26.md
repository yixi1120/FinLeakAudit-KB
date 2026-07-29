---
title: FinLeakAudit v4 three-model controlled pilot
date: 2026-07-26
status: completed-controlled-pilot
---

# FinLeakAudit v4 三模型受控实验

## 一句话结论

在 10 个受控案例、3 个模型形成的 30 个 model-case 运行中，预测模型
28/30 次显式引用了 cutoff 后证据，12/30 次因此改变预测方向；删除被审计器
识别的未来证据后，12/12 个翻转恢复到各自的 Clean 方向。该结果支持
FinLeakAudit 的 premise，但不证明其能提高预测准确率，也不能外推到自然
金融 RAG。

## 实验设置

- 数据：`数据线/cases_pilot_v4_mixed10_candidate.jsonl`
- 构成：7 个真实 SEC 来源上下文案例 + 3 个 semi-real 案例
- 模型：DeepSeek `deepseek-chat`、智谱 `glm-4-flashx-250414`、
  本地 Qwen2.5-14B-Instruct GGUF Q4_K_M
- 条件：Clean、Leaky、Audited
- Audited 输入：从实际 Leaky evidence 中删除 auditor 返回的
  `removed_evidence_ids`
- 时间判断：优先比较带时区的 `available_at` 与 prediction cutoff
- 旧 3 个 semi-real 案例的 clean evidence 缺少绝对 `available_at`，因此使用
  relative-time fallback；其未来证据及新增 7 例均使用绝对时间
- Predictor 可见信息：仅 evidence ID 和文本，不显示 `time`、
  `sentiment` 或 `available_at`
- 消融：对 Leaky context 中 4 条证据逐条执行 leave-one-out；这里只解释为
  marginal sensitivity，不称为 causal effect
- 随机性：temperature 0；基础 seed 17，每个案例使用固定派生 seed
- 调用量：每模型 10 case × 7 calls = 70 calls，共 210 calls
- 运行错误：三个模型均为 0

## 总体结果

| Model | Future cited | Clean→Leaky flip | Recovered flips | Clean / Leaky / Audited accuracy | Future flip driver | Removal P / R | Tokens | Runtime |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| DeepSeek | 10/10 | 5/10 | 5/5 | 3/10 / 7/10 / 3/10 | 5/10 | 10/10 / 10/10 | 46,416 | 225.5 s |
| Zhipu | 9/10 | 3/10 | 3/3 | 3/10 / 6/10 / 3/10 | 3/10 | 9/9 / 9/10 | 43,695 | 440.9 s |
| Qwen2.5-14B | 9/10 | 4/10 | 4/4 | 2/10 / 5/10 / 2/10 | 4/10 | 9/9 / 9/10 | 43,023 | 1,682.9 s |

描述性合计：

- 显式未来证据引用：28/30 = 93.3%
- Clean→Leaky 方向改变：12/30 = 40.0%，Wilson 95% CI
  [24.6%, 57.7%]
- 翻转后的 revision recovery：12/12；Wilson 95% CI
  [75.7%, 100%]
- Clean / Leaky / Audited accuracy：8/30、18/30、8/30
- 未来证据为 leave-one-out flip driver：12/30

30 个 model-case 共享同一组 10 个案例，不能当作 30 个相互独立的数据点做
总体推断。模型之间的差异也明显：未来证据在 DeepSeek、Zhipu、Qwen 中分别
造成 5、3、4 次方向改变。

## 真实来源层

仅看 7 个 `controlled_hard_real_source_context` 案例：

| Model | Future cited | Flip | Recovered flips | Clean / Leaky / Audited accuracy | Future flip driver |
|---|---:|---:|---:|---:|---:|
| DeepSeek | 7/7 | 3/7 | 3/3 | 3/7 / 5/7 / 3/7 | 3/7 |
| Zhipu | 7/7 | 1/7 | 1/1 | 3/7 / 4/7 / 3/7 | 1/7 |
| Qwen2.5-14B | 7/7 | 4/7 | 4/4 | 2/7 / 5/7 / 2/7 | 4/7 |

该层共 21 个 model-case：21/21 显式引用未来证据，8/21 改变预测方向，
8/8 翻转在审计后恢复。未来证据使描述性准确率从 8/21 升至 14/21，
但这是 cutoff 后信息带来的无效 look-ahead gain；审计后回到 8/21。

## 代表性案例

- `case_010` CRM：DeepSeek `UP→DOWN→UP`；Qwen
  `UP→NEUTRAL→UP`；Zhipu 未改变方向。
- `case_011` DELL：DeepSeek `UP→NEUTRAL→UP`；Qwen
  `NEUTRAL→DOWN→NEUTRAL`；Zhipu 未改变方向。
- `case_014` NKE：三个模型均被未来证据带到 `DOWN`，删除后恢复各自的
  Clean 方向。
- `case_005`：Zhipu 和 Qwen 没有显式引用未来 evidence ID，citation-only
  auditor 因而没有删除该证据，暴露出 attribution coverage 的缺口。仅凭未引用
  和证据仍被保留，不能断定模型在语义上依赖了该未来证据；该问题必须通过独立
  claim-evidence 标注验证。

## 如何解释

1. 结果支持一个有限 premise：cutoff 后证据会污染 rationale，并可对预测
   方向产生模型相关的边际影响。
2. Leaky accuracy 的上升不是模型进步，而是未来信息造成的回测虚高。
3. Audited accuracy 与 Clean 相同，说明当前 revision 主要撤销已检测的
   泄漏影响；它没有创造新的预测信号。
4. `12/12 recovery` 的分母只是发生翻转的 12 次运行，且 95% 置信区间下界
   为 75.7%。对外不得简写成“FinLeakAudit 100% 有效”。
5. 显式引用率高于 flip rate，说明 rationale contamination 与 forecast
   sensitivity 必须分开报告。

## 复现

```bash
python3 experiments/run_experiment.py \
  --model deepseek \
  --cases 数据线/cases_pilot_v4_mixed10_candidate.jsonl \
  --with-ablation \
  --run-name v4_mixed10_abs_time_20260726 \
  --overwrite

python3 experiments/run_experiment.py \
  --model zhipu \
  --cases 数据线/cases_pilot_v4_mixed10_candidate.jsonl \
  --with-ablation \
  --run-name v4_mixed10_abs_time_20260726 \
  --overwrite

python3 experiments/run_experiment.py \
  --model qwen \
  --cases 数据线/cases_pilot_v4_mixed10_candidate.jsonl \
  --with-ablation \
  --run-name v4_mixed10_abs_time_20260726 \
  --overwrite
```

总体与分层汇总分别由以下命令生成：

```bash
python3 experiments/analyze.py \
  --input experiments/results/MODEL_v4_mixed10_abs_time_20260726_ablation_results.jsonl \
  --output experiments/results/MODEL_v4_mixed10_abs_time_20260726_summary.csv

python3 experiments/analyze.py \
  --input experiments/results/MODEL_v4_mixed10_abs_time_20260726_ablation_results.jsonl \
  --output experiments/results/MODEL_v4_mixed10_abs_time_20260726_summary_by_tier.csv \
  --group-by dataset_tier
```

## 结果文件

- `experiments/results/deepseek_v4_mixed10_abs_time_20260726_ablation_results.jsonl`
- `experiments/results/zhipu_v4_mixed10_abs_time_20260726_ablation_results.jsonl`
- `experiments/results/qwen_v4_mixed10_abs_time_20260726_ablation_results.jsonl`
- 同名前缀的 `_summary.csv` 与 `_summary_by_tier.csv`

结果 JSONL/CSV 是本地生成文件并由 `.gitignore` 排除；可复查结论沉淀在本页。

## 局限与下一步

1. 只有 10 个 controlled cases；其中 3 个仍包含 synthetic clean evidence。
2. 7 个新案例虽有真实来源和时间戳，证据仍由研究者选择，不是自然检索。
3. 新案例全部是财报/业绩披露，事件类型单一。
4. Auditor 只能处理显式 evidence ID 引用，不能识别 citation-free semantic
   leakage。
5. 价格方向虽已复算，但论文级数据仍需第二行情源和许可证记录。
6. `deepseek-chat` 是可变 API alias；后续正式实验需保存返回版本信息或选用
   固定模型版本。
7. 下一轮应加入 timestamp-only、citation-only、delete-all-future 和
   semantic attribution baselines，并扩展 natural point-in-time cases。

## Baseline follow-up

The implemented policy comparison is reported in
[[baseline_comparison_v4_2026_07_26]]. In this controlled dataset,
timestamp-only filtering and citation-only revision have the same directional
accuracy, while citation-only revision retains 2/30 future items. This result
motivates semantic attribution but does not yet establish an advantage for the
full planned method.
