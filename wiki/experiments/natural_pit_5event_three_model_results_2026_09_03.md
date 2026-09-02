---
title: Natural point-in-time replay — five-event three-model pilot
date: 2026-09-03
status: completed-three-model-natural-source-replay-pilot
---

# Scope

This pilot replays a frozen query over a directly assembled primary-source candidate
corpus. It compares cutoff-safe retrieval, outcome-bounded unfiltered retrieval, and
timestamp-audited revision. It is not a preserved production RAG trace and does not
estimate the prevalence of leakage in deployed systems.

# Main result

Across 15 model-event runs and 45 prediction calls, cutoff-postdating evidence appeared in 100% of unfiltered top-k contexts and was validly cited by exact ID in 87%. Direction changed in 40% of runs. Among changed runs, timestamp removal restored the Clean direction in 100% (6/6; Wilson 95% interval 61%-100%).

Unfiltered outcome accuracy was 80%, versus 40% for Clean and 33% after audit. The apparent unfiltered gain is
hindsight inflation in this replay, not evidence of a better forecasting system.

Citation-format validation found 13 invalid IDs in 4/45 predictions. Errors include unavailable chunk suffixes and shortened document-level IDs, showing why semantic use cannot be inferred from exact-ID matching alone.

# Model summary

| Model | Runs | Future cited | Direction flip | Recovery on flips | Audited drift on non-flips | Clean acc. | Unfiltered acc. | Audited acc. | Tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deepseek | 5 | 100% | 60% | 100% | 0 | 20% | 80% | 20% | 103955 |
| qwen | 5 | 80% | 40% | 100% | 1 | 40% | 80% | 20% | 108344 |
| zhipu | 5 | 80% | 20% | 100% | 0 | 60% | 80% | 60% | 102585 |

# CrowdStrike case study

The same outcome-bounded event source changed all three model forecasts toward DOWN.
Removing all post-cutoff chunks returned each model to its own cutoff-safe
direction:

| Model | Clean | Unfiltered | Audited | Outcome | Future cited |
|---|---|---|---|---|---|
| deepseek | NEUTRAL | DOWN | NEUTRAL | DOWN | true |
| qwen | NEUTRAL | DOWN | NEUTRAL | DOWN | false |
| zhipu | UP | DOWN | UP | DOWN | true |

# Interpretation boundary

- The five events were selected for heterogeneity, not sampled from production traffic.
- The unfiltered condition is deliberately bounded by outcome time and therefore serves
  as a point-in-time replay stress test.
- Exact-ID citation is not complete semantic attribution; human gold labels for the
  new natural hard set remain future work.
- 4 outputs contained invalid evidence IDs, so citation validity must be checked
  rather than assumed. Qwen's CrowdStrike rationale named future documents but
  omitted their chunk suffixes, causing exact-ID leakage detection to miss them.
- Audited is Unfiltered top-k minus post-cutoff chunks, not a new cutoff-time top-k
  retrieval. One Qwen non-flip changed after deletion because the revised context was
  sparser than Clean; this revision instability is reported separately from recovery.
- Timestamp filtering is a strong deterministic baseline, not the complete planned
  FinLeakAudit semantic operator stack.
- 15 model-event observations are adequate for an RA portfolio pilot, not a paper-level
  general claim.

# Reproduce

```bash
python3 experiments/run_natural_experiment.py --model deepseek --minimal --run-name natural_pit_5event_v1
python3 experiments/run_natural_experiment.py --model zhipu --minimal --run-name natural_pit_5event_v1
python3 experiments/run_natural_experiment.py --model qwen --minimal --run-name natural_pit_5event_v1
python3 experiments/analyze_natural_experiment.py
```

# RA-safe wording

Built a point-in-time replay for five natural financial events and evaluated
three LLMs across 45 prediction calls. Post-cutoff evidence was validly cited by
exact ID in 13/15 model-event runs and changed the forecast direction in 6/15;
timestamp removal restored the corresponding cutoff-safe direction in all six changed
runs. This is a small outcome-bounded stress test, not an estimate of leakage
prevalence in deployed systems.
