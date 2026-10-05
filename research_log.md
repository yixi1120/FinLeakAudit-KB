# Research Log

## 2026-10-05 — AI4F 投稿稿 v2 P0 修订与模拟评审

- 根据外部修改建议逐项核验仓库证据，完成论文 P0 修订：加入 189 篇候选文档、
  201 个 retrieval units、195 个 active units 和 6 个 blocked units 的构成说明，
  并增加十事件紧凑表。
- 补充固定检索的抽取、分块、打分、版本限制、parent-source cap 和 tie-breaking；
  明确当前 pilot 不评测自主 query reformulation、tool planning 或 multi-agent
  coordination。
- 将独立数据核验准确限定为冻结规则抽取的 139 条记录，披露 133 accept、1 reject、
  5 needs-adjudication；没有声称全部 189 篇均经双人逐条核验。
- 补充 model-event 非独立性、归因标签分布和 citation/LLM confusion counts；保留
  Backfill 的 `24/30` 重建比例和 McNemar `p=0.25` 限制。
- 新增内部模拟审稿 `wiki/writing/ai4f_2026_simulated_review_v2.md`，结论为
  Weak Accept / 7 分、confidence 4/5；它不是实际录用预测。
- 新版论文为 6 页，104 项测试全部通过，PDF metadata 已填写；最终上传 PDF
  SHA-256 为 `b05485451a37193738e161ce061a3adce29f0d0803d5c45e5aa10e5b2c65aad1`。

## 2026-10-05 — AI4F 三作者投稿包完成

- 重新编译并逐页检查三作者论文，确认作者为 Ziyang Lu、Junwei Chen 和 Yating
  Zhang；Minzhen Lai 和 Imperial College London 未出现在论文或投稿材料中。
- 全部 103 项测试通过；最终上传 PDF 固定为
  `output/ai4f_2026_submission/FinLeakAudit_AI4F_2026.pdf`，SHA-256 为
  `dcaa4a4236987c23049baee663878596ae54a55324bbcbff22f1d33b1a3ff9a1`。
- 建立集中投稿目录，包含 OpenReview 可复制字段、作者确认消息、上传前后清单和
  checksum；未确认项仅剩两位合作者的 OpenReview profile、reviewer volunteer 和
  远程展示政策回复。
- 已由港科大邮箱向 `contact@ai4f.org` 询问 live remote presentation、无法现场
  出席时是否仍完成正常评审，以及出席是否只影响最终 workshop program。
- AI4F 组织者 Jacob Chanyeol Choi 于 2026-10-04 回复，明确所有录用论文必须现场
  展示；回复未回答无法现场出席时是否仍保留审稿意见。该结论已写入投稿包的
  `ORGANIZER_REPLY.md` 和最终清单。

## 2026-10-02 — AI4F OpenReview 投稿字段核验

- 通过 AI4F 官方页面和 OpenReview live submission invitation 交叉核验，确认截止
  时间为 2026-10-08 11:59 UTC，即 2026-10-08 19:59 HKT。
- 确认表单必填字段为 title、authors/author profiles、keywords、abstract 和 PDF，
  TL;DR 为可选项；提交记录默认采用 CC BY 4.0。
- 新增 `paper/openreview_submission_ai4f_2026.md`，固定可直接粘贴的题目、关键词、
  TL;DR、摘要、PDF 哈希和人工确认清单，不改动 `ai4f-2026-submission-v1` 冻结标签。

## 2026-10-01 — AI4F submission snapshot v1

- 将通讯作者邮箱统一更新为 `zluca@connect.ust.hk`。
- 使用冻结实验摘要生成并嵌入 protocol figure 与四面板 result figure；绘图源代码、
  矢量文件和 QA 报告一并保留。
- 在 Related Work 中明确区分 Profit Mirage / Look-Ahead-Bench 的模型或跨时期诊断，
  与 FinLeakAudit 的检索证据级 availability--attribution--revision 链路。
