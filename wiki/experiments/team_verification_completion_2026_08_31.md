---
title: Team verification completion record
date: 2026-08-31
status: completed-with-documented-bounds
---

# Scope

This record closes the two-person cross-verification round:

1. dual independent annotation of 79 semantic claim-evidence pairs;
2. independent source, timestamp, and archive verification of 139 Natural corpus
   records.

# Semantic annotation

- Annotator A: Zhang Yating.
- Annotator B: Chen Junwei.
- Both annotators confirmed the blind and independent workflow in writing to the
  coordinator via WeChat; Lu Ziyang recorded the confirmations on 2026-08-31.
- Three-class semantic-dependency agreement: 77/79 (97.5%), Cohen's kappa 0.952.
- Binary `yes` versus `other` agreement: 79/79.
- Lu Ziyang adjudicated the 13 rows with at least one field disagreement.
- Final artifact: `experiments/analysis/semantic_annotation_adjudicated_v1.csv`.
  SHA-256: `1a98b66fa9c0760ce27e4dc85a8599d999a76d37c8fef9f70136e19baac41341`.

# Natural source verification

- Second verifier: Zhang Yating (`verifier_b`).
- Reviewed records: 139, with no changes to the ten protected source columns.
- Accepted: 133.
- Rejected: 1.
- Required coordinator adjudication: 5.
- Archive files present and SHA-256 matched: 139/139.
- Coordinator decisions are frozen in
  `数据线/natural_second_verification_adjudication_v1.csv`.
- Second-verifier batch SHA-256:
  `34cc64e38c23ff5f828b7fcc7549f8db98842b3689e25c7aa273db0c469f8bb5`.
- Coordinator adjudication SHA-256:
  `8400fe712e5053f641122557cb48a4c226f0c3d38ddd36da70fbe707fd8bb651`.

The rejected row, `natural_001_doc_011`, confused the PDF's update time with its
first publication time. Metadata was corrected to 05:30 UTC published and 09:45
UTC revised. Four unresolved date-only CrowdStrike pages remain blocked. The
JetBlue court document retains a clearly labeled date-only conservative upper
bound because its publication date is still unambiguously post-cutoff.

# Experiment impact

The corrected CrowdStrike timestamp and the JetBlue date-level bound do not
change temporal condition membership. No retrieved text or model-visible input
changes, so the five-event replay does not require paid model reruns. Future runs
must use the corrected canonical metadata.

# Remaining boundary

This completion closes the current annotation and source-verification handoff. It
does not solve the paper-scale sample-size limitation: the natural replay still
contains five executed events and two models.
