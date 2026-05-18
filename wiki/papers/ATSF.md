---
title: "Position: Beyond Model-Centric Prediction — Agentic Time Series Forecasting"
year: 2026
venue: arXiv
ccf_level: preprint
arxiv: "2602.01776"
tags: [agentic-forecasting, time-series, reflection, iterative-correction, position-paper]
status: skimmed
collision_risk: low
must_cite: false
---

# 一句话总结

提出 Agentic Time Series Forecasting (ATSF) 范式：perception→planning→action→reflection 的 iterative forecasting。Reflection 包括评估和修正预测。

# 和 FinLeakAudit 的关系

- ATSF 定义了 reflection/self-correction 范式
- FinLeakAudit 是在 ATSF 框架下做 leakage-specific audit
- ATSF 的 reflection 是泛化的（预测值不对→改），FinLeakAudit 的 revision 是 leakage-driven

# 引用建议

可引用 ATSF 作为 background，说明我们在 ATSF 的 reflection 阶段引入 evidence-level leakage audit
