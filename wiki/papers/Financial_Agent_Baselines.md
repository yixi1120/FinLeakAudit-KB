---
title: "Financial Agent Baselines (TradingAgents, FinMem, FinAgent, QuantAgent, HedgeAgents, FinCON, FinRobot, StockAgent)"
year: 2023–2025
venue: Various
ccf_level: various
arxiv: ""
tags: [financial-agents, multi-agent-trading, llm-baselines, profit-mirage-baselines]
status: skimmed
collision_risk: low
must_cite: true
---

# 一句话总结

Profit Mirage 中作为 baseline 的 LLM 金融 Agent 系统集合。可以作为 FinLeakAudit 的被审计对象或实验 baseline。

# 论文清单

| 系统 | 任务 | 特点 |
|---|---|---|
| TradingAgents | Multi-agent trading | 多 Agent 交易决策 |
| FinMem | Financial memory agent | 分层记忆增强 |
| FinAgent | Financial trading agent | 策略生成 |
| QuantAgent | Quantitative trading | 量化策略 |
| HedgeAgents | Multi-agent hedge fund | 对冲基金风格 |
| FinCON/FinCon | Multi-agent financial decision | Conceptual verbal reinforcement |
| FinRobot | Agentic finance | 金融机器人 |
| StockAgent | Stock prediction | TRACE baseline |

# 和 FinLeakAudit 的关系

- 这些系统适合作为 leakage audit target
- Profit Mirage 发现它们在 backtesting vs generalization 中有 performance decay

# 可以引用的位置

- Related Work: financial agent systems
- Experiments: audited systems / baselines

# 待确认

- [ ] 各系统是否开源？
- [ ] 具体 arXiv ID / venue 需要补充
