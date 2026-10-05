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

# Submission deadline

The AI4F venue-specific page and live OpenReview submission invitation agree on the
submission deadline:

| Source | Submission deadline | Notification |
|---|---|---|
| AI4F venue-specific page | 2026-10-07 AoE | 2026-10-14 AoE |
| OpenReview submission invitation | 2026-10-08 11:59 UTC | Not specified in form |

These are the same closing instant: **2026-10-08 19:59 HKT**. The OpenReview
invitation remains the operational source of truth for form availability. The ICAIF
general workshop page previously displayed an earlier generic workshop date, but it
does not override the workshop-specific page and live submission form.

The team should still upload before the final day so author-profile problems can be
fixed without deadline pressure.

# Confirmed submission rules

- PDF submission through OpenReview.
- Single-blind review: author names and affiliations remain visible.
- No strict page limit or mandatory template; ACM formatting is recommended.
- Non-archival workshop with no official proceedings.
- At least one author must agree to serve as a reviewer and deliver reviews on time.
- The author list should be treated as frozen at initial submission.
- The live OpenReview form requires title, authors/author profiles, keywords,
  abstract, and PDF; TL;DR is optional.
- The live submission invitation assigns the submitted note a CC BY 4.0 license.
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
The repository includes a machine-checkable frozen-input and corpus manifest, and all
104 tests pass. The v2 compiled submission PDF SHA-256 is
`b05485451a37193738e161ce061a3adce29f0d0803d5c45e5aa10e5b2c65aad1`.

On 2026-10-05, the revised consolidated upload package was prepared under
`output/ai4f_2026_submission_v2/`. It contains the verified PDF, exact OpenReview
copy-paste fields, checksums, collaborator confirmation messages, and the final
submission checklist. The PDF was rendered and visually inspected again after the
three-author rollback and P0 manuscript revision; all 104 tests pass.

The team emailed `contact@ai4f.org` to request a written ruling on live remote
presentation and review feedback if no author can travel to Milan. Jacob Chanyeol Choi
replied on 2026-10-04 that in-person presentation is mandatory for all accepted papers.
The reply did not address whether review feedback remains available if the team later
cannot attend. This does not change the paper or the initial submission deadline, but
an attending author is required to retain an accepted paper in the workshop program.

# Submission-critical checklist

## P0: initial upload

- [x] Resolve the deadline against the live OpenReview invitation: 2026-10-08 19:59
  HKT.
- [x] Prepare the exact OpenReview fields in
  `paper/openreview_submission_ai4f_2026.md`.
- [ ] Confirm all three authors' OpenReview profiles, names, affiliations, and email
  addresses.
- [ ] Freeze the three-author list and author order before initial submission.
- [ ] Designate the required reviewer volunteer.
- [ ] Designate an in-person presenter for Milan if accepted.
- [ ] Create the AI4F OpenReview submission shell.
- [ ] Upload the current complete PDF before 2026-10-08 19:59 HKT.
- [ ] Save the OpenReview submission ID and uploaded-PDF checksum in this page.

## P1: final revision before the confirmed close

- [x] Keep Backfill as a diagnostic baseline and retain the `p=0.25` negative result.
- [x] Add the public versioned repository URL and verify anonymous access
  is not required under the single-blind policy.
- [x] Run all 104 tests and rebuild the PDF from the frozen analysis inputs.
- [x] Re-render every final page and repeat the visual inspection.
- [ ] Verify title, abstract, keywords, conflicts, author order, reviewer commitment,
  and any AI-assistance disclosure requested by the OpenReview form.

## P2: after submission

- [x] Prepare the `ai4f-2026-submission-v2` reproducibility snapshot and tagged release.
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
