#!/usr/bin/env python3
"""Render the paper's headline results directly from frozen CSV summaries."""

from __future__ import annotations

import csv
import math
import os
import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.transforms import ScaledTranslation


plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]
plt.rcParams["svg.fonttype"] = "none"

mpl.rcParams.update(
    {
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 6.5,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.linewidth": 0.75,
        "xtick.major.width": 0.65,
        "ytick.major.width": 0.65,
        "legend.frameon": False,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    }
)


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_suffix("")
CONTROLLED_CSV = ROOT / "experiments" / "analysis" / "paper_forecast_audit_metrics_2026_09_03.csv"
NATURAL_CSV = ROOT / "experiments" / "analysis" / "natural_pit_10event_three_model_summary_v1.csv"
ATTRIBUTION_CSV = ROOT / "experiments" / "analysis" / "paper_semantic_attribution_metrics_2026_09_03.csv"
SKILL_SCRIPTS = Path(
    os.environ.get(
        "NATURE_FIGURE_SCRIPTS",
        Path.home() / ".codex" / "skills" / "nature-figure" / "scripts",
    )
)
sys.path.insert(0, str(SKILL_SCRIPTS))

from audit_panel_alignment import require_matplotlib_panel_alignment  # noqa: E402


def normalize_svg(path: Path) -> None:
    """Keep generated vector diffs free of backend-added trailing spaces."""
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8")


