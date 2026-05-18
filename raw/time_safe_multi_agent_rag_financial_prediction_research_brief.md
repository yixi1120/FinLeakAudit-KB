# 金融预测方向：Time-Safe Verified Multi-Agent RAG 研究方案与查重/撞车调研任务书

> 用途：给 Hermes Agent 或其他文献调研 Agent 使用。  
> 目标：围绕 **Agentic RAG + 多智能体系统 + 金融时间序列预测/股票涨跌方向预测** 这一 topic，系统遍历同领域论文，判断现有研究进度，并检查是否与我们的创新点发生重叠或“撞车”。

---

## 1. 拟研究方向

### 1.1 英文题目候选

**Time-Safe Verified Multi-Agent RAG for Stock Movement Prediction**

也可以扩展为：

**Evidence-Grounded Agentic RAG for Financial Time-Series Forecasting**

或：

**Reducing Temporal Leakage and Hallucination in LLM-based Financial Forecasting via Multi-Agent RAG**

### 1.2 中文题目候选

**面向股票涨跌方向预测的时间安全验证型多智能体 RAG 框架**

或：

**面向金融时间序列预测的证据增强型 Agentic RAG 框架**

---

## 2. 研究问题定位

本研究不直接宣称“LLM 能炒股”，而是研究：

> 如何让 Agentic RAG 在金融预测任务中做到时间安全、证据可靠、多源融合、结果可解释。

具体关注金融预测中的四类核心问题：

1. **时间泄漏 Temporal Leakage**  
   金融预测中，模型可能无意使用预测日期之后的新闻、财报、市场数据或修订数据，导致回测结果虚高。

2. **证据不足 Evidence Insufficiency**  
   LLM 可能给出预测理由，但理由未被真实检索证据支持，属于“看似解释，实际无依据”。

3. **幻觉 Hallucination**  
   LLM 可能编造不存在的新闻、财报事件、政策变化或公司行为。

4. **多源信息融合不稳定 Multi-source Fusion Instability**  
   历史价格、技术指标、新闻事件、财报基本面、市场指数和宏观信息之间存在时间粒度、噪声水平和信息可靠性的差异。

---

## 3. 推荐任务定义

### 3.1 主任务

**未来 5 个交易日股票涨跌方向预测**

给定某只股票在预测日期 `t` 之前可获得的信息，预测未来 5 个交易日的收益方向。

### 3.2 输入

- 股票代码 ticker
- 预测日期 prediction date
- 过去 N 天 OHLCV 价格数据
- 截止预测日期之前发布的新闻
- 截止预测日期之前发布的财报、公告、公司事件
- 可选：市场指数、行业指数、宏观变量

### 3.3 输出

建议输出为结构化 JSON：

```json
{
  "ticker": "AAPL",
  "prediction_date": "2024-06-01",
  "horizon": "5 trading days",
  "prediction": "Up / Down / Neutral",
  "confidence": 0.0,
  "numerical_signal": "...",
  "event_signal": "...",
  "fundamental_signal": "...",
  "risk_factors": ["...", "..."],
  "evidence_ids": ["news_001", "filing_003"],
  "verification_result": {
    "temporal_safe": true,
    "evidence_supported": true,
    "numeric_checked": true,
    "hallucination_detected": false
  }
}
```

---

## 4. 标签定义建议

### 4.1 三分类标签

定义未来 5 日收益率：

```text
r_{t,5} = (Close_{t+5} - Close_t) / Close_t
```

标签规则：

```text
如果 r_{t,5} > 1%，标签 = Up
如果 r_{t,5} < -1%，标签 = Down
否则标签 = Neutral
```

### 4.2 二分类标签

如果样本量较小，也可以使用二分类：

```text
如果 r_{t,5} > 0，标签 = Up
否则标签 = Down
```

### 4.3 超额收益标签

更金融化的设定：

```text
excess_return = stock_return - market_return
```

预测：

```text
Outperform / Underperform
```

---

## 5. 拟提出系统：FinPredict-AgentRAG

### 5.1 总体流程

```text
用户输入：股票代码 + 预测日期 + 预测窗口
        ↓
Task Router Agent
        ↓
Temporal Retrieval Agent
        ↓
Numerical Analyst Agent
        ↓
News/Event Analyst Agent
        ↓
Fundamental Analyst Agent
        ↓
Prediction Agent
        ↓
Verifier Agent
        ↓
输出：涨跌方向 + 置信度 + 证据链 + 风险说明
```

