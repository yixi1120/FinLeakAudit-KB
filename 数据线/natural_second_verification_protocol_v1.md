# Natural corpus second-verifier handoff v1

The engineering pass has checked schema, hashes, timeline ordering, source
coverage, deterministic extraction, and retrieval behavior. It is not a second
human source verification.

Generate or refresh the independent batch with:

```bash
python3 tools/prepare_natural_second_verification.py
```

The batch includes every document currently labeled post-cutoff, every document
with an unresolved availability timestamp, and a deterministic sample of at
least 20% of each event's pre-cutoff documents. The second verifier must open
the source and timestamp-evidence URLs, compare the archived bytes, and fill all
blank review fields without consulting the first verifier's judgment.

Allowed `decision` values are `accept`, `reject`, and `needs_adjudication`.
Until all rows are filled by a different human, the corpus must be described as
engineering-validated and pending independent source verification.
