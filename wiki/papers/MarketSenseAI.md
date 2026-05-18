---
title: "MarketSenseAI 2.0: Enhancing Stock Analysis through LLM Agents"
year: 2025
venue: arXiv
ccf_level: preprint
arxiv: "2502.00415"
tags: [multi-agent, stock-analysis, rag, sec-filings, earnings-calls, investment-decision]
status: deep-read
collision_risk: high
must_cite: true
---

# 一句话总结

多 Agent + RAG 股票分析系统：Fundamental / Technical / News / Macro 四个 specialist agent 分别处理不同信息源，已在 S&P 100/S&P 500 上跑出 125.9% 累计收益（vs 73.5% benchmark）。

# 研究任务

S&P 100 / S&P 500 股票投资分析

# 方法

- 4 个 specialist agent：Fundamental, Technical, News Sentiment, Macro
- RAG 处理 SEC filings, earnings calls, macro reports
- 融合多源信号做投资决策

# 数据

S&P 100, S&P 500, SEC filings + earnings calls + macro reports + price data (2023–2024)

# 指标

Cumulative return 125.9% vs 73.5% S&P 100 benchmark

# 和 FinLeakAudit 的相似点

- Multi-Agent + RAG + 股票分析
- 最接近我们早期方向

# 和 FinLeakAudit 的区别

- No time-safe filtering
- No Verifier Agent
- No Temporal Leakage Rate
- No structured evidence traceability
- No evidence ablation
- No forecast revision

# 撞车风险

High — 如果我们继续做 "Multi-Agent RAG 股票预测" 就直接撞

# 可以引用的位置

- Related Work: multi-agent stock analysis baseline
- Motivation: "可能使用了未来信息导致收益虚高"

# 适合作为 baseline 吗？

是。可以作为被审计的 multi-agent 系统。

# 待确认问题

- [ ] 是否有时间约束？（大概率没有）
- [ ] 开源？
