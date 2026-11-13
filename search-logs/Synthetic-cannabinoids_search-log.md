# Synthetic cannabinoids (SCRAs) — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-15)

Section-level queries (`query.bibliographic`, `type:journal-article`, 15 rows, relevance-sorted) plus `works/<DOI>` fetches for recalled landmark DOIs. 33 papers retained into `Synthetic-cannabinoids_DOI-LIST.md`.

**Rate-limit problem (same as Cannabis).** Crossref answered a large share of requests with HTTP 429 (shared egress IP). Procedure: 90 s back-off after every 429, never re-fetching a refused URL, rephrasing refused queries; six DOIs resolved via publisher or Semantic Scholar pages when Crossref was unavailable (marked R in the list). Because the search endpoint returns `updated-by` in the `select` list, search hits are treated as verified (CS) for title/journal/year/retraction-flag; R items still need the Crossref retraction read.

### Section queries run (retained in parentheses)

| # | Query string (query.bibliographic) | Hits | Retained |
|---|---|---|---|
| S1 | synthetic cannabinoids clinical toxicology pharmacology review | 20 | Tait 2016; White 2017; Adamowicz 2019; Adamowicz 2020 |
| S2 | synthetic cannabinoid receptor agonists pharmacology efficacy CB1 full agonist | 15 | Wouters 2019 (others preclinical, screened out) |
| S3 | synthetic cannabinoids acute kidney injury outbreak | 15 | D'Errico 2022 (rest case reports) |
| S4 | synthetic cannabinoids psychosis psychiatric review | 15 | Fattore 2016; Deng 2018; Ricci 2026 |
| S5 | synthetic cannabinoids poison control center exposures United States | 15 | none on-target (query returned other-drug poison-centre papers; AAPCC SC analyses noted as a gap) |
| S6 | synthetic cannabinoids withdrawal dependence review | 15 | Prete 2025; Gatch & Forster 2014; Vandrey 2012 (Cooper, Castaneto re-surfaced) |
| S7 | synthetic cannabinoids prevalence use young adults survey novel psychoactive | 15 | Huestis 2016; Caviness 2015; Patrick 2016 |
| S8 | synthetic cannabinoid acute intoxication clinical features emergency Hermanns-Clausen | 15 | Hermanns-Clausen 2013 (Addiction); Addy 2013 commentary; Schneir 2011; Hermanns-Clausen 2013 (Drug Test Anal) |
| S9 | synthetic cannabinoids cardiovascular seizures myocardial toxicity | 15 | Tofighi 2012 (seizures); cardiovascular hits were all case reports/Cureus, screened out |
| S10 | MDMB-4en-PINACA 4F-MDMB-BINACA synthetic cannabinoid | 15 | Cannaert 2020; Simon 2023; Lie 2020 |
| S11 | synthetic cannabinoids epidemiology pharmacodynamics clinical implications review | 429 (not run) | covered by works/ fetch: Castaneto 2014 |

### `works/<DOI>` verification fetches
Castaneto 2014 (10.1016/j.drugalcdep.2014.08.005) and Trecki 2015 (10.1056/NEJMp1505328) fetched and resolved. Six landmark DOIs resolved via publisher/Semantic Scholar pages during Crossref outages: Cooper 2016, Tai & Fantegrossi 2014, Spaderna 2013, Giorgetti 2020, Fattore & Fratta 2011, Brents 2011 (all publisher pages) and Adams 2017 (Semantic Scholar DOI record).

