# Synthetic cathinones — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening (the plan in the co-editors' scratch file `cathinones_queries.md`, 16 section-level and ~50 targeted strings); not altered during screening. Only seven of them could be run (see "Operational notes").

## Layer 1 — Crossref bibliographic search (run by AI, 2026-10-15/16)

Endpoint: `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=<n>&select=DOI,title,container-title,issued,author[,updated-by]`, relevance order. From SC3 onward `updated-by` was added to the select, so every hit of those queries was checked for retractions and corrections in the same call. Hits screened by title and journal; 80 journal articles retained from these queries, plus 3 cathinone controlled-administration papers (methylone, mephedrone metabolomics) returned by the MDMA queries in this session, giving 83 in `Synthetic-cathinones_DOI-LIST.md`.

| # | Query string (`query.bibliographic=`) | Rows | `updated-by` | Retained |
|---|---|---|---|---|
| SC1 | mephedrone 4-MMC pharmacology toxicity human users review | 35 | no | 13 |
| SC2 | MDPV alpha-PVP synthetic cathinones bath salts pharmacology toxicity | 35 | no | 14 |
| SC3 | 3-MMC 3-methylmethcathinone intoxications deaths use | 30 | yes | 16 |
| SC4 | eutylone N-ethylpentylone synthetic cathinone deaths postmortem | 30 | yes | 10 |
| SC5 | mephedrone chemsex slamming injecting men who have sex with men | 30 | yes | 11 |
| SC6 | powerful cocaine-like actions of MDPV bath salts Baumann | 25 | yes | 13 |
| SC7 | mephedrone use subjective effects health risks survey Winstock | 30 | yes | 8 |

"Retained" counts include papers retained by more than one query (e.g. Cameron et al. 2013b appears in SC1, SC2 and SC6), so they sum to more than 80. Two further queries were refused by the proxy with HTTP 429 and were not re-sent (per protocol, a refused URL is never re-fetched): "Baumann MDPV cocaine-like mephedrone methylone substrates monoamine transporters" (replaced by SC6) and "mephedrone use survey users effects legal high emergence UK" (replaced by SC7).

**Screening decisions.** Excluded at title/venue stage: conference abstracts (*Drug and Alcohol Dependence* and *European Neuropsychopharmacology* supplements, *FASEB Journal*, Japanese Pharmacological Society proceedings, *Critical Care Medicine* and *Journal of the Endocrine Society* meeting abstracts), including two *Emerging Trends in Drugs, Addictions, and Health* records that duplicate the 3-MMC human studies as abstracts; single case reports, unless the report also reviews the literature; *The Microscope* microcrystal-test notes and analytical-chemistry method papers without clinical data; a JAMA Medical News item and its name-correction notice; *Lancet* correspondence and a *BMJ* editorial; venues excluded in the other stimulant lists; off-topic hits returned by generic terms ("toxicity", "review").

**Corrections, retractions and flags.** One correction found through `updated-by`: Cameron et al. 2013, *Psychopharmacology* (`10.1007/s00213-013-2967-2`), corrected by `10.1007/s00213-013-3056-2`; both are listed. No retraction was found among any hit of SC3–SC7. No DOI was written from memory, so none needed correcting.

**Thin literature.** Controlled human administration studies exist only for mephedrone, methylone and 3-MMC (the 3-MMC studies date from 2024–2025). For MDPV, α-PVP, N-ethylpentylone, eutylone and dipentylone the human evidence consists of case series, poison-centre data and post-mortem toxicology; this is stated in the list's "Known gaps" and must be stated in the monograph.

