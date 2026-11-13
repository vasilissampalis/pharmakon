# Batch 2, reader 6 — six methamphetamine primary studies read from the PDFs

First reading by AI reader 6 (PDFs), 2026-10-16. References built from Crossref through the app's browser
(`sekine_2001`, `harris_2003`, `mendelson_2006`, `schepers_2003`, `cook_1993`, `hart_2001`); six study cards in
`data/study-cards/_incoming/methamphetamine/`, all passing `check_card.py`; anchor proposals in
`reader6_patch.json` (dry-run clean, **not applied**); four new draft claims staged in
`data/claims/_incoming/methamphetamine_batch2.json`.

## The papers

**Sekine et al. (2001), pp. 1206–1214 — PET dopamine transporter, people who used only methamphetamine.**
Eleven men who had used methamphetamine and no other illicit drug (SCID-screened) and nine men who had not:
transporter binding potential was 20.2% lower in the caudate/putamen, 29.6% lower in the nucleus accumbens and
33.3% lower in the prefrontal cortex, all significant on Mann-Whitney tests. Within the methamphetamine group,
lower striatal and accumbens binding went with longer reported use and with higher BPRS positive-symptom scores.
The design limits are severe: the methamphetamine group came from three psychiatric services and 8 of 11 had
previously had methamphetamine psychosis, no dose or frequency was ever measured (only duration of use), nothing
was adjusted, and twenty-one or more tests were run at an uncorrected p<0.05. What it changes: `cl_meth_dat_lower`
no longer has to cite this study second-hand through Hart et al. (2012) — the primary numbers (20.2% and 29.6%,
with the selection of the sample) replace "about 20% ... as described by Hart et al., 2012". It also adds a fourth
cross-sectional null on abstinence to `cl_meth_dat_recovery`, and a primary number to the Parkinson's-disease
contrast in `cl_meth_dopamine_damage` (about 20% here against about 80% in unmedicated Parkinson's disease measured
by the same group with the same scanner and tracer).

**Harris et al. (2003), pp. 475–486 — bioavailability of intranasal and smoked methamphetamine.**
Eight men, balanced crossover of two conditions a week apart, each with a simultaneous 10 mg intravenous dose of
deuterium-labelled drug as the within-person reference. Absolute bioavailability was 79.4% (SD 13.1) intranasal and
37.4% (SD 14.2) of the amount placed in the device, or about 67% of the amount estimated to have left it, for the
smoked condition; terminal half-life was 10.7 hours by both extravascular routes and 11.0–11.8 hours intravenously;
clearance 272 mL·h⁻¹·kg⁻¹, steady-state volume of distribution about 4.2 L/kg; amphetamine's half-life was longer
(15–17 hours) at 15–19% of the parent AUC. Design limits: open administration, no placebo, unequal delivered doses
and an intravenous dose inside every session, which the authors say makes the between-route comparison of
physiological and subjective effects uninterpretable. What it changes: it is the primary source that replaces the
second-hand half-life in `cl_meth_pk_halflife`; it bounds the open question in `cl_meth_pk_intranasal_timecourse`
(the intranasal plasma peak is at about 2.7 hours, not later than the 3–4-hour samples of the two anchored studies,
and this is an independent laboratory); and it is the backbone of the new bioavailability-by-route claim.

**Cook et al. (1993), pp. 717–723 — smoked and intravenous pharmacokinetics.**
Six healthy men, each studied by both routes, with the amount taken up from the device measured by recovery.
Bioavailability 90.3% of the amount taken up; geometric mean half-life 11.1 hours (smoked) and 12.2 hours
(intravenous), individual values 8.3–18.2 hours; volume of distribution 3.2–3.7 L/kg; 37–45% of the dose excreted
unchanged, with renal clearance strongly dependent on urine pH (log clearance = −0.51 pH + 0.42 log flow + 4.58,
r² 0.688). Subjective and cardiovascular effects peaked at about 12–18 minutes and had subsided while plasma
concentrations were still high. Design limits: no placebo, no randomization or blinding, standard errors reported
throughout for n=6, and the subjective scale anchored to each man's own previous experience; the cardiovascular and
subjective data are partly reproduced from the group's own earlier paper on the same volunteers. What it changes: a
second independent half-life estimate for `cl_meth_pk_halflife`, the second (and incompatible-denominator)
bioavailability figure for the new route claim, and the only evidence behind the new acute-tolerance draft claim.

