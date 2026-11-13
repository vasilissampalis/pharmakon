# Caffeine — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening.

## Layer 1 — Crossref bibliographic search (run by AI, 2026-10-15)

### Conditions

Crossref's REST API was throttled throughout this session: HTTP 429 after roughly every second request, plus intermittent `CLIENT_ERROR` refusals from the same host. Pauses of 90–300 s were taken after every refusal, and a refused URL was never re-fetched as written. Direct (non-WebFetch) access to `api.crossref.org` is blocked in this environment.

As with the other lists in this batch, **every DOI was taken verbatim from a Crossref works-search record returned in this session** rather than recalled and then checked with `works/<DOI>`. The WebFetch proxy refuses URLs longer than roughly 250 characters, capping each query at about 90 characters of search terms.

Two Crossref relevance behaviours cost queries here and are worth recording for whoever runs the next substance. A query containing `pharmacokinetics` and `metabolism` was swamped by the journal *Drug Metabolism and Pharmacokinetics* (24 of 25 hits), because Crossref weights container titles. A query containing `overdose`, `toxicity` and `deaths` was swamped by *Reactions Weekly* case notes (20 of 25 hits). Substance-anchored distinctive phrases, and exact title fragments of known landmarks, worked far better than topic words.

### Pre-specified section queries (`filter=type:journal-article`, relevance-sorted)

| # | Query string | Status | Hits screened | Retained |
|---|---|---|---|---|
| CF1 | `caffeine pharmacokinetics CYP1A2 polymorphism metabolism humans variability` | 429 refused; re-worded as CF1b | — | — |
| CF1b | `caffeine pharmacokinetics CYP1A2 genotype metabolism interindividual variability` | run (rows 25) | 25 | 1 (Nehlig 2018) — ranking taken over by the journal *Drug Metabolism and Pharmacokinetics* |
| CF2 | `caffeine cognitive performance alertness withdrawal reversal systematic review` | 429 refused; variant `…mood withdrawal reversal net benefit review` also 429 refused | — | — |
| CF2b | `caffeine cognitive performance withdrawal reversal net benefit` | run (rows 25) | 25 | 13 (James 2005 ×3; Rogers 2005, 2008, 2012, 2014; Smith 2008; James 2014 ×2; Keane 2007; Phillips-Bute 1997; James & Rogers 2007) — the whole withdrawal-reversal debate with its replies |
| CF3 | `caffeine use disorder withdrawal DSM-5 diagnosis dependence validity` | CLIENT_ERROR; variant `…DSM diagnostic criteria dependence` also CLIENT_ERROR; re-worded as CF3b | — | — |
| CF3b | `caffeine withdrawal empirical validation of symptoms incidence severity` | run (rows 25) | 25 | 8 (Juliano 2004; Juliano 2012; Bodur 2024; Davoudi 2025; Ozsungur 2008; Lader 1996; Bruce 1991; Mills 2017; McGowan 1988) |
| CF4 | `coffee caffeine consumption cardiovascular disease mortality dose-response meta-analysis` | run (rows 25) | 25 | 11 (Crippa 2014; Aubin 2015 critique; Ding 2014; Grosso 2016; Cao 2022; Shahinfar 2021; Larsson 2018; Qi 2013; Lyngsø 2017; Torabynasab 2023; Asoudeh 2022) |
| CF5 | `coffee caffeine Mendelian randomization CYP1A2 blood pressure cardiovascular` | 429 refused; variant `coffee intake Mendelian randomization genetic variants CYP1A2 myocardial infarction` CLIENT_ERROR; re-worded as CF5b | — | — |
| CF5b | `coffee consumption Mendelian randomisation study cardiovascular outcomes` | run (rows 25) | 25 | 6 (Yuan 2021; Yuan 2019; Nicolopoulos 2020; Pham 2025; Carter 2022; Chen 2022) |
| CF6 | `energy drinks mixed with alcohol consumption risk young adults systematic review` | run (rows 25) | 25 | 15 (Peacock 2014; Roemer 2017; Speroni 2023; Marczinski 2011; Scalese 2023; Snipes 2015; Peacock 2015; Johnson 2016; Doggett 2019; Azagba 2013; Flotta 2014; Benson 2020; Pettigrew 2016; Caviness 2017; Vida 2015) |
| CF7 | `caffeine overdose toxicity fatalities powdered caffeine poisoning deaths` | run (rows 25) | 25 | 3 (Jones 2017; James 2012; Muncie 2012) — 20 of the 25 hits were *Reactions Weekly* case notes |
| CF8 | `maternal caffeine intake pregnancy birth weight miscarriage meta-analysis` | run (rows 25) | 25 | 11 (Chen 2014; Bracken 2014 critique; Chen 2015; Jin 2020; Soltani 2021 critique; Soltani 2021 MA; Sengpiel 2013; Rhee 2015; Okubo 2015; Collier 2009; Partosch 2015) |
| CF9 | `caffeine effects on sleep quality duration meta-analysis polysomnography` | run (rows 25) | 25 | 1 (Chang 2025) — ranking taken over by general sleep-epidemiology meta-analyses |
| CF10 | `coffee caffeine and sleep adenosine receptor tolerance mechanism review` | 429 refused; re-worded as CF10b | — | — |
| CF10b | `caffeine adenosine receptors brain mechanism of action tolerance humans` | run (rows 25) | 25 | 4 (Fredholm 1995; Holtzman 1990; Boulenger 1982; Fredholm 1982; Boulenger 1983) — Fredholm 1999 Pharmacol Rev did **not** surface; see Known gaps |
| CF11 | `coffee consumption and health umbrella review of meta-analyses multiple health outcomes` | run (rows 25) | 25 | 2 (Poole 2017, plus the second identically titled 2018 BMJ record treated as its correction) |

