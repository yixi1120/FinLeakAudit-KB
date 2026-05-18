# Agentic RAG 金融预测与证据泄漏审计：潜在引用论文清单

> 生成目的：整理本对话中提到的相关论文，供后续写论文、做 Related Work、设计 baseline、做 novelty/collision check 时让 agent 作为潜在引用与借鉴材料使用。  
> 当前研究定位建议：**Evidence-level leakage audit and verifier-guided correction for Agentic RAG financial forecasting**。  
> 建议框架名：**FinLeakAudit** 或 **FinLeakGuard**。  
> 生成日期：2026-05-18

---

## 0. 我们当前研究定位

原始方向：

```text
Time-Safe Verified Multi-Agent RAG for Stock Movement Prediction
```

经过竞品检查后，建议改为：

```text
FinLeakAudit:
A Skill-Based Evidence Leakage Auditing Framework
for Agentic RAG Financial Forecasting
```

中文：

```text
FinLeakAudit：面向 Agentic RAG 金融预测的技能化证据泄漏审计框架
```

核心问题不再是“再提出一个 Agentic RAG 股票预测器”，而是：

> 现有 Agentic RAG 金融预测系统是否使用了未来证据、不可用证据或 unsupported evidence？  
> 这些证据是否造成了 forecast inflation / profit mirage？  
> 能否通过 evidence-level audit、skill-based audit protocol 和 verifier-guided revision 来检测、删除并修正这些污染？

---

## 1. 最高优先级竞品论文

### 1.1 CARAG — Decoding the Market’s Pulse: Context-Enriched Agentic Retrieval Augmented Generation for Predicting Post-Earnings Price Shocks

- **年份**：2026
- **发表/来源**：EACL 2026 Long Paper，ACL Anthology
- **核心任务**：预测 earnings call 后的 post-earnings price shocks
- **关键词**：Agentic RAG, financial forecasting, earnings calls, CTKG, multi-agent reasoning, post-earnings price movement
- **方法概述**：
  - 构建 **Causal-Temporal Knowledge Graph, CTKG**
  - 从 earnings call transcripts 和 financial statements 中抽取 fact
  - 多个 specialist agents 并行分析：
    - Historic Performance Agent
    - Historic Earnings Agent
    - Competitor Analyst Agent
    - Synthesizer Agent
  - 用 CTKG 检索结构化证据，做 temporal-causal reasoning
- **数据**：
  - NASDAQ earnings calls
  - NYSE earnings calls
  - MAEC dataset
  - financial statements from SEC filings
- **预测目标**：
  - 多 horizon：1、3、7、15、30 个交易日方向预测
- **指标**：
  - Macro-F1
  - MCC
  - Sharpe
  - annualized return
- **已覆盖的维度**：
  - Agentic RAG × 股票预测
  - 多智能体分工
  - CTKG-grounded evidence
  - look-ahead bias mitigation
  - post-cutoff evaluation
  - 多 horizon 预测
  - 回测收益
- **对我们威胁级别**：极高
- **为什么危险**：
  - 它已经做了“Agentic RAG + 金融预测 + 多 Agent + 图谱证据 + 时间约束 + 回测”。
  - 我们不能再主打“Agentic RAG for stock prediction”。
- **我们的区别应写成**：
  - CARAG focuses on improving post-earnings price-shock prediction through CTKG-grounded multi-agent reasoning.
  - Our work focuses on evidence-level leakage auditing and verifier-guided correction for Agentic RAG forecasting pipelines.
- **写作用途**：
  - 主竞品
  - strong baseline / host system
  - Related Work 中必须单独讨论

---

### 1.2 Profit Mirage — Revisiting Information Leakage in LLM-based Financial Agents

- **年份**：2025
- **发表/来源**：arXiv 2510.07920
- **核心任务**：研究 LLM-based financial agents 的信息泄漏和“利润幻象”
- **关键词**：LLM financial agents, information leakage, profit mirage, FinLake-Bench, FactFin, counterfactual evaluation
- **方法概述**：
  - 系统性量化 LLM 金融智能体的信息泄漏
  - 提出 **profit mirage**：历史回测收益在模型知识窗口后消失
  - 提出 **FinLake-Bench**
  - 提出 **FactFin**：
    - Strategy Code Generator
    - RAG for market factors
    - MCTS
    - Counterfactual Simulator
- **泄漏评估实验**：
  1. Backtesting vs Generalization
  2. Counterfactual Evaluation
  3. Memorization Audits
  4. Before-and-after Fine-tuning
