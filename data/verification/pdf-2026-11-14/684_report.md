# Claim writer 684: report (round pdf-2026-11-14, questions 11–13)

Files: `data/claims/_incoming/pdf1114_w684.json`, `data/claims/_incoming/patch_pdf1114_w684.json` (dry run
passes, not applied), `data/verification/pdf-2026-11-14/684_simple.json`. All numbers are from the PDFs (figures rendered;
Brunt's Figures 7–8 measured by pixel).

## 11. cl_fent_fake_pills: very low, replicated

Rests on Palamar 2022 (seizure records) and O'Donnell 2023 (death records); Tupper 2018 only as a qualifier (very few pills
tested, no results by form). Descriptive: starts low, −1 for risk of bias (reporting coverage and testing undescribed;
seizures follow policing; counterfeit evidence coded from narratives, undercounted, perhaps documented more fully over time).
Denominators stated: 13.8% to 29.2% is the pills' share of pill-plus-powder fentanyl seizures; both trends compare first and
last quarters, with the mid-2021 peaks said. "Replicated" means two independent record systems agree in direction only; the
editor may prefer single-study. Would change it: a study testing street pills. Not read: the DEA laboratory statements
Palamar cites (no DOI), Green & Gilbert 2016 (10.1001/jamainternmed.2016.4310), Daniulaityte et al. 2022
(10.1186/s12954-022-00634-4).

## 12. cl_opi_overdose_recognition: very low, single study

Rests on Green 2008. Observational, −1 for risk of bias (groups picked by staff, no pre-training scores, unpublished
scenarios, answer key partly set by programme staff). The claim says: no results by scenario or sign; trained people still
did not choose naloxone in about 2 of 9 opioid scenarios; the printed 85.2% and 68.3% do not match the means (73.6% and
59.2%); kappa 1.0 cannot describe individuals; the cost and causal conclusions are unsupported. No signs or steps are
listed; "heavy nod" appears only as a training topic and a limit. Not read: the scenario validation abstract (Green, Grau &
Heimer 2006) and the scenario source (Green et al. 2003, J Drug Issues 33, 713); no DOIs printed.

## 13. Patch cl_mdma_pill_content: very low (unchanged), replicated

Adds Brunt 2017 (five anchors), so the claim no longer rests only on a narrative review. "Doubled" holds only for the
Netherlands (Figure 8: about 61 to 113 mg; elsewhere 1.4–1.6 times), and the claim says so. Brunt calls logo recognition
reliable without data and does not say whether logo-identified tablets are in its figures; whether a logo tells you what is
inside needs Vogels et al. (2009, Addiction 104, 2057) and Brunt & Niesink (2011, Drug Testing and Analysis 3, 621), not on
file. The senior author approved version 0.1.2; `claim_patch.py` does not reset a draft's review, so please mark it
pending.

## Cards and records against the PDFs

- sc_brunt_2017: I read Figure 8's Netherlands rise as about 1.8–1.9 times (card: up to 1.8; its 2013 marker is partly
  hidden) and Figure 7's Spain 2013 as about 61% (card 62%). Both approximate.
- sc_green_2008: two effect-size intervals differ from my recomputation by 0.01 (not used).
- None with the Palamar, O'Donnell or Tupper cards.
- References: Green's (103(6), 979–989) and Brunt's (9(2), 188–198) printed pages cannot be checked from the online-first
  PDFs; the other records match.

## Plain lines

Three myth-or-fact statements read slightly above grade 6 because of "opioid overdose" and "oxycodone".
