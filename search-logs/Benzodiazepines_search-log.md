# Benzodiazepines — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening.

## Layer 1 — Crossref bibliographic search (run by AI, 2026-10-15)

### Conditions

Crossref's REST API was throttled throughout this session: HTTP 429 ("rate limited, retry after ~60 s") after roughly every second request, on the `works?query` endpoint, and the `works/<DOI>` record endpoint was unusable. Pauses of 90–240 s were taken after every refusal, as the brief requires, and a refused URL was never re-fetched as written. Direct (non-WebFetch) access to `api.crossref.org` is blocked in this environment, so no alternative pacing was available.

Two adaptations followed. First, **every DOI in the list was taken verbatim from a Crossref works-search record returned in this session**, rather than recalled and then checked with `works/<DOI>`: a search record carries the same DOI, title, container-title, year and `update`/`updated-by` fields, and this made each successful request verify 3–10 papers instead of one. Second, two filters were tested and rejected: `filter=doi:<doi>,doi:<doi>…` is **not** a Crossref filter (it is silently ignored and the whole corpus is returned — 185 million records; do not use it), and the WebFetch proxy refuses any URL longer than roughly 250 characters, which caps a query at about 90 characters of search terms with the standard `select` list.

Consequence for coverage: 14 of ~20 planned section queries returned records. The list is therefore strong on dependence/withdrawal, the dementia debate, designer benzodiazepines, flumazenil and prescribing/overdose epidemiology, and thin on neuroscience, driving, pregnancy, deprescribing trials and the Cochrane intervention layer. Those are itemised by title in the "Known gaps" paragraph of `Benzodiazepines_DOI-LIST.md`.

### Pre-specified section queries (`filter=type:journal-article`, relevance-sorted)

