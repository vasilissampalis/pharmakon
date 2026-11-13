# Audit: protocol vs briefs, site text and scripts (2026-10-16)

**Auditor:** an independent AI auditor. I only read the project. This report is the only file I wrote.
**Snapshot:** files as they stood at 04:20 EEST on 16 October 2026. `docs/METHODS.md` is v0.2.3 and was last changed at 03:22. Three files changed while I worked: the site footer went from "prototype v0.3.0" to "v0.3.1" (template, 04:02), `docs/REVIEW-BRIEF-2.md` appeared (04:10), and `data/study-cards/methamphetamine.json` was rewritten (04:08). I re-checked every fact below after those changes.

**What I read:**
- Docs: METHODS, WORKFLOW, STATUS, TIER1 and README.
- Briefs: VERIFICATION, STUDY-CARD, REVIEW, REVIEW-2, ADJUDICATION and EVIDENCE-MAP.
- Site: `site/src/index.template.html`, `app.core.js`, `app.views.js` and `site/build.js`.
- Scripts: `validate.py`, `rob_vocab.py`, `check_card.py`, `reconcile_second_reader.py`, `apply_senior_review.py`, `claim_patch.py`, `check_anchor_numbers.py`, `make_blind_tasks.py`, `merge_cards.py`, `build_references.py` and `check_citations.js`.
- All schemas.
- Methamphetamine data: claims, cards, monograph, references, figures, legal, identity, glossary and the verification rounds.
- The exported v0.2.1 protocol at `/mnt/attach/outputs/DrugEncyclopedia/docs/METHODS.md`.

**What I ran (all read-only):**
- `python3 -I scripts/validate.py`: 0 hard failures and 266 warnings. The warnings are 259 anchors not yet senior-verified, 4 AMSTAR 2 items on Stockings 2019, and 3 cards whose design and instrument do not match.
- All counts below come from throw-away scripts I ran in the scratchpad.

**Data at a glance (methamphetamine):**

| What | Count | Breakdown |
|---|---|---|
| Claims | 33 | draft 9 (6 of them rest only on narrative reviews); metadata-verified 13; ai-anchored 11; none higher |
| Evidence anchors | 259 | unchecked 5; ai-located 40; ai-checked 214 (128 re-found blind, 86 checked at the stated place); senior-verified 0 |
| Anchors located by the editor, not the first reader | 64 | |
| Study cards | 40 | first-pass 21; ai-checked 19; appraised 0. Four cards have no `source_read` |
| Reference records | 53 | 46 from Crossref; 7 checked against publishers' pages |
| Monograph | v0.3.1 | status draft |
| Evidence maps | 36 | 30 substances and 6 cross-cutting topics |

**How each finding is laid out:**
- an id and a severity;
- where each side says it, as file:line (claims and cards are named by id);
- what each side says, and what the data show where that matters;
- which side should change and why, citing METHODS where it decides;
- replacement text ready to paste.

**Severity levels:**
- **contradiction:** two places say different things.
- **outdated:** a statement no longer holds.
- **gap:** a rule with no check, or a practice with no rule.
- **ambiguity:** a rule that can be read two ways, where practice has settled on one.
- **wording:** a small mismatch in phrasing.

Anchor indexes are 0-based.

---

## A. Verification ladder, statuses and readers

### M1 · contradiction · What `ai-checked` and `ai-anchored` mean: blind re-finding only, or also a check at the stated place?
- **Strict side:**
  - METHODS §6.2 table, `docs/METHODS.md:217`: ai-checked means "Re-found independently by a second AI reader that had not seen the first".
  - §12, `:344`: ai-anchored means every anchor was "re-found by an independent AI reader".
  - `schema/claim.schema.json:125` and `:293` use the same wording.
- **Permissive side:**
  - METHODS §5.5, `docs/METHODS.md:191`: anchors the blind reading missed are "checked one by one at the place the first reader gave". They then become ai-checked with `check_mode: targeted`.
  - `schema/claim.schema.json:149–155` defines `check_mode`.
- **Public text follows the strict side:**
  - `site/src/index.template.html:186` says AI-ANCHORED means "every number re-found in the paper by a second, independent AI reader".
  - `:322` says the second reader "has not seen the first reader's anchors".
  - `:330` says "independent, blind second AI reading".
  - `site/src/app.views.js:63` counts targeted anchors under "anchors re-found by an independent second AI reader" (214 / 259).
  - The glossary entry "Evidence anchor" says the same.
  - Only the label on each anchor tells the two apart (`app.views.js:131`, "checked at the stated place").
- **Practice:**
  - Of the 214 ai-checked anchors, 128 were re-found blind and 86 were checked at the stated place.
  - 46 of those 86 were added by the editor after the blind round, so no blind reader ever saw them.
  - 10 of the 11 ai-anchored claims rest partly on targeted checks. cl_meth_cognition_causal rests entirely on them (14 of 14 anchors), and it is first among the at-a-glance "largest uncertainties".
  - The claims' changelogs say: "re-found blind or checked at the stated place … metadata-verified → ai-anchored".
- **Which side changes:** §5.5 is the more specific rule, written later, and practice follows it. §6.2, §12, the schema descriptions and the public text should follow §5.5. If the senior author wants ai-anchored to mean blind re-finding only, the 10 claims step back instead.
- **Proposed text:**
  - `METHODS.md:217` → `| ai-checked | Confirmed by a second AI reader: re-found blind (check_mode: blind), or, if the blind reading missed it, checked at the place given (check_mode: targeted; shown as "checked at the stated place") |`
  - `METHODS.md:344` → `| ai-anchored | Every evidence anchor located in the full text and confirmed by a second AI reader, blind or at the stated place (§5.5) |`
  - `claim.schema.json:125` and `:293`: the same two definitions.
  - `index.template.html:186` → "AI-ANCHORED (every anchor confirmed by a second AI reader: re-found without seeing the first reader's work, or checked at the place the first reader gave)"
  - `:322` → "Every located evidence anchor is checked by a second AI reader: first blind, without the first reader's anchors; anchors it does not re-find are then checked at the stated place and labelled so."
  - `:330` → "runs an independent second AI reading (blind first, then checks at the stated place)"
  - `app.views.js:63`: split the counter in two. One counts "anchors re-found blind by a second AI reader" (`check_mode` blind). The other counts "anchors checked at the stated place by a second AI reader" (targeted).
  - Glossary "Evidence anchor" → "…located by an AI reader, re-found blind or checked at the stated place by a second AI reader, or checked by the senior author against the source."

### M2 · contradiction · The targeted-check rule entered §5.5 with no changelog entry
- **Sides:**
  - `docs/METHODS.md:4` says changes "are logged in the Changelog".
  - The site Methods page, `index.template.html:225`, says "every later change is listed in its changelog with the reason and the date".
  - Against this: `METHODS.md:191`, and the changelog at `:419–420`.
- **Evidence:**
  - I compared the v0.2.1 export with v0.2.3. Two sentences were added to §5.5 after 0.2.1: one on targeted checks, one on anchors written by the second reader.
  - Neither the 0.2.2 entry nor the 0.2.3 entry mentions them. Yet they changed what ai-checked means (M1) and moved 10 claims to ai-anchored.
  - The changelog also lists 0.2.3 above 0.2.2.
- **Which side changes:** the changelog. METHODS line 4 decides.
- **Proposed text:** add as item 5 of 0.2.3, or as a new 0.2.4:
  > "**(5) Targeted checks (§5.5).** Anchors that the blind second reading did not re-find are checked by the second reader at the place the first reader gave and become ai-checked with check_mode: targeted, labelled 'checked at the stated place'; an anchor written by the second reader counts only when the first reader's card records the same finding (`located_by`). Applied to 86 methamphetamine anchors; 10 claims became ai-anchored partly on this basis."

  Also move 0.2.2 above 0.2.3.

### M3 · contradiction · What "draft" means
- **Sides:**
  - METHODS §12, `METHODS.md:342`: "AI-drafted; nothing verified".
  - §16, `:388`: "no claim leaves draft status without the senior author checking its excerpts".
  - Site, `index.template.html:68`: "Nothing leaves draft until its evidence anchors are checked".
  - `:185`: "A claim cannot leave draft status until a human has checked its anchors".
  - `:320`: "Every claim drawn from a paper stays draft until the last step".
  - `:333`: "no claim leaves draft status until a human has checked…".
  - `app.views.js:63` counts all 33 claims as "draft claims".
  - The Review tab, `app.views.js:535`, labels draft claims "waits for primary sources".
- **Practice:** the ladder is set by `validate.py:65–71` and `:99–108`, and by `reconcile_second_reader.py:103–105`.
  - 24 of the 33 claims are above draft (13 metadata-verified, 11 ai-anchored). No human has checked any of them.
  - The 9 draft claims either have an unchecked anchor or rest only on narrative reviews.
  - Two draft claims have every anchor ai-checked: cl_meth_psychosis_treatment (5 of 5) and cl_meth_psychosis_vs_schizophrenia (9 of 9). So "nothing verified" is wrong as well.
- **Which side changes:** the ladder in §6.2 and §12, and the data, define rungs above draft that need no human. §16 and the site text are wrong. §12's own definition of draft is out of date.
- **Proposed text:**
  - `METHODS.md:342` → `| draft | Not yet on the ladder: an anchor is not yet located in a full text, or the claim rests only on narrative reviews (§6.3) |`
  - `:388` → "The AI co-editor can misread a source; this is why no claim is senior-reviewed or published (§12) until the senior author has checked its evidence anchors against the source."
  - `index.template.html:68` → "Nothing is published until the senior author has checked its evidence anchors against the source."
  - `:185` → "A claim cannot be published until the senior author has checked its anchors against the source."
  - `:320` → "Every claim drawn from a paper stays unpublished until the senior author has checked it; its stamp shows how far it has got."
  - `:333` → "…why no claim is published until a human has checked its evidence anchors against the source, and why that status is printed on every claim."
  - `app.views.js:63` → "claims (none yet checked by the senior author)". Alternatively, one counter per verification status.

