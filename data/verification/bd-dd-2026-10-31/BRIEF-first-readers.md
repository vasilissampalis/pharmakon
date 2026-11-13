# Before, during and after use; how drug deaths are counted: first readers (round `bd-dd-2026-10-31`)

You are a first reader for Pharmakon, an evidence library about drugs for the public and for people who use drugs.
Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/bd-dd/r<N>/` (N = your reader number; create it).

The senior author asked for two new parts of the site (31 October 2026):

- **Before, during and after use**: what research says people do before and during use to reduce harms or make the
  experience go better (preparation, mood and expectations, the place and the people, music, food, water and cooling,
  breaks, other drugs and supplements taken alongside), whether it worked, and what predicts a good or a difficult
  experience. Findings only: no amounts, timings or regimens as advice, nothing on making effects stronger. List:
  `search-logs/BeforeDuring_DOI-LIST.md`.
- **How drug deaths are counted**: how deaths are defined, investigated, certified, coded and counted, what a blood level
  after death can and cannot show, and how far the counts can be trusted in both directions (deaths wrongly put down to
  a drug, and drug deaths that are missed). List: `search-logs/DrugDeaths_DOI-LIST.md`.

You write study cards; other readers write the answers from them and blind second readers check everything.

## Read first

1. `docs/STUDY-CARD-BRIEF.md` in full: it is your procedure. Everything in it applies, with the changes below.
2. `docs/METHODS.md` §4.5, §5 (all of it, including the table of designs and instruments in §5.3), §6.2, §9.
3. The exemplar cards named in that brief and `schema/study-card.schema.json`.
4. The notes on your papers in the two lists above (each row says why the paper is there and what to read it with).

## Reading in the app's browser (all your papers are free full texts)

Reference records already exist (ids below; `data/references/before-during.json` and `drug-deaths.json`): use them,
add no reference lines, and say in your final message if a record disagrees with the article page. Load the browser
tools in one call: `ToolSearch` with query `mcp__remote-devices__Claude_Browser__` and `max_results` 64. Several readers
use the browser at once: make **one** tab of your own with `tabs_create` (never `preview_start`), `navigate` it to
`https://pmc.ncbi.nlm.nih.gov/articles/<PMCID>/` or to `https://doi.org/<DOI>` for a publisher page, pass its tabId on
every call, and confirm the page's title or DOI is your paper's before you extract. Read with `get_page_text`
(`max_chars` 120000; read the rest with `javascript_tool` if it is cut off). Never touch another tab, never open a PDF or
download link, never use a search engine, never interact with a check page or CAPTCHA (wait a few minutes, try once
more, otherwise report the paper **not readable** and move on); close your tab at the end. If your tab ever shows a page
you did not open, leave it alone and make a new tab. If the browser cannot be reached, stop and say so. A value printed
only in a figure image needs a screenshot of your tab; if the screenshot comes back blank (the pane is hidden on the
senior author's computer), say "figure image not viewable" and do not guess. Anchors cite `PMC HTML` or
`publisher HTML` with the section and running-text paragraph, table or figure; `source_read`: "PMC full text <PMCID>"
or "publisher full text (HTML), <journal>". If a page links a correction, erratum, comment or reply, read it if it is
free and give its DOI in your final message; say what online supplements hold and whether a finding depends on them.

## Changes for this round

- **Folders.** Cards: `data/study-cards/_incoming/<substance>/<card id>.json`, with `substance` the drug folder named in
  the table below (`cross-cutting` for papers about several drugs). Card ids: `sc_` + the reference id with hyphens as
  underscores. After writing each card, run `python3 -I scripts/check_card.py <file>` until it passes.
- **Designs and instruments** (METHODS §5.3): systematic reviews and meta-analyses, AMSTAR 2; scoping reviews and
  narrative reviews, `narrative-review` with the editors' five-domain checklist (instrument `none-applicable`; a scoping
  review that maps without appraising is never rated as if it were a systematic review); evidence reports and statistics
  by public bodies (for example an NCHS report), `evidence-report` with `editors-report`; consensus and position papers
  of professional bodies, `narrative-review` with the editors' checklist, saying who wrote them and on what evidence;
  surveys and record-linkage or certificate studies, the JBI prevalence checklist or ROBINS-E as STUDY-CARD-BRIEF
  says; randomized laboratory studies, RoB 2; mixed-methods studies: appraise the quantitative part with its instrument
  and describe the qualitative part.
