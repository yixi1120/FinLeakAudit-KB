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
- 这是 FinLeakAudit 的 technical novelty 关键所在
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
