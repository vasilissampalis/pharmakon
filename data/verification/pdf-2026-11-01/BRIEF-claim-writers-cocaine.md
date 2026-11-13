# Cocaine, round 2: claim writers (round `pdf-2026-11-01`)

You write graded answers (claims) for Pharmakon, an evidence library about drugs for the public and for people who use
drugs. Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/pdf1101/w<N>/` (N = your reader number; create it).

## The task

The Cocaine page so far answers questions about the crash after a binge, the first weeks after stopping and cocaine
with alcohol and cannabis. This round builds its core from the Tier A papers of `search-logs/Cocaine_DOI-LIST.md`, which
the senior author saved as PDFs: how cocaine acts by route and in the laboratory, how dependence starts, powder against
crack, chest pain and heart attacks and how hospitals treat them, levamisole in street cocaine, cocaine with alcohol
(cocaethylene), memory and thinking, deaths, psychosis and medicines tried for dependence. First readers have written
the study cards from the PDFs. You turn them into claims (WORKFLOW step 7), one per question a person would ask, and
revise the existing cocaine-with-alcohol answers where the primary papers now read change them. Blind second readers
will re-find your evidence in the sources, so every number must be right and anchored.

## Read first (only these parts)

1. `scratchpad/batch5/LEAN-RULES.md`: follow it.
2. `docs/WRITING-RULES.md`: Rule 0 and Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/METHODS.md` §6 (all of it), §7, §8, §9, §13.
4. `data/verification/pdf-2026-11-01/BRIEF-first-readers.md`, "What to record, by part" → "Cocaine": the same points
   must reach the claims.
5. Models, printed by id with `json.load`: `cl_meth_acute_toxicity` and `cl_meth_cognition` (`data/claims/methamphetamine.json`),
   `cl_mdma_memory` (`data/claims/mdma.json`), `cl_can_psychosis_causation` (`data/claims/cannabis.json`, a contested
   claim with a debate box). Plain lines: the same ids in `data/site/simple.json` → `claims`.
6. Your cards: new ones (first-pass) in `data/study-cards/_incoming/cocaine/<card id>.json`; older ones (ai-checked) in
   `data/study-cards/cocaine.json` and `data/study-cards/interactions.json` (print by id). Respect every card's
   `reporting_issues` and `interpretation_gap`.

## Hard rules for this round

- **Findings only.** Doses, routes, blood levels and timings appear only as a study's conditions, never as advice. No
  "safe" amount. Nothing on making effects stronger or longer. Hospital treatment (beta-blockers, labetalol, other
  medicines) is reported as what was given to patients and what was measured, never as self-treatment.
- **Who and where.** People in a laboratory (and their history of use), patients in an emergency department or a
  catheter laboratory, people in treatment, people in surveys: kept apart in every sentence.
- **Exposure and comparison.** Powder or crack, snorted, smoked or injected, as each source defines it; the comparison
  group and adjustment with every estimate; "present" or "associated" never as "caused".
- **Memory and thinking.** How long people had been abstinent, the comparison group, alcohol and other drugs as
  confounders, and whether a difference is within the normal range.
- Person-first words; no words of alarm or reassurance.

## Where everything goes

- **Ids and sections** (METHODS §8): `cl_coc_…`, `substance` `cocaine`. How cocaine acts by route: **3**; effects
  measured in laboratories: **5**; heart, levamisole, cocaethylene, heat and other acute risks and how emergency care
  responds: **6**; dependence and powder against crack: **8**; memory, thinking and psychosis: **9**; deaths: **10**;
  medicines for dependence: **12**. A disputed question gets `contested` and the six-part debate box (§7); the use of
  beta-blockers after cocaine is the obvious candidate.
- New claims: `data/claims/_incoming/pdf_w<N>.json` (validate with the jsonschema line in LEAN-RULES), version 0.1.0,
  `verification` `{"status": "draft", "drafted_by": "AI reader <N> (claim writer)", "drafted_on": "<today>"}`.
