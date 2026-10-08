#!/usr/bin/env python3
"""Generate data/ch12.json (Infective Endocarditis & 2023 Duke-ISCVID, Book p69-72) and update audit/coverage.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ch12_data import DATA  # noqa: E402

CHAPTER = 12
TITLE = "Infective Endocarditis & 2023 Duke-ISCVID"
PAGE_RANGE = "69-72"
EXPECTED_PAGES = {69, 70, 71, 72}

UNITS = [
    ("IE Diagnosis: Definite vs Possible", "IE Diagnosis: Definite vs Possible (Book p69)",
     "Definite: pathological criteria, 2 major + 1 minor, 1 major + 2 minor, or 5 minor.\n"
     "Possible: 1 major + 1 minor, or 3 minor."),
    ("Duke Criteria: Major — Blood Cultures", "Duke Criteria: Major — Blood Cultures (Book p69)",
     "Typical organisms from two cultures (Viridans streptococci, Streptococcus bovis, HACEK = Haemophilus, Actinobacillus, Cardiobacterium, Eikenella, Kingella), or community-acquired S. aureus/enterococci without a primary focus.\n"
     "Other organisms from persistently positive cultures (two >12 h apart, or all of three/majority of four, first-last 1 h apart); single Coxiella burnetii culture or serology for Q fever, Bartonella, Chlamydia psittaci."),
    ("Duke Criteria: Major — Endocardial Involvement", "Duke Criteria: Major — Endocardial Involvement (Book p69)",
     "Echocardiogram positive for IE: oscillating intracardiac mass without alternative explanation, abscess, or new partial dehiscence of prosthetic valve.\n"
     "Or NEW valvular regurgitation — worsening/changing a preexisting murmur is not sufficient."),
    ("Duke Criteria: Minor & Pathological", "Duke Criteria: Minor & Pathological (Book p69)",
     "Minors: predisposition (heart condition, injection drug use, previous IE, prosthetic material); fever >38°C; vascular phenomena (arterial emboli, septic pulmonary infarcts, mycotic aneurysm, intracranial haemorrhages, subconjunctival petechiae, Janeway lesions); immunologic (glomerulonephritis, Osler's nodes, Roth's spots, positive rheumatoid factor); microbiological evidence.\n"
     "Pathological: positive microbiology or histology of pathologic tissue at surgery or autopsy (vegetations, valve tissue, embolic fragments, tissue/pus from intracardiac abscesses)."),
    ("IE Prophylaxis — Old Regimens (p70, superseded)", "IE Prophylaxis — Old Regimens (Book p70, superseded)",
     "Oral procedures: can take oral — amoxicillin; cannot take oral — ampicillin; ceftriaxone; allergy row — clindamycin; azithro (oral) / clindamycin; ceftriaxone (IV). RESP: same as oral; abscess/empyema drainage add strep viridans; staph — Vanco.\n"
     "GU/GIT: not recommended (established infx/abx cover — enterococci: penicillin); SSTI: not for routine sx (infected tissue — penicillin; allergic or MRSA — Vance). The 2023 ESC + Duke-ISCVID pages supersede all of this, including prophylaxis."),
    ("2023 Update: What Duke-ISCVID Changed", "2023 Update: What Duke-ISCVID Changed (Book p71)",
     "Definite IE unchanged (2 major / 1 major + 3 minor / 5 minor); possible 1 major + 1 minor or 3 minor. Blood-culture rules relaxed; second organism tier (coagulase-negative staphylococci, Cutibacterium acnes, corynebacteria — typical only with intracardiac prosthetic material).\n"
     "New microbiology (PCR, amplicon/metagenomic sequencing, in-situ hybridisation, Bartonella enzyme immunoassay); cardiac CT + 18F-FDG PET/CT major (no longer prosthetic-only); intraoperative inspection a new major; previous IE + transcatheter valves/CIEDs as new minors."),
    ("2023 Update: Management by Type", "2023 Update: Management by Type (Book p71)",
     "Native community-acquired: ampicillin + (flu)cloxacillin + gentamicin (allergy: vancomycin + gentamicin), 4–6 weeks; streptococcal fully sensitive: penicillin/ceftriaxone 4 weeks (2 weeks with gentamicin).\n"
     "Prosthetic EARLY: vancomycin + gentamicin + rifampicin ≥6 weeks (assume MRSA; rifampicin 3–5 days later); LATE: as native + rifampicin if staph; right-sided/PWID: 2 weeks may suffice for uncomplicated tricuspid MSSA, look for septic pulmonary emboli; CIED: hardware extraction mandatory; culture-negative: HACEK, Coxiella, Bartonella, Brucella, Tropheryma (prior antibiotics = commonest cause)."),
    ("2023 Update: Team, Surgery, Stroke, POET", "2023 Update: Team, Surgery, Stroke, POET (Book p71)",
     "Endocarditis Team and Heart Valve Centre: every case discussed by cardiology, cardiac surgery, microbiology and imaging.\n"
     "Surgery (three H's): heart failure (commonest/most urgent), uncontrolled infection (abscess, false aneurysm, fistula, enlarging vegetation, cultures >7 days, fungal/resistant), embolism prevention (>10 mm with embolus or severe valve disease, or isolated >15 mm). Stroke no longer an automatic bar (ischaemic without haemorrhage: no delay; ICH: defer ~1 month). POET: oral switch non-inferior in stabilised left-sided IE; OPAT not in the first 10 days, not with complications."),
    ("2023 Prophylaxis: The Principle (bottom of Book p71)", "2023 Prophylaxis: The Principle (bottom of Book p71)",
     "The principle since 2007 is unchanged: prophylaxis is confined to high-risk patients undergoing high-risk procedures.\n"
     "Moderate-risk cardiac lesions no longer qualify."),
    ("2023 Prophylaxis: Who, When, What", "2023 Prophylaxis: Who, When, What (Book p72)",
     "Who (high risk only): prosthetic valve/material; previous IE; untreated cyanotic CHD or prosthetic-repair CHD (6 months, or lifelong with residual shunt/regurgitation); NEW 2023 — VAD or heart-transplant recipients with valvulopathy.\n"
     "When: dental only (gingiva/periapical manipulation or oral-mucosa perforation) — NOT respiratory/GI/GU/dermatological/musculoskeletal without established infection. What: amoxicillin or ampicillin 2 g PO/IV single dose 30–60 min before (children 50 mg/kg); allergy — doxycycline 100 mg, clindamycin 600 mg, azithro/clarithro 500 mg; no cephalosporins with penicillin anaphylaxis. Oral hygiene and dental review outweigh prophylaxis; aseptic technique; discourage piercing/tattooing."),
]


def main() -> None:
    rows = DATA
    pages = [r[0] for r in rows]
    assert pages == sorted(pages), "questions must follow book page order"
    assert set(pages) == EXPECTED_PAGES, "every page of 69-72 must be covered"

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
