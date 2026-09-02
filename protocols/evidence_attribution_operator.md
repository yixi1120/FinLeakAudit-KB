# Evidence Attribution Operator

## 功能

将预测理由拆解为原子 claims，逐条映射到支撑它的 retrieved evidence。

## 输入

```
预测理由: "The stock is likely to rise because analysts upgraded the company after strong earnings, and the technical indicators show bullish momentum."

Retrieved evidence:
- news_004: "Analysts raise target for Company A after Q2 beat" (T+1)
- news_005: "Company A reports strong Q2 earnings" (T-3)
- price_data: OHLCV showing MACD golden cross (T)
```

## 输出

```json
{
  "claims": [
    {
      "claim": "Analysts upgraded the company after strong earnings",
      "supporting_evidence": ["news_004", "news_005"],
      "evidence_times": ["T+1", "T-3"],
      "status": "partially_leaked_support"
    },
    {
      "claim": "Technical indicators show bullish momentum",
      "supporting_evidence": ["price_data"],
      "evidence_times": ["T"],
      "status": "valid_support"
    }
  ],
  "overall_status": "leaked_evidence_detected",
  "leaked_evidence_ids": ["news_004"]
}
```

## 关键设计决策

- 使用 LLM 还是规则做 attribution？
  - 建议：LLM 做 claim decomposition + evidence mapping，规则做时间验证
- Claim 粒度怎么定？
  - 建议：每个 claim 是单一可验证陈述，不过度拆分

## 当前实现边界（2026-09-02）

- LLM attribution 只接收 claim、cutoff 前证据文本和一条 cutoff 后候选证据；
  不接收 evidence ID、模型名称、预测结果或人工 gold label。
- `semantic_dependency=yes` 表示 claim 的核心内容被判定依赖候选证据，不表示
  该证据在时间上允许使用。
- 时间规则拥有 point-in-time 合规删除权。凡确定晚于 cutoff 的 evidence，在
  `full_semantic` 策略下都会删除，不由 LLM attribution 决定。
- `semantic_llm` selective removal 仅作为研究 baseline，用来测量语义判断本身，
  不得描述为合规过滤策略。

这一边界来自在线 smoke test：Judge 对 `case_005` 的 inventory-glut claim 给出
`yes, confidence=0.90`，但 cutoff 前 `e1` 已明确包含 severe inventory glut。
这是 high-confidence false positive，因此 semantic Judge 不能成为唯一删除门槛。

## 可能被审稿人攻击的点

- "LLM 做的 attribution 可靠吗？"
- 防御：报告 attribution 的 human evaluation agreement rate
