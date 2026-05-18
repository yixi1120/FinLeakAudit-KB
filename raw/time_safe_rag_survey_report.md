# Time-Safe Verified Multi-Agent RAG for Stock Movement Prediction
# 文献调研与撞车风险分析报告

> 生成日期：2026-05-15（更新于同日：新增后台脚本检索到的关键论文）  
> 调研范围：arXiv 2024–2026 + 已有 Related Work 文件 + 后台 arxiv_search.py 结果  
> 检索论文总数：~70 篇，深度分析 30 篇核心论文  
> ⚠️ **重点关注**：VERAFI、FinVet 为后台脚本新发现的高撞车风险论文

---

## 1. Top 20 最相关论文列表

| # | 论文 | 年份 | arXiv ID | 任务 | 方法 | 与本研究相似度 | 撞车风险 |
|---|------|------|----------|------|------|:---:|:---:|
| 1 | **🔴 VERAFI: Verified Agentic Financial Intelligence** | 2025 | 2512.14744 | 金融验证 | **Neurosymbolic 验证 + RAG + 工具 Agent** | **极高** | **极高** |
| 2 | **🔴 FinVet: RAG + External Fact-Checking Agents for Financial Misinformation** | 2025 | 2510.11654 | 金融验证 | 多Agent + 双重RAG + 事实核查投票 | **极高** | **极高** |
| 3 | The New Quant: A Survey of LLMs in Financial Prediction and Trading | 2025 | 2510.05533 | 金融预测综述 | Agentic RAG + 时间安全 + 幻觉 | 高 | 中 |
| 4 | MarketSenseAI 2.0: Enhancing Stock Analysis through LLM Agents | 2025 | 2502.00415 | 股票分析 | 多Agent + RAG融合基本面/技术/新闻/宏观 | **极高** | **高** |
| 3 | TRACE: Temporal Rule-Anchored Chain-of-Evidence for Stock Prediction | 2026 | 2603.12500 | 股票涨跌预测 | 时间规则 + 证据链 + KG + LLM | **极高** | **高** |
| 4 | History Rhymes: Macro-Contextual Retrieval for Financial Forecasting | 2025 | 2511.09754 | 金融预测 | 检索增强 + 历史类比 + OOD稳健 | 高 | 中高 |
| 5 | All Leaks Count: Interpretable Temporal Contamination Detection in LLM Backtesting | 2026 | 2602.17234 | 回测验证 | 时间泄漏检测框架 | 高 | 中 |
| 6 | ExAnte: A Benchmark for Ex-Ante Inference in LLMs | 2025 | 2505.19533 | 事前推理 | 时间约束推理基准 | 高 | 中 |
| 7 | Chronologically Consistent LLMs (ChronoBERT) | 2025 | 2502.21206 | 时序一致性 | 时间限制训练 LLM | 中 | 低 |
| 8 | FinAgent-RAG: Agentic RAG for Financial Document QA | 2026 | 2605.05409 | 金融问答 | 迭代检索+自校验+PoT+路由 | 高 | **高** |
| 9 | Enhancing Financial RAG with Agentic AI and Multi-HyDE | 2025 | 2509.16369 | 金融RAG | Agentic RAG + 多视角检索 | 中 | 中 |
| 10 | Can Blindfolded LLMs Still Trade? | 2026 | 2603.17692 | 交易验证 | 记忆偏差检测 + 信号验证 | 高 | 中高 |
| 11 | Knowledge-Augmented LLM Agents for Explainable Financial Decision-Making | 2025 | 2512.09440 | 金融决策 | 外部知识检索 + 语义表示 | 中高 | 中 |
| 12 | ElliottAgents: Multi-Agent LLM for Stock Market Forecasting | 2025 | 2506.16813 | 股票预测 | 多Agent + RAG + Elliott波浪 | 高 | 中 |
| 13 | RETuning: Inference-Time Scaling for Stock Movement Prediction | 2025 | 2510.21604 | 股票涨跌 | LLM推理 + 三分类(up/hold/down) | 中高 | 中 |
| 14 | CausalStock: Causal Discovery for News-driven Stock Prediction | 2024 | 2411.06391 | 股票预测 | 因果发现 + 新闻 | 中 | 低 |
| 15 | Ploutos: Interpretable Stock Movement Prediction with Financial LLM | 2024 | 2403.00782 | 股票涨跌 | 文本数值融合 + 可解释 | 中 | 低 |
| 16 | STONK: Multimodal Financial Forecasting | 2025 | 2508.13327 | 股票涨跌 | 跨模态注意力 + 情绪嵌入 | 中 | 中 |
| 17 | Agentic RAG for Time Series Analysis | 2024 | 2408.14484 | 时序分析 | 分层多Agent + RAG + 提示池 | 中 | 低 |
| 18 | FAITH: Framework for Assessing Tabular Hallucinations in Finance | 2025 | 2508.05201 | 幻觉评估 | 表格幻觉检测框架 | 中 | 低 |
| 19 | Finance Agent Benchmark | 2025 | 2508.00828 | 评测基准 | Agent测评(9类任务537题) | 中 | 低 |
| 20 | Agentic RAG Survey | 2025 | 2501.09136 | 综述 | Agentic RAG分类法 | 低 | 低 |

