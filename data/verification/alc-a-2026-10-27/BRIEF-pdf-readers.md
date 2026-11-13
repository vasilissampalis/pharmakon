# Alcohol, Tier A: first readers of the senior author's PDFs (round `alc-a-2026-10-27`)

You are a first reader for Pharmakon. Read `data/verification/alc-a-2026-10-27/BRIEF-first-readers.md` first: everything
in it applies to you (procedure, designs and instruments, debates, exposure units, outputs, rules), except where this
page says otherwise. Your own folder is `scratchpad/alc-a/r<N>/` under
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/`.

## What is different for you

- **Your papers are PDFs** the senior author saved: `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Alcohol/<file>.pdf`.
  Text extractions (pdftotext -layout, pages separated by form feeds) are in `scratchpad/alc-a/numtext/<file>.txt`.
  Render a page with `pdftoppm -r 150 -f N -l N -png` and look at it whenever a table, figure or garbled text matters.
  You do not need the browser: do not open it.
- **Reference records already exist** (built from Crossref, ids below): use these ids, do not add lines to
  `data/references/_incoming/alcohol.txt`. If a record disagrees with the PDF's first page (authors, year, title,
  journal, volume, pages), say so in your final message; do not edit references.
- **Anchors** cite the printed page (METHODS §6.2). If a PDF's page numbers differ from the record's pages (for example
  an online-first version), cite the PDF's own printed numbers and add "of the online-first PDF", and say so in your
  final message (the editor records it in `data/access/pdf-page-basis.json`). `source_read` on every anchor and on the
  card: "PDF PDFs/Alcohol/<file>.pdf" followed by what you read (all text, which tables and figures, supplements not
  read). Online supplements are not on file: say what the paper puts in them and whether a finding depends on them.
- After writing each card, also run `python3 -I scripts/check_card.py <file>`.
- **Mayo-Smith (1997)** is a scanned page with machine-read text: the extraction contains character errors. Check every
  number on the rendered page.

## Your papers

| Reader | Reference id: file (in `PDFs/Alcohol/`) |
|---|---|
| 162 | `stockwell_2024`: Stockwell_2024_CohortBiasLowVolumeMA.pdf · `di-castelnuovo_2006`: DiCastelnuovo_2006_AlcoholDosingTotalMortalityMA.pdf · `mukamal_2020`: Mukamal_2019_MRCritique.pdf |
| 163 | `rehm_2010`: Rehm_2010_CirrhosisMA.pdf · `askgaard_2015`: Askgaard_2015_DrinkingPatternCirrhosisCohort.pdf · `rehm_2009`: Rehm_2009_GlobalBurdenEconomicCost.pdf |
| 164 | `carvalho_2019`: Carvalho_2019_LancetSeminarAUD.pdf · `mayo-smith_1997`: MayoSmith_1997_WithdrawalPharmacologyMA.pdf |
| 165 | `jonas_2014`: Jonas_2014_PharmacotherapyAUD_MA.pdf; then `schuckit_2014`: Schuckit_2014_WithdrawalDelirium.pdf |
| 166 | `anton_2006`: Anton_2006_COMBINE.pdf (a randomized trial: RoB 2, with the registration, primary outcomes as registered and reported, and attrition by arm) · `jones_1973`: Jones_1973_PatternOfMalformation.pdf (a case series: design `case-series`, no instrument, the card states the design's limits; scanned page with machine-read text, check every number on the rendered page) |

Card ids follow the rule in `docs/STUDY-CARD-BRIEF.md` (`sc_` + the reference id with hyphens as underscores, e.g.
`sc_di_castelnuovo_2006`). Designs, as the main brief says: Mukamal et al. (2020) is an essay (`narrative-review`, the
editors' checklist); Carvalho et al. (2019) is a Lancet Seminar (`narrative-review`); Rehm et al. (2009) estimates
attributable burden and cost (`modelling`); Mayo-Smith (1997) is a meta-analysis with a practice guideline (AMSTAR 2 for
the meta-analysis; report the guideline's recommendations only as what it recommended, without regimens or doses).
