# Adjudication brief — review round 2 findings

Three independent methodologists reviewed the methamphetamine claims (review round 2, `docs/REVIEW-BRIEF-2.md`; findings
in `data/verification/review2/group_P.json`, `group_N.json`, `group_M.json`). You adjudicate one group's findings. The
reviewer is not presumed right and neither is the current text: **the source decides**. You never edit project data
files; you write proposals that the editor applies after reading them.

## What you read

- `docs/METHODS.md` (version 0.2.4, the protocol; read §4.5, §5.3, §5.5–5.6, §6, §8, §9, §10.3, §12 before starting).
- Your group's review file, every finding in it, and its `anchors_confirmed` and `needs_source_check` lists.
- The claims in `data/claims/methamphetamine.json` (and, for group P, the staged claims in
  `data/claims/_incoming/methamphetamine_wave2.json`); the study cards in `data/study-cards/methamphetamine.json` (or as
  single files in `data/study-cards/_incoming/methamphetamine/`); the monograph `data/monographs/methamphetamine.json`.
- The saved full texts listed in `data/verification/review2/saved-texts.json`. PDF texts mark pages as
  `=== PDF PAGE n ===` (printed page = article's first page + n − 1); the others are PubMed Central pages saved as text:
  locate by section and running-text paragraph (headings, figure and table legends are not paragraphs).

## Already done since the reviewers read the files (do not redo; mark such findings `already-fixed`)

- At a glance: `cl_meth_psychosis_course` replaced among the largest uncertainties by `cl_meth_cognition_abstinence`;
  the mechanism line now says the mechanism is described in a narrative review; the legal summary gives the Greek table.
- Anchors: `cl_meth_pk_intranasal_timecourse` anchor 5 set back to ai-located (written and checked by the same reader);
  `cl_meth_grey_matter` anchor 7 corrected by an independent reader (parietal finding from one study; 2nd paragraph only)
  and the statement changed to match; `cl_meth_cognition_abstinence` anchor 2 confirmed by an independent reader with its
  locator extended to Method › Participants; `cl_meth_psychosis_treatment` anchor 2 confirmed by an independent reader;
  `cl_meth_dopamine_damage` anchor 4 provenance recorded (card sc_volkow_2001a key finding 7).
- Cards: `sc_wearne_2018` back to first-pass (open overall risk-of-bias disagreement); `sc_ersche_2012`,
  `sc_callaghan_2012`, `sc_anthony_1994`, `sc_cruickshank_2009` set to draft (written from abstracts); `sc_harding_2022`
  uses the new `editors-qualitative` instrument; `sc_basterfield_2019` and `sc_cao_2026` ratings marked provisional.
- Known and queued, not for you: re-appraising `sc_kish_2008`, `sc_bramness_2012` and `sc_cruickshank_2009` with the
  narrative-review checklist needs their full texts (not saved) — mark such findings `deferred` with reason "full text
  needed". Person-first wording ("users") in anchors' `extracted` text and in GRADE reasoning will be handled by a
  separate language pass over all claims — mark pure wording findings of that kind `deferred` with reason "language
  pass", unless the wording also misstates the source.
- METHODS 0.2.4 added the relation `describes` for descriptive claims (§6.1). Recode a descriptive claim in your group
  (prevalence, base rates, trends, standardized mortality) to `relation: describes` in your patch.

## What to do with each finding

1. Read the finding, then check it yourself: in the saved source text at the stated place when the source is saved; in
   the study card and anchors otherwise. Recompute any arithmetic.
2. Give a verdict: `accept` (the finding is right and the proposed text is right), `accept-modified` (right, but you
   change the fix — say why), `reject` (the finding is wrong, or the change would make the claim less faithful to the
   source — say what the source shows), `already-fixed`, or `deferred` (needs a source that is not saved, or is the
   senior author's judgment call, or belongs to the language pass — say which).
3. For accepted changes, write the edit. Every number you put into a claim must sit in an anchor's `extracted` text or
   be labelled an editors' calculation that you have recomputed. If a fix needs a number that no anchor carries, add an
   anchor (`evidence_add`) located in a saved full text, with page/locator per §6.2, `role`, and
   `located_by: "AI adjudicator (review round 2), from the saved full text"` — it enters as ai-located (claim_patch
   moves an ai-anchored claim back to metadata-verified until a second reader checks it; say so in the log).
4. GRADE: change a rating only when the protocol requires it and say which rule (§6.3); keep the arithmetic right
   (start − downgrades + upgrades) and rewrite `grade.reasoning` to match the domains. State the strict reading where
   §6.3 asks for it. A change of certainty or meaning is a `minor` bump; wording is `patch`.
5. Keep `plain` and `statement` consistent; `plain` in short sentences and common words, person-first, no adjectives of
   alarm or reassurance; no dosing or administration guidance anywhere (study doses only as study conditions);
   quotations at most 15 words and one per claim.

## Output (scratchpad: `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/adj2/`)

- `<G>_log.json`: one entry per finding, in the review file's order:
  `{"n": 0, "claim_id": "...", "field": "...", "severity": "...", "verdict": "...", "reason": "what you checked and found",
  "evidence": "source page/section and paragraph, or card field", "patch_ref": "index in your patch file or null"}`.
- `<G>_patch.json`: claim edits in the format of `scripts/claim_patch.py` (read its docstring; one patch object per
  claim, using `expect` on the fields you change where useful, `replace` for exact substring edits, `set` for whole
  fields, `evidence_set` and `evidence_add` for anchors, `bump`, and `change` — the changelog line, which should say
  "Review round 2:" and what changed and why). Only claims of your own group; list cross-group items in the log with
  verdict `accept` and `patch_ref: "other group"`, saying exactly what the other claim needs.
  Check it with `cd /home/claude/drug-encyclopedia && python3 -I scripts/claim_patch.py <your patch> --dry-run` until it
  reports "checked (dry run)".
- `<G>_cards.json`: proposed study-card edits (not applied by you): `[{"card": "sc_...", "path": "key_findings.3.locator",
  "old": "...", "new": "...", "reason": "..."}]`.
- `<G>_monograph.json`: proposed monograph edits in the same shape (`"card"` replaced by `"target": "monograph"`).

## Rules (hard)

- Write only inside the `adj2/` folder above. Do not edit any file under `data/`, `docs/`, `scripts/` or `site/`.
- Do not use the web. Do not open `data/verification/review1*`, `round1*` or `round2*`; you may open the other two
  groups' review2 files only to avoid contradicting them on cross-group points.
- Final message: counts by verdict; the certainty changes you propose (claim, from → to, rule); new anchors added; the
  five most consequential edits; anything the editor must decide.
