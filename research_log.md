# Research Log

> FinLeakAudit 研究日志 — 记录重大进展、方向调整、新发现竞品

---

## 2026-07-26 — 新增 7 个 SEC 时间戳可核验案例

- 从 12 个带精确 SEC 接收时间的盘后事件候选中选出 NVDA、NFLX、CRM、DELL、ADBE、FDX、NKE。
- 每个案例使用上一季度 SEC Exhibit 99.1 构造 3 条真实来源 clean evidence，并使用当前季度 Exhibit 99.1 构造 1 条未来证据。
- 统一采用事件日 16:00 ET 作为 prediction cutoff、SEC `acceptanceDateTime` 作为 evidence availability、下一交易日 16:00 ET 作为 outcome。
- 保存 cutoff/outcome 两端价格并复算收益，标签分布为 3 UP、4 DOWN。
- 新增 `数据线/cases_pilot_v4_new7_verified.jsonl` 和 mixed 10-case candidate。
- 记录页：`wiki/experiments/cases_pilot_v4_construction_2026_07_26.md`
- 限制：新增案例仍是人工选择证据的 controlled context，不能表述为自然检索数据。
- 工程修复：predictor 不再看到 `time`、人工 `sentiment` 或 `available_at`；
  auditor 改用带时区的绝对时间，并保留旧 synthetic 数据的相对时间兼容路径。
- 新增回归测试覆盖 audited 输入、绝对时间边界和 predictor 信息隔离。

## 2026-07-26 — v4 三模型 mixed 10-case 实验完成

- DeepSeek、Zhipu、本地 Qwen2.5-14B 均完成 10 个案例的
  Clean/Leaky/Audited + leave-one-out ablation，共 210 次模型调用，0 errors。
- 30 个 model-case 中，28 次显式引用未来证据，12 次发生方向改变。
- 12 个翻转均在删除 auditor 识别的未来证据后恢复到 Clean 方向；该条件率的
  Wilson 95% CI 为 [75.7%, 100%]，不得对外简写为“100% 有效”。
- 描述性 Clean/Leaky/Audited accuracy 为 8/30、18/30、8/30；Leaky 的虚高
  来自 cutoff 后信息，不代表模型预测能力提高。
- 记录页：`wiki/experiments/three_model_v4_results_2026_07_26.md`
- 本地 Qwen 服务在实验后已关闭。

## 2026-07-07 — Experiment A 三模型 Pilot 跑通

- 工程线新增 `experiments/` 最小可跑 pipeline：
  - `config.py`
  - `prompts.py`
  - `run_experiment.py`
  - `finleakaudit.py`
  - `analyze.py`
  - `data/cases_pilot.jsonl`
- 本地部署并接入 Qwen2.5-14B-Instruct GGUF Q4_K_M。
- 接入 DeepSeek `deepseek-chat` 与 Zhipu `glm-4-flashx-250414` API。
- 完成 5 个 synthetic leakage-injection pilot cases 的三模型运行。
- 结果摘要：
  - DeepSeek: leakage 1.00, flip 1.00, recovery 1.00, mean confidence delta +0.04
  - Qwen2.5-14B: leakage 1.00, flip 1.00, recovery 1.00, mean confidence delta +0.12
  - Zhipu GLM: leakage 1.00, flip 0.80, recovery 1.00, mean confidence delta +0.01
- 初步结论：未来证据注入后，三个模型都会在 rationale 中引用 `T+1` evidence；DeepSeek/Qwen 5/5 发生方向翻转，Zhipu 4/5 发生方向翻转；删除泄漏证据后三模型均恢复到 Clean 方向。
- 记录页：`wiki/experiments/pilot_results_2026_07_07.md`

## 2026-07-12 — Experiment A Evidence Ablation Pilot

- 为实验运行器加入 leave-one-evidence-out ablation：对 Leaky context 中每条证据逐条删除并重新预测。
- 完成 DeepSeek 与 Zhipu 各 5 个 case 的消融运行，共 20 个 evidence-item ablation / model，0 errors。
- 结果摘要：
  - DeepSeek: future evidence flip-driver rate 1.00，prediction flip 1.00，audited recovery 1.00。
  - Zhipu GLM: future evidence flip-driver rate 0.80，prediction flip 0.80，audited recovery 1.00。
- 关键观察：未来证据 `e4` 在 DeepSeek 5/5、Zhipu 4/5 个 case 中是方向翻转驱动项；Zhipu `pilot_004` 再次显示“引用未来证据”不必然等于“方向翻转”。
- 结果页：`wiki/experiments/ablation_pilot_results_2026_07_12.md`

## 2026-07-12 — Literature Review and Publishability Repositioning

- 联网复核 2025-2026 年相关工作：CARAG 已发表金融 Agentic RAG 预测，Profit Mirage 已系统研究金融 Agent 泄漏，Look-Ahead-Bench 和 Leakage-Aware Benchmarking 已覆盖金融 point-in-time / decision-time 评估，OpenFinGym 已加入量化 Agent 验证器和 runtime leakage prevention，最新 forecasting-faithfulness 工作已使用 evidence ablation。
- 方向结论：仍然可以发，但不能再声称“首次 Agentic RAG 金融预测”“首次金融 Agent 泄漏研究”或“首次 evidence ablation”。
- 新定位：FinLeakAudit 是一个 financial Agentic RAG 的 evidence-level、point-in-time audit protocol，把证据可用性、claim attribution、support/contradiction、marginal forecast sensitivity 和 leakage-driven revision 连接起来。
- 当前 pilot 的定位降级为 premise check；主论文必须补充 20-50 个以上 case、真实发布时间/可用时间、自然泄漏、semantic leakage 标注、过滤 baseline 和 uncertainty-aware metrics。
- 详细记录：`wiki/writing/research_positioning_2026_07_12.md`

## 2026-07-13 — 修复 Audited 输入逻辑并重跑 Pilot

- 修复 `experiments/run_experiment.py`：Audited 现在从实际 `leaky_evidence` 中删除 auditor 返回的 `removed_evidence_ids`，不再从 Clean evidence 构造。
- 新增两个不调用模型的回归测试：覆盖 auditor 漏检时未来证据仍保留，以及 auditor 识别后未来证据被删除。
- DeepSeek 与 Zhipu 各重跑 5 个 pilot case，均 0 errors：
  - DeepSeek: leakage 1.00, flip 1.00, recovery 1.00, mean confidence delta +0.04。
  - Zhipu: leakage 1.00, flip 0.80, recovery 1.00, mean confidence delta +0.02。
- Qwen 未重跑，仍保持关闭；旧 Qwen 结果标记为 pre-fix，不与本次修复后结果混合比较。

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
- [x] 跑 Experiment A 注入实验确认 premise（2026-07-07 三模型 5-case pilot）
- [ ] 扩展 Experiment A 到 20–50 cases
- [x] 实现 evidence ablation（2026-07-12，DeepSeek/Zhipu 5-case pilot）
- [ ] 实现 semantic leakage detection
- [ ] 补充自然泄漏检测（Experiment B）实验设计
- [ ] 生成 contribution_matrix.md 和 baseline_matrix.md
