# Kratom (Mitragyna speciosa) — search log (PRISMA 2020)

Protocol: `docs/METHODS.md` §2. Section-level strings were written on 2026-10-15 before screening; re-worded re-runs of refused URLs are recorded as such. Date searched: 2026-10-16.

## Layer 1 — Crossref bibliographic search (run by AI co-editor)

Endpoint and screening rules as in `Heroin_search-log.md`. Additional exclusions here: *Reactions Weekly* notices; FASEB Journal, Toxicology Letters and Japanese Pharmacological Society conference abstracts; extraction-chemistry, antioxidant-assay and agronomy papers with no bearing on human effects; non-indexed regional journals where an indexed source covers the same ground. *ChemInform* abstract records were kept only where no other record of the original paper was surfaced, and are flagged in the list.

Access conditions: of 10 attempted calls, 6 returned records, 2 were refused with HTTP 429 and 2 returned a transient target error. Pacing 150 s between calls.

### Section-level and targeted queries

| # | Query string | Result |
|---|---|---|
| K1 | mitragynine 7-hydroxymitragynine kratom opioid receptor pharmacology Kruegel | transient target error; re-run as K2 |
| K2 | mitragynine 7-hydroxymitragynine opioid receptor pharmacology kratom | refused (429); re-run as K3 |
| K3 | kratom Mitragyna speciosa alkaloids pharmacology mu opioid review | 20 hits, 8 retained (Schimmel 2020; Hartley 2022; Abdullah 2021 ×2; Kameg 2026; Garza-Garcia 2024; Mudge 2019 **+ 2026 correction**; Torres-Ortiz 2022; Takayama 2004 ChemInform record) |
| K4 | Kruegel mitragynine pseudoindoxyl biased agonism mu opioid receptor | 20 hits, 7 retained (Yamamoto 1999; White 2025; Eccarius 2026; Bahari 2026; Kelly 2023; Thompson 2016; Vasudevan 2020). **Kruegel's own 2016/2019 papers and Váradi 2016 were not surfaced; recorded under Known gaps** |
| K5 | kratom use survey dependence withdrawal self-treatment opioid United States | 20 hits, 5 retained (Boyer 2007, 2008; Buttram 2024; Sivakumar 2025; Sherrick 2026; Wu 2016 as context). The string drifted heavily into the general opioid-use-disorder treatment literature |
| K6 | Grundmann Garcia-Romeu kratom users survey patterns motivations effects | 20 hits, 17 retained (Grundmann 2017, 2020, 2023; Garcia-Romeu 2020; Swogger 2022; Henningfield 2022, 2023; Smith 2022 ×3, 2023, 2024 ×2; Hill 2025; Vadiei 2025; Singh 2019; Abdullah 2020 ECG; Hubley 2026) — the single most productive call of this build |
| K7 | kratom related deaths poison center exposures mitragynine postmortem | refused (429); re-run as K8 |
| K8 | kratom associated fatalities mitragynine toxicology medical examiner cases | 20 hits, 11 retained (Schmitt 2021; McIntyre 2014; Papsun 2019, 2023; Eccarius 2026; Overbeek 2019; Heywood 2027; Barrett 2026; **Huestis 2026 human pharmacokinetics**; Le 2012; Uchaipichat 2025; Limsuwanchote 2016; Tokuda 2024) |
| K9 | kratom Malaysia Thailand traditional use dependence rural community users | transient target error; re-run as K10 |
| K10 | Singh kratom dependence withdrawal Malaysia regular users cognitive | 20 hits, 16 retained (Singh 2014, 2015, 2018 ×2, 2019 ×2, 2020, 2026; Saref 2019; Abdullah 2019, 2020 ×2, 2021 ×2; Jasim 2021; Ang 2026; Yang 2025; Smith 2017; Karunakaran 2024) |

One further record, Smith et al. 2019 on non-prescribed buprenorphine mediating the relationship between heroin and kratom use (10.1080/02791072.2019.1597224), was surfaced by the buprenorphine-diversion string in the Methadone-Buprenorphine build and carried here.

### DOI corrections and update checks

- No DOI was written from memory; all 72 were copied from Crossref responses in this session. No `works/<DOI>` re-fetch was needed; nothing was dropped.
- Correction found: Mudge & Brown 2019 (J AOAC Int) has a 2026 correction, 10.1093/jaoacint/qsag052.
- One record (Takayama 2004) is a *ChemInform* abstracting record rather than the primary article; it is listed with an instruction to obtain the original *Chemical and Pharmaceutical Bulletin* paper it abstracts.
- Two Crossref records exist for Limsuwanchote's ELISA work (*Planta Medica* 2015 conference abstract and *Forensic Toxicology* 2016 full paper); the full paper is listed.
- Retraction field (`updated-by`) not read; Retraction Watch check outstanding for all items.

