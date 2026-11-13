# Ketamine — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening (re-worded re-runs of refused URLs are listed as such).

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-15)

Endpoint: `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=N&select=DOI,title,container-title,issued,author,updated-by` (targeted queries added `query.author=<family names>`). Hits screened by title and journal; conference abstracts (Eur Neuropsychopharmacol / Biol Psychiatry / Schizophr Res supplements, DAD CPDD abstracts, Reactions Weekly items), letters, "Re:" commentaries, preclinical papers and off-topic hits dropped.

Environment note: Crossref answered a large share of calls with HTTP 429 (rate limit on the shared proxy egress; several co-editors were querying Crossref in parallel). Per the brief, after each 429 no Crossref call was made for 90–150 s and the refused URL was never re-fetched; re-runs used different wording. Three URLs were refused for length (kept below ~250 characters thereafter). This limited the number of individual `works/<DOI>` re-fetches; every retained DOI nevertheless comes from a Crossref response that returned the record's title, journal, year, author and `updated-by` field. `filter=doi:` batch verification was not used.

### Section-level queries (pre-registered)

| # | Query string | Result |
|---|---|---|
| K1 | ketamine pharmacokinetics bioavailability intranasal oral intramuscular | URL refused (429); re-run as "ketamine clinical pharmacokinetics pharmacodynamics review": 15 hits, 1 retained (Peltoniemi 2016) |
| K2 | ketamine NMDA receptor pharmacology review mechanism | 15 hits, 0 retained (preclinical, abstracts) |
| K3 | ketamine healthy volunteers fMRI PET neuroimaging subanesthetic | URL refused; re-run "ketamine healthy volunteers neuroimaging PET fMRI": 15 hits, 4 retained (Ait Bentaleb 2023; Vollenweider 1997a; Malhotra 1996; McMillan 2019) |
| K4 | ketamine subanesthetic healthy volunteers psychotomimetic dissociative effects | target error; coverage obtained through T2–T5 (Krystal, Lahti, Breier, Newcomer) |
| K5 | ketamine recreational toxicity emergency department presentations | URL refused; re-run "ketamine abusers emergency department presentations Hong Kong case series": 15 hits, 2 retained (Weiner 2000; Lee 2011) |
| K6 | ketamine deaths drowning postmortem toxicology recreational | run as "ketamine in non-hospital and nontraditional fatalities": 6 hits, 2 retained (Gill 2000; Lalonde 2004); deaths otherwise covered by T8–T9 |
| K7 | ketamine dependence withdrawal tolerance recreational users | URL refused; re-run "ketamine withdrawal dependence tolerance users review": 20 hits, 0 retained (abstracts, Reactions Weekly) |
| K8 | ketamine chronic users cognitive memory longitudinal | covered by T1 (Morgan/Curran author query, 20 hits, 16 retained) |
| K9 | ketamine cystitis uropathy bladder recreational users | run as "ketamine cystitis urinary tract recreational users new syndrome": 20 hits, 5 retained |
| K10 | ketamine abdominal pain cholangiopathy biliary dilatation users | run as "ketamine abusers biliary dilatation cholangiopathy abdominal pain liver": 12 hits, 0 retained (abstracts, case reports in minor venues) — gap |
| K11 | ketamine depression randomized controlled trial meta-analysis | run as "ketamine major depression systematic review meta-analysis randomized controlled trials": 20 hits, 1 retained (An 2021); backbone obtained via T11–T22 |
| K12 | esketamine nasal spray treatment-resistant depression randomized | run via T14–T16, T37 (Daly/Popova/Fedgchin author and title queries) |
| K13 | ketamine recreational use prevalence epidemiology trends | run via T24 (Palamar author query): 15 hits, 7 retained; and T33 (Dillon/Copeland): 10 hits, 3 retained |
| K14 | 2-fluorodeschloroketamine arylcyclohexylamines new psychoactive substances | two URL variants refused (429); Morris & Wallach 2014 obtained via T34 — 2-FDCK remains a gap |
| K15 | ketamine driving impairment drivers | run as "ketamine driving impairment drivers roadside DUID": 12 hits, 2 retained (Cheng 2007; Lucuta 2024) |
| K16 | ketamine pregnancy prenatal exposure | run as "ketamine pregnancy prenatal exposure human outcomes": 12 hits, 0 retained (no human data) — gap |
| K17 | ketamine alcohol interaction combined use | not run (rate limit); Dickerson 2008 obtained via T2 — gap |
| K18 | ketamine model psychosis schizophrenia systematic review | run via T38 (Beck/Hallak): 8 hits, 1 retained (Beck 2020) |

