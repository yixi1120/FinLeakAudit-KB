# Ingest Paper Prompt

## Instructions

Read the following paper and produce a paper card in the standard format.

## Paper Card Template

```markdown
---
title: 
year: 
venue: 
ccf_level: 
arxiv: 
tags: []
status: skimmed
collision_risk: low | medium | high | critical
must_cite: true | false
---

# 一句话总结

# 研究任务

# 方法

# 数据

# 指标

# 和 FinLeakAudit 的相似点

# 和 FinLeakAudit 的区别

# 撞车风险

# 可以引用的位置

# 适合作为 baseline 吗？

# 关键原文摘录

# 待确认问题
```

## Collision Risk Rules

See AGENTS.md for full rules. Summary:
- Critical: financial forecasting + Agentic RAG + leakage audit + evidence ablation + revision
- High: financial forecasting + Agentic RAG, or financial agent leakage, or forecast revision with retrieval
- Medium: financial QA with Agentic RAG, evidence cards, auditable financial agents
- Low: general RAG/time series/unrelated finance NLP
