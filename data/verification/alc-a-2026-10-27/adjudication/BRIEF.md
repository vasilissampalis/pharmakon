# Alcohol, Tier A: review and adjudication (AI readers 221, 222 and 223), 30 October 2026

You are an independent methodologist and adjudicator for Pharmakon, an evidence library about drugs for the public and
for people who use drugs. You did not write these claims or cards and you did not take part in the second reading.
Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/alc-a/a<N>/` (create it).

First readers wrote 37 study cards on alcohol's core papers; five claim writers (AI readers 170 to 174) turned them into
27 claims; ten blind second readers (AI readers 191 to 200) re-read every source, gave a verdict on each claim, and
checked each card; their unmatched anchors were then checked at the stated place. The claims are merged in
`data/claims/alcohol.json` (ids `cl_alc_` with first changelog date 2026-10-27; the older day-after and sleep claims in
that file are not yours) and the cards in `data/study-cards/alcohol.json`. You close the round: **the source decides**,
not the first reader and not the second reader.

## Read first

1. `docs/METHODS.md`: §4.5, §5.3–5.6, §6 (all of it), §7, §8, §9, §12.
2. `docs/WRITING-RULES.md`: Rule 0, Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/REVIEW-BRIEF-2.md`, "What to check, claim by claim" (A to F): your review standard.
4. `docs/ADJUDICATION-BRIEF.md` Part B (how to correct a card and log it) and `docs/ADJUDICATION-BRIEF-R2.md` "What to do
   with each finding" (verdicts, patches, GRADE rules).
5. `scripts/claim_patch.py` (its docstring): your patch format.
6. The claim writers' briefs and reports: `data/verification/alc-a-2026-10-27/BRIEF-claim-writers.md` (the grading
   rules this round used) and `scratchpad/alc-a/w170/report.md` to `w174/report.md`.

## Your group

| Reader | Claims | Cards you adjudicate |
|---|---|---|
| 221 | `cl_alc_low_volume_mortality`, `cl_alc_lowest_risk_amount`, `cl_alc_drinking_mortality_threshold`, `cl_alc_heart_cohorts`, `cl_alc_heart_genes`, `cl_alc_heart_heavy_days`, `cl_alc_stroke`, `cl_alc_blood_pressure`, `cl_alc_vessels_other` | `sc_di_castelnuovo_2006`, `sc_stockwell_2016`, `sc_stockwell_2024`, `sc_zhao_2023`, `sc_wood_2018`, `sc_chikritzhs_2015`, `sc_griswold_2018`, `sc_burton_2018`, `sc_bryazka_2022`, `sc_ronksley_2011`, `sc_roerecke_2012`, `sc_roerecke_2014`, `sc_holmes_2014`, `sc_millwood_2019`, `sc_biddinger_2022`, `sc_larsson_2020`, `sc_mukamal_2020` |
| 222 | `cl_alc_cancer_sites`, `cl_alc_cancer_light`, `cl_alc_cancer_burden`, `cl_alc_cirrhosis_amount`, `cl_alc_cirrhosis_women_men`, `cl_alc_cirrhosis_daily`, `cl_alc_deaths_global` | `sc_bagnardi_2015`, `sc_rumgay_2021`, `sc_rehm_2010`, `sc_roerecke_2019`, `sc_askgaard_2015`, `sc_rehm_2009` |
| 223 | `cl_alc_aud_prevalence`, `cl_alc_aud_treatment_gap`, `cl_alc_withdrawal_delirium`, `cl_alc_withdrawal_medicines`, `cl_alc_naltrexone`, `cl_alc_acamprosate`, `cl_alc_aud_other_medicines`, `cl_alc_combine_talking_therapy`, `cl_alc_pregnancy_drinking`, `cl_alc_fasd_fas_prevalence`, `cl_alc_fas_first_description` | `sc_grant_2015`, `sc_grant_2017`, `sc_carvalho_2019`, `sc_schuckit_2014`, `sc_mayo_smith_1997`, `sc_amato_2010`, `sc_jonas_2014`, `sc_mcpheeters_2023`, `sc_rosner_2010a`, `sc_rosner_2010b`, `sc_anton_2006`, `sc_popova_2017`, `sc_lange_2017`, `sc_jones_1973` |

Some sources serve two groups (Griswold 2018 serves 221 and 222; its card is 221's to change): a fact both groups state
must have the same number in both. You may read the other groups' claims to keep them consistent; patch only your own.

## What you work from

- The second readers' outputs, one per source: `data/verification/alc-a-2026-10-27/out/<reference>.json` (`claims`:
  verdict, overstatement and notes, their own anchors; `card_check`: each key finding and reporting issue, risk of bias,
  interpretation gap, `missed`). The reconciliation report: `data/verification/alc-a-2026-10-27/report.md`.
- The targeted checks: `data/verification/alc-a-2026-10-27/targeted/out_reader*.json` (already applied to the claims
  where confirmed or corrected; a `not-found` stays open for you; their notes often flag wording the claim still uses).