- **Deaths: what was counted, and by whom.** For every count of deaths say exactly how a death entered it (the ICD-10
  codes, "drug mentioned" on the certificate, toxicology found, the coroner's or medical examiner's conclusion, a
  register's own definition), who decided (a pathologist, a coroner, a medical examiner, a statistician), what was
  tested and in what share of deaths, and what the comparison was (for example an enhanced-surveillance review, a second
  register). When a paper reports that a drug was "involved" or "present", keep that word: never turn presence into
  cause. Report both directions where the paper does (overcounting and undercounting).
- **Before and during: findings, not advice.** Report preparations, settings, music, food, supplements and other drugs
  exactly as the study gave or measured them, inside the card's description of what was done, with who took part
  (healthy volunteers, patients, people who use drugs outside a laboratory) and where (laboratory, clinic, ceremony,
  festival, home). Never write anything that reads as advice on amounts, timing, routes or combinations, or on making a
  drug's effects stronger. For predictors of a "good" or "difficult" experience, say how the experience was measured
  (which questionnaire, rated when, by whom) and whether the predictor was measured before the drug.
- Record funding and conflicts exactly as printed.

## Your papers

| Reader | Reference id (substance): where to read it |
|---|---|
| 246 | `aday_2021` (cross-cutting): PMC8033773 · `haijen_2018` (cross-cutting): PMC6225734 · `studerus_2021` (mdma): PMC8155734 · `vizeli_2024` (lsd): PMC11374807 |
| 247 | `simonsson_2023` (cross-cutting): PMC9974873 · `wood_2024` (cross-cutting): PMC11582610 · `piercey_2024` (cross-cutting): PMC11658379 · `palmer_2022` (cross-cutting): PMC9310449 · `perkins_2021` (dmt-ayahuasca): PMC8097729 |
| 248 | `kaelen_2018` (cross-cutting): PMC5893695, with its correction (10.1007/s00213-018-4886-8) · `kheirkhah_2024` (ketamine): PMC13179047 · `zamarripa_2023` (cannabis): PMC9926328 · `jones_1997` (alcohol): PMC2042884 |
| 249 | `pearson_2013` (alcohol): PMC3844112 · `morrison_2025` (benzodiazepines): PMC12502574 · `papamihali_2020` (heroin): PMC7682134 · `klevebrant_2022` (caffeine): publisher, https://doi.org/10.1016/j.genhosppsych.2021.11.005 |
| 250 | `beynon_2007` (cross-cutting): PMC1976310 · `goldberger_2013` (cross-cutting): PMC3805449 · `garnett_2026` (cross-cutting): PMC12989908 · `slavova_2015` (cross-cutting): PMC4547584 · `slavova_2019` (cross-cutting): PMC6559129 |
| 251 | `gutkind_2025` (cross-cutting): PMC11916924 · `buchanich_2018` (cross-cutting): PMC6055296 · `horon_2018` (cross-cutting): PMC5944879 · `chen_2025` (cross-cutting): publisher, https://doi.org/10.1016/j.drugpo.2025.104976 |
| 252 | `davis_2020` (cross-cutting): publisher, https://doi.org/10.1097/paf.0000000000000550 · `lundberg_2026` (cross-cutting): PMC13623016 · `quesinberry_2019` (cross-cutting): PMC8351054 · `ferner_2008` (cross-cutting): PMC2561112, with Ritter's comment (PMC2561124) · `launiainen_2014` (cross-cutting): PMC4237191 |
| 253 | `strommer_2020` (cross-cutting): PMC7669776, with its published critiques and the replies named in its row of the list (read the free ones) · `goncalves-dias_2026` (cross-cutting): publisher, https://doi.org/10.1016/j.jflm.2026.103200 · `sumnall_2023` (cross-cutting): publisher, https://doi.org/10.1016/j.drugpo.2022.103909 |

## Final report (your last message)

As STUDY-CARD-BRIEF says: for each paper the card file written (or "not readable" with the reason), and two or three
lines on what the full text changed compared with its abstract; then the reporting issues that matter for the answers,
and every correction, comment or reply you found, with its DOI. Under 300 words.