---

## 2. 论文详细信息（按撞车风险排序）

### 🔴 极高/高撞车风险论文

#### 2.0 VERAFI: Verified Agentic Financial Intelligence (2512.14744) — 撞车风险：极高 ⚠️

- **任务**：金融 Agent 验证（GAAP 合规、计算验证）
- **方法**：Agentic RAG + Neurosymbolic 策略生成 + 工具 Agent + 验证
- **核心机制**：结合密集型检索 + 交叉编码重排 + 金融工具 Agent + 自动化推理策略（GAAP 合规、SEC 法规验证）
- **Agent 角色**：检索 Agent + 验证 Agent + 工具 Agent
- **时间约束**：❌ 摘要未提及
- **验证模块**：✅ Neurosymbolic policy generation — 在推理过程中自动检查 GAAP 合规和计算错误
- **数据**：金融文档（SEC filings 等）
- **与本研究相似点**：
  - ✅ RAG + Agent + Verification 三位一体
  - ✅ 金融领域
  - ✅ 验证计算正确性
  - ✅ 使用 "Verified Agentic Financial Intelligence" 命名（与 "Time-Safe Verified Multi-Agent RAG" 极为相似！）
- **与本研究差异**：
  - ❌ 可能不做股票涨跌预测（可能是 QA/合规验证）
  - ❌ 可能无时间安全过滤
  - ❌ 可能无多源证据融合
  - ❌ 可能无 Temporal Leakage Rate 量化
- **撞车分析**：⚠️⚠️⚠️ **这是迄今为止威胁最大的论文！** 论文名 "**Verified** Agentic Financial Intelligence" 与我们 "Time-Safe **Verified** Multi-Agent RAG" 高度重叠。需要尽快阅读全文确认差异点。

#### 2.0b FinVet: RAG + External Fact-Checking Agents (2510.11654) — 撞车风险：极高 ⚠️

- **任务**：金融虚假信息检测
- **方法**：双重 RAG 管道 + 外部事实核查 Agent + 置信度加权投票机制
- **核心机制**：自适应三层处理（根据检索置信度从直接元数据提取到混合推理）
- **Agent 角色**：2 个 RAG Agent + 事实核查 Agent + 投票机制
- **时间约束**：❌ 摘要未提及
- **验证模块**：✅ 外部事实核查 Agent + 置信度加权投票
- **与本研究相似点**：
  - ✅ Multi-Agent + RAG + Fact-Checking
  - ✅ 金融领域
  - ✅ 验证机制
  - ✅ 可追溯性（"transparency in decision-making, attribution to credible sources"）
- **与本研究差异**：
  - ❌ 任务是虚假信息检测而非股票预测
  - ❌ 可能无时间安全
  - ❌ 可能无多源证据融合（数值+新闻+基本面）
