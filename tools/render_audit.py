#!/usr/bin/env python3
"""Render annotated-notes pages to PNG for line-by-line review.

Usage:
    python3 tools/render_audit.py 3 14            # Book p3-14 at 2x into .audit-render/
    python3 tools/render_audit.py 95 95 3         # single page at 3x
"""
from __future__ import annotations

import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".audit-render"
SPLIT = 120  # Book p1-120 live in uploads/part_1.pdf; later pages in part_2.pdf


def sheet_path(book_page: int):
    if book_page <= SPLIT:
        return ROOT / "uploads" / "part_1.pdf", book_page - 1
    return ROOT / "uploads" / "part_2.pdf", book_page - SPLIT - 1


def main() -> None:
    first, last = int(sys.argv[1]), int(sys.argv[2])
    zoom = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
    OUT.mkdir(exist_ok=True)
    docs = {}
    for page in range(first, last + 1):
        path, index = sheet_path(page)
        docs.setdefault(path, pymupdf.open(path))
        pix = docs[path][index].get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
        target = OUT / f"book_{page:03d}.png"
        pix.save(target)
        print(f"Book p{page} -> {target.relative_to(ROOT)} ({pix.width}x{pix.height})")


if __name__ == "__main__":
    main()
