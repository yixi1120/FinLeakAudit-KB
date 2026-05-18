# Profit Mirage vs FinLeakAudit

## Summary

Profit Mirage studies **agent-level** leakage (model memorization). FinLeakAudit studies **evidence-level** leakage (RAG retrieval).

## Side-by-Side

| | Profit Mirage | FinLeakAudit |
|---|---|---|
| Leakage source | LLM pretraining memorization | RAG-retrieved future evidence |
| Level of analysis | Agent / system level | Individual evidence level |
| Detection method | Counterfactual evaluation, memorization audits | Temporal availability + attribution + ablation |
| Correction | FactFin (external framework) | Forecast Revision Operator |
| Benchmark | FinLake-Bench | Custom injection + natural audit |

## Citation Strategy

In Related Work: "Profit Mirage establishes that LLM-based financial agents suffer from information leakage. We extend this insight to the evidence level: rather than studying memorization-driven leakage, we study whether specific retrieved evidence items are temporally invalid and how they affect individual predictions."
