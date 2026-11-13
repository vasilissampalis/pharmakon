# Facts about drug use, round 2: review and adjudication (AI readers 355 to 358), 1 November 2026

You are an independent methodologist and adjudicator for Pharmakon, an evidence library about drugs for the public and
for people who use drugs. You did not write these claims or cards and you took no part in the second reading. Project:
`/home/claude/drug-encyclopedia`. Scratch folder: `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/`
(`scratchpad/` below); your own folder is `scratchpad/pdf1101/a<N>/` (create it).

The site's "Facts about drug use" page answers general questions, each read with a critical eye (decision
`s-quiz-v2`). First readers wrote study cards from the senior author's PDFs; two claim writers (AI readers 323 and 324)
wrote 9 new claims and revised 4 existing ones; seven blind second readers (AI readers 340 to 346) re-read every source,
gave a verdict on each claim and checked each new card; their unmatched anchors were then checked at the stated place.
New claims are staged in `data/claims/_incoming/pdf_w323.json` and `pdf_w324.json`; the revised claims are in
`data/claims/general.json` (`cl_gen_telescoping`, `cl_gen_genes_family`, `cl_gen_words_labels_stigma`) and
`data/claims/alcohol.json` (`cl_alc_early_drinking_later_problems`). Print claims by id; never edit claim files. You
close the round: **the source decides**, not the first reader and not the second reader.

## Read first

