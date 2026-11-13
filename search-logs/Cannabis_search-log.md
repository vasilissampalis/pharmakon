# Cannabis — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-15)

18 pre-registered section-level queries (`query.bibliographic`, `type:journal-article`, 10–20 rows, relevance-sorted) plus 14 targeted title/author queries to resolve landmark DOIs. Hits screened by title and journal; 116 papers retained into `Cannabis_DOI-LIST.md`.

**Rate-limit problem.** From 12:36 EEST the Crossref API answered a large share of requests with HTTP 429 (Retry-After ≈60 s), apparently a limit on the shared egress IP of the fetch proxy rather than on this session (bursts of 1–10 successes alternated with refusals regardless of request spacing; doi.org and Semantic Scholar were throttled at the same times). Procedure followed: 90 s back-off after every 429, never re-fetching a refused URL, rephrasing refused queries. Six section queries could not be run on Crossref at all (C1 pharmacokinetics, C2 neuroimaging, C6 cognition MA — wording 1, C8 withdrawal, C11 cardiovascular, C13 medical cannabinoids) and were covered by `works/<DOI>` fetches of recalled landmark DOIs instead; their PubMed equivalents are the priority strings below. Ten DOIs at publishers that block automated fetches (JAMA, Wiley, NEJM, LWW, Elsevier) were resolved through the Semantic Scholar DOI record or a publisher page and are marked `R` in the list.

### Section queries (C1–C18)

| # | Query string (query.bibliographic) | Result | Retained |
|---|---|---|---|
| C1 | cannabis tetrahydrocannabinol pharmacokinetics human cannabidiol | 429 (twice, rephrased) — not run | covered by works/ fetches: Huestis 2007; Grotenhermen 2003; Pertwee 2008; Lucas 2018; Spindle 2018 |
| C2 | cannabis users brain structure neuroimaging systematic review | 429 — not run | covered by works/ fetches: Gilman 2014; Weiland 2015; Pagliaccio 2015 |
| C3 | psychotomimetic effects intravenous delta-9-tetrahydrocannabinol healthy individuals psychosis | 429 (twice) — not run | D'Souza 2004 resolved via nature.com |
| C4 | cannabis psychosis systematic review meta-analysis | 15 hits | Large 2011 (retained); Kiburi 2021 and Groening 2024 screened out as duplicative of Marconi/Petrilli (umbrella review noted for snowballing) |
| C5 | Hines high-potency cannabis adolescence mental health substance use | 8 hits | Hines 2020 |
| C6 | acute chronic effects cannabinoids human cognition systematic review | 20 hits | Broyd 2016; Ranganathan & D'Souza 2006; Cohen & Weinstein 2018 |
| C6b | Meier adolescent cannabis use neuropsychological decline co-twin control | 6 hits | Meier 2018; Schaefer 2021; Schaefer 2022 |
| C7 | (CUD prevalence/transition) — covered by works/ fetches | — | Leung 2020; Hasin 2015 |
| C8 | (withdrawal) — covered by works/ fetches | — | Budney 2004; Bahji 2020; Allsop 2014 |
| C9 | cannabinoid hyperemesis syndrome systematic review | 12 hits | DeVuono 2020; Angulo 2024 (Sorensen 2017 by works/ fetch) |
| C10 | cannabis driving crash risk meta-analysis culpability tetrahydrocannabinol drivers | 20 hits | Rogeberg 2019; Li 2017; Rogeberg & Elvik 2017 reply |
| C11 | (cardiovascular) — covered by works/ fetches | — | Mittleman 2001; Page 2020; Ravi 2018; Jeffers 2024; Jouanjus 2014 (R) |
| C12 | (pregnancy) — covered by works/ fetches | — | Gunn 2016; Marchand 2022; Corsi 2019; Paul 2021; Conner 2016 (R) |
| C13 | (medical cannabinoids) — covered by works/ fetches | — | Whiting 2015; Stockings 2018; Black 2019; McDonagh 2022; Wang 2021; Devinsky 2017 (R) |
| C14 | cannabis smoking lung cancer respiratory function systematic review | 15 hits | Tetrault 2007; Ribeiro 2016 |
| C14b | marijuana use lung cancer risk case-control pooled analysis conscripts | 15 hits (noisy) | Callaghan 2013 |
| C14c | marijuana lung upper aerodigestive tract cancers case-control | 10 hits | Hashibe 2006 |
| C15 | recreational cannabis legalization adolescent use disorder difference-in-differences | 15 hits | O'Grady 2022; Coley 2024 |
| C15b | state recreational marijuana laws adolescent use disorder Cerda JAMA Psychiatry | 10 hits | Cerdá 2017; Cerdá 2020; Hasin 2017; Anderson 2024 (three 2020 letters to Anderson 2019 screened out as letters) |
| C16 | (edibles/ED visits) — covered by works/ fetches | — | Monte 2019; Monte 2015; Wang 2016 |
| C17 | Gobbi association cannabis use adolescence risk depression anxiety suicidality young adulthood | 12 hits | Gobbi 2019; Hengartner 2020 |
| C17b | cannabis schizophrenia causal relationship epidemiological evidence critical review | 20 hits | Calabria 2010; Hall & Degenhardt 2010; Sánchez-Iglesias 2023 |
| C18 | young adult sequelae of adolescent cannabis use integrative analysis | 10 hits | Silins 2014 (Nordentoft 2014 comment screened out) |

