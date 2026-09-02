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

## 当前状态（2026-09-02）

该字段目前只是 semantic Judge 的诊断输出，尚未进入删除或 revision 决策。在线
smoke 中出现过 `relation=contradict`，但 reason 实际描述候选未来证据支持 claim 的
内部不一致。因此在完成独立人工标注、方向定义和 agreement 评测前，不报告该算子
的准确率，也不把它描述为已实现的可靠 operator。

## 可能被审稿人攻击的点

- "support 关系的判断标准是什么？"
- 防御：定义基于 textual entailment 的判定标准，报告 inter-annotator agreement