1. `docs/METHODS.md`: §4.5, §5.3–5.6, §6 (all of it), §7, §8, §9, §12.
2. `docs/WRITING-RULES.md`: Rule 0, Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/REVIEW-BRIEF-2.md`, "What to check, claim by claim" (A to F): your review standard.
4. `docs/ADJUDICATION-BRIEF.md` Part B (how to correct a card and log it) and `docs/ADJUDICATION-BRIEF-R2.md` "What to do
   with each finding" (verdicts, patches, GRADE rules).
5. `scripts/claim_patch.py` (its docstring): your patch format.
6. The claim writers' briefs and reports: `data/verification/pdf-2026-11-01/BRIEF-claim-writers-general.md`,
   `data/verification/gen-a-2026-11-01/BRIEF-claim-writers.md` ("Hard rules for this round" and "Grading" apply to you
   unchanged) and `scratchpad/pdf1101/w323/report.md`, `w324/report.md`.

## Your group

| Reader | Claims | Cards you adjudicate |
|---|---|---|
| 355 | `cl_gen_telescoping`, `cl_alc_early_drinking_later_problems`, `cl_gen_early_drug_use` | `sc_randall_1999`, `sc_grant_1997` (folder `alcohol`), `sc_khan_2013`, `sc_lynskey_2003` (`cannabis`), `sc_grant_1998` (`cross-cutting`) |
| 356 | `cl_gen_gateway`, `cl_gen_polydrug` | `sc_kandel_1975`, `sc_wagner_2002`, `sc_connor_2014` (`cross-cutting`), `sc_morral_2002` (`cannabis`), `sc_gouzoulis_mayfrank_2006` (`mdma`) |
| 357 | `cl_gen_remission`, `cl_gen_rat_park`, `cl_coc_alternative_rewards`, `cl_alc_expectancy` | `sc_robins_1975`, `sc_fleury_2016`, `sc_gage_2019`, `sc_petrie_1996` (`cross-cutting`), `sc_mellor_2019`, `sc_marlatt_1973`, `sc_hull_1986` (`alcohol`), `sc_hart_2000` (`cocaine`) |
| 358 | `cl_gen_stigma_health_care`, `cl_gen_release_deaths`, `cl_gen_genes_family`, `cl_gen_words_labels_stigma` | `sc_van_boekel_2013`, `sc_borschmann_2024`, `sc_visscher_2008`, `sc_kelly_2010` (`cross-cutting`) |

The cards are in `data/study-cards/_incoming/<folder>/`. Cards cited by several groups (Lynskey 2003: 355 and 356) are
changed only by the reader named above; a fact two groups state must have the same number in both. The older cards
read on the web (Degenhardt et al. 2010, Lenoir et al. 2007, Vanyukov et al. 2012, Vergés et al. 2012, and the earlier
ai-checked cards) are already checked: do not change them; list any error found in them under `for_senior_author`
(the claim writer noted that `sc_lenoir_2007` still calls Hart 2000 and Gage 2019 "not yet appraised": list it). Only
the parts of a revised claim that come from this round's sources are in scope; older anchors and sentences stay unless a
sentence is now contradicted.

## What you work from

- The second readers' outputs, one per source: `data/verification/pdf-2026-11-01/gen/out/<reference>.json`. The
  reconciliation reports: `data/verification/pdf-2026-11-01/gen/report-<claims file>.md`.
- The targeted checks: `data/verification/pdf-2026-11-01/gen/targeted/out_reader*.json` (already applied to the claims;
  their notes often flag wording the claim still uses).
- The plain lines the claim writers wrote: `scratchpad/pdf1101/w323/simple.json` and `w324/simple.json`; the live lines
  in `data/site/simple.json` (`claims` → id) for the revised claims.
- **The sources.** PDFs: `/mnt/user-data/uploads/DrugEncyclopedia/` + the task file's `pdf_path`
  (`data/verification/pdf-2026-11-01/gen/tasks/<reference>.json`); check every number you use on a page rendered with
  `pdftoppm -r 150` (tables and figures at `-r 300`). Fleury 2016 (in press) and Gage & Sumnall 2019 (accepted
  manuscript) are cited as `PDF p. N`; Khan et al. 2013 as "PDF p. N of the in-press version". Old scans (Robins 1975,
  Kandel 1975, Marlatt 1973, Hull & Bond 1986, Petrie 1996, Grant & Dawson 1997 and 1998): the rendered page is the
  source. Web full texts (the four older sources): the second reader's saved copies in `scratchpad/pdf1101/s346/`; if a
  point cannot be settled from them, open the PMC page in one tab of your own in the app's browser (load the tools once
  with ToolSearch, query `mcp__remote-devices__Claude_Browser__`, max_results 64; `tabs_create`, its tabId on every
  call, closed at the end; never `preview_start`; never touch another tab; no search engines, no PDFs or downloads;
  stop at any check page).
- Not available (say so where a point turns on one: `deferred`, "not read"): supplements and appendices the readers
  name (Borschmann 2024 appendix and protocol, Mellor 2019 supplement, Degenhardt 2010 supplementary tables), and the
  companion papers the writers list as unread (for example Alexander et al. 1978 and 1981, Fergusson et al. 2006, Odgers
  et al. 2008, Richmond-Rakerd et al. 2016): a claim may name what they would add, never what they found.

## Points the editor has already noticed (check each; they are leads, not findings)

- **Degenhardt, Dierker et al. (2010)** (356, 355): "except where cannabis was rare" is incomplete (South Africa, with
  moderate cannabis use, 59.2% of people who used other illegal drugs had not used cannabis first; Mexico 48.4%); Table
  4's "not already used cannabis" includes people who never used it; "depended on" should be "varied with"; the
  Netherlands–USA odds ratios do not illustrate "weaker where cannabis was more common". For early use (355): the
  drug-dependence models drew on at most 11 of the 17 surveys, among people who had used each drug, and the 0.2–0.7
  range includes alcohol and tobacco dependence (0.2–0.5 for drug dependence).
- **Vergés et al. (2012)** (357): 1,172 is an editors' sum (422 + 750); treatment is never mentioned in the paper.
- **Lenoir et al. (2007)** (357): the rats chose between cocaine and sweetened water, against plain water elsewhere; the
  abstract's 94% cannot be rebuilt from N = 43; the authors frame any human extension as speculation.
- **Vanyukov et al. (2012)** (356): no co-twin-control study is cited (classical twin studies are); the review calls the
  cannabis association itself negligible; it argues one side.
- **Grant & Dawson (1997)** (355): other drug use, conduct problems and psychiatric disorders were "not taken into
  account in this analysis", not "not measured" (the card repeats "not measured" in three fields: correct them); the
  duration and age adjustments overlap.
- **Khan et al. (2013)** (355): "about 50 comparisons" counts outcomes; there are about 82 tests in Tables 2–4 (about
  103 with Table 1), so "more than 50" is safer.
- **Randall et al. (1999)** (355): the "same entry ages" cover all 1,589 people, not the 735 at first treatment; the 3.9-
  and 4.2-year gaps come from two different samples; Results and Discussion disagree on the loss-of-control interaction
  (printed p ≤ .001, recomputed about .010); the study did not ask ages at first drink.
- **Grant & Dawson (1998)** and **Lynskey et al. (2003)** (355): people "met criteria for" dependence (they did not
  "report" it); the twin study's drug "use disorders" are a simplified symptom count, not formal DSM-IV (p. 429); the
  concordance counts imply 865 early starters against a sample of 861; the card's "later" alcohol dependence has no
  timing in the data; "the only prospective study the authors cite" holds only for studies of age at first use; the
  paper does not place Robins & Murphy (1967) in St. Louis.
- **Wagner & Anthony (2002)**, **Morral et al. (2002)** and **Kandel (1975)** (356): Wagner's 15 and 20.4 compare people
  who had used cannabis with people who had not ("against no cannabis", not "against none"; the card repeats it);
  Morral's "reliability 0.8" is a correlation of 0.8 (64% of the variance), and the model's relative risk of 157 and the
  survey's 24 may not measure the same thing; Kandel's body also calls cannabis a "crucial step" (p. 913), the
  percentages are survey-weighted but not adjusted for confounders, and Table 1's parts add to 25% against 26% in the
  text. **Gouzoulis-Mayfrank & Daumann (2006)** (356): "some", not "often", earlier studies did not record other drugs
  (p. 191); "difficult", not "cannot separate" (p. 189); "up to 234" may count whole samples; key findings 0 and 10
  corrected for the same hedges.
- **Hull & Bond (1986)** and **Marlatt et al. (1973)** (357): Hull & Bond answer the separation question on p. 358
  (alcohol and belief never both had significant effects on the same measure); they report no doses, so "at the low
  doses these designs allow" has no basis; the pooled drinking effect mixes desire to drink with amount drunk; reporting
  issue 3 corrected (0.66 is about 58% of 1.13); Marlatt's 0.66 averages three measures (amount, sips, amount per sip);
  the exact interval for d is 0.60 to 1.66; "a moderate effect cannot be ruled out" needs its direction; Marlatt's key
  finding 11 is in the Discussion's 4th paragraph; the authors' own alternative (men may have drunk more to find the
  vodka taste, p. 240) is missing.
- **Petrie (1996)** (357): "did not find lower intake in colony rats" holds only for Experiment 1 (in Experiment 2 the
  colony averages were lower at 3 of 4 strengths, untested and smaller than in 1981); "no differently at the three
  weaker ones" should be "no significant difference" (colony means were higher at all three); key finding 2 corrected;
  its procedure differed in detail from the 1981 study it repeated. **Gage & Sumnall (2019)** (357): the 57-day forced
  period included 4 choice days (key finding 3); Table 1 prints df 1/69 although at most 28 rats remained. **Hart et al.
  (2000)** (357): the vouchers could be cashed only at discharge, so the rewards were not immediate; at 50 mg the rates
  were 77% and 90%; the card's RoB 2 tool fits poorly because the voucher order was fixed (ROBINS-I; the overall "high"
  stands either way). **Connor et al. (2014)** (356): the cognition sentence leaves out the review's report of large
  differences on standard tests outside the scanner (ref. 62, p. 272); "DSM-IV" is the editors' label, not the review's
  (key finding 1).
- **Borschmann et al. (2024)** (358): Figure 2's caption says the time-period analyses left out two cohorts (New
  Zealand's only cohort and one from Washington), so the days 2–7, weekly and more-than-one-year rates and rate ratios
  rest on 16 cohorts in 7 countries, not 18 in 8; the paper hedges the release-day miscoding ("might", "probably at
  least partially"); it does not say which release the "more than 4 weeks" split counts from. The claim writer's short
  answer ("Yes. Deaths were most common in the first week") needs the days 2–7 definition and should not open with
  "Yes" if the certainty does not carry it.
- **van Boekel et al. (2013)** (358): seven, not eight, other European countries (Scotland is in the UK); five, not "at
  least six", summaries use moderate, neutral, appropriate or positive (Strauser says "below the criterion for negative
  stigma"); the response-rate range leaves out Strauser (100%); reporting issue 5 corrected (search set #30 needs no
  attitude term). **Kelly & Westerhoff (2010)** (358): the "correlations" are factor loadings; p .020 one-sided (.041
  two-sided) and d 0.17–0.18 recompute.

## What to do

1. **Every second-reader verdict other than `supported`, every overstatement note, and every targeted-check note that
   flags wording** on your claims: check it at the source and give a verdict (`accept`, `accept-modified`, `reject`,
   `already-fixed`, `deferred`) with what you found.
2. **Your own review** of each claim (REVIEW-BRIEF-2 A to F): numbers against anchors and sources; who was sampled,
   where and when; how the outcome was defined; whether ages and intervals were recalled; what was adjusted for; what
   each design can and cannot show (co-twin, adoption, survey, cohort, model, experiment); a difference among people who
   already have a disorder never as a difference in risk; an order of first use never as a "gateway" effect; a
   heritability never as a share of one person's risk; animal findings labelled and never standing in for people; a
   review's citation never as its own finding; GRADE start, domains, arithmetic and reasoning per §6.3 and the round's
   rules (claims resting only on narrative reviews stay at draft and say their figures are second-hand); status flags
   per §6.4; the debate box (§7) where a claim is contested (gateway, telescoping, Rat Park). **Findings only.**
3. **Write the claim patch** (`claim_patch.py` format, one object per claim you change, with a `change` line beginning
   "Review and adjudication, facts round:"). Every number you put into a claim must be in an anchor's `extracted` text
   or be an editors' calculation you have recomputed. A needed number that no anchor carries goes in a new anchor
   (`evidence_add`, page and locator per §6.2, role, `located_by`: "AI reader <N> (adjudicator), from the PDF" or "from
   the web full text"); it enters as ai-located and a fresh reader will check it. A reworded anchor (`evidence_set` on
   `extracted`) also returns to ai-located: set `anchor_status` to `ai-located` in the same patch. Check with
   `python3 -I scripts/claim_patch.py <your patch> --dry-run` until it passes.
4. **Write the plain lines** for every claim of your group as they should read after your patch:
   `{"<claim id>": {"q", "pages", "short", "but", "how": [2 to 4], "how_src": [[ref ids] per point], "freq"?}}` (reading
   age 8 to 11; `short` about 14 words, a direct answer without its own "but"; `but` the main limit; name who was
   studied and the comparison; never more than the claim says; numbers as counts out of 100, or 1,000 for rare things).
   Start from the claim writers' lines (or the live line for a revised claim) and change what the claim or the source
   requires.
5. **Adjudicate the cards** of your group: every `card_check` item the second reader marked `corrected`,
   `wrong-location` or `not-found`, each `missed` item that is true and matters, and the card errors the claim writers'
   reports name (ADJUDICATION-BRIEF Part B). Write each changed card in full to its file in
   `data/study-cards/_incoming/<folder>/` (the editor keeps a backup), log every change in `verification.disagreements`,
   set `verification.checked_by` to "AI reader <second reader> (blind second reading) and AI reader <N> (adjudication)"
   and `checked_on` to today, and set `verification.status` to `ai-checked` when the readers agree on the overall
   risk-of-bias judgment; run `python3 -I scripts/check_card.py <file>` until it passes. Domain-level disagreements and
   interpretation-gap differences go to the senior author, not into the card.
6. **Anything the senior author must decide** goes in your log under `for_senior_author`.

## Output (in `data/verification/pdf-2026-11-01/gen/adjudication/`)

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
- Person-first words; quote a study's own labels (for example "addict" or "a substance abuser") only in quotation marks,
  as the study's wording; no words of alarm or reassurance. Quotations at most 15 words, at most one per claim, word for
  word.
- Final message under 250 words: counts by verdict; certainty or status changes (claim, from → to, rule); new anchors;
  cards changed and set to ai-checked; the five most consequential edits; what the senior author must decide. Then a
  short report (at most 300 words).
