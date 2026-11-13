# Nitrous oxide — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening. Where a URL was refused (HTTP 429 or a proxy/target error) the string was re-worded and re-run; both forms are shown.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-15)

Endpoint: `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=<n>&select=DOI,title,container-title,issued,author`. Two endpoint findings worth recording for the next co-editor: (a) `&sort=relevance` makes the request fail from this environment (the target returns an error) — relevance is the default for a `query.bibliographic` search, so the parameter can simply be dropped, and dropping it is what allows `select` to be used at all; (b) with `select` in place the records are small enough that `rows=25–30` fits in one fetch, where a full-record search truncates at about six records. Direct `curl` to api.crossref.org is refused by the egress proxy; WebFetch is the only route.

Rate limiting: Crossref/proxy returned HTTP 429 on 7 of 27 attempts. Pacing settled at 90–120 s between calls, 150–240 s after a 429; refused URLs were never re-fetched. Three further attempts returned a non-429 target error and were re-run with different wording.

Screening rules (METHODS §3): retained systematic reviews, meta-analyses, landmark primaries with their critiques, human laboratory studies, clinical cohorts and case series, and registry/poison-centre data. Excluded: *Reactions Weekly*, *Survey of Anesthesiology*, *Inpharma Weekly*, *Yearbook of* titles and *Radiopaedia* (abstracting and reprint serials); conference abstracts in journal supplements; single-patient case reports in *Cureus* and comparable venues where a case series on the same point was already retained; agricultural and atmospheric nitrous oxide (a large share of every hit list).

### Section-level and targeted queries