### Targeted author/title queries (landmarks, critiques, follow-ups)

T1 query.author=Morgan Curran + "ketamine" (rows 20; 140 total): 16 retained. T2 Krystal + "ketamine humans": 2 retained (Krystal 1994; Dickerson 2008). T3 Vollenweider + "ketamine psychosis PET": 2 retained. T4 Lahti + "subanesthetic ketamine schizophrenia": 4 retained. T5 Breier + "ketamine induced psychosis healthy volunteers": 2 retained (Adler 1999; Malhotra 1997); Breier 1997 itself not surfaced in two author variants and one exact-title query (refused) — gap. T6 Shahani Chu + "ketamine ulcerative cystitis lower urinary tract": 4 retained. T7 "ketamine uropathy cystitis systematic review pathophysiology treatment": 4 retained. T8 Schifano + "ketamine deaths K-hole UK": 4 retained. T9 Darke + "ketamine death toxicity": 1 retained. T11 Zarate Berman + "ketamine antidepressant depression randomized": 2 retained. T12 "randomized trial N-methyl-D-aspartate antagonist treatment-resistant major depression Zarate": 3 retained. T13 "antidepressant effects of ketamine in depressed patients Berman": 1 retained. T14 Daly Popova Fedgchin + "esketamine nasal spray treatment-resistant depression": 2 retained. T15 "flexibly dosed esketamine nasal spray newly initiated oral antidepressant active-controlled": 1 retained (Popova 2019). T16 Daly + "esketamine relapse prevention adjunctive intranasal": 2 retained (Daly 2018; Drevets 2019 reply). T17 "esketamine seven concerns efficacy FDA approval word to the wise repeating mistakes": 3 retained (Turner 2019; Horowitz & Moncrieff 2021 [corrigendum]; Schatzberg 2019). T18 "ketamine electroconvulsive therapy nonpsychotic treatment-resistant depression noninferiority": 1 retained (Shafiee 2023); Anand + "ketamine ECT nonpsychotic depression": 1 retained (Anand 2023). T19 Nikolin + "ketamine treatment major depression meta-regression": 1 retained. T20 Short Wilkinson + "ketamine depression side-effects suicidal ideation systematic review": 4 retained. T21 Bahji + "racemic ketamine esketamine depression comparative efficacy": 2 retained (Bahji 2021 [erratum]; Bahji 2022). T22 Dean + "ketamine glutamate receptor modulators depression adults unipolar": 2 retained (Cochrane 2021 ×2). T23 Jansen Critchlow + "ketamine dependence non-medical use": 3 retained. T24 Palamar + "ketamine": 7 retained. T25 "bioavailability pharmacokinetics analgesic activity ketamine humans Clements": 3 retained. T26 Yanagihara + "ketamine norketamine plasma concentration preparations volunteers": 1 retained. T27 Zanos + "ketamine metabolite pharmacology mechanisms antidepressant": 2 retained. T28 "chronic ketamine use frontal white matter gray matter prefrontal dopaminergic recreational": 4 retained (Liao 2010, 2011; Narendran 2005; Liang 2020). T30 Newcomer + "ketamine NMDA hypofunction memory psychosis": 2 retained. T34 Morris Wallach + "PCP MXE dissociative review": 1 retained. T35 Murrough + "ketamine treatment-resistant major depression two-site randomized": 1 retained. T37 "esketamine oral antidepressant relapse prevention randomized clinical trial": 1 retained (Daly 2019). T38 Beck Hallak + "ketamine psychiatric symptoms schizophrenia therapeutic use": 1 retained.

Refused (429) and not re-run within this build: Grabski + "ketamine alcohol use disorder psychological therapy randomized" (KARE trial); Fedgchin TRANSFORM-1 title query; Liao Narendran author query (covered by T28); Gill Stajic author query (covered by K6).

