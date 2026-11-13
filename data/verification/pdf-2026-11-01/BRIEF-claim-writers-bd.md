# Before and during use, round 2: claim writers (round `pdf-2026-11-01`)

You write graded answers (claims) for Pharmakon, an evidence library about drugs for the public and for people who use
drugs. Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/pdf1101/w<N>/` (N = your reader number; create it).

## The task

The site already answers what research says people do before and during use (decision `p-before-during-after`:
findings only, no amounts, timings or regimens as advice, nothing on making a drug's effects stronger). The checkers of
that round named papers that would make those answers stronger, and the senior author saved them; first readers have now
written their study cards from the PDFs. You do two things:

- **Revise existing answers** with the new evidence. An existing claim is changed only through a patch in the
  `scripts/claim_patch.py` format (read its docstring): `evidence_add` for the new anchors, `replace` or `set` for the
  statement, magnitude, limits, grade and plain text, `bump` `minor`, and a `change` line beginning "Round
  pdf-2026-11-01:". Print the current claim by id first; keep every existing anchor; change only what the new evidence
  requires, and say in the report what changed and why.
- **Write new answers** where a question has no answer yet, as new claims.

Blind second readers will re-find your evidence in the sources, so every number must be right and anchored.

## Read first (only these parts)

1. `scratchpad/batch5/LEAN-RULES.md`: follow it.
2. `docs/WRITING-RULES.md`: Rule 0 and Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/METHODS.md` §6 (all of it), §7, §8 (the section numbers; section 7 is the senior author's), §9, §13.
4. `data/verification/bd-dd-2026-10-31/BRIEF-claim-writers-before-during.md`, "Hard rules for this round" and "Where
   everything goes": they apply to you unchanged.
5. Your cards (first-pass): `data/study-cards/_incoming/<folder>/<card id>.json`. Respect their `reporting_issues` and
   `interpretation_gap`: several abstracts claim more than their data (a non-significant trend called an effect, an
   inferred mechanism called measured, an opinion piece's preview data without methods).

## Outputs

- New claims: a JSON list in `data/claims/_incoming/pdf_w<N>.json` (validate with the jsonschema line in LEAN-RULES),
  version 0.1.0, `verification` `{"status": "draft", "drafted_by": "AI reader <N> (claim writer)", "drafted_on":
  "<today>"}`.
- Revisions: `data/claims/_incoming/patch_pdf_w<N>.json` (claim_patch.py format); run
  `python3 -I scripts/claim_patch.py <file> --dry-run` until it passes. Never apply it.
- Plain lines for every new or revised claim: `scratchpad/pdf1101/w<N>/simple.json`, as in the earlier brief (`q`,
  `pages`, `short`, `but`, `how`, `how_src`); for a revised claim start from its current entry in
  `data/site/simple.json` and change what the evidence requires.
- Anchors from the new cards: `page` is the card's printed page (or `PDF p. N`, or `p. N of the journal pre-proof`, as
  the card gives it); `located_by` "AI reader <N> (claim writer), from AI reader <M>'s study card"; `source_read` the
  card's.
- Report (at most 500 words) at the end of your final message: per claim what changed or what it rests on, its
  certainty, what is missing (companion papers the cards name as unread), and any card error you found.

## Your questions

### Reader 320: psychedelics, ketamine and cannabis
Cards: `sc_carhart_harris_2018`, `sc_estric_2025` (folder `cross-cutting`), `sc_strickland_2021` (`psilocybin`),
`sc_greenway_2024` (`ketamine`), `sc_freeman_2019` (`cannabis`).
1. Revise `cl_xc_mindset_before` and `cl_xc_setting_support` (psilocybin file) with Carhart-Harris et al. (2018) and
   Estric et al. (2025): what each adds and what it cannot show (an opinion piece's preview data; a review that maps how
   trials reported set and setting and found no trial comparing settings).
2. Revise `cl_xc_music` with Strickland et al. (2021), a randomized crossover of music genres in ten people (say what
   was and was not different, with the size of each difference).
3. Revise `cl_ket_music` with Greenway et al. (2024), a randomized trial of music during ketamine infusions for
   depression (blood pressure measured; no clinical outcome reported).
4. Revise `cl_can_cbd_with_thc` (cannabis file, section 6) with Freeman et al. (2019), the systematic review: what the
   studies found by route and dose condition (as conditions only), and how little rests on the oral and intravenous
   studies. Keep it a mixing question, findings only; nothing that suggests combining the two.

### Reader 321: the body, practices and services
Cards: `sc_marzuk_1998`, `sc_crandall_2002` (folder `cocaine`), `sc_faria_2020`, `sc_allott_2006` (`mdma`),
`sc_bass_1970` (`alkyl-nitrites-and-inhalants`), `sc_jones_1997`, `sc_van_nhat_2026` (`alcohol`), `sc_klevebrant_2022`
(`caffeine`), `sc_gelberg_2025`, `sc_park_2020` (`drug-checking`).
1. New: Are cocaine deaths more common in hot weather, and does cocaine raise body temperature? (cocaine, section 6;
   `cl_coc_heat`). The day-level comparison is unadjusted; the laboratory study is seven people and one low dose.
2. Revise `cl_mdma_hyponatremia` or `cl_mdma_hyponatremia_risk` (mdma file) with Faria et al. (2020), a narrative
   review: its figures are second-hand and its case table has errors; say so.
3. New, section 7 (findings only; it waits for the senior author): What do people who use ecstasy do before and after
   to reduce harm, as surveyed? (`cl_mdma_preloading_practices`; Allott & Redman 2006: what people reported; their
   effectiveness was not studied).
4. New: Can sniffing solvents cause sudden death? (`cl_inh_sudden_death`, substance `alkyl-nitrites-and-inhalants`,
   section 6; Bass 1970, a landmark case series without denominators; the mechanism is inferred.)
5. New: Does eating before drinking change blood alcohol? (`cl_alc_meals_bac`, alcohol, section 3; Jones et al. 1997,
   a small laboratory study; report as conditions, never as advice.)
6. Revise `cl_alc_protective_strategies` (section 7; alcohol file) with Van Nhat et al. (2026), the meta-analysis of
   randomized trials of protective behavioural strategies.
7. New: Can caffeine bring on panic attacks in people with panic disorder? (`cl_caf_panic`, caffeine, section 6;
   Klevebrant & Frick 2022.)
8. Revise the drug-checking answers the two test-strip studies bear on (`cl_dc_after_positive`, `cl_dc_overdose_strip_users`
   and, if it applies, `cl_benzo_harm_reduction_services`) with Gelberg et al. (2025) and Park et al. (2020): what people
   did after a result, as reported, and what was or was not measured.
