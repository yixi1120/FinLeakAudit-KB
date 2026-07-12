# Evidence Ablation Pilot Results — 2026-07-12

## Purpose

This page records the first leave-one-evidence-out ablation run for Experiment A.
The question is narrower than whether a model cites future evidence:

> Does removing a particular evidence item change the leaky forecast, and is the changed item temporally unavailable?

For each case, the runner first obtains the Leaky forecast, then removes each evidence item once and re-runs the forecast. The ablation is measured against the original Leaky prediction.

## Setup

| Item | Setting |
|---|---|
| Cases | 5 synthetic leakage-injection pilot cases |
| Models | DeepSeek `deepseek-chat`; Zhipu `glm-4-flashx-250414` |
| Ablation | Leave one evidence item out from the Leaky context |
| Future evidence | One `T+1` item per case, `e4` |
| Total ablation items | 20 per model |
| Result files | `experiments/results/*_cases_pilot_ablation_results.jsonl` |

## Aggregate Results

| Model | N | Rationale Leakage Rate | Prediction Flip Rate | Audited Recovery Rate | Future Evidence Flip-Driver Rate | Mean Future Confidence Delta* |
|---|---:|---:|---:|---:|---:|---:|
| DeepSeek | 5 | 1.00 | 1.00 | 1.00 | 1.00 | -0.04 |
| Zhipu GLM | 5 | 1.00 | 0.80 | 1.00 | 0.80 | -0.02 |

`*` Confidence after removing future evidence minus the original Leaky confidence. A negative value means the future evidence increased confidence in the Leaky context on average.

## Findings

- DeepSeek: `e4` was a direction flip driver in all 5 cases. Removing it changed the forecast back from the Leaky direction, while removing the three clean evidence items did not change direction.
- Zhipu: `e4` was a direction flip driver in 4 of 5 cases. In `pilot_002`, both `e2` and `e4` were flip drivers, so the future evidence was influential but not the only influential item.
- Zhipu `pilot_004` again separates rationale contamination from forecast change: the model cited `e4`, but the Leaky prediction did not flip and removing `e4` did not change direction.
- The mean confidence effect is small in this pilot, but it is negative after removing future evidence (`-0.04` DeepSeek; `-0.02` Zhipu), consistent with future evidence increasing Leaky confidence slightly.

## Interpretation

The ablation pilot strengthens the evidence-level thesis: temporal availability alone identifies an invalid item, while leave-one-out ablation estimates whether that item actually mattered to the forecast. These are related but different measurements:

1. Future evidence can be cited without changing direction.
2. Future evidence can change direction and be a flip driver.
3. More than one evidence item can be a flip driver.

The current result is a pilot-level sensitivity analysis, not a causal estimate. The model is re-called for each ablation, and the sample contains only five synthetic cases per backend.

## Reproducibility

Run the ablation:

```bash
python3 experiments/run_experiment.py --model deepseek --limit 5 --with-ablation --overwrite
python3 experiments/run_experiment.py --model zhipu --limit 5 --with-ablation --overwrite
```

Summarize either output:

```bash
python3 experiments/analyze.py --input experiments/results/deepseek_cases_pilot_ablation_results.jsonl
```

## Next Steps

- Scale the dataset from 5 to 20–50 cases and preserve the same ablation protocol.
- Add Qwen2.5-14B ablation when the local server is intentionally restarted for the experiment.
- Add manual semantic-leakage labels for cases where the model paraphrases future evidence without citing its ID.
- Compare flip-driver rates against irrelevant-evidence calibration cases.
