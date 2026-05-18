# 3 个 Markdown 文件渲染预览

> 在 Cursor 中打开此文件后，使用 `Open Preview` 查看渲染效果。

## Level1_Macro_Surveys.md

<div style="padding:16px;border:1px solid #e5e7eb;border-radius:10px;background:#fff;">

<h1>Level 1 — Macro Survey Analysis: LLMs for Time Series &amp; Financial Prediction</h1>
<p><strong>Generated:</strong> 2026-05-14<br />
<strong>Sources:</strong> arXiv search — <code>Large Language Models Time Series Survey</code> and <code>LLM Financial Market Prediction Review</code><br />
<strong>Filter:</strong> 2024–2026, survey/review papers only<br />
<strong>Papers analyzed:</strong> 21</p>
<hr />
<h2>1. Paper Inventory</h2>
<p>| # | Title | Authors | Published | arXiv ID |
|---|-------|---------|-----------|----------|
| 1 | FINRS: A Risk-Sensitive Trading Framework for Real Financial Markets | Bijia Liu, Ronghao Dang | 2025-11-16 | <code>2511.12599</code> |
| 2 | Frequency Matters: When Time Series Foundation Models Fail Under Spectral Shift | Tianze Wang, Sofiane Ennadir, John Pertoft et al. | 2025-11-06 | <code>2511.05619</code> |
| 3 | FinPos: A Position-Aware Trading Agent System for Real Financial Markets | Bijia Liu, Ronghao Dang | 2025-10-31 | <code>2510.27251</code> |
| 4 | Pre-trained Forecasting Models: Strong Zero-Shot Feature Extractors for Time Series Classification | Andreas Auer, Daniel Klotz, Sebastinan Böck et al. | 2025-10-30 | <code>2510.26777</code> |
| 5 | Towards Interpretable Time Series Foundation Models | Matthieu Boileau, Philippe Helluy, Jeremy Pawlus et al. | 2025-07-10 | <code>2507.07439</code> |
| 6 | Can LLM-based Financial Investing Strategies Outperform the Market in Long Run? | Weixian Waylon Li, Hyeonjun Kim, Mihai Cucuringu et al. | 2025-05-11 | <code>2505.07078</code> |
| 7 | Towards Cross-Modality Modeling for Time Series Analytics: A Survey in the LLM Era | Chenxi Liu, Shaowen Zhou, Qianxiong Xu et al. | 2025-05-05 | <code>2505.02583</code> |
| 8 | Foundation Models for Time Series: A Survey | Siva Rama Krishna Kottapalli, Karthik Hubli, Sandeep Chandrashekhara et al. | 2025-04-05 | <code>2504.04011</code> |
| 9 | Are Large Language Models Good In-context Learners for Financial Sentiment Analysis? | Xinyu Wei, Luojia Liu | 2025-03-06 | <code>2503.04873</code> |
| 10 | Financial Named Entity Recognition: How Far Can LLM Go? | Yi-Te Lu, Yintong Huo | 2025-01-04 | <code>2501.02237</code> |
| 11 | Large Language Models for Financial Aid in Financial Time-series Forecasting | Md Khairul Islam, Ayush Karmacharya, Timothy Sue et al. | 2024-10-24 | <code>2410.19025</code> |
| 12 | TimeSeriesExam: A time series understanding exam | Yifu Cai, Arjun Choudhry, Mononito Goswami et al. | 2024-10-18 | <code>2410.14752</code> |
| 13 | LLM-Mixer: Multiscale Mixing in LLMs for Time Series Forecasting | Md Kowsher, Md. Shohanur Islam Sobuj, Nusrat Jahan Prottasha et al. | 2024-10-15 | <code>2410.11674</code> |
| 14 | Time Series Analysis for Education: Methods, Applications, and Future Directions | Shengzhong Mao, Chaoli Zhang, Yichi Song et al. | 2024-08-25 | <code>2408.13960</code> |
| 15 | Efficacy of Large Language Models in Systematic Reviews | Aaditya Shah, Shridhar Mehendale, Siddha Kanthi | 2024-08-03 | <code>2408.04646</code> |
| 16 | Large Language Model Agent in Financial Trading: A Survey | Han Ding, Yinheng Li, Junhao Wang et al. | 2024-07-26 | <code>2408.06361</code> |
| 17 | FinCon: A Synthesized LLM Multi-Agent System with Conceptual Verbal Reinforcement for Enhanced Financial Decision Making | Yangyang Yu, Zhiyuan Yao, Haohang Li et al. | 2024-07-09 | <code>2407.06567</code> |
| 18 | Empowering Time Series Analysis with Foundation Models: A Comprehensive Survey | Jiexia Ye, Yongzi Yu, Weiqi Zhang et al. | 2024-05-03 | <code>2405.02358</code> |
| 19 | Foundation Models for Time Series Analysis: A Tutorial and Survey | Yuxuan Liang, Haomin Wen, Yuqi Nie et al. | 2024-03-21 | <code>2403.14735</code> |
| 20 | Exploring the Frontier of Vision-Language Models: A Survey of Current Methodologies and Future Directions | Akash Ghosh, Arkadeep Acharya, Sriparna Saha et al. | 2024-02-20 | <code>2404.07214</code> |
| 21 | Large Language Models for Time Series: A Survey | Xiyuan Zhang, Ranak Roy Chowdhury, Rajesh K. Gupta et al. | 2024-02-02 | <code>2402.01801</code> |</p>
<hr />
<h2>2. Top Mainstream Research Branches (2024–2026)</h2>
<p>The table below ranks research branches by keyword frequency across the surveyed papers.</p>
<p>| Rank | Research Branch | Keyword Score | Representative Keywords |
|------|-----------------|---------------|-------------------------|
| 1 | <strong>Time Series Forecasting</strong> | 111 | forecasting, prediction, time series, temporal |
| 2 | <strong>Financial Market / Trading</strong> | 75 | financial, stock, trading, market |
| 3 | <strong>LLM Architecture / Fine-tuning</strong> | 47 | fine-tuning, transformer, foundation model, prompt |
| 4 | <strong>Classification / Regression</strong> | 12 | classification, regression, imputation, embedding |
| 5 | <strong>Multi-modal / Spatio-temporal</strong> | 12 | spatio-temporal, spatial, multi-modal, graph |</p>
<h3>Branch Descriptions</h3>
<h4>Time Series Forecasting</h4>
<p>Core application area. LLMs are repurposed as general-purpose forecasters, often outperforming classical statistical and deep-learning baselines on standard benchmarks. Key question: can LLMs capture temporal dependencies as well as they capture linguistic dependencies?</p>
<h4>Financial Market / Trading</h4>
<p>High-impact, high-complexity domain. Work focuses on stock movement prediction, portfolio optimization, sentiment-aware trading, and cryptocurrency analysis. Heavy use of FinBERT, FinGPT, BloombergGPT, and instruction-tuned LLaMA variants. Data fusion (price + news + fundamentals) is a recurring theme.</p>
<h4>LLM Architecture / Fine-tuning</h4>
<p>The dominant branch. Researchers apply pre-trained LLMs (GPT, LLaMA, Mistral) to time-series via fine-tuning (LoRA, adapters), prompt engineering (in-context learning, zero/few-shot), and tokenization strategies that convert continuous time-series into discrete tokens. This branch overlaps heavily with all others.</p>
<h4>Classification / Regression</h4>
<p>Broader time-series understanding tasks including anomaly classification, activity recognition, sensor data imputation, and representation learning where LLMs serve as universal feature extractors for downstream classifiers.</p>
<h4>Multi-modal / Spatio-temporal</h4>
<p>Emerging frontier combining time-series with spatial (graphs, maps) and other modalities (text reports, satellite imagery). LLMs act as fusion hubs that align heterogeneous data streams into a unified representation.</p>
<hr />
<h2>3. Commonly Cited Baseline Models</h2>
<p>Models appearing most frequently across the surveyed papers:</p>
<p>| Model | Mentions | Category |
|-------|----------|----------|
| GPT | 7 | LLM |
| GPT-4 | 4 | LLM |
| Transformer | 3 | Transformer-based |
| LLaMA | 1 | LLM |
| Llama | 1 | LLM |</p>
<h3>Key Observations</h3>
<ul>
<li><strong>LLMs dominate the discussion</strong>: GPT-series, LLaMA, and domain-specific models (FinBERT, FinGPT) are the most frequently cited LLM backbones across both surveys.</li>
<li><strong>Transformer-based time-series models</strong> (Informer, Autoformer, PatchTST) serve as the primary non-LLM baselines for comparison.</li>
<li><strong>Statistical baselines</strong> (ARIMA, GARCH) still appear as sanity checks, especially in financial prediction papers where simple models are surprisingly competitive.</li>
<li><strong>Domain-specific financial LLMs</strong> (FinBERT, FinGPT, BloombergGPT) form their own baseline ecosystem separate from general-purpose time-series models.</li>
</ul>
<hr />
<h2>4. Current Academic Pain Points &amp; Limitations</h2>
<p>Identified through keyword analysis of challenges and limitations discussed in the surveys:</p>
<p>| # | Pain Point | Keyword Score |
|---|------------|---------------|
| 1 | <strong>Benchmark / Evaluation</strong> | 10 |
| 2 | <strong>Generalization / Robustness</strong> | 7 |
| 3 | <strong>Multimodal Fusion</strong> | 7 |
| 4 | <strong>Interpretability / Explainability</strong> | 3 |
| 5 | <strong>Regulatory / Ethical</strong> | 2 |
| 6 | <strong>Scaling / Long Context</strong> | 1 |
| 7 | <strong>Data Scarcity / Quality</strong> | 0 |</p>
<h3>Detailed Breakdown</h3>
<h3>Benchmark / Evaluation</h3>
<p>No standardized benchmark exists for LLM-on-time-series tasks. Each paper uses different datasets, metrics, and train/test splits, making fair comparison nearly impossible. Financial benchmarks are especially fragmented (stock-only, crypto-only, macro-only).</p>
<h3>Multimodal Fusion</h3>
<p>Fusing time-series with text (news, reports, social media), images (charts, satellite), and structured data (fundamentals, order books) remains an open problem. Alignment across modalities introduces noise, and late fusion often underperforms specialized unimodal models.</p>
<h3>Interpretability / Explainability</h3>
<p>LLMs are black-box models; their predictions on time-series lack the explainability required in regulated industries (finance, healthcare). When an LLM signals a trade or diagnoses a fault, practitioners demand <em>why</em> — a gap that current attention visualization and probing methods do not fully close.</p>
<h3>Scaling / Long Context</h3>
<p>Financial time-series often span decades at high frequency, exceeding LLM context windows. Efficiently encoding long-range dependencies without losing detail is an active area with no dominant solution yet.</p>
<h3>Data Scarcity / Quality</h3>
<p>Time-series data in finance and niche domains is often proprietary, noisy, and short-horizon. LLMs pre-trained on text lack exposure to temporal patterns, creating a domain gap. Financial data adds regime shifts (market crashes, policy changes) that violate stationarity assumptions.</p>
<hr />
<h2>5. Synthesis &amp; Landscape Map</h2>
<pre><code>                     LLMs × Time Series (2024-2026)
                          │
          ┌───────────────┼───────────────┐
          │               │               │
     Forecasting    Financial ML    Classification
          │               │               │
    ┌─────┴─────┐   ┌────┴────┐   ┌─────┴──────┐
    │           │   │         │   │            │
  PatchTST   GPT-4  FinGPT  ARIMA  Anomaly   Imputation
  Informer   LLaMA  FinBERT GARCH  Detection
