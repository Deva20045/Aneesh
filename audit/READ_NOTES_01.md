# Read notes — Chapter 1, General Examination (Book p3–14)

**Method.** All twelve pages (Book p3–14) were read in printed order from the text
layer of `uploads/part_1.pdf` (the file's sheet number equals the book page for
p1–120), and every page was additionally rendered at 2× with
`python3 tools/render_audit.py 3 14 2` into `.audit-render/book_003.png` …
`book_014.png` to confirm layout and to read the three inserted Boloor reference
pages (p10–12), which carry no text layer. Text extraction was spot-checked
against the renders line by line, so no point below rests on an unverified guess.

**What was interrogated.** Every heading, bullet, sub-bullet, table cell, figure
label and numeric value in p3–14 is represented by at least one question, and
tables were converted into whole-set questions rather than single-fact recalls:
the temperature sites, the hyperthermia causes, the AUFI order, the PUO criteria
and obligatory investigations, the auto-inflammatory list, the fever-pattern
matrix (intermittent/remittent/continued and the named patterns), pallor sites,
the anaemia classification, the icterus tints, the cyanosis types and differential
patterns, the four clubbing grades, the cause groups, pseudoclubbing versus the
five theories, the Boloor neurological and atypical-clubbing tables, the
lymph-node characters and cervical levels, the oedema and leg-swelling lists, and
the Korotkoff, auscultatory-gap and pulse-pressure material.

**Points the book leaves blank** were deliberately not invented: the p14 stubs
"Drugs causing oedema", "Slow filling vs fast filling oedema", "Latest
hypertension guidelines", "Mean arterial pressure", "Pulsus paradoxus" and
"Types of hypertension — ref Alagappan" are headings with no detail in these
pages; the detail lives in the CVS pulse/BP pages (Book p26–30) and will be
built with that chapter. Nothing was fabricated to fill them.

**Insert cross-links.** Boloor p.85 (p10) adds the neurological causes of
clubbing; Boloor p.87 (p11) is the grade-4 clubbing photograph; Boloor p.88 (p12)
is the atypical clubbing table. The three inserts are questioned at their own
book page, so the citation stays exact.

## Unit and question inventory

| Unit | Section | Book page(s) | Questions | Formats |
|---:|---|---|---:|---|

| 1 | Overview & the Vital Signs | 3 | 4 | recall 1, fillup 1, oddoneout 1, match 1 |
| 2 | Temperature: Definition & Sites | 3 | 5 | numeric 2, recall 1, match 1, scenario 1 |
| 3 | Fever vs Hyperthermia & Hyperthermia Causes | 3 | 5 | recall 1, scenario 1, match 1, oddoneout 1, truefalse 1 |
| 4 | Hyperpyrexia, Hypothalamic Fever & the Fever Cascade | 4 | 5 | numeric 1, truefalse 1, match 1, fillup 1, oddoneout 1 |
| 5 | AUFI & PUO | 4 | 11 | scenario 3, recall 2, match 2, numeric 1, truefalse 1, oddoneout 1, fillup 1 |
| 6 | Auto-inflammatory Fevers | 4 | 6 | fillup 2, recall 2, oddoneout 1, numeric 1 |
| 7 | Relative Bradycardia & Tachycardia | 5 | 6 | recall 2, numeric 1, match 1, scenario 1, oddoneout 1 |
| 8 | Patterns of Fever | 5–6 | 15 | recall 5, match 4, scenario 2, numeric 1, oddoneout 1, fillup 1, truefalse 1 |
| 9 | Hypothermia | 6 | 4 | recall 2, oddoneout 1, scenario 1 |
| 10 | Pallor | 6 | 5 | recall 2, match 2, oddoneout 1 |
| 11 | Icterus | 6 | 6 | recall 3, numeric 1, match 1, scenario 1 |
| 12 | Cyanosis | 7 | 9 | numeric 2, scenario 2, match 2, recall 1, oddoneout 1, truefalse 1 |
| 13 | Clubbing: Definition & Grades | 7–8 | 6 | recall 3, numeric 1, match 1, scenario 1 |
| 14 | Causes of Clubbing | 8 | 6 | match 1, truefalse 1, oddoneout 1, recall 1, fillup 1, scenario 1 |
| 15 | Pseudoclubbing & Theories | 8 | 6 | recall 2, match 2, scenario 1, fillup 1 |
| 16 | Painful, Unilateral & Unidigital Patterns | 9 | 5 | recall 3, scenario 1, oddoneout 1 |
| 17 | Lymphadenopathy: Significance & Character | 9 | 8 | numeric 2, recall 2, match 2, scenario 2 |
| 18 | Neurological Causes of Clubbing (insert) | 10 | 2 | recall 1, oddoneout 1 |
| 19 | Grade 4 Clubbing Figure | 11 | 2 | recall 1, scenario 1 |
| 20 | Atypical Clubbing (insert table) | 12 | 8 | scenario 3, recall 2, match 2, oddoneout 1 |
| 21 | Generalised Lymphadenopathy & Oedema | 13 | 10 | scenario 4, match 3, oddoneout 2, recall 1 |
| 22 | Blood Pressure Measurement | 14 | 6 | recall 2, numeric 2, match 1, scenario 1 |
| 23 | Auscultatory Gap & Inter-limb BP Variation | 14 | 4 | recall 1, management 1, oddoneout 1, scenario 1 |
| 24 | Pulse Pressure | 14 | 5 | scenario 2, numeric 1, match 1, recall 1 |

