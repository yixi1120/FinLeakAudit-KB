---
title: FinLeakAudit 双线交叉核验行动手册 v1
date: 2026-08-19
status: ready-for-assignment
---

# 任务目标

本轮需要完成两项独立人工工作：

1. 对 79 条 claim-evidence pairs 完成 Annotator B 语义盲标；
2. 对 139 条 Natural corpus 文档完成第二人来源与时间核验。

这两项工作用于建立可信的人工标签和来源记录，不需要运行任何模型，也不需要启动
本地 Qwen。

# 人员隔离规则

- 做过 Annotator A 的人不能再做 Annotator B。
- 建设过 Natural 原始数据的人不能核验自己建设的数据。
- 最合适的安排是两位队员交叉换线。
- 如果执行者已经看过另一份答案，应更换执行者。
- 可以使用浏览器、翻译和表格工具，但最终判断必须由执行者本人逐行完成，不能让
  LLM 或脚本自动代填。

# 任务一：Annotator B 独立语义标注

## 输入和输出

输入文件：

```text
experiments/analysis/semantic_annotation_batch_v1.csv
```

输出文件：

```text
experiments/analysis/semantic_annotations_annotator_b_v1.csv
```

共 79 行。每一行表示一组：

```text
模型 rationale 中的一条 claim × 一条 cutoff 后 evidence
```

## 第一步：准备分支和文件

```bash
git pull origin main
git switch -c annotation-b-v1
cp experiments/analysis/semantic_annotation_batch_v1.csv \
   experiments/analysis/semantic_annotations_annotator_b_v1.csv
```

标注期间只能打开 B 文件。禁止查看：

- `semantic_annotations_annotator_a_v1.csv`；
- 模型名称和原始结果；
- Clean/Audited 预测；
- outcome label；
- 自动审计结果；
- leave-one-out 结果。

## 第二步：逐行判断

重点阅读三列：

- `claim_text`：需要判断的模型陈述；
- `pre_cutoff_evidence`：预测时点前可用证据；
- `post_cutoff_evidence_text`：预测时点后才可用的证据。

需要判断 claim 的核心事实是否依赖该条 post-cutoff evidence。

## 第三步：填写标注字段

| 字段 | 允许值或填写要求 |
|---|---|
| `label_semantic_dependency` | `yes` / `no` / `uncertain` |
| `label_relation` | `support` / `contradict` / `irrelevant` / `uncertain` |
| `label_exclusive_to_post_cutoff` | `yes` / `no` / `uncertain` |
| `label_should_remove` | `yes` / `no` / `uncertain` |
| `matched_claim_span` | 从 `claim_text` 原样复制最能体现依赖的片段 |
| `confidence_1_to_5` | 1 至 5 的整数 |
| `annotator_id` | 全部填写同一个匿名编号，例如 `annotator_b` |
| `notes` | 用一句话说明判断依据 |

判定原则：

- `yes`：claim 的核心事实明显来自 post-cutoff evidence；
- `no`：pre-cutoff evidence 已经支持该事实，或者 claim 与未来证据无关；
- `uncertain`：两边都可能支持，无法可靠区分；
- `support`：未来证据支持该 claim；
- `contradict`：未来证据反驳该 claim；
- `irrelevant`：两者没有实质关系。

特别要求：

- `label_semantic_dependency=yes` 时必须填写 `matched_claim_span`；
- span 必须是 `claim_text` 中能够逐字找到的原文子串，不能改写；
- 没有引用 evidence ID 不等于没有语义依赖；
- 不得根据预测是否正确、是否发生方向翻转来倒推标签；
- 不得批量填充相同标签，79 行必须逐行判断；
- `case_005` 等没有明确未来 ID 的 claim 仍需逐条阅读。

## 第四步：完成自检

提交前确认：

- 79 行全部完成；
- 四个 label 字段没有空值；
- 所有标签都属于允许枚举；
- confidence 全部为 1 至 5；
- 所有 dependency=`yes` 的行都有 exact span；
- 没有修改 `sample_id` 和其他样本内容列；
- CSV 表头和行顺序没有改变。

## 第五步：提交

```bash
git add experiments/analysis/semantic_annotations_annotator_b_v1.csv
git commit -m "analysis: add independent annotator B labels"
git push -u origin annotation-b-v1
```

预计耗时：2 至 4 小时。

# 任务二：Natural corpus 独立二次核验

## 输入和输出

需要直接填写：

```text
数据线/natural_second_verification_batch_v1.csv
```

共 139 行。该批次覆盖：

- 当前标记为 post-cutoff 的全部文档；
- availability time 尚未完全确认的文档；
- 每个事件至少 20% 的 pre-cutoff 文档样本。

