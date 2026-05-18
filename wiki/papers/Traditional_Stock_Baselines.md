---
title: "Traditional Stock Prediction Baselines (CCF A/B)"
year: 2018–2024
venue: KDD / EMNLP / CIKM / PAKDD
ccf_level: CCF A/B
arxiv: ""
tags: [traditional-baselines, stock-prediction, non-llm, ccfa, ccfb]
status: skimmed
collision_risk: low
must_cite: true
---

# 一句话总结

传统的非 LLM 股票预测强基线集合，包括 Data-Axis Transformer (KDD 2021)、Deep Attentive Learning (EMNLP 2020)、Hybrid Deep Sequential (CIKM 2018) 等。

# 论文清单

## Data-Axis Transformer (KDD 2021, CCF A)
- 多变量股票运动预测
- 多层级上下文 + transformer
- 强传统 baseline

## Deep Attentive Learning (EMNLP 2020, CCF B)
- 社交媒体文本 + 公司关系做股票预测
- Attention-based 文本驱动预测

## Hybrid Deep Sequential (CIKM 2018, CCF B)
- 社交文本驱动股票预测
- 早期文本+序列融合方法

## Multi-Time Window Ensemble (PAKDD 2024, CCF C)
- 多时间窗口集成 + 期望收益最大化

## Ploutos (WWW Companion 2025)
- 金融 LLM 可解释股票预测
- Companion paper，发表级别需注意

# 和 FinLeakAudit 的关系

- 传统 baseline，不做 RAG/Agent/Leakage
- Used for baseline comparison in experiments

# 可以引用的位置

- Related Work: traditional stock prediction background
- Experiments: baseline comparison
