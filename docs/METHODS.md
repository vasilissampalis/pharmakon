# Editorial Protocol (Methods)

**Version:** 0.4.0
**Status:** Version 0.1.0 was written on 2026-10-14, before any monograph content. Every later change is logged in the Changelog at the end of this document with its date and reason, and is never applied retroactively without a note on the affected pages; versions 0.2.0–0.2.4 were adopted before any claim was signed off by the senior author. Changes marked "for the senior author's confirmation" stand until he confirms or reverses them.
**Senior author:** Vasilis Sampalis, MSc (clinical neuropsychologist)
**AI co-editor:** Claude (Anthropic), first-pass extraction, appraisal and drafting under the senior author's review
**Last revised:** 2026-11-15 (v0.4.0)

---

## 1. Purpose and scope

### 1.1 Mission
This encyclopedia describes what the scientific literature does and does not establish about psychoactive drugs, for people who use them, the people around them, and the clinicians who work with them. It neither promotes nor vilifies drug use. Its unit of content is the **claim**: a statement about a population, an exposure and an outcome, linked to the exact evidence that supports it, graded for certainty, and shown with its disagreements.

### 1.2 What it is not
- It is not medical advice and does not replace a clinician.
- It does not author dosing instructions, administration techniques or potentiation methods. The template reserves a section for practical risk reduction (§8, section 7); that section is authored solely by the senior author under his clinical and legal responsibility, to the same citation standard as every other section, and only after legal review (§1.5).
- It does not take a position on drug policy. It reports the evidence on which policy arguments rest.

### 1.3 Scope by tier
- **Tier 1 (launch):** the 30 substances proposed in `docs/TIER1.md`, chosen by prevalence, harm burden and coverage of every pharmacological class, once approved by the senior author. Each receives a full monograph.
- **Tier 2:** the next 25 or so (listed in `docs/TIER1.md`), full monographs after launch.
- **Tier 3:** class-level pages for substances that the EUDA Early Warning System or UNODC lists in a class and that no Tier 1 or Tier 2 page covers, with substance stubs that carry only what the literature actually contains.
- Legal drugs (alcohol, nicotine, caffeine) and prescribed drugs with non-medical use are treated with exactly the same template, depth and appraisal as illicit drugs.

### 1.4 Principles
1. **Symmetry.** Every study is appraised with the same instrument regardless of its conclusion, its funder or its authors' reputation. A study that supports a position the editors find congenial gets no easier reading than one that does not.
2. **Claims, not narratives.** Text is built from claims with evidence attached. A paragraph with no citable claim is deleted.
3. **Anchored evidence.** Every claim carries at least one evidence anchor (§6.2), located on a page, or at a section and paragraph, of a source the editors have read in full. No claim is made from an abstract alone. Quotations only where the wording itself is the evidence, never more than 15 words (§4.5).
4. **Uncertainty is content.** Certainty is graded and displayed. "Not known" is a valid and frequently correct answer and is written as such.
5. **Base rates first.** Prevalence, conditional probabilities and absolute risks appear before relative risks, case reports or anecdotes.
6. **The interpretation gap is reported.** For each key study, what the data show is separated from what the abstract, discussion and press coverage claimed.
7. **Corrections are public.** Every change to a published claim is versioned and visible (§13).
8. **Interests are declared.** Study funding, author affiliations and the site's own funding are stated and never used as a trump card (§14).
9. **Language does not stigmatize** (§9).
10. **The method is public before the content.** This document is published before any monograph, so that the method cannot be fitted to conclusions.

### 1.5 Legal review
Before launch, the practical-risk-reduction sections (§8, section 7) and the community features (§15) receive a written legal opinion covering Greek law and the EU jurisdictions from which most traffic is expected. The opinion is summarized on the About page.

---

## 2. Search strategy

A monograph begins with a documented search, logged in `search-logs/<substance>.md` following PRISMA 2020 (Page et al., 2021). The log records, for each database: date searched, exact search string, number of hits, number screened, number included, and reasons for exclusion at full-text stage.

### 2.1 Databases and sources
Searched in this order; all usable without institutional access.

| Layer | Source | Use |
|---|---|---|
| Backbone | PubMed/MEDLINE | primary bibliographic search; run by the AI through the public E-utilities interface in the app's browser, or by the senior author; results logged in `search-logs/` (changed in 0.2.4 from "run by the senior author", for his confirmation) |
| Backbone | Europe PMC | full-text search of open-access literature; preprints flagged |
| Backbone | Cochrane Library | systematic reviews of interventions |
| Backbone | OpenAlex / Crossref | metadata verification, citation counts, backward and forward snowballing |
| Backbone | Google Scholar | grey literature, theses, forward citation of landmark papers |
| Supplementary | PsycInfo | search and result counts only (record access is subscription-based) |
| Registries | ClinicalTrials.gov, EU CTR, PROSPERO, OSF | registered but unpublished trials and reviews; pre-registration checks |
| Grey literature | EUDA (formerly EMCDDA), UNODC, WHO, NIDA, SAMHSA/NSDUH, ESPAD, national monitoring centres, Global Drug Survey | epidemiology, drug-checking data, policy documents |
| Retractions | Crossref/Retraction Watch database | mandatory check on every included source (§4.3) |

### 2.2 Search string template
For each substance, searches combine:
```
(<substance name> OR <IUPAC/INN synonyms> OR <common street names in the literature>)
AND (<outcome domain terms>)
```
Outcome domains correspond to the monograph sections: pharmacology/pharmacokinetics; neuroimaging and neuroscience; cognition; subjective and physiological effects; acute toxicity and overdose; drug interactions; dependence and withdrawal; long-term physical, psychiatric and cognitive outcomes; epidemiology and mortality; harm-reduction interventions; therapeutic trials. The exact strings for each substance are written before the search, stored in the log, and not altered during screening.

### 2.3 Hierarchy and depth
1. **Systematic reviews and meta-analyses** form the backbone of every section. Each is appraised with AMSTAR 2 (§5.3) before its conclusions are used.
   Evidence reports by public bodies that state how they weigh evidence and were externally reviewed (the US Surgeon General, IARC, the US National Academies, government-commissioned reviews) are used alongside systematic reviews and appraised with the editors' evidence-report checklist (§5.3).
2. **Primary studies** are retrieved when: (a) no adequate systematic review exists; (b) a claim is contested; (c) the study is a landmark whose interpretation the field relies on; (d) it was published after the most recent adequate review.
3. **Critiques, replies, commentaries and corrections** on landmark studies are retrieved deliberately (forward citation search). A landmark study is never cited without its published critiques.
4. **Preclinical studies** are cited only where human data do not exist for the question, and always with the translation caveats in §5.4.
5. **Date limits:** none for landmark studies; for synthesis, the last ten years are searched systematically and earlier work enters through reviews and snowballing.

### 2.4 Snowballing
For every included systematic review and landmark study: backward citation (its reference list) and forward citation (papers citing it, via OpenAlex/Google Scholar), screened by title and abstract. Snowballing is logged with the seed paper's DOI.

### 2.5 Stopping rule
Searching for a section stops when a full pass of forward and backward citation on the included studies yields no new eligible study. The date of the last systematic search is printed on every monograph.

---

## 3. Eligibility

### 3.1 Included
- Peer-reviewed journal articles, including systematic reviews, meta-analyses, RCTs, cohort, case-control, cross-sectional, qualitative and case-series designs, and human laboratory studies.
- Grey literature from recognized monitoring bodies (§2.1) for epidemiology and policy facts.
- Books and book chapters by academic publishers, for historical and conceptual material only; never as the sole source of an empirical claim.
- Preprints, flagged as such, only for very recent findings with no peer-reviewed equivalent; re-checked at every update (§13).

### 3.2 Excluded
- Papers in journals that appear in current predatory-publishing lists or that are absent from DOAJ/Scopus/MEDLINE without explanation; the exclusion is logged with the reason.
- Retracted papers (cited only inside a study card to document the retraction, never as evidence).
- Papers that cannot be obtained in full text. The senior author obtains all PDFs; a paper is not dropped for access reasons.
- Opinion pieces, editorials and press releases as evidence for empirical claims. They may be quoted in the "interpretation gap" field of a study card.

### 3.3 Language
English and Greek are read directly. Other languages are included when a reliable translation can be produced and are flagged.

---

## 4. Reference management and citation

