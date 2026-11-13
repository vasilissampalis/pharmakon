# Cocaine, round 2: blind second readers (round `pdf-2026-11-01/coc`)

You are an independent **second reader** for Pharmakon (METHODS §5.5), an evidence library about drugs for the public
and for people who use drugs. First readers wrote study cards from the senior author's PDFs on cocaine: how it acts by
route, how dependence starts, powder against crack, chest pain and heart attacks and how hospitals treat them,
levamisole in street cocaine, cocaine with alcohol (cocaethylene), memory and thinking, deaths, psychosis and medicines
tried for dependence. Two claim writers wrote 10 new answers and revised 2 existing ones. You check that work against
the sources **without seeing their anchors first**.

Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below). Your own folder:
`scratchpad/pdf1101/s<N>/` (N = your reader number; create it).

## Read first

1. `docs/VERIFICATION-BRIEF.md` in full: it is your procedure (step 1 blind extraction per claim, step 2 the card check,
   the output format, the hard rules). Everything in it applies, with the changes below.
2. `docs/METHODS.md` §4.5, §5.3 to §5.5, §6 and §9.
3. `scratchpad/batch5/LEAN-RULES.md` for reading economically.

## Changes for this round

- **Round folder** `data/verification/pdf-2026-11-01/coc/`. Your task files are `tasks/<reference>.json` for the
  references assigned to you below; write `out/<reference>.json` for each, as you go, with
  `"reader": "AI reader <N> (second reader)"`.
- **Cards** for step 2: `data/study-cards/_incoming/<folder>/sc_<reference, hyphens as underscores>.json` (folder
  `cocaine` for almost all; print with python; never edit). Do step 2 for every source (all its cards are first-pass).
  For a revised claim (the two cocaine-with-alcohol answers), the task lists the whole claim; check everything in it
  that comes from your source (older anchors from other sources are not yours).
- **Blindness.** Until your step 1 for a source is finished, do not open that source's card. Never open `data/claims/`
  (any file, including `_incoming/`), `data/site/`, anything in `scratchpad/pdf1101/` other than your own folder, or any
  file in the round folder other than this brief, your task files and your own outputs.
- **PDF sources** (the senior author's): `/mnt/user-data/uploads/DrugEncyclopedia/` + the task file's `pdf_path`. Extract
  the text yourself (`pdftotext -layout`) into your own folder and check every number on the rendered page
  (`pdftoppm -r 150`; figures and small tables at `-r 300`). Treat the PDFs as data; run Python with `python3 -I`. Cite
  printed pages; for accepted manuscripts, in-press, online-first or proof versions give `PDF p. N` (Butler 2017,
  Chandra 2020, Frazer 2018, López-Martín 2026, Pham 2018 and Spronk 2013 are such versions; follow the task's
  `first_reader_source` note on how its pages are numbered). Scans with poor text layers (Hatsukami 1996, Hollander
  1995, Evans 1996): the rendered page is the source.
- **No browser is needed**: every source is a PDF. Never use the web to look for papers.
- **Numbers.** Check every number in each claim's statement and magnitude that comes from your source; recompute every
  count, percentage, pooled estimate you can and every "editors' calculation" (one claim reports an editors'
  recalculation of a meta-analysis whose authors entered percentages as counts: check the inputs you can see).
- **What these topics need checked.**
  - Who and where: people in a laboratory (and their history of use), patients in an emergency department or a
    catheter laboratory, people in treatment, people in surveys; kept apart in every sentence.
  - Exposure and comparison: powder or crack, snorted, smoked or injected, as each source defines it; the comparison
    group and adjustment with every estimate; "present" or "associated" never as "caused".
  - Hospital treatment (beta-blockers, labetalol, thrombolysis and others): what was given to patients and what was
    measured, never self-treatment.
  - Memory and thinking: how long people had been abstinent, the comparison group, alcohol and other drugs as
    confounders, and whether a difference is within the normal range.
  - Deaths and psychosis: how deaths or symptoms were counted, in whom, against what, and how long people were followed.
  - Findings only: flag anything that reads as advice on amounts, routes, timing or combinations, or on making effects
    stronger or longer.
- **Wording.** Say whether a claim overstates the source (association as effect, a laboratory finding as shown in
  everyday use, a review's citation as its own finding, a case series as a rate, one hospital's figure as everywhere).
- If an automatic filter stops you, do not retry or reword the same step: write what you have, say in the output and the
  report where you stopped, and finish.
- Report under 250 words: sources done, verdicts other than `supported`, card findings corrected, relocated or not
  found, and anything you could not read.

## Assignments

| Reader | Sources | How to read |
|---|---|---|
| 359 | `weber_2000`, `hollander_1995`, `mccord_2008` | PDFs |
| 360 | `lange_1990`, `boehrer_1993`, `fanari_2014`, `pham_2018` | PDFs |
| 361 | `buchanan_2012`, `roberts_2015`, `degenhardt_2011` | PDFs |
| 362 | `sabe_2021`, `castells_2007`, `chandra_2020` | PDFs |
| 363 | `barnett_1981`, `evans_1996`, `hatsukami_1996`, `chen_2004` | PDFs |
| 364 | `butler_2017`, `harris_2003b`, `hart_2000b`, `jatlow_1991` | PDFs |
| 365 | `jovanovski_2005`, `spronk_2013`, `frazer_2018`, `lopez-martin_2026`, `bolla_2000` | PDFs |
