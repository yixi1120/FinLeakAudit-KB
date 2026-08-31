# FinLeakAudit Pilot Experiments

This folder contains the minimal runnable engineering pipeline for the leakage injection pilot.

## Start Local Qwen

```bash
llama-server \
  -m /path/to/qwen2.5-14b-instruct-q4_k_m-00001-of-00003.gguf \
  --alias qwen2.5-14b-instruct-q4_k_m \
  --host 127.0.0.1 \
  --port 8080 \
  -c 8192 \
  -ngl 99
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

Build the v4 policy-baseline comparison from the completed three-model result
files:

```bash
python3 experiments/analyze_baselines.py
```

Prepare the blinded claim-evidence annotation batch and coordinator key:

```bash
python3 experiments/prepare_semantic_annotations.py
```

After the dual annotations and adjudication are frozen, run the reproducible
citation-only and lexical attribution comparison without model calls:

```bash
python3 experiments/evaluate_semantic_baselines.py
```

To reproduce the API-based semantic baselines, first generate their blinded
predictions and then include them in the evaluator:

```bash
python3 experiments/run_semantic_embedding_baseline.py
python3 experiments/run_semantic_llm_judge.py --model deepseek
python3 experiments/evaluate_semantic_baselines.py \
  --llm-judge experiments/analysis/semantic_llm_judge_deepseek_v1.jsonl \
  --embedding experiments/analysis/semantic_embedding_zhipu_v1.csv
```

The embedding and LLM scripts never receive the gold-label file. The evaluator
joins predictions to frozen gold only after inference. Thresholds are declared
in the output metadata and were not tuned on the 79 labels.

## Run Offline Logic Tests

The regression tests do not start a model server or call an API:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

The offline tests do not require API keys and do not start Qwen.
