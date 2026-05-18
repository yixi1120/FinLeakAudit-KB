---
title: "TRACE: Temporal Rule-Anchored Chain-of-Evidence on Knowledge Graphs for Interpretable Stock Movement Prediction"
year: 2026
venue: arXiv
ccf_level: preprint
arxiv: "2603.12500"
tags: [stock-movement-prediction, temporal-kg, evidence-chain, interpretable, rule-mining]
status: deep-read
collision_risk: high
must_cite: true
---

# 一句话总结

在 temporal financial KG 上做规则引导的多跳证据链探索，输出 auditable UP/DOWN 预测。覆盖了时间约束 + 证据链 + 可解释预测。

# 研究任务

可解释的股票涨跌方向预测

# 方法

- Temporal financial KG（42K nodes, 174K edges）
- Entity types: TextSource, Event, Product, Financial, Company, Person
- Relations: EXTRACTED_FROM, SELLS, INVESTED_IN, PARTNERED, SUED
- Rule mining → relation motifs → constrained multi-hop exploration
- LLM 做 relation selection 和 path validation
- As-of temporal constraint，contemporaneous news grounding

# 数据

S&P 500，2022–2023

# 指标

Accuracy, Precision, Recall, F1, backtest return, Sharpe

# 和 FinLeakAudit 的相似点

- 都做时间约束证据分析
- 都有 evidence chain / grounding

# 和 FinLeakAudit 的区别

- TRACE 基于 KG，FinLeakAudit 基于 RAG 检索
- TRACE 做预测，FinLeakAudit 做审计
- TRACE 不做 evidence ablation 和 forecast revision

# 撞车风险

High — 如果主打"temporal evidence chain for stock prediction" 会撞

# 可以引用的位置

- Related Work: temporal evidence chain baseline
- Experiments: KG-based baseline 对比

# 待确认问题

- [ ] KG 是否开源？
