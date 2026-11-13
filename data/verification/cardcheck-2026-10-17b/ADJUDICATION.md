# Batch 3 adjudication (2026-10-17): cards and claims

You are the independent adjudicator (AI reader 18) for Pharmakon's methamphetamine page. You did not write or check any of the work below. The source decides; no reader's version is presumed right.

Project: `/home/claude/drug-encyclopedia`. Read `docs/ADJUDICATION-BRIEF.md` (Part B and the rules), `docs/METHODS.md` §5, §6, §9 and §12 as needed, and `data/verification/cardcheck-2026-10-17b/BRIEF.md` (what the second readers were asked).

## What there is
- Ten first-pass cards in `data/study-cards/methamphetamine.json`: sc_srisurapanont_2021, sc_voce_2019, sc_cohenlaroque_2024, sc_boden_2023, sc_sibanda_2019, sc_marel_2019, sc_foulds_2020, sc_zhu_2025, sc_mcketin_2026, sc_bakouni_2023.
- First readers' reports: `data/verification/batch3-2026-10-17/reader12_report.md`, `reader13_report.md`, `reader14_report.md`.
- Second readers' card checks: `data/verification/cardcheck-2026-10-17b/out/<reference>.json`; their views on the claims: `claims_reader15.json`, `claims_reader16.json`, `claims_reader17.json`.
- Second readers' anchor checks: `data/verification/targeted-2026-10-17f/out_reader15.json`, `out_reader16.json`, `out_reader17.json`. The editor applies these anchor results separately; you need them only where they bear on a claim's wording.
- The claims as they now stand: `data/claims/methamphetamine.json` (cl_meth_psychosis_treatment, cl_meth_psychosis_course, cl_meth_psychosis_vs_schizophrenia, cl_meth_psychosis_association, cl_meth_acute_toxicity, cl_meth_dependence_baserate, cl_meth_violence, cl_meth_us_trends, cl_meth_mirtazapine, cl_meth_bupropion_modafinil).
- The PDFs: `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Methamphetamine/` (file names in BRIEF.md). Page-number notes for the online-first PDFs are in BRIEF.md.

## Part B: the cards
Exactly as `docs/ADJUDICATION-BRIEF.md` Part B says: check every item a second reader flagged, in the source; fix what is plainly factual; log every change in `verification.disagreements`; leave judgment differences for the senior author. Write each whole corrected card to `data/study-cards/_incoming/methamphetamine/<card_id>.json` and run `python3 -I scripts/check_card.py <file>` until it passes. Set `verification.status` to `ai-checked` only if the readers agree on the overall risk-of-bias judgment; set `checked_by` to "AI reader 15/16/17 (card check) and AI reader 18 (adjudication)" as fits, `checked_on` today.

**AMSTAR 2 item 4.** Readers applied item 4 two ways when a language limit is not justified. AMSTAR 2 gives "Partial Yes" only if, among other things, publication restrictions such as language are justified. Apply the instrument as written on every card in this batch, then recompute the overall confidence from the critical domains, and list any earlier card in `data/study-cards/methamphetamine.json` that applied item 4 the other way, so the editor can correct it.

## Part C: the claims
For each of the ten claims, weigh the first reader's change, the second reader's view and the source, and decide:
1. **Wording.** Statement, plain text and magnitude say exactly what the sources show, no more. Fix factual errors the second readers found (for example: McKetin 2026's 2.2-day difference is a difference in the drop from baseline, not in end-of-treatment use; Boden 2023's symptoms and use were not reported for the same period at ages 18–25; check each in the source).
2. **Status label** (METHODS §6.4): replicated, replicated by the same team, single study, contested or mixed. Give the reason in one or two sentences.
3. **GRADE**: domains and certainty, with reasons; change only with a reason grounded in METHODS §6.
4. **Verification step**: draft or metadata-verified (a claim that rests only on narrative reviews stays draft).

Questions raised by the readers that you must settle (or leave for the senior author with your recommendation):
- cl_meth_mirtazapine: replicated (Coffin 2020 and McKetin 2026 share no authors) or replicated by the same team; the plain text's "2 fewer days".
- cl_meth_psychosis_treatment: replicated (reader 12) or single study (reader 15: the trials test different drug pairs and their directions are not reported).
- cl_meth_psychosis_vs_schizophrenia: one claim or two (negative symptoms replicated, positive symptoms mixed). Prefer keeping one claim with wording and status that fit the evidence unless splitting is clearly needed; say why.
- cl_meth_acute_toxicity and cl_meth_dependence_baserate: "mixed" or another label.
- Cohen-Laroque 2024's positive-symptom pooled result, which two readers could not reproduce from its Table 1: how the claim should describe it.

Write:
1. `data/verification/cardcheck-2026-10-17b/claims_patch.json`: a patch for `scripts/claim_patch.py` (format in its docstring: `set`, `replace`, `bump`, `change`; use `expect` on the fields you change). Check it with `python3 -I scripts/claim_patch.py <file> --dry-run`. Do not apply it.
2. `data/verification/cardcheck-2026-10-17b/adjudication.json`: per card, the changes made and the items for the senior author; per claim, your decision on each question with its reason, and anything left for the senior author.

## Rules
The hard rules of `docs/VERIFICATION-BRIEF.md` apply (no browser, no downloads, quotations at most 15 words and at most one per claim, person-first language, no dosing or administration guidance). Do not edit `data/study-cards/methamphetamine.json` or `data/claims/methamphetamine.json` directly.

Final report, under 300 words: per card, changes made and whether it is ai-checked; per claim, the decisions; the AMSTAR 2 item 4 list; what is left for the senior author.
