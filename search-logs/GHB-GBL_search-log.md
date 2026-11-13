# GHB-GBL — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening.

## Layer 1 — Crossref bibliographic search (run by AI, 2026-10-15)

### Conditions

Crossref's REST API was throttled throughout this session: HTTP 429 after roughly every second request, plus intermittent `CLIENT_ERROR` and `ROBOTS_DISALLOWED` refusals from the same host. Pauses of 90–240 s were taken after every refusal, and a refused URL was never re-fetched as written. Direct (non-WebFetch) access to `api.crossref.org` is blocked in this environment.

As with the benzodiazepine list, **every DOI was taken verbatim from a Crossref works-search record returned in this session** rather than recalled and then checked with `works/<DOI>`, because the record endpoint was unusable and a search record carries the same metadata. Two mechanical constraints shaped the strings: the WebFetch proxy refuses URLs longer than roughly 250 characters (so a query is capped at about 90 characters of terms), and a literal comma inside a query term — `1,4-butanediol` — triggers a `ROBOTS_DISALLOWED` refusal, so the precursor had to be searched as `butanediol`.

### Pre-specified section queries (`filter=type:journal-article`, relevance-sorted)

| # | Query string | Status | Hits screened | Retained |
|---|---|---|---|---|
| G1 | `gamma-hydroxybutyrate GHB pharmacokinetics dose response effects humans` | run (rows 25) | 25 | 4 (Brenneisen 2004; Krul 2011; McDaniel 2001; Goodwin 2009) |
| G2 | `GHB overdose coma emergency department intoxication case series` | 429 refused; re-worded as G2b | — | — |
| G2b | `gamma-hydroxybutyrate intoxication emergency department coma prospective series` | run (rows 25) | 25 | 9 (van Helmond 2020; Smits 2021; Berling 2024; Munir 2008; Abid 2021; Stomberg 2014; Shannon 2000; Kohrs 1999; Eckstein 1999) |
| G3 | `gamma-hydroxybutyrate withdrawal syndrome delirium detoxification management` | run (rows 25) | 25 | 11 (Dyer 2001; McDonough 2004; Tarabar 2004; van Noorden 2009; van Noorden 2015; Cappetta 2019; Borelli 2025; Rosenberg 2003; Liao 2018; Habibian 2019; Marinelli 2020; Chin 2001) |
| G4 | `GHB dependence detoxification pharmaceutical gamma-hydroxybutyrate titration relapse` | run (rows 25) | 25 | 10 (Dijkstra 2017; de Jong 2011; Kamal 2016; Kamal 2015; Kamal 2014; Scheuber 2026; Carter 2009; Sumnall 2008; Brunt 2013; Goodwin 2012) |
| G5 | `chemsex GHB mephedrone methamphetamine men who have sex with men` | CLIENT_ERROR; re-worded as G5b | — | — |
| G5b | `chemsex sexualised drug use GHB GBL men who have sex with men` | run (rows 25) | 25 | 10 (Maxwell 2019; Tomkins 2018; Georgiadis 2025; Wang 2023; Hibbert 2019; Hibbert 2021; Drückler 2021; Hsu 2024; Íncera-Fernández 2021; Stevens 2019) |
| G6 | `gamma-butyrolactone 1,4-butanediol conversion GHB precursor toxicity humans` | ROBOTS_DISALLOWED (the literal comma in `1,4-` breaks the fetch); variant without the comma also refused; re-worded as G6b | — | — |
| G6b | `gamma-butyrolactone GBL butanediol GHB precursors toxicity` | run (rows 25) | 25 | 12 (Wood 2011; Wood 2007; Corkery 2015; Dufayet 2023; Liechti 2004; Schneir 2001; Choudhuri 2013; Hennessy 2004; Munshi 2012; Elliott 2005; LeBeau 2000; Lonsdale 2021) |
| G7 | `GHB alcohol co-ingestion fatalities post-mortem blood concentrations deaths` | run (rows 25) | 25 | 5 (Korb 2014; Busardò 2014; Castro 2016; Jones 2018; Kalasinsky 2001). **Note:** this query also returned, verified, two records wanted by other substances' lists — Jones 2017, *Review of caffeine-related fatalities along with postmortem blood concentrations in 51 poisoning deaths* (10.1093/jat/bkx011), carried to the Caffeine list, and Hikin 2024, *Post mortem blood bromazolam concentrations and co-findings in 96 coronial cases within England and Wales* (10.1016/j.forsciint.2023.111891), carried to the Benzodiazepines list. |
| G8 | `GHB induced coma long-term cognitive effects neurotoxicity overdose users` | run (rows 25) | 25 | 5 (van Amsterdam 2012; Raposo Pereira 2018; Degenhardt 2003; Morse 2012; Marinetti 2005) |
| G9 | `GHB GABA-B receptor mechanism pharmacology sodium oxybate narcolepsy trial` | 429 refused; re-worded as G9b | — | — |
| G9b | `gamma-hydroxybutyrate GABAB receptor mechanism of action sodium oxybate review` | run (rows 25) | 25 | 4 (Pardi 2006; Madden 1998; Williams 1995; Huang 2009). Sodium-oxybate RCTs did **not** surface; see Known gaps |
| G10 | `GHB drug-facilitated sexual assault detection prevalence nightlife survey` | run (rows 25) | 25 | 11 (Goullé 2003; Busardò 2016 ×2; Busardò 2023 letter + Mestria 2023 reply; Prego-Meleiro 2024; Chatzichristos 2026; Lee 2024; Stillwell 2002; Elian 2000; Mehling 2016) |
| G11 | `GHB use prevalence trends harm reduction nightlife recreational users survey` | run (rows 25) | 25 | 2 (Bendau 2025; Freestone 2023); the rest of the ranking was taken over by unrelated *Harm Reduction Journal* content |

