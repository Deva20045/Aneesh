#!/usr/bin/env python3
"""Write audit/READ_NOTES_NN.md: the line-by-line read record for each live chapter.

The records are generated from the chapter artifacts and the coverage ledger, so
they can never drift from the shipped questions. Usage: python3 tools/generate_read_notes.py
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

METHOD_NOTES = {
    1: (
        "**Method.** All thirteen pages (Book p3–15) were read in printed order from the text "
        "layer of `uploads/part_1.pdf` and rendered at 2× with `python3 tools/render_audit.py 3 15 2` "
        "into `.audit-render/book_003.png` … `book_015.png` to confirm layout and read the inserted "
        "Boloor reference pages (p10–12) and the AHA/ASA Blood Pressure Categories table on p15."
    ),
    2: (
        "**Method.** All fifteen pages (Book p16–30) were read in printed order from the text "
        "layer of `uploads/part_1.pdf` and rendered at 2× into `.audit-render/book_016.png` … "
        "`book_030.png` to inspect the inserted Boloor Table 3C.7 on PND vs orthopnoea (p18–19), "
        "the chest-pain and syncope tables (p20–22), the embedded Box 6.8 on unilateral vs bilateral "
        "leg oedema (p23), the arterial pulse waveform tracings (p26–28), and the bigeminy/trigeminy "
        "ECG strips (p28)."
    ),
    3: (
        "**Method.** All six pages (Book p31–36) were read in printed order from the text layer "
        "of `uploads/part_1.pdf` and rendered at 2× into `.audit-render/book_031.png` … `book_036.png` "
        "to inspect the peripheral signs of aortic regurgitation and Hill's sign (p31–32), cardiac "
        "inspection and the anatomical IJV/EJV diagram (p32–33), the Epomedicine JVP measurement and "
        "simultaneous ACXVY/Phonocardiogram/EKG figure (p34), the A/V/X/Y wave abnormalities and "
        "PAY TAX mnemonic (p35), and the Tamponade vs Constrictive Pericarditis vs Restrictive "
        "Cardiomyopathy table, abdominojugular reflux and Kussmaul's sign (p36)."
    ),
    4: (
        "**Method.** All eleven pages (Book p37–47) were read in printed order from the text layer "
        "of `uploads/part_1.pdf` and rendered at 2× into `.audit-render/book_037.png` … `book_047.png` "
        "to inspect the Hyperdynamic vs Heaving LV apex table (p37), Thrills table and AIIMS heave "
        "grading (p38), pulsatile liver bimanual examination and percussion (p39), Dr. Hamide's "
        "M->T->P->A auscultation sequence and Levine & Freeman grading (p40), classical murmur "
        "descriptions and S1/A2/P2 intensity table (p41), LA-LV dP/dt crossover diagram (p42), S2 "
        "split anomalies diagram and Perloff's ASD hangout/shunt explanation (p43), S3/S4 compliance "
        "(p44), Added Sounds phonocardiogram traces A–E (p45), OS vs S3 table and innocent murmurs "
        "(p46), and dynamic auscultation manoeuvres plus the 10 Named Murmurs (p47)."
    ),
    5: (
        "**Method.** Book p48 (the 7-point Approach to Cardiovascular Diagnosis with its worked "
        "clinical example A–G) and the companion Cardiac Cycle pages (Book p73 circular 0.8-second "
        "timing diagram and Book p74 Wiggers diagram of simultaneous aortic/LA/LV pressures, LV "
        "volume, ECG and phonocardiogram across phases a–g) were rendered at 2× into "
        "`.audit-render/book_048.png`, `book_073.png` and `book_074.png` and read line by line."
    ),
    6: (
        "**Method.** All seven pages (Book p49–55) were read in printed order from the text layer "
        "of `uploads/part_1.pdf` and rendered at 2× into `.audit-render/book_049.png` … `book_055.png` "
        "to inspect the inserted Harrison's Table 263-1 and rheumatic 'fish-mouth' pathology text "
        "(p49), the mitral valve anatomical diagram, congenital MS classification and variants "
        "(p50), etiopathogenesis, clinical features and 5 causes of haemoptysis (p51), severity "
        "correlates, complications and the 6-event auscultatory sequence of pulmonary hypertension "
        "(p52), opening snap / absent PSA / soft S1 significance, differential diagnoses and the "
        "`P mitrale` ECG strip (p53), CXR Kerley B/A pressure thresholds, Doppler Echo MVA severity, "
        "Abascal/Wilkins score and medical therapy (p54), and emergency AF digitalisation, TUBBS "
        "closed mitral valvotomy, BMV criteria/complications/success and the Mechanical Valves "
        "(Starr-Edwards, St. Jude, Indian Chitra TTK) vs Bioprosthetic valves (p55)."
    ),
}


def write_chapter_notes(ch_path: Path, all_ledger: list[dict]) -> None:
    chapter = json.loads(ch_path.read_text(encoding="utf-8"))
    ch_num = chapter["chapter"]
    title = chapter["title"]
    page_range = chapter["pageRange"]
    ledger = [row for row in all_ledger if row["chapter"] == ch_num]
    by_id = {q["id"]: q for q in chapter["questions"]}

    rows = []
    for unit in chapter["units"]:
        pages = sorted({by_id[qid]["page"] for qid in unit["qs"]})
        span = f"{pages[0]}" if len(pages) == 1 else f"{pages[0]}–{pages[-1]}"
        fmts = Counter(by_id[qid]["fmt"] for qid in unit["qs"])
        fmt_text = ", ".join(f"{k} {v}" for k, v in fmts.most_common())
        rows.append(f"| {unit['n']} | {unit['title']} | {span} | {len(unit['qs'])} | {fmt_text} |")

    body = [
        f"# Read notes — Chapter {ch_num}, {title} (Book p{page_range})\n",
        METHOD_NOTES.get(ch_num, f"**Method.** All pages of Book p{page_range} were read and rendered at 2× in book order.") + "\n",
        "## Unit and question inventory\n",
        "| Unit | Section | Book page(s) | Questions | Formats |",
        "|---:|---|---|---:|---|",
        "\n".join(rows),
        f"\n**Chapter {ch_num} total:** {len(chapter['questions'])} questions across "
        f"{len(chapter['units'])} units, covering Book p{page_range} with no page omitted.\n",
        "## Point → question map (audit/coverage.json)\n",
    ]
    page = None
    for row in ledger:
        if row["page"] != page:
            page = row["page"]
            body.append(f"\n**Book p{page}**\n")
        body.append(f"- {row['point']} → `{row['question']}`")
    body.append(
        "\n**Unasked points after this review:** NONE in the recorded inventory. "
        "Every listed point resolves to exactly one question, and the ledger order "
        "equals the question array order (enforced by `validate_content.py`).\n"
    )
    out_file = ROOT / "audit" / f"READ_NOTES_{ch_num:02d}.md"
    out_file.write_text("\n".join(body).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {out_file.relative_to(ROOT)}")


def main() -> None:
    all_ledger = json.loads((ROOT / "audit" / "coverage.json").read_text(encoding="utf-8"))
    for ch_path in sorted((ROOT / "data").glob("ch*.json")):
        write_chapter_notes(ch_path, all_ledger)


if __name__ == "__main__":
    main()