- **撞车分析**：⚠️⚠️ **Fact-Checking/Verifier Agent 概念已存在！** 虽然任务不同（虚假信息 vs 股票预测），但 Fact-Checking Agent 架构与我们的 Verifier Agent 高度相似。需要区分"检查信息真实性"vs"检查预测可靠性"。

#### 2.1 MarketSenseAI 2.0 (2502.00415) — 撞车风险：高

- **任务**：S&P 100/S&P 500 股票投资分析
- **方法**：多Agent + RAG，专门化 Agent 分别处理 SEC 文件、财报电话会、宏观报告，通过 RAG 检索外部知识
- **Agent 角色**：Fundamental Agent、Technical Agent、News Sentiment Agent、Macro Agent
- **时间约束**：❌ 无明显时间安全机制
- **验证模块**：❌ 无 Verifier
- **数据**：SEC filings + earnings calls + 宏观报告 + 价格数据
- **指标**：累计收益 125.9% vs 73.5% S&P 100（2023-2024 回测）
- **与本方案相似点**：
  - ✅ 多 Agent 分工分析多种信息源（基本面、技术、新闻、宏观）
  - ✅ 使用 RAG 检索增强
  - ✅ 面向股票投资决策
  - ✅ 有回测评估
- **与本方案差异**：
  - ❌ 不做严格的时间安全过滤
  - ❌ 无 Verifier Agent
  - ❌ 不检测/量化 temporal leakage rate
  - ❌ 不输出结构化证据链
  - ❌ 不评估幻觉率和证据支持率
- **撞车分析**：任务最接近，但核心创新点（Time-Safe + Verifier）不同

#### 2.2 TRACE (2603.12500) — 撞车风险：高

- **任务**：可解释的股票涨跌方向预测
- **方法**：Temporal Rule-Anchored Chain-of-Evidence on Knowledge Graphs + LLM
- **Agent 角色**：规则引导的多跳探索、证据链锚定、LLM引导决策
- **时间约束**：✅ 时间规则约束（admissible relation sequences）
- **验证模块**：隐式（通过证据链）
- **与本研究相似点**：
  - ✅ 股票涨跌预测任务
  - ✅ 时间约束
  - ✅ 证据链（Chain-of-Evidence）
  - ✅ 可解释性
- **与本研究差异**：
  - ❌ 基于知识图谱而非 RAG
  - ❌ 无多 Agent 架构
  - ❌ 无 Verifier Agent
  - ❌ 无幻觉检测和证据支持率
  - ❌ 不涉及多源融合（新闻+价格+基本面）
- **撞车分析**：是 2026 年 3 月最新论文，非常相关，但技术路线不同（KG vs RAG）

#### 2.3 FinAgent-RAG (2605.05409) — 撞车风险：高

- **任务**：金融文档问答（FinQA/ConvFinQA/TAT-QA）
- **方法**：(1) 对比金融检索器 + 难负样本挖掘，(2) Program-of-Thought 生成可执行 Python，(3) 自适应策略路由
- **Agent 角色**：检索 Agent + 推理 Agent + 路由 Agent
- **时间约束**：❌ 无（不是预测任务）
- **验证模块**：✅ 迭代自校验（self-verification）
- **数据**：FinQA, ConvFinQA, TAT-QA
- **指标**：Execution Accuracy 76.81%/78.46%/74.96%
- **与本研究相似点**：
  - ✅ Agentic RAG 框架
  - ✅ 自校验模块
  - ✅ 自适应路由
  - ✅ 金融领域
- **与本研究差异**：
  - ❌ 任务是 QA 而不是预测
  - ❌ 不做时间安全
  - ❌ 不做股票涨跌预测
  - ❌ 不做多源证据融合
- **撞车分析**：模块级相似（Routing + Verification），但任务和目标完全不同

---

### 🟡 中高撞车风险论文

#### 2.4 History Rhymes (2511.09754) — 撞车风险：中高