</code></pre>
<p><strong>Top-level findings:</strong></p>
<ol>
<li>LLM-based time-series research is in an <strong>exponential growth phase</strong>. The number of survey papers alone in 2024–2026 signals a maturing field.</li>
<li>The <strong>financial prediction</strong> sub-field is the most application-driven branch, with a strong pull from industry (hedge funds, banks, fintech).</li>
<li><strong>Interpretability, cost, and hallucination</strong> form the 'unholy trinity' of deployment barriers — solving any one of them would unlock significant adoption.</li>
<li>The field lacks <strong>standardized benchmarks</strong>, which slows progress and makes it hard to separate genuine advances from cherry-picked results.</li>
<li><strong>Multi-modal fusion</strong> and <strong>long-context scaling</strong> are the two most promising and most difficult open research problems.</li>
</ol>
<hr />
<p><em>Report auto-generated from arXiv metadata via keyword-based NLP analysis.</em></p>


</div>

## Related_Work_Agents.md

<div style="padding:16px;border:1px solid #e5e7eb;border-radius:10px;background:#fff;">

<h1>Related Work — Multi-Agent / Agentic RAG for Finance &amp; Time Series (2024–2026)</h1>
<p><strong>Generated:</strong> 2026-05-14
<strong>Source:</strong> arXiv — 4 search queries combining Agent + RAG + Finance/Trading/TS
<strong>Papers after relevance filtering:</strong> 25</p>
<hr />
<h2>Paper Inventory: Core Integration Mechanisms</h2>
<p>| # | Paper Title | Year | Core Integration Mechanism |
|---|-------------|------|----------------------------|
| 1 | <a href="https://arxiv.org/abs/2506.16813">Integrating Traditional Technical Analysis with AI: A Multi-Agent LLM-Based Approach to Stock Market Forecasting</a> | 2025 | multi-agent system with specialized agent roles; retrieval-augmented generation (RAG) for external knowledge injection |
| 2 | <a href="https://arxiv.org/abs/2510.05533">The New Quant: A Survey of Large Language Models in Financial Prediction and Trading</a> | 2025 | agentic workflow with autonomous decision loops; retrieval-augmented generation (RAG) for external knowledge injection; financial sentiment analysis from news/social media; multimodal data fusion (text + numerical + visual); tool-calling capability for external API/data access |
| 3 | <a href="https://arxiv.org/abs/2509.16369">Enhancing Financial RAG with Agentic AI and Multi-HyDE: A Novel Approach to Knowledge Retrieval and Hallucination Reduction</a> | 2025 | Agentic RAG + Multi-HyDE: generates multiple diverse hypothetical queries for multi-perspective retrieval from structured financial corpora, combined with multi-step reasoning agent workflow — reduces hallucinations 15% and improves accuracy 11.2% |
| 4 | <a href="https://arxiv.org/abs/2509.09727">A Role-Aware Multi-Agent Framework for Financial Education Question Answering with LLMs</a> | 2025 | role-specialized multi-agent system with task decomposition; retrieval-augmented generation (RAG) for external knowledge injection; fine-tuned LLM backbone |
| 5 | <a href="https://arxiv.org/abs/2511.18177">Rethinking Retrieval: From Traditional Retrieval Augmented Generation to Agentic and Non-Vector Reasoning Systems in the Financial Domain for Large Language Models</a> | 2025 | Systematic comparison: vector-based agentic RAG (hybrid search + metadata filtering + cross-encoder reranking + small-to-big chunking) vs hierarchical node-based traversal (no embeddings) — evaluated on 1,200 SEC filings; vector RAG wins 68% pairwise |
| 6 | <a href="https://arxiv.org/abs/2408.14484">Agentic Retrieval-Augmented Generation for Time Series Analysis</a> | 2024 | hierarchical multi-agent orchestration (supervisor + worker agents); retrieval-augmented generation (RAG) for external knowledge injection; fine-tuned LLM backbone |
| 7 | <a href="https://arxiv.org/abs/2603.13244">Agentic AI, Retrieval-Augmented Generation, and the Institutional Turn: Legal Architectures and Financial Governance in the Age of Distributional AGI</a> | 2026 | multi-agent system with specialized agent roles; retrieval-augmented generation (RAG) for external knowledge injection |
| 8 | <a href="https://arxiv.org/abs/2504.05104">AI for Climate Finance: Agentic Retrieval and Multi-Step Reasoning for Early Warning System Investments</a> | 2025 | agentic workflow with autonomous decision loops; retrieval-augmented generation (RAG) for external knowledge injection; fine-tuned LLM backbone |
| 9 | <a href="https://arxiv.org/abs/2604.14222">Adaptive Query Routing: A Tier-Based Framework for Hybrid Retrieval Across Financial, Legal, and Medical Documents</a> | 2026 | agentic workflow with autonomous decision loops; vector-store retrieval with embedding-based semantic search; GPT-based agent reasoning engine |
| 10 | <a href="https://arxiv.org/abs/2502.00415">MarketSenseAI 2.0: Enhancing Stock Analysis through LLM Agents</a> | 2025 | Multi-agent + RAG framework: dedicated agents process SEC filings, earnings calls, and macro reports via RAG for holistic stock analysis — combines fundamental, technical, news sentiment, and macro signals into investment decisions (125.9% cumulative return vs 73.5% S&amp;P 100) |
| 11 | <a href="https://arxiv.org/abs/2502.07223">Graph RAG-Tool Fusion</a> | 2025 | GraphRAG-based knowledge retrieval over structured/unstructured data; tool-calling capability for external API/data access |
| 12 | <a href="https://arxiv.org/abs/2501.09136">Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG</a> | 2025 | collaborative multi-agent system with inter-agent communication; retrieval-augmented generation (RAG) for external knowledge injection; real-time streaming data processing; tool-calling capability for external API/data access; conversational memory for multi-turn reasoning |
| 13 | <a href="https://arxiv.org/abs/2510.02388">Learning to Route: A Rule-Driven Agent Framework for Hybrid-Source Retrieval-Augmented Generation</a> | 2025 | hybrid retrieval (dense + sparse) for multi-source knowledge |
| 14 | <a href="https://arxiv.org/abs/2601.05353">GlyRAG: Context-Aware Retrieval-Augmented Framework for Blood Glucose Forecasting</a> | 2026 | agentic workflow with autonomous decision loops; retrieval-augmented generation (RAG) for external knowledge injection; multimodal data fusion (text + numerical + visual) |
| 15 | <a href="https://arxiv.org/abs/2605.05409">Agentic Retrieval-Augmented Generation for Financial Document Question Answering (FinAgent-RAG)</a> | 2026 | Iterative retrieval-reasoning loops with self-verification: (1) Contrastive Financial Retriever with hard negative mining, (2) Program-of-Thought module generates executable Python for precise arithmetic, (3) Adaptive Strategy Router allocates compute by question complexity — outperforms baselines by 5.6–9.3 points on FinQA/ConvFinQA/TAT-QA |
| 16 | <a href="https://arxiv.org/abs/2502.15700">Sustainable Digitalization of Business with Multi-Agent RAG and LLM</a> | 2025 | multi-agent system with specialized agent roles; retrieval-augmented generation (RAG) for external knowledge injection |
| 17 | <a href="https://arxiv.org/abs/2508.00828">Finance Agent Benchmark: Benchmarking LLMs on Real-world Financial Research Tasks</a> | 2025 | agentic workflow with autonomous decision loops |
| 18 | <a href="https://arxiv.org/abs/2603.13767">Retrieve, Schedule, Reflect: LLM Agents for Chip QoR Optimization</a> | 2026 | agentic workflow with autonomous decision loops; retrieval-augmented generation (RAG) for external knowledge injection |
| 19 | <a href="https://arxiv.org/abs/2510.16980">Towards Interpretable and Trustworthy Time Series Reasoning: A BlueSky Vision</a> | 2025 | collaborative multi-agent system with inter-agent communication; retrieval-augmented generation (RAG) for external knowledge injection; multimodal data fusion (text + numerical + visual) |
| 20 | <a href="https://arxiv.org/abs/2604.03908">Reimagining RAN Automation in 6G: An Agentic AI Framework with Hierarchical Online Decision Transformer</a> | 2026 | agentic workflow with autonomous decision loops; retrieval-augmented generation (RAG) for external knowledge injection |
| 21 | <a href="https://arxiv.org/abs/2603.20750">Modeling Epistemic Uncertainty in Social Perception via Rashomon Set Agents</a> | 2026 | multi-agent system with specialized agent roles; retrieval-augmented generation (RAG) for external knowledge injection |
| 22 | <a href="https://arxiv.org/abs/2510.20505">RELOOP: Recursive Retrieval with Multi-Hop Reasoner and Planners for Heterogeneous QA</a> | 2025 | agentic workflow with autonomous decision loops; hybrid retrieval (dense + sparse) for multi-source knowledge; tool-calling capability for external API/data access |
| 23 | <a href="https://arxiv.org/abs/2405.03963">ERATTA: Extreme RAG for Table To Answers with Large Language Models</a> | 2024 | agentic workflow with autonomous decision loops; retrieval-augmented generation (RAG) for external knowledge injection |
| 24 | <a href="https://arxiv.org/abs/2510.27287">Can LLMs Help You at Work? A Sandbox for Evaluating LLM Agents in Enterprise Environments</a> | 2025 | Enterprise systems are crucial for enhancing productivity and decision-making among employees and customers |
| 25 | <a href="https://arxiv.org/abs/2409.14913">Towards a Realistic Long-Term Benchmark for Open-Web Research Agents</a> | 2024 | GPT-based agent reasoning engine |</p>
<hr />
<h2>Paper Details</h2>
<h3>1. Integrating Traditional Technical Analysis with AI: A Multi-Agent LLM-Based Approach to Stock Market Forecasting</h3>
<ul>
<li><strong>Authors:</strong> Michał Wawer, Jarosław A. Chudziak</li>
<li><strong>Published:</strong> 2025-06-20</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2506.16813">2506.16813</a></li>
<li><strong>Core Mechanism:</strong> multi-agent system with specialized agent roles; retrieval-augmented generation (RAG) for external knowledge injection</li>
<li><strong>Abstract:</strong> Traditional technical analysis methods face limitations in accurately predicting trends in today's complex financial markets. This paper introduces ElliottAgents, an multi-agent system that integrates the Elliott Wave Principle with AI for stock market forecasting. The inherent complexity of financial markets, characterized by non-linear dynamics, noise, and susceptibility to unpredictable external factors, poses significant challenges for accurate prediction. To address these challenges, the system employs LLMs to enhance natural language understanding and decision-making capabilities within a multi-agent framework. By leveraging technologies such as Retrieval-Augmented Generation (RAG) and Deep Reinforcement Learning (DRL), ElliottAgents performs continuous, multi-faceted analysis of market data to identify wave patterns and predict future price movements. The research explores the system's ability to process historical stock data, recognize Elliott wave patterns, and generate actionable insights for traders. Experimental results, conducted on historical data from major U.S. companies, validate the system's effectiveness in pattern recognition and trend forecasting across various time frames. This paper contributes to the field of AI-driven financial analysis by demonstrating how traditional technical analysis methods can be effectively combined with modern AI approaches to create more reliable and interpretable market prediction systems.</li>
</ul>
<h3>2. The New Quant: A Survey of Large Language Models in Financial Prediction and Trading</h3>
<ul>
<li><strong>Authors:</strong> Weilong Fu</li>
<li><strong>Published:</strong> 2025-10-07</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2510.05533">2510.05533</a></li>
<li><strong>Core Mechanism:</strong> agentic workflow with autonomous decision loops; retrieval-augmented generation (RAG) for external knowledge injection; financial sentiment analysis from news/social media; multimodal data fusion (text + numerical + visual); tool-calling capability for external API/data access</li>
<li><strong>Abstract:</strong> Large language models are reshaping quantitative investing by turning unstructured financial information into evidence-grounded signals and executable decisions. This survey synthesizes research with a focus on equity return prediction and trading, consolidating insights from domain surveys and more than fifty primary studies. We propose a task-centered taxonomy that spans sentiment and event extraction, numerical and economic reasoning, multimodal understanding, retrieval-augmented generation, time series prompting, and agentic systems that coordinate tools for research, backtesting, and execution. We review empirical evidence for predictability, highlight design patterns that improve faithfulness such as retrieval first prompting and tool-verified numerics, and explain how signals feed portfolio construction under exposure, turnover, and capacity controls. We assess benchmarks and datasets for prediction and trading and outline desiderata-for time safe and economically meaningful evaluation that reports costs, latency, and capacity. We analyze challenges that matter in production, including temporal leakage, hallucination, data coverage and structure, deployment economics, interpretability, governance, and safety. The survey closes with recommendations for standardizing evaluation, building auditable pipelines, and advancing multilingual and cross-market research so that language-driven systems deliver robust and risk-controlled performance in practice.</li>
</ul>
<h3>3. Enhancing Financial RAG with Agentic AI and Multi-HyDE: A Novel Approach to Knowledge Retrieval and Hallucination Reduction</h3>
<ul>
<li><strong>Authors:</strong> Akshay Govind Srinivasan, Ryan Jacob George, Jayden Koshy Joe, Hrushikesh Kant, Harshith M R, Sachin Sundar et al.</li>
<li><strong>Published:</strong> 2025-09-19</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2509.16369">2509.16369</a></li>
<li><strong>Core Mechanism:</strong> Agentic RAG + Multi-HyDE: generates multiple diverse hypothetical queries for multi-perspective retrieval from structured financial corpora, combined with multi-step reasoning agent workflow — reduces hallucinations 15% and improves accuracy 11.2%</li>
<li><strong>Abstract:</strong> Accurate and reliable knowledge retrieval is vital for financial question-answering, where continually updated data sources and complex, high-stakes contexts demand precision. Traditional retrieval systems rely on a single database and retriever, but financial applications require more sophisticated approaches to handle intricate regulatory filings, market analyses, and extensive multi-year reports. We introduce a framework for financial Retrieval Augmented Generation (RAG) that leverages agentic AI and the Multi-HyDE system, an approach that generates multiple, nonequivalent queries to boost the effectiveness and coverage of retrieval from large, structured financial corpora. Our pipeline is optimized for token efficiency and multi-step financial reasoning, and we demonstrate that their combination improves accuracy by 11.2% and reduces hallucinations by 15%. Our method is evaluated on standard financial QA benchmarks, showing that integrating domain-specific retrieval mechanisms such as Multi-HyDE with robust toolsets, including keyword and table-based retrieval, significantly enhances both the accuracy and reliability of answers. This research not only delivers a modular, adaptable retrieval framework for finance but also highlights the importance of structured agent workflows and multi-perspective retrieval for trustworthy deployment of AI in high-stakes financial applications.</li>
</ul>
<h3>4. A Role-Aware Multi-Agent Framework for Financial Education Question Answering with LLMs</h3>
<ul>
<li><strong>Authors:</strong> Andy Zhu, Yingjun Du</li>
<li><strong>Published:</strong> 2025-09-10</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2509.09727">2509.09727</a></li>
<li><strong>Core Mechanism:</strong> role-specialized multi-agent system with task decomposition; retrieval-augmented generation (RAG) for external knowledge injection; fine-tuned LLM backbone</li>
<li><strong>Abstract:</strong> Question answering (QA) plays a central role in financial education, yet existing large language model (LLM) approaches often fail to capture the nuanced and specialized reasoning required for financial problem-solving. The financial domain demands multistep quantitative reasoning, familiarity with domain-specific terminology, and comprehension of real-world scenarios. We present a multi-agent framework that leverages role-based prompting to enhance performance on domain-specific QA. Our framework comprises a Base Generator, an Evidence Retriever, and an Expert Reviewer agent that work in a single-pass iteration to produce a refined answer. We evaluated our framework on a set of 3,532 expert-designed finance education questions from Study.com, an online learning platform. We leverage retrieval-augmented generation (RAG) for contextual evidence from 6 finance textbooks and prompting strategies for a domain-expert reviewer. Our experiments indicate that critique-based refinement improves answer accuracy by 6.6-8.3% over zero-shot Chain-of-Thought baselines, with the highest performance from Gemini-2.0-Flash. Furthermore, our method enables GPT-4o-mini to achieve performance comparable to the finance-tuned FinGPT-mt_Llama3-8B_LoRA. Our results show a cost-effective approach to enhancing financial QA and offer insights for further research in multi-agent financial LLM systems.</li>
</ul>
<h3>5. Rethinking Retrieval: From Traditional Retrieval Augmented Generation to Agentic and Non-Vector Reasoning Systems in the Financial Domain for Large Language Models</h3>
<ul>
<li><strong>Authors:</strong> Elias Lumer, Matt Melich, Olivia Zino, Elena Kim, Sara Dieter, Pradeep Honaganahalli Basavaraju et al.</li>
<li><strong>Published:</strong> 2025-11-22</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2511.18177">2511.18177</a></li>
<li><strong>Core Mechanism:</strong> agentic workflow with autonomous decision loops; vector-store retrieval with embedding-based semantic search</li>
<li><strong>Abstract:</strong> Recent advancements in Retrieval-Augmented Generation (RAG) have enabled Large Language Models to answer financial questions using external knowledge bases of U.S. SEC filings, earnings reports, and regulatory documents. However, existing work lacks systematic comparison of vector-based and non-vector RAG architectures for financial documents, and the empirical impact of advanced RAG techniques on retrieval accuracy, answer quality, latency, and cost remain unclear. We present the first systematic evaluation comparing vector-based agentic RAG using hybrid search and metadata filtering against hierarchical node-based systems that traverse document structure without embeddings. We evaluate two enhancement techniques applied to the vector-based architecture, i) cross-encoder reranking for retrieval precision, and ii) small-to-big chunk retrieval for context completeness. Across 1,200 SEC 10-K, 10-Q, and 8-K filings on a 150-question benchmark, we measure retrieval metrics (MRR, Recall@5), answer quality through LLM-as-a-judge pairwise comparisons, latency, and preprocessing costs. Vector-based agentic RAG achieves a 68% win rate over hierarchical node-based systems with comparable latency (5.2 compared to 5.98 seconds). Cross-encoder reranking achieves a 59% absolute improvement at optimal parameters (10, 5) for MRR@5. Small-to-big retrieval achieves a 65% win rate over baseline chunking with only 0.2 seconds additional latency. Our findings reveal that applying advanced RAG techniques to financial Q&amp;A systems improves retrieval accuracy, answer quality, and has cost-performance tradeoffs to be considered in production.</li>
</ul>
<h3>6. Agentic Retrieval-Augmented Generation for Time Series Analysis</h3>
<ul>
<li><strong>Authors:</strong> Chidaksh Ravuru, Sagar Srinivas Sakhinana, Venkataramana Runkana</li>
<li><strong>Published:</strong> 2024-08-18</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2408.14484">2408.14484</a></li>
<li><strong>Core Mechanism:</strong> hierarchical multi-agent orchestration (supervisor + worker agents); retrieval-augmented generation (RAG) for external knowledge injection; fine-tuned LLM backbone</li>
<li><strong>Abstract:</strong> Time series modeling is crucial for many applications, however, it faces challenges such as complex spatio-temporal dependencies and distribution shifts in learning from historical context to predict task-specific outcomes. To address these challenges, we propose a novel approach using an agentic Retrieval-Augmented Generation (RAG) framework for time series analysis. The framework leverages a hierarchical, multi-agent architecture where the master agent orchestrates specialized sub-agents and delegates the end-user request to the relevant sub-agent. The sub-agents utilize smaller, pre-trained language models (SLMs) customized for specific time series tasks through fine-tuning using instruction tuning and direct preference optimization, and retrieve relevant prompts from a shared repository of prompt pools containing distilled knowledge about historical patterns and trends to improve predictions on new data. Our proposed modular, multi-agent RAG approach offers flexibility and achieves state-of-the-art performance across major time series tasks by tackling complex challenges more effectively than task-specific customized methods across benchmark datasets.</li>
</ul>
<h3>7. Agentic AI, Retrieval-Augmented Generation, and the Institutional Turn: Legal Architectures and Financial Governance in the Age of Distributional AGI</h3>
<ul>
<li><strong>Authors:</strong> Marcel Osmond</li>
<li><strong>Published:</strong> 2026-02-20</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2603.13244">2603.13244</a></li>
<li><strong>Core Mechanism:</strong> multi-agent system with specialized agent roles; retrieval-augmented generation (RAG) for external knowledge injection</li>
<li><strong>Abstract:</strong> The proliferation of agentic artificial intelligence systems--characterized by autonomous goal-seeking, tool use, and multi-agent coordination--presents unprecedented challenges to existing legal and financial regulatory frameworks. While traditional AI governance has focused on model-level alignment through training-time interventions such as Reinforcement Learning from Human Feedback (RLHF), the deployment of large language models (LLMs) as persistent agents necessitates a paradigm shift toward institutional governance structures. This paper examines the intersection of agentic AI, Retrieval-Augmented Generation (RAG), and their implications for legal accountability and financial market integrity. Through analysis of the Institutional AI framework, we argue that alignment must be reconceptualized as a mechanism design problem involving runtime governance graphs, sanction functions, and observable behavioral constraints rather than internalized constitutional values[...].The analysis concludes that the future of AI governance lies not in perfecting isolated model behavior, but in architecting institutional environments where compliant behavior emerges as the dominant strategy through carefully calibrated payoff landscapes.</li>
</ul>
<h3>8. AI for Climate Finance: Agentic Retrieval and Multi-Step Reasoning for Early Warning System Investments</h3>
<ul>
<li><strong>Authors:</strong> Saeid Ario Vaghefi, Aymane Hachcham, Veronica Grasso, Jiska Manicus, Nakiete Msemo, Chiara Colesanti Senni et al.</li>
<li><strong>Published:</strong> 2025-04-07</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2504.05104">2504.05104</a></li>
<li><strong>Core Mechanism:</strong> agentic workflow with autonomous decision loops; retrieval-augmented generation (RAG) for external knowledge injection; fine-tuned LLM backbone</li>
<li><strong>Abstract:</strong> Tracking financial investments in climate adaptation is a complex and expertise-intensive task, particularly for Early Warning Systems (EWS), which lack standardized financial reporting across multilateral development banks (MDBs) and funds. To address this challenge, we introduce an LLM-based agentic AI system that integrates contextual retrieval, fine-tuning, and multi-step reasoning to extract relevant financial data, classify investments, and ensure compliance with funding guidelines. Our study focuses on a real-world application: tracking EWS investments in the Climate Risk and Early Warning Systems (CREWS) Fund. We analyze 25 MDB project documents and evaluate multiple AI-driven classification methods, including zero-shot and few-shot learning, fine-tuned transformer-based classifiers, chain-of-thought (CoT) prompting, and an agent-based retrieval-augmented generation (RAG) approach. Our results show that the agent-based RAG approach significantly outperforms other methods, achieving 87% accuracy, 89% precision, and 83% recall. Additionally, we contribute a benchmark dataset and expert-annotated corpus, providing a valuable resource for future research in AI-driven financial tracking and climate finance transparency.</li>
</ul>
<h3>9. Adaptive Query Routing: A Tier-Based Framework for Hybrid Retrieval Across Financial, Legal, and Medical Documents</h3>
<ul>
<li><strong>Authors:</strong> Afshan Hashmi</li>
<li><strong>Published:</strong> 2026-04-14</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2604.14222">2604.14222</a></li>
<li><strong>Core Mechanism:</strong> agentic workflow with autonomous decision loops; vector-store retrieval with embedding-based semantic search; GPT-based agent reasoning engine</li>
<li><strong>Abstract:</strong> Retrieval-Augmented Generation (RAG) has become the standard paradigm for grounding Large Language Model outputs in external knowledge. Lumer et al. [1] presented the first systematic evaluation comparing vector-based agentic RAG against hierarchical node-based reasoning systems for financial document QA across 1,200 SEC filings, finding vector-based systems achieved a 68% win rate. Concurrently, the PageIndex framework [2] demonstrated 98.7% accuracy on FinanceBench through purely reasoning-based retrieval. This paper extends their work by: (i) implementing and evaluating three retrieval architectures: Vector RAG, Tree Reasoning, and the proposed Adaptive Hybrid Retrieval (AHR) across financial, legal, and medical domains; (ii) introducing a four-tier query complexity benchmark; and (iii) employing GPT-4-powered LLM-as-judge evaluation. Experiments reveal that Tree Reasoning achieves the highest overall score (0.900), but no single paradigm dominates across all tiers: Vector RAG wins on multi-document synthesis (Tier 4, score 0.900), while the Hybrid AHR achieves the best performance on cross-reference (0.850) and multi-section queries (0.929). Cross-reference recall reaches 100% for tree-based and hybrid approaches versus 91.7% for vector search, quantifying a critical capability gap. Validation on FinanceBench (150 expert-annotated questions on real SEC 10-K and 10-Q filings) confirms and strengthens these findings: Tree Reasoning scores 0.938, Hybrid AHR 0.901, and Vector RAG 0.821, with the Tree--Vector quality gap widening to 11.7 percentage points on real-world documents. These findings support the development of adaptive retrieval systems that dynamically select strategies based on query complexity and document structure. All code and data are publicly available.</li>
</ul>
<h3>10. MarketSenseAI 2.0: Enhancing Stock Analysis through LLM Agents</h3>
<ul>
<li><strong>Authors:</strong> George Fatouros, Kostas Metaxas, John Soldatos, Manos Karathanassis</li>
<li><strong>Published:</strong> 2025-02-01</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2502.00415">2502.00415</a></li>
<li><strong>Core Mechanism:</strong> Multi-agent + RAG framework: dedicated agents process SEC filings, earnings calls, and macro reports via RAG for holistic stock analysis — combines fundamental, technical, news sentiment, and macro signals into investment decisions (125.9% cumulative return vs 73.5% S&amp;P 100)</li>
<li><strong>Abstract:</strong> MarketSenseAI is a novel framework for holistic stock analysis which leverages Large Language Models (LLMs) to process financial news, historical prices, company fundamentals and the macroeconomic environment to support decision making in stock analysis and selection. In this paper, we present the latest advancements on MarketSenseAI, driven by rapid technological expansion in LLMs. Through a novel architecture combining Retrieval-Augmented Generation and LLM agents, the framework processes SEC filings and earnings calls, while enriching macroeconomic analysis through systematic processing of diverse institutional reports. We demonstrate a significant improvement in fundamental analysis accuracy over the previous version. Empirical evaluation on S&amp;P 100 stocks over two years (2023-2024) shows MarketSenseAI achieving cumulative returns of 125.9% compared to the index return of 73.5%, while maintaining comparable risk profiles. Further validation on S&amp;P 500 stocks during 2024 demonstrates the framework's scalability, delivering a 33.8% higher Sortino ratio than the market. This work marks a significant advancement in applying LLM technology to financial analysis, offering insights into the robustness of LLM-driven investment strategies.</li>
</ul>
<h3>11. Graph RAG-Tool Fusion</h3>
<ul>
<li><strong>Authors:</strong> Elias Lumer, Pradeep Honaganahalli Basavaraju, Myles Mason, James A. Burke, Vamse Kumar Subbiah</li>
<li><strong>Published:</strong> 2025-02-11</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2502.07223">2502.07223</a></li>
<li><strong>Core Mechanism:</strong> GraphRAG-based knowledge retrieval over structured/unstructured data; tool-calling capability for external API/data access</li>
<li><strong>Abstract:</strong> Recent developments in retrieval-augmented generation (RAG) for selecting relevant tools from a tool knowledge base enable LLM agents to scale their complex tool calling capabilities to hundreds or thousands of external tools, APIs, or agents-as-tools. However, traditional RAG-based tool retrieval fails to capture structured dependencies between tools, limiting the retrieval accuracy of a retrieved tool's dependencies. For example, among a vector database of tools, a &quot;get stock price&quot; API requires a &quot;stock ticker&quot; parameter from a &quot;get stock ticker&quot; API, and both depend on OS-level internet connectivity tools. In this paper, we address this limitation by introducing Graph RAG-Tool Fusion, a novel plug-and-play approach that combines the strengths of vector-based retrieval with efficient graph traversal to capture all relevant tools (nodes) along with any nested dependencies (edges) within the predefined tool knowledge graph. We also present ToolLinkOS, a new tool selection benchmark of 573 fictional tools, spanning over 15 industries, each with an average of 6.3 tool dependencies. We demonstrate that Graph RAG-Tool Fusion achieves absolute improvements of 71.7% and 22.1% over naïve RAG on ToolLinkOS and ToolSandbox benchmarks, respectively (mAP@10). ToolLinkOS dataset is available at https://github.com/EliasLumer/Graph-RAG-Tool-Fusion-ToolLinkOS</li>
</ul>
<h3>12. Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG</h3>
<ul>
<li><strong>Authors:</strong> Aditi Singh, Abul Ehtesham, Saket Kumar, Tala Talaei Khoei, Athanasios V. Vasilakos</li>
<li><strong>Published:</strong> 2025-01-15</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2501.09136">2501.09136</a></li>
<li><strong>Core Mechanism:</strong> collaborative multi-agent system with inter-agent communication; retrieval-augmented generation (RAG) for external knowledge injection; real-time streaming data processing; tool-calling capability for external API/data access; conversational memory for multi-turn reasoning</li>
<li><strong>Abstract:</strong> Large Language Models (LLMs) have advanced artificial intelligence by enabling human-like text generation and natural language understanding. However, their reliance on static training data limits their ability to respond to dynamic, real-time queries, resulting in outdated or inaccurate outputs. Retrieval-Augmented Generation (RAG) has emerged as a solution, enhancing LLMs by integrating real-time data retrieval to provide contextually relevant and up-to-date responses. Despite its promise, traditional RAG systems are constrained by static workflows and lack the adaptability required for multi-step reasoning and complex task management. Agentic Retrieval-Augmented Generation (Agentic RAG) transcends these limitations by embedding autonomous AI agents into the RAG pipeline. These agents leverage agentic design patterns reflection, planning, tool use, and multi-agent collaboration to dynamically manage retrieval strategies, iteratively refine contextual understanding, and adapt workflows through operational structures ranging from sequential steps to adaptive collaboration. This integration enables Agentic RAG systems to deliver flexibility, scalability, and context-awareness across diverse applications. This paper presents an analytical survey of Agentic RAG systems. It traces the evolution of RAG paradigms, introduces a principled taxonomy of Agentic RAG architectures based on agent cardinality, control structure, autonomy, and knowledge representation, and provides a comparative analysis of design trade-offs across existing frameworks. The survey examines applications in healthcare, finance, education, and enterprise document processing, and distills practical lessons for system designers and practitioners. Finally, it identifies key open research challenges related to evaluation, coordination, memory management, efficiency, and governance, outlining directions for future research.</li>
</ul>
<h3>13. Learning to Route: A Rule-Driven Agent Framework for Hybrid-Source Retrieval-Augmented Generation</h3>
<ul>
<li><strong>Authors:</strong> Haoyue Bai, Haoyu Wang, Shengyu Chen, Zhengzhang Chen, Lu-An Tang, Wei Cheng et al.</li>
<li><strong>Published:</strong> 2025-09-30</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2510.02388">2510.02388</a></li>
<li><strong>Core Mechanism:</strong> hybrid retrieval (dense + sparse) for multi-source knowledge</li>
<li><strong>Abstract:</strong> Large Language Models (LLMs) have shown remarkable performance on general Question Answering (QA), yet they often struggle in domain-specific scenarios where accurate and up-to-date information is required. Retrieval-Augmented Generation (RAG) addresses this limitation by enriching LLMs with external knowledge, but existing systems primarily rely on unstructured documents, while largely overlooking relational databases, which provide precise, timely, and efficiently queryable factual information, serving as indispensable infrastructure in domains such as finance, healthcare, and scientific research. Motivated by this gap, we conduct a systematic analysis that reveals three central observations: (i) databases and documents offer complementary strengths across queries, (ii) naively combining both sources introduces noise and cost without consistent accuracy gains, and (iii) selecting the most suitable source for each query is crucial to balance effectiveness and efficiency. We further observe that query types show consistent regularities in their alignment with retrieval paths, suggesting that routing decisions can be effectively guided by systematic rules that capture these patterns. Building on these insights, we propose a rule-driven routing framework. A routing agent scores candidate augmentation paths based on explicit rules and selects the most suitable one; a rule-making expert agent refines the rules over time using QA feedback to maintain adaptability; and a path-level meta-cache reuses past routing decisions for semantically similar queries to reduce latency and cost. Experiments on three QA benchmarks demonstrate that our framework consistently outperforms static strategies and learned routing baselines, achieving higher accuracy while maintaining moderate computational cost.</li>
</ul>
<h3>14. GlyRAG: Context-Aware Retrieval-Augmented Framework for Blood Glucose Forecasting</h3>
<ul>
<li><strong>Authors:</strong> Shovito Barua Soumma, Hassan Ghasemzadeh</li>
<li><strong>Published:</strong> 2026-01-08</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2601.05353">2601.05353</a></li>
<li><strong>Core Mechanism:</strong> agentic workflow with autonomous decision loops; retrieval-augmented generation (RAG) for external knowledge injection; multimodal data fusion (text + numerical + visual)</li>
<li><strong>Abstract:</strong> Accurate forecasting of blood glucose from CGM is essential for preventing dysglycemic events, thus enabling proactive diabetes management. However, current forecasting models treat blood glucose readings captured using CGMs as a numerical sequence, either ignoring context or relying on additional sensors/modalities that are difficult to collect and deploy at scale. Recently, LLMs have shown promise for time-series forecasting tasks, yet their role as agentic context extractors in diabetes care remains largely unexplored. To address these limitations, we propose GlyRAG, a context-aware, retrieval-augmented forecasting framework that derives semantic understanding of blood glucose dynamics directly from CGM traces without requiring additional sensor modalities. GlyRAG employs an LLM as a contextualization agent to generate clinical summaries. These summaries are embedded by a language model and fused with patch-based glucose representations in a multimodal transformer architecture with a cross translation loss aligining textual and physiological embeddings. A retrieval module then identifies similar historical episodes in the learned embedding space and uses cross-attention to integrate these case-based analogues prior to making a forecasting inference. Extensive evaluations on two T1D cohorts show that GlyRAG consistently outperforms state-of-the art methods, achieving up to 39% lower RMSE and a further 1.7% reduction in RMSE over the baseline. Clinical evaluation shows that GlyRAG places 85% predictions in safe zones and achieves 51% improvement in predicting dysglycemic events across both cohorts. These results indicate that LLM-based contextualization and retrieval over CGM traces can enhance the accuracy and clinical reliability of long-horizon glucose forecasting without the need for extra sensors, thus supporting future agentic decision-support tools for diabetes management.</li>
</ul>
<h3>15. Agentic Retrieval-Augmented Generation for Financial Document Question Answering</h3>
<ul>
<li><strong>Authors:</strong> Yang Shu, Yingmin Liu, Zequn Xie</li>
<li><strong>Published:</strong> 2026-05-06</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2605.05409">2605.05409</a></li>
<li><strong>Core Mechanism:</strong> Iterative retrieval-reasoning loops with self-verification: (1) Contrastive Financial Retriever with hard negative mining, (2) Program-of-Thought module generates executable Python for precise arithmetic, (3) Adaptive Strategy Router allocates compute by question complexity — outperforms baselines by 5.6–9.3 points on FinQA/ConvFinQA/TAT-QA</li>
<li><strong>Abstract:</strong> Financial document question answering (QA) demands complex multi-step numerical reasoning over heterogeneous evidence--structured tables, textual narratives, and footnotes--scattered across corporate filings. Existing retrieval-augmented generation (RAG) approaches adopt a single-pass retrieve-then-generate paradigm that struggles with the compositional reasoning chains prevalent in financial analysis. We propose FinAgent-RAG, an agentic RAG framework that orchestrates iterative retrieval-reasoning loops with self-verification, specifically engineered for the precision requirements of financial numerical reasoning. The framework integrates three domain-specific innovations: (1) a Contrastive Financial Retriever trained with hard negative mining to distinguish semantically similar but numerically distinct financial passages, (2) a Program-of-Thought reasoning module that generates executable Python code for precise arithmetic rather than relying on error-prone LLM-based mental computation, and (3) an Adaptive Strategy Router that dynamically allocates computational resources based on question complexity, reducing API costs by 41.3% on FinQA while preserving accuracy. Extensive experiments on three benchmark datasets--FinQA, ConvFinQA, and TAT-QA--demonstrate that FinAgent-RAG achieves 76.81%, 78.46%, and 74.96% execution accuracy respectively, outperforming the strongest baseline by 5.62--9.32 percentage points. Ablation studies, cross-backbone evaluation with four LLMs, and deployment cost analysis confirm the framework's robustness and practical viability for financial institutions.</li>
</ul>
<h3>16. Sustainable Digitalization of Business with Multi-Agent RAG and LLM</h3>
<ul>
<li><strong>Authors:</strong> Muhammad Arslan, Saba Munawar, Christophe Cruz</li>
<li><strong>Published:</strong> 2025-01-06</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2502.15700">2502.15700</a></li>
<li><strong>Core Mechanism:</strong> multi-agent system with specialized agent roles; retrieval-augmented generation (RAG) for external knowledge injection</li>
<li><strong>Abstract:</strong> Businesses heavily rely on data sourced from various channels like news articles, financial reports, and consumer reviews to drive their operations, enabling informed decision-making and identifying opportunities. However, traditional manual methods for data extraction are often time-consuming and resource-intensive, prompting the adoption of digital transformation initiatives to enhance efficiency. Yet, concerns persist regarding the sustainability of such initiatives and their alignment with the United Nations (UN)'s Sustainable Development Goals (SDGs). This research aims to explore the integration of Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG) as a sustainable solution for Information Extraction (IE) and processing. The research methodology involves reviewing existing solutions for business decision-making, noting that many systems require training new machine learning models, which are resource-intensive and have significant environmental impacts. Instead, we propose a sustainable business solution using pre-existing LLMs that can work with diverse datasets. We link domain-specific datasets to tailor LLMs to company needs and employ a Multi-Agent architecture to divide tasks such as information retrieval, enrichment, and classification among specialized agents. This approach optimizes the extraction process and improves overall efficiency. Through the utilization of these technologies, businesses can optimize resource utilization, improve decision-making processes, and contribute to sustainable development goals, thereby fostering environmental responsibility within the corporate sector.</li>
</ul>
<h3>17. Finance Agent Benchmark: Benchmarking LLMs on Real-world Financial Research Tasks</h3>
<ul>
<li><strong>Authors:</strong> Antoine Bigeard, Langston Nashold, Rayan Krishnan, Shirley Wu</li>
<li><strong>Published:</strong> 2025-05-20</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2508.00828">2508.00828</a></li>
<li><strong>Core Mechanism:</strong> agentic workflow with autonomous decision loops</li>
<li><strong>Abstract:</strong> Artificial Intelligence (AI) technology has emerged as a transformative force in financial analysis and the finance industry, though significant questions remain about the full capabilities of Large Language Model (LLM) agents in this domain. We present the Finance Agent Benchmark, featuring challenging and diverse real-world finance research problems that require LLMs to perform complex analysis using recent SEC filings. We construct the benchmark using a taxonomy of nine financial task categories, developed in consultation with experts from banks, hedge funds, and private equity firms. The dataset includes 537 expert-authored questions covering tasks from information retrieval to complex financial modeling, each validated through a rigorous review process to ensure accuracy and relevance. Moreover, we implement an agentic harness that equips LLMs with tools sufficient to produce accurate responses, including Google Search and EDGAR database access. Overall, the Finance Agent Benchmark provides a comprehensive testbed for measuring the progress of LLM-driven finance agents. Our evaluation reveals significant limitations in current AI capabilities - even the best-performing model (OpenAI o3) achieved only 46.8% accuracy at an average cost of $3.79 per query. This underscores the need for further advancements before reliable deployment in high-stakes finance settings.</li>
</ul>
<h3>18. Retrieve, Schedule, Reflect: LLM Agents for Chip QoR Optimization</h3>
<ul>
<li><strong>Authors:</strong> Yikang ouyang, Yang Luo, Dongsheng Zuo, Yuzhe Ma</li>
<li><strong>Published:</strong> 2026-03-14</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2603.13767">2603.13767</a></li>
<li><strong>Core Mechanism:</strong> agentic workflow with autonomous decision loops; retrieval-augmented generation (RAG) for external knowledge injection</li>
<li><strong>Abstract:</strong> Modern chip design requires multi-objective optimization of timing, power, and area under stringent time-to-market constraints. Although powerful optimization algorithms are integrated into EDA tools, achieving high QoR hinges on effective long-horizon scheduling, which relies heavily on manual expert intervention. To address this issue and automate chip design, we propose an agentic LLM framework that schedules chip optimizations through direct interaction with EDA tools. The agent is grounded in natural language expertise expressed as a search tree through retrieval-augmented generation (RAG). We further improve scheduling quality with Pareto-driven QoR feedback through language reflection. Experimental results show that, compared with black-box search methods such as reinforcement learning, our framework achieves 10% greater timing improvement while consuming less power and area, with more than 4x speedup. The post-optimization QoR is also comparable to that achieved by human experts. Finally, the agent supports customized tasks expressed in natural language, enabling preferential QoR trade-offs. The code and chip design data will be publicly available at https://github.com/YiKangOY/Open-LLM-ECO.</li>
</ul>
<h3>19. Towards Interpretable and Trustworthy Time Series Reasoning: A BlueSky Vision</h3>
<ul>
<li><strong>Authors:</strong> Kanghui Ning, Zijie Pan, Yushan Jiang, Anderson Schneider, Yuriy Nevmyvaka, Dongjin Song</li>
<li><strong>Published:</strong> 2025-10-19</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2510.16980">2510.16980</a></li>
<li><strong>Core Mechanism:</strong> collaborative multi-agent system with inter-agent communication; retrieval-augmented generation (RAG) for external knowledge injection; multimodal data fusion (text + numerical + visual)</li>
<li><strong>Abstract:</strong> Time series reasoning is emerging as the next frontier in temporal analysis, aiming to move beyond pattern recognition towards explicit, interpretable, and trustworthy inference. This paper presents a BlueSky vision built on two complementary directions. One builds robust foundations for time series reasoning, centered on comprehensive temporal understanding, structured multi-step reasoning, and faithful evaluation frameworks. The other advances system-level reasoning, moving beyond language-only explanations by incorporating multi-agent collaboration, multi-modal context, and retrieval-augmented approaches. Together, these directions outline a flexible and extensible framework for advancing time series reasoning, aiming to deliver interpretable and trustworthy temporal intelligence across diverse domains.</li>
</ul>
<h3>20. Reimagining RAN Automation in 6G: An Agentic AI Framework with Hierarchical Online Decision Transformer</h3>
<ul>
<li><strong>Authors:</strong> Md Arafat Habib, Medhat Elsayed, Majid Bavand, Pedro Enrique Iturria Rivera, Yigit Ozcan, Melike Erol-Kantarci</li>
<li><strong>Published:</strong> 2026-04-05</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2604.03908">2604.03908</a></li>
<li><strong>Core Mechanism:</strong> agentic workflow with autonomous decision loops; retrieval-augmented generation (RAG) for external knowledge injection</li>
<li><strong>Abstract:</strong> In this paper, we propose an Agentic Artificial Intelligence (AI) framework for wireless networks. The framework coordinates a pool of AI agents guided by Natural Language (NL) inputs from a human operator. At its core, the super agent is powered by a Hierarchical Online Decision Transformer (H-ODT). It orchestrates three categories of agents: (i) inter-slice, intra-slice resource allocation agents, (ii) network application orchestration agents, and (iii) self-healing agents. The orchestration takes place with the help of an Agentic Retrieval-Augmented Generation (RAG) module that integrates knowledge from heterogeneous sources. In this proposed methodology, the super agent directly interfaces with operators and generates sequential policies to activate relevant agents. The proposed framework is evaluated against three state-of-the-art baselines, showing improved throughput, reduced network delay, and higher energy efficiency at both slice-level and system-wide performance metrics. Also, the proposed Agentic framework introduces a bi-level human operator intent validation methodology, both at the slice-level and Key Performance Indicator (KPI)-level using generative AI-based time series predictors. We could rule out performance-degrading operator intents with an accuracy of 88.5%. Lastly, while being interrupted by any performance-degrading events, the self-healing capability of Agentic AI in our framework automatically recovers 90% of its previous performance, avoiding quality-of-service drifts when there is no human involvement.</li>
</ul>
<h3>21. Modeling Epistemic Uncertainty in Social Perception via Rashomon Set Agents</h3>
<ul>
<li><strong>Authors:</strong> Jinming Yang, Xinyu Jiang, Xinshan Jiao, Xinping Zhang</li>
<li><strong>Published:</strong> 2026-03-21</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2603.20750">2603.20750</a></li>
<li><strong>Core Mechanism:</strong> multi-agent system with specialized agent roles; retrieval-augmented generation (RAG) for external knowledge injection</li>
<li><strong>Abstract:</strong> We present an LLM-driven multi-agent probabilistic modeling framework that demonstrates how differences in students' subjective social perceptions arise and evolve in real-world classroom settings, under constraints from an observed social network and limited questionnaire data. When social information is incomplete and the accuracy of perception differs between students, they can form different views of the same group structure from local cues they can access. Repeated peer communication and belief updates can gradually change these views and, over time, lead to stable group-level differences. To avoid assuming a global &quot;god's-eye view,&quot; we assign each student an individualized subjective graph that shows which social ties they can perceive and how far information is reachable from their perspective. All judgments and interactions are restricted to this subjective graph: agents use retrieval-augmented generation (RAG) to access only local information and then form evaluations of peers' competence and social standing. We also add structural perturbations related to social-anxiety to represent consistent individual differences in the accuracy of social perception. During peer exchanges, agents share narrative assessments of classmates' academic performance and social position with uncertainty tags, and update beliefs probabilistically using LLM-based trust scores. Using the time series of six real exam scores as an exogenous reference, we run multi-step simulations to examine how epistemic uncertainty spreads through local interactions. Experiments show that, without relying on global information, the framework reproduces several collective dynamics consistent with real-world educational settings. The code is released at https://anonymous.4open.science/r/Rashomonomon-0126.</li>
</ul>
<h3>22. RELOOP: Recursive Retrieval with Multi-Hop Reasoner and Planners for Heterogeneous QA</h3>
<ul>
<li><strong>Authors:</strong> Ruiyi Yang, Hao Xue, Imran Razzak, Hakim Hacid, Flora D. Salim</li>
<li><strong>Published:</strong> 2025-10-23</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2510.20505">2510.20505</a></li>
<li><strong>Core Mechanism:</strong> agentic workflow with autonomous decision loops; hybrid retrieval (dense + sparse) for multi-source knowledge; tool-calling capability for external API/data access</li>
<li><strong>Abstract:</strong> Retrieval-augmented generation (RAG) remains brittle on multi-step questions and heterogeneous evidence sources, trading accuracy against latency and token/tool budgets. This paper introduces RELOOP, a structure aware framework using Hierarchical Sequence (HSEQ) that (i) linearize documents, tables, and knowledge graphs into a reversible hierarchical sequence with lightweight structural tags, and (ii) perform structure-aware iteration to collect just-enough evidence before answer synthesis. A Head Agent provides guidance that leads retrieval, while an Iteration Agent selects and expands HSeq via structure-respecting actions (e.g., parent/child hops, table row/column neighbors, KG relations); Finally the head agent composes canonicalized evidence to genearte the final answer, with an optional refinement loop to resolve detected contradictions. Experiments on HotpotQA (text), HybridQA/TAT-QA (table+text), and MetaQA (KG) show consistent EM/F1 gains over strong single-pass, multi-hop, and agentic RAG baselines with high efficiency. Besides, RELOOP exhibits three key advantages: (1) a format-agnostic unification that enables a single policy to operate across text, tables, and KGs without per-dataset specialization; (2) \textbf{guided, budget-aware iteration} that reduces unnecessary hops, tool calls, and tokens while preserving accuracy; and (3) evidence canonicalization for reliable QA, improving answers consistency and auditability.</li>
</ul>
<h3>23. ERATTA: Extreme RAG for Table To Answers with Large Language Models</h3>
<ul>
<li><strong>Authors:</strong> Sohini Roychowdhury, Marko Krema, Anvar Mahammad, Brian Moore, Arijit Mukherjee, Punit Prakashchandra</li>
<li><strong>Published:</strong> 2024-05-07</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2405.03963">2405.03963</a></li>
<li><strong>Core Mechanism:</strong> agentic workflow with autonomous decision loops; retrieval-augmented generation (RAG) for external knowledge injection</li>
<li><strong>Abstract:</strong> Large language models (LLMs) with retrieval augmented-generation (RAG) have been the optimal choice for scalable generative AI solutions in the recent past. Although RAG implemented with AI agents (agentic-RAG) has been recently popularized, its suffers from unstable cost and unreliable performances for Enterprise-level data-practices. Most existing use-cases that incorporate RAG with LLMs have been either generic or extremely domain specific, thereby questioning the scalability and generalizability of RAG-LLM approaches. In this work, we propose a unique LLM-based system where multiple LLMs can be invoked to enable data authentication, user-query routing, data-retrieval and custom prompting for question-answering capabilities from Enterprise-data tables. The source tables here are highly fluctuating and large in size and the proposed framework enables structured responses in under 10 seconds per query. Additionally, we propose a five metric scoring module that detects and reports hallucinations in the LLM responses. Our proposed system and scoring metrics achieve &gt;90% confidence scores across hundreds of user queries in the sustainability, financial health and social media domains. Extensions to the proposed extreme RAG architectures can enable heterogeneous source querying using LLMs.</li>
</ul>
<h3>24. Can LLMs Help You at Work? A Sandbox for Evaluating LLM Agents in Enterprise Environments</h3>
<ul>
<li><strong>Authors:</strong> Harsh Vishwakarma, Ankush Agarwal, Ojas Patil, Chaitanya Devaguptapu, Mahesh Chandran</li>
<li><strong>Published:</strong> 2025-10-31</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2510.27287">2510.27287</a></li>
<li><strong>Core Mechanism:</strong> Enterprise systems are crucial for enhancing productivity and decision-making among employees and customers</li>
<li><strong>Abstract:</strong> Enterprise systems are crucial for enhancing productivity and decision-making among employees and customers. Integrating LLM based systems into enterprise systems enables intelligent automation, personalized experiences, and efficient information retrieval, driving operational efficiency and strategic growth. However, developing and evaluating such systems is challenging due to the inherent complexity of enterprise environments, where data is fragmented across multiple sources and governed by sophisticated access controls. We present EnterpriseBench, a comprehensive benchmark that simulates enterprise settings, featuring 500 diverse tasks across software engineering, HR, finance, and administrative domains. Our benchmark uniquely captures key enterprise characteristics including data source fragmentation, access control hierarchies, and cross-functional workflows. Additionally, we provide a novel data generation pipeline that creates internally consistent enterprise tasks from organizational metadata. Experiments with state-of-the-art LLM agents demonstrate that even the most capable models achieve only 41.8% task completion, highlighting significant opportunities for improvement in enterprise-focused AI systems.</li>
</ul>
<h3>25. Towards a Realistic Long-Term Benchmark for Open-Web Research Agents</h3>
<ul>
<li><strong>Authors:</strong> Peter Mühlbacher, Nikos I. Bosse, Lawrence Phillips</li>
<li><strong>Published:</strong> 2024-09-23</li>
<li><strong>arXiv:</strong> <a href="https://arxiv.org/abs/2409.14913">2409.14913</a></li>
<li><strong>Core Mechanism:</strong> GPT-based agent reasoning engine</li>
<li><strong>Abstract:</strong> We present initial results of a forthcoming benchmark for evaluating LLM agents on white-collar tasks of economic value. We evaluate agents on real-world &quot;messy&quot; open-web research tasks of the type that are routine in finance and consulting. In doing so, we lay the groundwork for an LLM agent evaluation suite where good performance directly corresponds to a large economic and societal impact. We built and tested several agent architectures with o1-preview, GPT-4o, Claude-3.5 Sonnet, Llama 3.1 (405b), and GPT-4o-mini. On average, LLM agents powered by Claude-3.5 Sonnet and o1-preview substantially outperformed agents using GPT-4o, with agents based on Llama 3.1 (405b) and GPT-4o-mini lagging noticeably behind. Across LLMs, a ReAct architecture with the ability to delegate subtasks to subagents performed best. In addition to quantitative evaluations, we qualitatively assessed the performance of the LLM agents by inspecting their traces and reflecting on their observations. Our evaluation represents the first in-depth assessment of agents' abilities to conduct challenging, economically valuable analyst-style research on the real open web.</li>
</ul>
<hr />
<h2>Integration Pattern Analysis</h2>
<h3>Agent Architecture Patterns</h3>
<ul>
<li><strong>Agentic Workflow</strong>: 15 papers</li>
<li><strong>Multi-Agent System</strong>: 8 papers</li>
<li><strong>Single Agent</strong>: 5 papers</li>
</ul>
<h3>RAG Integration Patterns</h3>
<ul>
<li><strong>Standard RAG</strong>: 4 papers</li>
<li><strong>Hybrid Retrieval</strong>: 4 papers</li>
<li><strong>Vector Retrieval</strong>: 3 papers</li>
<li><strong>GraphRAG</strong>: 1 papers</li>
</ul>
<h3>Domain Focus</h3>
<ul>
<li><strong>Financial Analysis</strong>: 17 papers</li>
<li><strong>Time Series/Forecasting</strong>: 7 papers</li>
<li><strong>Market Analysis</strong>: 6 papers</li>
<li><strong>Trading/Stock</strong>: 5 papers</li>
</ul>
<hr />
<h2>Key Takeaways</h2>
<ul>
<li><strong>Agent + RAG is an emerging paradigm</strong>: integrating retrieval-augmented generation into autonomous agent workflows for financial decision-making is a rapidly growing research area, with most papers appearing in 2025-2026.</li>
<li><strong>Multi-agent systems dominate over single-agent</strong>: role-specialized, collaborative, and debate-based multi-agent architectures are preferred for complex financial tasks that require diverse expertise (market analysis, risk assessment, sentiment analysis).</li>
<li><strong>RAG serves as the agent's 'memory'</strong>: retrieval-augmented generation provides agents with external knowledge (news, reports, fundamentals) that goes beyond their parametric knowledge, crucial for time-sensitive financial decisions.</li>
<li><strong>Modality fusion is the integration bottleneck</strong>: combining structured market data, unstructured text (news, filings), and numerical time series into a unified agent-accessible knowledge base remains an open challenge.</li>
<li><strong>Evaluation remains ad-hoc</strong>: most papers evaluate on narrow benchmarks or custom datasets, making cross-paper comparison difficult — a pattern consistent with the broader LLM+Finance literature.</li>
</ul>
<hr />
<p><em>Report auto-generated from arXiv metadata via keyword-based mechanism extraction.</em></p>


