---
title: "Structured Security Auditing and Robustness Enhancement for Untrusted Agent Skills"
year: 2026
venue: arXiv
ccf_level: preprint
arxiv: "2604.25109"
tags: [agent-skill-security, pre-load-auditing, role-aware-evidence, semantic-verification]
status: skimmed
collision_risk: medium
must_cite: true
---

# 一句话总结

研究不可信 Agent Skill package 的 pre-load 安全审计，三分类：safe / suspicious / malicious。是 "Skill auditing" 方向的代表论文。

# 研究任务

Agent Skill 安全审计

# 方法

- Role-aware evidence extraction
- Selective semantic verification
- Consistency-preserving adjudication
- 三分类器: safe / suspicious / malicious

# 和 FinLeakAudit 的相似点

- 都叫 "auditing"
- 都用了 "skill" 概念（如果我们也用的话）

# 和 FinLeakAudit 的区别

- SkillGuard 审计 skill package 是否恶意/安全
- FinLeakAudit 审计金融预测中 evidence 是否时间泄漏
- 完全不同的任务和领域

# 撞车风险

Medium — 命名撞车风险，任务不撞

# 命名影响

**促使我们从 "Skill-based Audit" 转向 "Verification Operators"**，避免被误分类到 Agent Skill 安全审计方向。

# 可以引用的位置

- Related Work: Agent Skill 审计背景
- 区分我们的 audit target 是 evidence 不是 skill package
