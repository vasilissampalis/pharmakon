# Targeted checks, drug checking round (dc-2026-10-26), 27 October 2026

The blind reconciliation matched 94 of the first readers' 131 anchors to your blind extractions. The other 37 were not
matched, usually because they cite a different paragraph, table or a secondary point. You now check each of these at the
place it names (METHODS §5.5: a targeted check, labelled "checked at the stated place" on the site). You did not write
these anchors; the first readers (AI readers 139, 140 and 141) did.

Your tasks: `data/verification/dc-2026-10-26/targeted/tasks_reader<N>.json` (N = your reader number). Each gives the
claim id, the anchor index, the reference, page, locator, source read, the anchor's `extracted` text and its role.

## For each task

Follow "For each task" in `data/verification/targeted-2026-10-18o/BRIEF_a.md`:
1. check every detail of `extracted` at the source (numbers, names, groups, denominators, intervals, P values,
   adjustment; recompute any editors' calculation; check the role fits, and any quote word for word);
2. give one verdict: `confirmed`, `corrected` (change only what is wrong; give `corrected_extracted` and, if needed,
   `corrected_page` and `corrected_locator`), `wrong-location` (give the right place) or `not-found` (say where you
   looked);
3. one short note (at most 40 words).

Also say in the note when the anchor's wording overstates the source in the ways your brief listed (laboratory results
as real-life accuracy, intended or self-reported behaviour as observed behaviour, association as effect, one brand or
lot as all strips).

## Sources

The same sources you read in the blind round, from the same places: the PDFs under
`/mnt/user-data/uploads/DrugEncyclopedia/` (paths in your task file's `source_read`), your own saved texts in
`scratchpad/ux1026/dc/s<N>/`, and, for web papers, the built-in browser in a tab of your own if it is available. If a web
page cannot be opened now (the app's browser may be offline), check against what you saved, and if that cannot settle
it, give the verdict `not-found` with the note "deferred: web source not reachable" so the editor can return to it.

## Output

`data/verification/dc-2026-10-26/targeted/out_reader<N>.json`, written as you go:

```json
{"reader": "AI reader <N> (second reader)", "date": "2026-10-27", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Rules as in your first brief (no other file changed, quotations at most 15 words, no dosing advice). Final message under
150 words: counts by verdict, and every correction that changes a number.
