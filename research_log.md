# Research Log

> FinLeakAudit 研究日志 — 记录重大进展、方向调整、新发现竞品

---

## 2026-05-17 — 建立 Karpathy-style 研究 Wiki

- 从 `/LLM4TS_Finance_Survey_zh/` 和 `/LLM4TS_Finance/` 导入所有原始资料
- 搭建 `FinLeakAudit-KB/` 完整目录结构
- 撰写 AGENTS.md、README.md、index.md
- 从 `finleakaudit_related_papers_summary_v2.md` 和 `time_safe_rag_survey_report.md` 提取论文信息
- 建立论文卡片、概念页、竞品矩阵

## 2026-05-17 — 方向最终确认

- 从 "Time-Safe Verified Multi-Agent RAG for Stock Movement Prediction" 转向
- 最终定位：**FinLeakAudit: Evidence-Level Leakage Detection and Forecast Revision for Financial Agentic RAG**
- 核心转向：从"做预测模型"变为"做审计框架"
- 关键决策：
  - 不再用 "Skill" 作为主术语 → 改用 "Verification Operators" / "Audit Protocol"
  - 不再说 "causal" → 用 "support/contradiction/attribution"
  - 主要贡献落在 evidence-level audit + ablation + revision

## 2026-05-17 — 竞品扩展搜索

- Tavily 搜索发现新竞品：
  - **SHARP** (2605.06822): Morgan Stanley 的可审计交易策略树 — 撞车风险：中
  - **FLAIRR-TS** (EMNLP 2025): 自校正时序预测 — 撞车风险：中
  - **Multi-Dimensional Behavioral Evaluation** (2605.05739): LLM 评估股票 Agent — 撞车风险：低
  - **FinCARDS** (2601.06992): 证据卡片金融 QA — 撞车风险：低
  - **ATSF** (2602.01776): Agentic 时序预测范式 — 撞车风险：低

## 2026-05-15 — 第一轮竞品初查

- 来自 `time_safe_rag_survey_report.md`
- 关键发现：
  - VERAFI (2512.14744) 和 FinVet (2510.11654) 出现，Verifier 概念撞车风险上升
  - "Verified" 命名已被抢占
  - Time-Safe 成为最后的护城河
  - 建议从 "Verified" 改为 "Evidence-Grounded" 或 "Time-Constrained"

---

## 待办

- [ ] 对 SHARP、FLAIRR-TS、ATSF 做深度阅读
- [ ] 跑 Experiment A 注入实验确认 premise
- [ ] 补充自然泄漏检测（Experiment B）实验设计
- [ ] 生成 contribution_matrix.md 和 baseline_matrix.md
