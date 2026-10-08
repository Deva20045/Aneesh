#!/usr/bin/env python3
"""Generate data/ch04.json (CVS - Cardiac Examination: Palpation & Auscultation, Book p37-47) and update audit/coverage.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ch04_data_a import A  # noqa: E402
from ch04_data_b import B  # noqa: E402

CHAPTER = 4
TITLE = "CVS - Cardiac Examination: Palpation & Auscultation"
PAGE_RANGE = "37-47"

UNITS = [
    ("Palpation: Apex Beat, DR POPE & Hyperdynamic vs Heaving Impulse", "Palpation: Apex Beat, DR POPE & Hyperdynamic vs Heaving",
     "Apex beat = lowermost, outermost definite palpable cardiac impulse; report as '__ ICS, __ cm medial/lateral to MCL' and comment on character in the left lateral position.\n"
     "Isovolumetric contraction rotates the heart counterclockwise (spiral muscle fibres) and LV ejection causes regression; LV vs RV apex gives a palpatory see-saw.\n"
     "DR POPE = Dextrocardia (never say first; check right side if non-locatable), Rib, Pleural effusion, Obesity, Pericardial effusion, Emphysema; normal apex is L 5th ICS, 1/2 in medial to MCL, 1 ICS, ~2.5 cm2, <1/3 systole; contrast Hyperdynamic (volume overload) vs Heaving (pressure overload) vs Tapping (palpable S1)."),
    ("Apex Shift, Abnormal Impulses, Thrills & Parasternal Heave", "Apex Shift, Abnormal Impulses, Thrills & Heave",
     "LV enlargement shifts the apex downwards and laterally; RV enlargement shifts it only laterally.\n"
     "Retracting apex (inward in systole, outward in diastole) = constrictive pericarditis and TR; hypokinetic = MI; double apex = HOCM ('second LV contraction'), severe AS with AR, and LBBB.\n"
     "Thrill = palpable murmur (carotid AS shudder; A: AS/AR; P: PS, ASD/PDA; T: VSD; M: MR/MS); parasternal heave (2nd-5th ICS, midline to mid-MCL) is graded I-III (AIIMS) and caused by RVH or LA enlargement."),
    ("Pulsatile Liver, Epigastric Thumb Sign & Percussion", "Pulsatile Liver, Epigastric Thumb Sign & Percussion",
     "Thumb in epigastrium towards the shoulder: pulsation at the tip = RVH; pulsation at the pulp = aortic aneurysm.\n"
     "Pulsatile liver: right hand on lower border, left fist on right lower ICS, breath held in deep inspiration; use JVP to time systole/diastole — expansile (TR) vs transmitted (aortic/RV), presystolic ('a' wave, TS) vs systolic (TR).\n"
     "Cardiac percussion assesses liver span in suspected hepatomegaly and increased cardiac dullness in pericardial effusion."),
    ("Auscultation: Sequence, Areas, Gallavardin's Phenomenon & Murmur Grading", "Auscultation: Sequence, Areas, Gallavardin & Grading",
     "Dr. Hamide's sequence: M (Apex) -> T (L 5th ICS) -> P (L 2nd ICS) -> AA1 (R 2nd ICS) and AA2 (Erb's point, L 3rd ICS, where the EDM of AR is heard best).\n"
     "At AA1 the ESM of AS radiates to the carotids as a shudder and to the apex where it mimics MR (Gallavardin's phenomenon).\n"
     "Levine and Freeman systolic murmur grading I/VI to VI/VI: thrill begins at Grade IV/VI; Grade VI/VI is audible with the stethoscope lifted off the chest."),
    ("Classical Murmur Descriptions & Heart Sound Intensity Table", "Classical Murmurs & Heart Sound Intensity Table",
     "Classical MS (****): loud S1, normal S2, high-pitched opening snap after S2 (diaphragm), followed by a low-pitched rough rumbling MDM +/- PSA (bell, left lateral position, mid-expiration).\n"
     "Other apical MDMs: LA myxoma, Austin Flint (AR), Carey-Coombs (ARF), ball-valve LA thrombus, and high-flow states (MR, VSD, PDA, high-output, CHB); tricuspid MDMs: TS, high-flow (ASD, TR, TAPVR), RA myxoma.\n"
     "AS and AR murmurs are best heard sitting leaning forward in expiration; Loud S1 (MS, hyperdynamic) vs Soft S1 (MR, calcific MS, TR, acute AR) and Loud/Soft A2 & P2."),
    ("Heart Sounds S1, S2, Split S2 in ASD, S3 & S4", "Heart Sounds S1, S2, Split S2 in ASD, S3 & S4",
     "Loud S1 in MS results from the dP/dt steep crossover slope (Curve A vs B) and wide leaflet closing excursion; other loud S1 causes include holosystolic MVP, LA myxoma, short PR interval and Ebstein's anomaly ('sail sound').\n"
     "Split S1 (M1 20-30 ms before T1) widens in RBBB/Ebstein's; normal inspiratory S2 split is <0.03 s; ASD causes a wide fixed S2 split (increased low-resistance pulmonary hangout interval + reciprocal decrease in L-to-R shunt on inspiration, Perloff).\n"
     "S3 reflects passive diastolic filling (physiological in children/athletes/pregnancy; pathological in MR/TR, high-output, CHD, HOCM, systolic HF with overly compliant dilated LV, HTN); S4 reflects atrial emptying into a stiff ventricle (HTN, CAD, severe AS, HOCM, RCM)."),
    ("Added Sounds, OS vs S3 Table & Innocent Murmurs", "Added Sounds, OS vs S3 Table & Innocent Murmurs",
     "Added sounds: opening snap (early diastole), ejection click (post-S1), midsystolic click, prosthetic mitral (closes at S1, opens at OS timing) and prosthetic aortic (opens at EC timing, closes at S2).\n"
     "Standing widens the S2-OS gap in MS but narrows the A2-P2 gap; in the OS vs S3 table, treating HF makes OS louder whereas S3 is lost.\n"
     "Pericardial knock = abrupt halt to early diastolic filling in constriction; pericardial rub is triphasic; innocent murmurs are <3/6, systolic/continuous (never pure diastolic), without thrill (Still's, venous hum, mammary souffle)."),
    ("Dynamic Auscultation, Systolic Murmur Timing & 10 Named Murmurs", "Dynamic Manoeuvres, Systolic Timing & 10 Named Murmurs",
     "Carvallo's sign: inspiration increases all right-sided murmurs except pulmonic ejection; Valsalva/standing (low preload) increases HOCM and advances MVP click/murmur, whereas handgrip and rapid squatting decrease HOCM and delay MVP click/murmur.\n"
     "Systolic murmurs by timing: Pansystolic (MR, TR, VSD), Early (acute MR, muscular VSD, acute TR), Mid (supravalvular AS, coarctation, AS, sclerosis, HOCM, flow, PS, ASD), Late (MVP, acute MI, TVP).\n"
     "10 Named murmurs (****): Austin Flint, Carey-Coombs, Cole-Cecil, Cruveilhier-Baumgarten, Gibson, Graham Steell, Means-Lerman scratch, Roger's, Seagull and Still's."),
]


def main() -> None:
    rows = A + B
    pages = [r[0] for r in rows]
    assert pages == sorted(pages), "questions must follow book page order"
    assert set(pages) == set(range(37, 48)), "every page of 37-47 must be covered"

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
