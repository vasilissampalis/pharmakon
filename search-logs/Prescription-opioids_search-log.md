# Prescription opioids — search log (PRISMA 2020)

Protocol: `docs/METHODS.md` §2. Section-level strings were written on 2026-10-15 before screening; re-worded re-runs of refused URLs are recorded as such. Dates searched: 2026-10-15 to 2026-10-16. Scope: oxycodone, morphine, hydrocodone, tramadol, codeine.

## Layer 1 — Crossref bibliographic search (run by AI co-editor)

Endpoint and screening rules as in `Heroin_search-log.md`, plus: trade digests (*Reactions Weekly*, *Inpharma Weekly*, *The Back Letter*, *Topics in Pain Management*, *Survey of Anesthesiology* and other reprint vehicles) excluded; conference abstracts in *Value in Health*, *The Journal of Pain* and *European Psychiatry* excluded; duplicate Crossref records for the same article resolved to the more heavily cited record.

Access conditions: of 14 attempted calls, 11 returned records and 3 were refused with HTTP 429. Query strings kept to ≤75 characters. Pacing 110–150 s between calls; the refusal rate rose over the session, so the interval was lengthened.

### Section-level and targeted queries

| # | Query string | Result |
|---|---|---|
| O1 | oxycodone pharmacokinetics pharmacodynamics humans review | 20 hits, 6 retained (Kinnunen 2019; Söderberg Löfdal 2013; Heiskanen 1998; Leow 1992; Leow 1995; Davis 2003). Duplicate Crossref records for Leow 1995 resolved to 10.1097/00000539-199502000-00016 |
| O2 | codeine CYP2D6 ultrarapid metaboliser morphine toxicity children | refused (429); re-run as O3 |
| O3 | codeine pharmacogenetics CYP2D6 morphine formation clinical implications | 20 hits, 9 retained (Crews 2011; Nicholson 2015; Thorn 2009; Sindrup 1995; Eissing 2012; Tseng 1996; He 2008; Vree 2000; Shah 1990) **plus the Koren 2006 Lancet case report and the 2026 Lancet Expression of Concern on it** |
| O4 | tramadol pharmacology seizures serotonin syndrome adverse effects | 20 hits, 3 retained (Hassamal 2018; Mégarbane 2018 critique; Kaye 2015). The rest were *Reactions Weekly* case notices. Tramadol pharmacokinetics not surfaced |
| O5 | OxyContin promotion prescription opioid epidemic public health Van Zee | refused (429); partially re-run as O6 and O10 |
| O6 | prescription opioid epidemic United States policy response review | refused (429) — Kolodny 2015 not located; recorded under Known gaps |
| O7 | opioid prescribing chronic pain long term therapy effectiveness review | 20 hits, 8 retained (Häuser 2016; Chou 2015 reply; Retan 2015; Sehgal 2013; Zenz 1992; Manchikanti 2011 ×2; Rowbotham 2007; Saïdi 2018; Kollas 2024) |
| O8 | opioid versus nonopioid medications pain related function randomized trial | 20 hits, 2 retained (Krebs 2018 SPACE; Chang 2017). The rest were peri-operative opioid-free anaesthesia trials, out of scope |
| O9 | effectiveness and risks of long-term opioid therapy chronic pain systematic | 20 hits, 5 retained (Chou 2015 P2P systematic review; Noble 2008; Sullivan 2022; Savage 1996; Darnall 2012; Waters 2024 and Licciardone 2024 letter pair) |
| O10 | promotion marketing OxyContin commercial triumph public health tragedy | 20 hits, 2 retained (Van Zee 2009; Dennett 2023) |
| O11 | opioid tapering discontinuation overdose mental health crisis cohort | 20 hits, 8 retained (Agnoli 2021 **+ Fenton 2022 correction**; Fenton 2022 JAMA Netw Open; Larochelle 2022; Kennedy 2022 **+ 2023 correction**; Maharjan 2023; Morrow 2026; MacDougall 2022) |
| O12 | opioid prescriptions chronic pain overdose cohort study dose benzodiazepine | 20 hits, 9 retained (Dunn 2010; Dasgupta 2016; Chua 2021; Liang 2015; Kaplovitch 2015; Morasco 2020; Ekholm 2014; Kay 2019; Elyn 2024). Also surfaced an erratum in *Pain* 2022 (10.1097/j.pain.0000000000002615) whose parent record (Hallvik et al.) did not appear — logged under Known gaps |
| O13 | opioid induced hyperalgesia humans systematic review evidence | 20 hits, 11 retained (Angst 2006; Chu 2008; Fletcher 2014; Higgins 2019; Yang 2019; Guichard 2021; Kim 2014; Kim 2015; Rivosecchi 2014; Xie 2023; Ramasubbu 2011) |
| O14 | nonmedical prescription opioid use transition heroin initiation cohort | 20 hits, 12 retained (Compton 2016 **+ NEJM correspondence**; Jones 2013; Cerdá 2015; Kelley-Quon 2019; Banerjee 2016; Guarino 2018; Martins 2015; Marsh 2018; Havens 2020; Surratt 2017; Veliz 2016) |
| O15 | codeine promethazine cough syrup lean purple drank nonmedical use | 20 hits, 10 retained (Agnich 2013; Miuli 2020; Peters 2003, 2007 ×2; Chiappini 2021; Wu 2016; Weppner 1971; Tettey 2020; Winek 1970) |

