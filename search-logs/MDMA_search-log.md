# MDMA — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening.

## Layer 1 — Crossref bibliographic search (run by AI, 2026-10-15/16)

Endpoint: `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=<n>&select=DOI,title,container-title,issued,author`, relevance order; plus one `works/<DOI>` call to read an `updated-by` field. Hits screened by title and journal; 94 records retained into `MDMA_DOI-LIST.md` (90 as evidence, 4 in the retracted/retraction-notice table).

| # | Query string (`query.bibliographic=`) | Rows | Retained |
|---|---|---|---|
| M1 | Ricaurte severe dopaminergic neurotoxicity primates MDMA retraction | 25 | 6 |
| M2 | `works/10.1126/science.1074501` (single-record call, to read `updated-by`) | — | 1 (the retraction notice DOI) |
| M3 | MDMA-assisted therapy PTSD phase 3 randomized placebo-controlled | 35 | 12 |
| M4 | MDMA-assisted therapy for moderate to severe PTSD randomized trial | 25 | 3 |
| M5 | MDMA PTSD phase 3 trial (+ `query.container-title=Nature Medicine`) | 20 | 6 |
| M6 | MDMA ecstasy serotonergic neurotoxicity human users critical review | 35 | 11 |
| M7 | residual neurocognitive features long term ecstasy users minimal exposure | 25 | 8 |
| M8 | MDMA ecstasy hyperthermia hyponatraemia serotonin syndrome deaths | 35 | 6 |
| M9 | MDMA pharmacokinetics nonlinear dose controlled administration humans | 35 | 7 |
| M10 | non-linear pharmacokinetics MDMA humans safety acute administration | 30 | 4 |
| M11 | ecstasy tablets MDMA content dose trends drug checking | 30 | 9 |

A twelfth and thirteenth query (on blinding/expectancy methodology in psychedelic trials, and on the retraction notes of the Lykos/MAPS papers) were written but could not be run: the fetch proxy refused them repeatedly with HTTP 429. They are carried into the PubMed layer as strings P5 and P12 and are listed under "Known gaps".

**Screening decisions.** Excluded at title/venue stage: trade press and news digests (*Brown University Psychopharmacology Update*, *Psychiatric News*, *Pharmaceutical Journal*, *AJN* news briefs, *Nature Reviews Drug Discovery* news); conference abstracts of the phase 3 trials (*Biological Psychiatry* and *European Psychiatry* supplements) in favour of the full papers; ClinicalTrials.gov registry stubs republished as "Case Medical Research"; one malformed duplicate DOI carrying a trailing full stop; predatory or non-indexed venues; animal-only pharmacology except where it is the subject of the contested claim. Two news articles were deliberately **kept** (Mahase 2024, *BMJ*; Reardon 2024, *Nature*) because the monograph needs a citable record of the 2024 FDA decision and of the retractions; they are marked as news and may not support empirical claims (METHODS §3.2).

**Corrections, retractions and flags.**
- **Retraction 1:** Ricaurte et al. 2002, *Science* (`10.1126/science.1074501`). The `works/<DOI>` call returns `updated-by`: type *retraction*, DOI `10.1126/science.301.5639.1479b`, dated 2003-09-12, source Retraction Watch; Crossref's stored title is prefixed "RETRACTED:". Excluded from the evidence tiers; listed with its retraction notice for documentation.
- **Retraction 2:** Mithoefer et al. 2019, *Psychopharmacology* (`10.1007/s00213-019-05249-5`), Crossref title prefixed "RETRACTED ARTICLE:", retraction note `10.1007/s00213-024-06666-x` (2024). One of the three MAPS/Lykos papers retracted around the FDA rejection; the other two have not yet been identified and are logged as a gap (PubMed string P12).
- **Correction 1:** Benningfield & Cowan 2012, *Neuropsychopharmacology* — erratum `10.1038/npp.2012.257`.
- **Correction 2:** Mitchell et al. 2023, *Nature Medicine* (MAPP2) — author correction `10.1038/s41591-024-03331-w`.
- **Correction 3:** Tanner-Smith 2006, *Drug and Alcohol Dependence* — corrigendum `10.1016/j.drugalcdep.2007.09.003`.
No DOI had to be corrected, because none was written from memory: every DOI in the list was copied from a Crossref response in this session or carried over from `methamphetamine_DOI-LIST.md`.

