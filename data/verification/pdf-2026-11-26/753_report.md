# Reader 753 (claim writer): peeing on MDMA; the rat study behind "a new place" (items 4–5), 26 November 2026

Scans read on rendered pages, figures on 300-dpi crops. Arithmetic: `753_calculations.py`.

## Claims

**4. `cl_mdma_peeing`** (new, draft, section 5). Bryden 1995: one case of acute retention (24 hours; catheter 36 hours;
15 tablets in 36 hours by his own account; no toxicology, tablet analysis or bladder measurement; the alpha-adrenergic
account is reasoning). Henry 1998: vasopressin rose in 8 men (3 untreated occasions, not compared; no urine). Baggott
2016: 16 + 12 people against placebo, no rise in ADH or copeptin (prazosin did raise ADH); sodium fell, further after
20 mL/kg water; one woman 127 mmol/L; urine collected, no result reported. Hysek 2014: copeptin unchanged in 32.
**Very low**: starts low (one case on the outcome), risk of bias −2, indirectness −1, imprecision −1; insufficient
evidence; single study. Links the low-blood-salt answer once.

**5. `cl_opi_conditioned_tolerance`** (patch 0.1.2 → 0.2.0; dry run passes). Siegel 1982 added as four animal-study
anchors: both settings familiar to every rat (heroin-paired, dextrose-paired), so a cue-paired place, not a new place;
death the only outcome. **Counts checked**: each percentage fits one whole number only (12/37, 27/42, 27/28). **Printed
DT–ST P < .001 does not reproduce**: χ² 7.98, p = 0.005 (Fisher 0.007). The other p values reproduce; "P < .02" for six of
six replications holds one-sided only (0.016). Human evidence unchanged. **Very low**, single study. The live
myth-or-fact items (heroin, general) say rats died more "in a new place"; `753_simple.json` replaces both.

## Cards and records against the PDFs

- `sc_siegel_1982`: Katz interval "roughly 1.17 to 3.37"; recomputed 1.18 to 3.32. The paper has no headings: my
  locators count paragraphs from the first after the abstract.
- `sc_baggott_2016`: figure readings confirmed (about 133.6 against 137.7 mmol/L at 3 h). Not on the card: Study 1 drank
  1213 ± 76 mL in 8 h, not differing by condition; hyponatremia is defined as < 135, yet only the 127 value is called low,
  while Figure 5 shows other values below 135 after MDMA and placebo. The Introduction credits Henry with a rise in urine
  osmolality [21–24]; Henry measured no urine, so it must come from refs 22–24 (unread).
- `sc_bryden_1995`, `sc_henry_1998`, `sc_hysek_2014`: no disagreement. Record `bryden_1995`: page "504.2", printed 504.

## Missing (no DOIs printed)

No study recording passing urine after MDMA is on file. Closest: Wolff et al. (2006, J Psychopharmacol 20, 400–410; urine
osmolality in clubbers); Forsling et al. (2001, J Pharm Pharmacol 53, 1357–1363); also Simmler et al. (2011, J Clin
Endocrinol Metab 96, 2844–2850), Greer & Tolbert (1986). New place: Siegel, Hinson & Krank (1979, Behav Neural Biol 25,
257); Ferguson & Mitchell (1969, Clin Pharmacol Ther 10, 372; tolerance with unfamiliar cues in people, as cited).

## For the editor

- `cl_mdma_hyponatremia`'s flag note waits for Baggott 2016, now read: revisit its vasopressin sentence.
- `cl_mdma_kidney` mentions bladder-neck obstruction (second-hand): cross-link?
- Section 5 or 6 for `cl_mdma_peeing`.
