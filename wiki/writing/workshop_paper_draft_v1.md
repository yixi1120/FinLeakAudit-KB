---
title: "FinLeakAudit: Evidence-Level Point-in-Time Auditing for Financial Agentic RAG"
status: results-draft
target: workshop-paper
date: 2026-09-06
---

# Abstract

Financial forecasting systems built on retrieval-augmented large language models can
silently consume evidence that was unavailable at the historical prediction cutoff.
This produces plausible rationales and inflated backtest accuracy without preserving
the information set available to a real decision maker. We present FinLeakAudit, an
evidence-level audit protocol that separates point-in-time availability, structured
citation validity, claim-evidence attribution, marginal forecast sensitivity, and
leakage-driven revision. In a controlled 10-case study across three LLMs, post-cutoff
evidence was cited in 28/30 model-case runs and changed the forecast category in
12/30. Removing temporally invalid evidence restored the corresponding Clean category
in 12/12 changed runs, with a Wilson 95% interval of 75.7% to 100%. A 10-event
natural-source replay across the same three models produced 13 direction changes in
30 model-event runs. Sparse deletion recovered 11/13 changes, while rank-preserving
cutoff-safe backfill recovered 13/13 and matched the Clean direction in 30/30 runs
(Wilson 95% interval 88.6% to 100%). Backfill corrected three Sparse mismatches, but
24/30 inputs were identical to Clean and the exact paired McNemar p-value was 0.25.
A separate 79-pair human annotation study found that citation-only attribution
remained slightly stronger than a blinded LLM judge on the controlled sample, while
exposing both malformed citations and support-without-dependence errors. These
findings support the feasibility of
evidence-level temporal auditing but do not estimate leakage prevalence or demonstrate
improved forecasting accuracy. We release the pipeline, frozen replay artifacts, and
failure-preserving evaluation protocol as a controlled research pilot.

# 1. Introduction

Historical financial forecasting requires an information boundary: every document
used by the system must have been available no later than the decision cutoff. Agentic
RAG complicates this requirement because retrieval, synthesis, citation, and forecast
revision can each introduce or conceal look-ahead information. A forecast may cite a
post-cutoff source directly, paraphrase it without a valid evidence ID, or change after
an unavailable item enters the context.

Existing work studies financial Agentic RAG, look-ahead bias, agent-level leakage,
forecast faithfulness, and runtime verification. FinLeakAudit focuses on the audit
trail connecting an individual retrieved item to a forecast claim and subsequent
revision. It is not a new stock-prediction architecture.

This paper asks four questions:

1. Does post-cutoff evidence alter model forecasts under controlled injection?
2. Does the same effect appear in a small replay built from archived primary sources?
3. Does deleting invalid evidence restore the model's cutoff-safe prediction, and can
   deletion itself introduce revision instability?
4. How accurately do citation, lexical, embedding, and LLM-based methods identify
   claim-evidence dependence?

Our current contributions are deliberately bounded:

- An evidence-level point-in-time audit protocol with explicit predictor, auditor, and
  evaluator information boundaries.
- A paired Clean, contaminated, Sparse Audited, and Backfilled Audited evaluation
  design for measuring forecast change and revision instability.
- A controlled three-model pilot, a primary-source natural replay, and a human-labeled
  claim-evidence attribution benchmark with failure-level logs.

# 2. Related Work

## 2.1 Financial LLMs and Agentic RAG

Discuss CARAG, MarketSenseAI, Multi-HyDE, FinAgent-RAG, and representative financial
LLM foundations. The distinction is that FinLeakAudit audits a host forecasting
workflow rather than proposing a stronger predictor.

## 2.2 Look-Ahead Bias and Financial Leakage

Discuss Profit Mirage, Look-Ahead-Bench, Leakage-Aware Benchmarking, and OpenFinGym.
Position FinLeakAudit at the retrieved-evidence and claim-revision level. Do not claim
to be the first study of financial-agent leakage.

## 2.3 Evidence Attribution and Forecast Faithfulness

Discuss citation faithfulness, textual entailment, evidence ablation, and LLM
Forecasters Faithfulness. Leave-one-out results are marginal sensitivity, not causal
effects.

## 2.4 Verification and Revision

Discuss VERAFI, FinVet, FLAIRR-TS, and SHARP. Distinguish leakage-driven revision from
accuracy-driven self-correction.

TODO: convert the existing paper cards into a checked bibliography and add only claims
supported by primary paper text.

# 3. Problem Formulation

Let a forecasting event have prediction cutoff \(\tau\), forecast horizon \(h\), and a
retrieved evidence set \(E = \{e_1, \ldots, e_k\}\). Each item has a verifiable
availability time \(a(e_i)\). An item is point-in-time valid when
\(a(e_i) \leq \tau\), and post-cutoff otherwise.

