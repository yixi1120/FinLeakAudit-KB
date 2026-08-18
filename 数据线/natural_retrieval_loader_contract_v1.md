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
