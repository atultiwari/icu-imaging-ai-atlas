"""Extract Indications-for-Use (IFU) text from FDA 510(k)/De Novo summary PDFs.

Usage:
    python scripts/extract_ifu.py <dir-with-pdftotext-output> data/derived/fda_ifu_excerpts.csv <body.csv>

The IFU excerpts (small) are kept in the repo; the full summary body text
(large, used only for keyword rules) goes to <body.csv> outside the repo.

Each summary PDF is first converted with `pdftotext -l 12 K123456.pdf K123456.txt`.
The FDA clearance letter (pages 1-3) is boilerplate, so text before the first
"Sincerely," is dropped. The IFU excerpt is the text following the
"Indications for Use (Describe)" form field, or else the first IFU heading
after the letter.
"""
import csv
import re
import sys
from pathlib import Path

IFU_FORM = re.compile(
    r"Indications\s+for\s+Use\s*\(Describe\)|Please provide your Indications for Use below\.?", re.I
)
IFU_HEAD = re.compile(r"Indications?\s+for\s+Use\s*:?", re.I)
FORM_END = re.compile(
    r"Type of Use|Prescription Use|CONTINUE ON A SEPARATE PAGE|Please select the types? of uses", re.I
)
EXCERPT_CHARS = 1500
BODY_CHARS = 20000


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def body_after_letter(text: str) -> str:
    cut = text.find("Sincerely")
    return text[cut:] if cut != -1 else text[3000:]


def ifu_excerpt(body: str) -> str:
    m = IFU_FORM.search(body)
    if m:
        chunk = body[m.end(): m.end() + EXCERPT_CHARS * 2]
        end = FORM_END.search(chunk)
        return clean(chunk[: end.start()] if end else chunk)[:EXCERPT_CHARS]
    for m in IFU_HEAD.finditer(body):
        chunk = clean(body[m.end(): m.end() + EXCERPT_CHARS])
        if not chunk.startswith("."):  # skip table-of-contents lines
            return chunk
    return ""


def write_csv(path: str, rows: list[dict], fields: list[str]) -> None:
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main(txt_dir: str, out_csv: str, body_csv: str) -> None:
    rows = []
    for path in sorted(Path(txt_dir).glob("*.txt")):
        raw = path.read_text(errors="ignore")
        body = body_after_letter(raw)
        submission = path.stem[:-1] if path.stem.startswith("P") and path.stem.endswith("B") else path.stem
        rows.append({
            "submission": submission,
            "ifu_excerpt": ifu_excerpt(body),
            "body_text": clean(body)[:BODY_CHARS],
        })
    write_csv(out_csv, rows, ["submission", "ifu_excerpt"])
    write_csv(body_csv, rows, ["submission", "body_text"])
    print(f"{len(rows)} summaries -> {out_csv}, {body_csv}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
