# Section 7 answers that the reset of 13 November took back to older versions (found 27 November 2026, 01:00 Athens)

The senior author's to-do page of 13 November (kept in `data/verification/s7-review-2026-11-13/s7_on_todo_page.json`) shows
the plain lines of 46 section 7 answers. For 16 of them the claim files now hold an older version than the one those lines
were written for, and one answer is gone altogether: the reset of 13 November wiped the newest versions (section 7 answers
were not on the published site, so the recovery took them from the 6 November snapshot). Writers 791 to 794 flagged the
gaps on 27 November while writing new plain lines for the current versions.

## What was compared

For each answer, the lines on his page against the current claim and its sources (`scratchpad/regressed.txt` of the night
of 27 November; rebuild it with the snippet at the end of this file).

- **Same sources, smaller refinements lost (14 answers):** cl_alc_water_dehydration (0.1.4 lost; now 0.1.3),
  cl_pop_eye_stopping (0.1.3 / 0.1.2), cl_benzo_own_practices (0.2.4 / 0.2.3), cl_can_smoked_cancer (0.5.3 / 0.5.2),
  cl_can_evali (0.3.1 / 0.3.0), cl_can_vaped_lungs (0.4.2 / 0.4.1), cl_can_edibles (0.5.1 / 0.5.0), cl_nic_nrt_forms
  (0.2.2 / 0.2.1), cl_nic_vapes_stopping (0.1.3 / 0.1.2), cl_nic_vapes_exposure (0.2.1 / 0.2.0), cl_nic_snus (0.4.0 /
  0.3.1), cl_nic_vapes_relative_risk (0.6.0 / 0.5.2), cl_alc_protective_strategies (0.7.1 / 0.5.0), and
  cl_mdma_preloading_practices (0.2.3 / 0.1.1). Every source the lost lines name is still cited by the current claim, and
  every anchor of the current claim is checked. The current versions stand: their new plain lines (writers 791 to 794) were
  blind-checked (795 to 798) and go to him for approval as they are. Nothing more to rebuild.
- **New sources lost with the newest version (2 answers), to rebuild from papers already in his folder:**
  - `cl_can_smoked_vs_vaped` (0.6.1 lost; now 0.2.1, one trial): the lost version added a second trial and two machine
    studies: Abrams et al. (2007) `PDFs/Cannabis/Abrams_2007_VaporizationVsSmoking.pdf`, Gieringer et al. (2004)
    `PDFs/Cannabis/Gieringer_2004_VaporizerTHCDelivery.pdf`, Lanz et al. (2016) `PDFs/Cannabis/Lanz_2016_VaporizerDelivery.pdf`
    (his folder also holds `Cannabis/Lanz_2016_S1Table.pdf`). Their reference records survived; their study cards did not.
  - `cl_can_edibles_labels` (0.4.1 lost; now 0.1.0, the 2014 test only): the lost version added the Colorado test of
    2023 to 2024: Limbacher et al. (2026) `PDFs/Cannabis/Limbacher_2026_ProductLabelTesting.pdf` (and `Limbacher_2026_S1Fig.pdf`,
    the supplementary chart the lost lines cite: "at least 7 of the 29 fell short"). Reference record survived; card did not.
- **An answer lost altogether (1):** `cl_alc_hangover_cures` (0.3.1, "Do any hangover cures work?"), from Roberts et al.
  (2022) `PDFs/Alcohol/Roberts_2022_HangoverRemediesSR.pdf`. Reference record survived; claim and card did not.

## To do when his computer is connected (the bridge was off on the night of 27 November)

1. Stage the five PDFs (and the two supplements) into the session (`device_stage_files`), never into the repository.
2. First readers write study cards for the five papers (`docs/VERIFICATION-BRIEF.md`, step 1).
3. Claim writers: revision patches for cl_can_smoked_vs_vaped and cl_can_edibles_labels (`scripts/claim_patch.py`), and
   cl_alc_hangover_cures written again as a new claim; each from the papers, with the lost lines as a guide to what was
   there, never as a source.
4. Round-2 readers check the new anchors and cards; the editor adjudicates and merges; plain lines; blind check.
5. The three go to his to-do page for approval (section 7), each saying what came back.

## Rebuilding the comparison

```python
import json, re, glob
D = json.load(open("data/verification/s7-review-2026-11-13/s7_on_todo_page.json"))["items"]
C = {c["id"]: c for f in glob.glob("data/claims/*.json") for c in json.load(open(f))}
key = lambda x: tuple(int(p) for p in x.split("."))
for it in D:
    c = C.get(it["id"])
    if not c: print("gone:", it["id"], it["v"]); continue
    if key(it["v"]) > key(c["version"]): print(it["id"], "lost", it["v"], "now", c["version"])
```
