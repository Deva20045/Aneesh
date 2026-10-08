#!/usr/bin/env python3
"""Generate data/ch09.json (Aortic Regurgitation, Book p62-63) and update audit/coverage.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ch09_data import DATA  # noqa: E402

CHAPTER = 9
TITLE = "Aortic Regurgitation"
PAGE_RANGE = "62-63"
EXPECTED_PAGES = {62, 63}

UNITS = [
    ("Harrison's Table 262-1: Major Causes of Aortic Regurgitation", "Harrison's Table 262-1: Major Causes of Aortic Regurgitation (Book p62)",
     "Inserted Harrison's table — valve lesion 'Aortic regurgitation' with two etiology columns: Valvular (congenital bicuspid, endocarditis, rheumatic fever, myxomatous [prolapse], radiation, trauma, syphilis, ankylosing spondylitis).\n"
     "Aortic root disease (aortic dissection, medial degeneration, Marfan syndrome, bicuspid aortic valve, nonsyndromic familial aneurysm, aortitis, hypertension). The table says 'Medial degeneration'; 'Cystic' appears only in the p63 note."),
    ("AR Causes: Valvular, Root, Aortitis", "AR Causes: Valvular, Root, Aortitis (Book p63)",
     "Valvular: congenital bicuspid, rheumatic, endocarditis, myxomatous (prolapse), syphilis (Luetic Aortitis), ankylosing spondylitis, trauma; Root: dissection (displacement of the valves), cystic medial degeneration, Marfan's, bicuspid; plus c. Aortitis.\n"
     "Bicuspid aortic valve is listed under BOTH valvular and root disease; Hypertension, radiation and nonsyndromic familial aneurysm are table-only entries."),
    ("AR Haemodynamics: Acute vs Chronic", "AR Haemodynamics: Acute vs Chronic (Book p63)",
     "Cascade: increased total stroke volume -> increased LVEDV (preload) -> dilation and eccentric hypertrophy -> eventual LV failure.\n"
     "Acute severe AR (e.g. endocarditis): LV cannot compensate rapidly -> pulmonary oedema; chronic severe AR: asymptomatic for up to 10–15 years."),
    ("AR Symptoms", "AR Symptoms (Book p63)",
     "Palpitations can be an early complaint, seen for years before the exertional dyspnoea; angina can occur.\n"
     "Then exertional dyspnoea, PND, orthopnoea."),
    ("AR Signs: Head to Toe", "AR Signs: Head to Toe (Book p63)",
     "The '***Signs' list: peripheral signs (from head to toe); heaving apical impulse displaced down and out ('????'); pulsus bisferiens; diastolic thrill over the aortic area.\n"
     "Systolic thrill over carotids/suprasternal notch need not mean accompanying AS; in severe AR, A2 is usually absent."),
    ("AR Murmur & Auscultatory Discrimination", "AR Murmur & Auscultatory Discrimination (Book p63)",
     "High pitched, blowing, decrescendo diastolic murmur; best heard in the 3rd ICS along the left sternal border, sitting, breath held in expiration.\n"
     "Characteristically early diastolic and loudest at Erb's point (neo aortic area) because of the aorta's orientation; if instead best heard in the aortic area, suspect an aortic aneurysm causing the AR."),
]


def main() -> None:
    rows = DATA
    pages = [r[0] for r in rows]
    assert pages == sorted(pages), "questions must follow book page order"
    assert set(pages) == EXPECTED_PAGES, "every page of 62-63 must be covered"

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
