#!/usr/bin/env python3
"""Generate data/ch07.json (Mitral Regurgitation, Book p56-57) and update audit/coverage.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ch07_data import DATA  # noqa: E402

CHAPTER = 7
TITLE = "Mitral Regurgitation"
PAGE_RANGE = "56-57"
EXPECTED_PAGES = {56, 57}

UNITS = [
    ("Harrison's Table 264-1: Major Causes of Mitral Regurgitation", "Harrison's Table 264-1: Major Causes of Mitral Regurgitation (Book p56)",
     "Inserted Harrison's table with two acute rows and a chronic hierarchy: Acute = IE, papillary muscle rupture (post-MI), chordal rupture/leaflet flail (MVP, IE), blunt trauma.\n"
     "Chronic splits into Primary (affecting leaflets, chordae: myxomatous [MVP, Barlow's, forme fruste], rheumatic fever, healed IE, congenital [cleft, AV canal], radiation) and Secondary (leaflets/chordae 'innocent bystanders': ischemic CM, dilated CM, HOCM with SAM, AF with LA enlargement and annular dilation), plus Mitral annular calcification with its 'mixed' footnote.\n"
     "The abbreviation key defines AF, AV, HOCM, IE, LA, LV, MI, MVP and SAM."),
    ("MR Causes: Acute vs Chronic", "MR Causes: Acute vs Chronic (Book p57)",
     "Acute MR: Endocarditis, Post-MI papillary muscle rupture (posteromedial), chordal rupture/leaflet flail due to MVP and IE, trauma.\n"
     "Chronic MR: MVP, rheumatic fever, healed endocarditis, mitral annular calcification, congenital cleft, HOCM with SAM, dilated cardiomyopathy."),
    ("MR Haemodynamics: Chronic vs Acute", "MR Haemodynamics: Chronic vs Acute (Book p57)",
     "Chronic MR: gradual LA dilation with little pressure rise (very few symptoms), slow LV dilation, gradual LA and LV pressure rise from chronic volume overload; increased LV volume is often accompanied by reduced cardiac output (verify this).\n"
     "Acute MR: rapid rise in LA pressure because of normal LA compliance, with marked symptomatic deterioration."),
    ("MR Symptoms", "MR Symptoms (Book p57)",
     "Dyspnoea (early, along with palpitations); Fatigue from decreased cardiac output; Palpitations from A fib and increased stroke volume.\n"
     "Right heart failure appears in late stages."),
    ("MR Signs", "MR Signs (Book p57)",
     "Six entries in order: A fib; cardiomegaly with a displaced hyperdynamic apex; apical PSM ± thrill; soft S1, S3; signs of pulmonary venous congestion (crepts, oedema, effusions).\n"
     "Signs of pulmonary hypertension and right heart failure complete the list."),
    ("MR Investigations", "MR Investigations (Book p57)",
     "ECG: left atrial hypertrophy, left ventricular hypertrophy / A fib. CXR: inverted moustache; enlarged LA, LV, pulmonary venous congestion, pulmonary oedema if acute.\n"
     "Echo: dilated LA, LV; Doppler; cardiac catheterisation."),
    ("TR vs MR: Differentiating Features", "TR vs MR: Differentiating Features (Book p57)",
     "TR has: murmur best heard in the tricuspid area, positive Carvallo's, hepatic pulsation, response to abdominojugular reflux (Vitam sign), giant V waves with deep Y descents (Lancisi sign), earlobe pulsation.\n"
     "Acute MR produces an early systolic murmur because the undilated LA cannot buffer the regurgitant volume, so LV and LA pressures equalise in early systole itself."),
]


def main() -> None:
    rows = DATA
    pages = [r[0] for r in rows]
    assert pages == sorted(pages), "questions must follow book page order"
    assert set(pages) == EXPECTED_PAGES, "every page of 56-57 must be covered"

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
