# Di Forti et al. (2015): adjudication from the PDF (AI reader 317), 1 November 2026

You are an independent adjudicator for Pharmakon. You did not write these claims or the card and took no part in the
second reading. The cannabis round's adjudicators (241 to 244) closed everything except what turns on Di Forti et al.
(2015), whose full text could not be read in October; reader 242 marked those points `deferred`. The senior author has
now saved the PDF, and AI reader 292 has read it blind and checked every anchor from it (all seven are now ai-checked).
You settle the rest, from the PDF.

Read `data/verification/can-a-2026-10-27/adjudication/BRIEF.md` and everything it tells you to read first: all of it
applies to you, with these changes.

- **Your scope.** Claims `cl_can_psychosis_frequency` and `cl_can_psychosis_potency` (staged in
  `data/claims/_incoming/can_joined.json`; print them by id), only where they rest on Di Forti et al. (2015); card
  `sc_di_forti_2015` (`data/study-cards/_incoming/cannabis/`). Your folder: `scratchpad/can-a/a317/`.
- **The source.** `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Cannabis/DiForti_2015_HighPotencyCaseControl.pdf`
  (version of record, pp. 233–238). Extract the text yourself and check every number on the rendered page
  (`pdftoppm -r 150`; figures and Tables 3–4 at `-r 300`). The online appendix is not available.
- **What to settle.**
  1. Reader 292's verdict `partly-supported` on `cl_can_psychosis_potency` and every point in their output
     (`data/verification/can-a-2026-10-27/out/di-forti_2015.json`, `claims` and `card_check`): the adjustment set given
     for the figures that come only from Figure 2; the 24% attributable fraction that cannot be reproduced from its
     printed inputs; the intervals that do not fit their estimates or p values (decide how the claim reports them: as
     printed, with the inconsistency named; never replaced by our recomputed values as if printed); the p values printed
     differently in the text and the Summary.
  2. Reader 292's targeted-check notes (`data/verification/can-a-2026-10-27/targeted4/out_reader292.json`).
  3. The four items reader 242 deferred (in `adjudication/242_log.json`, verdict `deferred`): anchor 11 and the south
     London figures; anchors 0 to 5 and the 2015 sentence; 370 controls here against Murray et al.'s 390; whether
     "mainly" stays for the 2015 study.
  4. The card: reader 292's correction of key finding 10 (a review cited as primary), each `missed` item that is true
     and matters, and the page numbers (the card cites the publisher's web page; give printed pages now, and set
     `source_read` to say the PDF was read for the second reading and the adjudication).
- **Plain lines.** Write `317_simple.json` for both claims as they should read after your patch, starting from the
  current lines in `data/site/simple.json` (`claims` → each id) and the earlier adjudicator's `242_simple.json`; change
  only what the source or your patch requires.
- **Outputs** in `data/verification/can-a-2026-10-27/adjudication/`: `317_log.json`, `317_patch.json` (claim_patch.py
  format; dry-run until it passes), `317_simple.json`, and the corrected card written in full. Every new or reworded
  anchor enters as ai-located; list them in your log under `for_round2` (claim id, anchor index, why) so a fresh reader
  can check them.
- Final message under 200 words: what you changed in each claim and the card, any number that changed, and anything
  for the senior author.
