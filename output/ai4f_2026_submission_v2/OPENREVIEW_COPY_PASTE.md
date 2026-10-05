# OpenReview Copy-Paste Fields

## Title

FinLeakAudit: Evidence-Level Point-in-Time Auditing for Financial Agentic RAG

## Authors

Use this exact order:

1. Ziyang Lu - The Hong Kong University of Science and Technology -
   `zluca@connect.ust.hk` - corresponding author
2. Junwei Chen - Johns Hopkins University - OpenReview profile/email: **confirm**
3. Yating Zhang - South China Normal University - OpenReview profile/email: **confirm**

Candidate contact emails visible in Git commit metadata, to be confirmed rather than
entered blindly:

- Junwei Chen: `cjw29715603655@gmail.com`
- Yating Zhang: `yatingzhang930@gmail.com`

## Keywords

financial Agentic RAG, temporal evidence leakage, point-in-time auditing, claim-evidence attribution, forecast revision, trustworthy financial AI

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

## Optional AI-assistance disclosure

Use only if the submission form or organizer asks for it:

> Generative AI tools were used for language editing and code assistance. The authors
> reviewed and verified the experimental design, implementation, data, citations,
> numerical results, and final manuscript, and take responsibility for the submission.

## Upload file

`FinLeakAudit_AI4F_2026.pdf`

## License

CC BY 4.0, as shown by the AI4F OpenReview submission invitation.
