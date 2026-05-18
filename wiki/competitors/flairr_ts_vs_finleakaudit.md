# FLAIRR-TS vs FinLeakAudit

## Summary

Both have revision loops. FLAIRR-TS revises for accuracy. FinLeakAudit revises for leakage.

## Side-by-Side

| | FLAIRR-TS | FinLeakAudit |
|---|---|---|
| Revision trigger | Prediction accuracy (value wrong) | Evidence temporal leakage |
| Revision method | Self-verification → adjust | Remove leaked evidence → re-predict |
| Domain | General time series | Financial forecasting |
| Does it check evidence time? | No | Yes (core feature) |
| Does it ablate evidence? | No | Yes |
| Output | Revised prediction value | Revised prediction + leakage report |

## Citation Strategy

"FLAIRR-TS demonstrates that iterative refinement can improve LLM-agent forecasts. Our work introduces a different revision paradigm: leakage-driven revision, where forecasts are revised not because they are inaccurate, but because they rely on evidence that was unavailable at prediction time."
