# Evidence Ablation Operator

## 功能

逐条删除 retrieved evidence，重新生成预测，量化每条证据的边际影响。

## 流程

```
for each evidence_i in retrieved_evidence:
    prediction_without_i = re_predict(evidence_set - {evidence_i})
    compare: prediction_without_i vs original_prediction
    record: prediction_flip, confidence_delta, direction_change
```

## 输出示例

```json
{
  "original_prediction": {"direction": "UP", "confidence": 0.82},
  "ablation_results": [
    {
      "removed_evidence": "evidence_1",
      "result_prediction": "UP",
      "confidence": 0.79,
      "confidence_delta": -0.03,
      "prediction_flip": false,
      "importance": "low"
    },
    {
      "removed_evidence": "evidence_2",
      "result_prediction": "NEUTRAL",
      "confidence": 0.51,
      "confidence_delta": -0.31,
      "prediction_flip": true,
      "importance": "high"
    }
  ]
}
```

## 为什么这是 technical novelty

- 不是简单的 "删掉泄漏证据"
- 而是量化每条证据的 marginal contribution
- 发现哪些证据是预测翻转的关键驱动因素

## 成本考虑

- 每做一次 ablation，需要 N+1 次 LLM 调用（N 条 evidence）
- 建议在 PoC 阶段限制 evidence 数量（≤10 条）
- 论文中需要报告 ablation 的计算成本

## 可能被审稿人攻击的点

- "这不就是 leave-one-out 特征重要性吗？"
- 防御：这不是数值特征的重要性排名，而是对 textual evidence 做 ablation，观察预测方向和理由的变化。每条 evidence 的移除可能导致 prediction rationale 完全不同。
