# Second reading: targeted anchor checks, tolerance and mixing (AI reader 49, 2026-10-17)

You are a second reader for Pharmakon, an evidence library of psychoactive drugs (project: `/home/claude/drug-encyclopedia`). AI readers 46 and 47 wrote 58 evidence anchors. You wrote none of them. Check each one at the place it cites. The anchors cover:
- tolerance to methamphetamine and to MDMA;
- methamphetamine with alcohol;
- opioids mixed with benzodiazepines, alcohol or gabapentinoids.

**Tasks:** `data/verification/targeted-2026-10-17m/tasks.json`. Each task has `n`, `claim_id`, `anchor_index`, `reference`, `page`, `locator`, `source_read`, `extracted`, `role` and `quote`.

## Sources

**PDFs**, in `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/`:

| reference | file |
|---|---|
| comer_2001 | Methamphetamine/Comer_2001_RepeatedOralMethamphetamine.pdf |
| perez-reyes_1991 | Methamphetamine/PerezReyes_1991_DailyMethamphetamineClinicalEffects.pdf |
| cook_1992 | Methamphetamine/Cook_1992_PKRepeatedDailyDosing.pdf |
| farre_2004 | MDMA/Farre_2004_RepeatedDosesPharmacology.pdf |
| peiro_2013 | MDMA/Peiro_2012_RepeatedDoses2hApart.pdf |
| parrott_2005 | MDMA/Parrott_2005_ChronicToleranceReview.pdf |

- `page` is the journal's printed page number.
- Extract a page's text with `pdftotext -layout -f N -l N`. To find PDF page N from a printed page, compare with the PDF's first printed page.
- Perez-Reyes has no text layer, and Cook's is poor:
  - render the cited page (`pdftoppm -r 150 -f N -l N -png`) and look at it;
  - you may run `tesseract` on the render to search it, but check every number on the image itself.
- Render tables and figures the same way.

**PubMed Central** articles (kirkpatrick_2012b, humbert-droz_2026, park_2015, sun_2017, tori_2020, gomes_2017, macleod_2019) are at https://pmc.ncbi.nlm.nih.gov/articles/PMCxxxxxxx/, with the number given in `source_read`.
- Use the desktop app's built-in browser, in a tab you open yourself.
- **Pass your own tabId on every browser call.** A call without tabId acts on whatever tab is in front, which may be another reader's or the user's.
- Read each article once with `get_page_text` and save the text to `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader49/`. Work from that copy.
- Close your tab when you are done. Never touch any other tab.
- No downloads, no PDF links.

Do not open the first readers' folders or reports (`scratchpad/batch5/reader46*`, `reader47*`), or `data/claims/`.

## For each task

1. **Check every detail of `extracted` at the source:** every number, name, arm, denominator, interval, P value and adjustment. Recompute any "editors' calculation". Check that the `role` fits. If there is a `quote`, check it is word for word.
2. **Give one verdict:**
   - `confirmed`.
   - `corrected`: change only what is wrong and keep the rest of the wording. Give `corrected_extracted` and, if needed, `corrected_page` and/or `corrected_locator`.
   - `wrong-location`: the content is right but the place is wrong. Give the right place.
   - `not-found`: say where you looked.
3. **Write one short note** (at most 40 words).

## Output

`data/verification/targeted-2026-10-17m/out_reader49.json`:

```json
{"reader": "AI reader 49 (second reader)", "date": "2026-10-17", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Write the file as you go.

## Rules

- **Be economical:** read only the cited pages and sections, and fetch each source once.
- **Never change any project file except your output.**
- **Quotations:** at most 15 words.
- **Doses:** no dosing advice of any kind. Doses may be named only as study conditions.
- **Safety filter:** if an automatic safety filter stops a response, do not retry or reword that content. Skip it and say so in the note.
- **Final message** (under 150 words): how many tasks were confirmed, corrected, wrong-location and not-found, and the corrections that change a number.
