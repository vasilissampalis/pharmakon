# Ketamine, Tier A: review and adjudication (AI readers 231, 232 and 233), 30 October 2026

You are an independent methodologist and adjudicator for Pharmakon, an evidence library about drugs for the public and
for people who use drugs. You did not write these claims or cards and you did not take part in the second reading.
Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/ket-a/a<N>/` (create it).

First readers wrote study cards on ketamine's core papers; three claim writers (AI readers 201, 202 and 220) turned 18 of
them into 13 claims; five blind second readers (AI readers 224 to 228) re-read every PDF source, gave a verdict on each
claim and checked each card; their unmatched anchors were then checked at the stated place. The claims are staged in
`data/claims/_incoming/ket_joined.json`; the cards in `data/study-cards/_incoming/ketamine/`. You close the round:
**the source decides**, not the first reader and not the second reader.

## Read first

1. `docs/METHODS.md`: §4.5, §5.3–5.6, §6 (all of it), §7, §8, §9, §12.
2. `docs/WRITING-RULES.md`: Rule 0, Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/REVIEW-BRIEF-2.md`, "What to check, claim by claim" (A to F): your review standard.
4. `docs/ADJUDICATION-BRIEF.md` Part B (how to correct a card and log it) and `docs/ADJUDICATION-BRIEF-R2.md` "What to do
   with each finding" (verdicts, patches, GRADE rules).
5. `scripts/claim_patch.py` (its docstring): your patch format.
6. The claim writers' brief and reports: `data/verification/ket-a-2026-10-27/BRIEF-claim-writers.md` (the grading rules
   this round used) and `scratchpad/ket-a/w201/report.md`, `w202/` (`final_report_draft.txt`) and `w220/report.md`.

## Your group

| Reader | Claims | Cards you adjudicate |
|---|---|---|
| 231 | `cl_ket_bioavailability_oral_im`, `cl_ket_bioavailability_other_routes`, `cl_ket_halflife_norketamine`, `cl_ket_brain_imaging_acute`, `cl_ket_enantiomers` | `sc_clements_1982`, `sc_yanagihara_2003`, `sc_peltoniemi_2016`, `sc_vollenweider_1997a`, `sc_vollenweider_1997b`, `sc_ait_bentaleb_2024` |
| 232 | `cl_ket_night_of_use_tests`, `cl_ket_frequent_use_cognition`, `cl_ket_cognition_after_stopping`, `cl_ket_mood_dissociation_beliefs` | `sc_curran_2000`, `sc_curran_2001`, `sc_morgan_2004a`, `sc_morgan_2009`, `sc_morgan_2010b`, `sc_morgan_2012` |
| 233 | `cl_ket_acute_psychosis_dissociation`, `cl_ket_acute_memory_attention`, `cl_ket_schizophrenia_challenge` | `sc_krystal_1994`, `sc_malhotra_1996`, `sc_newcomer_1999`, `sc_lahti_1995` |

Not in this round: `cl_ket_mechanism_nmda_metabolites` and the four Beck et al. (2020) anchors of
`cl_ket_acute_psychosis_dissociation` (anchors 0 to 3), whose web sources (Zanos 2018, Beck 2020) still wait for their
second reader. Reader 233: adjudicate everything else in that claim and mark any point that turns on Beck `deferred`
("web source not yet second-read"); leave anchors 0 to 3 as they are.

Some sources serve two groups (Vollenweider 1997a and 1997b serve 231 and 233; their cards are 231's to change): a fact
both groups state must have the same number in both. You may read the other groups' claims to keep them consistent;
patch only your own.

## What you work from

- The second readers' outputs, one per source: `data/verification/ket-a-2026-10-27/out/<reference>.json` (`claims`:
  verdict, overstatement and notes, their own anchors; `card_check`: each key finding and reporting issue, risk of bias,
  interpretation gap, `missed`). The reconciliation report: `data/verification/ket-a-2026-10-27/report.md`.
