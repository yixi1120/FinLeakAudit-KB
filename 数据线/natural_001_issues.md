# natural_001 issues and exceptions

- `natural_001_doc_016`, `018`, `019`, `020`, and `021` expose date-only first-publication information. Exact `original_published_at` and `available_at` remain `null`; no time is inferred.
- `natural_001_doc_018` visibly says it was updated on 2024-07-25 at 19:00 UTC, while the downloaded HTML exposes later `dateModified` metadata of 2024-09-21T19:33:00Z. `revised_at` records the later metadata; the discrepancy requires second-verifier review.
- All `vendor_indexed_at` values are `null` because no third-party vendor copy was used.
- Engineering must use each `archive_path` raw snapshot as retrieval text. `text` is only a source-grounded audit excerpt and must not become a replacement retrieval corpus.