- 从保留日志中加入三类代表性失败：CrowdStrike citation ID 格式错误、Enphase
  support-without-exclusive-dependence 误判，以及 Intel/Exxon/Capital One 的删除后失稳。
- 新增 `paper/submission_manifest_ai4f_2026.json` 与哈希校验测试，固定标签名为
  `ai4f-2026-submission-v1`。
- 最终 PDF 为 6 页，SHA-256 为
  `dcaa4a4236987c23049baee663878596ae54a55324bbcbff22f1d33b1a3ff9a1`；
  103/103 项测试通过，逐页目检无裁切、重叠或未解析引用。

## 2026-09-10 — 作者单位与贡献声明冻结

- 作者顺序确认为 Lu Ziyang、Chen Junwei、Zhang Yating。
- 单位分别确认为香港科技大学、约翰斯霍普金斯大学和华南师范大学。
- Lu Ziyang 使用 `zluca@connect.ust.hk` 作为通讯作者邮箱。
- 根据 Git 历史、标注 provenance 和团队验收记录，将工程、自然语料建设、独立语义
  标注、来源时间复核及协调裁决等贡献写入论文；尚未确认的邮箱和额外写作职责不作推断。

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

## 2026-08-31 — Semantic attribution baselines 完成

- 在冻结的 79 条人工 gold labels 上完成 citation-only、lexical overlap、
  Embedding-3 similarity 和 blinded DeepSeek judge 四种基线。
- 二分类评测排除 1 条 gold `uncertain`：citation-only F1 0.941、LLM judge
  F1 0.937、lexical F1 0.667、embedding F1 0.509。
- citation-only 出现 4 个 false positives 和 1 个 citation-free false
  negative，说明显式引用不能等同于 semantic dependency；但当前 controlled
  sample 仍使 citation-only 成为最强基线，不能宣称 Full FinLeakAudit 已胜出。
- 新增可复现 runner、统一 evaluator、逐样本输出、Wilson 95% 区间和离线测试；
  完整报告见
  `wiki/experiments/semantic_attribution_baselines_2026_08_31.md`。

## 2026-09-02 — Semantic audit 闭环与失败诊断

- 将 blinded LLM claim-evidence attribution 接入 controlled runner，新增
  `citation_only`、`timestamp_only`、实验性 `semantic_llm` 和
  `full_semantic` 四种策略。
- DeepSeek `case_002` smoke 完成 `DOWN -> UP -> DOWN`，3 个语义 pairs 全部
  判定依赖并删除 `e4`；该 case 有显式引用，只验证工程闭环。
- Zhipu predictor + DeepSeek judge 的 `case_005` 发现 high-confidence false
  positive：cutoff 前 evidence 已包含 inventory glut，Judge 仍以 0.90 判定
  依赖 cutoff 后确认信息。
- 据此冻结架构边界：时间规则掌握 point-in-time 合规删除权；semantic Judge
  负责污染归因与解释，不单独决定 future evidence 能否保留。
- 新增 `--case-id` 精确运行、pair-level audit log、删除依据和 semantic
  调用级短重试。完整记录见
  `wiki/experiments/full_semantic_loop_smoke_2026_09_02.md`。

## 2026-09-02 — Natural Semantic Hard Set v1 冻结

- 从 5 个自然 point-in-time replay 事件的 DeepSeek/Zhipu 原始理由中构造
  38 个 claim、82 个 claim × post-cutoff-evidence pairs。
- 在新语义标签产生前使用固定种子 `29` 做事件级切分：Dev 2 事件 32 pairs，
  Test 3 事件 50 pairs；同一事件及其证据不跨 split。
- 生成器会从本地归档重建完整模型可见文本，并验证检索顺序、结果日志预览和
  cutoff 后证据成员均未漂移。
- 盲标表隐藏事件、模型、证据 ID、显式引用、时间戳、结果与预测正确性；协调密钥
  在 gold 冻结前保持本地且被 Git 忽略。
