# AI4F 2026 OpenReview Submission Metadata

Prepared on 2026-10-02 from the frozen manuscript tagged
`ai4f-2026-submission-v1`. This file is a transcription aid for the submission
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

- File: `output/pdf/FinLeakAudit_workshop_draft_v1.pdf`
- Pages: 6
- Size: 346560 bytes
- SHA-256: `dcaa4a4236987c23049baee663878596ae54a55324bbcbff22f1d33b1a3ff9a1`
- Reproducibility tag:
  https://github.com/yixi1120/FinLeakAudit-KB/tree/ai4f-2026-submission-v1

## Human Decisions Required Before Submission

- [ ] Junwei Chen confirms his exact OpenReview profile or submission email.
- [ ] Yating Zhang confirms her exact OpenReview profile or submission email.
- [ ] All authors confirm spelling, affiliation, order, and the contribution statement.
- [ ] One author explicitly agrees to serve as the required reviewer.
- [ ] One author confirms that they can present in person in Milan if accepted.
- [ ] All authors understand that the OpenReview submission uses CC BY 4.0.

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

