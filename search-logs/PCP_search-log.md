# PCP (phencyclidine) — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening (re-worded re-runs of refused URLs are listed as such).

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-15)

Endpoint and screening rules as in `Ketamine_search-log.md`. Crossref returned HTTP 429 for most calls in this window (shared proxy egress); after each 429 no Crossref call was made for 120–240 s and refused URLs were not re-fetched. Roughly one in four attempted searches completed. The section-level strings below were therefore run partly as targeted author queries (which return several landmarks per call); strings not run are marked and are covered by the PubMed layer.

### Section-level queries (pre-registered)

| # | Query string | Result |
|---|---|---|
| P1 | phencyclidine pharmacology NMDA receptor review | run as "phencyclidine pharmacology review NMDA sigma receptor Johnson Jones": 15 hits, 1 retained (Johnson & Jones 1990) |
| P2 | phencyclidine pharmacokinetics disposition humans | run as "phencyclidine disposition intravenous oral doses pharmacokinetics humans": refused (429) — gap (Cook 1982) |
| P3 | phencyclidine model schizophrenia psychosis | run via T2 (Jentsch/Javitt author query): 15 hits, 2 retained; T7 (Zukin): 8 hits, 1 retained; Javitt & Zukin 1991 not surfaced |
| P4 | phencyclidine intoxication clinical findings case series | run via T1 (McCarron author query): 11 hits, 4 retained |
| P5 | phencyclidine deaths fatal intoxication toxicology | run via T4 (Poklis/Fauman/Brecher author query): 12 hits, 6 retained |
| P6 | phencyclidine violence behavior intoxication | covered by T4 (Brecher 1988; Poklis 1990) |
| P7 | phencyclidine emergency department visits epidemiology trends | run as "phencyclidine PCP use trends United States emergency department visits": 15 hits, 0 retained (generic ED papers); Palamar author query refused — gap (reports R1–R3) |
| P8 | phencyclidine dependence abuse liability withdrawal | not run (rate limit) — gap |
| P9 | phencyclidine rhabdomyolysis hyperthermia complications | covered by T1 (Akmal 1981; McCarron 1981b) |
| P10 | phencyclidine pregnancy prenatal exposure neonates | not run (rate limit) — gap (Golden 1987) |
| P11 | 3-methoxyphencyclidine 3-MeO-PCP intoxication deaths | run: 15 hits, 8 retained |
| P12 | phencyclidine analogues new psychoactive substances review | Morris & Wallach 2014 from the ketamine build (T34 there); Roth 2013 / Wallach author query refused — partial |
| P13 | phencyclidine chronic use cognitive psychiatric effects | covered partly by T4 (Fauman 1976, 1980); Cosgrove & Newell 1991 not run — gap |
| P14 | phencyclidine treatment management agitation intoxication | covered by McCarron 1981b and Fauman 1981 |

### Targeted author/title queries

T1 McCarron + "phencyclidine intoxication": 4 retained. T2 Jentsch Javitt + "phencyclidine schizophrenia": 2 retained (Jentsch & Roth 1999; Javitt 2012). T3 Lodge Anis + "phencyclidine ketamine NMDA excitation neurones": target error ×2; exact-title query for Lodge & Mercier 2015 refused. T4 Poklis Fauman Brecher + "phencyclidine violence deaths": 6 retained. T5 Palamar + "phencyclidine PCP": refused. T6 Luby + "schizophrenomimetic Sernyl": 1 retained (Luby 1959). T7 Zukin + "recent advances phencyclidine model schizophrenia": 1 retained (Zukin & Zukin 1979). T8 Roth Wallach + "methoxetamine methoxy analogues phencyclidine NMDA": refused.

### DOI corrections and update checks
- No recalled DOI was written into the list; all DOIs were copied from Crossref responses.
- `updated-by`: none of the 24 retained records carries an update (no errata, no retractions).
- Individual `works/<DOI>` re-fetches: 4 attempted, 3 resolved (Luby 1959; McCarron 1981a; McCarron 1981b), 1 refused (Johnson & Jones 1990).

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed. For each: **Save → Selection: All results → Format: CSV** into `search-logs/` with the name given; note the hit count.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(phencyclidine[Title] OR PCP[Title]) AND (review[Publication Type] OR "systematic review"[Title]) AND (humans[MeSH Terms])` | pcp_pubmed_P1.csv | |
| P2 | `(phencyclidine[Title]) AND (intoxication OR overdose OR poisoning OR "emergency department") AND (humans[MeSH Terms])` | pcp_pubmed_P2.csv | |
| P3 | `(phencyclidine[Title]) AND (death OR deaths OR fatal* OR "medical examiner" OR postmortem) AND (humans[MeSH Terms])` | pcp_pubmed_P3.csv | |
| P4 | `(phencyclidine[Title]) AND (psychosis OR psychotic OR schizophreni*) AND (humans[MeSH Terms])` | pcp_pubmed_P4.csv | |
| P5 | `(phencyclidine[Title]) AND (violence OR violent OR aggress* OR homicide)` | pcp_pubmed_P5.csv | |
| P6 | `(phencyclidine[Title]) AND (pharmacokinetic* OR disposition OR "half-life" OR metabolism) AND (humans[MeSH Terms])` | pcp_pubmed_P6.csv | |
| P7 | `(phencyclidine[Title]) AND (dependence OR withdrawal OR "abuse liability" OR "self-administration") AND (humans[MeSH Terms])` | pcp_pubmed_P7.csv | |
| P8 | `(phencyclidine[Title]) AND (pregnan* OR prenatal OR neonat* OR "in utero")` | pcp_pubmed_P8.csv | |
| P9 | `(phencyclidine[Title] OR PCP[Title]) AND (prevalence OR epidemiolog* OR trends OR "emergency department visits" OR DAWN OR NSDUH) AND ("2005"[Date - Publication] : "3000"[Date - Publication])` | pcp_pubmed_P9.csv | |
| P10 | `("3-MeO-PCP" OR "3-methoxyphencyclidine" OR "4-MeO-PCP" OR "3-HO-PCP" OR "3-MeO-PCE" OR "phencyclidine analog*") AND (intoxication OR death OR fatal* OR case)` | pcp_pubmed_P10.csv | |
| P11 | `(phencyclidine[Title]) AND (rhabdomyolysis OR hyperthermia OR seizure* OR "renal failure") AND (humans[MeSH Terms])` | pcp_pubmed_P11.csv | |
| P12 | `(phencyclidine[Title]) AND (cognit* OR memory OR neuropsycholog*) AND (chronic OR "long-term" OR abstinen*) AND (humans[MeSH Terms])` | pcp_pubmed_P12.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `phencyclidine` in Cochrane Reviews (expected: none specific); export → `pcp_cochrane.csv`.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of items 2, 3, 6 (reviews) and 18 (3-MeO-PCP literature review). Forward: Google Scholar "cited by" on items 1, 4, 5, 8, 9. Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4.
