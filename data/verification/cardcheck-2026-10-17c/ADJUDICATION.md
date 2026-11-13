# Batch 3b adjudication (2026-10-17): cards and claims

You are the independent adjudicator (AI reader 23) for Pharmakon's methamphetamine page. You did not write or check any of the work below. The source decides; no reader's version is presumed right.

Project: `/home/claude/drug-encyclopedia`. Read `docs/ADJUDICATION-BRIEF.md` (Part B and the rules), `docs/METHODS.md` §5, §6, §9 and §12 as needed, and `data/verification/cardcheck-2026-10-17c/BRIEF.md` (what the second readers were asked).

## What there is
- Seven first-pass cards in `data/study-cards/methamphetamine.json`: sc_fluyau_2019, sc_chung_2026, sc_hall_2026, sc_murrie_2020 (first reader: AI reader 19) and sc_huang_2022, sc_tanz_2025, sc_dean_2018 (AI reader 20).
- First readers' reports: `data/verification/batch3b-2026-10-17/reader19_report.md` and `reader20_report.md`.
- Second readers' card checks: `data/verification/cardcheck-2026-10-17c/out/<reference>.json`; their views on the claims: `claims_reader21.json` and `claims_reader22.json`.
- Second readers' anchor checks, already applied to the claims: `data/verification/targeted-2026-10-17g/out_reader21.json` and `out_reader22.json`.
- The claims as they now stand: `data/claims/methamphetamine.json` (cl_meth_psychosis_treatment, cl_meth_psychosis_course, cl_meth_psychosis_association, cl_meth_us_trends, cl_meth_cognition_normal_range). Earlier today they were adjudicated by AI reader 18 (`data/verification/cardcheck-2026-10-17c/adjudication.json`); this round adds the seven newer papers.
- The sources are web full texts: each card's `verification.source_read` names the page. Read them in the desktop app's browser, in a tab you create yourself (load the tools with ToolSearch as `docs/STUDY-CARD-BRIEF.md` says; never touch another tab; no downloads, no PDF links, no CAPTCHAs; close your tab when you finish). If the browser is unreachable, say so and settle only what the second readers' notes and the project files allow, listing the rest for the editor.

## Part B: the cards
Exactly as `docs/ADJUDICATION-BRIEF.md` Part B says: check every item a second reader flagged, in the source; fix what is plainly factual; log every change in `verification.disagreements`; leave judgment differences for the senior author. Write each whole corrected card to `data/study-cards/_incoming/methamphetamine/<card_id>.json` and run `python3 -I scripts/check_card.py <file>` until it passes. Set `verification.status` to `ai-checked` only if the readers agree on the overall risk-of-bias judgment; set `checked_by` to "AI reader 15/16/17 (card check) and AI reader 18 (adjudication)" as fits, `checked_on` today.

**AMSTAR 2 item 4.** Apply the instrument as written (an unjustified language limit is "no"), as batch 3 did.

## Part C: the claims
For each of the five claims, weigh the first reader's change, the second reader's view and the source, and decide wording, status label (METHODS §6.4), GRADE and verification step, as batch 3 did. Questions raised by the readers:
- cl_meth_psychosis_treatment: reader 19 proposed "mixed"; AI reader 18 had set "single study" before these papers were read; AI reader 21 prefers "mixed" for inconsistent findings (not differing populations) and would then rate inconsistency down one level (still very low). Settle the label and the domain, and how the claim describes Chung 2026 (its registered primary outcome changed after the trial ended; check whether follow-up was cut from 36 to 24 months first).
- cl_meth_psychosis_course: AI reader 21 would call Murrie 2020's 22% an average and lead with the spread (I² 96%).
- cl_meth_us_trends: AI reader 22 says "found meth in" should read "meth was one of the causes", with a warning that Tanz 2025's share cannot be compared with 2019; it also suggests splitting the claim (recommend only if clearly needed).
- cl_meth_psychosis_association and cl_meth_cognition_normal_range: the second readers' small statement edits ("not adjusted for" rather than "not measured"; "difficult to disentangle").

Write:
1. `data/verification/cardcheck-2026-10-17c/claims_patch.json`: a patch for `scripts/claim_patch.py` (format in its docstring: `set`, `replace`, `bump`, `change`; use `expect` on the fields you change). Check it with `python3 -I scripts/claim_patch.py <file> --dry-run`. Do not apply it.
2. `data/verification/cardcheck-2026-10-17c/adjudication.json`: per card, the changes made and the items for the senior author; per claim, your decision on each question with its reason, and anything left for the senior author.

## Rules
The hard rules of `docs/VERIFICATION-BRIEF.md` apply (your own browser tab only, no downloads, quotations at most 15 words and at most one per claim, person-first language, no dosing or administration guidance). Do not edit `data/study-cards/methamphetamine.json` or `data/claims/methamphetamine.json` directly.

Final report, under 300 words: per card, changes made and whether it is ai-checked; per claim, the decisions; what is left for the senior author.
