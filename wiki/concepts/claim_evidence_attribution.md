# Claim-Evidence Attribution

## 定义

将 Agentic RAG 生成的预测理由拆解为原子 claims，然后逐条映射到支撑它的 retrieved evidence。

示例：
- 预测理由："The stock is likely to rise because analysts upgraded after strong earnings."
- 拆解 → Claim: "Analysts upgraded the company after strong earnings"
- 归因 → Supporting evidence: news_004, available at T+1

## 为什么重要

- 光检测"检索库里有未来新闻"不够，必须证明"模型真的用了未来新闻来支撑预测"
- Attribution 是 evidence ablation 的前置步骤
- 把 "if statement" 升级成可审计的归因框架

## 与相近概念的区别

| 概念 | 区别 |
|---|---|
| Fact-checking | 检查事实真假 |
| Claim-evidence attribution | 检查 claim 是否被 evidence 支撑，不判断真假 |
| Faithfulness evaluation | 更广的 RAG 指标，attribution 是其中一部分 |

## 相关论文

- [[FinVet]] — source attribution
- [[Bayesian_RAG_Finance]] — faithfulness/evidence support 指标