## 第一步：准备分支

```bash
git pull origin main
git switch -c natural-second-verification-v1
```

不要重新运行下面的生成命令：

```bash
python3 tools/prepare_natural_second_verification.py
```

该命令会重新生成空白批次，可能覆盖已经填写的内容。

## 第二步：逐行核验来源内容

打开该行的 `source_url`，确认：

- 网页或文档能够访问；
- 公司、事件和标题对应正确；
- 页面内容与该行描述一致；
- 页面不是无关文档或错误跳转。

将判断填写到 `url_content_match`：

```text
yes / no / uncertain
```

## 第三步：逐行核验时间证据

打开 `timestamp_source_url`，寻找能够证明首次可用时间的原始依据，例如：

- SEC EDGAR acceptance timestamp；
- 公司新闻稿发布时间；
- 法院文件发布日期；
- 状态页更新记录；
- 带明确时区的原始页面元数据。

核对：

- `available_at` 是否与来源一致；
- 日期和具体时间是否正确；
- 时区是否正确；
- 该证据相对 `prediction_cutoff` 是 cutoff 前还是 cutoff 后；
- 页面是否存在修订时间与首次发布时间混淆。

将判断填写到 `timestamp_evidence_match`：

```text
yes / no / uncertain
```

如果来源只有日期、没有具体时间和时区，不要猜测，应填写 `uncertain`。

## 第四步：检查本地归档 hash

根据 `archive_path` 找到本地文件，运行：

```bash
shasum -a 256 "<archive_path>"
```

将输出与该行的 `content_sha256` 比较，并填写：

```text
archive_hash_match = yes / no
```

## 第五步：填写核验结论

| 字段 | 填写要求 |
|---|---|
| `second_verifier_id` | 固定匿名编号，例如 `verifier_b` |
| `url_content_match` | `yes` / `no` / `uncertain` |
| `timestamp_evidence_match` | `yes` / `no` / `uncertain` |
| `archive_hash_match` | `yes` / `no` |
| `decision` | `accept` / `reject` / `needs_adjudication` |
| `verification_notes` | 写明确认依据或具体问题 |
| `verified_at` | 带时区的 ISO 8601 时间 |

`verified_at` 示例：

```text
2026-08-19T21:30:00+08:00
```

`decision` 规则：

- `accept`：内容、时间证据和 archive hash 均一致；
- `reject`：来源对应错误、时间明显冲突或 archive hash 不一致；
- `needs_adjudication`：网页无法访问、只有日期没有时间、时区不明、首次发布时间和
  修订时间无法区分，或者存在其他无法独立判断的问题。

## 第六步：禁止修改的内容

不能修改：

- 前 10 列原始信息；
- `prediction_cutoff`；
- `available_at`；
- `source_url` 和 `timestamp_source_url`；
- `archive_path` 和 `content_sha256`；
- `raw/` 文件夹内的任何文件。

发现错误时，只在 `verification_notes` 里记录。元数据和 raw source 由项目协调者统一
处理，不能在核验过程中直接改正。

## 第七步：完成自检

提交前确认：

- 139 行全部检查；
- 最后七列全部填写；
- `decision` 只有三个允许值；
- 没有修改原始信息列；
- 没有修改 CSV 表头和行顺序；
- 没有覆盖或删除任何 raw source。

## 第八步：提交

```bash
git add 数据线/natural_second_verification_batch_v1.csv
git commit -m "data: complete independent natural source verification"
git push -u origin natural-second-verification-v1
```

预计耗时：5 至 8 小时。可以按事件分给多位没有参与原始数据建设的人，但每一行必须
由同一位独立核验者完整检查并签名。

# 协调者后续工作

两项任务交付后，项目协调者将：

1. 校验两个 CSV 的行数、枚举、空值、exact span 和样本完整性；
2. 运行 `python3 experiments/analyze_semantic_annotations.py`；
3. 计算 agreement、Cohen's kappa 和 `yes` vs `other` agreement；
4. 只对分歧标注进行人工 adjudication；
5. 处理 Natural 核验中的 `reject` 和 `needs_adjudication`；
6. 冻结最终文件、记录文件 hash、更新研究日志和 Git 提交历史。

# 最终交付清单

- [ ] `semantic_annotations_annotator_b_v1.csv`：79 行完成；
- [ ] `natural_second_verification_batch_v1.csv`：139 行完成；
- [ ] 两份文件分别由符合独立性要求的真人完成；
- [ ] 两位执行者分别提交个人分支和 commit；
- [ ] 未修改样本输入、原始元数据和 `raw/` 文件。
