---
title: "VERAFI: Verified Agentic Financial Intelligence through Neurosymbolic Policy Generation"
year: 2025
venue: arXiv
ccf_level: preprint
arxiv: "2512.14744"
tags: [verified-rag, neurosymbolic, financial-qa, gaap, sec, mathematical-validation]
status: skimmed
collision_risk: high
must_cite: true
---

# 一句话总结

Agentic RAG + 神经符号验证，自动检查金融合规（GAAP/SEC）和计算正确性。"Verified Agentic Financial Intelligence" 命名与我们早期方向高度重叠。

# 研究任务

金融 QA / 合规推理 / Verified financial intelligence

# 方法

- Dense retrieval + cross-encoder reranking
- Tool-enabled financial agents (calculator / Python / web)
- Neurosymbolic policy generation
- GAAP / SEC / mathematical validation rules

# 指标

Factual correctness, completeness, retrieval metrics

# 和 FinLeakAudit 的相似点

- "Verified" + "Agentic" + "Financial" 三位一体
- 都有验证/审计机制

# 和 FinLeakAudit 的区别

- VERAFI 验证金融 QA 和合规推理
- FinLeakAudit 审计金融预测中的 evidence leakage
- VERAFI 不做时间泄漏检测
- VERAFI 不做预测修正

# 撞车风险

High — 命名高度重叠，"Verified" 被抢占

# 可以引用的位置

- Related Work: verified financial intelligence background
- Method: policy-guided generation 参考

# 关键教训

这促使我们从 "Verified" 转向 "Leakage Detection" / "Evidence-Grounded" 命名
