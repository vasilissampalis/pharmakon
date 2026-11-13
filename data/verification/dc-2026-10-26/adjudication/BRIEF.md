# Drug checking: review and adjudication (AI readers 148 and 149), 27 October 2026

You are an independent methodologist and adjudicator for Pharmakon, an evidence library about drugs for the public and
for people who use drugs. You did not write these claims or cards and you did not take part in the second reading.
Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own
folder is `scratchpad/ux1026/dc/a<N>/`.

The senior author asked: are home drug-test kits useful, do they detect what is in a drug, and does testing change what
people do or prevent overdoses? First readers wrote 21 study cards and 19 claims; six blind second readers re-read every
source, gave a verdict on each claim, and checked each card; their unmatched anchors were then checked at the stated
place. You close the round: **the source decides**, not the first reader and not the second reader.

## Read first

1. `docs/METHODS.md` version 0.3.1: §4.5, §5.3–5.6, §6 (all of it, including the **Test accuracy** rule at the end of
   §6.3), §7, §8 (section 11), §9, §12.
2. `docs/WRITING-RULES.md`: Rule 0, Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/REVIEW-BRIEF-2.md`, "What to check, claim by claim" (A to F): your review standard.
4. `docs/ADJUDICATION-BRIEF.md` Part B (how to correct a card and log it) and `docs/ADJUDICATION-BRIEF-R2.md`
   "What to do with each finding" (verdicts, patches, GRADE rules).
5. `scripts/claim_patch.py` (its docstring): your patch format.

## Your group

| Reader | Claims (in `data/claims/drug-checking.json`) | Cards you adjudicate (in `data/study-cards/drug-checking.json`) |
|---|---|---|
| 148 | the ten "What the tests find" claims: `cl_dc_fts_detects_fentanyl`, `cl_dc_fts_false_positives`, `cl_dc_fts_analogues`, `cl_dc_fts_brands_lots`, `cl_dc_nitazene_strips`, `cl_dc_xylazine_strips`, `cl_dc_benzo_strips`, `cl_dc_colour_mdma`, `cl_dc_home_vs_service`, `cl_dc_home_what_tests_miss` | `sc_green_2020`, `sc_bergh_2021`, `sc_halifax_2024`, `sc_lockwood_2021`, `sc_de_vrieze_2024`, `sc_sisco_2024a`, `sc_sisco_2024b`, `sc_laing_2021`, `sc_murray_2003`, `sc_winstock_2001`, `sc_philp_2018`, `sc_mcgowan_2018` |
| 149 | the nine "What testing changes" claims: `cl_dc_after_positive`, `cl_dc_disposal_unexpected`, `cl_dc_overdose_strip_users`, `cl_dc_law_deaths`, `cl_dc_uptake_offered`, `cl_dc_continued_use`, `cl_dc_uptake_who_tests`, `cl_dc_festival_hospital`, `cl_dc_caution_harms` | `sc_maghsoudi_2022`, `sc_kutscher_2024`, `sc_krieger_2018`, `sc_karamouzian_2018`, `sc_vickers_smith_2025`, `sc_erickson_2026`, `sc_klaire_2022`, `sc_measham_2019`, `sc_bhai_2025` |

Some sources serve both groups (Kutscher, Klaire, McGowan, Winstock): a fact both groups state must have the same number
in both. You may read the other group's claims to keep them consistent; patch only your own.

## What you work from

- The second readers' outputs, one per source: `data/verification/dc-2026-10-26/out/<reference>.json` (`claims`:
  verdict, overstatement and notes, their own anchors; `card_check`: each key finding and reporting issue, risk of bias,
  interpretation gap, `missed`). The reconciliation report: `data/verification/dc-2026-10-26/report.md`.
- The targeted checks: `data/verification/dc-2026-10-26/targeted/out_reader*.json` (results for the anchors the blind
  reading did not match; already applied to the claims where confirmed or corrected; a `not-found` stays open for you).
- The plain lines the first readers wrote: `scratchpad/ux1026/dc/reader139_simple.json` (group 148) and
  `reader140_simple.json` and `reader141_simple.json` (group 149).
- **The sources.** PDFs: `/mnt/user-data/uploads/DrugEncyclopedia/` + the reference's `verification.pdf_path`
  (`data/references/drug-checking.json`); a text extraction of each, pages separated by form feeds, is in
  `scratchpad/ux1026/dc/numtext/` (printed page = the article's first page + index; author manuscripts use "AM p." =
  PDF page). Web papers, saved as text by the second readers: Halifax, Lockwood and De Vrieze in
  `scratchpad/ux1026/dc/s146/`; Vickers-Smith in `scratchpad/ux1026/dc/s147/vickers_smith_2025_page1.txt` and
  `scratchpad/vickers_page.txt`; Karamouzian and Maghsoudi only as second-reader notes in `scratchpad/ux1026/dc/s147/`
  and in their out files. If the app's browser is available you may open a web paper in a tab of your own (its tabId on
  every call; close it at the end); if not, settle web points from the saved texts and the two readers' extractions, and
  mark anything they cannot settle `deferred` with the reason "web source not reachable".

## What to do

1. **Every second-reader verdict other than `supported`, and every overstatement note** on your claims: check it at the
   source and give a verdict (`accept`, `accept-modified`, `reject`, `already-fixed`, `deferred`) with what you found.
2. **Your own review** of each claim (REVIEW-BRIEF-2 A to F): numbers against anchors and sources; the wording against
   the design (laboratory results never presented as real-life accuracy; intended or self-reported behaviour never as
   observed behaviour; association never as effect; one brand, lot, festival or programme never as all); GRADE start,
   domains, arithmetic and reasoning per §6.3 (accuracy claims: the Test accuracy rule and the relation `describes`;
   behaviour and outcome claims: start low); status flags per §6.4, counting overlapping studies once (both reviews
   include Krieger and Karamouzian; Maghsoudi includes Measham; Kutscher's Goldman 2019 row and its reference 70 are
   probably Krieger's pilot); the debate box (§7) where a claim is contested; no advice on how to test or how to use a
   drug, anywhere.
3. **Write the claim patch** (`claim_patch.py` format, one object per claim you change, with a `change` line beginning
   "Review and adjudication, drug checking round:"). Every number you put into a claim must be in an anchor's
   `extracted` text or be an editors' calculation you have recomputed. A needed number that no anchor carries goes in a
   new anchor (`evidence_add`, page and locator per §6.2, role, `located_by`: "AI reader <N> (adjudicator), from the saved
   full text" or "… from the PDF"); it enters as ai-located and a second reader will check it later (say so in the log).
   Check with `python3 -I scripts/claim_patch.py <your patch> --dry-run` until it passes.
4. **Write the plain lines** for every claim of your group as they should read after your patch:
   `{"<claim id>": {"q", "short", "but", "how": [2 to 4], "freq"?}}` (reading age 8 to 11; `short` about 14 words; `but`
   the main limit; name the comparison group; never more than the claim says; numbers as counts out of 100, or 1,000
   for rare things). Start from the first reader's lines and change what the claim or the source requires.
5. **Adjudicate the cards** of your group: every `card_check` item the second reader marked `corrected`,
   `wrong-location` or `not-found`, and each `missed` item that is true and matters (ADJUDICATION-BRIEF Part B). Write
   each changed card in full to `data/study-cards/_incoming/drug-checking/<card id>.json`, log every change in
   `verification.disagreements`, set `verification.checked_by` to "AI reader <second reader> (blind second reading) and
   AI reader <N> (adjudication)" and `checked_on` to today, and set `verification.status` to `ai-checked` when the
   readers agree on the overall risk-of-bias judgment; run `python3 -I scripts/check_card.py <file>` until it passes.
   Domain-level disagreements and interpretation-gap differences go to the senior author, not into the card.
   Specific open points: `sc_sisco_2024b` is still `in-vitro` with no instrument, and reader 142 gave QUADAS-2 judgments
   for it (148: decide whether to re-file it as `test-accuracy` with QUADAS-2, as METHODS §5.6(c) allows, and log it);
   `sc_karamouzian_2018` and `sc_klaire_2022` are filed `cross-sectional` but appraised with ROBINS-I, which the
   validator flags (149: propose the right design or instrument for each and why; change only what is rule-based).
6. **Anything the senior author must decide** goes in your log under `for_senior_author`.

## Output (in `data/verification/dc-2026-10-26/adjudication/`)

- `<N>_log.json`: `{"reader": "AI reader <N> (adjudicator)", "date": "2026-10-27", "items": [{"claim_id" or "card",
  "source": "second reader <M> | targeted | own review", "finding": "...", "verdict": "...", "reason": "what you
  checked and found", "evidence": "page/section or card field", "patch_ref": "index in your patch or null"}],
  "for_senior_author": ["..."], "deferred": ["..."]}`
- `<N>_patch.json`: the claim patch.
- `<N>_simple.json`: the plain lines.
- Corrected cards in `data/study-cards/_incoming/drug-checking/`.

## Rules (hard)

- Never edit `data/claims/`, `data/study-cards/drug-checking.json`, `docs/`, `scripts/` or `site/`: you write proposals
  and corrected copies; the editor applies them.
- No dosing, administration or potentiation guidance; no instructions on how to test; findings only. Person-first words;
  no words of alarm or reassurance. Quotations at most 15 words, at most one per claim, word for word.
- Final message under 250 words: counts by verdict; certainty or status changes (claim, from → to, rule); new anchors;
  cards changed and set to ai-checked; the five most consequential edits; what the senior author must decide.
