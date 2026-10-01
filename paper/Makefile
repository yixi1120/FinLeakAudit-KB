LATEX=pdflatex
PYTHON?=python3

FIGURE_SOURCES=figures/finleakaudit_pipeline.py figures/finleakaudit_results.py
FIGURES=figures/finleakaudit_pipeline.pdf figures/finleakaudit_results.pdf

.PHONY: all figures clean

all: main.pdf

figures: $(FIGURES)

figures/finleakaudit_pipeline.pdf: figures/finleakaudit_pipeline.py
	$(PYTHON) $<

figures/finleakaudit_results.pdf: figures/finleakaudit_results.py \
	../experiments/analysis/paper_forecast_audit_metrics_2026_09_03.csv \
	../experiments/analysis/natural_pit_10event_three_model_summary_v1.csv \
	../experiments/analysis/paper_semantic_attribution_metrics_2026_09_03.csv
	$(PYTHON) $<

main.pdf: main.tex references.bib $(FIGURES)
	$(LATEX) -interaction=nonstopmode -halt-on-error main.tex
	bibtex main
	$(LATEX) -interaction=nonstopmode -halt-on-error main.tex
	$(LATEX) -interaction=nonstopmode -halt-on-error main.tex

clean:
	$(RM) main.aux main.bbl main.blg main.log main.out main.pdf
	$(RM) figures/finleakaudit_pipeline.{alignment.json,alignment.svg,collision-audit.json,collision-audit.pdf,pdf,png,svg}
	$(RM) figures/finleakaudit_results.{alignment.json,alignment.svg,collision-audit.json,collision-audit.pdf,pdf,png,svg}