### M4 · contradiction / gap · `appraised` and the senior author's reading of study cards exist only on paper
- **What the protocol says:**
  - METHODS §5.5, `METHODS.md:193–195`: the senior author "Reads the card against the source … Status appraised". No claim resting on a card rises above ai-anchored without that reading.
  - `schema/study-card.schema.json:432` agrees.
- **Where it disagrees:**
  - §12, `METHODS.md:346`, defines a claim as appraised when "All study cards complete with second reading". This is wording left over from the two-reader protocol.
  - The site Methods page repeats it at `index.template.html:275`.
- **Where it is not implemented:**
  - WORKFLOW steps 10–11 (`docs/WORKFLOW.md:17–18`) and `apply_senior_review.py:11–12` and `:50–53` move an approved claim straight to senior-reviewed once its anchors are ticked.
  - `validate.py:68–73` never looks at card status.
  - The Review tab (`app.views.js:515–541`) has no control for appraising a card.
- **Practice:**
  - No card is appraised.
  - No script ever sets a claim to anchor-verified or appraised.
  - An approved claim would jump from ai-anchored straight to senior-reviewed.
- **Which side changes:** §5.5 decides. The §12 row is ambiguous: "second reading" could mean AI reader 2, which would put appraised below ai-anchored. The §12 row, the workflow, the scripts and the Review tab should change.
- **Proposed text:**
  - `METHODS.md:346` → `| appraised | Every study card the claim rests on has been read against its source by the senior author (card status appraised, §5.5) |`
  - `WORKFLOW.md:17` (step 10) → "…ticks each anchor after checking it against the source, marks each study card appraised after reading it against the source, then approves, approves with edits, or flags each claim with a note"
  - `WORKFLOW.md:18` (step 11) → "…ticked anchors become senior-verified; a claim whose anchors are all senior-verified becomes anchor-verified, and appraised when every card it cites is appraised; approved claims that are appraised become senior-reviewed"
  - `apply_senior_review.py:11–12` → "'approved' or 'approved-with-edits' moves the claim to 'senior-reviewed' only when every anchor is senior-verified, every study card it cites is appraised, and the decision was made on the current claim version". The script should also set anchor-verified and appraised on the way.
  - `validate.py`: fail any claim at anchor-verified or above when a card it cites is not appraised (§5.5).
  - Review tab: add a per-card "read against the source" tick, stored as `cards/<card_id>` in the site's database.

### M5 · contradiction · `flagged` is a post-publication status but is used for review flags
- **The protocol:**
  - METHODS §12, `METHODS.md:349`: "A post-publication issue is open (§13)".
  - `:351`: the flag is shown publicly.
  - The site Methods page repeats this at `index.template.html:278`.
- **The scripts and site:**
  - `apply_senior_review.py:13` and `:58–59` set `verification.status = flagged` when the senior author flags a claim in review, before publication.
  - `WORKFLOW.md:18`: "flagged claims are reworked and go back to step 10".
  - How-to, `index.template.html:186`: "FLAGGED (a problem was found and the claim is being corrected)".
  - Nothing says which rung a reworked claim returns to.
- **Which side changes:** METHODS §12 decides, because `flagged` belongs to the public correction process of §13. The review decision is already stored in `senior_review.decision`.
- **Proposed text:**
  - `apply_senior_review.py:13` → "'flagged' is recorded in senior_review with its note; verification.status is left unchanged and the editor reworks the claim (WORKFLOW step 11)". Remove the status change at `:59`.
  - `index.template.html:186` → "FLAGGED (a problem reported after publication is open and being corrected)".
  - If the senior author prefers the wider use, change `METHODS.md:349` instead: `| flagged | An issue raised in senior review or after publication is open; when it is closed the claim returns to the rung its anchors support |`

### M6 · contradiction · When a study card becomes `ai-checked`
- **The rule:**
  - METHODS §5.5, `METHODS.md:191`: "A card that the second reader confirmed in full, with agreement on risk of bias, becomes ai-checked".
  - `reconcile_second_reader.py:116–117` applies it, and also requires agreement on the interpretation gap and nothing missed.
- **Where it disagrees:**
  - `ADJUDICATION-BRIEF.md:36–48` has the adjudicator correct the flagged items.
  - It leaves risk-of-bias and interpretation-gap disagreements of judgment to the senior author (`:42`).
  - Then it says "Then set verification.status to ai-checked" (`:47`).
  - `study-card.schema.json:432` defines ai-checked as "re-found … disagreements logged".
  - The site Methods page (`index.template.html:254`) says "every disagreement is settled against the source and logged on the card".
- **Practice:**
  - All 19 ai-checked cards carry `checked_by` "AI reader 2 (blind reading and adjudication)".
  - sc_hart_2012 logs 9 disagreements.
  - sc_wearne_2018 is ai-checked although its two blind narrative-checklist readers disagree on the overall rating (high against some-concerns). The card leaves that "for the senior author".
  - Four other narrative-review cards agree on the overall rating but not on every domain. sc_hart_2012 and sc_london_2015 differ on two domains each, sc_glasner_edwards_2014 on three and sc_dean_2013 on one. All are ai-checked, with the differences "for the senior author".
- **Which side changes:**
  - **Option 1 (recommended): keep §5.5 as written.** METHODS §5.5 decides as it stands. Cards with an open risk-of-bias disagreement go back to first-pass. Change `ADJUDICATION-BRIEF.md:47` to: "Then, if no risk-of-bias or interpretation-gap disagreement remains for the senior author, set verification.status to ai-checked; otherwise leave first-pass and list the disagreement."
  - **Option 2: rewrite §5.5 to match practice,** if the senior author prefers the adjudication route. Replace the §5.5 sentence with: "A card becomes ai-checked when the second reader confirmed every key finding and reporting issue and agreed on risk of bias and the interpretation gap, or when an adjudicating AI reader has checked each item the second reader flagged against the source, corrected the factual ones and logged every change in verification.disagreements; disagreements of judgment are left unchanged, listed for the senior author and shown on the card."

### M7 · gap · In practice, more readers check the work than the three-reader rule describes
- **The protocol:**
  - METHODS §5.5 (`METHODS.md:189–197`) describes three readers.
  - §16, `:387`, still says "two-reader rule".
  - The methodologist review appears only in changelog item 0.2.2 (4), `:420`.
  - WORKFLOW's step table (`WORKFLOW.md:6–21`) has none of the steps below.
  - The site Methods page (`index.template.html:254`) mentions only the methodologists.
- **Practice:**
  - **Adjudication** (round 1b, `ADJUDICATION-BRIEF.md`).
  - **Targeted checks by "AI reader 2 (targeted checks)"**, run from `data/verification/targeted-2026-10-16/tasks.json`. There is no brief for these in `docs/`.
  - **Two targeted checks by "AI editor (targeted check)"**: cl_meth_psychosis_treatment anchor 2 and cl_meth_cognition_abstinence anchor 2. The editor is the AI that drafted the claims, so these are not second-reader checks under §5.5. The second of them moved cl_meth_cognition_abstinence to ai-anchored.
  - **AI reader 3** re-appraised the narrative reviews (`review1/narrative_rerate.json`).
  - **AI reader 4** checked that re-appraisal blind (`review1-blind/narrative_reader4.json`).
  - **Methodologist review rounds 1 and 2** (`REVIEW-BRIEF.md`, `REVIEW-BRIEF-2.md`). Round 2 also returns `anchors_confirmed` (`REVIEW-BRIEF-2.md:91`). Nothing says what that does to an anchor's status.
- **Proposed text:** a new METHODS §5.6, "Further AI checks":
  > "Between the second reading and the senior author, further AI readers may: (a) adjudicate the second reader's card findings against the source (§5.5); (b) re-appraise a card with a different instrument, with a blind check by another reader whose disagreements go to the senior author; (c) review every claim as independent methodologists against its evidence and this protocol (docs/REVIEW-BRIEF*.md). Their findings are adjudicated against the source by the editor and logged on the claim or card. Only the second reader's blind or targeted checks set an anchor to ai-checked; a methodologist's confirmation of an anchor is recorded in the claim's changelog and does not change its status."

  Also:
  - Add these steps to WORKFLOW's table.
  - Have the second reader redo the two editor targeted checks. Alternatively, add "or the editor, from a saved full text" to §5.5, if the senior author accepts that.

### M8 · contradiction · Four anchors written by the second reader break the `located_by` rule
- **The rule:** METHODS §5.5, `METHODS.md:191`. An anchor written by the second reader "counts as ai-checked only when the first reader's card already records the same finding". In that case `located_by` names the card finding.
- **Data:** four ai-checked anchors have `located_by` "AI reader 2" and name no card finding:
  - cl_meth_pk_intranasal_timecourse anchor 5 (kirkpatrick_2012);
  - cl_meth_dopamine_damage anchor 4 (volkow_2001a);
  - cl_meth_grey_matter anchor 7 (london_2015);
  - cl_meth_psychosis_treatment anchor 2 (wearne_2018).

  Three other anchors follow the rule, for example "AI first reader (card sc_kirkpatrick_2012, key finding 3); anchor wording by AI reader 2". `validate.py` does not check this.
- **Which side changes:** METHODS decides, so the data and the validator change.
- **Proposed fix:**
  - For each of the four anchors, confirm the card records the finding, then write `located_by` as "AI first reader (card sc_…, key finding n); anchor wording by AI reader 2". Otherwise set the anchor back to `ai-located`.
  - Add to `validate.py`: fail any anchor whose `anchor_status` is ai-checked and whose `located_by` starts with "AI reader 2" without naming "card sc_".

