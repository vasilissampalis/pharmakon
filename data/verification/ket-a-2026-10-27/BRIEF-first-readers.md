# Ketamine, Tier A: first readers (round `ket-a-2026-10-27`)

You are a first reader for Pharmakon, an evidence library about drugs for the public and for people who use drugs.
Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/ket-a/r<N>/` (N = your reader number).

The Ketamine page has no answers yet. This round starts its core: what ketamine does to perception, thinking and memory
in controlled studies, how it moves through the body by route, and what is known about its harms (more papers on
bladder damage, longer-term thinking and memory, deaths and depression treatment follow). The papers are the Tier A list
in `search-logs/Ketamine_DOI-LIST.md` (read its notes). You write study cards; other readers write claims from them and
blind second readers check everything.

## Read first

1. `docs/STUDY-CARD-BRIEF.md` in full: it is your procedure. Everything in it applies, with the changes below.
2. `docs/METHODS.md` §4.5, §5 (all of it), §6.2, §9.
3. The exemplar cards named in that brief, `schema/study-card.schema.json`, and as a model for a laboratory study of
   a drug's effects and its blood levels, the card `sc_harris_2003` in `data/study-cards/methamphetamine.json`.

## Changes for this round

- **Folders.** Cards: `data/study-cards/_incoming/ketamine/<card id>.json`. Reference records already exist (ids
  below): use them and do not add reference lines; if a record disagrees with the PDF's first page, say so in your final
  message.
- **PDFs** the senior author saved: `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Ketamine/<file>.pdf`; text extractions
  (pdftotext -layout, pages separated by form feeds) in `scratchpad/ket-a/numtext/<file>.txt`. Several are old scanned
  pages with machine-read text (Krystal 1994, Malhotra 1996 and others with few fonts): check every number on the
  rendered page (`pdftoppm -r 150 -f N -l N -png`, then look at it). Anchors cite the printed page; if a PDF's page
  numbers differ from the record's (an online-first version, for example Peltoniemi 2016), cite the PDF's own numbers
  with "of the online-first PDF" and say so in your final message. `source_read`: "PDF PDFs/Ketamine/<file>.pdf" and
  what you read. You do not need the browser.
- **Designs and instruments** (METHODS §5.3): controlled laboratory studies in volunteers, including blood-level
  (pharmacokinetic) studies and placebo-controlled challenge studies: `human-laboratory`, RoB 2, as on the model card;
  narrative reviews and overviews: `narrative-review` with the editors' checklist. Say for each laboratory study whether
  order was randomized or counterbalanced, whether participants and raters were blind (ketamine's effects make blinding
  hard: say what the paper did and reported), and who took part (healthy volunteers, prior drug experience, patients).
- **Doses only as study conditions.** Report the doses, routes, infusion schedules and blood levels exactly as the study
  gave or measured them, inside the card's description of what was done; never write anything that reads as advice on
  amounts, routes, timing, combinations or ways of using ketamine.
- **What the measures are.** Name each rating scale and test (for example BPRS, CADSS, word recall), what it measures,
  and whether effects were measured during the infusion or after it; separate effects in healthy volunteers from effects
  in patients, and short-lived effects during a session from lasting ones.
- Record funding and conflicts exactly as printed.

## Your papers

| Reader | Reference id: file (in `PDFs/Ketamine/`) |
|---|---|
| 175 | `krystal_1994`: Krystal_1994_SubanestheticEffectsHumans.pdf · `malhotra_1996`: Malhotra_1996_NMDAHumanCognition.pdf · `newcomer_1999`: Newcomer_1999_NMDAHypofunctionModel.pdf |
| 176 | `vollenweider_1997a`: Vollenweider_1997a_SRKetaminePET.pdf · `vollenweider_1997b`: Vollenweider_1997b_HyperfrontalityPET.pdf |
| 177 | `clements_1982`: Clements_1982_BioavailabilityPK.pdf · `yanagihara_2003`: Yanagihara_2003_PKByPreparation.pdf · `peltoniemi_2016`: Peltoniemi_2016_ClinicalPKPDReview.pdf (narrative review) |
| 178 | `morgan_2012`: Morgan_2012_KetamineUseReview.pdf (overview for the Independent Scientific Committee on Drugs: narrative review) |
| 180 | `lahti_1995`: Lahti_1995_KetaminePsychosisSchizophrenia.pdf (challenge study in people with schizophrenia; scanned, the machine-read text misspells names) · `ait-bentaleb_2024`: AitBentaleb_2023_NeuroimagingMetaAnalysis.pdf (meta-analysis: AMSTAR 2; online 2023, print 2024) |
| 181 | `curran_2000`: Curran_2000_RecreationalUsersNightAnd3Days.pdf · `curran_2001`: Curran_2001_InAndOutOfTheKHole.pdf (studies of people who use ketamine outside a laboratory: observational, ROBINS-E; say exactly what was measured when, against which comparison group, and how ketamine use and other drug use were established) |
| 182 | `morgan_2004a`: Morgan_2004a_BeyondTheKHole3Year.pdf · `morgan_2009`: Morgan_2009_FrequentInfrequentExUsers.pdf · `morgan_2010b`: Morgan_2010_OneYearLongitudinal.pdf (observational, ROBINS-E). Morgan et al. (2010) has a published erratum (doi 10.1111/j.1360-0443.2010.02984.x, Addiction 105(4), 766), free on the publisher's page: open https://onlinelibrary.wiley.com/doi/10.1111/j.1360-0443.2010.02984.x in a browser tab of your own (load the tools with ToolSearch, query `mcp__remote-devices__Claude_Browser__`, `max_results` 64; make the tab with `tabs_create`, never `preview_start`; pass its tabId on every call; `get_page_text`; never touch any other tab, never a PDF or download link; close your tab), and record on the card what it corrects and whether your extracted numbers are the corrected ones |
| 183 | `shahani_2007`: Shahani_2007_UlcerativeCystitisNewEntity.pdf (case series: no instrument, the card states the design's limits) · `winstock_2012`: Winstock_2012_UrinarySymptomsPrevalence.pdf (survey: JBI prevalence checklist) · `schifano_2008`: Schifano_2008_KHoleDeathsUK.pdf (a letter describing deaths from a national register: design `registry`, no instrument; the PDF holds the journal's whole letters section, printed pp. 101–122, and this letter is pp. 114–116, PDF pp. 14–16: cite the printed pages) |
| 237 | (batch 5, 31 October) `berman_2000`: Berman_2000_AntidepressantEffects.pdf (randomized crossover trial: RoB 2) · `anand_2023`: Anand_2023_KetamineVsECT.pdf (randomized trial: RoB 2) · `short_2018`: Short_2018_SideEffectsSR.pdf (systematic review: AMSTAR 2) · `turner_2019`: Turner_2019_EsketamineSevenConcerns.pdf (commentary: narrative review) · `horowitz_2021`: Horowitz_2021_RepeatingMistakesEsketamine.pdf (critique: narrative review; the PDF is the 2020 online-first version, "Page N of 4": cite those pages and say so; its corrigendum, 10.1192/bjp.2021.40, is free at the publisher: read it in the app's browser as the browser readers below do, and record what it corrects) |

Card ids: `sc_` + the reference id (e.g. `sc_vollenweider_1997a`). After writing each card, run
`python3 -I scripts/check_card.py <file>` until it passes.

## Browser readers: your papers (free full texts)

These papers are free in PubMed Central or at the publisher; you read them in the app's built-in browser on the senior
author's computer. They have no reference records yet: append one line per paper to
`data/references/_incoming/ketamine.txt` (`reference_id>DOI>PMCID or publisher`; check existing ids in
`data/references/*.json` first and use the id given below) and set `source_read` to "PMC full text <PMCID>" or
"publisher full text (HTML), <journal>". Load the tools in one call: `ToolSearch` with query
`mcp__remote-devices__Claude_Browser__` and `max_results` 64. Several readers use the browser at once: make your own tab
with `tabs_create` (never `preview_start`, which can hand back a tab another reader is using), then `navigate` it to
`https://pmc.ncbi.nlm.nih.gov/articles/<PMCID>/` or the DOI link, pass its tabId on every call, and confirm the page's
title or DOI is your paper's before you extract. Read with `get_page_text` (`max_chars` 120000; read the rest with
`javascript_tool` if cut off). Never touch another tab, never open a PDF or download link, never use a search engine,
never interact with a check page (JAMA Network and psychiatryonline.org sometimes show one: wait a few minutes, try once
more, otherwise report the paper not readable); close your tab at the end. If your tab ever shows a page you did not
open, another reader is using it: leave it alone and make a new tab. If the browser cannot be reached, stop and say so.
Anchors cite `PMC HTML` or `publisher HTML` with the section, paragraph or table (STUDY-CARD-BRIEF's locator
convention). If a page links a correction or erratum, read it and give its DOI in your final message. Online
supplements: say what the paper puts in them and whether a finding depends on them.

Designs, beyond the list above: randomized trials (including crossover trials and trials with an active placebo such
as midazolam): RoB 2, with the registration, the primary outcomes as registered and as reported, attrition by arm, and
how the authors handled the unblinding that ketamine's effects cause; systematic reviews and meta-analyses: AMSTAR 2;
commentaries and critiques: `narrative-review` with the editors' checklist; case series of patients: `case-series`, no
instrument, the card states the design's limits; national death registers and coronial databases: `registry`, no
instrument. For trials of ketamine or esketamine for depression, record each outcome exactly as defined (scale,
response, remission, change score), when it was measured (hours, days, weeks after the first dose), the comparison, the
sponsor's role, and funding and conflicts exactly as printed. Doses only as study conditions, as above.

| Reader | Papers (reference id: DOI; where to read) |
|---|---|
| 203 | `chu_2008`: 10.1111/j.1464-410x.2008.07920.x (publisher) · `chan_2022`: 10.12809/hkmj209194 (publisher) · `corkery_2021`: 10.1177/02698811211021588 (PMC8600594) · `darke_2021`: 10.1111/add.15154 (publisher) |
| 204 | `zarate_2006`: 10.1001/archpsyc.63.8.856 (publisher) · `murrough_2013`: 10.1176/appi.ajp.2013.13030392 (PMC3992936) · `daly_2018`: 10.1001/jamapsychiatry.2017.3739 (PMC5838571) · `popova_2019`: 10.1176/appi.ajp.2019.19020172 (publisher) |
| 205 | `schatzberg_2019`: 10.1176/appi.ajp.2019.19040423 (publisher) · `dean_2021`: 10.1002/14651858.cd011612.pub3 (PMC8434915; a long Cochrane review: read the summary of findings, results and discussion in full, and the characteristics tables for the trials the results rest on) · `nikolin_2023`: 10.1016/j.eclinm.2023.102127 (PMC10430179) |
| 206 | `zanos_2018`: 10.1124/pr.117.015198 (PMC6020109; a long pharmacology review: narrative review; extract what it says about human pharmacokinetics, metabolites and receptor actions, each with the primary study cited; check the journal page for a correction notice) · `beck_2020`: 10.1001/jamanetworkopen.2020.4693 (PMC7243091) |

## Final message

Under 200 words: each card written; for each, two lines on what the full text changed compared with its abstract;
anything the claim writers must know (study conditions that limit what a claim can say, scanned pages, version read).
