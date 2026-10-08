#!/usr/bin/env python3
"""Generate data/ch05.json (CVS - Approach to Diagnosis & the Cardiac Cycle, Book p48, 73-74) and update audit/coverage.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ch05_data import DATA  # noqa: E402

CHAPTER = 5
TITLE = "CVS - Approach to Diagnosis & the Cardiac Cycle"
PAGE_RANGE = "48, 73-74"
EXPECTED_PAGES = {48, 73, 74}

UNITS = [
    ("Approach to Cardiovascular Diagnosis (7-Point Format)", "Approach to Cardiovascular Diagnosis (7-Point Format)",
     "Complete cardiovascular diagnosis order: 1. Etiology -> 2. Structural -> 3. Complications -> 4. Rhythm -> 5. Functional -> 6. Treatment Status -> 7. Precipitating Factor.\n"
     "Worked model example (A-G): Rheumatic Heart disease (1) / Severe MS with Mild MR (2) / in Congestive Cardiac Failure (3) / with Atrial Fibrillation (4) / in NYHA Class III (5) / not on any treatment (6) / due to Infective Endocarditis (7)."),
    ("The Cardiac Cycle: Atrial & Ventricular Timing (Circular Diagram)", "The Cardiac Cycle: Atrial & Ventricular Timing (0.8 s)",
     "Total cardiac cycle duration is 0.8 sec (8 sectors of 0.1 sec): inner ring = Atrial Systole (0.1 s) + Atrial Diastole (0.7 s); outer ring = Ventricular Systole (0.3 s) + Ventricular Diastole (0.5 s).\n"
     "Ventricular systole (0.3 s): Isometric contraction -> Maximum ejection -> Reduced ejection; Ventricular diastole (0.5 s): Protodiastole -> Isometric relaxation -> Rapid inflow -> Diastasis -> Atrial systole (final 0.1 s)."),
    ("Wiggers Diagram: Pressures, Volumes, Valves, ECG & Heart Sounds", "Wiggers Diagram: Pressures, Volumes, Valves, ECG & Sounds",
     "Seven phases (a-g): a = Atrial systole, b = Isovolumetric contraction, c = Rapid ejection, d = Reduced ejection, e = Isovolumetric relaxation, f = Rapid filling, g = Reduced filling (diastasis).\n"
     "Valve crossovers: MV closes at a->b (S1); AV opens at b->c (~80 mmHg, peaking at 120 mmHg); AV closes at d->e (dicrotic notch, S2); MV opens at e->f (v-wave peak, followed by S3 in rapid filling).\n"
     "LV volume is flat at EDV (~120-130 mL) during Phase b and flat at ESV (~50 mL) during Phase e; P wave precedes Phase a (4th sound), QRS precedes Phase b (1st sound), and T wave occurs in Phase d."),
]


def main() -> None:
    rows = DATA
    pages = [r[0] for r in rows]
    assert pages == sorted(pages), "questions must follow book page order"
    assert set(pages) == EXPECTED_PAGES, "every page of 48, 73-74 must be covered"

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
