# Cocaine — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening.

## Layer 1 — Crossref bibliographic search (run by AI, 2026-10-15)

Endpoint: `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=<n>&select=DOI,title,container-title,issued,is-referenced-by-count,author`, relevance order. Hits screened by title and journal; 102 journal articles retained into `Cocaine_DOI-LIST.md`.

| # | Query string (`query.bibliographic=`) | Rows | Retained |
|---|---|---|---|
| C1 | cocaine pharmacokinetics route of administration humans | 15 | 2 |
| C2 | crack cocaine versus intranasal cocaine dependence transition epidemiology | 40 | 9 |
| C3 | cocaine chest pain myocardial infarction beta blocker | 40 | 6 |
| C4 | cocaine coronary vasoconstriction propranolol labetalol | 40 | 6 |
| C5 | potentiation cocaine coronary vasoconstriction beta adrenergic blockade | 30 | 1 |
| C6 | McCord management cocaine associated chest pain myocardial infarction | 20 | 1 |
| C7 | levamisole contaminated cocaine agranulocytosis skin vasculitis | 30 | 3 |
| C8 | cocaethylene cocaine ethanol concurrent use humans toxicity | 30 | 7 |
| C9 | cocaine users neuropsychological cognitive meta-analysis critical review | 35 | 6 |
| C10 | long-term effects cocaine use cognitive functioning quantitative review | 30 | 1 |
| C11 | neurocognitive deficits cocaine users quantitative review | 25 | 4 |
| C12 | characterizing the cognitive effects of cocaine review | 25 | 2 |
| C13 | cocaine related stroke haemorrhage cerebrovascular risk | 30 | 2 |
| C14 | cocaine ischemic stroke systematic review young adults | 30 | 2 |
| C15 | cocaine dependence mortality cohort causes of death follow-up | 30 | 3 |
| C16 | mortality among cocaine users systematic review of cohort studies | 25 | 4 |
| C17 | treatment of cocaine dependence systematic review meta-analysis trials | 35 | 10 |
| C18 | contingency management cocaine dependence incentives randomized trial | 30 | 9 |
| C19 | psychosocial interventions cocaine amphetamine addiction network meta-analysis | 25 | 2 |

Addendum 2026-10-16: six further cocaine/methylphenidate PET papers (list items 103–108) were retained from the methylphenidate query `methylphenidate dopamine transporter occupancy human brain PET cocaine Volkow` (see `Methylphenidate_search-log.md`, MPH3), with `updated-by` read for each (none corrected or retracted).

Nineteen queries were run because the Crossref endpoint was heavily rate-limited through this session (see "Operational notes"); several broad topical queries returned mostly off-topic hits and had to be replaced by narrower title-level queries.

**Screening decisions.** Excluded at title/venue stage: `Reactions Weekly` and `InPharma` drug-safety news items; conference abstracts (JACC, Stroke, Chest, Critical Care Medicine supplements); single case reports of levamisole vasculitis; journals flagged as predatory (`Journal of Alcoholism & Drug Dependence`, `Open Access Journal of Addiction and Psychology`, `Global Journal of Addiction & Rehabilitation Medicine`); animal-only pharmacology except where no human study exists (none retained); and the *Survey of Anesthesiology* reprint of Lange et al. 1990 in favour of the *Annals of Internal Medicine* original.

**Corrections and flags.** One corrigendum was found and both parts are listed: Sabe et al. 2021, cocaine-induced psychosis prevalence (`10.1016/j.pnpbp.2021.110263`), corrected by `10.1016/j.pnpbp.2021.110434`. No retraction was found for any retained paper. No DOI had to be corrected, because no DOI was written from memory: every DOI in the list was copied from a Crossref response in this session, or carried over from `methamphetamine_DOI-LIST.md` where it was verified on 2026-10-14.

**Operational notes.** `api.crossref.org` was reachable only through WebFetch (direct HTTPS from the container is blocked by the agent proxy), and the fetch proxy returned HTTP 429 for roughly one request in three even at 100–300 s spacing. Effective throughput was about one successful query every three to five minutes, which is why the Crossref layer was capped at nineteen queries and why the neuroimaging, pregnancy, drug-checking and harm-reduction sections are left to the PubMed layer below.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count PubMed shows next to each string and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(cocaine[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type] OR "systematic review"[Title] OR "meta-analysis"[Title])` | cocaine_pubmed_P1.csv | |
| P2 | `(cocaine[Title]) AND (cognit* OR neuropsycholog* OR memory OR "executive function") AND (humans[MeSH Terms]) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | cocaine_pubmed_P2.csv | |
| P3 | `(cocaine[Title]) AND (PET OR "positron emission" OR MRI OR neuroimaging OR "dopamine transporter" OR "D2 receptor") AND (humans[MeSH Terms])` | cocaine_pubmed_P3.csv | |
| P4 | `(cocaine[Title]) AND (Volkow NC[Author] OR Breiter HC[Author] OR Ersche KD[Author]) AND (humans[MeSH Terms])` | cocaine_pubmed_P4.csv | |
| P5 | `(cocaine[Title]) AND (cardiomyopathy OR "aortic dissection" OR arrhythmia OR "chest pain" OR "myocardial infarction" OR stroke) AND (humans[MeSH Terms]) AND ("2010"[Date - Publication] : "3000"[Date - Publication])` | cocaine_pubmed_P5.csv | |
| P6 | `(cocaine[Title]) AND (toxicity OR overdose OR "emergency department" OR hyperthermia OR "body packing" OR "body stuffing") AND (humans[MeSH Terms]) AND ("2010"[Date - Publication] : "3000"[Date - Publication])` | cocaine_pubmed_P6.csv | |
| P7 | `(cocaine[Title]) AND (levamisole OR adulterant* OR "drug checking" OR purity OR phenacetin)` | cocaine_pubmed_P7.csv | |
| P8 | `(cocaine[Title]) AND (prenatal OR pregnan* OR "in utero" OR neonatal OR "child development") AND (humans[MeSH Terms])` | cocaine_pubmed_P8.csv | |
| P9 | `(cocaine[Title] OR "crack cocaine"[Title]) AND ("harm reduction" OR "safer smoking" OR pipe OR "supervised consumption" OR "drug consumption room" OR naloxone)` | cocaine_pubmed_P9.csv | |
| P10 | `(cocaine[Title]) AND (randomized controlled trial[Publication Type]) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | cocaine_pubmed_P10.csv | |
| P11 | `(cocaine[Title]) AND ("contingency management" OR "psychosocial intervention" OR "cognitive behavio*")` | cocaine_pubmed_P11.csv | |
| P12 | `(cocaine[Title]) AND (mortality OR "cause of death" OR "drug-induced death") AND (cohort OR registry OR "record linkage")` | cocaine_pubmed_P12.csv | |
| P13 | `(cocaine[Title]) AND (prevalence OR epidemiolog* OR trends OR wastewater) AND ("2019"[Date - Publication] : "3000"[Date - Publication])` | cocaine_pubmed_P13.csv | |
| P14 | `(cocaine[Title]) AND (withdrawal OR craving OR "use disorder") AND (humans[MeSH Terms]) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | cocaine_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `cocaine` in Cochrane Reviews; export the result list as CSV → `cocaine_cochrane.csv`. The reviews expected here (psychostimulants, antidepressants, antipsychotics, dopamine agonists, psychosocial interventions for cocaine dependence) are not in the Crossref layer and should be added from this export.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of every Tier-A review. Forward: Google Scholar "cited by" on items 1, 2, 8, 10, 21, 26, 28, 29 (landmarks and the beta-blocker controversy). Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included.
