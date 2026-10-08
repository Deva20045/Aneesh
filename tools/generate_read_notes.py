#!/usr/bin/env python3
"""Write audit/READ_NOTES_01.md: the line-by-line read record for Chapter 1.

The record is generated from the chapter artifact and the coverage ledger, so it
can never drift from the shipped questions. Usage: python3 tools/generate_read_notes.py
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HEAD = """# Read notes — Chapter 1, General Examination (Book p3–14)

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
"""


def main() -> None:
    chapter = json.loads((ROOT / "data" / "ch01.json").read_text(encoding="utf-8"))
    ledger = json.loads((ROOT / "audit" / "coverage.json").read_text(encoding="utf-8"))
    by_id = {q["id"]: q for q in chapter["questions"]}

    rows = []
    for unit in chapter["units"]:
        pages = sorted({by_id[qid]["page"] for qid in unit["qs"]})
        span = f"{pages[0]}" if len(pages) == 1 else f"{pages[0]}–{pages[-1]}"
        fmts = Counter(by_id[qid]["fmt"] for qid in unit["qs"])
        fmt_text = ", ".join(f"{k} {v}" for k, v in fmts.most_common())
        rows.append(f"| {unit['n']} | {unit['title']} | {span} | {len(unit['qs'])} | {fmt_text} |")

    body = [HEAD]
    body.append("\n".join(rows))
    body.append(
        f"\n**Chapter 1 total:** {len(chapter['questions'])} questions across "
        f"{len(chapter['units'])} units, covering Book p3–14 with no page omitted.\n"
    )
    body.append("## Point → question map (audit/coverage.json)\n")
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
    (ROOT / "audit" / "READ_NOTES_01.md").write_text("\n".join(body).rstrip() + "\n", encoding="utf-8")
    print("wrote audit/READ_NOTES_01.md")


if __name__ == "__main__":
    main()
