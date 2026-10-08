#!/usr/bin/env python3
"""Generate data/ch11.json (Rheumatic Fever, Book p65-68) and update audit/coverage.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ch11_data import DATA  # noqa: E402

CHAPTER = 11
TITLE = "Rheumatic Fever"
PAGE_RANGE = "65-68"
EXPECTED_PAGES = {65, 66, 67, 68}

UNITS = [
    ("ASD: Symptoms, Signs & DDs (top of Book p65)", "ASD: Symptoms, Signs & DDs — tail of the CHD section (top of Book p65)",
     "Small ASDs are usually asymptomatic; large defects present with tachycardia, right/left heart failure, exertional dyspnoea.\n"
     "Signs: associated PS, wide fixed split of S2 (narrowing with pulmonary hypertension), flow ESM across the pulmonary valve, flow MDM across the mitral valve; DDs: MS with pulmonary HTN, partial anomalous pulmonary venous connections, TAPVC with a large interatrial communication without pulmonary HTN. The page closes with the stubs 'TOF and VSD from peds' and 'Facies in congenital heart disease — Nice to know'."),
    ("RF: Age, Cause, Pathogenesis", "RF: Age, Cause, Pathogenesis (Book p65)",
     "ARF: children aged 5–14, rare >30 years; RHD peaks 25–40 years. Cause: Group A Streptococci.\n"
     "Pathogenesis: molecular mimicry — immune response targeted at streptococcal antigens (M protein and NAG) also recognises human tissues."),
    ("RF: RHD Statistics", "RF: RHD Statistics (Book p65)",
     "Mitral stenosis is seen in 99% of RHD cases; 40% of cases have MS with MR; isolated MS in 25%.\n"
     "38% have multi valve involvement; 35% aortic valve involvement; 6% tricuspid; the pulmonary valve is very rarely involved."),
    ("RF: Clinical Features", "RF: Clinical Features (Book p66)",
     "Latent period 1–5 weeks; the preceding infection is commonly subclinical but confirmable by antibody testing.\n"
     "Most common complaints: polyarthritis (60–75%), carditis (50–60%)."),
    ("RF: Heart Involvement", "RF: Heart Involvement (Book p66)",
     "Up to 60% of ARF patients progress to RHD; endocardium/myocardium/pericardium may be involved. Mitral valve almost always affected (sometimes with aortic); isolated aortic is rare.\n"
     "Early damage -> regurgitation, then (recurrent episodes) thickening, scarring, calcification -> stenosis; characteristic carditis in previously unaffected patients is MR +/- AR; myocarditis may cause first degree AV block and softening of S1."),
    ("RF: Joint Involvement", "RF: Joint Involvement (Book p67)",
     "Hot, swollen, red, tender joints and polyarthritis; typically migrates over a period of hours; large joints, asymmetric.\n"
     "Pain severe and disabling until anti-inflammatory therapy; characteristically sensitive to NSAIDs/Salicylates."),
    ("RF: Chorea", "RF: Chorea (Book p67)",
     "Sydenham's chorea: absence of other manifestations, prolonged latent period, more common in females; ALWAYS associated with carditis.\n"
     "Head (darting tongue movements) and upper limbs; generalised or unilateral; emotional lability/obsessive-compulsive traits; resolves around 6 weeks, up to 6 months."),
    ("RF: Skin", "RF: Skin (Book p67)",
     "Erythema marginatum: pink macules clearing centrally with a serpiginous spreading edge; evanescent (appears/disappears before the examiner's eyes); trunk, sometimes limbs, almost never the face.\n"
     "Subcutaneous nodules — the 3 P's: painless, pea sized, on bony prominences; days to weeks."),
    ("RF: Investigations", "RF: Investigations (Book p67)",
     "ESR, CRP; WBC count; ECG; chest X ray.\n"
     "The two conditional entries: blood culture if febrile, and throat swab before giving antibiotics."),
    ("RF: Treatment", "RF: Treatment (Book p67)",
     "Antibiotics: Phenoxymethylpenicillin 500 mg PO bd / Amox 50 mg/kg daily x 10 days. Salicylates/NSAIDs for arthritis/arthralgia/fever once dx confirmed (no value in carditis/chorea); aspirin 50–60 mg/kg/day up to 80–100 mg/kg/day in 4–5 divided doses; naproxen 10–20 mg/kg/day in two divided doses.\n"
     "Severe carditis: steroids (controversial) — prednisolone 1–2 mg/kg/day, max 3 weeks. Severe chorea: carbamazepine (1–2 weeks response, continue 1–2 weeks after remission); prednisolone 0.5 mg/kg/day with rapid weaning in very severe/refractory; IVIg not recommended except severe refractory chorea."),
    ("RF: Prevention", "RF: Prevention (Book p68)",
     "Primary: timely and complete treatment of group A streptococcal sore throat; penicillin within 9 days of onset prevents almost all ARF.\n"
     "Secondary: Benzathine penicillin G 1.2 MU every 4 weeks — no carditis: 5 years or until 21; carditis without residual valve disease: 10 years or until 21; persistent valvular disease: 20 years or until 40 (each 'whichever is longer')."),
]


def main() -> None:
    rows = DATA
    pages = [r[0] for r in rows]
    assert pages == sorted(pages), "questions must follow book page order"
    assert set(pages) == EXPECTED_PAGES, "every page of 65-68 must be covered"

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