- **指标**：
  - Total Return
  - Sharpe Ratio
  - Maximum Drawdown
  - Prediction Consistency, PC
  - Confidence Invariance, CI
  - Input Dependency Score, IDS
- **已覆盖的维度**：
  - LLM financial agents leakage
  - pretraining contamination
  - memorization-driven profit illusion
  - counterfactual leakage evaluation
  - out-of-sample generalization
- **对我们威胁级别**：极高
- **为什么危险**：
  - 它已经把“金融 Agent 存在信息泄漏”定义为核心问题。
  - 我们不能声称首次研究 financial agent leakage。
- **我们的区别应写成**：
  - Profit Mirage diagnoses memorization-driven profit inflation in LLM financial agents.
  - Our work audits and corrects retrieved-evidence-level leakage inside Agentic RAG forecasting pipelines.
- **写作用途**：
  - 问题定义型核心引用
  - leakage benchmark 参考
  - counterfactual evaluation 指标参考

---

### 1.3 TRACE — Temporal Rule-Anchored Chain-of-Evidence on Knowledge Graphs for Interpretable Stock Movement Prediction

- **年份**：2026
- **发表/来源**：arXiv 2603.12500
- **核心任务**：可解释股票涨跌预测
- **关键词**：stock movement prediction, temporal knowledge graph, rule-guided exploration, evidence chain, LLM-guided validation
- **方法概述**：
  - 构建 temporal financial KG
  - entity types：TextSource, Event, Product, Financial, Company, Person
  - relations：EXTRACTED_FROM, SELLS, INVESTED_IN, PARTNERED, SUED
  - 使用 rule mining 得到 relation motifs
  - 按规则约束 KG multi-hop exploration
  - LLM 做 relation selection 和 path validation
  - 输出 auditable UP/DOWN verdicts
- **重要机制**：
  - as-of temporal constraint
  - contemporaneous news grounding
  - rule-guided path search
  - evidence chain aggregation
- **数据**：
  - S&P 500
  - 2022–2023 temporal KG
  - 42K nodes, 174K edges
- **指标**：
  - Accuracy
  - Precision
  - Recall
  - F1
  - backtest return
  - Sharpe
- **对我们威胁级别**：高
- **为什么危险**：
  - 它已经覆盖“股票预测 + 时间有效证据链 + 可解释路径”。
  - 我们不能主打 temporal KG evidence chain。
- **我们的区别应写成**：
  - TRACE focuses on KG path reasoning for interpretable stock prediction.
  - Our work focuses on auditing retrieved evidence leakage and forecast revision in Agentic RAG systems.
- **写作用途**：
  - interpretable stock prediction 相关工作
  - KG-based baseline
  - time-aware evidence chain baseline

---

### 1.4 FinAgent-RAG — Agentic Retrieval-Augmented Generation for Financial Document Question Answering

- **年份**：2026
- **发表/来源**：arXiv 2605.05409
- **核心任务**：金融文档问答，尤其是多步数值推理
- **关键词**：Agentic RAG, financial QA, self-verification, Program-of-Thought, adaptive router
- **方法概述**：
  - Query Decomposer
  - Contrastive Financial Retriever
  - CoT Reasoner
  - PoT Reasoner
  - Adaptive Strategy Router
  - Self-Verifier with Query Refiner
- **关键创新**：
  1. Contrastive Financial Retriever
     - temporal hard negatives
     - metric-swap hard negatives
     - granularity hard negatives
     - entity-swap hard negatives
  2. Program-of-Thought Financial Reasoning
     - 生成 Python code 做金融数值计算
  3. Adaptive Strategy Router
     - 根据问题复杂度分配 single-pass 或 full agentic loop
  4. Self-verification
     - 检查答案可靠性并触发 query refinement
- **数据集**：
  - FinQA
  - ConvFinQA
  - TAT-QA
- **指标**：
  - Execution Accuracy
  - Program Accuracy
  - F1
  - API calls
  - latency
  - cost
- **对我们威胁级别**：中高
- **为什么危险**：
  - 它吃掉了 Agentic RAG + self-verification + adaptive router + PoT 的通用方法创新。
  - 但任务是金融 QA，不是股票预测。
- **我们的区别应写成**：
  - FinAgent-RAG solves financial document QA through iterative retrieval and self-verification.
  - Our work applies skill-based evidence leakage auditing to financial forecasting pipelines.
- **写作用途**：
  - self-verification 方法引用
  - PoT 数值计算引用
  - router / cost evaluation 借鉴
  - financial hard negatives 借鉴

---

## 2. 金融可信 RAG / 验证机制相关论文

### 2.1 VERAFI — Verified Agentic Financial Intelligence through Neurosymbolic Policy Generation