---

## 6. Agent 设计

### 6.1 Task Router Agent

负责判断当前预测任务需要哪些信息源和分析模块。

示例路由规则：

| 任务类型 | 优先调用模块 |
|---|---|
| 短期方向预测 | Numerical Agent + News/Event Agent |
| 财报后走势预测 | Fundamental Agent + News/Event Agent |
| 行业冲击预测 | News/Event Agent + Market Context |
| 风险预警 | Numerical Agent + Risk/Verifier Agent |
| 简单事实查询 | Retrieval Agent only |

作用：

- 减少不必要的 LLM 调用
- 降低成本和延迟
- 根据任务复杂度动态选择推理路径

---

### 6.2 Temporal Retrieval Agent

这是第一个核心创新模块。

普通 RAG 只关注相关性：

```text
retrieve documents with high relevance
```

本研究的 Time-Safe RAG 同时关注相关性和时间约束：

```text
retrieve documents with high relevance and publish_time <= prediction_time
```

每条检索证据必须保留：

```text
document_id
source
publish_time
ticker
document_type
retrieval_score
available_at_time
```

目标：

- 降低金融预测中的未来信息泄漏
- 让所有预测证据都可追溯
- 支持后续 Verifier Agent 审查

---

### 6.3 Numerical Analyst Agent

负责处理历史价格和技术指标。

建议由 Python 或固定函数计算，而不是让 LLM 自己计算。

输出示例：

```text
过去 5 日收益率：+2.1%
过去 20 日收益率：-3.4%
波动率：上升
成交量：高于 20 日均值
RSI：偏高
MACD：金叉
趋势：短期反弹，中期仍偏弱
```

可计算特征：

- 过去 5/10/20 日收益率
- 成交量变化
- 移动平均线
- RSI
- MACD
- 波动率
- 最大回撤
- 与市场指数的相对表现

---

### 6.4 News/Event Analyst Agent

负责把新闻、公告、社媒或研报摘要转换为结构化事件信号。

输出示例：

```text
事件类型：财报超预期 / 监管风险 / 产品发布 / 管理层变动 / 宏观冲击
情绪方向：正面 / 中性 / 负面
影响范围：公司 / 行业 / 市场
时间：YYYY-MM-DD
证据：新闻标题或文档片段
可信度：高 / 中 / 低
```

作用：

- 将非结构化金融文本转化为可用于预测的事件证据
- 为 Prediction Agent 提供 grounded evidence
- 为 Verifier Agent 提供可检查的证据链

---

### 6.5 Fundamental Analyst Agent

负责处理财报、基本面指标和公司长期信息。

不一定每个样本都调用，适合在以下情况调用：

- 财报发布窗口附近
- 预测窗口较长
- 重大基本面变化
- 公司公告较多

输出示例：

```text
营收增长：改善 / 恶化
利润率：改善 / 恶化
现金流：健康 / 紧张
债务压力：高 / 中 / 低
管理层展望：积极 / 谨慎 / 悲观
```

---

### 6.6 Prediction Agent

基于 Numerical Agent、News/Event Agent、Fundamental Agent 的结构化输出做最终预测。

输出要求：

- 预测方向：Up / Down / Neutral
- 置信度：0 到 1
- 主要证据
- 反向风险
- 不确定性说明
- 引用的 evidence IDs

该 Agent 不能直接凭感觉输出，必须依赖上游证据。

---

### 6.7 Verifier Agent

这是第二个核心创新模块。

检查项：

| 检查项 | 说明 |
|---|---|
| 时间安全 | 是否使用了预测日期之后的信息 |
| 证据支持 | 预测理由是否被检索证据支持 |
| 数值正确性 | 收益率、技术指标、标签是否算错 |
| 逻辑一致性 | 是否存在证据与结论明显冲突 |
| 幻觉检测 | 是否编造不存在的事件或文档 |
| 置信度合理性 | 是否过度自信 |
| 反向证据 | 是否忽略了明显相反的信息 |

Verifier Agent 可以要求 Prediction Agent 修正结果。

示例：

```text
第一次预测：Up
Verifier：证据不足，且主要新闻为负面，请降低置信度或改为 Neutral。
最终预测：Neutral，confidence = 0.51
```

---

## 7. 本研究拟定创新点

