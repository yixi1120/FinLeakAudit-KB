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

## Analyze

```bash
python3 experiments/analyze.py --input experiments/results/qwen_cases_pilot_results.jsonl
```

Outputs:

- `experiments/results/qwen_cases_pilot_results.jsonl`
- `experiments/results/qwen_cases_pilot_summary.csv`
