# Results Draft v1

Status: paper-facing draft generated from frozen experiment outputs. Numbers may
only change when a new model run is added and recorded as a new input artifact.

## RQ1: Does post-cutoff evidence alter financial forecasts?

In the controlled injection study, post-cutoff evidence was explicitly cited in 28/30 model-case runs (93.3%). The forecast category changed between Clean and Leaky conditions in 12/30 runs (40.0%).

| Study | Model | Runs | Valid future citation | Direction changed | Recovered changes | Audited drift without flip | Clean / contaminated / audited accuracy |
|---|---|---:|---:|---:|---:|---:|---:|
| controlled_injection | DeepSeek | 10 | 10/10 | 5/10 | 5/5 | 0 | 3/10 / 7/10 / 3/10 |
| controlled_injection | Zhipu | 10 | 9/10 | 3/10 | 3/3 | 0 | 3/10 / 6/10 / 3/10 |
| controlled_injection | Qwen2.5-14B | 10 | 9/10 | 4/10 | 4/4 | 0 | 2/10 / 5/10 / 2/10 |

The increase in Leaky accuracy is look-ahead inflation, not a valid forecasting gain.
The controlled cases deliberately inject outcome-adjacent evidence and therefore test
the audit premise rather than real-world leakage prevalence.

## RQ2: Does the effect reproduce with archived natural-source evidence?

The natural replay currently includes DeepSeek, Zhipu, Qwen2.5-14B. Across 15 model-event runs, post-cutoff evidence was explicitly cited in 13 runs and changed direction in 6 runs.

| Study | Model | Runs | Valid future citation | Direction changed | Recovered changes | Audited drift without flip | Clean / contaminated / audited accuracy |
|---|---|---:|---:|---:|---:|---:|---:|
| natural_replay | DeepSeek | 5 | 5/5 | 3/5 | 3/3 | 0 | 1/5 / 4/5 / 1/5 |
| natural_replay | Zhipu | 5 | 4/5 | 1/5 | 1/1 | 0 | 3/5 / 4/5 / 3/5 |
| natural_replay | Qwen2.5-14B | 5 | 4/5 | 2/5 | 2/2 | 1 | 2/5 / 4/5 / 1/5 |

This is an outcome-bounded candidate-feed stress test over five selected events. It is
not a preserved production retrieval trace or a frequency estimate for deployed RAG.

## RQ3: Does audit-driven revision restore the cutoff-safe forecast?

All 12/12 changed controlled runs returned to their Clean category after detected future evidence was removed (Wilson 95% CI 75.7% to 100.0%). In the natural replay, the corresponding result was 6/6 (Wilson 95% CI 61.0% to 100.0%). Recovery means agreement with the model's own Clean prediction, not agreement with the market outcome.

One additional revision side effect occurred in 1 natural run: Clean and Unfiltered agreed, but Audited changed after post-cutoff chunks were deleted. In the natural replay, Audited is the Unfiltered top-k with future chunks removed rather than a newly retrieved cutoff-time top-k, so deletion can leave a sparser context. This is reported as revision instability and is not counted as failed recovery.

## RQ4: How well can claim-evidence dependence be detected?

The frozen controlled annotation set contains 79 pairs, of which 78 have decisive
binary gold labels. Citation-only and a blinded DeepSeek judge achieved similar F1,
while lexical and embedding rules had high precision but substantially lower recall.

| Attribution method | Precision | Recall | F1 | FP | FN |
|---|---:|---:|---:|---:|---:|
| Citation-only | 90.9% | 97.6% | 94.1% | 4 | 1 |
| Lexical overlap | 95.5% | 51.2% | 66.7% | 1 | 20 |
| Embedding similarity | 100.0% | 34.1% | 50.9% | 0 | 27 |
| DeepSeek LLM judge | 97.4% | 90.2% | 93.7% | 1 | 4 |

Citation-only remained marginally stronger on this sample (F1 0.941 versus 0.937) and therefore provides no evidence that the semantic judge outperforms the simple baseline. Its four false positives and one citation-free false
negative nevertheless show that explicit citation is not equivalent to semantic
dependence.

## Failure analysis and design consequence

An online smoke test exposed a high-confidence semantic false positive: the candidate
post-cutoff evidence supported an inventory-glut claim, but the same core fact was
already available before cutoff. FinLeakAudit therefore separates two decisions.
Deterministic temporal validation controls compliance removal; semantic attribution
diagnoses which claims appear contaminated and must distinguish support from exclusive
dependence.

The Qwen CrowdStrike replay exposed a separate interface failure. Its rationale named
two post-cutoff documents but omitted the required chunk suffixes. Exact-ID citation
matching therefore recorded no valid future citation even though the claim discussed
the post-cutoff Falcon technical incident. Citation validity and semantic attribution
must consequently be evaluated as separate operators.

## Supported claims

- Post-cutoff evidence can materially change model forecasts in controlled injections
  and in a small natural-source replay.
- Removing temporally invalid evidence restores the model's cutoff-safe category in all
  observed changed runs, with wide uncertainty intervals due to small denominators.
- Citation-only auditing is incomplete, but current controlled data do not show that an
  LLM semantic judge is superior.

## Claims not supported

- The experiments do not estimate how often deployed financial RAG systems leak.
- Recovery does not demonstrate improved stock-prediction accuracy.
- Leave-one-out sensitivity is not a causal effect.
- The current evidence does not establish Full FinLeakAudit as state of the art.
