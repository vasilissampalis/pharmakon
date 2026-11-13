# Targeted checks, drug-deaths round (`pdf-2026-11-01/dd`), 1 November 2026

The blind reconciliation has run on the sources read so far. Of the claim writers' anchors from your sources, most
matched your blind extractions; those that did not, usually because they cite a different paragraph, table or figure,
or a secondary point, you now check at the place they name (METHODS §5.5: a targeted check, labelled "checked at the
stated place" on the site). You did not write these anchors; the claim writers (AI readers 318 and 319) did.

Your tasks: `data/verification/pdf-2026-11-01/dd/targeted/tasks_reader<N>.json` (N = your reader number). Each gives the
claim id, the anchor index, the reference, page, locator, source read, the anchor's `extracted` text and its role.

## For each task

1. Check every detail of `extracted` at the source: numbers, groups and their sizes, place and years, how a death
   entered a count (codes, "drug mentioned", toxicology, the certifier's conclusion, a register's definition), who
   decided, which specimen and how long after death, the comparison, adjustment, intervals, and any quote word for
   word. Recompute any count, percentage or editors' calculation. Check that the role fits.
2. Give one verdict: `confirmed`, `corrected` (change only what is wrong; give `corrected_extracted` and, if needed,
   `corrected_page` and `corrected_locator`), `wrong-location` (give the right place) or `not-found` (say where you
   looked).
3. One short note (at most 40 words). Say in the note when the anchor's wording overstates the source ("involved",
   "present" or "detected" as "caused", a model estimate as a count, a case series as a rate, a review's citation as its
   own finding, one place's figure as everywhere).

## Sources and context

PDF readers: the same PDFs you read in the blind round, with your own extracted texts and rendered pages in your folder
under `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/pdf1101/s<N>/`. Check every table and
figure value on a rendered page. No browser is needed.

Web readers (333, 334, 335): check against the text you saved in your blind round first; if that cannot settle a point,
open the PMC or Bookshelf page again in one tab of your own (load the browser tools once with ToolSearch, query
`mcp__remote-devices__Claude_Browser__`, `max_results` 64; `tabs_create`, its tabId on every call, closed at the end;
never `preview_start`; never touch another tab; no search engines, no PDFs or downloads; stop at any check page). A
value printed only in a figure image needs a screenshot; if it comes back blank, give `not-found` with the note
"deferred: figure image not viewable".

For context you may read the claims named in your tasks, and only those, in
`data/verification/pdf-2026-11-01/dd/targeted/claims_reader<N>.json`. Do not open `data/claims/` or any other reader's
files.

## Output

`data/verification/pdf-2026-11-01/dd/targeted/out_reader<N>.json`, written as you go:

```json
{"reader": "AI reader <N> (second reader)", "date": "2026-11-01", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Change no other file. Quotations at most 15 words. No advice on amounts, ways of using, timing or combinations.
Independence: every anchor in this round was written by the claim writers before your blind reading. Finding the same
thing in your blind round is agreement, not authorship; mark `"independent": "no"` only if an anchor's wording was
copied from your own output.

Final message under 150 words: counts by verdict, and every correction that changes a number.
