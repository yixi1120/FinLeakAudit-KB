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

- [ ] Annotator A and annotator B are two different people.
- [ ] Both received the blind batch, not the coordinator key.
- [ ] Neither viewed model identity, case identity, Clean/Audited predictions,
      outcome labels, automatic audit output, or leave-one-out results.
- [ ] They did not discuss individual samples before both files were frozen.
- [ ] Each annotator used a distinct, truthful `annotator_id` on all 79 rows.
- [ ] The coordinator recorded the file hashes and freeze times below.

| Artifact | Human owner | Frozen at (ISO 8601) | SHA-256 |
|---|---|---|---|
| Annotator A | pending | pending | pending |
| Annotator B | pending | pending | pending |

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

## Sign-off

- Coordinator: pending
- Second annotator: pending
- Adjudicator: pending
- Gold-label freeze date: pending
