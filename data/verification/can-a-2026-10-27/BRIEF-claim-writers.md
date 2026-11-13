# Cannabis, Tier A: claim writers (round `can-a-2026-10-27`)

You write graded answers (claims) for Pharmakon, an evidence library about drugs for the public and for people who use
drugs. Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/can-a/w<N>/` (N = your reader number; create it).

## The task

The Cannabis page already answers questions about smoking and vaping, edibles, strong cannabis, sleep, driving and
repeated vomiting. First readers have now written study cards for its Tier A papers (`search-logs/Cannabis_DOI-LIST.md`;
read its notes on how the papers answer each other). You turn the cards into claims (WORKFLOW step 7), one claim per
question a person would ask. Blind second readers will later re-find your evidence in the sources, so every number must
be right and anchored.

## Read first (only these parts)

1. `scratchpad/batch5/LEAN-RULES.md`: follow it.
2. `docs/WRITING-RULES.md`: Rule 0 and Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/METHODS.md` §6 (all of it), §7 (debate box), §8 (the section numbers), §9 (language), §5.5 point 1.
4. Models, printed by id with `json.load` (never read whole files): `cl_mdma_memory` and `cl_mdma_prospective`
   (`data/claims/mdma.json`), `cl_meth_cognition_causal` (`data/claims/methamphetamine.json`), a contested claim with a
   debate box `cl_nic_snus` (`data/claims/nicotine.json`), and the existing Cannabis claim `cl_can_thc_impairment_duration`
   (`data/claims/cannabis.json`), so that yours do not repeat it. Your claims start at version 0.1.0 with one changelog
   line and `verification` `{"status": "draft", "drafted_by": "AI reader <N> (claim writer)", "drafted_on": "<today>"}`.
   Plain lines: the entries `cl_mdma_memory` and `cl_can_thc_impairment_duration` in `data/site/simple.json` → `claims`.
5. The cards: `data/study-cards/_incoming/cannabis/<card id>.json` (first-pass; print the ones you need). Each has
   `key_findings` with page, locator and data, `reporting_issues`, `risk_of_bias`, `interpretation_gap`,
   `replication.timeline`, and the reader's notes on exposure definitions. Respect the reporting issues the first
   readers found.

## Where everything goes

- `substance`: `cannabis`. `section` per METHODS §8: long-term effects (psychosis, memory and thinking, IQ, mood, the
  heart) 9; dependence and withdrawal 8; acute effects measured in controlled studies 5; pregnancy and other acute risks
  6; treatment and medical uses 12. Never section 7.
- Claims: a JSON list in `data/claims/_incoming/can_w<N>.json` (validate with the jsonschema line in LEAN-RULES).
- Questions and plain lines: `scratchpad/can-a/w<N>/simple.json`: `{"<claim id>": {"q": "...", "short": "...", "but":
  "...", "how": ["...", "..."], "freq": {...optional}}}`. `short` about 14 everyday words; `but` the single most
  important limit; `how` 2 to 4 points; reading age 8 to 11; name the comparison group; never more than the claim.
- Report: this session does not let you write report files, so put the report (at most 500 words) at the end of your
  final message: per claim what it rests on and its certainty, what is missing, and any card error you found (do not
  edit cards). The rest of the final message under 200 words.

## Anchors

- Each anchor: `reference`, `study_card`, `page`, `locator`, `extracted` (the data in your own words), `role`
  (supports, contradicts, qualifies), `anchor_status` `ai-located`, `located_by`, `located_on`, `source_read`.
- **PDF papers** (the senior author's: `moore_2007`, `gage_2016`, `gillespie_2021`, `ksir_2016`, `hall_2009`,
  `hall_2015`, `curran_2016`, `broyd_2016`, `page_2020`): find every number yourself in the PDF text, not only on the
  card. Texts: `scratchpad/can-a/numtext/`; PDFs: `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Cannabis/`. `page` is
  the printed page; for the accepted manuscripts (Gage 2016, Broyd 2016) "AM p. N" as on the card. `located_by`:
  `AI reader <N> (claim writer)`; `source_read`: "PDF PDFs/Cannabis/<file>.pdf". Before you finish, run
  `python3 -I scripts/check_anchor_numbers.py scratchpad/can-a/numtext data/claims/_incoming/can_w<N>.json` and fix or
  explain every number it cannot find.