- **年份**：2025 / 2026
- **发表/来源**：arXiv 2512.14744
- **核心任务**：金融 QA / 合规推理 / verified financial intelligence
- **关键词**：verified RAG, neurosymbolic policy, financial QA, GAAP, SEC, mathematical validation
- **方法概述**：
  - dense retrieval + cross-encoder reranking
  - tool-enabled financial agents
  - calculator / Python / web tools
  - neurosymbolic policy generation
  - GAAP / SEC / mathematical validation rules
- **核心思想**：
  - RAG 找到正确文档不代表生成答案正确
  - 需要在 reasoning 阶段引入 policy-guided generation
- **指标**：
  - factual correctness
  - completeness
  - retrieval metrics
- **对我们威胁级别**：中高
- **为什么相关**：
  - 它的 policy-guided reasoning 与我们的 audit skill / verifier-guided generation 相关。
- **我们的区别**：
  - VERAFI 验证金融 QA 和合规推理。
  - 我们审计金融预测系统的 evidence leakage。
- **写作用途**：
  - policy-guided generation 参考
  - verified financial reasoning 参考
  - audit rules 设计参考

---

### 2.2 FinVet — A Collaborative Framework of RAG and External Fact-Checking Agents for Financial Misinformation Detection

- **年份**：2025
- **发表/来源**：arXiv 2510.11654
- **核心任务**：金融虚假信息检测
- **关键词**：financial misinformation detection, RAG, fact checking, confidence voting, source attribution
- **方法概述**：
  - dual RAG pipelines
  - external fact-checking pipeline
  - Google Fact Check API
  - LLM fallback
  - confidence-weighted voting
  - uncertainty flags
- **数据集**：
  - FinFact
- **指标**：
  - F1
  - Precision
  - Recall
  - ablation
- **对我们威胁级别**：中
- **为什么相关**：
  - 多路径验证、source attribution、confidence voting、uncertainty flags 可借鉴。
- **我们的区别**：
  - FinVet 做 misinformation detection。
  - 我们做 financial forecasting pipeline 中的 evidence leakage audit。
- **写作用途**：
  - external fact checking reference
  - confidence voting reference
  - uncertainty flag reference

---

### 2.3 Enhancing Financial RAG with Agentic AI and Multi-HyDE

- **年份**：2025
- **发表/来源**：FinNLP 2025 Workshop / ACL Anthology
- **核心任务**：金融问答中的 RAG 增强与幻觉降低
- **关键词**：Financial RAG, Agentic AI, Multi-HyDE, hallucination reduction
- **方法概述**：
  - Multi-HyDE 生成多个假设查询
  - multi-perspective retrieval
  - agentic multi-step reasoning
- **指标**：
  - accuracy improvement
  - hallucination reduction
- **相关结果**：
  - 准确率提升约 11.2%
  - 幻觉降低约 15%
- **对我们威胁级别**：中
- **我们的区别**：
  - 它做金融 RAG QA 可靠性。
  - 我们做 Agentic RAG 金融预测中的 evidence-level leakage audit。
- **写作用途**：
  - Multi-HyDE 检索参考
  - hallucination reduction related work

---

## 3. 金融 Agent / 股票分析系统相关论文

### 3.1 MarketSenseAI 2.0 — Enhancing Stock Analysis through LLM Agents

- **年份**：2025
- **发表/来源**：arXiv 2502.00415，另有 workshop 信息
- **核心任务**：LLM agents 做股票分析与投资决策
- **关键词**：LLM agents, RAG, SEC filings, earnings calls, macro reports, stock analysis
- **方法概述**：
  - 多 agent 系统
  - RAG 处理 SEC filings
  - RAG 处理 earnings calls
  - RAG 处理 macro reports
  - 结合 fundamental、technical、news sentiment、macro signals
- **指标**：
  - cumulative return
  - benchmark comparison
- **对我们威胁级别**：中高
- **为什么相关**：
  - 方向接近“LLM agents + RAG + stock analysis”。
- **我们的区别**：
  - 它做股票分析与投资建议。
  - 我们做证据泄漏审计与预测修正。
- **写作用途**：
  - financial LLM agent system baseline
  - stock analysis agent related work

---

### 3.2 TradingAgents

- **年份**：对话中作为金融 multi-agent baseline 提及
- **发表/来源**：需进一步核验具体版本
- **核心任务**：多智能体交易 / 金融决策
- **关键词**：multi-agent trading, LLM agents, financial decision-making
- **相关性**：
  - Profit Mirage 将其作为 LLM-based financial agent baseline 之一
  - 适合作为被审计对象或 baseline
