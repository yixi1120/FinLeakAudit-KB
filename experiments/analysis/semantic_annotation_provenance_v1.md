# Semantic annotation provenance v1

This record must be completed by the human coordinator before agreement numbers
or gold labels are reported. It is intentionally not a completion certificate.

## Frozen inputs

- Blind batch: `semantic_annotation_batch_v1.csv`
- Protocol: `wiki/experiments/semantic_attribution_annotation_protocol_v1.md`
- Expected pairs: 79
- Annotator A file: `semantic_annotations_annotator_a_v1.csv`
- Annotator B file: `semantic_annotations_annotator_b_v1.csv`

## Independence checklist

- [x] Annotator A and annotator B are two different people.
- [ ] Both received the blind batch, not the coordinator key.
- [ ] Neither viewed model identity, case identity, Clean/Audited predictions,
      outcome labels, automatic audit output, or leave-one-out results.
- [ ] They did not discuss individual samples before both files were frozen.
- [ ] Each annotator used a distinct, truthful `annotator_id` on all 79 rows.
- [x] The coordinator recorded the file hashes and repository freeze times below.

| Artifact | Human owner | Frozen at (ISO 8601) | SHA-256 |
|---|---|---|---|
| Annotator A | Zhang Yating | 2026-08-19T17:45:50+08:00 | `780ecee9c97324321c44f908f33b98db32317ee7df9b551a5d13c7d23e2e69f7` |
| Annotator B | Chen Junwei | 2026-08-22T15:30:40-04:00 | `b76892e8b8f13483b39bf811b024e314ea04a107b483b609cb75f15e4595452b` |

The current canonical files were frozen in commits `b452085` and `ab12c2a`.
Annotator A's labels originated in `be16042` and were refined in `57ad722`;
`b452085` normalized four exact claim spans without changing the four label
fields. Human independence attestations remain pending and must not be inferred
from Git metadata.

## Agreement and adjudication

After both files are frozen, run:

```bash
python3 experiments/analyze_semantic_annotations.py
```

The command validates both files, computes exact three-class agreement and
Cohen's kappa, reports `yes` versus `other` agreement, and writes only the
label disagreements to the adjudication template. A human adjudicator must fill
the blank `adjudicated_*` fields. Do not overwrite either original annotation
file.

Current generated artifacts:

- `semantic_annotation_agreement_v1.json`: 79 aligned pairs;
- `semantic_annotation_disagreements_v1.csv`: 13 rows with at least one label
  disagreement;
- `semantic_annotation_adjudication_template_v1.csv`: blank adjudication fields
  awaiting a third human reviewer.

## Sign-off

- Coordinator: pending
- Second annotator: pending
- Adjudicator: pending
- Gold-label freeze date: pending
