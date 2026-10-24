"""Manual review decisions (Dr. Atul Tiwari / Claude Code review, Oct 2026).

Each keyword candidate's device name and 510(k)/De Novo summary were read.
These tables record what the review changed. Anything not listed here keeps
its keyword-rule tags. `UNCERTAIN` notes are copied into NOTES.md.
"""

# Ultrasound *systems* (IYN/IYO) are kept only if the summary names a specific
# AI feature relevant to ICU work. Matched against the summary body.
US_SYSTEM_FEATURES = {
    "LV function/EF": r"auto ?ef\b|easy auto ?ef|real-time (?:ejection fraction|ef)\b|auto ejection fraction|"
                      r"automated (?:estimation of )?(?:left ventricular )?ejection fraction|auto lvef|ef quantification",
    "VTI/cardiac output": r"auto ?vti|automatic vti|auto(?:mated)? (?:lvot )?vti|lvot velocity time integral",
    "B-lines/lung US": r"b-?lines? (?:tool|counter|feature|software|ai)|auto b-?line|b-?line count",
}

# Keyword candidates judged NOT relevant to ICU imaging, with reason.
EXCLUDE = {
    **dict.fromkeys(["K253969", "K240791", "K191125"], "cardiac MR/CT scar analysis for EP planning"),
    "K260316": "MR/CT perfusion for oncology",
    "K260322": "3D printing / surgical planning",
    "K252148": "obstetric gestational age",
    "K253532": "SPECT processing",
    **dict.fromkeys(["K254207", "K250337", "K243158"], "aortic sizing for elective procedure planning"),
    **dict.fromkeys(["K251027", "K243672", "K233731", "K213725", "K242781", "K213998"],
                    "cardiac CT/MR coronary or structural analysis"),
    "K241038": "cardiac CT function (not a bedside ICU modality)",
    "K211611": "cardiac MR",
    "K250766": "quantitative lung CT for COPD/valves",
    "K203783": "quantitative lung CT texture (not acute triage)",
    "K242467": "fibrotic lung disease referral",
    **dict.fromkeys(["K252433", "K240406", "K230365", "K250959", "K251368", "K241380",
                     "K251456", "K243684", "K231965", "K213689"], "fetal / obstetric ultrasound"),
    "K250151": "cardiac amyloidosis screening",
    "K201555": "stress echo for coronary disease",
    **dict.fromkeys(["K242624", "K233209", "K233186"], "general post-processing suite; stroke/LVO keyword hit was incidental"),
    "K241984": "TAVR planning",
    "K232045": "liver surgical planning",
    "K223268": "low-field MR brain volumetry (portable MR, not CXR/CT/US)",
    **dict.fromkeys(["K221680", "K201103"], "nuclear medicine processing"),
    **dict.fromkeys(["K212383", "K160088"], "fluoroscopic overlay for endovascular repair"),
    "K170069": "Doppler colour classification, general",
    **dict.fromkeys(["K233977", "K223287"], "liver elastography"),
    **dict.fromkeys(["K200980", "K181574"], "bladder volume"),
    "K223443": "abdominal aortic aneurysm on routine CTA (not an acute finding)",
}

# Devices the keyword screen missed but review added: submission -> tags.
ADD = {
    "K212690": {"modality": "CXR", "task": "measure/quantify", "icu_problem": "tube/line position"},
    "K251934": {"modality": "CXR", "task": "detect/triage", "icu_problem": "other",
                "other_detail": "multi-region CXR CADe (pleura, hardware categories)"},
    "K231001": {"modality": "CXR", "task": "detect/triage", "icu_problem": "other",
                "other_detail": "multi-region CXR CADe (pleura, hardware categories)"},
    "K210666": {"modality": "CXR", "task": "detect/triage", "icu_problem": "other",
                "other_detail": "multi-region CXR CADe (pleura, hardware categories)"},
    "K232501": {"modality": "ultrasound/echo", "task": "measure/quantify; detect/triage",
                "icu_problem": "LV function/EF; B-lines/lung US"},
    "K252235": {"modality": "ultrasound/echo", "task": "measure/quantify", "icu_problem": "LV function/EF",
                "other_detail": "echo in patients with a percutaneous VAD"},
    **dict.fromkeys(["K243862", "K243235", "K243331"],
                    {"modality": "ultrasound/echo", "task": "measure/quantify; image quality",
                     "icu_problem": "LV function/EF"}),
    **dict.fromkeys(["K191171"], {"modality": "ultrasound/echo", "task": "measure/quantify",
                                  "icu_problem": "LV function/EF"}),
    **dict.fromkeys(["K223396", "K221100", "K203256"],
                    {"modality": "CT", "task": "measure/quantify", "icu_problem": "PE",
                     "other_detail": "RV/LV diameter ratio on CTPA"}),
}

