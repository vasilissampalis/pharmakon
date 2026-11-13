# Alkyl nitrites and inhalants — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-16 before screening; not altered during screening. Where a URL was refused the string was re-worded and re-run; both forms are shown.

This folder covers two literatures. The strings below are grouped accordingly: A-series for alkyl nitrites ("poppers"), S-series for volatile solvents and gases. Searching them together does not work — a query naming both returns the nitrite literature only, because "inhalant" is the solvent field's term and "nitrite" dominates relevance scoring.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-16)

Endpoint and parameter notes as in `Nitrous-oxide_search-log.md`: omit `&sort=relevance` (it makes the request fail from this environment, and omitting it is what allows `select` to be used), use `select=DOI,title,container-title,issued,author` with `rows=25`, and note that direct `curl` to api.crossref.org is refused by the egress proxy.

Rate limiting: Crossref/proxy returned HTTP 429 on 5 of 18 attempts and a non-429 target error on 4 more; waits of 120–300 s were used and no refused URL was re-fetched.

Screening rules (METHODS §3): retained systematic reviews and meta-analyses, the landmark case series with their published critiques, population surveys and poison-centre series, policy analyses in peer-reviewed journals, and mechanism studies in humans. Excluded: *Reactions Weekly*; *Cureus* and comparable single-case venues where a case series on the same point was already retained; trade newsletters; conference abstracts in *CHEST* and *Am J Respir Crit Care Med* supplements; and the very large gas-phase-chemistry and agricultural-nitrite literature that the pharmacology queries return.

### Alkyl nitrites (A-series)

| # | Query string (query.bibliographic) | Rows | Result |
|---|---|---|---|
| A1 | poppers maculopathy isopropyl nitrite retinal case series | 25 | 25 hits, 8 retained (Davies 2012, Rewbury 2017, Fajgenbaum 2013, Hui 2020, Ayala Rivera 2024, Docherty 2018, Rojas 2021, Cappellani 2025, Lam 2024, Kanda 2024, Friedrich 2024) — the densest query of the whole build |
| A2 | amyl nitrite poppers methemoglobinemia sildenafil interaction hypotension | 25 | 25 hits, 4 retained (Laaban 1985, Wong 2013, Wellershoff 2014, Bos 1985, Kofler 2014); the sildenafil half of the string returned only *Reactions Weekly* interaction notes |
| A3 | poppers nitrite use men who have sex with men chemsex sildenafil sexual risk | 25 | 25 hits, 7 retained (Hambrick 2018, Chen 2018, Chen 2025, Pepper 2024, Yu 2025, Wang 2023, Pufall 2018) |
| A4 | alkyl nitrites nitric oxide donor pharmacology vasodilation toxicology review | 25 | 25 hits, 3 retained (Omar 2012, Dishy 2001, Krantz 1939); the rest is nitric-oxide-donor bench pharmacology unrelated to inhaled nitrites — the NO-donor pharmacology of poppers specifically is thinly published |
| A5 | alkyl nitrites poppers review harms legal status regulation psychoactive substances act | 25 | 25 hits, 6 retained (Corkery 2025, Crossin 2025, Schwartz 2026, French 1998, Pain 2017, Hayashi 2023) |
| A6 | poppers inhaled nitrites health effects review immune Kaposi sarcoma epidemiology | 25 | target error; re-run as A6b |
| A6b | nitrite inhalants health consequences review immune function users | 25 | 25 hits, 8 retained (Haverkos 1988, Haverkos 1994, Haverkos 1996, Haverkos 1987, Wu 2005, Zhang 2020, Soderberg 1998, Soderberg 2002, Lange 1989, Brosig 2015) |
| A7 | amyl nitrite inhalant use abuse review pharmacology epidemiology history | 25 | refused (429); covered by A6b |
| A8 | nitrite inhalants use and abuse review pharmacotherapy Romanelli Smith | 25 | refused (429) — Romanelli et al. 2004 remains a gap |

### Volatile solvents and gases (S-series)

| # | Query string (query.bibliographic) | Rows | Result |
|---|---|---|---|
| S1 | toluene leukoencephalopathy solvent abuse neurotoxicity Filley white matter | 25 | refused (429); re-run as S1b |
| S1b | toluene leukoencephalopathy inhalant abuse white matter neurotoxicity | 25 | 25 hits, 11 retained (Filley 1990, Filley 2013, Rosenberg 1988, Ranson 2018, Fornazzari 2003, Marsolek 2010, Beauvais 2002, Crossin 2018, Siqueira 2007, Custer 2020, AAP 1996, Jain 2016, Bruckner 1981a, Bruckner 1981b) |
| S2 | sudden sniffing death volatile substance abuse butane propane fatalities trends | 25 | target error; re-run as S2b |
| S2b | volatile substance abuse deaths United Kingdom butane sudden sniffing death | 25 | target error; re-run as S2c |
| S2c | sudden sniffing death syndrome inhalant cardiac arrhythmia fatal | 25 | 25 hits, 0 retained — without the words "volatile substance" the query returns the general sudden-cardiac-death cardiology literature |
| S3 | volatile substance abuse mortality trends inhalant deaths young people | 25 | target error; re-run as S3b |
| S3b | inhalant related deaths gas aerosol solvent epidemiology mortality | 25 | target error — **the mortality topic was not successfully searched; see "Known gaps" in the DOI list** |
| S4 | inhalant use and inhalant use disorders United States Howard Bowen prevalence treatment | 25 | refused (429); re-run as S4b |
| S4b | inhalant use disorders United States prevalence adolescents treatment review | 25 | 25 hits, 5 retained (Howard 2008, Wu 2006, Wu 2007, Perron 2009, Howard 2009); no treatment trial surfaced, and the "treatment" half of the string returned the general adolescent-substance-treatment literature |
| S5 | poppers alkyl nitrite inhalant toluene maculopathy — with `filter=type:journal-article,has-update:true` (retraction/erratum screen) | 10 | refused (429); re-run as S5b |
| S5b | inhalant nitrite solvent abuse toxicity — with `filter=type:journal-article,has-update:true` | 10 | 5 hits; all in unrelated fields (photosynthetic nitrite reductase, sludge fermentation, a retracted antioxidant paper, a paediatric allergy paper); no update of any kind on a record in this list |

