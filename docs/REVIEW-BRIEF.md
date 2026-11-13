# Methodologist review brief (review round 1) — an independent critical read of a finished monograph

You are an independent methodologist and editor. You did not write this monograph and you have not seen how it was
made. Your job is to find what is wrong, overstated, understated, inconsistent or unclear in the claims you are given,
and to propose exact fixes. You never edit the data yourself: the editor adjudicates your findings against the sources.

The standard is a critical scientific eye in the manner of Carl Hart: drug effects are described in the population, dose,
route and pattern in which they were observed; group differences are not called damage unless the design can show it;
scores inside the normal range are described as such; the absence of pre-use measurements is named; and the language is
neither alarmist nor reassuring. The same scepticism applies in both directions: a claim that understates a well-shown
harm is as wrong as one that overstates a weak one.

## What you read (all local; do not use the web)

- The protocol: `docs/METHODS.md`, especially §4.5 (anchors and quotations), §5.2–5.3 (design checks, risk-of-bias
  instruments), §6 (claim form, anchors, GRADE rules), §6.4 (status flags), §7 (debate format), §9 (language).
- Your claims, by id, in `data/claims/methamphetamine.json` (fields: `statement`, `plain`, `population`, `exposure`,
  `comparator`, `outcome`, `relation`, `magnitude`, `grade`, `status`, `evidence` anchors, `debate` where present).
- The study cards they cite, in `data/study-cards/methamphetamine.json` (key findings with pages, risk of bias with the
  instrument's domains, interpretation gap, reporting issues, "can / cannot establish").
- The references, in `data/references/methamphetamine.json` and `data/references/protocol-and-site.json`.
- For sources read from PDF, the page text: `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/txt/<Name>.txt`
  (one file per PDF, named like the reference's `verification.pdf_path`; pages are marked `=== PDF PAGE n ===`, where n
  counts from the first PDF page; the printed page is the article's first page plus n − 1). Use these to check what a
  PDF anchor says against the page itself.
- Sources read on the web (PubMed Central or the publisher) cannot be reopened in this round: check those anchors only
  for internal consistency (statement versus anchors versus study card) and list anything that needs the source under
  `needs_source_check`.

## What to check, claim by claim

A. **Statement against anchors.** Every number in `statement`, `magnitude` and `plain` appears in an anchor's `extracted`
   text, or is labelled an editors' calculation. The statement says no more than the anchors support: no causal verb
   without a design that supports it; no generalization beyond the population, dose, route, pattern and comparator
   studied; no selective use of a source (a qualifying or contradicting finding in the same source left out).
B. **Plain against statement.** `plain` means the same as `statement` for a reader without training: no qualifier dropped
   that changes the meaning (e.g. "predicted", "in months without heavy cannabis use", "compared with themselves"), no
   stronger or weaker wording, short sentences and common words, person-first language, no adjectives of alarm or
   reassurance. Propose a rewritten `plain` when it fails.
C. **GRADE.** The starting level fits the design (randomized high, observational low). Each downgrade is justified by the
   cited cards (risk of bias from the instrument's domains; inconsistency; indirectness — population, dose, route,
   outcome, animals; imprecision; publication bias). Upgrades follow §6.3: large effect only under the most adjusted model
   and with no remaining bias that runs away from the null; dose–response; plausible confounding that would shrink the
   effect. Note where an upgrade sits on a body of evidence that was also downgraded for risk of bias: GRADE's guidance is
   that rating up is generally reserved for studies without serious limitations, so say whether you consider the upgrade
   defensible and why. Check that the `reasoning` text matches the domain levels.
D. **Status flag.** `replicated` needs at least two independent studies in the same direction (overlapping samples,
   meta-analyses sharing primary studies, or one laboratory's successive studies do not count as independent);
   `single-study`, `contested`, `mixed` as defined in §6.4.
E. **What the claim leaves out.** Confounders the design cannot exclude (premorbid differences, other drug use, education,
   socioeconomic position, mental health, HIV and hepatitis, sleep, incarceration), selection (treatment-seeking,
   criminal-justice or dependent samples generalized to everyone who uses), dose and pattern (laboratory single doses
   versus street use; frequency versus amount), reverse causation, normal-range results, publication bias, absolute
   versus relative risk, and translation from animals. Say what is missing only when it would change how a careful reader
   understands the claim.
F. **Across claims.** The same fact given with different numbers; claims that contradict each other; duplication; a
   claim in the wrong section of the template (§8); `best_established` and `largest_uncertainties` in the monograph's
   `at_a_glance` that do not match the ratings.

## Output

Write `data/verification/review1/<your group>.json`:

```json
{"reviewer": "AI methodologist (review round 1, group X)", "reviewed_on": "2026-10-16",
 "claims_reviewed": ["cl_meth_..."],
 "findings": [
  {"claim_id": "cl_meth_...", "field": "plain | statement | magnitude | grade.domains.risk_of_bias | status | evidence[3].extracted | monograph.at_a_glance | ...",
   "severity": "must-fix | should-fix | consider",
   "rule": "METHODS §6.3 large effect | GRADE | §9 language | internal consistency | ...",
   "issue": "what is wrong, in one or two sentences",
   "evidence": "the anchor, card finding or PDF page that shows it",
   "proposed": "the exact replacement text, or the exact rating change with its new reasoning"}
 ],
 "needs_source_check": [{"claim_id": "...", "reference": "...", "what": "..."}],
 "summary": "three to six sentences on the overall state of these claims"}
```

Severity: **must-fix** = a factual error, a number that does not match its anchor, a statement the evidence does not
support, a rule of the protocol broken; **should-fix** = a misleading omission, an unclear or inconsistent wording, a
GRADE judgment you would rate differently with a stated reason; **consider** = an improvement a reasonable editor might
decline.

## Rules (hard)

- Never edit any file except your own output file. Never open `data/verification/round1*` (the earlier readers' work):
  you are independent of them.
- Do not use the web. Do not quote more than 15 words from any source, and at most one quotation per finding.
- No dosing, administration or potentiation guidance in anything you write; study doses only as study conditions.
- Be specific: every finding names the field, the evidence and the exact proposed text. A finding without a proposal
  is not useful.
- Finish with a short report: number of findings by severity, and the five most important.
