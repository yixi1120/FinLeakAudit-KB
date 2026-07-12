# Evidence Ablation in Financial Forecasting

## 定义

系统性地移除每条 retrieved evidence，观察预测方向和置信度的变化，量化每条证据对预测的边际影响。

## 输出示例

```
原始预测：UP, confidence = 0.82
删除 evidence_1 后：UP, confidence = 0.79
删除 evidence_2 后：NEUTRAL, confidence = 0.51 ← 翻转！
删除 evidence_3 后：UP, confidence = 0.80
```

结论：evidence_2 是预测翻转的驱动证据。如果 evidence_2 是泄漏证据，则原始预测不可信。

## 为什么重要

- 把 "删掉泄漏证据" 从 simple filter 升级为定量归因框架
- 这不是可以单独宣称的新方法；它的价值在于和 financial point-in-time availability、claim attribution 以及 forecast revision 组合。
- 最新 forecasting-faithfulness 工作已经使用 evidence ablation，因此论文中必须将其作为已有技术并清楚说明 FinLeakAudit 的集成边界。
- 审稿人说 "这不就是 if statement 吗" → ablation 回答这个问题

## 与 feature attribution / SHAP 的区别

| | Feature Attribution | Evidence Ablation |
|---|---|---|
| 对象 | 数值特征 | 文本证据条目 |
| 方法 | SHAP / LIME | 逐个删除+重预测 |
| 输出 | 特征重要性分数 | 预测翻转 + confidence delta |

## 本文论文中的用法

- RQ3/RQ4 的核心实验方法
- Contribution 2 的关键组成部分

## 论文定位提醒

将 leave-one-out change 称为 **marginal forecast sensitivity**，不要称为 causal effect。必须加入 delete-all-future-evidence、timestamp-only 和 citation-only baselines，避免 ablation 看起来只是一个更昂贵的过滤器。
