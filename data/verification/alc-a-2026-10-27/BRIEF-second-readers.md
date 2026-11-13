# Alcohol, Tier A: blind second readers (round `alc-a-2026-10-27`)

You are an independent **second reader** for Pharmakon (METHODS §5.5). First readers wrote study cards for 37 core
papers on alcohol, and claim writers turned them into 27 draft answers: whether a little drinking is linked to living
longer, the heart and blood vessels, cancer, the liver, deaths caused, alcohol use disorder, withdrawal and its
treatment, and drinking in pregnancy. You check that work against the sources **without seeing their anchors first**.

Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below). Your own folder:
`scratchpad/alc-a/s<N>/` (N = your reader number; create it).

## Read first

1. `docs/VERIFICATION-BRIEF.md` in full: it is your procedure (step 1 blind extraction per claim, step 2 the card check,
   the output format, where to read, the hard rules). Everything in it applies, with the changes below.
2. `docs/METHODS.md` §4.5, §5.3 to §5.5, §6 and §9.
3. `scratchpad/batch5/LEAN-RULES.md` for reading PDFs and web pages economically.

## Changes for this round

- **Round folder** `data/verification/alc-a-2026-10-27/`. Your task files are `tasks/<reference>.json` for the
  references assigned to you below; write `out/<reference>.json` for each, as you go, with
  `"reader": "AI reader <N> (second reader)"`.
- **Cards** for step 2: `data/study-cards/_incoming/alcohol/sc_<reference, hyphens as underscores>.json` (print it with
  python; never edit it).
- **Blindness.** Until your step 1 for a source is finished, do not open that source's card. Never open
  `data/claims/` (any file, including `_incoming/`), `data/site/`, anything in `scratchpad/alc-a/` other than your own
  folder, or any file in the round folder other than this brief, your task files and your own outputs.
- **PDFs** (the senior author's): `/mnt/user-data/uploads/DrugEncyclopedia/` + the task file's `pdf_path`. Extract the
  text yourself (`pdftotext -layout`) into your own folder and render pages (`pdftoppm -r 110`) for tables and figures.
  Cite printed pages. Askgaard et al. (2015) and Mukamal et al. (2020) are online-first PDFs: cite their own page
  numbers as "p. N of the online-first PDF". Mayo-Smith (1997) and Jones et al. (1973) are scanned pages whose
  machine-read text has errors: check every number on the rendered page.
- **Web papers**: PubMed Central (`https://pmc.ncbi.nlm.nih.gov/articles/<PMCID>/`) or, where the task gives no PMCID,
  the DOI link (`https://doi.org/<DOI>`). Load the browser tools with `ToolSearch` (query
  `mcp__remote-devices__Claude_Browser__`, `max_results` 64), make your own tab with `tabs_create` (never
  `preview_start`), pass its tabId on every call, and confirm the page's title is your paper's before you extract.
  Read with `get_page_text` (`max_chars` 120000; read the rest with `javascript_tool` if cut off). Several readers use
  the browser at once: never touch another tab; if your tab shows a page you did not open, leave it and make a new one.
  Never open a PDF or download link, never use a search engine, never interact with a check page (wait a few minutes,
  retry once, otherwise record "not readable"). Two PMC texts are author manuscripts (Roerecke 2012 and 2019): say so in
  `source_read`. Close your tab when you finish. Online supplements are not read: say when a claim's figure can only
  come from one.
- **Numbers.** Check every number in each claim's statement and magnitude that comes from your source. Recompute every
  count, percentage, conversion and "editors' calculation" (for example a relative risk turned into counts out of 100,
  grams a day turned into grams a week, a drink size in grams); say whether you get the same.
- **Comparison groups and units.** For every estimate, check that the claim names the reference group the source used
  (lifetime abstainers, long-term abstainers, current non-drinkers who include former drinkers, occasional drinkers,
  the lowest-intake drinkers) and the units (grams of ethanol a day or a week, the paper's "drink" and its size). A
  wrong or missing reference group is an error, not a matter of wording.
- **Designs.** Model estimates (Global Burden of Disease, attributable deaths and cancers) must be presented as
  estimates from a model, not as counted cases. For genetic (Mendelian randomization) studies, check what the source
  reports about instrument strength and the sensitivity analyses for other pathways. For reviews, check the number of
  studies and participants behind each pooled figure.
- **Wording.** Say whether a claim's wording overstates the source: association presented as effect, one country's
  survey presented as the world, a subgroup presented as everyone, a model estimate presented as a count, "safe" or
  "no risk" where the source does not say it. Also flag any amount that reads as advice on how much to drink, and any
  medicine dose or regimen (claims must have none).
- Report under 250 words: sources done, verdicts other than `supported`, card findings corrected, relocated or not
  found, and anything you could not read.

## Assignments

Task files are in `data/verification/alc-a-2026-10-27/tasks/` (37 sources; each lists only the claims that cite it and
the number and roles of the first reader's anchors from that source).

| Reader | Sources | How to read |
|---|---|---|
| 191 | `stockwell_2024`, `di-castelnuovo_2006`, `mukamal_2020` | PDFs |
| 192 | `rehm_2010`, `askgaard_2015`, `rehm_2009` | PDFs |
| 193 | `carvalho_2019`, `mayo-smith_1997`, `schuckit_2014`, `jonas_2014` | PDFs |
| 194 | `anton_2006`, `jones_1973` | PDFs |
| 195 | `griswold_2018`, `bryazka_2022`, `wood_2018`, `burton_2018`, `chikritzhs_2015` | web (PMC; Burton and Chikritzhs at the publisher) |
| 196 | `stockwell_2016`, `zhao_2023`, `ronksley_2011`, `roerecke_2012`, `roerecke_2014` | web (PMC) |
| 197 | `holmes_2014`, `millwood_2019`, `biddinger_2022`, `larsson_2020` | web (PMC) |
| 198 | `bagnardi_2015`, `rumgay_2021` | web (PMC) |
| 199 | `roerecke_2019`, `popova_2017`, `lange_2017` | web (PMC; Popova at the publisher) |
| 200 | `grant_2015`, `grant_2017`, `amato_2010`, `mcpheeters_2023`, `rosner_2010a`, `rosner_2010b` | web (PMC) |
