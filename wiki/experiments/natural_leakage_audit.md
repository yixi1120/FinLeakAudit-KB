# Experiment B: Natural Leakage Detection

## Research Question

Do real RAG systems naturally produce evidence leakage or unsupported rationales without deliberate injection?

## Design

- Run Agentic RAG on 100 real prediction cases with normal retrieval
- Manually or semi-automatically annotate cases for:
  - Future evidence (publish_time > prediction_date)
  - Ambiguous timestamp (revised articles, data vendor quirks)
  - Unsupported rationale (claims without retrieved evidence)
  - Revised article contamination

## Metrics

- Natural Leakage Rate
- Ambiguous Timestamp Rate
- Unsupported Rationale Rate
- Inter-annotator Agreement (for manual annotation)

## Challenge

This experiment is harder than Experiment A because natural leakage is rarer and harder to detect. It determines the paper's ecological validity ceiling.
