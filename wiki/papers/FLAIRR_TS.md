---
title: "FLAIRR-TS: Forecasting LLM-Agents with Iterative Refinement and Retrieval for Time Series"
year: 2025
venue: EMNLP 2025 Findings
ccf_level: CCF B
arxiv: "2508.19279"
tags: [iterative-refinement, self-correction, time-series-forecasting, llm-agent, retrieval]
status: skimmed
collision_risk: medium
must_cite: true
---

# 一句话总结

用 frozen LLM agent 做时序预测，先 retrieval 再 forecast，然后 self-verification → self-correction 迭代精炼。最接近我们的 Forecast Revision 模块。

# 研究任务

通用时序预测（不限于金融），用 LLM agent + iterative refinement 提升预测准确性。

# 方法

- Frozen LLM agent（不做微调）
- retrieval → forecast → self-verification → self-correction 循环
- 参考 SETS (Self-verification and self-correction) 和 CRITIC 框架

# 数据

通用时序数据（非金融专用）

# 指标

预测准确率提升

# 和 FinLeakAudit 的相似点

- 都有 forecast revision / self-correction 循环
- 都结合 retrieval 和 agent

# 和 FinLeakAudit 的区别

- FLAIRR-TS 的 revision 是 accuracy-driven（预测值不对 → 改）
- FinLeakAudit 的 revision 是 leakage-driven（证据时间泄漏 → 删证据 → 重预测）
- FLAIRR-TS 不问"证据能不能用"
- FinLeakAudit 不单纯追求"预测更准"

# 撞车风险

Medium — revision 概念重叠，但触发器和目的完全不同

# 可以引用的位置

- Related Work: 区分 accuracy-driven vs leakage-driven revision
- Method: 引用其 iterative refinement 作为背景

# 适合作为 baseline 吗？

可以作为 general self-corrective forecasting 基线

# 待确认问题

- [ ] 开源代码？
- [ ] 金融数据上表现如何？
