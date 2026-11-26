# Claim writer 765: report (round pdf-2026-11-26, question 23, what a drug screen can miss)

Files: `data/claims/_incoming/pdf1126_w765.json` (one new draft; schema-valid, GRADE arithmetic checked;
`check_anchor_numbers.py` finds all 33 anchor numbers on their pages), `765_simple.json`. No claim already answers the
question: the false-positive and detection-time answers leave misses out (their flag notes say so), and the touching-fentanyl
answer only mentions that responders' urine screens could not detect fentanyl. So a new claim, not a patch.

**23 `cl_gen_drug_test_misses`: very low, replicated, describes; draft (narrative reviews only).** Moeller et al. (2017)
carries it: panels (five US workplace drugs, benzodiazepines often added); morphine-calibrated opiate screens (no reaction to
fentanyl, methadone or buprenorphine; weak to oxycodone and others; some laboratories test these only on request); benzodiazepine
screens (lorazepam and alprazolam missed without an enzyme step most laboratories skip; clonazepam poor; cutoffs too high);
synthetic cannabinoids, cathinones, salvia; a negative means only "below the cutoff". Saitman et al. (2014) only names
clinically important false negatives for opiate and benzodiazepine screens, then leaves them out. Verstraete (2004) gives one
study in which immunoassays never detected a single dose of flunitrazepam that chromatography and mass spectrometry found.
Start low; risk of bias −1 (unsystematic reviews; cited studies undescribed), indirectness −1 (second-hand; unnamed "most"
screens; 2004–2017, Table 4 from 2008). Imprecision not rated: these papers hold no frequencies, which the statement says. The
test-accuracy rule would also give very low.

**Editor to decide:** status replicated (separate primary sources agree for benzodiazepines; two reviews for opiates) or single
study (fentanyl, methadone and buprenorphine rest on the 2017 review alone); and whether the flunitrazepam study, which the 2004
and 2017 reviews connect with drug-facilitated assault, stays in the How points (kept without its dose).

**Left out on purpose:** detection times; amounts (the 2017 review explains the benzodiazepine cutoffs by prescribed doses);
tampering; the half-life and fatal blood levels printed beside the cathinone sentences; remarks on people choosing drugs that
screens miss.

**Disagreements and dates.** The reviews agree in direction and cite different sources on misses (Moeller cites Verstraete only
for detection times); none is newer than 2017. Inside Moeller, the text lists hydrocodone and hydromorphone among opioids
opiate screens may miss, while Table 4 lists them among possible positives (said in the statement); it calls parent cathinones
easily detected in biological materials yet says attempts in urine failed (reported as printed).

**Missing papers:** Reisfield, Goldberger & Bertholf 2009 (Bioanalysis 1, 937–952) and Mikel et al. 2012 (Clin Chim Acta 413,
1199–1202), Saitman's sources; Keary et al. 2012 (doi:10.4088/PCC.12f01371, the only printed DOI); Wang et al. 2011 and
Melanson et al. 2012 (fentanyl, buprenorphine assays); Fraser & Meatherall 1996, 1998; West et al. 2010; Barnes et al. 2015;
Ellefsen et al. 2014; Kintz et al. 2002; Moeller, Lee & Kissack 2008 (Table 4's source).

**Cards against the PDFs.** `sc_moeller_2017`, finding on THCV: the adopted round-2 correction ("5 times per week, as printed";
"'At least' is not in the source") is wrong. The rendered PDF p. 7 prints "≥5 times per week" (the text layer drops ≥), so the
first pass was right. `sc_saitman_2014` does not record the review's two sentences on false negatives (PDF pp. 1, 4). No card
disagrees with a PDF on anything used. The fentanyl myth-or-fact statement reads at grade 6.3 because of drug names.
