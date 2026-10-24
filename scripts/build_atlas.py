"""Build the ICU imaging AI atlas from the keyword screen + manual review.

Usage:
    python scripts/build_atlas.py data/raw/<fda list>.csv data/derived/candidates_keyword_screen.csv \
        data/derived/fda_ifu_excerpts.csv <body.csv> data/icu_imaging_ai_atlas.csv
"""
import re
import sys

import pandas as pd

import review_decisions as rd

TRIAGE_CODES = {"QAS", "QFM", "QBS", "MYN"}
US_SYSTEM_CODES = {"IYN", "IYO"}
US_CODES = US_SYSTEM_CODES | {"QJU"}
SPURIOUS_OTHER = {"cardiac view/quality", "IVC assessment"}
ACCESSDATA = "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID={}"
DENOVO = "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/denovo.cfm?ID={}"


def split(tags: str) -> list[str]:
    return [t.strip() for t in str(tags).split(";") if t.strip() and t.strip() != "nan"]


def join(tags: list[str]) -> str:
    return "; ".join(dict.fromkeys(tags))


def default_task(row: pd.Series) -> str:
    code = row["Primary Product Code"]
    if code in TRIAGE_CODES:
        return "detect/triage"
    if code == "QJU":
        return "guide acquisition"
    if code == "POK":
        return "detect/triage; measure/quantify"
    if code in US_SYSTEM_CODES:
        return "measure/quantify"
    kw = [t for t in split(row["kw_task"]) if t != "image quality"]
    return join(kw) or "measure/quantify"


def us_system_problems(body: str) -> list[str]:
    return [label for label, pat in rd.US_SYSTEM_FEATURES.items() if re.search(pat, body, re.I)]


def tag_candidate(row: pd.Series, body: str) -> dict | None:
    sub = row["submission"]
    if sub in rd.EXCLUDE:
        return None
    other = [o for o in split(row["kw_other_acute"]) if o not in SPURIOUS_OTHER]
    if sub in rd.PROBLEM:
        problems = split(rd.PROBLEM[sub])
    elif row["Primary Product Code"] in US_SYSTEM_CODES:
        problems = us_system_problems(body)
        if not problems:
            return None
    else:
        problems = split(row["kw_icu_problem"]) + (["other"] if other else [])
    if not problems:
        return None
    if sub in rd.MODALITY:
        modality = rd.MODALITY[sub]
    elif row["Primary Product Code"] in US_CODES:
        modality = "ultrasound/echo"
    else:
        modality = split(row["kw_modality"])[0] if row["kw_modality"] else "other"
    detail = rd.OTHER_DETAIL.get(sub, join(other) if "other" in problems else "")
    return {
        "modality": modality,
        "task": rd.TASK.get(sub, default_task(row)),
        "icu_problem": join(problems),
        "other_detail": detail,
        "review": "keyword + manual",
    }


def summary_url(sub: str) -> str:
    return DENOVO.format(sub) if sub.startswith("DEN") else ACCESSDATA.format(sub)


def main(fda_csv: str, cand_csv: str, ifu_csv: str, body_csv: str, out_csv: str) -> None:
    fda = pd.read_csv(fda_csv)
    fda["submission"] = fda["Submission Number"].str.split("/").str[0]
    cand = pd.read_csv(cand_csv).fillna("")
    body = pd.read_csv(body_csv).fillna("").set_index("submission")["body_text"]
    ifu = pd.read_csv(ifu_csv).fillna("").set_index("submission")["ifu_excerpt"]

    rows = []
    for _, r in cand.iterrows():
        tags = tag_candidate(r, body.get(r["submission"], ""))
        if tags:
            rows.append({"submission": r["submission"], **tags})
    for sub, tags in rd.ADD.items():
        rows.append({"submission": sub, "other_detail": "", **tags, "review": "manual addition"})

    tagged = pd.DataFrame(rows).drop_duplicates("submission")
    atlas = fda.merge(tagged, on="submission", how="inner")
    atlas["ifu_excerpt"] = atlas["submission"].map(ifu).fillna("").str.slice(0, 600)
    atlas["fda_database_url"] = atlas["submission"].map(summary_url)
    atlas = atlas.rename(columns={
        "Date of Final Decision": "decision_date", "Submission Number": "submission_number",
        "Device": "device", "Company": "company", "Panel (Lead)": "panel",
        "Primary Product Code": "product_code"})
    cols = ["decision_date", "submission_number", "device", "company", "panel", "product_code", "modality",
            "task", "icu_problem", "other_detail", "review", "ifu_excerpt", "fda_database_url"]
    atlas = atlas[cols].assign(_d=pd.to_datetime(atlas["decision_date"])).sort_values("_d", ascending=False)
    atlas.drop(columns="_d").to_csv(out_csv, index=False)
    print(f"{len(fda)} FDA AI devices; {len(atlas)} tagged ICU-relevant -> {out_csv}")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        sys.exit(__doc__)
    main(*sys.argv[1:])
