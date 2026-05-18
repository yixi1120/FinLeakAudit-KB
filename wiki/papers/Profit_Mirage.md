---
title: "Profit Mirage: Revisiting Information Leakage in LLM-based Financial Agents"
year: 2025
venue: arXiv
ccf_level: preprint
arxiv: "2510.07920"
tags: [information-leakage, llm-financial-agents, profit-mirage, counterfactual, finlake-bench, factfin]
status: deep-read
collision_risk: critical
must_cite: true
---

# 一句话总结

系统研究 LLM 金融 Agent 的信息泄漏问题，提出"profit mirage"（利润幻象）—回测收益在模型知识窗口后消失。

# 研究任务

诊断 LLM financial agent 是否存在 memorization-driven profit inflation。量化四类信息泄漏维度。

# 方法

- FinLake-Bench：泄漏鲁棒评估套件
- FactFin：外部框架 — Strategy Code Generator + RAG + MCTS + Counterfactual Simulator
- 四个实验：Backtesting vs Generalization、Counterfactual Evaluation、Memorization Audits、Before/After Fine-tuning

# 数据

6 种金融资产（美股/A股/港股/加密货币），2024.7–2025.6

# 指标

Total Return, Sharpe Ratio, Maximum Drawdown, Prediction Consistency (PC), Confidence Invariance (CI), Input Dependency Score (IDS)

# 和 FinLeakAudit 的相似点

- 都关注金融预测中的信息泄漏
- 都是一类"审计/诊断"视角

# 和 FinLeakAudit 的区别

- Profit Mirage 关注 LLM 预训练记忆导致的整体泄漏（memorization-driven）
- FinLeakAudit 关注 RAG 检索到的每条证据是否在预测时点可用（retrieved-evidence-level）
- Profit Mirage 不做 evidence attribution 和 forecast revision
- Profit Mirage 评估 agent-level leakage，FinLeakAudit 做 evidence-level audit

# 撞车风险

Critical — 不能声称"first to study leakage in LLM financial agents"

# 可以引用的位置

- Introduction: 泄漏问题的 motivation
- Related Work: 区分 agent-level leakage vs evidence-level leakage
- Experiments: 参考 FinLake-Bench 的泄漏评估指标

# 适合作为 baseline 吗？

是 — 泄漏诊断框架可作为问题意识来源

# 待确认问题

- [ ] FinLake-Bench 是否开源？
- [ ] FactFin 的 RAG 模块如何设置时间约束？