### DOI corrections and update checks
- No recalled DOI was written into the list; all DOIs were copied from Crossref responses.
- Duplicate DOI noted: Morgan et al. 2004 (DAD source-memory paper) is registered under both 10.1016/j.drugalcdep.2004.03.006 and the PII form 10.1016/s0376-8716(04)00071-7; the former is listed.
- `updated-by` entries found: Morgan 2010 (erratum 10.1111/j.1360-0443.2010.02984.x, confirmed on individual fetch); Horowitz & Moncrieff 2021 (correction 10.1192/bjp.2021.40, confirmed); Bahji 2021 (erratum 10.1016/j.jad.2020.11.103, from search record); Zanos 2018 (search record reported an erratum, individual fetch showed no `updated-by` — check the journal's correction notice when saving). No retractions.
- Individual `works/<DOI>` re-fetches: 24 attempted, 22 resolved to the intended paper (listed in the DOI list's Verification block); 2 refused by the proxy (Malhotra 1996, both case variants; one transient robots error on Schifano 2008 later resolved).

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count shown next to each string and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(ketamine[Title] OR esketamine[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type] OR "systematic review"[Title] OR "meta-analysis"[Title])` | ketamine_pubmed_P1.csv | |
| P2 | `(ketamine[Title]) AND (recreational OR "non-medical" OR nonmedical OR abuse OR misuse OR illicit) AND (humans[MeSH Terms]) AND ("2012"[Date - Publication] : "3000"[Date - Publication])` | ketamine_pubmed_P2.csv | |
| P3 | `(ketamine[Title]) AND (cystitis OR uropathy OR bladder OR "lower urinary tract" OR vesicopathy) AND (humans[MeSH Terms])` | ketamine_pubmed_P3.csv | |
| P4 | `(ketamine[Title]) AND (cholangiopathy OR "biliary" OR "abdominal pain" OR cramps OR hepat*) AND (humans[MeSH Terms])` | ketamine_pubmed_P4.csv | |
| P5 | `(ketamine[Title]) AND (cognit* OR memory OR neuropsycholog*) AND (chronic OR frequent OR recreational OR "long-term") AND (humans[MeSH Terms])` | ketamine_pubmed_P5.csv | |
| P6 | `(ketamine[Title]) AND (death OR deaths OR fatal* OR mortality OR drowning OR postmortem OR "post-mortem") AND (humans[MeSH Terms])` | ketamine_pubmed_P6.csv | |
| P7 | `(ketamine[Title]) AND (dependence OR withdrawal OR tolerance OR "use disorder" OR craving) AND (humans[MeSH Terms])` | ketamine_pubmed_P7.csv | |
| P8 | `(ketamine[Title]) AND (pharmacokinetic* OR bioavailability OR "half-life" OR norketamine OR "hydroxynorketamine") AND (humans[MeSH Terms])` | ketamine_pubmed_P8.csv | |
| P9 | `(ketamine[Title]) AND (healthy volunteers OR "healthy subjects") AND (psychotomimetic OR dissociat* OR "model psychosis" OR schizophrenia) AND (humans[MeSH Terms])` | ketamine_pubmed_P9.csv | |
| P10 | `(ketamine[Title] OR esketamine[Title]) AND (depress*) AND (randomized controlled trial[Publication Type])` | ketamine_pubmed_P10.csv | |
| P11 | `(esketamine[Title]) AND (concern* OR critique OR "FDA approval" OR "evidence" OR "mistakes")` | ketamine_pubmed_P11.csv | |
| P12 | `("2-fluorodeschloroketamine" OR "2F-DCK" OR "2-FDCK" OR methoxetamine OR deschloroketamine OR arylcyclohexylamine*) AND (humans[MeSH Terms] OR intoxication OR death OR seizure*)` | ketamine_pubmed_P12.csv | |
| P13 | `(ketamine[Title]) AND (driving OR drivers OR "under the influence" OR DUID)` | ketamine_pubmed_P13.csv | |
| P14 | `(ketamine[Title]) AND (prevalence OR epidemiolog* OR trends OR "poison control" OR seizures OR wastewater) AND ("2015"[Date - Publication] : "3000"[Date - Publication]) AND (humans[MeSH Terms])` | ketamine_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `ketamine` and `esketamine` in Cochrane Reviews; export the result lists as CSV → `ketamine_cochrane.csv`.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of every Tier-A review (items 1, 2, 3, 12, 21, 32, 33, 34, 35b). Forward: Google Scholar "cited by" on items 6, 17, 18, 20, 22, 26, 27, 28, 31 (landmarks and critiques). Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included.