### M9 · gap · The second-reading scripts use rules METHODS does not state
- **The protocol:** METHODS §5.5, `METHODS.md:191`. Anchors match when they are on the "same page or section" and the second reader recovered "at least 60% of the first reader's numbers".
- **What `reconcile_second_reader.py` adds:**
  - `:60` also matches an anchor at any place when at least 85% of its numbers agree and it has three or more numbers.
  - `:55–57` match anchors without numbers on at least 30% word overlap.
  - `:38` ignores whole numbers below 10.
  - `:32` and `:53` treat web anchors as being at the "same place" whenever their locators share any word of three or more letters, such as "Results".
  - `:91` upgrades an anchor only when reader 2 judged the claim supported or partly supported.
  - `:103–105` raise a claim to ai-anchored only from metadata-verified. That the ladder is cumulative is stated only in a code comment.
- **The mechanical number check:** `METHODS.md:192` says "every number written in a PDF anchor must appear". But:
  - `check_anchor_numbers.py:77–78` skips single digits.
  - `:65–66` skip numbers that follow "editors'".
  - `:50` only reads anchors marked `source_read` "PDF" (81 of 259).
  - `:192` sits after the targeted-check text and begins "Before that,", so the order of steps is unclear.
- **Proposed text:** replace the matching parenthesis in `METHODS.md:191` with:
  > "A script matches the two readers' anchors: same printed page (for web full texts, overlapping section words) and at least 60% of the first reader's numbers recovered, ignoring whole numbers below 10; or, wherever placed, at least 85% of three or more numbers; anchors without numbers match on the same place and 30% word overlap. A matched anchor becomes ai-checked only when the second reader judged the claim supported or partly supported. The ladder is cumulative: a claim reaches ai-anchored only from metadata-verified."

  Move `:192` into item 1 and reword it:
  > "Before the second reading, the first reader runs a mechanical check (scripts/check_anchor_numbers.py): every number of two or more digits in a PDF anchor, other than an editors' calculation, must appear, allowing for rounding, on the page the anchor names in a text extraction of the PDF."

### M10 · ambiguity · Anchors added by the editor carry the first reader's label
- **The protocol:** METHODS §6.2, `METHODS.md:216`: ai-located means "Found in the full text by the first AI reader".
- **Data:**
  - 64 anchors have a `located_by` value starting with "editor". Examples: "editor, from the study card or the PDF page text (review round 1)"; "editor, from the study card sc_stockings_2019 (key finding 3)".
  - `claim_patch.py:81` sets this as the default.
  - The site labels these anchors "located in the full text (AI reader 1)" (`app.views.js:82`).
  - 46 of them became ai-checked by targeted check. But §5.5 (`:191`) describes targeted checks only for anchors "the blind reading did not re-find". It says nothing about anchors added after the blind reading.
- **Practice has settled on:** editor-added anchors count as ai-located, and targeted checks cover them.
- **Proposed text:**
  - `METHODS.md:216` → `| ai-located | Located in the full text by an AI reader: the first reader, or the editor from the full text or from a key finding of the study card (located_by says which) |`
  - In `:191`, after "Anchors the blind reading did not re-find", insert "(and anchors the editor added after the blind reading)".
  - `app.views.js:82` → "located in the full text (AI)".

### M11 · gap · How to write locators, and what "page" means for web full texts, appear only in the briefs
- **The protocol:**
  - METHODS §4.5 (`METHODS.md:123`) and §6.2 (`:211`) say an anchor gives "the printed page" and a "locator (section, paragraph, table or figure)".
  - They give no rule for counting paragraphs, and none for full texts without printed pages.
- **The briefs:**
  - `VERIFICATION-BRIEF.md:88` and `STUDY-CARD-BRIEF.md:73` (each appended at the end) and `REVIEW-BRIEF-2.md:33–35` give the convention: count only running-text paragraphs, and use "PMC HTML" or "publisher HTML" as the page (`VERIFICATION-BRIEF.md:21`, `STUDY-CARD-BRIEF.md:35`).
  - ADJUDICATION-BRIEF does not carry it: its pointer at `:54` covers only "Where to read" and "Rules (hard)". REVIEW-BRIEF does not carry it either.
  - `claim.schema.json:94` still calls page "Printed page number(s)". `:98` shows a different locator format.
- **Data:**
  - Page values include "PMC HTML" 157 times, "publisher HTML" 15 times, and "registry record" once.
  - Nothing says how to count paragraphs in a PDF.
  - Practice counts running-text paragraphs. Example: the check note on cl_meth_psychosis_treatment anchor 2 says "the Figure 1 legend is not counted".
  - Anchors written on 15 October, before the convention was added, may count paragraphs differently. That matters when the senior author checks them in the review queue.
- **Proposed text:** a new paragraph in METHODS §6.2:
  > "Locators. For a PDF, page is the printed page (online-first PDFs: the article's own page numbers). For a web full text without print pagination, page is 'PMC HTML' or 'publisher HTML'; for a registry record, 'registry record'. The locator gives the section path as printed (Results › Sample, 2nd paragraph) or the table or figure with its row or column. Paragraphs are running-text paragraphs within the named section or subsection: headings, captions, figure legends, footnotes and boxed key points are not counted; a paragraph continued from the previous page counts on the page where it starts."

  Bring `claim.schema.json:94` and `:98` into line with it.

---

## B. Sources, search and access

### M12 · contradiction · Which full texts the AI may read
- **The protocol and schemas:**
  - METHODS §5.5, `METHODS.md:190`: "the PDF in the project folder, or the PubMed Central full text".
  - §12.1, `:354`: "PDFs … and PubMed Central full texts read through the browser".
  - The changelog, 0.2.0 (3), `:417`, says the same.
  - `claim.schema.json:143` and `study-card.schema.json:476` list only PDF or PMC.
- **Workflow, briefs and site:**
  - `WORKFLOW.md:13` and `:34–35`.
  - `STUDY-CARD-BRIEF.md:12` ("free at the publisher") and `:31` ("Publisher full text (HTML)").
  - `VERIFICATION-BRIEF.md:70`.
  - About page, `index.template.html:321` and `:330` ("free publisher pages").
  - Planned pages, `app.views.js:17`: "nothing is written until the PDFs have been read in full".
- **Data:**
  - Three cards were read on publishers' sites: sc_mcketin_2013 (JAMA Network), sc_arunogiri_2018 (SAGE) and sc_leung_2023 (Wiley).
  - 15 anchors have page "publisher HTML".
  - cl_meth_naltrexone_bupropion anchor 5 was read from ClinicalTrials.gov NCT03078075 while it cites trivedi_2021.
- **Which side changes:** METHODS. Practice and every brief agree, and §3.2 accepts any full text the editors obtain.
- **Proposed text:**
  - §5.5 (1) → "…from the full text: the PDF in the project folder, or a free full text read in the app's browser (PubMed Central, or the publisher's own HTML article), anchoring every number to a page or, for web full texts, a locator (§6.2). A trial-registry record may be read to check registration and outcomes; the anchor then says so in its page and locator."
  - §12.1 → "reads full texts (the PDFs in the project folder, and free full texts in PubMed Central or on publishers' pages, read through the app's browser)".
  - Schemas: add "publisher full text (HTML), <journal or URL>" and "ClinicalTrials.gov record <id>".
  - `app.views.js:17` → "nothing is written until the papers have been read in full".

### M13 · contradiction · Who runs the PubMed search
- **Senior author:**
  - METHODS §2.1, `METHODS.md:53`: "run by the senior author".
  - §16, `:385`: "PubMed and PsycInfo searches are run by the senior author".
  - `search-logs/methamphetamine_search-log.md:9`: "PubMed (to be run by VS)".
  - `EVIDENCE-MAP-BRIEF.md:23`.
- **The AI:**
  - `WORKFLOW.md:8`: "AI … runs them: PubMed through the E-utilities interface". `:34` adds that E-utilities is reachable.
  - About page, `index.template.html:330`: "Writes and runs the searches (PubMed, Crossref, OpenAlex)".
- **Data:** the monograph's last-search date reads "Crossref layer only; PubMed, Cochrane and citation searches not yet run". Nobody has run PubMed yet.
- **Which side changes:** METHODS decides as written, and the search logs follow it, so WORKFLOW and the About page should change. If the senior author now wants the AI to run PubMed through E-utilities, then §2.1 and §16 change instead.
- **Proposed text, if METHODS stands:**
  - `WORKFLOW.md:8` → "Writes the search strings (METHODS §2.2) and runs the Crossref and OpenAlex layers; writes the PubMed strings for VS to run; screens titles and abstracts; snowballs; builds the evidence map".
  - `index.template.html:330` → "Writes the searches and runs the Crossref and OpenAlex layers (the senior author runs PubMed)".
- **Proposed text, if METHODS changes:**
  - §2.1 row → "PubMed/MEDLINE | primary bibliographic search, run by the AI through the E-utilities interface or by the senior author; results exported into search-logs/".
  - §16 → "PsycInfo searches are run by the senior author for result counts."

### M14 · gap · METHODS says nothing about WebFetch, and the other documents disagree about it
- **The protocol:** METHODS is silent. §4.2 (`:111`) says "fetched from Crossref by DOI". §12.1 mentions only the browser.
- **The other documents:**
  - `WORKFLOW.md:41–45` and `STATUS.md:91–92`: never used to read papers; "short metadata lookups"; each transcription "compared with a second fetch or the browser before use".
  - `WORKFLOW.md:58–60`: a DOI copied from a works-search record "counts as verified".
  - `build_references.py:6` and `:108`: two agreeing WebFetch transcriptions become metadata-verified, with `metadata_source` "crossref (two agreeing WebFetch transcriptions)". `reference.schema.json:158–163` would reject that value.
  - `EVIDENCE-MAP-BRIEF.md:9–12` makes WebFetch the route to Crossref, and `:43` says DOIs from search results are "already verified".
