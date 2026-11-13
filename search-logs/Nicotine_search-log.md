# Nicotine — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; not altered during screening.

## Scope decision recorded before searching

The strings deliberately target **nicotine** rather than **tobacco smoking**. Queries were anchored on nicotine pharmacology, nicotine delivery systems (transdermal, intravenous, reduced-nicotine cigarettes, snus, pouches, e-cigarettes) and nicotine dependence, and were not extended to the smoking-and-disease literature, which belongs to a tobacco page and would have swamped every result set. This is a scope choice, not a coverage failure, and the monograph should state it.

## Layer 1 — Crossref bibliographic search (run by AI, 2026-10-15)

### Conditions

Crossref's REST API was throttled throughout this session: HTTP 429 after roughly every second request, plus intermittent `CLIENT_ERROR` refusals. Pauses of 90–300 s were taken after every refusal, and a refused URL was never re-fetched as written. Direct (non-WebFetch) access to `api.crossref.org` is blocked in this environment.

As with the other lists in this batch, **every DOI was taken verbatim from a Crossref works-search record returned in this session** rather than recalled and then checked with `works/<DOI>`. The WebFetch proxy refuses URLs longer than roughly 250 characters, capping each query at about 90 characters of search terms.

One Crossref behaviour cost a query outright and is worth recording: Crossref weights **container titles** heavily, and for this substance the journal *Nicotine & Tobacco Research* exists. A query on `cardiovascular effects of nicotine itself independent of tobacco smoke review` returned 23 of 25 hits from that journal on unrelated topics (smoke-free policies, secondhand smoke, radioactivity in tobacco). Queries anchored on an author surname (`Benowitz`) or on an exact title fragment were far more productive. Whoever searches a substance whose name is also a journal name should expect this.

### Pre-specified section queries (`filter=type:journal-article`, relevance-sorted)

| # | Query string | Status | Hits screened | Retained |
|---|---|---|---|---|
| NI1 | `nicotine addiction pharmacology nicotinic receptors Benowitz review` | 429 refused; re-worded as NI1b | — | — |
| NI1b | `nicotine addiction pharmacology pharmacokinetics nicotinic acetylcholine receptor review` | run (rows 25) | 25 | 3 (Wittenberg 2020; Govind 2009; Mineur 2008) — the rest was preclinical molecular work excluded under METHODS §5.4 |
| NI2 | `pharmacology of nicotine addiction smoking-induced disease and therapeutics` | run (rows 25) | 25 | 9 (Benowitz 2009; Benowitz 1996; Benowitz 2006; Benowitz 2004; Lerman 2006; Sabha 2000; Tutka 2019; Perkins 2009; Balfour 1996) |
| NI3 | `electronic cigarettes for smoking cessation Cochrane systematic review randomised trial` | 429 refused; variant `electronic cigarettes smoking cessation randomised controlled trial nicotine replacement` CLIENT_ERROR; variant `e-cigarettes versus nicotine replacement therapy randomized trial smoking cessation` 429 refused; re-worded as NI3b | — | — |
| NI3b | `electronic cigarettes smoking cessation Cochrane review nicotine randomised` | run (rows 25) | 25 | 4 (Hartmann-Boyce 2016 CD010216.pub3; Grabovac 2020; Pisinger 2020 critique; Vaz-Carneiro 2015) — eleven of the 25 hits were *Cochrane Clinical Answers* summaries of the same review |
| NI4 | `e-cigarette use adolescents subsequent cigarette smoking gateway longitudinal` | run (rows 25) | 25 | 10 (Soneji 2018 **correction**; Shahab 2020; Sun 2023; Cheng 2020 v3; Goldenson 2017; Duan 2021; Lozano 2017; Patanavanich 2022; Soneji 2015; Camenga 2018; Hanewinkel 2021; Gordon 2023) |
| NI5 | `nicotine replacement therapy varenicline bupropion smoking cessation network meta-analysis` | run (rows 25) | 25 | 9 (Mills 2012; Zhou 2025; Lang 2024 critique + Cinciripini 2024 reply; Zhong 2019; Wang 2026; Altalhi 2024; Hsueh 2021; Athanasakis 2012) |
| NI6 | `snus smokeless tobacco nicotine pouches health effects Sweden harm reduction` | run (rows 25) | 25 | 16 (Foulds 2003; Gartner 2007; Benowitz 2011; Kopa-Stojak 2026; Ramstrom 2024; Colilla 2010; Nelson 2018; La Rosa 2026; Pierce 2002; Kozlowski 2002; Stepanov 2012; Blank 2008; Frost-Pineda 2010; Rodu 2008; Foulds 2008; Sohlberg 2020; Ruokolainen 2025; Polosa 2025; Berg 2014; Tomar 2007) |
| NI7 | `cardiovascular effects of nicotine itself independent of tobacco smoke review` | run (rows 25) | 25 | 2 (Swan 2007; Hoffman 2012) — container-title failure, see Conditions |
| NI8 | `prevalence correlates of DSM nicotine dependence tobacco use disorder national survey` | run (rows 25) | 25 | 9 (Breslau 1994; Jackson 2025; Chung 2012; Storr 2004; Dierker 2008; Degenhardt 2001; Zech 2025; Gupta 2026; Ibrahim 2021; Hunter 2018; Rose 2004; Chen 2026 — the last three carried from NI6/NI7 result sets) |

