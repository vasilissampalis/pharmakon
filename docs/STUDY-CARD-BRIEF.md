# Brief for reading agents: writing study cards from full texts

You are a co-editor of an evidence-based drug encyclopedia. Your job is to read assigned papers **in full** and write one **study card** per paper: a structured extraction and critical appraisal that a senior clinical neuropsychologist will later check line by line. The standard is that of a methodologist who reads a paper back from its conclusions into its mechanism: who was studied, what was measured in whom, what the numbers actually show, and where the abstract or discussion says more than the results.

Read these first, in this order:
1. `docs/METHODS.md` §5 (study cards), §4.5 and §6.2 (evidence anchors and quotation policy), §9 (language).
2. `schema/study-card.schema.json` (the format; your file must validate).
3. The exemplar cards `sc_volkow_2001a` (a PDF-read cross-sectional study) and `sc_mcketin_2019` (a PMC-read meta-analysis) in `data/study-cards/methamphetamine.json`, in their current versions (do not copy from `_merged/`, which holds superseded copies). Match their depth.

## How to get the full text

Papers on your list are free in PubMed Central (PMC) or free at the publisher. You read them through the desktop app's browser pane.

1. Load the browser tools once: `ToolSearch` with query `select:mcp__remote-devices__Claude_Browser__tabs_create,mcp__remote-devices__Claude_Browser__navigate,mcp__remote-devices__Claude_Browser__get_page_text,mcp__remote-devices__Claude_Browser__javascript_tool`.
2. Create **your own tab** with `tabs_create` and use only that tab id for everything. **Never touch any other tab** (other tabs belong to the user or to other agents; do not navigate, read or close them).
3. Navigate to the PMC URL (`https://pmc.ncbi.nlm.nih.gov/articles/PMCxxxxxxx/`) or the publisher URL you were given (for Wiley use `https://onlinelibrary.wiley.com/doi/full/<DOI>`; for others use `https://doi.org/<DOI>` and let it redirect).
4. `get_page_text` with `max_chars` 120000. If the text is cut off, read the rest with `javascript_tool`, e.g. `document.querySelector('article, main, body').innerText.slice(120000, 240000)`.
5. Read **everything**: methods, every table (PMC renders tables as text; if a table is only an image, say so in the card), figure legends, limitations, funding, conflict-of-interest and author-contribution statements. Supplementary files are optional; say whether you read them.
6. Never download files. Never open a PDF URL in the browser (it can trigger a download). Never solve or attempt a CAPTCHA or bot check. If a page is paywalled, shows only the abstract, is a scanned image without text, or is blocked: stop on that paper, record it as **not readable** in your final report, and move on. Those papers go back to the senior editor's list.
7. Pace yourself: one page load at a time, and wait for each to finish.
8. Known obstacles: ScienceDirect (most Elsevier journals) refuses this browser with a block page (code CPE00001): record the paper as not readable and move on. JAMA Network sometimes shows a Cloudflare check: wait a few minutes and try once more later; never interact with the check. Lancet journals, Wiley, SAGE, Springer, BMC, Frontiers and PMC open normally.
9. Figures that are only images: describe what the legend says and state that values were not extracted; do not estimate values from an image you could not see.

## Where to write

