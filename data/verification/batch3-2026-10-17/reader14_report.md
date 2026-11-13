# AI reader 14 (first reader): methamphetamine currency update, 2026-10-17

Papers read: McKetin 2026 and Bakouni 2023, both in full from their PDFs. **Dean 2018: not readable.** The app's built-in browser could not be reached ("device not connected to the bridge" on four tries spread across the session), so the paper goes back to the senior editor's list. No other route was used (no WebFetch, no other browser).

Files:
- Cards, first-pass, both pass `check_card.py`:
  - `data/study-cards/_incoming/methamphetamine/sc_mcketin_2026.json`
  - `data/study-cards/_incoming/methamphetamine/sc_bakouni_2023.json`
- Patch, checked with `--dry-run` and **not applied**: `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/batch3/reader14_patch.json`
- Builder script for the patch: `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/batch3/r14build/build_patch.py`

Checks run:
- The patch was applied to a scratch copy of the project, with the two cards merged into that copy. `validate.py` then gave 0 hard failures. Without the merged cards, the only failures are the "unknown study card" ones expected before merging.
- The anchor-number check (METHODS §5.5) found 121 of 121 numbers in the 15 new PDF anchors on the stated pages.
- The same test on the cards' key findings and reporting issues came back clean.

## Papers

**McKetin et al. (2026), JAMA Psychiatry 83:581–589.**
- **Design.** Phase 3, double-blind trial at six Australian public clinics. 344 randomized, 339 analysed (5 placebo-arm people never treated). 37% women, 49% with PHQ-9 ≥10. Mirtazapine for 12 weeks as the trial condition, with no trial counselling described.
- **Primary result.** Self-reported use days at week 12 fell by 2.2 days of 28 more than on placebo (95% CI 0.2 to 4.2; IRR 0.89, 0.80–0.98). Weeks 4 and 8 were not significant. Both arms still used on about 16–17 of 28 days (editors' calculation).
- **What the abstract does not say.** The only drug-test outcome did not differ: negative oral-fluid samples 13.2% vs 12.0% (difference 1.3, −4.7 to 7.2). No secondary outcome differed.
- **Harms and stopping.** Drowsiness 47% vs 33%, weight gain 10% vs 3%. 23% vs 15% stopped the medication for reasons related to it, mostly because they disliked its effects, not adverse events as the abstract says. No post-treatment follow-up.
- **Risk of bias.** RoB 2 some concerns: the primary outcome is self-reported, side effects could have revealed allocation, there is no blinding check, and concealment is not described in the article. Interpretation gap substantial: the Key Points say "safe and effective", and the null objective measure is never discussed.
- **Independence.** Steven Shoptaw, second author here, is an author of Colfax 2011. No other author overlaps with the San Francisco trials.

**Bakouni et al. (2023), Drug Alcohol Depend 253:111018.**
- **Scope.** Meta-analysis of 8 bupropion trials.
- **Headline result.** RR 0.90 (0.84–0.96) for the share of amphetamine-positive urine samples, I² 89%, very low certainty by its own GRADE.
- **Unit-of-analysis error.** The full text shows that the 15,664 urine samples (and 119,680 pills for adherence) are pooled as independent observations, so every urine interval is too narrow.
- **Double counting.** The two stages of Trivedi 2021 are entered as separate studies, so its 225 re-randomized people are counted twice: 1239 participants as counted, about 1014 distinct.
- **Bupropion alone.** Five trials, 357 participants: 0.90 (0.81–1.00). The largest bupropion-alone trial (Anderson 2015) contributed no urine data.
- **Other outcomes.** Retention RR 0.97 (0.89–1.05). Adherence was lower on bupropion.
- **Subgroups.** The "longer treatment" and "larger in males" findings are study-level and confounded, the second resting on one trial.
- **AMSTAR 2.** Low confidence, provisional, because item 7 sits in an unread appendix. Item 11 (statistical methods) fails.

**Dean et al. (2018), Neuropsychopharmacology.** Not readable this session (browser offline). No card was written.

## Claims

**cl_meth_mirtazapine (0.2.5 → 0.3.0): change proposed.**
- **Wording.** The statement is rewritten to cover three trials. The San Francisco text is kept, and the Australian trial is added with use days, the oral-fluid null result, harms, stopping and the lack of follow-up. Population, exposure, comparator, outcome and magnitude are broadened to match. The plain text is rewritten in short sentences.
- **Anchors.** Nine new anchors.
- **Status.** replicated-same-team → **replicated**. A different team, sponsor, country, population and analysis model agrees in direction on its primary outcome. *Flag for the senior author:* one shared author (Shoptaw, also on Colfax 2011). A strict reading of §6.4 ("share investigators") would keep replicated-same-team.
- **GRADE stays low, for different reasons.**
  - Indirectness 1 → 0: women, people with depression and public clinics are now included.
  - Inconsistency 0 → 1: the San Francisco trials found lower modelled urine positivity, the Australian trial found no oral-fluid difference, and its effect is smaller.
  - Risk of bias stays at 1, now also covering the self-reported outcome. This is counted once, not twice.
  - Imprecision was considered and not rated down. A reasonable alternative is imprecision 1 instead of inconsistency 1 (the Australian interval reaches a trivial 0.2 days); the certainty is the same either way.

**cl_meth_bupropion_modafinil (0.2.4 → 0.3.0): qualifying evidence added, no rating change.**
- **Why no rating change.** Bakouni's outcome (share of positive samples) is not the claim's abstinence outcome. The claim stays insufficient-evidence, very low, status unchanged.
- **Wording.** The statement and plain text gain the RR 0.90 and the bupropion-alone 0.90 (0.81–1.00), with the unit-of-analysis problem stated, the combination-trial share, the missing Anderson urine data and the null retention result. The GRADE reasoning explains why the rating is unchanged.
- **Anchors.** Six new anchors.
- **Currency report.** The currency report's view that the bupropion conclusion "would need rewriting" is not supported once the full text is read.

**cl_meth_cognition_normal_range: no change.** Dean 2018 could not be read. The claim's caveat that no study measured a decline from a higher starting point stays until a reader can open the paper.

**Other claims.**
- **cl_meth_naltrexone_bupropion.** Bakouni's naltrexone-plus-bupropion subgroup (0.92, 0.89–0.94) is just Trivedi 2021's two stages re-pooled, and its bupropion-alone estimate is too imprecise to separate the two drugs' contributions. No change needed.
- **cl_meth_withdrawal_medication.** Still correct that the withdrawal trials of mirtazapine differ from the dependence trials. No change.
- **cl_meth_cognition.** Not touched.

## Reporting errors noticed

**McKetin 2026.**
- Abstract prints the mean difference as +2.2 with CI −4.2 to −0.2 (p. 581).
- The "8% reduction in risk" is an absolute 2.2 of 28 days, whereas the IRR implies an 11% relative reduction. It is compared with a "14%" figure for a different outcome (pp. 585, 587).
- Table 3 gives P = .19 for discontinuation due to adverse reactions, 25/167 vs 40/172. Recomputed from those counts, P ≈ .05 (p. 586).
- The abstract labels those discontinuations "due to adverse events", but Figure 1 shows mostly dislike of the medication or feeling it did not work.
- EQ-5D changes of 1.3 and 2.2 cannot be on the 0–1 utility scale of Table 1.
- "Intention-to-treat" in Table 2 is a modified ITT (n = 339).
- 11/339 is printed as 4%.

**Bakouni 2023.**
- N = 1239 double-counts 225 people.
- Urine samples and pills are used as the unit of analysis.
- A 19-person pilot moves two subgroup estimates noticeably (Table 4).
- RoB 2 is cited to the 2011 paper on the original tool.
- "Medium" is used as a GRADE level.

**Tooling.** The reference record for bakouni_2023 stores page "111018" (the article number), so `check_anchor_numbers.py` cannot map its printed pages 1–12. I ran it on a scratch copy with the pages set to 1–12; the editor may want to handle article-number references in the checker.