Searches that returned records: 8. Searches refused (429 or CLIENT_ERROR) and not re-run as written: 6.

Planned but not run before the query budget was exhausted: heated tobacco products; EVALI and vaping lung injury; nicotine in pregnancy; nicotine and adolescent brain development; e-liquid poisoning in children. All are itemised in the Known gaps paragraph of `Nicotine_DOI-LIST.md`.

### DOIs corrected or dropped at screening

- No DOI was recalled from memory, so none resolved to a different paper and none was corrected.
- *Cochrane Clinical Answers* records excluded wholesale (10.1002/cca.3341, .3703, .3875, .4184, .4435, .4627, .4745, .4882, .1502, .3205, .4338, .3881): these are plain-language summaries of reviews, not reviews.
- Study protocols excluded: 10.18332/tpc/128462 (ECSMOKE), 10.1186/1471-2458-13-210 (Bullen's ASCEND protocol — the published trial is in Known gaps), 10.1186/s13063-023-07876-y, and 10.1002/14651858.cd016337 (a 2026 Cochrane record with no citations, which has the signature of a protocol rather than a completed review; it must be checked before use).
- *Journal of Vascular Surgery* abstract reprints of trials published elsewhere excluded: 10.1016/j.jvs.2014.01.028 (Bullen), 10.1016/j.jvs.2014.08.086 (Koegelenberg). The underlying trials should be obtained from their original journals via the PubMed layer.
- Other conference/supplement abstracts excluded: 10.1016/j.chest.2021.07.2124, 10.1016/s1098-3015(11)72236-7, 10.1016/s1098-3015(10)74464-8, 10.1016/s0924-977x(05)81242-8, 10.1158/1538-7445.am10-3231.
- Low-rigour or non-indexed venues excluded: 10.7759/cureus.54228, 10.21276/ijcmr.2019.6.11.8, 10.21276/ijcmr.2019.6.6.52, 10.64355/agjhss4111, 10.24321/2454.325x.202301, 10.13188/2330-2178.1000022, 10.31436/jop.v4i2.328, 10.66794/2c70, 10.14340/spp.2013.10a0004, 10.2139/ssrn.3422321 (SSRN preprint of a paper published as #15).
- Superseded versions excluded in favour of the current one: 10.12688/f1000research.21377.1 and .2 (versions 1 and 2 of Cheng et al.; version 3 is listed).
- News-digest and editorial items excluded: *The Pharmaceutical Journal* (four records), 10.1016/s0027-9684(15)30794-x, 10.1136/ebn.12.1.10, 10.1136/bmj.i4819, 10.1093/ntr/ntw207.
- Cost-effectiveness analyses for Belgium, Nicaragua and Spain excluded as out of scope; the Greek one (Athanasakis 2012) is kept.

### Errata/retractions

- **Correction found and listed as a numbered item:** Soneji et al. 2018, *Errors in data input in meta-analysis on association between initial use of e-cigarettes and subsequent cigarette smoking among adolescents and young adults* (JAMA Pediatr, 10.1001/jamapediatrics.2017.4200). This corrects the 2017 JAMA Pediatrics gateway meta-analysis, whose own DOI did not surface in this session. The pair must be obtained together and the parent paper must never be cited without the correction. This is the most consequential errata finding across the four substances in this batch, because the uncorrected meta-analysis is still widely cited in the youth-uptake debate.
- Superseded Cochrane version noted: CD010216.pub3 (2016) is the version Crossref returned; a later `.pubN` supersedes it and is the one to obtain.
- Retracted papers: none identified among the 72 retained.

### Conflict-of-interest marking

Four retained papers carry `[industry-linked authorship — check COI]` in the DOI list (Colilla 2010; Frost-Pineda 2010; Rodu & Phillips 2008; Polosa 2025). The marking records that METHODS §14 must be applied when the study card is written; it is a prompt to check the declaration, not a finding about any author. The snus and nicotine-pouch literature cannot be represented honestly by excluding industry-linked work, but it also cannot be read without that check.

Screening outcome: 72 journal articles retained into `Nicotine_DOI-LIST.md` (Tier A 28, Tier B 26, Tier C 18).

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count shown by PubMed next to each string and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(nicotine[Title]) AND (pharmacokinetic* OR pharmacolog* OR metabolism OR CYP2A6 OR cotinine OR "nicotine metabolite ratio") AND (humans[MeSH Terms])` | Nicotine_pubmed_P1.csv | |
| P2 | `(nicotine[Title]) AND (cardiovascular OR "blood pressure" OR "heart rate" OR endothelial OR arrhythmia) NOT (smoking[Title]) AND (humans[MeSH Terms])` | Nicotine_pubmed_P2.csv | |
| P3 | `("nicotine dependence"[Title] OR "tobacco use disorder"[Title] OR "nicotine use disorder"[Title]) AND (prevalence OR epidemiolog* OR DSM OR Fagerstrom OR measurement)` | Nicotine_pubmed_P3.csv | |
| P4 | `("electronic cigarette*"[Title] OR "e-cigarette*"[Title] OR vaping[Title] OR ENDS[Title]) AND (smoking cessation[MeSH Terms]) AND (randomized controlled trial[Publication Type] OR systematic review[Publication Type] OR meta-analysis[Publication Type])` | Nicotine_pubmed_P4.csv | |
| P5 | `("electronic cigarette*" OR "e-cigarette*") AND (adolescent*[Title] OR youth[Title] OR "young adult*"[Title]) AND (gateway OR "subsequent" OR initiation OR "common liability") AND (humans[MeSH Terms])` | Nicotine_pubmed_P5.csv | |
| P6 | `("nicotine replacement"[Title] OR varenicline[Title] OR bupropion[Title] OR cytisine[Title] OR cytisinicline[Title]) AND (randomized controlled trial[Publication Type] OR meta-analysis[Publication Type])` | Nicotine_pubmed_P6.csv | |
| P7 | `(snus[Title] OR "smokeless tobacco"[Title] OR "nicotine pouch*"[Title] OR "oral nicotine"[Title]) AND (humans[MeSH Terms]) AND ("2010"[Date - Publication] : "3000"[Date - Publication])` | Nicotine_pubmed_P7.csv | |
| P8 | `("heated tobacco"[Title] OR "heat-not-burn"[Title] OR IQOS[Title]) AND (humans[MeSH Terms])` | Nicotine_pubmed_P8.csv | |
| P9 | `(EVALI OR "vaping-associated lung injury" OR "e-cigarette, or vaping, product use-associated lung injury" OR "vitamin E acetate")` | Nicotine_pubmed_P9.csv | |
| P10 | `(nicotine[Title]) AND (pregnan*[Title] OR prenatal[Title] OR fetal[Title] OR neonat*[Title]) AND (humans[MeSH Terms])` | Nicotine_pubmed_P10.csv | |
| P11 | `(nicotine[Title]) AND (adolescent*[Title] OR "brain development"[Title] OR cognit*[Title]) AND (humans[MeSH Terms]) AND ("2010"[Date - Publication] : "3000"[Date - Publication])` | Nicotine_pubmed_P11.csv | |
| P12 | `(nicotine[Title] OR "e-liquid"[Title]) AND (poisoning OR overdose OR toxicity OR "lethal dose" OR ingestion) AND (humans[MeSH Terms])` | Nicotine_pubmed_P12.csv | |
| P13 | `("reduced nicotine"[Title] OR "very low nicotine"[Title] OR "nicotine reduction"[Title]) AND (cigarette* OR policy OR trial)` | Nicotine_pubmed_P13.csv | |
| P14 | `(nicotine[Title]) AND ("Parkinson" OR "Alzheimer" OR "cognitive impairment" OR schizophrenia OR "ulcerative colitis") AND (randomized controlled trial[Publication Type] OR clinical trial[Publication Type])` | Nicotine_pubmed_P14.csv | |

## Layer 3 — Cochrane Library (to be run by VS)

Search `nicotine OR smoking cessation` in Cochrane Reviews (Tobacco Addiction group); export the result list as CSV → `Nicotine_cochrane.csv`. Take the current `.pubN` of each of: CD010216 (electronic cigarettes), CD000146 (NRT versus control), CD006103 (nicotine receptor partial agonists), CD000031 (antidepressants), CD013308 (NRT doses, durations and modes of delivery), and the pregnancy review (Coleman et al.). Do not save protocols.

## Layer 4 — Snowballing (AI, after PDFs arrive)

Backward: reference lists of every Tier-A review (#1, #3, #9, #10, #18, #19, #23, #24, #25, #26). Forward: Google Scholar "cited by" on the landmarks — #1 (Benowitz 2009), #5 (Lerman 2006), #9 (the Cochrane e-cigarette review), #12 (the Soneji correction — the forward search here should specifically find papers that cite the uncorrected 2017 meta-analysis, which is a finding in its own right for the contested-questions box), #13 (Shahab 2020), #23 (Foulds 2003). The NASEM 2018 report and the current OHID vaping evidence update are both near-complete bibliographies of the e-cigarette literature to their dates and should be mined in the backward pass.

## PRISMA counts

To be completed after Layers 2–4: records identified per source; duplicates removed; screened; excluded with reasons; included.
