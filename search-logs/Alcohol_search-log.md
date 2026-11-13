# Alcohol — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening.

## Layer 1 — Crossref bibliographic search (run by AI, 2026-10-15)

### Conditions
Crossref's REST API throttled this session for most of the day: HTTP 429 ("rate limited, retry after ~60 s") after every 1–10 requests, on both the `works?query` and the `works/<DOI>` endpoints, with 90-s pauses after each refusal as the brief requires. A refused URL was never re-fetched as written; `works/<DOI>` re-tries used a case-variant of the DOI (DOIs are case-insensitive). Because the search endpoint was refused far more often than the record endpoint, the method was adapted: landmark and backbone papers were verified directly by `works/<DOI>` from recalled DOIs (every recalled DOI was treated as unverified until Crossref echoed the intended title; three recalled DOIs resolved to other papers and were dropped or corrected, see below), and the pre-specified section queries were run only where the endpoint allowed. Two DOIs were verified from Crossref works-search records (marked † in the list) rather than `works/<DOI>`.

### Pre-specified section queries (16; `filter=type:journal-article`, `rows=15`, relevance-sorted)

| # | Query string | Status | Hits screened | Retained |
|---|---|---|---|---|
| A1 | `alcohol use disorder epidemiology prevalence NESARC-III DSM-5` | 429 refused (not re-run); pilot variant `alcohol use disorder prevalence NESARC epidemiology` run | 15 | 0 (Tucker 2020 ARCR and Lee 2023 Clin Liver Dis noted for the PubMed layer) |
| A2 | `alcohol consumption cirrhosis dose-response meta-analysis` | 429 refused | — | — (covered by recalled Rehm 2010, Roerecke 2019) |
| A3 | `alcohol consumption cancer risk dose-response meta-analysis` | 429 refused; targeted title query for Bagnardi 2015 run instead | 5 | 1 (Bagnardi 2015; Corrao 1999 noted) |
| A4 | `alcohol cardiovascular disease Mendelian randomization J-shaped` | run (minimal URL form) | 10 | 1 (Larsson 2020) |
| A5 | `moderate alcohol mortality systematic error abstainer bias meta-analysis` | 429 refused twice | — | — (covered by recalled Stockwell 2016/2024, Zhao 2023, Chikritzhs 2015) |
| A6 | `alcohol withdrawal delirium tremens management benzodiazepines meta-analysis` | run | 15 | 1 (Eyer 2011) |
| A7 | `naltrexone acamprosate alcohol dependence randomized trial meta-analysis` | not run (rate limit) | — | — (covered by recalled Cochrane/JAMA reviews) |
| A8 | `alcohol hangover systematic review pathophysiology` | not run | — | — (covered by recalled Penning, Verster, Pittler, Roberts, Wiese) |
| A9 | `ethanol pharmacokinetics elimination rate alcohol dehydrogenase sex differences` | not run | — | — |
| A10 | `fetal alcohol spectrum disorder prevalence meta-analysis prenatal alcohol exposure` | not run | — | — |
| A11 | `alcohol dementia cognitive decline brain structure cohort` | not run | — | — |
| A12 | `acute alcohol cognitive impairment driving crash risk blood alcohol concentration` | not run | — | — |
| A13 | `alcohol poisoning deaths blood ethanol concentration fatal intoxication` | not run | — | — (gap: see list) |
| A14 | `alcohol opioid benzodiazepine interaction respiratory depression overdose` | not run | — | — |
| A15 | `alcohol minimum unit pricing taxation policy mortality` | not run | — | — |
| A16 | `alcohol global burden of disease no safe level Lancet critique` | not run | — | — |

Targeted author/title queries run (`query.author` + `query.bibliographic`, rows 3–5): Goodson 2014 (→ 10.1111/acer.12529); Palpacuer 2018 (→ 10.1111/add.13974); Bagnardi 2015 (confirmed 10.1038/bjc.2014.579); Fillmore 2006 (429 refused).

### DOIs corrected or dropped at verification
- 10.1111/acer.12504 (recalled for Goodson 2014) resolves to Monk et al. 2014 → corrected to 10.1111/acer.12529.
- 10.1111/add.14058 (recalled for Palpacuer 2018) resolves to Rubenis et al. 2017 → corrected to 10.1111/add.13974.
- 10.1111/j.1360-0443.2005.01010.x (recalled for Dawson 2005) resolves to a Casswell 2005 commentary → Dawson 2005 moved to Known gaps.
- Unresolvable within the session (repeat CLIENT_ERROR, no search slot): Roerecke 2017 (blood pressure), Fillmore 2006, Wood 2018 JAMA, Cederbaum 2012 → Known gaps.

