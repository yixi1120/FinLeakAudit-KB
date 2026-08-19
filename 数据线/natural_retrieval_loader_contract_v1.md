# Natural retrieval loader contract v1

Engineering must ingest only rows with `ingest_status=active` from each
`natural_XXX_retrieval_units_v1.csv`. A row is rejected if its local path is
missing, its SHA-256 differs, `available_at` is null, or its ID duplicates an
already ingested unit. Rows marked `blocked_historical_snapshot_required`,
`superseded`, or any unrecognized status must not be indexed.

Run from repository root:

```bash
python3 tools/validate_natural_retrieval_corpus.py > 数据线/natural_retrieval_validation_report_v1.json
```

The validator resolves immutable retrieval units and timing metadata only. It
does not rank sources, select top-k, assign sentiment, or expose outcome fields.
Candidate-source count remains the 8–20 protocol measure; a single source may
expand into multiple chronological units only when an official update history
explicitly contains separate timestamped versions (as for natural_001 Google
status updates).

## Deterministic loader

`tools/natural_retrieval.py` extracts visible body text from HTML/XML, uses
PyMuPDF for PDF text, splits long sources into stable chunks, and applies two
anti-duplication caps:

- at most three chronological retrieval units per parent document before
  ranking (the latest units available at the requested `as_of` time);
- at most two ranked chunks per parent document.

This prevents a status page with many updates or a long filing with many chunks
from occupying the complete top-k. The internal loader retains `available_at`
for temporal auditing. `predictor_view()` removes timestamps, URLs, and all
evaluator-only outcome metadata before model prompting.

Smoke-test one event without making any model calls:

```bash
python3 tools/natural_retrieval.py \
  --event natural_002 \
  --as-of 2024-05-23T16:00:00-04:00 \
  --top-k 8
```
