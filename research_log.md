# Research Log

> FinLeakAudit 研究日志 — 记录重大进展、方向调整、新发现竞品

---

## 2026-08-19 — 两条线技术收口与自然语料离线检索

- 合并 `main` 的语义标注提交与 `develop` 的 10 事件自然候选语料，保留两条线原始
  Git 历史。
- 修正 4 条 Annotator A claim span；新增 A/B 完整性校验、三分类 agreement、
  Cohen's kappa、`yes` vs `other` agreement、分歧导出和 provenance 模板。第二位
  真人标注与人工裁决仍待完成，未用模型代填。
- 修正 NVIDIA、NIKE、Intel、JetBlue 的 cutoff/horizon，以及 NIKE、Capital One
  的交易所/日历；为 10 个事件补齐 evaluator-only outcome，并使用 Yahoo Finance
  chart API 与 StatMuse Money 交叉核验方向，10/10 一致（显示价格并不完全相同）。
- 新增 9 份 SEC Exhibit/DOJ 判决原文；`raw/` 旧文件未改动。自然语料当前包含
  195 个 active retrieval units，validator 报告 0 errors。
- 新增 HTML/XML/PDF 正文抽取、稳定分块、时间过滤、parent-source cap 和确定性
  lexical top-k；10/10 事件的关键事件来源组均自然进入 outcome-bounded top-8。
- 新增 139 行独立二次来源核验批次，覆盖全部 post-cutoff、全部 unresolved-time
  文档和每事件至少 20% 的 pre-cutoff 文档。该文档级人工核验仍待另一位真人完成；
  投稿前仍建议换用或补充许可清晰、版本固定的市场数据源。
- 离线回归测试增至 31 个，全部通过；本次没有调用任何预测模型。
- 详细交接：`wiki/experiments/team_completion_handoff_2026_08_19.md`。

## 2026-08-19 — Natural point-in-time replay 最小实验

- 新增 Natural 专用 runner，将 cutoff-safe Clean、outcome-bounded Unfiltered 和
  timestamp-audited revision 三种条件接入现有 DeepSeek/智谱调用层。
- Audited 严格从实际 Unfiltered top-k 删除 cutoff 后 chunks，不使用 Clean 输入替换；
  predictor prompt 不展示证据时间、URL、availability 标签或 outcome。
- 冻结 5 个异质事件，完成 DeepSeek 与智谱各 5 个事件、共 30 次预测调用，0 errors；
  本轮未启动本地 Qwen。
- 10 个 model-event 中，未来证据进入 Unfiltered top-k 10/10，被显式引用 9/10，
  预测方向改变 4/10；四个改变均在时间过滤后恢复到各自 Clean 方向。
- Clean/Unfiltered/Audited 准确率分别为 4/10、8/10、4/10。Unfiltered 的暂时提升
  解释为 outcome-bounded replay 中的 hindsight inflation，不解释为预测能力提升。
- 新增结果分析器、citation ID 有效性检查、模型/事件明细表、聚合表和 CrowdStrike
  case study；离线测试增至 38 个。另记录到 2/30 个预测输出共形成 5 个不可解析
  引用：一处使用了不存在的 chunk 后缀，一处把 chunk ID 缩写成 document ID。
- 结果页：`wiki/experiments/natural_pit_5event_results_2026_08_19.md`。

## 2026-08-08 — 标注线与自然数据线交付复核

- 复核标注线提交 `be16042`：79 条 Annotator A 样本结构完整，可保留为单人原始标注；
  正式 gold labels 前仍需保护 B 的独立盲标、缩短 41 条 `yes` 的 matched span、记录
  annotation provenance，并完成 agreement、Cohen's kappa 和分歧裁决。
- 复核数据线提交 `506ffe3`：CrowdStrike `natural_001` 的 18 篇候选文档、JSON、CSV、
  archive path 和 SHA-256 一致；正式实验前仍需处理当前网页与历史版本混用、状态页版本
  拆分、三处已确认的时间/URL 元数据、候选语料收集记录和第二人核验。
