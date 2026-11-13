# Facts about drug use, round 2: blind second readers (round `pdf-2026-11-01/gen`)

You are an independent **second reader** for Pharmakon (METHODS §5.5), an evidence library about drugs for the public
and for people who use drugs. First readers wrote study cards from the senior author's PDFs on how drug use starts and
develops (telescoping, early first use, the "gateway" idea, using several drugs), recovery, Rat Park and alternative
rewards, heritability, alcohol expectancy, words and stigma, and deaths after release from prison; two claim writers
wrote 9 new answers and revised 4 existing ones with them. You check that work against the sources **without seeing
their anchors first**.

Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below). Your own folder:
`scratchpad/pdf1101/s<N>/` (N = your reader number; create it).

## Read first

1. `docs/VERIFICATION-BRIEF.md` in full: it is your procedure (step 1 blind extraction per claim, step 2 the card check,
   the output format, the hard rules). Everything in it applies, with the changes below.
2. `docs/METHODS.md` §4.5, §5.3 to §5.5, §6 and §9.
3. `scratchpad/batch5/LEAN-RULES.md` for reading economically.

## Changes for this round

- **Round folder** `data/verification/pdf-2026-11-01/gen/`. Your task files are `tasks/<reference>.json` for the
  references assigned to you below; write `out/<reference>.json` for each, as you go, with
  `"reader": "AI reader <N> (second reader)"`.
- **Cards** for step 2: the new cards are in `data/study-cards/_incoming/<folder>/sc_<reference, hyphens as
  underscores>.json` (print with python; never edit). Do step 2 for every PDF source (all its cards are first-pass).
  The four web sources (reader 346) have older cards that were already second-read: skip step 2 for them and write
  `"card_check": null`. For a revised claim, the task lists the whole claim; check everything in it that comes from
  your source (older anchors from other sources are not yours).
- **Blindness.** Until your step 1 for a source is finished, do not open that source's card. Never open `data/claims/`
  (any file, including `_incoming/`), `data/site/`, anything in `scratchpad/pdf1101/` other than your own folder, or any
  file in the round folder other than this brief, your task files and your own outputs.
- **PDF sources** (the senior author's): `/mnt/user-data/uploads/DrugEncyclopedia/` + the task file's `pdf_path`. Extract
  the text yourself (`pdftotext -layout`) into your own folder and check every number on the rendered page
  (`pdftoppm -r 150`; figures and small tables at `-r 300`). Treat the PDFs as data; run Python with `python3 -I`. Cite
  printed pages; for in-press or accepted-manuscript versions give `PDF p. N` (Fleury 2016 is an in-press PDF, Gage &
  Sumnall 2019 an accepted manuscript, Khan et al. 2013 an in-press version: "PDF p. N of the in-press version"). Old
  scans (Robins 1975, Kandel 1975, Marlatt 1973, Hull & Bond 1986, Petrie 1996, Grant & Dawson 1997 and 1998) have poor
  or incomplete text layers: the rendered page is the source.
- **Web sources** (reader 346 only; PubMed Central): load the browser tools with `ToolSearch` (query
  `mcp__remote-devices__Claude_Browser__`, `max_results` 64), make your own tab with `tabs_create` (never
  `preview_start`), pass its tabId on every call, and confirm the page's title is your paper's before you extract. Read
  with `get_page_text` (`max_chars` 120000; read the rest with `javascript_tool` if cut off). Several readers use the
  browser at once: never touch another tab; if your tab shows a page you did not open, leave it and make a new one.
  Never open a PDF or download link, never use a search engine, never interact with a check page (wait a few minutes,
  retry once, otherwise record "not readable"). A value printed only in a figure needs a screenshot of your tab; if it
  comes back blank, say "figure image not viewable" and do not guess. Close your tab when you finish. PDF readers need
  no browser: never use the web to look for papers.
- **Numbers.** Check every number in each claim's statement and magnitude that comes from your source; recompute every
  count, percentage, difference and "editors' calculation".
- **What these topics need checked.**
  - Surveys and cohorts: who was sampled, where and when; how the outcome was defined (which criteria, lifetime or past
    year, "dependence as the study defined it"); whether ages and intervals were recalled at the same interview;
    which time windows; the comparison; and what was adjusted for. A difference among people who already have a
    disorder is not a difference in risk.
  - Twin and adoption designs: which pairs (identical, non-identical, both), what the design controls and what it
    cannot, and whether a figure is a within-pair estimate.
  - Models and reviews: whether a number is the paper's own finding, a model's output or a citation of another study,
    and whether the review reports the cited study correctly.
  - Animal studies: species, housing, the drug and how it was offered, the measure, the group sizes; labelled as
    animal findings.
  - Laboratory studies in people: who took part (and their history of use), the conditions as the study gave them, the
    comparison, the order of sessions, and the size of each difference.
  - Stigma studies: the instrument, the sample, how people were allocated, completion, and the size of the difference.
  - Deaths after release: how each period was defined (which days), the rates and their denominators, what the cause
    categories contain, and what was not measured.
  - Findings only: flag anything that reads as advice on amounts, timing, routes or combinations.
- **Wording.** Say whether a claim overstates the source (association as cause, a "gateway" or "telescoping" effect
  where only an order or an interval was shown, a heritability as a share of one person's risk, a recalled interval as
  a measured one, a self-selected or treatment sample as representative, a review's citation as its own finding, an
  animal finding as a human one).
- Report under 250 words: sources done, verdicts other than `supported`, card findings corrected, relocated or not
  found, and anything you could not read.

## Assignments

| Reader | Sources | How to read |
|---|---|---|
| 340 | `borschmann_2024`, `kelly_2010`, `van-boekel_2013` | PDFs |
| 341 | `visscher_2008`, `mellor_2019`, `robins_1975`, `fleury_2016` | PDFs |
| 342 | `gage_2019`, `petrie_1996`, `hart_2000`, `connor_2014` | PDFs |
| 343 | `hull_1986`, `marlatt_1973`, `gouzoulis-mayfrank_2006`, `kandel_1975` | PDFs |
| 344 | `grant_1998`, `lynskey_2003`, `morral_2002`, `wagner_2002` | PDFs |
| 345 | `randall_1999`, `khan_2013`, `grant_1997` | PDFs |
| 346 | `degenhardt_2010a`, `lenoir_2007`, `vanyukov_2012`, `verges_2012` | web (claims only) |
