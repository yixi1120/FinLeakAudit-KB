# AI4F 2026 OpenReview Submission Metadata

Prepared on 2026-10-02 and updated on 2026-10-03 for the four-author manuscript.
The scientific results remain grounded in the snapshot tagged
`ai4f-2026-submission-v1`; a new submission tag will be created after the fourth-author
metadata and assigned deliverables are verified. This file is a transcription aid for
the submission form; it does not replace the PDF or manifest.

## Venue

- Venue: ACM ICAIF 2026 Workshop AI4F
- OpenReview group: https://openreview.net/group?id=ACM.org/ICAIF/2026/Workshop/AI4F
- Submission deadline: 2026-10-08 11:59 UTC / 2026-10-08 19:59 HKT
- Review model: single-blind
- OpenReview submission license: CC BY 4.0

## Title

FinLeakAudit: Evidence-Level Point-in-Time Auditing for Financial Agentic RAG

## Authors

Use this exact order. Do not submit until each author has confirmed the profile or
email used in OpenReview.

1. Ziyang Lu — The Hong Kong University of Science and Technology —
   `zluca@connect.ust.hk` — corresponding author
2. Junwei Chen — Johns Hopkins University — OpenReview profile/email: **confirm**
3. Yating Zhang — South China Normal University — OpenReview profile/email:
   **confirm**
4. Minzhen Lai — Imperial College London — OpenReview profile/email: **confirm**

## Keywords

Paste as a comma-separated list:

`financial Agentic RAG, temporal evidence leakage, point-in-time auditing, claim-evidence attribution, forecast revision, trustworthy financial AI`

## TL;DR

FinLeakAudit audits whether financial Agentic RAG forecasts depend on evidence
unavailable at a historical cutoff, measures forecast sensitivity, and revises
predictions after removing detected leakage.

## Abstract

Financial forecasting systems built on retrieval-augmented large language models
can silently consume evidence that was unavailable at a historical prediction
cutoff. This can produce plausible rationales and inflated backtests without
preserving the information set available to a real decision maker. We present
FinLeakAudit, an evidence-level audit protocol separating point-in-time
availability, citation validity, claim-evidence attribution, marginal forecast
sensitivity, and leakage-driven revision. In a controlled 10-case study across
three LLMs, post-cutoff evidence was cited in 28/30 model-case runs and changed
12/30 forecast categories; removing it restored the corresponding cutoff-safe
category in 12/12 changed runs. A 10-event primary-source replay produced 13
changes in 30 model-event runs. Sparse deletion recovered 11/13, while
rank-preserving cutoff-safe backfill recovered 13/13 and matched the Clean direction
in 30/30 runs. However, 24/30 backfilled inputs were identical to Clean and the
exact paired McNemar test was not significant ($p=0.25$). On 78 decisive
human-labeled claim-evidence pairs, citation-only attribution achieved F1 0.941 and
a blinded LLM judge achieved F1 0.937. The results establish a reproducible audit
pilot and expose concrete failure modes; they do not estimate real-world leakage
prevalence or demonstrate improved forecasting accuracy.

## PDF

- File: `output/pdf/FinLeakAudit_workshop_draft_v2.pdf`
- Pages: 6
- Size: 348166 bytes
- SHA-256: `b7147c065889da58cb648d6028b9f86421367394d20e62c221be5ddca81e9d42`
- Reproducibility tag:
  https://github.com/yixi1120/FinLeakAudit-KB/tree/ai4f-2026-submission-v1

## Human Decisions Required Before Submission

- [ ] Junwei Chen confirms his exact OpenReview profile or submission email.
- [ ] Yating Zhang confirms her exact OpenReview profile or submission email.
- [ ] Minzhen Lai confirms his exact email and OpenReview profile.
- [ ] Minzhen Lai completes the assigned external reproduction, model-stratified
  analysis, manuscript-to-artifact audit, and corresponding revision work.
- [ ] All authors confirm spelling, affiliation, order, and the contribution statement.
- [ ] One author explicitly agrees to serve as the required reviewer.
- [ ] One author confirms that they can present in person in Milan if accepted.
- [ ] All authors understand that the OpenReview submission uses CC BY 4.0.

## Final Form Check

- [ ] Title matches this file and the PDF.
- [ ] All four author profiles resolve to the intended people.
- [ ] Keywords are entered as separate comma-delimited items.
- [ ] Abstract matches the four-author v2 PDF.
- [ ] The six-page PDF uploads and previews correctly.
- [ ] The submission confirmation page shows all four authors in the frozen order.
- [ ] Record the OpenReview forum/submission ID below.
- [ ] Download or re-open the uploaded PDF and verify its SHA-256 if OpenReview
  provides a downloadable copy.

OpenReview submission ID: **pending**
