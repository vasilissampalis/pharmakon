# Round-2 checks, round gen-a-2026-11-01 (general facts about drug use), 1 November 2026

You are a new, independent AI reader for Pharmakon, an evidence library about drugs for the public and for people who
use drugs. You did not write any of the anchors below and you took no part in this round. Project:
`/home/claude/drug-encyclopedia`. Scratch folder: `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/`;
your own folder is `scratchpad/gen-a/c<N>/` (create it).

The adjudicators (AI readers 286 to 288) settled the second readers' findings against the sources. Where a claim needed a
number that no anchor carried, they added an anchor (it enters as ai-located); where a second reader's note asked for
it, they reworded an anchor that had already been checked. Every such anchor now needs a check by a reader who did not
write it (METHODS §5.5: a targeted check, "checked at the stated place").

Your tasks: `tasks_reader<N>.json` in this folder. Each gives the claim id, the anchor index, the reference, page,
locator, source read, the anchor's `extracted` text, its role, and why it is being checked (`why`: "new anchor" or
"reworded after a check").

## For each task

1. Find the stated place in the source and check every detail of `extracted`: numbers, groups and their sizes, the
   comparison group, what was measured and how, when (during use, after, recalled later), adjustment, intervals, P values,
   and any quote word for word. Recompute any count, percentage or editors' calculation. Check that the role fits.
2. Give one verdict: `confirmed`, `corrected` (change only what is wrong; give `corrected_extracted` and, if needed,
   `corrected_page` and `corrected_locator`), `wrong-location` (give the right place) or `not-found` (say where you
   looked).
3. One short note (at most 40 words). Say when the anchor's wording overstates the source (an association as an effect,
   a subgroup as everyone, a review's citation as its own finding).

Locators: count running-text paragraphs one way: a bulleted or numbered list is not a paragraph, and a heading starts a
new count.

## Sources

All are web full texts in PubMed Central. Saved copies of some source texts are in `scratchpad/gen-a/`: `a287/kendler_2012.txt`,
`r262/pennington_2023.txt`, `r262/liu_2018.txt`, `r261/src_greenfield`, `r261/src_mchugh`. Read only the source texts there,
not the readers' notes, checks or outputs. Keyes et al. (2010), Marks et al. (2018), Maimaris & McCambridge (2014) and Irons
et al. (2015) have no saved copy: read them on their PMC pages. Open pages in one tab of your own in the app's browser (load the
tools once with ToolSearch, query `mcp__remote-devices__Claude_Browser__`, max_results 20; `tabs_create`, its tabId on every call,
closed at the end; never `preview_start`; never touch another tab; no search engines, no PDFs or downloads; stop at any check
page). A value printed only in a figure image: open the image's own address in your tab and take a screenshot; if the screenshot
comes back blank, give `not-found` with the note "deferred: figure image not viewable".

For context you may read the claims named in your tasks, and only those, in `claims_reader<N>.json` in this folder. Do
not open `data/claims/`, the adjudicators' files or any other reader's files.

## Output

`out_reader<N>.json` in this folder, written as you go:

```json
{"reader": "AI reader <N> (round-2 checker)", "date": "2026-11-01", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Change no other file. Quotations at most 15 words. No advice on amounts, ways of using, timing or combinations.

Final message under 150 words: counts by verdict, and every correction that changes a number.