### 4.1 Reference record
Every source is stored once, as a CSL-JSON record (`schema/reference.schema.json`) with the site's own fields added: the PMCID where it exists (PMIDs are added from the PubMed Central ID converter), retraction status, the date metadata was verified, who verified it, and the location of the full-text PDF in the project folder.

### 4.2 Metadata verification
Metadata is never typed by hand. It is fetched from Crossref by DOI (`api.crossref.org/works/<DOI>`) and stored. The publication year used in citations is the **print-issue year** (`published-print` in Crossref) when it exists, otherwise the online-first year; the online-first date is stored separately. Records fetched from Crossref are stored as `metadata-verified`. Where a PDF is on file, the senior author compares authors, year and title with its first page and the record becomes `pdf-checked`; for full texts read on the web the comparison is made against the article page. When Crossref can only be reached through WebFetch (§12.1), a record becomes metadata-verified only when two independent fetches agree on every field. Sources without a DOI (reports, books, web pages) are verified against the publisher's page and store an ISBN or URL and the access date.

### 4.3 Retraction and correction check
Before a source is cited, and at every monograph update, its DOI is checked against the Crossref/Retraction Watch data for retractions, expressions of concern and corrections. Results are stored on the reference record. A retracted source is removed from evidence immediately; the claim that relied on it is re-graded or withdrawn, and the change is logged (§13).

### 4.4 Citation rendering
- Style: APA 7th edition, rendered from the CSL-JSON records by the prototype's own code until citeproc-js with the APA CSL style replaces it. Formatting is never typed by hand.
- In-text citations are interactive: hovering shows the full APA 7 reference; clicking opens the DOI (`https://doi.org/<DOI>`), or the publisher/registry URL where no DOI exists.
- Each in-text citation also exposes the study card (§5) and the evidence anchors (§6.2) it supports.
- The reference list of each monograph is generated from the claims on the page, so a reference cannot appear in the list without supporting a claim and vice versa.

### 4.5 Evidence anchors and quotation policy
The site does not reproduce passages from its sources. A claim is tied to its source by an **evidence anchor** (§6.2): the printed page, the place on the page (section, paragraph, table or figure), and the data the claim rests on, stated in the editors' own words: numbers, sample sizes, intervals, test statistics and conditions. What a reader needs in order to check a claim is the location and the numbers, and those are not anyone's prose.

A verbatim quotation is used only where the wording itself is the evidence, for example an author's conclusion whose strength is being appraised. It is limited to **15 words** (and 140 characters), in quotation marks, with the page, and to **one per claim**. Figures and tables are never reproduced; their values are reported with page and table numbers. Rationale: copyright, and the fact that what gets verified is a number at a location, not a sentence. (Revised 2026-10-15; earlier drafts of this protocol called for one-to-three-sentence excerpts.)

---

## 5. Study cards (data extraction and appraisal)

Every primary study and every systematic review that supports a claim receives a study card (`schema/study-card.schema.json`). The card is the device by which the site reads back from a paper's conclusions into its mechanism.

### 5.1 Fields

| Field | Content |
|---|---|
| Design | Named design (RCT, crossover human-laboratory, prospective cohort, retrospective cohort, case-control, cross-sectional, case series, qualitative, systematic review, meta-analysis, preclinical with species and model). **What this design can and cannot establish** is written in one sentence. |
| Sample and recruitment | n per group; source (treatment-seeking, community, prison, advertisements, registry); inclusion and exclusion criteria; demographics; attrition. Selection effects are named explicitly. |
| Exposure measurement | How use was measured (self-report instrument, biological verification, records); dose, frequency, duration, route; purity known or unknown; polysubstance use and how it was handled; abstinence at testing and how verified. |
| Comparison group | Who the controls were; matching variables; **premorbid variables that were not measured** (there is almost never a pre-use baseline); whether controls used other drugs. |
| Outcome measures | Instruments; validity and norms; how "impairment" or "harm" was operationalized; number of outcomes tested; correction for multiplicity; blinding of assessors. |
| Analysis and reporting | Effect sizes with confidence intervals (computed by the editors if the paper reports only p-values); covariates adjusted for; pre-registration status and deviations; selective reporting; power. |
| Interpretation gap | What the results section shows, versus what the abstract, the discussion and (where traceable) the press release or institutional communication claimed. Paraphrased with page numbers; a quotation of 15 words or fewer only where the wording itself is at issue (§4.5). |
| Replication and timeline | Direct and conceptual replications; failures; published critiques and replies; where the question stands now, with dates. |
| Funding and interests | Funder; declared conflicts; author affiliations relevant to the question. Stated for every study, used as a flag for closer reading, never as a reason to discount results. |
| What would settle it | The study that has not been done and that would resolve the question, in one or two sentences. |
| Risk of bias | Instrument used (§5.3), domain-level judgments, overall judgment, and the reasoning. |
| Verification | Who extracted, who reviewed, dates, and the disagreement log (§5.5). |

### 5.2 Design-specific checks
- **Cross-sectional user-versus-control studies**: pre-existing difference versus drug-induced change cannot be separated; the card says so and names any sibling, twin or prospective study that addresses it.
- **Prospective cohorts**: baseline timing relative to onset of use; loss to follow-up; time-varying confounding.
- **Human laboratory studies**: dose range relative to real-world use; route; sample size; whether participants were experienced users; generalizability.
- **RCTs of therapeutic use**: blinding integrity (psychedelic trials in particular), expectancy, functional unblinding, outcome timing.
- **Imaging studies**: sample size; multiple comparisons; the gap between a group difference in a biomarker and a functional deficit; reversibility data if any.
- **Mortality and registry studies**: cause-of-death coding; denominator definition; competing risks.

### 5.3 Risk-of-bias instruments by design
| Design | Instrument |
|---|---|
| Randomized trials | RoB 2 (Sterne et al., 2019) |
| Non-randomized studies of exposures (most observational drug-effect studies) | ROBINS-E (Higgins et al., 2024) |
| Non-randomized studies of interventions | ROBINS-I (Sterne et al., 2016) |
| Systematic reviews and meta-analyses | AMSTAR 2 (Shea et al., 2017) |
| Animal studies | SYRCLE's RoB tool (Hooijmans et al., 2014) |
| Test accuracy (design `test-accuracy`): a test's results compared with a reference method, for example drug-checking strips and colour tests against laboratory analysis of the same samples or of known concentrations | QUADAS-2 (Whiting et al., 2011) |
| Prevalence studies | JBI critical appraisal checklist for prevalence studies |
| Narrative reviews | No validated instrument. The card records the editors' checklist (systematic search and explicit selection; appraisal of the cited studies; reliance on the authors' own work; separation of evidence from speculation; balance), stored as `none-applicable`. The review is cited for arguments and pointers; a claim whose only support is narrative reviews stays at draft and says its figures are second-hand (§6.3) |
| Evidence reports by public bodies (for example the US Surgeon General, IARC monographs, the US National Academies, government-commissioned reviews) | The editors' evidence-report checklist, stored as `editors-report` (design `evidence-report`): search and selection; appraisal of the included studies; stated grading rules; independence and funding; external review; conclusions within the evidence. AMSTAR 2 where the report states a systematic search for the conclusions used. The report's graded wording (for example "sufficient to infer a causal relationship") is cited as that body's judgment, never as the editors' own; a claim may rest on it, and where such a report and a systematic review disagree, both are shown |
| Qualitative studies | The editors' qualitative checklist (domains adapted from CASP: design, sampling, data collection, researcher relationship, ethics, rigour of analysis, grounding of findings, transferability), stored as `editors-qualitative` |
| Case series, case reports, modelling, registry descriptions | No instrument; the card states the design's limits |

The instrument's domain judgments are stored on the card and displayed; a single summary word is never shown without the domains behind it.

**Each instrument keeps its own words** (checked by `scripts/rob_vocab.py`, which the validator runs):

| Instrument | Domain judgments | Overall |
|---|---|---|
| RoB 2 | low · some concerns · high | low · some concerns · high |
| ROBINS-E | low · some concerns · high · very high | same |
| ROBINS-I | low · moderate · serious · critical · no information | same |
| AMSTAR 2 | yes · no; partial yes only for items 2, 4, 7, 8 and 9; no meta-analysis only for items 11, 12 and 15 | high · moderate · low · critically low confidence |
| SYRCLE, QUADAS-2 | low · high · unclear | same |
| JBI prevalence | yes · no · unclear · not applicable | the editors' summary: low · moderate · high (JBI has no overall algorithm) |
| Editors' narrative-review, qualitative and evidence-report checklists | low · some concerns · high | same |

