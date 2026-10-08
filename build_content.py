#!/usr/bin/env python3
"""Embed the chapter JSON artifacts into the standalone PULSE Aneesh Notes app.

The browser app is intentionally a single offline HTML file. Structured chapter
artifacts in data/chNN.json are the editable source of truth; run this script
whenever a chapter artifact changes. Chapters without an artifact remain on
the roadmap as "Soon" (live: false).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP_PATH = ROOT / "pulse-aneesh.html"
DATA_PATH = ROOT / "data"

# Full roadmap of the annotated notes (Book p3-249), grouped in the book's own
# order. Page numbers are the annotated-document pages defined on Book p1.
# Chapter 1 is verified line by line (see PROGRESS.md); the remaining start
# pages come from the heading scan in audit/PAGE_MAP.md and are confirmed
# chapter by chapter as each one is built.
CHAPTERS = [
    (1, "General Examination", 3),
    (2, "CVS - History & Symptomatology", 16),
    (3, "CVS - Cardiac Examination: Inspection & JVP", 31),
    (4, "CVS - Cardiac Examination: Palpation & Auscultation", 37),
    (5, "CVS - Approach to Diagnosis & the Cardiac Cycle", 48),
    (6, "Mitral Stenosis", 49),
    (7, "Mitral Regurgitation", 56),
    (8, "Aortic Stenosis", 58),
    (9, "Aortic Regurgitation", 62),
    (10, "Congenital Heart Disease", 64),
    (11, "Rheumatic Fever", 65),
    (12, "Infective Endocarditis & 2023 Duke-ISCVID", 69),
    (13, "RS - History, Symptomatology & Breathlessness Tables", 75),
    (14, "RS - General Examination & Chest Wall", 80),
    (15, "RS - Inspection, Palpation & Percussion", 93),
    (16, "RS - Auscultation, Breath Sounds & Crackles", 98),
    (17, "RS - Clubbing, Lung Lymphatics & TB/Pneumonia Protocols", 105),
    (18, "RS - Consolidation, Collapse, Fibrosis & Cavity", 108),
    (19, "RS - Pleural Effusion & Empyema", 110),
    (20, "Abdomen - History, Ascites & General Examination", 112),
    (21, "Abdomen - Venous Flow Patterns & the Liver", 117),
    (22, "Abdomen - The Spleen", 125),
    (23, "Hepatic Encephalopathy - West Haven & Mechanisms", 132),
    (24, "Portal Hypertension & Abdomen Additions", 138),
    (25, "Ascites - Investigations, Refractory Ascites & Complications", 141),
    (26, "Leukaemias - CML & CLL", 144),
    (27, "Polycythemia, Fever with Splenomegaly & Hypersplenism", 149),
    (28, "Portal Hypertension - Pressure, Diagnosis & Treatment", 152),
    (29, "Acute Liver Failure, Child-Pugh & Transplantation", 154),
    (30, "Alcohol & Liver Disease", 156),
    (31, "Chemotherapy Protocols - AML & Myeloma", 160),
    (32, "Approach to an Abdominal Mass", 162),
    (33, "MMSE & Bedside Cognitive Testing", 164),
    (34, "Stroke - History & Risk Factors", 165),
    (35, "Neurocutaneous Markers & Neck Examination", 171),
    (36, "Higher Mental Functions & Cranial Nerves", 174),
    (37, "Motor System Examination & Subtle Hemiparesis", 187),
    (38, "Plantar Response & Primitive Reflexes", 193),
    (39, "Cerebellum, Gait & Sensory Examination", 198),
    (40, "Stroke - Theory, Classification & Management", 204),
    (41, "Stroke - 2026 AHA/ASA Guideline Update", 209),
    (42, "Internal Capsule & Cerebral Arterial Supply", 212),
    (43, "Brainstem Strokes & Viva Points", 217),
    (44, "CNS & Stroke - Niharika's Additions", 222),
    (45, "Paraplegia - Case Proforma & Approach", 224),
    (46, "Conus Medullaris, SACD, GBS & CIDP", 234),
    (47, "Bladder in Cord Lesions & Micturition", 239),
    (48, "Chronic Myelopathies", 242),
    (49, "Paraplegia - Niharika's Additions", 243),
    (50, "Appendix - Harrison's JVP, Arterial Pulse & Blood Pressure", 244),
    (51, "Extras - Vivek Sir's PDFs (pointer page)", 249),
]


def compact(value: object) -> str:
    """Use compact, UTF-8 JSON so the standalone app remains easy to ship."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def between(text: str, start: str, end: str) -> tuple[int, int]:
    first = text.index(start)
    second = text.index(end, first)
    return first, second


def main() -> None:
    # Fail before touching the offline HTML if schema, inventory or app parsing
    # regresses. The visual self-audit is recorded separately in PROGRESS.md.
    from validate_content import validate_all
    validate_all()

    questions: list[dict] = []
    units: list[dict] = []
    live: dict[int, dict] = {}

    for number, title, start_page in CHAPTERS:
        path = DATA_PATH / f"ch{number:02d}.json"
        if not path.exists():
            continue
        chapter = json.loads(path.read_text(encoding="utf-8"))
        if chapter["chapter"] != number:
            raise ValueError(f"{path.name}: chapter number does not match filename")
        if chapter["title"] != title:
            raise ValueError(f"{path.name}: expected title {title!r}, got {chapter['title']!r}")
        first = int(chapter["pageRange"].split("-", 1)[0])
        if first != start_page:
            raise ValueError(f"{path.name}: pageRange starts at {first}, expected {start_page}")
        questions.extend(chapter["questions"])
        units.extend(chapter["units"])
        live[number] = chapter

    html = APP_PATH.read_text(encoding="utf-8")
    q_start, _ = between(html, "const QUESTIONS = ", "\nconst UNITS = ")
    u_start, _ = between(html, "const UNITS = ", "\nconst CHAPTERS = ")
    c_start, c_end = between(html, "const CHAPTERS = ", "\nconst QBYID = ")

    roadmap = []
    for number, title, start_page in CHAPTERS:
        if number in live:
            first = int(live[number]["pageRange"].split("-", 1)[0])
            roadmap.append({"n": number, "t": title, "p": first, "live": True})
        else:
            roadmap.append({"n": number, "t": title, "p": start_page, "live": False})

    html = (
        html[:q_start]
        + "const QUESTIONS = "
        + compact(questions)
        + ";\nconst UNITS = "
        + compact(units)
        + ";\nconst CHAPTERS = "
        + json.dumps(roadmap, ensure_ascii=False, indent=2)
        + ";"
        + html[c_end:]
    )
    APP_PATH.write_text(html, encoding="utf-8")
    print(
        f"Embedded {len(questions)} questions and {len(units)} units across "
        f"{len(live)} live chapter(s) of {len(CHAPTERS)} roadmap chapters in {APP_PATH.name}."
    )


if __name__ == "__main__":
    main()
