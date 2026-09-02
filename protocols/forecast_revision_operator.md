# Forecast Revision Operator

## 功能

发现泄漏证据后，执行预测修正并生成 revision log。

## 流程

1. 用时间规则确定不可在 cutoff 时使用的证据
2. 用 citation/semantic attribution 记录哪些 claim 受其影响
3. 从实际 Leaky evidence set 中删除时间无效证据
4. 使用剩余 evidence 重新生成预测
5. 比较 revision 前后并生成 revision log

Semantic attribution 不覆盖 temporal availability。已知 post-cutoff 的证据即使
未被引用、被 Judge 判定为 `no`，也不能留在 point-in-time 合规输入中。

## 输出示例

```json
{
  "original_prediction": "UP",
  "original_confidence": 0.82,
  "leaked_evidence": ["news_003"],
  "removed_evidence": ["news_003"],
  "revised_prediction": "NEUTRAL",
  "revised_confidence": 0.51,
  "revision_reason": "The strongest positive evidence was published after the prediction date. After removing it, remaining evidence provides mixed signals."
}
```

## 与 accuracy-driven revision 的区别

- FLAIRR-TS: 预测值不准 → 修改预测
- FinLeakAudit: 证据时间泄漏 → 删除证据 → 修改预测

## 评估指标

- Revision Success Rate: 修正后预测是否更接近真实结果
- Confidence Calibration Delta: 修正前后的置信度变化
- Rationale Purity: 修正后预测理由中泄漏证据引用率

## 可能被审稿人攻击的点

- "修正后的预测也不一定更准"
- 防御：我们不主张修正后预测一定更准，而是主张修正后的预测是基于可靠证据的、不依赖未来信息的、更 faithful 的预测。