- **对我们威胁级别**：中
- **写作用途**：
  - baseline
  - target system for leakage audit

---

### 3.3 FinMem

- **年份**：对话中作为 LLM-based financial agent baseline 提及
- **发表/来源**：需进一步核验具体版本
- **核心任务**：金融记忆增强 agent / 股票交易
- **关键词**：financial memory, LLM agent, trading
- **相关性**：
  - Profit Mirage 中作为 baseline
  - 在 backtesting vs generalization 中表现出明显 performance decay
- **对我们威胁级别**：中
- **写作用途**：
  - leakage audit baseline
  - memorization risk example

---

### 3.4 FinAgent

- **年份**：对话中作为 financial agent baseline 提及
- **发表/来源**：需进一步核验具体版本
- **核心任务**：金融 agent / 交易策略生成
- **相关性**：
  - Profit Mirage 中作为 baseline
- **写作用途**：
  - baseline
  - financial agent comparison

---

### 3.5 QuantAgent

- **年份**：对话中作为 financial agent baseline 提及
- **发表/来源**：需进一步核验具体版本
- **核心任务**：量化交易 agent
- **相关性**：
  - Profit Mirage 中作为 baseline
- **写作用途**：
  - baseline

---

### 3.6 HedgeAgents

- **年份**：对话中作为 financial multi-agent baseline 提及
- **发表/来源**：需进一步核验具体版本
- **核心任务**：多智能体金融交易 / 对冲基金风格分析
- **相关性**：
  - Profit Mirage 中作为 baseline
- **写作用途**：
  - multi-agent baseline

---

### 3.7 FinRobot

- **年份**：对话中作为 financial multi-agent baseline 提及
- **发表/来源**：需进一步核验具体版本
- **核心任务**：金融机器人 / agentic finance
- **相关性**：
  - Profit Mirage 中作为 baseline
- **写作用途**：
  - financial agent baseline

---

### 3.8 FinCON / FinCon

- **年份**：2024 附近
- **发表/来源**：对话中作为 LLM multi-agent financial decision-making 论文提及
- **核心任务**：金融决策多智能体系统
- **关键词**：LLM multi-agent, conceptual verbal reinforcement, financial decision-making
- **相关性**：
  - 作为金融 multi-agent 系统背景
- **写作用途**：
  - multi-agent financial reasoning related work

---

### 3.9 StockAgent

- **年份**：对话中作为 stock prediction baseline 提及
- **核心任务**：LLM/Agent 股票预测或股票分析
- **相关性**：
  - TRACE 的 baseline 之一
- **写作用途**：
  - stock prediction agent baseline

---

## 4. 金融 LLM / Benchmark / 基础模型相关论文

### 4.1 FinBen — A Holistic Financial Benchmark for Large Language Models

- **年份**：2024
- **发表/来源**：NeurIPS 2024 Datasets & Benchmarks
- **CCF**：NeurIPS 属 CCF A
- **核心任务**：金融 LLM 综合评测
- **关键词**：financial benchmark, LLM evaluation, finance tasks
- **相关性**：
  - 提供金融 LLM 评测背景
  - 适合作为 benchmark 相关工作
- **写作用途**：
  - financial LLM evaluation related work

---

### 4.2 FinBERT — A Pre-trained Financial Language Representation Model for Financial Text Mining

- **年份**：2020
- **发表/来源**：IJCAI 2020
- **CCF**：IJCAI 属 CCF B
- **核心任务**：金融文本预训练模型
- **关键词**：FinBERT, financial text mining, sentiment analysis
- **相关性**：
  - 金融文本分析基础模型
  - 股票预测、财报理解、情绪分析 baseline
- **写作用途**：
  - financial language model background
  - baseline

---

### 4.3 BloombergGPT

- **年份**：2023
- **发表/来源**：industry/arXiv
- **核心任务**：金融领域大语言模型
- **关键词**：financial LLM, Bloomberg, financial NLP
- **相关性**：
  - 金融 LLM 背景
- **写作用途**：
  - financial domain LLM related work

---

### 4.4 FinGPT

- **年份**：2023 左右
- **发表/来源**：arXiv / open-source financial LLM project
- **核心任务**：开源金融大模型
- **关键词**：FinGPT, financial LLM, open-source finance
- **相关性**：
  - 金融 LLM 生态重要背景
  - Profit Mirage baseline 之一
- **写作用途**：
  - financial LLM baseline/background

---

### 4.5 Fin-LLaMA

