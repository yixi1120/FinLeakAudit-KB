# Experiment B: Natural Leakage Detection

## Research Question

Do real RAG systems naturally produce evidence leakage or unsupported rationales without deliberate injection?

## Design

- Run Agentic RAG on 20-50 real prediction cases first, with a path toward 100 cases and normal retrieval
- Manually or semi-automatically annotate cases for:
  - Future evidence (publish_time > prediction_date)
  - Actual availability (timezone, market-open, reporting lag)
  - Ambiguous timestamp (revised articles, data vendor quirks)
  - Unsupported rationale (claims without retrieved evidence)
  - Semantic leakage (future evidence paraphrased without its evidence ID)
  - Revised article contamination

## Metrics

- Natural Leakage Rate
- Evidence-level detection precision/recall
- Ambiguous Timestamp Rate
- Unsupported Rationale Rate
- Semantic Leakage Rate
- False-positive removal rate
- Inter-annotator Agreement (for manual annotation)

## Challenge

This experiment is harder than Experiment A because natural leakage is rarer and harder to detect. It is the main ecological-validity test and the decisive experiment before making claims about real financial Agentic RAG systems.