- **任务**：金融预测（OOD 场景下的稳健预测）
- **方法**：宏观上下文检索（macro-contextual retrieval），检索历史类比场景
- **核心创新**：检索增强用于金融时间序列预测
- **与本研究差异**：单 Agent、无时间安全过滤、无 Verifier
- **撞车分析**：检索用于金融预测的概念相似，但具体方案不同

#### 2.5 Can Blindfolded LLMs Still Trade? (2603.17692) — 撞车风险：中高

- **任务**：验证 LLM 交易 Agent 是否有记忆偏差
- **方法**：匿名化框架 + 信号验证
- **核心创新**：验证 Agent 是否真正理解市场而非记忆股票代码
- **与本研究相似点**：✅ 验证 Agent 决策可靠性
- **与本研究差异**：聚焦记忆偏差而非时间泄漏
- **撞车分析**：验证思路相似，但角度不同

---

## 3. 创新点撞车风险逐一评估

### 创新点 1：Temporal-Constrained RAG for Financial Forecasting

| 评估维度 | 结论 |
|---------|------|
| 是否已有论文明确提出 Time-Safe RAG 用于股票预测？ | ❌ 没有 |
| 是否已有论文把时间约束作为主要创新？ | ⚠️ TRACE 有时间规则，但不是 RAG；ExAnte/ChronoBERT/All Leaks Count 关注时间问题但无预测系统 |
| 是否已有论文检测/量化 Temporal Leakage Rate？ | ⚠️ All Leaks Count 提出泄漏检测框架，但不是金融 RAG |
| The New Quant 综述是否提到时间泄漏？ | ✅ 综述明确列为关键挑战 |
| **撞车风险** | **🟡 中高** — 时间泄漏是热点，但还没有人把 Time-Safe RAG + 金融预测 + 系统级实现做出来 |

**结论**：概念层面有竞争（时间泄漏正在成为关注焦点），但尚无完整系统。**需要尽快发表以抢占先机。**

---

### 创新点 2：Multi-Agent Evidence Fusion

| 评估维度 | 结论 |
|---------|------|
| 是否已有金融预测论文使用多 Agent 分工？ | ✅ MarketSenseAI 2.0、ElliottAgents、TradingGPT |
| 是否已有论文显式结构化 evidence？ | ⚠️ TRACE 有证据链；FinAgent-RAG 输出结构化结果 |
| 是否已有论文多源融合并输出可解释预测？ | ✅ MarketSenseAI 2.0 融合4种信号 |
| MarketSenseAI 2.0 的 Agent 分工是否跟我们高度一致？ | ⚠️ 有 Fundamental、Technical、News、Macro Agent，类似但不完全一样 |
| **撞车风险** | **🟡 中高** — Multi-Agent 金融预测已有人做，但 Evidence Fusion 视角不同 |

**调整建议**：不要强调"多 Agent"，而强调 **"结构化证据融合 + Evidence Schema + 可追溯证据 ID"**。市场现有方案是多 Agent 但不出结构化 evidence。

---

### 创新点 3：Verifier-Guided Prediction Revision

| 评估维度 | 结论 |
|---------|------|
| 是否已有金融 Agent 系统包含 Critic/Verifier？ | ✅ **是的 — VERAFI 和 FinVet！** |
| VERAFI 的验证范围？ | RAG + Neurosymbolic 验证（GAAP 合规、计算错误） |
| FinVet 的验证机制？ | 外部 Fact-Checking Agent + 置信度加权投票 |
| Verifier 检查时间泄漏？ | ❌ 现有方案都没有 |
| Verifier 检查证据一致性 + 数值正确性？ | ⚠️ VERAFI 检查计算正确性 |
| 是否有自校验—修正循环？ | ⚠️ FinAgent-RAG 有迭代自校验 |
| 是否量化 Temporal Leakage Rate？ | ❌ 都没有 |
| **撞车风险** | **🔴 中高→高** — VERAFI 和 FinVet 的出现将 Verifier Agent 的撞车风险从"中低"提升到"高" |

