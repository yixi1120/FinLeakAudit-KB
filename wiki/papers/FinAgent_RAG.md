---
title: "Agentic Retrieval-Augmented Generation for Financial Document Question Answering"
year: 2026
venue: arXiv
ccf_level: preprint
arxiv: "2605.05409"
tags: [agentic-rag, financial-qa, self-verification, program-of-thought, adaptive-router]
status: deep-read
publication_status: withdrawn
collision_risk: excluded
must_cite: false
---

# 一句话总结

金融文档 QA 的 Agentic RAG：对比检索器 + PoT 数值推理 + 自适应路由 + 自校验。
该预印本已于 2026-07-05 撤稿，作者说明实验设计存在重大方法错误，结论不再受支持。

# 研究任务

金融文档问答，尤其是多步数值推理（FinQA / ConvFinQA / TAT-QA）

# 方法

1. Contrastive Financial Retriever — temporal/metric-swap/granularity/entity-swap hard negatives
2. Program-of-Thought — 生成 Python 做数值计算
3. Adaptive Strategy Router — 按复杂度分配 single-pass 或 full agentic loop
4. Self-Verifier — 检查答案可靠性并触发 query refinement

# 数据

FinQA, ConvFinQA, TAT-QA

# 指标

Execution Accuracy 76.81%/78.46%/74.96%, Program Accuracy, F1, API calls, latency, cost

# 和 FinLeakAudit 的相似点

- Agentic RAG + self-verification
- 对比检索器中的 temporal hard negatives 与我们的时间约束相关
- Self-verifier 与我们的 verification operators 类似

# 和 FinLeakAudit 的区别

- 任务是 QA 不是 stock prediction
- 不做 evidence-level leakage audit
- 不做 forecast revision
- Self-verification 是 accuracy 导向

# 撞车风险

Medium — 模块相似但任务完全不同

# 可以引用的位置

- 不作为支持性引用。
- 如讨论研究筛选或撤稿处置，可明确标注 withdrawn 后提及。

# 撤稿核验

- 核验日期：2026-09-08
- 官方页面：https://arxiv.org/abs/2605.05409
- 页面状态：withdrawn
- 作者说明：实验设计存在影响结论有效性的重大方法错误，且无法在当前框架内修复。

# 处置

从论文 Related Work、baseline 与结果支撑列表中排除；保留本卡作为研究审计记录。
