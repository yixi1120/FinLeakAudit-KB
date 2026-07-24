---
title: FinLeakAudit verified smoke pilot results
date: 2026-07-24
dataset: 数据线/cases_pilot_v3_smoke_eligible.jsonl
model: deepseek-chat
status: preliminary
---

# 实验目的

用最小可运行轮次验证三件事：

1. 加入未来证据后，预测是否发生变化；
2. auditor 是否能识别并移除被引用的未来证据；
3. 移除后，audited prediction 是否回到 clean prediction。

本轮不是预测准确率实验，也不能支持自然金融 RAG 中泄漏普遍存在的结论。

# 数据与运行

- 数据文件：`数据线/cases_pilot_v3_smoke_eligible.jsonl`
- case 数量：3（case_002 Target、case_004 Novavax、case_005 Enphase）
- 每个 case：clean、leaky、audited，并执行 leave-one-evidence-out ablation
- 模型：DeepSeek `deepseek-chat`
- 运行命令：

```bash
cd experiments
python3 run_experiment.py \
  --model deepseek \
  --cases '../数据线/cases_pilot_v3_smoke_eligible.jsonl' \
  --with-ablation \
  --run-name pilot3_verified_20260724 \
  --overwrite
```

- 结果文件：`experiments/results/deepseek_pilot3_verified_20260724_ablation_results.jsonl`
- 错误数：0

# 结果

| 指标 | 结果 | 解释 |
|---|---:|---|
| rationale 引用未来证据 | 3/3 = 100% | 三个 leaky prediction 都引用了 e4 |
| clean -> leaky 方向翻转 | 2/3 = 66.7% | Target、Novavax 发生翻转 |
| future evidence 是 flip driver | 2/3 = 66.7% | leave-one-out 中移除 e4 会改变方向 |
| audited 回到 clean 方向 | 3/3 = 100% | 这是 recovery-to-clean，不是预测正确率 |
| 平均 confidence 变化 | -0.067 | leaky 相比 clean 的平均置信度变化 |
| clean prediction 命中 gold | 0/3 | 三个 case 的 gold label 均为 UP，模型 clean 均为 DOWN |
| leaky prediction 命中 gold | 2/3 | Target、Novavax 在加入不可用的未来证据后命中 gold |
| audited prediction 命中 gold | 0/3 | 审计恢复了 clean 方向，但没有提高本轮预测准确率 |

# 按 case 结果

| Case | Clean | Leaky | Audited | 移除证据 | Flip driver |
|---|---|---|---|---|---|
| Target | DOWN | UP | DOWN | e4 | e4 |
| Novavax | DOWN | UP | DOWN | e4 | e4 |
| Enphase | DOWN | DOWN | DOWN | e4 | 否 |

# 可对外表达

可以谨慎表述为：

> In a three-case verified smoke pilot, future evidence was cited in all leaky rationales; it changed the forecast direction in two cases, and removing the cited future evidence restored the clean-condition direction in all three cases.

必须同时说明：本轮只有 3 个 case；clean、leaky、audited 的预测命中分别为 0/3、2/3、0/3。两个 leaky 预测在事后变得正确，恰恰说明不可用的未来证据会虚高预测表现。结果只能证明 pipeline 的敏感性和审计流程可运行，不能证明 FinLeakAudit 提高了金融预测性能。

# 下一步

1. 将 4 个被排除 case 重建为时间顺序正确的案例。
2. 将 25 条 synthetic evidence 替换为真实 point-in-time 来源，或单独划入 Controlled-Hard synthetic split。
3. 扩展至至少 20 个真实 case，再计算 detection precision/recall、flip-driver precision、recovery rate 和成本。
