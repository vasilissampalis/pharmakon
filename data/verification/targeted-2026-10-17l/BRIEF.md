# Batch 4 second reading: targeted anchor checks, MDMA therapy beyond PTSD (AI reader 48, 2026-10-17)

You are a second reader for Pharmakon, an evidence library of psychoactive drugs (project: `/home/claude/drug-encyclopedia`). AI readers 42 and 43 wrote 102 evidence anchors for twelve claims on MDMA-assisted therapy outside PTSD and on long-term follow-up. You wrote none of them. Check each one at the place it cites.

**Tasks:** `data/verification/targeted-2026-10-17l/tasks.json`. Each task has `n`, `claim_id`, `anchor_index`, `reference`, `page`, `locator`, `source_read`, `extracted`, `role` and `quote`.

## Sources

All sources are web pages, named in each task's `source_read`:

- **PubMed Central** articles: https://pmc.ncbi.nlm.nih.gov/articles/PMCxxxxxxx/
- **Registry records** on ClinicalTrials.gov (https://clinicaltrials.gov/study/NCTxxxxxxxx) and the EU Clinical Trials Register.
- **Three publisher pages:** Wiley (jts.70126, jts.23098) and Sage (10.1177/2050324518767442).

How to read them:
- Use the desktop app's built-in browser, in a tab you open yourself. Never touch, read or close a tab you did not open, and close yours when you are done.
- Read each source once with `get_page_text` and save the text to `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/reader48/`. Then work from that copy with grep, instead of fetching again.
- For a table that comes out garbled, take one screenshot of that table.
- Do not download anything, and do not open PDF links.
- If a page is blocked or will not load, mark its tasks `not-found` and say why. Do not retry the same URL more than once.

Do not open the first readers' folders (`scratchpad/mdma4/`), their reports, or `data/claims/`. The task file gives you everything you need.

## For each task

1. **Check every detail of `extracted` at the source:** every number, name, date, arm, denominator, interval and P value. Recompute any "editors' calculation". Check that the `role` fits: "supports", "qualifies" or "contradicts". If there is a `quote`, check it is word for word.
2. **Give one verdict:**
   - `confirmed`.
   - `corrected`: change only what is wrong and keep the rest of the wording. Give `corrected_extracted` and, if needed, `corrected_page` and/or `corrected_locator`.
   - `wrong-location`: the content is right but the place is wrong. Give the right place.
   - `not-found`: say where you looked.
3. **Write one short note** (at most 40 words) saying what you checked.

## Output

`data/verification/targeted-2026-10-17l/out_reader48.json`:

```json
{"reader": "AI reader 48 (second reader)", "date": "2026-10-17", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Write the file as you go (every 10 or so tasks), so that work is not lost.

## Rules

- **Be economical.** Group the tasks by source, so that each source is fetched once.
- **Never change any project file except your output.**
- **Quotations:** at most 15 words, copied exactly.
- **Doses:** no dosing advice of any kind. Dose levels may be named only as study conditions.
- **Safety filter:** if an automatic safety filter stops a response, do not retry or reword that content. Skip it and say so in the note.
- **Final message** (under 150 words): how many tasks were confirmed, corrected, wrong-location and not-found, and the corrections that change a number.
