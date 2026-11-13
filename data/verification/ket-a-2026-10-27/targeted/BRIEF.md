# Targeted checks, Ketamine round (ket-a-2026-10-27), 30 October 2026

The blind reconciliation matched 73 of the claim writers' 117 anchors from your sources to your blind extractions. The
other 44 were not matched, usually because they cite a different paragraph, table or figure, or a secondary point. You
now check each of these at the place it names (METHODS §5.5: a targeted check, labelled "checked at the stated place" on
the site). You did not write these anchors; the claim writers (AI readers 201, 202 and 220) did.

Your tasks: `data/verification/ket-a-2026-10-27/targeted/tasks_reader<N>.json` (N = your reader number). Each gives the
claim id, the anchor index, the reference, page, locator, source read, the anchor's `extracted` text and its role.

## For each task

1. Check every detail of `extracted` at the source: numbers, units, groups and their sizes, the comparison group, the
   route, preparation and dose as the study's condition, when it was measured (during the session, hours later, after
   days without use), intervals, P values, and any quote word for word. Recompute any count, percentage, conversion or
   editors' calculation. Check that the role fits.
2. Give one verdict: `confirmed`, `corrected` (change only what is wrong; give `corrected_extracted` and, if needed,
   `corrected_page` and `corrected_locator`), `wrong-location` (give the right place) or `not-found` (say where you
   looked).
3. One short note (at most 40 words). Say in the note when the anchor's wording overstates the source (an association as
   an effect, one small sample as general, a review's citation as its own finding, a laboratory or animal finding as
   shown in people), or mixes up volunteers, patients and people who use ketamine outside a laboratory.

## Sources

The same PDFs you read in the blind round (`/mnt/user-data/uploads/DrugEncyclopedia/` + `source_read`), with your own
extracted texts and rendered pages in `scratchpad/ket-a/s<N>/` under
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/`. Check every table and figure value on a rendered
page; the old scanned papers' machine-read text has errors. No browser is needed.

## Output

`data/verification/ket-a-2026-10-27/targeted/out_reader<N>.json`, written as you go:

```json
{"reader": "AI reader <N> (second reader)", "date": "2026-10-30", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Rules as in your first brief, except that you may now read the claim named in each task in
`data/claims/_incoming/ket_joined.json` for context. Change no other file. Quotations at most 15 words. No advice on
amounts, routes, timing or combinations. Independence: every anchor in this round was written by the claim writers before
your blind reading. Finding the same thing in your blind round is agreement, not authorship; mark `"independent": "no"`
only if an anchor's wording was copied from your own output (corrected 30 October, after the first reader to finish).

Final message under 150 words: counts by verdict, and every correction that changes a number.