### Note on literature size

This substance is declared a thin literature under the brief's rule. Ten Crossref calls were planned and ten were attempted; the six that completed were sufficient to saturate the field's main lines of work (the Grundmann/Garcia-Romeu/Smith US survey programme, the Singh/Abdullah Malaysian field programme, the Papsun/Schmitt forensic programme, and the small pharmacology literature). The residual gaps are specific named papers, not unexplored sections, with two exceptions: controlled human laboratory studies and poison-centre series, both of which the PubMed layer must cover.

## Layer 2 — PubMed (to be run by VS)

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(kratom[Title/Abstract] OR "Mitragyna speciosa"[Title/Abstract] OR mitragynine[Title/Abstract]) AND (pharmacolog* OR "opioid receptor" OR "biased agonis*" OR "partial agonis*")` | kratom_pubmed_P1.csv | |
| P2 | `(mitragynine[Title/Abstract] OR "7-hydroxymitragynine"[Title/Abstract]) AND (pharmacokinetic* OR metabolism OR CYP OR "drug interaction*") AND humans[MeSH Terms]` | kratom_pubmed_P2.csv | |
| P3 | `(kratom[Title/Abstract]) AND (dependence OR withdrawal OR "use disorder" OR craving) AND humans[MeSH Terms]` | kratom_pubmed_P3.csv | |
| P4 | `(kratom[Title/Abstract]) AND (survey OR prevalence OR "use patterns" OR motivations OR "ecological momentary")` | kratom_pubmed_P4.csv | |
| P5 | `(kratom[Title/Abstract] OR mitragynine[Title/Abstract]) AND (death* OR fatal* OR postmortem OR "medical examiner" OR overdose)` | kratom_pubmed_P5.csv | |
| P6 | `(kratom[Title/Abstract]) AND ("poison center" OR "poison centre" OR "National Poison Data System" OR exposure* OR toxicity) AND (series OR surveillance OR trends)` | kratom_pubmed_P6.csv | |
| P7 | `(kratom[Title/Abstract] OR mitragynine[Title/Abstract]) AND (hepatotox* OR "liver injury" OR DILI OR jaundice OR cholestasis)` | kratom_pubmed_P7.csv | |
| P8 | `(kratom[Title/Abstract]) AND ("opioid withdrawal" OR "self-treatment" OR "harm reduction" OR "opioid use disorder") AND (treatment OR substitution)` | kratom_pubmed_P8.csv | |
| P9 | `("7-hydroxymitragynine"[Title/Abstract] OR "7-OH" OR "mitragynine pseudoindoxyl") AND (product* OR extract* OR potency OR concentrat* OR regulation)` | kratom_pubmed_P9.csv | |
| P10 | `(kratom[Title/Abstract] OR "Mitragyna speciosa"[Title/Abstract]) AND (Malaysia OR Thailand OR Indonesia OR "Southeast Asia") AND (traditional OR community OR users OR decriminali*)` | kratom_pubmed_P10.csv | |
| P11 | `(kratom[Title/Abstract]) AND (seizure* OR psychosis OR cardiac OR QT OR "respiratory depression" OR hyperkalemia)` | kratom_pubmed_P11.csv | |
| P12 | `(kratom[Title/Abstract]) AND (pregnan* OR neonat* OR "neonatal opioid withdrawal" OR breastfeed*)` | kratom_pubmed_P12.csv | |
| P13 | `(kratom[Title/Abstract]) AND (adulterant* OR krypton OR "O-desmethyltramadol" OR contamination OR "heavy metal*" OR Salmonella)` | kratom_pubmed_P13.csv | |
| P14 | `(kratom[Title/Abstract]) AND (policy OR scheduling OR "consumer protection" OR regulation OR FDA OR WHO)` | kratom_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `kratom` and `mitragynine` in Cochrane Reviews. Expected: no reviews. Record the nil result — it is itself reportable in the monograph's research-gaps section.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of items 1, 2, 11, 18, 21, 22 and 24. Forward: "cited by" on items 3, 6, 7, 10 and 13 — the priority is to recover the Kruegel and Váradi pharmacology papers, the Post/Eggleston poison-centre series and the Olsen MMWR death analysis, none of which the Crossref layer surfaced.

## PRISMA counts

To be completed after Layers 2–4. Layer 1 so far: 10 Crossref calls attempted, 6 result sets screened (approximately 120 records), 72 records retained.
