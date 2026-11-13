# MDMA batch 2 adjudication (2026-10-17): the MDMA-assisted therapy trials, cards and claims

You are the independent adjudicator (AI reader 38) for Pharmakon's MDMA page (batch 2). You did not write or check any of the work below. The source decides; no reader's version is presumed right.

Project: `/home/claude/drug-encyclopedia`. Read `docs/ADJUDICATION-BRIEF.md` (Part B and the rules), `docs/METHODS.md` §5, §6, §7, §9 and §12 as needed, and `data/verification/cardcheck-2026-10-17f/BRIEF.md` (what the second readers were asked).

## What there is
- Thirteen first-pass cards, now in `data/study-cards/mdma.json`: sc_mitchell_2021 (MAPP1), sc_mitchell_2023 (MAPP2), sc_brett_2025, sc_halvorsen_2021, sc_mitchell_2021b (the reply) (first reader AI reader 27) and sc_nutt_2021, sc_madero_2023, sc_earleywine_2025, sc_marseille_2025, sc_mahase_2024, sc_feduccia_2024, sc_jerome_2024, sc_mithoefer_2024 (the three retraction notices) (first reader AI reader 28). Reports: `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/mdma2/reader27_report.md`, `reader28_report.md`.
- Six claims in `data/claims/mdma.json` (cl_mdma_ptsd_efficacy, cl_mdma_ptsd_blinding, cl_mdma_ptsd_adverse_events, cl_mdma_regulatory_2024, cl_mdma_ptsd_cost, cl_mdma_therapy_contested), joined by the editor from both readers (the editor's joined version: `data/verification/cardcheck-2026-10-17f/claims_joined_by_editor.json`).
- The second readers' (AI readers 34 and 35) anchor checks `data/verification/targeted-2026-10-17j/out_reader34.json` (51 confirmed, 3 corrected: n16, n46, n84) and `out_reader35.json` (40 confirmed, 8 corrected); card checks `data/verification/cardcheck-2026-10-17f/out/<reference>.json`; claim views `claims_reader34.json`, `claims_reader35.json`.
- Sources: PDFs in `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/MDMA/`; the two trials (nature.com), their ClinicalTrials.gov records, MAPP2's correction and the three retraction notices (link.springer.com) on the web: read them in the desktop app's browser in a tab you open yourself (`mcp__remote-devices__Claude_Browser__*`; ToolSearch "mcp__remote-devices__Claude_Browser__", max_results 64), never touching any other tab, and close it when you finish. Never open a PDF link in the browser.

## Part A: the anchors
The editor has applied the second readers' anchor checks (patches `data/verification/targeted-2026-10-17j/patch_reader34.json`, `patch_reader35.json`): every anchor is ai-checked, and the corrected texts are in place. Check each of the 11 corrections at the source. The four role corrections (n87 to n90: `cl_mdma_therapy_contested` anchors 13 to 16, supports → qualifies) were NOT applied by the script: decide them. Put any change in the claims patch (`evidence_set`, with `expect`).

## Part B: the cards
As `docs/ADJUDICATION-BRIEF.md` Part B says: check every item a second reader corrected or found missing, in the source; fix what is plainly factual; log every change in `verification.disagreements`; leave judgment differences for the senior author (for example Nutt 2021's domain on reliance on the authors' own studies, low or high; MAPP1's selection of the reported result for the SDS). Write each whole card to `data/study-cards/_incoming/mdma/<card_id>.json` (all thirteen, corrected or not) and run `python3 -I scripts/check_card.py <file>` until it passes; `verification.status` "ai-checked" where the readers agree on the overall risk-of-bias judgment (they did on all thirteen); `checked_by` "AI reader 34 (card check) and AI reader 38 (adjudication)" or "AI reader 35 …", `checked_on` today.

## Part C: the claims
For each of the six claims decide wording, relation, status label, GRADE and verification step, with reasons. Questions to settle (or leave for the senior author with your recommendation):
- `cl_mdma_ptsd_efficacy`: both second readers would rate risk of bias down two levels (functional unblinding shared by both trials with a participant-reported outcome, unmeasured expectancy, one sponsor), giving low; "most could tell their group" holds only for MAPP2 (MAPP1 did not assess blinding); keep "reduces" (project precedent) with wording "lowered … scores"?
- `cl_mdma_ptsd_adverse_events`: moderate for the rise in common events; MAPP1 says expected effects were "not solicited", not "not recorded"; MAPP2's list omits three rows.
- `cl_mdma_regulatory_2024`: both readers say metadata-verified fits only the retraction part: split into two claims (the regulator's decision as reported, draft; the three retractions, from the notices) or keep one claim at draft. Fix the wording the readers found beyond the sources ("press reports"; "citing news reports" where one source is a JAMA piece; "doubted that the treatment worked" in the plain text). If you split, write the new claim whole in `data/verification/cardcheck-2026-10-17f/new_claims.json` (schema-valid; anchors moved from the old claim keep their checked status).
- `cl_mdma_ptsd_cost`: reader 35's five wording fixes and reader 34's note on the critique's second author (same name and affiliation as both trials' first author).
- `cl_mdma_therapy_contested`: the debate box (a source for the August month; the long-term follow-up on the yes side; Brett's search terms included MAPS, so "no trial without MAPS links" needs that caveat; anything unsupported in the editors' reading).
- In-text citations in debate boxes must match the site's APA labels, or they do not resolve: MAPP1 is "(Mitchell, Bogenschutz, et al., 2021)", the reply "(Mitchell, Coker, et al., 2021)", MAPP2 "(Mitchell et al., 2023)", Halvorsen "(Halvorsen et al., 2021)"; two authors are joined with "&". Check with `node scripts/check_citations.js` after a dry run if useful.
Every claim says no more than its anchors show. Claims resting only on commentaries, news or narrative reviews stay draft.

Write:
1. `data/verification/cardcheck-2026-10-17f/claims_patch.json` for `scripts/claim_patch.py` (`expect` on the fields you change); check it with `--dry-run`. Do not apply it.
2. `data/verification/cardcheck-2026-10-17f/adjudication.json`: per anchor decided, per card and per claim, your decisions with reasons, and what is left for the senior author.
3. Suggested simple lines for every claim (short, but, two to four how points; `docs/WRITING-RULES.md`: everyday words, never more than the claim, the But carries its main limit, "dummy pill" not "placebo"), in `data/verification/cardcheck-2026-10-17f/simple_reader38.json`. The first readers' suggestions are in `scratchpad/mdma2/reader27_simple.json` and `reader28_simple.json`.

## Rules
The hard rules of `docs/VERIFICATION-BRIEF.md` apply (quotations at most 15 words and at most one per claim, person-first language, no dosing or administration guidance: the trials' doses only as study conditions, on the cards). No downloads, no PDF links in the browser, no CAPTCHAs. Do not edit `data/study-cards/mdma.json` or `data/claims/mdma.json` directly. If an automatic safety filter stops one of your responses, do not retry or reword that content: save what is done and say what was not done. Write files as you go.

Final report, under 300 words: anchors decided; per card, changes made; per claim, the decisions; what is left for the senior author.
