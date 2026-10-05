# AI4F 2026 OpenReview Submission Metadata

Prepared on 2026-10-02 and revised on 2026-10-05 from the manuscript prepared for
tag `ai4f-2026-submission-v2`. The consolidated upload package is under
`output/ai4f_2026_submission_v2/`. This file is a transcription aid for the submission
form; it does not replace the frozen PDF or manifest.

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

Candidate emails from repository commit metadata, pending direct confirmation:

- Junwei Chen: `cjw29715603655@gmail.com`
- Yating Zhang: `yatingzhang930@gmail.com`

## Keywords

Paste as a comma-separated list:

`financial Agentic RAG, temporal evidence leakage, point-in-time auditing, claim-evidence attribution, forecast revision, trustworthy financial AI`

## TL;DR

FinLeakAudit audits whether financial Agentic RAG forecasts depend on evidence
unavailable at a historical cutoff, measures forecast sensitivity, and revises
predictions after removing detected leakage.

## Abstract

Financial forecasting systems built on retrieval-augmented large language models can
silently consume evidence that was unavailable at a historical prediction cutoff. This
can produce plausible rationales and inflated backtests without preserving the
information set available to a real decision maker. We present FinLeakAudit, an
evidence-level audit protocol separating point-in-time availability, citation
validity, claim-evidence attribution, marginal forecast sensitivity, and
leakage-driven revision. In a controlled 10-case study across three LLMs, post-cutoff
evidence was cited in 28/30 model-case runs and changed 12/30 forecast categories;
removing it restored the corresponding cutoff-safe category in 12/12 changed runs. A
10-event primary-source replay produced 13 changes in 30 model-event runs. Sparse
deletion recovered 11/13, while rank-preserving cutoff-safe backfill recovered 13/13
and matched the Clean direction in 30/30 runs. However, 24/30 backfilled inputs were
identical to Clean and the exact paired McNemar test was not significant (p=0.25). On
78 decisive human-labeled claim-evidence pairs, citation-only attribution achieved F1
0.941 and a blinded LLM judge achieved F1 0.937. The results provide a reproducible
audit pilot and expose concrete failure modes; they do not estimate real-world leakage
prevalence or demonstrate improved forecasting accuracy.

## PDF

- Upload file: `output/ai4f_2026_submission_v2/FinLeakAudit_AI4F_2026.pdf`
- Frozen source file: `paper/main.pdf`
- Pages: 6
- Size: 357685 bytes
- SHA-256: `b05485451a37193738e161ce061a3adce29f0d0803d5c45e5aa10e5b2c65aad1`
- Reproducibility tag:
  https://github.com/yixi1120/FinLeakAudit-KB/tree/ai4f-2026-submission-v2

## Human Decisions Required Before Submission

- [ ] Junwei Chen confirms his exact OpenReview profile or submission email.
- [ ] Yating Zhang confirms her exact OpenReview profile or submission email.
- [ ] All authors confirm spelling, affiliation, order, and the contribution statement.
- [ ] One author explicitly agrees to serve as the required reviewer.
- [ ] One author confirms that they can present in person in Milan if accepted.
- [ ] All authors understand that the OpenReview submission uses CC BY 4.0.
- [x] The organizers were emailed on 2026-10-04 to clarify live remote presentation
  and whether review feedback is retained if no author can travel.

## Final Form Check

- [ ] Title matches this file and the PDF.
- [ ] All three author profiles resolve to the intended people.
- [ ] Keywords are entered as separate comma-delimited items.
- [ ] Abstract matches the frozen PDF.
- [ ] The six-page PDF uploads and previews correctly.
- [ ] The submission confirmation page shows all three authors in the frozen order.
- [ ] Record the OpenReview forum/submission ID below.
- [ ] Download or re-open the uploaded PDF and verify its SHA-256 if OpenReview
  provides a downloadable copy.

OpenReview submission ID: **pending**
