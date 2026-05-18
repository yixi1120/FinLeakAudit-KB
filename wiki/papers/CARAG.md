---
title: "Decoding the Market's Pulse: Context-Enriched Agentic Retrieval Augmented Generation for Predicting Post-Earnings Price Shocks"
year: 2026
venue: EACL 2026 Long Paper
ccf_level: CCF B
arxiv: aclanthology.org/2026.eacl-long.141
tags: [agentic-rag, financial-forecasting, earnings-calls, multi-agent, ctkg, stock-prediction]
status: deep-read
collision_risk: critical
must_cite: true
---

# 一句话总结

用 Causal-Temporal Knowledge Graph (CTKG) 驱动多 Agent 协作，预测 earnings call 后的价格冲击。这是目前最完整的 Agentic RAG 金融预测系统。

# 研究任务

预测 post-earnings price shocks（财报电话会后股价变动方向），多 horizon：1/3/7/15/30 交易日。

# 方法

- CTKG：Causal-Temporal Knowledge Graph，从 earnings transcripts + financial statements 抽取结构化事实
- 多 specialist agent 并行分析：Historic Performance、Historic Earnings、Competitor Analyst、Synthesizer
- Temporal-causal reasoning，leakage-free evaluation

# 数据

NASDAQ + NYSE earnings calls，SEC filings，MAEC dataset。另释放 post-cutoff transcripts（Aug 2023–Dec 2024）做泄漏测试。

# 指标

Macro-F1, MCC, Sharpe, annualized return（回测 2 年 36%, Sharpe 1.64）

# 和 FinLeakAudit 的相似点

- 都是 Agentic RAG + 金融预测
- 都做了时间泄漏相关的评估
- 都有 evidence grounding

# 和 FinLeakAudit 的区别

- CARAG 做更好的预测（improve prediction accuracy）
- FinLeakAudit 审计现有系统的证据泄漏（audit leakage）
- CARAG 基于 KG，FinLeakAudit 审计 RAG 检索的证据
- CARAG 没有 evidence-level ablation 和 leakage-driven revision

# 撞车风险

Critical — 如果我们继续主打"Agentic RAG 股票预测"，正面撞车。

# 可以引用的位置

- Introduction: 引入 Agentic RAG 金融预测背景
- Related Work: 作为最强 baseline 和主要竞品讨论
- Experiments: 作为 host system 或对比基线

# 适合作为 baseline 吗？

是。如果开源，可以作为被审计的 host system。

# 关键原文摘录

"the first study... that integrates causal reasoning and temporal inference"
"We mitigate leakage via named entity time constraints and post-cutoff evaluation"

# 待确认问题

- [ ] CTKG 是否开源？
- [ ] 数据集是否可获取？
- [ ] 是否可以用作 host system？