Hermes Agent 在调研同 topic 论文时，需要重点检查以下创新点是否已经被提出、是否只是部分相似、是否完全撞车。

### 创新点 1：Temporal-Constrained RAG for Financial Forecasting

核心：

```text
publish_time(d) <= prediction_time(t)
```

要求所有检索证据必须在预测时点之前已经公开可得。

需要检查：

- 是否已有论文明确提出 time-safe RAG / time-aware RAG / temporal-constrained retrieval 用于股票预测？
- 是否已有论文把时间约束作为主要创新，而不是简单实验设置？
- 是否已有论文检测或量化 temporal leakage rate？
- 是否已有论文在 Agentic RAG 中引入时间安全审查模块？

撞车风险等级判断：

| 情况 | 风险 |
|---|---|
| 只是按时间划分训练测试集 | 低 |
| RAG 检索时加入时间过滤 | 中 |
| 明确提出 Time-Safe/Temporal-Constrained RAG 并用于金融预测 | 高 |
| 同时有时间过滤、Verifier、股票预测、证据链 | 极高 |

---

### 创新点 2：Multi-Agent Evidence Fusion

核心：

不同 Agent 分别处理：

```text
Numerical Evidence
News/Event Evidence
Fundamental Evidence
Market Context Evidence
```

再由 Prediction Agent 融合。

需要检查：

- 是否已有金融预测论文使用多智能体分工分析价格、新闻、财报、宏观信息？
- 是否已有论文把这些 evidence 显式结构化？
- 是否已有论文做了多源证据融合并输出可解释预测？
- 是否已有论文比较 single-agent 和 multi-agent 的预测效果？

撞车风险等级判断：

| 情况 | 风险 |
|---|---|
| 只做多 Agent 金融问答 | 低到中 |
| 多 Agent 做投资分析但不做严格预测评估 | 中 |
| 多 Agent 做股票预测并融合新闻/价格/财报 | 高 |
| 和我们的 Agent 分工高度一致 | 极高 |

---

### 创新点 3：Verifier-Guided Prediction Revision

核心：

Verifier Agent 检查：

```text
时间安全
证据支持
数值正确性
逻辑一致性
幻觉
置信度合理性
```

并可以让 Prediction Agent 修改预测。

需要检查：

- 是否已有金融预测 Agent 系统包含 Critic/Verifier/Reviewer Agent？
- 是否该 Verifier 只检查语言质量，还是检查时间泄漏、证据一致性和数值计算？
- 是否有自校验—修正循环？
- 是否有量化 hallucination rate / evidence support rate / numeric correctness？

撞车风险等级判断：

| 情况 | 风险 |
|---|---|
| 只有普通 reviewer agent | 中 |
| reviewer 检查证据一致性 | 中高 |
| verifier 检查金融预测中的时间泄漏和证据支持 | 高 |
| verifier 还能修正预测并报告多维可靠性指标 | 极高 |

---

### 创新点 4：综合评估框架

本研究计划同时报告三类指标：

1. 预测指标
2. 金融交易指标
3. Agent/RAG 可靠性指标

需要检查是否已有同领域论文使用类似综合评估。

#### 预测指标

```text
Accuracy
Macro-F1
AUC
MCC
```

#### 金融指标

```text
Long-short return
Sharpe ratio
Max drawdown
Win rate
Turnover
Transaction-cost-adjusted return
```

#### RAG / Agent 指标

```text
Retrieval Recall@k
Evidence Support Rate
Hallucination Rate
Temporal Leakage Rate
Average Cost
Average Latency
```

撞车风险等级判断：

| 情况 | 风险 |
|---|---|
| 只报告 Accuracy/F1 | 低 |
| 报告收益和 Sharpe | 中 |
| 同时报告预测、收益、幻觉、证据支持 | 高 |
| 还加入 Temporal Leakage Rate 和成本延迟分析 | 极高 |

---

## 8. Baseline 设计

Hermes Agent 需要检查相关论文中使用了哪些 baseline，并判断我们是否需要加入。

建议 baseline：

| Baseline | 说明 |
|---|---|
| Price-only ML | Logistic Regression / XGBoost / Random Forest |
| Technical indicators only | 只用技术指标 |
| LSTM / GRU | 常规深度时序模型 |
| Transformer / PatchTST | 时序 Transformer 基线 |
| LLM-only | 不检索，直接给历史信息让 LLM 判断 |
| Standard RAG | 检索新闻，但不做时间安全过滤 |
| Single-Agent RAG | 一个 Agent 同时做检索、分析、预测 |
| Multi-Agent RAG | 多 Agent，但没有 Verifier |
| Ours | Time-Safe + Multi-Agent + Verifier |

