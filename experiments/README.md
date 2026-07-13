# FinLeakAudit Pilot Experiments

This folder contains the minimal runnable engineering pipeline for the leakage injection pilot.

## Start Local Qwen

```bash
/Users/luziyang/qwen-local/start-qwen-server.sh
```

The local OpenAI-compatible endpoint is:

```text
http://127.0.0.1:8080/v1
```

Quick check:

```bash
curl http://127.0.0.1:8080/v1/models
```

## Run Pilot

Run all 5 pilot cases with local Qwen:

```bash
python3 experiments/run_experiment.py --model qwen --overwrite
```

Default result names include the cases file stem to avoid overwriting runs:

```text
experiments/results/qwen_cases_pilot_results.jsonl
experiments/results/qwen_cases_pilot_errors.jsonl
```

Run only the first case for a smoke test:

```bash
python3 experiments/run_experiment.py --model qwen --limit 1 --overwrite
```

By default the runner supports resume. If a result file already contains a
`case_id`, that case is skipped on the next run:

```bash
python3 experiments/run_experiment.py --model deepseek
```

Use `--overwrite` only when you want to delete the existing result and error
files for that model before rerunning.

Retry controls:

```bash
python3 experiments/run_experiment.py --model deepseek --retries 3 --retry-delay 5
```

Failed attempts are written to:

```text
experiments/results/{model}_{cases_file_stem}_errors.jsonl
```

Override the run name or exact output paths when needed:

```bash
python3 experiments/run_experiment.py --model deepseek --run-name cases_20
python3 experiments/run_experiment.py --model deepseek --output experiments/results/debug.jsonl
```

## Run Evidence Ablation

Add `--with-ablation` to run leave-one-evidence-out ablation after the Leaky
prediction. This adds one model call per evidence item in each case.

```bash
python3 experiments/run_experiment.py --model deepseek --limit 1 --with-ablation --overwrite
```

Default ablation outputs are separated from normal runs:

```text
experiments/results/deepseek_cases_pilot_ablation_results.jsonl
experiments/results/deepseek_cases_pilot_ablation_errors.jsonl
```

The Audited prediction is reconstructed from the Leaky evidence set minus the
IDs actually returned by the auditor. It must not be reconstructed from the
Clean evidence set, because that would make recovery look successful even
when the auditor misses the future evidence.

Each ablation item records whether removing that evidence changed the forecast
direction and how confidence changed:

```json
{
  "evidence_id": "e4",
  "is_future_leakage": true,
  "full_prediction": "UP",
  "removed_prediction": "DOWN",
  "direction_changed": true,
  "confidence_delta_removed_minus_full": -0.20,
  "is_flip_driver": true
}
```

## Analyze

```bash
python3 experiments/analyze.py --input experiments/results/qwen_cases_pilot_results.jsonl
```

Outputs:

- `experiments/results/qwen_cases_pilot_results.jsonl`
- `experiments/results/qwen_cases_pilot_summary.csv`

## Run Offline Logic Tests

The regression tests do not start a model server or call an API:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```