**⚠️ 重大调整**：之前认为 Verifier Agent 在金融预测中是个空白。但 VERAFI (2025年12月) 明确提出了"Verified Agentic Financial Intelligence"，FinVet 有外部 Fact-Checking Agent。需要紧急阅读这两篇全文，确认它们：
1. 是做 QA/合规验证还是预测验证？
2. 是否涵盖时间安全维度？
3. Verifier 是否参与预测修正？

**紧急差异化策略**：
- 如果它们做 QA/合规 → 我们强调 "Prediction-Specific Verification"
- 如果它们做预测 → 我们强调 "Temporal Safety + Multi-Dimensional Reliability"
- 无论如何加强 "Time-Safe" 这块的独特性

---

### 创新点 4：综合评估框架

| 评估维度 | 结论 |
|---------|------|
| 是否已有论文同时报告预测+金融+RAG可靠性指标？ | ❌ 没有 |
| The New Quant 是否呼吁此类评估？ | ✅ 综述明确建议 |
| 是否有人提出 Temporal Leakage Rate 指标？ | ❌ 没有 |
| **撞车风险** | **🟢 低** — 综合评估框架是明确空白 |

---

## 4. 最接近的 3 篇论文深度分析

### 🥇 MarketSenseAI 2.0 (2502.00415) — 最强竞品

**为什么是最大威胁**：
- 直接做美股预测（S&P 100 + S&P 500）
- 已有 Multi-Agent 架构（Fundamental / Technical / News / Macro）
- 已有 RAG 检索
- 已有两年回测（2023-2024）
- 累计收益显着优于指数（125.9% vs 73.5%）

**我们能差异化**：
1. 他们没有 **时间安全过滤**（可能使用了未来信息）
2. 他们没有 **Verifier Agent**（无法验证预测可靠性）
3. 他们没有 **Temporal Leakage Rate / Hallucination Rate / Evidence Support Rate** 指标
4. 他们没有 **结构化证据输出**（只是给了一个投资信号）

**策略**：在 Related Work 中承认 MarketSenseAI，然后指出其缺少时间安全和可靠性验证。

---

### 🥈 TRACE (2603.12500) — 方法论竞品

**为什么关注**：
- 同时涉及时间约束 + 证据链 + 股票预测
- 2026 年 3 月最新论文
- 可解释性定位

**我们能差异化**：
1. 基于 RAG 而非 Knowledge Graph（更灵活、可扩展）
2. 多 Agent 分工（数值/新闻/基本面分开处理）
3. 有 Verifier Agent
4. 有量化指标

**策略**：可作为 baseline 比较。展示 RAG 路线优于 KG 路线。

---

### 🥉 FinAgent-RAG (2605.05409) — 模块竞品

**为什么关注**：
- 自校验（self-verification）模块
- 路由（adaptive routing）模块
- 金融领域 Agentic RAG
- 2026 年 5 月最新

**我们能差异化**：
1. 任务是预测不是 QA
2. 时间安全是核心而非事后
3. Verifier 检查更全面（时间泄漏 + 证据支持 + 幻觉）

**策略**：承认其自校验和路由设计，说明我们扩展了这些概念到预测任务。

---

## 5. 创新点修改建议

### 当前创新点存在的主要问题

1. **Multi-Agent Evidence Fusion** 和 MarketSenseAI 2.0 高度重叠
2. **Time-Safe RAG** 概念并非完全独创（时间泄漏正成为热门话题）
3. 整体框架的 **selling point 不够尖锐**

### 建议调整后的创新点

```
创新点 1（主创新）：Time-Constrained Retrieval-Augmented Stock Forecasting
→ 不只过滤时间，而是：时间戳约束检索 + Temporal Leakage Rate 量化 + 泄漏敏感性分析
→ 与 MarketSenseAI 等竞品的核心区别：我们能证明他们可能用了未来信息

创新点 2（改）：Structured Evidence Schema for Financial Agent Predictions
→ 不强调 Multi-Agent，强调 Evidence 的结构化、可追溯、可验证
→ 每个 Agent 输出 Structured Evidence（JSON Schema）+ Evidence ID

创新点 3（保留并强化）：Verifier-Guided Prediction with Multi-Dimensional Reliability Report
→ 强化为多维可靠性报告：Temporal Safety / Evidence Support / Numerical Correctness / Hallucination / Confidence Calibration
→ 不只是"修正预测"，而是"生成可靠性报告"

创新点 4（保留）：Unified Evaluation Protocol for Financial Agentic RAG
→ 预测指标 + 金融交易指标 + RAG/Agent 可靠性指标的统一评估协议
```

