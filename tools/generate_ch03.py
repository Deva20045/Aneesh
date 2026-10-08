#!/usr/bin/env python3
"""Generate data/ch03.json (CVS - Cardiac Examination: Inspection & JVP, Book p31-36) and update audit/coverage.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ch03_data_a import A  # noqa: E402
from ch03_data_b import B  # noqa: E402

CHAPTER = 3
TITLE = "CVS - Cardiac Examination: Inspection & JVP"
PAGE_RANGE = "31-36"

UNITS = [
    ("Peripheral Signs of Aortic Regurgitation & Hill's Sign", "Peripheral Signs of AR & Hill's Sign",
     "Peripheral AR signs 2-16: Becker's (retinal), Landolfi's (pupil), Muller's (uvula), De Musset's (head), Corrigan's (dancing carotids/waterhammer), locomotor brachii, Quincke's (nail bed), Rosenbach's (liver), Gerhardt's (spleen), Duroziez's (distal diastolic femoral murmur) and Traube's pistol-shot femorals.\n"
     "Hill's sign (LL SBP >20 mmHg above UL SBP; popliteal/thigh cuff or posterior tibial/supramalleolar cuff): >20 mild, >40 moderate, >60 severe AR.\n"
     "Hill's sign is a sphygmomanometer artefact from summation of reflected and forward waves (Jules Constant), and is falsely low in CHF and severe AS."),
    ("Cardiac Inspection: Neck, Precordium & Pulsations", "Cardiac Inspection: Neck, Precordium & Pulsations",
     "Inspect JVP, trachea and thyroid (if enlarged, look for thyrotoxic palpitations and eye signs), then chest shape: precordial bulge (left nipple displaced laterally/upward) vs pectus excavatum (backward bulge).\n"
     "See-saw movement: RVH pulls the apex in while the precordium moves out in systole; LVH is the reverse. Back pulsations in coarctation = Suzman's sign.\n"
     "Epigastric pulsations: RV origin coincides with the apex beat higher in the epigastrium; abdominal aortic origin occurs after the apex beat lower down."),
    ("JVP: Definition, RAP Conversion, POLICE & IJV vs EJV", "JVP: Definition, RAP Formula, POLICE & IJV vs EJV",
     "JVP = vertical height above the sternal angle (<=4 cm normal, since sternal angle is 5 cm above RA and normal RAP is <7 mmHg / 9 cm H2O; RAP mmHg = [JVP + 5] x 0.736; Harrison notes >4.5 cm at 30 deg).\n"
     "POLICE separates JVP from carotid: non-Palpable, Occludable, Located between SCM heads lateral to carotid, drops on Inspiration, biphasic Contour, drops on Erection.\n"
     "Right IJV is preferred over EJV (two 90-deg turns, fascial compression, sympathetic constriction) and over left IJV (left innominate vein compression in arteriosclerosis)."),
    ("JVP Procedure, Non-pulsatile JVP & ACXVY Waveforms", "JVP Procedure, Non-pulsatile JVP & ACXVY Waves",
     "Check JVP sitting first (if above clavicle), then at 45 deg; on inspiration mean JVP falls by suction while pulsations become more prominent from increased right-heart volume.\n"
     "Non-pulsatile elevated JVP: bilateral = SVC obstruction; unilateral = innominate vein obstruction/thrombosis.\n"
     "ACXVY: a = atrial contraction; c = tricuspid bulging in isovolumetric contraction (+ carotid component); v = venous return; x' (atrial relaxation) and x (systolic downward pull of tricuspid ring); y = atrial emptying."),
    ("Abnormalities of JVP Waves & Descents (A, V, X, Y)", "Abnormalities of A, V, X & Y Waves (PAY TAX)",
     "Prominent a wave = RVH (PAH, PE, PS); giant a wave = TS and marked LVH (Bernheim effect, before S1); cannon a wave (just after S1, RA vs closed TV) = intermittent in 3rd-degree block/VT, regular in junctional tachycardia, absent in SVT with aberrancy.\n"
     "Equal a and v waves occur in RV failure and ASD ('left atrialization' of JVP because 4 pulmonary veins lower LA compliance).\n"
     "PAY TAX: Constrictive Pericarditis gives a prominent Y descent; Cardiac Tamponade gives a prominent X descent (and blunted y descent); TR blunts the x descent and TS blunts the y descent."),
    ("Constrictive Pericarditis, Abdominojugular Reflux & Kussmaul's Sign", "Constrictive Pericarditis, Abdominojugular Reflux & Kussmaul's Sign",
     "In constrictive pericarditis the adherent pericardium causes rapid early RV relaxation followed by sudden recoil — producing a rapid y descent and the catheterisation 'dip and square root' sign.\n"
     "Abdominojugular reflux (periumbilical pressure >=15 s; positive if JVP rises >3 cm throughout) unmasks subclinical RV failure and confirms symptomatic LV failure.\n"
     "Kussmaul's sign (paradoxical inspiratory JVP rise vs normal 3 mmHg fall): say RVMI first, then RV failure, TS, cor pulmonale, constrictive pericarditis and RCM — never tamponade (where septal bowing into the LV accommodates venous return and causes pulsus paradoxus instead)."),
]


def main() -> None:
    rows = A + B
    pages = [r[0] for r in rows]
    assert pages == sorted(pages), "questions must follow book page order"
    assert set(pages) == set(range(31, 37)), "every page of 31-36 must be covered"

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