### Errata/retractions
Errata or corrections found on: Bryazka 2022 (GBD 2020); Wood 2018 (Lancet); Mewton 2023; Henderson 2007. Retracted: none. Superseded Cochrane version: Minozzi 2018 baclofen (pub2) → Agabio 2023 (pub3) listed.

Screening outcome: 134 journal articles retained into `Alcohol_DOI-LIST.md` (Tier A 37, Tier B 75, Tier C 22).

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count shown by PubMed next to each string and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(alcohol[Title] OR ethanol[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type] OR "umbrella review"[Title]) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | Alcohol_pubmed_P1.csv | |
| P2 | `(alcohol[Title]) AND ("all-cause mortality" OR "J-shaped" OR "abstainer" OR "former drinkers") AND (meta-analysis OR cohort) AND (humans[MeSH Terms])` | Alcohol_pubmed_P2.csv | |
| P3 | `(alcohol[Title]) AND ("Mendelian randomization" OR "Mendelian randomisation" OR ALDH2 OR ADH1B) AND (cardiovascular OR "coronary" OR stroke OR cancer OR mortality)` | Alcohol_pubmed_P3.csv | |
| P4 | `(alcohol[Title]) AND (cancer[Title] OR carcinoma[Title] OR neoplasm[Title]) AND ("dose-response" OR "dose response") AND (meta-analysis OR "pooled analysis")` | Alcohol_pubmed_P4.csv | |
| P5 | `(alcohol[Title]) AND (cirrhosis[Title] OR "liver disease"[Title] OR hepatitis[Title]) AND (meta-analysis OR cohort OR guideline) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | Alcohol_pubmed_P5.csv | |
| P6 | `("alcohol withdrawal"[Title] OR "delirium tremens"[Title]) AND (humans[MeSH Terms]) AND ("2010"[Date - Publication] : "3000"[Date - Publication])` | Alcohol_pubmed_P6.csv | |
| P7 | `("alcohol use disorder"[Title] OR "alcohol dependence"[Title]) AND (randomized controlled trial[Publication Type]) AND (naltrexone OR acamprosate OR disulfiram OR nalmefene OR baclofen OR topiramate OR gabapentin OR varenicline OR psilocybin OR ketamine OR semaglutide)` | Alcohol_pubmed_P7.csv | |
| P8 | `(hangover[Title]) AND (humans[MeSH Terms])` | Alcohol_pubmed_P8.csv | |
| P9 | `(ethanol[Title] OR alcohol[Title]) AND (pharmacokinetic* OR "elimination rate" OR "first-pass" OR "breath alcohol") AND (humans[MeSH Terms]) AND ("2005"[Date - Publication] : "3000"[Date - Publication])` | Alcohol_pubmed_P9.csv | |
| P10 | `("fetal alcohol"[Title] OR "prenatal alcohol"[Title]) AND (prevalence OR meta-analysis OR cohort OR guideline) AND ("2012"[Date - Publication] : "3000"[Date - Publication])` | Alcohol_pubmed_P10.csv | |
| P11 | `(alcohol[Title]) AND (dementia[Title] OR "cognitive decline"[Title] OR "brain volume"[Title] OR "gray matter"[Title] OR Korsakoff[Title] OR Wernicke[Title]) AND (humans[MeSH Terms]) AND ("2010"[Date - Publication] : "3000"[Date - Publication])` | Alcohol_pubmed_P11.csv | |
| P12 | `("alcohol poisoning"[Title] OR "ethanol poisoning"[Title] OR "acute alcohol intoxication"[Title] OR "blood alcohol concentration"[Title]) AND (death OR fatal OR mortality OR "emergency department")` | Alcohol_pubmed_P12.csv | |
| P13 | `(alcohol[Title]) AND (opioid* OR benzodiazepine* OR "energy drink*" OR caffeine OR cocaine OR cannabis) AND (interaction OR "co-use" OR combined OR "respiratory depression") AND (humans[MeSH Terms]) AND ("2010"[Date - Publication] : "3000"[Date - Publication])` | Alcohol_pubmed_P13.csv | |
| P14 | `(alcohol[Title]) AND ("minimum unit pricing" OR taxation OR "tax" OR "availability" OR "advertising" OR "drink-driving" OR "drink driving") AND (policy OR evaluation OR "interrupted time series" OR meta-analysis)` | Alcohol_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `alcohol` in Cochrane Reviews (Drugs and alcohol group); export the result list as CSV → `Alcohol_cochrane.csv`.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of every Tier-A review. Forward: Google Scholar "cited by" on items 1, 3, 4, 5, 8, 13, 17, 19, 22, 27, 29, 33, 34 (landmarks). Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included.
