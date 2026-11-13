# Cannabis, Tier A: first readers (round `can-a-2026-10-27`)

You are a first reader for Pharmakon, an evidence library about drugs for the public and for people who use drugs.
Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/can-a/r<N>/` (N = your reader number).

The Cannabis page answers questions about smoking and vaping, edibles, strong cannabis, sleep, driving and repeated
vomiting. This round builds the questions people ask most: does cannabis cause psychosis or schizophrenia, does it harm
memory and thinking (now and later), how many people who use it become dependent, and what research shows about its
health effects overall. The papers are the Tier A list in `search-logs/Cannabis_DOI-LIST.md` (read its notes on how the
papers answer each other). You write study cards; other readers write claims from them and blind second readers check
everything.

## Read first

1. `docs/STUDY-CARD-BRIEF.md` in full: it is your procedure. Everything in it applies, with the changes below.
2. `docs/METHODS.md` §4.5, §5 (all of it), §6.2, §9.
3. The exemplar cards named in that brief, and `schema/study-card.schema.json`.

## Changes for this round

- **Folders.** Cards: `data/study-cards/_incoming/cannabis/<card id>.json`. Check existing reference and card ids first
  (the brief gives the command); several cannabis papers already have cards (do not redo them).
- **PDF readers (this page's table).** Your papers are PDFs the senior author saved:
  `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Cannabis/<file>.pdf`; text extractions (pdftotext -layout, pages
  separated by form feeds) are in `scratchpad/can-a/numtext/<file>.txt`. Render a page with `pdftoppm -r 150 -f N -l N
  -png` and look at it whenever a table, figure or garbled text matters. Reference records already exist (ids below):
  use them and do not add reference lines; if a record disagrees with the PDF's first page, say so in your final
  message. Anchors cite the printed page; for an accepted manuscript ("Author's Accepted Manuscript", Gage 2016 and
  Broyd 2016) write "AM p. N" = PDF page, as METHODS §6.2 allows, and say in the card that the version read is the
  accepted manuscript. `source_read`: "PDF PDFs/Cannabis/<file>.pdf" and what you read. Online supplements are not on
  file: say what the paper puts in them and whether a finding depends on them. You do not need the browser.
- **Designs and instruments** (METHODS §5.3): systematic reviews and meta-analyses: AMSTAR 2; narrative reviews,
  monographs, viewpoints and critical overviews: `narrative-review` with the editors' checklist (STUDY-CARD-BRIEF names
  its five domains and the model card). A narrative review is cited for its arguments and pointers, never as primary
  evidence; extract its figures with the primary study each comes from (author, year), so that claim writers can tell
  second-hand figures from first-hand ones, and note when a figure has no citation.
- **Debates.** These papers are on contested questions: whether cannabis causes psychosis or only goes with it
  (confounding, reverse causation, shared genetic liability, rates of schizophrenia over time as cannabis use changed),
  and whether cognitive differences in people who use cannabis come before use, last after stopping, or reflect other
  factors. In each card's `replication.timeline`, name the critiques, replies and genetic or quasi-experimental tests
  the paper itself discusses; use a reference id only if it exists in `data/references/*.json`. Appraise every paper on
  its own methods; neither the "cannabis causes psychosis" reading nor the "it is all confounding" reading gets the
  benefit of the doubt. Record funding and conflicts exactly as printed.
- **Exposure and outcomes.** Record how each source defines cannabis use (ever, weekly, daily, heaviest use; potency),
  the outcome (psychotic symptoms, psychotic disorder, schizophrenia diagnosis; which cognitive tests, after how long
  without cannabis), the comparison group and the adjustment set with every estimate: claims will depend on it.
- No dosing, preparation or administration advice of any kind.

## PDF readers: your papers

| Reader | Reference id: file (in `PDFs/Cannabis/`) |
|---|---|
| 167 | `moore_2007`: Moore_2007_PsychoticAffectiveOutcomesSR.pdf (systematic review with meta-analysis) · `gage_2016`: Gage_2016_EpidemiologicEvidenceReview.pdf (narrative review; accepted manuscript) · `gillespie_2021`: Gillespie_2021_GeneticallyInformedMethods.pdf (viewpoint) · `ksir_2016`: Ksir_2016_CriticalOverviewPsychosis.pdf (critical narrative review) |
| 168 | `hall_2009`: Hall_2009_AdverseHealthEffectsLancet.pdf (narrative review) · `hall_2015`: Hall_2015_TwoDecadesAdverseEffects.pdf (narrative review, monograph) |
| 169 | `curran_2016`: Curran_2016_KeepOffTheGrass.pdf (narrative review) · `broyd_2016`: Broyd_2016_CognitionSR.pdf (systematic review; accepted manuscript) |
| 179 | `page_2020`: Page_2020_AHAStatement.pdf (an American Heart Association scientific statement on cannabis and the heart and blood vessels: file it as `evidence-report` with the editors' evidence-report checklist, or AMSTAR 2 if it states a systematic search for its conclusions, per METHODS §5.3; say which and why) |

Card ids: `sc_` + the reference id (e.g. `sc_moore_2007`). After writing each card, run
`python3 -I scripts/check_card.py <file>` until it passes.

## Browser readers: your papers (free full texts)

These papers are free in PubMed Central or at the publisher; you read them in the app's built-in browser on the senior
author's computer. Load the tools in one call: `ToolSearch` with query `mcp__remote-devices__Claude_Browser__` and
`max_results` 64. Several readers use the browser at once: make your own tab with `tabs_create` (never `preview_start`,
which can hand back a tab another reader is using), then `navigate` it to `https://pmc.ncbi.nlm.nih.gov/articles/<PMCID>/`
or the publisher link, pass its tabId on every call, and confirm the page's title or DOI is your paper's before you
extract. Read with `get_page_text` (`max_chars` 120000; read the rest with `javascript_tool` if cut off). Never touch
another tab, never open a PDF or download link, never interact with a check page, never use a search engine; close your
tab at the end. If your tab ever shows a page you did not open, another reader is using it: leave it alone and make a
new tab. If the
browser cannot be reached, stop and say so. Anchors cite `PMC HTML` or `publisher HTML` with the section, paragraph or
table (STUDY-CARD-BRIEF's locator convention). Append one line per paper to `data/references/_incoming/cannabis.txt`
(`reference_id>DOI>PMCID or publisher`); check existing ids first. If a page links a correction, read it and give its
DOI in your final message.

Designs, beyond the list above: Mendelian randomization and other genetic tests of causation (Gage 2017, Vaucher 2018):
ROBINS-E, design by the data used, `design_detail` beginning "Mendelian randomization", and inside the domains the three
instrument assumptions (strength; no confounding of the instrument; no other path from the variants to the outcome,
with the sensitivity analyses that test it); a genome-wide association study (Pasman 2018): say what it can and cannot
show about cause, and file it as `cross-sectional` with ROBINS-E; case-control studies of first-episode psychosis (Di
Forti 2015, 2019): ROBINS-E; cohort and twin studies (Meier 2012, Jackson 2016, Meier 2018): ROBINS-E; letters with a
reanalysis or simulation (Rogeberg 2013, Moffitt 2013): `modelling` for a simulation, or the design of the data
reanalysed, and say which and why; systematic reviews and meta-analyses: AMSTAR 2.

| Reader | Papers (DOI; where to read) |
|---|---|
| 184 | Marconi et al. (2016) (10.1093/schbul/sbw003; PMC4988731) · Di Forti et al. (2019) (10.1016/S2215-0366(19)30048-3; PMC7646282) · Di Forti et al. (2015) (10.1016/S2215-0366(14)00117-5; https://doi.org/10.1016/S2215-0366(14)00117-5) |
| 185 | Gage et al. (2017) (10.1017/S0033291716003172; PMC5341491) · Vaucher et al. (2018) (10.1038/mp.2016.252; PMC5984096) · Pasman et al. (2018) (10.1038/s41593-018-0206-1; PMC6386176) |
| 186 | Meier et al. (2012) (10.1073/pnas.1206820109; PMC3479587) · Rogeberg (2013) (10.1073/pnas.1215678110; PMC3600466) · Moffitt et al. (2013) (10.1073/pnas.1300618110; PMC3600438) · Jackson et al. (2016) (10.1073/pnas.1516648113; PMC4747759) |
| 187 | Meier et al. (2018) (10.1111/add.13946; PMC5760333) · Scott et al. (2018) (10.1001/jamapsychiatry.2018.0335; PMC6137521) · Gobbi et al. (2019) (10.1001/jamapsychiatry.2018.4500; PMC6450286) |
| 188 | Volkow et al. (2014) (10.1056/NEJMra1402309; PMC4827335) · Connor et al. (2021) (10.1038/s41572-021-00247-4; PMC8655458) · Murray et al. (2016) (10.1002/wps.20341; PMC5032490) |
| 189 | Huestis (2007) (10.1002/cbdv.200790152; PMC2689518) · Bahji et al. (2020) (10.1001/jamanetworkopen.2020.2370; PMC7146100) · Sorensen et al. (2017) (10.1007/s13181-016-0595-z; PMC5330965) |
| 190 | Gunn et al. (2016) (10.1136/bmjopen-2015-009986; PMC4823436) · Whiting et al. (2015) (10.1001/jama.2015.6358; https://doi.org/10.1001/jama.2015.6358; JAMA sometimes shows a check page: wait a few minutes, try once more, otherwise report it not readable) |

## Final message

Under 200 words: each card written; for each, two lines on what the full text changed compared with the abstract or
its reputation; anything the claim writers must know (second-hand figures, definitions that differ between sources).
