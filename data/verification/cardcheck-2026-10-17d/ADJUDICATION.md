# MDMA batch 1 adjudication (2026-10-17): cards and claims

You are the independent adjudicator (AI reader 36) for Pharmakon's MDMA page. You did not write or check any of the work below. The source decides; no reader's version is presumed right.

Project: `/home/claude/drug-encyclopedia`. Read `docs/ADJUDICATION-BRIEF.md` (Part B and the rules), `docs/METHODS.md` §5, §6, §7, §9 and §12 as needed, and `data/verification/cardcheck-2026-10-17d/BRIEF.md` (what the second readers were asked, the page conventions of each PDF, and reader 24's final notes).

## What there is
- Eleven first-pass cards, now in `data/study-cards/mdma.json`: sc_mccann_1994, sc_schilt_2007, sc_halpern_2011, sc_ung_2026, sc_murphy_2009 (first reader AI reader 24) and sc_parrott_2013, sc_parrott_2011, sc_lyvers_2011, sc_cowan_2012, sc_mithoefer_2003, sc_barnett_2021 (first reader AI reader 25).
- Nine claims, now in `data/claims/mdma.json` (joined by the editor from reader 25's claims and reader 24's cards; anchors from reader 24's cards were placed by the editor). They are not shown on the site until their anchors are second-read and this adjudication is applied.
- Reader 25's report: `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/mdma1/reader25_report.md`.
- The second readers' anchor checks: `data/verification/targeted-2026-10-17h/out_reader31.json` (50 confirmed) and `out_reader32.json` (35 confirmed, 3 corrected); their card checks, `data/verification/cardcheck-2026-10-17d/out/<reference>.json`; their views on the claims, `claims_reader31.json` and `claims_reader32.json`.
- Sources: PDFs in `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/MDMA/`; Halpern 2011 (PMC3053129), Lyvers 2011 (publisher HTML) and Cowan 2012 (PMC3280662) on the web: read them in the desktop app's browser in a tab you open yourself (`mcp__remote-devices__Claude_Browser__*`; ToolSearch "mcp__remote-devices__Claude_Browser__", max_results 64), never touching any other tab, and close it when you finish.

## Part A: the anchors
The editor has applied the second readers' anchor checks (`scripts/apply_targeted.py`; patches in `data/verification/targeted-2026-10-17h/patch_reader31.json` and `patch_reader32.json`): every anchor is now ai-checked, and three carry the second reader's correction (n = 54, 67 and 80 in `tasks.json`: `cl_mdma_sert_binding` anchor 0, `cl_mdma_retraction_2002` anchor 6, `cl_mdma_neurotoxicity_contested` anchor 7). Check those three at the source. If you disagree with a correction, put your version in the claims patch (`evidence_set`, with `expect`). Claims are now at the versions the patches produced; read them as they stand in `data/claims/mdma.json`.

## Part B: the cards
Exactly as `docs/ADJUDICATION-BRIEF.md` Part B says: check every item a second reader flagged (including the "missed" items: Parrott 2013's uncited "Wagner et al. (2013)" and its uncarded tolerance section §5.2; Mithoefer's omitted route exchange and unsourced emergency figures; Lyvers's fenfluramine case resting on a legal textbook; Cowan's uncited primate sentence), in the source; fix what is plainly factual; log every change in `verification.disagreements`; leave judgment differences for the senior author. Write each whole corrected card to `data/study-cards/_incoming/mdma/<card_id>.json` and run `python3 -I scripts/check_card.py <file>` until it passes. Set `verification.status` to "ai-checked" where the readers agree on the overall risk-of-bias judgment (they did on all eleven); `checked_by` "AI reader 31 (card check) and AI reader 36 (adjudication)" or "AI reader 32 …", `checked_on` today. Cards with no change still get the ai-checked status (write them too).

## Part C: the claims
For each of the nine claims, weigh the editor's text, both second readers' views and the source, and decide wording, status label, relation, GRADE and verification step, with reasons. Questions you must settle (or leave for the senior author with your recommendation):
- `cl_mdma_memory` and `cl_mdma_abstinence`: reader 31 asks for an indirectness downgrade because they rest on reviews (as `cl_mdma_sert_binding` has); apply METHODS §6.3 as written. Reader 32: "more consistent" in the memory statement is the opposite of what both reviews say.
- `cl_mdma_minimal_polydrug`: the relation "does-not-detectably-change" and METHODS §6.3's precision requirement; "4 of 15 tests" against the roughly 40 measures; Table 4: a medium effect excluded on 6 of 14 measures (reader 31) or 5 strictly, the sixth at exactly 0.50 (reader 32). Say exactly what the table shows.
- `cl_mdma_prospective`: the "second cohort" described by the review is partly the same cohort (reader 32); Schilt's baseline is one multivariate test (reader 31).
- `cl_mdma_sert_binding`: possible recovery with abstinence (reader 31), and other imaging measures that did differ (reader 32).
- The two debate boxes (`cl_mdma_dopamine_human`, `cl_mdma_neurotoxicity_contested`): Halpern's strategy-application finding belongs on the yes side; Lyvers's "one of 15 tests" understates Halpern's Table 3; "well attested" transporter binding is second-hand; and two in-text citations in the dopamine box do not resolve on the site ("(Ricaurte and colleagues, reply to Mithoefer et al., 2003)" and "(Barnett and Doblin, 2021)"): write citations as "(Author & Author, Year)" or "(Author et al., Year)", naming the reply's authors in the sentence instead.
Every claim says no more than its anchors show. Claims resting only on narrative reviews or commentaries stay draft.

Write:
1. `data/verification/cardcheck-2026-10-17d/claims_patch.json`: a patch for `scripts/claim_patch.py` (format in its docstring; `expect` on the fields you change). Check it with `python3 -I scripts/claim_patch.py <file> --dry-run`. Do not apply it.
2. `data/verification/cardcheck-2026-10-17d/adjudication.json`: per anchor decided, per card and per claim, your decisions with reasons, and what is left for the senior author.
3. For every claim, suggested simple lines (short, but, and two to four how points; following `docs/WRITING-RULES.md`: everyday words, never more than the claim, the But carries its main limit) in `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/mdma1/reader36_simple.json`. Reader 25's suggestions are in `scratchpad/mdma1/reader25_simple.json`.

## Rules
The hard rules of `docs/VERIFICATION-BRIEF.md` apply (quotations at most 15 words and at most one per claim, person-first language, no dosing or administration guidance; no downloads, no PDF links in the browser, no CAPTCHAs). Do not edit `data/study-cards/mdma.json` or `data/claims/mdma.json` directly. If an automatic safety filter stops one of your responses, do not retry or reword that content: save what is done and say what was not done. Write files as you go.

Final report, under 300 words: anchors decided; per card, changes made; per claim, the decisions; what is left for the senior author.
