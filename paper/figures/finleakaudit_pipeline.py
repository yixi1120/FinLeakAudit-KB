#!/usr/bin/env python3
"""Render the FinLeakAudit point-in-time audit workflow."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]
plt.rcParams["svg.fonttype"] = "none"

mpl.rcParams.update(
    {
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 7,
        "axes.linewidth": 0.8,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    }
)


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_suffix("")
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
    "line": "#B8C2C8",
    "panel": "#F5F7F8",
    "safe": "#3775BA",
    "safe_light": "#DCE9F6",
    "future": "#B64342",
    "future_light": "#F6D9D6",
    "backfill": "#2F8F83",
    "backfill_light": "#D8EFEB",
    "audit": "#725A9A",
    "audit_light": "#E9E2F2",
}


def rounded_box(ax, x, y, w, h, face, edge=None, radius=0.012, lw=0.8):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.006,rounding_size={radius}",
        linewidth=lw,
        edgecolor=edge or face,
        facecolor=face,
        transform=ax.transAxes,
        clip_on=False,
    )
    ax.add_patch(patch)
    return patch


def arrow(ax, start, end, color=None, lw=1.15):
    patch = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=8,
        linewidth=lw,
        color=color or COLORS["muted"],
        transform=ax.transAxes,
        clip_on=False,
    )
    ax.add_patch(patch)


def evidence_chip(ax, x, y, color, label):
    ax.add_patch(
        Rectangle(
            (x, y),
            0.025,
            0.072,
            linewidth=0.7,
            edgecolor=color,
            facecolor="white",
            transform=ax.transAxes,
        )
    )
    ax.add_patch(
        Rectangle(
            (x, y + 0.052),
            0.025,
            0.020,
            linewidth=0,
            facecolor=color,
            transform=ax.transAxes,
        )
    )
    ax.text(
        x + 0.0125,
        y + 0.028,
        label,
        ha="center",
        va="center",
        fontsize=5.5,
        color=COLORS["ink"],
        transform=ax.transAxes,
    )


def draw_condition(ax, y, title, chips, note):
    rounded_box(ax, 0.275, y, 0.255, 0.125, "white", COLORS["line"])
    ax.text(
        0.292,
        y + 0.086,
        title,
        fontsize=6.8,
        fontweight="bold",
        color=COLORS["ink"],
        transform=ax.transAxes,
    )
    for idx, (color, label) in enumerate(chips):
        evidence_chip(ax, 0.405 + 0.031 * idx, y + 0.030, color, label)
    ax.text(
        0.292,
        y + 0.035,
        note,
        fontsize=5.6,
        color=COLORS["muted"],
        transform=ax.transAxes,
    )


def main() -> None:
    fig, ax = plt.subplots(figsize=(7.15, 2.65))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(
        0.018,
        0.955,
        "Evidence-level point-in-time audit",
        fontsize=9,
        fontweight="bold",
        color=COLORS["ink"],
        transform=ax.transAxes,
    )
    ax.text(
        0.018,
        0.900,
        "Prediction, auditing, and evaluation use deliberately separated views.",
        fontsize=6.3,
        color=COLORS["muted"],
        transform=ax.transAxes,
    )

    # Stage 1: the historical information boundary.
    rounded_box(ax, 0.018, 0.125, 0.225, 0.70, COLORS["panel"], COLORS["line"])
    ax.text(
        0.035,
        0.770,
        "1  Evidence boundary",
        fontsize=7.2,
        fontweight="bold",
        color=COLORS["ink"],
        transform=ax.transAxes,
    )
    ax.plot(
        [0.045, 0.218],
        [0.525, 0.525],
        color=COLORS["line"],
        linewidth=1.2,
        transform=ax.transAxes,
    )
    cutoff_x = 0.155
    ax.plot(
        [cutoff_x, cutoff_x],
        [0.405, 0.700],
        color=COLORS["ink"],
        linewidth=1.0,
        linestyle=(0, (3, 2)),
        transform=ax.transAxes,
    )
    ax.text(
        cutoff_x,
        0.720,
        "cutoff τ",
        ha="center",
        va="bottom",
        fontsize=6.3,
        fontweight="bold",
        color=COLORS["ink"],
        transform=ax.transAxes,
    )
    for x, label in [(0.055, "e1"), (0.092, "e2"), (0.126, "e3")]:
        evidence_chip(ax, x, 0.540, COLORS["safe"], label)
    evidence_chip(ax, 0.178, 0.540, COLORS["future"], "e4")
    ax.text(
        0.095,
        0.455,
        "available by τ",
        ha="center",
        fontsize=5.9,
        color=COLORS["safe"],
        fontweight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.195,
        0.455,
        "post-cutoff",
        ha="center",
        fontsize=5.9,
        color=COLORS["future"],
        fontweight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.035,
        0.300,
        "Availability uses archived timestamps\nand provenance, not market outcomes.",
        fontsize=5.8,
        color=COLORS["muted"],
        linespacing=1.35,
        transform=ax.transAxes,
    )

    arrow(ax, (0.245, 0.480), (0.270, 0.480))

    # Stage 2: paired predictor inputs.
    ax.text(
        0.275,
        0.770,
        "2  Paired predictor inputs",
        fontsize=7.2,
        fontweight="bold",
        color=COLORS["ink"],
        transform=ax.transAxes,
    )
    draw_condition(
        ax,
        0.605,
        "Clean",
        [(COLORS["safe"], "e1"), (COLORS["safe"], "e2"), (COLORS["safe"], "e3")],
        "cutoff-safe",
    )
    draw_condition(
        ax,
        0.450,
        "Unfiltered",
        [(COLORS["safe"], "e1"), (COLORS["safe"], "e2"), (COLORS["future"], "e4")],
        "may contain future",
    )
    draw_condition(
        ax,
        0.295,
        "Sparse",
        [(COLORS["safe"], "e1"), (COLORS["safe"], "e2")],
        "delete future",
    )
    draw_condition(
        ax,
        0.140,
        "Backfilled",
        [(COLORS["safe"], "e1"), (COLORS["safe"], "e2"), (COLORS["backfill"], "e5")],
        "add unused safe",
    )

    arrow(ax, (0.535, 0.480), (0.560, 0.480))

    # Stage 3: audit, revision, and evaluator separation.
    rounded_box(ax, 0.565, 0.125, 0.417, 0.70, "white", COLORS["line"])
    ax.text(
        0.582,
        0.770,
        "3  Audit, revise, evaluate",
        fontsize=7.2,
        fontweight="bold",
        color=COLORS["ink"],
        transform=ax.transAxes,
    )

    rounded_box(ax, 0.585, 0.545, 0.115, 0.135, COLORS["safe_light"], COLORS["safe"])
    ax.text(
        0.6425,
        0.627,
        "Predictor",
        ha="center",
        fontsize=6.8,
        fontweight="bold",
        color=COLORS["safe"],
        transform=ax.transAxes,
    )
    ax.text(
        0.6425,
        0.575,
        "text + IDs\nforecast + claims",
        ha="center",
        va="center",
        fontsize=5.4,
        color=COLORS["ink"],
        transform=ax.transAxes,
    )

    rounded_box(ax, 0.735, 0.505, 0.105, 0.215, COLORS["audit_light"], COLORS["audit"])
    ax.text(
        0.7875,
        0.668,
        "Auditor",
        ha="center",
        fontsize=6.8,
        fontweight="bold",
        color=COLORS["audit"],
        transform=ax.transAxes,
    )
    for index, label in enumerate(["availability", "attribution", "ablation"]):
        y = 0.615 - index * 0.050
        ax.text(
            0.7875,
            y,
            label,
            ha="center",
            fontsize=5.5,
            color=COLORS["ink"],
            transform=ax.transAxes,
        )

    rounded_box(ax, 0.875, 0.545, 0.085, 0.135, COLORS["backfill_light"], COLORS["backfill"])
    ax.text(
        0.9175,
        0.627,
        "Revision",
        ha="center",
        fontsize=6.8,
        fontweight="bold",
        color=COLORS["backfill"],
        transform=ax.transAxes,
    )
    ax.text(
        0.9175,
        0.575,
        "rerun after\nremoval/backfill",
        ha="center",
        va="center",
        fontsize=5.4,
        color=COLORS["ink"],
        transform=ax.transAxes,
    )
    arrow(ax, (0.704, 0.612), (0.731, 0.612), COLORS["muted"])
    arrow(ax, (0.844, 0.612), (0.871, 0.612), COLORS["muted"])

    rounded_box(ax, 0.585, 0.230, 0.375, 0.175, COLORS["panel"], COLORS["line"])
    ax.text(
        0.602,
        0.350,
        "Evaluator-only view",
        fontsize=6.8,
        fontweight="bold",
        color=COLORS["ink"],
        transform=ax.transAxes,
    )
    ax.text(
        0.602,
        0.292,
        "Clean agreement  •  flip recovery  •  revision drift  •  attribution F1",
        fontsize=5.7,
        color=COLORS["muted"],
        transform=ax.transAxes,
    )
    ax.text(
        0.602,
        0.250,
        "Outcome labels never trigger evidence removal.",
        fontsize=5.5,
        color=COLORS["future"],
        fontweight="bold",
        transform=ax.transAxes,
    )
    arrow(ax, (0.9175, 0.540), (0.9175, 0.412), COLORS["muted"])

    fig.subplots_adjust(left=0.01, right=0.99, bottom=0.03, top=0.98)
    require_matplotlib_panel_alignment(
        fig,
        json_out=OUT.with_suffix(".alignment.json"),
        overlay_svg=OUT.with_suffix(".alignment.svg"),
        require_panel_labels=False,
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
