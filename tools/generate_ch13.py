#!/usr/bin/env python3
"""Generate data/ch13.json (RS - History, Symptomatology & Breathlessness Tables, Book p75-79) and update audit/coverage.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ch13_data import DATA  # noqa: E402

CHAPTER = 13
TITLE = "RS - History, Symptomatology & Breathlessness Tables"
PAGE_RANGE = "75-79"
EXPECTED_PAGES = {75, 76, 77, 78, 79}

UNITS = [
    ("History Proforma & Chest Pain", "History Proforma & Chest Pain (Book p75)",
     "Proforma: cough with expectoration, haemoptysis, dyspnoea (rule out CVS causes), chest pain, fever/evening rise/weight loss/night sweats, cor pulmonale features, bronchiectasis complications, oedema, past TB?, occupational history**.\n"
     "Unilateral chest pain usually points to RS causes; pleuritic pain increases on inspiration (coughing) — minimal effusion = pleural layers more in contact = more irritation; pleural disease gives dry cough and stabbing pain."),
    ("Dyspnoea & Acute Onset", "Dyspnoea & Acute Onset (Book p75)",
     "MRC grading preferred in RS — advantages: distance is checked, peer comparison, slope vs level ground.\n"
     "Acute onset dyspnoea: pulmonary oedema, pulmonary embolism, acute COPD exacerbation, acute severe asthma, status asthmaticus, one more asthma."),
    ("Cough & Expectoration History", "Cough & Expectoration History (Book p75)",
     "Onset/duration (TB, chronic bronchitis); postural (post nasal drip, bronchiectasis, LHF 'orthopnoea equalii', tracheal mass); nocturnal (PND, asthma, cough-variant asthma, GERD, TPE); colour (mucopurulent-purulent = infection, serous/frothy pink = pulmonary oedema, blood-stained = bronchiectasis/TB/PE/carcinoma).\n"
     "Bronchorrhoea >100 ml/day (tumbler 150–200 ml): bronchiectasis, lung abscess, empyema into a bronchus, necrotising pneumonia; foul smell = abscess/bronchiectasis; frank vs blood-stained."),
    ("Haemoptysis: Types & Severity", "Haemoptysis: Types & Severity (Book p76)",
     "Frank (blood only), spurious (URTI), pseudo (Serratia marcescens), endemic (Paragonimus westermani).\n"
     "Severity: mild <100 ml/day, moderate 100–150 ml, severe up to 200 ml; massive >500 ml/day or >150 ml/hr or 100 ml/day for >3 days."),
    ("Haemoptysis: Causes", "Haemoptysis: Causes (Book p76)",
     "Airway: bronchitis (acute/chronic), bronchogenic carcinoma, bronchiectasis, body (foreign body) — repeated small haemoptysis/blood-streaked sputum highly suggests carcinoma; bronchial bleed more dangerous (systemic-circulation pressure).\n"
     "Alveolar: pneumonia, fibrocavitary TB (Rasmussen aneurysm rupture), lung abscess, pulmonary oedema (pink frothy); interstitial: ILD (rare); vascular: PH, PE, PA fistula; CVS: MS, PE, PH, AV malformation; CVD: Wegener's, Goodpasture, vasculitis; infective: Weil's, fibrocavitary TB, invasive aspergillosis, paragonimiasis."),
    ("Massive Haemoptysis: Causes & Management", "Massive Haemoptysis: Causes & Management (Book p76)",
     "Causes: bronchiectasis, fibrocavitary TB, aspergillosis, paragonimiasis.\n"
     "Management: intubate; volume resuscitation; blood transfusion; bronchoscopy with balloon tamponade / topical epinephrine or vasopressin."),
    ("Recurrent Haemoptysis & Differential Diagnosis", "Recurrent Haemoptysis & Differential Diagnosis (Book p77)",
     "Recurrent causes: bronchiectasis, chronic bronchitis, bronchogenic carcinoma; pseudohemoptysis = upper respiratory/oral bleeding.\n"
     "Haemoptysis vs haematemesis: cough (not nausea/vomiting) with frothing; alkaline vs acidic pH; food particles and melaena with haematemesis. Cause of death: asphyxia from blood in the bronchial tree. Cor pulmonale history: RV failure or protein loss — also amyloidosis."),
    ("Causes of Dry Cough & Special Coughs", "Causes of Dry Cough & Special Coughs (Book p77)",
     "Dry cough: pleural pathologies, ILD, cough-variant asthma, tropical pulmonary eosinophilia, atypical pneumonia, GERD, ACE inhibitors, RLN palsy.\n"
     "Brassy cough (metallic, tracheal compression); bovine cough (non-explosive, RLN palsy); post-tussive syncope: high intrathoracic pressure -> decreased venous return -> decreased cardiac output."),
    ("Past History of TB", "Past History of TB (Book p78)",
     "Category; treatment taken? treatment completed? compliance?\n"
     "Side effects experienced?"),
    ("Breathlessness: MRC Scale & Receptors", "Breathlessness: MRC Scale & Receptors (Book p78)",
     "Modified MRC grades 0–4 verbatim; note: no 'breathlessness at rest'.\n"
     "Advantages vs NYHA: slope vs level ground, peer comparison, distance checked; other classification — Sherwood Jones."),
    ("Breathlessness: Receptors (JSCR) & CVS vs RS", "Breathlessness: JSCR Receptors & CVS vs RS (Book p78)",
     "Dyspnoea receptors (JSCR): J (alveolar capillary junction), stretch (thoracic cage and lungs), chemoreceptors (carotid artery, aorta, medulla), respiratory muscle receptors.\n"
     "CVS breathlessness: associated CVS cardinal symptoms; orthopnoea, PND. RS breathlessness: no associated CVS symptoms; orthopnoea may be present (asthma, COPD) but PND is specific to CVS."),
    ("Box 19.8: Differential Diagnosis of Acute Breathlessness", "Box 19.8: Differential Diagnosis of Acute Breathlessness (Book p79)",
     "Seven conditions x History/Signs/CXR/ABG/ECG: pulmonary oedema, massive PE, acute severe asthma, acute COPD exacerbation, pneumonia, metabolic acidosis, psychogenic (* = valuable discriminatory feature).\n"
     "Key rows: PE — normal CXR with oligemic fields, S1Q3T3/RBBB/T(V1–V4) inversion; asthma — hyperinflation only, up-PaCO2 in extremis, bradycardia in extremis; COPD — flapping tremor/bounding pulses, type II ABG; psychogenic — normal PaO2, down-down-PaCO2, carpopedal spasm."),
]


def main() -> None:
    rows = DATA
    pages = [r[0] for r in rows]
    assert pages == sorted(pages), "questions must follow book page order"
    assert set(pages) == EXPECTED_PAGES, "every page of 75-79 must be covered"

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