A predictor \(f\) maps the predictor-visible evidence text to a categorical forecast
\(y \in \{UP, DOWN, NEUTRAL\}\), a confidence value, and a set of rationale claims.
The predictor never sees audit labels, outcome labels, or availability timestamps.

We distinguish four evidence conditions:

- Clean: cutoff-time retrieval containing only available evidence.
- Unfiltered/Leaky: retrieval that contains one or more post-cutoff items.
- Sparse Audited: the actual Unfiltered set minus temporally invalid items.
- Backfilled Audited: Sparse Audited supplemented with cutoff-safe ranked fallbacks.

Recovery is defined only when Clean and Unfiltered directions differ. A recovered run
has an Audited direction equal to Clean. Revision drift is defined on non-flipped runs
where Clean equals Unfiltered but Audited differs from Clean.

# 4. FinLeakAudit

## 4.1 Information Separation

Document the exact fields visible to the predictor, temporal auditor, semantic
attribution judge, and evaluator. The predictor sees evidence IDs and text only. The
temporal operator receives timestamps and provenance. Gold outcomes remain evaluator
only.

## 4.2 Point-in-Time Availability

Normalize timezone-aware availability timestamps and compare them with \(\tau\).
Current natural cases use archived primary-source timestamps and human cross-checking.
Market-calendar alignment, original/revision/vendor timestamps, and ambiguous
availability remain partially implemented or planned and must be stated as such.

## 4.3 Citation Validation

Validate cited IDs against the exact evidence IDs exposed in the prompt. Record
shortened, fabricated, or unavailable IDs rather than silently normalizing them. A
malformed citation is an interface failure and does not prove semantic independence.

## 4.4 Claim-Evidence Attribution

Compare explicit citation, lexical overlap, embedding similarity, and a blinded LLM
judge. The semantic judge sees a claim, pre-cutoff evidence text, and one post-cutoff
candidate, but not model identity, event identity, timestamps, citation flags, or
outcomes. Separate candidate support from exclusive dependence.

## 4.5 Marginal Evidence Sensitivity

Remove one evidence item at a time and rerun the predictor. Report category changes and
confidence deltas as marginal sensitivity. Do not use causal language.

## 4.6 Revision Policies

Sparse deletion preserves the actual contaminated retrieval set minus invalid items.
Backfilled deletion preserves surviving order and fills empty slots with the highest
ranked cutoff-safe evidence not already present. Temporal validity controls compliance
removal; semantic attribution diagnoses contamination but does not override known
post-cutoff status.

# 5. Data

## 5.1 Controlled Injection Set

Ten controlled cases include seven cases grounded in verified SEC-source contexts and
three semi-real cases. Each case has Clean evidence plus one post-cutoff item. This set
tests the premise and pipeline; it is not a sample of naturally occurring leakage.

## 5.2 Natural Point-in-Time Replay

Ten selected events use frozen queries, archived primary-source documents, lexical
retrieval, and top-k evidence. Clean retrieval is bounded by the prediction cutoff;
Unfiltered retrieval is bounded by outcome time. This is a constructed candidate-feed
stress test, not a production retrieval trace.

## 5.3 Semantic Attribution Gold

The controlled annotation set contains 79 claim-evidence pairs labeled independently
by two annotators and adjudicated by the coordinator. Binary metrics exclude one
uncertain gold label. A separate natural 82-pair event-level Dev/Test split is frozen
before labeling and is not used for current claims.

# 6. Experimental Setup

## 6.1 Models

- DeepSeek `deepseek-chat`, temperature 0.
- Zhipu `glm-4-flashx-250414`, temperature 0.
- Qwen2.5-14B-Instruct GGUF Q4_K_M through llama.cpp, temperature 0.

Record API dates, local runtime commit, prompt hashes, token usage, and errors. Provider
temperature 0 is not treated as proof of deterministic serving.

## 6.2 Baselines

- No Audit.
- Timestamp-only filtering.
- Citation-only audit.
- Delete-All-Future-Evidence.
- Leave-One-Out marginal sensitivity.
- Sparse Audited revision.
- Rank-Preserving Backfilled Audited revision.
- Full FinLeakAudit diagnostic pipeline.

## 6.3 Metrics

Report exact counts before percentages. Forecast metrics include future-citation rate,
direction-change rate, conditional recovery, revision drift on non-flips, rationale
purity, invalid citation count, confidence change, token cost, and runtime. Attribution
metrics include precision, recall, F1, specificity, false-positive rate, and human
agreement. Use Wilson intervals for binomial proportions with small denominators.

# 7. Results

## 7.1 Controlled Evidence Injection

Across 30 model-case runs and 210 calls, 28/30 runs cited the future item and 12/30
changed direction. All 12 changed runs returned to Clean after removal, with a Wilson
95% interval of 75.7% to 100%.

## 7.2 Natural Replay