需要调研：

- 该领域论文常用哪些 baseline？
- 是否必须加入 FinBERT / FinGPT / BloombergGPT？
- 是否已有论文用 GPT-4 / LLaMA / Mistral 作为预测 Agent？
- 是否已有论文把 XGBoost、LSTM、PatchTST 和 Agentic RAG 一起比较？

---

## 9. 数据集与数据源建议

### 9.1 股票范围

推荐初始版本：

```text
S&P 100 或 Nasdaq 100 中的 20–50 只股票
```

原因：

- 新闻丰富
- 财报规范
- 流动性强
- 更容易复现
- 回测更容易解释

### 9.2 时间范围

推荐：

```text
2020–2024 或 2021–2024
```

最好覆盖：

- 牛市
- 熊市
- 震荡市
- 高波动时期

### 9.3 数据类型

| 数据 | 用途 |
|---|---|
| OHLCV 价格数据 | 构造技术指标和涨跌标签 |
| 公司新闻 | 文本事件分析 |
| 财报 / 10-K / 10-Q / 8-K | 基本面分析 |
| 市场指数 | 判断是否跑赢市场 |
| 行业分类 | 行业背景与相对表现 |
| 宏观事件 | 可选，不建议第一版做太大 |

### 9.4 需要调研的公开数据集

Hermes Agent 需要搜索这些关键词：

```text
stock movement prediction dataset news price
financial news stock prediction dataset
stock price movement prediction with news dataset
FinQA ConvFinQA TAT-QA financial reasoning
StockNet dataset
ACL18 stock movement prediction dataset
BigData22 financial news dataset
EDGAR SEC filings stock prediction dataset
```

---

## 10. 实验设计

### 10.1 主实验

目标：证明本方法优于 baseline。

示例表格：

| Method | Accuracy | Macro-F1 | Sharpe | Max Drawdown | Leakage Rate | Hallucination Rate |
|---|---:|---:|---:|---:|---:|---:|
| Price-only XGBoost |  |  |  |  | - | - |
| LLM-only |  |  |  |  |  |  |
| Standard RAG |  |  |  |  |  |  |
| Single-Agent RAG |  |  |  |  |  |  |
| Ours |  |  |  |  |  |  |

---

### 10.2 消融实验

| Version | 去掉什么 | 预期影响 |
|---|---|---|
| Full Model | 完整系统 | 最优综合表现 |
| w/o Temporal Filter | 去掉时间安全过滤 | 表面准确率可能上升，但泄漏率上升 |
| w/o News Agent | 不用新闻事件 | 事件驱动样本表现下降 |
| w/o Fundamental Agent | 不用财报基本面 | 财报期样本表现下降 |
| w/o Verifier | 不做验证修正 | 幻觉率和证据不一致率上升 |
| w/o Router | 固定调用所有 Agent | 成本和延迟上升 |

---

### 10.3 Case Study

建议展示以下类型案例：

```text
Case 1：财报超预期 + 成交量放大 → 预测 Up
Case 2：负面监管新闻 + 技术破位 → 预测 Down
Case 3：新闻正面但市场整体下跌 → 预测失败
Case 4：Verifier 发现检索到未来新闻 → 删除证据并修正预测
Case 5：多源证据冲突 → 降低置信度并输出 Neutral
```

---

## 11. Hermes Agent 文献调研任务

请 Hermes Agent 围绕以下目标进行系统调研。

### 11.1 调研目标

1. 遍历 2024–2026 年关于 **Agentic RAG / Multi-Agent / LLM Agent / Financial Forecasting / Stock Movement Prediction / Financial Time-Series Forecasting** 的论文。
2. 找出与本研究最接近的论文。
3. 判断现有论文是否已经提出：
   - Time-Safe RAG
   - Temporal-Constrained Retrieval
   - Multi-Agent Evidence Fusion
   - Verifier-Guided Prediction Revision
   - Temporal Leakage Rate
   - Hallucination Rate for financial forecasting
   - Evidence Support Rate for prediction explanation