# Corrected ICU-problem tags for kept candidates (replace keyword result).
PROBLEM = {
    **dict.fromkeys(["K241582"], "LV function/EF; VTI/cardiac output"),
    **dict.fromkeys(["K242837", "K240942"], "other"),
    **dict.fromkeys(["K243548", "K193271", "K202992"], "other"),
    **dict.fromkeys(["K250248", "K241727", "K232751", "K222277", "K220499", "K213886", "K201020", "K233968"], "PE"),
    "K190072": "ICH; PE",
    "K210237": "PE; other",
    **dict.fromkeys(["K253578"], "pneumothorax; effusion/edema; other"),
    **dict.fromkeys(["K243808", "K230899"], "pneumothorax; effusion/edema"),
    **dict.fromkeys(["K252105", "K250670", "K233676", "K210791", "K241430", "K213275", "K220956",
                     "K234141", "K241222", "K191493", "K173810"], "LV function/EF"),
    **dict.fromkeys(["K251416", "K242807", "K243065", "K223347", "K201992", "K200755", "DEN190040", "K260780"],
                    "LV function/EF"),
    "K243239": "effusion/edema; B-lines/lung US",
    "K222179": "effusion/edema; other",
    "K250831": "pneumothorax; effusion/edema; other",
    "K241620": "effusion/edema; pneumothorax; other",
    "K221330": "tube/line position",
    "K182177": "ICH",
    "K212261": "stroke/LVO",
    "K241719": "ICH",
    **dict.fromkeys(["K251533", "K231094", "K231384", "K243378", "K232083", "K241923"], "other"),
    **dict.fromkeys(["K251406", "K222329", "K240291"], "other"),
    **dict.fromkeys(["K252970", "K252366", "K211803"], "other"),
}

# Corrected modality tags.
MODALITY = {"K243239": "ultrasound/echo"}

# Free-text detail for "other" problems.
OTHER_DETAIL = {
    **dict.fromkeys(["K242837", "K240942"], "cervical spine fracture"),
    **dict.fromkeys(["K243548", "K193271", "K202992"], "rib fractures"),
    **dict.fromkeys(["K251533", "K231094"], "obstructive hydrocephalus"),
    "K231384": "intracranial mass effect",
    **dict.fromkeys(["K243378", "K232083", "K241923"], "midline shift"),
    **dict.fromkeys(["K251406", "K222329", "K240291"], "aortic dissection / acute aortic syndrome"),
    "K210237": "aortic dissection",
    "K253578": "pericardial effusion, large aortic aneurysm",
    "K252970": "multi-finding body CT triage (e.g. free air, obstruction)",
    "K252366": "abdominal CT triage (free air, obstruction, aortic)",
    "K211803": "pneumoperitoneum on CXR",
    "K222179": "pneumoperitoneum on CXR",
    "K250831": "pneumoperitoneum and other CXR findings",
    "K241620": "multi-region CXR CADe",
}

# Corrected task tags (replace keyword result).
TASK = {
    **dict.fromkeys(["K253502", "K211161"], "detect/triage; measure/quantify"),
    **dict.fromkeys(["K252105", "K233676", "K210791", "K234141"], "measure/quantify; report drafting"),
    "K250670": "measure/quantify; report drafting",
    **dict.fromkeys(["K251416", "K242807", "K243065", "K223347", "K201992", "K200755", "DEN190040", "K260780"],
                    "guide acquisition; image quality"),
    **dict.fromkeys(["K260217", "K240953"], "measure/quantify; detect/triage; guide acquisition; image quality"),
    **dict.fromkeys(["K252557", "K223771", "K232808", "K220068"], "measure/quantify"),
}

# Things the reviewer was unsure about (copied into NOTES.md).
UNCERTAIN = {
    "US systems": "Ultrasound systems (IYN/IYO) whose summary does not name an AI EF/VTI/B-line feature were "
                  "excluded (e.g. several EPIQ/Affiniti, ACUSON Sequoia, Kosmos K193518/K212100, Clarius K192107, "
                  "Venue K180599). Some of these probably ship AI features that the summary does not describe.",
    "K243794/K242800": "EPIQ and 5000 Compact summaries list LVOT VTI among measurements; unclear whether "
                       "AI-automated, so not tagged VTI.",
    "K251481": "ACUSON Sequoia mentions cardiac output calculations; AI role unclear; excluded.",
    "Echo-lab suites": "TOMTEC-ARENA (K213544), QLAB (K191647) and Sonix Health (K230209, K240645) quantify "
                       "echo but the summaries do not state AI-automated LVEF clearly; excluded.",
    "Multi-region CXR CADe": "qXR-Detect, DeepTek CXR Analyzer, Chest-CAD and ChestView list 'pleura' and "
                             "'hardware' categories but not named findings; tagged 'other'.",
    "Comprehensive echo AI": "Us2.ai, Ligence Heart, EchoGo Core, EchoConfidence, Libby, AISAP and Ventripoint "
                             "measure LVEF among many parameters; tagged LV function/EF, though they are mainly "
                             "echo-lab tools.",
    "K223443": "Viz AAA excluded (routine AAA); aortic dissection triage tools were kept as 'other'.",
    "Generic radiography": "General X-ray systems and noise-reduction software (e.g. Canon Intelligent NR "
                           "K252503/K212269, Radiography 7300 C) mention intensive care use but have no "
                           "ICU-specific AI output; excluded.",
    "Portable MR": "Hyperfine Swoop portable MR (bedside) and BrainInsight are AI-enabled but outside "
                   "CXR/CT/US; excluded.",
    "K250354": "Viz Subdural+ IFU text was garbled in the PDF; tagged ICH from name and body.",
}
