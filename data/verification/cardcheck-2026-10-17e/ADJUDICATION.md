# Batch 3c adjudication (2026-10-17): McKetin 2020, the Ersche 2012 supplement, and three claims

You are the independent adjudicator (AI reader 37) for Pharmakon's methamphetamine page. You did not write or check any of the work below. The source decides; no reader's version is presumed right.

Project: `/home/claude/drug-encyclopedia`. Read `docs/ADJUDICATION-BRIEF.md` (Part B and the rules), `docs/METHODS.md` §5, §6, §9 and §12 as needed, and `data/verification/cardcheck-2026-10-17e/BRIEF.md` (what the second reader was asked).

## What there is
- Two first-pass cards in `data/study-cards/methamphetamine.json`: `sc_mcketin_2020` (new) and `sc_ersche_2012` (rewritten from the Supporting Online Material, 67 logged changes). First reader: AI reader 29; report, patch and suggested simple lines in `data/verification/batch3c-2026-10-17/`.
- The second reader's (AI reader 33) checks: anchors `data/verification/targeted-2026-10-17i/out_reader33.json` (all 7 confirmed; the editor has applied them, so both claims now carry checked anchors), cards `data/verification/cardcheck-2026-10-17e/out/mcketin_2020.json` and `ersche_2012.json`, claims `claims_reader33.json` (with replacement text for a new crime claim).
- The claims as they now stand in `data/claims/methamphetamine.json`: `cl_meth_violence` (0.8.1) and `cl_meth_siblings` (0.5.1), each with today's changelog entries.
- PDFs: `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Methamphetamine/McKetin_2020_ContributionMethamphetamineUseCrime.pdf`, `Ersche_2012_Supplement.pdf`, `Ersche_2012_AbnormalBrainStructureSiblings.pdf` (a cover page, then pp. 601–604).

## Part B: the cards
As `docs/ADJUDICATION-BRIEF.md` Part B says: check every item the second reader corrected or found missing, in the source; fix what is plainly factual; log every change in `verification.disagreements`; leave judgment differences for the senior author. Write each whole corrected card to `data/study-cards/_incoming/methamphetamine/<card_id>.json` and run `python3 -I scripts/check_card.py <file>` until it passes; set `verification.status` "ai-checked" (the readers agree on the overall risk-of-bias judgment), `checked_by` "AI reader 33 (card check) and AI reader 37 (adjudication)", `checked_on` today.

## Part C: the claims
1. `cl_meth_violence` and `cl_meth_siblings`: decide wording, relation, status label, GRADE and verification step, weighing reader 29's change, reader 33's view and the source. Questions: for violence, "is associated with" and "replicated by the same team" (two longitudinal cohorts with adjusted associations, sharing three authors; the MATES cohort is inside the review's pooled estimate, whose adjusted range includes no association), and reader 33's two edits; for siblings, the withdrawn sentence and reader 33's wording fixes. Write `data/verification/cardcheck-2026-10-17e/claims_patch.json` for `scripts/claim_patch.py` (`expect` on the fields you change) and check it with `--dry-run`. Do not apply it.
2. The new crime claim (`cl_meth_crime`, section 9): decide whether it is justified and write it whole, in the form of `schema/claim.schema.json`, to `data/verification/cardcheck-2026-10-17e/new_claim_crime.json` (a JSON list with one claim), starting from reader 33's replacement text and checking every number in the PDF. Its anchors point to `sc_mcketin_2020`; an anchor whose number and place match a key finding that reader 33 confirmed at the stated place in the card check may be "ai-checked" with `checked_by` "AI reader 33 (card check: key finding <n> confirmed at the stated place)" and `check_mode` "card-check"; any other anchor is "ai-located" by you. Validate it against the schema.
3. Suggested simple lines for all three claims (short, but, and two to four how points), following `docs/WRITING-RULES.md` (everyday words, never more than the claim, the But carries its main limit, "linked to" unless the study shows cause), in `data/verification/cardcheck-2026-10-17e/simple_reader37.json`, as `{"cl_meth_x": {"short": "...", "but": "...", "how": ["..."]}}`. Reader 29's are in `data/verification/batch3c-2026-10-17/reader29_simple.json`.
4. `data/verification/cardcheck-2026-10-17e/adjudication.json`: per card and per claim, your decisions with reasons, and what is left for the senior author.

## Rules
The hard rules of `docs/VERIFICATION-BRIEF.md` apply (quotations at most 15 words and at most one per claim, person-first language, no dosing or administration guidance). No browser is needed. Do not edit `data/study-cards/methamphetamine.json` or `data/claims/methamphetamine.json` directly. If an automatic safety filter stops one of your responses, do not retry or reword that content: save what is done and say what was not done. Write files as you go.

Final report, under 250 words: per card, changes made; per claim, the decisions; what is left for the senior author.
