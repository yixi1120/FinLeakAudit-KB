# AGENTS.md — FinLeakAudit Knowledge Base Rules

You are maintaining a research wiki for the project:

**FinLeakAudit: Evidence-Level Leakage Detection and Forecast Revision for Financial Agentic RAG**

## Core Thesis

FinLeakAudit is **not** a stock prediction model. It is an **evidence-level audit layer** for financial Agentic RAG forecasting systems. We detect whether retrieved evidence was temporally available at prediction time, trace which evidence supports which prediction claims, quantify each piece of evidence's marginal impact on forecasts, and revise predictions when leakage is found.

## Folder Rules

- `raw/` — immutable source material. **Never edit files in raw/.** Contains PDFs, search reports, chat exports, and survey notes.
- `wiki/` — synthesized markdown pages maintained by LLM. You may create and update these pages.
  - `wiki/papers/` — one file per paper (paper card template)
  - `wiki/concepts/` — concept pages (definitions, cross-references)
  - `wiki/competitors/` — pairwise competitor comparisons
  - `wiki/experiments/` — experiment design and results
  - `wiki/metrics/` — metric definitions
  - `wiki/writing/` — drafts, reviewer attack bank, abstract drafts
- `matrices/` — comparison tables (collision, contribution, baseline)
- `protocols/` — formal audit operator definitions
- `prompts/` — reusable prompts for ingest/compare/write workflows

## Ingest Workflow

When ingesting a new paper:

1. Read the source from `raw/`.
2. Create or update a paper card in `wiki/papers/` using the paper card template.
3. Extract: task, method, data, metrics, key findings.
4. Compare it with FinLeakAudit — what overlaps? What doesn't?
5. Assign collision risk: `low` / `medium` / `high` / `critical`.
6. Update `matrices/collision_matrix.md`.
7. Update relevant concept pages in `wiki/concepts/`.
8. Append a dated entry to `research_log.md`.

## Collision Risk Rules

**Critical** — papers that cover ALL of:
- financial forecasting + Agentic RAG + temporal leakage audit + evidence ablation + forecast revision

**High** — papers that cover most of:
- financial forecasting + Agentic RAG
- financial agent leakage
- forecast revision with retrieval

**Medium** — papers that cover some of:
- financial QA with Agentic RAG
- evidence cards / structured evidence
- auditable financial agents

**Low** — papers that cover:
- general RAG / general time series / unrelated finance NLP

## Writing Safety Rules

**Never claim:**
- "first Agentic RAG for stock prediction" (CARAG did it)
- "first leakage study in financial agents" (Profit Mirage did it)
- "causal graph" / "causal prediction" (avoid causal inference attacks)

**Prefer:**
- "evidence-level temporal leakage"
- "claim-evidence attribution"
- "leakage-driven forecast revision"
- "point-in-time evidence availability"
- "verification operators" (NOT "skill" in titles)

## Paper Card Template

Every paper in `wiki/papers/` must follow this structure:

```markdown
---
title: 
year: 
venue: 
ccf_level: 
arxiv: 
tags: []
status: unread | skimmed | deep-read
collision_risk: low | medium | high | critical
must_cite: true | false
---

# 一句话总结

# 研究任务

# 方法

# 数据

# 指标

# 和 FinLeakAudit 的相似点

# 和 FinLeakAudit 的区别

# 撞车风险

# 可以引用的位置
- Introduction:
- Related Work:
- Method:
- Experiments:

# 适合作为 baseline 吗？

# 关键原文摘录 / 证据

# 待确认问题
```

## Update vs Create

- When new information arrives about an existing paper, **update** its card (don't create a duplicate).
- When a new competitor is discovered, create a new card and update `matrices/collision_matrix.md`.
- When a concept definition evolves, update the concept page and note the change in `research_log.md`.
