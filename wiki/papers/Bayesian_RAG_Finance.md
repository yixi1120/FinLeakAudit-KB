---
title: "Bayesian RAG: Uncertainty-Aware Retrieval for Reliable Financial Question Answering"
year: 2025
venue: Frontiers / PMC
ccf_level: journal
arxiv: "PMC 12886353"
tags: [bayesian-rag, uncertainty-aware, financial-qa, faithfulness, hallucination, evidence-support]
status: skimmed
collision_risk: low
must_cite: false
---

# 一句话总结

将 Bayesian uncertainty 引入金融 RAG QA，报告 faithfulness 0.87、hallucination rate 0.13、evidence support rate 指标。

# 研究任务

金融 QA 的可靠性提升

# 方法

- Bayesian uncertainty-aware retrieval
- 评测 faithfulness, hallucination rate, evidence support rate, claim coverage

# 指标

- Faithfulness: 0.87 (+6.1% over ColBERT)
- Hallucination: 0.13 (-27.8%)
- Evidence support rate

# 和 FinLeakAudit 的关系

- 适合借鉴 evaluation protocol
- 不做 temporal leakage，不做 forecasting，不做 ablation

# 撞车风险

Low

# 可以引用的位置

- Experiments: faithfulness/hallucination/evidence support 指标参考
