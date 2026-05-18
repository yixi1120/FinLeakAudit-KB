# 第 1 层：宏观综述分析——用于时间序列与金融预测的 LLM（2024–2026）

**生成日期：** 2026-05-14  
**数据来源：** arXiv 检索（`Large Language Models Time Series Survey`、`LLM Financial Market Prediction Review`）  
**筛选条件：** 仅保留 2024–2026 年的 survey/review 论文  
**分析论文数：** 21

---

## 1. 论文清单

| # | 论文标题 | 作者 | 发表时间 | arXiv ID |
|---|---|---|---|---|
| 1 | FINRS: A Risk-Sensitive Trading Framework for Real Financial Markets | Bijia Liu, Ronghao Dang | 2025-11-16 | 2511.12599 |
| 2 | Frequency Matters: When Time Series Foundation Models Fail Under Spectral Shift | Tianze Wang et al. | 2025-11-06 | 2511.05619 |
| 3 | FinPos: A Position-Aware Trading Agent System for Real Financial Markets | Bijia Liu, Ronghao Dang | 2025-10-31 | 2510.27251 |
| 4 | Pre-trained Forecasting Models... for Time Series Classification | Andreas Auer et al. | 2025-10-30 | 2510.26777 |
| 5 | Towards Interpretable Time Series Foundation Models | Matthieu Boileau et al. | 2025-07-10 | 2507.07439 |
| 6 | Can LLM-based Financial Investing Strategies Outperform the Market in Long Run? | Weixian Waylon Li et al. | 2025-05-11 | 2505.07078 |
| 7 | Towards Cross-Modality Modeling for Time Series Analytics: A Survey in the LLM Era | Chenxi Liu et al. | 2025-05-05 | 2505.02583 |
| 8 | Foundation Models for Time Series: A Survey | Siva R. K. Kottapalli et al. | 2025-04-05 | 2504.04011 |
| 9 | Are LLMs Good In-context Learners for Financial Sentiment Analysis? | Xinyu Wei, Luojia Liu | 2025-03-06 | 2503.04873 |
| 10 | Financial Named Entity Recognition: How Far Can LLM Go? | Yi-Te Lu, Yintong Huo | 2025-01-04 | 2501.02237 |
| 11 | Large Language Models for Financial Aid in Financial Time-series Forecasting | Md Khairul Islam et al. | 2024-10-24 | 2410.19025 |
| 12 | TimeSeriesExam: A time series understanding exam | Yifu Cai et al. | 2024-10-18 | 2410.14752 |
| 13 | LLM-Mixer: Multiscale Mixing in LLMs for Time Series Forecasting | Md Kowsher et al. | 2024-10-15 | 2410.11674 |
| 14 | Time Series Analysis for Education... | Shengzhong Mao et al. | 2024-08-25 | 2408.13960 |
| 15 | Efficacy of Large Language Models in Systematic Reviews | Aaditya Shah et al. | 2024-08-03 | 2408.04646 |
| 16 | Large Language Model Agent in Financial Trading: A Survey | Han Ding et al. | 2024-07-26 | 2408.06361 |
| 17 | FinCon: A Synthesized LLM Multi-Agent System... | Yangyang Yu et al. | 2024-07-09 | 2407.06567 |
| 18 | Empowering Time Series Analysis with Foundation Models... | Jiexia Ye et al. | 2024-05-03 | 2405.02358 |
| 19 | Foundation Models for Time Series Analysis: A Tutorial and Survey | Yuxuan Liang et al. | 2024-03-21 | 2403.14735 |
| 20 | Exploring the Frontier of Vision-Language Models... | Akash Ghosh et al. | 2024-02-20 | 2404.07214 |
| 21 | Large Language Models for Time Series: A Survey | Xiyuan Zhang et al. | 2024-02-02 | 2402.01801 |

---

## 2. 主流研究分支（按关键词频次）

| 排名 | 研究分支 | 关键词得分 | 代表关键词 |
|---|---|---:|---|
| 1 | 时间序列预测 | 111 | forecasting, prediction, time series, temporal |
| 2 | 金融市场/交易 | 75 | financial, stock, trading, market |
| 3 | LLM 架构/微调 | 47 | fine-tuning, transformer, foundation model, prompt |
| 4 | 分类/回归 | 12 | classification, regression, imputation, embedding |
| 5 | 多模态/时空建模 | 12 | spatio-temporal, spatial, multi-modal, graph |

