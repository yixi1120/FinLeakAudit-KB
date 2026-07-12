# Pilot Results — 2026-07-07

## Context

This page records the first runnable FinLeakAudit engineering pilot for Experiment A: leakage injection.

The purpose was not to claim full experimental validity, but to test the minimum premise:

> Future evidence enters the input context → the model cites it → the forecast changes → FinLeakAudit removes the leaked evidence → the forecast recovers.

## Setup

| Item | Setting |
|---|---|
| Cases | 5 synthetic leakage-injection pilot cases |
| Evidence design | `clean_evidence` at `T-*`; one injected `leaked_evidence` at `T+1` |
| Groups | Clean / Leaky / Audited |
| Audit implementation | Temporal availability check + citation-based rationale leakage detection + forecast revision |
| Result files | `experiments/results/*_pilot_results.jsonl` |

## Model Backends

| Model | Backend | Notes |
|---|---|---|
| DeepSeek | API | `deepseek-chat` |
| Qwen2.5-14B | Local GGUF | Q4_K_M on MacBook via `llama-cpp-python` |
| Zhipu GLM | API | `glm-4-flashx-250414` |

## Aggregate Results

| Model | N | Rationale Leakage Rate | Prediction Flip Rate | Audited Recovery Rate | Mean Confidence Delta | Avg. Latency / Case |
|---|---:|---:|---:|---:|---:|---:|
| DeepSeek | 5 | 1.00 | 1.00 | 1.00 | +0.04 | 8.55s |
| Qwen2.5-14B | 5 | 1.00 | 1.00 | 1.00 | +0.12 | 28.28s |
| Zhipu GLM | 5 | 1.00 | 0.80 | 1.00 | +0.01 | 18.13s |

## Per-Model Interpretation

### DeepSeek

- Cited future evidence in all 5 pilot cases.
- Flipped forecast direction in all 5 pilot cases.
- Recovered to the clean-context direction in all 5 audited cases.
- Confidence increased only slightly on average (`+0.04`), so the main effect is direction flip rather than confidence inflation.

### Qwen2.5-14B

- Cited future evidence in all 5 pilot cases.
- Flipped forecast direction in all 5 pilot cases.
- Recovered to the clean-context direction in all 5 audited cases.
- Had the largest mean confidence increase (`+0.12`), suggesting injected future evidence made this backend more confident.
- Slowest backend in this pilot because it runs locally on MacBook.

### Zhipu GLM

- Cited future evidence in all 5 pilot cases.
- Flipped forecast direction in 4 of 5 pilot cases.
- Recovered to the clean-context direction in all audited cases.
- `pilot_004` is important: the model cited `T+1` evidence but did not flip direction. This shows leakage can contaminate rationale without necessarily changing the final forecast direction.

## Key Finding

The pilot supports the core Phase 1 premise across three model backends:

> When injected future evidence is present, models cite it in their rationales and often change forecast direction. Removing the cited future evidence restores the clean-context forecast direction.

This strengthens the motivation for evidence-level audit: leakage should be measured not only by whether future evidence exists in the context, but also by whether it is cited, supports a claim, changes confidence, or flips the forecast.

## Best Case Study Candidate

`pilot_004` is useful because it separates two phenomena:

- Qwen and DeepSeek: future negative guidance flips the prediction from UP to DOWN.
- Zhipu: future negative guidance is cited but does not flip the final prediction.

This case can illustrate why FinLeakAudit should track multiple leakage effects:

- rationale contamination
- confidence change
- direction flip
- revision recovery

## Evidence Ablation Follow-up — 2026-07-12

The first leave-one-evidence-out ablation run is recorded in [[ablation_pilot_results_2026_07_12]]. On the same five cases, the future `T+1` item `e4` was a direction flip driver in all DeepSeek cases and 4 of 5 Zhipu cases. This separates the presence or citation of future evidence from its marginal influence on the forecast.

## Caveats

- Only 5 pilot cases; statistical conclusions are not stable.
- Synthetic injection tests context contamination, not natural retrieval leakage.
- Current leakage detection is citation-based; semantic leakage remains unimplemented.
- The ablation follow-up still uses only 5 synthetic cases per backend; its sensitivity estimates are not stable enough for a general claim.

## Next Steps

- Expand Experiment A to 20 then 50 cases.
- Add retry/resume for API runs.
- ~~Implement leave-one-out evidence ablation.~~ Done for DeepSeek and Zhipu on the 5-case pilot; Qwen and larger samples remain.
- Add semantic leakage detection or manual semantic leakage annotation.
- Add calibration cases with irrelevant evidence.
- Update analysis metrics for model-level comparison tables.