4. 判断我们的创新点是否发生撞车。
5. 给出修改建议：如果撞车，应该如何调整创新点。

---

### 11.2 推荐检索关键词

#### 核心查询

```text
"Agentic RAG" "financial forecasting"
"multi-agent" "stock movement prediction" "LLM"
"retrieval augmented generation" "stock prediction"
"LLM agent" "financial time series forecasting"
"financial forecasting" "temporal leakage" "RAG"
"time-aware retrieval" "financial prediction"
"time-safe RAG" "stock prediction"
"verified RAG" "financial forecasting"
"evidence-grounded" "stock movement prediction"
"hallucination" "financial forecasting" "LLM agent"
```

#### 扩展查询

```text
"FinAgent-RAG"
"MarketSenseAI 2.0"
"The New Quant" "financial prediction" "trading"
"Agentic Retrieval-Augmented Generation for Time Series Analysis"
"Agentic RAG for financial document question answering"
"Multi-HyDE" "financial RAG"
"role-aware multi-agent" "financial"
"stock prediction" "news" "large language model"
"LLM-based trading agent"
"financial agent benchmark"
"RAG" "temporal reasoning" "time series"
```

---

### 11.3 重点检索平台

优先级：

1. arXiv
2. Google Scholar
3. Semantic Scholar
4. ACL Anthology
5. NeurIPS / ICLR / ICML / AAAI / IJCAI / KDD / WWW / SIGIR / EMNLP
6. SSRN，若金融工作论文较多可以补充

---

## 12. 文献提取表格模板

Hermes Agent 对每篇论文请填写以下字段。

| 字段 | 内容 |
|---|---|
| Paper Title | 论文标题 |
| Year | 年份 |
| Venue / arXiv | 发表地点或 arXiv |
| Task | 股票预测 / 金融问答 / 投资分析 / 时间序列预测 |
| Data | 价格 / 新闻 / 财报 / 社媒 / 宏观 / 多模态 |
| Method | RAG / Agentic RAG / Multi-Agent / Tool-use / GraphRAG |
| Agent Roles | 是否有多智能体分工，角色是什么 |
| Time Constraint | 是否有时间安全检索或时间过滤 |
| Leakage Control | 是否检测或讨论时间泄漏 |
| Verifier / Critic | 是否有验证、评审、自校验模块 |
| Evidence Grounding | 是否输出证据链 |
| Hallucination Evaluation | 是否量化幻觉 |
| Metrics | Accuracy / F1 / Sharpe / MDD / Recall@k / Cost / Latency |
| Baselines | 使用了哪些 baseline |
| Main Findings | 核心结果 |
| Similarity to Our Idea | 低 / 中 / 高 / 极高 |
| Collision Risk | 低 / 中 / 高 / 极高 |
| Notes | 备注 |

---

## 13. 撞车判断标准

### 13.1 极高撞车风险

满足以下多数条件：

- 也是股票涨跌方向预测
- 也是 Agentic RAG / 多智能体架构
- 有时间安全检索或时间约束 RAG
- 有 Verifier / Critic Agent 检查证据和时间泄漏
- 有预测指标 + 金融指标 + 幻觉/证据指标
- 方法结构与本方案高度类似

### 13.2 高撞车风险

满足以下部分条件：

- 做金融预测或投资决策
- 使用多智能体 + RAG
- 有新闻/财报/价格多源融合
- 有证据链或自校验
- 但没有完整时间安全评估

### 13.3 中等撞车风险

满足以下条件：

- 做金融问答或金融分析，不是预测
- 使用 Agentic RAG
- 有 verifier 或 critic
- 与本研究有模块相似，但任务不同

### 13.4 低撞车风险

满足以下条件：

- 只是普通 LLM 金融预测
- 只是普通 RAG 金融问答
- 只是多智能体金融助手 demo
- 没有时间安全、证据验证或预测评估

---

## 14. 如果发生撞车，可能的调整方向

### 14.1 如果 Time-Safe RAG 已有人做

调整为：

**Temporal Leakage Quantification and Mitigation in Agentic Financial Forecasting**

强调：

- 提出 temporal leakage rate 指标
- 系统性比较不同 RAG 结构的泄漏风险
- 做泄漏敏感性分析

---

### 14.2 如果 Multi-Agent Financial Forecasting 已有人做

调整为：

**Verifier-Guided Evidence Calibration for LLM-based Stock Forecasting**

强调：

