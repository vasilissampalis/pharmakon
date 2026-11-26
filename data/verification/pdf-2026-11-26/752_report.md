# Claim writer 752 (round pdf-2026-11-26): who gets addicted, and who recovers

Files: `data/claims/_incoming/pdf1126_w752.json` (two drafts), `patch_pdf1126_w752.json` (cl_gen_remission 0.4.3 → 0.5.0;
dry run passes, not applied), `752_simple.json`. Every number was checked on its PDF page.

## cl_gen_most_users_not_addicted: low, single study
Lopez-Quintero et al. (2011, version of record): projected lifetime chance of DSM-IV dependence 8.9% cannabis, 20.9%
cocaine, 22.7% alcohol, 67.5% nicotine; timing figures; predictors. Not downgraded:
recall, projection without intervals and excluded institutions mostly lower the figures and cannot make dependence the
usual outcome. Strict reading: the nicotine projection and timing figures alone are very low. Hart (2017, 2020) only for
what he argues; his 70–90% (cited to his book) is named as unsourced, never used as a figure. No figure here for heroin
or methamphetamine; Anthony et al. (1994), already on the site, could add heroin.

## cl_gen_remission (patch): very low, unchanged
Adds Heyman (2013): 76/83/81% (57% under a stricter rule) of people ever drug-dependent not dependent in the past year
(his calculations); remission is not quitting and was counted drug by drug in the curves; times to remission by drug
(no heroin); treatment uncommon. Adds Robins (1993): 5% re-addicted in the first year, 12% within 3 years; little
treatment. Recovery without treatment is still counted directly only for alcohol. Proposed pages add cocaine, cannabis
and nicotine; my myth-or-fact items replace the two at 0.4.3.

Heyman's treated/untreated figure is not repeated: Robins (pp. 1045–1046) gives 6% as the share of men urine-positive at
departure who entered treatment (not of men dependent at departure), two-thirds of treated men relapsed by the
interview (not a one-year rate), and 12% as the 3-year re-addiction of all men addicted in Vietnam, treated men
included. Groups and time spans are mixed, and the treated selected themselves.

## cl_opi_vietnam_veterans: low, single study
Robins (1993) with Robins et al. (1975), one cohort counted once; lecture-only figures are very low strictly read.
6% against 12%: the text's "6% overall" (p. 1046) has no time frame; Figure 6 (p. 1049), measured at 300 dpi, shows
12.0–12.1% re-addicted in every bar, matching the 3-year 12% (p. 1045), which I used. Robins's caution (p. 1051) is in
the But line.

## Disagreements with the PDFs
- sc_lopez_quintero_2011: "likely underestimated" is an inference; p. 128 says only that excluded institutionalized
  people more often have a dependence diagnosis. Fig. 1 prints "7.0" for 70 (p. 125).
- sc_robins_1993: Fig. 6 regular use measures 23% (card 24%). Lecture 45% tried narcotics, 96% interviewed; the 1975
  paper 43% (general sample), 95%. Text "nearly half" used again; Fig. 6 about 61%.
- Heyman, Hart and all six reference records agree with the PDFs.

## Not read (could change figures)
Lopez-Quintero et al. 2011, Addiction 106:657–669 (Heyman's curves; DOI not printed); Moos & Finney 2011, Addiction
106:670–671; Robins, Davis & Nurco 1974 (the 5%); Robins et al. 1980 (3-year report); Price et al. 2001; Compton et al.
2010, Am J Psychiatry 167:473–474; Wagner & Anthony 2002.

validate.py will warn on "addicted" (the sources' word; nobody is labelled).