- **年份**：对话中作为金融模型 baseline 提及
- **核心任务**：金融领域 LLaMA
- **相关性**：
  - Profit Mirage baseline
- **写作用途**：
  - financial model baseline

---

### 4.6 InvestLM

- **年份**：对话中作为金融模型 baseline 提及
- **核心任务**：投资领域 LLM
- **相关性**：
  - Profit Mirage baseline
- **写作用途**：
  - financial model baseline

---

## 5. CCF A/B/C 股票预测相关论文

### 5.1 Learning to Generate Explainable Stock Predictions using Self-Reflective Large Language Models

- **年份**：2024
- **发表/来源**：WWW 2024
- **CCF**：WWW 属 CCF A
- **核心任务**：可解释股票预测
- **关键词**：self-reflective LLM, explainable stock prediction, Summarize-Explain-Predict
- **方法概述**：
  - Summarize-Explain-Predict framework
  - self-reflective LLM 生成可解释预测
- **相关性**：
  - CCF A 中非常相关的 LLM 股票预测论文
- **对我们威胁级别**：中高
- **我们的区别**：
  - 它做 explainable stock prediction。
  - 我们做 evidence leakage audit and verifier-guided correction。
- **写作用途**：
  - CCF A related work
  - explainable stock prediction baseline

---

### 5.2 Accurate Multivariate Stock Movement Prediction via Data-Axis Transformer with Multi-Level Contexts

- **年份**：2021
- **发表/来源**：KDD 2021
- **CCF**：KDD 属 CCF A
- **核心任务**：多变量股票运动预测
- **关键词**：stock movement prediction, Data-Axis Transformer, multi-level contexts
- **相关性**：
  - 强传统股票预测 baseline
  - 不涉及 LLM/RAG/Agent
- **写作用途**：
  - traditional stock prediction baseline
  - CCF A background

---

### 5.3 Deep Attentive Learning for Stock Movement Prediction From Social Media Text and Company Correlations

- **年份**：2020
- **发表/来源**：EMNLP 2020
- **CCF**：EMNLP 属 CCF B
- **核心任务**：利用社交媒体文本和公司关系预测股票运动
- **关键词**：stock movement prediction, social media, company correlations, attention
- **相关性**：
  - 文本驱动股票预测强基线
- **写作用途**：
  - text-based stock prediction baseline
  - company correlation baseline

---

### 5.4 Hybrid Deep Sequential Modeling for Social Text-Driven Stock Prediction

- **年份**：2018
- **发表/来源**：CIKM 2018
- **CCF**：CIKM 属 CCF B
- **核心任务**：社交文本驱动股票预测
- **关键词**：social text, stock prediction, sequential modeling
- **相关性**：
  - 早期文本股票预测基线
- **写作用途**：
  - traditional text-driven stock prediction baseline

---

### 5.5 Multi-Time Window Ensemble and Maximization of Expected Return for Stock Movement Prediction

- **年份**：2024
- **发表/来源**：PAKDD 2024
- **CCF**：PAKDD 属 CCF C
- **核心任务**：股票运动预测与期望收益最大化
- **关键词**：stock movement prediction, expected return, ensemble
- **相关性**：
  - CCF C 传统股票预测/收益优化
- **写作用途**：
  - CCF C stock prediction related work

---

### 5.6 Ploutos: Towards Explainable Stock Movement Prediction with Financial LLM

- **年份**：2025
- **发表/来源**：WWW Companion 2025
- **CCF 注意**：
  - Companion 通常不按 CCF A 主会计
- **核心任务**：金融 LLM 可解释股票预测
- **关键词**：financial LLM, explainable stock movement prediction
- **相关性**：
  - 方向相关，但发表级别需谨慎
- **写作用途**：
  - related work，可不作为主竞品

---

## 6. Agentic RAG / RAG / Self-verification 通用论文

- **Self-RAG**：自反思检索增强生成；adaptive retrieval / self-critique 基础。
- **CRAG**：纠错型 RAG；检索结果不可靠时触发纠正。
- **Active RAG**：主动检索；动态决定何时检索/检索什么。
- **ReAct**：reasoning + acting；agentic reasoning 基础。
- **Reflexion**：基于反思的 agent 自我改进。
- **IterRAG**：迭代式 RAG，作为 FinAgent-RAG baseline 提及。
- **MultiHop-RAG**：多跳 RAG benchmark / multi-hop reasoning。
- **IRCoT**：推理步骤和检索交替进行。
- **GraphRAG / GraphRAG-Tool Fusion**：图结构 RAG / 工具调用融合。
- **Agentic Retrieval-Augmented Generation for Time Series Analysis**：Agentic RAG 用于时间序列分析。
- **Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG**：Agentic RAG 综述。
- **SoK: Agentic RAG**：系统化总结 Agentic RAG。

