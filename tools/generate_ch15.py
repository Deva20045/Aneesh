#!/usr/bin/env python3
"""Generate data/ch15.json (RS - Percussion & Auscultation, Book p93-97) and update audit/coverage.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ch15_data import DATA  # noqa: E402

CHAPTER = 15
TITLE = "RS - Inspection, Palpation & Percussion"
PAGE_RANGE = "93-97"
EXPECTED_PAGES = {93, 94, 95, 96, 97}

UNITS = [
    ("Chest Wall Tenderness, Subcutaneous Emphysema & Fremitus", "Chest Wall Tenderness, Subcutaneous Emphysema & Fremitus (Book p93)",
     "Chest wall tenderness — empyema, pleuritis, infiltration of chest wall; then subcutaneous emphysema.\n"
     "Fremitus: vocal (increased in consolidation, decreased in effusion), tactile (crackles, rhonchi), friction (pleural rub)."),
    ("VR/VF & Percussion: Physics", "VR/VF & Percussion: The Physics (Book p93)",
     "Transmission of sound: solid > liquid > air; ability to vibrate: air > liquid > solid.\n"
     "VR/VF measure transmission (from vocal cords); percussion measures vibration. More lung-to-skin distance = more attenuation, vibration unchanged."),
    ("Pathology Table: VR/VF & Percussion", "Pathology Table: VR/VF & Percussion (Book p94)",
     "Consolidation (fluid, increased, DULL) vs hyperinflation (air, reduced, RESONANT) vs pleural effusion (STONY DULL) vs pneumothorax (reduced, Resonant) vs collapse (dull, solid like area).\n"
     "Only consolidation INCREASES VR/VF; all others reduce it."),
    ("Percussion Technique & Areas", "Percussion Technique & Areas (Book p95)",
     "Anterior — hand by the side; posterior — head bent forward, hands on opposite shoulder; lateral — hands over head.\n"
     "Nine areas (supraclavicular -> infra-axillary 4th-7th ICS; suprascapular -> infrascapular); liver dullness normal upper level 5th ICS, pushed down = emphysema."),
    ("Liver Dullness, Traube's & Grocco's Triangle", "Liver Dullness, Traube's Space & Grocco's Triangle (Book p95)",
     "Left sided pathologies — also percuss Traube's space. Grocco's triangle — dullness against the spine at the base of the opposite lung,\n"
     "posterior mediastinal pleura bulging into the contralateral hemithorax — pathognomonic of pleural effusion; figure labels incl. Garland's triangle."),
    ("Grocco's Triangle: The Red Box & Kronig's Isthmus", "Grocco's Triangle Red Box & Kronig's Isthmus (Book p96)",
     "Red box: triangular dullness on the healthy back; base along 12th rib; apex at the upper fluid margin on the diseased side; internally vertebral line; externally apex-to-lateral-base.\n"
     "Kronig's isthmus 5-7 cm (scalenus medius, acromion, clavicle, trapezius); stand behind, lateral to medial, clavicle not touched; up = emphysema, down = TB/apical tumour; tidal percussion."),
    ("Traube's Space", "Traube's Space (Book p96)",
     "6th rib superiorly, left midaxillary line laterally, left costal margin inferiorly; content — fundus of stomach; right side — left lobe of liver; left side — spleen.\n"
     "Obliterated — effusion, splenomegaly, left lobe liver, full stomach, pericardial effusion; shifted up — diaphragmatic paralysis, left lower lobe collapse, left lung fibrosis; Castell's sign area."),
    ("Clavicular Percussion & Hydropneumothorax Signs", "Clavicular Percussion & Hydropneumothorax Signs (Book p97)",
     "Clavicle — stretch the skin, medial 1/3 with middle finger, dull note = secondary TB (apex).\n"
     "Hydropneumothorax: shifting dullness (immediate), straight line dullness, succussion splash (hug and shake), silver coin sounds."),
    ("S shaped Curve of Ellis & the 20-Second Rule", "S Shaped Curve of Ellis & the 20-Second Rule (Book p97)",
     "Ellis curve — moderate pleural effusion; highest in axilla, lowest near spine/sternum; capillary suction between the two pleura layers;\n"
     "radiologically — scattering of X rays by the fluid. No 20-second wait like ascites (same compartment)."),
    ("Vesicular Breath Sounds", "Vesicular Breath Sounds (Book p97)",
     "Low pitched, rustling; I:E = 3:1; no pause between phases.\n"
     "Diminished in — bronchial asthma (silent chest), tumour, small effusion, pleural thickening."),
    ("Causes of Diminished Vesicular Breathing (Box)", "Causes of Diminished Vesicular Breathing — Box (Book p97)",
     "Reduced conduction: obesity/thick chest wall, pleural effusion or thickening, pneumothorax.\n"
     "Reduced airflow: generalised (COPD), localised (collapsed lung due to occluding lung cancer)."),
]


def main() -> None:
    rows = DATA
    pages = [r[0] for r in rows]
    assert pages == sorted(pages), "questions must follow book page order"
    assert set(pages) == EXPECTED_PAGES, "every page of 93-97 must be covered"

    questions = []
    new_ledger = []
    for index, (page, fmt, sec, point, q, opts, ans, exp) in enumerate(rows, 1):
        qid = f"MED-C{CHAPTER}-{index:02d}"
        assert len(opts) == 4 and len(set(opts)) == 4, f"{qid}: options"
        assert 0 <= ans < 4, f"{qid}: answer index"
        assert exp.endswith(f"(Book p{page})"), f"{qid}: page citation"
        if fmt == "fillup":
            assert "____" in q, f"{qid}: fill-up blank"
        questions.append(dict(id=qid, sec=sec, page=page, fmt=fmt, q=q, opts=opts, ans=ans, exp=exp))
        new_ledger.append(dict(chapter=CHAPTER, page=page, point=point, question=qid))

    order = [unit_sec for unit_sec, _, _ in UNITS]
    seen = [q["sec"] for q in questions]
    unique = []
    for s in seen:
        if not unique or unique[-1] != s:
            unique.append(s)
    assert unique == order, f"section order mismatch: {unique} != {order}"

    units = []
    for index, (sec, unit_title, guide) in enumerate(UNITS, 1):
        assert 2 <= len(guide.splitlines()) <= 4, f"unit {index}: guide must be 2-4 lines"
        qs = [q["id"] for q in questions if q["sec"] == sec]
        assert qs, f"unit {index}: no questions"
        units.append(dict(id=f"MED-U{CHAPTER}-{index}", ch=CHAPTER, n=index, title=unit_title, sec=sec, guide=guide, qs=qs))

    flat = [qid for unit in units for qid in unit["qs"]]
    assert flat == [q["id"] for q in questions], "units must tile the question array exactly"

    artifact = dict(chapter=CHAPTER, title=TITLE, pageRange=PAGE_RANGE, questions=questions, units=units)
    (ROOT / "data" / f"ch{CHAPTER:02d}.json").write_text(json.dumps(artifact, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    cov_path = ROOT / "audit" / "coverage.json"
    existing = json.loads(cov_path.read_text(encoding="utf-8")) if cov_path.exists() else []
    merged = [row for row in existing if row["chapter"] != CHAPTER] + new_ledger
    merged.sort(key=lambda r: (r["chapter"], int(r["question"].rsplit("-", 1)[1])))
    cov_path.write_text(json.dumps(merged, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"ch{CHAPTER:02d}: {len(questions)} questions, {len(units)} units, {len(new_ledger)} ledger points")


if __name__ == "__main__":
    main()
