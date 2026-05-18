---
title: "SHARP: A Self-Evolving Human-Auditable Rubric Policy for Financial Trading Agents"
year: 2026
venue: arXiv
ccf_level: preprint
arxiv: "2605.06822"
tags: [auditable-trading, rubric-policy, self-evolving, neurosymbolic, morgan-stanley]
status: skimmed
collision_risk: medium
must_cite: true
---

# 一句话总结

Morgan Stanley 的神经符号框架：把交易策略写成可读的 condition→action 规则表，attribution agent 定位策略失败根源，做原子级规则编辑 + walk-forward validation。

# 研究任务

让金融交易 Agent 的策略可审计、可自我进化。

# 方法

- 神经符号：LLM 文本分析 → 符号规则引擎
- Attribution agent：跨样本推理定位失败规则
- Atomic rule edits + walk-forward validation
- 规则表（rubric）限制 agent 推理边界

# 数据

多市场交易数据

# 指标

Walk-forward validation performance

# 和 FinLeakAudit 的相似点

- 都有 "auditable" / "audit" 概念
- 都面向金融系统
- 都有修正/进化机制

# 和 FinLeakAudit 的区别

- SHARP 审计 trading policy rules（策略规则对不对）
- FinLeakAudit 审计 retrieved evidence temporal validity（证据时间有没有泄漏）
- SHARP 做 policy optimization，FinLeakAudit 做 evidence auditing
- SHARP 是交易执行层面，FinLeakAudit 是 RAG 检索层面

# 撞车风险

Medium — 标题都含 "Audit"，但审计对象完全不同

# 可以引用的位置

- Related Work: 说明 auditable financial agents 是趋势，区分 policy audit vs evidence audit

# 待确认问题

- [ ] 是否涉及 RAG / evidence retrieval？
