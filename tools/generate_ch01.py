#!/usr/bin/env python3
"""Generate data/ch01.json (General Examination, Book p3-14) and its coverage ledger.

Run from the repository root:  python3 tools/generate_ch01.py
The artifact is the editable source of truth; build_content.py embeds it in the app.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from ch01_data_a import A  # noqa: E402
from ch01_data_b import B  # noqa: E402
from ch01_data_c import C  # noqa: E402
from ch01_data_d import D  # noqa: E402

CHAPTER = 1
TITLE = "General Examination"
PAGE_RANGE = "3-14"

# Unit sources: (section in book order, unit title, 2-4 line guide).
UNITS = [
    ("General Examination: Overview & Vitals", "Overview & the Vital Signs",
     "The general survey runs conscious/oriented/cooperative to build and nutrition to the vitals.\n"
     "Vitals = pulse (rate, rhythm, volume, character, delay, vessel wall thickening, peripheral pulses), respiratory rate, blood pressure and temperature.\n"
     "Temperature must be measured with a thermometer - never record 'afebrile' without one.\n"
     "Then pallor, icterus, cyanosis, clubbing, lymphadenopathy and oedema complete the survey."),
    ("Temperature & its Measurement", "Temperature: Definition & Sites",
     "Fever (Harrison's 19e) = AM >98.9 F (>37.2 C) or PM >99.9 F (>37.7 C); normal range 36.5-37.5 C (97.7-99.5 F).\n"
     "Evening rise is due to increased basal metabolic rate and skeletal muscle activity.\n"
     "Sites beyond axilla/oral: rectum (higher than oral; lower oral readings from mouth breathing), lower oesophagus (core), tympanic membrane."),
    ("Fever vs Hyperthermia", "Fever vs Hyperthermia & Hyperthermia Causes",
     "Fever raises the hypothalamic set point; hyperthermia is an uncontrolled rise that exceeds heat loss with an intact set point - so antipyretics fail.\n"
     "Causes of hyperthermia: heat stroke; malignant hyperthermia (halothane); neuroleptic malignant syndrome (haloperidol, fluphenazine); serotonin syndrome (two or more serotonergic drugs)."),
    ("Hyperpyrexia, Hypothalamic Fever & Fever Mechanism", "Hyperpyrexia, Hypothalamic Fever & the Fever Cascade",
     "Hyperpyrexia = fever >41.5 C (>106.7 F); causes CNS haemorrhage and severe infection.\n"
     "Hypothalamic dysfunction usually gives subnormal, not supranormal, temperature.\n"
     "Fever cascade: IL-1, IL-6, TNF-alpha -> hypothalamic endothelial cells -> PGE2 -> raised set point."),
    ("AUFI & PUO", "AUFI & PUO",
     "AUFI = fever <14 days without an organ-system-specific cause; say Dengue, Scrub typhus, Leptospirosis, Malaria, Enteric fever in that order and never volunteer Kala-azar.\n"
     "PUO (Petersdorf and Beeson): >3 weeks, fever >101 on two occasions, uncertain despite 1 week inpatient evaluation; Harrison's adds no immunocompromise and an obligatory investigation set.\n"
     "Variants: nosocomial, neutropenic, HIV-associated. PUO is atypical presentations of common illness, not typical presentations of rare illness.\n"
     "Causes: infectious, neoplastic (including atrial myxoma), connective tissue disease and drug fever."),
    ("Auto-inflammatory Diseases of Fever", "Auto-inflammatory Fevers",
     "Auto-inflammatory diseases with characteristic fever: adult and juvenile Still's disease, familial Mediterranean fever (Robbins; colchicine), Behcet's syndrome, CAPS, PAPA and hyper-IgD syndrome.\n"
     "Colchicine has exactly three listed uses: gout, pericarditis, FMF.\n"
     "PAPA = Pyogenic arthritis, Pyoderma gangrenosum, Acne."),
    ("Relative Bradycardia & Tachycardia", "Relative Bradycardia & Tachycardia",
     "Pulse should rise about 10/min per 1 F of fever (about 18 per 1 C).\n"
     "Relative bradycardia: enteric fever first week (heart block), viral fevers including dengue and yellow fever (Faget's sign), brucellosis, Weil's disease.\n"
     "Relative tachycardia: acute rheumatic carditis, tuberculosis, polyarteritis nodosa, diphtheritic myocarditis."),
    ("Patterns of Fever", "Patterns of Fever",
     "Intermittent touches the baseline (quotidian, double quotidian, tertian, quartan); remittent swings >2 C (normal fluctuation 0.9 C) and never touches it; continued swings <=1 C and never touches it.\n"
     "Named patterns: Pel-Ebstein (Hodgkin's lymphoma only), camel hump/double quotidian (kala-azar, gonococcal perihepatitis), step-ladder (enteric fever), undulant (brucellosis), relapsing (Borrelia), hectic (pent-up pus).\n"
     "Charcot's intermittent fever = chills with RUQ pain and jaundice from a stone in the CBD."),
    ("Hypothermia", "Hypothermia",
     "Primary hypothermia is accidental exposure; secondary is failure of thermoregulation (CVA, overwhelming sepsis, low cardiac output after acute MI, endocrine failure, intoxication).\n"
     "Signs and symptoms listed: altered sensorium from confusion to coma, tachypnoea, tachycardia, lethargy, shivering and pallor."),
    ("Pallor", "Pallor",
     "Anaemia and pallor are not interchangeable - anaemia is only one cause of pallor.\n"
     "Examine in sunlight: lower palpebral conjunctiva, tip and dorsum of tongue, palatal mucosa, nail beds, palms and soles.\n"
     "Pallor without anaemia (Kundu): shock, low cardiac output, hypothyroidism, hypopituitarism.\n"
     "Anaemia classification: marrow production defect, ineffective erythropoiesis (nuclear and cytoplasmic), blood loss/haemolysis."),
    ("Icterus", "Icterus",
     "Look at the sclera through the upper palpebral conjunctiva - not the bulbar conjunctiva (mud and dust) - and ask the patient to look down.\n"
     "Minimum bilirubin for clinical icterus is 2.5 mg/dL; the sclera is rich in elastic tissue where bilirubin deposits.\n"
     "Tint: lemon yellow = mild haemolytic, orange yellow = moderate hepatocellular, greenish yellow = severe obstructive."),
    ("Cyanosis", "Cyanosis",
     "Bluish discolouration from reduced Hb or Hb derivatives (metHb/sulfHb) in small vessels; visible when reduced Hb exceeds 4 g/dL, i.e. SpO2 below about 85%.\n"
     "It is the absolute, not relative, quantity of reduced Hb that matters - severe anaemia may show no cyanosis.\n"
     "Central (saturation reduced or abnormal derivative) vs peripheral (slow flow, high extraction; oral mucosa and tongue underside spared).\n"
     "Differential cyanosis: lower limb only = PDA with pulmonary hypertension and right-to-left shunt; upper limb only adds TGV; intermittent = Ebstein's anomaly."),
    ("Clubbing: Definition & Grades", "Clubbing: Definition & Grades",
     "Selective bulbous enlargement of the distal digit from subungual soft tissue deposition; Lovibond angle is the normal nail-to-nail-bed angle.\n"
     "Minimum duration 2-3 weeks; the index finger is affected first.\n"
     "Grades: 1 nail bed fluctuation, 2 increase in Lovibond angle, 3 drumstick/parrot beak, 4 hypertrophic osteoarthropathy."),
    ("Causes of Clubbing", "Causes of Clubbing",
     "Suppurative lung disease (bronchiectasis, lung abscess, empyema), thoracic malignancy (bronchogenic carcinoma, bronchial adenoma, mesothelioma), interstitial lung disease.\n"
     "Clubbing is rare in COPD and TB. Cardiovascular: cyanotic heart disease, infective endocarditis, left atrial myxoma. GI: cirrhosis (especially PBC), inflammatory bowel disease.\n"
     "Others: thyroid acropachy of Graves' disease and POEMS syndrome."),
    ("Pseudoclubbing & Theories of Clubbing", "Pseudoclubbing & Theories",
     "Pseudoclubbing preserves the Lovibond angle; per Kundu it is subperiosteal bone resorption without soft tissue proliferation.\n"
     "Causes: leprosy, scleroderma, hyperparathyroidism, acromegaly, vinyl chloride workers with acro-osteolysis.\n"
     "Most accepted theory: megakaryocytes bypass the lung, reach nail-bed arterioles and release PDGF. Other theories: neurogenic (vagal), humoral (GH/PTH/oestrogen), hypoxic (AV fistulae), ferritin."),
    ("Painful, Unilateral & Unidigital Clubbing", "Painful, Unilateral & Unidigital Patterns",
     "Painful clubbing: bronchogenic carcinoma, lung abscess, infective endocarditis.\n"
     "Unilateral clubbing: presubclavian coarctation of aorta (left-sided only), apical bronchogenic carcinoma, cervical rib, aneurysm of the subclavian or axillary artery.\n"
     "Unidigital clubbing: hereditary, repeated local trauma, rarely median nerve injury. The index finger is affected first."),
    ("Lymphadenopathy: Significance & Character", "Lymphadenopathy: Significance & Character",
     "Significant nodes: any supraclavicular or epitrochlear node, inguinal >1.5 cm, others >1 cm.\n"
     "Generalised = two or more non-contiguous areas (Harrison's says three, which the book calls impractical); persistent if more than 3 months.\n"
     "Painful = infection or acute leukaemia; firm rubbery = lymphoma; fluctuant = suppurative; stony hard = metastasis; matted = tuberculous (benign) or lymphoma/metastatic (malignant).\n"
     "Cervical levels: Ia submental, Ib submandibular, II-IV jugular, V posterior triangle, VI anterior triangle, VII superior mediastinal."),
    ("Neurological Causes of Clubbing (Boloor insert)", "Neurological Causes of Clubbing (insert)",
     "The Boloor insert on the neurological causes of clubbing adds syringomyelia, median nerve injury and hemiplegia.\n"
     "It completes the respiratory, cardiovascular, gastrointestinal and other groups given in the main text."),
    ("Grade 4 Clubbing (Boloor figure)", "Grade 4 Clubbing Figure",
     "Boloor Fig. 2C.18 demonstrates grade 4 clubbing.\n"
     "Grade 4 is defined by hypertrophic osteoarthropathy - periosteal reaction of the long bones with joint symptoms - not by the finger appearance alone."),
    ("Atypical Presentations of Clubbing (Boloor table)", "Atypical Clubbing (insert table)",
     "Acute clubbing: subacute bacterial endocarditis, lung abscess, empyema. Reversible: lung abscess, empyema.\n"
     "Unilateral: hemiplegia, aneurysm of the subclavian artery, Pancoast tumour. Unidigital: median nerve injury, trauma. Painful: bronchogenic carcinoma, SBE, lung abscess.\n"
     "Clubbing with cyanosis: cyanotic congenital heart disease and ILD. Pseudoclubbing list adds leukaemic infiltration, thyroid acropachy, sclerodactyly, subungual tumours or cysts.\n"
     "Differential clubbing (upper normal, lower clubbed) = PDA with reversal of shunt; reverse differential clubbing (upper clubbed, lower normal) = PDA + TGA + reversal of shunt."),
    ("Generalised Lymphadenopathy & Oedema", "Generalised Lymphadenopathy & Oedema",
     "Generalised lymphadenopathy groups: infections (HIV, infectious mononucleosis, TB), malignancies, autoimmune (SLE, Felty's, Still's), miscellaneous (sarcoidosis).\n"
     "Non-pitting oedema: myxoedema, late filarial lymphoedema, scleroderma, angioneurotic oedema. Pitting: CCF, cirrhosis, nephrotic syndrome, hypoproteinaemia, pericardial effusion, constrictive pericarditis, amlodipine.\n"
     "Unilateral leg swelling: DVT, soft tissue infection, trauma, lymphoedema, immobility such as hemiplegia. Bilateral: heart failure, chronic venous insufficiency, hypoproteinaemia, lymphatic obstruction, drugs, Milroy's disease."),
    ("Blood Pressure Measurement", "Blood Pressure Measurement",
     "BP is the lateral force of the blood column per unit area of vascular wall. Cuff length about twice its width, average length 25 cm, bladder at least two-thirds of arm circumference.\n"
     "Korotkoff 1 first low-frequency tapping; 2 softer and longer; 3 crisper and louder; 4 muffling (often absent); 5 disappearance. Normally phase 5 is the DBP; in severe AR phase 4 is taken.\n"
     "Normal inter-arm difference 10-15 mmHg."),
    ("Auscultatory Gap & Inter-limb BP Variation", "Auscultatory Gap & Inter-limb BP Variation",
     "Auscultatory gap: sounds disappear after the systolic reading and return just above the diastolic value, seen in elderly hypertensives; it underestimates the systolic BP.\n"
     "Avoid it by palpating the radial pulse, which persists through the gap.\n"
     "Wide inter-arm difference: aortic dissection (haematoma occluding the subclavian artery) and subclavian steal syndrome."),
    ("Pulse Pressure & Haemodynamics", "Pulse Pressure",
     "Pulse pressure = SBP minus DBP; normal 30-60 mmHg.\n"
     "Raised: exercise, AR, PDA, fever, anaemia, AV fistulas, beriberi, Paget's disease (bone fistulae), cirrhosis (intrahepatic and extrahepatic AV fistulae), pregnancy (placenta as a large AV fistula).\n"
     "Narrow: aortic stenosis (outflow obstruction), constrictive pericarditis and cardiac tamponade (filling obstruction), with MS and DSS queried."),
]


def main() -> None:
    rows = A + B + C + D
    pages = [r[0] for r in rows]
    assert pages == sorted(pages), "questions must follow book page order"
    assert set(pages) == set(range(3, 15)), "every page of the range must be covered"

    questions = []
    ledger = []
    for index, (page, fmt, sec, point, q, opts, ans, exp) in enumerate(rows, 1):
        qid = f"MED-C{CHAPTER}-{index:02d}"
        assert len(opts) == 4 and len(set(opts)) == 4, f"{qid}: options"
        assert 0 <= ans < 4, f"{qid}: answer index"
        assert exp.endswith(f"(Book p{page})"), f"{qid}: page citation"
        if fmt == "fillup":
            assert "____" in q, f"{qid}: fill-up blank"
        questions.append(dict(id=qid, sec=sec, page=page, fmt=fmt, q=q, opts=opts, ans=ans, exp=exp))
        ledger.append(dict(chapter=CHAPTER, page=page, point=point, question=qid))

    for _sec, _title, _guide in UNITS:
        if not any(item["sec"] == _sec for item in questions):
            raise SystemExit(f"unit section without questions: {_sec!r}")
    order = [unit_sec for unit_sec, _, _ in UNITS]
    seen = [q["sec"] for q in questions]
    unique = []
    for s in seen:
        if not unique or unique[-1] != s:
            unique.append(s)
    if unique != order:
        for _i, (_a, _b) in enumerate(zip(unique, order)):
            if _a != _b:
                raise SystemExit(f"section order differs at {_i}: data={_a!r} units={_b!r}")
        raise SystemExit(f"section order length mismatch: data={len(unique)} units={len(order)}")

    units = []
    for index, (sec, unit_title, guide) in enumerate(UNITS, 1):
        assert 2 <= len(guide.splitlines()) <= 4, f"unit {index}: guide must be 2-4 lines"
        qs = [q["id"] for q in questions if q["sec"] == sec]
        assert qs, f"unit {index}: no questions"
        units.append(dict(id=f"MED-U{CHAPTER}-{index}", ch=CHAPTER, n=index, title=unit_title, sec=sec, guide=guide, qs=qs))

    flat = [qid for unit in units for qid in unit["qs"]]
    assert flat == [q["id"] for q in questions], "units must tile the question array exactly"

    artifact = dict(chapter=CHAPTER, title=TITLE, pageRange=PAGE_RANGE, questions=questions, units=units)
    (ROOT / "data" / "ch01.json").write_text(json.dumps(artifact, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (ROOT / "audit" / "coverage.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"ch01: {len(questions)} questions, {len(units)} units, {len(ledger)} ledger points")


if __name__ == "__main__":
    main()
