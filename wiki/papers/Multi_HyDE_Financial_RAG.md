---
title: "Enhancing Financial RAG with Agentic AI and Multi-HyDE: A Novel Approach to Knowledge Retrieval and Hallucination Reduction"
year: 2025
venue: FinNLP 2025 Workshop
ccf_level: workshop
arxiv: "2509.16369"
tags: [financial-rag, agentic-ai, multi-hyde, hallucination-reduction, multi-perspective-retrieval]
status: skimmed
collision_risk: medium
must_cite: true
---

# 一句话总结

Multi-HyDE 生成多个假设查询做多视角检索 + agentic multi-step reasoning，金融问答准确率提升 11.2%，幻觉降低 15%。

# 研究任务

金融 RAG QA 的检索增强与幻觉降低

# 方法

- Multi-HyDE: 生成多个 diverse hypothetical queries
- Multi-perspective retrieval from structured financial corpora
- Agentic multi-step reasoning workflow

# 指标

Accuracy +11.2%, Hallucination -15%

# 和 FinLeakAudit 的相似点

- Agentic RAG + 金融领域
- Multi-perspective / multi-source 检索

# 和 FinLeakAudit 的区别

- 做 QA 不做 forecasting
- 不做 temporal leakage
- 不做 evidence ablation
- 不做 forecast revision

# 撞车风险

Medium

# 可以引用的位置

- Related Work: Agentic RAG for finance
- Method: Multi-HyDE 检索策略参考
