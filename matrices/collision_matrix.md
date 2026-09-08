# Collision Matrix — FinLeakAudit vs Competitors

> 最后更新：2026-09-08

## Master Comparison Table

| Paper | Stock Forecasting | Agentic RAG | Temporal Leakage | Evidence Audit | Forecast Revision | Collision Risk |
|---|---|---|---|---|---|---|---|
| **FinLeakAudit (Ours)** | ✓ | ✓ | ✓ (evidence-level) | ✓ | ✓ (leakage-driven) | — |
| CARAG | ✓ | ✓ | partial (eval only) | partial | ✗ | Critical |
| Profit Mirage | ✓ | partial | ✓ (agent-level) | ✗ | ✗ | Critical |
| MarketSenseAI 2.0 | ✓ | ✓ | ✗ | ✗ | ✗ | High |
| SEP (WWW 2024) | ✓ | ✗ | ✗ | ✗ | ✗ | Medium |
| TRACE | ✓ | ✗ | ✓ (KG-based) | partial | ✗ | High |
| FLAIRR-TS | partial | ✓ | ✗ | ✗ | ✓ (accuracy-driven) | Medium |
| FinAgent-RAG (withdrawn) | ✗ (QA) | ✓ | partial (hard negatives) | ✗ | ✗ (self-verify for QA) | Excluded |
| Multi-HyDE | ✗ (QA) | ✓ | ✗ | ✗ | ✗ | Medium |
| SHARP | ✓ (trading) | ✗ | ✗ | ✓ (policy audit) | ✓ (policy edits) | Medium |
| VERAFI | ✗ (QA/Compliance) | ✓ | ✗ | ✗ (compliance check) | ✗ | High |
| FinVet | ✗ (misinformation) | ✓ | ✗ | ✓ (fact-checking) | ✗ | Medium |
| SkillGuard-Robust | ✗ (security) | ✗ | ✗ | ✓ (skill security) | ✗ | Medium |
| FinCARDS | ✗ (QA) | ✗ | ✗ | ✗ (reranking) | ✗ | Low |
| Multi-Dim Behavioral | ✓ | ✓ | ✗ | ✗ (behavior) | ✗ | Low |
| ATSF | ✓ (position paper) | ✓ | ✗ | ✗ | ✓ (reflection) | Low |
| Bayesian RAG | ✗ (QA) | ✗ | ✗ | ✗ (faithfulness) | ✗ | Low |
| Look-Ahead-Bench | ✓ (financial workflows) | partial | ✓ (point-in-time) | ✗ | ✗ | High |
| Leakage-Aware Benchmarking | ✓ (factor ranking) | ✓ | ✓ (decision-time) | ✗ | ✗ | High |
| OpenFinGym | partial (quant tasks) | partial | ✓ (runtime leakage prevention) | ✓ (verification interface) | ✗ | Medium |
| LLM Forecasters Faithfulness | partial (forecasting) | ✗ | ✗ | ✓ (ablation/faithfulness) | ✗ | Medium |

## Key Insights

1. No representative work checked in the 2026-07-12 review combines item-level availability, claim attribution, support/contradiction, marginal sensitivity, and revision in one financial Agentic RAG audit workflow. This is a positioning hypothesis, not a first-work claim.
2. **CARAG** is the strongest host system candidate — it does Agentic RAG + financial forecasting.
3. **Profit Mirage** is the strongest problem-definition reference — it established leakage as a problem.
4. **Look-Ahead-Bench** and **Leakage-Aware Benchmarking** occupy system-level point-in-time evaluation and must be distinguished explicitly.
5. **Evidence ablation** is now a shared evaluation technique, so the novelty candidate is the financial evidence-level integration and revision protocol.
6. **SHARP** shows auditable financial agents are trending — window of opportunity is finite.

## Citation Map

| Paper | Must Cite? | Where to Cite |
|---|---|---|
| CARAG | Yes | Main baseline + Related Work |
| Profit Mirage | Yes | Problem motivation + Related Work |
| FLAIRR-TS | Yes | Related Work (distinguish revision types) |
| TRACE | Yes | KG-based baseline |
| SHARP | Yes | Related Work (auditable agents trend) |
| VERAFI | Yes | Related Work (verification background) |
| FinAgent-RAG | No | Withdrawn for methodological errors; do not use as supporting evidence |
| FinVet | Optional | Fact-checking related work |
| FinCARDS | Optional | Evidence card reference |
| ATSF | Optional | Paradigm background |
| MarketSenseAI 2.0 | Yes | Multi-agent stock analysis baseline |
| SEP (WWW 2024) | Yes | CCF A explainable stock prediction |
| Multi-HyDE | Yes | Agentic RAG for finance |
| SkillGuard-Robust | Optional | Skill auditing background (distinguish) |
| SkillProbe | Optional | Same as above |
| Semia | Optional | Same as above |
| Multi-Dim Behavioral | Optional | Agent evaluation background |
| The New Quant | Yes | Survey reference for motivation |
| Bayesian RAG | Optional | Faithfulness evaluation reference |
