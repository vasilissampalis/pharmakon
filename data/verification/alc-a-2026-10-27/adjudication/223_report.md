# Adjudicator 223 (alcohol use disorder, withdrawal, treatment, pregnancy): report

Saved by the editor from the reader's final message, 30 October 2026.

Verdicts, 111 items: accept 72, accept-modified 17, reject 16, deferred 6 (claims 38/16/11/1; cards 34/1/5/5).
Certainty or status changes: none. New anchors: 8, all ai-located (Grant 2017, Mayo-Smith, Jonas (2), McPheeters (2),
Anton, Jones); seven claims back to metadata-verified until they are checked. Cards: all 14 corrected and set to
ai-checked (the second readers agreed on the overall risk of bias).

Five most consequential edits:
1. Naltrexone: the pooled trials lasted 12 to 24 weeks (mostly 12), not 12 to 52; COMBINE supplies 612 of the 1,141
   people in the head-to-head comparison, on the higher dose; harms are pooled over all doses.
2. COMBINE: the headline now covers only adding therapy to medicine; the placebo-pill benefit (79.8 vs 73.8, P = .04)
   and the authors' reading added; "differences shrank" removed.
3. Prevalence: the interviewers were not clinicians; NSDUH now compared with NESARC-III's DSM-IV 12.7 ("a little over
   half"); the authors' reading of a real rise sits beside the editors' caution.
4. Acamprosate: drop-outs from side effects given for both reviews; added that the manufacturer part-funded the Cochrane
   patient database, and the crude 7 in 100 beside the pooled 9.
5. Withdrawal medicines: the adverse-event estimate moved to the comparison with all other medicines (18 trials).

For the senior author: whether low or moderate randomized evidence gets "may" or "probably" verbs; COMBINE's relation;
the status flags; the Rösner 2010b and Anton interpretation-gap ratings; Lange's AMSTAR item 6; whether to cite WHO's US
band; the Popova and Lange regional means.

Outputs in `data/verification/alc-a-2026-10-27/adjudication/`: `223_log.json` (111 items, 9 points for the senior
author, 5 deferred), `223_patch.json` (10 claim patches; `cl_alc_pregnancy_drinking` unchanged), `223_simple.json`
(plain lines for all 11 claims). Builder scripts in `scratchpad/alc-a/a223/scripts/`. Checks: claim_patch dry run
passes; on a scratch copy validate.py gives 0 hard failures (only new warnings: the 8 unverified anchors);
check_anchor_numbers finds every number in the new PDF anchors except "30" (Jones Table I has no text layer; read on the
rendered page, and the anchor says so); check_card: 14 cards, 0 failing. Methods: Jonas Figures 2–3, Jones Table I and
Carvalho Figure 1 read on rendered pages (the USA band matched by pixel colour); Mayo-Smith's pooling recomputed
(DerSimonian–Laird): Table 2 matches only without a continuity correction, and Table 4 does not match at all, both now
reporting issues on the card; COMBINE gaps recomputed from Tables 3 and 7. Rejected: the "such as Alcoholics Anonymous"
gloss; "may reduce" (listed for the senior author); qualifiers already in the claims. Deferred (web source not
reachable, or supplements not on file): Popova's study counts by region and the PROSPERO dates; whether the regional FAS
and FASD means include country values from the meta-analyses; which Golbert 1967 arm is in Amato's Analysis 2.2.2.
