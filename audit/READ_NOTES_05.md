# Read notes — Chapter 5, CVS - Approach to Diagnosis & the Cardiac Cycle (Book p48, 73-74)

**Method.** Book p48 (the 7-point Approach to Cardiovascular Diagnosis with its worked clinical example A–G) and the companion Cardiac Cycle pages (Book p73 circular 0.8-second timing diagram and Book p74 Wiggers diagram of simultaneous aortic/LA/LV pressures, LV volume, ECG and phonocardiogram across phases a–g) were rendered at 2× into `.audit-render/book_048.png`, `book_073.png` and `book_074.png` and read line by line.

## Unit and question inventory

| Unit | Section | Book page(s) | Questions | Formats |
|---:|---|---|---:|---|
| 1 | Approach to Cardiovascular Diagnosis (7-Point Format) | 48 | 6 | match 2, recall 1, fillup 1, scenario 1, oddoneout 1 |
| 2 | The Cardiac Cycle: Atrial & Ventricular Timing (0.8 s) | 73 | 3 | numeric 1, match 1, truefalse 1 |
| 3 | Wiggers Diagram: Pressures, Volumes, Valves, ECG & Sounds | 74 | 5 | match 2, numeric 1, scenario 1, management 1 |

**Chapter 5 total:** 14 questions across 3 units, covering Book p48, 73-74 with no page omitted.

## Point → question map (audit/coverage.json)


**Book p48**

- Ordered 7-point template for a complete cardiovascular diagnosis on Book p48 → `MED-C5-01`
- Mapping parts A–D of the worked clinical example on Book p48 to headings 1–4 → `MED-C5-02`
- Mapping parts D–G of the worked clinical example on Book p48 to headings 4–7 → `MED-C5-03`
- Structural lesion (B) and precipitating factor (G) in the Book p48 model diagnosis → `MED-C5-04`
- Distinguishing Complications (3) from Precipitating Factor (7) and Functional status (5) when presenting a CVS case → `MED-C5-05`
- Identifying the seven required headings of the Book p48 diagnosis format → `MED-C5-06`

**Book p73**

- Total cardiac cycle duration (0.8 s) and atrial vs ventricular systole/diastole durations on Book p73 → `MED-C5-07`
- Ordered phases of Ventricular Systole (0.3 s) and Ventricular Diastole (0.5 s) in the circular diagram on Book p73 → `MED-C5-08`
- Overlap between Atrial Diastole (0.7 s) and Ventricular Systole/Diastole on Book p73 → `MED-C5-09`

**Book p74**

- Seven labelled phases (a to g) of the Wiggers diagram on Book p74 → `MED-C5-10`
- Four valve opening/closing crossover points on the Wiggers pressure curves (Book p74) → `MED-C5-11`
- Pressure and ventricular volume values plotted on the Wiggers diagram on Book p74 → `MED-C5-12`
- Aligning the Left Atrial a, c, v waves, ECG (P, QRS, T) and Phonocardiogram (1st, 2nd, 3rd, 4th heart sounds) on Book p74 → `MED-C5-13`
- Using the Wiggers diagram (Book p74) to time bedside auscultatory events and constant-volume phases → `MED-C5-14`

**Unasked points after this review:** NONE in the recorded inventory. Every listed point resolves to exactly one question, and the ledger order equals the question array order (enforced by `validate_content.py`).
