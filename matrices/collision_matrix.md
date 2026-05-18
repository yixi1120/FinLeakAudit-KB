# Collision Matrix — FinLeakAudit vs Competitors

> 最后更新：2026-05-17

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
| FinAgent-RAG | ✗ (QA) | ✓ | partial (hard negatives) | ✗ | ✗ (self-verify for QA) | Medium |
| Multi-HyDE | ✗ (QA) | ✓ | ✗ | ✗ | ✗ | Medium |
| SHARP | ✓ (trading) | ✗ | ✗ | ✓ (policy audit) | ✓ (policy edits) | Medium |
| VERAFI | ✗ (QA/Compliance) | ✓ | ✗ | ✗ (compliance check) | ✗ | High |
| FinVet | ✗ (misinformation) | ✓ | ✗ | ✓ (fact-checking) | ✗ | Medium |
| SkillGuard-Robust | ✗ (security) | ✗ | ✗ | ✓ (skill security) | ✗ | Medium |
| FinCARDS | ✗ (QA) | ✗ | ✗ | ✗ (reranking) | ✗ | Low |
| Multi-Dim Behavioral | ✓ | ✓ | ✗ | ✗ (behavior) | ✗ | Low |
| ATSF | ✓ (position paper) | ✓ | ✗ | ✗ | ✓ (reflection) | Low |
| Bayesian RAG | ✗ (QA) | ✗ | ✗ | ✗ (faithfulness) | ✗ | Low |

## Key Insights

1. **No single competitor does evidence-level temporal leakage audit + ablation + revision** — this is our unique space.
2. **CARAG** is the strongest host system candidate — it does Agentic RAG + financial forecasting.
3. **Profit Mirage** is the strongest problem-definition reference — it established leakage as a problem.
4. **FLAIRR-TS** is the closest to our revision mechanism but is accuracy-driven not leakage-driven.
5. **SHARP** shows auditable financial agents are trending — window of opportunity is finite.

## Citation Map

| Paper | Must Cite? | Where to Cite |
|---|---|---|
| CARAG | Yes | Main baseline + Related Work |
| Profit Mirage | Yes | Problem motivation + Related Work |
| FLAIRR-TS | Yes | Related Work (distinguish revision types) |
| TRACE | Yes | KG-based baseline |
| SHARP | Yes | Related Work (auditable agents trend) |
| VERAFI | Yes | Related Work (verification background) |
| FinAgent-RAG | Yes | Related Work (self-verification, temporal hard negatives) |
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
