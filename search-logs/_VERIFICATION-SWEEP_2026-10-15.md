# Independent DOI verification sweep — 15 October 2026

Run by the lead co-editor (AI) over every DOI in every evidence map then completed (Methamphetamine, Alcohol, Cannabis, Ketamine, PCP, Synthetic-cannabinoids, _Interactions), independently of the checks the individual co-editors recorded in their own verification blocks.

**Method.** Each distinct DOI was fetched from the Crossref REST API (`api.crossref.org/works/<DOI>`), one request every ~0.3 s, from a different network route than the co-editors used. For each record: resolution, first author (family name), print-issue year (online year if no print), title, and the `updated-by` field (Crossref's retraction, correction and erratum links, including Retraction Watch data). The list's own first-author surname and year were then compared with Crossref's.

**Results.**

| Check | Result |
|---|---|
| Distinct DOIs | 609 |
| Resolved in Crossref | 609 (100%) |
| Retracted | **0** |
| Errata / corrections linked | 12 (all already marked in their lists) |
| First-author or year mismatch | 4 flagged, all explained (below) |

**Errata and corrections linked in Crossref** (obtain the notice with the paper):
Wood 2018 (Lancet) · Bryazka 2022 (Lancet) · Degenhardt 2018 (Lancet Psychiatry) · Black 2019 (Lancet Psychiatry) · Lee 2018 (Drug Alcohol Depend) · Bahji 2021 (J Affect Disord) · Pasman 2018 (Nat Neurosci) · Mewton 2023 (Addiction) · Morgan 2010 (Addiction) · Henderson 2007 (BJOG) · Zanos 2018 (Pharmacol Rev) · Horowitz 2021 (Br J Psychiatry).

**The four flags.**
1. `10.1038/s41593-018-0206-1` — Crossref lists a group author ("the 23andMe Research Team") first; the paper is Pasman et al. (2018), GWAS of lifetime cannabis use. Correct as listed.
2. `10.1007/s00787-022-01994-9` — O'Grady et al.: online 2022, print issue 2024. Corrected in the Cannabis list to "2024 (online 2022)" (METHODS §4.2: the citation year is the print-issue year).
3. `10.1177/0269881108098612` — Dickerson et al.: online 2008, print issue 2010. Corrected in the Ketamine list to "2010 (online 2008)"; filename now `Dickerson_2010_EthanolLikeEffects.pdf`.
4. `10.1159/000166498` — Akmal et al. (1981): Crossref's 2008 date is the digitisation date. Correct as listed.

**Conclusion.** No listed DOI points to the wrong paper; none is retracted. The lists completed so far are safe to retrieve from. The same sweep will be run on each further list as it lands.
