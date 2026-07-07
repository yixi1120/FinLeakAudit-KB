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

Run only the first case for a smoke test:

```bash
python3 experiments/run_experiment.py --model qwen --limit 1 --overwrite
```

## Analyze

```bash
python3 experiments/analyze.py
```

Outputs:

- `experiments/results/qwen_pilot_results.jsonl`
- `experiments/results/summary.csv`

