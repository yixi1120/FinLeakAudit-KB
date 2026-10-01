# Manuscript figures

The figures are generated with Python/Matplotlib from frozen experiment summaries.
They use the `nature-figure` workflow for editable vector output, panel alignment,
rendered-text checks, and collision auditing.

## Figure contracts

### Pipeline figure

- Core conclusion: FinLeakAudit separates evidence availability, prediction,
  auditing, revision, and outcome evaluation so future information cannot enter a
  removal decision through the evaluator.
- Archetype: schematic-led workflow.
- Source data: none; the diagram encodes the protocol in `paper/main.tex`.

### Results figure

- Core conclusion: post-cutoff evidence frequently enters rationales and sometimes
  changes forecasts; revision usually restores the cutoff-safe direction, while
  attribution and Backfill results retain important limitations.
- Archetype: quantitative grid.
- Source data:
  - `experiments/analysis/paper_forecast_audit_metrics_2026_09_03.csv`
  - `experiments/analysis/natural_pit_10event_three_model_summary_v1.csv`
  - `experiments/analysis/paper_semantic_attribution_metrics_2026_09_03.csv`
- Intervals: Wilson 95% confidence intervals for conditional recovery proportions.
- Replicate unit: one case/event evaluated by one model.
- Raster note: the workshop manuscript embeds vector PDF figures, so TIFF is not
  generated; the 600-dpi PNG files are review previews rather than submission assets.

## Rendered QA note

- Panel alignment and the 5-pt rendered glyph floor pass for both figures.
- The pipeline collision audit passes with no findings.
- The results collision audit reports one `text-fill-edge` warning for the
  `F1 0.941` label at the white axes boundary. Final-size inspection confirms that
  the label is clear of the data line, markers, grid, legend, and adjacent text; the
  warning is retained as a reviewed detector-boundary false positive.

## Rebuild

```bash
python3 paper/figures/finleakaudit_pipeline.py
python3 paper/figures/finleakaudit_results.py
make -C paper
```

Set `NATURE_FIGURE_SCRIPTS` when the `nature-figure` Skill is installed outside
its default Codex location.