- 不是多 Agent 本身
- 而是证据校准、置信度修正、幻觉降低

---

### 14.3 如果 Verifier Agent 已有人做

调整为：

**Cost-Aware Routing for Time-Safe Financial Agentic RAG**

强调：

- 动态路由
- 成本控制
- 简单任务不用复杂 Agent
- 复杂任务才调用多源检索与验证

---

### 14.4 如果 Agentic RAG + 股票预测整体已高度撞车

调整为 benchmark paper：

**A Benchmark Study of Agentic RAG Architectures for Financial Forecasting**

强调：

- 系统比较
- 统一评估
- 时间安全
- 成本、延迟、幻觉、证据支持
- 形成 benchmark 和评估协议

---

## 15. 最小可行论文版本

### 15.1 最小版本

```text
任务：未来 5 日股票方向预测
市场：美股
股票：20–50 只大盘股
数据：价格 + 新闻
模型：XGBoost + LLM-only + Standard RAG + Single-Agent RAG + Ours
创新：Temporal Filter + Verifier Agent
指标：Accuracy + Macro-F1 + Leakage Rate + Hallucination Rate + Cost/Latency
```

### 15.2 完整版本

```text
任务：未来 5 日股票方向预测 + 超额收益预测
市场：美股
股票：S&P 100 / Nasdaq 100
数据：价格 + 新闻 + 财报 + 市场指数
模型：传统 ML + 时序模型 + LLM/RAG/Agent baselines
创新：Temporal RAG + Multi-Agent Evidence Fusion + Verifier-Guided Revision
指标：预测指标 + 金融指标 + RAG/Agent 可靠性指标
```

---

## 16. 预期论文贡献写法

英文版：

```text
Our contributions are threefold:

1. We propose a time-safe multi-agent RAG framework for financial time-series forecasting, where all retrieved evidence is constrained by the prediction timestamp to reduce temporal leakage.

2. We design a multi-agent evidence fusion mechanism that combines numerical signals, textual events, and fundamental information for stock movement prediction.

3. We introduce a verifier-guided revision module to check evidence consistency, numerical correctness, and hallucination, and evaluate the framework using both prediction metrics and financial/RAG-specific reliability metrics.
```

中文版：

```text
本文贡献如下：

1. 提出一种面向金融时间序列预测的时间安全多智能体 RAG 框架，通过预测时间戳约束所有检索证据，以降低未来信息泄漏风险。

2. 设计多智能体证据融合机制，分别建模数值信号、新闻事件和基本面信息，并用于股票涨跌方向预测。

3. 引入验证驱动的预测修正模块，对证据一致性、数值正确性和幻觉风险进行检查，并结合预测指标、金融指标和 RAG/Agent 可靠性指标进行综合评估。
```

---

## 17. 当前最需要 Hermes Agent 输出的结果

请 Hermes Agent 最终给出以下内容：

1. **Top 20 最相关论文列表**
2. **每篇论文的任务、方法、数据、指标、结论**
3. **与本研究的相似度评分**
4. **每个创新点的撞车风险**
5. **最接近的 3–5 篇论文深度分析**
6. **我们的创新点是否需要修改**
7. **建议的最终论文题目和贡献点表述**
8. **推荐必须加入的 baseline 和数据集**
9. **潜在审稿风险**
10. **下一步实验实施建议**

---

## 18. 给 Hermes Agent 的最终执行指令

```text
请围绕“Time-Safe Verified Multi-Agent RAG for Stock Movement Prediction”这一研究主题，系统检索 2024–2026 年 Agentic RAG、多智能体金融预测、LLM-based stock movement prediction、financial time-series forecasting、financial RAG、verified RAG、temporal leakage 相关论文。

请重点判断现有工作是否已经覆盖以下创新点：
1. Temporal-Constrained / Time-Safe RAG for financial forecasting
2. Multi-Agent Evidence Fusion for stock movement prediction
3. Verifier-Guided Prediction Revision
4. Temporal Leakage Rate / Evidence Support Rate / Hallucination Rate 综合评估
5. 预测指标 + 金融收益指标 + RAG/Agent 可靠性指标的统一评估

请输出：
- 相关论文清单
- 论文方法总结
- 与本研究的相似度
- 撞车风险等级
- 最接近论文分析
- 需要避开的已有创新
- 我们可以保留或强化的创新点
- 推荐最终研究定位
```
