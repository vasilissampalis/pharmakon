# Cocaine, Tier A: first readers (round `coc-a-2026-10-27`)

You are a first reader for Pharmakon, an evidence library about drugs for the public and for people who use drugs.
Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/coc-a/r<N>/` (N = your reader number; create it).

The Cocaine page so far answers questions about the crash after a binge and the first weeks after stopping. This round
builds its core: how cocaine moves through the body by route, powder against crack (dependence and health), chest pain
and heart attacks and how emergency departments treat them, adulterants such as levamisole, cocaine with alcohol
(cocaethylene), memory and thinking, stroke, deaths and treatment. The papers are the Tier A list in
`search-logs/Cocaine_DOI-LIST.md` (read its notes). You write study cards; other readers write claims from them and blind
second readers check everything.

## Read first

1. `docs/STUDY-CARD-BRIEF.md` in full: it is your procedure. Everything in it applies, with the changes below.
2. `docs/METHODS.md` §4.5, §5 (all of it), §6.2, §9.
3. The exemplar cards named in that brief, `schema/study-card.schema.json`, and as a model for a laboratory study of
   a drug's effects and its blood levels, the card `sc_harris_2003` in `data/study-cards/methamphetamine.json`.

## Changes for this round

- **Folders.** Cards: `data/study-cards/_incoming/cocaine/<card id>.json`. Check existing card ids first (the brief
  gives the command); the Cocaine page already has cards, so do not redo one that exists. Reference records already
  exist for the papers in "Your papers" (ids given): use them and do not add reference lines; if a record disagrees with
  the PDF's first page (authors, year, title, journal, volume, pages), say so in your final message.
- **PDFs** the senior author saved: `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Cocaine/<file>.pdf`; text extractions
  (pdftotext -layout, pages separated by form feeds) in `scratchpad/coc-a/numtext/<file>.txt`. Older papers are scanned
  pages with machine-read text: check every number on the rendered page (`pdftoppm -r 150 -f N -l N -png`, then look at
  it). Anchors cite the printed page; if a PDF's page numbers differ from the record's (an online-first version, a cover
  page, a whole journal section), cite the printed numbers and say so in your final message. `source_read`: "PDF
  PDFs/Cocaine/<file>.pdf" and what you read (all text, which tables and figures, supplements not read). Online
  supplements are not on file: say what the paper puts in them and whether a finding depends on them. You do not need
  the browser.
- **Designs and instruments** (METHODS §5.3): controlled laboratory studies in volunteers, including blood-level
  (pharmacokinetic) and self-administration studies: `human-laboratory`, RoB 2, as on the model card; randomized trials:
  RoB 2 with the registration (if any), the primary outcomes as registered and reported, and attrition by arm;
  systematic reviews and meta-analyses: AMSTAR 2; national surveys: `cross-sectional` with the JBI prevalence checklist
  for prevalence, ROBINS-E for associations; cohorts and case-control studies: ROBINS-E; emergency-department case
  series: `case-series`, no instrument, the card states the design's limits; narrative reviews, scientific statements
  and overviews: `narrative-review` with the editors' checklist (a statement that describes a systematic search for its
  conclusions: AMSTAR 2; say which and why). Say for each laboratory study whether order was randomized or
  counterbalanced, whether participants and staff were blind, and who took part (people who already used cocaine, their
  route of use, people seeking or not seeking treatment).
- **Doses only as study conditions.** Report the doses, routes and blood levels exactly as the study gave or measured
  them, inside the card's description of what was done; never write anything that reads as advice on amounts, routes,
  timing, combinations or ways of using cocaine.
- **Powder and crack.** Record how each source defines its exposure (powder cocaine hydrochloride, crack or freebase,
  route: snorted, smoked, injected), the outcome, the comparison group and the adjustment set with every estimate, and
  whether a difference between powder and crack is tested or only described. Name the population and years of every
  survey.
- Record funding and conflicts exactly as printed.

## Your papers

| Reader | Reference id: file (in `PDFs/Cocaine/`) |
|---|---|
| 238 | `chen_2004`: Chen_2004_PowderVersusCrackDependenceRisk.pdf (national survey data: cross-sectional; JBI for prevalence, ROBINS-E for associations) · `hatsukami_1996`: Hatsukami_1996_CrackVersusCocaineHCl.pdf (review in JAMA: narrative review with the editors' checklist, or AMSTAR 2 if it describes a systematic search; say which) · `butler_2017`: Butler_2017_CrackHealthOutcomesSRMA.pdf (systematic review and meta-analysis: AMSTAR 2; 82 pages: check whether it is the accepted manuscript or the journal version and cite pages accordingly) |
| 239 | `barnett_1981`: Barnett_1981_CocainePKHumans.pdf (blood-level study: human-laboratory, RoB 2; scanned pages) · `evans_1996`: Evans_1996_ArterialVenousPKRoute.pdf (laboratory study of smoked and injected cocaine: human-laboratory, RoB 2; scanned with no text layer: its text in `numtext/` is the editor's OCR and has errors, so read every number on the rendered page) |

Card ids: `sc_` + the reference id (e.g. `sc_chen_2004`). After writing each card, run
`python3 -I scripts/check_card.py <file>` until it passes.

## Final message

Under 200 words: each card written; for each, two lines on what the full text changed compared with its abstract;
anything the claim writers must know (study conditions that limit what a claim can say, scanned pages, version read).
