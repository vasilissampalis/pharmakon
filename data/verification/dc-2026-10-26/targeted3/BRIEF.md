# Targeted checks of the adjudicators' new anchors (dc-2026-10-26), 27 October 2026

The adjudicators (AI readers 148 and 149) added 13 anchors on 27 October while settling the second readers' findings; eight
were checked in the PDFs, and these last five need the web papers. A
second reader must check each at the place it names before it counts (METHODS §5.5, a targeted check), and that reader
must have written neither the anchor nor the finding behind it: so these tasks come from sources whose points were raised
by another reader. You did not write these anchors.

Your tasks: `data/verification/dc-2026-10-26/targeted3/tasks_reader<N>.json` (N = your reader number). Each gives the
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

These anchors are on **web papers**, read in the app's built-in browser (load its tools with ToolSearch, query
"mcp__remote-devices__Claude_Browser__", max_results 64). Open your own tab with `tabs_create` and pass its tabId on every call;
never touch any other tab; one page load at a time; never a PDF link, a download or a check page; close your tab at the end.
- Halifax et al. (2024): https://link.springer.com/article/10.1186/s12954-023-00921-8 — its figures each have a page of
  their own (…/figures/1, …/figures/2); open the full-size image and check every value the anchor gives against it.
- Lockwood et al. (2021): https://link.springer.com/article/10.1186/s12954-021-00478-4 (…/figures/1 for Fig. 1).
- Vickers-Smith et al. (2025): the PubMed Central copy https://pmc.ncbi.nlm.nih.gov/articles/PMC12076174/ (Table 3 and
  its notes; the publisher page does not show the notes).
Use `get_page_text` for text and a screenshot or zoom of the figure for values that are only in the image. Do not open
`data/claims/` itself.

## Output

`data/verification/dc-2026-10-26/targeted3/out_reader<N>.json`, written as you go:

```json
{"reader": "AI reader <N> (second reader)", "date": "2026-10-27", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Rules as in your first brief (no other file changed, quotations at most 15 words, no dosing advice). Final message under
150 words: counts by verdict, and every correction that changes a number.
