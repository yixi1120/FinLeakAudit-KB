---
title: Semantic attribution baseline evaluation
date: 2026-08-31
status: completed-controlled-pilot
---

# Question

Can automatic methods determine whether a forecast-rationale claim depends on
a specific post-cutoff evidence item, rather than merely mentioning the same
topic or explicitly citing its ID?

# Evaluation set

- 79 blinded `claim x post-cutoff evidence` pairs from the controlled v4 runs.
- Gold labels: 41 `yes`, 37 `no`, and 1 `uncertain` after dual independent
  annotation and coordinator adjudication.
- Binary metrics use 78 decisive labels; the gold `uncertain` row is excluded.
- Positive means semantic dependency. A predicted `uncertain` is treated as
  `other` for the yes-versus-other comparison.
- The coordinator key was not exposed during annotation. It was released only
  after gold-label freeze so citation-only results can be reproduced.

# Baselines

| Baseline | Decision rule |
|---|---|
| Citation-only | Predict dependency when the rationale explicitly cites the candidate future evidence ID. |
| Lexical overlap | Compare claim-to-future token overlap against the strongest claim-to-past overlap; threshold 0.35 and margin 0.08. |
| Embedding similarity | Use Zhipu `embedding-3`, 512 dimensions; require cosine similarity at least 0.65 and a future-minus-past margin of 0.03. |
| Blind LLM judge | DeepSeek `deepseek-chat`, temperature 0; show only the claim, pre-cutoff evidence, and candidate post-cutoff evidence. |

The lexical and embedding thresholds were declared before inspecting their
gold-label metrics and were not optimized on this dataset. The embedding run
used 3,852 tokens. The LLM-judge run used 32,948 provider-reported tokens.

# Results

| Baseline | Accuracy | Precision | Recall | Specificity | F1 | TP / FP / FN / TN |
|---|---:|---:|---:|---:|---:|---:|
| Citation-only | 93.6% | 90.9% | 97.6% | 89.2% | 94.1% | 40 / 4 / 1 / 33 |
| Lexical overlap | 73.1% | 95.5% | 51.2% | 97.3% | 66.7% | 21 / 1 / 20 / 36 |
| Embedding similarity | 65.4% | 100.0% | 34.1% | 100.0% | 50.9% | 14 / 0 / 27 / 37 |
| Blind LLM judge | 93.6% | 97.4% | 90.2% | 97.3% | 93.7% | 37 / 1 / 4 / 36 |

Wilson 95% intervals are stored with the machine-readable results. The point
estimates should not be ranked as if differences of a few tenths of a percentage
point were stable: the evaluation set is small and controlled.

# What the errors show

Citation-only is a strong shortcut in this dataset because the predictor prompt
asked models to cite evidence IDs. It is still not semantic attribution:

- Four citation-only false positives explicitly cited future evidence even
  though pre-cutoff evidence already supported the claim's core content.
- One false negative (`semantic_v1_074`) did not cite the future evidence ID,
  but human adjudication found that the claim's reference to mixed current
  results semantically depended on the future report.
- Lexical and embedding margin rules were conservative. Their high precision
  came with 20 and 27 false negatives respectively.
- The blind LLM judge reduced these false negatives to four, but still missed
  the citation-free sample and introduced one false positive.

# Interpretation boundary

This is evidence for a measurable gap between explicit citation and semantic
dependency in a controlled pilot. It is not evidence that the current semantic
baselines outperform citation-only, and it does not establish performance on
natural financial retrieval traces. The next dataset must deliberately include
more citation-free dependencies, redundant citations, paraphrases, conflicting
evidence, and hard negatives; otherwise citation-only remains artificially easy.

# Reproduction

```bash
python3 experiments/run_semantic_embedding_baseline.py
python3 experiments/run_semantic_llm_judge.py --model deepseek
python3 experiments/evaluate_semantic_baselines.py \
  --llm-judge experiments/analysis/semantic_llm_judge_deepseek_v1.jsonl \
  --embedding experiments/analysis/semantic_embedding_zhipu_v1.csv
```

Tracked outputs:

- `experiments/analysis/semantic_baseline_predictions_v1.csv`
- `experiments/analysis/semantic_baseline_results_v1.json`
- `experiments/analysis/semantic_embedding_zhipu_v1.csv`
- `experiments/analysis/semantic_embedding_zhipu_v1.json`
- `experiments/analysis/semantic_llm_judge_deepseek_v1.jsonl`

# External API reference

The embedding endpoint and model parameters follow the official Zhipu
Embedding-3 documentation:
https://docs.bigmodel.cn/cn/guide/models/embedding/embedding-3

# Online-loop follow-up (2026-09-02)

The blinded judge was integrated into the controlled experiment runner. A
`case_005` smoke run produced a high-confidence semantic false positive: the
judge treated post-cutoff confirmation of an inventory glut as a new dependency,
although pre-cutoff evidence already stated that the company faced a severe
inventory glut. This confirms that the LLM judge cannot be the sole authority
for point-in-time evidence removal.

The runner now separates compliance from attribution. `full_semantic` removes
all known post-cutoff evidence using deterministic timestamps, while semantic
judgments describe claim contamination. The selective `semantic_llm` policy is
retained only as an experimental baseline. Full details are in
`wiki/experiments/full_semantic_loop_smoke_2026_09_02.md`.