- 冻结顺序为：双人 Dev 盲标与裁决 → 仅用 Dev 调参 → 方法冻结 → Test 双人盲标 →
  一次性 Test 评测。协议见
  `wiki/experiments/natural_semantic_hardset_protocol_v1.md`。

## 2026-09-03 — Qwen 自然回放与论文结果快照

- 本地 Qwen2.5-14B-Instruct Q4_K_M 完成 5 个自然事件、15 次预测调用，0 错误；
  运行结束后关闭 llama.cpp 服务。
- 三模型自然回放合计 15 个 model-event runs、45 次调用：13/15 有效 exact-ID
  未来引用，6/15 发生 Clean-to-Unfiltered 方向变化，6/6 在删除 cutoff 后证据后
  恢复 Clean 方向；Wilson 95% CI 为 61.0%–100%。
- Aggregate accuracy 为 Clean 6/15、Unfiltered 12/15、Audited 5/15；Unfiltered
  增幅属于 outcome-bounded hindsight inflation。
- Qwen CrowdStrike 理由使用了未来事故语义并写出对应 document ID，但省略 chunk
  suffix，严格 exact-ID citation detector 因此漏检；该例是结构化引用接口失效，
  不能草率称为完全 citation-free。
- Qwen Capital One 在 Clean 与 Unfiltered 均为 UP 时，Audited 变为 NEUTRAL；
  这是删除后上下文稀疏造成的 revision instability，不计为 recovery failure。
- 新增自动生成的论文指标 CSV、三张图、结果快照与 Results 草稿，完整报告见
  `wiki/experiments/natural_pit_5event_three_model_results_2026_09_03.md` 和
  `wiki/experiments/paper_results_snapshot_2026_09_03.md`。

## 2026-09-03 — Revision Backfill 最小诊断

- 新增独立 Rank-Preserving Backfill runner：先从实际 Unfiltered top-k 删除 cutoff
  后证据，再按 cutoff-safe 检索排名补齐，不改写原始 Sparse Audited 结果。
- 离线验证显示五事件均能安全补齐至 8 条且无重复；其中四个事件的补齐序列与 Clean
  相同，`natural_010` 因候选排序与父文档限额交互而不同。
- Qwen `natural_007` 新增一次调用：Clean `UP`、Unfiltered `UP`、Sparse Audited
  `NEUTRAL`、Backfilled Audited `UP`；补齐序列与 Clean 完全一致且引用 ID 有效。
- 该单事件 smoke 支持上下文稀疏是本次 revision drift 的原因，但不用于宣称 Backfill
  在总体上更优。协议与记录见
  `wiki/experiments/natural_revision_refill_baseline_protocol_v1.md`。

## 2026-09-06 — Revision Backfill 三模型对照完成

- DeepSeek、Zhipu、Qwen 在固定五事件上完成 15 个 Backfilled Audited 新调用，0 错误；
  原有 Clean、Unfiltered 与 Sparse Audited 结果未重跑或覆盖。
- 6 个 Clean-to-Unfiltered 初始翻转中，Sparse 与 Backfilled 均恢复 6/6；9 个非翻转
  run 中，Sparse drift 为 1/9，Backfilled drift 为 0/9。
- Backfilled 与 Clean 方向一致 15/15（Wilson 95% CI 79.6%–100%），但 12/15 的
  evidence sequence 与 Clean 完全相同，且 drift 改善只有一个 discordant pair。
- JetBlue 的三个 Backfilled 序列与 Clean 不同但方向仍一致；DeepSeek confidence
  从 0.65 升至 0.85，说明方向一致不等于校准或模型状态完全一致。
- 15 个 Backfilled 输出均有引用，共 53 个 evidence ID，53/53 有效。
- 新增自动分析器、逐事件 CSV、聚合 CSV 和正式结果报告；当前结论限定为删除后
  上下文稀疏的失败诊断，不宣称 Backfill 已取得统计可靠的总体优势。

