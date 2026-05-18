# Temporal Availability Operator

## 输入

```json
{
  "evidence_id": "news_003",
  "prediction_date": "2024-05-10 09:30:00 ET",
  "publish_time": "2024-05-11 08:00:00 ET",
  "source_type": "news"
}
```

## 输出

```json
{
  "evidence_id": "news_003",
  "temporal_status": "invalid_future_evidence",
  "leakage_type": "post_prediction_news",
  "severity": "high",
  "reason": "publish_time is after prediction_date by 1 day"
}
```

## 检查规则（多层）

1. **publish_time vs prediction_date** — 基本检查
2. **available_time vs prediction_date** — 新闻可能发布后可立即获取或有延迟
3. **market_open vs publish_time** — 盘后发布的财报在下一个交易日开盘前是否可用
4. **timezone normalization** — 跨时区映射到统一时间
5. **revision_time** — 修订稿的原始时间 vs 修订时间
6. **data_vendor_timestamp** — 数据商的时戳可能与原始时间不一致

## 特殊情况

| 情况 | 处理 |
|---|---|
| After-hours release (16:00 ET) | 如果 prediction 在盘后发布后、次日开盘前，可能可用 |
| Weekend news | 如果 prediction_date 是周一，周末新闻是否可用取决于 retrieval window |
| Revised article | 用 original publish_time，标记 revision_time |
| Timezone ambiguity | 归一化到 market timezone |
| Press release vs news report | 区分事件发生时间和新闻报道时间 |

## JSON Schema

详见 prompts/ 中的 audit schemas

## 可能被审稿人攻击的点

- "这不就是一个 if statement 吗？"
- 防御：多级时间约束 ≠ 简单时间戳比较。需要处理时区、盘后、修订稿、数据供应商时戳差异。

## 防御话术

"Temporal Availability Operator enforces multi-level checks beyond simple timestamp comparison, including timezone normalization, market open/close alignment, revision tracking, and data vendor timestamp reconciliation."
