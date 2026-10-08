# PDF → Book page map (annotated notes, Book p1–249)

The notes are an **annotated document of 249 pages**. Book p1 states plainly:
*"Page numbers refer to this annotated document, not the original 197-page compilation."*
Every citation in this app — `(Book pN)`, the roadmap `p` column, the chapter
`pageRange` — therefore uses the **annotated-document page number 1–249**.

## The page-offset formula

The two uploaded PDFs are contiguous halves of the same document:

| File | PDF sheets | Book pages | Formula |
|---|---:|---|---|
| `uploads/part_1.pdf` | 120 | 1–120 | `book page = PDF sheet number` |
| `uploads/part_2.pdf` | 129 | 121–249 | `book page = PDF sheet number + 120` |

Equivalently, `PDF sheet = book page` for pages ≤ 120 and
`PDF sheet = book page − 120` for pages ≥ 121. `tools/render_audit.py` and
`tools/heading_scan.py` implement exactly this (`SPLIT = 120`).

Both files carry a real text layer (pypdf/pymupdf extraction), so the line-by-line
read of Chapter 1 used extracted text, with 2× renders of every page to confirm
layout, tables and figures and to read the image-only inserted pages.

## Inserted reference pages (coloured tab, "INSERTED REFERENCE")

| Book page | Source |
|---|---|
| 10 | Boloor p.85 — neurological causes of clubbing (syringomyelia, median nerve injury, hemiplegia) |
| 11 | Boloor p.87 — Fig. 2C.18, grade 4 clubbing photograph |
| 12 | Boloor p.88 — atypical presentation of clubbing table |
| 18–19 | Boloor Table 3C.7 — orthopnoea vs PND (2 pages) |
| 49 | Harrison's Table 263-1 — major causes of mitral stenosis |
| 56 | Harrison's Table 264-1 — major causes of mitral regurgitation |
| 59 | Harrison's Table 261-1 — major causes of aortic stenosis |
| 62 | Harrison's Table 262-1 — major causes of aortic regurgitation |
| 71–72 | 2023 ESC endocarditis guideline + 2023 Duke-ISCVID criteria (written addendum) |
| 86–88 | Boloor pp.141–143 — surface marking of lung and pleura; lower borders 6/8/10 vs 8/10/12 |
| 91–92 | Boloor pp.146, 151 — chest wall, Trail's sign, tracheal palpation, Oliver's and Campbell's signs |
| 117–118 | Boloor pp.304–305 — direction of venous flow; milking technique |
| 121–123 | Boloor pp.281–283 — liver palpation: preferred, hooking, dipping; liver span |
| 127–131 | Boloor pp.288–293 — spleen: Hackett's grading, bimanual and hooking, Castell's sign, Traube's space |
| 134–135 | AASLD/EASL 2014 West Haven criteria table |
| 136–137 | Hepatic encephalopathy — why each precipitant works |
| 138 | Niharika's notes — abdomen additions (portal hypertension table, Child-Pugh, Maddrey, MELD, DSM-V) |
| 148 | Niharika's notes — leukaemia additions (CML, CLL, bone marrow) |
| 159 | Alcohol addendum — unit vs US standard drink, binge definitions, cirrhotic dose |
| 161 | Myeloma addendum — current first-line therapy to July 2026 |
| 191–192 | Boloor pp.454–455 — subtle hemiparesis: pronator drift, forearm rolling, tapping tests |
| 209–211 | 2026 AHA/ASA acute ischaemic stroke guideline addendum |
| 222–223 | Niharika's notes — CNS and stroke additions |
| 240–241 | Micturition figure supplied by the user (Fowler, Griffiths & de Groat) + three-lesion rule |
| 243 | Niharika's notes — paraplegia additions |
| 244–248 | Harrison's 21e Chapter 239 (pp.1816–1819) — JVP, arterial pulse, blood pressure |

## Image-only pages (no text layer or < 400 characters)

These pages must be read from a render (`tools/render_audit.py N N 2.2`), never
from extracted text: **10, 11, 12, 15, 18, 19, 48, 49, 56, 59, 62, 69, 73, 74,
79, 84, 87, 90, 118, 123, 131, 152, 153, 157, 163, 164, 171, 172, 177, 181, 192,
193, 206, 221, 244, 249**.

Notable ones already read and identified while building Chapters 1–6:
p15 AHA/ASA Blood Pressure Categories chart (end of Chapter 1, Book p3–15);
p18–19 Boloor Table 3C.7 orthopnoea vs PND (Chapter 2, Book p16–30);
p48 7-point Approach to Cardiovascular Diagnosis (Chapter 5, Book p48, 73–74);
p49 Harrison's Table 263-1 & rheumatic mitral stenosis pathology (Chapter 6, Book p49–55);
p73 circular 0.8 s cardiac cycle diagram & p74 Wiggers cardiac-cycle diagram (Chapter 5, Book p48, 73–74);
p79 NCPF/EHPVO/cirrhosis differentiation table; p163 Kumar &
Clark Table 19.8 (acute breathlessness); p164 MMSE form; p177 Waldeyer's
lymphatic rings; p206 (stroke figure page, to be read with Chapter 40).

## Chapter start pages (roadmap)

Chapters 1–6 are verified line by line. The remaining start pages come from the
12.4 pt+ heading scan (`tools/heading_scan.py`) and are confirmed chapter by
chapter as each one is built; `build_content.py` holds the same table.

| Ch | Start | Ch | Start | Ch | Start |
|---:|---:|---:|---:|---:|---:|
| 1 General Examination | 3 | 18 RS Consolidation → cavity | 108 | 35 Neck & neurocutaneous | 171 |
| 2 CVS history | 16 | 19 RS Pleural effusion | 110 | 36 Higher mental & cranial nerves | 174 |
| 3 CVS inspection/JVP | 31 | 20 Abdomen history/ascites | 112 | 37 Motor system | 187 |
| 4 CVS palpation/auscultation | 37 | 21 Venous flow & liver | 117 | 38 Plantar response | 193 |
| 5 CVS diagnosis/cardiac cycle | 48 | 22 Spleen | 125 | 39 Cerebellum/sensory | 198 |
| 6 Mitral stenosis | 49 | 23 Hepatic encephalopathy | 132 | 40 Stroke theory | 204 |
| 7 Mitral regurgitation | 56 | 24 Portal hypertension | 138 | 41 Stroke 2026 update | 209 |
| 8 Aortic stenosis | 58 | 25 Ascites complications | 141 | 42 Capsule & arteries | 212 |
| 9 Aortic regurgitation | 62 | 26 Leukaemias | 144 | 43 Brainstem strokes | 217 |
| 10 Congenital heart disease | 64 | 27 Polycythemia/fever | 149 | 44 CNS & stroke additions | 222 |
| 11 Rheumatic fever | 65 | 28 Portal hypertension II | 152 | 45 Paraplegia approach | 224 |
| 12 Infective endocarditis | 69 | 29 Acute liver failure | 154 | 46 Conus/SACD/GBS | 234 |
| 13 RS history | 75 | 30 Alcohol | 156 | 47 Bladder & micturition | 239 |
| 14 RS chest wall | 80 | 31 Chemotherapy protocols | 160 | 48 Chronic myelopathies | 242 |
| 15 RS percussion | 93 | 32 Abdominal mass | 162 | 49 Paraplegia additions | 243 |
| 16 RS auscultation | 98 | 33 MMSE | 164 | 50 Harrison's appendix | 244 |
| 17 RS clubbing/TB | 105 | 34 Stroke history | 165 | 51 Extras (pointer) | 249 |
