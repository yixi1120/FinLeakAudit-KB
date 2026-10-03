# Paper Build

This directory contains the AI4F 2026 submission draft. AI4F permits open-format PDF
submissions and recommends, but does not require, ACM formatting.

Build from this directory with:

```bash
make
```

The provisional author order is Ziyang Lu (The Hong Kong University of Science and
Technology), Junwei Chen (Johns Hopkins University), Yating Zhang (South China Normal
University), and Minzhen Lai (Imperial College London). Minzhen Lai's assigned scope is
independent external reproduction, model-stratified robustness analysis,
manuscript-to-artifact consistency auditing, related manuscript revisions, and
conference presentation preparation. Contributions must be verified against
repository-visible work records before the final submission freeze. Ziyang Lu is the
corresponding author using `zluca@connect.ust.hk`.
The reproducible submission snapshot is tagged `ai4f-2026-submission-v1` and documented
in [REPRODUCIBILITY.md](REPRODUCIBILITY.md). The manuscript uses a compact two-column
article layout; conversion to ACM `sigconf` remains optional under the venue rules.

Current evidence boundary:

- The controlled and 10-event natural replay results are complete.
- The 79-pair controlled attribution gold set is complete.
- The frozen 82-pair natural semantic hard set is not yet labeled and is not used for
  paper claims.
- The current study supports a controlled auditability claim, not leakage prevalence
  or forecasting-performance superiority.
