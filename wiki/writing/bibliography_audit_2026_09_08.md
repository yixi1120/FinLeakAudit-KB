---
title: Workshop bibliography primary-source audit
date: 2026-09-08
status: verified-for-draft
---

# Scope

This page records the primary publication pages used to freeze the first workshop
bibliography. Verification covers title, authors, year, publication status, and the
specific claim used in `paper/main.tex`. It does not imply endorsement of every
experimental conclusion in the cited work.

# Included sources

| Key | Source | Status | Use in FinLeakAudit |
|---|---|---|---|
| `lewis2020rag` | https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html | NeurIPS 2020 | RAG and explicit non-parametric evidence background |
| `gao2023alce` | https://aclanthology.org/2023.emnlp-main.398/ | EMNLP 2023 | Citation correctness and completeness evaluation |
| `koa2024sep` | https://doi.org/10.1145/3589334.3645611 | WWW 2024 | Explainable self-reflective stock prediction |
| `fatouros2025marketsenseai` | https://arxiv.org/abs/2502.00415 | active preprint v2 | Agentic RAG for multi-source stock analysis |
| `li2026carag` | https://aclanthology.org/2026.eacl-long.141/ | EACL 2026 long paper | Agentic RAG and structured temporal evidence for financial forecasting |
| `li2025profitmirage` | https://arxiv.org/abs/2510.07920 | active preprint v1 | Memorization-driven leakage in financial agents |
| `benhenda2026lookahead` | https://arxiv.org/abs/2601.13770 | active preprint v1 | Point-in-time look-ahead benchmark |
| `guan2026leakageaware` | https://arxiv.org/abs/2606.22719 | workshop paper / preprint | Decision-time observability in leakage-aware forecasting |
| `zhang2026openfingym` | https://arxiv.org/abs/2606.26350 | active preprint v1 | Runtime train-test leakage prevention in quant-agent evaluation |
| `ding2026trace` | https://arxiv.org/abs/2603.12500 | active preprint v1 | Temporal evidence chains on financial knowledge graphs |
| `jalori2025flairr` | https://arxiv.org/abs/2508.19279 | active preprint v1 | Accuracy-driven forecasting refinement |
| `chen2026sharp` | https://arxiv.org/abs/2605.06822 | active preprint v1 | Human-auditable trading-policy revision |
| `akinfaderin2025verafi` | https://arxiv.org/abs/2512.14744 | active preprint v1 | Financial calculation and compliance verification |
| `sarfati2026forecasters` | https://arxiv.org/abs/2607.08046 | active preprint v1 | Forecast faithfulness under evidence ablation |

# Excluded source

`FinAgent-RAG` (`arXiv:2605.05409`) is excluded from all supporting claims. Its
official arXiv page marks the paper withdrawn and states that major experimental
design errors invalidate the conclusions. The local paper card and collision matrix
retain the withdrawal as an audit record rather than deleting the prior entry.

# Claim boundary

- Conference and arXiv pages are used as metadata and abstract-level primary sources.
- The bibliography does not support a "first" claim for FinLeakAudit.
- Preprint results are described as author-reported findings, not independently
  replicated facts.
- Venue-specific style and final author metadata remain pending.
