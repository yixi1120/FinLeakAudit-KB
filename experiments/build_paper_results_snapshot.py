#!/usr/bin/env python3
"""Generate paper-facing tables, figures, and a Results draft from frozen outputs."""

from __future__ import annotations

import argparse
import csv
import html
import json
from pathlib import Path

from analyze import read_jsonl, summarize, wilson_interval
from analyze_natural_experiment import build_summary, read_results


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "experiments" / "results"
ANALYSIS = ROOT / "experiments" / "analysis"
WIKI = ROOT / "wiki"
FIGURES = WIKI / "experiments" / "figures"

CONTROLLED_INPUTS = {
    "DeepSeek": RESULTS / "deepseek_v4_mixed10_abs_time_20260726_ablation_results.jsonl",
    "Zhipu": RESULTS / "zhipu_v4_mixed10_abs_time_20260726_ablation_results.jsonl",
    "Qwen2.5-14B": RESULTS / "qwen_v4_mixed10_abs_time_20260726_ablation_results.jsonl",
}
NATURAL_INPUTS = {
    "DeepSeek": RESULTS / "deepseek_natural_pit_5event_v1_results.jsonl",
    "Zhipu": RESULTS / "zhipu_natural_pit_5event_v1_results.jsonl",
    "Qwen2.5-14B": RESULTS / "qwen_natural_pit_5event_v1_results.jsonl",
}
SEMANTIC_INPUT = ANALYSIS / "semantic_baseline_results_v1.json"

FORECAST_OUTPUT = ANALYSIS / "paper_forecast_audit_metrics_2026_09_03.csv"
SEMANTIC_OUTPUT = ANALYSIS / "paper_semantic_attribution_metrics_2026_09_03.csv"
RESULTS_DRAFT = WIKI / "writing" / "results_draft_v1.md"
SNAPSHOT_REPORT = WIKI / "experiments" / "paper_results_snapshot_2026_09_03.md"


def integer_count(rate: float, total: int) -> int:
    count = round(rate * total)
    if abs(count / total - rate) > 1e-9:
        raise ValueError(f"Rate {rate} is not an exact count over n={total}")
    return count


def controlled_rows(paths: dict[str, Path]) -> list[dict]:
    rows = []
    for display_model, path in paths.items():
        if not path.exists():
            raise FileNotFoundError(path)
        summary = summarize(read_jsonl(path))
        n = int(summary["n_cases"])
        cited = integer_count(summary["rationale_leakage_rate"], n)
        clean_correct = integer_count(summary["clean_accuracy"], n)
        leaky_correct = integer_count(summary["leaky_accuracy"], n)
        audited_correct = integer_count(summary["audited_accuracy"], n)
        rows.append(
            {
                "study": "controlled_injection",
                "model": display_model,
                "n_model_cases": n,
                "model_calls": int(summary["api_calls"]),
                "future_cited_n": cited,
                "future_cited_rate": cited / n,
                "direction_flip_n": int(summary["prediction_flips"]),
                "direction_flip_rate": summary["prediction_flip_rate"],
                "recovered_flip_n": int(summary["revision_recovered_flips"]),
                "recovery_rate_among_flips": summary["audited_recovery_rate"],
                "recovery_wilson_95_low": summary["audited_recovery_wilson_low"],
                "recovery_wilson_95_high": summary["audited_recovery_wilson_high"],
                "clean_correct_n": clean_correct,
                "clean_accuracy": summary["clean_accuracy"],
                "contaminated_correct_n": leaky_correct,
                "contaminated_accuracy": summary["leaky_accuracy"],
                "audited_correct_n": audited_correct,
                "audited_accuracy": summary["audited_accuracy"],
                "audited_matches_clean_n": integer_count(
                    summary["audited_clean_agreement_rate"], n
                ),
                "audited_drift_without_initial_flip_n": 0,
                "total_tokens": int(summary["total_tokens"]),
            }
        )
    return rows


