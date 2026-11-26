# Claim writers for the papers saved on 26 November 2026 (round `pdf-2026-11-26`)

You write graded answers (claims), their plain lines and myth-or-fact items for Pharmakon (https://pharmakon.world), an
evidence library about drugs for the public and for people who use drugs. Project: `/home/claude/pharmakon` (read
`CLAUDE.md` there first, above all "Demand first"). Scratch folder: `/tmp/claude-0/-home-claude/26a1fab4-6c74-5648-a9fc-9f33a45fba6c/scratchpad/pdf1126/w<N>/`
(N = your reader number; create it; it is not saved).

## Your procedure

Follow `data/verification/pdf-2026-11-14/BRIEF-claim-writers.md` exactly for everything general: "Read first", "Hard rules",
"Where everything goes" and "Grading". In it read, everywhere: round `pdf-2026-11-26` for `pdf-2026-11-14`; new claims in
`data/claims/_incoming/pdf1126_w<N>.json`; patches in `data/claims/_incoming/patch_pdf1126_w<N>.json` with `change`
beginning "Round pdf-2026-11-26:"; plain lines in `data/verification/pdf-2026-11-26/<N>_simple.json`; report in
`data/verification/pdf-2026-11-26/<N>_report.md`; dates `2026-11-26`. Its own question list (readers 681 to 686) is not yours:
yours is below.

Also read, for your questions only: the first readers' reports in `data/verification/pdf-2026-11-26/first-reader-reports.md`
(what each full text changed, and the reporting issues found), and the cards named below. The PDFs are at
`/mnt/user-data/uploads/DrugEncyclopedia/PDFs/` (paths in `data/verification/pdf-2026-11-26/BRIEF-first-readers.md`, "Your
papers"); open the page of every number you use. Where a card and the PDF disagree, the PDF wins: say so in your report.

The people's questions behind these papers, and how much they are read: `data/verification/questions-2026-11-14/forums.md`
("Most-read questions the site does not answer yet") and `papers-next.md` beside it.

## Rules repeated, because they are never broken

Findings only: no advice on how much, how often, when or how to use; no preparation or potentiation; doses only as a
study's conditions, never as a comparison of strength. Mixing only as risk facts. Emergency guidance is the senior
author's: never a list of signs to act on or what to do. Animal findings labelled as such. An association is not a cause.
Counts out of 100 (out of 1,000 for rare events), absolute numbers before relative ones, editors' calculations labelled and
redoable. Person-first language. At most one quotation per claim, at most 15 words. A narrative review, a letter or an
opinion piece is cited for what it says, never as if it measured something; a claim resting only on such sources stays a
draft and says its figures are second-hand. If an automatic filter stops you, do not retry or reword that step.

---

## Your questions

### Reader 751: the sources for "How to read this site" (no claims)

Cards (`data/study-cards/_incoming/cross-cutting/`): `sc_cohen_1984`, `sc_hill_1965`, `sc_wasserstein_2016`,
`sc_gigerenzer_2007`, `sc_open_science_collaboration_2015`, `sc_ioannidis_2005`, `sc_sumner_2014`, `sc_boutron_2010`; older:
`sc_robins_1975` (`data/study-cards/cross-cutting.json`) and `heroin/sc_robins_1993` for the Vietnam figures Cohen repeats.
The page's text is in `site/src/index.template.html` (section "How to read this site": "'Linked to' is not 'causes'" and
"Seven questions to ask about any drug story"). Write `data/verification/pdf-2026-11-26/751_howto.json`:
`{"items": [{"id": "linked" | "q1" … "q7", "site_text": "...", "anchors": [{reference, study_card, page, locator, extracted,
role, anchor_status: "ai-located", located_by: "AI reader 751 (claim writer), from the PDF", source_read}], "verdict":
"supported" | "partly" | "needs-rewording", "proposed_text": "...", "why": "..."}]}`. Anchor each statement in what the
papers themselves say (not in examples they invent: Cohen's numbers are a constructed example). Where a source says
something different from the site's sentence (Wasserstein's principle 2 against "'Significant' means probably not chance";
Ioannidis: a result with P < 0.05 can still be more likely false than true; Hill: "no significant difference" is not "no
difference"), propose a plain rewording of the same length that the sources support. Items no paper here supports (q2, q3
perhaps): say so, and name in the report what kind of source would. Commit the file; no claim file.

### Reader 752: who gets addicted, and who recovers

Cards: `cross-cutting/sc_hart_2017`, `sc_hart_2020`, `sc_heyman_2013`, `heroin/sc_robins_1993`; older:
`sc_lopez_quintero_2011` (`data/study-cards/methamphetamine.json`, written from the author manuscript: its anchors' printed
pages and six corrections are in `data/verification/pdf-2026-11-26/734_checks.json`; the PDF is the version of record),
`sc_robins_1975`, `sc_fleury_2016`, `sc_mellor_2019`.

1. **`cl_gen_most_users_not_addicted`** (file `general`, substance `general`; pages `general`, `cannabis`, `cocaine`,
   `alcohol`, `nicotine`). "Do most people who try drugs get addicted?" How many people who ever used each drug went on to
   dependence, and how soon, in the US surveys (Lopez-Quintero 2011): absolute numbers first, what "dependence" meant, and
   that these are survey reports. Hart's two opinion pieces only for what he argues, beside the data; never as the source
   of a number (his figures have no source of their own).
2. **Patch `cl_gen_remission`** (print it first) with Heyman 2013 and Robins 1993: what "remission" meant in the surveys
   (not meeting dependence criteria in the past year, one drug at a time; not quitting), by drug (heroin is not among the
   survey curves), and the Vietnam figures as Robins gives them. Do not repeat Heyman's mixed figure ("70% relapse with
   treatment, under 12% without"): the report should say why.
3. **`cl_opi_vietnam_veterans`** (file `heroin`, substance `heroin`; pages `heroin`, `general`). "Did the soldiers addicted to
   heroin in Vietnam stay addicted?" 45 in 100 tried narcotics there and 20 in 100 reported addiction; 5 in 100 addicted again
   in the first year back and 12 in 100 over three years (Figure 6; the text's "6%" disagrees: say how you resolved it).
   Keep Robins's own caution: the conditions in Vietnam were unprecedented. Myth-or-fact items for each answer.

### Reader 753: why it is hard to pee on MDMA, and the rat study behind "a new place"

Cards: `mdma/sc_bryden_1995`, `mdma/sc_baggott_2016`, `heroin/sc_siegel_1982`; older: `sc_henry_1998`, `sc_hysek_2014`
(`data/study-cards/mdma.json`), `sc_siegel_1984`, `sc_siegel_2005` (`data/study-cards/heroin.json`).

4. **`cl_mdma_peeing`** (file `mdma`, substance `mdma`; pages `mdma`). "Why is it hard to pee on MDMA?" What was measured,
   and in whom: the water-holding hormone after MDMA (Henry 1998: 8 men), blood sodium after MDMA with a water load (Baggott
   2016; urine was collected but no urine result is reported), and one case of being unable to pass urine (Bryden 1995: no
   toxicology, no bladder measurement). Say plainly that no study here measured how hard it was to pee; no mechanism beyond
   what the studies show. Link `cl_mdma_hyponatremia` in one sentence, do not repeat it.
5. **Patch `cl_opi_conditioned_tolerance`** with Siegel 1982 as an animal study: both settings were familiar to every rat
   (one paired with heroin, one with an inactive injection), so it is about a cue-paired place, not a new place; tolerance
   was never measured, only death; mortality by group from the printed percentages (editors' counts 12/37, 27/42, 27/28:
   check them); the printed p value that does not reproduce. The human evidence stays as the claim has it.

### Reader 754: what a pill's logo or look can tell you

Cards: `drug-checking/sc_vrolijk_2017`, `drug-checking/sc_vogels_2009`, `drug-checking/sc_brunt_2011`; older:
`sc_brunt_2017` (`data/study-cards/drug-checking.json`).

6. **`cl_dc_pill_logo`** (file `drug-checking`, substance `drug-checking`; pages `drug-checking`, `mdma`). "Can you tell
   what's in a pill from its logo or how it looks?" How often reports passed on online were wrong against laboratory
   testing, and which errors (Vrolijk: overstatement the commonest; the 15.3% called "dangerous"; "twice as likely" is an
   odds ratio, 21 against 12 in 100 rebuilt from the tables: check), what the testing services found over the years, and the
   limit that matters most: none of these papers measured how much tablets with the same logo differ (the only source
   cited for it, Cole et al. 2002, is not on file); the "99% reliable" identification by look has no data behind it.

### Reader 755: research chemicals: NBOMes sold as LSD, and designer benzos

Cards: `lsd/sc_wood_2015`, `benzodiazepines/sc_brunetti_2021`, `benzodiazepines/sc_carpenter_2019`.

7. **`cl_lsd_nbome`** (file `lsd`, substance `lsd`; pages `lsd`, `2c-x`). "What are NBOMes, and are they sold as LSD?" Harms
   reported, from which kind of data (published cases against a poison-centre series: seizures in 38 against 4 in 100),
   deaths with laboratory confirmation (five, not the abstract's eight), and that several people, some who died, believed
   they had taken LSD. Counts the reader could not rebuild stay as printed, with the discrepancy in the report.
8. **`cl_benzo_designer`** (file `benzodiazepines`, substance `benzodiazepines`; pages `benzodiazepines`). "Are designer
   benzos like etizolam more dangerous?" What the death reports and poison-centre reports show: of 141 death entries, 115
   also list an opioid and 3 list no other drug (the reader's count from Table 1: recount), possible double entries; the
   US rise spans a coding change (only etizolam had a code before 2016); no laboratory confirmation; coma and agitation as
   Table 3 gives them. Risk facts only.

### Reader 756: what snorting cocaine does to the nose

Cards: `cocaine/sc_nitro_2022`, `cocaine/sc_saibene_2025`, `cocaine/sc_trimarchi_2001`.

9. **`cl_coc_nose_damage`** (file `cocaine`, substance `cocaine`; pages `cocaine`). "What does snorting coke do to your nose,
   and does it heal?" What the damage is and how often each part was affected in the published cases (Table 4 and Fig. 2,
   not the abstract's mislabelled sites), how it was told apart from other diseases, what repair is reported and when (the
   experts' consensus: after 12 months without cocaine, shown by drug tests: an opinion), and the gap: no study followed
   people after they stopped; the only repeat imaging is of four people who went on using, all worse. Counts out of the 16
   people imaged where Trimarchi's percentages disagree.

### Reader 757: how Xanax and Valium feel, and why people use them

Cards: `benzodiazepines/sc_griffiths_1997`, `benzodiazepines/sc_de_wit_1986`, `benzodiazepines/sc_maust_2019`.

10. **`cl_benzo_liking`** (file `benzodiazepines`, substance `benzodiazepines`; pages `benzodiazepines`). "Do benzos get you
    high, and who likes them?" In the laboratory: who chose a benzodiazepine over a dummy pill and who did not (people with
    and without a history of heavy drinking or other drug use; anxious volunteers: most chose the dummy pill, diazepam
    calmed and sedated but brought no euphoria), and the review's caution that the contrast is confounded with dose.
11. **`cl_benzo_misuse_reasons`** (file `benzodiazepines`; pages `benzodiazepines`, `general`). "Why do people misuse Xanax?"
    In the US survey of 2015–16: how many used and how many misused, their own main reasons (to relax, to sleep, to get
    high: the shares add to more than 100, say why), and where the pills came from (a friend or relative for about 69 in
    100). The abstract's advice that conflicts with Table 2 stays out.

### Reader 758: gabapentin and pregabalin (Lyrica)

Cards: `cross-cutting/sc_evoy_2021`, `cross-cutting/sc_bonnet_2017`, `cross-cutting/sc_bonnet_2021`; older: `sc_gomes_2017`,
`sc_launiainen_2014`.

12. **`cl_gen_gabapentinoids`** (file `general`, substance `general`; pages `general`, `prescription-opioids`). "Can you get
    addicted to gabapentin or Lyrica, and how risky is it?" How often misuse was found and in whom (mostly people with
    opioid use disorder), what dependence and withdrawal look like and on what evidence (case reports; the very low risk for
    people without a substance use disorder rests on counts of case reports with most criteria missing), and the harms as
    associations with opioid use (with the Swedish cohort's HR 0.99 once people with substance use disorders were left
    out). The critique's points of method, not as facts. Link `cl_mix_opioids_gabapentinoids` in one sentence.

### Reader 759: benzos with alcohol, cocaine or Adderall

Cards: `interactions/sc_tanaka_2002`, `interactions/sc_koski_2003`, `interactions/sc_bushnell_2022`.

13. **`cl_mix_benzodiazepines_alcohol`** (file `interactions`, substance `interactions`; pages `interactions`,
    `benzodiazepines`, `alcohol`). "Is it dangerous to mix Xanax and alcohol?" What the death records show (the alcohol
    level in deaths with alcohol and temazepam against alcohol alone: 2.5 against 3.3, an estimate the paper does not name;
    the groups unadjusted and unlike each other), what the review says about breathing and on what (no datum behind
    "synergistic"; metabolism unchanged in 5 of 8 arms), and that only temazepam was studied. Use the tables, not the
    abstract's 53%. Risk facts only. Benzodiazepines with cocaine or stimulants: Bushnell 2022 does not study them taken
    together; say in your report that no study on file answers that part, and write no claim for it.

### Reader 760: Suboxone (buprenorphine) with other opioids, and after stopping

Cards (`methadone-buprenorphine/`): `sc_greenwald_2014`, `sc_varshneya_2022`, `sc_williams_2020`; the reader's arithmetic:
`data/verification/pdf-2026-11-26/741_calculations.py`.

14. **`cl_bup_other_opioids`** (file `methadone-buprenorphine`, substance `methadone-buprenorphine`; pages
    `methadone-buprenorphine`, `heroin`, `fentanyl-and-analogues`). "Does Suboxone stop other opioids from working, and
    when do they work again?" What the scans showed about how many receptors buprenorphine occupies and how that fell after
    stopping (volunteers not in treatment, 3 to 10 people), and that the thresholds in the abstract are not results (blocking
    "not reliably observed"; 20% from early modelling). Findings only: nothing that reads as when to use another opioid.
15. **`cl_bup_fentanyl_withdrawal`** (same file; pages also `fentanyl-and-analogues`). "Can Suboxone put you in withdrawal
    if you use fentanyl?" How often precipitated withdrawal was reported and how severe, by how long people had waited (the
    gradual fall, 45 to 14 in 100), with the denominators exactly (152 of 685 overall; 152 of 339 among those who waited less
    than 24 hours), and the limits (no adjustment; a comparison group of 37). Findings only: no waiting times as advice.
16. **`cl_bup_after_stopping`** (same file; pages `methadone-buprenorphine`, `heroin`). "What happens after stopping
    Suboxone?" Medically treated overdoses and acute care in the six months after stopping long treatment (5.2 in 100), who
    was left out (people who died or lost Medicaid) and that no group stayed on treatment; the overdose codes as printed.
    Keep it consistent with `cl_opi_treatment_mortality` (link it).

### Reader 761: tramadol

Cards (`prescription-opioids/`): `sc_rostam_abadi_2020`, `sc_ryan_2015`, `sc_senay_2003`.

17. **`cl_opi_tramadol_overdose`** (file `prescription-opioids`, substance `prescription-opioids`; pages
    `prescription-opioids`). "Can tramadol cause seizures, and what happens in an overdose?" Seizures, breathing and coma in
    the overdose series (most people had taken other medicines too; not split out for tramadol alone) and the Iran review's
    pooled figures with their prediction intervals; serotonin toxicity: none in 71 overdoses rules out only rates above
    about 5 in 100 in overdose, and says nothing about ordinary doses. No list of signs to act on.
18. **`cl_opi_tramadol_withdrawal`** (same file). "Is tramadol withdrawal different from other opioids?" The reported cases,
    opioid-like and "atypical" withdrawal, with the limits (reported cases only, about 1 in 10 captured by the authors' own
    estimate; manufacturer-funded; "nearly 40%" is 33 in 100 in Table 3).

### Reader 762: Adderall against Ritalin

Cards: `methylphenidate/sc_cortese_2018`, `methylphenidate/sc_farhat_2025`, `methylphenidate/sc_efron_1997`,
`amphetamine/sc_moran_2019`. Efron's PDF opens with a cover page: printed p. 661 is PDF page 2.

19. **`cl_amph_vs_mph`** (file `amphetamine`, substance `amphetamine`; pages `amphetamine`, `methylphenidate`). "Adderall
    or Ritalin: which works better, and which has more side effects?" Benefit and stopping because of side effects in
    children and in adults (network estimates, mostly indirect, entirely indirect in adults; stopping for side effects did
    not differ between the two, OR 1.60, 0.94–2.73), heart rate and blood pressure (similar rises over placebo, about 1–3 mm
    Hg and 2–5 beats a minute, over a median of 7 weeks), and the one blinded head-to-head trial in children (no placebo).
    Prescribed medicines as studied in people with ADHD: nothing about use without a prescription.
20. **`cl_amph_vs_mph_psychosis`** (same file; pages `amphetamine`, `methylphenidate`). "Is psychosis more likely on
    Adderall than Ritalin?" Absolute numbers first (about 1 in 660 over a median of 4 to 5 months), the prespecified hazard
    ratio 1.65 (about 1 extra episode in 1,000 person-years), and why "about twice" overstates it.

### Reader 763: drug tests

Cards (`cross-cutting/`): `sc_verstraete_2004`, `sc_moeller_2017`, `sc_saitman_2014`; `cannabis/sc_goodwin_2008`.

21. **`cl_gen_drug_test_times`** (file `general`, substance `general`; pages `general`, `cannabis`). "How long do drugs show up
    on a drug test?" What the reviews' tables rest on (single small studies, detection limits rather than screening cutoffs;
    textbooks and laboratory pages), and the one study that watched people stop cannabis (times from admission; many still
    positive when watching ended, so its means are minimums). No advice on passing a test.
