---
title: Full semantic audit loop smoke test
date: 2026-09-02
status: completed-with-failure-diagnosis
---

# Objective

Validate the executable loop:

`Leaky forecast -> blinded semantic attribution -> removal decision -> revised forecast`

This is an engineering and failure-diagnosis smoke test, not a paper-scale
comparison.

# Implemented policies

| Policy | Removal authority | Semantic role |
|---|---|---|
| `citation_only` | Explicit future evidence IDs in rationale | None |
| `timestamp_only` | Deterministic post-cutoff classification | None |
| `semantic_llm` | LLM dependency judgment | Experimental selective baseline only |
| `full_semantic` | Deterministic post-cutoff classification | Contamination attribution and explanation |

The key design decision is that semantic attribution does not grant permission
to retain known future evidence. Timestamp validity and semantic use are
different questions.

# Smoke 1: DeepSeek predictor and judge

- Case: `case_002` (Target)
- Predictor and judge model ID: `deepseek-chat`
- Policy: experimental `semantic_llm`
- Directions: Clean `DOWN`, Leaky `UP`, Audited `DOWN`
- Explicit future citation: yes
- Semantic dependency detected: yes
- Evaluated pairs: 3 claims x 1 future item
- Removed evidence: `e4`
- Combined provider-reported usage: 3,203 tokens
- Errors: 0

This validates the code path but does not show an advantage over citation-only,
because the future item was explicitly cited.

One pair was labeled `relation=contradict` even though the accompanying reason
said the future evidence supplied the claim's positive result. Relation labels
were not used for removal. This inconsistency keeps the support/contradiction
operator in planned status until it receives a separate protocol and gold-label
evaluation.

# Smoke 2: Zhipu predictor, DeepSeek judge

- Case: `case_005` (Enphase Energy)
- Predictor model ID: `glm-4-flashx-250414`
- Judge model ID: `deepseek-chat`
- Policy: `full_semantic`
- Directions: Clean `DOWN`, Leaky `DOWN`, Audited `DOWN`
- Explicit future citation: no
- Semantic dependency detected: yes
- Evaluated pairs: 6 claims x 1 future item
- Removed evidence: `e4`
- Removal basis: `post_cutoff_timestamp`
- Audit coverage: complete
- Final successful case attempt: 3
- Successful-attempt provider-reported usage: 4,562 tokens

The sixth claim said that the company faced a severe inventory glut. The judge
returned `semantic_dependency=yes` with confidence 0.90 because the post-cutoff
report confirmed inventory-related shipment reductions. However, pre-cutoff
`e1` already stated that analysts expected poor guidance amid a severe inventory
glut. Under the frozen human protocol this is not exclusive post-cutoff
dependency. It is a high-confidence online false positive.

Because `full_semantic` assigns removal authority to deterministic timestamps,
`e4` was removed for being post-cutoff, not because of the false-positive LLM
judgment. The forecast direction did not change, so this case demonstrates
rationale-contamination detection and compliance separation, not directional
recovery.

# Reliability observation

The full smoke encountered two transient connection resets: one prediction call
and one semantic-judge call. The existing case-level retry completed on attempt
3. Semantic-judge calls now also have local short retries so a transient judge
failure need not repeat already completed predictor calls in future runs.

# Claim boundary

Supported:

- the semantic audit path is executable and records pair-level decisions;
- citation-free candidates can be surfaced for human or calibrated review;
- deterministic time filtering protects compliance from LLM attribution errors.

Not supported:

- semantic attribution outperforms citation-only or timestamp-only;
- the detected `case_005` semantic dependency was correct;
- semantic revision improves forecast accuracy;
- the current smoke generalizes to natural retrieval traces.

In the current controlled construction, Leaky evidence is Clean evidence plus
known future items. Therefore `full_semantic` and `timestamp_only` remove the
same items and should produce the same revised input. Semantic attribution adds
diagnosis, not a directional-recovery advantage, in this setting.

# Next experiment

Before a three-model rerun, construct a frozen hard set with redundant future
confirmation, citation-free paraphrase, conflicting evidence, and unrelated but
semantically similar negatives. Use separate development data for thresholds and
prompt changes, then evaluate once on untouched test data.

# Artifacts

- `experiments/results/deepseek_semantic_loop_smoke_20260902_semantic_llm_results.jsonl`
  (`SHA-256 17594dc80625d2f027c7c288f9435bdd0d3ecf5148e0d6d938097e8ee38fda4d`)
- `experiments/results/zhipu_full_semantic_case005_20260902_full_semantic_results.jsonl`
  (`SHA-256 45a353f63fe4338097ff8f3bad64af19fff91e2ad7d9a30771348d1a01207e28`)

The local error log is intentionally not published because raw tracebacks embed
machine-specific paths. The two sanitized failure types and retry sequence are
recorded in the Reliability observation above.
