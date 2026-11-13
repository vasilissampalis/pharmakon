# Drug use in general: blind second readers (round `gen-a-2026-11-01`)

You are an independent **second reader** for Pharmakon (METHODS §5.5). First readers wrote study cards for papers on
drug use in general (women and men, "telescoping", treatment, genes and family, starting young, the gateway idea,
using several drugs, the words used about people who use drugs, and one rat study), and a claim writer turned some of
them into draft answers. You check that work against the sources **without seeing the anchors first**.

Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below). Your own folder:
`scratchpad/gen-a/s<N>/` (N = your reader number; create it).

## Read first

1. `data/verification/bd-dd-2026-10-31/BRIEF-second-readers.md`: everything in it applies (the procedure in
   `docs/VERIFICATION-BRIEF.md`, blindness, reading in one browser tab of your own, numbers, wording, the report), with
   these changes.
2. `data/verification/gen-a-2026-11-01/BRIEF-first-readers.md`, "What to record for these topics": check that the cards
   and claims carry those points.

## Changes for this round

- **Round folder** `data/verification/gen-a-2026-11-01/`: tasks in `tasks/<reference>.json`, outputs in
  `out/<reference>.json`. Cards: `data/study-cards/_incoming/<folder>/sc_<reference, hyphens as underscores>.json`.
- **Blindness** as in the bd-dd brief, with `scratchpad/gen-a/` in place of `scratchpad/bd-dd/`.
- **What these topics need checked.** For every difference between women and men: treatment or general-population
  sample, how the timing of each step was measured, and the adjustment set; whether a figure is a hazard among everyone
  at risk or a mean among those who reached the step. For genes and family: what the design can show (adoption,
  co-twin, common factor), the population and era, and that no heritability is claimed where the source gives none.
  Animal findings stay labelled as such.
- **Known points to check in step 2:** the claim writer reported that `sc_prom_wormley_2017` presents Kendler et al.
  (2012) as giving a heritability estimate while `sc_kendler_2012` records none, and that the sibling percentages on
  `sc_kendler_2012` are the siblings' own rates grouped by the adoptee's record. Settle both against the sources.

## Assignments

Task files: `data/verification/gen-a-2026-11-01/tasks/` (14 sources; an empty claim list means a card check only).

| Reader | Sources | Kind |
|---|---|---|
| 276 | `keyes_2010`, `marks_2018`, `mchugh_2018`, `greenfield_2007` | claims and cards |
| 277 | `kendler_2012`, `prom-wormley_2017`, `pennington_2023` (publisher page, https://doi.org/10.1037/adb0000919) | claims and cards |
| 278 | `maimaris_2014`, `irons_2015`, `liu_2018`, `lenoir_2007` | claims and cards (`lenoir_2007` card only) |
| 279 | `verges_2012`, `vanyukov_2012`, `degenhardt_2010a` | cards only |
