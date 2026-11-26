# Claim writer 760: Suboxone (buprenorphine) with other opioids, and after stopping (items 14–16), 26 November 2026

All three PDFs read in full; every number used checked on rendered pages. Reader 741's arithmetic rechecked: all reproduces. Sections (not given in the brief): 3, 6, 12.

## Claims (`data/claims/_incoming/pdf1126_w760.json`)

**14. `cl_bup_other_opioids`.** Greenwald 2014 only: a narrative review of the authors' own studies (scans of 3, 5 and 10 people dependent on heroin, not in treatment; one modelling study, 7 against 8). Free receptors fell with dose (9–20% at 16 mg/day); heroin and hydromorphone were blunted, never blocked; after stopping 16 mg/day free receptors rose over 3 days. The abstract's thresholds appear as inferences, with the authors' words that blockade "has not been reliably observed". **Very low** (fixed-order designs start low; −1 risk of bias, −1 indirectness, −1 imprecision); draft (narrative-review rule); replicated by the same team. Left out: the abstract's dose translations; the mis-cited "earlier" Comer 2005 study. Missing (no DOIs printed): Zubieta et al. (2000), *Neuropsychopharmacology*, 23, 326–334; Greenwald et al. (2003), *Neuropsychopharmacology*, 28, 2000–2009; Greenwald et al. (2007), *Biological Psychiatry*, 61, 101–110; Comer et al. (2005), *Psychopharmacology*, 181, 664–675.

**15. `cl_bup_fentanyl_withdrawal`.** Varshneya 2022: 250 of 685 (36.5%) remembered severe withdrawal after buprenorphine following fentanyl, against 30 of 200 (15.0%) after methadone; by shortest wait 152/339 (44.8%) down to 5/37 (13.5%), no cut-off. The abstract's 22.19% is 152 of all 685. Odds ratios unadjusted against 37 people (the reconstructed counts are the only solution adding up to 250). **Very low** (survey; −1 each for risk of bias, indirectness, imprecision). Missing: D'Onofrio et al. (2023), doi 10.1001/jamanetworkopen.2023.6108 (supervised starts); Appendix 1.

**16. `cl_bup_after_stopping`.** Williams 2020: 464 of 8,996 (5.2 in 100) had a medically treated overdose within 6 months of stopping after 6–18 months; 41–49 in 100 an emergency visit. No group stayed on treatment; everyone who died or lost Medicaid excluded (30.5%); codes printed T36–T39, T40.5–T50 (opioid codes missing, as the card notes). **Very low** (descriptive, −1 for coverage and measurement). Linked to, and consistent with, `cl_opi_treatment_mortality` (deaths, not treated overdoses). Missing: online Table S1; Larochelle et al. (2018), *Annals of Internal Medicine*, 169, 137–145.

## Cards and records against the PDFs

- `sc_varshneya_2022` says the question wording is not given; Table 1's headings are phrased as questions (verbatim or not is unstated). Minor.
- `sc_greenwald_2014`, `sc_williams_2020`: no disagreement; their reporting issues confirmed.
- Reference records agree with the PDFs.

## For the editor

- No timing appears as advice. The time course after stopping is in the claim, its plain paragraph and one How point, as the brief asks; the short line says the hold "faded slowly over 3 days of scans". Please judge whether that belongs in the short line.
- A card "Suboxone completely blocks other opioids" was drafted and dropped: it describes what a mixture does, not a risk.
- Item 16: low instead of very low if the exclusions are read as part of the population as worded.
- Plain lines: `760_simple.json`.
