---
title: "The New Quant: A Survey of Large Language Models in Financial Prediction and Trading"
year: 2025
venue: arXiv
ccf_level: preprint
arxiv: "2510.05533"
tags: [survey, financial-prediction, trading, agentic-rag, temporal-leakage, faithfulness]
status: deep-read
collision_risk: low
must_cite: true
---

# 一句话总结

50+ 论文综述，覆盖 LLM 金融预测六大方向。明确提出 temporal leakage 和 faithfulness 是关键挑战。

# 关键引用价值

- Section 5: RAG 在金融预测中的应用
- Section 7.1: "Temporal leakage and time machine effects" — 直接陈述 LLM 预训练记忆导致泄漏
- Section 7.2: 呼吁 time-safe evaluation、cost/latency/capacity 的综合评估
- 提出 "auditable pipelines" 和 "retrieval-first prompting"

# 和 FinLeakAudit 的关系

- 这篇综述为 FinLeakAudit 提供了问题背景和需求论证
- 综述说明 "evidence-level leakage audit" 是一个未被填补的空白

# 可以引用的位置

- Introduction: 引出 temporal leakage 问题
- Related Work: 综述引述
- Experiments: 评估协议参考
