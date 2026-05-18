# Verification Operators (Audit Primitives)

## 定义

FinLeakAudit 的审计协议由 5 个 operator 组成：

1. **Temporal Availability Operator** — 检查每条 evidence 在预测时点是否可用
2. **Evidence Attribution Operator** — 将预测理由拆成 claims 并映射到 evidence
3. **Support/Contradiction Operator** — 判断 evidence 与 claim 的关系（支持/反驳/无关）
4. **Evidence Ablation Operator** — 逐条删除 evidence 观察预测变化
5. **Forecast Revision Operator** — 删除泄漏证据后修正预测

## 为什么不用 "Skill"

- "Skill" 已与 OpenAI/Anthropic 产品生态和 SkillGuard-Robust 等安全审计论文绑定
- "Operator" 或 "Audit Primitive" 更正式、更像方法论文

## 相关论文

- [[SkillGuard_Robust]] — Agent Skill 安全审计（不同方向）
- [[SkillProbe]] — 同上
- [[VERAFI]] — policy-guided generation（类似理念但不同目标）