### Targeted `works/<DOI>` verification fetches
78 recalled landmark DOIs fetched and resolved to the intended paper (listed with code CR in the DOI list). One recalled DOI resolved to a different paper and was dropped (10.1111/add.14082 → Weinberger et al. 2018; Meier 2018 re-found as 10.1111/add.13946). One recalled DOI was corrected before fetching (Broyd 2016 → 10.1016/j.biopsych.2015.12.002). Two retained papers carry published errata (Pasman 2018; Black 2019); none is retracted.

### Screening rules applied
Kept: systematic reviews/meta-analyses, landmark primaries with their critiques and replies, major cohorts, RCTs, authoritative reviews in serious journals. Dropped: conference abstracts and supplements (e.g., Thorax P147; JAACAP 1.37), letters (JAMA Pediatrics 2020 ×3), newsletters (Brown University updates; Clinical/Pharmaceutical Journal news), predatory-looking venues (Journal of Student Research; Addiction Research and Adolescent Behaviour; Archives of Depression and Anxiety; MedScien; Cureus items), off-topic hits.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count shown by PubMed next to each string and send me the numbers. P1, P2, P4 and P8 cover the Crossref queries that could not be run.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(cannabis[Title] OR marijuana[Title] OR cannabinoid*[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type] OR "systematic review"[Title] OR "meta-analysis"[Title]) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | Cannabis_pubmed_P1.csv | |
| P2 | `(tetrahydrocannabinol[Title] OR cannabis[Title] OR cannabidiol[Title]) AND (pharmacokinetic* OR bioavailability OR "half-life" OR "plasma concentration" OR metabolism) AND (humans[MeSH Terms])` | Cannabis_pubmed_P2.csv | |
| P3 | `(cannabis[Title] OR marijuana[Title]) AND (psychosis OR psychotic OR schizophrenia) AND (cohort OR "case-control" OR "mendelian randomization" OR "meta-analysis") AND (humans[MeSH Terms]) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | Cannabis_pubmed_P3.csv | |
| P4 | `(cannabis[Title] OR marijuana[Title]) AND (MRI OR "magnetic resonance" OR neuroimaging OR "gray matter" OR hippocamp*) AND (humans[MeSH Terms]) AND ("2014"[Date - Publication] : "3000"[Date - Publication])` | Cannabis_pubmed_P4.csv | |
| P5 | `(cannabis[Title] OR marijuana[Title]) AND (cognit* OR IQ OR neuropsycholog* OR memory) AND (longitudinal OR cohort OR twin OR "meta-analysis") AND (humans[MeSH Terms]) AND ("2012"[Date - Publication] : "3000"[Date - Publication])` | Cannabis_pubmed_P5.csv | |
| P6 | `("cannabis use disorder"[Title] OR "cannabis dependence"[Title] OR "marijuana use disorder"[Title]) AND (prevalence OR transition OR "natural history" OR remission OR treatment) AND (humans[MeSH Terms]) AND ("2010"[Date - Publication] : "3000"[Date - Publication])` | Cannabis_pubmed_P6.csv | |
| P7 | `(cannabis[Title] OR marijuana[Title] OR cannabinoid[Title]) AND (withdrawal[Title] OR hyperemesis[Title]) AND (humans[MeSH Terms])` | Cannabis_pubmed_P7.csv | |
| P8 | `(cannabis[Title] OR marijuana[Title]) AND (cardiovascular OR "myocardial infarction" OR stroke OR arrhythmia) AND (humans[MeSH Terms]) AND ("2012"[Date - Publication] : "3000"[Date - Publication])` | Cannabis_pubmed_P8.csv | |
| P9 | `(cannabis[Title] OR marijuana[Title]) AND (driving OR "motor vehicle" OR crash OR collision) AND (humans[MeSH Terms]) AND ("2012"[Date - Publication] : "3000"[Date - Publication])` | Cannabis_pubmed_P9.csv | |
| P10 | `(cannabis[Title] OR marijuana[Title]) AND (pregnan* OR prenatal OR neonatal OR "birth weight") AND (humans[MeSH Terms]) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | Cannabis_pubmed_P10.csv | |
| P11 | `(cannabis[Title] OR marijuana[Title]) AND (legalization OR legalisation OR "recreational marijuana laws" OR "medical marijuana laws") AND (humans[MeSH Terms]) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | Cannabis_pubmed_P11.csv | |
| P12 | `(cannabis[Title] OR marijuana[Title] OR edible*[Title]) AND ("emergency department" OR poisoning OR "poison control" OR "unintentional exposure" OR toxicity) AND (humans[MeSH Terms]) AND ("2014"[Date - Publication] : "3000"[Date - Publication])` | Cannabis_pubmed_P12.csv | |
| P13 | `(cannabis[Title] OR marijuana[Title]) AND (lung OR pulmonary OR respiratory OR "lung cancer" OR COPD OR vaping) AND (humans[MeSH Terms]) AND ("2010"[Date - Publication] : "3000"[Date - Publication])` | Cannabis_pubmed_P13.csv | |
| P14 | `(cannabis[Title] OR marijuana[Title]) AND ("harm reduction" OR "lower-risk" OR guideline* OR vaporiz* OR potency OR "drug checking") AND (humans[MeSH Terms]) AND ("2015"[Date - Publication] : "3000"[Date - Publication])` | Cannabis_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `cannabis OR cannabinoid` in Cochrane Reviews; export the result list as CSV → `Cannabis_cochrane.csv` (expected: cannabinoids for chronic neuropathic pain; CINV; cannabis use disorder psychosocial and pharmacological treatment; epilepsy; MS spasticity).

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of every Tier-A review. Forward: Google Scholar "cited by" on items 9, 10, 19, 20, 22, 29, 30, 31 (landmarks). Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included.
