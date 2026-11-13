# Round-2 checks: two new Di Forti et al. (2015) anchors (reader 322, 1 November 2026)

You are a new, independent AI reader for Pharmakon, an evidence library about drugs for the public and for people who
use drugs. You did not write these anchors and you took no part in this round. Project: `/home/claude/drug-encyclopedia`.
Scratch folder: `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/`; your own folder is
`scratchpad/can-a/c322/` (create it).

An adjudicator (AI reader 317) added two anchors from the PDF of Di Forti et al. (2015) to two cannabis claims. Each needs
a check by a reader who did not write it (METHODS §5.5: a targeted check, "checked at the stated place").

Your tasks: `data/verification/can-a-2026-10-27/targeted5/tasks_reader322.json`. Each gives the claim id, the anchor
index, the page, locator, the anchor's `extracted` text and its role.

## For each task

1. Find the stated place in the PDF and check every detail of `extracted`: numbers, groups and their sizes, the comparison
   group, the adjustment set, intervals, P values, and any quote word for word. Recompute every editors' calculation
   (an interval's centre, a P value implied by an estimate and its interval, an upper or lower limit implied by an estimate
   and its P value) and say whether you get the same. Check that the role fits.
2. Give one verdict: `confirmed`, `corrected` (change only what is wrong; give `corrected_extracted` and, if needed,
   `corrected_page` and `corrected_locator`), `wrong-location` (give the right place) or `not-found` (say where you
   looked).
3. One short note (at most 40 words).

## Source

`/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Cannabis/DiForti_2015_HighPotencyCaseControl.pdf` (version of record,
pp. 233–238). Extract the text yourself and check every number on the rendered page (`pdftoppm -r 150`; figures and
Tables 3–4 at `-r 300`). No browser is needed. For context you may read the two claims in `targeted5/claims_reader322.json`
and nothing else in `data/claims/`, the adjudicators' files or other readers' files.

## Output

`data/verification/can-a-2026-10-27/targeted5/out_reader322.json`:

```json
{"reader": "AI reader 322 (round-2 checker)", "date": "2026-11-01", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Change no other file. Quotations at most 15 words. Final message under 100 words: verdicts, and every correction that
changes a number.
