# Alcohol, Tier A: claim writers (round `alc-a-2026-10-27`)

You write graded answers (claims) for Pharmakon, an evidence library about drugs for the public and for people who use
drugs. Project: `/home/claude/drug-encyclopedia`. Scratch folder:
`/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/` (`scratchpad/` below); your own folder
is `scratchpad/alc-a/w<N>/` (N = your reader number).

## The task

The Alcohol page so far answers questions about the day after drinking and sleep. First readers have now written study
cards for its 37 core papers (Tier A of `search-logs/Alcohol_DOI-LIST.md`). You turn the cards into claims (WORKFLOW
step 7), one claim per question a person would ask. Blind second readers will later re-find your evidence in the
sources, so every number must be right and anchored.

## Read first (only these parts)

1. `scratchpad/batch5/LEAN-RULES.md`: follow it.
2. `docs/WRITING-RULES.md`: Rule 0 and Rule 0b, "One page, three depths", "The answer format", "Sentence rules".
3. `docs/METHODS.md` §6 (all of it), §7 (debate box), §8 (the section numbers), §9 (language), §5.5 point 1.
4. Models, printed by id with `json.load` (never read whole files): claim `cl_fent_withdrawal_severity`
   (`data/claims/fentanyl-and-analogues.json`), contested claim with a debate box `cl_nic_snus`
   (`data/claims/nicotine.json`), and from this week `cl_dc_law_deaths` and `cl_dc_caution_harms`
   (`data/claims/drug-checking.json`). Your claims start at version 0.1.0 with one changelog line and `verification`
   `{"status": "draft", "drafted_by": "AI reader <N> (claim writer)", "drafted_on": "<today>"}`. Plain lines: entries
   `cl_meth_dependence_baserate` and `cl_dc_law_deaths` in `data/site/simple.json` → `claims`.
5. The cards: `data/study-cards/_incoming/alcohol/<card id>.json` (first-pass; print the ones you need). Each has
   `key_findings` with page, locator and data, `reporting_issues`, `risk_of_bias`, `interpretation_gap`, and the
   reader's notes on reference groups and units. Respect the reporting issues the first readers found.

## Where everything goes

- `substance`: `alcohol`. `section` per METHODS §8: long-term effects (death rates, heart, cancer, liver) 9;
  prevalence, trends and deaths caused 10; dependence and withdrawal 8; treatment of the disorder and of withdrawal 12;
  pregnancy: drinking in pregnancy 10, effects on the child 9. Never section 7.
- Claims: a JSON list in `data/claims/_incoming/alc_w<N>.json` (validate with the jsonschema line in LEAN-RULES).
- Questions and plain lines: `scratchpad/alc-a/w<N>/simple.json`: `{"<claim id>": {"q": "...", "short": "...", "but":
  "...", "how": ["...", "..."], "freq": {...optional}}}`. `short` about 14 everyday words; `but` the single most
  important limit; `how` 2 to 4 points; reading age 8 to 11; name the comparison group; never more than the claim.
- Report: `scratchpad/alc-a/w<N>/report.md` (at most 500 words): per claim what it rests on and its certainty, what is
  missing, and any card error you found (do not edit cards). Final message under 200 words.

## Anchors

- Each anchor: `reference`, `study_card`, `page`, `locator`, `extracted` (the data in your own words), `role`
  (supports, contradicts, qualifies), `anchor_status` `ai-located`, `located_by`, `located_on`, `source_read`.
- **PDF papers** (the senior author's: `stockwell_2024`, `di-castelnuovo_2006`, `mukamal_2020`, `rehm_2010`,
  `askgaard_2015`, `carvalho_2019`, `rehm_2009`, `mayo-smith_1997`, `jonas_2014`, `schuckit_2014`, `anton_2006`,
  `jones_1973`): find every number yourself in the PDF text, not only on the card. Texts: `scratchpad/alc-a/numtext/`;
  PDFs: `/mnt/user-data/uploads/DrugEncyclopedia/PDFs/Alcohol/`. `page` is the printed page (see the card for online-
  first or scanned PDFs). `located_by`: `AI reader <N> (claim writer)`; `source_read`: "PDF PDFs/Alcohol/<file>.pdf".
  Before you finish, run `python3 -I scripts/check_anchor_numbers.py scratchpad/alc-a/numtext data/claims/_incoming/alc_w<N>.json`
  and fix or explain every number it cannot find.
