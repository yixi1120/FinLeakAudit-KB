---
title: Natural point-in-time data collection protocol v1
date: 2026-07-29
status: ready-for-data-line
---

# 目标

数据线收集 10 个真实金融事件的冻结候选语料，为后续确定性检索实验提供输入。
本阶段不手工挑选最终的 `clean_evidence` 和 `leaked_evidence`，也不运行预测模型。

研究问题是：当检索系统面对一个历史预测查询时，未经时间过滤的检索结果是否会
自然混入 cutoff 后才可获得的文档。

# 核心原则

1. 先固定事件、prediction cutoff、查询和候选语料，再做时间标注。
2. 数据线收集候选文档，工程线使用固定检索器生成 top-k；不得人工把某篇文档塞进
   top-k。
3. Predictor 不得看到时间标签、人工 sentiment、outcome label 或未来价格。
4. `published_at` 不等于 `available_at`。必须记录真正可公开访问的最早时间及其证据。
5. 无法核验的字段填 `null` 并说明原因，禁止猜测 URL、时间或时区。
6. 原文、改写文本和摘要必须分开保存。自然检索主实验优先使用可追溯的原始文本或
   原始摘要，不把人工改写伪装成自然检索结果。

# 事件选择

第一批提交 10 个事件，至少覆盖 4 类：

- earnings / guidance；
- regulatory / litigation；
- product / cybersecurity incident；
- management / financing / M&A。

每个事件建议收集 8–20 篇候选文档，至少同时包含：

- cutoff 前可用文档；
- cutoff 后发布、但与同一查询高度相关的文档；
- 相关但不影响预测的干扰文档；
- 如存在，记录修订稿或供应商延迟收录的文档。

# 每个事件必须固定

| 字段 | 要求 |
|---|---|
| `event_id` | 全局唯一，如 `natural_001` |
| `prediction_cutoff` | ISO-8601，必须带 UTC offset |
| `market_timezone` | IANA 名称，如 `America/New_York` |
| `trading_calendar` | 如 `XNYS`、`XNAS` |
| `retrieval_query` | 只能根据 cutoff 前信息编写 |
| `query_origin` | 说明查询由谁、何时、根据什么信息生成 |
| `forecast_horizon` | 如 `next trading day close` |
| `outcome_time` | 仅 evaluator 使用，不进入检索或 predictor |

# 每篇文档必须记录

- 稳定 `document_id`；
- 标题、原始文本或可复核摘要；
- canonical URL 与 timestamp evidence URL；
- `original_published_at`、`available_at`、`revised_at`；
- 来源时区及转换依据；
- 检索/下载日期；
- source type、license/use note；
- 本地快照或归档标识；
- 内容哈希；
- 核验状态和核验人。

# 验收条件

```text
pre-cutoff document:  available_at <= prediction_cutoff
post-cutoff document: available_at > prediction_cutoff
```

以下情况退回：

- URL 404、跳到首页或与文本不对应；
- 只有搜索摘要，没有原始来源；
- 时间没有时区且无法确定来源时区；
- 用文章更新时间替代首次公开时间；
- 在看到 outcome 后修改 retrieval query；
- 为了制造泄漏手动选择最终 top-k；
- 文档直接由生成式模型虚构；
- 把价格涨跌结果写进 predictor evidence 的人工摘要。

# 交付物

1. 每个事件一份按
   `数据线/natural_point_in_time_candidate_template_v1.json` 填写的 JSON。
2. 合并后的
   `数据线/natural_point_in_time_source_ledger_v1.csv`。
3. 所有原始快照放入 `raw/`，只新增，不改写。
4. 一份问题清单，列出所有 `null`、时间冲突和修订版本。

# 分工边界

数据线负责来源收集和第一次核验；工程线负责 schema 校验、内容哈希、确定性检索、
时间过滤和实验运行；第二位核验者抽查全部 post-cutoff 文档及至少 20% 的
pre-cutoff 文档。
