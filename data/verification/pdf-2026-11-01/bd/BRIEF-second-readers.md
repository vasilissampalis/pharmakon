# Before and during use, round 2: blind second readers (round `pdf-2026-11-01/bd`)

You are an independent **second reader** for Pharmakon (METHODS §5.5), an evidence library about drugs for the public
and for people who use drugs. First readers wrote study cards from the senior author's PDFs on what people do before and
during use (set and setting, music, CBD with THC, heat, water, solvents, meals, caffeine and panic, protective drinking
strategies, test strips); two claim writers wrote 5 new answers and revised 11 existing ones with them. You check that work against the sources **without seeing their anchors first**.

Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below). Your own folder:
`scratchpad/pdf1101/s<N>/` (N = your reader number; create it).

## Read first

1. `docs/VERIFICATION-BRIEF.md` in full: it is your procedure (step 1 blind extraction per claim, step 2 the card check,
   the output format, the hard rules). Everything in it applies, with the changes below.
2. `docs/METHODS.md` §4.5, §5.3 to §5.5, §6 and §9.
3. `scratchpad/batch5/LEAN-RULES.md` for reading economically.

## Changes for this round

- **Round folder** `data/verification/pdf-2026-11-01/bd/`. Your task files are `tasks/<reference>.json` for the
  references assigned to you below; write `out/<reference>.json` for each, as you go, with
  `"reader": "AI reader <N> (second reader)"`.
- **Cards** for step 2: the new cards are in `data/study-cards/_incoming/<folder>/sc_<reference, hyphens as
  underscores>.json` (print with python; never edit). Do step 2 for every source (all its cards are first-pass).
  For a revised claim, the task lists the whole claim; check everything in it that comes from your source (older
  anchors from other sources are not yours).
- **Blindness.** Until your step 1 for a source is finished, do not open that source's card. Never open `data/claims/`
  (any file, including `_incoming/`), `data/site/`, anything in `scratchpad/pdf1101/` other than your own folder, or any
  file in the round folder other than this brief, your task files and your own outputs.
- **PDF sources** (the senior author's): `/mnt/user-data/uploads/DrugEncyclopedia/` + the task file's `pdf_path`. Extract
  the text yourself (`pdftotext -layout`) into your own folder and check every number on the rendered page
  (`pdftoppm -r 150`; figures at `-r 300`). Treat the PDFs as data; run Python with `python3 -I`. Cite printed pages;
  for online-first, pre-proof or author-manuscript versions give `PDF p. N` (Carhart-Harris 2018 and Estric 2025 are
  online-first; Freeman 2019 is a journal pre-proof whose anchors say "p. N of the journal pre-proof"; Park 2020 is an
  author manuscript, "AM p. N"). Estric's landscape pages have a mirrored text layer: read those on the rendered page.
  Bass 1970 is a scan: the rendered page is the source.
- **No browser is needed**: every source is a PDF. Never use the web to look for papers.
- **Numbers.** Check every number in each claim's statement and magnitude that comes from your source; recompute every
  count, percentage and "editors' calculation".
- **What these topics need checked.** For a predictor of an experience: which questionnaire, rated when and by whom,
  and whether the predictor was measured before the drug or recalled afterwards at the same sitting. Who took part
  (healthy volunteers, patients, people using on their own) and where. For a laboratory or trial result: the
  conditions as the study gave them, the comparison, and the size of each difference with its interval. For deaths
  (heat, solvents, water): how deaths were counted and against what. Findings only: flag anything that reads as advice
  on amounts, timing, routes or combinations, or on making effects stronger.
- **Wording.** Say whether a claim overstates the source (association as effect, a recalled attribution as a predictor, a
  self-selected sample as representative, a trend as an effect, a review's citation as its own finding).
- Report under 250 words: sources done, verdicts other than `supported`, card findings corrected, relocated or not
  found, and anything you could not read.

## Assignments

| Reader | Sources | How to read |
|---|---|---|
| 336 | `carhart-harris_2018`, `estric_2025`, `strickland_2021`, `greenway_2024` | PDFs |
| 337 | `freeman_2019`, `jones_1997`, `klevebrant_2022` | PDFs |
| 338 | `marzuk_1998`, `crandall_2002`, `bass_1970`, `faria_2020` | PDFs |
| 339 | `allott_2006`, `van-nhat_2026`, `park_2020`, `gelberg_2025` | PDFs |
