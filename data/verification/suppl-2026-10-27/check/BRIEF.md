# Checks after the supplement reading (AI reader 153), 27 October 2026

Three supplement readers (AI readers 150, 151 and 152) read the supplementary files of Bhai et al. (2025), Kutscher et
al. (2024) and Vickers-Smith et al. (2025) and changed the drug-checking claims and cards
(`data/verification/suppl-2026-10-27/BRIEF.md` says what they were asked to do; their logs are `150_log.json`,
`151_log.json`, `152_log.json` in that folder). You wrote none of this. Following METHODS §5.5, you check each new or
changed anchor at the place it names, and two appraisal changes on the cards. Project: `/home/claude/drug-encyclopedia`;
scratch folder `scratchpad/ux1026/suppl/r153/` under `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/`.

## Part 1: 16 anchors

Your tasks: `data/verification/suppl-2026-10-27/check/tasks_reader153.json` (claim id, anchor index, reference, page,
locator, source read, the anchor's `extracted` text, its role, and what kind of change it was). The anchors are also in
`data/claims/drug-checking.json` at the index given. Follow "For each task" in
`data/verification/targeted-2026-10-18o/BRIEF_a.md`:
1. check every detail of `extracted` at the source: numbers, names, groups, denominators, intervals, reference numbers
   and the studies they point to; recompute any editors' calculation; check that the role fits and any quote is word
   for word;
2. give one verdict: `confirmed`, `corrected` (change only what is wrong; give `corrected_extracted` and, if needed,
   `corrected_page` and `corrected_locator`), `wrong-location` (give the right place) or `not-found` (say where you
   looked);
3. one short note (at most 40 words), and say when the wording overstates the source (laboratory results as real-life
   accuracy; intended or self-reported behaviour as observed behaviour; association as effect; one brand, lot,
   programme or state as all).

Sources (the senior author's files are under `/mnt/user-data/uploads/DrugEncyclopedia/`; text versions in
`scratchpad/ux1026/suppl/`):
- Bhai et al. (2025): `PDFs/_Cross-cutting/Bhai_2025_AppendixA.docx` (text `Bhai_2025_AppendixA.txt`), with the paper
  `PDFs/_Cross-cutting/Bhai_2025_FTSDrugMortality.pdf` and its corrigendum `PDFs/_Cross-cutting/Bhai_2026_Corrigendum..pdf`.
- Kutscher et al. (2024): `PDFs/_Cross-cutting/Kutscher_2024_Appendix1.docx` and `Kutscher_2024_Suppl1.docx` to
  `Suppl3.docx` (texts `Kutscher_2024_Appendix1.txt`, `Kutscher_2024_Suppl1.txt` to `Suppl3.txt`), with the author
  manuscript `PDFs/_Cross-cutting/Kutscher_2024_FTSScopingReview.pdf` ("AM p. N" = PDF page).
- Vickers-Smith et al. (2025): `PDFs/_Cross-cutting/VickersSmith_2025_Supplement.pdf` (texts
  `VickersSmith_2025_Supplement.txt` and `.plain.txt`; "supplement p. N" = PDF page). The article itself is a web
  source: use the second reader's saved texts `scratchpad/ux1026/dc/s147/vickers_smith_2025_page1.txt` and
  `scratchpad/vickers_page.txt`; if they cannot settle a point, you may open
  https://pmc.ncbi.nlm.nih.gov/articles/PMC12076174/ in the app's built-in browser (tools: `ToolSearch` query
  `mcp__remote-devices__Claude_Browser__`, `max_results` 64; one tab of your own via `preview_start`, its tabId on every
  call, `get_page_text`; never touch another tab, never a PDF or download link; close your tab at the end). If neither
  settles it, give `not-found` with the note "deferred: web source not reachable".
- Render a PDF page with `pdftoppm` when a table or figure matters; a .docx can be re-read with `pandoc -t plain`.

## Part 2: two appraisal changes

- `sc_kutscher_2024` (corrected copy: `data/study-cards/_incoming/drug-checking/sc_kutscher_2024.json`): reader 151 changed
  AMSTAR 2 items 7 and 8 from "no information" to "no" after reading the supplement, and set the card to first-pass.
  Judge items 7 and 8 yourself from the manuscript and the supplement, and say whether the overall confidence stays
  critically low.
- `sc_bhai_2025` (`data/study-cards/_incoming/drug-checking/sc_bhai_2025.json`): reader 150 made the ROBINS-I judgment for
  classification of interventions final (serious) using Appendix A. Check that every fact its note states is in the
  appendix or the paper, and give your own judgment for that domain.

## Output

`data/verification/suppl-2026-10-27/check/out_reader153.json`, written as you go:
`{"reader": "AI reader 153 (checker)", "date": "2026-10-27", "results": [{"n": 1, "claim_id": "...", "anchor_index": 8,
"verdict": "confirmed", "note": "..."}], "cards": [{"card": "sc_kutscher_2024", "item": "AMSTAR 2 items 7 and 8",
"your_judgment": "...", "agree": true, "note": "..."}, {...}]}`

Rules: change no other file; quotations at most 15 words; no dosing advice or instructions on how to test. Final
message under 150 words: counts by verdict, every correction that changes a number or a study named, and the two card
judgments.
