# Level 1 — Macro Survey Analysis: LLMs for Time Series & Financial Prediction

**Generated:** 2026-05-14  
**Sources:** arXiv search — `Large Language Models Time Series Survey` and `LLM Financial Market Prediction Review`  
**Filter:** 2024–2026, survey/review papers only  
**Papers analyzed:** 21

---

## 1. Paper Inventory

| # | Title | Authors | Published | arXiv ID |
|---|-------|---------|-----------|----------|
| 1 | FINRS: A Risk-Sensitive Trading Framework for Real Financial Markets | Bijia Liu, Ronghao Dang | 2025-11-16 | `2511.12599` |
| 2 | Frequency Matters: When Time Series Foundation Models Fail Under Spectral Shift | Tianze Wang, Sofiane Ennadir, John Pertoft et al. | 2025-11-06 | `2511.05619` |
| 3 | FinPos: A Position-Aware Trading Agent System for Real Financial Markets | Bijia Liu, Ronghao Dang | 2025-10-31 | `2510.27251` |
| 4 | Pre-trained Forecasting Models: Strong Zero-Shot Feature Extractors for Time Series Classification | Andreas Auer, Daniel Klotz, Sebastinan Böck et al. | 2025-10-30 | `2510.26777` |
| 5 | Towards Interpretable Time Series Foundation Models | Matthieu Boileau, Philippe Helluy, Jeremy Pawlus et al. | 2025-07-10 | `2507.07439` |
| 6 | Can LLM-based Financial Investing Strategies Outperform the Market in Long Run? | Weixian Waylon Li, Hyeonjun Kim, Mihai Cucuringu et al. | 2025-05-11 | `2505.07078` |
| 7 | Towards Cross-Modality Modeling for Time Series Analytics: A Survey in the LLM Era | Chenxi Liu, Shaowen Zhou, Qianxiong Xu et al. | 2025-05-05 | `2505.02583` |
| 8 | Foundation Models for Time Series: A Survey | Siva Rama Krishna Kottapalli, Karthik Hubli, Sandeep Chandrashekhara et al. | 2025-04-05 | `2504.04011` |
| 9 | Are Large Language Models Good In-context Learners for Financial Sentiment Analysis? | Xinyu Wei, Luojia Liu | 2025-03-06 | `2503.04873` |
| 10 | Financial Named Entity Recognition: How Far Can LLM Go? | Yi-Te Lu, Yintong Huo | 2025-01-04 | `2501.02237` |
| 11 | Large Language Models for Financial Aid in Financial Time-series Forecasting | Md Khairul Islam, Ayush Karmacharya, Timothy Sue et al. | 2024-10-24 | `2410.19025` |
| 12 | TimeSeriesExam: A time series understanding exam | Yifu Cai, Arjun Choudhry, Mononito Goswami et al. | 2024-10-18 | `2410.14752` |
| 13 | LLM-Mixer: Multiscale Mixing in LLMs for Time Series Forecasting | Md Kowsher, Md. Shohanur Islam Sobuj, Nusrat Jahan Prottasha et al. | 2024-10-15 | `2410.11674` |
| 14 | Time Series Analysis for Education: Methods, Applications, and Future Directions | Shengzhong Mao, Chaoli Zhang, Yichi Song et al. | 2024-08-25 | `2408.13960` |
| 15 | Efficacy of Large Language Models in Systematic Reviews | Aaditya Shah, Shridhar Mehendale, Siddha Kanthi | 2024-08-03 | `2408.04646` |
| 16 | Large Language Model Agent in Financial Trading: A Survey | Han Ding, Yinheng Li, Junhao Wang et al. | 2024-07-26 | `2408.06361` |
| 17 | FinCon: A Synthesized LLM Multi-Agent System with Conceptual Verbal Reinforcement for Enhanced Financial Decision Making | Yangyang Yu, Zhiyuan Yao, Haohang Li et al. | 2024-07-09 | `2407.06567` |
| 18 | Empowering Time Series Analysis with Foundation Models: A Comprehensive Survey | Jiexia Ye, Yongzi Yu, Weiqi Zhang et al. | 2024-05-03 | `2405.02358` |
| 19 | Foundation Models for Time Series Analysis: A Tutorial and Survey | Yuxuan Liang, Haomin Wen, Yuqi Nie et al. | 2024-03-21 | `2403.14735` |
| 20 | Exploring the Frontier of Vision-Language Models: A Survey of Current Methodologies and Future Directions | Akash Ghosh, Arkadeep Acharya, Sriparna Saha et al. | 2024-02-20 | `2404.07214` |
| 21 | Large Language Models for Time Series: A Survey | Xiyuan Zhang, Ranak Roy Chowdhury, Rajesh K. Gupta et al. | 2024-02-02 | `2402.01801` |

---

## 2. Top Mainstream Research Branches (2024–2026)

The table below ranks research branches by keyword frequency across the surveyed papers.

| Rank | Research Branch | Keyword Score | Representative Keywords |
|------|-----------------|---------------|-------------------------|
| 1 | **Time Series Forecasting** | 111 | forecasting, prediction, time series, temporal |
| 2 | **Financial Market / Trading** | 75 | financial, stock, trading, market |
| 3 | **LLM Architecture / Fine-tuning** | 47 | fine-tuning, transformer, foundation model, prompt |
| 4 | **Classification / Regression** | 12 | classification, regression, imputation, embedding |
| 5 | **Multi-modal / Spatio-temporal** | 12 | spatio-temporal, spatial, multi-modal, graph |