写作用途：

```text
这些论文适合放在 Agentic RAG / verifier-guided RAG / iterative retrieval 的背景部分。
但它们大多不是金融预测，不是我们的直接竞品。
```

---

## 7. Skill / Knowledge Base / Audit Skill 相关论文与资料

### 7.1 Karpathy LLM Knowledge Base / LLM Wiki

- **来源**：Karpathy gist / 技术笔记
- **核心思想**：
  - raw sources 是不可变 source of truth
  - LLM 持续编译和维护中间层 wiki
  - wiki 包含 entity pages、主题总结、交叉引用、矛盾点
- **相关性**：
  - 可抽象为 **Point-in-Time Evidence Wiki**
- **注意**：
  - 不适合直接作为强学术引用
  - 适合作为灵感来源
- **写作转化**：
  - 不写“Karpathy Wiki”
  - 写 “agent-compiled point-in-time evidence memory”

---

### 7.2 OpenAI Skills / ChatGPT Skills

- **来源**：OpenAI Help / product documentation
- **核心思想**：
  - Skills 是可复用、可分享的 workflow
  - 可包含 instructions、examples、code
- **相关性**：
  - 可抽象为 **Skill-based Audit Layer**
- **注意**：
  - 产品文档不是学术论文
  - 不建议作为主要 related work
- **写作转化**：
  - 不写“我们用了 OpenAI Skills”
  - 写 “we formalize audit routines as reusable skill protocols”

---

### 7.3 Anthropic Agent Skills

- **来源**：Anthropic engineering blog / docs
- **核心思想**：
  - Agent Skills 包含 SKILL.md、scripts、resources
  - agent 根据任务动态加载技能
- **相关性**：
  - skill-based audit protocol 设计参考
- **注意**：
  - 工程资料，不是主论文引用
- **写作用途**：
  - 可以放在 system design inspiration，慎用

---

### 7.4 SkillGuard-Robust

- **年份**：2026
- **发表/来源**：arXiv 2604.25109
- **核心任务**：不可信 Agent Skills 的安全审计
- **关键词**：agent skill security, pre-load auditing, role-aware evidence extraction, semantic verification
- **相关性**：
  - “Skill auditing” 方向竞品
  - 不是金融预测
- **对我们威胁级别**：中
- **为什么相关**：
  - 名字和 skill audit 概念接近
- **我们的区别**：
  - 它审计 skill package 是否恶意/安全。
  - 我们用 skill-based protocols 审计金融预测证据泄漏。
- **命名提醒**：
  - 不要用 SkillGuard 作为框架名。

---

### 7.5 SkillProbe

- **年份**：2026
- **发表/来源**：arXiv / html
- **核心任务**：multi-agent collaborative skill security auditing
- **关键词**：agent skills, security auditing, compliance filtering, semantic consistency, cross-skill link attacks
- **相关性**：
  - skill 审计安全方向
- **我们的区别**：
  - 它审计 skill 的安全风险。
  - 我们用 skill 审计金融预测 evidence leakage。
- **写作用途**：
  - 说明 skill auditing 已有安全方向，但金融预测 evidence audit 仍不同。

---

### 7.6 Semia

- **年份**：2026
- **发表/来源**：arXiv 2605.00314
- **核心任务**：Agent Skill 静态安全审计
- **关键词**：Skill Description Language, Datalog, static audit, prompt injection, secret leakage, confused deputy
- **相关性**：
  - skill package auditing
- **我们的区别**：
  - Semia 审计 skill 包自身是否危险。
  - 我们把 skill 当作可复用审计流程，用于金融预测 evidence leakage。
- **写作用途**：
  - skill-based audit related work
  - 命名避让

---

## 8. 金融 RAG / 金融检索 / 金融问答相关论文

- **RE-FIN — Retrieval-based Enrichment for Financial Data**
  - COLING Industry 2025
  - 金融数据检索增强
  - 可作为 financial retrieval related work

- **Nano-ESG**
  - ECIR 2025
  - 企业 ESG 信息抽取
  - optional background

- **ERATTA**
  - Extreme RAG for Table To Answers with Large Language Models
  - 企业表格问答的极限 RAG 架构
  - table QA / enterprise RAG background

- **Finance Agent Benchmark**
  - 真实金融研究任务上的 LLM agent benchmark
  - 可作为 benchmark reference

---

## 9. 综述类论文

