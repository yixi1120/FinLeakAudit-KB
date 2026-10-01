---
title: AI4F 2026 submission plan
date: 2026-10-01
status: active
target: ACM ICAIF 2026 Workshop AI4F
---

# Venue fit

FinLeakAudit is a strong topical match for AI4F 2026. The venue explicitly solicits
work on agentic financial workflows, evaluation and verification, retrieval-augmented
systems, governance and auditability, and reproducible benchmarks. FinLeakAudit should
be positioned primarily as a reliability and auditability study for financial Agentic
RAG, not as a stock-prediction system.

Evidence source:

- AI4F official call: https://ai4f.org/
- Direct submission venue: https://openreview.net/group?id=ACM.org/ICAIF/2026/Workshop/AI4F

# Date conflict and operating deadline

Two official pages currently disagree:

| Source | Submission deadline | Notification |
|---|---|---|
| AI4F venue-specific page | 2026-10-07 AoE | 2026-10-14 AoE |
| ICAIF general workshop page | 2026-10-01 23:59 AoE | 2026-10-15 23:59 AoE |

Source for the general page: https://icaif2026.org/workshop.html

The venue-specific AI4F page and its direct OpenReview link are the more specific
sources, but the team must not rely on that inference alone. The internal safe deadline
is therefore **2026-10-01 AoE for creating and uploading an initial complete
submission**, while `contact@ai4f.org` is asked to confirm whether revisions remain
open until 2026-10-07 AoE.

# Confirmed submission rules

- PDF submission through OpenReview.
- Single-blind review: author names and affiliations remain visible.
- No strict page limit or mandatory template; ACM formatting is recommended.
- Non-archival workshop with no official proceedings.
- At least one author must agree to serve as a reviewer and deliver reviews on time.
- The author list should be treated as frozen at initial submission.
- Accepted papers are invited to an in-person poster session in Milan on 2026-11-14;
  selected papers may receive a short oral slot.

# Frozen author metadata

1. Ziyang Lu, The Hong Kong University of Science and Technology, first and
   corresponding author.
2. Junwei Chen, Johns Hopkins University, second author.
3. Yating Zhang, South China Normal University, third author.

Before the initial OpenReview submission, all authors must confirm the spelling of
their names, affiliations, email addresses, OpenReview profiles, author order, and
contribution statement. One author must explicitly volunteer as the required reviewer,
and one author must confirm the ability to present in Milan if accepted.

# Current manuscript readiness

The current `paper/main.pdf` is a readable six-page, two-column, single-blind paper.
All six pages were rendered and visually inspected on 2026-10-01. No clipping,
overlap, broken tables, unresolved citations, or blank pages were found. The paper now
includes a protocol figure, a four-panel result figure, and a three-row failure-mode
table grounded in retained experiment logs.

The Related Work section explicitly separates evidence-level retrieval auditing from
the model-memory and across-period diagnostics in Profit Mirage and Look-Ahead-Bench.
The repository includes a machine-checkable frozen-input manifest, and all 103 tests
pass. The compiled submission PDF SHA-256 is
`dcaa4a4236987c23049baee663878596ae54a55324bbcbff22f1d33b1a3ff9a1`.

# Submission-critical checklist

## P0: initial upload

- [ ] Ask `contact@ai4f.org` to resolve the 2026-10-01 versus 2026-10-07 deadline
  conflict.
- [ ] Confirm all three authors' OpenReview profiles, names, affiliations, and email
  addresses.
- [ ] Freeze the three-author list and author order before initial submission.
- [ ] Designate the required reviewer volunteer.
- [ ] Designate an in-person presenter for Milan if accepted.
- [ ] Create the AI4F OpenReview submission shell.
- [ ] Upload the current complete PDF by the internal 2026-10-01 AoE safety deadline.
- [ ] Save the OpenReview submission ID and uploaded-PDF checksum in this page.

## P1: final revision before the confirmed close

- [x] Keep Backfill as a diagnostic baseline and retain the `p=0.25` negative result.
- [x] Add the public versioned repository URL and verify anonymous access
  is not required under the single-blind policy.
- [x] Run all 103 tests and rebuild the PDF from the frozen analysis inputs.
- [x] Re-render every final page and repeat the visual inspection.
- [ ] Verify title, abstract, keywords, conflicts, author order, reviewer commitment,
  and any AI-assistance disclosure requested by the OpenReview form.

## P2: after submission

- [x] Prepare the `ai4f-2026-submission-v1` reproducibility snapshot and tagged release.
- [ ] Prepare a poster outline and a ten-minute oral outline in case the paper is
  selected.
- [ ] Expand the four incomplete Novel-safe candidate pools only after the submission
  package is secure; this remains the next experiment-line task.

# Go/no-go assessment

The project is ready for an initial AI4F upload now. The main remaining risks are
administrative rather than scientific: conflicting deadlines, author-profile
completion, reviewer commitment, and in-person presentation responsibility. The
current pilot scale and non-significant Backfill comparison must remain explicit, but
they do not prevent submission to this non-archival workshop.
