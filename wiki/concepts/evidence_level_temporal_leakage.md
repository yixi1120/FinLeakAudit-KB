# Evidence-Level Temporal Leakage

## 定义

在 Agentic RAG 金融预测中，如果检索到的某条证据（新闻、财报、公告）的发布时间晚于预测时间点，但仍然被系统检索、引用并用于支撑预测，这就是 **证据级时间泄漏**。

与传统的 look-ahead bias 不同：evidence-level leakage 聚焦于 RAG pipeline 中 **单条 retrieved evidence** 的时间有效性。

## 2026 研究边界更新

Look-Ahead-Bench 和 Leakage-Aware Benchmarking 已经把 point-in-time / decision-time 约束带入金融 LLM 预测评估。FinLeakAudit 不应把“时间可用性检查”单独包装成完整 novelty，而应研究更窄的组合问题：单条证据的可用性如何连接到 claim attribution、support/contradiction、forecast sensitivity 和 revision。

## 为什么重要

- 金融预测中，未来信息会虚高回测收益 → forecast inflation / profit mirage
- Agentic RAG 的检索机制可能无意中检索到未来证据
- LLM 可能基于未来证据生成看似合理但不可用的预测理由

## 相关论文

- [[CARAG]] — 做了 leakage-free evaluation
- [[Profit_Mirage]] — 定义了 profit mirage 问题
- [Look-Ahead-Bench](https://arxiv.org/abs/2601.13770) — benchmark-level look-ahead bias evaluation
- [Leakage-Aware Benchmarking](https://arxiv.org/abs/2606.22719) — decision-time constrained financial forecasting
- [[FinLeakAudit]] — 本文的审计目标

## 与相近概念的区别

| 概念 | 区别 |
|---|---|
| Look-ahead bias | 传统量化金融概念，关注特征构造时的数据泄漏 |
| Pretraining contamination | LLM 预训练记忆导致的泄漏（Profit Mirage 关注的） |
| Evidence-level temporal leakage | RAG 检索到的具体证据时间不可用（本文关注的） |
| Data snooping | 研究者在设计阶段看到全部数据导致的选择偏差 |

## 本文论文中的用法

- Introduction: Problem statement
- RQ1: 泄漏是否真实存在？
- RQ3: FinLeakAudit 能否检测并删除泄漏证据？

## 可写进论文的句子

"Evidence-level temporal leakage occurs when a retrieved news article, financial filing, or corporate announcement published after the prediction date enters the RAG pipeline and influences the forecast direction or confidence."
