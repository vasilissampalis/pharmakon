# Targeted checks of the adjudicators' new anchors (dc-2026-10-26), 27 October 2026

The adjudicators (AI readers 148 and 149) added 13 anchors on 27 October while settling the second readers' findings. A
second reader must check each at the place it names before it counts (METHODS §5.5, a targeted check), and that reader
must have written neither the anchor nor the finding behind it: so these tasks come from sources whose points were raised
by another reader. You did not write these anchors.

Your tasks: `data/verification/dc-2026-10-26/targeted2/tasks_reader<N>.json` (N = your reader number). Each gives the
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

These are PDFs, some of them papers you did not read before: `/mnt/user-data/uploads/DrugEncyclopedia/` + the
reference's `verification.pdf_path` in `data/references/drug-checking.json`. A text extraction of each, pages separated
by form feeds, is in `scratchpad/ux1026/dc/numtext/`; render a page with `pdftoppm -r 110 -f N -l N -png` into your own
folder to check a figure or a table, and check every negative number on the rendered page. Author manuscripts
(Kutscher) are cited as "AM p. N" = PDF page. Do not open `data/claims/` itself.

## Output

`data/verification/dc-2026-10-26/targeted2/out_reader<N>.json`, written as you go:

```json
{"reader": "AI reader <N> (second reader)", "date": "2026-10-27", "results": [{"n": 1, "claim_id": "...", "anchor_index": 0, "verdict": "confirmed", "note": "..."}]}
```

Rules as in your first brief (no other file changed, quotations at most 15 words, no dosing advice). Final message under
150 words: counts by verdict, and every correction that changes a number.