The instrument must match the card's design (randomized trials and placebo-controlled laboratory studies with randomized or counterbalanced order: RoB 2; observational studies: ROBINS-E, or ROBINS-I for interventions; prevalence surveys: JBI; systematic reviews and meta-analyses: AMSTAR 2; narrative reviews, qualitative studies and evidence reports: the editors' checklists (AMSTAR 2 also for an evidence report with a stated systematic search); animal studies: SYRCLE; test-accuracy studies: QUADAS-2); `scripts/rob_vocab.py` reports a mismatch for every design with a listed instrument. For RoB 2, ROBINS-E, ROBINS-I and the editors' checklists, the overall judgment is never less severe than the worst domain. Two documented extensions: an AMSTAR 2 item that can only be judged from a supplement the readers have not seen is recorded as "no information", and the overall confidence rating is then marked provisional; a JBI item met in part is recorded as "partial yes" with the reason. Corrections of vocabulary or of rule-based consistency made by the editor after the readers finished are logged on the card (`verification.editorial_corrections`); changes of judgment go back to the readers or the senior author.

### 5.4 Preclinical evidence
Animal and in vitro findings are stored with species, strain, sex, dose (and the allometric or pharmacokinetic basis for any human-equivalent-dose statement), route, dosing schedule, and whether the regimen resembles human use patterns. A preclinical finding never raises the certainty of a human claim above "low" on its own. Test-accuracy studies of drug samples (§5.3) are not preclinical: their claims are about the test itself, and laboratory conditions are rated as indirectness (§6.3).

### 5.5 Three-reader rule
1. **First reader (AI).** Writes the card from the full text — the PDF in the project folder, or a free full text read in the app's browser (PubMed Central, or the publisher's own HTML article) — anchoring every number to a page or, for web full texts, a locator (§6.2). A trial-registry record may be read to check registration and outcomes; the anchor then says so in its page and locator. Before the second reading, the first reader runs a mechanical check (`scripts/check_anchor_numbers.py`): every number of two or more digits in a PDF anchor, other than an editors' calculation, must appear, allowing for rounding, on the page the anchor names in a text extraction of the PDF. Status `first-pass`.
2. **Independent second reader (AI).** A separate AI reader works blind to the first reader's anchors: for each source it is given only the claims that cite it (statement and magnitude), finds in the full text everything that supports, contradicts or qualifies each claim, records its own anchors and gives a verdict on each claim (supported, partly supported, not supported, contradicted), including whether the wording overstates the source. Only then does it open the first reader's study card and confirm, correct or relocate each key finding and reporting issue. A script (`scripts/reconcile_second_reader.py`) matches the two readers' anchors: same printed page (for web full texts, overlapping section words) and at least 60% of the first reader's numbers recovered, ignoring whole numbers below 10; or, wherever placed, at least 85% of three or more numbers; anchors without numbers match on the same place and 30% word overlap. A matched anchor becomes `ai-checked` (`check_mode: blind`) only when the second reader judged the claim supported or partly supported. Anchors the blind reading did not re-find, and anchors the editor added after the blind reading, are then checked one by one at the place given (a **targeted check**): a second reader sees the anchor, confirms, relocates or corrects it against the source, and the anchor becomes `ai-checked` with `check_mode: targeted`. The site labels these "checked at the stated place", because a targeted check is weaker than a blind re-finding. An anchor written by the second reader itself counts as `ai-checked` only when the first reader's card already records the same finding, which `located_by` then names, or when a reader who wrote neither the anchor nor that finding has checked it at the stated place. The editor's own check is never a second reader's check. Every disagreement is listed for the senior author. The second reader's findings on the card are settled against the source by an adjudicating AI reader, who corrects factual errors and logs every change in `verification.disagreements`; a card becomes `ai-checked` when every key finding and reporting issue has been confirmed or corrected in this way and the readers agree on the overall risk-of-bias judgment. Differences on single domains or on the interpretation-gap rating are logged and shown for the senior author; an open disagreement on the overall judgment keeps the card at `first-pass`.
3. **Senior author.** Reads the card against the source and may overrule any field or judgment; the card's status becomes `appraised`. In the site's review queue each anchor shows its source (link or PDF filename) and is ticked when checked, each study card is marked read when he has read it against its source, and each claim is then approved, approved with edits, or flagged with a note. Decisions are read back into the claim and card files (`scripts/apply_senior_review.py`) with the claim version they were made on; a decision taken on an earlier version of a claim does not carry over to a changed claim, and a claim edited after approval returns to the rung its anchors support with its review pending.

No card is marked `appraised`, and no claim resting on it rises above `ai-anchored`, without the senior author's reading. The card records what was read (`source_read`): a card written from an abstract alone cannot leave `draft`.

The first reader also records **reporting issues**: internal inconsistencies found on reading (degrees of freedom that do not match the sample size, a correlation reported without its sign, inclusion criteria contradicted by the sample table, text that contradicts a table, a figure that differs from the same value elsewhere in the paper). Each is anchored to a page and its consequence for interpretation is stated.

### 5.6 Further AI checks
Between the second reading and the senior author, further AI readers may: (a) adjudicate the second reader's card findings against the source (§5.5; `docs/ADJUDICATION-BRIEF.md`); (b) check anchors at the stated place (§5.5); (c) re-appraise a card with a different instrument, with a blind check by another reader whose disagreements go to the senior author; (d) review every claim as independent methodologists against its evidence and this protocol (`docs/REVIEW-BRIEF*.md`). Their findings are adjudicated against the source by the editor and logged on the claim or card. Only a second reader's blind re-finding or targeted check sets an anchor to `ai-checked`; a methodologist's confirmation of an anchor is recorded in the round's output and the claim's changelog and does not change its status.

---

## 6. Claims and certainty

### 6.1 Claim statement
A claim (`schema/claim.schema.json`) is written in a fixed form:

> In **[population]**, **[exposure]** compared with **[comparator]** **[is associated with / increases / reduces / causes / does not detectably change / evidence is insufficient to say whether … changes]** **[outcome]**: **[direction and magnitude, with interval]**. Certainty: **[GRADE]**. Status: **[replicated / replicated by the same team / single study / contested / mixed]**.

Causal language ("increases", "reduces", "causes", "damages", "impairs") is used only when the certainty rating and the designs support it. Otherwise the verb is "is associated with", and the card explains why. Descriptive claims (§6.3: prevalence, base rates, trends, standardized mortality) take the relation `describes`. "Insufficient evidence" is used when neither an effect nor its absence can be shown with precision.

### 6.2 Evidence anchors
Each claim links to one or more evidence anchors (§4.5): reference, study card, printed page, locator (section, paragraph, table or figure), the extracted data in the editors' words, the anchor's role (supports, contradicts or qualifies) and its status:

| Anchor status | Meaning |
|---|---|
| unchecked | Drafted; not yet located in the full text |
| ai-located | Located in the full text by an AI reader: the first reader, or the editor from the full text or from a key finding of the study card (`located_by` says which) |
| ai-checked | Confirmed by a second AI reader: re-found blind (`check_mode: blind`), or, if the blind reading missed it or it was added later, checked at the place given (`check_mode: targeted`; shown as "checked at the stated place") |
| senior-verified | Checked against the source by the senior author |

A claim rises to `ai-anchored` when all its anchors are `ai-checked`, and to `anchor-verified` when all are `senior-verified` (§12).

