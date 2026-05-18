# Leakage-Driven Forecast Revision

## 定义

当 FinLeakAudit 检测到预测中使用了时间泄漏证据后，不是简单地报错或标记，而是执行：
1. 删除污染证据
2. 重新生成预测
3. 比较修正前后的预测方向、置信度和预测理由
4. 输出 revision log

## 与 accuracy-driven revision 的区别

| | Accuracy-driven | Leakage-driven |
|---|---|---|
| 触发器 | 预测值不准 | 证据时间泄漏 |
| 修正方式 | 调整参数/推理 | 删除污染证据再预测 |
| 代表论文 | FLAIRR-TS, SETS | FinLeakAudit (本文) |
| 核心问题 | "怎么预测更准" | "预测用了不该用的证据吗" |

## 相关论文

- [[FLAIRR_TS]] — accuracy-driven self-correction
- [[FinAgent_RAG]] — self-verification for QA

## 本文论文中的用法

- RQ4: 修正后预测是否更可靠？
- 核心贡献点之一