**Schepers et al. (2003), pp. 121–132 — oral sustained-release pharmacokinetics in plasma and oral fluid.**
Eight residential volunteers (four women) received four daily 10 mg doses and five of them, three weeks later, four
daily 20 mg doses of a sustained-release tablet formulation. Plasma half-life 9.3 and 11.1 hours (overall mean 10.0,
SD 5.2); time to peak 5.4 and 7.5 hours, which the authors show is a property of the slow-release preparation
(2.9–3.6 hours for other oral formulations); amphetamine about a fifth of the parent AUC; oral-fluid concentrations
higher than plasma but too variable to predict it (R² 0.222) and strongly dependent on the collection device and on
oral-fluid pH. Design limits: fixed dose order (low first, high three weeks later) with three of eight not reaching
the high dose, subject-blind only, physiological analyses on five people. What it changes: it adds the oral route to
`cl_meth_pk_halflife` and supplies the time-to-peak contrast that keeps the new bioavailability claim honest about
formulation.

**Mendelson et al. (2006), pp. 403–420 — the methamphetamine stereoisomers.**
Twelve men, six-session double-blind placebo-controlled Latin-square crossover with an enantioselective assay: the
strongest design among these six papers. l-Methamphetamine was eliminated more slowly (13.3–15.0 hours against
10.2–10.7) and converted to amphetamine four to seven times less; exposure to the two isomers was nearly equal when
given separately but not after the racemate (d/l AUC ratio 0.679, 90% CI 0.622–0.736). Acutely, conditions
containing d-methamphetamine raised blood pressure and positive ratings more and for longer (about 6 hours against
2–4), and the racemate behaved like d-methamphetamine; l-methamphetamine at the higher dose was not inert and drew
the same money valuation. Design limits: single intravenous doses, men only, 12 participants, about forty outcomes
without correction, blinding integrity untested. What it changes: it qualifies `cl_meth_pk_halflife` (the ~11-hour
figure belongs to the d-isomer) and it is the whole of the new stereoisomer claim, which nothing in the monograph
covered although which isomer is present depends on how a batch was made.

**Hart et al. (2001), pp. 75–81 — oral methamphetamine self-administration.**
Eight volunteers in a 20-day residential laboratory chose, on eight occasions per condition, between a capsule they
had sampled and a $1 voucher: a mean of 4.3 of 8 choices at 5 mg and 4.4 at 10 mg against 1.4 and 1.3 in the matched
placebo conditions, with no difference between the two doses. The 10 mg sample raised positive ratings and lowered
hunger and sedation ratings; measured daily food intake fell by about 43% (5 mg) and 37% (10 mg). Design limits:
eight people, only three of whom had ever used methamphetamine; a single $1 alternative; subjective ratings taken
only after the sample dose; three of eleven did not complete, one because of drug-related sleep difficulty; and the
reporting is thin (significant items only, F values without degrees of freedom, an unexplained P<0.03 threshold).
What it changes: it gives `cl_meth_choice_alternatives` a second study — from the same laboratory group, so
replicated by the same team, not independently — and a within-person double-blind drug-versus-placebo comparison
that the existing between-group money comparison does not have; and its food-intake data support a new claim on an
acute effect no claim covered.

## Reporting errors found (the ones that matter for citation)