**Chapter 1 total:** 149 questions across 24 units, covering Book p3–14 with no page omitted.

## Point → question map (audit/coverage.json)


**Book p3**

- Opening sequence of general examination → `MED-C1-01`
- Temperature must always be measured with a thermometer → `MED-C1-02`
- Steps of general examination → `MED-C1-03`
- Reporting lymphadenopathy: site, number, consistency, tenderness, shape, matted → `MED-C1-04`
- Harrison's/19e definition of fever → `MED-C1-05`
- Normal body temperature range → `MED-C1-06`
- Why temperature is higher in the evening → `MED-C1-07`
- Alternative sites for temperature measurement → `MED-C1-08`
- Mouth breathing lowers oral reading → `MED-C1-09`
- Fever vs hyperthermia: the set-point distinction → `MED-C1-10`
- Antipyretics do not reduce hyperthermia → `MED-C1-11`
- Drugs and settings of the four hyperthermia causes → `MED-C1-12`
- Causes of hyperthermia → `MED-C1-13`
- Statements on fever and hyperthermia → `MED-C1-14`

**Book p4**

- Definition of hyperpyrexia → `MED-C1-15`
- Hypothalamic fever → `MED-C1-16`
- Mechanism of fever → `MED-C1-17`
- Pyrogenic cytokines → `MED-C1-18`
- Pyrogenic cytokine list → `MED-C1-19`
- Definition of AUFI → `MED-C1-20`
- Order in which AUFI causes should be said → `MED-C1-21`
- Kala-azar and 'our setting' → `MED-C1-22`
- Petersdorf and Beeson definition of PUO → `MED-C1-23`
- Harrison's criteria for PUO → `MED-C1-24`
- Obligatory investigations in PUO → `MED-C1-25`
- Types of PUO → `MED-C1-26`
- Key principle underlying PUO → `MED-C1-27`
- Aetiology of PUO by group → `MED-C1-28`
- Atrial myxoma as a neoplastic cause of PUO → `MED-C1-29`
- Intra-abdominal abscess sites in PUO → `MED-C1-30`
- Auto-inflammatory diseases with characteristic fever → `MED-C1-31`
- FMF pathogenesis reference and treatment → `MED-C1-32`
- The three diseases in which colchicine is used → `MED-C1-33`
- PAPA syndrome → `MED-C1-34`
- CAPS expansion → `MED-C1-35`
- Hyper-IgD syndrome → `MED-C1-36`

**Book p5**

- Pulse response to fever → `MED-C1-37`
- Causes of relative bradycardia → `MED-C1-38`
- Faget's sign → `MED-C1-39`
- Mechanism of relative bradycardia in enteric fever → `MED-C1-40`
- Separating causes of relative bradycardia from relative tachycardia → `MED-C1-41`
- Relative tachycardia list → `MED-C1-42`
- Definition of intermittent fever → `MED-C1-43`
- Subdivisions of intermittent fever → `MED-C1-44`
- Causes of quotidian fever → `MED-C1-45`
- Double quotidian fever and its classic associations → `MED-C1-46`
- Malarial fevers and their other names → `MED-C1-47`
- Definition of remittent fever → `MED-C1-48`
- Normal daily temperature fluctuation → `MED-C1-49`
- Remittent and continued fever causes → `MED-C1-50`
- Which fever never touches the baseline → `MED-C1-51`
- Pel-Ebstein pattern → `MED-C1-52`
- Specific named fever patterns → `MED-C1-53`
- Step-ladder fever → `MED-C1-54`
- Baseline behaviour across fever patterns → `MED-C1-55`
- Fever with splenomegaly and double spikes → `MED-C1-56`

**Book p6**

- Hectic fever and pent-up pus → `MED-C1-57`
- Primary versus secondary hypothermia → `MED-C1-58`
- Secondary hypothermia → `MED-C1-59`
- Hypothermia in a myxoedematous patient → `MED-C1-60`
- Signs and symptoms of hypothermia → `MED-C1-61`
- Anaemia and pallor are not interchangeable → `MED-C1-62`
- Sites to examine for pallor → `MED-C1-63`
- Sites for pallor versus sites for icterus → `MED-C1-64`
- Pallor without anaemia → `MED-C1-65`
- Aetiopathological classification of anaemia → `MED-C1-66`
- Where to look for icterus → `MED-C1-67`
- Minimum bilirubin for clinical icterus → `MED-C1-68`
- Why the sclera shows icterus early → `MED-C1-69`
- Tints of icterus → `MED-C1-70`
- Why ask the patient to look down → `MED-C1-71`
- Mild haemolytic jaundice → `MED-C1-72`

