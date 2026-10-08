#!/usr/bin/env python3
"""Fail-closed content gate: schema, sequence, coverage inventory and app parsers.

The ledger in audit/coverage.json records one source point per question, in book
order. Software verifies referential integrity and ordering; the human review of
each point against the rendered page is recorded in PROGRESS.md.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
FORMATS = {"recall", "fillup", "match", "truefalse", "scenario", "oddoneout", "numeric", "management"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parse_page_range(page_range: str) -> list[int]:
    require(bool(re.fullmatch(r"\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*", page_range)), f"invalid pageRange syntax: {page_range!r}")
    out: list[int] = []
    for part in page_range.split(","):
        part = part.strip()
        if "-" in part:
            a, b = map(int, part.split("-", 1))
            require(b >= a, f"invalid page span {part!r} in {page_range!r}")
            span = list(range(a, b + 1))
        else:
            span = [int(part)]
        if out:
            require(span[0] > out[-1], f"non-increasing page spans in {page_range!r}")
        out.extend(span)
    return out


def validate_chapter(chapter, number, title, start_page):
    label = f"ch{number:02d}"
    require(chapter["chapter"] == number, f"{label}: chapter number")
    require(chapter["title"] == title, f"{label}: title")
    expected_pages = parse_page_range(chapter["pageRange"])
    expected_set = set(expected_pages)
    require(expected_pages[0] == start_page, f"{label}: pageRange start/end")
    questions = chapter["questions"]
    require(bool(questions), f"{label}: no questions")
    ids = []
    pages = []
    for seq, q in enumerate(questions, 1):
        qid = f"MED-C{number}-{seq:02d}"
        require(q["id"] == qid, f"{label}: sequential id {qid}")
        require(q["fmt"] in FORMATS, f"{qid}: format")
        for key in ("sec", "q", "exp"):
            require(isinstance(q[key], str) and q[key].strip(), f"{qid}: empty {key}")
        require(type(q["page"]) is int and q["page"] in expected_set, f"{qid}: page range")
        require(isinstance(q["opts"], list) and len(q["opts"]) == 4, f"{qid}: exactly four options")
        require(all(isinstance(o, str) and o.strip() for o in q["opts"]), f"{qid}: empty option")
        require(len(set(q["opts"])) == 4, f"{qid}: duplicate options")
        require(type(q["ans"]) is int and 0 <= q["ans"] < 4, f"{qid}: answer range")
        require(q["exp"].endswith(f"(Book p{q['page']})"), f"{qid}: explanation page suffix")
        if q["fmt"] == "fillup":
            require("____" in q["q"], f"{qid}: missing fillup blank")
        if q["fmt"] == "truefalse":
            starts = Counter(
                re.match(r"^(True|False)\b", o).group(1) if re.match(r"^(True|False)\b", o) else "?"
                for o in q["opts"]
            )
            require(starts == {"True": 2, "False": 2}, f"{qid}: requires two True and two False options")
        require("None of the above" not in q["opts"], f"{qid}: 'None of the above' option")
        ids.append(qid)
        pages.append(q["page"])
    require(pages == sorted(pages), f"{label}: printed page order")
    require(set(pages) == expected_set, f"{label}: omitted page")
    units = chapter["units"]
    require(bool(units), f"{label}: no units")
    sections = []
    flat = []
    for n, unit in enumerate(units, 1):
        require(unit["id"] == f"MED-U{number}-{n}" and unit["ch"] == number and unit["n"] == n, f"{label}: unit identity")
        require(isinstance(unit["title"], str) and unit["title"].strip(), f"{label}: unit title")
        require(2 <= len(unit["guide"].splitlines()) <= 4, f"{unit['id']}: guide must have 2-4 lines")
        expected = [q["id"] for q in questions if q["sec"] == unit["sec"]]
        require(unit["qs"] == expected and bool(expected), f"{unit['id']}: qs must follow sec in array order")
        sections.append(unit["sec"])
        flat.extend(unit["qs"])
    require(len(set(sections)) == len(sections), f"{label}: duplicate unit section")
    require(flat == ids, f"{label}: unit coverage/order must equal full question array")


def validate_ledger(chapters, ledger):
    indexed = {q["id"]: q for c in chapters for q in c["questions"]}
    seen_points = set()
    covered = []
    for row in ledger:
        require(row["question"] in indexed, f"ledger: unknown {row['question']}")
        q = indexed[row["question"]]
        require(row["question"].startswith(f"MED-C{row['chapter']}-"), "ledger: chapter mismatch")
        require(row["page"] == q["page"], "ledger: page mismatch")
        require(bool(row["point"].strip()), "ledger: empty point")
        point = (row["chapter"], row["page"], row["point"])
        require(point not in seen_points, f"ledger: duplicate point {point}")
        seen_points.add(point)
        covered.append(row["question"])
    expected = [q["id"] for c in chapters for q in c["questions"]]
    require(covered == expected, "ledger: inventory book order and complete question coverage")


def validate_all(*, ledger_output=False, embedded=False):
    from build_content import CHAPTERS

    chapters = []
    for number, title, start in CHAPTERS:
        path = ROOT / "data" / f"ch{number:02d}.json"
        if path.exists():
            chapter = json.loads(path.read_text(encoding="utf-8"))
            validate_chapter(chapter, number, title, start)
            chapters.append(chapter)
    ledger = json.loads((ROOT / "audit" / "coverage.json").read_text(encoding="utf-8"))
    validate_ledger(chapters, ledger)
    if ledger_output:
        page = None
        for row in ledger:
            if row["page"] != page:
                page = row["page"]
                print(f"\nBook p{page}")
            print(f"  {row['point']} -> {row['question']}")
        print("\nUnasked points after line-by-line review: NONE in the recorded inventory.")
    # Execute the actual JavaScript parsers, avoiding Python/JS regex drift.
    subprocess.run(["node", str(ROOT / "tests" / "app_parsers.cjs")], check=True, cwd=ROOT)
    if embedded:
        html = (ROOT / "pulse-aneesh.html").read_text(encoding="utf-8")

        def constant(name, next_name):
            text = html.split(f"const {name} = ", 1)[1].split(f";\nconst {next_name} = ", 1)[0]
            return json.loads(text)

        require(constant("QUESTIONS", "UNITS") == [q for c in chapters for q in c["questions"]], "embedded question mismatch")
        require(constant("UNITS", "CHAPTERS") == [u for c in chapters for u in c["units"]], "embedded unit mismatch")
        roadmap = constant("CHAPTERS", "QBYID")
        live = {c["chapter"] for c in chapters}
        require(len(roadmap) == len(CHAPTERS), "roadmap length")
        for entry, (number, title, start) in zip(roadmap, CHAPTERS):
            require(entry == dict(n=number, t=title, p=start, live=number in live), f"roadmap entry {number}")
    for c in chapters:
        print(f"Ch{c['chapter']}: {len(c['questions'])} questions / {len(c['units'])} units; formats {dict(Counter(q['fmt'] for q in c['questions']))}")
    print(f"PASS: schema, book/unit order, {len(ledger)} inventoried points, full unit coverage" + (", embedded arrays/live flags" if embedded else ""))
    return chapters


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", action="store_true", help="Print every reviewed point -> question mapping before build")
    parser.add_argument("--embedded", action="store_true", help="Also require exact data/HTML agreement")
    args = parser.parse_args()
    validate_all(ledger_output=args.ledger, embedded=args.embedded)