1. **Cook 1993, abstract against Table 1.** The abstract gives mean residence times of 11.5 ± 0.5 h and 11.3 ± 1.74 h;
   Table 1 gives 16.7 ± 1.46 h (smoked) and 17.4 ± 2.15 h (intravenous), and AUMC/AUC from the same table reproduces
   the table values (16.9 and 17.2 h, editors' calculation). The abstract's figures are wrong by about five hours.
2. **Cook 1993, denominators.** The 90.3% bioavailability is computed against the amount taken up from the device, a
   qualification that appears only in the Results and Discussion. It is not comparable with the 37.4% that Harris et
   al. (2003) compute against the amount placed in the device. The claim text now carries the denominator with each
   figure.
3. **Schepers 2003, Table 1.** In the 20-mg oral-fluid block the Range column is displaced by one row: the half-life
   row has no range, the AUC row carries the half-life range (5.5–10.5), the volume-of-distribution row carries the
   AUC range (673.8–3891.0). Also, the model parameters appear twice with different values and units (Results:
   K01 = 1.07 h, K10 = 10.76 h; Discussion: K01 = 0.93 h⁻¹, K10 = 0.085 h⁻¹); only the Discussion values are
   consistent with the measured half-lives. Person-sessions are repeatedly called "individuals" (13 individuals from
   8 people), and Suzuki et al. is cited as reference 17, which is Cook et al. (1993).
4. **Mendelson 2006, abstract against Table II.** The abstract calls the peak subjective effects of 0.5 mg/kg
   l-methamphetamine "similar" to the same dose of d-methamphetamine and prints the value pairs in an order that
   reads as though the larger figure were the l-isomer's; Table II and the Results show the d-isomer significantly
   higher (intoxication 46.0 against 30.3; liking 47.7 against 28.6; P<.0001). The abstract also gives systolic
   blood-pressure changes in beats per minute. In Table I, the amphetamine peak after the racemate is printed as
   4.9 ± 1.8 with a 95% interval of 4.9–7.6, so the mean sits on its own lower bound. The Results say the l-isomer's
   AUC was "30% greater" than the d-isomer's after the racemate, while the printed ratio of 0.679 means about 47%
   greater (or the d-isomer 32% smaller).
5. **Harris 2003, abstract against tables.** The abstract's intravenous half-life (11.4 h), clearance, volume of
   distribution and mean residence time are averages of, or one of, the two tabulated condition values and appear in
   no row. Table I gives an intravenous time to peak of 3.55 ± 8.27 h for a 15-minute infusion, and the smoked
   time-to-peak difference is significant only after one outlier is excluded. λz is given units of L/h throughout
   (it is h⁻¹).
6. **Sekine 2001.** Every Kendall's tau is reported with "df=10"; a rank correlation has no degrees of freedom and
   n−2 would be 9. The text's mean age for the methamphetamine group (27.4, SD 5.6) does not match Table 1, whose
   eleven ages give 28.0, SD 5.7 (editors' calculation). Duration of use is treated in the discussion as a proxy for
   cumulative dose although no quantity of drug was measured.
7. **Hart 2001.** F values are printed without degrees of freedom anywhere in the paper; the significance threshold
   is an unexplained P<0.03; the food-intake percentages (−43% at 5 mg, −37% at 10 mg) run against the dose ordering
   of the subjective effects and cannot be reconciled with the discussion's single ~1415 kcal figure, because the
   absolute intakes are only in Figure 4; some placebo standard errors in Table 1 are implausibly small (for example
   "content" 30.80 ± 0.07 across 8 participants).

## Notes for the editor and the second reader

- **Metadata that Crossref gets wrong** (nothing was typed by hand; these need entries in
  `data/access/metadata-overrides.json`): `harris_2003` has only one author in Crossref ("Harris, D"), while the PDF
  title page lists six (Debra S. Harris, Harold Boxenbaum, E. Thomas Everhart, Gina Sequeira, John E. Mendelson,
  Reese T. Jones); `mendelson_2006` has all-capital surnames and "JACOBIII" for Peyton Jacob III; `hart_2001` drops
  the middle initials (the PDF gives Carl L. Hart, Amie S. Ward, Margaret Haney, Richard W. Foltin, Marian W.
  Fischman); `cook_1993` is registered under a re-issued Elsevier DOI (10.1016/s0090-9556(25)07478-1) although the
  1993 article is an ASPET publication, and the sentence-case rule lowercases the stereodescriptor in
  "S-(+)-methamphetamine".
- **`check_anchor_numbers.py` flags eleven numbers, all in Cook (1993)**: 11.1, 11.8, 13.1, 0.192, 18, 1.6 and 20.1.
  That PDF's text layer renders digits as letters ("I 1.8" for 11.8, "l3.lc" for 13.1, "0. 192", "20. 1"), so the
  mechanical check cannot match them. Each was confirmed by rasterizing the printed pages 719 and 720
  (`scratchpad/batch2/r6/img/cook_t1-3.png`, `cook_p720b-4.png`, `cook_p720f-4.png`). No other anchor was flagged.
- **The patch pushes five claims down the ladder**, as the protocol requires: `cl_meth_pk_intranasal_timecourse`,
  `cl_meth_dat_lower`, `cl_meth_dat_recovery`, `cl_meth_dopamine_damage` and `cl_meth_choice_alternatives` are
  `ai-anchored` today and return to `metadata-verified` until the new anchors are checked. `cl_meth_pk_halflife` moves
  the other way, from `draft` to `metadata-verified`, because it no longer rests only on a narrative review; that
  rung should be confirmed by the editor.
- **Two anchors are now superseded** and the patch cannot delete them: the `kish_2008` anchor on
  `cl_meth_pk_halflife` (a review citing a review) and the `hart_2012` p. 592 anchor on `cl_meth_dat_lower` (Sekine
  described second-hand). Both can be dropped by hand.
- **Open question on `relation`.** `cl_meth_pk_halflife` uses `is-associated-with`, which reads oddly for a measured
  pharmacokinetic parameter; the new pharmacokinetic claims follow it for consistency. If the senior author prefers
  `describes`, all three should change together, and §6.3's rule that descriptive claims are never upgraded for a
  large effect would then apply to them.
- **`cl_meth_choice_alternatives` may be worth splitting**, as the patch's GRADE note says: "an oral or intranasal
  methamphetamine dose is chosen over placebo" is now supported by a double-blind within-person comparison that would
  start high, while "a larger monetary alternative reduces drug choice" rests on a between-group comparison of 7 and
  6 people and stays very low.
- **Doses appear only as study conditions** in the cards and claims, and nothing is written about how to take the
  drug; the route-specific bioavailability claim is deliberately worded so that no figure can be read as a
  comparison of what one route "delivers" relative to another for the reader's own use. Section 7 remains the senior
  author's.
