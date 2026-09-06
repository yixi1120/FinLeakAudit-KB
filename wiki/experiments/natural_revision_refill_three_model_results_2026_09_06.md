---
title: Natural revision backfill, five-event three-model comparison
date: 2026-09-06
status: completed-three-model-backfill-comparison
---

# Scope

This experiment adds one Backfilled Audited call to each frozen natural replay
model-event result. It removes post-cutoff items from the actual Unfiltered top-k,
preserves the surviving order, and appends cutoff-safe ranked fallbacks until top-k
is restored. It does not rerun or overwrite Clean, Unfiltered, or Sparse Audited.

# Main result

Across 15 paired model-event runs, Backfilled Audited matched the Clean direction in 15/15 (100.0%; Wilson 95% interval 79.6%-100.0%). Both Sparse and Backfilled revision recovered all 6 initial Clean-to-Unfiltered direction changes.

The distinction appeared on the 9 non-flipped runs: Sparse revision drifted in 1/9, while Backfilled revision drifted in 0/9.

This is one corrected drift in a very small paired sample. It supports context
sparsity as a concrete failure mode, but is not evidence of a statistically reliable
general improvement. Backfilled accuracy was unchanged from Clean because every
Backfilled direction matched Clean.

# Model summary

| Model | Runs | Initial flips | Sparse recovery | Backfilled recovery | Sparse drift / non-flips | Backfilled drift / non-flips | Backfilled = Clean | Tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| deepseek | 5 | 3 | 3/3 | 3/3 | 0/2 | 0/2 | 5/5 | 37693 |
| qwen | 5 | 2 | 2/2 | 2/2 | 1/3 | 0/3 | 5/5 | 39323 |
| zhipu | 5 | 1 | 1/1 | 1/1 | 0/4 | 0/4 | 5/5 | 37052 |

# Retrieval control

The Backfilled evidence sequence exactly matched Clean in 12/15 runs. The three exceptions were the JetBlue event,
where parent-document caps and ranking interactions preserved a different survivor
order. Even there, all three models retained the Clean direction:

| Model | Clean | Sparse Audited | Backfilled Audited | Confidence gap from Clean |
|---|---|---|---|---:|
| deepseek | NEUTRAL | NEUTRAL | NEUTRAL | 0.20 |
| qwen | NEUTRAL | NEUTRAL | NEUTRAL | 0.00 |
| zhipu | UP | UP | UP | 0.00 |

All 15 Backfilled outputs cited evidence. All 53 cited IDs were valid. Total Backfill-only usage was
114,068 tokens. The calls took 692.7 recorded seconds in aggregate, with local
Qwen accounting for most wall time.

# Interpretation boundary

- Backfill controls context size and partially controls retrieval composition; it
  does not prove that the remaining evidence is truthful or decision-relevant.
- Matching Clean is a revision-consistency target, not market accuracy.
- The single Sparse-to-Backfilled drift correction is descriptive. No significance
  claim is made from one discordant paired observation.
- Twelve runs had a Backfilled sequence identical to Clean, so their direction
  agreement is partly expected under temperature-zero replay.
- The JetBlue cases show that Backfilled is not globally equivalent to rerunning
  Clean, although all three directions happened to match here.

# Reproduce

```bash
python3 experiments/run_natural_refill_baseline.py --model deepseek --minimal
python3 experiments/run_natural_refill_baseline.py --model zhipu --minimal
python3 experiments/run_natural_refill_baseline.py --model qwen --minimal
python3 experiments/analyze_natural_refill.py
```