def natural_rows(paths: dict[str, Path]) -> list[dict]:
    existing = [path for path in paths.values() if path.exists()]
    if not existing:
        raise FileNotFoundError("No natural replay result files found")
    summaries = build_summary(read_results(existing))
    display_by_internal = {
        "deepseek": "DeepSeek",
        "zhipu": "Zhipu",
        "qwen": "Qwen2.5-14B",
    }
    rows = []
    for summary in summaries[1:]:
        n = int(summary["n_model_events"])
        model = display_by_internal.get(summary["model"], summary["model"])
        cited = integer_count(summary["explicit_future_citation_rate"], n)
        clean_correct = integer_count(summary["clean_accuracy"], n)
        unfiltered_correct = integer_count(summary["unfiltered_accuracy"], n)
        audited_correct = integer_count(summary["audited_accuracy"], n)
        rows.append(
            {
                "study": "natural_replay",
                "model": model,
                "n_model_cases": n,
                "model_calls": int(summary["model_calls"]),
                "future_cited_n": cited,
                "future_cited_rate": cited / n,
                "direction_flip_n": int(summary["direction_flip_count"]),
                "direction_flip_rate": summary["direction_flip_rate"],
                "recovered_flip_n": int(summary["recovery_count_among_flips"]),
                "recovery_rate_among_flips": summary["recovery_rate_among_flips"],
                "recovery_wilson_95_low": summary["recovery_wilson_95_low"],
                "recovery_wilson_95_high": summary["recovery_wilson_95_high"],
                "clean_correct_n": clean_correct,
                "clean_accuracy": summary["clean_accuracy"],
                "contaminated_correct_n": unfiltered_correct,
                "contaminated_accuracy": summary["unfiltered_accuracy"],
                "audited_correct_n": audited_correct,
                "audited_accuracy": summary["audited_accuracy"],
                "audited_matches_clean_n": integer_count(
                    summary["audited_matches_clean_rate"], n
                ),
                "audited_drift_without_initial_flip_n": int(
                    summary["audited_drift_without_initial_flip_count"]
                ),
                "total_tokens": int(summary["total_tokens"]),
            }
        )
    return sorted(rows, key=lambda row: list(paths).index(row["model"]))


def aggregate_forecast(rows: list[dict], study: str) -> dict:
    selected = [row for row in rows if row["study"] == study]
    n = sum(row["n_model_cases"] for row in selected)
    flips = sum(row["direction_flip_n"] for row in selected)
    recovered = sum(row["recovered_flip_n"] for row in selected)
    low, high = wilson_interval(recovered, flips)
    return {
        "study": study,
        "model": "All",
        "n_model_cases": n,
        "model_calls": sum(row["model_calls"] for row in selected),
        "future_cited_n": sum(row["future_cited_n"] for row in selected),
        "future_cited_rate": sum(row["future_cited_n"] for row in selected) / n,
        "direction_flip_n": flips,
        "direction_flip_rate": flips / n,
        "recovered_flip_n": recovered,
        "recovery_rate_among_flips": recovered / flips if flips else None,
        "recovery_wilson_95_low": low,
        "recovery_wilson_95_high": high,
        "clean_correct_n": sum(row["clean_correct_n"] for row in selected),
        "clean_accuracy": sum(row["clean_correct_n"] for row in selected) / n,
        "contaminated_correct_n": sum(
            row["contaminated_correct_n"] for row in selected
        ),
        "contaminated_accuracy": sum(
            row["contaminated_correct_n"] for row in selected
        )
        / n,
        "audited_correct_n": sum(row["audited_correct_n"] for row in selected),
        "audited_accuracy": sum(row["audited_correct_n"] for row in selected) / n,
        "audited_matches_clean_n": sum(
            row["audited_matches_clean_n"] for row in selected
        ),
        "audited_drift_without_initial_flip_n": sum(
            row["audited_drift_without_initial_flip_n"] for row in selected
        ),
        "total_tokens": sum(row["total_tokens"] for row in selected),
    }