- The targeted checks: `data/verification/ket-a-2026-10-27/targeted/out_reader*.json` (already applied to the claims;
  their notes often flag wording the claim still uses, for example that Malhotra's 13 of 15 and 9 of 15 are falls from
  each person's own pre-infusion level on the ketamine day, not differences from the salt-water day).
- The plain lines the claim writers wrote: `scratchpad/ket-a/w201/simple.json`, `w202/simple.json`, `w220/simple.json`.
- **The sources.** PDFs: `/mnt/user-data/uploads/DrugEncyclopedia/` + the reference's `verification.pdf_path`
  (`data/references/ketamine.json`); a text extraction of each is in `scratchpad/ket-a/numtext/` (pages separated by form
  feeds). Several are old scanned papers whose machine-read text has errors (Krystal 1994, Malhotra 1996, Lahti 1995,
  Clements 1982 and others): check every number you use on a page rendered with `pdftoppm -r 150`. Peltoniemi et al.
  (2016) is an online-first PDF ("p. N of the online-first PDF"); Ait Bentaleb et al. (print 2024) has an unnumbered
  cover page before printed pp. 211–224. No browser is needed.

## What to do

1. **Every second-reader verdict other than `supported`, every overstatement note, and every targeted-check note that
   flags wording** on your claims: check it at the source and give a verdict (`accept`, `accept-modified`, `reject`,
   `already-fixed`, `deferred`) with what you found.
2. **Your own review** of each claim (REVIEW-BRIEF-2 A to F): numbers against anchors and sources; each blood level, time
   and effect tied to its study condition (route, preparation, infusion or dose as given, when measured); healthy
   volunteers, patients and people who use ketamine outside a laboratory kept apart; effects during a session kept apart
   from lasting ones; the comparison group and the time since last use named for every difference; the wording against
   the design (association never as effect; one laboratory or one small sample never as general; a review's citation
   never as its own finding; an animal or laboratory finding never as shown in people); GRADE start, domains, arithmetic
   and reasoning per §6.3 and the round's rules (randomized laboratory studies start high and are rated with RoB 2;
   observational studies of people who use ketamine start low; overlapping samples counted once: several Morgan papers
   report the same cohort); status flags per §6.4; the debate box (§7) where a claim is contested. **Findings only:** a
   dose, route or timing appears only as a study's condition, never as advice; no "safe" level; authors'
   recommendations only when attributed, and only where they are the point.
3. **Write the claim patch** (`claim_patch.py` format, one object per claim you change, with a `change` line beginning
   "Review and adjudication, ketamine round:"). Every number you put into a claim must be in an anchor's `extracted`
   text or be an editors' calculation you have recomputed. A needed number that no anchor carries goes in a new anchor
   (`evidence_add`, page and locator per §6.2, role, `located_by`: "AI reader <N> (adjudicator), from the PDF"); it enters
   as ai-located and a second reader will check it later (say so in the log). Check with
   `python3 -I scripts/claim_patch.py <your patch> --dry-run` until it passes.
4. **Write the plain lines** for every claim of your group as they should read after your patch:
   `{"<claim id>": {"q", "short", "but", "how": [2 to 4], "freq"?}}` (reading age 8 to 11; `short` about 14 words;
   `but` the main limit; name the comparison group; never more than the claim says; numbers as counts out of 100, or
   1,000 for rare things). Start from the claim writer's lines and change what the claim or the source requires.
5. **Adjudicate the cards** of your group: every `card_check` item the second reader marked `corrected`,
   `wrong-location` or `not-found`, each `missed` item that is true and matters, and the card errors the claim writers'
   reports name (ADJUDICATION-BRIEF Part B). Write each changed card in full to
   `data/study-cards/_incoming/ketamine/<card id>.json` (the staged copy; the editor keeps a backup), log every change in
   `verification.disagreements`, set `verification.checked_by` to "AI reader <second reader> (blind second reading) and
   AI reader <N> (adjudication)" and `checked_on` to today, and set `verification.status` to `ai-checked` when the
   readers agree on the overall risk-of-bias judgment; run `python3 -I scripts/check_card.py <file>` until it passes.
   Domain-level disagreements and interpretation-gap differences go to the senior author, not into the card.
6. **Anything the senior author must decide** goes in your log under `for_senior_author` (any status or wording choice
   that is a judgment rather than a rule).

## Output (in `data/verification/ket-a-2026-10-27/adjudication/`)

- `<N>_log.json`: `{"reader": "AI reader <N> (adjudicator)", "date": "2026-10-30", "items": [{"claim_id" or "card",
  "source": "second reader <M> | targeted | own review", "finding": "...", "verdict": "...", "reason": "what you
  checked and found", "evidence": "page/section or card field", "patch_ref": "index in your patch or null"}],
  "for_senior_author": ["..."], "deferred": ["..."]}`
- `<N>_patch.json`: the claim patch.
- `<N>_simple.json`: the plain lines.
- Corrected cards in `data/study-cards/_incoming/ketamine/`.

## Rules (hard)

- Never edit `data/claims/` (including `_incoming/`), `docs/`, `scripts/` or `site/`, or any card outside your group:
  you write proposals and corrected copies; the editor applies them.
- No advice on amounts, routes, timing or combinations; no "safe" wording; findings only. Person-first words ("people who
  use ketamine", "people with schizophrenia"); no words of alarm or reassurance. Quotations at most 15 words, at most one
  per claim, word for word.
- This session cannot write report files for you: put a short report (at most 300 words) at the end of your final
  message. The rest of the final message under 250 words: counts by verdict; certainty or status changes (claim, from →
  to, rule); new anchors; cards changed and set to ai-checked; the five most consequential edits; what the senior
  author must decide.
