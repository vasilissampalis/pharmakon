# Second reading: targeted anchor checks, part a of the 18 October PDF anchors (AI reader 59, 2026-10-18)

You are a second reader for Pharmakon, an evidence library of psychoactive drugs (project: `/home/claude/drug-encyclopedia`). AI readers 51, 52, 54, 55 and 56 wrote the 81 evidence anchors in your task file (MDMA's effects on the body, pills, dependence, medicines and serotonin toxicity, and mixing). You wrote none of them. Check each one at the place it cites.

**Tasks:** `data/verification/targeted-2026-10-18o/tasks_a.json`. Each task has `n`, `claim_id`, `anchor_index`, `reference`, `page`, `locator`, `source_read`, `extracted`, `role` and `quote`.

## Sources

**PDFs**, in `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/`:

| reference | file (under /mnt/user-data/uploads/DrugEncyclopedia/) | page basis |
|---|---|---|
| campbell_2008 | PDFs/MDMA/Campbell_2008_AgonyOfEcstasyKidney.pdf | journal page numbers |
| degenhardt_2010 | PDFs/MDMA/Degenhardt_2010_EcstasyDependence.pdf | journal page numbers |
| droogmans_2007 | PDFs/MDMA/Droogmans_2007_ValvularHeartDisease.pdf | journal page numbers |
| hartung_2002 | PDFs/MDMA/Hartung_2002_HyponatraemicStates.pdf | journal page numbers |
| parrott_2004 | PDFs/MDMA/Parrott_2004_IsEcstasyMDMA.pdf | journal page numbers |
| parrott_2012 | PDFs/MDMA/Parrott_2012_MDMAAndTemperature.pdf | journal page numbers |
| pilgrim_2011 | PDFs/MDMA/Pilgrim_2011_MDMADeathsPharmaceuticals.pdf | journal page numbers |
| rosenson_2007 | PDFs/MDMA/Rosenson_2007_HyponatremiaCalifornia.pdf | journal page numbers |
| vizeli_2017 | PDFs/MDMA/Vizeli_2017_SafetyPharmacologyAcute.pdf | journal page numbers |

Accepted manuscripts (dubois_2015, galicia_2019) are cited by section and paragraph.

- `page` is the journal's printed page number.
- Extract a page's text with `pdftotext -layout -f N -l N`. To find PDF page N from a printed page, compare with the PDF's first printed page.
- Render tables and figures (`pdftoppm -r 150 -f N -l N -png`) and look at them.

Do not open the first readers' files (`scratchpad/batch5/reader5*`), or `data/claims/`.

## For each task

1. **Check every detail of `extracted` at the source:** every number, name, arm, denominator, interval, P value and adjustment. Recompute any "editors' calculation". Check that the `role` fits. If there is a `quote`, check it is word for word.
2. **Give one verdict:**
   - `confirmed`.
   - `corrected`: change only what is wrong and keep the rest of the wording. Give `corrected_extracted` and, if needed, `corrected_page` and/or `corrected_locator`.
   - `wrong-location`: the content is right but the place is wrong. Give the right place.
   - `not-found`: say where you looked.
3. **Write one short note** (at most 40 words).

## Output

`data/verification/targeted-2026-10-18o/out_reader59.json`:

```json
{"reader": "AI reader 59 (second reader)", "date": "2026-10-18", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Write the file as you go.

## Rules

- **Be economical:** read only the cited pages and sections, and fetch each source once.
- **Never change any project file except your output.**
- **Quotations:** at most 15 words.
- **Doses:** no dosing advice of any kind. Doses may be named only as study conditions.
- **Safety filter:** if an automatic safety filter stops a response, do not retry or reword that content. Skip it and say so in the note.
- **Final message** (under 150 words): how many tasks were confirmed, corrected, wrong-location and not-found, and the corrections that change a number.

- pdftotext can drop minus signs: check every negative number on the rendered page.
- The task file's `page` values follow the page basis in the table.
