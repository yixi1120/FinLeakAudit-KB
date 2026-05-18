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

## 可能被审稿人攻击的点

- "LLM 做的 attribution 可靠吗？"
- 防御：报告 attribution 的 human evaluation agreement rate