Searches that returned records: 10. Searches refused (429, CLIENT_ERROR, ROBOTS_DISALLOWED) and not re-run as written: 6.

### DOIs corrected or dropped at screening

- No DOI was recalled from memory, so none resolved to a different paper and none was corrected.
- Conference abstracts excluded in favour of the full papers: 10.1016/s0924-977x(17)31860-6, 10.1016/s0924-977x(17)30165-7, 10.1016/j.euroneuro.2018.11.734 (Raposo Pereira), 10.1016/j.eurpsy.2017.01.2002 (Michielsen), 10.1093/sleepj/zsx050.822 and 10.1093/sleep/zsad077.0591 (sodium oxybate), 10.1096/fasebj.21.5.a413-d (Goodwin), 10.1055/s-0033-1351547 (*Suchttherapie* congress abstract of the Dutch GHB Monitor, whose full papers are #12 and #13).
- 10.1186/1757-1627-2-6530 and 10.1186/1757-1626-2-6530 — two Crossref records for one 2009 *Cases Journal* case report; both excluded.
- Single case reports in low-citation or non-indexed venues excluded where a case series covered the same point: 10.7759/cureus.25728, 10.7727/wimjopen.2014.263, 10.4172/2329-6488.1000156, 10.58837/chula.cmj.48.7.5, 10.5350/dajpn2017300111.
- News-digest venues excluded wholesale: *Reactions Weekly*, *InPharma*, *Journal of Emergency Nursing*, *Emergency Medicine News*.

### Errata/retractions

None found among the 84 retained papers. One published critique/reply pair was captured and both halves are listed (#53 Busardò et al. letter; #54 Mestria et al. response).

Screening outcome: 84 journal articles retained into `GHB-GBL_DOI-LIST.md` (Tier A 26, Tier B 37, Tier C 21).

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count shown by PubMed next to each string and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `("gamma-hydroxybutyrate"[Title] OR "gamma hydroxybutyrate"[Title] OR GHB[Title] OR "sodium oxybate"[Title] OR "gamma-butyrolactone"[Title] OR GBL[Title] OR "1,4-butanediol"[Title])` | GHB-GBL_pubmed_P1.csv | |
| P2 | `(GHB[Title] OR "gamma-hydroxybutyrate"[Title] OR "sodium oxybate"[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type] OR review[Publication Type])` | GHB-GBL_pubmed_P2.csv | |
| P3 | `(GHB[Title] OR "gamma-hydroxybutyrate"[Title] OR "gamma-butyrolactone"[Title]) AND (overdose OR intoxication OR coma OR poisoning OR "emergency department") AND (humans[MeSH Terms])` | GHB-GBL_pubmed_P3.csv | |
| P4 | `(GHB[Title] OR "gamma-hydroxybutyrate"[Title] OR "gamma-butyrolactone"[Title]) AND (withdrawal OR dependence OR detoxification OR "use disorder") AND (humans[MeSH Terms])` | GHB-GBL_pubmed_P4.csv | |
| P5 | `("sodium oxybate"[Title] OR "oxybate"[Title]) AND (narcolepsy OR cataplexy OR fibromyalgia OR "alcohol withdrawal" OR "alcohol dependence") AND (randomized controlled trial[Publication Type] OR meta-analysis[Publication Type])` | GHB-GBL_pubmed_P5.csv | |
| P6 | `(GHB OR "gamma-hydroxybutyrate") AND (pharmacokinetic* OR "dose-response" OR "dose response" OR "non-linear" OR "monocarboxylate transporter") AND (humans[MeSH Terms])` | GHB-GBL_pubmed_P6.csv | |
| P7 | `(GHB OR "gamma-hydroxybutyrate") AND (endogenous[Title] OR "cut-off" OR "cutoff" OR "post-mortem" OR postmortem) AND (blood OR urine OR hair)` | GHB-GBL_pubmed_P7.csv | |
| P8 | `(GHB OR "gamma-hydroxybutyrate" OR "gamma-butyrolactone") AND (death* OR fatal* OR mortality) AND ("case series" OR cohort OR "coronial" OR "medical examiner")` | GHB-GBL_pubmed_P8.csv | |
| P9 | `(chemsex OR "sexualised drug use" OR "sexualized drug use") AND (GHB OR "gamma-hydroxybutyrate" OR mephedrone OR methamphetamine) AND (humans[MeSH Terms])` | GHB-GBL_pubmed_P9.csv | |
| P10 | `("drug-facilitated sexual assault" OR "drug facilitated sexual assault" OR "chemical submission") AND (GHB OR "gamma-hydroxybutyrate")` | GHB-GBL_pubmed_P10.csv | |
| P11 | `(GHB OR "gamma-hydroxybutyrate") AND (alcohol OR ethanol OR benzodiazepine* OR opioid* OR ketamine) AND (interaction OR "co-ingestion" OR combined OR "respiratory depression")` | GHB-GBL_pubmed_P11.csv | |
| P12 | `(GHB OR "gamma-hydroxybutyrate") AND (cognitive OR memory OR neuroimaging OR "grey matter" OR "gray matter" OR neuropsychological) AND (humans[MeSH Terms])` | GHB-GBL_pubmed_P12.csv | |
| P13 | `("gamma-butyrolactone" OR GBL OR "1,4-butanediol" OR "1,4 butanediol") AND (conversion OR precursor OR industrial OR "cleaning product" OR ingestion)` | GHB-GBL_pubmed_P13.csv | |
| P14 | `(GHB OR "gamma-hydroxybutyrate") AND (prevalence OR epidemiolog* OR "nightlife" OR "harm reduction" OR "drug checking" OR surveillance) AND ("2010"[Date - Publication] : "3000"[Date - Publication])` | GHB-GBL_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `gamma-hydroxybutyrate OR oxybate` in Cochrane Reviews; export the result list as CSV → `GHB-GBL_cochrane.csv`. The review specifically wanted is Leone et al. on GHB for the treatment of alcohol withdrawal and prevention of relapse — take the current `.pubN` version.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of every Tier-A review (#1, #2, #3, #4, #5, #9, #10, #14, #24, #25, #26). Forward: Google Scholar "cited by" on the landmarks — #6 (Brenneisen 2004), #8 (Dyer 2001), #12 (de Jong 2011), #13 (Dijkstra 2017), #17 (Degenhardt 2003), #23 (Korb 2014). The EMCDDA GHB risk assessment and the Euro-DEN Plus reports should also be snowballed for emergency-department series. Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included.
