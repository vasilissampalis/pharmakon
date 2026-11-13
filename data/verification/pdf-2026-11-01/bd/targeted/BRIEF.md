# Targeted checks, before-and-during round (`pdf-2026-11-01/bd`), 1 November 2026

The blind reconciliation has run on the sources read so far. Of the claim writers' anchors from your sources, most
matched your blind extractions; those that did not, usually because they cite a different paragraph, table or figure,
or a secondary point, you now check at the place they name (METHODS §5.5: a targeted check, labelled "checked at the
stated place" on the site). You did not write these anchors; the claim writers (AI readers 320 and 321) did.

Your tasks: `data/verification/pdf-2026-11-01/bd/targeted/tasks_reader<N>.json` (N = your reader number). Each gives the
claim id, the anchor index, the reference, page, locator, source read, the anchor's `extracted` text and its role.

## For each task

1. Check every detail of `extracted` at the source: numbers, groups and their sizes, who took part and where, the
   conditions as the study gave them, which questionnaire was rated when and by whom, the comparison, adjustment,
   intervals, and any quote word for word. Recompute any count, percentage or editors' calculation. Check that the role fits.
2. Give one verdict: `confirmed`, `corrected` (change only what is wrong; give `corrected_extracted` and, if needed,
   `corrected_page` and `corrected_locator`), `wrong-location` (give the right place) or `not-found` (say where you
   looked).
3. One short note (at most 40 words). Say in the note when the anchor's wording overstates the source ("involved",
   "present" or "detected" as "caused", a model estimate as a count, a case series as a rate, a review's citation as its
   own finding, a self-selected sample as representative, a recalled attribution as a predictor). Flag anything that reads as
   advice on amounts, timing, routes or combinations.

## Sources and context

PDF readers: the same PDFs you read in the blind round, with your own extracted texts and rendered pages in your folder
under `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/pdf1101/s<N>/`. Check every table and
figure value on a rendered page. No browser is needed.

For context you may read the claims named in your tasks, and only those, in
`data/verification/pdf-2026-11-01/bd/targeted/claims_reader<N>.json`. Do not open `data/claims/` or any other reader's
files.

## Output

`data/verification/pdf-2026-11-01/bd/targeted/out_reader<N>.json`, written as you go:

```json
{"reader": "AI reader <N> (second reader)", "date": "2026-11-01", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Change no other file. Quotations at most 15 words. No advice on amounts, ways of using, timing or combinations.
Independence: every anchor in this round was written by the claim writers before your blind reading. Finding the same
thing in your blind round is agreement, not authorship; mark `"independent": "no"` only if an anchor's wording was
copied from your own output.

Final message under 150 words: counts by verdict, and every correction that changes a number.