### 分支解读

#### 时间序列预测
这是当前核心应用方向。研究通常将 LLM 改造为通用预测器，并在标准基准上与统计模型和深度学习模型对比。关键问题是：LLM 是否能像建模语言依赖那样有效建模时间依赖。

#### 金融市场/交易
这是高价值且高复杂度场景。重点包括股价方向预测、组合优化、情绪驱动交易和加密资产分析。常见模型有 FinBERT、FinGPT、BloombergGPT 与指令微调 LLaMA。价格+新闻+基本面的数据融合是高频主题。

#### LLM 架构/微调
这是最主流分支。典型做法包括 LoRA/Adapter 微调、in-context/zero/few-shot 提示学习，以及将连续时间序列离散化为 token 的编码策略。该分支与其他方向高度重叠。

#### 分类/回归
覆盖异常检测、行为识别、缺失值填补、表征学习等任务。很多工作将 LLM 作为通用特征提取器，再接下游分类或回归模块。

#### 多模态/时空建模
这是新兴前沿方向。研究尝试将时间序列与空间信息（图、地理）以及文本、图像等模态统一建模。LLM 主要作为跨模态对齐与融合中枢。

---

## 3. 常见基线模型

| 模型 | 提及次数 | 类别 |
|---|---:|---|
| GPT | 7 | LLM |
| GPT-4 | 4 | LLM |
| Transformer | 3 | Transformer |
| LLaMA / Llama | 2 | LLM |

### 观察

- LLM 明显占据讨论中心：GPT 系列、LLaMA 及金融专用模型（FinBERT、FinGPT）是最常见骨干。
- 非 LLM 对照主要是 Informer、Autoformer、PatchTST 等 Transformer 时序模型。
- ARIMA、GARCH 这类统计模型仍常作为 sanity check，在金融场景里有时竞争力不弱。
- 金融专用 LLM 与通用时序模型，逐渐形成相对独立的比较生态。

---

## 4. 当前痛点与局限

| # | 痛点 | 关键词得分 |
|---|---|---:|
| 1 | 基准与评估体系缺失 | 10 |
| 2 | 泛化与鲁棒性不足 | 7 |
| 3 | 多模态融合困难 | 7 |
| 4 | 可解释性不足 | 3 |
| 5 | 合规与伦理问题 | 2 |
| 6 | 长上下文扩展压力 | 1 |
| 7 | 数据稀缺与质量问题 | 0 |

### 详细说明

#### 基准与评估
目前缺乏统一基准。数据集、指标、划分方式差异很大，跨论文公平比较困难。金融基准尤其分散（股票、加密、宏观常各自为政）。

#### 多模态融合
时间序列与新闻、报告、社媒文本，以及图像和结构化数据融合时，跨模态对齐容易引入噪声；简单后融合常不如专用单模态模型。

#### 可解释性
LLM 属黑箱模型。在金融等强监管场景中，决策不仅要“对”，还要“说得清为什么”。现有注意力可视化/探针方法仍不够。

#### 长上下文
金融高频时序跨度可能达数十年，超出上下文窗口。如何保留细节且建模长程依赖仍无统一优解。

#### 数据稀缺与质量
很多金融数据私有、噪声高、周期短。文本预训练 LLM 对时序模式先验不足，加上市场 regime shift（崩盘、政策变化）会破坏平稳性假设。

---

## 5. 综合结论

1. 2024–2026 年该方向进入显著增长阶段，综述数量本身说明领域正在成熟。  
2. 金融预测是最强应用驱动分支，产业牵引明显（对冲基金、银行、金融科技）。  
3. 可解释性、成本与幻觉问题共同构成落地三大障碍。  
4. 缺少统一基准导致研究进展可比性偏弱。  
5. 多模态融合与长上下文建模是最有前景、也最困难的开放问题。

---

*说明：以上为在不改变原意前提下的中文润色版。*
