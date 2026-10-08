# PULSE · Aneesh Notes — Progress

Updated **2026-10-08** (Chapters 1–6 shipped — General Examination through Mitral Stenosis, Book p3–55 & p73–74).
Standalone offline quiz built line by line from the annotated clinical notes in `uploads/`.

- Repository: `Deva20045/Aneesh`
- Session branch: `arena/59b97b63-aneesh`
- **Live link: https://deva20045.github.io/Aneesh/** (`index.html` redirects to `pulse-aneesh.html`)
- Architecture: template of `Deva20045/Med-V2` — one standalone HTML app, `QUESTIONS`/`UNITS`/`CHAPTERS` schema, unit guides, index redirect.
- Editable source of truth: `data/chNN.json`; generated deliverable: `pulse-aneesh.html`.
- **Build status: 6 live chapters / 51 roadmap chapters · 374 questions · 61 units.**
- Book PDFs (now `uploads/part_1.pdf`, `uploads/part_2.pdf`) were moved out of the repository root and committed there.

## Goal

Turn the annotated clinical notes (Book p1–249) into a chapter-wise question bank
that is a **complete substitute for reading the PDF**: every important line, table,
figure label, classification, value, investigation and exception becomes a
question with four plausible options, an explanation that teaches, and the exact
citation `(Book pX)`. Book and section order are preserved; nothing is fabricated;
anything unclear is re-read from the rendered page.

## PDF → book page map and the page-offset formula

Book p1 states that page numbers refer to the **annotated document** (249 pages),
not the original 197-page compilation. All citations use that numbering.

| File | PDF sheets | Book pages | Formula |
|---|---:|---|---|
| `uploads/part_1.pdf` | 120 | 1–120 | `book page = PDF sheet number` |
| `uploads/part_2.pdf` | 129 | 121–249 | `book page = PDF sheet number + 120` |

Both PDFs carry a text layer, so pages are read as text plus a 2× render
(`tools/render_audit.py 3 14 2`). The **image-only pages** — no text layer or under
400 characters — are: 10, 11, 12, 15, 18, 19, 48, 49, 56, 59, 62, 69, 73, 74, 79,
84, 87, 90, 118, 123, 131, 152, 153, 157, 163, 164, 177, 181, 192, 193, 206, 221,
244, 249. Inserted reference pages and the verified chapter-start table are in
`audit/PAGE_MAP.md`.

## Schema (mirrors Med-V2 exactly)

```jsonc
// data/chNN.json
{ "chapter": 1, "title": "General Examination", "pageRange": "3-14",
  "questions": [
    { "id": "MED-C1-01", "sec": "<unit section>", "page": 3,
      "fmt": "recall|fillup|match|truefalse|scenario|oddoneout|numeric|management",
      "q": "…", "opts": ["…", "…", "…", "…"], "ans": 0, "exp": "… (Book p3)" } ],
  "units": [
    { "id": "MED-U1-1", "ch": 1, "n": 1, "title": "…", "sec": "…",
      "guide": "2–4 lines of the teaching the unit assumes", "qs": ["MED-C1-01", "…"] } ] }
```

Rules enforced fail-closed by `validate_content.py` before every build: sequential
ids, four unique options, an answer index 0–3, every explanation ending in
`(Book pX)` for that question's own page, question pages non-decreasing and
covering **every** page of the chapter's `pageRange`, `fillup` stems containing
`____`, `truefalse` questions with exactly two `True` and two `False` options, no
"None of the above", 2–4 line unit guides, and unit `qs` lists that tile the
question array exactly (contiguous, in order). `tests/app_parsers.cjs` then runs
the **actual app JavaScript** parsers (`parseMatch`, `fillupHtml`, `matchOptHtml`,
`splitExp`) against every question, including negative controls. The match grammar
is `stem — 1) … 2) … … A) … B) …` with bijective key options.

## Per-chapter pipeline

1. Read: render the chapter's pages at 2× (`tools/render_audit.py first last 2`) and
   read text + render together, page by page, in book order. Image-only pages are
   read from the render alone.
2. Capture: write the questions into `tools/chNN_data_*.py` as
   `(page, fmt, sec, point, question, opts, ans, exp)` tuples — one `point` per
   source line/table row/figure label, so the audit ledger is generated, not hand-kept.
3. Generate: `python3 tools/generate_chNN.py` writes `data/chNN.json` and appends the
   chapter's rows to `audit/coverage.json`.
4. Read record: `python3 tools/generate_read_notes.py` → `audit/READ_NOTES_NN.md`
   (unit inventory + every point → question).
