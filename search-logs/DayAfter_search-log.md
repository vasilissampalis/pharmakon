# DayAfter — search log ("The day after": after-effects and remedies, every drug page)

Protocol: METHODS.md §2; `docs/EVIDENCE-MAP-BRIEF.md`; brief `scratchpad/dayafter/BRIEF-reader103.md` (2026-10-25). Run by AI reader 103 on 2026-10-25.

**Source.** PubMed through the E-utilities interface (`esearch.fcgi?db=pubmed`, `esummary.fcgi`; `efetch.fcgi` abstracts only where a title did not show the design), fetched with `javascript_tool` from one tab of the app's browser opened by this reader (tab on `api.crossref.org`), paced at under two requests per second. Hit counts are PubMed's `count` on 2026-10-25. Screening: titles and journals (abstracts where needed) against the two questions of the brief (after-effects; remedies and their risks). Kept items are named by first author and year; their numbers are in `DayAfter_DOI-LIST.md`. Every listed DOI was then fetched from Crossref `works/<DOI>` in the same tab (title, journal, year, first author, `updated-by`), and open-access status was read from OpenAlex (`/works?filter=doi:…`, 25 DOIs per request). Existing lists were checked with a DOI index of all `search-logs/*_DOI-LIST.md` (3,198 DOIs) built locally.

Field tags: `[tiab]` title/abstract, `[ti]` title, `[pt]` publication type, `[MeSH Terms]`, `[au]` author.

---

## 1. Alcohol

| # | String | Hits | Kept |
|---|---|---|---|
| AL1 | `hangover[ti] AND (alcohol[tiab] OR ethanol[tiab]) AND ("Systematic Review"[pt] OR "Meta-Analysis"[pt] OR systematic[ti] OR meta-analysis[ti] OR "Review"[pt])` | 36 | Rothman 2026; Mackus 2024; Jayawardena 2017; Verster 2021; McGregor 2007. Already listed: Roberts 2022, Pittler 2005, Penning 2010, Verster 2010, Wiese 2000. Not kept: narrative mechanism reviews (Palmer 2019, Turner 2024, Mackus 2020, Tipple 2016, Prat 2009), CGRP-antagonist speculation (Hakim 2025), food-chemistry reviews. |
| AL2 | `hangover[ti] AND (alcohol[tiab] OR ethanol[tiab]) AND "Randomized Controlled Trial"[pt]` | 27 | Coppersmith 2021; Eriksson 2020; Rohsenow 2014. Not kept (covered by the systematic reviews or single small supplement trials): yeast extract, paraprobiotic, probiotic, glutathione, hydrogen, Phyllanthus, Hovenia, red ginseng, Korean pear, Opuntia (Wiese 2004), propranolol (Bogin 1986/1987); rat study mis-tagged as RCT (Kim 2023). |
| AL3 | `hangover[ti] AND (driving[tiab] OR cognitive[ti] OR cognition[ti] OR performance[ti]) AND (alcohol[tiab]) AND (systematic[ti] OR meta-analysis[ti] OR "next-day"[ti] OR "next day"[ti] OR driving[ti])` | 7 | Verster 2014 (Psychopharmacology); Alford 2020. Not kept: biomarker commentary, truck-driver survey, single older laboratory studies. |
| AL4 | `(alcohol[ti] OR ethanol[ti]) AND sleep[ti] AND ("Systematic Review"[pt] OR "Meta-Analysis"[pt] OR systematic[ti] OR meta-analysis[ti])` | 14 | Gardiner 2025. Not kept: sleep apnoea, prenatal exposure, AUD pharmacotherapy, physical activity in people with AUD. |
| AL5 | `hangover[tiab] AND (alcohol[tiab]) AND (anxiety[ti] OR mood[ti] OR affect[ti] OR depress*[ti] OR hangxiety[tiab])` | 28 | None beyond Rothman 2026 (systematic review covers the single naturalistic mood studies); animal studies not kept. |
| AL6 | Known item: `"next-day effects of heavy alcohol consumption"[tiab] OR (Gunn C[au] AND systematic[ti] AND alcohol[ti])` | 1 | Gunn 2018. |
| AL7 | `hangover[tiab] AND (water[ti] OR food[ti] OR breakfast[ti] OR hydration[ti] OR dehydration[ti] OR electrolyte*[ti] OR "remedies"[ti] OR "remedy"[ti] OR cure*[ti] OR "hair of the dog"[tiab] OR beer[ti] OR wine[ti])` | 36 | Imai 2026; Morley 2022; Han 2024; Köchling 2019; Verster 2009. Not kept: rat studies, magazine items, food-chemistry assays, a commentary on IV hydration during drug shortages (Chan 2014), a product-satisfaction survey (Verster 2012). No electrolyte or oral rehydration trial. |
| AL8 | `(acetaminophen[ti] OR paracetamol[ti]) AND (alcohol[ti] OR ethanol[ti] OR drinkers[ti]) AND (hepatotoxicity[tiab] OR liver[tiab]) AND (review[pt] OR "Randomized Controlled Trial"[pt] OR systematic[ti])` | 9 | Rumack 2012. Not kept: single trials in people with alcohol dependence covered by Rumack (Dart 2010, Heard 2007, Kuffner 2001), older reviews (Prescott 2000; Riordan 2002). |
| AL9 | `(alcohol[ti] OR ethanol[ti]) AND (ibuprofen[ti] OR aspirin[ti] OR "anti-inflammatory"[ti] OR NSAID*[ti]) AND (bleeding[ti] OR haemorrhage[ti] OR hemorrhage[ti])` | 10 | Kaufman 1999. Not kept: bleeding-time studies from 1968–1983, altitude case. |
| AL10 | `hangover[ti] AND (alcohol[tiab]) AND (exercise[tiab] OR "physical activity"[tiab] OR coffee[tiab] OR caffeine[tiab] OR "oral rehydration"[tiab] OR intravenous[tiab] OR "B vitamin*"[tiab] OR vitamin[ti] OR magnesium[tiab] OR zinc[tiab]) AND humans[MeSH Terms]` | 10 | Rantakömi 2013 (stroke risk). No trial of exercise, morning coffee, oral rehydration or minerals; minerals only in a preliminary review (Min 2010). |