- **Practice goes beyond metadata lookups:**
  - The Greek numbers on the Emergency page were read through WebFetch (`protocol-and-site.json`: moh-gr_166, moh-gr_poison, kyriakou_contact and visitgreece_health).
  - So was the Greek legal row (`data/legal/methamphetamine.json`, the Greece note).
  - WebFetch was also used to read UNODC figures. Only one ratio could be read that way (`STATUS.md:77–79`).
- **Proposed text:** a new paragraph in METHODS §12.1:
  > "WebFetch (a fetch tool that answers through a summarizing model) is never used to read papers for study cards or anchors. It may be used (a) for bibliographic metadata, which becomes metadata-verified only when two independent fetches (works/<DOI> and a works search) agree on every field, or one agrees with a browser record; (b) for short official facts on public pages (emergency numbers, scheduling entries), each confirmed in at least two sources, recorded as read through WebFetch, and kept at draft until the senior author's check. A retraction status is set only from a works/<DOI> record or a search that returns update links."

  Also add the WebFetch value, or a separate field, to `metadata_source` in `reference.schema.json`.

### M15 · outdated · EVIDENCE-MAP-BRIEF contradicts what WORKFLOW later learned
- **The conflicts:**
  - `EVIDENCE-MAP-BRIEF.md:10` uses `&sort=relevance`, which "makes requests fail" (`WORKFLOW.md:47`).
  - `:12` sets "one Crossref request every 2 seconds". WORKFLOW says 90–130 seconds, 150–300 seconds after a refusal, and one Crossref agent at a time (`WORKFLOW.md:48–49`, `:64–65`).
  - `:14` says "PubMed, Europe PMC and OpenAlex are NOT reachable". WORKFLOW says OpenAlex works through WebFetch (`:34`, `:66`).
  - `:20` says "Verify EVERY DOI … works/<DOI>", but `:43` says DOIs taken from search results need no fetch. Meanwhile `WORKFLOW.md:59–61` and METHODS §4.3 (`:114`) require a retraction check for every item. Only works/<DOI>, or a search with `updated-by`, provides one.
- **Proposed text:**
  - Replace "Sources you can use" with: "Follow docs/WORKFLOW.md, 'What the AI can and cannot reach', for endpoints, URL limits and pacing: no &sort=relevance; 90–130 s between Crossref calls; one Crossref agent at a time. OpenAlex is reachable through WebFetch."
  - Replace the first sentence of step 4, and item 3 of "Working economically", with: "Every DOI in the list must come from a Crossref record (a works/<DOI> fetch, or verbatim from a search fetched with select=…,updated-by) and carry its update links; a DOI taken from a search without updated-by needs a works/<DOI> check for retractions and corrections."

---

## C. Claims, GRADE and status flags

### M16 · contradiction · A claim resting only on narrative reviews appears in the at-a-glance box
- **The protocol:**
  - METHODS §6.3, `METHODS.md:248`: such claims "are never shown in the at-a-glance box".
  - §8 row 1, `:282`, applies the exclusion only to the best-established facts. The mechanism line rests "on a section 3 claim".
  - The comment at `validate.py:99` states the broad rule, but the check at `:111–116` covers only `best_established`.
- **Data:**
  - `largest_uncertainties` includes cl_meth_psychosis_course. That claim is draft, and its 9 anchors all cite three narrative reviews: glasner-edwards_2014, wearne_2018 and bramness_2012. Its plain text does say "Reviews quoting…".
  - The mechanism line rests on cl_meth_mechanism_release, the only section-3 mechanism claim. It is draft and rests on one narrative review (kish_2008). The line in the box does not say the evidence is second-hand.
- **Which side changes:** METHODS contradicts itself here. Keep §6.3 as written and change the data:
  - Replace cl_meth_psychosis_course with a very-low-certainty claim that does not rest only on reviews, such as cl_meth_dat_recovery, cl_meth_grey_matter or cl_meth_cognition_abstinence.
  - Extend `validate.py:111–116` to `largest_uncertainties`.
  - §8 row 1 needs a sentence for the mechanism line.
- **Proposed text:** in `METHODS.md:282`, after "(resting on a section 3 claim)", add: "; if the only such claim rests on narrative reviews, the line says that the mechanism is described second-hand and the claim is not otherwise shown in the box".

### M17 · ambiguity · Can one meta-analysis make a claim "replicated"?
- **The protocol:**
  - METHODS §6.4, `METHODS.md:251`: "at least two independent studies with consistent direction".
  - §6.3, `:243`: overlapping evidence is not independent replication.
  - The reviewers are asked to check this at `REVIEW-BRIEF.md:47–49` and `REVIEW-BRIEF-2.md:60–62`.
- **Data:**
  - These claims are "replicated" although each rests on one meta-analysis: cl_meth_psychosis_association (adjusted estimate from 4 studies), cl_meth_suicidality (4 studies) and cl_meth_mortality (23 cohorts).
  - cl_meth_depression rests on two overlapping meta-analyses and is also "replicated".
- **Practice counts:** the independent primary studies pooled inside a review. A reviewer counting the claim's independent sources would find one, and so call it "single study".
- **Proposed text:** `METHODS.md:251` → "replicated: at least two independent studies with consistent direction, counted among the primary studies, including those pooled in a meta-analysis when the review reports their direction; reviews that share primary studies count once (§6.3)."

### M18 · ambiguity · Starting level for non-randomized experiments, and for evidence seen only through reviews
- **The protocol:**
  - METHODS §6.3, `METHODS.md:225`: "randomized evidence starts high; observational evidence starts low".
  - `claim.schema.json:179` says the same.
- **Data:**
  - cl_meth_acute_lab and cl_meth_pk_intranasal_timecourse start high. In one study the dose order was "randomized", in the other "counterbalanced".
  - cl_meth_pk_halflife starts high because "Controlled pharmacokinetic studies would start high". That evidence was seen only in a narrative review.
  - cl_meth_psychosis_treatment starts high from trials seen only through narrative reviews.
- **Practice has settled on:**
  - Start from the design of the underlying primary studies.
  - Treat placebo-controlled within-person studies with counterbalanced order as randomized.
- **Proposed text:** add after `:225`, for the senior author to confirm:
  > "Placebo-controlled within-person laboratory studies start high when condition order was randomized or counterbalanced; the risk-of-bias domain records which. A claim seen only through reviews starts from the design of the primary studies the review describes and is downgraded for risk of bias (not appraisable) and indirectness (second-hand)."

### M19 · contradiction · The verbs in the claim form, and the relations in the schema
- **The protocol:**
  - METHODS §6.1, `METHODS.md:206`, offers three verbs: "is associated with / causes / does not detectably change".
  - Its status list is "[replicated / single study / contested / mixed]", without "replicated by the same team".
- **The schema and validator:**
  - `claim.schema.json:55–63` allows six relations, adding `reduces`, `increases` and `insufficient-evidence`.
  - `validate.py:86` warns about causal language only for `causes`.
  - The glossary entry "Is associated with / causes" adds "randomization, or strong within-person or sibling designs".
- **Data:**

  | Relation | Uses |
  |---|---|
  | is-associated-with | 23 |
  | increases | 5 |
  | insufficient-evidence | 5, plus 2 in staged claims |
  | reduces | 1, in a staged claim |
  | does-not-detectably-change | 0 |

- **"increases" carries two meanings:**
  - causal, in an RCT (cl_meth_naltrexone_bupropion) and in laboratory claims;
  - descriptive, in cl_meth_us_trends, a time trend rated low.
- **Proposed text:** METHODS §6.1, the verbs →
  > "[is associated with / increases / reduces / causes / does not detectably change / evidence is insufficient to say whether … changes]",

  and add:
  > "'Increases', 'reduces' and 'causes' are causal and follow the rule below. Descriptive claims (§6.3: prevalence, base rates, trends, standardized mortality) take the relation 'describes'. 'Insufficient evidence' is used when neither an effect nor its absence can be shown with precision."

  Then:
  - Add `describes` to the schema enum. Recode cl_meth_us_trends, cl_meth_mortality and cl_meth_dependence_baserate.
  - Status list → "[replicated / replicated by the same team / single study / contested / mixed]".
  - Extend `validate.py:86` to `increases` and `reduces`.

### M20 · wording · How the site words the GRADE upgrade rules
- **Two mismatches:**
  - `index.template.html:264`: when evidence rated down for bias is also rated up, "the claim says so and gives the stricter rating". That reads as if the claim takes the stricter rating. METHODS §6.3 (`:247`) says only that the reasoning "gives the certainty a strict reading would give". Practice follows METHODS: cl_meth_psychosis_dose, the live example on How-to, is rated low and says "without it certainty would be very low".
  - The same line leaves mortality ratios out of "never for a prevalence, a count or a trend". METHODS `:246` includes standardized mortality. The glossary entry "Certainty (GRADE)" also omits the third reason for upgrading and the observational-only restriction.
- **Proposed text:**
  - `:264` → "When evidence already rated down for bias is also rated up, the claim says so and states the lower rating a strict reading would give. … and never for a prevalence, a count, a mortality ratio or a trend over time."
  - Glossary → "…moved down for risk of bias, inconsistency, indirectness, imprecision or publication bias, and, for observational evidence only, up for a large effect, a dose–response gradient, or confounding that would have reduced the effect."

### M21 · contradiction · "Never primary evidence" against claims that rest only on narrative reviews
- **"Never":**
  - METHODS §5.3, `METHODS.md:168`: "never as primary evidence".
  - Site Methods, `index.template.html:251`: "never primary evidence for a claim".
  - Glossary "Narrative review": "never the primary evidence for a claim".
