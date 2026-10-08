#!/usr/bin/env python3
"""Generate data/ch06.json (Mitral Stenosis, Book p49-55) and update audit/coverage.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ch06_data_a import A  # noqa: E402
from ch06_data_b import B  # noqa: E402

CHAPTER = 6
TITLE = "Mitral Stenosis"
PAGE_RANGE = "49-55"

UNITS = [
    ("Mitral Stenosis: Causes, Anatomy, Congenital Types & Variants", "MS: Causes, Anatomy, Congenital Types & Variants",
     "Harrison Table 263-1: RHD (~40% pure/predominant MS, fish-mouth valve), congenital, MAC, SLE, RA, methysergide, carcinoid, Lutembacher's, Hurler-Scheie/Fabry/Whipple, and LA outflow mimics (cor triatriatum, LA myxoma, pulmonary vein obstruction).\n"
     "Mitral anatomy: 1 anterior leaflet, 3-lobed posterior leaflet, anteromedial & posterolateral commissures, chordae tendineae, lateral & medial papillary muscles; Congenital MS = supravalvular (fibrous ring), valvular, subvalvular (parachute = 1 papillary muscle; hammock = large/numerous papillary muscles).\n"
     "Variants: Lutembacher (MS + ASD), Damped/Silent MS (RV forms apex in severe PAH so MDM disappears at apex), and Juvenile MS (<20 yr, rheumatic, severe MS & PAH, less AF, needs immediate surgery if symptomatic); gradual LA pressure rise -> protective PAH, sudden rise (AF) -> pulmonary oedema."),
    ("Etiopathogenesis, Clinical Features & Haemoptysis in MS", "Etiopathogenesis, Clinical Features & Haemoptysis in MS",
     "Up to severe MS, resting CO and EF are normal, but tachycardia abolishes the atrial kick and lowers CO (precipitants: fever, excitement, exertion, anaemia, paroxysmal AF, pregnancy, thyrotoxicosis).\n"
     "PAH arises from passive backward transmission + reactive pulmonary arteriolar constriction ('second stenosis'); presystolic accentuation reflects atrial systole before S1.\n"
     "Latent period ~2 decades; dyspnoea (J receptors, low compliance), palpitations (AF from pulmonary vein stretch), mitral facies, and 5 causes of haemoptysis: pulmonary apoplexy (bronchial vein rupture — #1), winter bronchitis, acute pulmonary oedema, pulmonary infarction, warfarin overdose."),
    ("Clinical Severity, Complications & Pulmonary Hypertension Signs", "Severity, Complications & Pulmonary Hypertension Signs",
     "Severity of MS: shorter S2-OS gap ('less'), longer duration of MDM ('more'), and features of pulmonary hypertension.\n"
     "Complications: AF (thrombus most commonly in LA appendage/auricle), PAH/RVF/cor pulmonale, embolic stroke/limb/mesenteric ischaemia, haemoptysis, Ortner's syndrome (RLN -> hoarseness) & dysphagia; IE is very rare ('don't say it').\n"
     "PAH (normal PAP 15-25/10 mmHg; PAH mean PAP >25 rest / >30 exercise, severe >60 exercise): low-volume pulse, prominent 'a' wave, 2nd ICS pulsation & dullness, diastolic shock (palpable P2), parasternal heave, and 6-event auscultation (S1, pulmonary EC, pulmonary ESM, loud P2 narrow split, Graham Steell, right S3)."),
    ("Opening Snap, Absent PSA, Soft S1 & Differential Diagnoses of MS", "OS, Absent PSA, Soft S1, DDs & ECG in MS",
     "Opening snap (6 meanings): organic MS, pliable non-calcified valve, S2-OS gauges severity, amenable to surgery, significant MS, high LA pressure.\n"
     "Absent PSA = AF, left heart failure, massive LA thrombus; Soft S1 in MS = co-existent MR, MV calcification, digitalis overdose (long PR), acute rheumatic carditis (long PR), AF, and damped MS (RV apex).\n"
     "DDs: ASD (fixed S2 split, LSM ESM, functional TS), LA myxoma (positional murmur, fever, weight loss, anaemia, emboli, high IgG & IL-6), significant MR (no OS/loud P2, soft S1, loud PSM), severe AR (Austin Flint not presystolic, softens with vasodilators); ECG shows AF, P mitrale (bifid P), and RVH (tall R in V1-V2, deep S in V6)."),
    ("Investigations (CXR, Doppler Echo, Wilkins Score) & Medical Management", "CXR, Doppler Echo, Wilkins Score & Medical Management",
     "CXR: straightening of left heart border (earliest, PA + LA appendage), double atrial shadow ('shadow within a shadow'), Kerley B lines (PVP 20-30 mmHg, costophrenic horizontal lines), and Kerley A lines (PVP >30 mmHg, towards hilum).\n"
     "Doppler Echo: normal MVA 4-6 cm2, progressive >1.5 cm2, severe 1-1.5 cm2, very severe/tight/critical <1 cm2, enlarged LA >5.5 cm; Abascal/Wilkins score (mobility, thickness, subvalvular thickening, calcification x 4 pts = 16; <8/16 amenable to BMV).\n"
     "Medical management: Penicillin V 250 mg BD (250 mg QID in ARF; lifelong in established HD), Digoxin 0.25 mg 5 days/wk OD for AF (+ oral Diltiazem/Atenolol if needed), Warfarin INR 2-3 indefinitely (AF or thromboembolism), and diuretics."),
    ("Surgical & Interventional Management: Emergency AF, BMV & Prosthetic Valves", "Emergency AF, Valvotomy, BMV & Prosthetic Valves",
     "Emergency AF: rapid digitalisation 0.25 mg IV bolus, wait 2 h, repeat 0.25 mg up to max 1 mg, then beta-blockers if needed; Closed mitral valvotomy (pliable valve, no MR) uses the TUBBS transventricular dilator.\n"
     "BMV: 5 criteria (significant symptoms, isolated MS, no MR, mobile non-calcified valve, no LA thrombus), 4 complications (emboli, perforation, MR, iatrogenic ASD), and 2 success criteria (50% fall in mean MV gradient + doubling of MVA).\n"
     "Valve replacement (if MR or rigid/calcified valve): Mechanical prostheses (INR 2.5-3.5; caged-ball Starr-Edwards vs preferred tilting-disc/bileaflet St. Jude, Bjork-Shiley, Indian Chitra TTK — less space, less haemolysis, less strut fracture) vs Bioprostheses (porcine/pericardial/cadaveric; less thromboembolism, not useful <65 yr due to rapid deterioration)."),
]


def main() -> None:
    rows = A + B
    pages = [r[0] for r in rows]
    assert pages == sorted(pages), "questions must follow book page order"
    assert set(pages) == set(range(49, 56)), "every page of 49-55 must be covered"

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