## 2026-09-06 — Natural Replay 扩展至十事件

- 对后五个自然事件完成独立资格验收：67 条二次来源核验记录全部为 `accept`，归档
  哈希和时间证据均匹配；十事件均可构造 Clean、Unfiltered、Sparse 与 Backfilled
  四种条件。
- DeepSeek、Zhipu 与本地 Qwen 完成新增五事件回放；与冻结的首批五事件合并后，共
  10 个事件、30 个 model-event runs、120 个保留预测输出。
- Unfiltered 中 27/30 显式引用未来证据，13/30 出现方向变化。Sparse 恢复 11/13，
  Backfilled 恢复 13/13，并在全部 30/30 runs 上匹配 Clean 方向。
- Backfill 修正三处 Sparse 不一致：DeepSeek Intel、Qwen Exxon 的恢复失败，以及
  Qwen Capital One 的非翻转漂移。17 个非翻转 runs 中，Sparse drift 为 1/17，
  Backfilled 为 0/17。
- 24/30 个 Backfilled 输入序列与 Clean 完全相同，配对 exact McNemar `p=0.25`；
  因此只报告样本内一致性和失败诊断，不宣称方法具有统计显著优势。
- Accuracy 为 Clean 11/30、Unfiltered 16/30、Sparse 11/30、Backfilled 11/30；
  Unfiltered 的较高值属于 outcome-bounded hindsight inflation。
- 引用完整性检查保留了原始失败：90 个基础条件输出中 11 个输出含 30 个无效 ID，
  30 个 Backfilled 输出中 3 个含 8 个无效 ID。Qwen 有一个事件级超时并成功重试，
  错误记录未删除。
- 新增十事件分析器、冻结指标测试、逐事件和聚合 CSV、正式报告及对比图；Qwen 服务
  在本地实验后关闭。

## 2026-09-08 — Workshop 可编译初稿与引用审计

- 新建 `paper/main.tex`：完成匿名、双栏、workshop-neutral 的 4 页可编译初稿，覆盖
  Introduction、Related Work、问题定义、审计协议、数据、实验、结果、限制与伦理。
- 新建 `paper/references.bib`，对 14 篇实际引用逐项核验官方 ACL Anthology、NeurIPS、
  DOI 或 arXiv 页面；不再使用知识库摘要直接充当论文证据。
- 发现 `FinAgent-RAG` (`arXiv:2605.05409`) 已由作者撤稿，官方理由为实验设计存在重大
  方法错误。已从支持性引用和 baseline 候选中排除，并保留撤稿审计记录。
- 论文数字与冻结结果重新对齐：controlled 30 runs、natural 30 runs、attribution 78 个
  decisive labels；未把尚未标注的 natural semantic Test set 写成结果。
- LaTeX 经 `pdflatex -> bibtex -> pdflatex x2` 编译，引用全部解析；最终 PDF 逐页检查
  无重叠、截断、空白页或损坏表格。

## 2026-09-15 — Novel-safe Backfill 消融决策

- 十事件结果中 24/30 个 Standard Backfilled evidence sequence 与 Clean 完全相同，
  因而 30/30 的方向一致不能单独证明回填方法具有一般优势。
- 保留 Rank-Preserving Standard Backfill 作为主 baseline，因为它模拟正确执行 cutoff
  filtering 后应返回的高排名安全证据；不强制排除 Clean top-k。
- 新增 Novel-safe Backfill 作为计划中的鲁棒性消融：保留 Unfiltered 中幸存的安全证据，
  但新增 evidence 必须来自 cutoff 前、且不在 Clean top-k 和 survivors 中的冻结候选。
- Novel-safe 只用于判断恢复是否依赖重建 Clean 输入，不作为生产检索策略，也不用于
  声称提高市场预测准确率。
