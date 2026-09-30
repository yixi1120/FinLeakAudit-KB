---
title: Novel-safe Backfill, six-event three-model ablation
date: 2026-09-30
status: completed-eligible-subset
---

# Scope

This ablation evaluates only the six events frozen as eligible before model
calls. Newly added evidence is cutoff-safe and excluded from the Clean top-k;
safe survivors from the actual Unfiltered context are retained. Four events
were ineligible because their candidate pools could not restore top-k.

# Main result

Across 18 model-event runs, Sparse matched Clean in 15/18, Standard Backfill in 18/18, and Novel-safe Backfill in 15/18.

On 6 initial flips, recovery was 4/6 Sparse, 6/6 Standard, and 4/6 Novel-safe. On 12 non-flips, drift was 1/12, 0/12, and 1/12, respectively.

Standard was the only method matching Clean in 3 paired runs; Novel-safe was uniquely correct in 0. The exact paired McNemar p-value is 0.25; the eligible subset does not establish a statistically reliable general advantage.

# Model summary

| Model | Runs | Flips | Sparse recovery | Standard recovery | Novel recovery | Sparse / Standard / Novel match Clean |
|---|---:|---:|---:|---:|---:|---:|
| deepseek | 6 | 4 | 3/4 | 4/4 | 3/4 | 5 / 6 / 5 |
| zhipu | 6 | 0 | 0/0 | 0/0 | 0/0 | 6 / 6 / 6 |
| qwen | 6 | 2 | 1/2 | 2/2 | 1/2 | 4 / 6 / 4 |

# Novel-safe mismatches

| Model | Event | Clean | Unfiltered | Sparse | Standard | Novel-safe |
|---|---|---|---|---|---|---|
| deepseek | natural_005 (INTC) | UP | DOWN | DOWN | UP | NEUTRAL |
| qwen | natural_006 (XOM) | NEUTRAL | UP | UP | NEUTRAL | UP |
| qwen | natural_007 (COF) | UP | UP | NEUTRAL | UP | NEUTRAL |

# Input and runtime checks

- Novel-safe input exactly matched Clean in 0/18 runs.
- Novel-safe changed the Sparse direction in 1/18 runs.
- Novel-safe and Standard predictions matched in 15/18 runs.
- Citation validation found 13 invalid IDs across 3/18 outputs.
- Successful outputs used 128646 recorded tokens and 426.8 recorded seconds.
- Qwen natural_007 initially produced seven retained truncated-JSON errors
  because the 8,102-token prompt exhausted an 8,192-token server context.
  The final call used the same model, prompt, temperature, and 700-token output
  cap after restarting llama.cpp with a 16,384-token context.

# Interpretation

Novel-safe did not reproduce the three corrections observed under Standard
Backfill. It matched Sparse on Clean-direction consistency, although DeepSeek
Intel moved from DOWN under Sparse to NEUTRAL under Novel-safe. This supports
the claim that revision behavior depends on the content and ranking of the
replacement evidence, not context count alone. It does not prove that Standard
Backfill is generally superior: the comparison is conditional on a purposively
eligible six-event subset, has only three discordant pairs, and is not significant.

# Paper status

The workshop draft remains unchanged. These results are an experimental
follow-up and require author review before any manuscript revision.