- **The New Quant: A Survey of Large Language Models in Financial Prediction and Trading**
  - arXiv 2510.05533
  - 金融预测与交易中 LLM 的综述
  - 对 introduction / related work 很重要

- **Large Language Model Agent in Financial Trading: A Survey**
  - arXiv 2408.06361
  - 金融交易中的 LLM Agent 综述

- **Large Language Models for Financial Aid in Financial Time-series Forecasting**
  - arXiv 2410.19025
  - LLM 辅助金融时间序列预测

- **Large Language Models for Time Series: A Survey**
  - arXiv 2402.01801
  - LLM4TS 基础综述

- **Foundation Models for Time Series Analysis: A Tutorial and Survey**
  - arXiv 2403.14735
  - 时间序列基础模型综述

- **Empowering Time Series Analysis with Foundation Models**
  - arXiv 2405.02358
  - TS foundation models

- **Foundation Models for Time Series: A Survey**
  - arXiv 2504.04011

- **Towards Cross-Modality Modeling for Time Series Analytics: A Survey in the LLM Era**
  - arXiv 2505.02583
  - multimodal time series related work

---

## 10. 时间序列 LLM 方法论文

- **PatchFormer**
  - patch-based hierarchical masked reconstruction
  - zero-shot multi-horizon forecasting

- **DP-GPT4MTS**
  - dual prompt
  - textual-numerical time series forecasting

- **PatchInstruct**
  - patch prompting + decomposition

- **Time-LlaMA**
  - linear tokenization + D-LoRA

- **One-for-All**
  - frozen LLM + rank-stabilized LoRA

- **LLM-Mixer**
  - multiscale mixing in LLMs for time series forecasting

- **TimeSeriesExam**
  - time series understanding benchmark

- **Frequency Matters**
  - spectral shift robustness

- **Towards Interpretable Time Series Foundation Models**
  - interpretability of TS FMs

这些适合写在 LLM4TS / financial time-series forecasting 的背景部分。

---

## 11. 其他金融 NLP / 信息抽取相关论文

- **Financial Named Entity Recognition: How Far Can LLM Go?**
  - financial NER
  - evidence wiki 中实体抽取可参考

- **Are LLMs Good In-context Learners for Financial Sentiment Analysis?**
  - 金融情绪分析
  - event sentiment extraction 可参考

- **Integrating Traditional Technical Analysis with AI: A Multi-Agent LLM-Based Approach to Stock Market Forecasting**
  - Elliott Wave + multi-agent LLM stock forecasting
  - financial multi-agent forecasting related work

- **A Role-Aware Multi-Agent Framework for Financial Education Question Answering with LLMs**
  - generator / retriever / expert reviewer
  - reviewer agent 参考

- **Rethinking Retrieval: From Traditional RAG to Agentic and Non-Vector Reasoning Systems in the Financial Domain**
  - financial retrieval evaluation
  - vector RAG vs non-vector hierarchical retrieval

- **Graph RAG-Tool Fusion**
  - graph retrieval + tool calling

- **Adaptive Query Routing**
  - financial/legal/medical document hybrid retrieval routing

---

## 12. 建议的论文 Related Work 分组

### 12.1 Financial Forecasting and Stock Movement Prediction

可引用：

- Data-Axis Transformer, KDD 2021
- Deep Attentive Learning, EMNLP 2020
- Hybrid Deep Sequential Modeling, CIKM 2018
- SEP, WWW 2024
- TRACE
- CARAG
- Ploutos
- MarketSenseAI 2.0

重点写：

> Existing works focus on improving forecasting accuracy and interpretability, but rarely audit whether retrieved evidence is temporally admissible and faithfully used in prediction rationales.

---

### 12.2 LLM-based Financial Agents and Leakage

可引用：

- Profit Mirage
- TradingAgents
- FinMem
- FinAgent
- QuantAgent
- HedgeAgents
- FinCON
- MarketSenseAI 2.0
- The New Quant

重点写：

> Prior work reveals memorization-driven profit mirage and leakage in LLM financial agents, but does not provide evidence-level auditing for Agentic RAG forecasting pipelines.

---

### 12.3 Agentic RAG and Financial RAG

可引用：

- FinAgent-RAG
- Enhancing Financial RAG with Agentic AI and Multi-HyDE
- VERAFI
- FinVet
- Rethinking Retrieval
- GraphRAG-Tool Fusion
- Agentic RAG Survey
- Agentic RAG for Time Series Analysis

重点写：

> Existing Agentic RAG work improves retrieval, reasoning, and self-verification, but most targets QA or fact checking rather than forecasting reliability under temporal constraints.

---

