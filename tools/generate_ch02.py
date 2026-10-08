#!/usr/bin/env python3
"""Generate data/ch02.json (CVS - History & Symptomatology, Book p16-30) and update audit/coverage.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ch02_data_a import A  # noqa: E402
from ch02_data_b import B  # noqa: E402
from ch02_data_c import C  # noqa: E402

CHAPTER = 2
TITLE = "CVS - History & Symptomatology"
PAGE_RANGE = "16-30"

UNITS = [
    ("Cardinal Symptoms, Dyspnoea & NYHA Grading", "Cardinal Symptoms, Dyspnoea & NYHA Grading",
     "Five cardinal CVS symptoms: breathlessness, chest pain, palpitations, syncope and pedal oedema (Dr. Hamide replaces pedal oedema with cough).\n"
     "Dyspnoea is abnormal awareness of one's own respiration; orthopnoea is more severe than PND and reflects recumbent fluid shift from splanchnic/lower-limb beds.\n"
     "NYHA Class I-IV is graded by both Dr. Hamide (unaccustomed, accustomed, day-to-day, rest) and Dr. Vivekanandan (if walking produces symptoms, consider Class III)."),
    ("Trepopnea, Platypnea & Orthodeoxia", "Trepopnea, Platypnea & Orthodeoxia",
     "Normal daily physical activity benchmark is 1-2 flights of stairs.\n"
     "Trepopnea (dyspnoea in right or left decubitus) is seen in dilated cardiomyopathy.\n"
     "Platypnea (upright dyspnoea) and orthodeoxia (>=5% SpO2 drop upright) occur in LA thrombus, LA myxoma, hepatopulmonary syndrome (NO-mediated basal AV shunts), ASD and V/Q mismatch."),
    ("Chest Pain: Semiological Analysis", "Chest Pain: Site, Onset, Nature, Radiation & Posture",
     "Site: central = angina/ischaemia; retrosternal = oesophageal; epigastric radiating to chest = GI or angina.\n"
     "Onset & nature: builds over minutes = MI/angina; immediate peak = aortic dissection, PE, spontaneous pneumothorax; burning pain can still be MI.\n"
     "Radiation & posture: neck/jaw/arms = MI; interscapular back = dissection; trapezius ridge and relief on sitting upright leaning forward = pericarditis."),
    ("Orthopnoea vs PND (Boloor Table 3C.7)", "Orthopnoea vs PND (Boloor Insert Table)",
     "Boloor Table 3C.7 (p18-19) contrasts PND (sudden dyspnoea 2-2.5 h into sleep during REM from sympathetic surge and transient PCWP spike, with transient hypoxia) and orthopnoea (>400 mL recumbent venous shift with slow sustained PCWP rise and normal SpO2).\n"
     "PND differentials: nightmares, panic attacks, nocturnal hypoglycaemia, OSA.\n"
     "Orthopnoea differentials: COPD, gross obesity, acute asthma, gross ascites."),
    ("Chest Pain: Meals, Causes Table & Angina Variants", "Chest Pain Causes & Angina Variants",
     "Post-meal pain (60-90 min) occurs in pancreatitis, cholecystitis, peptic ulcer and postprandial angina; NTG relieves both angina/MI and oesophageal spasm.\n"
     "Non-ischaemic CVS chest pain includes AS/HOCM (LVH oxygen demand) and AR (diastolic coronary filling lost to regurgitation).\n"
     "Variants: unstable, crescendo (never at rest), nocturnal/decubitus (severe CAD), walk-through (exercise vasodilation), silent MI (30%, elderly/DM), angina equivalents and second-wind angina."),
    ("CCS Angina Grading & Syncope vs Seizure", "CCS Angina Grading & Syncope vs Seizure",
     "CCS stable angina: Grade 1 strenuous exercise only; Grade 2 slight limitation; Grade 3 walking 1-2 blocks or <1 flight of stairs; Grade 4 discomfort with any activity or at rest.\n"
     "Exertional syncope points to fixed-output lesions (AS, HOCM).\n"
     "Vasovagal syncope (<60 s, pale/grey, rare lateral tongue bite, rapid recovery) is separated from seizure (1-2 min tonic-clonic, red/blue, lateral tongue bite, >30 min post-ictal confusion)."),
    ("Syncope Classification: Pathophysiology & Causes", "Syncope: Pathophysiology & Aetiologies",
     "Orthostatic syncope = fall in SBP >20 mmHg or DBP >10 mmHg within 3 min of standing (antihypertensives, diabetic autonomic neuropathy, anaemia).\n"
     "Post-tussive syncope = violent coughing in lung disease raising intrathoracic pressure and reducing venous return.\n"
     "CVS syncope splits into electrical (bradycardia, heart block, VT, SVT) and mechanical (AS, HOCM, PS, TOF, PE, and postural syncope in LA myxoma)."),
    ("Palpitations, Pedal Oedema (Box 6.8) & Cough", "Palpitations, Pedal Oedema (Box 6.8) & Cough",
     "Palpitations (abnormal awareness of one's own heartbeat): exertional in regurgitant lesions, at rest in arrhythmia, followed by post-palpitation diuresis; in AR dyspnoea occurs much later than palpitations, whereas in MR they appear together.\n"
     "Box 6.8 lists unilateral (DVT, infection, trauma, hemiplegia, lymphoedema) and bilateral leg oedema causes including drugs (NSAIDs, nifedipine, amlodipine, fludrocortisone), IVC obstruction, wet beriberi and Milroy's disease.\n"
     "In cough with blood, always ask about melena and association with food."),
    ("Negative, Past, Personal & Drug History", "Negative, Past, Personal & Drug History",
     "Negative history screens RHF, RF, left-sided disease (voice change, dysphagia, oliguria), congenital spells/squatting, PHT (pulmonary apoplexy) and IE (stroke/TIA, haematuria).\n"
     "Past history notes BMV in MS can cause MR; personal history checks IV drug abuse in suspected IE.\n"
     "Drug schedule: digoxin 5 days on / 2 days off; diuretics and nitroglycerin at 8 am and 4 pm (avoiding nocturia and nocturnal hypotension)."),
    ("History Summary & Arterial Pulse: Rate, Rhythm, Volume & Delay", "History Summary & Pulse Rate, Rhythm, Volume & Delay",
     "Warfarin is taken at 4 pm daily and benzathine penicillin every 21 days.\n"
     "Normally femoral precedes radial pulse by a few ms (reversal = radiofemoral delay); in AF, variable diastolic filling causes weak contractions and an apex-pulse deficit.\n"
     "VT (unchanged by vagal manoeuvres, cannon A waves and variable S1 from AV dissociation) is separated from PAT (abrupt termination with Valsalva/carotid massage, neck pounding)."),
    ("Types of Pulse: Normal, Bisferiens, Bifid, Dicrotic, Anacrotic & Corrigan", "Pulse Waveforms: Bisferiens, Bifid, Dicrotic, Anacrotic & Corrigan",
     "Normal pulse has an anacrotic upstroke and dicrotic downstroke separated by the dicrotic notch at S2.\n"
     "Pulsus bisferiens (two equal systolic peaks via Bernoulli effect) occurs in moderate AS + severe AR, HOCM and severe AR; bifid ('spike and dome') is classic for HOCM; dicrotic has its second peak in diastole (LV failure with low CO + high PVR); anacrotic has an upstroke notch (severe AS).\n"
     "Corrigan/Waterhammer pulse is accentuated by raising the arm (gravity empties the radial artery and aligns it with the aorta)."),
    ("Parvus et Tardus, Bigeminy, Pulsus Paradoxus & Pulsus Alternans", "Parvus et Tardus, Bigeminy, Paradoxus & Alternans",
     "Pulsus parvus et tardus (weak low peak + slow wide upstroke) characterises AS; bigeminy pairs every sinus beat with a PVC (irregular rhythm), whereas regular alternating beats are pulsus alternans.\n"
     "Pulsus paradoxus (>10 mmHg inspiratory SBP drop, measured from expiration-only to inspiration+expiration Korotkoff sounds) occurs in tamponade, constrictive pericarditis, asthma/COPD and OSA/obesity; reversed pulsus paradoxus occurs in HOCM.\n"
     "Pulsus alternans (LV dysfunction, sarcoplasmic reticulum Ca2+ alternation) is detected by cuff when >10 mmHg."),
    ("CVS General Examination: PICCLE, Slow vs Fast Oedema, RF, IE & AR Signs", "CVS General Survey: PICCLE, Oedema Kinetics & Peripheral Signs",
     "Check ruddy/suffused conjunctiva for polycythaemia of cyanotic heart disease, tongue/mucosa for central vs peripheral cyanosis, and clubbing (cyanotic HD, IE, LA myxoma).\n"
     "Slow oedema pits >40 s (4 kg Na/water retention; treat with salt restriction); fast oedema pits <40 s (hypoproteinaemia); cardiac dependent oedema is presacral.\n"
     "Check rheumatic nodules/joint swelling, IE stigmata (immunologic = Osler nodes, Roth spots, microscopic haematuria; vascular = Janeway lesions, splinter haemorrhages), and the Lighthouse sign of AR."),
]


def main() -> None:
    rows = A + B + C
    pages = [r[0] for r in rows]
    assert pages == sorted(pages), "questions must follow book page order"
    assert set(pages) == set(range(16, 31)), "every page of 16-30 must be covered"

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
