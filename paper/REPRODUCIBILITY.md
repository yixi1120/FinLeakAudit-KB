# AI4F 2026 Reproducibility Snapshot

This document freezes the paper-facing FinLeakAudit pilot at Git tag
`ai4f-2026-submission-v1`. The snapshot supports the claims in `paper/main.tex`; it
does not claim that provider APIs are bitwise deterministic.

## Environment

- Python: 3.11
- LaTeX: pdfLaTeX with BibTeX
- DeepSeek: `deepseek-chat`
- Zhipu: `glm-4-flashx-250414`
- Qwen: `Qwen2.5-14B-Instruct` GGUF `Q4_K_M` through llama.cpp
- Inference temperature: `0.0`

Create the analysis environment from the repository root:

```bash
uv venv .venv --python 3.11
uv pip install --python .venv/bin/python -r requirements.txt
```

Local Qwen inference requires a separate llama.cpp installation. API reruns require
the provider credentials described in `.env.example`. The frozen outputs are retained
so rebuilding the reported tables and figures does not require new paid model calls.

## Frozen Inputs

The machine-readable hashes, expected headline counts, and commands are stored in
`paper/submission_manifest_ai4f_2026.json`. Verify them with:

```bash
.venv/bin/python -m unittest tests.test_submission_manifest -v
```

## Reproduce Analyses

```bash
.venv/bin/python experiments/analyze_natural_10event.py
.venv/bin/python experiments/build_paper_results_snapshot.py
.venv/bin/python experiments/analyze_semantic_baselines.py
```

## Rebuild Figures and Paper

```bash
make -C paper PYTHON=../.venv/bin/python
```

The manuscript embeds vector PDFs generated from the frozen summary files. PNG and
SVG exports in `paper/figures/` are review and editing artifacts.

## Verification

```bash
.venv/bin/python -m unittest discover -s tests
```

The submission snapshot expects 103 tests to pass. Model-provider aliases may change
behind stable API names, so any new online run must record its date, model identifier,
retry history, token use, and output as a new artifact rather than overwriting this
snapshot.
