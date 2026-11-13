# Ketamine, Tier A: claim writers (round `ket-a-2026-10-27`)

You write graded answers (claims) for Pharmakon, an evidence library about drugs for the public and for people who use
drugs. Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/ket-a/w<N>/` (N = your reader number; create it).

## The task

The Ketamine page has no answers yet. First readers have written study cards for the core papers the senior author
saved as PDFs (Tier A of `search-logs/Ketamine_DOI-LIST.md`). You turn the cards into claims (WORKFLOW step 7), one claim
per question a person would ask. Blind second readers will later re-find your evidence in the sources, so every number
must be right and anchored. More cards (bladder damage, deaths, depression treatment, acute effects in a meta-analysis)
are still being read; answer only the questions given to you.

## Read first (only these parts)

1. `scratchpad/batch5/LEAN-RULES.md`: follow it.
2. `docs/WRITING-RULES.md`: Rule 0 and Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/METHODS.md` §6 (all of it), §7 (debate box), §8 (the section numbers), §9 (language), §5.5 point 1.
4. Models, printed by id with `json.load` (never read whole files): `cl_meth_pk_bioavailability_route` and
   `cl_meth_glucose_metabolism` (`data/claims/methamphetamine.json`), `cl_mdma_memory` and `cl_mdma_prospective`
   (`data/claims/mdma.json`), and a contested claim with a debate box, `cl_nic_snus` (`data/claims/nicotine.json`).
   Your claims start at version 0.1.0 with one changelog line and `verification`
   `{"status": "draft", "drafted_by": "AI reader <N> (claim writer)", "drafted_on": "<today>"}`. Plain lines: the entries
   `cl_meth_pk_bioavailability_route` and `cl_mdma_memory` in `data/site/simple.json` → `claims`.
5. The cards: `data/study-cards/_incoming/ketamine/<card id>.json` (first-pass; print the ones you need). Each has
   `key_findings` with page, locator and data, `reporting_issues`, `risk_of_bias`, `interpretation_gap`, and the
   reader's notes on study conditions. Respect the reporting issues the first readers found.

## Where everything goes

- `substance`: `ketamine`. `section` per METHODS §8: pharmacology and blood levels by route 3; brain imaging 4; effects
  measured in controlled studies, and effects on the night of use 5; long-term effects 9. Never section 7.
- Claims: a JSON list in `data/claims/_incoming/ket_w<N>.json` (validate with the jsonschema line in LEAN-RULES).
- Questions and plain lines: `scratchpad/ket-a/w<N>/simple.json`: `{"<claim id>": {"q": "...", "short": "...", "but":
  "...", "how": ["...", "..."], "freq": {...optional}}}`. `short` about 14 everyday words; `but` the single most
  important limit; `how` 2 to 4 points; reading age 8 to 11; name the comparison group; never more than the claim.
- Report: this session does not let you write report files, so put the report (at most 500 words) at the end of your
  final message: per claim what it rests on and its certainty, what is missing, and any card error you found (do not
  edit cards). The rest of the final message under 200 words.

## Anchors

- All papers here are the senior author's PDFs. Find every number yourself in the PDF text, not only on the card.
  Texts: `scratchpad/ket-a/numtext/`; PDFs: `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Ketamine/`. Several are old
  scanned pages whose machine-read text has errors (the cards say which): check every number you use on the rendered
  page (`pdftoppm -r 150 -f N -l N -png`). `page` is the printed page (see `data/access/pdf-page-basis.json` and the
  card for the online-first Peltoniemi et al., 2016, and for Ait Bentaleb et al., whose print year is 2024).
- Each anchor: `reference`, `study_card`, `page`, `locator`, `extracted` (the data in your own words), `role`
  (supports, contradicts, qualifies), `anchor_status` `ai-located`, `located_by` `AI reader <N> (claim writer)`,
  `located_on`, `source_read` "PDF PDFs/Ketamine/<file>.pdf".
- Before you finish, run `python3 -I scripts/check_anchor_numbers.py scratchpad/ket-a/numtext data/claims/_incoming/ket_w<N>.json`
  and fix or explain every number it cannot find.
- Quote at most 15 words, at most one per claim, only where the wording is the evidence.

## Grading (METHODS §6.3)