COLORS = {
    "ink": "#24323D",
    "muted": "#65737E",
    "grid": "#D9E0E4",
    "cited": "#7884B4",
    "flip": "#B64342",
    "controlled": "#0F4D92",
    "sparse": "#767676",
    "backfill": "#2F8F83",
    "citation": "#0F4D92",
    "lexical": "#C7973C",
    "embedding": "#8C98A3",
    "judge": "#2F8F83",
    "identical": "#B4C0E4",
    "novel": "#E4CCD8",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total <= 0:
        raise ValueError("Wilson interval requires a positive denominator")
    p = successes / total
    denominator = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denominator
    margin = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return centre - margin, centre + margin


def add_panel_label(ax, label: str) -> None:
    offset = ScaledTranslation(-12 / 72, 16 / 72, ax.figure.dpi_scale_trans)
    ax.text(
        0,
        1,
        label,
        transform=ax.transAxes + offset,
        fontsize=8,
        fontweight="bold",
        ha="left",
        va="bottom",
        color=COLORS["ink"],
    )


def style_percent_axis(ax, xlabel: str) -> None:
    ax.set_xlim(0, 1.08)
    ax.set_xticks([0, 0.25, 0.50, 0.75, 1.0])
    ax.set_xticklabels(["0", "25", "50", "75", "100"])
    ax.set_xlabel(xlabel)
    ax.grid(axis="x", color=COLORS["grid"], linewidth=0.55, zorder=0)
    ax.tick_params(length=2.5, pad=2)


def main() -> None:
    controlled = next(
        row
        for row in read_rows(CONTROLLED_CSV)
        if row["study"] == "controlled_injection" and row["model"] == "All"
    )
    natural = next(
        row
        for row in read_rows(NATURAL_CSV)
        if row["scope"] == "all" and row["model"] == "all"
    )
    attribution = read_rows(ATTRIBUTION_CSV)

    # Freeze the values used in the manuscript. Any upstream change must be reviewed.
    assert int(controlled["n_model_cases"]) == 30
    assert int(controlled["future_cited_n"]) == 28
    assert int(controlled["direction_flip_n"]) == 12
    assert int(controlled["recovered_flip_n"]) == 12
    assert int(natural["n_model_events"]) == 30
    assert int(natural["future_cited_count"]) == 27
    assert int(natural["initial_flip_count"]) == 13
    assert int(natural["sparse_recovery_count"]) == 11
    assert int(natural["backfill_recovery_count"]) == 13
    assert int(natural["backfill_matches_clean_sequence_count"]) == 24
    assert len(attribution) == 4

    fig, axes = plt.subplots(2, 2, figsize=(7.15, 4.45))
    ax_a, ax_b, ax_c, ax_d = axes.flat
    fig.subplots_adjust(left=0.095, right=0.985, bottom=0.105, top=0.845, wspace=0.35, hspace=0.92)

    # a: observed citation and forecast changes.
    studies = ["Controlled\ninjection", "Natural\nreplay"]
    cited_counts = [int(controlled["future_cited_n"]), int(natural["future_cited_count"])]
    flip_counts = [int(controlled["direction_flip_n"]), int(natural["initial_flip_count"])]
    y = np.array([1, 0], dtype=float)
    cited_rates = np.array(cited_counts) / 30
    flip_rates = np.array(flip_counts) / 30
    for yy, cited, flip, cited_n, flip_n in zip(y, cited_rates, flip_rates, cited_counts, flip_counts):
        ax_a.plot([0, cited], [yy + 0.11, yy + 0.11], color=COLORS["cited"], linewidth=2.8, solid_capstyle="round")
        ax_a.scatter(cited, yy + 0.11, s=32, color=COLORS["cited"], edgecolor="white", linewidth=0.5, zorder=3)
        ax_a.text(cited - 0.020, yy + 0.23, f"{cited_n}/30", va="center", ha="right", fontsize=6.2, color=COLORS["cited"], fontweight="bold")
        ax_a.plot([0, flip], [yy - 0.13, yy - 0.13], color=COLORS["flip"], linewidth=2.8, solid_capstyle="round")
        ax_a.scatter(flip, yy - 0.13, s=32, color=COLORS["flip"], edgecolor="white", linewidth=0.5, zorder=3)
        ax_a.text(flip - 0.020, yy - 0.01, f"{flip_n}/30", va="center", ha="right", fontsize=6.2, color=COLORS["flip"], fontweight="bold")
    ax_a.set_yticks(y)
    ax_a.set_yticklabels(studies)
    style_percent_axis(ax_a, "Model-event runs (%)")
    ax_a.set_ylim(-0.48, 1.43)
    ax_a.set_title("Post-cutoff evidence changes forecasts", loc="left", fontsize=7, fontweight="bold", color=COLORS["ink"], y=1.22, pad=0)
    handles = [
        plt.Line2D([0], [0], color=COLORS["cited"], marker="o", linewidth=2.4, markersize=4, label="Future cited"),
        plt.Line2D([0], [0], color=COLORS["flip"], marker="o", linewidth=2.4, markersize=4, label="Direction changed"),
    ]
    ax_a.legend(handles=handles, loc="lower left", bbox_to_anchor=(0, 1.03), ncol=2, fontsize=5.7, handlelength=1.6, columnspacing=1.0)
    add_panel_label(ax_a, "a")

    # b: conditional revision recovery with Wilson intervals.
    recovery_labels = ["Controlled\nSparse", "Natural\nSparse", "Natural\nBackfilled"]
    recovery_counts = [(12, 12), (11, 13), (13, 13)]
    recovery_colors = [COLORS["controlled"], COLORS["sparse"], COLORS["backfill"]]
    estimates = np.array([k / n for k, n in recovery_counts])
    intervals = np.array([wilson_interval(k, n) for k, n in recovery_counts])
    yy = np.array([2, 1, 0], dtype=float)
    for pos, estimate, (low, high), (k, n), color in zip(yy, estimates, intervals, recovery_counts, recovery_colors):
        ax_b.plot([low, high], [pos, pos], color=color, linewidth=2.1, solid_capstyle="round")
        ax_b.scatter(estimate, pos, s=42, marker="D", color=color, edgecolor="white", linewidth=0.6, zorder=3)
        ax_b.text(0.97, pos + 0.25, f"{k}/{n}", va="center", ha="right", fontsize=6.2, color=color, fontweight="bold")
    ax_b.set_yticks(yy)
    ax_b.set_yticklabels(recovery_labels)
    style_percent_axis(ax_b, "Recovery among initial flips (%)")
    ax_b.set_ylim(-0.55, 2.55)
    ax_b.set_title("Revision recovers the cutoff-safe direction", loc="left", fontsize=7, fontweight="bold", color=COLORS["ink"], y=1.22, pad=0)
    ax_b.text(0.01, 1.035, "Point estimate and Wilson 95% CI", transform=ax_b.transAxes, fontsize=5.7, color=COLORS["muted"], va="bottom")
    add_panel_label(ax_b, "b")

    # c: attribution methods expose different precision-recall trade-offs.
    method_display = {
        "Citation-only": "Citation-only",
        "Lexical overlap": "Lexical overlap",
        "Embedding similarity": "Embedding similarity",
        "DeepSeek LLM judge": "Blinded LLM judge",
    }
    method_colors = {
        "Citation-only": COLORS["citation"],
        "Lexical overlap": COLORS["lexical"],
        "Embedding similarity": COLORS["embedding"],
        "DeepSeek LLM judge": COLORS["judge"],
    }
    yy = np.arange(len(attribution))[::-1]
    for pos, row in zip(yy, attribution):
        precision = float(row["precision"])
        recall = float(row["recall"])
        f1 = float(row["f1"])
        color = method_colors[row["method"]]
        ax_c.plot([min(precision, recall), max(precision, recall)], [pos, pos], color=color, alpha=0.65, linewidth=2.0)
        ax_c.scatter(precision, pos, s=25, facecolor="white", edgecolor=color, linewidth=1.0, zorder=3)
        ax_c.scatter(recall, pos, s=27, marker="s", facecolor=color, edgecolor="white", linewidth=0.4, zorder=3)
        ax_c.scatter(f1, pos, s=38, marker="D", facecolor=color, edgecolor=COLORS["ink"], linewidth=0.45, zorder=4)
        label_positions = {
            "Citation-only": (0.70, "right"),
            "Lexical overlap": (0.58, "left"),
            "Embedding similarity": (0.54, "left"),
            "DeepSeek LLM judge": (0.88, "right"),
        }
        label_x, label_ha = label_positions[row["method"]]
        ax_c.text(label_x, pos + 0.42, f"F1 {f1:.3f}", fontsize=5.8, color=color, fontweight="bold", va="center", ha=label_ha)
    ax_c.set_yticks(yy)
    ax_c.set_yticklabels([method_display[row["method"]] for row in attribution])
    style_percent_axis(ax_c, "Score")
    ax_c.set_xticklabels(["0", ".25", ".50", ".75", "1.0"])
    ax_c.set_ylim(-0.55, len(attribution) - 0.45)
    ax_c.set_title("Attribution methods trade precision for recall", loc="left", fontsize=7, fontweight="bold", color=COLORS["ink"], y=1.22, pad=0)
    metric_handles = [
        plt.Line2D([0], [0], marker="o", markerfacecolor="white", markeredgecolor=COLORS["ink"], color="none", label="Precision", markersize=4),
        plt.Line2D([0], [0], marker="s", markerfacecolor=COLORS["muted"], markeredgecolor="white", color="none", label="Recall", markersize=4),
        plt.Line2D([0], [0], marker="D", markerfacecolor=COLORS["muted"], markeredgecolor=COLORS["ink"], color="none", label="F1", markersize=4),
    ]
    ax_c.legend(handles=metric_handles, loc="lower left", bbox_to_anchor=(0, 1.03), ncol=3, fontsize=5.7, handletextpad=0.3, columnspacing=0.8)
    add_panel_label(ax_c, "c")

    # d: the apparent Backfill advantage is confounded by input reconstruction.
    ax_d.set_axis_off()
    ax_d.set_title("Backfill's perfect match is partly reconstructive", loc="left", fontsize=7, fontweight="bold", color=COLORS["ink"], y=1.22, pad=0)
    identical = int(natural["backfill_matches_clean_sequence_count"])
    total = int(natural["n_model_events"])
    for index in range(total):
        row = index // 10
        col = index % 10
        x = 0.05 + col * 0.071
        y0 = 0.70 - row * 0.135
        face = COLORS["identical"] if index < identical else COLORS["novel"]
        ax_d.add_patch(
            Rectangle((x, y0), 0.050, 0.075, facecolor=face, edgecolor="white", linewidth=0.6, transform=ax_d.transAxes)
        )
    ax_d.text(0.05, 0.89, "30 Backfilled inputs: blue = identical to Clean; pink = different safe sequence", fontsize=5.8, color=COLORS["muted"], transform=ax_d.transAxes)
    ax_d.text(0.05, 0.24, "24/30", fontsize=13, fontweight="bold", color=COLORS["controlled"], transform=ax_d.transAxes)
    ax_d.text(0.30, 0.255, "exactly reconstructed Clean", fontsize=6.2, color=COLORS["ink"], transform=ax_d.transAxes)
    ax_d.text(0.05, 0.13, "Paired exact McNemar p = 0.25", fontsize=7, fontweight="bold", color=COLORS["flip"], transform=ax_d.transAxes)
    ax_d.text(0.05, 0.055, "Diagnostic evidence, not a proven general advantage", fontsize=6.0, color=COLORS["muted"], transform=ax_d.transAxes)
    add_panel_label(ax_d, "d")

    require_matplotlib_panel_alignment(
        fig,
        axes=[ax_a, ax_b, ax_c, ax_d],
        panel_ids={ax_a: "a", ax_b: "b", ax_c: "c", ax_d: "d"},
        json_out=OUT.with_suffix(".alignment.json"),
        overlay_svg=OUT.with_suffix(".alignment.svg"),
        tolerance_pt=1.5,
        gutter_tolerance_pt=1.5,
        require_panel_labels=True,
        strict=True,
    )
    svg_path = OUT.with_suffix(".svg")
    fig.savefig(svg_path, bbox_inches="tight")
    normalize_svg(svg_path)
    fig.savefig(OUT.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(OUT.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