**Operational notes.** As for the other stimulant logs: `api.crossref.org` reachable only through WebFetch; HTTP 429 on roughly one call in three at 200–235 s spacing, with the limit shared with other co-editor agents (see the shared `ratelog.txt`); URLs over ~250 characters and query terms containing commas are refused, so chemical names such as "3,4-methylenedioxypyrovalerone" were searched by their abbreviations.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count PubMed shows next to each string and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `("synthetic cathinone*"[Title] OR "bath salts"[Title] OR mephedrone[Title] OR MDPV[Title] OR methylenedioxypyrovalerone[Title] OR "alpha-PVP"[Title] OR "α-PVP"[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type] OR review[Publication Type])` | cathinones_pubmed_P1.csv | |
| P2 | `(mephedrone[Title] OR methylone[Title] OR "3-MMC"[Title] OR "3-methylmethcathinone"[Title]) AND (humans[MeSH Terms]) AND (pharmacokinetic* OR "controlled administration" OR "healthy volunteers" OR intranasal)` | cathinones_pubmed_P2.csv | |
| P3 | `(Baumann MH[Author] OR Simmler LD[Author] OR Eshleman AJ[Author]) AND (cathinone* OR mephedrone OR MDPV OR methylone)` | cathinones_pubmed_P3.csv | |
| P4 | `("synthetic cathinone*" OR mephedrone OR MDPV OR "alpha-PVP" OR "N-ethylpentylone" OR eutylone OR "3-MMC") AND (death* OR fatal* OR "post-mortem" OR postmortem)` | cathinones_pubmed_P4.csv | |
| P5 | `("alpha-PVP"[Title] OR "α-PVP"[Title] OR flakka[Title] OR "alpha-pyrrolidinopentiophenone"[Title] OR pyrovalerone[Title])` | cathinones_pubmed_P5.csv | |
| P6 | `(eutylone[Title] OR "N-ethylpentylone"[Title] OR ephylone[Title] OR dipentylone[Title] OR "N,N-dimethylpentylone"[Title])` | cathinones_pubmed_P6.csv | |
| P7 | `("3-MMC"[Title] OR "3-methylmethcathinone"[Title] OR "3-CMC"[Title] OR "3-chloromethcathinone"[Title] OR "4-CMC"[Title])` | cathinones_pubmed_P7.csv | |
| P8 | `(chemsex OR "sexualised drug use" OR "sexualized drug use" OR slamming) AND (mephedrone OR cathinone* OR "3-MMC")` | cathinones_pubmed_P8.csv | |
| P9 | `("synthetic cathinone*" OR mephedrone OR MDPV) AND (inject*) AND (HIV OR "hepatitis C" OR outbreak OR abscess)` | cathinones_pubmed_P9.csv | |
| P10 | `("synthetic cathinone*" OR mephedrone OR MDPV OR "bath salts") AND (psychosis OR psychotic OR delirium OR agitation OR "excited delirium")` | cathinones_pubmed_P10.csv | |
| P11 | `("synthetic cathinone*" OR mephedrone OR MDPV OR "bath salts") AND (emergency department OR "poison center" OR "poison centre" OR "STRIDA" OR intoxication*) AND (humans[MeSH Terms])` | cathinones_pubmed_P11.csv | |
| P12 | `(mephedrone[Title] OR "synthetic cathinone*"[Title]) AND (dependence OR withdrawal OR craving OR "use disorder")` | cathinones_pubmed_P12.csv | |
| P13 | `(mephedrone[Title] OR "synthetic cathinone*"[Title]) AND (neurotoxic* OR "dopamine nerve endings" OR serotonergic) ` | cathinones_pubmed_P13.csv | |
| P14 | `("synthetic cathinone*" OR mephedrone OR "new psychoactive substances") AND ("drug checking" OR adulterat* OR "sold as" OR "mis-sold") AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | cathinones_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `cathinone OR mephedrone` in Cochrane Reviews; a nil result is expected and should be recorded as such.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of items 1, 2, 17, 18, 19, 24 and of each EMCDDA risk-assessment report (R1–R5), which are the most complete inventories of the human case literature for each substance. Forward: Google Scholar "cited by" on items 4, 11 and 12. Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included.
