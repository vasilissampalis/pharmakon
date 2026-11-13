# LSD — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; re-worded re-runs of refused or errored URLs are listed as such.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-15)

Endpoint: `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=15&select=DOI,title,container-title,issued,is-referenced-by-count,author&sort=relevance`. Record verification used `https://api.crossref.org/works?filter=doi:A,doi:B,doi:C&select=DOI,title,container-title,issued,updated-by&rows=10` (three DOIs per request is the working limit; see the Psilocybin log).

Environment: Crossref refused about half of all calls with HTTP 429 and errored on several syntactically valid URLs. Each refusal was followed by a 60–185 s pause; refused URLs were never re-fetched. Query strings were kept under ~75 characters because the proxy rejects URLs over ~250 characters.

### Section-level queries

| # | Query string | Result |
|---|---|---|
| L1 | acute dose-response effects of LSD in healthy subjects Holze | URL refused (429); re-run as L1b |
| L1b | acute dose-dependent effects LSD healthy subjects Holze Liechti | 15 hits, 9 retained (Holze 2020 dose-dependent; Holze 2021a safety pharmacology + its Correction; Holze 2019a distinct acute effects; Holze 2019b oral formulation PK; Holze 2021b 5-HT2A empathy; Vizeli 2021 CYP2D6; Mueller 2017 amygdala; Straumann 2023 MDMA+LSD). Also surfaced **Klaiber 2024, acute dose-dependent effects of mescaline (Transl Psychiatry, 10.1038/s41398-024-03116-2)** — carried forward to the Mescaline list |
| L2 | pharmacokinetics pharmacodynamics lysergic acid diethylamide humans Dolder | 15 hits, 6 retained (Dolder 2017; Holze 2020b microdose PK/PD; Holze 2023a urinary recovery; Morse 2025 sublingual microdose; Tanaka 2025 LSD analogues; Preller 2019 microdosing commentary) |
| L3 | microdosing psychedelics placebo controlled trial self-blinding null | URL refused (429); re-run as "microdosing LSD psychedelics randomised placebo controlled self-blinding": client error; re-run as L3c |
| L3c | self-blinding microdose psychedelic trial placebo anecdotal benefits | 15 hits, 2 retained (Szigeti 2021 eLife; Ona 2020 Neurosci Biobehav Rev) |
| L4 | repeated low doses LSD healthy volunteers mood cognition Bershad de Wit | 15 hits, 7 retained (de Wit 2022; Hutten 2020; Bershad 2019; Murray 2021; Murray 2024; Glazer 2022; Molla 2023; plus Glazer 2026) |
| L5 | hallucinogen persisting perception disorder HPPD review flashbacks | URL refused (429); re-run as L5b, itself refused (429), then run successfully after a 185 s pause |
| L5b | hallucinogen persisting perception disorder flashbacks clinical review | 15 hits, 5 retained (Neven 2025 SR; Litjens 2014 review; Young 1997; Morehead 1997; Alcántara 1998). Cureus case reports, Reactions Weekly items and the Neuroscience Applied abstract dropped |
| L6 | psychedelics mental health population study Krebs Johansen Hendricks | 15 hits, 4 retained (Krebs & Johansen 2013; Johansen & Krebs 2015; Sexton 2020; Dourron 2026). Hendricks' own papers did not surface; Hendricks 2015 obtained by `filter=doi:` verification |
| L7 | lysergic acid diethylamide alcoholism meta-analysis randomized trials | client error; re-run as L7b |
| L7b | LSD for alcoholism meta-analysis of randomized controlled trials Krebs | 15 hits, 1 retained (Krebs & Johansen 2012) |
| L8 | 1P-LSD ALD-52 lysergamide novel psychoactive substances pharmacology | 15 hits, 4 retained (Jurowski 2026; Zhang 2023; Liechti 2015; Schifano 2023). No human pharmacology of any 1-acyl lysergamide exists in the indexed literature |
| L9 | LSD-assisted psychotherapy anxiety life-threatening disease Gasser trial | client error; re-run as L9b |
| L9b | LSD assisted psychotherapy anxiety associated with life threatening diseases | 15 hits, 4 retained (Gasser 2014a; Gasser 2014b; Schipper 2024 Cochrane; Grof, Int Pharmacopsychiatry). Ross 2025 (psilocybin phase 2b, Gen Hosp Psychiatry) noted for the Psilocybin list's next pass |
| L10 | LSD brain imaging 5-HT2A ketanserin human Preller Vollenweider | 15 hits, 5 retained (Preller 2018 eLife; Kraehenmann 2017; Pokorny 2019; Olbrich 2021; Burt 2021; Duerler 2020). Six Biol Psychiatry / Eur Neuropsychopharmacol abstracts of the same work dropped |
| L11 | Halpern Pope hallucinogen persisting perception disorder 50 years | first form ("hallucinogen persisting perception disorder what do we know after 50 years") returned a client error; the author-form re-run was refused (429) — recorded as a gap |
| L12 | LSD toxicity overdose emergency department adverse reactions epidemiology | 15 hits, 0 retained (Reactions Weekly overdose notes for unrelated drugs; one 1969 American Biology Teacher item) — recorded as a gap |

