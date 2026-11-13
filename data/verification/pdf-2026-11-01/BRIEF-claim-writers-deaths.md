# How drug deaths are counted: claim writers (round `pdf-2026-11-01`)

You write graded answers (claims) for Pharmakon, an evidence library about drugs for the public and for people who use
drugs. Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/pdf1101/w<N>/` (N = your reader number; create it).

## The task

The senior author asked for a critical, realistic account of drug deaths (decision `p-death-counts` in
`data/site/decisions.json`): how deaths are certified, coded and counted; what a drug level after death can and cannot
show; who investigates deaths and with what resources; deaths put down to a drug that was only present; and drug deaths
that are missed. **Both directions**, so the picture is neither frightening nor dismissive, every point graded like any
other answer. First readers have written study cards from the full texts (`search-logs/DrugDeaths_DOI-LIST.md` explains
why each paper is there). You turn the cards into claims (WORKFLOW step 7), one claim per question a person would ask.
Blind second readers will re-find your evidence in the sources, so every number must be right and anchored.

## Read first (only these parts)

1. `scratchpad/batch5/LEAN-RULES.md`: follow it.
2. `docs/WRITING-RULES.md`: Rule 0 and Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/METHODS.md` §6 (all of it), §7 (debate box), §8 (the section numbers), §9 (language), §5.5 point 1.
4. `data/verification/pdf-2026-11-01/BRIEF-first-readers.md`, "What to record, by part" → "Deaths": the same points must
   reach the claims.
5. Models, printed by id with `json.load` (never read whole files): `cl_mdma_deaths_medicines` (`data/claims/mdma.json`,
   deaths in coroners' files), `cl_can_psychosis_causation` (`data/claims/cannabis.json`, a contested claim with a debate
   box) and `cl_can_dependence_how_many` (same file, built on surveys). Plain lines: the same ids in
   `data/site/simple.json` → `claims`.
6. Your cards. New cards (first-pass) are in `data/study-cards/_incoming/<folder>/<card id>.json`; thirteen older cards
   (ai-checked) are in `data/study-cards/cross-cutting.json` (print a card by id). Every card's `reporting_issues` and
   `interpretation_gap` matter here: several papers contradict their own tables, and several abstracts claim more than
   the data. Respect what the first readers found; where a card and its paper's abstract disagree, the card's reading of
   the full text wins.

## Hard rules for this round

