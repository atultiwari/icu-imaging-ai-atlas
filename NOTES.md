# NOTES — ICU Imaging AI Atlas

## Method (short)
FDA AI-enabled device list (page current as of 4 Sep 2026; downloaded 24 Oct 2026) → 510(k)/De Novo summaries for 1,015 imaging-related devices → keyword rules on device name + Indications for Use → 279 candidates → manual reading of each candidate's name and summary → 202 ICU-relevant devices. All review decisions and reasons are in `scripts/review_decisions.py`.

## Data sources
| Source | URL | Licence |
|---|---|---|
| FDA List of AI-Enabled Medical Devices (CSV) | https://www.fda.gov/medical-devices/artificial-intelligence-enabled-medical-devices/list-artificial-intelligence-enabled-medical-devices (CSV: https://www.fda.gov/media/178541/download) | US Government work, public domain |
| 510(k) / De Novo summaries | https://www.accessdata.fda.gov/cdrh_docs/ | US Government work, public domain |

The FDA site blocks scripted downloads; the CSV was saved through a browser. Summaries for 6 submissions were not found (DEN250057, K082483 and three older PMAs); those devices were judged on name only and none was ICU-relevant.

## Things I was unsure about (not guessed)
- **Ultrasound systems.** Systems (product codes IYN/IYO) whose summary does not name an AI EF, VTI or B-line feature were excluded — e.g. several EPIQ/Affiniti releases, ACUSON Sequoia (K251481 mentions cardiac-output calculations, AI role unclear), Kosmos (K193518, K212100), Clarius scanner (K192107), Venue (K180599). Some of these probably include such features. The atlas likely under-counts ultrasound.
- **LVOT VTI on EPIQ (K243794) and 5000 Compact (K242800).** Listed among measurements; not clear they are AI-automated, so not tagged VTI. Only one device (Canon Aplio i-series V7.0, K241582, whose validation describes LVOT VTI) is tagged VTI/cardiac output.
- **Echo-lab quantification suites.** TOMTEC-ARENA (K213544), QLAB (K191647), Sonix Health (K230209, K240645) quantify echo but their summaries do not clearly state AI-automated LVEF; excluded.
- **Comprehensive echo AI** (Us2.ai, Ligence Heart, EchoGo Core, EchoConfidence, Libby, AISAP, Ventripoint) — tagged LV function/EF because they automate LVEF among many parameters, although they are mainly echo-lab tools.
- **Multi-region CXR CADe** (qXR-Detect, DeepTek CXR Analyzer, Chest-CAD, ChestView) list "pleura" and "hardware" categories rather than named findings; tagged "other" (ChestView also tagged effusion/pneumothorax from its summary).
- **Generic radiography** and noise-reduction software (e.g. Canon Intelligent NR K252503/K212269, Radiography 7300 C) mention ICU use but have no ICU-specific AI output; excluded. So the "image quality" task count (13) is mostly echo quality feedback.
- **Portable MR** (Hyperfine Swoop, BrainInsight) is bedside and AI-enabled but outside CXR/CT/US; excluded. The "other" modality therefore has 0 devices.
- **Viz AAA (K223443)** excluded as a routine-aneurysm tool; acute aortic dissection triage tools kept as "other".
- **Viz Subdural+ (K250354)** — Indications text garbled in the PDF; tagged from name and body.
- Some CT perfusion platforms (Rapid, Viz CTP, icobrain-ctp, Vitrea) are tagged stroke/LVO; they measure perfusion rather than detect LVO.

## Limitations
- FDA status only; **does not cover CDSCO**.
- Intended use ≠ performance. No device was tested.
- Single reviewer; keyword rules can miss devices whose names and summaries avoid the usual terms.
