# FinLeakAudit Research Wiki

> 面向 Agentic RAG 金融预测的证据级泄漏审计框架 — 研究知识库

## 项目定位

FinLeakAudit 不是一个新的股票预测模型。它是一个面向金融 Agentic RAG 系统的**证据级审计层**：检测预测中是否使用了未来证据，追踪预测理由由哪些证据支持，量化每条证据对预测的边际影响，并在发现泄漏后删除污染证据、修正预测和置信度。

## 核心理念

现有 Agentic RAG 金融预测系统可能因为检索、引用或解释了预测时点之后才可获得的证据，导致回测收益和预测准确率虚高（forecast inflation / profit mirage）。FinLeakAudit 检测 evidence-level leakage、量化其对预测的影响，并通过 verifier-guided revision 修正预测。

## 知识库结构

```
FinLeakAudit-KB/
├── AGENTS.md              # Agent 规则文件
├── README.md              # 本文件
├── index.md               # 全局索引
├── research_log.md        # 研究日志
│
├── raw/                   # 不可变原始材料
│   ├── papers/            # PDF / search results
│   ├── tavily_reports/    # Tavily 搜索报告
│   └── chat_exports/      # 对话总结
│
├── wiki/                  # LLM 维护的知识层
│   ├── papers/            # 论文卡片
│   ├── concepts/          # 概念页
│   ├── competitors/       # 竞品对比
│   ├── experiments/       # 实验设计
│   ├── metrics/           # 指标定义
│   └── writing/           # 论文写作
│
├── matrices/              # 对比矩阵
├── protocols/             # 审计协议 / 算子
└── prompts/               # 可复用 prompt
```

## 快速入口

- 核心概念：[[evidence_level_temporal_leakage]] | [[forecast_inflation]] | [[leakage_driven_forecast_revision]]
- 主要竞品：[[CARAG]] | [[Profit_Mirage]] | [[FLAIRR_TS]]
- 竞品矩阵：[[collision_matrix]]
- 审计算子：[[temporal_availability_operator]] | [[evidence_ablation_operator]]

## 使用方式

向 Agent 提问时，引用 wiki 中的页面：

> "基于 wiki/papers/CARAG.md 和 wiki/concepts/evidence_level_temporal_leakage.md，写一段 Related Work"

而不是：

> "帮我找 CARAG 和我有什么区别"
