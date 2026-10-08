# PULSE · Aneesh Notes

A single-file, offline quiz built line by line from the annotated clinical notes in
`uploads/` (Book p1–249). **Live: https://deva20045.github.io/Aneesh/**

- `pulse-aneesh.html` — the whole app (open it directly, works offline).
- `index.html` — redirect to the app (GitHub Pages entry point).
- `data/chNN.json` — editable chapter artifacts (source of truth).
- `audit/` — page map, read records and the point → question ledger.
- `PROGRESS.md` — single source of truth: goal, page-offset formula, schema,
  per-chapter pipeline, chapter status (DONE / NEXT / Soon) and the live link.

```bash
python3 validate_content.py --ledger   # gate: schema, order, inventory, app parsers
python3 build_content.py               # embed data/chNN.json into the app
python3 validate_content.py --embedded # require exact data/HTML agreement
python3 -m http.server 8000            # local preview
```

Book page = PDF sheet number in `uploads/part_1.pdf` (p1–120); book page = PDF
sheet + 120 in `uploads/part_2.pdf` (p121–249). See `audit/PAGE_MAP.md`.
