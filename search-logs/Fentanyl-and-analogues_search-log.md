# Fentanyl and analogues — search log (PRISMA 2020)

Protocol: `docs/METHODS.md` §2. Section-level strings were written on 2026-10-15 before screening; re-worded re-runs of refused URLs are recorded as such. Date searched: 2026-10-15. Scope includes fentanyl analogues, nitazene (benzimidazole) opioids and xylazine as an adulterant.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-15)

Endpoint and screening rules as in `Heroin_search-log.md`. Additional exclusions applied here: *Reactions Weekly*, *Alcoholism & Drug Abuse Weekly*, *The Back Letter*, *Brown University* update newsletters and *Clinical Pharmacist* news items (trade digests, not primary sources); single-patient peri-operative case reports where a published series covers the same phenomenon; analytical-method papers unless they bear on detection in the drug supply or on post-mortem interpretation.

Access conditions: of 15 attempted calls, 11 returned records, 3 were refused with HTTP 429 and 1 returned a transient target error. Query strings were kept to ≤75 characters to stay inside the proxy's URL-length limit. Pacing 110 s between calls.

### Section-level and targeted queries

| # | Query string | Result |
|---|---|---|
| F1 | fentanyl analogues pharmacology potency structure activity review | 20 hits, 6 retained (Higashikawa 2008; Casy 1988; Casy 1982; Vučković 1995; Finch 1967; Hiranita 2024). Weak yield — the string pulled unrelated structure–activity literature from other drug classes |
| F2 | illicit fentanyl analogues forensic toxicology review deaths | 20 hits, 14 retained (Henderson 1991; Denton 2008; Marinetti 2014; Palmer 2010; Krinsky 2011; Jumbelic 2010; Ruan 2016; Roxburgh 2022; Kleinman 2024; Schackmuth 2018; Rab 2019; Ellefsen 2023; Vincent 2024) |
| F3 | fentanyl chest wall rigidity wooden chest syndrome overdose | 20 hits, 3 retained (Çoruh 2013; Rosal 2021; Baruah 2022). The remainder were *Reactions Weekly* entries and conference abstracts; the mechanism literature (Torralva & Janowsky) was not surfaced |
| F4 | synthetic opioid overdose death rates trends United States fentanyl | 20 hits, 6 retained (Gladden 2016; Jones 2018; Miller 2025; Raheemullah 2019; Chen 2022; Segel 2020) |
| F5 | higher naloxone doses fentanyl overdose reversal debate evidence | 20 hits, 1 retained (Fareed 2015). The naloxone-dosing debate papers themselves were not surfaced; recorded under Known gaps |
| F6 | limitations naloxone reversal respiratory depression prevention cardiac arrest | transient target error; re-run as F7 |
| F7 | naloxone reversal opioid induced respiratory depression cardiac arrest Dahan | 20 hits, 13 retained (van Lemmen 2023 **+ erratum**; van Lemmen 2026; Dahan 2010; Dahan 2026; van der Schrier 2021; van der Schier 2014; Roozekrans 2014; Olofsen 2010; Laffont 2024; Purohit 2025; Jansen 2024; plus van Dorp 2006 and Yassen 2007, carried to the Methadone-Buprenorphine map) |
| F8 | fentanyl test strips drug checking people who use drugs behaviour | 20 hits, 14 retained (Krieger 2018; Bergh 2021; Zibbell 2024; Erickson 2026; Tilhou 2023; Goldman 2024; Sisco 2024; Reed 2022; Geddes 2018; Sutherland 2025; Aronson 2024; Olson 2022; Haider 2025; Goh 2025; Noguchi 2026; Naidu 2026; Ludwig 2026; Peiper 2025; Shaw 2025) |
| F9 | nitazene isotonitazene benzimidazole opioid deaths case series | 20 hits, 11 retained (Montanari 2022; Vandeputte 2022; Shover 2020; Nahar 2021; Walton 2025; Roberts 2022; Papsun 2017; Gevorkyan 2021; Schüller 2023; Tishion 2025; Zhao 2023). Also surfaced Bohnert 2011 JAMA, carried to the Prescription-opioids map |
| F10 | xylazine adulterant illicit opioid supply wounds overdose review | 20 hits, 8 retained (Wu 2024; Love 2026; Zhu 2026; Zhu 2025; Levine 2026; Duhart Clarke 2022; Noonan 2023; Colbert 2026) |
| F11 | carfentanil related deaths detection potency opioid outbreak | 20 hits, 1 retained for this map (Zibbell 2019 Ohio seizures). The string drifted to the prescription-opioid mortality literature; Calcaterra 2013 was surfaced and carried to the Prescription-opioids map. Carfentanil-specific case series not surfaced |
| F12 | Ciccarone heroin fentanyl triple wave overdose crisis drug supply | 20 hits, 15 retained (Ciccarone 2009 ×1, 2017 ×2, 2019, 2021, 2025; Unick 2014, 2017; Hempstead 2013; Coffin 2022; Peiper 2019; Montero 2022; Cano 2023; Sibley 2026; Huhn 2026; Schwehr 2025) |
| F13 | fentanyl clinical pharmacokinetics context sensitive half time review | refused (429) — **human PK of fentanyl not covered; recorded under Known gaps** |
| F14 | fentanyl use patterns tolerance withdrawal people who use drugs | refused (429) — **tolerance and use patterns not covered; recorded under Known gaps** |

