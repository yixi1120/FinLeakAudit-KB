---
title: "Multi-Dimensional Behavioral Evaluation of Agentic Stock Prediction Systems Using LLM Judges with Closed-Loop RL Feedback"
year: 2026
venue: arXiv → Knowledge-Based Systems
ccf_level: preprint
arxiv: "2605.05739"
tags: [agentic-stock-prediction, llm-judge, behavioral-evaluation, rl-feedback, sac]
status: skimmed
collision_risk: low
must_cite: false
---

# 一句话总结

用 LLM judge ensemble 评估 agentic 股票预测系统在 6 个行为维度的表现，评分转为 SAC reward 做 fine-tuning。

# 研究任务

评估 agentic 股票预测系统的行为质量

# 方法

- 6 个行为维度: regime detection, routing, adaptation, risk calibration, strategy coherence, error recovery
- LLM judge ensemble with rubric-anchored scoring
- Closed-loop RL feedback (SAC reward)

# 指标

MAPE: 0.61% → 0.54%, Sharpe +18%

# 和 FinLeakAudit 的区别

- 评估 agent behavior（行为质量）
- FinLeakAudit 审计 evidence temporal validity（证据可靠性）
- 不同 audit target

# 撞车风险

Low — 维度不同

# 可以引用的位置

- Related Work: 说明 agentic stock prediction evaluation 是热点