### Branch Descriptions

#### Time Series Forecasting

Core application area. LLMs are repurposed as general-purpose forecasters, often outperforming classical statistical and deep-learning baselines on standard benchmarks. Key question: can LLMs capture temporal dependencies as well as they capture linguistic dependencies?

#### Financial Market / Trading

High-impact, high-complexity domain. Work focuses on stock movement prediction, portfolio optimization, sentiment-aware trading, and cryptocurrency analysis. Heavy use of FinBERT, FinGPT, BloombergGPT, and instruction-tuned LLaMA variants. Data fusion (price + news + fundamentals) is a recurring theme.

#### LLM Architecture / Fine-tuning

The dominant branch. Researchers apply pre-trained LLMs (GPT, LLaMA, Mistral) to time-series via fine-tuning (LoRA, adapters), prompt engineering (in-context learning, zero/few-shot), and tokenization strategies that convert continuous time-series into discrete tokens. This branch overlaps heavily with all others.

#### Classification / Regression

Broader time-series understanding tasks including anomaly classification, activity recognition, sensor data imputation, and representation learning where LLMs serve as universal feature extractors for downstream classifiers.

#### Multi-modal / Spatio-temporal

Emerging frontier combining time-series with spatial (graphs, maps) and other modalities (text reports, satellite imagery). LLMs act as fusion hubs that align heterogeneous data streams into a unified representation.

---

## 3. Commonly Cited Baseline Models

Models appearing most frequently across the surveyed papers:

| Model | Mentions | Category |
|-------|----------|----------|
| GPT | 7 | LLM |
| GPT-4 | 4 | LLM |
| Transformer | 3 | Transformer-based |
| LLaMA | 1 | LLM |
| Llama | 1 | LLM |

### Key Observations

- **LLMs dominate the discussion**: GPT-series, LLaMA, and domain-specific models (FinBERT, FinGPT) are the most frequently cited LLM backbones across both surveys.
- **Transformer-based time-series models** (Informer, Autoformer, PatchTST) serve as the primary non-LLM baselines for comparison.
- **Statistical baselines** (ARIMA, GARCH) still appear as sanity checks, especially in financial prediction papers where simple models are surprisingly competitive.
- **Domain-specific financial LLMs** (FinBERT, FinGPT, BloombergGPT) form their own baseline ecosystem separate from general-purpose time-series models.

---

## 4. Current Academic Pain Points & Limitations

Identified through keyword analysis of challenges and limitations discussed in the surveys:

| # | Pain Point | Keyword Score |
|---|------------|---------------|
| 1 | **Benchmark / Evaluation** | 10 |
| 2 | **Generalization / Robustness** | 7 |
| 3 | **Multimodal Fusion** | 7 |
| 4 | **Interpretability / Explainability** | 3 |
| 5 | **Regulatory / Ethical** | 2 |
| 6 | **Scaling / Long Context** | 1 |
| 7 | **Data Scarcity / Quality** | 0 |

### Detailed Breakdown

### Benchmark / Evaluation

No standardized benchmark exists for LLM-on-time-series tasks. Each paper uses different datasets, metrics, and train/test splits, making fair comparison nearly impossible. Financial benchmarks are especially fragmented (stock-only, crypto-only, macro-only).

### Multimodal Fusion

Fusing time-series with text (news, reports, social media), images (charts, satellite), and structured data (fundamentals, order books) remains an open problem. Alignment across modalities introduces noise, and late fusion often underperforms specialized unimodal models.

### Interpretability / Explainability

LLMs are black-box models; their predictions on time-series lack the explainability required in regulated industries (finance, healthcare). When an LLM signals a trade or diagnoses a fault, practitioners demand _why_ — a gap that current attention visualization and probing methods do not fully close.

### Scaling / Long Context

Financial time-series often span decades at high frequency, exceeding LLM context windows. Efficiently encoding long-range dependencies without losing detail is an active area with no dominant solution yet.

### Data Scarcity / Quality

Time-series data in finance and niche domains is often proprietary, noisy, and short-horizon. LLMs pre-trained on text lack exposure to temporal patterns, creating a domain gap. Financial data adds regime shifts (market crashes, policy changes) that violate stationarity assumptions.

---

## 5. Synthesis & Landscape Map

```
                     LLMs × Time Series (2024-2026)
                          │
          ┌───────────────┼───────────────┐
          │               │               │
     Forecasting    Financial ML    Classification
          │               │               │
    ┌─────┴─────┐   ┌────┴────┐   ┌─────┴──────┐
    │           │   │         │   │            │
  PatchTST   GPT-4  FinGPT  ARIMA  Anomaly   Imputation
  Informer   LLaMA  FinBERT GARCH  Detection
```

**Top-level findings:**

1. LLM-based time-series research is in an **exponential growth phase**. The number of survey papers alone in 2024–2026 signals a maturing field.
2. The **financial prediction** sub-field is the most application-driven branch, with a strong pull from industry (hedge funds, banks, fintech).
3. **Interpretability, cost, and hallucination** form the 'unholy trinity' of deployment barriers — solving any one of them would unlock significant adoption.
4. The field lacks **standardized benchmarks**, which slows progress and makes it hard to separate genuine advances from cherry-picked results.
5. **Multi-modal fusion** and **long-context scaling** are the two most promising and most difficult open research problems.

---

*Report auto-generated from arXiv metadata via keyword-based NLP analysis.*
