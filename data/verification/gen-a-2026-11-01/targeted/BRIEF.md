# Targeted checks, round gen-a-2026-11-01 (general facts about drug use), 1 November 2026

The blind reconciliation has run (`../report.md`): 65 of the claim writer's 82 anchors matched
your blind extractions and are now ai-checked. The 17 that did not, usually because they cite a different paragraph,
table or figure, or a secondary point, you now check at the place they name (METHODS §5.5: a targeted check, labelled
"checked at the stated place" on the site). You did not write these anchors; the claim writer (AI reader 267)
did.

Your tasks: `data/verification/gen-a-2026-11-01/targeted/tasks_reader<N>.json` (N = your reader number). Each gives the
claim id, the anchor index, the reference, page, locator, source read, the anchor's `extracted` text and its role.

## For each task

1. Check every detail of `extracted` at the source: numbers, groups and their sizes, the comparison group, what was
   measured and how, when (during use, after, recalled later), adjustment, intervals, P values, and any quote word for
   word. Recompute any count, percentage or editors' calculation. Check that the role fits.
2. Give one verdict: `confirmed`, `corrected` (change only what is wrong; give `corrected_extracted` and, if needed,
   `corrected_page` and `corrected_locator`), `wrong-location` (give the right place) or `not-found` (say where you
   looked).
3. One short note (at most 40 words). Say in the note when the anchor's wording overstates the source (an association as
   an effect, a recalled attribution as a measured predictor, a model estimate as a count, a subgroup as everyone, a
   review's citation as its own finding).

Locators: count running-text paragraphs one way: a bulleted or numbered list is not a paragraph, and a heading starts a
new count.

## Sources

Check against the text you saved in your blind round first. If that cannot settle a point, open the PMC page again in
one tab of your own (load the browser tools once with ToolSearch, query `mcp__remote-devices__Claude_Browser__`;
`tabs_create`, its tabId on every call, closed at the end; never `preview_start`; never touch another tab; no search
engines, no PDFs or downloads; stop at any check page). A value printed only in a figure image needs a screenshot; if your
screenshot comes back blank, give `not-found` with the note "deferred: figure image not viewable" so the editor can
return to it.

For context you may read the claims named in your tasks, and only those, in `claims_reader<N>.json` in this folder. Do
not open `data/claims/` or any other reader's files.

## Output

`data/verification/gen-a-2026-11-01/targeted/out_reader<N>.json`, written as you go:

```json
{"reader": "AI reader <N> (second reader)", "date": "2026-11-01", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Change no other file. Quotations at most 15 words. No advice on amounts, ways of using, timing or combinations.
Independence: every anchor in this round was written by the claim writers before your blind reading. Finding the same
thing in your blind round is agreement, not authorship; mark `"independent": "no"` only if an anchor's wording was
copied from your own output.

Final message under 150 words: counts by verdict, and every correction that changes a number.
