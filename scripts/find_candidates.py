"""First-pass keyword screen: FDA AI list + IFU excerpts -> candidate list for manual review.

Usage:
    python scripts/find_candidates.py data/raw/<fda list>.csv data/derived/fda_ifu_excerpts.csv \
        <body.csv> data/derived/candidates_keyword_screen.csv
"""
import sys

import pandas as pd

from tag_rules import (ICU_PROBLEM_RULES, IMAGING_CODES, MODALITY_RULES, OTHER_ACUTE_RULES,
                       TASK_RULES, match_any)

# Ultrasound *systems* list many generic applications; only count ICU problems
# when the summary body names a specific AI measurement.
US_SYSTEM_CODES = {"IYN", "IYO"}
US_FEATURE_RULES = {k: ICU_PROBLEM_RULES[k] for k in ("LV function/EF", "VTI/cardiac output", "B-lines/lung US")}


def screen(row: pd.Series) -> dict:
    head = f"{row['Device']} {row['ifu_excerpt']}"
    body = row["body_text"]
    code = row["Primary Product Code"]
    modality = match_any(MODALITY_RULES, head) or match_any(MODALITY_RULES, body[:6000])
    problems = match_any(ICU_PROBLEM_RULES, head)
    if code in US_SYSTEM_CODES:
        problems = sorted(set(problems) | set(match_any(US_FEATURE_RULES, body)))
    other = match_any(OTHER_ACUTE_RULES, head)
    tasks = match_any(TASK_RULES, head)
    is_candidate = bool(modality) and (bool(problems) or bool(other) or code == "QJU")
    return {
        "kw_modality": "; ".join(modality),
        "kw_icu_problem": "; ".join(problems),
        "kw_other_acute": "; ".join(other),
        "kw_task": "; ".join(tasks),
        "kw_candidate": is_candidate,
    }


def main(fda_csv: str, ifu_csv: str, body_csv: str, out_csv: str) -> None:
    fda = pd.read_csv(fda_csv)
    fda["submission"] = fda["Submission Number"].str.split("/").str[0]
    ifu = pd.read_csv(ifu_csv).fillna("")
    body = pd.read_csv(body_csv).fillna("")
    df = fda.merge(ifu, on="submission", how="left").merge(body, on="submission", how="left").fillna("")
    pool = df[df["Primary Product Code"].isin(IMAGING_CODES) | (df["Panel (Lead)"] == "Radiology")
              | df["ifu_excerpt"].str.contains("image|imaging", case=False)]
    tags = pool.apply(screen, axis=1, result_type="expand")
    out = pd.concat([pool.drop(columns=["body_text"]), tags], axis=1)
    out = out[out["kw_candidate"]].drop(columns=["kw_candidate"])
    out.to_csv(out_csv, index=False)
    print(f"{len(fda)} devices; pool {len(pool)}; keyword candidates {len(out)} -> {out_csv}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    main(*sys.argv[1:])
