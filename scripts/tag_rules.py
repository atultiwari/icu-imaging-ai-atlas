"""Keyword rules for tagging FDA AI-enabled devices by ICU imaging relevance.

Rules are a first pass only. Every candidate they surface is then reviewed by
hand against its 510(k)/De Novo summary; overrides live in
data/manual_review.csv and win over these rules.
"""
import re

MODALITY_RULES = {
    "CXR": r"chest x-?ray|chest radiograph|\bcxr\b|chest film|thoracic radiograph|frontal chest|"
           r"(?:portable|mobile|bedside) (?:digital )?(?:x-ray|radiograph)",
    "CT": r"computed tomography|\bct\b|\bcta\b|\bncct\b|\bctpa\b|\bctp\b",
    "ultrasound/echo": r"ultrasound|ultrasonic|sonograph|echocardiogra|\becho\b|doppler|\bpocus\b|"
                       r"transthoracic|\btte\b",
}

ICU_PROBLEM_RULES = {
    "tube/line position": r"endotracheal|\bett\b|enteric tube|nasogastric|feeding tube|central venous|"
                          r"\bcvc\b|\bpicc\b|catheter tip|tube (?:tip|position)|line position|malposition",
    "pneumothorax": r"pneumothora",
    "effusion/edema": r"pleural effusion|pulmonary edema|pulmonary oedema|pericardial effusion|"
                      r"\beffusion\b|consolidation",
    "ICH": r"intracranial h[a]?emorrhage|\bich\b|subdural|epidural h|subarachnoid|"
           r"intracranial bleed|brain bleed|hyperdensit",
    "PE": r"pulmonary embol|\bpe\b(?! ?ct)",
    "stroke/LVO": r"large vessel occlusion|\blvo\b|ischemic stroke|ischaemic stroke|aspects|"
                  r"perfusion|vessel occlusion|core infarct|hypoperfusion",
    "LV function/EF": r"ejection fraction|\blvef\b|\bef\b|left ventricular function|"
                      r"global longitudinal strain|\bgls\b|ventricular volume",
    "VTI/cardiac output": r"velocity time integral|\bvti\b|cardiac output|stroke volume|\blvot\b",
    "B-lines/lung US": r"b-?lines?\b|lung ultrasound|lung sliding|pleural line",
}

# Acute findings that intensivists act on but that fall outside the named
# problem list; they are tagged "other" with a note.
OTHER_ACUTE_RULES = {
    "aortic dissection/aneurysm": r"aortic dissection|aortic aneurysm",
    "free air/pneumoperitoneum": r"pneumoperitoneum|free air|intraperitoneal air",
    "cervical spine fracture": r"cervical spine fracture|c-spine fracture",
    "rib fracture": r"rib fracture",
    "pneumonia/consolidation": r"pneumonia|airspace opacit",
    "obstructive hydrocephalus/mass effect": r"hydrocephalus|midline shift|mass effect",
    "bowel obstruction": r"bowel obstruction",
    "IVC assessment": r"inferior vena cava|\bivc\b",
    "cardiac view/quality": r"cardiac (?:ultrasound )?images?|view classif|apical (?:four|4)",
}

TASK_RULES = {
    "detect/triage": r"triage|notif|prioriti[sz]|worklist|flag|detect|suspect|cad[ex]?\b|computer[- ]aided",
    "measure/quantify": r"measure|quantif|calculat|volume|segment|automated (?:measurement|tracing)",
    "guide acquisition": r"guidance|guide|acquisition of .*images|real-time feedback|assist .* acquir|"
                         r"probe (?:position|placement)",
    "image quality": r"denois|noise reduction|reconstruct|image quality|enhance|artifact|"
                     r"bone suppress|super-?resolution",
    "report drafting": r"draft|preliminary report|report generat|generat\w* (?:a )?report|"
                       r"structured report",
}

# Product codes that are imaging-AI by definition (used to bound the candidate pool).
IMAGING_CODES = {
    "QAS": "Radiological computer-assisted triage and notification",
    "QFM": "Radiological computer-assisted prioritization (lesions)",
    "QJU": "Image acquisition/optimization guided by AI",
    "QIH": "Automated radiological image processing",
    "MYN": "Medical image analyzer (CADe)",
    "QBS": "Radiological CAD for fracture",
    "LLZ": "Radiological image processing system",
    "IYN": "Pulsed Doppler ultrasound imaging system",
    "IYO": "Pulsed echo ultrasound imaging system",
    "JAK": "CT system",
    "KPR": "Stationary X-ray system",
    "IZL": "Mobile X-ray system",
    "OEB": "Lung nodule CAD (CT)",
    "POK": "CADx for lesions suspicious for cancer",
}


def match_any(rules: dict[str, str], text: str) -> list[str]:
    return [label for label, pattern in rules.items() if re.search(pattern, text, re.I)]