### DOI corrections and update checks

- No DOI was written from memory; all 96 were copied from Crossref responses in this session. No `works/<DOI>` re-fetch was needed and no DOI was dropped.
- Correction found in the search records: van Lemmen et al. 2023 (Anesthesiology) carries an erratum, 10.1097/aln.0000000000004760, listed as item 9.
- Four records surfaced here belong to other maps and were carried across rather than listed: Bohnert 2011 (JAMA) and Calcaterra 2013 (Drug Alcohol Depend) → Prescription-opioids; van Dorp 2006 (Anesthesiology) and Yassen 2007 (Clin Pharmacokinet) → Methadone-Buprenorphine.
- Retraction field (`updated-by`) not read; Retraction Watch check outstanding for all items.

## Layer 2 — PubMed (to be run by VS)

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(fentanyl[Title]) AND (pharmacokinetic* OR "context-sensitive" OR lipophilic* OR potency OR "receptor binding") AND humans[MeSH Terms]` | fentanyl_pubmed_P1.csv | |
| P2 | `(fentanyl[Title] OR "fentanyl analog*"[Title/Abstract]) AND ("chest wall rigidity" OR "wooden chest" OR "muscle rigidity" OR laryngospasm)` | fentanyl_pubmed_P2.csv | |
| P3 | `(fentanyl OR "synthetic opioid*") AND (overdose[Title] OR "overdose death*"[Title]) AND (trend* OR epidemiolog* OR surveillance OR cohort)` | fentanyl_pubmed_P3.csv | |
| P4 | `(naloxone[Title]) AND (fentanyl OR "synthetic opioid*") AND (dose OR dosing OR "two doses" OR "higher dose" OR nalmefene)` | fentanyl_pubmed_P4.csv | |
| P5 | `("fentanyl test strip*" OR "drug checking") AND (overdose OR behavior* OR behaviour* OR "harm reduction") AND humans[MeSH Terms]` | fentanyl_pubmed_P5.csv | |
| P6 | `(nitazene* OR isotonitazene OR metonitazene OR etonitazene OR protonitazene OR "benzimidazole opioid*") AND (death* OR intoxication OR pharmacolog* OR seizure)` | fentanyl_pubmed_P6.csv | |
| P7 | `(carfentanil[Title/Abstract]) AND (death* OR detection OR outbreak OR potency OR exposure)` | fentanyl_pubmed_P7.csv | |
| P8 | `(xylazine[Title]) AND (human* OR "people who use drugs" OR wound* OR withdrawal OR overdose OR naloxone)` | fentanyl_pubmed_P8.csv | |
| P9 | `(fentanyl[Title]) AND (tolerance OR withdrawal OR "use pattern*" OR qualitative) AND ("people who use drugs" OR "injection drug use" OR cohort)` | fentanyl_pubmed_P9.csv | |
| P10 | `("opioid-induced respiratory depression"[Title/Abstract]) AND (mechanism* OR reversal OR "cardiac arrest" OR hypoxia) AND humans[MeSH Terms]` | fentanyl_pubmed_P10.csv | |
| P11 | `(fentanyl OR "synthetic opioid*") AND (stimulant* OR methamphetamine OR cocaine) AND (co-use OR polysubstance OR "fourth wave")` | fentanyl_pubmed_P11.csv | |
| P12 | `(fentanyl[Title]) AND (Estonia OR Europe OR "European") AND (epidemic OR deaths OR prevalence)` | fentanyl_pubmed_P12.csv | |
| P13 | `("illicitly manufactured fentanyl" OR "fentanyl-adulterated") AND (heroin OR counterfeit OR "pressed pill*" OR supply)` | fentanyl_pubmed_P13.csv | |
| P14 | `(medetomidine OR BTMPS OR "novel adulterant*") AND ("drug supply" OR overdose OR "people who use drugs")` | fentanyl_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `naloxone overdose`, `opioid overdose prevention`, `drug checking`. Export → `fentanyl_cochrane_<topic>.csv`. A Cochrane review specific to illicit fentanyl is not expected; the relevant reviews are on naloxone for opioid overdose and on opioid agonist treatment.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of items 1, 2, 8, 10, 19 and 22 (the reviews). Forward: "cited by" on items 1, 3, 5, 16, 19 and 22 — in particular to recover the naloxone-dosing debate, the chest-wall-rigidity mechanism papers and the carfentanil case series, which the Crossref layer did not surface.

## PRISMA counts

To be completed after Layers 2–4. Layer 1 so far: 15 Crossref calls attempted, 11 result sets screened (approximately 220 records), 96 records retained.