5. Gate: `python3 validate_content.py` then `python3 build_content.py` (which runs the
   gate again) and `python3 validate_content.py --embedded`.
6. Ship: commit, push the session branch, open the PR, merge, and confirm the Pages URL.

## Chapter status

**DONE (live):**
- **Ch 1** — General Examination, Book p3–15 · 151 questions · 25 units (recall 42, scenario 31, match 30, oddoneout 17, numeric 16, fillup 8, truefalse 6, management 1).
- **Ch 2** — CVS - History & Symptomatology, Book p16–30 · 93 questions · 13 units (match 25, scenario 19, numeric 12, oddoneout 11, fillup 9, recall 8, truefalse 7, management 2).
- **Ch 3** — CVS - Cardiac Examination: Inspection & JVP, Book p31–36 · 42 questions · 6 units (scenario 11, match 10, numeric 7, truefalse 4, fillup 4, oddoneout 3, recall 2, management 1).
- **Ch 4** — CVS - Cardiac Examination: Palpation & Auscultation, Book p37–47 · 42 questions · 8 units (match 17, scenario 9, numeric 4, recall 3, truefalse 3, fillup 3, oddoneout 2, management 1).
- **Ch 5** — CVS - Approach to Diagnosis & the Cardiac Cycle, Book p48, 73–74 · 14 questions · 3 units (match 5, scenario 2, numeric 2, recall 1, fillup 1, oddoneout 1, truefalse 1, management 1).
- **Ch 6** — Mitral Stenosis, Book p49–55 · 32 questions · 6 units (match 11, scenario 6, recall 3, fillup 3, numeric 3, truefalse 2, oddoneout 2, management 2).