- Controlled studies in volunteers (blood-level studies, placebo-controlled infusion studies) start **high**, like the
  methamphetamine models, and are rated down for what the cards found: order not randomized or not reported, blinding
  that ketamine's effects break, no placebo, small samples, one laboratory.
- Studies of people who use ketamine outside a laboratory (cohorts, cross-sectional comparisons) start **low**. Most come
  from one research group in London with overlapping samples: say so, count shared participants once, and use
  `replicated-same-team` rather than `replicated` where that is the case.
- Claims resting only on narrative reviews (Morgan & Curran, 2012; Peltoniemi et al., 2016) stay at draft and say their
  figures are second-hand (§6.3); use the reviews to qualify, to frame a debate box, or for a definition.
- Status flags per §6.4. A claim whose evidence points both ways, or that a credible critique changes, is `contested`
  and carries the six-part debate box (§7).

## Hard rules for this topic

- Findings only. Doses, routes, infusion schedules and blood levels appear only as the conditions of a named study,
  never as amounts, timings or routes a reader could follow, compare for use, or combine. Do not convert a study's dose
  into any other route or body weight. No "safe", no "recommended".
- Separate effects in healthy volunteers from effects in patients, effects during a session from lasting ones, and
  people who use often from people who use rarely; name the comparison group and the time since last use for every
  difference.
- Person-first words ("people who use ketamine", "people with schizophrenia"); no words of alarm or reassurance.

---

## Your questions

Ids start `cl_ket_`. Merge or split where the evidence demands, and say why in the report.

### Reader 201: blood levels, brain imaging, the two forms of ketamine
Cards: `sc_clements_1982`, `sc_yanagihara_2003`, `sc_peltoniemi_2016`, `sc_vollenweider_1997a`,
`sc_vollenweider_1997b`, `sc_ait_bentaleb_2024`.
1. How much of a ketamine dose reaches the blood by each route that was studied, and how quickly?
2. How long does ketamine stay in the blood, and what does the body turn it into (norketamine)?
3. What do brain-imaging studies show during ketamine in healthy volunteers?
4. Do the two mirror-image forms, S-ketamine and R-ketamine, have different effects? (only what the cards support)

### Reader 202: people who use ketamine: memory, thinking and wellbeing
Cards: `sc_curran_2000`, `sc_curran_2001`, `sc_morgan_2004a`, `sc_morgan_2009`, `sc_morgan_2010b`, `sc_morgan_2012`.
1. On the night of use and a few days later, how do people who use ketamine do on memory and thinking tests, and what
   do they report feeling?
2. Do people who use ketamine often score lower on memory and thinking tests than people who do not, when they have not
   used for days?
3. Do these differences fade or remain after people cut down or stop?
4. Is frequent use linked to low mood, dissociation or unusual beliefs?

### Reader 220: effects measured during controlled sessions, and how ketamine acts
Cards: `sc_krystal_1994`, `sc_malhotra_1996`, `sc_newcomer_1999`, `sc_lahti_1995`, `sc_beck_2020`, the psychopathology
findings of `sc_vollenweider_1997a` and `sc_vollenweider_1997b`, `sc_zanos_2018`, and `sc_morgan_2012` as context.
Existing claims you must not repeat: `cl_ket_enantiomers`, `cl_ket_brain_imaging_acute`, `cl_ket_halflife_norketamine`,
`cl_ket_night_of_use_tests` (print them from `data/claims/_incoming/ket_w201.json` and `ket_w202.json`).
**Two of your cards are web papers** (`sc_beck_2020`, `sc_zanos_2018`, read in PubMed Central): take their anchors from
the card's key findings (page `PMC HTML`, the card's locator), set `located_by` to `AI reader 220 (claim writer), from AI
reader 206's study card` and `source_read` to the card's source, and do not open the browser.
1. In controlled studies of healthy volunteers, what does ketamine do during the session to perception, thinking,
   psychosis-like and dissociative experiences, and how quickly do these effects pass? (name the scales and when they
   were measured; Beck's pooled figures are peak, within-person changes)
2. What does ketamine do to memory and attention during the session?
3. What happened when people with schizophrenia were given ketamine in a study? (separate patients from volunteers)
4. How does ketamine act in the brain (the receptor it blocks, its metabolites), and how much of this is known only from
   animal or laboratory studies? (Zanos is a narrative review: the claim stays at draft and says so)
