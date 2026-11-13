# Facts about drug use, round 2: claim writers (round `pdf-2026-11-01`)

You write graded answers (claims) for Pharmakon, an evidence library about drugs for the public and for people who use
drugs. Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/pdf1101/w<N>/` (N = your reader number; create it).

## The task

The site's "Facts about drug use" page answers general questions (women and men, telescoping, genes and family, drinking
young, using several drugs, the words used about people), each read with a critical eye (decision `s-quiz-v2`). Its
first round named papers it had not read; the senior author saved them and first readers have written their study cards
from the PDFs. You do two things:

- **Revise existing answers** with the new evidence, only through a patch in the `scripts/claim_patch.py` format (read
  its docstring): `evidence_add` for new anchors, `replace` or `set` for statement, magnitude, limits, grade and plain
  text, `bump` `minor`, and a `change` line beginning "Round pdf-2026-11-01:". Print the current claim by id first;
  keep every existing anchor (an anchor that the primary paper now shows to be wrong stays, with the claim saying what
  the primary paper shows instead); say in the report what changed and why.
- **Write new answers** as new claims.

Blind second readers will re-find your evidence in the sources, so every number must be right and anchored.

## Read first (only these parts)

1. `scratchpad/batch5/LEAN-RULES.md`: follow it.
2. `docs/WRITING-RULES.md`: Rule 0 and Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/METHODS.md` §6 (all of it), §7, §8, §9, §13.
4. `data/verification/gen-a-2026-11-01/BRIEF-claim-writers.md`, "Hard rules for this round", "Where everything goes"
   and "Grading": they apply to you unchanged, with the output paths below.
5. Your cards: new ones (first-pass) in `data/study-cards/_incoming/<folder>/<card id>.json`; older ones (ai-checked)
   in `data/study-cards/<folder>.json` (print by id). Respect every card's `reporting_issues` and `interpretation_gap`:
   several abstracts claim more than their data, and some reviews misreport the papers they cite.

## Outputs

- New claims: `data/claims/_incoming/pdf_w<N>.json` (validate with the jsonschema line in LEAN-RULES), version 0.1.0,
  `verification` `{"status": "draft", "drafted_by": "AI reader <N> (claim writer)", "drafted_on": "<today>"}`.
- Revisions: `data/claims/_incoming/patch_pdf_w<N>.json`; run `python3 -I scripts/claim_patch.py <file> --dry-run`
  until it passes. Never apply it.
- Plain lines for every new or revised claim: `scratchpad/pdf1101/w<N>/simple.json` (`q`, `pages`, `short`, `but`,
  `how`, `how_src`); `pages` is `general` (the Facts page) plus any drug page the answer belongs on; for a revised claim
  start from its current entry in `data/site/simple.json`.
- Anchors from the new cards: `page` as the card gives it (printed page, `PDF p. N`, `AM p. N`); `located_by` "AI reader
  <N> (claim writer), from AI reader <M>'s study card"; `source_read` the card's.
- Report (at most 500 words) at the end of your final message: per claim what changed or what it rests on, its
  certainty, what is missing, and any card error you found.

## Your questions

### Reader 323: how drug use starts and develops
Cards: new `sc_randall_1999`, `sc_grant_1997` (folder `alcohol`), `sc_khan_2013`, `sc_morral_2002`, `sc_lynskey_2003`
(`cannabis`), `sc_grant_1998`, `sc_kandel_1975`, `sc_wagner_2002`, `sc_connor_2014` (`cross-cutting`),
`sc_gouzoulis_mayfrank_2006` (`mdma`); older `sc_keyes_2010`, `sc_marks_2018`, `sc_mchugh_2018`, `sc_greenfield_2007`,
`sc_maimaris_2014`, `sc_irons_2015`, `sc_vanyukov_2012`, `sc_degenhardt_2010a`, `sc_liu_2018`.
1. Revise `cl_gen_telescoping` (general file) with Randall et al. (1999) and Khan et al. (2013), read in full. Khan et
   al. give a difference of 0.40 years (2.64 against 2.24, among people who already had the disorder, not adjusted for
   age), not the "2.5 years" the claim now reports second-hand from Marks & Clark (2018): replace that sentence and its
   plain line, and say that the review misreports it.
2. Revise `cl_alc_early_drinking_later_problems` (alcohol file) with Grant & Dawson (1997), read in full.
3. New: Does starting to use drugs young go with drug problems later? (`cl_gen_early_drug_use`; Grant & Dawson 1998;
   the co-twin study; what the designs can and cannot show about cause).
4. New: Does cannabis lead to other drugs (the "gateway" idea)? (`cl_gen_gateway`; Kandel 1975, Lynskey et al. 2003,
   Morral et al. 2002, Wagner & Anthony 2002, Vanyukov et al. 2012): contested, with the debate box; pages `general` and
   `cannabis`.
5. New: How common is using more than one drug, and why does it matter for research? (`cl_gen_polydrug`; Connor et al.
   2014, Gouzoulis-Mayfrank & Daumann 2006; link to the existing cocaine co-use answer rather than repeating it.)

### Reader 324: recovery, surroundings, genes, expectations, stigma and leaving prison
Cards: new `sc_robins_1975`, `sc_fleury_2016`, `sc_gage_2019`, `sc_petrie_1996`, `sc_visscher_2008`, `sc_connor_2014`
(shared), `sc_van_boekel_2013`, `sc_kelly_2010`, `sc_borschmann_2024` (folder `cross-cutting`), `sc_mellor_2019`,
`sc_marlatt_1973`, `sc_hull_1986` (`alcohol`), `sc_hart_2000` (`cocaine`); older `sc_verges_2012`, `sc_kendler_2012`,
`sc_prom_wormley_2017`, `sc_pennington_2023`, `sc_lenoir_2007`.
6. New: Do people with drug or alcohol problems recover, and do many recover without treatment? (`cl_gen_remission`;
   Robins et al. 1975, Fleury et al. 2016, Mellor et al. 2019, Vergés et al. 2012: definitions and time windows matter.)
7. New: Does a better environment make drug taking less likely? The "Rat Park" studies and what they show
   (`cl_gen_rat_park`; Gage & Sumnall 2019, Petrie 1996: animal findings labelled as such), and, as its own claim if the
   evidence warrants it, do people choose other rewards over cocaine when offered them? (`cl_coc_alternative_rewards`;
   Hart et al. 2000, a small inpatient laboratory study; pages `cocaine` and `general`; conditions only.)
8. Revise `cl_gen_genes_family` with Visscher et al. (2008): what a heritability figure does and does not mean.
9. New: Does believing you have drunk alcohol change how you act? (`cl_alc_expectancy`; Marlatt et al. 1973, Hull &
   Bond 1986; pages `alcohol` and `general`.)
10. Revise `cl_gen_words_labels_stigma` with Kelly & Westerhoff (2010), the randomized study of two terms, and write
    a new claim on health workers' attitudes and care (`cl_gen_stigma_health_care`; van Boekel et al. 2013).
11. New: Is the time after leaving prison a time of higher risk of death? (`cl_gen_release_deaths`; Borschmann et al.
    2024; section 6; pages `general`, `heroin`, `prescription-opioids`, `fentanyl-and-analogues`; the "first week" is
    days 2 to 7, most poisoning deaths came later, the category mixes alcohol, drugs and undetermined intent, and the
    study measured no tolerance: say so.)