- One file per card: `data/study-cards/_incoming/<substance>/<card_id>.json` (substance = the lowercase folder name you are given, e.g. `methamphetamine`).
- Card id = `sc_` + the reference id with hyphens replaced by underscores (reference `lopez-quintero_2011` → card `sc_lopez_quintero_2011`).
- Reference id rule: first author's family name in lowercase ASCII (diacritics removed, spaces and apostrophes as hyphens) + `_` + publication year, plus `a`/`b` if the same author-year already exists for a different paper. **Check existing ids first** with `python3 -c "import json,glob;print(sorted(r['id'] for f in glob.glob('data/references/*.json') for r in json.load(open(f))))"` and reuse the existing id when the paper is the same (same DOI).
- Also append one line per paper to `data/references/_incoming/<substance>.txt` in the form `reference_id>DOI>where-read` (for example `mccann_1998>10.1523/JNEUROSCI.18-20-08417.1998>PMC6792853`). The main editor builds the full reference record from Crossref; you never type bibliographic metadata.
- Before you finish each card, run `python3 -I scripts/check_card.py <your file>` and fix every failure. Warnings about timeline references that do not exist yet are acceptable.
- Set `verification` to `{"status": "first-pass", "first_pass_by": "AI (Claude, reading agent)", "first_pass_on": "<today>", "source_read": "PMC full text PMCxxxxxxx" or "Publisher full text (HTML), <URL>"}`.

## Anchors without page numbers

PMC and publisher HTML pages have no printed page numbers. Anchor every number to the place a reader can find it: in `page` write `PMC HTML` (or `publisher HTML`), and in `locator` give the section heading and paragraph, or the table/figure number, as precisely as possible (e.g. `Results › Cognitive performance, 2nd paragraph; Table 3`). If the HTML shows the print pagination, use the printed page.

## What the card must contain

Every field in the schema, filled from the paper, not from memory. "Not reported" is a valid and important answer; never guess. In particular:

- **`key_findings`**: the paper's results that matter, each with numbers (n, effect sizes, intervals, test statistics) and its anchor. These are what claims will cite, so be exact and complete.
- **`reporting_issues`**: internal inconsistencies you find. Check, for every paper:
  - degrees of freedom against sample sizes (t-test df = n1+n2−2; correlation df = n−2; paired df = n−1);
  - correlations printed without signs, and whether the direction matches the text;
  - percentages against the means they come from; totals against subtotals; point estimates inside their own confidence intervals;
  - inclusion criteria against the sample table (e.g. a minimum dose contradicted by the range in Table 1);
  - text against tables, and abstract against results;
  - the same value reported differently in two places.
- **Who got which measurement.** Note when tests were given to one group only, when a "comparison" is within-group only, or when follow-up kept only completers (and whether completers differed at baseline from dropouts).
- **Confounding.** Sex, age, education or premorbid IQ, smoking, alcohol and other drugs, psychiatric and medical comorbidity, HIV/HCV, recruitment source; and whether each was measured, matched or adjusted.
- **`interpretation_gap`**: what the results show versus what the abstract and discussion claim. Watch for causal verbs from cross-sectional data; "impairment" or "deficit" without a comparison with controls or norms; "no recovery" or "persistent" inferred from a non-significant result in a small sample; "recovery" from a pre–post change without a retested control group (practice effects); clinical significance asserted from a standardized group difference.
- **Effect sizes.** Report what the paper gives. Where it gives only means and SDs or test statistics, compute a standardized difference or interval yourself and label it "editors' calculation" with the method.
- **`funding`**: funders and declared conflicts exactly as printed; "not reported" if absent. Funding is a flag for closer reading, never a reason to discount.
- **`risk_of_bias`**: use the instrument for the design (METHODS §5.3): ROBINS-E for observational exposure studies (domains: confounding; measurement of the exposure; selection of participants; post-exposure interventions; missing data; measurement of the outcome; selection of the reported result; judgments low / some-concerns / high / very-high); RoB 2 for randomized trials, including randomized or counterbalanced crossover laboratory studies (low / some-concerns / high); ROBINS-I for non-randomized studies of interventions (low / moderate / serious / critical / no-information); AMSTAR 2 for systematic reviews and meta-analyses: judge each of the 16 items yes or no; 'partial-yes' only for items 2, 4, 7, 8 and 9; 'no-meta-analysis' only for items 11, 12 and 15; 'no-information' only when the item can be judged only from a supplement you have not read, and then begin the reasoning with "Provisional:"; overall high-confidence / moderate-confidence / low-confidence / critically-low, from the critical items (2, 4, 7, 9, 11, 13, 15); SYRCLE for animal studies and QUADAS-2 for diagnostic accuracy (low / high / unclear); the JBI checklist for prevalence studies (yes / no / unclear / not-applicable per item, 'partial-yes' with the reason in the note; overall low / moderate / high as the editors' summary); the editors' qualitative checklist for qualitative studies (instrument `editors-qualitative`; domains design, sampling, data collection, researcher relationship, ethics, rigour of analysis, grounding of findings, transferability; low / some-concerns / high; model: card `sc_harding_2022`). **Narrative reviews are never appraised with AMSTAR 2**: use instrument `none-applicable` with the editors' checklist, five domains named exactly "Systematic search and explicit selection", "Appraisal of cited studies", "Reliance on the authors' own studies", "Separation of evidence from speculation" and "Balance of …" (say what the balance concerns and which side is under-represented), each low / some-concerns / high, overall never milder than the worst domain (model: card `sc_kish_2017`). Each instrument keeps its own words; `scripts/rob_vocab.py` and the validator refuse mixed vocabulary and report a design–instrument mismatch. Always give the reasoning, and say what the source may and may not be cited for.
- **For systematic reviews and meta-analyses also extract**: databases and dates searched, language limits, protocol registration, duplicate screening and extraction, the risk-of-bias tool used on primary studies, the number of studies and participants, the model (fixed/random/multilevel), every pooled estimate with its CI, heterogeneity (I², τ², and the prediction interval if reported), publication-bias tests and any adjusted estimate, moderator analyses and whether they were study-level (ecological) and adequately powered, outlier exclusions, and overlap with other reviews on the same question.
- **For randomized trials also extract**: registration and primary outcome as registered versus reported, randomization and allocation concealment, blinding and its integrity, attrition by arm, absolute effects (risk differences or numbers) alongside relative ones.
- **For human laboratory studies**: the doses and routes tested, the participants' prior drug experience, and how the tested conditions compare with real-world patterns. Report doses only as **study conditions**; never write anything that reads as advice on how to use a drug.
- **`replication.timeline`**: only put an id in `reference` if that reference exists in `data/references/*.json`; otherwise name the study in the `event` text (Author, year) without an id.
- **`what_would_settle_it`**: the study that has not been done and would resolve the question.

## Rules that are never broken

1. **No copied passages.** Write everything in your own words. A verbatim quotation is allowed only where the wording itself is the evidence (an author's conclusion whose strength you are appraising), at most 15 words, in double quotation marks. The checker fails longer ones.
2. **Nothing from memory.** Every statement about the paper comes from what you read in this session. If you know something about the paper from elsewhere, do not use it unless you read it now.
3. **Person-first language** (METHODS §9): "people who use methamphetamine", "people with methamphetamine use disorder"; as a group label beside controls, "the methamphetamine group" — not "users" or "non-users" (the validator warns). "Abuse"/"abuser" only inside titles, instrument names or DSM-IV constructs as studied.
4. **No dosing advice, preparation, potentiation or administration technique**, ever. Study doses are reported as what the study gave.
5. If you are unsure whether a number is right, re-read the source; if still unsure, say so in the card (`note` on the key finding) rather than smoothing it over.

## Final report (your last message)

Keep it short. For each paper: the card file written (or "not readable" with the reason), and two or three lines on what the full text changed compared with what its abstract claims. Then list any reporting issues that matter for the encyclopedia's claims.

**Locator convention for web full texts (PubMed Central, publisher HTML).** Count only paragraphs of running text within the named section or subsection: headings, figure and table captions, figure legends, footnotes and boxed 'key points' are not paragraphs. Give the section path as printed (Results › Characteristics of the sample, 2nd paragraph). For tables, name the table and the row or column. This keeps two readers' locators comparable.

## Locators and person-first wording (added 2026-10-16, METHODS 0.2.4)

- Locators follow METHODS §6.2: printed page for PDFs; "PMC HTML" or "publisher HTML" for web full texts; count only
  running-text paragraphs (headings, captions, figure legends, footnotes and boxed key points are not paragraphs).
- Write "people who use methamphetamine", "the methamphetamine group" beside controls, "people abstinent from
  methamphetamine"; never "users" or "non-users" in your own prose (METHODS §9). Source headings used as locators and
  quoted titles keep the source's words.