- **Allowed and present:**
  - METHODS §6.3 (`:248`) provides for claims that rest only on narrative reviews, held at draft.
  - The page shows six such claims: cl_meth_pk_halflife, cl_meth_mechanism_release, cl_meth_acute_toxicity, cl_meth_psychosis_treatment, cl_meth_psychosis_course and cl_meth_psychosis_vs_schizophrenia.
  - The About page (`index.template.html:323`) says "five". The mechanism claim added in 0.3.0 is the sixth.
- **Proposed text:**
  - `METHODS.md:168`, end of the row → "…and the review is cited for arguments and pointers; a claim whose only support is narrative reviews stays at draft and says its figures are second-hand (§6.3)".
  - `index.template.html:251` → "…never the sole support of a claim above draft".
  - Glossary → "…on this site a claim that rests only on narrative reviews stays in draft and says that its figures are second-hand."
  - `:323` → "six claims that rest only on narrative reviews".

### M22 · wording · §7 calls the editors' reading the "only" editorial judgment, but §8 adds others
- **Sides:**
  - `METHODS.md:271`: the editors' reading is "the only place on the page where an editorial judgment appears".
  - §8 row 1 (`:282`): the uncertainties are "chosen by the editors", and ties are decided by relevance.
  - §8 row 15 (`:296`): "The editors' priority questions".
  - The site labels both as the editors' choices (`app.views.js:179`, `:211–212`).
- **Proposed text:** `:271` → "The editors' reading is the only place where the editors give their own answer to a contested question, and it is labelled as such; other editorial selections (the at-a-glance uncertainties, the priority research questions) are labelled as the editors' choice."

---

## D. Risk of bias

### M23 · contradiction · Public text stretches two rules of §5.3
- **The two cases:**
  - Home page pipeline, `index.template.html:66`: "AMSTAR 2 for reviews". METHODS §5.3 assigns AMSTAR 2 only to systematic reviews and meta-analyses (`:164`); narrative reviews use the editors' checklist (`:168`).
  - Site Methods, `index.template.html:253`, says of every instrument that "the overall judgment is never milder than the worst domain". METHODS `:184` applies that only to RoB 2, ROBINS-E, ROBINS-I and the narrative checklist. AMSTAR 2 and JBI overall ratings are not built that way: sc_arunogiri_2018 is low-confidence with three items judged "no".
- **Proposed text:**
  - `:66` → "RoB 2 for trials, ROBINS-E for exposure studies, AMSTAR 2 for systematic reviews, the editors' checklist for narrative reviews."
  - `:253` → "…and for the tools that build an overall judgment from domains (RoB 2, ROBINS-E, ROBINS-I and the narrative-review checklist), the overall judgment is never milder than the worst domain."

### M24 · contradiction · STUDY-CARD-BRIEF leaves out the vocabularies of §5.3
- **The brief:** `STUDY-CARD-BRIEF.md:54`:
  - tells readers to judge each AMSTAR 2 item "yes / partial-yes / no";
  - gives no vocabulary for RoB 2, SYRCLE, QUADAS-2 or JBI;
  - never mentions ROBINS-I (METHODS `:163`).
- **The protocol:** METHODS §5.3 (`:176–184`):
  - allows "partial yes" only for items 2, 4, 7, 8 and 9;
  - allows "no meta-analysis" only for items 11, 12 and 15;
  - allows "no information" (with a provisional rating) as an extension;
  - gives JBI yes / no / unclear / not applicable, plus "partial yes" with its reason.
- **Data:** sc_stockings_2019, written by a reading agent from this brief, judges items 5, 6, 11 and 13 "partial yes". These are the four validator warnings (`STATUS.md:62`).
- **Proposed text:** replace the AMSTAR 2 part of `:54`, and add the other instruments:
  > "AMSTAR 2 (systematic reviews and meta-analyses): judge each of the 16 items yes or no; 'partial-yes' only for items 2, 4, 7, 8 and 9; 'no-meta-analysis' only for items 11, 12 and 15; 'no-information' only when the item can be judged only from a supplement you have not read, and then write 'provisional' in the overall rating's reasoning; overall high-confidence / moderate-confidence / low-confidence / critically-low, from the critical items. RoB 2 (randomized trials, including randomized crossover laboratory studies): low / some-concerns / high. ROBINS-I (non-randomized studies of interventions): low / moderate / serious / critical / no-information. SYRCLE (animal studies) and QUADAS-2: low / high / unclear. JBI prevalence checklist: yes / no / unclear / not-applicable per item, 'partial-yes' with the reason in the note; overall low / moderate / high as the editors' summary."

### M25 · gap · Some designs have no instrument, and `none-applicable` is used for two different checklists
- **No instrument for some designs:**
  - METHODS §5.3 (`:158–168`) has no row for qualitative studies, case series or case reports, modelling, registry or in-vitro studies.
  - Yet §3.1 (`:89`) admits qualitative and case-series designs, and `study-card.schema.json:35–55` allows all of them.
- **One label, two checklists:**
  - `study-card.schema.json:336` and `rob_vocab.py:38` define `none-applicable` as the narrative-review checklist (low / some-concerns / high).
  - sc_harding_2022 is qualitative. It uses `none-applicable` with eight different domains: design, sampling, data collection, researcher relationship, ethics, rigour, findings and transferability. It is held to the narrative checklist's vocabulary, and the site shows it as the "editors' narrative-review checklist" (`app.views.js:405`).
- **The mismatch check is narrower than METHODS says:**
  - METHODS `:184` says `rob_vocab.py` "reports any mismatch".
  - `rob_vocab.py:74–86` checks only reviews. An RCT, animal or prevalence card using the wrong tool passes.
  - `validate.py:100` and `rob_vocab.py:75` test for "commentary" and "editorial" designs, which the card schema does not allow.
- **Proposed text, for the senior author to decide:**
  - New §5.3 rows:
    - `| Qualitative studies | The editors' qualitative checklist (design, sampling, data collection, researcher relationship, ethics, rigour of analysis, grounding of findings, transferability), stored as instrument "editors-qualitative", low · some concerns · high |`
    - `| Case series, case reports, modelling | No instrument; the card states the design's limits |`
  - `:184` → "…`scripts/rob_vocab.py` reports a mismatch for every design with a listed instrument". Then extend `DESIGN_INSTRUMENT` in `rob_vocab.py:74–77`: rct and crossover-rct → RoB 2; preclinical-animal → SYRCLE; survey → JBI-prevalence; qualitative → editors-qualitative.

### M26 · gap · An AMSTAR 2 "no information" item does not mark the rating provisional
- **The rule:** METHODS §5.3, `:184`: when an item is "no information", "the overall confidence rating is then marked provisional". `rob_vocab.py:10–11` repeats the rule.
- **Data:**
  - sc_basterfield_2019 (low-confidence) and sc_cao_2026 (moderate-confidence) each record item 7, a critical item (the list of excluded studies), as no-information because the supplement was not read.
  - Neither card marks its rating provisional.
  - The site prints, for example, "OVERALL: MODERATE CONFIDENCE" (`app.views.js:405`).
  - `STATUS.md:67` lists the two supplements as pending.
  - Nothing checks this.
- **Proposed fix:**
  - Begin each card's `risk_of_bias.reasoning` with "Provisional: item 7 depends on an unread supplement." Log it as an editorial correction.
  - `validate.py`: warn when an AMSTAR 2 card has a no-information item and its reasoning lacks "provisional".

---

## E. Quotations and language

### M27 · contradiction · The Numbers page shows long verbatim passages from its sources
- **The rule:**
  - METHODS §4.5, `:123–125`: the site "does not reproduce passages", and a quotation is at most 15 words.
  - How-to, `index.template.html:185`: "We do not copy passages".
  - §10 makes no exception for statistics.
- **What the site does:**
  - The Numbers lede (`index.template.html:113`) promises the sentence or table row behind each figure. It is shown on hover (`app.views.js:259`, from `page_or_table`).
  - In `data/epidemiology/*.json`, `page_or_table` holds 265 quoted segments. 115 of them run past 15 words; the longest has 58. One example: ep_eu_cannabis_lastyear_15_64_2024, 35 words.
- **Why it isn't caught:**
  - `validate.py:48–52` checks only the `quote` field of claim anchors.
  - `check_card.py` checks only cards, and only at merge.
- **Related:** `claim.schema.json:106` caps a quotation at 140 characters. METHODS does not state that limit, and a 15-word quotation made of long technical words can exceed it.
- **Which side changes:** §4.5 decides as written, so the hover text should be cut to 15 words or fewer. If the senior author wants full sentences there, §10 needs an exception.
- **Proposed text for the exception:** a new bullet in §10.2:
  > "The sentence or table row a figure was checked against may be shown verbatim, in quotation marks, when the source is a public statistical or monitoring publication (EUDA, UNODC, WHO, NSDUH); the 15-word limit of §4.5 applies to every other source."

  Either way, add "(at most 140 characters)" to §4.5, or drop `maxLength` from the schema.

### M28 · gap · §9 does not state the "users" rule that the briefs and scripts enforce
- **The protocol:** METHODS §9, `:304`, lists "addicts", "abusers", "abuse" and "junkies". It says nothing about "user(s)".
- **The briefs and scripts:**
  - `STUDY-CARD-BRIEF.md:65` says not "users" or "non-users".
  - `validate.py:84–85` and `check_card.py:23` and `:53–55` warn on these words, citing §9.
  - `STATUS.md:25–26` and `:40–41` report 364 replacements logged as "Language (METHODS §9)".
  - `validate.py:79` also flags "clean urine" and "dirty urine", which §9 does not mention.
  - The brief leaves out §9's exception for institutional names, such as the National Institute on Drug Abuse.