---

## 6. 推荐最终论文题目

### 首选（已调整，避开 VERAFI 的 "Verified" 命名）：

**Time-Safe Agentic RAG for Evidence-Grounded Stock Movement Prediction**

### 备选（均避免 "Verified" 关键词）：

1. **Temporal-Constrained Multi-Agent RAG for Reliable Financial Forecasting**
2. **Evidence-Grounded Financial Prediction with Agentic RAG and Temporal Safety**
3. **Reducing Temporal Leakage and Hallucination in LLM-based Stock Forecasting**

### 推荐中文题目：

**面向股票涨跌预测的时间安全型多智能体证据增强 RAG 框架**

---

## 7. 推荐贡献点表述

```
1. We propose Time-Safe Agentic RAG, a financial forecasting framework
   that enforces temporal constraints on all retrieved evidence, and
   introduce the Temporal Leakage Rate metric to quantify future
   information contamination in financial predictions.

2. We design a multi-agent evidence schema where specialized agents
   produce structured, traceable evidence from numerical, textual,
   and fundamental sources, enabling evidence-grounded prediction.

3. We introduce a Reliability Auditor Agent that conducts multi-
   dimensional checks (temporal safety, evidence support, numerical
   correctness, hallucination) on financial predictions and can
   request revision when reliability thresholds are not met.

4. We establish a unified evaluation protocol combining prediction
   metrics, financial trading metrics, and RAG/Agent reliability
   metrics for comprehensive assessment of financial Agentic RAG.
```

---

## 8. Baseline 推荐

| 层级 | Baseline | 必要性 |
|------|----------|:---:|
| 传统 ML | XGBoost / Random Forest (只用价格特征) | ✅ 必须 |
| 传统 ML | XGBoost + 新闻情绪特征 | ✅ 必须 |
| 深度学习 | LSTM / GRU | ✅ 必须 |
| 时序 Transformer | PatchTST / TimesNet | ✅ 推荐 |
| 金融 LLM | FinBERT 情绪 + 价格 | ✅ 推荐 |
| LLM-only | GPT-4 直接预测（不检索） | ✅ 必须 |
| Standard RAG | 检索新闻但不做时间过滤 | ✅ 必须 |
| Single-Agent RAG | 单一 Agent 同时检索+分析+预测 | ✅ 必须 |
| Multi-Agent w/o Verifier | 多 Agent 但没有验证模块 | ✅ 必须 |
| MarketSenseAI-style | 参考 MarketSenseAI 2.0 的方法 | 推荐 |
| TRACE-style | 基于 KG 的时间约束方法 | 推荐 |

---

## 9. 数据集推荐

| 数据集 | 用途 | 说明 |
|--------|------|------|
| **StockNet** (ACL 2018) | 新闻驱动的股票涨跌预测 | 88只股票, ~140K tweets, 2年 |
| **FinBen/PIXIU** | 金融 LLM 基准 | 35+任务, 23+数据集 |
| **Yahoo Finance / Alpha Vantage** | OHLCV 价格数据 | 免费 API |
| **SEC EDGAR** | 10-K/10-Q/8-K 财报 | 公开数据 |
| **Financial PhraseBank** | 金融情绪分析 | 经典基准 |
| **FiQA** | 金融问答 | 可辅助评估 |
| 自建 | 2020-2024 S&P 100 数据 | 价格 + 新闻 + 财报 |

---

## 10. 潜在审稿风险

