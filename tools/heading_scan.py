#!/usr/bin/env python3
"""Print the heading skeleton of the annotated notes (Book p1-249).

Headings are lines whose maximum font size is at least the page's body size and
at least 12.4 pt (the notes use 11 pt body, 12-14 pt section headings and 17-20 pt
topic titles). Underlined key lines are recovered separately from PDF drawings.

Usage: python3 tools/heading_scan.py [first_book_page] [last_book_page] [min_pt]
"""
from __future__ import annotations

import sys

import pymupdf

ROOT_PATH = __file__
import pathlib  # noqa: E402

ROOT = pathlib.Path(ROOT_PATH).resolve().parents[1]
SPLIT = 120


def main() -> None:
    first = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    last = int(sys.argv[2]) if len(sys.argv) > 2 else 249
    min_pt = float(sys.argv[3]) if len(sys.argv) > 3 else 12.4
    docs = {
        "part_1": pymupdf.open(ROOT / "uploads" / "part_1.pdf"),
        "part_2": pymupdf.open(ROOT / "uploads" / "part_2.pdf"),
    }
    for page in range(first, last + 1):
        name = "part_1" if page <= SPLIT else "part_2"
        index = page - 1 if page <= SPLIT else page - SPLIT - 1
        doc = docs[name]
        found = []
        for block in doc[index].get_text("dict")["blocks"]:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                text = "".join(span["text"] for span in line["spans"]).strip()
                if not text or len(text) > 90:
                    continue
                size = max(span["size"] for span in line["spans"])
                if size >= min_pt:
                    found.append(f"[{size:.1f}] {text}")
        if found:
            print(f"--- Book p{page}")
            for line in found:
                print("   ", line)


if __name__ == "__main__":
    main()
