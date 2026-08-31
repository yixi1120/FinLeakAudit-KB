---
title: Natural point-in-time replay — five-event pilot
date: 2026-08-19
status: controlled-natural-source-replay-pilot
---

# Scope

This pilot replays a frozen query over a directly assembled primary-source candidate
corpus. It compares cutoff-safe retrieval, outcome-bounded unfiltered retrieval, and
timestamp-audited revision. It is not a preserved production RAG trace and does not
estimate the prevalence of leakage in deployed systems.

# Main result

Across 10 model-event runs and 30 prediction calls, cutoff-postdating evidence appeared in 100% of unfiltered top-k contexts and was explicitly cited in 90%. Direction changed in 40% of runs. Among changed runs, timestamp removal restored the Clean direction in 100% (4/4; Wilson 95% interval 51%-100%).

Unfiltered outcome accuracy was 80%, versus 40% for Clean and 40% after audit. The apparent unfiltered gain is
hindsight inflation in this replay, not evidence of a better forecasting system.

Citation-format validation found 5 invalid IDs in 2/30 predictions: one output invented unavailable chunk suffixes and another shortened chunk IDs to document IDs.

# Model summary

| Model | Runs | Future cited | Direction flip | Recovery on flips | Clean acc. | Unfiltered acc. | Audited acc. | Tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| deepseek | 5 | 100% | 60% | 100% | 20% | 80% | 20% | 103955 |
| zhipu | 5 | 80% | 20% | 100% | 60% | 80% | 60% | 102585 |

# CrowdStrike case study

The same outcome-bounded event source changed both model forecasts toward DOWN.
Removing all post-cutoff chunks returned each model to its own cutoff-safe
direction:

| Model | Clean | Unfiltered | Audited | Outcome | Future cited |
|---|---|---|---|---|---|
| deepseek | NEUTRAL | DOWN | NEUTRAL | DOWN | true |
| zhipu | UP | DOWN | UP | DOWN | true |

# Interpretation boundary

- The five events were selected for heterogeneity, not sampled from production traffic.
- The unfiltered condition is deliberately bounded by outcome time and therefore serves
  as a point-in-time replay stress test.
- Explicit citation is not complete semantic attribution; the separate 79-pair semantic
  attribution set completed dual annotation and coordinator adjudication on 2026-08-31.
- Two outputs contained invalid evidence IDs, so citation validity must be checked
  rather than assumed.
- Timestamp filtering is a strong deterministic baseline, not the complete planned
  FinLeakAudit semantic operator stack.
- Ten model-event observations are adequate for an RA portfolio pilot, not a paper-level
  general claim.

# Post-run source-verification amendment

Independent verification completed on 2026-08-31 for 139 sampled source records:
133 were accepted, one timestamp was rejected, and five required coordinator
adjudication. `natural_001_doc_011` was corrected from 09:45 UTC to 05:30 UTC as
its first publication time; 09:45 UTC is the update time. Both timestamps are
post-cutoff and before the outcome bound, so Clean/Unfiltered/Audited membership,
retrieved text, model inputs, and the reported pilot metrics are unchanged. Four
date-only CrowdStrike pages remain blocked, and the JetBlue court document retains
an explicitly labeled date-only conservative upper bound.

# Reproduce

```bash
python3 experiments/run_natural_experiment.py --model deepseek --minimal --run-name natural_pit_5event_v1
python3 experiments/run_natural_experiment.py --model zhipu --minimal --run-name natural_pit_5event_v1
python3 experiments/analyze_natural_experiment.py
```

# RA-safe wording

Built a point-in-time replay for five natural financial events and evaluated
two LLMs across 30 prediction calls. Post-cutoff evidence was explicitly cited
in 9/10 model-event runs and changed the forecast direction in 4/10; timestamp
removal restored the corresponding cutoff-safe direction in all four changed
runs. This is a small outcome-bounded stress test, not an estimate of leakage
prevalence in deployed systems.