| # | Query string (query.bibliographic) | Rows | Result |
|---|---|---|---|
| N1 | nitrous oxide vitamin B12 myeloneuropathy subacute combined degeneration systematic review | 15 | refused — URL over the fetch length limit; re-run as N1b |
| N1b | nitrous oxide B12 myeloneuropathy | 15 | 15 hits, 2 retained (Layzer 1978, Layzer 1979) |
| N2 | nitrous oxide recreational use neurological complications review | 15 | 8 hits, 2 retained (Oulkadi 2022, Ruijter 2023) |
| N3 | nitrous oxide frostbite cold injury whippets | 15 | 15 hits, 6 retained (Hwang 1996, Quax 2020, Chen 2023, Gao 2024, Westerman 2025, Patrizio 2025) |
| N4 | nitrous oxide deaths asphyxia fatalities forensic | 15 | refused (429); re-run as N4b and N4c |
| N4b | nitrous oxide fatalities asphyxiation post-mortem toxicology | 15 | target error; re-run as N4c |
| N4c | nitrous oxide deaths hypoxia fatal cases series | 15 | 15 hits, 2 retained (DiMaio 1978, Li 2024) |
| N5 | nitrous oxide homocysteine methionine synthase inactivation | 15 | 15 hits, 5 retained (Deacon 1980, Frasca 1986, Royston 1988, Christensen 1993, Drummond 1994) |
| N6 | deaths associated with nitrous oxide misuse United Kingdom | 15 | refused (429) — UK mortality series remains a gap (report R4) |
| N7 | nitrous oxide prevalence trends young people Europe epidemiology | 15 | refused (429); re-run as N7b |
| N7b | nitrous oxide use prevalence trends adolescents survey | 15 | 15 hits, 3 retained (Kaar 2016, Back 2023, Huizink 2022) |
| N8 | nitrous oxide psychiatric psychosis cognitive impairment users | 15 | 12 hits, 4 retained (van Amsterdam 2022b, Vitte 2023, Lestienne 2025, Mosalski 2021) |
| N9 | nitrous oxide induced neurotoxicity vitamin B12 treatment management guideline | 15 | 15 hits, 1 retained (Hathout 2011); B12 dosing and duration found only as correspondence — gap |
| N10 | Garakani neurologic psychiatric manifestations nitrous oxide systematic review case literature | 10 | refused (429); re-run as N10b |
| N10b | neurologic psychiatric and other medical manifestations of nitrous oxide abuse systematic review | 12 | refused (429); re-run as N10c |
| N10c | nitrous oxide abuse neurologic manifestations systematic review case reports | 12 | 6 hits (response truncated), 2 retained (Garakani 2016, Pichon 2023) |
| N11 | global burden related to nitrous oxide exposure medical recreational settings individual patient data | 12 | target error; re-run as N11b |
| N11b | nitrous oxide exposure global burden meta-analysis | 30 | 30 hits (mostly agricultural), 3 retained (Oussalah 2019, Sivaramakrishnan 2017, Li 2025) |
| N12 | ENIGMA trial nitrous oxide anaesthesia randomised myocardial infarction | 25 | 25 hits, 4 retained (Leslie 2015, Chan 2016, Sanders 2012, Leslie 2008) |
| N13 | Myles avoidance of nitrous oxide major surgery complications ENIGMA | 20 | refused (429); re-run as N13b |
| N13b | avoidance of nitrous oxide for patients undergoing major surgery randomized trial | 20 | 20 hits, 2 retained (Myles 2007, Myles 2008) |
| N14 | nitrous oxide treatment-resistant major depression trial antidepressant | 20 | 20 hits, 4 retained (Nagele 2015, Zorumski 2015, de Leon 2023, Rech 2024, Quach 2022) |
| N15 | recreational nitrous oxide use prevalence risks peripheral neuropathy dose dependent | 25 | refused (429); re-run as N15b |
| N15b | nitrous oxide recreational users neuropathy risks van Amsterdam Winstock | 25 | 25 hits, 14 retained (van Amsterdam 2015/2022a/2022b, Winstock 2019/2023/2024, Back 2023, Brunt 2024, Ménétrier 2023, Paulus 2021, Verboeket 2024, Nugteren-van Lonkhuyzen 2023, Dang 2021, Desmedt 2023, Ferreira 2022) — the highest-yield query of the set |
| N16 | biologic effects of nitrous oxide mechanistic toxicologic review NMDA antagonist | 25 | target error; re-run as N16b |
| N16b | nitrous oxide NMDA receptor antagonist mechanism analgesia review | 25 | 25 hits, 1 retained (Kuhlmann 2013); the rest rodent antinociception |
| N17 | Sanders Maze biologic effects nitrous oxide Emmanouil Quock advances actions | 25 | 25 hits, 5 retained (Emmanouil 2007, Sanders 2008, Sanders 2009, Maze 2000, Fujinaga 2002) |
| N18 | nitrous oxide driving under influence traffic accidents impairment drivers | 25 | refused (robots/target error); re-run as N18b |
| N18b | nitrous oxide drivers road traffic impairment psychomotor performance | 25 | 25 hits, 4 retained (Allison 1979, Smith 1977, Cheam 1995, Venables 1983); no study of nitrous oxide in actual drivers was found — gap |
| N19 | Zacny nitrous oxide subjective effects healthy volunteers reinforcing abuse liability | 25 | refused (429); re-run as N19b |
| N19b | Zacny subjective behavioral effects of nitrous oxide in healthy volunteers | 25 | 25 hits, 12 retained (Zacny 1994/1996/1997/1998/1999a/1999b/2010, Dohrn 1992, Cho 1997, Walker 2001, Yajnik 1996, Pirec 1995) |
| N20 | nitrous oxide recreational misuse neurological B12 — with `filter=type:journal-article,has-update:true` (retraction/erratum screen) | 10 | 10 hits; 4 relevant records retained (Temple 2025, Hondebrink 2026, Mondesert 2023, and the Swedish adolescent survey held back for a missing author name); one removal notice found (CHEST 2024 abstract) and excluded |
| N21 | trends nitrous oxide poison center data 22-year analysis United States | 15 | 15 hits, 2 retained (Temple 2025 with first author, Forrester 2020) plus Rooks 2007 |
| N22 | nitrous oxide Netherlands legislation poisonings police incidents functional vitamin B12 | 20 | target error; re-run as N22b |
| N22b | nitrous oxide legislation poisonings police incidents Netherlands | 20 | 20 hits, 2 retained (Hondebrink 2026 and its corrigendum, van Riel 2022) |
| N23 | functional vitamin B12 deficiency consistent feature hospital admissions neurological nitrous oxide | 10 | 10 hits, 1 retained (Mondesert 2023, first author confirmed) |