### Record verification (`filter=doi:`)

| Batch | DOIs | Result |
|---|---|---|
| V1 | 10.1177/0269881114565653, 10.1016/j.biopsych.2022.08.025, 10.1073/pnas.1518377113 | total-results 3; 3/3 resolved to the intended papers (Hendricks 2015; Holze 2023 anxiety phase II; Carhart-Harris 2016 PNAS). No `updated-by` on any |

### DOI corrections and update checks
- No recalled DOI was written into the list without a `filter=doi:` check; every other DOI was copied verbatim from a Crossref search response.
- `updated-by`/correction records found: Holze 2021 safety pharmacology has a published Correction registered as its own record (10.1007/s00213-021-05988-4). The parent paper is kept and marked.
- Retractions: none.
- Duplicate/abstract records noted and not listed: Dolder 2016 (Eur Neuropsychopharmacol abstract of the dose-response study), Bershad 2019 (Biol Psychiatry abstract S125 of the microdose study), Preller 2015–2019 (four congress abstracts), Murphy 2024 and Arikci 2024 (Neuroscience Applied abstracts), Holze 2022 (Neuroscience Applied abstract comparing LSD and psilocybin).

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count shown next to each string and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(LSD[Title] OR "lysergic acid diethylamide"[Title] OR lysergide[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type])` | lsd_pubmed_P1.csv | |
| P2 | `("lysergic acid diethylamide"[Title] OR LSD[Title]) AND (pharmacokinetic* OR bioavailability OR "plasma concentration" OR CYP2D6 OR metabolism) AND (humans[MeSH Terms])` | lsd_pubmed_P2.csv | |
| P3 | `("lysergic acid diethylamide"[Title] OR LSD[Title]) AND (dose OR "dose-response" OR "dose-dependent") AND ("healthy volunteers"[MeSH Terms] OR "healthy subjects")` | lsd_pubmed_P3.csv | |
| P4 | `(microdos*[Title] OR "low dose"[Title] OR "low doses"[Title]) AND (LSD OR psychedelic* OR psilocybin) AND (randomized controlled trial[Publication Type] OR placebo)` | lsd_pubmed_P4.csv | |
| P5 | `("hallucinogen persisting perception disorder"[Title/Abstract] OR HPPD[Title/Abstract] OR flashback*[Title]) AND (hallucinogen* OR LSD OR psychedelic*)` | lsd_pubmed_P5.csv | |
| P6 | `(LSD OR psychedelic* OR hallucinogen*) AND (psychosis OR schizophrenia OR "psychotic disorder") AND (cohort OR "population study" OR registry OR survey) AND (humans[MeSH Terms])` | lsd_pubmed_P6.csv | |
| P7 | `("lysergic acid diethylamide"[Title] OR LSD[Title]) AND (alcoholism OR "alcohol use disorder" OR alcohol) AND (trial OR "meta-analysis")` | lsd_pubmed_P7.csv | |
| P8 | `("1P-LSD" OR "ALD-52" OR "1cP-LSD" OR "1V-LSD" OR "1B-LSD" OR "AL-LAD" OR lysergamide*)` | lsd_pubmed_P8.csv | |
| P9 | `(LSD[Title] OR "lysergic acid diethylamide"[Title]) AND (toxicity OR overdose OR poisoning OR "emergency department" OR intoxication) AND (humans[MeSH Terms])` | lsd_pubmed_P9.csv | |
| P10 | `(LSD[Title] OR "lysergic acid diethylamide"[Title]) AND (anxiety OR depression OR "end of life" OR "life-threatening") AND (randomized controlled trial[Publication Type])` | lsd_pubmed_P10.csv | |
| P11 | `(LSD OR psychedelic*) AND (blinding OR unblinding OR expectancy OR "placebo response") AND (trial OR trials)` | lsd_pubmed_P11.csv | |
| P12 | `(LSD[Title] OR "lysergic acid diethylamide"[Title]) AND (neuroimaging OR fMRI OR EEG OR MEG OR "functional connectivity") AND (humans[MeSH Terms])` | lsd_pubmed_P12.csv | |
| P13 | `(LSD OR hallucinogen*) AND (prevalence OR trends OR epidemiolog* OR NSDUH OR "Monitoring the Future")` | lsd_pubmed_P13.csv | |
| P14 | `(LSD[Title] OR "lysergic acid diethylamide"[Title]) AND (pregnan* OR driving OR "psychomotor" OR dependence OR tolerance)` | lsd_pubmed_P14.csv | |

## Layer 3 — grey literature (VS)

UNODC World Drug Report 2025; EUDA European Drug Report 2026, Statistical Bulletin and EDND notifications for 1P-LSD / 1cP-LSD / 1V-LSD; SAMHSA NSDUH 2024 detailed tables; Monitoring the Future latest; Global Drug Survey latest; WEDINOS annual report; UK Home Office CSEW drug-misuse tables. Saved to `PDFs/_Epidemiology/` with the names in the DOI list's reports table.
