---
title: FinLeakAudit RA application project brief
date: 2026-07-26
status: application-ready-draft
---

# FinLeakAudit RA Application Project Brief

## 30-Second Pitch

FinLeakAudit is an evidence-level audit layer for financial Agentic RAG. It
tests whether retrieved evidence was actually available at the historical
prediction cutoff, traces which evidence appears in the forecast rationale,
measures each item's marginal influence, and revises the forecast after
detected future evidence is removed. A controlled 10-case, three-model pilot
found explicit future-evidence citations in 28/30 model-case runs and
prediction-category changes in 12/30.

## Project Description for a CV or Application Form

Built a controlled research prototype for auditing point-in-time evidence
leakage in financial Agentic RAG forecasting. The pipeline separates
predictor-visible evidence from auditor and evaluator metadata, validates
timezone-aware evidence availability, traces explicit evidence citations,
performs leave-one-out marginal sensitivity analysis, and reconstructs revised
forecasts from the actual leaky context. Integrated DeepSeek, Zhipu GLM, and a
local Qwen2.5-14B model and executed 210 model calls across 10 controlled cases
with zero runtime errors. Future evidence was explicitly cited in 28/30
model-case runs and changed the prediction category in 12/30. All 12 changed
predictions returned to their Clean category after detected future evidence was
removed, while baseline analysis showed that the current citation-only policy
does not yet outperform timestamp filtering.

## CV Bullet Options

Use two or three bullets, depending on available space:

- Engineered a point-in-time evidence audit pipeline for financial Agentic RAG,
  including timezone-aware availability checks, citation tracing,
  leave-one-out marginal sensitivity, and leakage-driven forecast revision.
- Integrated DeepSeek, Zhipu GLM, and local Qwen2.5-14B; completed 210 model
  calls across 10 controlled cases with reproducible seeds, structured outputs,
  retry/resume support, and zero runtime errors.
- Measured explicit future-evidence citation in 28/30 model-case runs and
  prediction-category changes in 12/30; reported 12/12 conditional revision
  recovery with Wilson 95% CI [75.7%, 100%] rather than claiming universal
  100% effectiveness.
- Built timestamp-only, citation-only, delete-all-future, and leave-one-out
  comparisons; identified citation-free semantic attribution as the main
  unresolved gap.

## Short Email Paragraph

I have been developing FinLeakAudit, a controlled research prototype for
auditing point-in-time evidence leakage in financial Agentic RAG systems. I
implemented the experiment pipeline, three-model integration, evidence
availability checks, attribution-based revision, ablation analysis, and
reproducibility tests. In a 10-case pilot, post-cutoff evidence was explicitly
cited in 28/30 model-case runs and changed the prediction category in 12/30.
The baseline result is deliberately cautious: the current citation-only policy
does not yet outperform timestamp filtering, which motivates my next work on
semantic attribution and natural point-in-time retrieval cases. This project
reflects the kind of trustworthy financial AI research I hope to pursue as an
RA.

## Interview Explanation

### What did the experiment show?

It showed that post-cutoff evidence can contaminate model rationales and alter
forecast categories in a controlled setting. It also showed that removing
detected future evidence can undo those observed category changes.

### What did it not show?

It did not show that FinLeakAudit improves stock prediction accuracy, that
leakage is common in deployed financial RAG systems, or that the current method
is better than perfect timestamp filtering.

### Why is the negative baseline result useful?

It prevents an inflated contribution claim. On data with perfect timestamps,
timestamp filtering is already strong. A richer audit becomes valuable when
availability metadata is uncertain, evidence is revised, or a model absorbs
future content without explicitly citing its source.

### What is the next technical contribution?

Citation-free semantic claim-evidence attribution, followed by
support/contradiction classification and evaluation on natural point-in-time
retrieval outputs.

## Safe Claim

> A controlled pilot for measuring point-in-time evidence availability,
> rationale contamination, marginal forecast sensitivity, and leakage-driven
> revision in financial Agentic RAG.

## Claims to Avoid

- "FinLeakAudit improves stock prediction accuracy."
- "FinLeakAudit is 100% effective."
- "This is the first financial-agent leakage study."
- "Leave-one-out proves a causal effect."
- "The 10 cases constitute a natural or production benchmark."
- "The current citation-only policy is the full FinLeakAudit method."

## Evidence Links

- Repository README: `README.md`
- Main result: `wiki/experiments/three_model_v4_results_2026_07_26.md`
- Baselines: `wiki/experiments/baseline_comparison_v4_2026_07_26.md`
- Compact 30-row output:
  `wiki/experiments/three_model_v4_case_results_2026_07_26.csv`
- Data construction:
  `wiki/experiments/cases_pilot_v4_construction_2026_07_26.md`
- Research positioning:
  `wiki/writing/research_positioning_2026_07_12.md`

## P0 Checklist Before Sending an Application

- [ ] Add the applicant's exact English name and contact details to the CV.
- [ ] Tailor the email paragraph to the professor's current research.
- [ ] Decide repository access: public after a copyright/license audit, or
      private with the professor explicitly invited.
- [ ] Do not send a private GitHub URL to someone who has not been granted
      access.
- [ ] Verify that public history does not expose API keys or private team
      material.
- [ ] Add precise collaborator names and contribution ownership where required.
- [ ] Link the repository and the exact result report from the CV.
- [ ] Keep the project description within the claim boundary above.

## P1 Follow-Up After Initial Applications

- Add semantic-leakage annotation and evaluator precision/recall/F1.
- Expand to at least 20 natural point-in-time cases and more event types.
- Add a second licensed market-price source.
- Freeze immutable model versions and repeat runs where provider
  nondeterminism remains possible.
- Add a repository license and citation metadata after ownership is confirmed.