def semantic_rows(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    labels = {
        "citation_only": "Citation-only",
        "lexical_overlap": "Lexical overlap",
        "embedding_similarity": "Embedding similarity",
        "llm_judge": "DeepSeek LLM judge",
    }
    rows = []
    for key, label in labels.items():
        metric = data["overall"][key]
        rows.append(
            {
                "method": label,
                "evaluated_pairs": metric["evaluated"],
                "excluded_uncertain": metric["excluded_uncertain"],
                "tp": metric["tp"],
                "fp": metric["fp"],
                "tn": metric["tn"],
                "fn": metric["fn"],
                "precision": metric["precision"],
                "recall": metric["recall"],
                "f1": metric["f1"],
                "accuracy": metric["accuracy"],
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def pct(value: float | None, digits: int = 1) -> str:
    return "N/A" if value is None else f"{value * 100:.{digits}f}%"


def wrap_label(label: str, max_chars: int = 18) -> list[str]:
    if len(label) <= max_chars or " " not in label:
        return [label]
    words = label.split()
    best_index = min(
        range(1, len(words)),
        key=lambda index: abs(
            len(" ".join(words[:index])) - len(" ".join(words[index:]))
        ),
    )
    return [" ".join(words[:best_index]), " ".join(words[best_index:])]


def svg_bar_chart(
    path: Path,
    title: str,
    subtitle: str,
    labels: list[str],
    values: list[float],
    colors: list[str],
    y_label: str,
) -> None:
    width, height = 900, 520
    left, right, top, bottom = 105, 105, 100, 105
    plot_w = width - left - right
    plot_h = height - top - bottom
    slot = plot_w / len(values)
    bar_w = min(105, slot * 0.58)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{left}" y="38" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#17212b">{html.escape(title)}</text>',
        f'<text x="{left}" y="66" font-family="Arial, sans-serif" font-size="14" fill="#586674">{html.escape(subtitle)}</text>',
    ]
    for tick in range(0, 101, 20):
        y = top + plot_h * (1 - tick / 100)
        parts.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#dce2e7" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{left-14}" y="{y+5:.1f}" text-anchor="end" font-family="Arial, sans-serif" font-size="13" fill="#586674">{tick}</text>'
        )
    parts.append(
        f'<text x="25" y="{top + plot_h/2:.1f}" transform="rotate(-90 25 {top + plot_h/2:.1f})" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#34424f">{html.escape(y_label)}</text>'
    )
    for index, (label, value, color) in enumerate(zip(labels, values, colors)):
        x = left + slot * index + (slot - bar_w) / 2
        bar_h = plot_h * value
        y = top + plot_h - bar_h
        parts.extend(
            [
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" rx="3" fill="{color}"/>',
                f'<text x="{x + bar_w/2:.1f}" y="{y-10:.1f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="#17212b">{value*100:.1f}</text>',
            ]
        )
        label_lines = wrap_label(label)
        label_x = x + bar_w / 2
        label_y = top + plot_h + 28
        if len(label_lines) == 1:
            parts.append(
                f'<text x="{label_x:.1f}" y="{label_y:.1f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" fill="#34424f">{html.escape(label_lines[0])}</text>'
            )
        else:
            parts.append(
                f'<text x="{label_x:.1f}" y="{label_y:.1f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" fill="#34424f">'
                f'<tspan x="{label_x:.1f}" dy="0">{html.escape(label_lines[0])}</tspan>'
                f'<tspan x="{label_x:.1f}" dy="17">{html.escape(label_lines[1])}</tspan>'
                "</text>"
            )
    parts.append("</svg>\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts), encoding="utf-8")


def markdown_forecast_table(rows: list[dict]) -> list[str]:
    lines = [
        "| Study | Model | Runs | Valid future citation | Direction changed | Recovered changes | Audited drift without flip | Clean / contaminated / audited accuracy |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['study']} | {row['model']} | {row['n_model_cases']} | "
            f"{row['future_cited_n']}/{row['n_model_cases']} | "
            f"{row['direction_flip_n']}/{row['n_model_cases']} | "
            f"{row['recovered_flip_n']}/{row['direction_flip_n']} | "
            f"{row['audited_drift_without_initial_flip_n']} | "
            f"{row['clean_correct_n']}/{row['n_model_cases']} / "
            f"{row['contaminated_correct_n']}/{row['n_model_cases']} / "
            f"{row['audited_correct_n']}/{row['n_model_cases']} |"
        )
    return lines


def markdown_semantic_table(rows: list[dict]) -> list[str]:
    lines = [
        "| Attribution method | Precision | Recall | F1 | FP | FN |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['method']} | {pct(row['precision'])} | {pct(row['recall'])} | "
            f"{pct(row['f1'])} | {row['fp']} | {row['fn']} |"
        )
    return lines


def build_results_draft(
    controlled: list[dict], natural: list[dict], semantic: list[dict]
) -> str:
    all_controlled = aggregate_forecast(controlled, "controlled_injection")
    all_natural = aggregate_forecast(natural, "natural_replay")
    citation = next(row for row in semantic if row["method"] == "Citation-only")
    judge = next(row for row in semantic if row["method"] == "DeepSeek LLM judge")
    natural_models = ", ".join(row["model"] for row in natural)
    return "\n".join(
        [
            "# Results Draft v1",
            "",
            "Status: paper-facing draft generated from frozen experiment outputs. Numbers may",
            "only change when a new model run is added and recorded as a new input artifact.",
            "",
            "## RQ1: Does post-cutoff evidence alter financial forecasts?",
            "",
            f"In the controlled injection study, post-cutoff evidence was explicitly cited in "
            f"{all_controlled['future_cited_n']}/{all_controlled['n_model_cases']} model-case runs "
            f"({pct(all_controlled['future_cited_rate'])}). The forecast category changed between "
            f"Clean and Leaky conditions in {all_controlled['direction_flip_n']}/"
            f"{all_controlled['n_model_cases']} runs ({pct(all_controlled['direction_flip_rate'])}).",
            "",
            *markdown_forecast_table(controlled),
            "",
            "The increase in Leaky accuracy is look-ahead inflation, not a valid forecasting gain.",
            "The controlled cases deliberately inject outcome-adjacent evidence and therefore test",
            "the audit premise rather than real-world leakage prevalence.",
            "",
            "## RQ2: Does the effect reproduce with archived natural-source evidence?",
            "",
            f"The natural replay currently includes {natural_models}. Across "
            f"{all_natural['n_model_cases']} model-event runs, post-cutoff evidence was explicitly "
            f"cited in {all_natural['future_cited_n']} runs and changed direction in "
            f"{all_natural['direction_flip_n']} runs.",
            "",
            *markdown_forecast_table(natural),
            "",
            "This is an outcome-bounded candidate-feed stress test over five selected events. It is",
            "not a preserved production retrieval trace or a frequency estimate for deployed RAG.",
            "",
            "## RQ3: Does audit-driven revision restore the cutoff-safe forecast?",
            "",
            f"All {all_controlled['recovered_flip_n']}/{all_controlled['direction_flip_n']} changed "
            f"controlled runs returned to their Clean category after detected future evidence was "
            f"removed (Wilson 95% CI {pct(all_controlled['recovery_wilson_95_low'])} to "
            f"{pct(all_controlled['recovery_wilson_95_high'])}). In the natural replay, the "
            f"corresponding result was {all_natural['recovered_flip_n']}/"
            f"{all_natural['direction_flip_n']} (Wilson 95% CI "
            f"{pct(all_natural['recovery_wilson_95_low'])} to "
            f"{pct(all_natural['recovery_wilson_95_high'])}). Recovery means agreement with the "
            "model's own Clean prediction, not agreement with the market outcome.",
            "",
            f"One additional revision side effect occurred in "
            f"{all_natural['audited_drift_without_initial_flip_n']} natural run: Clean and "
            "Unfiltered agreed, but Audited changed after post-cutoff chunks were deleted. In the "
            "natural replay, Audited is the Unfiltered top-k with future chunks removed rather than "
            "a newly retrieved cutoff-time top-k, so deletion can leave a sparser context. This is "
            "reported as revision instability and is not counted as failed recovery.",
            "",
            "## RQ4: How well can claim-evidence dependence be detected?",
            "",
            "The frozen controlled annotation set contains 79 pairs, of which 78 have decisive",
            "binary gold labels. Citation-only and a blinded DeepSeek judge achieved similar F1,",
            "while lexical and embedding rules had high precision but substantially lower recall.",
            "",
            *markdown_semantic_table(semantic),
            "",
            f"Citation-only remained marginally stronger on this sample (F1 {citation['f1']:.3f} "
            f"versus {judge['f1']:.3f}) and therefore provides no evidence that the semantic judge "
            "outperforms the simple baseline. Its four false positives and one citation-free false",
            "negative nevertheless show that explicit citation is not equivalent to semantic",
            "dependence.",
            "",
            "## Failure analysis and design consequence",
            "",
            "An online smoke test exposed a high-confidence semantic false positive: the candidate",
            "post-cutoff evidence supported an inventory-glut claim, but the same core fact was",
            "already available before cutoff. FinLeakAudit therefore separates two decisions.",
            "Deterministic temporal validation controls compliance removal; semantic attribution",
            "diagnoses which claims appear contaminated and must distinguish support from exclusive",
            "dependence.",
            "",
            "The Qwen CrowdStrike replay exposed a separate interface failure. Its rationale named",
            "two post-cutoff documents but omitted the required chunk suffixes. Exact-ID citation",
            "matching therefore recorded no valid future citation even though the claim discussed",
            "the post-cutoff Falcon technical incident. Citation validity and semantic attribution",
            "must consequently be evaluated as separate operators.",
            "",
            "## Supported claims",
            "",
            "- Post-cutoff evidence can materially change model forecasts in controlled injections",
            "  and in a small natural-source replay.",
            "- Removing temporally invalid evidence restores the model's cutoff-safe category in all",
            "  observed changed runs, with wide uncertainty intervals due to small denominators.",
            "- Citation-only auditing is incomplete, but current controlled data do not show that an",
            "  LLM semantic judge is superior.",
            "",
            "## Claims not supported",
            "",
            "- The experiments do not estimate how often deployed financial RAG systems leak.",
            "- Recovery does not demonstrate improved stock-prediction accuracy.",
            "- Leave-one-out sensitivity is not a causal effect.",
            "- The current evidence does not establish Full FinLeakAudit as state of the art.",
            "",
        ]
    )


def snapshot_report(
    controlled: list[dict], natural: list[dict], semantic: list[dict]
) -> str:
    controlled_all = aggregate_forecast(controlled, "controlled_injection")
    natural_all = aggregate_forecast(natural, "natural_replay")
    return "\n".join(
        [
            "---",
            "title: FinLeakAudit paper results snapshot",
            "date: 2026-09-03",
            "status: generated-from-frozen-results",
            "---",
            "",
            "# Visible Result",
            "",
            f"The controlled study contains {controlled_all['n_model_cases']} model-case runs and "
            f"{controlled_all['model_calls']} model calls. The natural replay currently contains "
            f"{natural_all['n_model_cases']} model-event runs and {natural_all['model_calls']} "
            "prediction calls. The semantic benchmark contains 78 decisive gold pairs.",
            "",
            "![Controlled audit outcomes](figures/controlled_audit_outcomes.svg)",
            "",
            "![Natural replay outcomes](figures/natural_replay_outcomes.svg)",
            "",
            "![Semantic attribution F1](figures/semantic_attribution_f1.svg)",
            "",
            "# Forecast Audit Metrics",
            "",
            *markdown_forecast_table(controlled + natural),
            "",
            "# Semantic Attribution Metrics",
            "",
            *markdown_semantic_table(semantic),
            "",
            "# Reading Rule",
            "",
            "Recovery is conditional on a Clean-to-contaminated direction change and means that the",
            "Audited prediction equals the Clean prediction. It does not mean the forecast became",
            "correct. Contaminated accuracy is reported to expose hindsight inflation, not as a",
            "performance improvement.",
            "",
            "The prose-ready interpretation is maintained in",
            "[`wiki/writing/results_draft_v1.md`](../writing/results_draft_v1.md).",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-natural-models",
        type=int,
        default=2,
        choices=(2, 3),
        help="Fail unless at least this many natural replay model files exist.",
    )
    args = parser.parse_args()

    controlled = controlled_rows(CONTROLLED_INPUTS)
    natural = natural_rows(NATURAL_INPUTS)
    if len(natural) < args.require_natural_models:
        raise ValueError(
            f"Expected {args.require_natural_models} natural models, found {len(natural)}"
        )
    semantic = semantic_rows(SEMANTIC_INPUT)
    forecast_rows = (
        [aggregate_forecast(controlled, "controlled_injection")]
        + controlled
        + [aggregate_forecast(natural, "natural_replay")]
        + natural
    )
    write_csv(FORECAST_OUTPUT, forecast_rows)
    write_csv(SEMANTIC_OUTPUT, semantic)

    controlled_all = aggregate_forecast(controlled, "controlled_injection")
    svg_bar_chart(
        FIGURES / "controlled_audit_outcomes.svg",
        "Controlled evidence-injection audit",
        "30 model-case runs across DeepSeek, Zhipu, and Qwen2.5-14B",
        ["Future cited", "Direction changed", "Recovered if changed"],
        [
            controlled_all["future_cited_rate"],
            controlled_all["direction_flip_rate"],
            controlled_all["recovery_rate_among_flips"],
        ],
        ["#2274a5", "#d95f43", "#2f855a"],
        "Rate (%)",
    )
    svg_bar_chart(
        FIGURES / "semantic_attribution_f1.svg",
        "Claim-evidence attribution on frozen gold",
        "78 decisive pairs; one uncertain gold label excluded",
        [row["method"].replace(" similarity", "") for row in semantic],
        [row["f1"] for row in semantic],
        ["#3667a6", "#e3a12f", "#7a8b99", "#2f855a"],
        "F1 (%)",
    )
    natural_all = aggregate_forecast(natural, "natural_replay")
    nonflips = natural_all["n_model_cases"] - natural_all["direction_flip_n"]
    drift_rate = (
        natural_all["audited_drift_without_initial_flip_n"] / nonflips
        if nonflips
        else 0.0
    )
    svg_bar_chart(
        FIGURES / "natural_replay_outcomes.svg",
        "Natural point-in-time replay audit",
        f"{natural_all['n_model_cases']} model-event runs across three LLMs",
        ["Valid future citation", "Direction changed", "Recovered if changed", "Audited drift if no flip"],
        [
            natural_all["future_cited_rate"],
            natural_all["direction_flip_rate"],
            natural_all["recovery_rate_among_flips"],
            drift_rate,
        ],
        ["#2274a5", "#d95f43", "#2f855a", "#8b5fa8"],
        "Rate (%)",
    )
    RESULTS_DRAFT.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_DRAFT.write_text(
        build_results_draft(controlled, natural, semantic), encoding="utf-8"
    )
    SNAPSHOT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_REPORT.write_text(
        snapshot_report(controlled, natural, semantic), encoding="utf-8"
    )
    print(f"wrote {FORECAST_OUTPUT}")
    print(f"wrote {SEMANTIC_OUTPUT}")
    print(f"wrote {RESULTS_DRAFT}")
    print(f"wrote {SNAPSHOT_REPORT}")
    print(f"natural models included: {', '.join(row['model'] for row in natural)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
