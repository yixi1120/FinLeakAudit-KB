# Experiment A: Leakage Injection

## Research Question

RQ1: Do financial Agentic RAG systems retrieve and use future evidence when forecasting?

## Design

### Data Construction

20–50 earnings-event cases, each with:
- `company`: anonymized (Company A, Company B...)
- `prediction_date`: Day T
- `clean_evidence`: news/articles published before or at T
- `leaked_evidence`: news/articles published at T+1 with strong directional signal

### Three Groups

| Group | Input | Purpose |
|---|---|---|
| Clean | Only pre-T evidence | Baseline |
| Leaky | Pre-T + leaked evidence (T+1) | Measure leakage impact |
| Audited | Full set → FinLeakAudit removes leaked → re-predict | Measure audit effectiveness |

### Anonymization

```
NVIDIA → Company A
TSMC → Supplier B
AI GPU → Product X
2024-05-10 → Day T
2024-05-11 → Day T+1
```

## Metrics

- Future Evidence Adoption Rate: % of cases where leaked evidence enters prediction rationale
- Rationale Leakage Rate: % of prediction claims supported by leaked evidence
- Prediction Flip Rate: % of cases where leaked evidence changes prediction direction
- Confidence Delta: mean confidence change with/without leaked evidence
- Revision Recovery Rate: % of cases where FinLeakAudit correctly identifies and removes leaked evidence

## Expected Results

Hypothesis: Agentic RAG systems will frequently retrieve and use future evidence, leading to inflated confidence and occasional prediction flips.

## Pilot Results — 2026-07-07

See: [[pilot_results_2026_07_07]]

### Setup

- Cases: 5 synthetic leakage-injection pilot cases
- Models:
  - DeepSeek `deepseek-chat`
  - Qwen2.5-14B-Instruct GGUF Q4_K_M, local MacBook deployment
  - Zhipu `glm-4-flashx-250414`
- Groups: Clean / Leaky / Audited
- Output files:
  - `experiments/results/deepseek_pilot_results.jsonl`
  - `experiments/results/qwen_pilot_results.jsonl`
  - `experiments/results/zhipu_pilot_results.jsonl`

### Summary

| Model | Rationale Leakage Rate | Prediction Flip Rate | Audited Recovery Rate | Mean Confidence Delta | Avg. Latency / Case |
|---|---:|---:|---:|---:|---:|
| DeepSeek | 1.00 | 1.00 | 1.00 | +0.04 | 8.55s |
| Qwen2.5-14B | 1.00 | 1.00 | 1.00 | +0.12 | 28.28s |
| Zhipu GLM | 1.00 | 0.80 | 1.00 | +0.01 | 18.13s |

### Takeaway

The pilot supports the Phase 1 premise: when temporally unavailable `T+1` evidence is injected into the context, all three model backends cite it in their rationales, and two of three backends flip forecast direction in all pilot cases. After FinLeakAudit removes the cited future evidence, all audited forecasts recover to the clean-context direction.

### Evidence Ablation Follow-up — 2026-07-12

The first leave-one-evidence-out run is recorded in [[ablation_pilot_results_2026_07_12]]. Across the same five cases, the future `e4` item was a direction flip driver in 5/5 DeepSeek cases and 4/5 Zhipu cases. This provides an initial marginal-impact signal beyond citation-based leakage detection.

Important caveat: this remains a synthetic injection pilot, not evidence that natural RAG retrieval frequently leaks future information. The next step is to scale Experiment A to 20–50 cases, add Qwen ablation when the local server is intentionally restarted, and then run Experiment B for natural leakage.
