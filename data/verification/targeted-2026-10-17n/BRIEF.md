# Second reading: targeted anchor checks, MDMA brain imaging and the 2002 retraction (AI reader 50, 2026-10-17)

You are a second reader for Pharmakon, an evidence library of psychoactive drugs (project: `/home/claude/drug-encyclopedia`). AI reader 45 wrote 39 evidence anchors on brain scans of serotonin transporters in people who use ecstasy, and on the retracted 2002 primate report and its retraction notice. You wrote none of them. Check each one at the place it cites.

**Tasks:** `data/verification/targeted-2026-10-17n/tasks.json`. Each task has `n`, `claim_id`, `anchor_index`, `reference`, `page`, `locator`, `source_read`, `extracted`, `role` and `quote`.

## Sources

**PDFs**, in `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/`:

| reference | file |
|---|---|
| reneman_2001 | MDMA/Reneman_2001_DoseSexAbstentionSERT.pdf (the Lancet prints decimals with a middle dot: 0·5 is 0.5) |
| mccann_2005 | MDMA/McCann_2005_QuantitativePETSERT.pdf |
| kish_2010 | MDMA/Kish_2010_SERTBindingPET.pdf |
| de-win_2008 | MDMA/deWin_2008_ProspectiveNeuroimagingNovelUsers.pdf |
| erritzoe_2011 | MDMA/Erritzoe_2011_SERT5HT2AImaging.pdf |
| selvaraj_2009 | MDMA/Selvaraj_2009_SERTFormerUsers.pdf |
| schilt_2007 | MDMA/Schilt_2007_NoviceUsersProspective.pdf |
| ricaurte_2002 | MDMA/Ricaurte_2002_PrimateStudyRetracted.pdf (retracted; it is cited only as a record of what was claimed) |
| ricaurte_2003 | MDMA/Ricaurte_2003_RetractionNotice.pdf |

- `page` is the journal's printed page number.
- Extract a page's text with `pdftotext -layout -f N -l N`. To find PDF page N from a printed page, compare with the PDF's first printed page.
- Render tables and figures (`pdftoppm -r 150 -f N -l N -png`) and look at them.

**PubMed Central** articles (urban_2012, vegting_2016) are at https://pmc.ncbi.nlm.nih.gov/articles/PMCxxxxxxx/, with the number given in `source_read`.
- Use the desktop app's built-in browser. Open your own tab with `tabs_create` (not `preview_start`, which can hand back another reader's tab), check with `tabs_context` that it is yours, then use `navigate` and `get_page_text` with that tabId only.
- **Pass your own tabId on every browser call.** A call without tabId acts on whatever tab is in front, which may be another reader's or the user's.
- Read each article once with `get_page_text` and save the text to `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader50/`; it stops at 50,000 characters, so read the rest with `javascript_tool` on the same tab. Work from that copy.
- Close your tab when you are done. Never touch any other tab.
- No downloads, no PDF links.

Do not open the first reader's files (`scratchpad/batch5/reader45*`), or `data/claims/`.

## For each task

1. **Check every detail of `extracted` at the source:** every number, name, arm, denominator, interval, P value and adjustment. Recompute any "editors' calculation". Check that the `role` fits. If there is a `quote`, check it is word for word.
2. **Give one verdict:**
   - `confirmed`.
   - `corrected`: change only what is wrong and keep the rest of the wording. Give `corrected_extracted` and, if needed, `corrected_page` and/or `corrected_locator`.
   - `wrong-location`: the content is right but the place is wrong. Give the right place.
   - `not-found`: say where you looked.
3. **Write one short note** (at most 40 words).

## Output

`data/verification/targeted-2026-10-17n/out_reader50.json`:

```json
{"reader": "AI reader 50 (second reader)", "date": "2026-10-17", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Write the file as you go.

## Rules

- **Be economical:** read only the cited pages and sections, and fetch each source once.
- **Never change any project file except your output.**
- **Quotations:** at most 15 words.
- **Doses:** no dosing advice of any kind. Doses may be named only as study conditions.
- **Safety filter:** if an automatic safety filter stops a response, do not retry or reword that content. Skip it and say so in the note.
- **Final message** (under 150 words): how many tasks were confirmed, corrected, wrong-location and not-found, and the corrections that change a number.
