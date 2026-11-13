# Before and during use; how drug deaths are counted: blind second readers (round `bd-dd-2026-10-31`)

You are an independent **second reader** for Pharmakon (METHODS §5.5). First readers wrote study cards for the papers
of two new parts of the site (what people do before and during use, and what predicts a good or a difficult
experience; how drug deaths are defined, investigated, certified and counted). Claim writers have turned the
before-and-during cards into draft answers; the drug-death cards have no answers yet. You check that work against the
sources **without seeing the anchors first**.

Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below). Your own folder:
`scratchpad/bd-dd/s<N>/` (N = your reader number; create it).

## Read first

1. `docs/VERIFICATION-BRIEF.md` in full: it is your procedure (step 1 blind extraction per claim, step 2 the card check,
   the output format, where to read, the hard rules). Everything in it applies, with the changes below.
2. `docs/METHODS.md` §4.5, §5.3 to §5.5, §6 and §9.
3. `scratchpad/batch5/LEAN-RULES.md` for reading web pages economically.

## Changes for this round

- **Round folder** `data/verification/bd-dd-2026-10-31/`. Your task files are `tasks/<reference>.json` for the
  references assigned to you below; write `out/<reference>.json` for each, as you go, with
  `"reader": "AI reader <N> (second reader)"`. A task with an empty claim list is a card check only (step 2).
- **Cards** for step 2: `data/study-cards/_incoming/<folder>/sc_<reference, hyphens as underscores>.json` (print it with
  python; never edit it).
- **Blindness.** Until your step 1 for a source is finished, do not open that source's card. Never open
  `data/claims/` (any file, including `_incoming/`), `data/site/`, anything in `scratchpad/bd-dd/` or `scratchpad/gen-a/`
  other than your own folder, or any file in the round folder other than this brief, your task files and your own
  outputs.
- **Every source is a web page** (PubMed Central, `https://pmc.ncbi.nlm.nih.gov/articles/<PMCID>/`, or the DOI link
  where the task gives no PMCID). Load the browser tools with `ToolSearch` (query `mcp__remote-devices__Claude_Browser__`,
  `max_results` 64), make your own tab with `tabs_create` (never `preview_start`), pass its tabId on every call, and
  confirm the page's title is your paper's before you extract. Read with `get_page_text` (`max_chars` 120000; read the
  rest with `javascript_tool` if cut off). Several readers use the browser at once: never touch another tab; if your tab
  shows a page you did not open, leave it and make a new one. Never open a PDF or download link, never use a search
  engine, never interact with a check page or CAPTCHA (wait a few minutes, retry once, otherwise record "not
  readable"). A value printed only in a figure needs a screenshot of your tab; if it comes back blank, say "figure
  image not viewable" and do not guess. If the browser cannot be reached, wait about 3 minutes and try once more; if it
  still fails, stop and report which sources remain. Close your tab when you finish. Online supplements are not read:
  say when a claim's figure can only come from one.
- **Numbers.** Check every number in each claim's statement and magnitude that comes from your source; recompute every
  count, percentage, correlation-to-plain-words conversion and "editors' calculation".
- **What these topics need checked.** For a predictor of an experience: which questionnaire, rated when and by whom,
  and whether the predictor was measured before the drug or recalled afterwards at the same sitting. Who took part
  (healthy volunteers, patients, people using on their own) and where. For a count of deaths: how a death entered it
  (codes, "drug mentioned", toxicology, the certifier's conclusion), who decided, what was tested and in what share of
  deaths, and the comparison; "involved" or "present" must never become "caused".
- **Wording.** Say whether a claim overstates the source (association as effect, a recalled attribution as a
  predictor, a self-selected sample as representative, a review's citation as its finding). Flag anything that reads as
  advice on amounts, timing, routes or combinations, or on making a drug's effects stronger.
- Report under 250 words: sources done, verdicts other than `supported`, card findings corrected, relocated or not
  found, and anything you could not read.

## Assignments

Task files are in `data/verification/bd-dd-2026-10-31/tasks/` (28 sources; each lists only the claims that cite it and
the number and roles of the first anchors from that source; an empty list means a card check only).

| Reader | Sources | Kind |
|---|---|---|
| 268 | `simonsson_2023`, `wood_2024`, `piercey_2024` | claims and cards |
| 269 | `haijen_2018`, `aday_2021`, `vizeli_2024`, `studerus_2021` | claims and cards |
| 270 | `palmer_2022`, `perkins_2021`, `kaelen_2018` (with its correction, 10.1007/s00213-018-4886-8), `kheirkhah_2024` | claims and cards |
| 271 | `zamarripa_2023`, `pearson_2013`, `morrison_2025`, `papamihali_2020` | claims and cards |
| 272 | `beynon_2007`, `goldberger_2013`, `garnett_2026`, `slavova_2015` | cards only (drug deaths) |
| 273 | `slavova_2019`, `gutkind_2025`, `buchanich_2018`, `horon_2018` | cards only (drug deaths) |
| 274 | `lundberg_2026`, `quesinberry_2019`, `ferner_2008` (with Ritter's comment, PMC2561124) | cards only (drug deaths) |
| 275 | `launiainen_2014`, `strommer_2020` (with the free critiques and replies its card names) | cards only (drug deaths) |