**Operational notes.** `api.crossref.org` is reachable only through WebFetch (direct HTTPS from the container is blocked by the agent proxy at the CONNECT stage). The fetch proxy returned HTTP 429 for a large share of requests, at spacings from 3 s up to 450 s, and the usable rate fell to roughly one query every four to ten minutes over the session. Query length is also capped: URLs longer than about 220 characters are refused with "url exceeds the maximum fetchable length", so each query had to be kept to roughly seven terms. Sorting by `is-referenced-by-count` was tried once and abandoned: Crossref drops relevance weighting under that sort and returns the most-cited papers matching any term.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count PubMed shows next to each string and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(MDMA[Title] OR ecstasy[Title] OR "3,4-methylenedioxymethamphetamine"[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type])` | mdma_pubmed_P1.csv | |
| P2 | `(MDMA[Title] OR ecstasy[Title]) AND (cognit* OR memory OR neuropsycholog*) AND (humans[MeSH Terms])` | mdma_pubmed_P2.csv | |
| P3 | `(MDMA[Title] OR ecstasy[Title]) AND (serotonin OR SERT OR "serotonin transporter" OR neurotoxic*) AND (humans[MeSH Terms])` | mdma_pubmed_P3.csv | |
| P4 | `(Reneman L[Author] OR Krebs TS[Author] OR Cowan RL[Author] OR Parrott AC[Author] OR Halpern JH[Author]) AND (MDMA OR ecstasy)` | mdma_pubmed_P4.csv | |
| P5 | `(psychedelic* OR MDMA OR psilocybin) AND (blinding OR "functional unblinding" OR expectancy OR "expectancy effects" OR "adverse event reporting") AND (clinical trial[Publication Type] OR review[Publication Type])` | mdma_pubmed_P5.csv | |
| P6 | `(MDMA[Title] OR ecstasy[Title]) AND (hyponatrem* OR hyponatraem* OR SIADH OR hyperthermia OR rhabdomyolysis OR "liver failure")` | mdma_pubmed_P6.csv | |
| P7 | `(MDMA[Title] OR ecstasy[Title]) AND (death OR fatal* OR mortality OR "post-mortem" OR toxicology)` | mdma_pubmed_P7.csv | |
| P8 | `(MDMA[Title]) AND (pharmacokinetic* OR CYP2D6 OR metabolism OR enantiomer*) AND (humans[MeSH Terms])` | mdma_pubmed_P8.csv | |
| P9 | `(MDMA[Title] OR ecstasy[Title]) AND (interaction* OR SSRI OR MAOI OR moclobemide OR ritonavir OR "serotonin syndrome")` | mdma_pubmed_P9.csv | |
| P10 | `(MDMA[Title] OR ecstasy[Title]) AND (tablet* OR pill* OR purity OR "drug checking" OR adulterant* OR content)` | mdma_pubmed_P10.csv | |
| P11 | `(MDMA[Title]) AND (PTSD OR "posttraumatic stress") AND (randomized controlled trial[Publication Type] OR clinical trial[Publication Type])` | mdma_pubmed_P11.csv | |
| P12 | `(MDMA OR midomafetamine) AND (retracted publication[Publication Type] OR "retraction of publication"[Publication Type] OR retraction[Title])` | mdma_pubmed_P12.csv | |
| P13 | `(MDMA[Title] OR ecstasy[Title]) AND (prevalence OR epidemiolog* OR trends OR "nightlife" OR festival) AND ("2018"[Date - Publication] : "3000"[Date - Publication])` | mdma_pubmed_P13.csv | |
| P14 | `(MDMA[Title] OR ecstasy[Title]) AND (dependence OR "use disorder" OR withdrawal OR craving) AND (humans[MeSH Terms])` | mdma_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `MDMA OR ecstasy` in Cochrane Reviews; export the result list as CSV → `mdma_cochrane.csv`.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of every Tier-A review, and of the two retracted papers (to reconstruct what the retracted claims rested on). Forward: Google Scholar "cited by" on items 1, 5, 8, 14, 15, 27 and on the retracted Ricaurte 2002 paper — the forward citations of a retracted paper are themselves a finding for the monograph's contested-questions section. Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included.
