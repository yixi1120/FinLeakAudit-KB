# Support / Contradiction Operator

## 功能

判断每条 evidence 与每个 claim 的关系：supports / contradicts / neutral / unsupported

## 分类

| 关系 | 定义 | 示例 |
|---|---|---|
| supports | evidence 直接支撑 claim | "earnings beat" → "stock likely up" |
| contradicts | evidence 与 claim 冲突 | "earnings miss" → "stock likely up" |
| neutral | evidence 相关但不直接支撑 | "company announces new office" → "stock likely up" |
| unsupported | claim 没有对应 evidence | "market sentiment is positive" 无来源 |

## 安全表述

**不要用：** "causal relation" / "causally supports"
**使用：** "supports" / "contradicts" / "is consistent with" / "is attributed to"

## 可能被审稿人攻击的点

- "support 关系的判断标准是什么？"
- 防御：定义基于 textual entailment 的判定标准，报告 inter-annotator agreement