**NEXT:** Ch 7 — Mitral Regurgitation, Book p56–57 (includes Harrison's Table 264-1 on p56).

| Ch | Title | Book pages | Status |
|---:|---|---:|---|
| 1 | General Examination | 3–15 | **DONE — live** |
| 2 | CVS - History & Symptomatology | 16–30 | **DONE — live** |
| 3 | CVS - Cardiac Examination: Inspection & JVP | 31–36 | **DONE — live** |
| 4 | CVS - Cardiac Examination: Palpation & Auscultation | 37–47 | **DONE — live** |
| 5 | CVS - Approach to Diagnosis & the Cardiac Cycle | 48, 73–74 | **DONE — live** |
| 6 | Mitral Stenosis | 49–55 | **DONE — live** |
| 7 | Mitral Regurgitation | 56–57 | NEXT |
| 8 | Aortic Stenosis | 58–61 | Soon |
| 9 | Aortic Regurgitation | 62–63 | Soon |
| 10 | Congenital Heart Disease | 64 | Soon |
| 11 | Rheumatic Fever | 65–68 | Soon |
| 12 | Infective Endocarditis & 2023 Duke-ISCVID | 69–72 | Soon |
| 13 | RS - History, Symptomatology & Breathlessness Tables | 75–79 | Soon |
| 14 | RS - General Examination & Chest Wall | 80–92 | Soon |
| 15 | RS - Inspection, Palpation & Percussion | 93–97 | Soon |
| 16 | RS - Auscultation, Breath Sounds & Crackles | 98–104 | Soon |
| 17 | RS - Clubbing, Lung Lymphatics & TB/Pneumonia Protocols | 105–107 | Soon |
| 18 | RS - Consolidation, Collapse, Fibrosis & Cavity | 108–109 | Soon |
| 19 | RS - Pleural Effusion & Empyema | 110–111 | Soon |
| 20 | Abdomen - History, Ascites & General Examination | 112–116 | Soon |
| 21 | Abdomen - Venous Flow Patterns & the Liver | 117–124 | Soon |
| 22 | Abdomen - The Spleen | 125–131 | Soon |
| 23 | Hepatic Encephalopathy - West Haven & Mechanisms | 132–137 | Soon |
| 24 | Portal Hypertension & Abdomen Additions | 138–140 | Soon |
| 25 | Ascites - Investigations, Refractory Ascites & Complications | 141–143 | Soon |
| 26 | Leukaemias - CML & CLL | 144–148 | Soon |
| 27 | Polycythemia, Fever with Splenomegaly & Hypersplenism | 149–151 | Soon |
| 28 | Portal Hypertension - Pressure, Diagnosis & Treatment | 152–153 | Soon |
| 29 | Acute Liver Failure, Child-Pugh & Transplantation | 154–155 | Soon |
| 30 | Alcohol & Liver Disease | 156–159 | Soon |
| 31 | Chemotherapy Protocols - AML & Myeloma | 160–161 | Soon |
| 32 | Approach to an Abdominal Mass | 162–163 | Soon |
| 33 | MMSE & Bedside Cognitive Testing | 164 | Soon |
| 34 | Stroke - History & Risk Factors | 165–170 | Soon |
| 35 | Neurocutaneous Markers & Neck Examination | 171–173 | Soon |
| 36 | Higher Mental Functions & Cranial Nerves | 174–186 | Soon |
| 37 | Motor System Examination & Subtle Hemiparesis | 187–192 | Soon |
| 38 | Plantar Response & Primitive Reflexes | 193–197 | Soon |
| 39 | Cerebellum, Gait & Sensory Examination | 198–203 | Soon |
| 40 | Stroke - Theory, Classification & Management | 204–208 | Soon |
| 41 | Stroke - 2026 AHA/ASA Guideline Update | 209–211 | Soon |
| 42 | Internal Capsule & Cerebral Arterial Supply | 212–216 | Soon |
| 43 | Brainstem Strokes & Viva Points | 217–221 | Soon |
| 44 | CNS & Stroke - Niharika's Additions | 222–223 | Soon |
| 45 | Paraplegia - Case Proforma & Approach | 224–233 | Soon |
| 46 | Conus Medullaris, SACD, GBS & CIDP | 234–238 | Soon |
| 47 | Bladder in Cord Lesions & Micturition | 239–241 | Soon |
| 48 | Chronic Myelopathies | 242 | Soon |
| 49 | Paraplegia - Niharika's Additions | 243 | Soon |
| 50 | Appendix - Harrison's JVP, Arterial Pulse & Blood Pressure | 244–248 | Soon |
| 51 | Extras - Vivek Sir's PDFs (pointer page) | 249 | Soon |

## Release — Chapter 1 (General Examination, Book p3–14)

| Ch | Title | Book pages | Questions | Units |
|---:|---|---:|---:|---:|
| 1 | General Examination | 3–14 | 149 | 24 |

### Quality and ordering contract delivered

1. All twelve pages were read in printed order — text layer plus 2× renders of every
   page — and the three inserted Boloor pages (p10 neurological causes of clubbing,
   p11 grade-4 clubbing figure, p12 atypical-clubbing table) were read from their
   images because they carry no text layer. The read record with every point →
   question mapping is `audit/READ_NOTES_01.md`.
2. 149 points are inventoried in `audit/coverage.json` in book order, one per
   question; `tools/generate_ch01.py` regenerates `data/ch01.json` and the ledger
   idempotently. No page in 3–14 is skipped and no page carries a question that is
   not on it.
3. Formats are mixed deliberately (recall 42, scenario 30, match 29, oddoneout 17,
   numeric 16, fillup 8, truefalse 6, management 1) so the answer position and the
   question style are never predictable; distractors are same-category medical
   alternatives (for example IL-4 beside IL-1/IL-6/TNF-α in the pyrogenic-cytokine
   question, P. malariae beside P. vivax/ovale and P. falciparum in the malarial-fever
   match, or "lobar pneumonia" beside the remittent-fever causes in the
   which-pattern question).
4. Whole tables were converted into multi-row questions: temperature sites,
   hyperthermia syndromes, fever-pattern matrix, pallor sites, anaemia
   classification, icterus tints, cyanosis types and differential patterns,
   clubbing grades, cause groups, five theories of clubbing, the Boloor atypical
   table, cervical node levels, pitting/non-pitting and leg-swelling lists, and the
   Korotkoff phases.
5. Stub headings with no detail on these pages ("Drugs causing oedema", "Slow
   filling vs fast filling oedema", "Latest hypertension guidelines", "Mean
   arterial pressure", "Pulsus paradoxus", "Types of hypertension — ref
   Alagappan") were **not** invented; they are completed from the CVS pulse/BP
   pages when that chapter is built.
6. `validate_content.py` passes on schema, sequence, inventory and the app's own
   JavaScript parsers, and `validate_content.py --embedded` confirms the HTML
   arrays equal `data/ch01.json` with the roadmap flags (Chapter 1 `live: true`,
   the other 50 chapters `"Soon"`).

## Build and check locally

```bash
python3 tools/render_audit.py 3 14 2      # review renders -> .audit-render/book_003.png …
python3 tools/generate_ch01.py            # regenerate data/ch01.json + audit/coverage.json
python3 tools/generate_read_notes.py      # regenerate audit/READ_NOTES_01.md
python3 validate_content.py --ledger      # print every point -> question, then gate
python3 build_content.py                  # embed artifacts in pulse-aneesh.html
python3 validate_content.py --embedded    # require exact data/HTML agreement
python3 -m http.server 8000               # preview at http://localhost:8000/
```