- **Web papers** (the rest, read in PubMed Central or at the publisher): take the anchor from the card's key finding
  (page `PMC HTML` or `publisher HTML`, the card's locator); set `located_by` to `AI reader <N> (claim writer), from AI
  reader <M>'s study card` and `source_read` to the card's source. Do not open the browser.
- Quote at most 15 words, at most one per claim, only where the wording is the evidence.

## Grading (METHODS §6.3)

- Observational evidence (cohorts, pooled cohorts, case-control, surveys, meta-analyses of them) starts **low**.
  Mendelian randomization studies are observational too: they start low; say in the reasoning what the genetic design
  does and does not protect against (it addresses some confounding; pleiotropy, weak instruments, selection and the
  inability to show a curve at low intake remain) and whether that justifies not rating down for confounding. The
  editor will log this rule for the senior author.
- Randomized trials and meta-analyses of them start **high** (withdrawal and treatment questions).
- Modelling studies (Global Burden of Disease, attributable-burden estimates) are not graded as evidence of an effect:
  use them for "how many deaths or cancers are estimated to be caused", say they are model estimates resting on
  relative-risk curves from other studies, and grade the claim from the evidence behind those curves.
- Reviews and the studies inside them are not independent: count each study once (for example, the mortality
  meta-analyses largely share their cohorts; Stockwell 2016 and Zhao 2023 are the same group's analyses; the liver
  meta-analyses overlap). Say so.
- Claims resting only on narrative reviews or commentaries (Burton & Sheron 2018, Chikritzhs 2015, Mukamal et al. 2020,
  Carvalho et al. 2019, Schuckit 2014) stay at draft and say their figures are second-hand (§6.3); use them to
  qualify, to frame a debate box, or for a definition.
- Status flags per §6.4. A claim whose evidence points both ways, or that a credible critique changes, is `contested`
  and carries the six-part debate box (§7). The question whether a little drinking is good for health is the obvious
  candidate: weigh the J-curve meta-analysis and the observational heart findings against the abstainer-bias and
  genetic studies, without taking a side the evidence does not support.

## Hard rules for this topic

- Findings only: no advice on how much to drink, no "safe limit" recommendations of your own, no withdrawal regimens or
  medicine doses. When a paper gives a guideline or a limit, you may say what it recommended and on what evidence.
- Name each estimate's **reference group** (lifetime abstainers, current non-drinkers including former drinkers,
  occasional drinkers, the lowest-intake drinkers) and its **units** (grams of ethanol per day or week, the paper's
  "drink"); give a standard drink in grams where the paper defines it. Absolute numbers before relative ones; counts out
  of 100 (or 1,000, or 100,000 for deaths) with denominators; editors' calculations labelled.
- Person-first words ("people who drink", "people with alcohol use disorder"); no words of alarm or reassurance; no
  country featured beyond what the study covers.

---

## Your questions

Ids start `cl_alc_`. Merge or split where the evidence demands, and say why in the report.

### Reader 170: is a little drinking good for you?
Cards: `sc_di_castelnuovo_2006`, `sc_stockwell_2016`, `sc_stockwell_2024`, `sc_zhao_2023`, `sc_wood_2018`,
`sc_chikritzhs_2015`, `sc_griswold_2018`, `sc_burton_2018`, `sc_bryazka_2022`.
1. Do people who drink a little live longer than people who do not drink? (the J-curve and the abstainer-bias
   critique; a debate box if contested)
2. Is there an amount of alcohol with no health risk? (GBD 2016 and GBD 2020; what "lowest risk" means, by age)
3. At what amount does drinking start to shorten life, among people who drink?

### Reader 171: the heart and blood vessels
Cards: `sc_ronksley_2011`, `sc_roerecke_2012`, `sc_roerecke_2014`, `sc_holmes_2014`, `sc_millwood_2019`,
`sc_biddinger_2022`, `sc_larsson_2020`, `sc_mukamal_2020`, and the heart findings of `sc_griswold_2018`.
1. Do studies find less heart disease in people who drink a little than in people who do not drink?
2. What do studies that use genes find about alcohol and heart disease? (with the published critique)
3. Does heavy drinking on some days change the heart risk of people who drink?
4. Does drinking raise the risk of stroke, high blood pressure or other blood-vessel disease? (only what the cards
   support)

### Reader 172: cancer, the liver, and deaths
Cards: `sc_bagnardi_2015`, `sc_rumgay_2021`, `sc_rehm_2010`, `sc_roerecke_2019`, `sc_askgaard_2015`, `sc_rehm_2009`,
and the death estimates of `sc_griswold_2018`.
1. Does drinking raise the risk of cancer, and does a little drinking? (which cancers)
2. How many cancers are estimated to be caused by alcohol?
3. How much drinking raises the risk of liver cirrhosis, and is it different for women and men?
4. Does drinking every day harm the liver more than drinking the same amount on fewer days?
5. How many deaths are estimated to be caused by alcohol worldwide?

### Reader 173: alcohol use disorder, withdrawal and treatment
Cards: `sc_grant_2015`, `sc_grant_2017`, `sc_carvalho_2019`, `sc_schuckit_2014`, `sc_mayo_smith_1997`,
`sc_amato_2010`, `sc_jonas_2014`, `sc_mcpheeters_2023`, `sc_rosner_2010a`, `sc_rosner_2010b`, `sc_anton_2006`.
1. How common is alcohol use disorder, and how many people with it get treatment?
2. What is delirium tremens, how often does it happen during withdrawal, and how serious is it?
3. Do medicines make stopping drinking safer (seizures, delirium)? (findings only, no regimens)
4. Do medicines help people with alcohol use disorder drink less or stop? (which medicines, how much, compared with
   what)
5. Does adding talking therapy to medicine help more? (the COMBINE trial)

### Reader 174: drinking in pregnancy
Cards: `sc_popova_2017`, `sc_lange_2017`, `sc_jones_1973`.
1. How many people drink alcohol while pregnant?
2. How common is fetal alcohol spectrum disorder, and fetal alcohol syndrome?
3. Only if the cards support it: what were the first described signs of fetal alcohol syndrome, and in whom?
