# Research Positioning and Publishability Review - 2026-07-12

## Executive Judgment

FinLeakAudit is still a publishable direction, but the current 5-case pilot is not sufficient evidence for a main-track paper. The project should not pivot to another prediction model. It should narrow its claim and mature into a point-in-time benchmark plus an evidence-level audit protocol for financial Agentic RAG.

The core claim should be:

> FinLeakAudit measures not only whether future information is present, but whether a particular retrieved item is unavailable at decision time, cited for a forecast claim, influential to the forecast, and removable through an auditable revision step.

This is a reliability and evaluation contribution, not a new stock prediction architecture.

## Literature Positioning Snapshot

This review is based on representative papers checked online on 2026-07-12.

| Work | What it establishes | Boundary relevant to FinLeakAudit |
|---|---|---|
| [CARAG](https://aclanthology.org/2026.eacl-long.141/) | Agentic RAG for post-earnings price-shock prediction with a financial temporal knowledge graph | Prediction quality and system design; do not claim first Agentic RAG for financial forecasting |
| [Profit Mirage](https://arxiv.org/abs/2510.07920) | Information leakage in LLM-based financial agents, FinLake-Bench, and counterfactual mitigation | Strong prior art for agent-level and model-knowledge leakage; do not claim first financial-agent leakage study |
| [Look-Ahead-Bench](https://arxiv.org/abs/2601.13770) | Standardized look-ahead-bias evaluation for point-in-time financial LLMs | Benchmark-level temporal bias evaluation; not the same as claim-level evidence attribution and revision |
| [Leakage-Aware Benchmarking](https://arxiv.org/abs/2606.22719) | Decision-time constrained retrieval-augmented LLM forecasting for equity factor ranking | Real-time information-set control and system ablations; not a five-operator evidence audit |
| [OpenFinGym](https://arxiv.org/abs/2606.26350) | Verifiable multi-task quant-agent environment with runtime leakage prevention | Evaluation infrastructure and verifier isolation; broader than the retrieved-evidence audit target |
| [LLM Forecasters Faithfulness](https://arxiv.org/abs/2607.08046) | Forecast faithfulness testing with evidence ablation and diversionary injection | Evidence ablation is not novel by itself; our novelty candidate must be the financial point-in-time integration and revision protocol |

The literature is therefore crowded around financial Agentic RAG, model-level leakage, point-in-time evaluation, and generic evidence faithfulness. In the representative works checked here, we did not find one that integrates all of the following in a financial Agentic RAG workflow: item-level availability, claim-evidence attribution, support/contradiction, marginal forecast sensitivity, and leakage-driven revision. This is a positioning observation, not a first-work claim.

## What the Current Pilot Proves

The current Experiment A pilot is a premise check:

- 5 synthetic cases across three model backends;
- all backends cited the injected future evidence;
- DeepSeek and Qwen flipped in 5/5 cases, while Zhipu flipped in 4/5;
- the first ablation follow-up found the future item `e4` was a flip driver in 5/5 DeepSeek cases and 4/5 Zhipu cases;
- audited predictions recovered the clean direction in the pilot.

These results show that the pipeline runs and that leakage presence, rationale contamination, and forecast influence can be measured separately. They do not yet establish natural leakage frequency or general performance.

## Main Reviewer Vulnerabilities

1. The sample is too small and synthetic.
2. The `T+1` label and evidence IDs make the pilot easier than a natural retrieval setting.
3. Citation detection can miss semantic paraphrases that omit the evidence ID.
4. A leave-one-out change is a marginal sensitivity measure, not a causal claim.
5. Revision can look trivial if the auditor is given perfect future-evidence labels.
6. A simple policy that deletes every future item may be a strong baseline.

## Required Upgrade Before Paper Submission

### Data

- Expand from 5 pilot cases to at least 20-50 cases, with a path toward 100 real cases.
- Use real publication, availability, market-open, revision, and timezone metadata.
- Include both controlled injection and natural retrieval leakage.
- Add multiple future items, distractors, contradictory evidence, and semantic paraphrases.
- Split by time and company so that the evaluation does not reuse events across partitions.

### Annotation

Create a manually checked subset with labels for:

- point-in-time availability;
- claim-evidence attribution;
- support versus contradiction;
- explicit citation versus semantic leakage;
- whether an auditor's removal decision is justified.

### Baselines and Metrics

Compare no audit, timestamp-only filtering, citation-only audit, leave-one-out ablation, full FinLeakAudit, and delete-all-future-evidence. Report detection precision/recall, false-positive rate, flip-driver precision, confidence calibration, revision recovery, human agreement, and compute cost.

## Writing Decision

Keep the project direction, but replace broad novelty language with the following framing:

> We introduce an evidence-level, point-in-time audit protocol for financial Agentic RAG. The protocol links temporal validity to claim attribution and forecast sensitivity, then evaluates whether removing invalid evidence produces an auditable revision.

Do not use:

- first Agentic RAG for stock prediction;
- first leakage study in financial agents;
- evidence ablation as a standalone new method;
- causal prediction or causal effect claims.

## Next Research Milestone

The next decisive milestone is Experiment B: a natural-leakage audit on real timestamped retrieval outputs. A larger model comparison is secondary. If natural cases are unavailable, the paper should be framed explicitly as a controlled benchmark and not as evidence that production RAG frequently leaks.