22. **`cl_gen_drug_test_false_positives`** (same file; pages `general`). "Can medicines cause a false positive on a drug
    test?" Which medicines and foods were reported with which tests (each interference specific to one test, mostly from
    case reports or spiked urine), the few frequencies printed (bupropion and amphetamine screens; sertraline and
    benzodiazepine screens), that a screen is confirmed by another method, and where the two reviews disagree.

### Reader 764: what the supplements change in five answers

The check file `data/verification/pdf-2026-11-26/745_supplements.json` (reader 745) lists what each supplement adds and
where a card or claim disagrees with it. Supplements (paths under `PDFs/`): `LSD/Holze_2022_LSDVersusPsilocybin_Supplement.pdf`
(a Word file: copy it to your folder as .docx and read it with `pandoc -t plain`), `MDMA/Straumann_2023_MDMALSDCoadministration_Supplement.pdf`,
`Cannabis/Smith_2022_CommercialCannabisChemistry_Supplement.pdf` (a zip of TIFF figures: unzip into a new folder of your own),
`Heroin/Sordo_2017_MortalityOpioidSubstitution_Supplement_Part 1.pdf` to `Part 3.pdf`, `Heroin/Darke_2017_DeathFromOpiateWithdrawal_Supplement.pdf`
(a Word file). Patches, each re-reading the supplement for every number you use:

23. **`cl_lsd_vs_psilocybin`**: Table S5 against the claim's heart-rate statement (LSD 100 µg did not raise heart rate more
    than psilocybin, by the table); the table's values in place of readings from Figure 3; how often people named the right
    drug (71, 86, 78 and 79 in 100; placebo 100); the headache counts.
24. **`cl_mix_mdma_lsd`**: the nausea counts that settle the paper's contradiction (14, 7 and 11 of 24); how long effects
    lasted with both drugs.
25. **`cl_can_strain_labels`**: how many samples were THC-dominant in each state (93.6 to 97.3 in 100); the count
    disagreement between S2 and Figure 1 (say it; use what both support).
26. **`cl_opi_treatment_mortality`**: Table B of appendix 2: deaths after incomplete against complete treatment (69 against 17,
    and 84 against 26, per 1,000 person-years), where the claim now says the review lacks this.
27. **`cl_opi_withdrawal_deaths`**: what the appendix lists for the ten cases (no clinical detail; one rests on a prosecutor's
    letter), still a draft resting on an editorial.
The files saved as the Timmermann, Nayak and Hysek supplements are the articles themselves: nothing from them.

---

## Saving your work

After each file passes its check, commit and push it (other agents work in the same folder: add only your own files):
`cd /home/claude/pharmakon && git add <your files> && git -c user.name="Claude (Anthropic), AI co-editor" -c user.email="noreply@anthropic.com" commit -q -m "Claim writer <N>: <what>" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" -m "Claude-Session: https://claude.ai/code/session_018eyT8uK1o68qcrMFU7AWHn" && git push -q origin main`
(if refused: `git pull -q --rebase origin main`, then push again; if the pull is refused because of someone else's
uncommitted files, push again later). Never `git stash`, `git add -A` or `git add .`.

## Final message

Under 200 words: the files written, per claim its certainty in one line, and anything the editor must decide.
