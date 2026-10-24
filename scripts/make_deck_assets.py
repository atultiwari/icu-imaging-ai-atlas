"""Export deck/atlas_summary.json and deck/icu_ai_by_problem.png (1600x900, white).

Usage: python scripts/make_deck_assets.py data/raw/<fda list>.csv data/icu_imaging_ai_atlas.csv deck/
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

AS_OF = "2026-09-04"  # FDA page "Content current as of"
LATEST_DECISION = "2026-06-29"
NAVY, TEAL, INK, MUTED, GRID = "#0B2545", "#13807A", "#1B1F24", "#5B6470", "#E3E7EC"
CREDIT = "Dr. Atul Tiwari · Vedant Research Labs"
DISCLAIMER = "Teaching and research only — not a clinical device."


def counts(series: pd.Series) -> dict:
    exploded = series.fillna("").str.split("; ").explode().str.strip()
    return exploded[exploded != ""].value_counts().to_dict()


def write_summary(fda: pd.DataFrame, atlas: pd.DataFrame, out: Path) -> dict:
    summary = {
        "source": "US FDA, List of AI-Enabled Medical Devices",
        "source_url": "https://www.fda.gov/medical-devices/artificial-intelligence-enabled-medical-devices/"
                      "list-artificial-intelligence-enabled-medical-devices",
        "list_as_of": AS_OF,
        "latest_decision_date_in_list": LATEST_DECISION,
        "total_fda_ai_devices": int(len(fda)),
        "icu_relevant_tagged": int(len(atlas)),
        "by_modality": counts(atlas["modality"]),
        "by_task": counts(atlas["task"]),
        "by_icu_problem": counts(atlas["icu_problem"]),
        "note": "Task and ICU-problem counts sum to more than the device total because a device can carry "
                "several tags. FDA status only; does not cover CDSCO (India).",
        "credit": CREDIT,
    }
    (out / "atlas_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


def draw_chart(summary: dict, out: Path) -> None:
    data = sorted(summary["by_icu_problem"].items(), key=lambda kv: kv[1])
    labels, values = zip(*data)
    labels = tuple("other acute findings" if label == "other" else label for label in labels)
    fig = plt.figure(figsize=(16, 9), dpi=100, facecolor="white")
    ax = fig.add_axes([0.20, 0.13, 0.74, 0.66])
    colors = [TEAL if label not in ("tube/line position", "VTI/cardiac output") else NAVY for label in labels]
    bars = ax.barh(labels, values, color=colors, height=0.62, edgecolor="white", linewidth=2)
    for bar, v in zip(bars, values):
        ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height() / 2, str(v),
                va="center", ha="left", fontsize=18, color=INK)
    ax.set_xlim(0, max(values) * 1.12)
    ax.tick_params(axis="y", labelsize=19, colors=INK, length=0)
    ax.tick_params(axis="x", labelsize=14, colors=MUTED)
    ax.xaxis.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.set_xlabel("Number of FDA-authorised AI devices (a device can address more than one problem)",
                  fontsize=15, color=MUTED, labelpad=10)
    fig.text(0.04, 0.92, "ICU imaging AI mostly measures LVEF or flags bleeds and strokes; "
             "tube and VTI tools are rare", fontsize=19.5, color=NAVY, weight="bold")
    fig.text(0.04, 0.865, f"{summary['icu_relevant_tagged']} of {summary['total_fda_ai_devices']:,} "
             f"FDA AI-enabled devices tagged ICU-relevant · FDA list as of {AS_OF} · FDA status only, not CDSCO",
             fontsize=16, color=MUTED)
    fig.text(0.04, 0.025, f"Source: US FDA AI-Enabled Medical Devices list; tags by keyword rules + manual "
             f"review of 510(k) summaries.   {CREDIT}", fontsize=12.5, color=MUTED)
    fig.savefig(out / "icu_ai_by_problem.png", dpi=100, facecolor="white")


def main(fda_csv: str, atlas_csv: str, out_dir: str) -> None:
    out = Path(out_dir)
    out.mkdir(exist_ok=True)
    summary = write_summary(pd.read_csv(fda_csv), pd.read_csv(atlas_csv), out)
    draw_chart(summary, out)
    print(json.dumps(summary["by_icu_problem"]))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