- The plain lines the claim writers wrote: `scratchpad/alc-a/w170/simple.json` to `w174/simple.json`.
- **The sources.** PDFs: `/mnt/user-data/uploads/DrugEncyclopedia/` + the reference's `verification.pdf_path`
  (`data/references/alcohol.json`); a text extraction of each is in `scratchpad/alc-a/numtext/` (pages separated by form
  feeds; printed pages as the cards give them; Askgaard 2015 and Mukamal 2020 are online-first PDFs). Web papers, as
  saved by the first readers (`scratchpad/alc-a/r154/` to `r161/`) and the second readers (`scratchpad/alc-a/s195/` to
  `s200/`). The app's browser is not reachable at the moment: settle web points from the saved texts and the two
  readers' extractions, and mark anything they cannot settle `deferred` with the reason "web source not reachable". If
  browser tools are present and working when you start, you may open a web paper in a tab of your own (made with
  `tabs_create`, its tabId on every call, closed at the end; never touch another tab).

## What to do

1. **Every second-reader verdict other than `supported`, every overstatement note, and every targeted-check note that
   flags wording** on your claims: check it at the source and give a verdict (`accept`, `accept-modified`, `reject`,
   `already-fixed`, `deferred`) with what you found.
2. **Your own review** of each claim (REVIEW-BRIEF-2 A to F): numbers against anchors and sources; each estimate's
   reference group and units as the source gives them; the wording against the design (association never as effect; a
   model estimate never as a count; a subgroup or one country never as everyone; a review's citation never as its own
   finding); GRADE start, domains, arithmetic and reasoning per §6.3 and the round's rules (observational and Mendelian
   randomization evidence starts low; model estimates graded from the evidence behind their risk curves; overlapping
   studies counted once); status flags per §6.4 (for model-estimate claims, decide whether `replicated-same-team` fits
   when the estimates come from different groups); the debate box (§7) where a claim is contested. **Findings only:** no
   amount that reads as advice on how much or how often to drink, no "safe" level, no medicine doses or regimens;
   authors' recommendations only when attributed, and only where they are the point.
3. **Write the claim patch** (`claim_patch.py` format, one object per claim you change, with a `change` line beginning
   "Review and adjudication, alcohol round:"). Every number you put into a claim must be in an anchor's `extracted`
   text or be an editors' calculation you have recomputed. A needed number that no anchor carries goes in a new anchor
   (`evidence_add`, page and locator per §6.2, role, `located_by`: "AI reader <N> (adjudicator), from the saved full
   text" or "… from the PDF"); it enters as ai-located and a second reader will check it later (say so in the log).
   Check with `python3 -I scripts/claim_patch.py <your patch> --dry-run` until it passes.
4. **Write the plain lines** for every claim of your group as they should read after your patch:
   `{"<claim id>": {"q", "short", "but", "how": [2 to 4], "freq"?}}` (reading age 8 to 11; `short` about 14 words;
   `but` the main limit; name the comparison group; never more than the claim says; numbers as counts out of 100, or
   1,000 for rare things). Start from the claim writer's lines and change what the claim or the source requires.
5. **Adjudicate the cards** of your group: every `card_check` item the second reader marked `corrected`,
   `wrong-location` or `not-found`, each `missed` item that is true and matters, and the card errors the claim writers'
   reports name (ADJUDICATION-BRIEF Part B). Write each changed card in full to
   `data/study-cards/_incoming/alcohol/<card id>.json`, log every change in `verification.disagreements`, set
   `verification.checked_by` to "AI reader <second reader> (blind second reading) and AI reader <N> (adjudication)" and
   `checked_on` to today, and set `verification.status` to `ai-checked` when the readers agree on the overall
   risk-of-bias judgment; run `python3 -I scripts/check_card.py <file>` until it passes. Domain-level disagreements and
   interpretation-gap differences go to the senior author, not into the card.
6. **Anything the senior author must decide** goes in your log under `for_senior_author` (for example how Mendelian
   randomization was graded, and any status or wording choice that is a judgment rather than a rule).

## Output (in `data/verification/alc-a-2026-10-27/adjudication/`)

- `<N>_log.json`: `{"reader": "AI reader <N> (adjudicator)", "date": "2026-10-30", "items": [{"claim_id" or "card",
  "source": "second reader <M> | targeted | own review", "finding": "...", "verdict": "...", "reason": "what you
  checked and found", "evidence": "page/section or card field", "patch_ref": "index in your patch or null"}],
  "for_senior_author": ["..."], "deferred": ["..."]}`
- `<N>_patch.json`: the claim patch.
- `<N>_simple.json`: the plain lines.
- Corrected cards in `data/study-cards/_incoming/alcohol/`.

## Rules (hard)

- Never edit `data/claims/`, `data/study-cards/alcohol.json`, `docs/`, `scripts/` or `site/`: you write proposals and
  corrected copies; the editor applies them.
- No advice on drinking amounts, no "safe" or "no risk" wording, no withdrawal regimens or medicine doses; findings
  only. Person-first words ("people who drink", "people with alcohol use disorder"); no words of alarm or reassurance.
  Quotations at most 15 words, at most one per claim, word for word.
- This session cannot write report files for you: put a short report (at most 300 words) at the end of your final
  message. The rest of the final message under 250 words: counts by verdict; certainty or status changes (claim, from →
  to, rule); new anchors; cards changed and set to ai-checked; the five most consequential edits; what the senior
  author must decide.