- Revisions of existing claims: only through a patch in the `scripts/claim_patch.py` format,
  `data/claims/_incoming/patch_pdf_w<N>.json` (`evidence_add`, `replace` or `set`, `bump` `minor`, a `change` line
  beginning "Round pdf-2026-11-01:"); dry-run until it passes; never apply it.
- Plain lines: `scratchpad/pdf1101/w<N>/simple.json` (`q`, `pages`, `short`, `but`, `how`, `how_src`); `pages` is
  `cocaine` (add `interactions` for cocaine with alcohol).
- Anchors: `page` as the card gives it; `located_by` "AI reader <N> (claim writer), from AI reader <M>'s study card";
  `source_read` the card's.
- Report (at most 500 words) at the end of your final message: per claim what it rests on and its certainty, what is
  missing, and any card error you found.

## Your questions

### Reader 325: the heart, adulterants, deaths and psychosis
Cards: `sc_weber_2000`, `sc_hollander_1995`, `sc_lange_1990`, `sc_boehrer_1993`, `sc_mccord_2008`, `sc_pham_2018`,
`sc_fanari_2014`, `sc_buchanan_2012`, `sc_roberts_2015`, `sc_degenhardt_2011`, `sc_sabe_2021`.
1. How often is chest pain after cocaine a heart attack? (`cl_coc_chest_pain_mi`)
2. Does cocaine narrow the heart's arteries, and does a beta-blocker given in hospital make that worse? (`cl_coc_beta_blockers`;
   the laboratory studies in patients, the AHA statement, the meta-analysis and the hospital records; contested.)
3. What is levamisole, found in street cocaine, and what harm can it do? (`cl_coc_levamisole`; how cases were found
   and confirmed; no estimate of how common harm is unless a source gives one.)
4. How much higher is the risk of death for people who use cocaine? (`cl_coc_mortality`; the cohorts, the comparison
   and the causes.)
5. How common is psychosis brought on by cocaine? (`cl_coc_psychosis`; the corrigendum to Sabe et al. 2021 is not yet
   read: say so, and say what it might change.)

### Reader 326: the body, dependence, alcohol, thinking and treatment
Cards: `sc_walsh_2010`, `sc_chandra_2020`, `sc_harris_2003b`, `sc_jatlow_1991`, `sc_hart_2000b`, `sc_bolla_2000`,
`sc_jovanovski_2005`, `sc_spronk_2013`, `sc_frazer_2018`, `sc_lopez_martin_2026`, `sc_castells_2007`, and the earlier
first-pass cards `sc_barnett_1981`, `sc_evans_1996`, `sc_chen_2004`, `sc_hatsukami_1996`, `sc_butler_2017`; older
`sc_mccance_katz_1998`, `sc_pennings_2002` (interactions).
6. How fast does cocaine act, and for how long, by route? (`cl_coc_pk_route`; Barnett 1981, Evans 1996; conditions only.)
7. What happens in the laboratory when people who use cocaine can choose to take more? (`cl_coc_lab_self_administration`;
   Walsh et al. 2010; people with and without dependence.)
8. How quickly can dependence start after first use? (`cl_coc_dependence_onset`; Chandra & Anthony 2020.)
9. Is crack more addictive or more harmful than powder cocaine? (`cl_coc_crack_powder`; Chen & Anthony 2004,
   Hatsukami & Fischman 1996, Butler et al. 2017; what differs is the route and the people, as the sources say.)
10. Revise `cl_mix_cocaine_alcohol` and `cl_mix_cocaine_alcohol_drunkenness` (`data/claims/interactions.json`) with the
    primary studies of cocaethylene now read (Jatlow et al. 1991, Harris et al. 2003, Hart et al. 2000); a new claim
    only if a question is not covered by these two.
11. Does cocaine affect memory and thinking, and does it get better after stopping? (`cl_coc_cognition`; Jovanovski et
    al. 2005, Spronk et al. 2013, Frazer et al. 2018, López-Martín et al. 2026, Bolla et al. 2000.)
12. Do stimulant medicines help people stop using cocaine? (`cl_coc_stimulant_medicines`; Castells et al. 2007.)
