---
title: Minzhen Lai fourth-author handoff
date: 2026-10-03
status: assigned-pending-delivery
deadline: 2026-10-06
target: AI4F 2026 initial submission
---

# 定位

这是 Minzhen Lai（Imperial College London）的投稿前工作包。它只分配尚未完成的独立复现、分层分析、
论文修订和展示准备，不追溯转让前三位作者已经完成的历史贡献。

论文源文件已将 Minzhen Lai 列为拟定第四作者，以便投稿材料同步准备；最终提交前
仍须完成核心交付物、确认作者信息，并由团队验收。仅承诺前往米兰或制作海报不
构成作者资格。

# Minzhen Lai 负责的完整模块

## A. 独立外部复现审计（核心，必须完成）

在英国的独立机器上，从公开 GitHub 标签
`ai4f-2026-submission-v1` 全新克隆项目，不使用项目负责人本地已有的虚拟环境。

执行并记录：

```bash
git clone https://github.com/yixi1120/FinLeakAudit-KB.git
cd FinLeakAudit-KB
git checkout ai4f-2026-submission-v1

uv venv .venv --python 3.11
uv pip install --python .venv/bin/python -r requirements.txt

.venv/bin/python -m unittest tests.test_submission_manifest -v
.venv/bin/python experiments/analyze_natural_10event.py
.venv/bin/python experiments/build_paper_results_snapshot.py
.venv/bin/python experiments/analyze_semantic_baselines.py
.venv/bin/python -m unittest discover -s tests -v
make -C paper PYTHON=../.venv/bin/python
```

交付 `paper/external_reproduction_report.md`，至少包含：

- 操作系统、CPU、内存、Python、LaTeX 和关键依赖版本；
- 当前 commit/tag 和执行日期；
- 每条命令的退出状态与关键输出；
- 预期的 103 项测试是否全部通过；
- manifest 哈希是否一致；
- 是否能够从冻结结果重新生成分析表、图和 PDF；
- 所有 warning、失败、手工步骤和环境偏差；
- 明确区分“离线结果复现”和“重新调用在线模型”。

不得修改 `raw/`，不得覆盖冻结结果，不要求共享任何 API key，也不得为了得到成功
结果而静默更改依赖或输入。

## B. Model-by-event 分层分析（核心，必须完成）

基于仓库已有冻结结果新增：

- `experiments/analyze_model_stratified.py`
- `experiments/analysis/model_stratified_summary_v1.csv`
- `tests/test_analyze_model_stratified.py`

至少分别报告 DeepSeek、Zhipu 和 Qwen 的：

- Controlled：未来证据引用率、预测方向/类别变化率、变化后的恢复率；
- Natural replay：未来证据引用率、方向变化率、Sparse 恢复率、Backfill 恢复率、
  Backfill 与 Clean 方向一致率；
- 每个指标的分子、分母和缺失值处理；
- 至少列出一个模型间差异或失败案例，但不得将小样本差异描述为显著优势。

分析必须与论文总计数保持一致，并保留以下边界：

- leave-one-out 只能表述为 marginal sensitivity；
- 不能由 10 个自然事件推断现实世界泄漏发生率；
- Backfill 是诊断性对照，不是已证明的改进方法；
- 不根据结果反向修改阈值、样本或指标定义。

## C. 论文修订（核心，必须完成）

候选人根据 A、B 两项结果提交文字修改建议，至少包括：

- Reproducibility 段落的独立复现结论；
- Results 或 Discussion 中的一段 model-stratified 结果解释；
- 一段对复现失败、跨环境差异或小样本不确定性的限制说明；
- 对摘要、表格、图和正文数字做独立一致性核验。

修改以 PR 或逐项 diff 形式提交，由前三位作者审核；不得直接重写研究结论。

## D. 现场展示（录用后职责，不单独构成作者资格）

- 负责 2026-11-14 米兰 AI4F 的现场海报或 oral presentation；
- 熟悉 cutoff、claim-evidence attribution、Sparse/Backfill、McNemar `p=0.25`
  和项目限制；
- 准备海报、十分钟讲稿和 reviewer Q&A；
- 录用后按主办方要求完成现场作者注册。

# 验收标准

以下项目全部满足后，拟定四作状态才转为最终确认：

- [ ] 公开标签在独立机器上完成全新复现，并保留可审计报告；
- [ ] 103 项现有测试结果得到记录，任何失败均有解释；
- [ ] 新的分层分析脚本、CSV 和测试可在主仓库复跑；
- [ ] 分层指标与冻结总计数一致，没有选择性报告；
- [ ] 候选人实际参与论文相关段落的撰写或重要修改；
- [ ] 候选人确认最终稿、作者顺序、投稿行为和内容责任；
- [ ] 前三位作者共同同意加入四作；
- [ ] 英文姓名、单位、邮箱和 OpenReview Profile ID 已确认；
- [ ] 所有交付在 2026-10-06 前提交，留出投稿前复核时间。

若核心交付未通过，候选人不进入作者名单；可以作为受邀协作者或现场代理方案继续
向主办方申请，但不能以出席承诺替代作者贡献。

# 完成后使用的贡献声明草案

验收完成后，将论文中的职责表述从“is responsible for”更新为下列完成时表述：

> Minzhen Lai independently reproduced the frozen artifact in a clean external
> environment, performed model-stratified robustness analysis, audited
> manuscript-to-artifact consistency, contributed to the reproducibility and
> results discussion, and prepared the conference presentation.

# 前三位作者调整后的边界

- Ziyang Lu：保留 conceptualization、methodology、software、核心 experiments、
  annotation adjudication、主要 formal analysis、visualization、主稿写作和项目管理；
  将“外部独立复现审计、model-stratified 新分析及其对应文字”交给 Minzhen Lai。
- Junwei Chen：保留自然 point-in-time 语料、source/timestamp metadata、retrieval
  units 和独立语义标注等已完成贡献，不追溯转让。
- Yating Zhang：保留独立语义标注、claim-span refinement 和自然来源/时间复核等
  已完成贡献，不追溯转让。
- Minzhen Lai：完成 A-C 后获得独立复现、分层分析、artifact consistency audit
  和对应论文修订贡献；D 为录用后的附加职责。

# 提交方式

建议使用独立分支 `fourth-author-reproduction-v1`，先提交 PR，不直接推送 `main`。
PR 描述必须列出运行环境、执行命令、结果文件、失败记录和论文数字是否一致。