- 两项交付均定位为可保留的内部初稿，暂不作为论文金标或自然检索正式结果。
- 详细说明：`wiki/experiments/team_submission_review_2026_08_08.md`

## 2026-07-29 — 自然数据与语义归因任务启动

- 冻结数据线 v1 协议：先收集带真实时间的候选语料，再由固定检索器生成
  top-k，禁止人工挑选最终泄漏证据。
- 从 v4 三模型结果生成 79 条随机化 claim-evidence 盲标样本和独立
  coordinator key；模型、case、自动引用标签和 outcome 不对标注者可见。
- 新增离线 lexical attribution baseline。它比较 claim 与 cutoff 后证据的
  重合，同时扣除 cutoff 前证据可解释的最大重合；人工 gold labels 冻结前不报告
  precision、recall 或 F1。
- 将旧 `experiments/analysis/case_studies.md` 标为 legacy illustrative
  draft。旧稿中关于 cosine threshold 和 LLM judge 的表述不是已实现实验，不得
  作为项目结果引用。

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

## 2026-07-26 — Baseline 对照与 RA 对外材料

- 新增离线 baseline 汇总器，复用三模型结果比较 No Audit、
  Timestamp-only、Citation-only 和 Delete-All-Future，不增加模型调用。
- 总体结果：No Audit accuracy 18/30；其余三项均为 8/30。
  Citation-only 保留 2/30 条未显式引用的未来证据，当前结果尚不能证明其
  优于 timestamp filtering。
- 新增 48 行 baseline 分层表和 30 行逐案例公开结果表。
- 根 README 从内部 Wiki 说明改为 RA-facing 研究项目首页。
- 新增 `wiki/writing/ra_application_project_brief_2026_07_26.md`，提供克制的
  CV、邮件和面试表述。

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

## 2026-08-31 — 双线交叉核验完成

- 协调者记录 Zhang Yating 与 Chen Junwei 通过微信提交的书面盲标独立性确认，79 条
  consolidated labels 正式冻结为 gold-label set。
- Natural corpus 第二核验完成 139 条：133 accept、1 reject、5
  needs_adjudication；139/139 本地归档 SHA-256 匹配，原始十列零改动。
- `natural_001_doc_011` 的首次发布时间由 09:45 UTC 修正为 05:30 UTC，09:45 UTC
  记录为更新时间；两个时间均为 cutoff 后，实验条件和既有指标不变。
- 四个无法证明精确首次可用时间的 CrowdStrike 页面继续 blocked；JetBlue 法院文件
  保留日期级保守上界并明确不作为精确时间。
- 完成记录：`wiki/experiments/team_verification_completion_2026_08_31.md`。

## 2026-08-25 — Semantic Attribution 双人标注与第三方裁决

- Annotator A 与 Annotator B 分别完成同一批 79 条 claim-evidence pairs。
- 三分类 semantic dependency 一致率为 77/79（97.5%），Cohen's kappa 为
  0.952；`yes` 对 `other` 的二分类判断为 79/79 一致。
- 13 条至少存在一个字段分歧，由协调者 Lu Ziyang 于 2026-08-25 确认裁决，生成
  `semantic_annotation_adjudicated_v1.csv` 共 79 条 consolidated labels。
- 分析脚本已加入人工裁决保护：重跑时保留已有裁决，并在裁决完整后自动生成整合
  标签，避免覆盖人工结果。
- 两位标注者的独立盲标声明已由协调者于 2026-08-31 记录，consolidated labels
  正式冻结为 publication-ready gold labels。

---

## 待办

- [ ] 对 SHARP、FLAIRR-TS、ATSF 做深度阅读
- [x] 跑 Experiment A 注入实验确认 premise（2026-07-07 三模型 5-case pilot）
- [ ] 扩展 Experiment A 到 20–50 cases
- [x] 实现 evidence ablation（2026-07-12，DeepSeek/Zhipu 5-case pilot）
- [ ] 实现 semantic leakage detection
- [ ] 补充自然泄漏检测（Experiment B）实验设计
- [ ] 生成 contribution_matrix.md 和 baseline_matrix.md
