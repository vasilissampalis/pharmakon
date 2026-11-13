# Cannabis, Tier A: blind second readers (round `can-a-2026-10-27`)

You are an independent **second reader** for Pharmakon (METHODS §5.5). First readers wrote study cards for 30 core
papers on cannabis, and claim writers turned them, with two older cards on dependence, into 21 draft answers: memory,
thinking and IQ; psychosis and schizophrenia; dependence, withdrawal and repeated vomiting; how THC moves through the
body; pregnancy, the heart and mood; and cannabis medicines. You check that work against the sources **without seeing
their anchors first**.

Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below). Your own folder:
`scratchpad/can-a/s<N>/` (N = your reader number; create it).

## Read first

1. `docs/VERIFICATION-BRIEF.md` in full: it is your procedure (step 1 blind extraction per claim, step 2 the card check,
   the output format, where to read, the hard rules). Everything in it applies, with the changes below.
2. `docs/METHODS.md` §4.5, §5.3 to §5.5, §6 and §9.
3. `scratchpad/batch5/LEAN-RULES.md` for reading PDFs and web pages economically.

## Changes for this round

- **Round folder** `data/verification/can-a-2026-10-27/`. Your task files are `tasks/<reference>.json` for the
  references assigned to you below; write `out/<reference>.json` for each, as you go, with
  `"reader": "AI reader <N> (second reader)"`.
- **Cards** for step 2: `data/study-cards/_incoming/cannabis/sc_<reference, hyphens as underscores>.json` (print it with
  python; never edit it). Two cards are older and already merged: `sc_anthony_1994` and `sc_lopez_quintero_2011`, in
  `data/study-cards/methamphetamine.json` (print the card by id).
- **Blindness.** Until your step 1 for a source is finished, do not open that source's card. Never open
  `data/claims/` (any file, including `_incoming/`), `data/site/`, anything in `scratchpad/can-a/` other than your own
  folder, or any file in the round folder other than this brief, your task files and your own outputs.
- **PDFs** (the senior author's): `/mnt/user-data/uploads/DrugEncyclopedia/` + the task file's `pdf_path`. Extract the
  text yourself (`pdftotext -layout`) into your own folder and render pages (`pdftoppm -r 110`) for tables and figures.
  Cite printed pages; for the accepted manuscripts (Gage 2016, Broyd 2016) give "AM p. N" (N = PDF page). Anthony et al.
  (1994) is a scanned page whose machine-read text has errors: check every number on the rendered page.
- **Web papers**: PubMed Central (`https://pmc.ncbi.nlm.nih.gov/articles/<PMCID>/`) or, where the task gives no PMCID,
  the DOI link (`https://doi.org/<DOI>`). Load the browser tools with `ToolSearch` (query
  `mcp__remote-devices__Claude_Browser__`, `max_results` 64), make your own tab with `tabs_create` (never
  `preview_start`), pass its tabId on every call, and confirm the page's title is your paper's before you extract.
  Read with `get_page_text` (`max_chars` 120000; read the rest with `javascript_tool` if cut off). Several readers use
  the browser at once: never touch another tab; if your tab shows a page you did not open, leave it and make a new one.
  Never open a PDF or download link, never use a search engine, never interact with a check page (JAMA sometimes shows
  one: wait a few minutes, retry once, otherwise record "not readable"). Say in `source_read` when a PMC text is an
  author manuscript. Close your tab when you finish. Online supplements are not read: say when a claim's figure can only
  come from one.
- **Numbers.** Check every number in each claim's statement and magnitude that comes from your source. Recompute every
  count, percentage, conversion and "editors' calculation" (for example an odds ratio turned into counts out of 100, a
  standardized difference turned into IQ points); say whether you get the same.
- **Exposure, outcome, comparison, adjustment.** For every estimate, check that the claim names the exposure as the
  source defined it (ever, weekly, daily, heaviest use, waves of dependence; potency and how it was judged), the outcome
  (psychotic symptoms, psychotic disorder, schizophrenia diagnosis; which tests, after how long without cannabis), the
  comparison group and the adjustment set. A wrong or missing one is an error, not a matter of wording.
- **Designs.** For genetic (Mendelian randomization) studies, check what the source reports about instrument strength,
  the exposure the variants stand for (genetic liability to ever use) and the sensitivity analyses for other pathways.
  For reviews, check the number of studies and participants behind each pooled figure, and whether a figure the review
  gives is its own result or a citation of another study (narrative reviews are cited only second-hand).
- **Wording.** Say whether a claim's wording overstates the source: association presented as effect, a subgroup
  presented as everyone, a review's citation presented as its finding, a trial of one product presented as all cannabis,
  "safe" or "no risk" where the source does not say it. Also flag anything that reads as advice on how much or how to
  use, and any dose given other than as a study's condition.
- Report under 250 words: sources done, verdicts other than `supported`, card findings corrected, relocated or not
  found, and anything you could not read.

## Assignments

Task files are in `data/verification/can-a-2026-10-27/tasks/` (32 sources; each lists only the claims that cite it and
the number and roles of the first reader's anchors from that source).

| Reader | Sources | How to read |
|---|---|---|
| 211 | `moore_2007`, `gage_2016`, `gillespie_2021`, `ksir_2016` | PDFs |
| 212 | `hall_2009`, `hall_2015`, `page_2020` | PDFs |
| 213 | `broyd_2016`, `curran_2016`, `anthony_1994`, `lopez-quintero_2011` | PDFs (Lopez-Quintero et al., 2011, from its PDF in `PDFs/_Cross-cutting/`) |
| 214 | `meier_2012`, `rogeberg_2013`, `moffitt_2013`, `jackson_2016`, `meier_2018` | web (PMC) |
| 215 | `scott_2018`, `gobbi_2019` | web (PMC) |
| 216 | `di-forti_2019`, `di-forti_2015`, `marconi_2016`, `murray_2016` | web (PMC; Di Forti 2015 at the publisher) |
| 217 | `gage_2017`, `vaucher_2018`, `pasman_2018`, `connor_2021` | web (PMC) |
| 218 | `bahji_2020`, `sorensen_2017`, `huestis_2007`, `volkow_2014` | web (PMC) |
| 219 | `whiting_2015`, `gunn_2016` | web (Whiting at the publisher, JAMA; Gunn in PMC) |