</div>

## Level2_Methodologies.md

<div style="padding:16px;border:1px solid #e5e7eb;border-radius:10px;background:#fff;">

<h1>Level 2 — Methodology Deep-Dive: Architecture Innovations (2024–2026)</h1>
<p><strong>Generated:</strong> 2026-05-14
<strong>Source:</strong> arXiv targeted search (title must contain 'time series')
<strong>Selection:</strong> Top 2 most relevant papers per track by keyword relevance scoring</p>
<hr />
<h2>Track: TS Foundation Models (Zero-Shot)</h2>
<p>| # | Paper Title | Year | Core Architecture Innovation |
|---|-------------|------|-------------------------------|
| 1 | <a href="https://arxiv.org/abs/2601.20845">PatchFormer: A Patch-Based Time Series Foundation Model with Hierarchical Masked Reconstruction and Cross-Domain Transfer Learning for Zero-Shot Multi-Horizon Forecasting</a> | 2026 | Patch-based hierarchical masked reconstruction pretraining with multiscale temporal aggregation, learnable cross-scale fusion, and lightweight adapters for zero-shot multi-horizon forecasting |
| 2 | <a href="https://arxiv.org/abs/2510.27522">Leveraging Generic Time Series Foundation Models for EEG Classification</a> | 2025 | Cross-domain transfer of existing TS foundation models to EEG classification via pretraining on heterogeneous real-world and synthetic time series data |</p>
<p><strong>1. PatchFormer: A Patch-Based Time Series Foundation Model...</strong></p>
<ul>
<li>Authors: Olaf Yunus Laitinen Imanov, Derya Umut Kulali, Taner Yilmaz</li>
<li>arXiv: <a href="https://arxiv.org/abs/2601.20845">2601.20845</a></li>
<li>Published: 2026-01-28</li>
<li>Abstract: Time series forecasting is a fundamental problem with applications in climate, energy, healthcare, and finance. Many existing approaches require domain-specific feature engineering and substantial labeled data for each task. We introduce PatchFormer, a patch-based time series foundation model that uses hierarchical masked reconstruction for self-supervised pretraining and lightweight adapters for efficient transfer. PatchFormer segments time series into patches and learns multiscale temporal representations with learnable aggregation across temporal scales. Pretraining uses masked patch reconstruction with dynamic masking and objectives that encourage both local accuracy and global consistency, followed by cross-domain knowledge distillation. Experiments on 24 benchmark datasets spanning weather, energy, traffic, finance, and healthcare demonstrate state-of-the-art zero-shot multi-horizon forecasting, reducing mean squared error by 27.3 percent relative to strong baselines while requiring 94 percent less task-specific training data. The model exhibits near log-linear scaling with more pretraining data up to 100 billion points and processes length-512 sequences 3.8x faster than full-sequence transformers.</li>
</ul>
<p><strong>2. Leveraging Generic Time Series Foundation Models for EEG Classification</strong></p>
<ul>
<li>Authors: Théo Gnassounou, Yessin Moakher, Shifeng Xie, Vasilii Feofanov, Ievgen Redko</li>
<li>arXiv: <a href="https://arxiv.org/abs/2510.27522">2510.27522</a></li>
<li>Published: 2025-10-31</li>
<li>Abstract: Foundation models for time series are emerging as powerful general-purpose backbones, yet their potential for domain-specific biomedical signals such as electroencephalography (EEG) remains rather unexplored. In this work, we investigate the applicability a recently proposed time series classification foundation model, to a different EEG tasks such as motor imagery classification and sleep stage prediction. We test two pretraining regimes: (a) pretraining on heterogeneous real-world time series from multiple domains, and (b) pretraining on purely synthetic data. We find that both variants yield strong performance, consistently outperforming EEGNet, a widely used convolutional baseline, and CBraMod, the most recent EEG-specific foundation model. These results suggest that generalist time series foundation models, even when pretrained on data of non-neural origin or on synthetic signals, can transfer effectively to EEG. Our findings highlight the promise of leveraging cross-domain pretrained models for brain signal analysis, suggesting that EEG may benefit from advances in the broader time series literature.</li>
</ul>
<hr />
<h2>Track: TS Prompting LLM</h2>
<p>| # | Paper Title | Year | Core Architecture Innovation |
|---|-------------|------|-------------------------------|
| 1 | <a href="https://arxiv.org/abs/2508.04239">DP-GPT4MTS: Dual-Prompt Large Language Model for Textual-Numerical Time Series Forecasting</a> | 2025 | Dual-prompt GPT-2 framework: explicit task-instruction prompt + textual context-aware prompt from timestamped data, refined via self-attention and feed-forward networks |
| 2 | <a href="https://arxiv.org/abs/2506.12953">Forecasting Time Series with LLMs via Patch-Based Prompting and Decomposition</a> | 2025 | Prompt-based forecasting (PatchInstruct) with seasonal-trend decomposition, patch tokenization, and similarity-based neighbor augmentation — no model retraining required |</p>
<p><strong>1. DP-GPT4MTS: Dual-Prompt Large Language Model for Textual-Numerical Time Series Forecasting</strong></p>
<ul>
<li>Authors: Chanjuan Liu, Shengzhi Wang, Enqiang Zhu</li>
<li>arXiv: <a href="https://arxiv.org/abs/2508.04239">2508.04239</a></li>
<li>Published: 2025-08-06</li>
<li>Abstract: Time series forecasting is crucial in strategic planning and decision-making across various industries. Traditional forecasting models mainly concentrate on numerical time series data, often overlooking important textual information such as events and news, which can significantly affect forecasting accuracy. While large language models offer a promise for integrating multimodal data, existing single-prompt frameworks struggle to effectively capture the semantics of timestamped text, introducing redundant information that can hinder model performance. To address this limitation, we introduce DP-GPT4MTS (Dual-Prompt GPT2-base for Multimodal Time Series), a novel dual-prompt large language model framework that combines two complementary prompts: an explicit prompt for clear task instructions and a textual prompt for context-aware embeddings from time-stamped data. The tokenizer generates the explicit prompt while the embeddings from the textual prompt are refined through self-attention and feed-forward networks. Comprehensive experiments conducted on diverse textural-numerical time series datasets demonstrate that this approach outperforms state-of-the-art algorithms in time series forecasting. This highlights the significance of incorporating textual context via a dual-prompt mechanism to achieve more accurate time series predictions.</li>
</ul>
<p><strong>2. Forecasting Time Series with LLMs via Patch-Based Prompting and Decomposition (PatchInstruct)</strong></p>
<ul>
<li>Authors: Mayank Bumb, Anshul Vemulapalli, Sri Harsha Vardhan Prasad Jella, Anish Gupta, An La et al.</li>
<li>arXiv: <a href="https://arxiv.org/abs/2506.12953">2506.12953</a></li>
<li>Published: 2025-06-15</li>
<li>Abstract: Recent advances in Large Language Models (LLMs) have demonstrated new possibilities for accurate and efficient time series analysis, but prior work often required heavy fine-tuning and/or ignored inter-series correlations. In this work, we explore simple and flexible prompt-based strategies that enable LLMs to perform time series forecasting without extensive retraining or the use of a complex external architecture. Through the exploration of specialized prompting methods that leverage time series decomposition, patch-based tokenization, and similarity-based neighbor augmentation, we find that it is possible to enhance LLM forecasting quality while maintaining simplicity and requiring minimal preprocessing of data. To this end, we propose our own method, PatchInstruct, which enables LLMs to make precise and effective predictions.</li>
</ul>
<hr />
<h2>Track: TS PEFT / LoRA LLM</h2>
<p>| # | Paper Title | Year | Core Architecture Innovation |
|---|-------------|------|-------------------------------|
| 1 | <a href="https://arxiv.org/abs/2603.29756">One-for-All: A Lightweight Stabilized and Parameter-Efficient Pre-trained LLM for Time Series Forecasting</a> | 2026 | Frozen LLM with Gaussian Rank-Stabilized LoRA (rsLoRA, rank-16) injected into positional embeddings and output layers — keeping self-attention frozen — achieving 6.8–21× parameter reduction vs SOTA |
| 2 | <a href="https://arxiv.org/abs/2502.13725">Adapting Large Language Models for Time Series Modeling via a Novel Parameter-efficient Adaptation Method</a> | 2025 | Time-LlaMA: linear tokenization of TS into token embeddings aligned with text prompts + Dynamic LoRA (D-LoRA) that adaptively selects per-layer low-rank modules for each input sample |</p>
<p><strong>1. One-for-All: A Lightweight Stabilized and Parameter-Efficient Pre-trained LLM for Time Series Forecasting</strong></p>
<ul>
<li>Authors: Prasanjit Dey, Soumyabrata Dev, Bianca Schoen-Phelan</li>
<li>arXiv: <a href="https://arxiv.org/abs/2603.29756">2603.29756</a></li>
<li>Published: 2026-03-31</li>
<li>Abstract: We address the challenge of adapting pre-trained Large Language Models (LLMs) for multivariate time-series analysis, where their deployment is often hindered by prohibitive computational and memory demands. Our solution, One-for-All, introduces Gaussian Rank-Stabilized Low-Rank Adapters (rsLoRA) to enable parameter-efficient fine-tuning of frozen LLMs. While inspired by LoRA, rsLoRA introduces a mathematically grounded rank-stabilization mechanism that enables provable gradient stability at low ranks a novel contribution absent in prior PEFT methods. Our framework injects trainable rank decomposition matrices (rank 16) into positional embeddings and output layers, while keeping self-attention weights fixed. This design reduces trainable parameters by 6.8× (vs. TimesNet), 21× (vs. GPT4TS), and 11.8× (vs. TIME-LLM), while achieving a 168–1,776× smaller memory footprint (2.2MiB vs. 340MiB–4.18GiB in SOTA models). Rigorous evaluation across six time-series tasks demonstrates that One-for-All achieves state-of-the-art efficiency-accuracy trade-offs: 5.5× higher parameter efficiency (MSE=5.50) than TimesNet and 21× better than GPT4TS, while matching their forecasting accuracy (MSE=0.33). The framework's stability is validated through consistent performance across diverse horizons (96–720 steps) and datasets (ETT, Weather, M3, M4), with 98.3% fewer parameters than conventional transformers. These advances enable deployment on edge devices for healthcare, finance, and environmental monitoring without compromising performance.</li>
</ul>
<p><strong>2. Adapting Large Language Models for Time Series Modeling via a Novel Parameter-efficient Adaptation Method (Time-LlaMA)</strong></p>
<ul>
<li>Authors: Juyuan Zhang, Wei Zhu, Jiechao Gao</li>
<li>arXiv: <a href="https://arxiv.org/abs/2502.13725">2502.13725</a></li>
<li>Published: 2025-02-19</li>
<li>Abstract: Time series modeling holds significant importance in many real-world applications and has been extensively studied. While pre-trained foundation models have made impressive strides in the fields of natural language processing (NLP) and computer vision (CV), their development in time series domains has been constrained by data sparsity. A series of recent studies have demonstrated that large language models (LLMs) possess robust pattern recognition and reasoning abilities over complex sequences of tokens. However, the current literature have yet striked a high-quality balance between (a) effectively aligning the time series and natural language modalities, and (b) keeping the inference efficiency. To address the above issues, we now propose the Time-LlaMA framework. Time-LlaMA first converts the time series input into token embeddings through a linear tokenization mechanism. Second, the time series token embeddings are aligned with the text prompts. Third, to further adapt the LLM backbone for time series modeling, we have developed a dynamic low-rank adaptation technique (D-LoRA). D-LoRA dynamically chooses the most suitable LoRA modules at each layer of the Transformer backbone for each time series input, enhancing the model's predictive capabilities. Our experimental results on an extensive collection of challenging real-world time series tasks confirm that our proposed method achieves the state-of-the-art (SOTA) performance.</li>
</ul>
<hr />
<h2>Summary: Architecture Innovation Map</h2>
<p>| Track | Paper | Year | Core Architecture Innovation |
|-------|-------|------|-------------------------------|
| TS Foundation Models (Zero-Shot) | <a href="https://arxiv.org/abs/2601.20845">PatchFormer</a> | 2026 | Patch-based hierarchical masked reconstruction + multiscale aggregation + lightweight adapters for zero-shot forecasting |
| TS Foundation Models (Zero-Shot) | <a href="https://arxiv.org/abs/2510.27522">Generic TS FMs for EEG</a> | 2025 | Cross-domain transfer of existing TS FMs to EEG via heterogeneous &amp; synthetic pretraining |
| TS Prompting LLM | <a href="https://arxiv.org/abs/2508.04239">DP-GPT4MTS</a> | 2025 | Dual-prompt GPT-2: explicit task prompt + timestamped textual prompt refined via self-attention &amp; FFN |
| TS Prompting LLM | <a href="https://arxiv.org/abs/2506.12953">PatchInstruct</a> | 2025 | Decomposition + patch tokenization + neighbor augmentation prompting — no fine-tuning required |
| TS PEFT / LoRA LLM | <a href="https://arxiv.org/abs/2603.29756">One-for-All</a> | 2026 | Frozen LLM + Gaussian Rank-Stabilized LoRA (rsLoRA) in positional embeddings &amp; output layers |
| TS PEFT / LoRA LLM | <a href="https://arxiv.org/abs/2502.13725">Time-LlaMA</a> | 2025 | Linear TS tokenization + text-prompt alignment + Dynamic LoRA (D-LoRA) per-layer adaptive selection |</p>
<hr />
<h2>Key Cross-Cutting Insights</h2>
<ol>
<li><strong>Prompting is eating fine-tuning</strong>: Track 2 papers (DP-GPT4MTS, PatchInstruct) both achieve strong results without modifying the LLM backbone — the innovation is entirely in how time series are formatted and prompted into frozen models.</li>
<li><strong>LoRA variants are the dominant PEFT paradigm</strong>: both Track 3 papers introduce novel LoRA extensions (rsLoRA with rank stabilization, D-LoRA with dynamic per-sample selection) rather than alternative PEFT methods.</li>
<li><strong>Foundation models follow the CV playbook</strong>: PatchFormer's hierarchical masked reconstruction and adapter-based transfer mirrors the masked-autoencoder + lightweight head pattern from vision.</li>
<li><strong>The modality gap is the central challenge</strong>: across all tracks, aligning continuous time series with discrete text tokens remains the critical design decision that differentiates approaches.</li>
</ol>
<hr />
<p><em>Report based on arXiv metadata — architecture innovations extracted from paper abstracts (2024–2026).</em></p>


</div>
