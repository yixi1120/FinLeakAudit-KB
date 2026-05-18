# Level 2 — Methodology Deep-Dive: Architecture Innovations (2024–2026)

**Generated:** 2026-05-14
**Source:** arXiv targeted search (title must contain 'time series')
**Selection:** Top 2 most relevant papers per track by keyword relevance scoring

---

## Track: TS Foundation Models (Zero-Shot)

| # | Paper Title | Year | Core Architecture Innovation |
|---|-------------|------|-------------------------------|
| 1 | [PatchFormer: A Patch-Based Time Series Foundation Model with Hierarchical Masked Reconstruction and Cross-Domain Transfer Learning for Zero-Shot Multi-Horizon Forecasting](https://arxiv.org/abs/2601.20845) | 2026 | Patch-based hierarchical masked reconstruction pretraining with multiscale temporal aggregation, learnable cross-scale fusion, and lightweight adapters for zero-shot multi-horizon forecasting |
| 2 | [Leveraging Generic Time Series Foundation Models for EEG Classification](https://arxiv.org/abs/2510.27522) | 2025 | Cross-domain transfer of existing TS foundation models to EEG classification via pretraining on heterogeneous real-world and synthetic time series data |

**1. PatchFormer: A Patch-Based Time Series Foundation Model...**
- Authors: Olaf Yunus Laitinen Imanov, Derya Umut Kulali, Taner Yilmaz
- arXiv: [2601.20845](https://arxiv.org/abs/2601.20845)
- Published: 2026-01-28
- Abstract: Time series forecasting is a fundamental problem with applications in climate, energy, healthcare, and finance. Many existing approaches require domain-specific feature engineering and substantial labeled data for each task. We introduce PatchFormer, a patch-based time series foundation model that uses hierarchical masked reconstruction for self-supervised pretraining and lightweight adapters for efficient transfer. PatchFormer segments time series into patches and learns multiscale temporal representations with learnable aggregation across temporal scales. Pretraining uses masked patch reconstruction with dynamic masking and objectives that encourage both local accuracy and global consistency, followed by cross-domain knowledge distillation. Experiments on 24 benchmark datasets spanning weather, energy, traffic, finance, and healthcare demonstrate state-of-the-art zero-shot multi-horizon forecasting, reducing mean squared error by 27.3 percent relative to strong baselines while requiring 94 percent less task-specific training data. The model exhibits near log-linear scaling with more pretraining data up to 100 billion points and processes length-512 sequences 3.8x faster than full-sequence transformers.

**2. Leveraging Generic Time Series Foundation Models for EEG Classification**
- Authors: Théo Gnassounou, Yessin Moakher, Shifeng Xie, Vasilii Feofanov, Ievgen Redko
- arXiv: [2510.27522](https://arxiv.org/abs/2510.27522)
- Published: 2025-10-31
- Abstract: Foundation models for time series are emerging as powerful general-purpose backbones, yet their potential for domain-specific biomedical signals such as electroencephalography (EEG) remains rather unexplored. In this work, we investigate the applicability a recently proposed time series classification foundation model, to a different EEG tasks such as motor imagery classification and sleep stage prediction. We test two pretraining regimes: (a) pretraining on heterogeneous real-world time series from multiple domains, and (b) pretraining on purely synthetic data. We find that both variants yield strong performance, consistently outperforming EEGNet, a widely used convolutional baseline, and CBraMod, the most recent EEG-specific foundation model. These results suggest that generalist time series foundation models, even when pretrained on data of non-neural origin or on synthetic signals, can transfer effectively to EEG. Our findings highlight the promise of leveraging cross-domain pretrained models for brain signal analysis, suggesting that EEG may benefit from advances in the broader time series literature.

---

## Track: TS Prompting LLM

| # | Paper Title | Year | Core Architecture Innovation |
|---|-------------|------|-------------------------------|
| 1 | [DP-GPT4MTS: Dual-Prompt Large Language Model for Textual-Numerical Time Series Forecasting](https://arxiv.org/abs/2508.04239) | 2025 | Dual-prompt GPT-2 framework: explicit task-instruction prompt + textual context-aware prompt from timestamped data, refined via self-attention and feed-forward networks |
| 2 | [Forecasting Time Series with LLMs via Patch-Based Prompting and Decomposition](https://arxiv.org/abs/2506.12953) | 2025 | Prompt-based forecasting (PatchInstruct) with seasonal-trend decomposition, patch tokenization, and similarity-based neighbor augmentation — no model retraining required |

**1. DP-GPT4MTS: Dual-Prompt Large Language Model for Textual-Numerical Time Series Forecasting**
- Authors: Chanjuan Liu, Shengzhi Wang, Enqiang Zhu
- arXiv: [2508.04239](https://arxiv.org/abs/2508.04239)
- Published: 2025-08-06
- Abstract: Time series forecasting is crucial in strategic planning and decision-making across various industries. Traditional forecasting models mainly concentrate on numerical time series data, often overlooking important textual information such as events and news, which can significantly affect forecasting accuracy. While large language models offer a promise for integrating multimodal data, existing single-prompt frameworks struggle to effectively capture the semantics of timestamped text, introducing redundant information that can hinder model performance. To address this limitation, we introduce DP-GPT4MTS (Dual-Prompt GPT2-base for Multimodal Time Series), a novel dual-prompt large language model framework that combines two complementary prompts: an explicit prompt for clear task instructions and a textual prompt for context-aware embeddings from time-stamped data. The tokenizer generates the explicit prompt while the embeddings from the textual prompt are refined through self-attention and feed-forward networks. Comprehensive experiments conducted on diverse textural-numerical time series datasets demonstrate that this approach outperforms state-of-the-art algorithms in time series forecasting. This highlights the significance of incorporating textual context via a dual-prompt mechanism to achieve more accurate time series predictions.

**2. Forecasting Time Series with LLMs via Patch-Based Prompting and Decomposition (PatchInstruct)**
- Authors: Mayank Bumb, Anshul Vemulapalli, Sri Harsha Vardhan Prasad Jella, Anish Gupta, An La et al.
- arXiv: [2506.12953](https://arxiv.org/abs/2506.12953)
- Published: 2025-06-15
- Abstract: Recent advances in Large Language Models (LLMs) have demonstrated new possibilities for accurate and efficient time series analysis, but prior work often required heavy fine-tuning and/or ignored inter-series correlations. In this work, we explore simple and flexible prompt-based strategies that enable LLMs to perform time series forecasting without extensive retraining or the use of a complex external architecture. Through the exploration of specialized prompting methods that leverage time series decomposition, patch-based tokenization, and similarity-based neighbor augmentation, we find that it is possible to enhance LLM forecasting quality while maintaining simplicity and requiring minimal preprocessing of data. To this end, we propose our own method, PatchInstruct, which enables LLMs to make precise and effective predictions.

---

## Track: TS PEFT / LoRA LLM

| # | Paper Title | Year | Core Architecture Innovation |
|---|-------------|------|-------------------------------|
| 1 | [One-for-All: A Lightweight Stabilized and Parameter-Efficient Pre-trained LLM for Time Series Forecasting](https://arxiv.org/abs/2603.29756) | 2026 | Frozen LLM with Gaussian Rank-Stabilized LoRA (rsLoRA, rank-16) injected into positional embeddings and output layers — keeping self-attention frozen — achieving 6.8–21× parameter reduction vs SOTA |
| 2 | [Adapting Large Language Models for Time Series Modeling via a Novel Parameter-efficient Adaptation Method](https://arxiv.org/abs/2502.13725) | 2025 | Time-LlaMA: linear tokenization of TS into token embeddings aligned with text prompts + Dynamic LoRA (D-LoRA) that adaptively selects per-layer low-rank modules for each input sample |

**1. One-for-All: A Lightweight Stabilized and Parameter-Efficient Pre-trained LLM for Time Series Forecasting**
- Authors: Prasanjit Dey, Soumyabrata Dev, Bianca Schoen-Phelan
- arXiv: [2603.29756](https://arxiv.org/abs/2603.29756)
- Published: 2026-03-31
- Abstract: We address the challenge of adapting pre-trained Large Language Models (LLMs) for multivariate time-series analysis, where their deployment is often hindered by prohibitive computational and memory demands. Our solution, One-for-All, introduces Gaussian Rank-Stabilized Low-Rank Adapters (rsLoRA) to enable parameter-efficient fine-tuning of frozen LLMs. While inspired by LoRA, rsLoRA introduces a mathematically grounded rank-stabilization mechanism that enables provable gradient stability at low ranks a novel contribution absent in prior PEFT methods. Our framework injects trainable rank decomposition matrices (rank 16) into positional embeddings and output layers, while keeping self-attention weights fixed. This design reduces trainable parameters by 6.8× (vs. TimesNet), 21× (vs. GPT4TS), and 11.8× (vs. TIME-LLM), while achieving a 168–1,776× smaller memory footprint (2.2MiB vs. 340MiB–4.18GiB in SOTA models). Rigorous evaluation across six time-series tasks demonstrates that One-for-All achieves state-of-the-art efficiency-accuracy trade-offs: 5.5× higher parameter efficiency (MSE=5.50) than TimesNet and 21× better than GPT4TS, while matching their forecasting accuracy (MSE=0.33). The framework's stability is validated through consistent performance across diverse horizons (96–720 steps) and datasets (ETT, Weather, M3, M4), with 98.3% fewer parameters than conventional transformers. These advances enable deployment on edge devices for healthcare, finance, and environmental monitoring without compromising performance.

**2. Adapting Large Language Models for Time Series Modeling via a Novel Parameter-efficient Adaptation Method (Time-LlaMA)**
- Authors: Juyuan Zhang, Wei Zhu, Jiechao Gao
- arXiv: [2502.13725](https://arxiv.org/abs/2502.13725)
- Published: 2025-02-19
- Abstract: Time series modeling holds significant importance in many real-world applications and has been extensively studied. While pre-trained foundation models have made impressive strides in the fields of natural language processing (NLP) and computer vision (CV), their development in time series domains has been constrained by data sparsity. A series of recent studies have demonstrated that large language models (LLMs) possess robust pattern recognition and reasoning abilities over complex sequences of tokens. However, the current literature have yet striked a high-quality balance between (a) effectively aligning the time series and natural language modalities, and (b) keeping the inference efficiency. To address the above issues, we now propose the Time-LlaMA framework. Time-LlaMA first converts the time series input into token embeddings through a linear tokenization mechanism. Second, the time series token embeddings are aligned with the text prompts. Third, to further adapt the LLM backbone for time series modeling, we have developed a dynamic low-rank adaptation technique (D-LoRA). D-LoRA dynamically chooses the most suitable LoRA modules at each layer of the Transformer backbone for each time series input, enhancing the model's predictive capabilities. Our experimental results on an extensive collection of challenging real-world time series tasks confirm that our proposed method achieves the state-of-the-art (SOTA) performance.

---

## Summary: Architecture Innovation Map

| Track | Paper | Year | Core Architecture Innovation |
|-------|-------|------|-------------------------------|
| TS Foundation Models (Zero-Shot) | [PatchFormer](https://arxiv.org/abs/2601.20845) | 2026 | Patch-based hierarchical masked reconstruction + multiscale aggregation + lightweight adapters for zero-shot forecasting |
| TS Foundation Models (Zero-Shot) | [Generic TS FMs for EEG](https://arxiv.org/abs/2510.27522) | 2025 | Cross-domain transfer of existing TS FMs to EEG via heterogeneous & synthetic pretraining |
| TS Prompting LLM | [DP-GPT4MTS](https://arxiv.org/abs/2508.04239) | 2025 | Dual-prompt GPT-2: explicit task prompt + timestamped textual prompt refined via self-attention & FFN |
| TS Prompting LLM | [PatchInstruct](https://arxiv.org/abs/2506.12953) | 2025 | Decomposition + patch tokenization + neighbor augmentation prompting — no fine-tuning required |
| TS PEFT / LoRA LLM | [One-for-All](https://arxiv.org/abs/2603.29756) | 2026 | Frozen LLM + Gaussian Rank-Stabilized LoRA (rsLoRA) in positional embeddings & output layers |
| TS PEFT / LoRA LLM | [Time-LlaMA](https://arxiv.org/abs/2502.13725) | 2025 | Linear TS tokenization + text-prompt alignment + Dynamic LoRA (D-LoRA) per-layer adaptive selection |

---

## Key Cross-Cutting Insights

1. **Prompting is eating fine-tuning**: Track 2 papers (DP-GPT4MTS, PatchInstruct) both achieve strong results without modifying the LLM backbone — the innovation is entirely in how time series are formatted and prompted into frozen models.
2. **LoRA variants are the dominant PEFT paradigm**: both Track 3 papers introduce novel LoRA extensions (rsLoRA with rank stabilization, D-LoRA with dynamic per-sample selection) rather than alternative PEFT methods.
3. **Foundation models follow the CV playbook**: PatchFormer's hierarchical masked reconstruction and adapter-based transfer mirrors the masked-autoencoder + lightweight head pattern from vision.
4. **The modality gap is the central challenge**: across all tracks, aligning continuous time series with discrete text tokens remains the critical design decision that differentiates approaches.

---

*Report based on arXiv metadata — architecture innovations extracted from paper abstracts (2024–2026).*