| # | Query string | Status | Hits screened | Retained |
|---|---|---|---|---|
| B1 | `benzodiazepine dependence withdrawal syndrome systematic review` | 429 refused (not re-run) | — | — |
| B2 | `benzodiazepine discontinuation taper long-term users randomized trial` | run (rows 15) | 15 | 3 (Rickels 1999; Maust 2023; Golombok 1988) |
| B3 | `concurrent benzodiazepine opioid prescription overdose death cohort` | 429 refused; re-worded as B3b | — | — |
| B3b | `benzodiazepine opioid overdose death risk cohort` | run (rows 15) | 15 | 3 (Hernandez 2018; Park 2015; Chua 2021) |
| B4 | `benzodiazepine use risk of dementia Alzheimer disease cohort` | run (rows 15) | 15 | 1 (Saarelainen 2017); low yield, Crossref relevance dominated by generic "dementia cohort" hits |
| B5 | `benzodiazepine dementia protopathic bias systematic review meta-analysis` | 429 refused twice (not re-run); re-worded as B5b | — | — |
| B5b | `benzodiazepine dementia meta-analysis protopathic bias` | run (rows 20) | 20 | 4 (Penninkilampi 2018; Zhong 2015; He 2019; Horwitz & Feinstein 1980) |
| B6 | `Benzodiazepine use and risk of dementia prospective population based study` | run (rows 20) | 20 | 5 (Billioti de Gage 2012; Gray 2016; vom Hofe 2024; Gallacher 2011; Cho 2026) |
| B7 | `cognitive effects long-term benzodiazepine use meta-analysis withdrawal persistence` | 429 refused; variants `…neuropsychological performance meta-analysis` (CLIENT_ERROR) and `cognitive effects of long-term benzodiazepine use meta-analysis` (429) also refused | — | — (Barker 2004 ×2 remain gaps) |
| B8 | `designer benzodiazepines etizolam flualprazolam bromazolam` | run (rows 30) | 30 | 13 (Zawilska 2019; Moosmann 2015; Brunetti 2021; Rodda 2024; El Balkhi 2023; Yu 2023; Wilde 2021; Moustafa 2021; Høiseth 2016; Wagmann 2020; Maskell 2023 + its correction; Shoff 2026; Ballotari 2025; Canfield 2023; Theofel 2022; Drevin 2022; Girard 2024; Bade 2020; Bazydlo 2025) |
| B9 | `benzodiazepine z-drug hip fracture falls older adults meta-analysis` | run (rows 30) | 30 | 1 (Zint 2010); low yield — "falls older adults" swamped the ranking |
| B10 | `Benzodiazepines Z-drugs and the risk of hip fracture` | run (rows 25) | 25 | 4 (Donnelly 2017; Cumming 2003; Ray 1989; Nurmi-Lüthje 2006) |
| B11 | `benzodiazepine use misuse and use disorders among adults in the United States` | run (rows 25) | 25 | 4 (Blanco 2018; Maust 2019; McHugh 2021; Votaw 2025) |
| B12 | `Ashton benzodiazepine withdrawal protracted syndrome diagnosis management dependence` | run (rows 25) | 25 | 10 (Ashton 1984, 1987, 1991, 1994, 1995, 2005; Pétursson 1994; Schweizer & Rickels 1998; Marriott & Tyrer 1993; Authier 2009) |
| B13 | `flumazenil benzodiazepine intoxication adverse events antidote coma seizure` | run (rows 25) | 25 | 6 (Penninga 2015 SR/MA + the three published letters and replies; Hieger 2024; Hanson 2026) |
| B14 | `zolpidem zopiclone Z-drug dependence insomnia hypnotics efficacy meta-analysis` | run (rows 25) | 25 | 5 (Hajak 2003; Nowell 1997; Gustavsen 2008; Morera-Fumero 2020; Nguyen 2025) |
| B15 | `GABAA receptor subtypes benzodiazepine addiction dopamine neurons pharmacology` | 429 refused; variants `…addiction hooked` (CLIENT_ERROR) and `…addiction reward neural basis` (429) also refused | — | — (Tan 2010/2011, Rudolph 2011 remain gaps) |
| B16 | `benzodiazepine pharmacokinetics GABAA receptor subunit selectivity clinical` | run (rows 25) | 25 | 2 (Pritchett 1989; Engin 2023); the remainder was preclinical molecular work excluded under METHODS §5.4 |
| B17 | `increasing benzodiazepine prescriptions and overdose mortality in the United States` | run (rows 25) | 25 | 7 (Bachhuber 2016; Tori 2020; Zhang 2022; Olfson 2026; Zoorob 2018; Bushnell 2022; Ramdin 2024) |
| B18 | `interventions for benzodiazepine discontinuation Cochrane systematic review psychosocial pharmacological` | run (rows 25) — **returned 25 entirely off-topic records** (Crossref relevance failure on an all-common-words string); 0 retained | 25 | 0 |
| B19 | `effectiveness of current treatment approaches for benzodiazepine discontinuation a meta-analysis` | run (rows 20) | 20 | 6 (Parr 2008; Huedo-Medina 2012; Roy-Byrne 1990; Wright 2015; Zhang 2026; van de Steeg-van Gompel 2009 and Gorgels 2005 carried from B2's result set) |

Searches that returned records: 14. Searches refused (429) or failed (CLIENT_ERROR) and not re-run as written: 10.

### DOIs corrected or dropped at screening

- No DOI was recalled from memory, so no DOI resolved to a different paper and none was corrected.
- 10.1002/14651858.cd011481 — Crossref record is the Cochrane **protocol** (2015), not Baandrup et al.'s review; excluded, and the review is listed under Known gaps so the senior author does not save the protocol by mistake.
- 10.1097/xeb.0000000000000161 — an *International Journal of Evidence-Based Healthcare* summary of that Cochrane review, not the review; excluded.
- 10.1002/alz.074601 and 10.1016/j.jalz.2017.06.602 — conference abstracts of papers already listed in full (vom Hofe 2024; Penninkilampi 2018); excluded.
- 10.1136/bmj.323.7315.752a and 10.1136/bmj.323.7315.752/a — two Crossref records for one 2001 BMJ author's reply on benzodiazepines and hip fracture; both left out pending a `works/<DOI>` check of which is canonical.
- News-digest venues excluded wholesale as not peer-reviewed primary sources: *Reactions Weekly*, *Inpharma Weekly*, *The Pharmaceutical Journal*, *Clinical Pharmacist*, *Alcoholism & Drug Abuse Weekly*, *Case Medical Research*.

### Errata/retractions

- Correction found: Maskell et al. 2023, *Designer benzodiazepines gidazepam and desalkygidazepam (bromonordiazepam): what do we know?* (J Anal Toxicol, 10.1093/jat/bkad004) — correction published as 10.1093/jat/bkad035. Both to be obtained.
- Retracted papers: none identified among the 85 listed.
- Superseded version noted: the Cochrane discontinuation review exists as protocol (CD011481) and review (CD011481.pub2); only the review is wanted.

Screening outcome: 86 journal articles retained into `Benzodiazepines_DOI-LIST.md` (Tier A 35, Tier B 33, Tier C 18). The 86th, Hikin et al. 2024 on post-mortem bromazolam concentrations in 96 coronial cases (10.1016/j.forsciint.2023.111891), was returned and verified by query G7 of the GHB-GBL log and carried across.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count shown by PubMed next to each string and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(benzodiazepine*[Title] OR diazepam[Title] OR alprazolam[Title] OR lorazepam[Title] OR clonazepam[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type] OR "umbrella review"[Title]) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | Benzodiazepines_pubmed_P1.csv | |
| P2 | `("benzodiazepine withdrawal"[Title] OR "benzodiazepine dependence"[Title] OR "benzodiazepine discontinuation"[Title] OR deprescrib*[Title]) AND (humans[MeSH Terms])` | Benzodiazepines_pubmed_P2.csv | |
| P3 | `(benzodiazepine*[Title]) AND (taper* OR discontinu* OR withdraw*) AND (randomized controlled trial[Publication Type] OR "cluster randomised" OR "cluster randomized")` | Benzodiazepines_pubmed_P3.csv | |
| P4 | `(benzodiazepine*[Title]) AND (opioid*[Title] OR "co-prescri*" OR concurrent OR concomitant) AND (overdose OR mortality OR "respiratory depression" OR death*) AND (humans[MeSH Terms])` | Benzodiazepines_pubmed_P4.csv | |
| P5 | `(benzodiazepine*[Title] OR "z-drug*"[Title] OR zolpidem[Title] OR zopiclone[Title]) AND (dementia[Title] OR "cognitive decline"[Title] OR "cognitive impairment"[Title] OR Alzheimer*[Title]) AND (humans[MeSH Terms])` | Benzodiazepines_pubmed_P5.csv | |
| P6 | `(benzodiazepine*[Title]) AND (dementia OR Alzheimer*) AND ("protopathic" OR "reverse causation" OR "reverse causality" OR "confounding by indication" OR "lag time" OR "immortal time")` | Benzodiazepines_pubmed_P6.csv | |
| P7 | `(benzodiazepine*[Title] OR "z-drug*"[Title]) AND (fall*[Title] OR fracture*[Title] OR "motor vehicle" OR driving OR crash) AND (humans[MeSH Terms])` | Benzodiazepines_pubmed_P7.csv | |
| P8 | `("designer benzodiazepine*" OR etizolam OR flualprazolam OR bromazolam OR flubromazolam OR clonazolam OR phenazepam OR "desalkylgidazepam" OR "novel benzodiazepine*")` | Benzodiazepines_pubmed_P8.csv | |
| P9 | `(benzodiazepine*[Title]) AND (prescri*[Title] OR trend*[Title] OR epidemiolog*[Title] OR misuse[Title]) AND ("2010"[Date - Publication] : "3000"[Date - Publication]) AND (humans[MeSH Terms])` | Benzodiazepines_pubmed_P9.csv | |
| P10 | `(flumazenil[Title]) AND (overdose OR poisoning OR intoxication OR coma OR seizure* OR antidote)` | Benzodiazepines_pubmed_P10.csv | |
| P11 | `("GABA-A" OR "GABAA" OR "gamma-aminobutyric acid type A") AND benzodiazepine*[Title] AND (subtype* OR subunit* OR addiction OR reward OR tolerance) AND (review[Publication Type] OR humans[MeSH Terms])` | Benzodiazepines_pubmed_P11.csv | |
| P12 | `(benzodiazepine*[Title] OR "z-drug*"[Title]) AND (pregnan*[Title] OR neonat*[Title] OR "congenital malformation*" OR teratogen*) AND (humans[MeSH Terms])` | Benzodiazepines_pubmed_P12.csv | |
| P13 | `(benzodiazepine*[Title]) AND ("anxiety disorder*"[Title] OR insomnia[Title] OR "panic disorder"[Title]) AND (randomized controlled trial[Publication Type] OR meta-analysis[Publication Type]) AND ("2010"[Date - Publication] : "3000"[Date - Publication])` | Benzodiazepines_pubmed_P13.csv | |
| P14 | `(benzodiazepine*[Title]) AND ("drug checking" OR "unregulated supply" OR "illicit" OR "counterfeit" OR "wastewater" OR "post-mortem" OR "postmortem") AND ("2018"[Date - Publication] : "3000"[Date - Publication])` | Benzodiazepines_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `benzodiazepine` in Cochrane Reviews (Drugs and Alcohol group, plus Common Mental Disorders); export the result list as CSV → `Benzodiazepines_cochrane.csv`. The three reviews specifically wanted are Denis et al. (mono-dependence, pharmacological), Darker et al. (psychosocial interventions) and Baandrup et al. (discontinuation in chronic users) — take the current `.pubN` version of each, not the protocol.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of every Tier-A review (#4, #6, #7, #20, #24, #25, #26, #30, #32, #35). Forward: Google Scholar "cited by" on the landmarks — #1 (Ashton 1984), #9 (Park 2015), #14 (Billioti de Gage 2012), #16 (Gray 2016), #23 (Ray 1989), #26 (Penninga 2015), #34 (Pritchett 1989). Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included.
