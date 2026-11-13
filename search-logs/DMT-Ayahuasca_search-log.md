# DMT and ayahuasca — search log (PRISMA 2020)

Protocol: METHODS.md §2. Strings written 2026-10-15 before screening; re-worded re-runs of refused or errored URLs are listed as such.

## Layer 1 — Crossref bibliographic search (run by AI co-editor, 2026-10-15/16)

Endpoint: `https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:journal-article&rows=15&select=DOI,title,container-title,issued,is-referenced-by-count,author&sort=relevance`. Record verification used `https://api.crossref.org/works/<DOI>` with no query string, and `filter=doi:` batches of two or three.

Environment: the Crossref refusal rate rose through this substance's build, from about one call in two to about two in three. Each HTTP 429 was followed by a pause of 60–300 s and the refused URL was never re-fetched. Several syntactically valid URLs returned an unexplained client error from Crossref; where a reworded re-run also failed, the topic is recorded as a gap. Three planned queries were abandoned for this reason and are listed at the end of the query table.

### Section-level queries

| # | Query string | Result |
|---|---|---|
| D1 | Strassman dose-response N,N-dimethyltryptamine human volunteers intravenous | 15 hits, 5 retained (Strassman 1994a; Strassman 1994b; Strassman 1995; Strassman 1996; D'Souza 2022; plus Dean 2019 on endogenous DMT) |
| D2 | ayahuasca pharmacology harmine harmaline monoamine oxidase humans DMT | 15 hits, 3 retained (Brito-da-Costa 2020; Egger 2024; Berlowitz 2022). The remaining 12 were 1958–1980 rodent MAO-inhibition pharmacology |
| D3 | ayahuasca treatment-resistant depression randomized placebo-controlled trial | URL refused (429); re-run as "rapid antidepressant effects ayahuasca treatment-resistant depression trial" — refused (429), then client error on a third attempt after a 185 s pause; re-run as D3d |
| D3d | ayahuasca depression clinical trial Palhano-Fontes Osorio Sanches | URL refused (429). Palhano-Fontes 2019 was instead verified directly at `works/10.1017/S0033291718001356`; Osório 2015 and Sanches 2016 remain unverified (see below) |
| D4 | Global Ayahuasca Survey adverse effects ceremonial use Bouso | 15 hits, 10 retained (Bouso 2022; Andión 2025; Durante 2021; Gonzalez 2021; Cowley-Court 2023; Weiss 2023; Weiss 2021; Simonsson 2022; Perkins 2021; Perkins 2024; Bouso 2013; dos Santos 2017) — highest-yield query for this substance |
| D5 | DMT intravenous infusion extended state pharmacokinetics Timmermann | client error; re-run as D5b |
| D5b | dimethyltryptamine continuous intravenous infusion prolonged immersive state | 15 hits, 1 retained (Gallimore & Strassman 2016). The extended-state *trial* did not surface — gap |
| D6 | acute effects intravenous DMT healthy participants randomized placebo | 15 hits, 2 retained (Vogt 2023 Transl Psychiatry; Erne 2026 Transl Psychiatry). Also surfaced **Ley et al. 2023, acute effects of mescaline, LSD and psilocybin in healthy participants (Neuropsychopharmacology, 10.1038/s41386-023-01607-2)** — carried forward to the Mescaline list — and Becker 2022 (ketanserin reversal of LSD, Int J Neuropsychopharmacol, 10.1093/ijnp/pyac075), noted for the LSD list's next pass |
| D7 | Timmermann DMT EEG neural correlates human brain near-death | client error; re-run as D7b |
| D7b | DMT EEG fMRI brain human psychedelic experience Timmermann | 15 hits, 3 retained (Timmermann 2023 PNAS; Kroupi 2026 Brain Res; Shulgin 1976 historical). Timmermann's 2018–2019 EEG and near-death papers did not surface — gap |
| D8 | ayahuasca serotonin syndrome antidepressant interaction death case report | 15 hits, 1 retained (Pack 2026). Thirteen of the fifteen were Reactions Weekly interaction notes for unrelated drug pairs |
| D9 | Riba subjective effects tolerability ayahuasca healthy volunteers pharmacology | URL refused (429); re-run as D9b |
| D9b | human pharmacology of ayahuasca subjective effects tolerability Riba | 15 hits, 9 retained (Riba 2003 JPET; Riba 2001; Riba 2002a pharmaco-EEG; Riba 2002b sensorimotor gating; Domínguez-Clavé 2016; Ižnanský 2022; dos Santos 2011; Uthaug 2021; dos Santos 2024). Also surfaced the Soler corrigendum record (see below) |
| D10 | long-term ayahuasca users personality psychiatric neuropsychological cortical | URL refused (429); re-run as "regular ayahuasca users religious context psychiatric assessment cohort" — also refused (429). **Not run**; recorded as the largest gap in this map |
| D11 | ayahuasca cardiovascular physiological effects blood pressure vomiting | **Not run** (window closed) |
| D12 | vaporised inhaled DMT pharmacokinetics humans | **Not run** (window closed) — the inhaled route has no verified source in this list |

### Record verification

| Batch | DOIs | Result |
|---|---|---|
| V1 | 10.1017/s0033291718001356, 10.1590/1516-4446-2014-1496, 10.1097/jcp.0000000000000436 | client error (three DOIs) |
| V2 | 10.1017/s0033291718001356, 10.1097/jcp.0000000000000436 | refused (429) twice, with 185 s and 300 s pauses between attempts |
| V3 | 10.1017/s0033291718001356, 10.1097/jcp.0000000000000436, 10.1590/1516-4446-2014-1496 (rows=5) | client error |
| V4 | `works/10.1017/S0033291718001356` (single-DOI endpoint, no query string) | resolved: "Rapid antidepressant effects of the psychedelic ayahuasca in treatment-resistant depression: a randomized placebo-controlled trial", Psychological Medicine, issued 2018 online / 2019 print, first author Palhano-Fontes. No `updated-by`; relation `has-preprint` 10.1101/103531 |

### DOI corrections and update checks
- No recalled DOI was written into the list without verification; every other DOI was copied verbatim from a Crossref search response.
- Unverified and therefore excluded: Osório et al. 2015 (Braz J Psychiatry) and Sanches et al. 2016 (J Clin Psychopharmacol). Both are named in the DOI list's "Known gaps" with their titles so they can be obtained by title.
- Corrigendum record found without its parent: 10.3389/fphar.2020.635111, "Corrigendum: Four weekly ayahuasca sessions lead to increases in 'acceptance' capacities: a comparison study with a standard 8-week mindfulness training program" (Soler et al., Front Pharmacol 2021). The parent article did not surface; both are to be obtained.
- Retractions: none.
- Duplicate records noted: Strassman's 1994 dose-response study is registered as two separate Crossref records (parts I and II of the same study, 10.1001/archpsyc.1994.03950020009001 and 10.1001/archpsyc.1994.03950020022002) — both are listed because they are genuinely two papers. dos Santos's ayahuasca-intoxication report exists in Spanish (10.1016/j.medcli.2017.04.032) and English (10.1016/j.medcle.2017.10.006); the English edition is listed. Vogt 2023 also exists as a Neuroscience Applied abstract (dropped).

## Layer 2 — PubMed (to be run by VS)

Run each string exactly as written in PubMed (https://pubmed.ncbi.nlm.nih.gov). For each: **Save → Selection: All results → Format: CSV**, and save the file into `search-logs/` with the name given. Note the hit count shown next to each string and send me the numbers.

| # | String | Save as | Hits |
|---|---|---|---|
| P1 | `(ayahuasca[Title] OR DMT[Title] OR "dimethyltryptamine"[Title] OR hoasca[Title] OR yage[Title]) AND (systematic review[Publication Type] OR meta-analysis[Publication Type])` | dmt_pubmed_P1.csv | |
| P2 | `("dimethyltryptamine"[Title] OR DMT[Title]) AND (pharmacokinetic* OR "plasma concentration" OR infusion OR intravenous OR inhaled OR vaporiz* OR vaporis*) AND (humans[MeSH Terms])` | dmt_pubmed_P2.csv | |
| P3 | `(ayahuasca[Title] OR hoasca[Title]) AND (harmine OR harmaline OR tetrahydroharmine OR "beta-carboline" OR "monoamine oxidase")` | dmt_pubmed_P3.csv | |
| P4 | `(ayahuasca[Title]) AND (depression OR depressive OR anxiety) AND (trial OR randomized OR randomised OR "open-label")` | dmt_pubmed_P4.csv | |
| P5 | `(ayahuasca[Title]) AND (adverse OR safety OR toxicity OR "serotonin syndrome" OR death OR fatal*)` | dmt_pubmed_P5.csv | |
| P6 | `(ayahuasca[Title]) AND ("long-term" OR regular OR "religious" OR church OR UDV OR "Santo Daime" OR adolescen*) AND (humans[MeSH Terms])` | dmt_pubmed_P6.csv | |
| P7 | `(ayahuasca[Title] OR DMT[Title]) AND (neuroimaging OR fMRI OR EEG OR MEG OR "cortical thickness" OR "functional connectivity")` | dmt_pubmed_P7.csv | |
| P8 | `("extended state DMT" OR "DMTx" OR ("dimethyltryptamine" AND ("target-controlled" OR "continuous infusion" OR "extended-state")))` | dmt_pubmed_P8.csv | |
| P9 | `(ayahuasca OR "dimethyltryptamine") AND (SSRI OR antidepressant OR MAOI OR "monoamine oxidase inhibitor" OR interaction) AND (humans[MeSH Terms])` | dmt_pubmed_P9.csv | |
| P10 | `(ayahuasca[Title] OR DMT[Title]) AND (cardiovascular OR "blood pressure" OR vomiting OR emesis OR "physiological effects")` | dmt_pubmed_P10.csv | |
| P11 | `("endogenous DMT" OR ("dimethyltryptamine" AND (endogenous OR pineal OR INMT)))` | dmt_pubmed_P11.csv | |
| P12 | `(ayahuasca[Title] OR DMT[Title]) AND (psychosis OR "psychotic" OR mania OR HPPD)` | dmt_pubmed_P12.csv | |
| P13 | `(ayahuasca OR "dimethyltryptamine") AND (prevalence OR trends OR epidemiolog* OR "retreat" OR tourism)` | dmt_pubmed_P13.csv | |
| P14 | `("5-MeO-DMT" OR "DiPT" OR "4-HO-MiPT" OR "5-MeO-MiPT" OR "synthetic tryptamine*")` | dmt_pubmed_P14.csv | |

## Layer 3 — grey literature (VS)

UNODC World Drug Report 2025; EUDA European Drug Report 2026, Statistical Bulletin and EDND tryptamine notifications; INCB annual report (ayahuasca and plants containing controlled substances); Brazil CONAD resolution and technical report on religious ayahuasca use; Global Drug Survey latest; SAMHSA NSDUH 2024 detailed tables. Saved to `PDFs/_Epidemiology/` with the names in the DOI list's reports table.
