# Targeted checks, Alcohol round (alc-a-2026-10-27), 27 October 2026

The blind reconciliation matched 179 of the claim writers' 271 anchors to your blind extractions. The other 92 were not
matched, usually because they cite a different paragraph, table or figure, or a secondary point. You now check each of
these at the place it names (METHODS §5.5: a targeted check, labelled "checked at the stated place" on the site). You
did not write these anchors; the claim writers (AI readers 170 to 174) did.

Your tasks: `data/verification/alc-a-2026-10-27/targeted/tasks_reader<N>.json` (N = your reader number). Each gives the
claim id, the anchor index, the reference, page, locator, source read, the anchor's `extracted` text and its role.

## For each task

1. Check every detail of `extracted` at the source: numbers, names, groups, reference groups (lifetime abstainers,
   current non-drinkers, the lowest-intake drinkers), units (grams a day or a week, the paper's drink), denominators,
   intervals, P values, adjustment; recompute any editors' calculation; check that the role fits, and any quote word for
   word.
2. Give one verdict: `confirmed`, `corrected` (change only what is wrong; give `corrected_extracted` and, if needed,
   `corrected_page` and `corrected_locator`), `wrong-location` (give the right place) or `not-found` (say where you
   looked).
3. One short note (at most 40 words). Say in the note when the anchor's wording overstates the source (association as
   effect, a model estimate as a count, a subgroup as everyone, a review's citation as its own finding).

## Sources

The same sources you read in the blind round, from the same places: the PDFs under
`/mnt/user-data/uploads/DrugEncyclopedia/` (paths in your task file's `source_read`) and your own saved texts in
`scratchpad/alc-a/s<N>/` under `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/`. For a web paper,
check against what you saved first; if that cannot settle a point, open the page again in a tab of your own (made with
`tabs_create`, its tabId on every call, closed at the end; never touch another tab). If the page cannot be opened, give
`not-found` with the note "deferred: web source not reachable" so the editor can return to it.

## Output

`data/verification/alc-a-2026-10-27/targeted/out_reader<N>.json`, written as you go:

```json
{"reader": "AI reader <N> (second reader)", "date": "2026-10-27", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Rules as in your first brief (no other file changed; you may now read the claim named in each task in
`data/claims/alcohol.json` for context; quotations at most 15 words; no advice on amounts of drinking or on medicines).
Final message under 150 words: counts by verdict, and every correction that changes a number.
