# Experiment A: Leakage Injection

## Research Question

RQ1: Do financial Agentic RAG systems retrieve and use future evidence when forecasting?

## Design

### Data Construction

20–50 earnings-event cases, each with:
- `company`: anonymized (Company A, Company B...)
- `prediction_date`: Day T
- `clean_evidence`: news/articles published before or at T
- `leaked_evidence`: news/articles published at T+1 with strong directional signal

### Three Groups

| Group | Input | Purpose |
|---|---|---|
| Clean | Only pre-T evidence | Baseline |
| Leaky | Pre-T + leaked evidence (T+1) | Measure leakage impact |
| Audited | Full set → FinLeakAudit removes leaked → re-predict | Measure audit effectiveness |

### Anonymization

```
NVIDIA → Company A
TSMC → Supplier B
AI GPU → Product X
2024-05-10 → Day T
2024-05-11 → Day T+1
```

## Metrics

- Future Evidence Adoption Rate: % of cases where leaked evidence enters prediction rationale
- Rationale Leakage Rate: % of prediction claims supported by leaked evidence
- Prediction Flip Rate: % of cases where leaked evidence changes prediction direction
- Confidence Delta: mean confidence change with/without leaked evidence
- Revision Recovery Rate: % of cases where FinLeakAudit correctly identifies and removes leaked evidence

## Expected Results

Hypothesis: Agentic RAG systems will frequently retrieve and use future evidence, leading to inflated confidence and occasional prediction flips.