- **Web papers** (the rest, read in PubMed Central or at the publisher): take the anchor from the card's key finding
  (page `PMC HTML` or `publisher HTML`, the card's locator); set `located_by` to `AI reader <N> (claim writer), from AI
  reader <M>'s study card` and `source_read` to the card's source. Do not open the browser.
- Quote at most 15 words, at most one per claim, only where the wording is the evidence.

## Grading (METHODS §6.3)

- Observational evidence (cohorts, case-control studies, surveys, twin comparisons, meta-analyses of them) starts
  **low**. Mendelian randomization studies are observational too: they start low; say in the reasoning what the genetic
  design does and does not protect against (it addresses some confounding; weak instruments, other pathways from the
  variants to the outcome, and the use of genetic liability to ever use rather than amount or frequency remain), and
  whether the sensitivity analyses the cards report justify not rating down for confounding. A genome-wide association
  study shows genetic overlap, not cause. Co-twin comparisons remove shared family factors, not others.
- Randomized trials and meta-analyses of them start **high**.
- Reviews and the studies inside them are not independent: count each study once, and say so (for example, the London
  case-control studies share their sample and team; the genetic studies share consortium data; the IQ papers reanalyse
  one cohort).
- Claims resting only on narrative reviews, viewpoints or critical overviews (Hall 2009 and 2015, Curran 2016, Gage
  2016, Ksir 2016, Gillespie 2021, Volkow 2014, Murray 2016) stay at draft and say their figures are second-hand (§6.3);
  use them to qualify, to frame a debate box, or for a definition.
- Status flags per §6.4. A claim whose evidence points both ways, or that a credible critique changes, is `contested`
  and carries the six-part debate box (§7). Whether cannabis causes psychosis, and whether teenage use lowers later IQ,
  are the obvious candidates: weigh the association and dose-response findings against confounding, reverse causation
  and shared genetic liability, without taking a side the evidence does not support.

## Hard rules for this topic

- Findings only: no advice on how much, how often or how to use; no doses except as a study's conditions.
- Name with every estimate the **exposure** as the source defined it (ever, weekly, daily, heaviest use, waves of
  dependence; potency and how it was measured), the **outcome** (psychotic symptoms, psychotic disorder, schizophrenia
  diagnosis; which tests, after how long without cannabis), the **comparison group** and the **adjustment set**.
  Absolute numbers before relative ones; counts out of 100 (or 1,000) with denominators; editors' calculations labelled.
- Person-first words ("people who use cannabis", "people with schizophrenia"); no words of alarm or reassurance.

---

## Your questions

Ids start `cl_can_`. Merge or split where the evidence demands, and say why in the report.

### Reader 207: memory, thinking and IQ
Cards: `sc_broyd_2016`, `sc_curran_2016`, `sc_scott_2018`, `sc_meier_2012`, `sc_rogeberg_2013`, `sc_moffitt_2013`,
`sc_jackson_2016`, `sc_meier_2018`.
1. Do people who use cannabis do worse on memory and thinking tests, and does it depend on how recently they used?
   (do not repeat `cl_can_thc_impairment_duration`, which covers the hours after a single dose)
2. Do differences remain after people have stopped for days or weeks?
3. Does using cannabis as a teenager lower IQ later in life? (the Dunedin finding, the published reanalysis and reply,
   and the twin studies; a debate box if contested)

### Reader 208: psychosis and schizophrenia
Cards: `sc_moore_2007`, `sc_marconi_2016`, `sc_di_forti_2015`, `sc_di_forti_2019`, `sc_gage_2016`, `sc_gage_2017`,
`sc_vaucher_2018`, `sc_pasman_2018`, `sc_gillespie_2021`, `sc_ksir_2016`, `sc_murray_2016`, and the psychosis findings
of `sc_hall_2009` and `sc_hall_2015`.
1. Are people who use cannabis more likely to develop a psychotic disorder or schizophrenia, and does it depend on how
   often they use and how strong the cannabis is?
2. Does cannabis cause psychosis, or could confounding, reverse causation or shared genes explain the link? (genetic
   studies and critiques; a debate box if contested)
3. Only if the cards support it: have rates of schizophrenia changed as cannabis use rose?

### Reader 209: dependence, withdrawal, repeated vomiting, and how THC moves through the body
Cards: `sc_connor_2021`, `sc_volkow_2014`, `sc_hall_2009`, `sc_hall_2015`, `sc_bahji_2020`, `sc_sorensen_2017`,
`sc_huestis_2007`, and the dependence findings of `sc_curran_2016`. Existing claims you must not repeat:
`cl_can_potency_dependence`, `cl_can_sleep_stopping`, `cl_can_stopping_sleep_lab`, `cl_can_chs_capsaicin`,
`cl_can_chs_dopamine_antagonists` (print them).
1. How many people who use cannabis develop cannabis use disorder or dependence, and does it depend on how often they
   use and how young they start? (trace each figure to the survey and diagnostic criteria it comes from)
2. How common is cannabis withdrawal in people who use regularly, and what does it involve?
3. What is cannabis hyperemesis syndrome (repeated bouts of vomiting), how is it recognised, and does it stop when
   people stop using?
4. How does THC move through the body after smoking and after eating, and how long can it be found in blood and urine?

### Reader 210: pregnancy, the heart, mood, and medical uses
Cards: `sc_gunn_2016`, `sc_page_2020`, `sc_gobbi_2019`, `sc_whiting_2015`, and the relevant findings of
`sc_hall_2009`, `sc_hall_2015` and `sc_volkow_2014`.
1. Is using cannabis during pregnancy linked to differences in the baby (birth weight, early birth, intensive care)?
   (say what the studies could and could not separate from tobacco and alcohol)
2. Is cannabis use linked to heart attacks, strokes or other heart and blood-vessel problems?
3. Is cannabis use in adolescence linked to depression, anxiety or suicidal thoughts in young adulthood?
4. What do randomized trials show about cannabis and cannabinoid medicines (pain, muscle stiffness in multiple
   sclerosis, nausea and vomiting with chemotherapy, sleep, and other uses the review covers), and what side effects?