Across 30 model-event runs and 120 retained predictions, post-cutoff evidence was
explicitly cited in 27/30 Unfiltered runs and direction changed in 13/30. Sparse
deletion recovered 11/13 changes. Rank-preserving cutoff-safe backfill recovered
13/13 changes (Wilson 95% interval 77.2% to 100%) and matched the Clean direction in
30/30 runs (Wilson 95% interval 88.6% to 100%). On 17 non-flipped runs, Sparse drifted
in 1/17 and Backfilled in 0/17.

Backfill corrected three Sparse mismatches, but its evidence sequence was identical
to Clean in 24/30 runs. The exact paired McNemar p-value was 0.25. The result therefore
diagnoses concrete context-sparsity failures and demonstrates replay consistency in
this sample; it does not establish a statistically reliable general advantage.

## 7.3 Attribution Baselines

On 78 decisive gold pairs, citation-only achieved F1 0.941 and the blinded DeepSeek
judge achieved F1 0.937. Lexical overlap and embedding similarity achieved F1 0.667
and 0.509. The current data do not show semantic-judge superiority.

## 7.4 Failure Cases

- Qwen CrowdStrike: future documents were named without chunk suffixes, so exact-ID
  matching missed an otherwise visible semantic dependency.
- Zhipu semantic smoke: post-cutoff evidence supported an inventory-glut claim, but the
  same fact was already available before cutoff; the judge produced a high-confidence
  support-without-dependence false positive.
- Qwen Capital One: Clean and Unfiltered were both UP, while Sparse Audited became
  NEUTRAL after deletion left six rather than eight items. Rank-preserving safe
  backfill restored UP.
- DeepSeek Intel: Clean was UP and Unfiltered became DOWN, but Sparse remained DOWN;
  safe backfill restored UP.
- Qwen Exxon: Clean was NEUTRAL and Unfiltered became UP, but Sparse remained UP;
  safe backfill restored NEUTRAL.
- DeepSeek JetBlue: Backfilled preserved the Clean `NEUTRAL` direction despite a
  non-identical evidence sequence, but confidence increased from 0.65 to 0.85. Matching
  direction therefore does not imply identical model state or calibration.

The current natural-replay table, comparison figure, and detailed integrity checks are
maintained in
`wiki/experiments/natural_pit_10event_three_model_results_2026_09_06.md`.

# 8. Discussion

The evidence supports an auditability claim, not a forecasting-performance claim.
Perfect timestamps make timestamp filtering a strong baseline. The value of richer
operators appears when citations are malformed, evidence is semantically absorbed
without exact attribution, timestamps are uncertain or revised, and deletion changes
the evidence distribution.

The Backfilled baseline tests whether sparse revision side effects can be reduced
without reintroducing future evidence. It must be evaluated independently rather than
retroactively replacing Sparse Audited results. The current comparison corrects three
observed Sparse mismatches, but the exact paired test is not significant and inputs
are frequently identical to Clean. It remains a failure diagnosis rather than a
method-superiority result.

# 9. Limitations and Ethics

- Ten natural events and 30 model-event runs are too small for prevalence claims.
- Event selection is purposive and outcome-bounded.
- Controlled injections are intentionally easy relative to production retrieval.
- Natural semantic Test labels are not yet available.
- API model aliases may change behind stable provider names.
- Market outcomes are noisy and are not used to justify evidence removal.
- The project is a reliability benchmark, not investment advice or a trading system.

# 10. Author Contributions

Draft from repository-visible records, to be confirmed by every contributor before
submission: Lu Ziyang coordinated the project, adjudicated annotation disagreements,
and implemented and ran the current experiment pipeline. Zhang Yating completed
Annotator A labels and independently verified the natural-source metadata. Chen Junwei
completed Annotator B labels. Final author order, manuscript-writing roles, and any
additional contributions must be agreed by the team rather than inferred from this
draft.

# 11. Conclusion

FinLeakAudit demonstrates a reproducible way to audit whether financial RAG forecasts
respect point-in-time evidence boundaries and whether removing invalid evidence changes
their conclusions. The pilot exposes both leakage-driven forecast changes and audit
failure modes. Larger natural event sets, frozen semantic evaluation, and revision
policy comparisons are required before broader claims.

# Reproducibility Checklist

- [x] Predictor/auditor/evaluator visibility boundaries documented.
- [x] Three model configurations recorded.
- [x] Raw model outputs and generated summary tables retained.
- [x] Point-in-time source corpus cross-checked with hashes.
- [x] Random seeds or deterministic retrieval policies recorded where applicable.
- [x] Error rows and malformed citation IDs retained.
- [x] Unit and data-validation tests provided.
- [x] Full ten-event, three-model natural replay complete.
- [x] Backfilled baseline complete across all three models and ten events.
- [ ] Natural semantic Test gold frozen and evaluated once.
- [ ] Final bibliography and venue formatting complete.
