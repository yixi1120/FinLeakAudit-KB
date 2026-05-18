---
title: "FinVet: A Collaborative Framework of RAG and External Fact-Checking Agents for Financial Misinformation Detection"
year: 2025
venue: arXiv
ccf_level: preprint
arxiv: "2510.11654"
tags: [fact-checking, financial-misinformation, dual-rag, confidence-voting, source-attribution]
status: skimmed
collision_risk: medium
must_cite: true
---

# 一句话总结

双 RAG 管道 + 外部 Fact-Checking Agent + 置信度加权投票做金融虚假信息检测。Fact-Checking Agent 架构与我们的 Verification Operators 类似。

# 研究任务

金融虚假信息检测（不是预测）

# 方法

- Dual RAG pipelines
- External fact-checking pipeline (Google Fact Check API + LLM fallback)
- Confidence-weighted voting
- Uncertainty flags
- Source attribution

# 和 FinLeakAudit 的区别

- FinVet 做 misinformation detection
- FinLeakAudit 做 forecasting evidence leakage audit
- FinVet 不涉及时间泄漏

# 撞车风险

Medium — fact-checking agent 概念重叠，但任务不同

# 引用建议

可在 Related Work 中说明 fact-checking/verification agents 存在，但我们的审计目标是 evidence temporal validity