- **Proposed text:** add to the first bullet of §9:
  > "'People who use [substance]' or, beside a control group, 'the [substance] group', rather than 'users' or 'non-users', except in quoted titles and in official indicator names; 'positive' or 'negative' urine results rather than 'dirty' or 'clean'."

### M29 · gap · The language check misses most reader-facing text, and public pages use "users"
- **What is claimed and what is checked:**
  - `STATUS.md:26` says the validator warns on "user(s)" in "any reader-facing field".
  - `validate.py:75–76` actually checks only the statement, plain text, magnitude, the PECO fields and the debate box.
- **"users" still appears in:**
  - 70 anchor `extracted` texts across 15 claims (shown under "Evidence anchors");
  - 10 locators that quote source headings;
  - the GRADE reasoning of 6 claims, shown under "Why this rating": cl_meth_pk_intranasal_timecourse, cl_meth_dat_lower, cl_meth_dopamine_damage, cl_meth_acute_lab, cl_meth_dependence_baserate and cl_meth_cognition_normal_range.
- **Public site text uses it too:**
  - `app.views.js:54`: "Past-year users worldwide in 2023".
  - `data/site/landing-stats.json`: five figures measured as "past-year users, 2023".
  - `data/site/glossary.json:142`, the cross-sectional study entry: "Measures users and non-users".
  - Labels on the Numbers page, for example ep_eu_highrisk_opioid_users_2024: "…high-risk opioid users".
- **Proposed fix:**
  - Apply the §9 checks in `validate.py` to every string in claims, including `evidence[].extracted`, `grade.reasoning` and debates. Also cover cards (outside titles and logs), monographs, `data/site/*.json` and figure labels. Exempt locators that quote a source heading.
  - Until then, `STATUS.md:26` → "…warns on 'user(s)' in claim statements, plain text, PECO fields and debate boxes; anchors, reasoning and site tables are not yet checked".
  - Site → "People who used a drug in the past year, worldwide, 2023".

### M30 · outdated · STUDY-CARD-BRIEF points to old copies of its model cards
- **The brief:** `STUDY-CARD-BRIEF.md:8` points to `data/study-cards/_merged/methamphetamine/sc_volkow_2001a.json` and `sc_mcketin_2019.json`.
- **Why that is wrong:**
  - `merge_cards.py:4–6` keeps in `_merged` the incoming file as it was at merge, not the current card.
  - The `_merged` sc_volkow_2001a differs from the current card in 35 fields.
  - It also uses "users" 27 times, against the brief's own `:65`.
- **Proposed text:** `:8` → "The model cards are sc_volkow_2001a (PDF-read cross-sectional study) and sc_mcketin_2019 (PMC-read meta-analysis) in data/study-cards/methamphetamine.json, in their current versions; do not copy from _merged/, which holds superseded copies."

---

## F. Public site text

### M31 · gap · No conflicts of interest or AI statement on the monograph page or the About page
- **What METHODS promises:**
  - §8 row 0 (`:281`): the header includes conflicts of interest.
  - §14 (`:369`): declared "on the About page and on each monograph they author".
  - §12.1 (`:354`): the AI's role is stated "on the About page and on every monograph".
  - The site Methods page also says "All editors declare conflicts of interest" (`index.template.html:288`).
- **What the site shows:**
  - The monograph header (`app.views.js:207`) shows author names only. Yet `data/monographs/methamphetamine.json` holds each author's role and conflict of interest ("To be declared" for the senior author; "None" for the AI).
  - There is no AI statement on the monograph page.
  - The About page (`index.template.html:311–338`) has no conflict-of-interest declaration.
  - The donation threshold mentioned in §14 is stated nowhere.
- **Proposed fix:**
  - In `app.views.js:207`, after Authors, generate from `authors[].coi` and `role`: "Conflicts of interest: Vasilis Sampalis, MSc — to be declared; Claude (Anthropic) — none" and "AI assistance: first-pass extraction, appraisal and drafting by Claude, under the senior author's review (Methods §12.1)".
  - About page: add an "Interests" heading with each editor's declaration and "Donations: none accepted yet; the disclosure threshold will be stated here before any are."

### M32 · contradiction · The site overstates how references were verified
- **The site's claims:**
  - How-to (`index.template.html:183`): "Every reference's details were pulled from Crossref and checked for retractions".
  - About (`:319`) says the same.
  - `app.views.js:63`: "53 references with Crossref-verified metadata".
  - The pop-up (`app.views.js:340`) prints "Crossref <date>" for any record that has a `verified_on` date.
- **Data:**
  - 46 of the 53 records come from Crossref.
  - 7 do not: the five Emergency-page web pages (europa_112, moh-gr_166, moh-gr_poison, kyriakou_contact, visitgreece_health), plus unodc_2025 and euda_2026. Their `metadata_source` is "publisher" and their `retraction_check` is "not-checked".
  - That is correct under METHODS §4.2 (`:111`), which has sources without a DOI checked against the publisher's page.
- **Which side changes:** §4.2 decides, so the site text changes.
- **Proposed text:**
  - `:183` and `:319` → "Every journal article's details were pulled from Crossref and checked for retractions on the date shown; reports and web pages were checked against the publisher's page."
  - `app.views.js:63`: count only records whose `metadata_source` is crossref.
  - `app.views.js:340`: print the metadata source, as the reference list already does at `:240`.

### M33 · contradiction · Four cards written from abstracts are labelled "from the full text"
- **The rule:**
  - METHODS §5.5: first-pass means written from the full text (`:190`), and "a card written from an abstract alone cannot leave draft" (`:195`).
  - `check_card.py:67–71` enforces this, but only at merge (`merge_cards.py:27`).
  - `validate.py` never runs it on the merged file.
- **Data:**
  - sc_ersche_2012, sc_callaghan_2012, sc_anthony_1994 and sc_cruickshank_2009 are first-pass.
  - None has a `source_read` or key findings, and each holds 3–7 "[to be extracted from PDF]" placeholders.
  - They were written on 2026-10-14, when the claims citing them were "Draft from abstracts".
  - The study-card panel labels them "first pass: one AI reader, from the full text" (`app.views.js:412`).
  - Their claims are draft, so no claim status is affected.
- **Proposed fix:**
  - Set each card's `verification.status` to "draft" and its `source_read` to "abstract only (prototype, 2026-10-14)".
  - In `validate.py`, run `check_card.check()` on every card in `data/study-cards/*.json`. Make placeholders, quotations, a missing `source_read` and the abstract rule hard failures for any card that is not draft.

### M34 · outdated · Version labels and progress counters on the site
- **Version labels:**
  - The top bar says "prototype v0.3" (`index.template.html:11`). The footer says "prototype v0.3.1" (`:343`; it read v0.3.0 when this audit began).
  - The monograph is v0.3.1. `STATUS.md:24` says "Monograph v0.3.0, site version 14".
  - The substance index badge is hard-coded "draft v0.1" (`app.views.js:77`).
  - Error reports record `page_version` "prototype 0.2.0" (`app.views.js:448`).
- **Progress counter:** "Where the project stands" shows "36 / 30 evidence maps built" (`app.views.js:59` and `:63`). The 36 counts 30 substance maps plus 6 cross-cutting ones.
- **Error-report form:** How-to (`:204`) says "Every page will carry an error-report form". It already does: the footer button (`:345`) and per-claim buttons store reports (`app.views.js:445–461`).
- **Proposed fix:**
  - One constant, `SITE_VERSION`, used for the top bar, the footer and `page_version`.
  - The badge reads "draft v" plus the monograph's own version.
  - Counter → "30 / 30 substance evidence maps built, plus 6 cross-cutting maps".
  - `:204` → "Every page carries an error-report form ('Report an error' at the foot of the page and on each claim) that asks for a DOI, PMID or page reference."

### M35 · wording · What an error report requires
- **Sides:**
  - METHODS §13 (`:363`) and the site Methods page (`index.template.html:285`): "a DOI or a page reference".
  - METHODS §15 (`:377`) and the form itself (`index.template.html:351`, `:355`): "a DOI, PMID or page reference".
- **Proposed text:** `METHODS.md:363` and `index.template.html:285` → "…requires a DOI, PMID or page reference".

---

## G. Scripts and validation

### M36 · gap · §11's list of validation checks no longer matches `validate.py`, and "publish" can be read two ways
- **METHODS §11** (`:332`) lists these checks: schemas; anchors and placeholders; quotations; "every reference metadata-verified and retraction-checked"; citations; and "publication is blocked while any anchor is below senior-verified".
- **What `validate.py` actually does:**
  - Unverified or unchecked references only produce warnings (`:126–130`).
  - The publication block is a printed count (`:139`). The script exits with 0 and has no publish mode.
  - Quotations are checked only in claim anchors (`:48–52`).
- **What it checks that §11 does not list:**
  - GRADE arithmetic (`:54–63`);
  - the ladder (`:64–73`);
  - language and raw claim ids (`:74–87`);
  - risk-of-bias vocabulary, plus AMSTAR 2 items and design matches as warnings (`:88–98`);
  - narrative-only claims and the best-established list (`:99–116`);
  - sections (`:120–125`);
  - key findings without pages (`:135–137`);
  - a contested claim without a debate box (`:53`).
- **"Publish":** `WORKFLOW.md:90` publishes the prototype with the Artifact tool after every build. A reader of §11 could take that as forbidden.
- **Proposed text:** last bullet of §11 →
  > "Validation (scripts/validate.py) runs before every build. It fails on: schema errors; a claim without anchors; a located anchor with a placeholder; a quotation over 15 words or a second quotation in a claim; an unknown reference or study card; GRADE arithmetic; a claim above its rung on the ladder (§12); a contested claim without a debate box; a narrative-only claim above draft or among the best-established facts; risk-of-bias words outside the instrument's vocabulary; a retracted reference. It warns on: unverified or retraction-unchecked references, language (§9), AMSTAR 2 items and design–instrument mismatches, section mismatches, key findings without a page, and every anchor not yet senior-verified. The prototype is deployed with draft content labelled as such; a monograph cannot reach 'published' (§12) while any reference warning or any anchor below senior-verified remains."

