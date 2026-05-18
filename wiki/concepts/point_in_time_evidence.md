# Point-in-Time Evidence

## 定义

每条 evidence 都附带了可用的时间元数据：
- publish_time：发布时间
- available_time：可用时间（可能晚于发布时间）
- prediction_date：预测日期
- market_open / market_close：市场交易时间
- revision_time：修订时间（如果有更正）

## 不是 temporal knowledge graph

Point-in-Time Evidence 强调的是：
- 证据条目层面的时间可用性约束
- 不是构建图结构
- 每条 evidence 是独立的、可审计的单元

## 相关论文

- [[TRACE]] — 做了 temporal KG，我们是 evidence 条目级
- [[FinCARDS]] — 做了结构化 cards，我们加了时间可用性
- [[CARAG]] — CTKG 有 temporal structure

## 本文论文中的用法

- 作为 Temporal Availability Operator 的输入格式
- 与 TRACE 的 KG 方法形成对比
