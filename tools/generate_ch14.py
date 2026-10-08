#!/usr/bin/env python3
"""Generate data/ch14.json (RS - General Examination & Chest Wall, Book p80-92) and update audit/coverage.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ch14_data import DATA  # noqa: E402

CHAPTER = 14
TITLE = "RS - General Examination & Chest Wall"
PAGE_RANGE = "80-92"
EXPECTED_PAGES = set(range(80, 93))

UNITS = [
    ("Chest Pain: Origins & Character Table", "Chest Pain: Origins & Character Table (Book p80)",
     "Origins: parietal pleura, chest wall, mediastinal structures — NOT lung (autonomic innervation only).\n"
     "Table: parietal pleura sharp/stabbing with inspiration (upper 6 ribs localised, lower ribs -> upper abdomen, diaphragmatic -> shoulder tip/neck); chest wall dull/aching, progressive, hinders sleep; mediastinal central/retrosternal."),
    ("Specific TB History Points", "Specific History Points in Suspected TB (Book p80)",
     "Occupation of husband — high risk group for HIV; evening rise of temperature — due to TNFa;\n"
     "contact history of tuberculosis."),
    ("Examination: Pulse, Pallor, Cyanosis, Clubbing", "Examination: Pulse, Pallor, Cyanosis, Clubbing (Book p81)",
     "Pulsus paradoxus >10 mmHg is significant, reduces on treatment. Pallor — recurrent haemoptysis, bronchial ca, TB. Cyanosis — SpO2 <85%.\n"
     "Clubbing in TB: post-TB bronchiectasis, scar carcinoma (adenocarcinoma), empyema, endobronchial TB."),
    ("Lymphadenopathy: Epitrochlear & Scalene", "Lymphadenopathy: Epitrochlear & Scalene Nodes (Book p81)",
     "Epitrochlear nodes are always pathologic — NHL, secondary syphilis, sarcoidosis, forearm/hand infections, tularaemia (rare), but not in TB (Dr. Hamide).\n"
     "Scalene node: index finger between SCM and clavicle; head tilted to the same side; press firmly down towards the first rib."),
    ("Lymphadenopathy: Generalised & Mediastinal; Oedema", "Generalised & Mediastinal Lymphadenopathy; RS Oedema (Book p82)",
     "Generalised — HIV, IM, sarcoidosis. Mediastinal — dull percussion on manubrium sterni, bronchial breathing below T4 spine (d'Espine sign) from subcarinal nodes.\n"
     "RS oedema: cor pulmonale; protein loss in sputum (esp bronchiectasis); amyloidosis of long standing bronchiectasis."),
    ("Respiration: Rate, Distress & Muscles", "Respiration: Rate, Distress Signs & Muscles (Book p82)",
     "Normal rate 12-18/min; women thoraco-abdominal, men abdomino thoracic. Distress: alar nasii, pursed lip (PEEP), tracheal indrawing, accessory muscles, intercostal retraction.\n"
     "Muscles (I always with E): inspiration — external intercostals/diaphragm + SCM, scalenes, pectoralis minor, trapezius; expiration quiet passive, active — internal intercostals, abdominal, quadratus lumborum."),
    ("External Markers of Tuberculosis", "External Markers of Tuberculosis (Book p82)",
     "Phlycten, choroid tubercles, scars/sinuses, scrofula; skin — lupus vulgaris (apple-jelly), erythema nodosum, verrucous cutis, scrofuloderma;\n"
     "cold abscess/collar stud abscess; epididymo-orchitis."),
    ("Other in General Examination", "Other Things in General Examination (Book p82)",
     "Horner's syndrome in lung malignancies.\n"
     "Signs of neurovascular compression: wasting of small muscles of hands."),
    ("Dahl's Sign", "Dahl's Sign (Book p83)",
     "Also Thinker's sign or Target sign: darkened/thickened skin on lower thighs and elbows.\n"
     "Mechanism: air trapping flattens the diaphragm; sitting forwards improves it; hemosiderin from trapped RBCs -> brown discolouration."),
    ("Inspection: Upper Respiratory Tract", "Inspection of the Upper Respiratory Tract (Book p83)",
     "Oral cavity — thrush, tonsils, halitosis -> lung abscess; nose — DNS, polyps;\n"
     "pharynx — post nasal drip can cause respiratory symptoms and breathing difficulty."),
    ("Tracheal Position & Trail's Sign", "Tracheal Position & Trail's Sign (Book p83)",
     "Tracheal position affected mainly by the upper lobes; if no deviation — 'trachea appears central'.\n"
     "Trail's sign: pretracheal fascia relaxes on the shifted side -> undue prominence of the clavicular head of SCM."),
    ("Chest Wall Inspection: Volume Loss, Symmetry, Shapes", "Chest Wall Inspection: Volume Loss, Symmetry & Shapes (Book p83-84)",
     "Volume loss: shoulder droop, medial scapular border prominence (not winging), crowding of ribs. Ratios: normal 5:7, flat 1:2 (TB, fibrothorax), barrel 1:1.\n"
     "Pectus carinatum (rickets) vs excavatum (funnel/cobbler's); Harrison's sulcus (chronic childhood respi disease, rickets); rachitic rosary."),
    ("Back Inspection & Palpation: Movements", "Back Inspection & Palpation: Movements (Book p85)",
     "Flail chest — paradoxical thoracic movement. Kyphosis (forward), scoliosis (lateral; convexity opposite the fibrosed lung).\n"
     "Expansion: normal 5-8 cm; emphysema/ILD/ankylosing spondylitis <1 cm; apical (supraclavicular fossae), anterior (thumbs in front), posterior (TRAPS for upper lobes); metal end in front / on spines; full expiration first."),
    ("Significant URT Findings & Syndromes", "Significant URT Findings & Syndromes (Book p86)",
     "Turbinate hypertrophy/polyps; sinus tenderness = sinusitis. Kartagener's (situs inversus), Wegener's (necrotizing granuloma),\n"
     "Samter's triad (aspirin-asthma-ethmoidal polyps), Young's (sinopulmonary + azoospermia), Churg-Strauss (asthma, eosinophilia, vasculitis, granuloma)."),
    ("Surface Marking of Lungs & Lower Borders", "Surface Marking of Lungs & Lower Borders (Book p86-88)",
     "Right 3 lobes, left 2. Oblique fissure: T2/T3 spinous process -> medial scapular border -> 5th rib MAL -> 6th rib MCL; RML by the horizontal fissure (4th rib sternal border, cuts at 5th rib).\n"
     "Boloor p142/143 views; lower border LUNG 6/8/10 vs PLEURA 8/10/12; front (upper/middle lobes), back (lower lobe), axillary (all three)."),
    ("Tracheal Position: Pushed/Pulled, CricoSternal Distance", "Tracheal Position: Pushed/Pulled & CricoSternal Distance (Book p89)",
     "Slight right deviation normal; pushed opposite — effusion, pneumothorax, apical tumour; pulled same — fibrosis, collapse; same-side in effusion — fibrosis/collapse, mesothelioma.\n"
     "CricoSternal distance: number of fingers insinuated; reduced in COPD (mediastinum pulls the cricoid down)."),
    ("Inspiratory Tracheal Descent & Tracheal Tug (p90)", "Inspiratory Tracheal Descent & Tracheal Tug (Book p90)",
     "Inspiratory tracheal descent — COPD — Campbell's sign.\n"
     "Oliver's sign: chin raised, cricoid held up on deglutition; positive — downward tug (aortic arch aneurysm); false positive — tumour attached to the arch; false negative — non pulsatile thrombosed aneurysm."),
    ("Trachea: Normal Position & Trail's Sign (p91)", "Trachea: Normal Position & Trail's Sign (Book p91)",
     "Normally central or slightly deviated to right. Trail's sign — ipsilateral fascia relaxes, SCM contracts -> prominent clavicular head.\n"
     "Implication of tracheal shift: upper mediastinal shift; indicates upper lobe fibrosis or collapse."),
    ("Tracheal Palpation: Oliver's & Campbell's (p92)", "Tracheal Palpation: Oliver's & Campbell's Sign (Book p92)",
     "Oliver's sign: stand behind, hold cricoid, slight upward thrust; positive — downward pull with each heart beat (aortic aneurysm); false positive — tumour attached to abdominal aorta; false negative — thrombosed aneurysm.\n"
     "Campbell sign: downward pull of the depressed diaphragm in long standing hyperinflation. Figs 3D.14/15 — tracing the trachea, feeling for resistance."),
]


def main() -> None:
    rows = DATA
    pages = [r[0] for r in rows]
    assert pages == sorted(pages), "questions must follow book page order"
    assert set(pages) == EXPECTED_PAGES, "every page of 80-92 must be covered"

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
