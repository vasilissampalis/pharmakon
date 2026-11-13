# _Language-and-stigma — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening. Searches executed 2026-10-16. Cross-cutting topic treated as a substance for the purposes of the evidence-map brief.

This log matters more than most, because the topic it serves is the evidence base for the project's own editorial rule (METHODS §9). A rule the site applies to every page should not rest on an unaudited search.

## Layer 1 — Crossref bibliographic search and DOI verification (run by AI co-editor)

Searches run against `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=<n>&select=DOI,title,container-title,issued,author`. Verifications run against `https://api.crossref.org/works?filter=doi:<a>,doi:<b>,doi:<c>&select=DOI,title,container-title,issued,author&rows=5`, reading `total-results` to confirm the filter applied.

| # | Query | rows | Status / hits retained |
|---|---|---|---|
| S1 | terminology substance use disorder stigmatizing language clinician attitudes person-first | 40 | **Not run** on first attempt — HTTP 429. Run after a 480 s wait: 40 returned, 21 retained (Robinson 2017; Kalkat 2022; Samberg 2024; Eschliman 2025; Friedman 2025; Schiff 2021; Feingold 2019; Salwan 2019; Dadwani 2026; Weiner 2023; Chhabra 2025; Braun 2026; Kennedy 2026; Butler 2025; Aşık 2024; Chung 2024; Alqaisi 2026; Pasman 2022; Brown 2022; Bailey 2024; Lanzillotta-Rangeley 2021). Dropped: *Pakistan Journal of Medical and Health Sciences* items, a *Dusunen Adam* item, gaming/smartphone-addiction stigma papers, bipolar-adherence and person–environment-fit papers that matched on "attitudes", and two *Mental Health Clinician* reprises. **The Kelly, Ashford, Goddu, Volkow and Botticelli papers were not returned by this query**, which is why the DOI-verification route was used instead. |
| S2 | does it matter how we refer to individuals with substance-related conditions randomized two terms | 40 | **Not run** — HTTP 429, not re-fetched. |
| S2b | how we refer to individuals with substance-related conditions randomized study two commonly used terms | 40 | Run after a 540 s wait, and the **matcher failed completely**: all 40 records were unrelated (veterinary immunology, Russian dialect prosody, petroleum engineering, 19th-century *Notes and Queries*). This is the same failure mode seen in `_Dependence-epidemiology` query E2 with the Anthony 1994 title. **Finding worth recording: Crossref's `query.bibliographic` endpoint does not reliably match long natural-language article titles, and on failure it returns a default list that looks like a normal result set rather than an empty one.** Always check whether the returned container-titles are plausible for the field. |
| V1 | `filter=doi:` — Kelly & Westerhoff 2010; Kelly, Saitz & Wakeman 2015 (recalled); Botticelli & Koh 2016 (recalled) | 5 | Run: `total-results` = **1**. Only Kelly & Westerhoff 2010 (10.1016/j.drugpo.2009.10.010) exists as given, and its title, journal, year and first author match. The two recalled DOIs returned no record and are therefore wrong; both papers were excluded from the list and named under Known gaps. |
| V2 | `filter=doi:` — Ashford 2018; Goddu 2018; Volkow 2021 | 5 | Run: `total-results` = **3**; all three returned with matching titles, journals, years and first authors. Verified. |
| S3 | stigma barrier to treatment seeking substance use disorder systematic review | 40 | **Not run** on first attempt — HTTP 429. Run after a 300 s wait: 40 returned, 17 retained (Crapanzano 2018; Madden 2021; Sibley 2024; Bielenberg 2021; Pavone 2026; Zwick 2020; Benz 2021; Witte 2021; Anvari 2022; Garett 2022; Mitchell 2024; Kitt-Lewis 2025; Hartman 2025; Zewdu 2019; Hilton 2026; Ford 2024; Jones 2026). Dropped: treatment-modality systematic reviews that matched only on "systematic review" + "substance use disorder" (memantine, varenicline, buprenorphine group treatment, digital interventions, chatbots, physical activity, economic evaluations); comorbidity-prevalence reviews (autism, bipolar, borderline personality, PTSD, diabetes); a *Cureus* review; an *International Journal of Science and Research* item; a conference-proceedings item. **van Boekel et al. 2013 was not returned**, which is the main loss from this query. |

**Note on the search endpoint.** The Crossref API was shared with several co-editor sessions behind one egress address. Of 9 requests, 5 produced usable output; 3 were refused with HTTP 429 and 1 (S2b) returned a failed match. Waits of 300–540 s were used between requests. No refused URL was re-fetched.

### DOI verification outcomes

