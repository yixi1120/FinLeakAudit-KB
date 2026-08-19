---
title: Data and analysis line completion handoff
date: 2026-08-19
status: engineering-complete-human-verification-pending
---

# 本轮完成内容

## 分析线

- Annotator A 的 79 行文件通过完整性、枚举、置信度和 exact-span 校验。
- 4 个过短 span 已修正。
- `experiments/analyze_semantic_annotations.py` 可在 A/B 冻结后计算三分类
  agreement、Cohen's kappa 和 `yes` vs `other` agreement，并只导出分歧样本。
- `semantic_annotation_provenance_v1.md` 明确记录双人独立性和文件哈希。

## 数据线

- 10 个事件统一由 `tools/natural_event_registry.py` 冻结时间线和 evaluator-only
  outcome；四个 cutoff/horizon 和两个交易所错误已修正。
- 新增 9 份缺失的 SEC Exhibit/DOJ 判决正文。旧 `raw/` 文件没有被覆盖。
- validator 检查 10 个 manifest、195 个 active retrieval units、SHA-256、事件来源、
  cutoff/event/outcome 顺序和收益标签，当前为 0 errors。
- 离线 loader 从 HTML/XML/PDF 抽正文、稳定分块、按 `as_of` 过滤，并限制同一
  parent source 的候选版本和 top-k chunk 数。
- outcome-bounded lexical top-8 smoke test 中，10/10 事件均命中关键事件来源组。

# 可复现命令

```bash
python3 -m pip install -r requirements.txt
python3 tools/finalize_natural_event_metadata.py
python3 tools/validate_natural_retrieval_corpus.py
python3 tools/smoke_natural_retrieval.py
python3 -m unittest discover -s tests -v
```

# 仍需真人完成

1. 另一位真人使用 blind batch 独立完成 79 行 Annotator B；随后运行 agreement
   工具，并由真人裁决分歧。不能参考 A 文件代填。
2. 另一位真人填写 `natural_second_verification_batch_v1.csv` 的 139 行核验字段。

价格方向已用 Yahoo Finance chart API 与 StatMuse Money 做第二次公开源交叉检查，
10/10 方向一致；两边显示价格并不完全相同。投稿级数据仍应换成或补充许可清晰、
版本固定的市场数据源。

# 研究边界

当前自然语料是直接 SEC/官方文档构成的 primary-source candidate feed，配套的是
确定性 lexical retrieval。它不是保存下来的搜索引擎 SERP、生产系统检索轨迹，也还
没有完成三模型自然泄漏实验。因此可对外说“natural candidate corpus and offline
retrieval pipeline implemented”，不能说“已证明自然金融 RAG 普遍发生泄漏”。
