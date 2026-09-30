---
title: Novel-safe Backfill offline eligibility
date: 2026-09-30
status: frozen-before-model-calls
---

# Scope

This check excludes the Clean top-k only for newly added evidence. Safe
survivors from the actual Unfiltered context are retained. Candidates are
ranked using the frozen cutoff-time lexical retrieval and parent-document cap.
No outcome label or model prediction is used.

# Eligibility result

6/10 events can be refilled to top-k using cutoff-safe evidence
outside the Clean top-k. The remaining events are frozen as incomplete and
must not be silently included in a complete-case model comparison.

| Event | Ticker | Sparse | Needed | Safe pool | Novel candidates | Added | Complete |
|---|---|---:|---:|---:|---:|---:|---|
| natural_001 | CRWD | 5 | 3 | 8 | 0 | 0 | no |
| natural_002 | NVDA | 6 | 2 | 12 | 4 | 2 | yes |
| natural_003 | NKE | 6 | 2 | 8 | 0 | 0 | no |
| natural_004 | SBUX | 6 | 2 | 9 | 1 | 1 | no |
| natural_005 | INTC | 6 | 2 | 10 | 2 | 2 | yes |
| natural_006 | XOM | 6 | 2 | 15 | 7 | 2 | yes |
| natural_007 | COF | 6 | 2 | 14 | 6 | 2 | yes |
| natural_008 | MSFT | 6 | 2 | 8 | 0 | 0 | no |
| natural_009 | UNH | 7 | 1 | 10 | 2 | 1 | yes |
| natural_010 | JBLU | 6 | 2 | 10 | 2 | 2 | yes |

# Frozen complete-case set

natural_002, natural_005, natural_006, natural_007, natural_009, natural_010

# Frozen incomplete set

natural_001, natural_003, natural_004, natural_008

# Interpretation boundary

- This is an input-eligibility result, not a model-performance result.
- Complete-case model results will be conditional on this six-event subset.
- Expanding the four incomplete candidate pools requires a separately frozen
  source-collection protocol; sources must not be chosen using outcomes.
- The workshop paper remains unchanged until model calls and analysis finish.