| 风险 | 说明 | 应对策略 |
|------|------|---------|
| **"MarketSenseAI already did this"** | Multi-Agent + RAG + 股票分析 | 强调 Time-Safe + Verifier + 可靠性指标三方面的独特性 |
| **"Temporal leakage is not new"** | 综述已提及时间泄漏 | 强调系统级实现 + 量化指标 + 与现有方案的对比 |
| **"Where is the trading simulation?"** | 只有预测没有交易模拟 | 加入简单的回测/Long-Short portfolio 评估 |
| **"LLM is just a wrapper"** | 被认为只是调用 GPT-4 | 强调 Agentic 编排、时间约束、证据验证的工程贡献 |
| **"Not enough stocks"** | 只测试 20-50 只股票 | MVP 阶段范围小但分析深，完整版扩展到 S&P 500 |
| **"Why not just use FinGPT/BloombergGPT?"** | 为什么不用现成金融 LLM | 我们的框架是模型无关的，可以把它们作为 backbone 之一 |

---

## 11. 下一步实验实施建议

### 第一阶段：MVP（2-3 周）

1. **数据准备**：选 10 只 S&P 100 股票，2023-2024 年数据
2. **实现 Temporal Retriever**：时间戳过滤的新闻检索
3. **实现 Numerical Agent**：Python 计算技术指标
4. **实现 Simple RAG Baseline**：不做时间过滤的对照
5. **跑通端到端 Pipeline**（Numerical Agent + News Agent → Prediction）
6. **计算 Temporal Leakage Rate**：对比有无时间过滤

### 第二阶段：完整系统（3-4 周）

7. **实现 News/Event Agent**：结构化事件抽取
8. **实现 Fundamental Agent**：财报分析
9. **实现 Prediction Agent**：证据融合
10. **实现 Verifier Agent**：多维检查
11. **实现 Task Router**：动态调用

### 第三阶段：评估与论文（3-4 周）

12. **跑完所有 Baseline 对比**
13. **消融实验**
14. **Case Study 撰写**
15. **论文写作**

---

## 12. 总结

### ⚠️ 重大更新（2026-05-15 第二轮检索）

**VERAFI (2512.14744) 和 FinVet (2510.11654) 的出现改变了局势：**

1. **Innovation 3 (Verifier Agent) 的撞车风险从"中低"升级为"高"** — VERAFI 明确提出了 "Verified Agentic Financial Intelligence"，FinVet 有 Fact-Checking Agent。虽然它们可能不是做股票预测，但 Verification 的叙事空间已被抢占。

2. **论文题目的冲突** — "Verified Agentic Financial Intelligence" 与 "Time-Safe Verified Multi-Agent RAG" 命名高度重叠。建议把 "Verified" 换成 "Evidence-Grounded" 或 "Time-Constrained" 来差异化。

3. **Time-Safe 成为最后的护城河** — 在所有四个创新点中，Time-Safe/Temporal-Constrained RAG 现在是唯一没有明显竞品的创新点。VERAFI 和 FinVet 都未提及时间安全。

### 核心结论

1. **四个创新点整体组合是新颖的** — 虽然每个子模块都有相邻工作，但没有一篇论文把 Time-Safe RAG + Multi-Agent Evidence Fusion + Verifier-Guided Revision + 综合评估放在一起做股票涨跌预测。

2. **最紧急的威胁** — MarketSenseAI 2.0 在任务和方法上最接近，TRACE 在时间约束+证据链上最相关。但两者都没有 Verifier 和时间泄漏量化。

3. **时间窗口** — "时间安全/时间泄漏"正在成为热点（2025-2026 年有多篇相关论文出现），需要尽快发表，否则 6-12 个月内可能被他人覆盖。

4. **建议调整** — 削弱"Multi-Agent"叙事，强化"Time-Safe + Evidence-Grounded + Verifier + Reliability Metrics"四合一。

5. **风险可控** — 即使某些子模块部分撞车，可以通过调整创新点表述（见第 5 节）来差异化。

---

*报告由 Hermes Agent 基于 arXiv 2024-2026 论文检索及已有 Related Work 文件综合分析生成。*