### M37 · gap · Rules in METHODS that could be checked mechanically but are not
These need additions to `validate.py`. The METHODS text is already in M36.
- (a) **Section 7 is the senior author's only** (§1.2, §8 row 7, `:288`). Nothing fails an AI-drafted claim in section 7. `claim.schema.json` allows section 7, and `monograph.schema.json:189–192` sets `senior_author_only` to false by default.
- (b) **The at-a-glance rule** (`:282`): three best-established facts, ordered by certainty and then replication; uncertainties that are very low or contested. Not checked; the current data comply.
- (c) **Descriptive claims are never upgraded for large effect** (`:246`). No field marks a claim as descriptive. With the `describes` relation proposed in M19, the validator could fail any such claim with `large_effect` above 0.
- (d) **An upgrade on evidence already downgraded for risk of bias must state the strict reading** (`:247`). Warn when `risk_of_bias.levels` is above 0, an upgrade is above 0, and the reasoning does not give the certainty without the upgrade. cl_meth_psychosis_dose complies.
- (e) **A preclinical finding never raises a human claim above low** (§5.4, `:188`). Fail when every supporting card is preclinical-animal or in-vitro and certainty is above low. Separately, `study-card.schema.json:399–401` calls the preclinical block "Required" but does not enforce it.
- (f) **JBI "partial yes" carries its reason** (`:184`). Warn when the note is empty. The current data comply.

### M38 · gap · A senior decision is not tied to the claim version it was made on
- **The rule:** METHODS §5.5 (`:193`): "a decision taken on an earlier version of a claim does not carry over to a changed claim".
- **Where it holds:** the site enforces it (`app.views.js:483–485`), and `apply_senior_review.py:46–48` skips stale decisions.
- **Where it breaks:**
  - The script stores `senior_review` without the claim version (`:49`), and the schema has no field for it (`claim.schema.json:348–369`).
  - `claim_patch.py:87–91` steps a claim down only when a new anchor is unchecked. A senior-reviewed claim edited later would keep its status and its old approval.
  - `validate.py:72–73` accepts any approval.
- **Proposed fix:**
  - Add `senior_review.claim_version` to the schema, and set it at `apply_senior_review.py:49`.
  - `claim_patch.py`: "a claim at anchor-verified or above whose statement, plain, magnitude, grade or evidence changes returns to the rung its anchors support and its senior_review becomes pending".
  - `validate.py`: fail a claim that is senior-reviewed or published when `senior_review.claim_version` differs from its version.

### M39 · contradiction · Checking metadata against the PDF, PMIDs, and who verified
- **The protocol:**
  - METHODS §4.2 (`:111`): "Author names are compared against the PDF's first page before the record is marked verified".
  - §4.1 (`:108`): records store "PMID/PMCID where they exist" and "who verified it".
- **The schema and script:**
  - `reference.schema.json:150–154` makes "pdf-checked" (authors, year and title compared against the PDF by a human) a separate status above metadata-verified.
  - `build_references.py:108` marks records metadata-verified straight from Crossref.
- **Data:**
  - No record is pdf-checked.
  - 23 of the 39 study references in `methamphetamine.json` have a PDF on file. The other 16 were read on the web.
  - No record has a PMID.
  - 14 records have no `verified_by`: all of `protocol-and-site.json` and `reports.json`.
- **Which side changes:** this is the senior author's call. If §4.2 stands, no reference is verified yet, and none of the 24 claims above draft could stay there. The schema's two-step design is what the ladder has relied on.
- **Proposed text, if the schema's design is adopted:**
  - §4.2 → "…Records fetched from Crossref are stored as metadata-verified. Where a PDF is on file, the senior author compares authors, year and title with its first page and the record becomes pdf-checked; for full texts read on the web the comparison is made against the article page. Sources without a DOI…"
  - §4.1 → "PMCID where it exists (PMID when added)". Otherwise, add PMIDs through the PMC ID converter.
  - Fill in `verified_by` on the 14 records.

### M40 · contradiction · Version numbers before publication
- **The protocol:** METHODS §13 (`:360`): a version goes up "major when a conclusion or certainty rating changes; minor when evidence is added…; patch for wording".
- **The script:** `claim_patch.py:12` makes a rating change "minor", and `:92–94` allow only patch or minor bumps.
- **Data:**
  - cl_meth_psychosis_dose and cl_meth_us_trends dropped from moderate to low and went from 0.2.x to 0.3.0.
  - The monograph went from 0.2.1 to 0.3.0 for the same change.
  - `WORKFLOW.md:21` puts publication at 1.0.0.
- **Which side changes:** practice is coherent; METHODS should state it.
- **Proposed text:** add to the first bullet of §13:
  > "Before first publication (version 1.0.0) versions stay below 1: a change of conclusion or certainty raises the minor number and anything else the patch number. Claims carry their own versions on the same scheme."

---

## H. Data model, tooling and content that is not a claim

### M41 · outdated · §11 describes Git, Zotero and citeproc-js, which are not in use
- **The protocol:**
  - METHODS §11, `:329`: "a version-controlled repository (Git). Public repository history is the audit trail".
  - `:330`: "Zotero (group library)".
  - `:331`: "citeproc-js … claims, cards and excerpts rendered".
  - §4.4 (`:117`) and `reference.schema.json:5` also say citeproc-js.
- **Practice:**
  - The working copy is not a Git repository, and no public repository exists.
  - Files are copied to the senior author's computer by hand (`STATUS.md:80`).
  - References are built by `build_references.py` from a Crossref cache.
  - APA is rendered by the site's own functions. `app.core.js:1` says "production uses citeproc-js".
- **Consequence:** METHODS §13 (`:361`) says "Every version is retained and viewable". The home page (`index.template.html:68`) says "Every version and correction stays public". In practice:
  - `claim_patch.py` overwrites a claim and keeps only a changelog line, so the old text is lost;
  - card versions survive in `_superseded/` only when a card is merged;
  - the site does not show claim changelogs.
- **Proposed text:**
  - §11, first bullets →
    > "Source of truth: the project folder (data/, schema/, scripts/, docs/), copied to the senior author's computer after each session; before launch it moves to a version-controlled repository (Git) whose public history becomes the audit trail. References are built from Crossref records by scripts/build_references.py (CSL-JSON); there is no reference manager. Rendering: a static page generated by site/build.js; APA 7 is rendered by the prototype's own code until citeproc-js replaces it; claims, cards and anchors are rendered from the data files."
  - `index.template.html:68` → "Every correction will stay public."

### M42 · gap · Two sources of truth for the home-page figures, one of them unvalidated
- **The rule:** METHODS §10.2 (`:322`): the home page shows only figures that meet §10's rules, with all their fields.
- **What happens:**
  - `site/build.js:24` takes the home figures from `data/site/landing-stats.json`.
  - `validate.py` never checks that file, and it has no unit, population, data year, edition year or URL.
  - The schema-checked `data/epidemiology/landing.json` (last changed 14 October) goes unused.
- **The two files disagree:**
  - ep_us_cocaine_dependence_transition is "draft", with "[table to be confirmed on PDF]", in `landing.json`.
  - It is "verified" in `landing-stats.json`, and the home page shows it with a "verified" badge (`app.views.js:48`).
  - Five figures (past-year use by drug) appear under different ids in the two places.
- **Proposed fix:**
  - Build the home tiles from the `data/epidemiology` records that have `display.landing_page` set to true, so there is one source, and let `validate.py` check them.
  - Meanwhile, update `landing.json` for that figure (status verified; `page_or_table` "Results › 3.3, 1st paragraph; PMC3069146"), or show it on the home page as draft.

### M43 · gap · Content that is not a claim has statuses METHODS never defines
- **The protocol says everything is a claim:**
  - METHODS §1.1 (`:14`): "Its unit of content is the claim".
  - §1.4 (`:29`): "A paragraph with no citable claim is deleted".
  - The home page (`index.template.html:40`): "Every sentence is a claim tied to the page of the study".
  - §11 (`:328`) lists the data model without identity, legal or site tables.
- **Practice:**
  - Sections 2 and 13 are "Sourced facts, not graded claims" (`app.views.js:163`; `legal.schema.json:24`). They have their own ladder: draft, ai-checked, senior-verified (`identity.schema.json:18`, `legal.schema.json:44`).
  - Statistics are "not claims" and carry draft or verified (`epidemiology-figure.schema.json:73`; `index.template.html:113`). "Verified" means the AI checked the figure against the source page.
  - The Emergency numbers come from references read through WebFetch.
  - The 51 glossary definitions are shown to readers but never validated.
- **Proposed text:** a new METHODS §10.3, "Sourced facts":
  > "Identity and nomenclature (section 2), legal status (section 13), official statistics (§10) and the Emergency page's numbers are sourced facts, not graded claims: each names its source, the date read and how it was read (browser or WebFetch, §12.1). Statuses: draft (compiled by the AI) → ai-checked (confirmed in a second source or by a second reader) → senior-verified (checked by the senior author); a statistic shown as 'verified' has been checked by the AI against the source page on the date shown. Glossary definitions name their source."

  Also:
  - Add identity, legal, glossary and home-figure records, with their schemas, to §11.
  - Home page `:40` → "Every finding is a claim tied to the page of the study that supports it".

### M44 · gap · No section of METHODS governs the Emergency guide or the interactions matrix
- **What the site promises:**
  - The Emergency page (`index.template.html:160–162`) will carry, for each class, "the signs that mean call now; what to do while waiting; what not to do", reviewed by the senior author.
  - The interactions page (`:126`) promises "for every pair of classes, a claim with its certainty".