### Screening rules applied
Kept: systematic reviews of adverse events/deaths, the NEJM outbreak/mortality papers, the confirmed-consumption toxicity series and its commentary, pharmacology/metabolism reviews, drug-discrimination and receptor-activity characterisations of named SCs, population use surveys. Dropped: single case reports in low-impact or predatory venues (Cureus, Journal of Addiction Research, Eurasian J Emerg Med, Case Reports in Emergency Medicine), conference abstracts/supplements (Toxicology Letters abstract items), veterinary and off-topic poison-centre hits, preclinical rodent receptor-pharmacology papers not needed for human claims.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed. For each: **Save → Selection: All results → Format: CSV** into `search-logs/`. Note the hit count and send me the numbers. P5 and P9 cover the Crossref queries that returned weakly.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `("synthetic cannabinoid*"[Title] OR "synthetic cannabinoid receptor agonist*"[Title] OR spice[Title] OR "K2"[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type] OR "systematic review"[Title] OR review[Title])` | SC_pubmed_P1.csv | |
| P2 | `("synthetic cannabinoid*"[Title] OR "synthetic cannabinoid receptor agonist*"[Title]) AND (pharmacolog* OR "receptor" OR agonist OR efficacy OR metabolism OR pharmacokinetic*)` | SC_pubmed_P2.csv | |
| P3 | `("synthetic cannabinoid*"[Title] OR spice[Title] OR "K2"[Title]) AND (toxicity OR intoxication OR poisoning OR "emergency department" OR overdose) AND (humans[MeSH Terms])` | SC_pubmed_P3.csv | |
| P4 | `("synthetic cannabinoid*"[Title] OR spice[Title]) AND (death OR fatal OR mortality OR "post-mortem" OR postmortem) AND (humans[MeSH Terms])` | SC_pubmed_P4.csv | |
| P5 | `("synthetic cannabinoid*"[Title] OR spice[Title] OR "K2"[Title]) AND ("poison control" OR "poison center" OR "poison centre" OR surveillance OR exposures) AND (humans[MeSH Terms])` | SC_pubmed_P5.csv | |
| P6 | `("synthetic cannabinoid*"[Title]) AND (psychosis OR psychotic OR psychiatric OR anxiety OR agitation) AND (humans[MeSH Terms])` | SC_pubmed_P6.csv | |
| P7 | `("synthetic cannabinoid*"[Title]) AND ("acute kidney injury" OR nephrotoxicity OR renal OR rhabdomyolysis) AND (humans[MeSH Terms])` | SC_pubmed_P7.csv | |
| P8 | `("synthetic cannabinoid*"[Title]) AND (withdrawal OR dependence OR "use disorder") AND (humans[MeSH Terms])` | SC_pubmed_P8.csv | |
| P9 | `("synthetic cannabinoid*"[Title] OR spice[Title] OR "K2"[Title]) AND (prison OR incarcerat* OR homeless) AND (humans[MeSH Terms])` | SC_pubmed_P9.csv | |
| P10 | `("synthetic cannabinoid*"[Title]) AND (cardiovascular OR myocardial OR seizure OR stroke OR cardiotoxic*) AND (humans[MeSH Terms])` | SC_pubmed_P10.csv | |
| P11 | `(MDMB-4en-PINACA OR "4F-MDMB-BINACA" OR "5F-MDMB-PINACA" OR "AMB-FUBINACA" OR CUMYL-PEGACLONE OR brodifacoum) AND (cannabinoid OR synthetic)` | SC_pubmed_P11.csv | |
| P12 | `("synthetic cannabinoid*"[Title] OR spice[Title] OR "K2"[Title]) AND (prevalence OR survey OR epidemiolog* OR "novel psychoactive")` | SC_pubmed_P12.csv | |
| P13 | `(hexahydrocannabinol OR HHC OR "semi-synthetic cannabinoid*") AND (humans[MeSH Terms] OR toxicity OR use)` | SC_pubmed_P13.csv | |

## Layer 3 — EUDA / grey literature (to be collected by VS)

EUDA EU Early Warning System technical reports and formal risk assessments for individual SCRAs; EUDA "Synthetic cannabinoids in Europe" review; CDC MMWR and health advisories (2018 brodifacoum-contaminated SC outbreak); HM Inspectorate of Prisons reports. Listed in the Reports table of the DOI list.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of Castaneto 2014, Cooper 2016, Tait 2016, Prete 2025, Giorgetti 2020. Forward: Google Scholar "cited by" on Hermanns-Clausen 2013, Trecki 2015, Adams 2017.

## PRISMA counts

To be completed after Layers 2–4.