- **What was counted, and by whom.** For every count say how a death entered it (ICD-10 codes, a drug mentioned on the
  certificate, toxicology found, a coroner's or medical examiner's conclusion, a register's own definition), who decided,
  what was tested and in what share of deaths, and against what it was compared. Never turn "involved", "present" or
  "detected" into "caused".
- **Both directions in one answer** where the evidence has both: deaths missed (undercounting) and deaths wrongly put
  down to a drug (overcounting). Give the size of each as the papers give it, with its denominator, place and years.
- **Places and years.** Every figure belongs to one country, system and period; say which, and do not generalize a
  Swedish or US figure to "official statistics" everywhere.
- **No alarm, no reassurance.** Write "drug deaths" or "deaths involving a drug", not "overdose epidemic" in our own
  voice; never imply a death "doesn't count". Deaths in custody and the term "excited delirium" are contested: present
  the term as a contested label, name who uses it and who rejects it, and give the evidence for each side (debate box).
- **Findings only.** Nothing that reads as advice on amounts, routes or combinations.
- Person-first words; quote a study's own labels (for example "addict") only in quotation marks.

## Where everything goes

- **Ids, substances and sections.** Answers about drug deaths in general: id `cl_gen_deaths_…`, `substance` `general`,
  section **10** (epidemiology; how deaths are counted); the debate on "excited delirium": section **14** with a debate
  box. Answers about one drug: its prefix and substance (`cl_can_…` cannabis, `cl_mdma_…` mdma, `cl_opi_…` heroin,
  `cl_cath_…` synthetic-cathinones), section **6** for what can cause a death, **10** for how many deaths were counted.
- Claims: a JSON list in `data/claims/_incoming/pdf_w<N>.json` (validate with the jsonschema line in LEAN-RULES).
  Your claims start at version 0.1.0 with one changelog line and `verification` `{"status": "draft", "drafted_by": "AI
  reader <N> (claim writer)", "drafted_on": "<today>"}`.
- Questions and plain lines: `scratchpad/pdf1101/w<N>/simple.json`: `{"<claim id>": {"q": "...", "pages": ["general",
  "<drug slug>", ...], "short": "...", "but": "...", "how": ["...", "..."], "how_src": [["ref id"], ...], "freq": {...
  optional}}}`. `q` as a person would ask it; `pages` where it belongs (`general` is the Facts page; add a drug page when
  the answer is about that drug); `short` about 14 everyday words; `but` the single most important limit; `how` 2 to 4
  points; `how_src` for each point the reference ids it rests on (an empty list for a point about the evidence as a
  whole); reading age 8 to 11; never more than the claim.
- Report: put it (at most 500 words) at the end of your final message: per claim what it rests on and its certainty,
  what is missing (which unread papers would change it), and any card error you found (do not edit cards). The rest of
  the final message under 200 words.

## Anchors

Take each anchor from the card's key finding: `reference`, `study_card`, `page` (the card's printed page, or `PDF p. N`
for an accepted manuscript or online-first PDF, or `PMC HTML`/`publisher HTML`/`Bookshelf HTML` for the older cards read
on the web), the card's `locator`, `extracted` (the data in your own words), `role` (supports, contradicts, qualifies),
`anchor_status` `ai-located`, `located_by` `AI reader <N> (claim writer), from AI reader <M>'s study card`,
`located_on`, and `source_read` (the card's source). Quote at most 15 words, at most one per claim, only where the
wording is the evidence.

## Grading (METHODS §6.3)

- Counts of deaths, register comparisons and certificate studies are `describes` claims (§6.1): they are graded for how
  far the count can be trusted, start **low**, and are never upgraded. Comparisons of two counting methods for the same
  deaths (linkage, enhanced review, autopsy against no autopsy) are the strongest evidence here; say so.
- Narrative reviews, position papers and case series: claims resting only on them stay at draft and say their figures
  are second-hand or illustrative.
- A claim whose evidence points both ways is `contested` and carries the six-part debate box (§7).
- Count each study once: Slavova's review and Gutkind's scoping review cite primary studies you also have.

---

## Your questions

Merge or split where the evidence demands, and say why in the report.

### Reader 318: counting, coding and investigating
Cards: new `sc_fugelstad_2020`, `sc_ruhm_2018`, `sc_ossiander_2014`, `sc_chen_2025`, `sc_stam_2019`, `sc_webb_2003`,
`sc_landen_2003`, `sc_amundsen_2017`, `sc_hancock_2024`, `sc_smiley_mcdonald_2025`, `sc_zaychik_2024`, `sc_davis_2020`,
`sc_sumnall_2023` (folder `cross-cutting`), `sc_forsyth_2012` (`synthetic-cathinones`); older `sc_beynon_2007`,
`sc_goldberger_2013`, `sc_garnett_2026`, `sc_slavova_2015`, `sc_slavova_2019`, `sc_gutkind_2025`, `sc_buchanich_2018`,
`sc_horon_2018`, `sc_lundberg_2026`, `sc_quesinberry_2019`.
1. How are drug deaths counted, and why do the numbers differ between countries and registers? (definitions and codes,
   who decides, registers that do not overlap)
2. Do official counts miss drug deaths? (certificates that name no drug, coding, literal text, enhanced reviews, and how
   much the counts change when corrected)
3. Does it matter who investigates a death, and whether there is an autopsy and toxicology testing? (both directions:
   deaths found and deaths wrongly suspected; access to testing; system changes)
4. How do news stories about drug deaths change what people think? (the randomized online experiment; the mephedrone
   news study)

### Reader 319: what a death can and cannot show
Cards: new `sc_pounder_1990`, `sc_ketola_2019`, `sc_leikin_2003`, `sc_borra_2026`, `sc_goncalves_dias_2026` (folder
`cross-cutting`), `sc_milroy_2011`, `sc_henry_1992` (`mdma`), `sc_drummer_2019` (`cannabis`), `sc_darke_1996`
(`heroin`), `sc_schifano_2012` (`synthetic-cathinones`); older `sc_ferner_2008`, `sc_launiainen_2014`, `sc_strommer_2020`.
You may also cite `sc_webb_2003` and `sc_hancock_2024` (reader 318's) for deaths put down to a drug wrongly.
5. Can a drug level measured after death show that the drug caused the death? (redistribution after death, the site of
   the sample, the overlap between levels in drug deaths and in other deaths or living people)
6. Can cannabis cause death? (what the deaths attributed to it show; cannabis page)
7. Are deaths called heroin "overdoses" always caused by heroin alone? (heroin and opioid pages)
8. How many deaths blamed on mephedrone were confirmed? (synthetic cathinones page)
9. What MDMA level is fatal? (the overlap in Milroy; the early deaths series of Henry et al.; MDMA page)
10. What is "excited delirium", and why is the term disputed? (deaths in custody; contested; Facts page, and the cocaine
    and methamphetamine pages if the evidence names those drugs)
