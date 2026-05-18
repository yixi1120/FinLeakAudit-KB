---
title: "FinCARDS: Card-Based Analyst Reranking for Financial Document Question Answering"
year: 2026
venue: ICAIF 2025 / arXiv
ccf_level: preprint
arxiv: "2601.06992"
tags: [evidence-cards, financial-qa, structured-evidence, card-abstraction, reranking]
status: skimmed
collision_risk: low
must_cite: false
---

# 一句话总结

把金融文档 chunk 编译成带 entities/metrics/periods 的 cards，用于 QA 场景 reranking。与我们的 evidence card 概念有交集但不撞。

# 研究任务

金融文档 QA 中的检索重排

# 方法

- Card abstraction：每个 chunk → structured card（entities, metrics, periods, numeric spans）
- Deterministic field-level matching
- Multi-stage retrieval + reranking

# 和 FinLeakAudit 的区别

- FinCARDS 的 card 用于检索优化
- FinLeakAudit 的 evidence 条目用于时间泄漏审计
- FinCARDS 关注 QA correctness，不关注预测泄漏

# 撞车风险

Low — card 概念重叠但目的不同

# 引用建议

如果论文中使用 "evidence card" 概念，应引用 FinCARDS 并区分