- 运行前必须冻结候选资格、排名、parent-document cap 和候选不足处理；当前状态为
  `planned-not-run`。详细规则见
  `wiki/experiments/natural_revision_refill_baseline_protocol_v1.md`。

## 2026-09-30 — Novel-safe Backfill 三模型消融完成

- 在模型调用前冻结 Novel-safe 资格：10 个自然事件中 6 个能在排除 Clean top-k 后使用
  不同的 cutoff-safe evidence 补满 8 条；其余 4 个因候选不足冻结为 incomplete。
- 在 6 个合格事件和 DeepSeek、Zhipu、Qwen 三个模型上完成 18 个 Novel-safe 调用；
  原有 Clean、Unfiltered、Sparse 和 Standard Backfill 结果均未重跑或覆盖。
- Clean 方向一致数为 Sparse 15/18、Standard 18/18、Novel-safe 15/18；6 个初始翻转的
  恢复数分别为 4/6、6/6、4/6，12 个非翻转的 drift 分别为 1/12、0/12、1/12。
- Standard-only match 为 3、Novel-only match 为 0，配对 exact McNemar `p=0.25`；
  Novel-safe 与 Clean 完全同序列为 0/18。
- Novel-safe 未复现 Standard 对 DeepSeek Intel、Qwen Exxon 和 Qwen Capital One 三处
  Sparse mismatch 的修正，说明 revision 依赖回填内容和排序，不只依赖上下文数量。
- Qwen `natural_007` 在 8192 上下文下因 8102-token prompt 连续产生 7 条截断 JSON
  错误；错误全部保留。将 llama.cpp 上下文提高到 16384 后，在相同模型、prompt、
  temperature 和 700-token 输出上限下完成调用；实验后服务已关闭。
- 新增资格检查、Novel-safe policy、分析脚本、冻结 CSV、测试和正式实验报告；论文初稿
  按约定未修改。

## 2026-09-30 — Backfill Citation ID 门禁

- 为之后的 Standard 与 Novel-safe Backfill 调用增加 evidence ID 白名单校验。
- 无效 ID 输出最多接受两次定向纠错；仍未通过时记为不可重试的
  `InvalidCitationError`，不进入正式结果。
- 每条成功结果记录 citation 尝试次数和失败 ID；持久失败不会再触发外层整事件重跑。
- 既有 18 条 Novel-safe 结果保持冻结，不用新门禁事后替换，论文初稿仍未修改。

## 2026-09-30 — AI4F 2026 投稿优先级切换

- 将 ACM ICAIF 2026 Workshop AI4F 确认为当前投稿目标。其主题覆盖 financial agents、
  evaluation and verification、RAG、governance and auditability，与 FinLeakAudit 高度匹配。
- 官方页面存在日期冲突：AI4F 专页写 2026-10-07 AoE，ICAIF workshop 总页写
  2026-10-01 AoE。团队采用 2026-10-01 AoE 作为首次完整上传的内部安全线，并计划向
  `contact@ai4f.org` 核实最终关闭时间。
- 当前四页 PDF 已逐页检查，无裁切、重叠、坏表格、缺失引用或空白页；正文在此检查点
  保持不变。
- 实验线下一步仍为扩充四个候选不足事件的 Novel-safe cutoff-safe evidence pool，但在
  AI4F 初始投稿包安全上传前暂缓。
- 新增投稿行动页：`wiki/writing/ai4f_2026_submission_plan.md`。

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
- [x] 实现 semantic leakage detection（controlled attribution baseline + online smoke）
- [x] 补充自然泄漏检测（Experiment B）实验设计并完成 10-event replay
- [x] 实现并运行 Novel-safe Backfill 输入重合消融（2026-09-30，6 eligible events × 3 models）
- [ ] 完成 AI4F 2026 OpenReview 初始投稿与作者确认
- [ ] AI4F 投稿后扩充 4 个 Novel-safe 候选不足事件
- [ ] 生成 contribution_matrix.md 和 baseline_matrix.md
