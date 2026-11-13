# Targeted checks, Cannabis round (can-a-2026-10-27), 30 October 2026

The blind reconciliation has run on the 16 sources read so far. Of the claim writers' anchors from your PDF sources,
most matched your blind extractions; those that did not, usually because they cite a different paragraph, table or
figure, or a secondary point, you now check at the place they name (METHODS §5.5: a targeted check, labelled "checked
at the stated place" on the site). You did not write these anchors; the claim writers (AI readers 207 to 210) did.

Your tasks: `data/verification/can-a-2026-10-27/targeted/tasks_reader<N>.json` (N = your reader number). Each gives the
claim id, the anchor index, the reference, page, locator, source read, the anchor's `extracted` text and its role.

## For each task

1. Check every detail of `extracted` at the source: numbers, groups and their sizes, the comparison group, how often
   and how long people used cannabis and how this was measured, ages, follow-up, adjustment, intervals, P values, and any
   quote word for word. Recompute any count, percentage or editors' calculation. Check that the role fits.
2. Give one verdict: `confirmed`, `corrected` (change only what is wrong; give `corrected_extracted` and, if needed,
   `corrected_page` and `corrected_locator`), `wrong-location` (give the right place) or `not-found` (say where you
   looked).
3. One short note (at most 40 words). Say in the note when the anchor's wording overstates the source (an association as
   an effect, a model estimate as a count, a subgroup as everyone, a review's citation as its own finding, an animal
   finding as shown in people).

## Sources and context

The same PDFs you read in the blind round, with your own extracted texts and rendered pages in your folder under
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/`. Check every table and figure value on a
rendered page. No browser is needed.

For context you may read the claims named in your tasks, and only those, in
`data/verification/can-a-2026-10-27/targeted/claims_reader<N>.json`. Do not open `data/claims/` or any other reader's
files. Reader 213: you still have Lopez-Quintero et al. (2011) to read blind; nothing in your claims file comes from it.

## Output

`data/verification/can-a-2026-10-27/targeted/out_reader<N>.json`, written as you go:

```json
{"reader": "AI reader <N> (second reader)", "date": "2026-10-30", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Change no other file. Quotations at most 15 words. No advice on amounts, ways of using, timing or combinations.
Independence: every anchor in this round was written by the claim writers before your blind reading. Finding the same
thing in your blind round is agreement, not authorship; mark `"independent": "no"` only if an anchor's wording was
copied from your own output.

Final message under 150 words: counts by verdict, and every correction that changes a number.

## Web papers (readers 213 for Lopez-Quintero, 214, 215, 217 and 218; added 31 October)

Your task file for this part is `tasks_reader<N>.json`, or `tasks_reader<N>b.json` if you already did a PDF part. Check
against the text you saved in your blind round first; if that cannot settle a point, open the PMC page again in one tab
of your own (load the browser tools once with ToolSearch, query `mcp__remote-devices__Claude_Browser__`; `tabs_create`,
its tabId on every call, closed at the end; never `preview_start`; never touch another tab; no search engines, no PDFs or
downloads; stop at any check page). A value printed only in a figure image needs a screenshot; if your screenshot comes
back blank (the browser pane is hidden on the senior author's computer), give `not-found` with the note "deferred:
figure image not viewable" so the editor can return to it. Write `out_reader<N>.json` (or `out_reader<N>b.json`).
