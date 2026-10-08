#!/usr/bin/env python3
"""Generate data/ch08.json (Aortic Stenosis, Book p58-61) and update audit/coverage.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ch08_data import DATA  # noqa: E402

CHAPTER = 8
TITLE = "Aortic Stenosis"
PAGE_RANGE = "58-61"
EXPECTED_PAGES = {58, 59, 60, 61}

UNITS = [
    ("MR Treatment (top of Book p58)", "MR Treatment — tail of the MR note (top of Book p58)",
     "The MR '7. Mx' section closes at the top of Book p58: Medical = same as MS; vasodilators in severe cases may help in reducing R.\n"
     "Surgical = MVR under open heart surgery, sometimes by mitral valvuloplasty or annuloplasty."),
    ("Anatomic Classification of Aortic Stenosis", "Anatomic Classification of Aortic Stenosis (Book p58)",
     "Aortic stenosis is classified into 1. Supravalvular, 2. Valvular, 3. Subvalvular (a. Hypertrophic subaortic stenosis — HOCM; b. Fixed fibrotic subvalvular stenosis).\n"
     "Only the Valvular level opens the 'Valvular aortic stenosis' subsection on p58; the other two are detailed on p61."),
    ("Valvular AS: Causes", "Valvular AS: Causes (Book p58)",
     "Three causes: rheumatic heart disease (almost always with mitral valve involvement + aortic regurgitation), congenital anomalies (bicuspid or unicuspid aortic valve), degenerative calcific stenosis.\n"
     "Rheumatic AS is therefore never 'isolated' — the mitral valve is involved along with aortic regurgitation."),
    ("Valvular AS: Classification by Valve Area", "Valvular AS: Classification by Valve Area (Book p58)",
     "Normal valve area = 3–4 cm². Severe AS <1 cm²; Moderate AS 1–1.5 cm²; Mild AS >1.5 cm².\n"
     "Severity is graded strictly by valve area on p58, before any haemodynamic discussion."),
    ("Valvular AS: Haemodynamics", "Valvular AS: Haemodynamics (Book p58)",
     "LVOT obstruction -> concentric LVH (pressure overload); normal haemodynamic function for years without decline in CO, then eventual LV systolic dysfunction.\n"
     "The hypertrophied LV has a high oxygen demand, so angina on exertion is common."),
    ("Valvular AS: Symptoms", "Valvular AS: Symptoms (Book p58)",
     "Presentation in the 6th–8th decade once severe (bicuspid disease presents sooner): exertional dyspnoea, angina pectoris (somewhat later), exertional syncope.\n"
     "In isolated severe AS, left heart failure and pulmonary hypertension occur very late."),
    ("Valvular AS: Early Signs — Rhythm, BP, Carotid Pulse", "Valvular AS: Early Signs — Rhythm, BP, Carotid Pulse (Book p58)",
     "Usually sinus rhythm; AF suggests associated mitral valve disease. BP usually normal early; late, stroke volume declines and pulse pressure falls.\n"
     "Pulsus parvus et tardus 'rises slowly to a delayed peak'."),
    ("Harrison's Table 261-1: Major Causes of Aortic Stenosis", "Harrison's Table 261-1: Major Causes of Aortic Stenosis (Book p59)",
     "Inserted Harrison's table — valve lesion 'Aortic stenosis' with four etiologies: Congenital (bicuspid, unicuspid), Degenerative calcific disease, Rheumatic fever, Radiation.\n"
     "Radiation appears only in the table, not in the p58 cause list."),
    ("Valvular AS: Auscultation & JVP Signs", "Valvular AS: Auscultation & JVP Signs (Book p60)",
     "Carotid shudder (thrill, especially left); soft S2 (cuspal calcification, prolonged LV ejection time); accentuated JVP a wave — Bernheim effect; laterally displaced apical impulse; systolic thrill.\n"
     "Ejection click (younger bicuspid patients; inaudible if calcified/rigid); low pitched rough rasping ejection (mid) systolic murmur, aortic area, sitting, breath held in expiration, radiating to carotids; Gallavardin effect (apical transmission confused with MR)."),
    ("Valvular AS: Investigations", "Valvular AS: Investigations (Book p60)",
     "ECG — LVH; Doppler Echo; Chest X Ray; Cardiac catheterisation.\n"
     "Only the ECG entry carries an elaborated finding (LVH); the other three are listed as-is."),
    ("Valvular AS: Treatment", "Valvular AS: Treatment (Book p60)",
     "Medical: severe AS — avoid strenuous physical activity; asymptomatic — ACE inhibitors and beta blockers; serial Echo.\n"
     "Surgical indications: symptomatic severe AS, LV systolic dysfunction, bicuspid aortic valve disease, aneurysmal root/ascending aorta; procedures: Ross (declined use), percutaneous aortic balloon valvuloplasty, TAVR."),
    ("Valvular AS: Determinants of Severity", "Valvular AS: Determinants of Severity (Book p60)",
     "Single second heart sound (LV systole prolongation), pulsus parvus et tardus, and a louder and later peaking murmur.\n"
     "These bedside markers track worsening gradient severity as the obstruction progresses."),
    ("Supravalvular Aortic Stenosis", "Supravalvular Aortic Stenosis (Book p61)",
     "Localised discrete narrowing above the sinuses of Valsalva; murmur loudest at suprasternal notch/first right interspace, radiating more to the RIGHT carotid (arch diagram 'more towards R side').\n"
     "a/w hypercalcaemia and elfin facies (wide set eyes, upturned nose, small chin, patulous lips, deep husky voice); stronger pulse/BP right arm and carotid; almost never with an ejection click."),
    ("HOCM", "HOCM (Book p61)",
     "Disproportionate asymmetric IV septal thickening; systolic bulge draws the anterior mitral leaflet medially -> LVOT obstruction (proximity-dependent).\n"
     "Murmur increases with manoeuvres that decrease LV size (inspiration, tachycardia, amyl nitrite, standing after squatting); bifid pulse; double or triple apical impulse."),
    ("AS vs PS: Comparison Table", "AS vs PS: Comparison Table (Book p61)",
     "Murmur best heard at — AS right 2nd ICS, PS left sternal border; inspiration — AS decreases, PS increases; standing — makes the PS murmur louder on inspiration.\n"
     "Ejection click — AS may be present, PS may be present but disappears in inspiration."),
]


def main() -> None:
    rows = DATA
    pages = [r[0] for r in rows]
    assert pages == sorted(pages), "questions must follow book page order"
    assert set(pages) == EXPECTED_PAGES, "every page of 58-61 must be covered"

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
