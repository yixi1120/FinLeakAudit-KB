# Forecast Inflation / Profit Mirage

## 定义

由于 Agentic RAG 金融预测系统在检索、引用或解释阶段使用了预测时点之后才可获得的证据，导致回测收益、预测准确率和置信度虚高的现象。

Profit Mirage（利润幻象）是其一种特定表现：历史回测收益在模型知识窗口后消失。

## 为什么重要

- 如果预测的"好成绩"来自未来信息，系统在实盘中必然失败
- 审计框架的核心 motivation

## 相关论文

- [[Profit_Mirage]] — 提出 profit mirage 概念
- [[CARAG]] — 报告了 leakage-free 回测收益
- [[The_New_Quant]] — 综述中讨论了 temporal leakage

## 本文论文中的用法

- Motivation section 的核心概念
- 与 Profit Mirage 的区分：我们关注 evidence-level inflation，不是 agent-level inflation