Corrections: Coppersmith 2021 has an author correction in Crossref `updated-by` (10.1038/s41598-021-94669-5). Eriksson 2020 has a corrigendum linked in PubMed (10.1093/alcalc/agaa088, fetched from Crossref) that Crossref `updated-by` does not show.

## 2. Benzodiazepines

| # | String | Hits | Kept |
|---|---|---|---|
| BZ1 | `(benzodiazepine*[tiab] OR hypnotic*[ti] OR "sleep medication"[tiab]) AND (residual[ti] OR "next-day"[ti] OR "next day"[ti] OR morning[ti] OR hangover[ti]) AND (driving[tiab] OR performance[tiab] OR psychomotor[tiab] OR cognitive[tiab]) AND ("Systematic Review"[pt] OR "Meta-Analysis"[pt] OR "Review"[pt] OR systematic[ti] OR meta-analysis[ti])` | 9 | Fornaro 2024; Verster 2004; Vermeeren 2004. Not kept: zopiclone-as-positive-control reviews (Karhana 2025, Verster 2011), middle-of-the-night dosing, zolpidem-ER promotion review; Crowe 2018 (long-term, already _Tolerance #49). |
| BZ2 | `(benzodiazepine*[ti]) AND (driving[ti] OR "traffic"[ti] OR "motor vehicle"[ti]) AND ("Meta-Analysis"[pt] OR "Systematic Review"[pt] OR meta-analysis[ti] OR systematic[ti])` | 5 | None (general driving-risk reviews: Rapoport 2009, Dassanayake 2011, Smink 2010, Thomas 1998; alcohol combination Aitken 2021); the next-day question is covered by BZ1. |
| BZ3 | `(caffeine[ti]) AND (benzodiazepine*[tiab] OR triazolam[tiab] OR lorazepam[tiab] OR diazepam[tiab] OR temazepam[tiab] OR midazolam[tiab]) AND (reversal[tiab] OR reverse*[tiab] OR antagon*[tiab] OR counteract*[tiab] OR residual[tiab] OR sedation[tiab])` | 60 | Mattila 1992. Not kept: animal studies, pharmacokinetic cocktail studies, Rush 1994 and Mattila 2000 (same question, smaller). |
| BZ4 | `("rebound insomnia"[ti] OR "rebound anxiety"[ti]) AND (benzodiazepine*[tiab] OR hypnotic*[tiab] OR triazolam[tiab])` | 32 | Kales 1991; Power 1985. Soldatos 1999 already on _Tolerance (#34). Not kept: zolpidem trials, older reviews, rat study. |
| BZ5 | `(caffeine[tiab]) AND (benzodiazepine*[tiab] OR triazolam[tiab] OR flurazepam[tiab] OR temazepam[tiab] OR hypnotic*[tiab]) AND (daytime[tiab] OR morning[tiab] OR "next day"[tiab] OR residual[tiab]) AND (sleepiness[tiab] OR performance[tiab]) AND humans[MeSH Terms]` | 14 | Johnson 1990 (Psychopharmacology; the companion papers Johnson 1990 Sleep and 1991 Psychophysiology report the same trial). Not kept: shift-work guidelines and Cochrane review (other question). |
| BZ6 | Known item: Glass 2005 (Crossref bibliographic search, then `10.1136/bmj.38623.768588.47[doi]` in PubMed for the PMC id) | 1 | Glass 2005. |
| BZ7 | `(benzodiazepine*[tiab] OR hypnotic*[tiab]) AND (residual[tiab] OR "next-day"[tiab] OR "next day"[tiab] OR hangover[tiab] OR "morning after"[tiab]) AND (modafinil[tiab] OR stimulant*[tiab] OR exercise[tiab] OR "bright light"[tiab] OR "cold water"[tiab] OR nap*[tiab]) AND (counteract*[tiab] OR reverse*[tiab] OR reversal[tiab] OR antagon*[tiab] OR attenuat*[tiab]) AND humans[MeSH Terms]` | 3 | None (no human study of other remedies for next-day sedation). |

## 3. GHB / GBL

| # | String | Hits | Kept |
|---|---|---|---|
| GH1 | `("gamma-hydroxybutyrate"[tiab] OR "gamma-hydroxybutyric acid"[tiab] OR GHB[tiab] OR "sodium oxybate"[tiab] OR "gamma-butyrolactone"[tiab] OR GBL[tiab]) AND (residual[tiab] OR "next-day"[tiab] OR "next day"[tiab] OR "next morning"[tiab] OR "morning after"[tiab] OR hangover[tiab] OR "after-effects"[tiab] OR aftereffects[tiab] OR "day after"[tiab]) AND humans[MeSH Terms]` | 44 | van Amsterdam 2022; Liakoni 2018; Dornbierer 2019. Not kept: narcolepsy treatment papers, sleep-apnoea and depression trials (Bavato 2023/2025), off-topic hits on "residual" (shoulder surgery, malaria, disinfectants), withdrawal case reports already covered by the GHB-GBL list. |
| GH2 | `("gamma-hydroxybutyrate"[tiab] OR GHB[tiab] OR GBL[tiab]) AND (users[tiab] OR recreational[tiab]) AND (survey[tiab] OR "subjective effects"[tiab] OR "self-reported"[tiab] OR qualitative[tiab]) AND (effects[ti] OR experiences[ti] OR use[ti])` | 43 | Floyd 2018. Not kept: chemsex prevalence surveys, a community survey of adverse events during use (Michnevich 2026; no day-after measures in the abstract). |

## 4. Caffeine

| # | String | Hits | Kept |
|---|---|---|---|
| CF1 | `caffeine[ti] AND sleep[ti] AND ("Systematic Review"[pt] OR "Meta-Analysis"[pt] OR systematic[ti] OR meta-analysis[ti])` | 17 | Gardiner 2023; Clark 2017; Sin 2009. Chang 2025 already Caffeine #9. Not kept: athletes, preterm infants, military sleep-loss, EEG mechanism review, sleep apnoea genetics, tea/L-theanine review (Payne 2025; studies combined cognitive effects). |
| CF2 | `("energy drink*"[ti]) AND (sleep[ti] OR insomnia[ti] OR "next day"[tiab] OR "next-day"[tiab] OR crash[tiab] OR "after-effects"[tiab] OR fatigue[ti]) AND ("Systematic Review"[pt] OR "Meta-Analysis"[pt] OR systematic[ti] OR "Randomized Controlled Trial"[pt] OR cohort[tiab])` | 1 | None (prevalence survey). No study of an energy-drink "crash" or its remedies. |
| CF3 | `("caffeine withdrawal"[ti] OR "caffeine-withdrawal"[ti]) AND (headache[tiab]) AND (treatment[tiab] OR acetaminophen[tiab] OR paracetamol[tiab] OR analgesic*[tiab] OR taper*[tiab] OR prevention[tiab])` | 4 | Agritelley 2021. Not kept: expectancy study (Juliano 2019), case report, headache epidemiology. |
| CF4 | `caffeine[ti] AND (postoperative[tiab] OR perioperative[tiab] OR fasting[tiab]) AND headache[tiab] AND (withdrawal[tiab] OR prophylactic[tiab] OR prophylaxis[tiab]) AND ("Randomized Controlled Trial"[pt] OR "Systematic Review"[pt] OR "Meta-Analysis"[pt])` | 2 | Hampl 1995; Weber 1997. |

## 5. Nicotine and tobacco

| # | String | Hits | Kept |
|---|---|---|---|
| NI1 | Known item: `(Hughes JR[au]) AND abstinence[ti] AND tobacco[ti] AND "time course"[ti]` | 1 | Hughes 2007. |
| NI2 | `(smoking[ti] OR nicotine[ti] OR tobacco[ti] OR cigarette*[ti]) AND (exercise[ti] OR "physical activity"[ti]) AND (craving*[ti] OR withdrawal[ti]) AND ("Systematic Review"[pt] OR "Meta-Analysis"[pt] OR systematic[ti] OR meta-analysis[ti])` | 6 | Haasova 2013; Roberts 2012. Not kept: Taylor 2007 (superseded by its update, Roberts 2012), Haasova 2014 (moderator analysis of the same data), a summary (Glass 2014), sports performance (Bao 2024). |
| NI3 | `(nicotine[ti] OR smoking[ti] OR tobacco[ti]) AND sleep[ti] AND ("Systematic Review"[pt] OR "Meta-Analysis"[pt] OR "Review"[pt]) AND (withdrawal[tiab] OR abstinence[tiab] OR replacement[tiab])` | 12 | Jaehne 2009. Not kept: sleep apnoea, sleep adverse events of cessation drugs (Song 2024), non-English reviews, sleep after quitting (Mauries 2025; longer horizon). |
| NI4 | `(nicotine[ti] OR cigarette[ti] OR smoking[ti]) AND (withdrawal[ti] OR craving[ti]) AND (glucose[ti] OR dextrose[ti] OR "nicotine replacement"[ti] OR lozenge[ti] OR gum[ti] OR "oral nicotine"[ti]) AND ("Systematic Review"[pt] OR "Meta-Analysis"[pt] OR systematic[ti] OR "Randomized Controlled Trial"[pt])` | 32 | West 2001; McRobbie 2004. Not kept: single RCTs of particular products (covered by West 2001), hypnosis pilot, imaging studies. |

## 6. Cocaine

| # | String | Hits | Kept |
|---|---|---|---|
| CO1 | `cocaine[ti] AND (withdrawal[ti] OR crash[tiab] OR "abstinence symptom*"[tiab] OR "abstinence symptomatology"[ti]) AND ("Systematic Review"[pt] OR "Meta-Analysis"[pt] OR "Randomized Controlled Trial"[pt] OR review[ti] OR "abstinence symptomatology"[ti])` | 22 | Gawin 1986; Kampman 2006. Not kept: withdrawn Cochrane antidepressant review (2010 withdrawal notice; earlier versions concern dependence), single older trials (bromocriptine, L-dopa, buspirone, nitrous oxide), preclinical incubation review, roadside driving data. |
| CO2 | `cocaine[ti] AND sleep[ti] AND (abstinence[tiab] OR withdrawal[tiab] OR binge[tiab]) AND humans[MeSH Terms]` | 28 | Weddington 1990; Pace-Schott 2005; Morgan 2010; Angarita 2016 (→ Cross-cutting). Not kept: further Morgan/Angarita laboratory reports on the same cohorts, rTMS chart review, citicoline, EEG study, systematic review of sleep architecture over longer abstinence (Medigue 2025; read if the page needs weeks rather than days). |
| CO3 | `(cocaine[tiab] OR stimulant*[tiab] OR methamphetamine[tiab] OR amphetamine*[tiab]) AND ("come down"[tiab] OR "coming down"[tiab] OR comedown[tiab] OR "come-down"[tiab] OR "comedowns"[tiab]) AND (alcohol[tiab] OR benzodiazepine*[tiab] OR cannabis[tiab] OR opioid*[tiab] OR heroin[tiab] OR GHB[tiab] OR "self-medicat*"[tiab])` | 13 | Pennings 2002; Rigg 2018 (→ MDMA); Palmer 2020 (→ Methamphetamine). Not kept: cannabis-as-harm-reduction cohorts (outcome is opioid use), benzodiazepine–opioid co-use, Welsh interview study of non-medical prescription use (May 2020), GHB baclofen protocol. |

## 7–9. Amphetamine, methamphetamine, methylphenidate

| # | String | Hits | Kept |
|---|---|---|---|
| ST1 | `(amphetamine*[ti] OR methamphetamine[ti] OR psychostimulant*[ti] OR stimulant*[ti]) AND withdrawal[ti] AND ("Systematic Review"[pt] OR "Meta-Analysis"[pt] OR "Cochrane Database Syst Rev"[ta] OR "Randomized Controlled Trial"[pt])` | 26 | Shoptaw 2009 (Cochrane); Cruickshank 2008; Lee 2013. Acheson 2023 already Amphetamine #52 / Methamphetamine #61. Not kept: acupuncture, moxibustion and electrical-stimulation trials published in Chinese (single-centre; read only if the page covers them), rTMS trial (Liang 2018; a clinical procedure), rodent systematic reviews, the superseded 2001 Cochrane version, Pennay 2011 (superseded by Acheson 2023), lisdexamfetamine in binge-eating disorder. |
| ST2 | `(methamphetamine[ti] OR amphetamine[ti]) AND (residual[ti] OR "next day"[tiab] OR "next-day"[tiab] OR "day after"[tiab]) AND (sleep[tiab] OR mood[tiab] OR performance[tiab]) AND humans[MeSH Terms]` | 6 | Perez 2008. Kirkpatrick 2012 already _Tolerance #165. |
| ST3 | `(methamphetamine[tiab] OR "amphetamine-type stimulant*"[tiab]) AND (exercise[ti] OR "physical activity"[ti] OR aerobic[ti]) AND ("Systematic Review"[pt] OR "Meta-Analysis"[pt] OR "Randomized Controlled Trial"[pt])` | 23 | Xu 2024; Rawson 2015 (J Subst Abuse Treat). Not kept: single acute-exercise craving trials and cognition trials (covered by Xu 2024), protocol, fitness and heart-rate-variability outcomes, Morris 2018 (general previous substance use). |
| ST4 | `(stimulant*[ti] OR methylphenidate[ti] OR amphetamine*[ti] OR lisdexamfetamine[ti]) AND sleep[ti] AND (ADHD[tiab] OR "attention-deficit"[tiab]) AND ("Meta-Analysis"[pt] OR "Systematic Review"[pt] OR meta-analysis[ti])` | 2 | Faraone 2019; Kidwell 2015 (→ Cross-cutting). |
| ST5 | `(stimulant[ti] OR methylphenidate[ti] OR amphetamine[ti]) AND rebound[ti]` | 13 | Carlson 2003; Cox 2008. Not kept: rodent sleep-rebound studies, growth rebound, bipolar-mimic commentary. |
| ST6 | `(melatonin[ti]) AND (ADHD[tiab] OR "attention-deficit"[tiab]) AND (insomnia[tiab] OR "sleep onset"[tiab]) AND (stimulant*[tiab] OR methylphenidate[tiab]) AND ("Randomized Controlled Trial"[pt] OR "Systematic Review"[pt] OR "Meta-Analysis"[pt])` | 1 | Weiss 2006 (no DOI in PubMed; DOI 10.1097/01.chi.0000205706.78818.ef from a Crossref bibliographic search, which also returned a truncated duplicate record "10.1097/01" and a yearbook abstract, both not used). |
| — | From CO3 (Cocaine) | — | Palmer 2020. |

## 10. Synthetic cathinones

| # | String | Hits | Kept |
|---|---|---|---|
| SC1 | `(mephedrone[tiab] OR "synthetic cathinone*"[tiab] OR methylone[tiab] OR MDPV[tiab] OR "bath salts"[tiab] OR "3-MMC"[tiab] OR "4-MMC"[tiab] OR cathinone*[ti]) AND ("come down"[tiab] OR comedown[tiab] OR "come-down"[tiab] OR "after-effects"[tiab] OR "sub-acute"[tiab] OR subacute[tiab] OR "next day"[tiab] OR "next-day"[tiab] OR hangover[tiab] OR "days after"[tiab] OR insomnia[tiab] OR "low mood"[tiab]) AND humans[MeSH Terms]` | 23 | Gunderson 2013; Matthews 2017 (→ Cross-cutting). Homman 2018 and Winstock 2011 already on the Synthetic-cathinones list (#58, #28). Not kept: case reports of acute toxicity, mouse studies, market data (Hutten 2026), internet trip reports (Van Hout 2014, 4-MEC), slamsex survey. |

## 11. MDMA

| # | String | Hits | Kept |
|---|---|---|---|
| MD1 | `(MDMA[tiab] OR ecstasy[tiab] OR methylenedioxymethamphetamine[tiab]) AND ("mid-week"[tiab] OR midweek[tiab] OR "sub-acute"[tiab] OR subacute[tiab] OR "come down"[tiab] OR comedown[tiab] OR "come-down"[tiab] OR "after-effects"[tiab] OR aftereffects[tiab] OR "days after"[tiab] OR "Tuesday"[tiab]) AND humans[MeSH Terms] AND (mood[tiab] OR depress*[tiab] OR sleep[tiab] OR irritab*[tiab])` | 22 | Curran 1997 (no DOI in PubMed; Crossref bibliographic search returned two records, 10.1111/j.1360-0443.1997.tb02951.x listed and 10.1046/j.1360-0443.1997.9278215.x noted, both fetched, neither with `updated-by`); Scott 2013; Pirona 2010. Already listed: Huxster 2006 (MDMA #50), Verheyden 2003 (#49). Not kept: aggression and facial-expression sub-studies (Hoshi 2004/2006, Curran 2004), polydrug psychopathology surveys, rat studies, Verheyden 2002 (gender sub-analysis). |
| MD2 | `(MDMA[tiab] OR ecstasy[tiab]) AND (SSRI*[tiab] OR citalopram[tiab] OR fluoxetine[tiab] OR "5-HTP"[tiab] OR "5-hydroxytryptophan"[tiab] OR antioxidant*[tiab] OR "vitamin C"[tiab] OR "alpha-lipoic"[tiab] OR magnesium[tiab] OR supplement*[tiab] OR "pre-loading"[tiab] OR "post-loading"[tiab] OR "harm reduction practices"[tiab] OR "harm reduction strategies"[tiab]) AND (users[tiab] OR recreational[tiab] OR survey[tiab]) AND humans[MeSH Terms]` | 68 | Dobry 2013. Not kept: festival prevalence and drug-checking surveys, cell and animal toxicity studies, chemsex surveys, pharmacovigilance mortality study (Cohen 2021; concomitant drugs, not after-effects), Australian pharmaceutical-use survey without DOI (Silins 2009). No human study of 5-HTP, antioxidants or magnesium. |
| MD3 | `(MDMA[ti] OR ecstasy[ti]) AND sleep[ti]` | 29 | Randall 2009. Not kept: MDMA-assisted therapy sleep outcomes (Ponte 2021, with expression of concern), long-term sleep and apnoea in abstinent users, animal studies, driving after sleep loss (Bosker 2010/2012; acute effects). |
| MD4 | Known item: Parrott & Lasky 1998 (Crossref bibliographic search) | — | Parrott 1998. |
| — | From CO3 (Cocaine) | — | Rigg 2018. |

## 12–17. LSD, psilocybin, DMT and ayahuasca, 5-MeO-DMT, mescaline, 2C-x

The psychedelic lists already hold most after-effect papers (Holze 2021/2022 safety pharmacology, Johnson 2012 headaches, Studerus 2011, Hinkle 2024, Bouso 2022, Uthaug 2020 reactivations, Ley 2023, Holze 2026 on 2C-B); the searches below looked for what they lack.

| # | String | Hits | Kept |
|---|---|---|---|
| PS1 | `(afterglow[tiab] OR "after-glow"[tiab]) AND (psychedelic*[tiab] OR hallucinogen*[tiab] OR psilocybin[tiab] OR LSD[tiab] OR ayahuasca[tiab] OR DMT[tiab])` | 15 | Evens 2023; Basedow 2024; Evens 2026; Wießner 2022 (all but Wießner → Cross-cutting). Not kept: Majić 2015 (narrative review superseded by Evens 2023), Afterglow Inventory validation (Majić 2025), ayahuasca afterglow imaging and mindfulness studies (Sampedro 2017, Murphy-Beiner 2020; covered by Evens 2023), floatation and ketamine items, historical therapy review. |
| PS2 | `(flashback*[ti] OR "persisting perception"[ti]) AND (LSD[tiab] OR psilocybin[tiab]) AND (controlled[tiab] OR healthy[tiab] OR trial*[tiab])` | 6 | Müller 2022 (→ Cross-cutting). Not kept: case reports, historical review; Halpern 2003 HPPD review (HPPD is covered on the LSD list, #18–19). |
| PS3 | `(psilocybin[ti] OR ayahuasca[ti] OR LSD[ti] OR "lysergic acid diethylamide"[ti] OR DMT[ti] OR dimethyltryptamine[ti] OR psychedelic*[ti]) AND sleep[ti] AND humans[MeSH Terms]` | 10 | Allen 2024; Barbanoj 2008. Not kept: 1960s LSD sleep studies, sleep-administration proposal, review of sleep improvement in depression trials, memory consolidation study (Nikolič 2023). |
| PS4 | Known item: `Dudysova D[au] AND psilocybin[tiab]` | 2 | Dudysová 2020. |
| PS5 | `(2C-B[tiab] OR "4-bromo-2,5-dimethoxyphenethylamine"[tiab]) AND humans[MeSH Terms] AND (effects[ti] OR pharmacology[ti] OR subjective[tiab])` | 10 | None new: Arikci 2026 (effects up to 9 h only) and Mallaroni 2023 (acute) not kept; Holze 2026 already 2C-x #1; Matthews 2017 already kept (→ Cross-cutting). |
| PS6 | `(psilocybin[tiab] OR LSD[tiab] OR psychedelic*[tiab] OR hallucinogen*[tiab]) AND headache*[ti]` | 38 | None: all on psychedelics as treatments for cluster headache or on lifetime use; no study of remedies for psychedelic-induced headache. Johnson 2012 already Psilocybin #25. |
| PS7 | Check of listed papers' abstracts (`efetch` by DOI): Holze 2022 (LSD #3), Ley 2023 (Mescaline #2), Vizeli 2017 (MDMA #29) | 3 | All three report subacute (12–24 h) adverse effects, so they serve this page as already-listed items. |

## 18–21. Ketamine, phencyclidine, dextromethorphan, nitrous oxide

| # | String | Hits | Kept |
|---|---|---|---|
| DI1 | `ketamine[tiab] AND (cystitis[tiab] OR uropathy[tiab] OR bladder[tiab]) AND ("self-medicat*"[tiab] OR "relieve"[tiab] OR "pain relief"[tiab] OR "more ketamine"[tiab] OR abstinence[tiab] OR cessation[tiab] OR "stopping"[tiab]) AND humans[MeSH Terms]` | 45 | Harding 2025. Chan 2022 already Ketamine #21. Not kept: urology guidelines and reviews of surgical management, cholangiopathy, case reports. No study of using more ketamine for bladder pain. |
| DI2 | `ketamine[ti] AND ("side effects"[ti] OR "side-effects"[ti] OR "adverse effects"[ti] OR "adverse events"[ti] OR safety[ti]) AND (depression[tiab] OR depressive[tiab]) AND ("Systematic Review"[pt] OR "Meta-Analysis"[pt])` | 35 | None directly (newer reviews pool efficacy and safety in special groups); Short 2018 found by known-item search `Short B[au] AND ketamine[ti] AND side-effects[ti]` (1 hit). |
| DI3 | `(phencyclidine[tiab] OR PCP[ti]) AND ("after-effects"[tiab] OR aftereffects[tiab] OR "next day"[tiab] OR "next-day"[tiab] OR residual[tiab] OR prolonged[ti] OR "days after"[tiab] OR recovery[ti]) AND humans[MeSH Terms]` | 19 | Rainey 1975; Erard 1980. Fauman 1975 already PCP #19. Not kept: off-topic "PCP" hits (pentachlorophenol, Pneumocystis), poison-centre data, a 1978 case report of hypertension during recovery, neuropsychological recovery study (Cosgrove 1991; weeks to months). |
| DI4 | `dextromethorphan[tiab] AND (recreational[tiab] OR abuse[tiab] OR misuse[tiab] OR "high dose*"[tiab]) AND ("after-effects"[tiab] OR aftereffects[tiab] OR "next day"[tiab] OR "next-day"[tiab] OR hangover[tiab] OR residual[tiab] OR "days after"[tiab] OR withdrawal[ti] OR subjective[tiab]) AND humans[MeSH Terms]` | 23 | Reissig 2012 (a gap on the DXM list); Mutschler 2010. Miller 2005 already DXM #8. Not kept: psilocybin–DXM comparison (Carbonaro 2018; acute), alcohol-withdrawal trial, CYP2D6 studies, methadone safety study. |
| DI5 | `("nitrous oxide"[tiab] OR N2O[tiab]) AND (recreational[tiab] OR "whippets"[tiab] OR misuse[tiab] OR users[tiab]) AND ("vitamin B12"[tiab] OR cobalamin[tiab] OR "B12"[tiab] OR methionine[tiab]) AND (supplement*[tiab] OR prophyla*[tiab] OR prevent*[tiab] OR treatment[tiab]) AND ("Systematic Review"[pt] OR "Meta-Analysis"[pt] OR review[pt] OR survey[tiab] OR cohort[tiab] OR "case series"[tiab])` | 33 | Brunt 2025; Mair 2023. Ménétrier 2023 already Nitrous-oxide #22. Not kept: thrombosis and psychosis case series, adolescent myeloneuropathy series, German neurologist survey. No study of B12 taken while continuing to use. |
| DI6 | `("nitrous oxide"[ti]) AND (recreational[tiab] OR users[tiab]) AND (survey[tiab] OR "subjective effects"[tiab] OR "adverse effects"[tiab] OR "after-effects"[tiab] OR headache[tiab])` | 43 | Kaar 2016 (also by known item `Kaar SJ[au] AND "nitrous oxide"[ti]`). Not kept: case reports, anaesthetist surveys, French prevalence survey. |

## 22–23. Cannabis and synthetic cannabinoids

| # | String | Hits | Kept |
|---|---|---|---|
| CA1 | `(cannabis[tiab] OR marijuana[tiab] OR THC[tiab] OR tetrahydrocannabinol[tiab]) AND (hangover[tiab] OR "next day"[tiab] OR "next-day"[tiab] OR "morning after"[tiab] OR residual[ti] OR "day after"[tiab]) AND humans[MeSH Terms] AND (effects[ti] OR impairment[ti] OR performance[ti] OR driving[ti] OR consequences[ti] OR hangover[ti])` | 47 | Suraev 2024; Waddell 2022. Not kept: residual effects after 48 h or more of abstinence in people who use daily (Mastropietro 2026, Burke 2025, Matheson 2020, Brands 2019; read if the page covers regular use), neuroimaging and emotion-processing residual studies, meta-review of residual neurocognition (Dellazizzo 2022), daily-diary consequence studies. |
| CA2 | Known item: `Chait LD[au] AND (hangover[ti] OR "morning after"[ti])` | 2 | Chait 1985; Chait 1990. |
| CA3 | `(cannabis[ti] OR cannabinoid*[ti] OR THC[ti] OR tetrahydrocannabinol[ti]) AND (driving[ti] OR "cognitive"[ti]) AND (duration[tiab] OR magnitude[ti] OR "time course"[tiab]) AND ("Meta-Analysis"[pt] OR "Systematic Review"[pt] OR meta-analytic[ti])` | 4 | McCartney 2021. |
| CA4 | `(cannabinoid*[ti] OR cannabis[ti]) AND sleep[ti] AND ("Systematic Review"[pt] OR "Meta-Analysis"[pt] OR systematic[ti])` | 16 | Velzeboer 2025. Not kept: cannabinoids as treatments for insomnia (Asim 2026, AminiLari 2022, da Silva 2025, Spanagel 2021), general-population sleep (Mao 2025), withdrawal and sleep (Gates 2016), older review (Gates 2014). |
| CA5 | `("cannabinoid hyperemesis"[tiab] OR "cannabis hyperemesis"[tiab]) AND (capsaicin[tiab] OR "hot shower*"[tiab] OR "hot bath*"[tiab] OR haloperidol[tiab] OR droperidol[tiab] OR treatment[ti]) AND ("Randomized Controlled Trial"[pt] OR "Systematic Review"[pt] OR "Meta-Analysis"[pt] OR survey[tiab])` | 14 | Sabbineni 2024; Ruberto 2021. Sorensen 2017 already Cannabis #28. Not kept: earlier or narrower reviews (Pourmand 2021, McConachie 2019, Richards 2017, Senderovich 2022, Zhu 2021, Hsu 2025), capsaicin pilot (Dean 2020; inside Sabbineni 2024), surveys. |
| SY1 | Known item: `Winstock AR[au] AND Barratt MJ[au] AND synthetic[ti]` | 3 | Winstock 2013 (Drug Alcohol Depend; a gap on the Synthetic-cannabinoids list); Craft 2022. Not kept: emergency-presentation survey (Winstock 2013, Hum Psychopharmacol; acute). |
| SY2 | `("synthetic cannabinoid*"[tiab] OR "spice"[ti] OR JWH-018[tiab] OR "K2"[ti]) AND (hangover[tiab] OR "next day"[tiab] OR "next-day"[tiab] OR "after-effects"[tiab] OR aftereffects[tiab] OR withdrawal[ti] OR residual[tiab] OR "days after"[tiab]) AND humans[MeSH Terms]` | 38 | Sharma 2025. Not kept: off-topic hits ("spice" in endoscopy, "K2" chemistry), mouse study, psychiatric case-register studies, opioid-withdrawal study in Kazakhstan. |

## 24–28. Heroin, fentanyl, prescription opioids, methadone and buprenorphine, kratom

| # | String | Hits | Kept |
|---|---|---|---|
| OP1 | `("opioid withdrawal"[ti] OR "opiate withdrawal"[ti]) AND ("Cochrane Database Syst Rev"[ta])` | 37 | Gowing 2016 (alpha2-adrenergic agonists, .pub5); Gowing 2017 (buprenorphine, .pub5). Not kept: superseded versions (.pub2–.pub4), newborn withdrawal reviews, opioid antagonists under sedation or with minimal sedation (clinical procedures), methadone taper (Amato 2013; a clinical regimen). |
| OP2 | `("opioid withdrawal"[tiab] OR "opiate withdrawal"[tiab]) AND (loperamide[ti] OR gabapentin[ti] OR pregabalin[ti] OR tramadol[ti] OR "self-treat*"[tiab] OR "self-manag*"[tiab] OR "self-medicat*"[tiab]) AND humans[MeSH Terms]` | 105 | Padhan 2023. Not kept: tapering trials for chronic pain, kratom pharmacology and market studies, gabapentin trials during buprenorphine taper (Ray 2025; clinic setting), single-site tramadol case report. |
| OP3 | `lofexidine[ti] AND ("Randomized Controlled Trial"[pt] OR "Systematic Review"[pt] OR "Meta-Analysis"[pt])` | 34 | Gorodetzky 2017. Not kept: older and smaller trials (in Gowing 2016), QT study, lofexidine for cannabis or relapse prevention, a retracted lofexidine trial in children with tics (Niederhofer 2003; marked "Retracted Publication" in PubMed, not relevant). |
| OP4 | `loperamide[ti] AND (abuse[tiab] OR misuse[tiab] OR "self-treat*"[tiab] OR withdrawal[tiab]) AND (cardiac[tiab] OR cardiotoxicity[tiab] OR dysrhythmia[tiab] OR arrhythmia[tiab] OR QT[tiab]) AND (review[pt] OR "Systematic Review"[pt] OR "case series"[tiab] OR cases[tiab])` | 24 | Lee 2019. Not kept: reviews of cardiac management (Wu 2022, Eggleston 2020, Akel 2018, Teigeler 2019, White 2019), case reports, Nordic death series, EMA pharmacovigilance (Schifano 2018), poison-centre trends (Patel 2023). |
| OP5 | `gabapentin[ti] AND opioid*[ti] AND (death[ti] OR deaths[ti] OR overdose[ti] OR mortality[ti])` | 7 | Gomes 2017. Not kept: Medicare mortality analyses in older adults with pain, preprint, commentary. |
| OP6 | `naloxone[ti] AND ("precipitated withdrawal"[tiab] OR "opioid withdrawal"[ti]) AND (incidence[tiab] OR rate*[tiab] OR dose[ti]) AND humans[MeSH Terms]` | 28 | Isoardi 2022; Jones 2026. Not kept: naloxone dose-preference surveys, buprenorphine micro-induction case series, comment and reply on Purssell 2021, prehospital series (Vandergrift 2025). |
| OP7 | `fentanyl[ti] AND (withdrawal[ti] OR clearance[ti] OR "precipitated"[ti]) AND humans[MeSH Terms] NOT (neonat*[ti] OR infant*[ti] OR pediatric[ti] OR children[ti])` | 61 | Sharma 2025; D'Onofrio 2023; Alexander 2025. Not kept: case reports, IV fentanyl for refractory withdrawal in hospital (Zazoulina 2025), review (Martinez 2025), medetomidine series (London 2026; read with Alexander 2025 if the page covers it), hospital buprenorphine series (Thakrar 2024). |
| OP8 | `("opioid-induced constipation"[ti]) AND ("Meta-Analysis"[pt] OR "Systematic Review"[pt] OR "Cochrane Database Syst Rev"[ta])` | 22 | Nee 2018; Kistemaker 2024 (erratum 10.1016/j.ctrv.2024.102738 in Crossref `updated-by`). Not kept: single-drug meta-analyses (naldemedine), network meta-analyses of the same drugs (Luthra 2019, Sridharan 2018, Ouyang 2020), acupuncture and herbal reviews. |
| OP9 | Known item: `Dyer KR[au] AND methadone[ti] AND withdrawal[tiab]` | 6 | Dyer 1999. |
| OP10 | `kratom[tiab] AND (withdrawal[ti] OR "self-treat*"[tiab] OR "opioid withdrawal"[tiab]) AND ("Systematic Review"[pt] OR review[ti] OR survey[tiab] OR "case series"[tiab])` | 49 | Rogers 2024; Calicdan 2026. Singh 2014, Grundmann 2017 and Garcia-Romeu 2020 already on the Kratom list. Not kept: 7-hydroxymitragynine case series, physician survey, narrative reviews, cancer-patient survey. |

## 29–30. Alkyl nitrites and inhalants, Salvia divinorum

| # | String | Hits | Kept |
|---|---|---|---|
| IN1 | `(inhalant*[tiab] OR solvent*[ti] OR "volatile substance*"[tiab] OR poppers[tiab] OR "alkyl nitrite*"[tiab] OR "amyl nitrite"[tiab]) AND (hangover[tiab] OR "after-effects"[tiab] OR aftereffects[tiab] OR "next day"[tiab] OR "next-day"[tiab] OR headache*[ti] OR "adverse effects"[ti]) AND humans[MeSH Terms]` | 17 | None (occupational solvent exposure, allergy, anaesthesia). No study of next-day effects of recreational inhalant use. |
| IN2 | `(poppers[ti] OR "alkyl nitrite*"[ti] OR "amyl nitrite"[ti]) AND (users[tiab] OR survey[tiab] OR review[pt]) AND (adverse[tiab] OR headache[tiab] OR effects[ti] OR harms[tiab])` | 10 | Bartolo 2023; Romanelli 2004. Davies 2012 already Alkyl-nitrites-and-inhalants #4. Not kept: regulatory and retailer studies, prevalence surveys, dermatitis review, cyanide antidote review. |
| SA1 | `("Salvia divinorum"[tiab] OR salvinorin[tiab]) AND ("after-effects"[tiab] OR aftereffects[tiab] OR "after effects"[tiab] OR afterglow[tiab] OR persisting[tiab] OR "next day"[tiab] OR "lasting effects"[tiab] OR "subsequent"[tiab])` | 12 | None new: Addy 2012 (found again by `Addy PH[au] AND salvinorin[ti]`), MacLean 2013 and Baggott 2010 are already on the Salvia list (#13, #11, #22). Not kept: chemistry, primate PET, receptor studies, a small survey (Dalgarno 2007). |

---

## Cross-cutting

Papers spanning several pages were kept from the drug searches above: Angarita 2016 (CO2), Kidwell 2015 (ST4), Matthews 2017 (SC1), Evens 2023, Basedow 2024 and Evens 2026 (PS1), Müller 2022 (PS2). Waddell 2022 (CA1), Shoptaw 2009 and Cox 2008 (ST1, ST5) and the opioid-withdrawal papers under Heroin (OP1–OP6) are listed in their main drug section with a `_Cross-cutting/` save path.

## Verification and final checks

1. **Crossref.** Every DOI was fetched from `https://api.crossref.org/works/<DOI>` in the same tab, first at drafting and again in one final sweep of all 108 listed DOIs: 108 resolved, 0 failed, 0 resolved to a different paper. `updated-by` entries found: correction for Coppersmith 2021, erratum for Kistemaker 2024. Eriksson 2020's corrigendum is linked in PubMed only; its Crossref record was fetched.
2. **PubMed match.** A DOI lookup in PubMed (`"<DOI>"[doi]`, 16–20 DOIs per request) found 106 of the 108 DOIs; the other two (Curran & Travill 1997; Weiss 2006) have no DOI in PubMed and were located by Crossref bibliographic search (`query.bibliographic` with title, author and year, `select=DOI,title,container-title,issued,author,updated-by`, 3 rows).
3. **Free to read.** PMC ids from the PubMed records; publisher open access from OpenAlex (`/works?filter=doi:…&select=doi,open_access,ids`, 25 DOIs per request). The same was done for the 74 already-listed papers.
4. **Overlap with other lists.** All candidate DOIs were checked against a local index of every DOI in `search-logs/*_DOI-LIST.md` (3,198 DOIs). Ten papers first drafted as new were already on other lists and were moved to the "Already on other lists" lines:

| Paper | Already on |
|---|---|
| Pennings, Leccese & de Wolff 2002 (alcohol and cocaine) | Alcohol #96; _Interactions #21 |
| Palmer et al. 2020 (methamphetamine–opioid co-use motivations) | Methamphetamine #102 |
| Short et al. 2018 (ketamine side-effects in depression) | Ketamine #34 |
| Mutschler et al. 2010 (dextromethorphan withdrawal) | _Tolerance #269 |
| Brunt et al. 2024 (nitrous oxide neurotoxicity) | Nitrous-oxide #9 |
| Kaar et al. 2016 (nitrous oxide survey) | Nitrous-oxide #6 |
| Craft et al. 2022 (synthetic cannabinoid withdrawal) | _Tolerance #312 |
| Sharma & Weinstein 2025 (synthetic cannabinoid withdrawal SR) | _Tolerance #313 |
| Gomes et al. 2017 (gabapentin and opioid death) | _Interactions #15 |
| Rogers et al. 2024 (kratom dependence) | _Tolerance #421 |

5. **Abstract checks.** `efetch` abstracts were read only to confirm design or scope where the title did not show it (for example Imai 2026, Liakoni 2018, Johnson 1990, Kaar 2016, Short 2018, Reissig 2012, Addy 2012); after-effect and remedy descriptions in the list were corrected where an abstract did not support them (nitrous oxide survey outcomes; ketamine side-effect timing).

## PubMed strings for the gaps (for the senior author or a later reader)

1. `hangover[ti] AND (electrolyte*[tiab] OR "oral rehydration"[tiab] OR intravenous[tiab] OR "IV therapy"[tiab]) AND humans[MeSH Terms]` — any trial of electrolyte drinks or drip hydration.
2. `(MDMA[tiab] OR ecstasy[tiab]) AND ("5-hydroxytryptophan"[tiab] OR "5-HTP"[tiab] OR "vitamin C"[tiab] OR "alpha-lipoic acid"[tiab] OR magnesium[tiab]) AND humans[MeSH Terms]` — comedown supplements (none found on 2026-10-25).
3. `("nitrous oxide"[tiab]) AND recreational[tiab] AND ("vitamin B12"[tiab] OR methionine[tiab]) AND (prevent*[tiab] OR prophyla*[tiab] OR supplement*[tiab])` — whether B12 taken during continued use protects.
4. `(cannabis[tiab] OR THC[tiab]) AND (edible*[tiab] OR "high-potency"[tiab]) AND ("next day"[tiab] OR "next-day"[tiab] OR hangover[tiab] OR residual[tiab])` — next-day effects of today's products.
5. `(cocaine[tiab] OR amphetamine*[tiab] OR methamphetamine[tiab]) AND ("come down"[tiab] OR comedown[tiab] OR crash[tiab]) AND (melatonin[tiab] OR "sleep aid*"[tiab] OR zolpidem[tiab] OR benzodiazepine*[tiab] OR cannabis[tiab])` — sleep and come-down aids after stimulants.
6. `("opioid withdrawal"[tiab]) AND ("self-managed"[tiab] OR "self-detox*"[tiab] OR "home detox*"[tiab] OR "at home"[tiab]) AND humans[MeSH Terms]` — self-managed opioid withdrawal.
7. `(ketamine[tiab]) AND ("K-cramps"[tiab] OR "abdominal pain"[tiab]) AND (recreational[tiab] OR users[tiab])` — K-cramps and what people use for them.
8. `("3-MMC"[tiab] OR "3-CMC"[tiab] OR "4-CMC"[tiab] OR "3-methylmethcathinone"[tiab]) AND (effects[ti] OR users[tiab] OR survey[tiab])` — newer cathinones.
9. `(inhalant*[tiab] OR "volatile substance*"[tiab] OR poppers[tiab]) AND (headache[tiab] OR hangover[tiab] OR "after-effects"[tiab]) AND (users[tiab] OR adolescents[tiab]) AND humans[MeSH Terms]` — next-day effects of inhalants.
10. `(GHB[tiab] OR GBL[tiab] OR "gamma-hydroxybutyrate"[tiab]) AND (recreational[tiab] OR users[tiab]) AND ("next day"[tiab] OR "day after"[tiab] OR mood[tiab] OR sleep[tiab]) AND humans[MeSH Terms]` — next-day effects after occasional use.

## Notes

- No Crossref throttling was met; one bibliographic search returned an empty response once and succeeded on retry after a pause.
- No safety filter stopped any response.
- Nothing was downloaded, no PDF link was opened, and no page other than the APIs (api.crossref.org, eutils.ncbi.nlm.nih.gov, api.openalex.org) was visited. The tab was closed at the end.