**Book p7**

- Definition of cyanosis → `MED-C1-73`
- Reduced haemoglobin threshold for cyanosis → `MED-C1-74`
- SpO2 corresponding to cyanosis → `MED-C1-75`
- Absolute quantity of reduced haemoglobin → `MED-C1-76`
- Central versus peripheral cyanosis → `MED-C1-77`
- Causes of central cyanosis → `MED-C1-78`
- Iron-replete and iron-deplete cyanosis → `MED-C1-79`
- Differential cyanosis patterns → `MED-C1-80`
- Differential cyanosis with lower-limb cyanosis → `MED-C1-81`
- Definition of clubbing → `MED-C1-82`
- The Lovibond angle → `MED-C1-83`
- Minimum duration for clubbing to appear → `MED-C1-84`
- First finger to be affected → `MED-C1-85`

**Book p8**

- Grades of clubbing → `MED-C1-86`
- Grade 4 clubbing and HOA → `MED-C1-87`
- Groups of causes of clubbing → `MED-C1-88`
- Diseases in which clubbing is rare → `MED-C1-89`
- Clubbing in suppurative and interstitial disease → `MED-C1-90`
- Thyroid acropachy → `MED-C1-91`
- POEMS syndrome → `MED-C1-92`
- Graves' disease with clubbing → `MED-C1-93`
- Definition of pseudoclubbing → `MED-C1-94`
- Causes of pseudoclubbing → `MED-C1-95`
- Bulbous fingers with a preserved angle → `MED-C1-96`
- Most accepted theory of clubbing → `MED-C1-97`
- Growth factor released in the nail bed → `MED-C1-98`
- Theories of clubbing → `MED-C1-99`

**Book p9**

- Causes of painful clubbing → `MED-C1-100`
- Unilateral clubbing → `MED-C1-101`
- Left-sided clubbing only → `MED-C1-102`
- Unidigital clubbing → `MED-C1-103`
- First affected finger → `MED-C1-104`
- When lymphadenopathy is significant → `MED-C1-105`
- Nodes significant whatever their size → `MED-C1-106`
- Definition of generalised lymphadenopathy → `MED-C1-107`
- Persistent generalised lymphadenopathy → `MED-C1-108`
- Character of lymph nodes → `MED-C1-109`
- Matted nodes → `MED-C1-110`
- Levels of cervical nodes → `MED-C1-111`
- Node character in a young patient → `MED-C1-112`

**Book p10**

- Neurological causes of clubbing → `MED-C1-113`
- Neurological clubbing list → `MED-C1-114`

**Book p11**

- The grade demonstrated in Boloor Fig. 2C.18 → `MED-C1-115`
- Interpretation of grade 4 → `MED-C1-116`

**Book p12**

- Acute clubbing → `MED-C1-117`
- Unilateral and unidigital clubbing in the table → `MED-C1-118`
- Painful and cyanotic clubbing in the table → `MED-C1-119`
- Differential clubbing and its lesion → `MED-C1-120`
- Reverse differential clubbing → `MED-C1-121`
- Pseudoclubbing list in the table → `MED-C1-122`
- Clubbing with cyanosis in the table → `MED-C1-123`
- Reversible clubbing → `MED-C1-124`

**Book p13**

- Causes of generalised lymphadenopathy by group → `MED-C1-125`
- Pitting and non-pitting oedema → `MED-C1-126`
- Amlodipine-induced oedema → `MED-C1-127`
- Non-pitting oedema → `MED-C1-128`
- Unilateral and bilateral leg swelling → `MED-C1-129`
- Milroy's disease → `MED-C1-130`
- Unilateral leg swelling list → `MED-C1-131`
- Autoimmune causes of generalised lymphadenopathy → `MED-C1-132`
- Miscellaneous cause of generalised lymphadenopathy → `MED-C1-133`
- Which oedema is non-pitting? → `MED-C1-134`

**Book p14**

- Definition of blood pressure → `MED-C1-135`
- Dimensions of the BP cuff → `MED-C1-136`
- Phases of Korotkoff sounds → `MED-C1-137`
- Which Korotkoff phase is taken as DBP → `MED-C1-138`
- Choosing the diastolic end point → `MED-C1-139`
- Normal variation between upper limbs → `MED-C1-140`
- Definition and effect of the auscultatory gap → `MED-C1-141`
- Avoiding the error of the auscultatory gap → `MED-C1-142`
- Causes of increased inter-arm BP difference → `MED-C1-143`
- Subclavian steal syndrome → `MED-C1-144`
- Normal pulse pressure → `MED-C1-145`
- Raised and narrow pulse pressure causes → `MED-C1-146`
- Paget's disease and pulse pressure → `MED-C1-147`
- Narrow pulse pressure in a young patient → `MED-C1-148`
- Adjuncts queried in narrow pulse pressure → `MED-C1-149`

**Unasked points after this review:** NONE in the recorded inventory. Every listed point resolves to exactly one question, and the ledger order equals the question array order (enforced by `validate_content.py`).
