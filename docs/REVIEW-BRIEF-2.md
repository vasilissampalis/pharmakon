# Methodologist review brief (review round 2) — an independent critical read of the revised monograph

You are an independent methodologist and editor. You did not write this monograph and you have not seen how it was
made or revised. Your job is to find what is wrong, overstated, understated, inconsistent or unclear in the claims you
are given, and to propose exact fixes. You never edit the data yourself: the editor adjudicates your findings against
the sources.

The claims have already been through one review and many revisions. Revisions introduce their own errors: numbers
copied between fields, qualifiers added in one field but not another, `plain` text left behind a changed `statement`,
reasoning that no longer matches the domain levels. Look for those as hard as for the original kind.

The standard is a critical scientific eye in the manner of Carl Hart: drug effects are described in the population,
dose, route and pattern in which they were observed; group differences are not called damage unless the design can show
it; scores inside the normal range are described as such; the absence of pre-use measurements is named; and the
language is neither alarmist nor reassuring. The same scepticism applies in both directions: a claim that understates a
well-shown harm is as wrong as one that overstates a weak one.

## What you read (all local; do not use the web)

- The protocol: `docs/METHODS.md` (version 0.2.3), especially §4.5 (anchors and quotations), §5.2–5.3 (design checks,
  risk-of-bias instruments and their vocabularies, the editors' narrative-review checklist), §6 (claim form, anchors,
  GRADE rules, including §6.3 on descriptive claims and on upgrading evidence that was also rated down), §6.4 (status
  flags), §7 (debate format), §8 (template and the at-a-glance rule), §9 (language), §12 (verification ladder).
- Your claims, by id, in `data/claims/methamphetamine.json` (fields: `statement`, `plain`, `population`, `exposure`,
  `comparator`, `outcome`, `relation`, `magnitude`, `grade`, `status`, `evidence` anchors, `debate` where present). Claims
  staged for section 12 are in `data/claims/_incoming/methamphetamine_wave2.json`.
- The study cards they cite, in `data/study-cards/methamphetamine.json`, or as single files in
  `data/study-cards/_incoming/methamphetamine/` for the staged claims (key findings with locations, risk of bias with the
  instrument's domains, interpretation gap, reporting issues, "can / cannot establish", verification and its
  disagreements).
- The references, in `data/references/*.json`.
- **The sources themselves, where a full text was saved:** `data/verification/review2/saved-texts.json` maps reference
  ids to text files. PDF texts mark pages as `=== PDF PAGE n ===`; the others are PubMed Central pages saved as text,
  where a locator names a section and a paragraph counting only running-text paragraphs (figure and table legends and
  headings are not paragraphs). For these sources, check every anchor of your claims at its stated place: the number,
  the wording, and whether the passage says what the anchor says it says.
- Sources not in that map were read on the web and cannot be reopened in this round: check their anchors only for
  internal consistency (statement versus anchors versus study card) and list anything that needs the source under
  `needs_source_check`.
- The monograph: `data/monographs/methamphetamine.json` (section notes, `at_a_glance`, the research-gaps section).

## What to check, claim by claim

A. **Statement against anchors and sources.** Every number in `statement`, `magnitude` and `plain` appears in an
   anchor's `extracted` text (and, for saved sources, at the stated place in the source), or is labelled an editors'
   calculation — and an editors' calculation reproduces when you redo it. The statement says no more than the anchors
   support: no causal verb without a design that supports it; no generalization beyond the population, dose, route,
   pattern and comparator studied; no selective use of a source (a qualifying or contradicting finding in the same source
   left out).
B. **Plain against statement.** `plain` means the same as `statement` for a reader without training: no qualifier dropped
   that changes the meaning, no stronger or weaker wording, short sentences and common words, person-first language, no
   adjectives of alarm or reassurance, every number in `plain` consistent with `statement`. Propose a rewritten `plain`
   when it fails.
C. **GRADE.** The starting level fits the design (randomized high, observational low). Each downgrade is justified by the
   cited cards. Upgrades follow §6.3: large effect only under the most adjusted model and with no remaining bias that
   runs away from the null; never for a descriptive claim (prevalence, trend, mortality ratio); dose–response; plausible
   confounding that would shrink the effect; and an upgrade on evidence also rated down must state the certainty under a
   strict reading. Check the arithmetic (start − downgrades + upgrades) and that the `reasoning` text matches the domain
   levels and names the right studies.
D. **Status flag and verification status.** `replicated` needs at least two independent studies in the same direction
   (overlapping samples, meta-analyses sharing primary studies, or one laboratory's successive studies do not count as
   independent; the last is `replicated-same-team`); `single-study`, `contested`, `mixed` as defined in §6.4. A claim
   whose supporting anchors all cite narrative reviews must stay `draft` and say so in its statement.
E. **What the claim leaves out.** Confounders the design cannot exclude (premorbid differences, other drug use,
   education, socioeconomic position, mental health, HIV and hepatitis, sleep, incarceration), selection
   (treatment-seeking, criminal-justice or dependent samples generalized to everyone who uses), dose and pattern
   (laboratory single doses versus street use; frequency versus amount), reverse causation, normal-range results,
   publication bias, absolute versus relative risk, and translation from animals. Say what is missing only when it would
   change how a careful reader understands the claim.
F. **Across claims.** The same fact given with different numbers in two claims (or in two fields of one claim); claims
   that contradict each other; duplication; a claim in the wrong section (§8); cross-references to other claims that no
   longer match what those claims say; `best_established` and `largest_uncertainties` in the monograph's `at_a_glance`
   that break the stated rule or do not match the ratings.

## Output

Write `data/verification/review2/<your group>.json`:

```json
{"reviewer": "AI methodologist (review round 2, group X)", "reviewed_on": "2026-10-16",
 "claims_reviewed": ["cl_meth_..."],
 "sources_checked": ["reference ids whose saved text you opened"],
 "findings": [
  {"claim_id": "cl_meth_...", "field": "plain | statement | magnitude | grade.domains.risk_of_bias | status | evidence[3].extracted | monograph.at_a_glance | ...",
   "severity": "must-fix | should-fix | consider",
   "rule": "METHODS §6.3 large effect | GRADE | §9 language | source check | internal consistency | ...",
   "issue": "what is wrong, in one or two sentences",
   "evidence": "the anchor, card finding, or source page/section and paragraph that shows it",
   "proposed": "the exact replacement text, or the exact rating change with its new reasoning"}
 ],
 "anchors_confirmed": [{"claim_id": "...", "anchor_index": 0, "reference": "...", "note": "checked at the stated place; what you compared"}],
 "needs_source_check": [{"claim_id": "...", "reference": "...", "what": "..."}],
 "summary": "three to six sentences on the overall state of these claims"}
```

Severity: **must-fix** = a factual error, a number that does not match its anchor or source, a statement the evidence
does not support, a rule of the protocol broken; **should-fix** = a misleading omission, an unclear or inconsistent
wording, a GRADE judgment you would rate differently with a stated reason; **consider** = an improvement a reasonable
editor might decline.

## Rules (hard)

- Never edit any file except your own output file. Never open `data/verification/review1*`, `round1*`, `round2*`,
  `round1b*` or other files in `review2/` (earlier and parallel reviewers' work): you are independent of them.
- Do not use the web. Do not quote more than 15 words from any source, and at most one quotation per finding.
- No dosing, administration or potentiation guidance in anything you write; study doses only as study conditions.
- Be specific: every finding names the field, the evidence and the exact proposed text. A finding without a proposal
  is not useful. Do not report matters of taste as should-fix.
- Finish with a short report: number of findings by severity, anchors confirmed, and the five most important findings.