### 12.4 Verification, Skill-based Audit, and Evidence Memory

可引用：

- VERAFI
- FinVet
- SkillGuard-Robust
- SkillProbe
- Semia
- OpenAI Skills
- Anthropic Agent Skills
- Karpathy LLM Wiki

重点写：

> Skill-based auditing and agent-compiled memory are emerging paradigms, but have not been systematically adapted to evidence leakage auditing in financial forecasting.

---

## 13. 建议重点对比矩阵

| Paper | Stock Forecasting | Agentic RAG | Temporal Safety | Evidence Audit | Verifier Revision | Leakage Metric | Skill/Evidence Wiki | Trading Metrics |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| CARAG | ✓ | ✓ | ✓ | partial | ✗ | ✗ | ✗ | ✓ |
| Profit Mirage | ✓ | partial | ✓ | ✗ | ✗ | ✓ | ✗ | ✓ |
| TRACE | ✓ | partial | ✓ | partial | ✗ | ✗ | ✗ | ✓ |
| FinAgent-RAG | ✗ | ✓ | partial | partial | ✓ | ✗ | ✗ | ✗ |
| VERAFI | ✗ | ✓ | partial | partial | policy-guided | ✗ | ✗ | ✗ |
| FinVet | ✗ | partial | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| SkillGuard-Robust | ✗ | ✗ | ✗ | skill security | ✗ | ✗ | skill audit | ✗ |
| Semia | ✗ | ✗ | ✗ | skill security | ✗ | ✗ | skill audit | ✗ |
| **Ours: FinLeakAudit** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## 14. 最终建议写法

### 不要写

```text
We propose a new Agentic RAG framework for stock prediction.
```

因为 CARAG 已经非常接近。

### 应该写

```text
We propose FinLeakAudit, a skill-based evidence leakage auditing framework for Agentic RAG financial forecasting.
Unlike prior work that focuses on improving forecast accuracy, FinLeakAudit audits retrieved evidence at the point-in-time level, detects future-evidence leakage and unsupported rationales, and performs verifier-guided forecast revision.
```

中文：

```text
本文提出 FinLeakAudit，一个面向 Agentic RAG 金融预测的技能化证据泄漏审计框架。
不同于已有工作主要关注提升预测准确率，FinLeakAudit 从 point-in-time 证据层面对检索证据进行审计，检测未来证据泄漏与不受支持的预测理由，并通过 verifier-guided revision 对预测结果进行修正。
```

---

## 15. 最优论文标题候选

### 标题 1：最稳

```text
FinLeakAudit: Skill-Based Evidence Leakage Auditing for Agentic RAG Financial Forecasting
```

### 标题 2：更有冲击力

```text
When Agentic RAG Forecasts Markets: Evidence Leakage, Forecast Inflation, and Verifier-Guided Correction
```

### 标题 3：更技术化

```text
Point-in-Time Evidence Memory and Skill-Based Auditing for Leakage-Aware Financial Forecasting
```

### 标题 4：更像 evaluation paper

```text
Auditing Evidence Leakage in Agentic RAG for Financial Forecasting
```

---

## 16. 下一步让 agent 做什么

建议给 agent 的任务：

```text
请基于本文档中的论文清单，构建一个 Zotero/BibTeX 候选引用库。
每篇论文输出：
1. 标题
2. 作者
3. 年份
4. venue / arXiv ID
5. 任务
6. 方法关键词
7. 与 FinLeakAudit 的关系
8. 应放入论文哪个 section
9. 是否必须精读
10. 是否适合作 baseline
11. 是否适合作 related work
12. 是否存在撞车风险
```

---

## 17. 最高优先级精读顺序

1. CARAG
2. Profit Mirage
3. TRACE
4. FinAgent-RAG
5. VERAFI
6. FinVet
7. Enhancing Financial RAG with Agentic AI and Multi-HyDE
8. MarketSenseAI 2.0
9. SEP, WWW 2024
10. Data-Axis Transformer, KDD 2021
11. Deep Attentive Learning, EMNLP 2020
12. FinBen
13. SkillGuard-Robust / SkillProbe / Semia
14. The New Quant
15. Agentic RAG Survey

---

## 18. 最终一句话定位

> 当前已有工作分别解决了 Agentic RAG 金融预测、LLM 金融智能体泄漏、时间图谱证据链、金融 QA 自验证和 skill 安全审计。  
> 但尚缺少一个针对 Agentic RAG 金融预测 pipeline 的 **point-in-time evidence memory + skill-based evidence leakage audit + verifier-guided forecast revision** 框架。  
> 这正是 FinLeakAudit 的目标。