Four of the nine failures in this block fell on the same topic — volatile-substance mortality — which is why that section is empty. The failures were target errors rather than rate-limit refusals, and three different wordings produced the same result, so it is worth trying a shorter string (for example `volatile substance abuse deaths`) when the API is quieter.

### DOI corrections and update checks
- No recalled DOI was written into the list; every DOI was copied from a Crossref response in this session.
- No `works/<DOI>` verification fetch was needed (no DOI came from memory).
- Duplicate DOI: Haverkos 1994 appears as both 10.1289/ehp.94102858 and 10.2307/3432118; the EHP form is listed.
- `updated-by`: no erratum, correction or retraction was found on any of the 63 retained records, and the dedicated `has-update:true` screen returned nothing in this field.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed. For each: **Save → Selection: All results → Format: CSV** into `search-logs/` with the name given; note the hit count.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `("alkyl nitrite*"[Title/Abstract] OR "amyl nitrite"[Title/Abstract] OR "isobutyl nitrite"[Title/Abstract] OR "isopropyl nitrite"[Title/Abstract] OR poppers[Title/Abstract]) AND (humans[MeSH Terms])` | nitrites_pubmed_P1.csv | |
| P2 | `(poppers[Title/Abstract] OR "alkyl nitrite*"[Title/Abstract]) AND (maculopathy OR retina* OR "visual acuity" OR "optical coherence tomography" OR fovea*)` | nitrites_pubmed_P2.csv | |
| P3 | `("amyl nitrite"[Title/Abstract] OR "alkyl nitrite*"[Title/Abstract] OR poppers[Title/Abstract]) AND (methemoglobin* OR methaemoglobin* OR hemolysis OR haemolysis OR G6PD OR "methylene blue")` | nitrites_pubmed_P3.csv | |
| P4 | `(poppers[Title/Abstract] OR "nitrite inhalant*"[Title/Abstract]) AND (sildenafil OR tadalafil OR vardenafil OR "phosphodiesterase type 5" OR "PDE5") ` | nitrites_pubmed_P4.csv | |
| P5 | `(poppers[Title/Abstract] OR "nitrite inhalant*"[Title/Abstract]) AND (chemsex OR "sexualised drug use" OR "sexualized drug use" OR "men who have sex with men" OR HIV)` | nitrites_pubmed_P5.csv | |
| P6 | `(poppers[Title/Abstract] OR "alkyl nitrite*"[Title/Abstract]) AND (death OR deaths OR fatal* OR ingestion OR swallow* OR postmortem)` | nitrites_pubmed_P6.csv | |
| P7 | `("inhalant abuse"[MeSH Terms] OR "solvent abuse"[Title/Abstract] OR "volatile substance"[Title/Abstract] OR "inhalant use"[Title/Abstract]) AND (toluene OR butane OR propane OR difluoroethane OR "lighter fuel" OR aerosol* OR glue)` | inhalants_pubmed_P7.csv | |
| P8 | `("sudden sniffing death"[Title/Abstract] OR ("volatile substance"[Title/Abstract] AND (death OR deaths OR fatal* OR mortality)))` | inhalants_pubmed_P8.csv | |
| P9 | `(toluene[Title/Abstract]) AND (leukoencephalopathy OR "white matter" OR dementia OR cerebell* OR MRI OR neuropsycholog*) AND (abuse OR inhalation OR "inhalant use")` | inhalants_pubmed_P9.csv | |
| P10 | `("inhalant use"[Title/Abstract] OR "inhalant abuse"[Title/Abstract]) AND (prevalence OR epidemiolog* OR trends OR ESPAD OR "Monitoring the Future" OR NSDUH OR adolescen*)` | inhalants_pubmed_P10.csv | |
| P11 | `("inhalant use disorder*"[Title/Abstract] OR "inhalant dependence"[Title/Abstract]) AND (treatment OR intervention OR therapy OR randomized controlled trial[Publication Type])` | inhalants_pubmed_P11.csv | |
| P12 | `("inhalant use"[Title/Abstract] OR "solvent abuse"[Title/Abstract] OR poppers[Title/Abstract]) AND (pregnan* OR prenatal OR neonat* OR "fetal solvent syndrome")` | inhalants_pubmed_P12.csv | |
| P13 | `(poppers[Title/Abstract] OR "inhalant abuse"[Title/Abstract] OR "volatile substance"[Title/Abstract]) AND (retracted publication[Publication Type] OR published erratum[Publication Type])` | inhalants_pubmed_P13.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `inhalant` and `volatile substance` in Cochrane Reviews (the treatment question in P11 is the one this layer is for). Export → `inhalants_cochrane.csv`.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of items 2, 3, 16, 18 and 22 — items 2 and 3 carry the whole pre-2000 nitrite literature, item 16 the toluene literature, item 22 a formal search. Forward: Google Scholar "cited by" on items 4, 5, 14, 15 and 19. The mortality gap should be closed first by forward-citing item 9 and by the reference list of report R1. Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4. Layer 1 so far: 18 Crossref requests attempted, 9 completed, 9 refused or errored; approximately 225 records screened by title and journal; 63 retained.