Searches that returned records: 10. Searches refused (429 or CLIENT_ERROR) and not re-run as written: 8.

### DOIs corrected or dropped at screening

- No DOI was recalled from memory, so none resolved to a different paper and none was corrected.
- 10.1136/eb-2014-102027 — an *Evidence Based Nursing* structured abstract of Chen 2014, not a study; excluded (the substantive commentary on that paper, Bracken 2014, is listed as #21).
- 10.18632/oncotarget.23947 — excluded on venue grounds under METHODS §3.2.
- 10.1123/ijsnem.2023-0135 — an erratum notice ("Erratum. CYP1A2 Genotype Polymorphism Influences the Effect of Caffeine on Anaerobic Performance in Trained Males") whose parent article's DOI was not returned by the query; neither could be listed, and the exercise-performance section is left to the PubMed layer.
- Conference abstracts excluded: 10.1093/sleep/zsaa056.427, 10.1016/j.sleep.2019.11.466.
- Non-indexed or low-quality venues excluded: 10.12775/jehs.2023.13.02.012, 10.14450/2318-9312.v35.e2.a2023.pp133-147, 10.5580/60c, 10.48047/hm.10.2.2024.1771-1780, 10.4103/mjbl.mjbl_107_22, 10.1051/shsconf/202112301015, 10.1016/j.drugalcdep.2014.09.344 (abstract), 10.3906/sag-0809-26.
- News-digest venues excluded wholesale: *Reactions Weekly*, *Inpharma Weekly*, *Reactions*.

### Errata/retractions

- Probable correction found: a second BMJ record, 10.1136/bmj.k194, carries the identical title to Poole et al. 2017 (10.1136/bmj.j5024) with a 2018 date and a very low citation count. Both are listed; the record type should be confirmed with a `works/10.1136/bmj.k194` fetch when the API allows.
- Retracted papers: none identified among the 78 retained.

Screening outcome: 78 journal articles retained into `Caffeine_DOI-LIST.md` (Tier A 27, Tier B 35, Tier C 16).

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count shown by PubMed next to each string and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(caffeine[Title] OR coffee[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type] OR "umbrella review"[Title]) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | Caffeine_pubmed_P1.csv | |
| P2 | `(caffeine[Title]) AND (pharmacokinetic* OR metabolism OR CYP1A2 OR "half-life" OR paraxanthine) AND (humans[MeSH Terms])` | Caffeine_pubmed_P2.csv | |
| P3 | `(caffeine[Title] OR coffee[Title]) AND ("CYP1A2" OR ADORA2A OR "genome-wide" OR genotype OR "gene-environment") AND (humans[MeSH Terms])` | Caffeine_pubmed_P3.csv | |
| P4 | `(caffeine[Title]) AND (cognit* OR alertness OR vigilance OR "psychomotor" OR attention) AND ("withdrawal reversal" OR withdrawal OR abstinence OR "net benefit")` | Caffeine_pubmed_P4.csv | |
| P5 | `(caffeine[Title] OR coffee[Title]) AND (sleep[Title] OR insomnia[Title] OR "sleep latency" OR polysomnograph*) AND (humans[MeSH Terms])` | Caffeine_pubmed_P5.csv | |
| P6 | `("caffeine withdrawal"[Title] OR "caffeine dependence"[Title] OR "caffeine use disorder"[Title] OR "caffeine intoxication"[Title])` | Caffeine_pubmed_P6.csv | |
| P7 | `(coffee[Title] OR caffeine[Title]) AND (mortality OR "cardiovascular" OR "coronary" OR stroke OR "atrial fibrillation" OR "blood pressure") AND (cohort OR meta-analysis[Publication Type])` | Caffeine_pubmed_P7.csv | |
| P8 | `(coffee OR caffeine) AND ("Mendelian randomization" OR "Mendelian randomisation") AND (humans[MeSH Terms])` | Caffeine_pubmed_P8.csv | |
| P9 | `("energy drink*"[Title]) AND (alcohol OR caffeine) AND (humans[MeSH Terms]) AND ("2010"[Date - Publication] : "3000"[Date - Publication])` | Caffeine_pubmed_P9.csv | |
| P10 | `(caffeine[Title]) AND (toxicity[Title] OR overdose[Title] OR poisoning[Title] OR fatal*[Title] OR "powdered caffeine" OR "caffeine powder")` | Caffeine_pubmed_P10.csv | |
| P11 | `(caffeine[Title] OR coffee[Title]) AND (pregnan*[Title] OR maternal[Title] OR fetal[Title] OR "birth weight"[Title] OR miscarriage[Title] OR "pregnancy loss"[Title])` | Caffeine_pubmed_P11.csv | |
| P12 | `("caffeine citrate"[Title] OR caffeine[Title]) AND ("apnea of prematurity" OR "apnoea of prematurity" OR preterm[Title]) AND (randomized controlled trial[Publication Type] OR "follow-up")` | Caffeine_pubmed_P12.csv | |
| P13 | `(caffeine[Title]) AND (anxiety[Title] OR panic[Title] OR "psychiatric" OR depression[Title] OR psychosis[Title]) AND (humans[MeSH Terms])` | Caffeine_pubmed_P13.csv | |
| P14 | `(caffeine[Title]) AND (clozapine OR theophylline OR "oral contraceptive*" OR ciprofloxacin OR fluvoxamine OR interaction[Title]) AND (humans[MeSH Terms])` | Caffeine_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `caffeine` in Cochrane Reviews; export the result list as CSV → `Caffeine_cochrane.csv`. The reviews specifically wanted are the caffeine-for-apnoea-of-prematurity reviews and any caffeine-for-cognitive-performance or energy-drink reviews — take the current `.pubN` version of each.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of every Tier-A review (#1, #2, #3, #10, #16, #17, #18, #19, #26). Forward: Google Scholar "cited by" on the landmarks — #3 (Juliano & Griffiths 2004), #4 (James & Rogers 2005), #10 (Poole 2017), #11 (Crippa 2014), #13 (Ding 2014), #20 (Chen 2014). The EFSA 2015 opinion's reference list is itself a near-complete bibliography of the caffeine safety literature to that date and should be mined in the backward pass.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included.
