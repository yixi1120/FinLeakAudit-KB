---
title: FinLeakAudit v4 baseline comparison
date: 2026-07-26
status: completed-controlled-pilot
---

# FinLeakAudit v4 Baseline Comparison

## Purpose

This comparison asks whether the current citation-aware revision policy provides
evidence beyond a simpler timestamp filter. It reuses the completed predictions
from the 10-case, three-model experiment and makes no additional model calls.

The unit of analysis is a `model × case` result. The 30 rows share 10 cases and
must not be treated as 30 independent observations.

## Policies

| Policy | Operational definition |
|---|---|
| No Audit | Use the prediction made with all retrieved evidence, including post-cutoff items. |
| Timestamp-only | Remove every item whose `available_at` is after cutoff before prediction. |
| Citation-only | Remove a future item only when the model explicitly cites its evidence ID. |
| Delete-All-Future | Oracle deletion of every known future item. |
| Leave-One-Out | Remove one item at a time to measure marginal forecast sensitivity; this is a diagnostic, not a filtering policy. |
| Full FinLeakAudit | Planned: timestamp validation plus semantic attribution, support/contradiction, ablation, and revision logging. |

In the current controlled dataset, `timestamp_only` and
`delete_all_future` are identical by construction: every case contains exactly
one future item with a verified timestamp. They will diverge only when future
availability is missing, uncertain, revised, or semantically reconstructed.

## Overall Result

| Policy | Accuracy | Future items retained | Direction changes vs No Audit |
|---|---:|---:|---:|
| No Audit | 18/30 (60.0%) | 30/30 (100%) | 0/30 |
| Timestamp-only | 8/30 (26.7%) | 0/30 (0%) | 12/30 |
| Citation-only | 8/30 (26.7%) | 2/30 (6.7%) | 12/30 |
| Delete-All-Future | 8/30 (26.7%) | 0/30 (0%) | 12/30 |

Leave-one-out identifies the future item as a direction flip driver in 12/30
model-case runs. This matches the 12 Clean-to-Leaky direction changes and
provides a second marginal-sensitivity check.

## By Model

| Model | No Audit accuracy | Timestamp-only | Citation-only | Citation-only future retained |
|---|---:|---:|---:|---:|
| DeepSeek | 7/10 | 3/10 | 3/10 | 0/10 |
| Zhipu | 6/10 | 3/10 | 3/10 | 1/10 |
| Qwen2.5-14B | 5/10 | 2/10 | 2/10 | 1/10 |

DeepSeek explicitly cited every future item. Zhipu and Qwen each failed to cite
the future item in `case_005`, so citation-only revision retained it.

## By Data Tier

| Tier | Policy | Accuracy | Future retained | Changes vs No Audit |
|---|---|---:|---:|---:|
| Real-source context, 21 model-cases | No Audit | 14/21 | 21/21 | 0/21 |
| Real-source context, 21 model-cases | Timestamp-only | 8/21 | 0/21 | 8/21 |
| Real-source context, 21 model-cases | Citation-only | 8/21 | 0/21 | 8/21 |
| Semi-real, 9 model-cases | No Audit | 4/9 | 9/9 | 0/9 |
| Semi-real, 9 model-cases | Timestamp-only | 0/9 | 0/9 | 4/9 |
| Semi-real, 9 model-cases | Citation-only | 0/9 | 2/9 | 4/9 |

## Interpretation

1. The 60.0% No Audit accuracy is not a valid forecasting gain. It is measured
   after models receive post-cutoff evidence and therefore represents
   look-ahead inflation.
2. Timestamp-only filtering is the strongest implemented policy on evidence
   removal in this dataset: it removes 30/30 future items.
3. Citation-only revision changes the same 12 directions but retains 2 future
   items that were not explicitly cited. It does not outperform timestamp-only
   filtering here.
4. The current experiment therefore validates temporal contamination,
   attribution failure, marginal sensitivity, and revision behavior. It does
   not yet validate an advantage for Full FinLeakAudit.
5. The next method milestone is citation-free semantic attribution under
   uncertain or incomplete availability metadata. That is the condition under
   which a richer evidence-level audit could improve over timestamp filtering.

## Reproduction

```bash
python3 experiments/analyze_baselines.py \
  --output wiki/experiments/three_model_v4_baseline_summary_2026_07_26.csv \
  --case-output wiki/experiments/three_model_v4_case_results_2026_07_26.csv
```

Generated, tracked summaries:

- `wiki/experiments/three_model_v4_baseline_summary_2026_07_26.csv`
- `wiki/experiments/three_model_v4_case_results_2026_07_26.csv`

The policy summary includes pooled, per-model, per-tier, and model-by-tier rows.
The compact case table contains all 30 prediction triples and audit signals
without publishing full model rationales.
