# FinLeakAudit Knowledge Base — 全局索引

> 最后更新：2026-09-06
> 维护方式：每次新增/修改 wiki 页面后更新本索引

---

## 论文索引 (wiki/papers/)

### 核心竞品
- [[CARAG]] — Decoding the Market's Pulse (EACL 2026)
- [[Profit_Mirage]] — Revisiting Information Leakage in LLM-based Financial Agents (2025)
- [[FLAIRR_TS]] — Forecasting LLM-Agents with Iterative Refinement and Retrieval for Time Series (EMNLP 2025)

### 直接竞品
- [[TRACE]] — Temporal Rule-Anchored Chain-of-Evidence for Stock Prediction (2026)
- [[FinAgent_RAG]] — Agentic RAG for Financial Document QA (2026)
- [[SHARP]] — Self-Evolving Human-Auditable Rubric Policy for Financial Trading Agents (2026)
- [[FinCARDS]] — Card-Based Analyst Reranking for Financial Document QA (2026)

### 金融验证/审计
- [[VERAFI]] — Verified Agentic Financial Intelligence (2025)
- [[FinVet]] — RAG + External Fact-Checking Agents for Financial Misinformation (2025)
- [[MarketSenseAI]] — Enhancing Stock Analysis through LLM Agents (2025)

### 综述与背景
- [[The_New_Quant]] — A Survey of LLMs in Financial Prediction and Trading (2025)
- [[Multi_Agent_Financial_RAG]] — Enhancing Financial RAG with Agentic AI and Multi-HyDE (2025)
- [[ATSF]] — Position: Beyond Model-Centric Prediction — Agentic Time Series Forecasting (2026)
- [[Bayesian_RAG_Finance]] — Bayesian RAG for Reliable Financial QA

### 传统股票预测
- [[Self_Reflective_Stock_Prediction]] — WWW 2024
- [[Data_Axis_Transformer]] — KDD 2021
- [[Deep_Attentive_Stock]] — EMNLP 2020
- [[FinBERT]] — IJCAI 2020

---

## 概念索引 (wiki/concepts/)

- [[evidence_level_temporal_leakage]] — 证据级时间泄漏
- [[forecast_inflation]] — 预测虚高 / profit mirage
- [[leakage_driven_forecast_revision]] — 泄漏驱动的预测修正
- [[claim_evidence_attribution]] — 预测理由-证据归因
- [[evidence_ablation]] — 证据消融
- [[point_in_time_evidence]] — 时点证据可用性
- [[verification_operators]] — 验证算子

---

## 竞品对比索引 (wiki/competitors/)

- [[carag_vs_finleakaudit]]
- [[profit_mirage_vs_finleakaudit]]
- [[flairr_ts_vs_finleakaudit]]
- [[trace_vs_finleakaudit]]
- [[sharp_vs_finleakaudit]]

---

## 方法协议索引 (protocols/)

- [[temporal_availability_operator]]
- [[evidence_attribution_operator]]
- [[support_contradiction_operator]]
- [[evidence_ablation_operator]]
- [[forecast_revision_operator]]

---

## 矩阵索引 (matrices/)

- [[collision_matrix]]
- [[contribution_matrix]]
- [[baseline_matrix]]

---

## 实验索引 (wiki/experiments/)

- [[smoke_pilot_results_2026_07_24]] — 3-case verified smoke pilot
- [[cases_pilot_v4_construction_2026_07_26]] — 新增 7 个 SEC 时间戳案例与 mixed 10-case candidate
- [[three_model_v4_results_2026_07_26]] — v4 mixed 10-case 三模型结果与分层指标
- [[baseline_comparison_v4_2026_07_26]] — No Audit、时间过滤、引用审计与删除未来证据对照
- [[semantic_attribution_annotation_protocol_v1]] — 79 个 claim-evidence pair 的双人盲标协议
- [[natural_point_in_time_data_protocol_v1]] — 自然检索候选语料与时间台账收集规范
- [[team_submission_review_2026_08_08]] — 标注线与自然数据线交付物的人话版复核和验收清单
- [[natural_remaining5_eligibility_2026_09_06]] — 后五个自然事件的时点、来源与检索资格验收
- [[natural_pit_10event_three_model_results_2026_09_06]] — 十事件、三模型、四条件回放结果

---

## 写作索引 (wiki/writing/)

- [[title_candidates]]
- [[contributions]]
- [[related_work_outline]]
- [[abstract_drafts]]
- [[reviewer_attacks]]
- [[ra_application_project_brief_2026_07_26]] — RA 简历、邮件和面试用项目表述
- [[workshop_paper_draft_v1]] — 当前 workshop 论文草稿与复现清单
