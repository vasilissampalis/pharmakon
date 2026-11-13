# Batch 2b second reading: targeted anchor checks (AI reader 44, 2026-10-17)

You are a second reader for Pharmakon, an evidence library of psychoactive drugs (project: `/home/claude/drug-encyclopedia`). AI readers 39 and 40 (and, for one anchor, AI reader 38) wrote 94 evidence anchors for the MDMA-therapy claims. You wrote none of them. Check each one at the place it cites.

**Tasks:** `data/verification/targeted-2026-10-17k/tasks.json`. Each task has `n`, `claim_id`, `anchor_index`, `reference`, `page`, `locator`, `source_read`, `extracted`, `role` and `quote`.

## Sources

PDFs are in `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/MDMA/`:

| reference | file |
|---|---|
| fda_2024a | FDA_2024_BriefingDocument.pdf (FDA briefing document, 83 pp.) |
| fda_2024b | FDA_2024_BriefingErrata.pdf |
| fda_2024c | FDA_2024_AdvisoryMinutes.pdf |
| fda_2024d | FDA_2024_FinalQuestions.pdf |
| lykos_2024 | Lykos_2024_BriefingDocument.pdf (sponsor's briefing, 145 pp.; many pages are images without text) |
| mitchell_2021, mitchell_2023 | when `source_read` says "PDF supplement", use Mitchell_2021_MAPP1_Supplement.pdf or Mitchell_2023_MAPP2_Supplement.pdf |
| burke_2021 | Burke_2021_CautionPsychedelicFrontier.pdf |

- `page` is the document's printed page number. If the content is not there, look at the PDF page with that index and its neighbours, and report the right page.
- Extract the text yourself: `pdftotext -layout -f N -l N file.pdf -`.
- Render a page (`pdftoppm -r 110 -f N -l N -png file.pdf <prefix>`) and look at it when it is a table or figure, or when the page has no text layer.
- Work in `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader44/`.
- Do not open the first readers' folders (`scratchpad/mdma2/reader39`, `reader40`), their reports, or `data/claims/`. The task file gives you everything you need.

Three tasks (60, 89, 90) cite the trial articles' publisher HTML (the DOIs are in `source_read`). Read them in the desktop app's built-in browser, in a tab you create yourself. Read each article's text once with get_page_text, save it to your folder, and search that copy. Never touch, read or close a tab you did not open. Do not download anything and do not open PDF links. Close your tab when you are done.

## For each task

1. **Check every detail of `extracted` at the source:** every number, name, date, arm, denominator and P value. Recompute any "editors' calculation". Check that the `role` fits ("supports", "qualifies" and so on). If there is a `quote`, check it is word for word.
2. **Give one verdict:**
   - `confirmed`.
   - `corrected`: change only what is wrong and keep the rest of the wording. Give `corrected_extracted` and, if needed, `corrected_page` and/or `corrected_locator`.
   - `wrong-location`: the content is right but the place is wrong. Give the right place.
   - `not-found`: say where you looked.
3. **Write one short note** (at most 40 words) saying what you checked.

## Output

`data/verification/targeted-2026-10-17k/out_reader44.json`:

```json
{"reader": "AI reader 44 (second reader)", "date": "2026-10-17", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Write the file as you go (every 10 or so tasks), so that work is not lost.

## Rules

- **Be economical.** Read only the pages the tasks cite. Never extract or render a whole long document. Group the tasks by document and page so that each page is read once.
- **Never change any project file except your output.**
- **Quotations:** at most 15 words, copied exactly.
- **Doses:** no dosing advice of any kind. Dose levels may be named only as study conditions.
- **Safety filter:** if an automatic safety filter stops a response, do not retry or reword that content. Skip it and say so in the note.
- **Final message** (under 150 words): how many tasks were confirmed, corrected, wrong-location and not-found, and the corrections that change a number.
