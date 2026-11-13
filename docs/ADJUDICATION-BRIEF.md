# Adjudication brief — closing the second reading

First written for round 1b; used again in round 2b. Paths name round 1; use `data/verification/<round>/…` for the round
named in your task.

The blind second reading (round 1, `docs/VERIFICATION-BRIEF.md`) produced two things this round closes:

1. **Anchors reader 2 did not re-find blind.** They are listed per source in
   `data/verification/round1/unmatched_anchors.json` (claim id, anchor index, page, locator, extracted text, role). Most are
   secondary or "editors' appraisal" anchors that a blind reader would not extract; some may be wrong.
2. **Reader 2's checks of the study cards**, in the `card_check` section of `data/verification/round1/out/<reference>.json`:
   key findings and reporting issues marked `corrected`, `wrong-location` or `not-found`, risk-of-bias and
   interpretation-gap opinions, and important items the card `missed`.

You are an independent checker. Neither reader's version is presumed right: the source decides.

## Part A — anchors (output only; you never edit claims)

For each unmatched anchor of your sources, open the source at the stated place and give a verdict:
`confirmed` (data and location right), `corrected` (give the right page, locator and/or data, in your own words),
`wrong-location` (data right, place wrong: give the place), or `not-found` (the source does not contain it; say what it
does contain). For "editors' appraisal" anchors, check the factual basis of the appraisal (e.g. that the degrees of
freedom printed are what the anchor says).

Write `data/verification/round1b/out/<reference>.json`:

```json
{"reference": "dean_2013", "checker": "AI reader 2 (adjudication)", "checked_on": "2026-10-16",
 "anchors": [{"claim_id": "…", "anchor_index": 3, "verdict": "confirmed", "page": "p. 263", "locator": "…",
              "extracted": "only if corrected", "note": ""}],
 "card": {"file": "data/study-cards/_incoming/methamphetamine/sc_dean_2013.json", "changes": 4, "for_senior_author": ["…"]}}
```

## Part B — the study card (you write a corrected copy)

Start from the card's current version in `data/study-cards/methamphetamine.json` (id `sc_<reference>`, hyphens → underscores).
For each item reader 2 flagged, check it in the source, then:

- `wrong-location` confirmed → fix `page`/`locator`.
- `corrected` confirmed → fix the finding or issue text (your own words; keep numbers exact).
- `missed` items that are true and matter → add them as key findings (with page and locator) or reporting issues
  (with page and consequence).
- Arithmetic or terminology errors that are plainly factual (e.g. a ROBINS-I word such as "serious" in a ROBINS-E rating,
  which should be "high") → fix.
- Risk-of-bias and interpretation-gap disagreements that are matters of judgment → do not change; list them under
  `for_senior_author` in your Part A output.

Log every change in the card's `verification.disagreements` array as
`{"field": "key_findings[3].locator", "first_pass": "<old>", "reviewer": "<reader 2's version>", "resolution": "<what you
did and why, after checking the source>"}`. Then, if the readers agree on the overall risk-of-bias judgment (METHODS §5.5; differences on single domains or the interpretation-gap rating are listed for the senior author), set `verification.status` to `ai-checked`; if an overall disagreement remains, leave `first-pass` and list it. In
both cases set `verification.checked_by` to `"AI reader 2 (blind reading and adjudication)"` and
`verification.checked_on` to today. Write the whole corrected card to
`data/study-cards/_incoming/methamphetamine/<card_id>.json` and run `python3 -I scripts/check_card.py <file>` from the
project root until it passes. Never edit `data/study-cards/methamphetamine.json` or any claim file directly.

## Where to read and the rules

Exactly as in `docs/VERIFICATION-BRIEF.md` ("Where to read" and "Rules (hard)"): PDFs from
`/mnt/user-data/uploads/DrugEncyclopedia/<pdf_path>` (use the reference's `verification.pdf_path` in
`data/references/methamphetamine.json`), web full texts in one browser tab you create yourself, never any other tab, no
downloads, no PDF links in the browser, no CAPTCHAs, no copied passages, no dosing or administration guidance.

Final report: per source, anchors not confirmed (with the correction), card changes made, items left for the senior author.
