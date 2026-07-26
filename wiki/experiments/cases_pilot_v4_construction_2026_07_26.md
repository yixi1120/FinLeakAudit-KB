---
title: Pilot v4 case construction and verification
date: 2026-07-26
status: candidate
---

# 目标

在原有 3 个时间线合格的 semi-real smoke cases 之外，补充 7 个具有真实证据来源、精确公开时间和可复算结果标签的 controlled cases。

本轮不把案例描述为 natural RAG retrieval。新增案例的上下文由研究者从真实 SEC 文件中选择并改写，目的是先建立可审计、可重复的时间边界。

# 验收规则

每个案例必须严格满足：

```text
clean evidence available_at <= prediction cutoff
prediction cutoff < leaked evidence available_at < outcome time
```

具体设计统一为：

- prediction cutoff：事件披露当日美东时间 16:00 收盘；
- leaked evidence availability：SEC EDGAR `acceptanceDateTime`；
- outcome time：下一交易日美东时间 16:00 收盘；
- outcome return：`outcome_close / cutoff_close - 1`；
- outcome label：正收益为 `UP`，负收益为 `DOWN`。

# 新增案例

| Case | Ticker | Cutoff | SEC acceptance | Outcome | Return | Label |
|---|---|---|---|---|---:|---|
| case_008 | NVDA | 2024-02-21 16:00 ET | 2024-02-21 21:22:09Z | 2024-02-22 16:00 ET | +16.4068% | UP |
| case_009 | NFLX | 2024-04-18 16:00 ET | 2024-04-18 20:02:24Z | 2024-04-19 16:00 ET | -9.1058% | DOWN |
| case_010 | CRM | 2024-05-29 16:00 ET | 2024-05-29 20:03:58Z | 2024-05-30 16:00 ET | -19.7382% | DOWN |
| case_011 | DELL | 2024-05-30 16:00 ET | 2024-05-30 20:09:22Z | 2024-05-31 16:00 ET | -17.8663% | DOWN |
| case_012 | ADBE | 2024-06-13 16:00 ET | 2024-06-13 20:06:10Z | 2024-06-14 16:00 ET | +14.5638% | UP |
| case_013 | FDX | 2024-06-25 16:00 ET | 2024-06-25 20:15:10Z | 2024-06-26 16:00 ET | +15.5302% | UP |
| case_014 | NKE | 2024-06-27 16:00 ET | 2024-06-27 20:16:39Z | 2024-06-28 16:00 ET | -19.9844% | DOWN |

标签分布为 3 `UP`、4 `DOWN`。

# 来源设计

每个新增案例包含：

- 3 条 clean evidence：从该公司上一季度 SEC Exhibit 99.1 中提取的 source-grounded paraphrases；
- 1 条 leaked evidence：从当前季度 SEC Exhibit 99.1 中提取的 source-grounded paraphrase；
- 2 个价格页面：分别记录 cutoff close 和 outcome close；
- SEC accession number、稳定文档 URL 和精确接收时间。

内容来源、SEC 时间来源和价格来源共 42 个唯一 URL，在 2026-07-26 检查时均返回 HTTP 200；14 个 filing index 页面均包含 `Accepted` 时间标记。

# 文件

- 新增 7-case：`数据线/cases_pilot_v4_new7_verified.jsonl`
- mixed 10-case candidate：`数据线/cases_pilot_v4_mixed10_candidate.jsonl`
- 原有 3-case：`数据线/cases_pilot_v3_smoke_eligible.jsonl`

# 候选池

除最终选择的 7 个案例外，还核验了 ORCL、MU、AVGO、LULU 和 RH 的盘后 8-K 接收时间，作为后续替补池。META Q1 2024 没有在目标日期找到对应 8-K，因此没有为了凑数而保留。

# 自动检查结果

新增 7-case 已通过：

- JSONL 逐行解析；
- case ID 唯一；
- 每条案例 3 clean + 1 leaked evidence；
- 所有 evidence URL 非空且不是占位链接；
- clean evidence 均不晚于 cutoff；
- leaked evidence 均严格晚于 cutoff 且早于 outcome；
- outcome return 可由两端价格复算；
- return 符号与 `label`、`outcome_label` 一致。

# 局限

1. 三条 clean claims 来自同一份上一季度 SEC 文件，不是三个独立来源。
2. 证据由研究者选择并改写，不是自然检索结果，因此仍属于 controlled evaluation。
3. 七个新增案例均为财报或业绩披露，事件类型多样性不足。
4. 价格采用 StatMuse 历史页面展示值；相邻交易日收益方向已复算，但论文级实验还应增加第二个行情来源并记录数据许可证。
5. mixed 10-case 包含 3 个使用 synthetic clean evidence 的旧案例，不能把 10 个案例整体称为 fully real-world。
6. v4 运行已对 predictor 隐藏 `time`、`sentiment` 和
   `available_at`，auditor 也改为比较带时区的绝对时间；但当前归因仍依赖
   rationale 中显式给出的 evidence ID，尚不能识别 citation-free semantic
   leakage。

# 下一步

1. 完成 DeepSeek、Zhipu、Qwen 三模型 mixed 10-case 运行；
2. 同时报告总体结果和按 `dataset_tier` 分层结果；
3. 为证据内容、SEC 时间和价格增加第二人抽查记录；
4. 实现 citation-free semantic attribution baseline；
5. 扩展事件类型，并建立 natural point-in-time retrieval cases。
