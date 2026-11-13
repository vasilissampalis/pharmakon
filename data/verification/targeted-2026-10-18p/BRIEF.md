# Second reading: targeted anchor checks, opioids, cocaine and alcohol (AI reader 61, 2026-10-18)

You are a second reader for Pharmakon, an evidence library of psychoactive drugs (project: `/home/claude/drug-encyclopedia`). AI reader 57 wrote the 33 evidence anchors in your task file (opioids with benzodiazepines, gabapentinoids or alcohol; cocaine with alcohol; lower tolerance after a break). You wrote none of them. Check each one at the place it cites.

**Tasks:** `data/verification/targeted-2026-10-18p/tasks.json`. Each task has `n`, `claim_id`, `anchor_index`, `reference`, `page`, `locator`, `source_read`, `extracted`, `role` and `quote`.

## Sources

**PDFs**, in `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/`:

| reference | file (under /mnt/user-data/uploads/DrugEncyclopedia/) | page basis |
|---|---|---|
| dasgupta_2016 | PDFs/_Cross-cutting/Dasgupta_2016_HighDoseOpioidOverdoseMortalityCohort.pdf | journal page numbers |
| gomes_2018 | PDFs/_Cross-cutting/Gomes_2018_PregabalinOpioidDeath.pdf | printed first page of PDF: 1 |
| hickman_2008 | PDFs/_Cross-cutting/Hickman_2008_AlcoholOverdoseDeathTranslational.pdf | journal page numbers |
| jones_2015 | PDFs/_Cross-cutting/Jones_2015_OpioidBenzodiazepineEDVisitsDeaths.pdf | journal page numbers |
| mccance-katz_1998 | PDFs/_Cross-cutting/McCanceKatz_1998_CocaineAlcoholMultipleDose.pdf | journal page numbers |
| pennings_2002 | PDFs/_Cross-cutting/Pennings_2002_AlcoholCocaineConcurrent.pdf | journal page numbers |
| white_1999 | PDFs/_Cross-cutting/White_1999_MechanismsFatalOpioidOverdose.pdf | journal page numbers |

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

`data/verification/targeted-2026-10-18p/out_reader61.json`:

```json
{"reader": "AI reader 61 (second reader)", "date": "2026-10-18", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
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
