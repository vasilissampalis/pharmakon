# Before and during use, round 2: review and adjudication (AI readers 351 to 354), 1 November 2026

You are an independent methodologist and adjudicator for Pharmakon, an evidence library about drugs for the public and
for people who use drugs. You did not write these claims or cards and you took no part in the second reading. Project:
`/home/claude/drug-encyclopedia`. Scratch folder: `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/`
(`scratchpad/` below); your own folder is `scratchpad/pdf1101/a<N>/` (create it).

The site answers what research says people do before and during use (decision `p-before-during-after`: **findings
only**, no amounts, timings or regimens as advice, nothing on making a drug's effects stronger). First readers wrote
study cards from the senior author's PDFs; two claim writers (AI readers 320 and 321) wrote 5 new claims and revised 11
existing ones; four blind second readers (AI readers 336 to 339) re-read every source, gave a verdict on each claim and
checked each card; their unmatched anchors were then checked at the stated place. New claims are staged in
`data/claims/_incoming/pdf_w321.json`; the revised claims are in the main files (`data/claims/psilocybin.json`,
`ketamine.json`, `cannabis.json`, `mdma.json`, `alcohol.json`, `drug-checking.json`, `benzodiazepines.json`). Print
claims by id; never edit claim files. You close the round: **the source decides**, not the first reader and not the
second reader.

## Read first

1. `docs/METHODS.md`: §4.5, §5.3–5.6, §6 (all of it), §7, §8, §9, §12.
2. `docs/WRITING-RULES.md`: Rule 0, Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/REVIEW-BRIEF-2.md`, "What to check, claim by claim" (A to F): your review standard.
4. `docs/ADJUDICATION-BRIEF.md` Part B (how to correct a card and log it) and `docs/ADJUDICATION-BRIEF-R2.md` "What to do
   with each finding" (verdicts, patches, GRADE rules).
5. `scripts/claim_patch.py` (its docstring): your patch format.
6. The claim writers' briefs and reports: `data/verification/pdf-2026-11-01/BRIEF-claim-writers-bd.md`,
   `data/verification/bd-dd-2026-10-31/BRIEF-claim-writers-before-during.md` ("Hard rules for this round" apply to you
   unchanged) and `scratchpad/pdf1101/w320/report.md`, `w321/report.md`.

## Your group

| Reader | Claims | Cards you adjudicate |
|---|---|---|
| 351 | `cl_xc_mindset_before`, `cl_xc_setting_support`, `cl_xc_music`, `cl_ket_music` | `sc_carhart_harris_2018`, `sc_estric_2025`, `sc_strickland_2021`, `sc_greenway_2024` |
| 352 | `cl_can_cbd_with_thc`, `cl_caf_panic`, `cl_alc_meals_bac`, `cl_alc_protective_strategies` | `sc_freeman_2019`, `sc_klevebrant_2022`, `sc_van_nhat_2026` |
| 353 | `cl_coc_heat`, `cl_inh_sudden_death`, `cl_mdma_hyponatremia`, `cl_mdma_hyponatremia_risk`, `cl_mdma_preloading_practices` | `sc_bass_1970`, `sc_faria_2020`, `sc_allott_2006` |
| 354 | `cl_dc_after_positive`, `cl_dc_overdose_strip_users`, `cl_benzo_harm_reduction_services` | `sc_park_2020`, `sc_gelberg_2025` |

The cards are in `data/study-cards/_incoming/<folder>/`. `sc_jones_1997` is already ai-checked: leave it. **`sc_marzuk_1998`
and `sc_crandall_2002` (353): their second card check was stopped by an automatic filter and will not be redone; do not
check or change these two cards** (they stay first-pass); the claim anchors from those papers were checked and are
yours to adjudicate as usual. Only the parts of a revised claim that come from this round's sources are in scope; older
anchors and sentences from earlier rounds stay unless a sentence is now contradicted. `cl_alc_protective_strategies`
and `cl_mdma_preloading_practices` are section 7 claims: you review them like any other, and the senior author
approves the final version before it goes on the site.

## What you work from

- The second readers' outputs, one per source: `data/verification/pdf-2026-11-01/bd/out/<reference>.json`. The
  reconciliation reports: `data/verification/pdf-2026-11-01/bd/report-<claims file>.md`.
- The targeted checks: `data/verification/pdf-2026-11-01/bd/targeted/out_reader*.json` (already applied to the claims;
  their notes often flag wording the claim still uses).
- The plain lines the claim writers wrote: `scratchpad/pdf1101/w320/simple.json` and `w321/simple.json`; the live lines
  in `data/site/simple.json` (`claims` → id) for the revised claims.
- **The sources.** PDFs: `/mnt/user-data/uploads/DrugEncyclopedia/` + the task file's `pdf_path`
  (`data/verification/pdf-2026-11-01/bd/tasks/<reference>.json`); check every number you use on a page rendered with
  `pdftoppm -r 150` (tables and figures at `-r 300`). Online-first and manuscript versions: Carhart-Harris 2018 and
  Estric 2025 `PDF p. N`; Freeman 2019 "p. N of the journal pre-proof"; Park 2020 "AM p. N". Estric's landscape pages
  have a mirrored text layer (read them on the rendered page); Bass 1970 is a scan. No browser is needed.
- Not available (say so where a point turns on one: `deferred`, "supplement not read"): Strickland 2021's correction
  notice and Supporting Information, Greenway 2024's supplements and registry record, Klevebrant 2022's supplement,
  Freeman 2019's appendices, Van Nhat 2026's supplements.

## Points the editor has already noticed (check each; they are leads, not findings)

- **Van Nhat et al. (2026)** (352): "a step not described as planned" is contradicted (Methods 2.7 describes dropping
  influential studies); only 11 of the 15 trials enter any pooled estimate; the paper never says "all outcomes" were
  self-reported; the card's reporting issue 6 is corrected (six multi-arm trials, not five). The claim's certainty was
  raised from very low to low because the evidence is now randomized: check that rating against §6.3 and the round's
  rules, and keep the claim to findings.
- **Gelberg et al. (2025)** (354): "measures neither harm nor overdose" is wrong (baseline overdose is a covariate; the
  companion paper by Vickers-Smith et al. reports follow-up overdoses, not read here); Table 4's own benzodiazepine
  probabilities imply an odds ratio of about 3.6 to 5.3, not the printed 19.9, and by those probabilities the largest
  contrast is stimulants only (report as printed, with the inconsistency named); the amount odds ratio is a
  proportional-odds ratio over both cut-points.
- **Park et al. (2020)** (354): the overdose counts (4 to 1) are printed in Table 3, not an editors' subtraction;
  Park's own abstract gives "one month" and "96%", which the claim attributes to a review; key findings 4 to 7 are at
  Results paragraphs 5, 5, 6 and 4; the needle-exchange row does not add up.
- **Freeman et al. (2019)** (352): "mostly occasionally" is not shown (several studies took weekly, daily or current
  users; others only "at least once"); "shortly before" understates oral pre-treatment 90 to 480 minutes before THC; key
  finding 10 is corrected (CBD did not change THC's working-memory impairment, digit span included).
- **Klevebrant & Frick (2022)** (352): all five caffeine-against-placebo studies found more anxiety after caffeine;
  Table 1 gives Charney's dose as caffeine citrate 10 mg/kg: if that is the salt, the caffeine dose was about 375 mg,
  which would undo "no study tested less than 400 mg" (settle it at the source or word the claim so it does not depend
  on it, and keep doses as study conditions only); key finding 3 belongs at Results 3.5.2, 1st paragraph, p. 27.
- **Jones & Jönsson (1997)** (352): time to peak is counted from the start of drinking; the fed-fasting gap in the time
  to reach zero is under an hour by Figure 1f (a figure reading: say so).
- **Marzuk et al. (1998)** (353): the 10 heat deaths used to set the temperature threshold date from 1990 to 1995,
  overlapping the 1993–1995 test years. **Crandall et al. (2002)**: Figure 1 ends at about 37.79 against 37.55 °C, not
  37.5; "skin blood flow" was forearm vascular conductance; Figure 2 (about 54 against 67%) disagrees with the text (49
  against 70%).
- **Bass (1970)** (353): "attributed from the circumstances" is an inference the paper does not state; the author's
  mechanism also names carbon dioxide build-up; key finding 2 corrected (the benzene panel peaks in 1967).
- **Faria et al. (2020)** (353): the single-dose statement covers only deaths or lasting brain injury in women aged 15
  to 30; the table gives no amount for 14 of 21 deaths; a fatal row is cited only as "(2001)"; a row listed as
  methamphetamine cites a title about ecstasy; 46/52 = 88.5% (printed 89%); key finding 1 corrected.
- **Allott & Redman (2006)** (353): "most", not all, rodent studies used injection (key finding 10 corrected); the claim
  omits that 21.8% preloaded or postloaded to increase pleasure: report it as a finding about what people said, never
  as a way to make effects stronger.
- **Strickland et al. (2021)** (351): one of the ten people chose no music, so "each person's own chosen music" needs a
  qualifier; Results say "exhaled carbon dioxide" where Methods say carbon monoxide.
- **Estric et al. (2025)** (351): Table 1 sums to 761 participants (422 women), so the abstract's 763 is wrong; 21 ticks
  in the "safe environment" column against a printed 20; Gasser 2014 listed under both one and two preparatory
  interviews. Second reader 336 rates the interpretation gap substantial (the card says minor): settle the card's
  wording; a disagreement on the rating goes to the senior author.

## What to do

1. **Every second-reader verdict other than `supported`, every overstatement note, and every targeted-check note that
   flags wording** on your claims: check it at the source and give a verdict (`accept`, `accept-modified`, `reject`,
   `already-fixed`, `deferred`) with what you found.
2. **Your own review** of each claim (REVIEW-BRIEF-2 A to F): numbers against anchors and sources; for a predictor of an
   experience, which questionnaire was rated when and by whom, and whether the predictor was measured before the drug
   or recalled afterwards; who took part (healthy volunteers, patients, people using on their own) and where; for a
   laboratory or trial result, the conditions as the study gave them, the comparison and the size of each difference
   with its interval; for deaths (heat, solvents, water), how deaths were counted and against what; the wording
   against the design (association never as effect; a recalled attribution never as a predictor; a self-selected
   sample never as representative; a trend never as an effect; a review's citation never as its own finding); GRADE
   start, domains, arithmetic and reasoning per §6.3; status flags per §6.4; the debate box (§7) where a claim is
   contested. **Findings only:** doses, times and routes appear only as a study's conditions; no "safe" level; nothing
   on making effects stronger; authors' recommendations only when attributed.
3. **Write the claim patch** (`claim_patch.py` format, one object per claim you change, with a `change` line beginning
   "Review and adjudication, before-and-during round:"). Every number you put into a claim must be in an anchor's
   `extracted` text or be an editors' calculation you have recomputed. A needed number that no anchor carries goes in a
   new anchor (`evidence_add`, page and locator per §6.2, role, `located_by`: "AI reader <N> (adjudicator), from the
   PDF"); it enters as ai-located and a fresh reader will check it. A reworded anchor (`evidence_set` on `extracted`)
   also returns to ai-located: set `anchor_status` to `ai-located` in the same patch. Check with
   `python3 -I scripts/claim_patch.py <your patch> --dry-run` until it passes.
4. **Write the plain lines** for every claim of your group as they should read after your patch:
   `{"<claim id>": {"q", "pages", "short", "but", "how": [2 to 4], "how_src": [[ref ids] per point], "freq"?}}` (reading
   age 8 to 11; `short` about 14 words; `but` the main limit; name who took part and the comparison; never more than the
   claim says; numbers as counts out of 100, or 1,000 for rare things). Start from the claim writers' lines (or the
   live line for a revised claim) and change what the claim or the source requires.
5. **Adjudicate the cards** of your group: every `card_check` item the second reader marked `corrected`,
   `wrong-location` or `not-found`, each `missed` item that is true and matters, and the card errors the claim writers'
   reports name (ADJUDICATION-BRIEF Part B). Write each changed card in full to its file in
   `data/study-cards/_incoming/<folder>/` (the editor keeps a backup), log every change in `verification.disagreements`,
   set `verification.checked_by` to "AI reader <second reader> (blind second reading) and AI reader <N> (adjudication)"
   and `checked_on` to today, and set `verification.status` to `ai-checked` when the readers agree on the overall
   risk-of-bias judgment; run `python3 -I scripts/check_card.py <file>` until it passes. Domain-level disagreements and
   interpretation-gap differences go to the senior author, not into the card.
6. **Anything the senior author must decide** goes in your log under `for_senior_author`.

## Output (in `data/verification/pdf-2026-11-01/bd/adjudication/`)

- `<N>_log.json`: `{"reader": "AI reader <N> (adjudicator)", "date": "2026-11-01", "items": [{"claim_id" or "card",
  "source": "second reader <M> | targeted | own review", "finding": "...", "verdict": "...", "reason": "what you
  checked and found", "evidence": "page/section or card field", "patch_ref": "index in your patch or null"}],
  "for_round2": [{"claim_id", "anchor_index", "why"}], "for_senior_author": ["..."], "deferred": ["..."]}`. Every new
  or reworded anchor goes under `for_round2` (its index after your patch is applied: new anchors are appended in order).
- `<N>_patch.json`: the claim patch.
- `<N>_simple.json`: the plain lines.
- Corrected cards in `data/study-cards/_incoming/<folder>/`.
Write each file as you go (rewrite it after every claim or card), so nothing is lost if you are stopped. If an automatic
filter stops you, do not retry the same step: write what you have, say where you stopped, and finish.

## Rules (hard)

- Never edit `data/claims/` (including `_incoming/`), `docs/`, `scripts/` or `site/`, or any card outside your group:
  you write proposals and corrected copies; the editor applies them.
- Person-first words ("people who use drugs"); no words of alarm or reassurance. Quotations at most 15 words, at most
  one per claim, word for word.
- Final message under 250 words: counts by verdict; certainty or status changes (claim, from → to, rule); new anchors;
  cards changed and set to ai-checked; the five most consequential edits; what the senior author must decide. Then a
  short report (at most 300 words).
