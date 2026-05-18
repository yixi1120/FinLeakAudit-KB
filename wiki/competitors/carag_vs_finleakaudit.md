# CARAG vs FinLeakAudit

## Summary

CARAG is a prediction system. FinLeakAudit is an audit layer.

## Side-by-Side

| | CARAG | FinLeakAudit |
|---|---|---|
| Goal | Predict post-earnings price shocks | Audit evidence leakage in forecasting |
| Core method | CTKG + multi-agent reasoning | 5 verification operators |
| Primary output | Stock movement prediction (UP/DOWN) | Leakage report + revised prediction |
| Novelty axis | Better prediction accuracy | Better prediction reliability |
| Evidence source | KG-structured facts | RAG-retrieved documents |
| Leakage handling | Post-cutoff eval (system-level) | Evidence-level audit + ablation |

## Relationship

FinLeakAudit could use CARAG as a **host system** — applying the audit layer on top of CARAG's predictions.

## Citation Strategy

In Related Work: "CARAG represents the state-of-the-art in Agentic RAG for financial prediction. However, CARAG focuses on prediction accuracy, while our work focuses on prediction reliability through evidence-level leakage auditing."