Records carried in from searches run for other substances in this session: Bohnert 2011 (JAMA) and Calcaterra 2013 (Drug Alcohol Depend), surfaced by the nitazene and carfentanil strings; Huang 2018 (Am J Public Health), Bohm 2020, Kuo 2021 and Bharat 2024, surfaced by the heroin mortality strings.

### DOI corrections and update checks

- No DOI was written from memory; all 100 were copied from Crossref responses in this session. No `works/<DOI>` re-fetch was needed; nothing was dropped.
- **Integrity notices found in the search records:** (a) an Expression of Concern, issued 2026 by the editors of The Lancet, on Koren et al. 2006 (codeine in a breastfeeding mother); (b) a JAMA correction, "Errors in data analysis and outcomes coding", on Agnoli et al. 2021; (c) a PLOS Medicine correction on Kennedy et al. 2022. All three parent papers are retained and flagged in the DOI list; the Koren paper must not be used as evidence until the Expression of Concern has been read.
- Duplicate Crossref records were resolved for Leow 1995 (Anesth Analg) and for the *Survey of Anesthesiology* reprint of Bohnert 2011.
- Retraction field (`updated-by`) not read; Retraction Watch check outstanding for all items.

## Layer 2 — PubMed (to be run by VS)

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(oxycodone[Title] OR hydrocodone[Title] OR morphine[Title] OR tramadol[Title] OR codeine[Title]) AND (pharmacokinetic* OR metabolism OR "active metabolite*") AND humans[MeSH Terms]` | rxopioids_pubmed_P1.csv | |
| P2 | `(codeine[Title] OR tramadol[Title]) AND (CYP2D6 OR pharmacogenetic* OR "ultrarapid metaboli*") AND (toxicity OR death* OR children OR breastfeeding OR analgesia)` | rxopioids_pubmed_P2.csv | |
| P3 | `(tramadol[Title]) AND (seizure* OR "serotonin syndrome" OR dependence OR withdrawal OR death*) AND humans[MeSH Terms]` | rxopioids_pubmed_P3.csv | |
| P4 | `("long-term opioid therapy" OR "chronic opioid therapy") AND ("chronic pain") AND (randomized controlled trial[Publication Type] OR "systematic review"[Publication Type] OR meta-analysis[Publication Type])` | rxopioids_pubmed_P4.csv | |
| P5 | `("opioid dose"[Title/Abstract] OR "morphine equivalent*") AND (overdose OR mortality) AND (cohort OR "case-control" OR "dose-response")` | rxopioids_pubmed_P5.csv | |
| P6 | `(opioid*[Title]) AND (taper* OR discontinu* OR "dose reduction") AND (overdose OR suicide OR "mental health crisis" OR mortality)` | rxopioids_pubmed_P6.csv | |
| P7 | `("opioid-induced hyperalgesia"[Title/Abstract]) AND humans[MeSH Terms] AND (systematic review[Publication Type] OR meta-analysis[Publication Type] OR "quantitative sensory testing")` | rxopioids_pubmed_P7.csv | |
| P8 | `(opioid*[Title]) AND (benzodiazepine* OR gabapentin* OR pregabalin OR "z-drug*") AND (overdose OR "respiratory depression" OR mortality) AND humans[MeSH Terms]` | rxopioids_pubmed_P8.csv | |
| P9 | `("prescription opioid*"[Title/Abstract]) AND (heroin[Title/Abstract]) AND (transition OR initiation OR trajector*) AND (cohort OR longitudinal)` | rxopioids_pubmed_P9.csv | |
| P10 | `("prescription drug monitoring program*" OR "abuse-deterrent formulation*" OR "OxyContin reformulation") AND (opioid* OR heroin) AND (evaluation OR effect* OR substitution)` | rxopioids_pubmed_P10.csv | |
| P11 | `(codeine[Title]) AND ("over-the-counter" OR "cough syrup" OR promethazine OR "purple drank" OR dependence)` | rxopioids_pubmed_P11.csv | |
| P12 | `(opioid*[Title]) AND (endocrin* OR hypogonadism OR immunosuppress* OR constipation OR "sleep-disordered breathing" OR "sleep apnea") AND (chronic OR "long-term")` | rxopioids_pubmed_P12.csv | |
| P13 | `(opioid* AND (prescri* OR analgesic*)) AND (Europe OR Greece OR "United Kingdom" OR Germany) AND (consumption OR trends OR misuse OR deaths)` | rxopioids_pubmed_P13.csv | |
| P14 | `(tramadol OR codeine) AND (Africa OR Egypt OR Nigeria OR "Middle East" OR India) AND (epidemic OR misuse OR prevalence OR seizure*)` | rxopioids_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search: `opioids for chronic non-cancer pain`; `opioids low back pain`; `opioids osteoarthritis`; `tramadol`; `codeine cough`; `opioid tapering`. Export each → `rxopioids_cochrane_<topic>.csv`.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of items 1, 4, 20, 22, 23 and 16. Forward: "cited by" on items 1, 5, 6, 7, 9 and 15 — in particular to recover Kolodny 2015, Busse 2018, Oliva 2020 and the abuse-deterrent-formulation literature, which the Crossref layer did not surface.

## PRISMA counts

To be completed after Layers 2–4. Layer 1 so far: 14 Crossref calls attempted, 11 result sets screened (approximately 220 records), 100 records retained.