**Locators.** For a PDF, the page is the printed page (online-first PDFs: the article's own page numbers). For a web full text without print pagination, the page is "PMC HTML" or "publisher HTML"; for a registry record, "registry record". The locator gives the section path as printed (e.g. Results › Sample, 2nd paragraph) or the table or figure with its row or column. Paragraphs are running-text paragraphs within the named section or subsection: headings, captions, figure legends, footnotes and boxed key points are not counted; a paragraph continued from the previous page counts on the page where it starts. Anchors written before this convention was stated (2026-10-16) are re-checked against it at the senior author's review.

### 6.3 GRADE certainty
Certainty is rated with GRADE (Guyatt et al., 2008; GRADE Handbook) and displayed on every claim as **high / moderate / low / very low**, with the reasons.

Starting point: randomized evidence starts **high**; observational evidence starts **low**. Placebo-controlled within-person laboratory studies start high when condition order was randomized or counterbalanced; the risk-of-bias domain records which. A claim seen only through reviews starts from the design of the primary studies the review describes and is downgraded for risk of bias (not appraisable) and indirectness (second-hand). (Made explicit in 0.2.4, for the senior author's confirmation.)

Downgrade one or two levels for each of:
1. **Risk of bias** (from the study cards' instrument judgments)
2. **Inconsistency** (unexplained heterogeneity across studies)
3. **Indirectness** (population, exposure, comparator or outcome differ from the claim; preclinical evidence is always indirect)
4. **Imprecision** (wide intervals; small samples; intervals that include both benefit and harm)
5. **Publication bias** (small-study effects, missing registered trials, industry-sponsored literature with one-sided results)

Upgrade observational evidence one level for each of: a large effect (RR > 2 or < 0.5, with no plausible confounders), a dose–response gradient, or plausible residual confounding that would reduce the observed effect.

Rules:
- A claim inherits the certainty of its weakest necessary link.
- Absence of evidence is not evidence of absence: "no detectable effect" claims require precision (an interval that excludes meaningful effects), not a non-significant p-value.
- Relative effects are always accompanied by absolute effects where the base rate is known.
- Where two bodies of evidence conflict, the claim is marked **contested** and routed to the debate format (§7).
- **Rate the claim as worded.** A claim worded as an association is rated for the association; whether it is causal is a separate claim, usually contested. Risk of bias is downgraded when the biases that remain after the reported adjustment could plausibly change the estimate materially (unadjusted comparisons with known confounders, selected samples, unblinded outcome rating); it is not downgraded twice for the same problem in two domains.
- **Large effect** is applied only when the estimate stays large under the most adjusted model reported and no remaining bias runs away from the null; a large standardized difference between small selected groups does not qualify.
- **Overlapping evidence** (meta-analyses sharing primary studies; a cohort that is also inside a pooled estimate; one laboratory's successive studies) is not counted as independent replication, and the claim says so.
- **Editors' calculations** (absolute risks, two-sided intervals from a reported standard error, standardized differences from printed means and SDs) are labelled as such and recomputed by the second reader.
- The arithmetic (starting level minus downgrades plus upgrades) is checked by the validator, and upgrades apply only to evidence that starts low.
- **Descriptive claims** (prevalence, base rates, time trends, standardized mortality) are rated as descriptions of the population sampled. They start low like other observational evidence, are downgraded when coverage, response or measurement could materially change the figure, and are never upgraded for large effect, which concerns the size of an exposure's effect under adjustment, not a count, a rate or a change over time. A GRADE paper on rating confidence in estimates of event rates (BMJ, 2015, doi:10.1136/bmj.h870) is to be read (it is on the protocol reading list in `docs/STATUS.md`); this rule will be revisited when it has been read.
- **Upgrading evidence already rated down.** When evidence downgraded for risk of bias is also upgraded (for example for a within-person dose–response gradient), the reasoning says so, explains why, and gives the certainty a strict reading would give.
- **Claims resting only on narrative reviews** (every supporting anchor cites a narrative review) stay at draft, say in the statement that their figures are second-hand, and are never shown in the at-a-glance box; the validator enforces the status.
- **Test accuracy** (for the senior author's confirmation, decision `p-test-accuracy`). A claim about how often a test gives the right result is rated the way GRADE rates tests (Schünemann et al., 2008): accuracy studies that compare the test with an appropriate reference method on the kind of samples the test is used for start **high**, and are rated down with their QUADAS-2 judgments (for example a selected set of known positives and negatives, or readers who knew the answer), for indirectness (pure compounds in water, trained chemists in a laboratory, or one brand or production lot, when the claim is about real samples, home use or tests in general) and for imprecision (few samples, single strips, no repeats). Such claims take the relation `describes` (no other relation fits how often a test reads right), but this rule, not the rule for descriptive claims above, sets their starting level. Accuracy is a stand-in for what matters to people: whether testing changes what people do, or prevents overdoses and deaths, is a separate claim rated from studies of people, which start low unless randomized.

### 6.4 Status flags
- **replicated**: at least two independent studies with consistent direction, counted among the primary studies, including those pooled in a meta-analysis when the review reports their direction; reviews that share primary studies count once (§6.3).
- **replicated by the same team** (`replicated-same-team`): two or more studies in the same direction that share investigators, site, sample or analysis model. Shown with that label, because agreement within one group is weaker than independent replication (§6.3, overlapping evidence).
- **single study**: one study only; displayed with that label.
- **contested**: credible evidence in both directions, or a credible published critique that changes the interpretation.
- **mixed**: several studies with inconsistent findings and no adequate explanation of the heterogeneity.
- **retraction-dependent**: a claim whose only support has been retracted; withdrawn on sight.

---

## 7. Contested questions (debate format)

Any claim flagged **contested** is presented in a fixed six-part box:

1. **The question**, in plain language.
2. **Strongest evidence that the answer is yes**, with study cards.
3. **Strongest evidence that the answer is no**, with study cards.
4. **What neither side's evidence can show**, by design.
5. **The editors' reading**, with the certainty rating and the reasoning.
6. **What would settle it.**

Both sides are written to the standard their own best proponents would accept. The editors' reading is the only place where the editors give their own answer to a contested question, and it is labeled as such; other editorial selections (the at-a-glance uncertainties, the priority research questions) are labeled as the editors' choice.

---

## 8. Monograph template

Every substance page has the same sections in the same order. Sections with no evidence say so rather than being omitted.

| # | Section | Content |
|---|---|---|
| 0 | Header | Name; verification status badge; version; dates of last search and last review; authors; conflicts of interest |
| 1 | At a glance | Class; mechanism in one line (resting on a section 3 claim; if the only such claim rests on narrative reviews, the line says that the mechanism is described second-hand and the claim is not otherwise shown in the box); legal status summary, dated; the three best-established facts, chosen by rule: claims that do not rest only on narrative reviews, ordered by certainty and then by independent replication (replicated, then replicated by the same team, then single study), with ties decided by relevance to people who use the drug, each shown with its own rating; the three largest uncertainties (very-low-certainty or contested claims that do not rest only on narrative reviews, chosen by the editors and labeled as their choice) |
| 2 | Identity and nomenclature | INN/IUPAC; synonyms; street names with region and date; forms and preparations; common adulterants and drug-checking findings |
| 3 | Pharmacology | Receptor and transporter pharmacology; pharmacokinetics by route (onset, peak, duration, half-life, metabolism, active metabolites); pharmacogenetics; mechanisms of drug–drug interactions |
| 4 | Neuroscience | Acute neural effects; human neuroimaging; electrophysiology; preclinical findings with translation limits |
| 5 | Effects | Subjective, cognitive and physiological effects as measured in controlled human studies, by dose range and route as reported; individual variability; **tolerance**, as a standard question on every page: how fast it develops with repeated use, how long it takes to return toward the starting level after use stops (including receptor measures from human imaging), and cross-tolerance with other drugs, each from human studies, with preclinical findings only where human evidence is absent and labelled as such |
| 6 | Acute risks | Toxicity and overdose syndrome and its recognition; interactions; contextual risks, including **lower tolerance than a person expects** (for example after release from prison, detoxification, treatment or another break), where studied; special populations (pregnancy, cardiac, psychiatric history, adolescence); emergency response evidence |
| 7 | Routes of administration and practical risk reduction | **Senior-author section.** Evidence on route-specific harms and on risk-reduction practices studied in the literature. Authored only by the senior author after legal review (§1.5) |
| 8 | Dependence and patterns of use | Dependence liability with conditional probabilities from population surveys; withdrawal syndrome; natural history, including remission without treatment; treatment-demand data |
| 9 | Long-term effects | Physical, psychiatric and cognitive outcomes, each with the full appraisal; reversibility data |
| 10 | Epidemiology | Prevalence by region and measure; trends; deaths with the coding definition; year-stamped |
| 11 | Harm-reduction interventions | Interventions with evidence for this substance (drug checking, naloxone, supervised consumption, outreach, substitution), each GRADE-rated |
| 12 | Treatment and therapeutic research | Treatments for the use disorder, its withdrawal and its complications (randomized trials first), and clinical trials of the substance itself as a medicine, where applicable |
| 13 | Legal status | Scheduling by jurisdiction, date-stamped |
| 14 | Contested questions | Debate boxes (§7) |
| 15 | Research gaps | The editors' priority questions, each with the study that would answer it; topics the page does not yet cover; then, generated, the debate boxes' open questions, the very-low-certainty claims (named by outcome and population, not by their findings) and each study card's 'what would settle it' |
| 16 | References | Generated from the claims on the page |
| 17 | Changelog | Versions and corrections (§13) |

**Site-wide pages.** The Emergency page and the interactions matrix are built from claims graded under §6 (for the matrix, claims about pairs of classes). Emergency guidance (signs, what to do, what not to do) is written or approved line by line by the senior author and is included in the legal review of §1.5; until then the page carries only verified emergency numbers (§10.3).

---

## 9. Language

- "People who use drugs", "person with [substance] use disorder", "use" and "non-medical use" rather than "addicts", "abusers", "abuse" or "junkies". "Abuse" appears only inside quoted titles, instrument names, institutional names and DSM-IV constructs reported as studied (Kelly & Westerhoff, 2010).
- "People who use [substance]" or, beside a control group, "the [substance] group", rather than "users" or "non-users", except in quoted titles, source headings used as locators, and official indicator names; "positive" or "negative" urine results rather than "dirty" or "clean".
- "Dependence" and "use disorder" are used in their DSM-5/ICD-11 senses and the instrument used in each source is named.
- "Overdose" is used for the clinical syndrome; "drug-induced death" and "overdose death" follow the coding definition of the source.
- Effects are described in the population and dose range in which they were observed, not generalized to "the drug".
- No adjectives of alarm or reassurance ("devastating", "harmless"). Magnitudes are numbers.

---

## 10. Epidemiology and statistics

### 10.1 Sources and hierarchy
UNODC World Drug Report; EUDA European Drug Report and Statistical Bulletin; US NSDUH; ESPAD; national surveys; peer-reviewed global burden estimates (e.g., GBD). Each figure carries: source, edition year, data year, measure (lifetime / past-year / past-month prevalence; incidence; deaths with coding), population and age range, and a link.

### 10.2 Rules
- No figure without all of the fields in §10.1.
- No rounding beyond the precision of the source; intervals reported when the source gives them.
- Denominators are stated. "X people died of Y" is always accompanied by the number of people who used Y in the same population and year where that number exists.
- Conditional probabilities of dependence are reported from the primary surveys (e.g., Anthony et al., 1994; Lopez-Quintero et al., 2011), per substance, with the instrument and follow-up window.
- The landing page shows only figures that meet these rules and is refreshed at every annual update.
- The sentence or table row a figure was checked against is kept in the data as the verification record; the site shows at most 15 consecutive words of it around the figure (§4.5).

### 10.3 Sourced facts
Identity and nomenclature (section 2), legal status (section 13), official statistics (§10) and the Emergency page's numbers are sourced facts, not graded claims: each names its source, the date read and how it was read (in the app's browser or through WebFetch, §12.1). Statuses: draft (compiled by the AI) → ai-checked (confirmed in a second source or by a second reader) → senior-verified (checked by the senior author); a statistic shown as "verified" has been checked by the AI against the source page on the date shown. Glossary definitions name their source.

---

## 11. Data model and tooling

- Content is structured data, not prose files: references (CSL-JSON), study cards, claims, monographs, epidemiology records, identity and legal tables, and the site tables (glossary, home figures), each validated against the JSON schemas in `schema/` where one exists.
- Source of truth: the project folder (`data/`, `schema/`, `scripts/`, `docs/`), kept under a local Git history in the working copy and copied, with that history, to the senior author's computer after each session; before launch it moves to a public repository whose history becomes the audit trail. Until then, superseded claim text survives only in the claims' changelogs and in the Git history.
- References are built from Crossref records by `scripts/build_references.py` (CSL-JSON); there is no reference manager. PDFs are stored in the project folder under `PDFs/<Substance>/`.
- Rendering: a static page generated by `site/build.js`; APA 7 is rendered by the prototype's own code until citeproc-js replaces it; claims, cards and anchors are rendered from the data files.
- Validation (`scripts/validate.py`) runs before every build. It fails on: schema errors; a claim without anchors; a located anchor with a placeholder; a quotation over 15 words or a second quotation in a claim; an unknown reference or study card; GRADE arithmetic; a claim above its rung on the ladder (§12), including anchors confirmed without an independent check (§5.5); a contested claim without a debate box; a narrative-only claim above draft or shown at a glance; risk-of-bias words outside the instrument's vocabulary; a study card above draft that fails the card checks (placeholders, missing source, abstract-only reading); a section 7 claim not written by the senior author; a descriptive claim upgraded for a large effect; a claim resting only on preclinical evidence rated above low; a senior decision made on an earlier claim version; a retracted reference. It warns on: unverified or retraction-unchecked references, language (§9), AMSTAR 2 items and design–instrument mismatches, unmarked provisional AMSTAR 2 ratings, upgrades of evidence rated down for bias without the strict reading, causal verbs at low certainty, section mismatches, key findings without a page, and every anchor not yet senior-verified. The prototype is deployed with draft content labeled as such; a monograph cannot reach `published` (§12) while any reference warning or any anchor below `senior-verified` remains.

---

## 12. Verification workflow and status

Each claim and each monograph displays its status.

| Status | Meaning |
|---|---|
| draft | Not yet on the ladder: an anchor is not yet located in a full text, or the claim rests only on narrative reviews (§6.3) |
| metadata-verified | All references verified against Crossref and retraction-checked |
| ai-anchored | Every evidence anchor located in the full text and confirmed by a second AI reader, blind or at the stated place (§5.5) |
| anchor-verified | Every evidence anchor checked against the source by the senior author |
| appraised | In addition, every study card the claim rests on has been read against its source by the senior author (card status `appraised`, §5.5) |
| senior-reviewed | Senior author has signed off on the claims, grades and text |
| published | Live, with version number |
| flagged | A post-publication issue is open (§13). A flag raised in senior review before publication is recorded in the claim's `senior_review` and does not change its status; the editor reworks the claim |

The ladder is cumulative: a claim reaches `ai-anchored` only from `metadata-verified`. Flagged claims show the flag publicly while the issue is open.

**Publication at launch (0.3.0).** A claim is published when the senior author has read and approved its answer and statement at its current version (`senior_review.decision` approved, with `claim_version` equal to the claim's version) and every anchor has been confirmed by a second AI reader (`ai-anchored`); a claim still at `draft` may appear only with its early-draft label. The approval is separate from the ladder: it does not mean the senior author has checked every anchor himself (`anchor-verified`). His own anchor checks continue after publication in the review queue, and each claim's stamp says how far its checks have gone. A changed claim loses its approval until he approves the new version. Section 7 claims still need his approval of each version before they appear (decision `p-ways-of-taking`).

### 12.1 Role of AI
The AI co-editor performs searches where it has access, fetches and checks metadata, reads full texts (the PDFs in the project folder, and free full texts in PubMed Central or on publishers' pages, read through the app's browser), produces first-pass study cards, evidence anchors, GRADE assessments and drafts, runs the independent second reading with a separate AI reader, and runs validation. It does not have the final word on any field. The site states this on the About page and on every monograph.

**WebFetch.** WebFetch (a fetch tool that answers through a summarizing model) is never used to read papers for study cards or anchors. It may be used (a) for bibliographic metadata, which becomes metadata-verified only when two independent fetches (for example `works/<DOI>` and a works search) agree on every field, or one agrees with a browser record; (b) for open-access status (routing a paper to the AI's reading list; a paper that turns out not to be free goes back to the senior author's list); (c) for short official facts on public pages (emergency numbers, scheduling entries), each confirmed in at least two sources, recorded as read through WebFetch, and kept at draft until the senior author's check. A retraction status is set only from a `works/<DOI>` record or a search that returns update links.

---

## 13. Versioning, updates and corrections

- Each monograph carries a semantic version: **major** when a conclusion or certainty rating changes; **minor** when evidence is added without changing conclusions; **patch** for wording and formatting. Before first publication (version 1.0.0) versions stay below 1: a change of conclusion or certainty raises the minor number and anything else the patch number. Claims carry their own versions on the same scheme.
- Every version is retained and viewable.
- **Update cadence:** a full re-search (§2) every 12 months, or sooner when a systematic review, a large trial, a retraction or a credible critique appears. The date of the last search is printed on the page.
- **Corrections:** reports are accepted through the error-report form (§15), which requires a DOI, PMID or page reference. The editors respond within 14 days. Accepted corrections are applied with a public entry in the monograph changelog and the site-wide correction log, stating what was wrong, what changed and why. The previous text remains in version history.

---

## 14. Interests and funding

- All editors declare conflicts of interest on the About page and on each monograph they author.
- The site does not accept funding from alcohol, tobacco, cannabis, pharmaceutical or drug-paraphernalia companies, or from organizations whose mission depends on a particular conclusion about drugs. Donations above a stated threshold are disclosed with the donor's name.
- The funding of every cited study is stored on its study card.

---

## 15. Community input

- **Error reports and source suggestions:** a form on every page, requiring a DOI, PMID or page reference. Triaged by the editors; outcomes logged.
- **Questions:** a moderated per-substance question board, opened after launch. Rules: no sourcing, buying or selling; no personal medical advice; no dosing advice from users to users; posts that describe an emergency receive emergency-service information.
- Contributors who submit accepted corrections are credited in the changelog if they wish.

---

## 16. Limitations of this protocol

- Database access is partial: PubMed is searched through its public interface and PsycInfo for result counts only; Scopus, Web of Science and ProQuest are not searched. Snowballing and multiple databases mitigate but do not remove the risk of missed studies.
- GRADE was built for intervention questions; its application to exposure and prognosis questions follows published guidance but involves judgment, which is why the domains are always shown.
- The three-reader rule has one human reader; the others are AI systems. Independent external review of each monograph is a goal for the second year after launch.
- The AI co-editor can misread a source; this is why no claim is senior-reviewed or published (§12) until the senior author has checked its evidence anchors against the source.

---

## References for this protocol

Anthony, J. C., Warner, L. A., & Kessler, R. C. (1994). Comparative epidemiology of dependence on tobacco, alcohol, controlled substances, and inhalants: Basic findings from the National Comorbidity Survey. *Experimental and Clinical Psychopharmacology, 2*(3), 244–268. https://doi.org/10.1037/1064-1297.2.3.244

Guyatt, G. H., Oxman, A. D., Vist, G. E., Kunz, R., Falck-Ytter, Y., Alonso-Coello, P., & Schünemann, H. J. (2008). GRADE: An emerging consensus on rating quality of evidence and strength of recommendations. *BMJ, 336*(7650), 924–926. https://doi.org/10.1136/bmj.39489.470347.AD

Higgins, J. P. T., Morgan, R. L., Rooney, A. A., Taylor, K. W., Thayer, K. A., Silva, R. A., Lemeris, C., Akl, E. A., Bateson, T. F., Berkman, N. D., Glenn, B. S., Hróbjartsson, A., LaKind, J. S., McAleenan, A., Meerpohl, J. J., Nachman, R. M., Obbagy, J. E., O'Connor, A., Radke, E. G., … Sterne, J. A. C. (2024). A tool to assess risk of bias in non-randomized follow-up studies of exposure effects (ROBINS-E). *Environment International, 186*, Article 108602. https://doi.org/10.1016/j.envint.2024.108602

Hooijmans, C. R., Rovers, M. M., de Vries, R. B. M., Leenaars, M., Ritskes-Hoitinga, M., & Langendam, M. W. (2014). SYRCLE’s risk of bias tool for animal studies. *BMC Medical Research Methodology, 14*(1), Article 43. https://doi.org/10.1186/1471-2288-14-43

Iorio, A., Spencer, F. A., Falavigna, M., Alba, C., Lang, E., Burnand, B., McGinn, T., Hayden, J., Williams, K., Shea, B., Wolff, R., Kujpers, T., Perel, P., Vandvik, P. O., Glasziou, P., Schunemann, H., & Guyatt, G. (2015). Use of GRADE for assessment of evidence about prognosis: Rating confidence in estimates of event rates in broad categories of patients. *BMJ, 350*, Article h870. https://doi.org/10.1136/bmj.h870

Kelly, J. F., & Westerhoff, C. M. (2010). Does it matter how we refer to individuals with substance-related conditions? A randomized study of two commonly used terms. *International Journal of Drug Policy, 21*(3), 202–207. https://doi.org/10.1016/j.drugpo.2009.10.010

Lopez-Quintero, C., Pérez de los Cobos, J., Hasin, D. S., Okuda, M., Wang, S., Grant, B. F., & Blanco, C. (2011). Probability and predictors of transition from first use to dependence on nicotine, alcohol, cannabis, and cocaine: Results of the National Epidemiologic Survey on Alcohol and Related Conditions (NESARC). *Drug and Alcohol Dependence, 115*(1–2), 120–130. https://doi.org/10.1016/j.drugalcdep.2010.11.004

Munn, Z., Moola, S., Lisy, K., Riitano, D., & Tufanaru, C. (2015). Methodological guidance for systematic reviews of observational epidemiological studies reporting prevalence and cumulative incidence data. *International Journal of Evidence-Based Healthcare, 13*(3), 147–153. https://doi.org/10.1097/xeb.0000000000000054

Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S. E., Chou, R., Glanville, J., Grimshaw, J. M., Hróbjartsson, A., Lalu, M. M., Li, T., Loder, E. W., Mayo-Wilson, E., McDonald, S., … Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. *BMJ, 372*, Article n71. https://doi.org/10.1136/bmj.n71

Schünemann, H., Brożek, J., Guyatt, G., & Oxman, A. (Eds.). (2013). *GRADE handbook: Handbook for grading the quality of evidence and the strength of recommendations using the GRADE approach* (Updated October 2013). https://gdt.gradepro.org/app/handbook/handbook.html

Schünemann, H. J., Oxman, A. D., Brozek, J., Glasziou, P., Jaeschke, R., Vist, G. E., Williams, J. W., Kunz, R., Craig, J., Montori, V. M., Bossuyt, P., & Guyatt, G. H. (2008). Grading quality of evidence and strength of recommendations for diagnostic tests and strategies. *BMJ, 336*(7653), 1106–1110. https://doi.org/10.1136/bmj.39500.677199.ae

Shea, B. J., Reeves, B. C., Wells, G., Thuku, M., Hamel, C., Moran, J., Moher, D., Tugwell, P., Welch, V., Kristjansson, E., & Henry, D. A. (2017). AMSTAR 2: A critical appraisal tool for systematic reviews that include randomised or non-randomised studies of healthcare interventions, or both. *BMJ, 358*, Article j4008. https://doi.org/10.1136/bmj.j4008

Sterne, J. A. C., Hernán, M. A., Reeves, B. C., Savović, J., Berkman, N. D., Viswanathan, M., Henry, D., Altman, D. G., Ansari, M. T., Boutron, I., Carpenter, J. R., Chan, A.-W., Churchill, R., Deeks, J. J., Hróbjartsson, A., Kirkham, J., Jüni, P., Loke, Y. K., Pigott, T. D., … Higgins, J. P. T. (2016). ROBINS-I: A tool for assessing risk of bias in non-randomised studies of interventions. *BMJ, 355*, Article i4919. https://doi.org/10.1136/bmj.i4919

Sterne, J. A. C., Savović, J., Page, M. J., Elbers, R. G., Blencowe, N. S., Boutron, I., Cates, C. J., Cheng, H.-Y., Corbett, M. S., Eldridge, S. M., Emberson, J. R., Hernán, M. A., Hopewell, S., Hróbjartsson, A., Junqueira, D. R., Jüni, P., Kirkham, J. J., Lasserson, T., Li, T., … Higgins, J. P. T. (2019). RoB 2: A revised tool for assessing risk of bias in randomised trials. *BMJ, 366*, Article l4898. https://doi.org/10.1136/bmj.l4898

Whiting, P. F., Rutjes, A. W. S., Westwood, M. E., Mallett, S., Deeks, J. J., Reitsma, J. B., Leeflang, M. M. G., Sterne, J. A. C., Bossuyt, P. M. M., & QUADAS-2 Group. (2011). QUADAS-2: A revised tool for the quality assessment of diagnostic accuracy studies. *Annals of Internal Medicine, 155*(8), 529–536. https://doi.org/10.7326/0003-4819-155-8-201110180-00009

*(Every entry except the GRADE Handbook is generated from its Crossref record in `data/references/` by the site's APA code (records verified 2026-10-14 to 2026-10-16, and on 2026-10-26 for Schünemann et al., 2008, whose rule for tests was read in its full text, PMC2386626, section "Study design" and Table 2; documented corrections in `data/access/metadata-overrides.json`: the ROBINS-I volume and the event-rates paper's article number from the publisher's pages, QUADAS-2's group author, SYRCLE's article number, and the NESARC survey's name kept as a proper noun). The GRADE Handbook has no DOI: its title, editors and update statement were read once through WebFetch on the official page on 2026-10-16 and stay draft until the senior author checks the page (§12.1).)*

### 12.2 The machine lane (0.4.0; official pages, summaries, amounts and the second look: 0.5.0)

At the senior author's instruction of 15 November 2026 the site also publishes answers written by a system of programs, without a person, before a person has checked them. His words: "it should be claims... and make them written as good as possible as close to 100% correct as possible and they should also be written in the language and format we write the rest of the website" (17:33); "it should be published and automatically deployed with a very discreet disclaimer and we should just be able to access everything that was automatically written and deployed to check whenever we want" (20:58); "if the automatic answer is not complete it should have a small discreet disclaimer" (20:58); "it should find more than one sources if they are relevant, whatever is relevant, the algorithm has to mimick completely how claude writes answers" (21:07). This is an exception to the rule of publication above and to the principle that nothing unverified is published. It holds only under the conditions below.

1. **Apart and marked.** A machine-lane answer is not a claim in the sense of §6: it is kept in `data/auto/answers`, never in `data/claims`, has no GRADE rating and no status on the ladder, and shows no certainty bars. Wherever it is shown it carries the line "Written by our system from N papers. Not yet checked by a person.", and "Not complete yet." where a paper that stands nearer the question could not be read. On a drug's page it stands in a section of its own; one page lists every such answer.
2. **The steps** (`scripts/auto/`; each is done by a model that did not do the one before, and each is followed by a gate that is code). *Find*: searches of Europe PMC, written into the repository as they were sent; Crossref for every reference (the record is made by `scripts/build_references.py`, never typed) and for retraction links. *Read*: a reader model reads the passages of one paper nearest the question; every finding must come with a part of the passage copied word for word, and a finding whose quote is not found in the passage, or that states a number its quote does not hold, is thrown away; in a single study the introduction is not read. *Write*: a writer model writes the short answer, the But and the How do we know? lines from the findings only, naming for each sentence the findings it rests on. *Check*: a different model reads each sentence beside the passages it rests on, without the writer's notes; a line it does not accept is dropped, and a short answer or a But it does not accept twice means there is no answer. *Rules*: code refuses amounts, doses, re-dosing, ways of taking compared for strength, making an effect stronger, advice, words that are not person-first, quotations, and any number that is not in the quotes. *Sources*: at least one review or meta-analysis, or two studies in people; never a retracted paper or one under an expression of concern.
3. **What waits for a person.** An answer to a question about dying, overdose, an emergency, mixing drugs, pregnancy, children or suicide is written and checked in the same way and is then not published by the system: it waits until a person releases it. Emergency guidance stays the senior author's own (§1).
4. **The models** are open models run within Cloudflare Workers AI's free allowance; each answer's record names the reader, the writer and the checker. They read and check less well than the AI co-editor. The lane's error rate is measured on our own blind checks (`scripts/auto/exam.py`, `exam_models.py`) and the result is kept in the repository; the senior author's goal is 1 wrong sentence in 1,000, and the measured rate is stated to him as it is.
5. **After publication.** The senior author reads these answers when he chooses; the page that lists them is his list. One that is wrong is taken down (`data/auto/held.json`). One that is to stay is taken through the checked lane (§5, §6) and then loses its label.
6. **Quotations and copyright.** The reader's quotes are kept in the private repository for checking and are never shown on the site (§4.5), except the quotation of an answer about amounts (point 9). Full texts are read where they are fetched and are not stored.
7. **Official bodies (0.5.0).** At the senior author's instruction of 15 November 2026 ("I want it to read official websites too where it can get access", 22:24; "official sites like NHS and EVERYTHING similar", 22:31) the lane also reads pages of official bodies, listed in `data/auto/official/sources.json`: health services, health ministries and agencies and UN and EU bodies (tier 1), and information services a government pays for (tier 2). Law-enforcement pages are not health sources and are not listed. A site is read only where its own robots.txt allows a reader that is not a browser, slowly and under the site's name; a refusal is taken as no and is never gone around (`scripts/auto/official.py`; which bodies can be read is found out on the machine that reads, `_probe.json`). A page is read like a paper (the same quotes, the same gates) and the answer names the body ("The NHS says"), so that a body's statement is never passed off as a research finding. Its reference is made by code from the page itself, in APA 7; a page that gives only the date of its last review is cited as n.d. with the day it was read. The gate on sources becomes: one review or meta-analysis read in full, or one page of a tier 1 body, or two of: a study in people, a review read in summary only, a tier 2 page.
8. **Summaries of papers behind a paywall (0.5.0).** The senior author, 22:40: "we can make everything answerable perfectly even with paywalled articles". What the lane may do: read the summary (abstract) that Europe PMC holds, which is free to read. An answer that rests on a summary says so in its line ("the summary of 1 paper"), is never "complete", and the paper stays on the list of papers wanted. Nothing goes around a paywall or a site that refuses.
9. **Amounts (0.5.0).** Until 15 November 2026 no machine-lane answer could hold an amount, and the editor's first rule was that an answer about amounts waits for the senior author. His decisions: "I want it to appear if it is cited by a valid website or scientific articles" (22:40); and, to the one hold the editor kept for opioids and GHB/GBL, "disclaimer then" (22:46). So: a question about amounts is answered by the system, without a writer model. The reader copies each amount stated for people with who received it and under what care; code keeps a row only if its quote stands in the source, holds a number with its unit, names no animal, no amount that harmed or killed, no amount added in the same session and no time between uses; a second model reads each row beside its passage; code cuts the quotation to 15 words at most (§4.5: one quotation for each row) and writes three fixed lines that no model can change (`data/auto/lane/lines.json`): that these are amounts reported by studies and official pages and not a recommendation; that each was for the people and the care named; and, first of all, for opioids that such amounts are often for people whose bodies are used to opioids and can kill a person who is not, and for GHB and GBL that the gap between an effect and stopped breathing is small. Amounts count only from a tier 1 body, a medicine's label, or a study in people. A question about which amount kills is a question about dying and waits for a person (point 3), as do amounts for pregnancy or children. Answers to other questions hold no amounts; the checked lane's rule (no dosing, administration or potentiation guidance; the doses section is the senior author's text) is unchanged.
10. **The second look (0.5.0).** The senior author, 22:54 and 22:55: the system "should be able to update or criticize answers" that conflict with other findings or are wrong, "and either adjust, delete or add new claims"; "it should not only add but change towards being complete". Its own answers: when more can be read for a question, when a source is retracted, or when an answer is not complete, the lane writes the answer again or takes it down; the record keeps what the answer was before (`history`). Checked claims: the system never edits one. Where it finds research that conflicts with a checked claim it writes the conflict down with the sentences on both sides and a proposed change, which goes through the checked lane's checks (§5, §6).

---

## Changelog

- **0.1.0 (2026-10-14)** — Initial pre-registration draft.
- **0.2.0 (2026-10-15)** — Before any claim left draft: (1) verbatim evidence excerpts replaced by **evidence anchors** (page, locator, extracted data in the editors' words; quotations limited to 15 words and one per claim) for copyright reasons and because numbers at a location are what get verified (§4.5, §6.2); (2) the two-reader rule became a **three-reader rule** with an independent AI second reader before the senior author (§5.5), and study cards now record what was read and any reporting issues found; (3) PubMed Central full texts read through the browser are accepted as full-text sources alongside PDFs (§12.1); (4) verification statuses `ai-anchored` and `anchor-verified` replace `excerpt-verified` (§12). No published content existed, so nothing was changed retroactively.
- **0.2.1 (2026-10-16)** — (1) The second reader's procedure is specified: blind extraction per claim before opening the first reader's card, then card checking; anchors are matched by script and disagreements go to the senior author (§5.5). (2) The first reader's mechanical number check for PDF anchors (§5.5). (3) The senior author's review queue in the site (§5.5, §12). (4) Rules for applying GRADE to association claims, large effects, overlapping evidence and editors' calculations, with arithmetic checked by the validator (§6.3). (5) Free papers on ScienceDirect, which refuses the app's browser, are obtained by the senior author like paywalled ones (WORKFLOW). (6) Section 12 widened to "Treatment and therapeutic research": the template had no home for treatments of the use disorder (§8); for the senior author's confirmation. No claim had left draft, so nothing was changed retroactively.
- **0.2.2 (2026-10-16)** — (1) Each risk-of-bias instrument keeps its own vocabulary, the overall judgment is never less severe than the worst domain, and both are checked by the validator; two documented extensions (AMSTAR 2 "no information" for unread supplements, JBI "partial yes"); 22 mislabelled judgments on methamphetamine cards corrected and logged on the cards (§5.3). (2) Narrative reviews are appraised with the editors' narrative-review checklist, not AMSTAR 2, and are never primary evidence (§5.3). (3) New status flag **replicated by the same team** for agreement within one group (§6.4). (4) An independent methodologist review of every claim, by AI reviewers who had not seen the drafting, before the senior author's review (`docs/REVIEW-BRIEF.md`). No claim had left draft, so nothing was changed retroactively.
- **0.2.3 (2026-10-16)** — After review round 1 (all 32 methamphetamine claims), four rules made explicit (§6.3): descriptive claims are never upgraded for large effect; an upgrade of evidence already rated down for risk of bias is stated with the strict reading's certainty; claims resting only on narrative reviews stay at draft (validator); and the instrument must match the design (§5.3, checked by script), including AMSTAR 2's item-specific responses. The at-a-glance box is filled by a stated rule and shows each claim's rating, and the research-gaps section leads with curated questions (§8). Applied to the methamphetamine monograph (v0.3.0): two claims lowered from moderate to low; no claim had left draft.
- **0.2.4 (2026-10-16)** — After an independent audit of this protocol against the briefs, the site and the scripts (`data/verification/methods-audit-2026-10-16.md`, 51 findings), the text now says what practice is, and the practice was corrected where the text was right: (1) **Targeted checks** (§5.5): anchors that the blind second reading did not re-find, or that the editor added later, are checked at the stated place by a second reader and labeled so; this rule entered §5.5 between 0.2.1 and 0.2.3 without a changelog entry, which this entry corrects. 86 methamphetamine anchors were confirmed this way. An anchor written by the second reader needs independent confirmation; the editor's own check does not count, so two such checks were redone by an independent reader and four anchors were set back to located until checked (the validator now enforces this). (2) **Card status** (§5.5): a card is `ai-checked` when its findings have been confirmed or corrected against the source and the readers agree on the overall risk-of-bias judgment; one card with an open overall disagreement returned to first-pass, and four cards written from abstracts in the first prototype were returned to draft. (3) **The ladder** (§12): draft means "not yet on the ladder"; appraised requires the senior author's reading of every card; a flag raised in review does not change status; the senior decision is tied to the claim version. (4) **Further AI checks** (§5.6), **locators** (§6.2), **full-text sources** (§5.5, §12.1) and **WebFetch** (§12.1) are described. (5) For the senior author's confirmation: PubMed searched by the AI through E-utilities (§2.1); start levels for counterbalanced laboratory studies and for second-hand evidence (§6.3); counting replication inside meta-analyses (§6.4); the relation `describes` for descriptive claims (§6.1); the editors' qualitative checklist (§5.3). (6) The at-a-glance box no longer shows a claim resting only on narrative reviews, and the mechanism line says when it is second-hand (§8). (7) Sourced facts (§10.3), site-wide pages (§8), versioning before 1.0 (§13), the users/urine wording (§9), the validation list (§11), and the statistics quotation limit (§10.2) are stated. No claim had been signed off by the senior author, so nothing was changed retroactively.
- **0.2.5 (2026-10-16)** — No rule changed. (1) The references for this protocol are complete: every one cited in the text is listed, generated from its verified Crossref record by the site's APA code, with documented corrections; the GRADE Handbook, which has no DOI, is listed as read once from its official page and stays draft until checked. (2) Identity sections record how each source was read (`read_via`), and pages that were not read are kept out of the sources (§10.3). (3) Facts from papers read only through WebFetch are held back from the site until the paper is read in full (§12.1).
- **0.2.6 (2026-10-17)** — For the senior author's confirmation. At the senior author's request, tolerance becomes a standard question on every page (§8, section 5: how fast it develops, how long it takes to return toward baseline after stopping, cross-tolerance), and lower-than-expected tolerance (for example after prison or detoxification) is named among the contextual risks of section 6. Like every other topic it is reported from human studies, as findings and never as advice on amounts. A cross-cutting evidence map for tolerance is being built (`search-logs/_Tolerance_DOI-LIST.md`). (2) A third way a second reader confirms an anchor (§5.5): an anchor written after the second reader's card check, whose number and place match a key finding that reader confirmed at the stated place, is ai-checked with check mode 'card-check' and shown, like a targeted check, as checked at the stated place. No other rule changed.
- **0.2.7 (2026-10-19)** — For the senior author's confirmation (decision `p-public-reports`). Evidence reports by public bodies get their own design, `evidence-report`, and checklist, `editors-report` (§2.3, §5.3): they grade conclusions by stated rules and are externally reviewed, but most publish no reproducible search, so filing them as narrative reviews kept every claim resting on them at draft. Their graded wording is cited as the body's judgment. Also: section 7 comparisons of forms and routes may be drafted by the AI as findings only and stay off the site until the senior author approves each version (decision `p-ways-of-taking`; WORKFLOW step 12).
- **0.3.0 (2026-10-25)** — Launch, at the senior author's instruction. A claim may be published once he has read and approved its answer at its current version and every anchor has been confirmed by a second AI reader; his own checks of each anchor against the source continue after publication and are shown on each claim (§12). Before this version, publication required every anchor to be checked by the senior author. His approval of 25 October 2026 covers the 168 answers then on the preview; the 41 section 7 answers still need his approval of each version.
- **0.3.1 (2026-10-26)** — For the senior author's confirmation (decision `p-test-accuracy`), before the drug-checking answers were written. Studies that compare a test with a reference method get their own design, `test-accuracy`, appraised with QUADAS-2 (§5.3); four first readers had noted that the card schema had no such design and filed these studies as `in-vitro`, which the preclinical rule (§5.4) would have capped at low certainty whatever their quality. Claims about a test's accuracy are rated as GRADE rates tests, starting high and rated down for risk of bias, indirectness and imprecision, and take the relation `describes` (§6.3); whether testing changes behaviour or prevents overdoses stays a separate question, rated from studies of people. Seven drug-checking cards were re-filed under the new design (logged on each card); no judgment was changed.
- **0.3.2 (2026-11-13)** — At the senior author's instruction (13 November 2026: the draft line "reduces rigor; I check everything"): pages no longer carry a draft banner, and answers no longer carry the stamp "Draft: not yet checked by our editor". The senior author holds editorial responsibility for everything published. Each answer's check stamp still says how far its checks have gone ("Sources checked by a second AI reader", "Approved by our editor", "Checked by our editor"), the About page still says how answers are made, and the footer and About page still say that the site is information, not medical advice. The publication rule of 0.3.0 is otherwise unchanged: a claim is shown only in a version whose anchors a second reader has checked, and section 7 claims only in a version he has approved.
- **0.5.0 (2026-11-15)** — At the senior author's instruction (15 November 2026, 22:24 to 22:55; his words are in §12.2 and in `docs/AUTOMATION.md`): the machine lane also reads **pages of official health bodies** where a site allows it, and the **summaries of papers behind a paywall**; it answers **questions about amounts** in the sources' own words under fixed lines (his decisions of 22:40 and 22:46, which replace the editor's rule that such answers wait for him); and it **goes back to its own answers** to complete or withdraw them, while a checked claim is changed only through the checks (§12.2, points 7 to 10). Nothing changes for the checked lane.
- **0.4.0 (2026-11-15)** — At the senior author's instruction (15 November 2026, 17:33, 20:58 and 21:07; his words are in §12.2 and in `docs/AUTOMATION.md`): **the machine lane**. Answers written by a system of programs from papers it found and read are published before a person has checked them, kept apart from the claims, each with the line "Written by our system from N papers. Not yet checked by a person." and without certainty bars; every sentence must rest on words copied from the paper, be accepted by a second, different model, and pass the site's content rules in code; questions about dying, overdose, emergencies, mixing drugs, pregnancy, children or suicide are not published by the system (§12.2). Nothing changes for the checked lane.