- 42 DOIs entered the list: 38 taken verbatim from Crossref search records (title, journal, year and first author echoed into the DOI list for checking against the PDF, METHODS §4.2) and 4 verified by `works?filter=doi:`.
- **2 recalled DOIs were found to be wrong and the papers were excluded:** `10.1080/08897077.2015.1129669` (recalled for Kelly, Saitz & Wakeman, "addiction-ary") and `10.1001/jama.2016.13057` (recalled for Botticelli & Koh, "Changing the language of addiction"). Neither returned a Crossref record. Both are in Known gaps with their titles.
- Corrections/errata found: none. Retractions: none. The per-DOI `updated-by` check of METHODS §4.3 still has to be run item by item.
- **Cross-reference for METHODS.** `docs/METHODS.md` cites Kelly & Westerhoff (2010) in its own reference list with DOI `10.1016/j.drugpo.2009.10.010` and marks its verification status "pending". That DOI was verified in this session (V1) and is correct.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count PubMed shows and send me the numbers. **P3 and P4 are the priorities**: between them they recover all four named papers this list is missing.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `("person-first language" OR "person first" OR terminology[Title] OR "word choice" OR "language matters" OR "words matter") AND (addiction OR "substance use" OR "drug use" OR alcohol) AND (stigma OR bias OR attitudes)` | _Language_pubmed_P1.csv | |
| P2 | `("stigmatizing language" OR "pejorative language" OR "stigmatising language") AND (medical record* OR "clinical note*" OR chart OR documentation OR coding)` | _Language_pubmed_P2.csv | |
| P3 | `(Kelly JF[Author] AND (terminology OR language OR "addiction-ary" OR stigma)) OR (Botticelli MP[Author]) OR (Ashford RD[Author] AND language) OR (Broyles LM[Author] AND language)` | _Language_pubmed_P3.csv | |
| P4 | `(van Boekel LC[Author]) OR ("stigma among health professionals" AND "substance use disorder*") OR (Barry CL[Author] AND stigma AND (addiction OR "drug addiction"))` | _Language_pubmed_P4.csv | |
| P5 | `(stigma[Title]) AND ("substance use disorder*" OR "drug use" OR "opioid use disorder") AND (systematic review[Publication Type] OR meta-analysis[Publication Type] OR "scoping review")` | _Language_pubmed_P5.csv | |
| P6 | `(stigma OR discrimination) AND ("treatment seeking" OR "help-seeking" OR "treatment gap" OR "unmet need") AND ("substance use disorder*" OR "alcohol use disorder" OR "drug dependence") AND (humans[MeSH Terms])` | _Language_pubmed_P6.csv | |
| P7 | `("public opinion" OR "public attitudes" OR "survey experiment" OR vignette) AND (stigma) AND (addiction OR "drug addiction" OR "substance use disorder") AND (policy OR discrimination OR "social distance")` | _Language_pubmed_P7.csv | |
| P8 | `("self-stigma" OR "internalized stigma" OR "internalised stigma") AND ("people who use drugs" OR "substance use disorder*") AND (intervention OR measure* OR outcome*)` | _Language_pubmed_P8.csv | |
| P9 | `("stigma reduction" OR "anti-stigma") AND (clinician* OR provider* OR "medical student*" OR nurse*) AND (addiction OR "substance use disorder*") AND (trial OR intervention OR curriculum)` | _Language_pubmed_P9.csv | |
| P10 | `("Conceptualizing stigma" OR Link BG[Author] OR Corrigan PW[Author]) AND (stigma) AND (mechanism* OR theory OR "structural stigma")` | _Language_pubmed_P10.csv | |

## Layer 3 — Greek-language and non-Anglophone sources (to be run by VS)

METHODS §3.3 allows Greek sources to be read directly, and this is the one topic where the English-language findings may not transfer: the terms at issue are English words, and Greek clinical and lay vocabulary for substance use has its own history. Search the Greek medical and psychological literature (IATROTEK, the Hellenic Psychological Society journals, ΕΚΤΕΠΝ/OKANA publications) for terminology and stigma studies, and record whether any experimental work exists. If none does, that absence should be stated on the About page where §9 is explained, rather than left implicit.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of items 1, 2, 7, 10 and 11 — these five between them cite essentially the whole term-choice and stigma-intervention literature, and will recover van Boekel 2013, Broyles 2014, Kelly/Dow/Westerhoff 2010 and the Barry public-opinion experiments without further searching. Forward (Google Scholar "cited by"): item 1 (Kelly & Westerhoff 2010) is the seed that matters; screen its citing papers for replications and for any published failure to replicate, which the site must report if one exists. Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included. Layer 1 so far: 120 records returned across 3 executed Crossref searches (one further search, S2b, returned 40 records but matched nothing in the field and is excluded from the count), plus 2 DOI-verification fetches; 42 included.
