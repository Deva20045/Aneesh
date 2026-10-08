#!/usr/bin/env python3
"""Generate data/ch10.json (Congenital Heart Disease, Book p64) and update audit/coverage.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ch10_data import DATA  # noqa: E402

CHAPTER = 10
TITLE = "Congenital Heart Disease"
PAGE_RANGE = "64"
EXPECTED_PAGES = {64}

UNITS = [
    ("AR Signs i-l (top of Book p64)", "AR Signs i–l — tail of the AR note (top of Book p64)",
     "Right sternal border murmur -> aneurysmal dilation; a mid systolic ejection murmur can also be best in the aortic area, transmitted to the carotids.\n"
     "Two eponymous murmurs are named without elaboration: Austin Flint and Cole Cecil."),
    ("AR Investigations (p64)", "AR Investigations (Book p64)",
     "ECG — LVH; Doppler Echo (color doppler: most sensitive for mild cases); cardiac cath.\n"
     "CXR: cardiomegaly (cor bovinum / bovine heart), aortic root dilation (prominent aortic knuckle), aortic valve calcification (sus for concomitant AS)."),
    ("AR Management (p64)", "AR Management (Book p64)",
     "As in MS (IE or syphilitic aortitis needs Rx); chronic + significant volume overload requires a vasodilator (hydralazine, nifedipine, or ACE inhibitor).\n"
     "Surgery: AVR — ideal time after haemodynamic/echogenic evidence of LVdys but before significant symptoms."),
    ("Congenital HD — ASD: Types", "Congenital HD — ASD: Types (Book p64)",
     "Ostium secundum ASD = 90%; ostium primum ASD = 5%.\n"
     "The primum type is commonly associated with Down syndrome or endocardial cushion defects."),
    ("Congenital HD — ASD: Syndromic Associations", "Congenital HD — ASD: Syndromic Associations (Book p64)",
     "Holt-Oram (triphalangeal fingerised thumb, sometimes abrachia or phocomelia); Patau — trisomy 13 (polydactyly, flexion deformity of fingers, simian crease, cleft lip and palate, microcephaly; ASD, VSD, PDA).\n"
     "Edward — trisomy 18 (prominent occiput, low set malformed ears, rocker bottom feet, micrognathia, clenched fists; ASD, VSD, PDA); Ellis van Creveld (polydactyly, nail dysplasia, dwarfism); Lutembacher = MS + ASD."),
    ("Congenital HD — ASD: Atrial Fibrillation", "Congenital HD — ASD: Atrial Fibrillation (Book p64)",
     "The final point of the ASD section: atrial fibrillation is common in ASD.\n"
     "This arrhythmic point closes the congenital heart disease page."),
]


def main() -> None:
    rows = DATA
    pages = [r[0] for r in rows]
    assert pages == sorted(pages), "questions must follow book page order"
    assert set(pages) == EXPECTED_PAGES, "every page of 64 must be covered"

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