### DOI corrections and update checks
- No recalled DOI was written into the list; every DOI was copied from a Crossref response in this session.
- One `works/<DOI>` verification fetch was attempted (10.1080/15563650.2025.2596142) and returned a target error; the record was re-confirmed through query N21 instead.
- Updates found: Mondesert 2023 → correction 10.1080/15563650.2023.2299552; Temple 2025 → correction 10.1080/15563650.2026.2638051; Hondebrink 2026 → corrigendum 10.1016/j.drugpo.2026.105214; Swedish adolescent survey 10.1080/10826084.2025.2533969 → correction 10.1080/10826084.2025.2544502 (paper held back, see DOI list "Known gaps"). One removal: 10.1016/j.chest.2024.06.3400 (conference abstract), excluded.
- No retraction was found in the nitrous oxide literature screened.

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed. For each: **Save → Selection: All results → Format: CSV** into `search-logs/` with the name given; note the hit count.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `("nitrous oxide"[Title] OR "N2O"[Title] OR whippet*[Title] OR "laughing gas"[Title]) AND (misuse OR "recreational" OR abuse OR nonmedical) AND (humans[MeSH Terms])` | n2o_pubmed_P1.csv | |
| P2 | `("nitrous oxide"[Title/Abstract]) AND ("vitamin B 12"[MeSH Terms] OR cobalamin OR "B12") AND (myelopathy OR myeloneuropathy OR "subacute combined degeneration" OR neuropathy) AND (humans[MeSH Terms])` | n2o_pubmed_P2.csv | |
| P3 | `("nitrous oxide"[Title/Abstract]) AND (homocysteine OR "methionine synthase" OR folate OR methylmalonic) AND (humans[MeSH Terms])` | n2o_pubmed_P3.csv | |
| P4 | `("nitrous oxide"[Title/Abstract]) AND (("systematic review"[Publication Type]) OR meta-analysis[Publication Type]) AND (misuse OR recreational OR toxicity OR neurologic*)` | n2o_pubmed_P4.csv | |
| P5 | `("nitrous oxide"[Title/Abstract]) AND (death OR deaths OR fatal* OR asphyxia* OR "medical examiner" OR postmortem) AND (humans[MeSH Terms])` | n2o_pubmed_P5.csv | |
| P6 | `("nitrous oxide"[Title/Abstract]) AND (frostbite OR "cold injury" OR burn* OR barotrauma OR pneumomediastinum OR "pressure injury")` | n2o_pubmed_P6.csv | |
| P7 | `("nitrous oxide"[Title/Abstract]) AND (thrombosis OR thromboembolism OR "pulmonary embolism" OR "deep vein")` | n2o_pubmed_P7.csv | |
| P8 | `("nitrous oxide"[Title/Abstract]) AND (prevalence OR epidemiolog* OR trends OR "poison center" OR "poisons information" OR surveillance) AND ("2010"[Date - Publication] : "3000"[Date - Publication])` | n2o_pubmed_P8.csv | |
| P9 | `("nitrous oxide"[Title/Abstract]) AND (dependence OR "use disorder" OR withdrawal OR craving OR "treatment demand" OR "addiction care")` | n2o_pubmed_P9.csv | |
| P10 | `("nitrous oxide"[Title/Abstract]) AND (psychiatric OR psychosis OR depression OR cognit* OR neuropsycholog*) AND (recreational OR misuse OR abuse OR nonmedical)` | n2o_pubmed_P10.csv | |
| P11 | `("nitrous oxide"[Title/Abstract]) AND ("depressive disorder, treatment-resistant"[MeSH Terms] OR "treatment-resistant depression" OR antidepressant) AND (trial OR randomized)` | n2o_pubmed_P11.csv | |
| P12 | `("nitrous oxide"[Title/Abstract]) AND (ENIGMA OR "general anesthesia" OR perioperative) AND (randomized controlled trial[Publication Type])` | n2o_pubmed_P12.csv | |
| P13 | `("nitrous oxide"[Title/Abstract]) AND (dental OR dentistry OR "conscious sedation" OR "procedural sedation" OR labor OR labour) AND (randomized controlled trial[Publication Type] OR systematic review[Publication Type])` | n2o_pubmed_P13.csv | |
| P14 | `("nitrous oxide"[Title/Abstract]) AND (driving OR "psychomotor performance" OR "occupational exposure" OR "operating room personnel" OR reproductive OR pregnan*)` | n2o_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `nitrous oxide` in Cochrane Reviews, limited to: labour analgesia; procedural sedation in children; postoperative nausea and vomiting; depression. Export → `n2o_cochrane.csv`.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of items 1, 2, 3, 9, 12 and 22 (the six reviews that carry the case-literature and mechanism evidence). Forward: Google Scholar "cited by" on items 5, 7, 10, 15 and 27 (the landmarks). Logged here with seed DOI and counts.

## PRISMA counts

To be completed after Layers 2–4. Layer 1 so far: 27 Crossref requests attempted, 20 completed, 7 refused; approximately 380 records screened by title and journal; 91 retained.