- **What METHODS covers:**
  - §8 covers only pages for single substances. Section 6 includes "emergency response evidence" (`:287`).
  - §1.2 and §1.5 reserve practical risk-reduction guidance for the senior author, after legal review (section 7). Neither mentions the Emergency page, though its what-to-do content is practical guidance of the same kind.
- **Proposed text, for the senior author to decide:** add after the §8 table:
  > "Site-wide pages. The Emergency page and the interactions matrix are built from claims graded under §6 (claims about pairs of classes for the matrix). Emergency guidance (signs, what to do, what not to do) is written or approved line by line by the senior author and is included in the legal review of §1.5; until then the page carries only verified emergency numbers."

---

## I. Outdated statements

### M45 · outdated · METHODS principle 3 still requires verbatim excerpts
- **Sides:**
  - `METHODS.md:30`: "Verbatim evidence. Every claim carries at least one page-referenced excerpt".
  - §4.5 and changelog 0.2.0 (1) (`:417`) replaced excerpts with anchors.
  - The site Methods page has already been updated (`index.template.html:231`).
- **Proposed text:** `:30` →
  > "3. **Anchored evidence.** Every claim carries at least one evidence anchor (§6.2), located on a page, or at a section and paragraph, of a source the editors have read in full. No claim is made from an abstract alone. Quotations only where the wording itself is the evidence, never more than 15 words (§4.5)."

### M46 · outdated · §16 limitations
- **Sides:**
  - `METHODS.md:387` says "The two-reader rule has one human reader". The protocol now uses a three-reader rule (§5.5).
  - The same line says external review is "a goal for the second year (§13)". §13 says nothing about external review.
  - `:388` still says "excerpts" (see M3).
- **Proposed text:** `:387` → "The three-reader rule has one human reader; the others are AI systems. Independent external review of each monograph is a goal for the second year after launch." For `:388`, use the text in M3.

### M47 · outdated · METHODS header and README
- **Sides:**
  - `METHODS.md:4`: "Frozen before any monograph content is written". Four later versions (0.2.0 to 0.2.3) were adopted after content existed.
  - `README.md:5`: "pre-registered v0.1.0".
  - `README.md:10` lists only two scripts; `scripts/` now holds 15.
  - `README.md:7` omits the identity and legal schemas.
- **Proposed text:**
  - `METHODS.md:4` →
    > "**Status:** Version 0.1.0 was written on 2026-10-14, before any monograph content. Every later change is logged in the Changelog with its date and reason and is never applied retroactively without a note on the affected pages; versions 0.2.0–0.2.3 were adopted before any claim left draft."
  - `README.md:5` → "editorial protocol (authoritative; v0.2.3; v0.1.0 written before any content)".
  - `README.md:10` → "`scripts/` — validation (`validate.py`, `rob_vocab.py`, `check_card.py`, `check_citations.js`), data building and reading rounds (see the pipeline in `docs/WORKFLOW.md`)".
  - `README.md:7`: add "identity, legal".

### M48 · outdated · A paper said to be "on the reading list" is on no list, and the protocol's reference list is incomplete
- **The reading-list claim:** §6.3 (`:246`) says doi:10.1136/bmj.h870 "is on the reading list". That DOI appears nowhere else in the project: not in `READ-MYSELF-LIST.md`, `PDF-REQUEST-LIST.md`, the search logs or `source_checks.json`.
- **Cited in the text but missing from "References for this protocol"** (`:392–410`):
  - the GRADE Handbook (`:223`);
  - QUADAS-2 (`:166`);
  - the JBI prevalence checklist (`:167`);
  - Anthony et al., 1994, and Lopez-Quintero et al., 2011 (`:321`);
  - the BMJ 2015 paper.
- **Proposed fix:**
  - Add the DOI to `docs/READ-MYSELF-LIST.md`, or change the text to "is to be read".
  - Add the missing entries from their Crossref records (§4.2) and update the count in the footnote at `:410`.

### M49 · outdated · Counts and pending items in STATUS

| Line | STATUS says | The data show | Proposed text |
|---|---|---|---|
| `:8` | "v0.2.x: 32 claims, 40 study cards (36 from full text), 49 references from Crossref" | Monograph v0.3.1; 33 claims; 40 cards (36 with a full-text `source_read`); 39 study references in `methamphetamine.json` plus harding_2022, which is filed in `protocol-and-site.json`. 53 records in all, 46 of them from Crossref. | "Methamphetamine monograph v0.3.1: 33 claims, 40 study cards (36 from full text), 40 study references from Crossref (53 reference records in all)." |
| `:9–10` | "153 anchors re-found independently, 11 cards checked" | 128 anchors re-found blind and 86 checked at the stated place; 19 cards ai-checked (monograph changelog 0.3.1). | "…128 anchors re-found blind and 86 checked at the stated place; 19 cards ai-checked." |
| `:10` | "every number in a PDF anchor confirmed … by script" | The script skips single digits and editors' calculations (see M9). | "every number of two or more digits in a PDF anchor (editors' calculations excepted) found on its printed page by script" |
| `:31` | "34 … maps, 2,420 unique papers" | `data/evidence-maps.json` lists 36 maps (30 substances and 6 cross-cutting). | "36 maps (30 substances, 6 cross-cutting)" |
| `:39` | "ai-anchored: 12 claims" | 11 | "ai-anchored: 11 claims" |
| `:57–61` (item 3) | "Round 1b for the 24 web sources" still to do | `round1b/out` holds 19 outputs: 10 PDF and 9 web sources. The "five cards … being re-rated" are done (`:33–35`). | "Round 1b for the remaining 15 web sources" |
| `:63` (item 3b) | "McKetin 2019 is being fixed" | Done; no validator warning remains. | Delete. |

### M50 · wording · The second-reader and adjudication briefs are tied to rounds 1 and 1b
- **The briefs:**
  - VERIFICATION-BRIEF names round 1 and its paths at `:1`, `:10`, `:38` and `:83`.
  - ADJUDICATION-BRIEF names rounds 1 and 1b at `:1`, `:5` and `:22`.
- **What happened since:**
  - Rounds 2 and 2b (`data/verification/round2`, `round2b`) used the same procedures.
  - Neither brief mentions targeted checks, which set the status of 86 anchors. Those checks ran from `data/verification/targeted-2026-10-16/tasks.json`, with no brief in `docs/`.
- **Proposed text:**
  - VERIFICATION-BRIEF `:1` → "Second-reader brief (AI reader 2)". Use the paths `data/verification/<round>/…`, with the round named in the task.
  - Add a section: "Targeted checks: for each anchor in the round's targeted task file, open the source at the stated place and answer confirmed / corrected / wrong-location / not-found; the editor sets check_mode: targeted."
  - Make the same path change in ADJUDICATION-BRIEF.

### M51 · wording · Tiers
- **Sides:**
  - METHODS §1.3 (`:23`): "Tier 2: the next ~30". `TIER1.md:44` lists 25.
  - `:24` gives "novel benzodiazepines" and "nitazenes" as Tier 3 class pages. TIER1 covers designer benzodiazepines and nitazenes inside Tier 1 pages (rows 2 and 25, `TIER1.md:12`, `:35`), and also lists "Nitazenes (own page if burden warrants)" in Tier 2.
  - `TIER1.md:3` marks Tier 1 "proposed, awaiting senior-author approval". METHODS §1.3 and the site (`index.template.html:80`, "Thirty substances, one template") present it as settled.
- **Proposed text:** `METHODS.md:22–24` →
  > "**Tier 1 (launch):** the 30 substances proposed in docs/TIER1.md, once approved by the senior author… **Tier 2:** the next 25 or so (docs/TIER1.md)… **Tier 3:** class-level pages for substances the EUDA Early Warning System or UNODC lists in a class and that no Tier 1 or Tier 2 page covers, with substance stubs that carry only what the literature contains."

---

## The five findings that matter most

1. **M1, with M2.**
   - 86 of the 214 anchors counted as "re-found independently" were checked at the stated place, not re-found blind.
   - 10 of the 11 ai-anchored claims rest partly on such checks; cl_meth_cognition_causal rests on them entirely.
   - §6.2, §12 and the public labels still define ai-checked as blind re-finding.
   - The rule that changed this entered §5.5 with no changelog entry.
2. **M3.** The public site says no claim leaves draft until a human has checked its anchors. In fact 24 of the 33 claims are above draft and no human has checked any of them. METHODS §12 and §16 also contradict each other here.
3. **M4.** The senior author's reading of study cards (`appraised`) exists only on paper:
   - no step, tool or script marks a card appraised;
   - an approved claim would jump straight to senior-reviewed;
   - §12 defines appraised in words left over from the two-reader era.
4. **M6.** Adjudication sets cards to ai-checked even when the readers still disagree on risk of bias, against §5.5. sc_wearne_2018 is an example, and all 19 ai-checked cards went through adjudication.
5. **M27.** The Numbers page shows verbatim source sentences on hover: 115 of them run past 15 words, and the longest has 58. That is against §4.5, and nothing checks it.

## Counts by severity

| Severity | Number | Findings |
|---|---|---|
| contradiction | 19 | M1, M2, M3, M4, M5, M6, M8, M12, M13, M16, M19, M21, M23, M24, M27, M32, M33, M39, M40 |
| gap | 15 | M7, M9, M11, M14, M25, M26, M28, M29, M31, M36, M37, M38, M42, M43, M44 |
| outdated | 9 | M15, M30, M34, M41, M45, M46, M47, M48, M49 |
| ambiguity | 3 | M10, M17, M18 |
| wording | 5 | M20, M22, M35, M50, M51 |
| **Total** | **51** | |
