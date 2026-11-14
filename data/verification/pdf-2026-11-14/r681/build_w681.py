# Builder for claim writer 681 (round pdf-2026-11-14). Writes the incoming claims file and the plain lines.
# Run: python3 -I build_w681.py  (paths are absolute; nothing is read from the PDFs here)
import json, re, sys

ROOT = "/home/claude/pharmakon"
TODAY = "2026-11-14"
ME = "AI reader 681 (claim writer)"
LOC = ME + ", from the PDF"

SRC_T = ("PDF PDFs/_Cross-cutting/Timmermann_2021_PsychedelicsMetaphysicalBeliefs.pdf.pdf (version of record, Scientific "
         "Reports 11, article 22166, pp. 1–13; text layer read in full; pp. 3–6 with Figures 1–5 checked on pages rendered at "
         "150 dpi; Supplementary Information not on file)")
SRC_N = ("PDF PDFs/_Cross-cutting/Nayak_2022_BeliefChangeConsciousness.pdf.pdf (version of record, Frontiers in Psychology 13, "
         "article 852248, pp. 1–8; text layer read in full; pp. 4–6 with Tables 1–3 and Figures 1–2 checked on pages rendered "
         "at 150 dpi; Supplementary Material not on file)")
SRC_M = ("PDF PDFs/Psilocybin/MacLean_2011_PsilocybinOpenness.pdf (version of record, Journal of Psychopharmacology 25(11), "
         "pp. 1453–1461; text layer read in full; pp. 1455–1458 rendered at 150 dpi and Figure 1 at 300 dpi)")
SRC_E = ("PDF PDFs/Psilocybin/Erritzoe_2018_PsilocybinPersonality.pdf.pdf (version of record, Acta Psychiatrica Scandinavica "
         "138(5), pp. 368–378; text layer read in full; pp. 370–371 with Table 1 and the Cohen's d formula checked on pages "
         "rendered at 150 dpi)")
SRC_B = ("PDF PDFs/_Cross-cutting/Bressloff_2001_GeometricHallucinationsCortex.pdf (version of record, JSTOR scan, Philosophical "
         "Transactions of the Royal Society of London B 356(1407), pp. 299–330; the first PDF page is a JSTOR cover, so printed "
         "p. 299 is PDF page 2; the OCR text layer is imperfect, so every number used here was read on pages rendered at 150 dpi: "
         "pp. 299–301, 303–305, 317, 323–326; the mathematical sections were read for their conclusions)")
SRC_G = ("Study card sc_griffiths_2006 (ai-checked: round-2 check by AI reader 540, adjudication by AI reader 565); the PDF "
         "named in the reference record, PDFs/Psilocybin/Griffiths_2006_MysticalExperience.pdf, is not on file on 14 November 2026")
LOC_G = ME + ", from the study card sc_griffiths_2006"


def anchor(ref, card, page, locator, extracted, role, src, located_by=LOC):
    return {"reference": ref, "study_card": card, "page": page, "locator": locator, "extracted": extracted, "role": role,
            "anchor_status": "ai-located", "located_by": located_by, "located_on": TODAY, "source_read": src}


def verification(note):
    return {"status": "draft", "drafted_by": ME, "drafted_on": TODAY, "flag_note": note}


def changelog(papers):
    return [{"version": "0.1.0", "date": TODAY,
             "change": "Drafted by " + ME + " from the PDFs of " + papers + ", round pdf-2026-11-14; anchors ai-located; staged "
                       "in data/claims/_incoming/pdf1114_w681.json."}]


# ---------------------------------------------------------------------------------------------------------------
# 1. Beliefs about reality and consciousness
# ---------------------------------------------------------------------------------------------------------------
c1 = {
 "id": "cl_xc_psychedelic_beliefs",
 "substance": "psilocybin",
 "section": 5,
 "statement": (
  "In adults who chose to attend a ceremony, retreat or other guided session with a classic psychedelic and signed up for "
  "online surveys (mostly from Western countries, highly educated, and already leaning towards non-physicalist views "
  "beforehand), attending, compared with their own answers about a week before, is associated with modestly stronger "
  "agreement with non-physicalist statements 4 weeks and 6 months later; in one randomized trial in depression the shift "
  "after psilocybin therapy exceeded the shift after escitalopram only on a one-tailed test; and none of the studies tests "
  "whether the beliefs are true. On a questionnaire written for the study, whose main factor groups belief in other realms "
  "that can be visited, a unifying principle beyond scientific explanation, panpsychism (mind as a quality of all things), "
  "dualism and idealism against materialism and naturalism (Timmermann et al., 2021), the 122 respondents with answers at all "
  "three time points (819 in the baseline table and 866 said to have answered at some time point, so about 85 in 100 are "
  "missing from these analyses and were not compared with those who stayed) shifted by d = 0.33 at 4 weeks and d = 0.46 at "
  "6 months, and the 53 taking a psychedelic for the first time by d = 0.53 and 0.73; belief in fatalistic determinism rose at "
  "4 weeks (d = 0.25) but not at 6 months. Positions moved both ways: of respondents classed as 'hard materialists' at "
  "baseline, 24.4% still held that position at 4 weeks and 22.2% at 6 months, most of the others moving to a mixed position "
  "or to dualism, while 17.6% and 15.2% of respondents with mixed positions moved to materialism; of those neutral on "
  "panpsychism, 57.3% and 54.5% became 'believers' (group sizes not printed, and the samples behind these tables not stated). "
  "In an exploratory path model, feeling emotionally in tune with the group during the session predicted the 4-week score "
  "(standardized beta 0.22), while mystical-type and visual-effect scores were dropped as not significant. In the same team's "
  "double-blind trial in 59 adults with major depression, a 5-item version of the questionnaire shifted after psilocybin "
  "therapy (two 25 mg doses and 6 weeks of daily placebo, study condition; d = 0.45) and less after 6 weeks of daily "
  "escitalopram given with two 1 mg doses of psilocybin (d = 0.2, p = 0.33, which the authors call no change); the "
  "difference between the arms had p = 0.041 one-tailed, about 0.08 two-sided (editors' calculation). In a retrospective online survey by another team, of 1,606 adults recruited because they attributed a change "
  "in their beliefs to a psychedelic experience, each rating 'before', 'after' and 'now' for their most belief-changing "
  "experience in one sitting a mean of 8.2 years after it, the share agreeing that plants can be conscious was 26% before "
  "against 61% after, fungi 21% against 56%, insects 33% against 57%, rocks 8% against 26% and the universe 34% against 80%, "
  "with 'now' close to 'after'; superstitions (black cats bringing bad luck: 8%, 4% and 3%) and belief in free will (74%, 74% "
  "and 73%) did not change meaningfully, and people who remembered a more mystical experience reported larger changes (Nayak "
  "& Griffiths, 2022). The cohort cannot separate the drug from the ceremony's group, ritual, teaching and expectations, or "
  "show that those who stopped answering changed like those who stayed, and its authors say that views held by co-attendees "
  "and by the trial's staff may have passed to participants; the survey, recruited on belief change and relying on memory "
  "over years, cannot show how often or how much beliefs change. On truth, the first team writes that judging the value of "
  "the positions is beyond its work and that it would be hasty to read its results as favouring them, and the second that "
  "persistent beliefs after compelling experiences neither support nor undermine their validity. Certainty: very low. "
  "Status: replicated by the same team."),
 "plain": (
  "Do psychedelics change what people believe about reality? In one study that asked people a week before a psychedelic "
  "retreat or ceremony, and again 4 weeks and 6 months after, beliefs moved a little away from 'everything is physical' and "
  "towards ideas such as other worlds and a conscious universe, more in first-timers. But only 122 of more than 800 people "
  "answered all three times, most already leaned that way, there was no comparison group, and in an exploratory analysis the "
  "shift went with feeling in tune with the group rather than with how mystical or visual the trip was. In a small trial in "
  "depression, beliefs shifted after psilocybin therapy and a little after a standard antidepressant too, and the difference "
  "between them was too small to be sure of. In a survey of people whose beliefs had changed after a psychedelic, looking back "
  "about 8 years on average, 26 in 100 remembered believing plants could be conscious before and 61 in 100 after, while "
  "superstitions did not rise. None of these studies can say whether the beliefs are true."),
 "population": (
  "Adults who planned to attend a retreat, ceremony or other guided experience with a classic psychedelic and signed up at a "
  "study website after online advertisements (819 in the baseline table: mean age 44.4; 55.6% men; 43.8% from the United "
  "States and 19.5% from the United Kingdom; 90.7% White; 54.1% with a master's, doctoral or professional degree, editors' "
  "sum), of whom 122 answered the belief questions at baseline, 4 weeks and 6 months; 59 adults with major depression (30 and "
  "29) in a randomized trial by the same team; and 1,606 adults recruited online by another team because they attributed a "
  "change in their beliefs to a psychedelic experience (mean age 35.1; 67% men; 89% White; 69% from the United States)."),
 "exposure": (
  "Attending a ceremony or retreat with a classic psychedelic (psilocybin mushrooms or truffles, ayahuasca, DMT, San Pedro, "
  "LSD or 1P-LSD), the substance, amount and setting chosen by the respondents and not reported; in the trial, psilocybin "
  "therapy: 25 mg on two dosing days and 6 weeks of daily placebo (study condition); in the survey, a past experience with psilocybin "
  "mushrooms (49%), LSD (33%), ayahuasca (7%), N,N-DMT (6%), 5-MeO-DMT (3%) or mescaline-containing cacti (2%), chosen by each "
  "respondent as the one that most changed their beliefs."),
 "comparator": (
  "Each respondent's own answers about a week before the ceremony (no comparison group); in the trial, randomized daily "
  "escitalopram for 6 weeks with two 1 mg doses of psilocybin; in the survey, respondents' remembered 'before' beliefs, rated "
  "in the same sitting as 'after' and 'now'."),
 "outcome": (
  "Agreement with non-physicalist statements: a 9-item factor (Cronbach's alpha 0.86) of a 13-item Metaphysical Beliefs "
  "Questionnaire written for the study, and 5 of its items in the trial; fatalistic determinism (FAD-Plus items); changes in "
  "the position most strongly endorsed; in the survey, the share agreeing that ten kinds of entity can be conscious, five "
  "superstition items and one free-will item. Whether any belief is true was not assessed."),
 "relation": "is-associated-with",
 "magnitude": (
  "Timmermann et al. (2021), cohort, 122 with paired data: non-physicalist factor at 4 weeks t(121) = 3.66, Bonferroni p = "
  "0.001, d = 0.33; at 6 months t(121) = 5.07, p < 0.0001, d = 0.46 (the printed 95% CIs [0.12, 0.39] and [0.22, 0.50] cannot "
  "be intervals of d; editors' approximate 95% intervals for d, SE = √(1/n + d²/2n), 0.15 to 0.51 and 0.27 to 0.65); first-"
  "timers (53): d = 0.53 and 0.73; fatalistic determinism d = 0.25 at 4 weeks (p = 0.012), not at 6 months. Conversion "
  "(Figure 2; group sizes not printed): 'hard materialists' remaining 24.4% (4 weeks) and 22.2% (6 months); dualists remaining "
  "55.5% and 65.2%; none/mixed to materialism 17.6% and 15.2%; panpsychism neutral to believer 57.3% and 54.5%, sceptic to "
  "believer 22.6% and 37.8%. Lifetime psychedelic use and baseline factor score: Spearman r = 0.223 (cross-sectional). Path "
  "model: emotional synchrony to the 4-week score, beta 0.22. Trial (psilocybin therapy 30, escitalopram 29; 5 items): "
  "interaction F(56) = 3.13, p = 0.041 one-tailed (editors' calculation: two-sided p = 0.082); psilocybin Z = 2.28, p = 0.02, "
  "d = 0.45; escitalopram Z = 0.24, p = 0.33, d = 0.2 (Z = 0.24 gives a one-tailed p of about 0.41, editors' calculation). "
  "Nayak & Griffiths (2022), 1,606, % agreeing before, after and now: plants 26, 61, 64; fungi 21, 56, 62; insects 33, 57, 60; "
  "inanimate natural objects 8, 26, 29; inanimate man-made objects 3, 15, 17; the universe 34, 80, 82; self 80, 97, 98; no "
  "meaningful change for superstitions (black cats 8, 4, 3; Loch Ness monster 10, 10, 10) or free will (74, 74, 73)."),
 "evidence": [
  anchor("timmermann_2021", "sc_timmermann_2021", "pp. 8–10",
   "Methods › Design and participants, 1st paragraph (p. 8, continuing on p. 9) and 2nd paragraph (p. 9, continuing on "
   "p. 10); Table 2 (p. 9); Measures, 1st paragraph (p. 10)",
   "People planning to attend a ceremony with a classic psychedelic (psilocybin mushrooms or truffles, ayahuasca, DMT, San "
   "Pedro, LSD or 1P-LSD) were recruited by online advertisements to a study website; eligibility: aged 18 or over, good "
   "English, and the intention to take part in a retreat, ceremony or other guided experience with a classic psychedelic. "
   "Survey links went out about a week before, one day after and 4 weeks after the indicated date, and the two main measures "
   "(the Metaphysical Beliefs Questionnaire and nine FAD-Plus free-will and fatalism items) were taken at baseline, 4 weeks "
   "and 6 months. Baseline table: N = 819, mean age 44.4 (SD 12.6), 359 women (43.8%) and 455 men (55.6%), United States "
   "43.8%, United Kingdom 19.5%, master's degree 33.6% and doctorate or professional degree 20.5%, White 90.7%, median "
   "household income 9000 dollars a month. Trial: 59 patients with major depression who completed a double-blind randomized "
   "trial (30 given two 25 mg doses of psilocybin and 6 weeks of daily placebo, 29 given two 1 mg doses and daily "
   "escitalopram), with an adapted questionnaire at baseline and 6 weeks; registered as NCT03429075.",
   "qualifies", SRC_T),
  anchor("timmermann_2021", "sc_timmermann_2021", "p. 2",
   "Table 1; Results › Non-physicalist beliefs, 1st and 2nd paragraphs",
   "866 respondents are said to have completed the belief survey at different time points. The 13-item questionnaire (ten "
   "items written for the survey, three from earlier work) gave one factor of nine items, Non-physicalist Beliefs (Cronbach's "
   "alpha 0.86), loading positively on another realm that can be visited (0.790), a supernatural transition to such realms "
   "(0.740), a unifying principle beyond any material or scientific explanation (0.776), panpsychism (0.642), primacy of "
   "other realms (0.592), dualism (0.444) and the physical world as an illusion generated by the mind (0.441), and negatively "
   "on materialism (−0.727) and naturalism (−0.598). The authors say the relation between items and philosophical positions "
   "could be contested, so the items are best taken at face value.",
   "qualifies", SRC_T),
  anchor("timmermann_2021", "sc_timmermann_2021", "pp. 2–3",
   "Results › Non-physicalist beliefs, 3rd paragraph (p. 2, continuing on p. 3); Figure 1a (p. 3)",
   "Against baseline, the factor score shifted away from physicalism at 4 weeks (t(121) = 3.66, Bonferroni-corrected p = "
   "0.001, d = 0.33) and at 6 months (t(121) = 5.07, p < 0.0001, d = 0.46), that is in 122 respondents by the degrees of "
   "freedom; in respondents embarking on their first psychedelic experience, t(52) = 3.85, p = 0.001, d = 0.53 at 4 weeks and "
   "t(52) = 5.32, p < 0.0001, d = 0.73 at 6 months. The intervals printed beside the d values ([0.12, 0.39], [0.22, 0.50], "
   "[0.21, 0.66], [0.36, 0.80]) cannot be confidence intervals of d; editors' approximate 95% intervals for d with n = 122, "
   "SE = √(1/n + d²/2n), are 0.15 to 0.51 and 0.27 to 0.65. At baseline, lifetime psychedelic use correlated with the factor "
   "score (Spearman r = 0.223, p < 0.0001), a cross-sectional association.",
   "supports", SRC_T),
  anchor("timmermann_2021", "sc_timmermann_2021", "p. 3",
   "Figure 1b (left panel) and legend",
   "Item means (with standard errors) at baseline lie on the agree side of neutral for ontological and supernatural "
   "transcendentalism, non-naturalism, panpsychism, primacy of other realms and dualism, and on the disagree side for "
   "materialism. Changes are marked significant up to 6 months for ontological and supernatural transcendentalism, materialism "
   "(down), panpsychism and dualism, and at 4 weeks only for non-naturalism and primacy of other realms; naturalism and "
   "solipsism/idealism carry no marker, although the legend lists solipsism/idealism among the items that shifted. The axis "
   "runs from Disagree to Agree without numbers, so item changes cannot be given in scale units.",
   "qualifies", SRC_T),
  anchor("timmermann_2021", "sc_timmermann_2021", "p. 3",
   "Results › Fatalism, 1st paragraph",
   "Fatalistic determinism rose at 4 weeks against baseline (t(121) = 2.81, p = 0.012, d = 0.25), and the effect did not "
   "persist at 6 months; in first-timers, d = 0.46 at 4 weeks (p = 0.003) and 0.39 at 6 months (p = 0.012).",
   "supports", SRC_T),
  anchor("timmermann_2021", "sc_timmermann_2021", "pp. 3–4",
   "Results › Conversion of preferred metaphysical beliefs, 1st paragraph (p. 3, continuing on p. 4); Figure 2a–d (p. 4)",
   "Respondents were grouped by the position they most strongly endorsed at baseline. Of 'hard materialists', 24.4% remained "
   "at 4 weeks and 22.2% at 6 months, 31.1% and 33.3% moved to dualism and 42.2% and 44.4% to none/mixed; of dualists, 55.5% "
   "and 65.2% remained and 37% and 23.9% moved to none/mixed; of none/mixed respondents, 17.6% and 15.2% moved to materialism. "
   "Of respondents neutral on panpsychism, 57.3% and 54.5% became 'believers', and of sceptics 22.6% and 37.8%; 83.9% and "
   "86.8% of believers stayed believers. The number of respondents in each group is not printed, and the tests appear only as "
   "asterisks.",
   "supports", SRC_T),
  anchor("timmermann_2021", "sc_timmermann_2021", "pp. 5, 11",
   "Results › Process of change modelling, 1st paragraph, and Figure 4 (p. 5); Methods › Statistical analysis, 4th paragraph "
   "(p. 11)",
   "Exploratory path model of the 4-week score: perceived emotional synchrony with the group during the session predicted it "
   "(standardized beta 0.22), moderated by baseline peer conformity (0.08); synchrony was predicted by identity fusion with "
   "the group shortly before the session (0.30), trait absorption (0.18), gender (−0.17), age (−0.12) and baseline beliefs "
   "(0.13); baseline beliefs predicted the 4-week score with beta 0.75. Visual-imagery (ASC) and mystical-type (MEQ) scores, "
   "expected to predict the shift, were left out because their effects were not significant; for people who attended more "
   "than one ceremony, only the largest score on each scale was used.",
   "qualifies", SRC_T),
  anchor("timmermann_2021", "sc_timmermann_2021", "pp. 5–6",
   "Results › Validation with data from a controlled clinical trial, 1st paragraph (p. 5, continuing on p. 6); Figure 5 "
   "(p. 6)",
   "Psilocybin therapy (n = 30) against escitalopram (n = 29) on the 5-item version: drug by time interaction F(56) = 3.13, "
   "p = 0.041 one-tailed (editors' calculation: F(1, 56) = 3.13 gives a two-sided p of 0.082); psilocybin arm Z = 2.28, p = "
   "0.02, d = 0.45; escitalopram arm Z = 0.24, p = 0.33, d = 0.2, described as no change (editors' calculation: Z = 0.24 gives "
   "a one-tailed p of about 0.41, so the three printed figures do not agree); psilocybin responders shifted more than "
   "escitalopram responders (Z = 1.74, p = 0.041, g = 0.56, 90% CI −0.17 to 1.26, which includes zero); in the psilocybin arm, "
   "belief change correlated with change in spiritual 'universality' (r = 0.52, p = 0.003), with no figure given for the "
   "escitalopram arm.",
   "supports", SRC_T),
  anchor("timmermann_2021", "sc_timmermann_2021", "pp. 10–11",
   "Methods › Measures, 6th paragraph (p. 10); Methods › Statistical analysis, 6th paragraph (p. 11)",
   "The trial used a shortened questionnaire of five items (ontological and supernatural transcendentalism, dualism, "
   "materialism and non-naturalism) from which the factor was extracted; change was compared between arms by repeated-measures "
   "ANCOVA adjusted for baseline, and single-sided p values are reported for the trial because the hypotheses were derived "
   "from the survey data.",
   "qualifies", SRC_T),
  anchor("timmermann_2021", "sc_timmermann_2021", "p. 8",
   "Discussion, 12th paragraph",
   "The authors write that assessing the value of competing philosophical positions is beyond the remit of their work, and "
   "some might argue of science; that it would be hasty to read the findings as evidence for the positive value of "
   "non-physicalist, panpsychist or fatalistic beliefs; and that adopting non-physicalist or supernatural beliefs has been "
   "linked to avoidant coping ('spiritual bypassing').",
   "qualifies", SRC_T),
  anchor("timmermann_2021", "sc_timmermann_2021", "p. 8",
   "Discussion, 14th and 15th paragraphs",
   "Limitations stated by the authors: religious affiliation, environmental susceptibilities and interest in metaphysical "
   "beliefs were not collected, so the sample may be skewed towards people sensitive to these shifts; both samples were "
   "largely Western and well educated; the samples differ in size, distress and expectations; the cultural milieu was not "
   "measured, which they call an oversight, and views held by co-attendees and by the trial's research staff, or by the wider "
   "psychedelic culture, may have transferred to participants.",
   "qualifies", SRC_T),
  anchor("nayak_2022", "sc_nayak_2022", "pp. 2–4",
   "Materials and methods › Participant Recruitment (p. 2); Results › Survey Completion, 1st paragraph (p. 3, continuing on "
   "p. 4)",
   "Anonymous, unpaid online survey, August 2020 to January 2021, advertised on social media, relevant websites (for example "
   "Erowid) and by email to people who had had changes in their beliefs that they attributed to a psychedelic experience, the "
   "belief changes described vaguely on purpose. Of 11,281 who reached the landing page, 4,997 consented; 170 lacked English "
   "fluency, 264 reported no belief-changing experience, 38 failed attention checks, 76 had used another drug, 633 several "
   "psychoactive drugs, 11 gave inconsistent ages, 2,086 did not complete and 113 appeared to describe several experiences, "
   "leaving 1,606.",
   "qualifies", SRC_N),
  anchor("nayak_2022", "sc_nayak_2022", "pp. 2–3",
   "Materials and methods › Survey Administration and Details of the Psychedelic Belief-Changing Experience (p. 2); Ratings of "
   "Beliefs Before and After the Experience (p. 3)",
   "The survey was designed to take about 50 minutes, completed in one sitting. Respondents answered about the single "
   "psychedelic experience they felt led to the greatest belief change, and rated each belief from strongly disagree (−3) to "
   "strongly agree (+3) for three time points, 'Before (e.g., a month)', 'After (e.g., a month)' and 'Now', all at the time "
   "of the survey.",
   "qualifies", SRC_N),
  anchor("nayak_2022", "sc_nayak_2022", "p. 4",
   "Results › Respondent Characteristics, 1st paragraph; Table 1",
   "Mean age 35.1 (SD 13.3); 67% men; 89% White; 69% from the United States; the reference experience a mean of 8.2 years "
   "(SD 12.6) before the survey, within the past 12 months for 25%, and the first belief-changing psychedelic experience for "
   "44%; psilocybin mushrooms 49%, LSD 33%, ayahuasca 7%, N,N-DMT 6%, 5-MeO-DMT 3%, mescaline-containing cacti 2%; 20.9 "
   "lifetime uses of classic psychedelics on average (SD 25.7).",
   "qualifies", SRC_N),
  anchor("nayak_2022", "sc_nayak_2022", "pp. 4–5",
   "Results › Changes in Attribution of Consciousness, 1st paragraph (p. 4); Table 2 and footnote (p. 5)",
   "Shares agreeing (+1 to +3) that each entity can have conscious experience, before, after and now: self 80%, 97%, 98%; "
   "other humans 78%, 94%, 95%; non-human primates 63%, 83%, 85%; four-legged animals 59%, 79%, 82%; insects 33%, 57%, 60%; "
   "fungi 21%, 56%, 62%; plants 26%, 61%, 64%; inanimate natural objects such as rocks 8%, 26%, 29%; inanimate man-made "
   "objects 3%, 15%, 17%; 'the universe is conscious' 34%, 80%, 82%. Every before-after difference met the study's criteria "
   "(at least 10 points and p < 10⁻¹⁰ or smaller); no after-now difference did. The effects were said not to depend on whether "
   "the experience was in the past year or the first one (data not shown).",
   "supports", SRC_N),
  anchor("nayak_2022", "sc_nayak_2022", "pp. 5–6",
   "Results › Changes in Attribution of Consciousness, 2nd paragraph (p. 5); Figure 2 and legend (p. 6)",
   "Respondents whose remembered Mystical Experience Questionnaire score was at or above the median reported larger increases "
   "than those below it; their 'before' ratings were similar, and their 'after' ratings differed for every entity except other "
   "humans; the relation held with the score as a continuous variable after adjustment (model in a supplementary table, not "
   "read; group sizes not given).",
   "qualifies", SRC_N),
  anchor("nayak_2022", "sc_nayak_2022", "pp. 5–6",
   "Results › Changes in Superstitious Beliefs and Freewill, 1st paragraph (p. 5); Table 3 (p. 6)",
   "No meaningful change in the superstition or free-will items, before, after and now: black cats can bring bad luck 8%, 4%, "
   "3%; breaking a mirror brings bad luck 10%, 5%, 4%; 13 is unlucky 7%, 3%, 2%; the abominable snowman exists 6%, 8%, 8%; the "
   "Loch Ness monster exists 10%, 10%, 10%; people have free will 74%, 74%, 73%.",
   "qualifies", SRC_N),
  anchor("nayak_2022", "sc_nayak_2022", "p. 6",
   "Discussion, 4th paragraph (end) and 5th paragraph",
   "The authors write that compelling experiences leading to persistent beliefs neither support nor undermine the epistemic "
   "validity of those beliefs. They list as limitations the retrospective design, the restriction to people who endorsed a "
   "belief change they attributed to a psychedelic, and possible demand effects, and argue that unchanged free-will beliefs "
   "suggest the findings are not only an artefact of demand.",
   "qualifies", SRC_N),
 ],
 "grade": {
  "starting_level": "low",
  "domains": {
   "risk_of_bias": {"levels": 2, "note": (
    "The cohort is at very high risk of bias on its card (ROBINS-E): with no comparison group, the drug cannot be separated "
    "from the ceremony's setting, group, ritual, teaching and expectations; about 85 in 100 baseline respondents are missing "
    "from the paired analyses, with no comparison of those who stayed and those who left; analytic samples differ between "
    "analyses and are not stated; the path model kept significant predictors only; and the questionnaire is new and "
    "self-rated, in a culture where the expected direction is familiar. The survey selected respondents on the outcome and "
    "asked them to recall earlier beliefs years later (JBI: high risk). The trial is randomized, but its belief items are a "
    "5-item version without reported reliability, analysed secondarily with one-tailed tests, and the paper does not say "
    "whether patients could tell their treatment.")},
   "inconsistency": {"levels": 0, "note": (
    "The direction agrees across the cohort, the trial and the survey (away from materialism, towards panpsychism and wider "
    "attribution of consciousness); the conversion tables also show moves towards materialism, which the statement reports. "
    "The two papers differ on the role of mystical experience (no link in the cohort's path model, a link in the survey), "
    "which the statement also reports.")},
   "indirectness": {"levels": 0, "note": (
    "Rated as worded, for self-selected ceremony attendees, patients in one trial and survey respondents chosen for a belief "
    "change; the statement does not extend the shifts to people who use psychedelics in general.")},
   "imprecision": {"levels": 0, "note": (
    "The cohort's shifts exclude no change (editors' approximate 95% intervals for d 0.15 to 0.51 at 4 weeks and 0.27 to 0.65 "
    "at 6 months); the trial's difference between arms is imprecise (two-sided p about 0.08), which the statement says.")},
   "publication_bias": {"levels": 0, "note": (
    "Not assessable: no registration or analysis plan is mentioned for the cohort or the survey analyses, and the paper does "
    "not say whether the belief items were a registered outcome of the trial.")},
   "large_effect": {"levels": 0},
   "dose_response": {"levels": 0},
   "plausible_confounding": {"levels": 0}
  },
  "certainty": "very-low",
  "reasoning": (
   "Observational evidence (a prospective cohort without a comparison group and a retrospective survey) starts low; rated down "
   "two levels for risk of bias, which is below the floor: very low. Rated as worded: an association between attending a "
   "psychedelic ceremony and modest shifts in stated beliefs among people who kept answering; not that psychedelics cause the "
   "shift, that it is specific to psychedelics (escitalopram also moved, d = 0.2, and the difference between the arms was "
   "significant only one-tailed), or that it lasts beyond 6 months. The trial is randomized and would start high on its own, "
   "but as the only comparison between treatments it rests on 59 patients, a 5-item version and a one-tailed p of 0.041 "
   "(about 0.08 two-sided), so it qualifies the claim rather than raising it. Status replicated by the same team: the cohort "
   "and the trial are one group's two samples, reported in one paper; the survey from another group agrees in direction but "
   "recruited people because their beliefs had changed and relied on recall, so it is not counted as an independent test. "
   "Whether the beliefs are true is outside what any of these designs can address, as both teams say.")
 },
 "status": "replicated-same-team",
 "verification": verification(
  "Theme 10. Not read: the Supplementary Information of Timmermann et al. (2021) (characteristics of the 122, model fit, "
  "first-timers' item results), the parent cohort report (Kettner et al., 2021, Frontiers in Pharmacology 12) and the trial "
  "report (Carhart-Harris et al., 2021, New England Journal of Medicine 384, 1402–1411), which would say whether patients "
  "could tell their treatment and whether belief items were a registered outcome; the Supplementary Material of Nayak & "
  "Griffiths (2022) (effect sizes, adjusted model). No DOIs are printed for these. The cards and the PDFs agree on every "
  "number used."),
 "version": "0.1.0",
 "changelog": changelog("Timmermann et al. (2021) and Nayak & Griffiths (2022)"),
}

# ---------------------------------------------------------------------------------------------------------------
# 2. Personality after psilocybin
# ---------------------------------------------------------------------------------------------------------------
c2 = {
 "id": "cl_psi_personality",
 "substance": "psilocybin",
 "section": 5,
 "statement": (
  "Evidence is insufficient to say whether psilocybin changes personality. In two small studies with no comparison group for "
  "the change, self-rated Openness to experience on the NEO Personality Inventory-Revised (T scores: population mean 50, "
  "SD 10) was a few points higher 1 to 3 months after psilocybin with preparation and support than each person's own score "
  "before; the one randomized comparison of personality in these trials found no difference, no paper checked a change "
  "against behaviour, and the two papers disagree on whether the change followed the experience. In 52 healthy, "
  "hallucinogen-naive, unpaid volunteers pooled from two double-blind trials at Johns Hopkins (mean age 46; 54% with "
  "postgraduate degrees; 90% regularly taking part in religious or spiritual activities; screening Openness 65.4 and 62.7), "
  "Openness was 2.8 T points higher 1 to 2 months after the high-dose session (psilocybin 30 mg/70 kg, study condition; "
  "F(1, 51) = 5.47, p = 0.023), Neuroticism, Extroversion, Agreeableness and Conscientiousness did not change detectably, "
  "and in the 30 whose first session was placebo, methylphenidate or a low psilocybin dose Openness did not change after "
  "that session (p = 0.48), though the two changes were never compared with each other (MacLean et al., 2011). The rise was "
  "in the 30 who met the criterion for a 'complete mystical experience' (+5.7, p = 0.002), not in the other 22 (−1.2), and "
  "it correlated with the session's mystical score (r = 0.42); individual changes ranged from about −12 to +36 T points, "
  "about 17 of the 51 visible points in the paper's figure lie below zero (about a third of the volunteers scored lower; "
  "editors' reading), and without the three largest rises the other 49 would average about +1.3 (editors' approximate "
  "calculation, (2.8 × 52 − 84) / 49). At a mean of 16 months the complete-mystical group was 4.2 points above its screening "
  "score at p = 0.050 (0.0503 by the editors' calculation) and the others 0.3 below; the change for all participants together "
  "was not reported. In the earlier trial that supplied 35 of these volunteers, the randomized comparison of 15 people given "
  "psilocybin first with 15 given methylphenidate first found no difference in any personality factor 2 months later (no "
  "values printed; Griffiths et al., 2006, as its checked study card reports), a result MacLean et al. do not mention. In 19 "
  "adults with treatment-resistant depression given psilocybin 10 mg and then 25 mg a week later with psychological support "
  "in an open-label study in London (Erritzoe et al., 2018; its authors include MacLean et al.'s first author), Neuroticism "
  "fell from T 76.6 to 70.9 (p = 0.002), Extraversion rose from 31.1 to 37.6 (p < 0.001) and Openness from 52.7 to 57.6 "
  "(p = 0.012) at 3 months, Conscientiousness rose at trend level (p = 0.086) and Agreeableness did not change; Neuroticism, "
  "Extraversion and Conscientiousness moved from far outside the norms towards them, and the authors say it is hard to infer "
  "that the changes, particularly in Neuroticism and Extraversion, are traits rather than states. The Openness rise did not "
  "differ between the 7 patients whose depression responded and the 12 whose did not, and no 'peak experience' score related "
  "to it, whereas insightfulness during the session went with the Neuroticism and Extraversion changes in uncorrected, "
  "exploratory correlations (r = −0.47 and 0.54). All scores are self-ratings by people who knew, or could probably tell, "
  "that they had taken psilocybin, in volunteers drawn to a psilocybin study or to a psychedelic treatment; in the 2006 trial, "
  "three people close to each volunteer rated a small positive change in behaviour and attitudes after psilocybin (Griffiths "
  "et al., 2006, as its card reports), but no paper read related such ratings, or any behaviour, to the personality scores. "
  "Certainty: very low. Status: contested."),
 "plain": (
  "Can psilocybin change your personality? It has not been shown. In two small studies, people rated themselves a few points "
  "more open to experience 1 to 3 months after psilocybin with preparation and support than before, on a scale where the "
  "average adult scores 50 and the usual spread is 10 points: 2.8 points in 52 healthy, mostly religious or spiritual "
  "volunteers, and 4.9 points in 19 patients with hard-to-treat depression. Neither study compared the change with people "
  "who did not get psilocybin, and in the one comparison of this kind in the same trials, 15 people who had psilocybin first "
  "and 15 who had a stimulant first did not differ 2 months later. In the volunteers, the rise came from those who had a "
  "'complete' mystical experience, and about a third of all the volunteers scored lower afterwards; more than a year later "
  "that group was still about 4 points up, a result right on the edge of chance. The patients also rated themselves less "
  "anxious and more sociable as their depression lifted, which the researchers say may reflect mood rather than lasting "
  "traits, and the two studies disagree on whether the change followed the experience. Neither study checked the scores "
  "against how people behave."),
 "population": (
  "52 healthy, hallucinogen-naive, unpaid volunteers recruited by community flyers for a study of states of consciousness "
  "brought about by psilocybin (35 from a 2006 trial and 17 from a 2011 trial at Johns Hopkins; mean age 46; 22 men and 30 "
  "women, editors' sum; 54% with postgraduate degrees; 90% regularly taking part in religious services, discussion groups, "
  "prayer or meditation; screening Openness T 65.4 and 62.7); in the 2006 trial, 30 volunteers randomized to drug order "
  "(15 per order); and 19 analysed of 20 adults with moderate to severe treatment-resistant unipolar depression in an "
  "open-label study in London (6 women, 13 men; mean age 44.7; five had tried a psychedelic before)."),
 "exposure": (
  "Psilocybin by mouth with preparation and support, as study conditions only: one session at 30 mg/70 kg (in the 2011 trial "
  "within four ascending or descending doses with a placebo session), lying down with an eye mask and music, after at least "
  "8 hours of meetings with the session monitors; in the open-label study, 10 mg and then 25 mg a week later, eyes closed "
  "with music and two therapists, with integration visits afterwards."),
 "comparator": (
  "Each person's own personality scores before (screening or baseline), with no concurrent comparison of change in either "
  "main study; within the healthy volunteers, people with and without a 'complete mystical experience' (not randomized) and, "
  "separately, change after a first session of placebo, methylphenidate or psilocybin 5 mg/70 kg; in the 2006 trial, people "
  "given psilocybin first against people given methylphenidate first (randomized; no values printed)."),
 "outcome": (
  "Self-rated personality on the NEO Personality Inventory-Revised (240 items; five domains of six facets; T scores from "
  "combined-sex norms), 1 to 2 months after the session and about 14 months after the last session (a mean of 16 months "
  "after the high-dose session) in the healthy volunteers, and 3 months after in the patients; no behavioural measure and no "
  "ratings of personality by others."),
 "relation": "insufficient-evidence",
 "magnitude": (
  "MacLean et al. (2011), 52 volunteers, screening to 1–2 months: Openness +2.8 T points, F(1, 51) = 5.47, p = 0.023, "
  "partial eta squared 0.10 (editors' calculation: within-person standardized change about 0.32, √(5.47/52)); Neuroticism "
  "−0.5 (p = 0.62), Extroversion +0.8 (p = 0.38), Agreeableness +1.7 (F = 2.31, printed p = 0.16; 0.13 by the editors' "
  "calculation), Conscientiousness −0.9 (p = 0.28). After a first session without high-dose psilocybin (30): F(1, 29) = 0.52, "
  "p = 0.48. Complete mystical experience (30) against not (22): F(1, 50) = 9.32, p = 0.004; +5.7 (t(29) = 3.44, p = 0.002) "
  "against −1.2 (t(21) = 0.87, p = 0.39). Mystical score and Openness change r = 0.42, p = 0.002 (editors' 95% CI about 0.17 "
  "to 0.62, Fisher z). Follow-up (mean 16 months): complete group +4.2, F(1, 29) = 4.17, p = 0.050 (0.0503 by the editors' "
  "calculation); others (21) −0.3, p = 0.86; all participants not reported. Figure 1 (editors' reading): changes from about "
  "−12 to +36, about 17 of 51 visible points below zero; about +1.3 without the three largest (editors' approximate "
  "calculation). Griffiths et al. (2006, card): no personality factor differed between order groups (15 and 15) at 2 months; "
  "no values. Erritzoe et al. (2018), 19 patients, baseline to 3 months (T scores): Neuroticism 76.6 to 70.9 (−5.7, "
  "p = 0.002), Extraversion 31.1 to 37.6 (+6.5, p < 0.001), Openness 52.7 to 57.6 (+4.9, p = 0.012), Agreeableness 46.8 to "
  "46.7 (p = 0.953), Conscientiousness 29.9 to 33.1 (+3.2, p = 0.086); printed d −0.571, 0.716, 0.437, −0.006 and 0.273, "
  "from a formula whose denominator is not divided by 2 (about 0.71 times the usual average-SD d; editors' calculation); "
  "Openness change in responders (7) against non-responders (12) 11 ± 21 against 7 ± 6, p = 0.623 (units not stated); "
  "insightfulness with Neuroticism change r = −0.47 (p = 0.043) and with Extraversion change r = 0.54 (p = 0.017), "
  "uncorrected; no peak-experience score related to the Openness change."),
 "evidence": [
  anchor("maclean_2011", "sc_maclean_2011", "pp. 1454–1455",
   "Methods › Participants, 1st and 2nd paragraphs (p. 1454); Table 1 (p. 1455)",
   "Volunteers recruited from the local community by flyers announcing a study of states of consciousness brought about by "
   "psilocybin, a naturally occurring substance used sacramentally in some cultures; about 20% of those screened by telephone "
   "passed; one Study 2 participant with lifetime psilocybin use and one Study 1 participant with incomplete personality data "
   "were excluded, leaving 52 hallucinogen-naive participants (35 from Study 1, Griffiths et al., 2006; 17 from Study 2, "
   "Griffiths et al., 2011). 54% had postgraduate degrees and 90% regularly took part in religious services, discussion "
   "groups, prayer or meditation; no payment; motivation described as curiosity and the chance for self-reflection. Table 1: "
   "mean age 46 in both studies; 14 men and 21 women, and 8 men and 9 women; screening T scores (mean 50, SD 10), Study 1 and "
   "Study 2: Openness 65.4 and 62.7, Neuroticism 41.8 and 46.1, Extroversion 55.3 and 52.1, Agreeableness 55.7 and 55.1, "
   "Conscientiousness 51.0 and 51.7.",
   "qualifies", SRC_M),
  anchor("maclean_2011", "sc_maclean_2011", "pp. 1455–1456",
   "Methods › Psilocybin sessions › Dose conditions and Session protocol; Measures › NEO Personality Inventory (p. 1455); "
   "Analysis, 1st paragraph (p. 1456)",
   "Participants were told they would receive a moderate or high dose of psilocybin in one session, without knowing which. "
   "Study 1: psilocybin 30 mg/70 kg in one session and methylphenidate 40 mg/70 kg in the other one or two; Study 2: 5, 10, "
   "20 and 30 mg/70 kg in ascending or descending order with a placebo session inserted quasi-randomly (study conditions). "
   "At least 8 hours of preparation meetings with the monitors; sessions lying on a couch with an eye mask and music. NEO "
   "PI-R (240 items, T scores from combined-sex norms) at screening, 1–2 months after each session and about 14 months after "
   "the last session. The analysis pools the two studies for power; the high-dose session in Study 2 could not be fully "
   "isolated from the lower doses, and personality after it was always measured within 1–2 months and before any later "
   "session.",
   "qualifies", SRC_M),
  anchor("maclean_2011", "sc_maclean_2011", "p. 1456",
   "Results › Changes in personality following the psilocybin session, 1st paragraph",
   "Openness rose from screening to 1–2 months after the high-dose session by 2.8 T points (F(1, 51) = 5.47, p = 0.023, "
   "partial eta squared 0.10); Neuroticism −0.5 (p = 0.62), Extroversion +0.8 (p = 0.38), Agreeableness +1.7 (F(1, 51) = "
   "2.31, printed p = 0.16, which is 0.13 by the editors' calculation) and Conscientiousness −0.9 (p = 0.28) did not change "
   "significantly; test-retest correlations 0.61–0.84. In the 30 whose first session was placebo, methylphenidate or "
   "psilocybin 5 mg/70 kg, Openness did not change after that session (F(1, 29) = 0.52, p = 0.48); this change is not tested "
   "against the change after the high-dose session.",
   "supports", SRC_M),
  anchor("maclean_2011", "sc_maclean_2011", "pp. 1456–1457",
   "Results › Relationship between session-day effects and changes in Openness, 1st and 2nd paragraphs (p. 1456, the 2nd "
   "continuing on p. 1457); Figure 1 (p. 1457)",
   "The mystical score of the high-dose session (subscale scores 0.03 to 1.00) correlated with the Openness change (r = 0.42, "
   "p = 0.002; Spearman 0.47; editors' 95% CI about 0.17 to 0.62, Fisher z) but not with screening Openness (r = 0.12, "
   "p = 0.41); the change also correlated with the Mysticism Scale (0.33), oceanic boundlessness (0.44), visionary "
   "restructuralization (0.41) and dread of ego dissolution (0.31).",
   "supports", SRC_M),
  anchor("maclean_2011", "sc_maclean_2011", "p. 1457",
   "Figure 1 (editors' reading of a 300-dpi rendering)",
   "Individual changes in Openness from screening to 1–2 months range from about −12 to about +36 T points; about 17 of the "
   "51 visible points lie below zero, 2 at about zero and 32 above (one point presumably hidden by overlap); the three largest "
   "rises, about +21, +26 and +36, are at high mystical scores. Without them the mean of the other 49 would be about +1.3 "
   "(editors' approximate calculation, (2.8 × 52 − 84) / 49).",
   "qualifies", SRC_M),
  anchor("maclean_2011", "sc_maclean_2011", "pp. 1457–1458",
   "Results › Effect of mystical experience on changes in Openness, 1st paragraph (p. 1457); Figures 2 and 3 (p. 1458)",
   "30 of 52 met the criterion for a complete mystical experience (at least 60% on each of six subscales). Time by group "
   "interaction F(1, 50) = 9.32, p = 0.004, partial eta squared 0.16: Openness +5.7 in the complete group (t(29) = 3.44, "
   "p = 0.002) and −1.2 in the other 22 (t(21) = 0.87, p = 0.39); five of six facets showed the same interaction (not "
   "Actions). Screening Openness and its facets did not differ between the groups (p > 0.10). The groups are defined by what "
   "happened in the session, not by randomization.",
   "supports", SRC_M),
  anchor("maclean_2011", "sc_maclean_2011", "p. 1457",
   "Results › Follow-up, 1st paragraph",
   "At a follow-up a mean of 16 months after the high-dose session, the complete-mystical group (n = 30) was slightly lower "
   "than at post-test (p = 0.12) and 4.2 T points above screening (F(1, 29) = 4.17, p = 0.050, partial eta squared 0.13; "
   "0.0503 by the editors' calculation); the other group (n = 21, against 22 at post-test, the missing person not described) "
   "was 0.3 below screening (p = 0.86). The change for all participants together is not reported.",
   "supports", SRC_M),
  anchor("maclean_2011", "sc_maclean_2011", "pp. 1457–1459",
   "Discussion, 1st paragraph (p. 1457, continuing on p. 1458), 2nd paragraph (p. 1458, continuing on p. 1459) and 4th "
   "paragraph (p. 1459)",
   "The authors call this the first study to show personality change in healthy adults after an experimentally manipulated "
   "discrete event and call for replication in larger groups with diverse baseline personalities; they compare the rise with "
   "the usual fall in Openness of about 1 T point per decade in normal ageing and with smaller rises after antidepressant "
   "treatment or intensive outpatient counselling, figures from other studies; and they suggest that participants' motivation "
   "and preparation, and their regular spiritual practice, may have contributed to the result.",
   "qualifies", SRC_M),
  anchor("griffiths_2006", "sc_griffiths_2006", "p. 278",
   "Results › Personality and affect",
   "No factor of the NEO PI-R personality inventory, and neither the positive nor the negative affect scale of the PANAS-X, "
   "was differentially affected by psilocybin: the two order groups (15 given psilocybin first, 15 methylphenidate first) did "
   "not differ at screening or 2 months after session 1, and the methylphenidate-first group did not change from after "
   "session 1 to after session 2, its psilocybin session. No values are shown.",
   "contradicts", SRC_G, located_by=LOC_G),
  anchor("griffiths_2006", "sc_griffiths_2006", "p. 278",
   "Table 4; Results › Community observer ratings of changes in participants' and behavior and attitudes (heading as printed)",
   "Three adults nominated by each participant, interviewed by telephone 7 to 8 weeks after each session (N = 26), rated a "
   "mean positive change in the participant's behaviour and attitudes of 2.42 (SEM 0.70) after psilocybin against −0.03 "
   "(SEM 0.68) after methylphenidate (p < 0.01), which the authors call a small but significant positive change. These "
   "ratings are not related to the personality scores in the card.",
   "qualifies", SRC_G, located_by=LOC_G),
  anchor("griffiths_2006", "sc_griffiths_2006", "pp. 269, 276, 278–279, 281",
   "Materials and methods › Study design (p. 269) and the session counts, as the card's sample record and its reporting issue "
   "on the decoy arm give them",
   "Of 36 enrolled (14 men), 30 were randomized to drug order (15 per order) and 6 to a decoy arm that had methylphenidate "
   "twice and then open-label psilocybin in a third session; the decoy arm's data were left out of the statistical analyses. "
   "MacLean et al. took 35 of these 36 into their analysis (one excluded for incomplete personality data) and describe every "
   "high-dose session as blinded, so their 35 would include at least five of the six open-label sessions (editors' "
   "inference).",
   "qualifies", SRC_G, located_by=LOC_G),
  anchor("erritzoe_2018", "sc_erritzoe_2018", "pp. 368–370",
   "Limitations box (p. 368); Methods › Participants (p. 369, continuing on p. 370), Study procedure and Measures (p. 370); "
   "Results, 1st paragraph (p. 370)",
   "Open-label feasibility study: 20 patients with unipolar major depression of at least moderate severity (17 or more on "
   "the 21-item HAM-D) and no improvement after two pharmacologically distinct antidepressants, given psilocybin 10 mg and, a "
   "week later, 25 mg (study conditions), lying with eyes closed to music with two therapists in a non-directive, supportive "
   "role, with integration visits a day and a week after the 25 mg session. NEO PI-R at screening and 3 months; one patient "
   "did not complete most follow-up measures, leaving 19 (6 women, 13 men, mean age 44.7). Five had tried a psychedelic "
   "before. The authors list a small sample, the open-label design and the absence of a control condition, and two-thirds "
   "men, as limitations. Cohen's d was computed as the difference in means over the square root of the sum of the two "
   "variances, not divided by 2.",
   "qualifies", SRC_E),
  anchor("erritzoe_2018", "sc_erritzoe_2018", "pp. 370–371",
   "Results › Personality changes from baseline to 3-month follow-up, 1st paragraph (p. 370, continuing on p. 371); Table 1 "
   "(p. 371)",
   "Baseline to 3 months, T scores: Neuroticism 76.6 to 70.9 (−5.7, p = 0.002, d −0.571), Extraversion 31.1 to 37.6 (+6.5, "
   "p < 0.001, d 0.716), Openness 52.7 to 57.6 (+4.9, p = 0.012, d 0.437), Agreeableness 46.8 to 46.7 (p = 0.953), "
   "Conscientiousness 29.9 to 33.1 (+3.2, p = 0.086); eleven of 30 facets changed and ten survived false-discovery-rate "
   "correction; standard deviations are not reported.",
   "supports", SRC_E),
  anchor("erritzoe_2018", "sc_erritzoe_2018", "pp. 371–372",
   "Results › Personality changes vs. changes in depression scores, 1st paragraph (p. 371); Relationship between Peak "
   "Experience and personality changes, 1st paragraph (p. 371, continuing on p. 372)",
   "Responders at 3 months (n = 7) against non-responders (n = 12): Neuroticism −23 ± 17 against −6 ± 8 (p = 0.038), "
   "Conscientiousness 15 ± 11 against 0 ± 12 (p = 0.017), Openness 11 ± 21 against 7 ± 6 (p = 0.623), units not stated; no "
   "domain change correlated significantly with the change in depression scores. Insightfulness during the 25 mg session "
   "went with a larger fall in Neuroticism (r = −0.47, p = 0.043) and rise in Extraversion (r = 0.54, p = 0.017), and "
   "spiritual experience with the Extraversion rise (r = 0.47, p = 0.048); none of the peak-experience scores related to the "
   "change in Openness or Conscientiousness. The correlations are uncorrected and called exploratory (Methods, p. 370).",
   "qualifies", SRC_E),
  anchor("erritzoe_2018", "sc_erritzoe_2018", "p. 373",
   "Discussion, 3rd to 6th paragraphs",
   "Openness change did not correlate with treatment response or differ between responders and non-responders, which the "
   "authors read as a change beyond improved mood, citing their own unpublished survey (data not shown). Against d values "
   "they computed from three antidepressant trials (five samples, 469 patients, 8 to 20 weeks), Neuroticism, Agreeableness and "
   "Conscientiousness changed similarly (−0.59, 0.04 and 0.18 there; −0.57, −0.01 and 0.27 here), while Openness (0.44 "
   "against 0.13) and Extraversion (0.72 against 0.32) changed more; they advise caution because follow-up times differ. From "
   "these data, they write, it is hard to infer that the changes, in particular in Neuroticism and Extraversion, are trait "
   "rather than state changes, though a change lasting 3 months might suggest more than a state artefact.",
   "qualifies", SRC_E),
  anchor("erritzoe_2018", "sc_erritzoe_2018", "pp. 374–375",
   "Discussion, 10th paragraph (p. 374), 12th paragraph (p. 374, continuing on p. 375) and 13th paragraph (p. 375)",
   "Openness started 2.7 T points above the norms and rose a further 4.9, while Neuroticism fell from an abnormally high level "
   "and Extraversion and Conscientiousness rose from abnormally low levels, towards healthy norms; the authors suggest that "
   "people low in Openness are less likely to volunteer for a psychedelic treatment. They note that the correlation analyses "
   "were uncorrected and exploratory and the sample modest, and call their findings somewhat inconsistent with MacLean et al. "
   "(2011), where mystical-type experience predicted sustained Openness increases, suggesting differences in population, "
   "questionnaires, the support offered and timing (3 months against more than 12).",
   "qualifies", SRC_E),
 ],
 "grade": {
  "starting_level": "low",
  "domains": {
   "risk_of_bias": {"levels": 2, "note": (
    "The estimates are before-and-after changes in self-ratings: the parent trials' randomization does not protect them (RoB 2 "
    "high on the MacLean card), and the patient study has no control group (ROBINS-I critical). The volunteers could probably "
    "tell when they had the high dose, were unpaid, motivated and mostly spiritually active, and their expectations were not "
    "measured; the mystical-experience groups were formed by what happened in the session; the patients knew they had "
    "psilocybin, their depression was lifting, and their extreme baseline scores leave room for regression towards the norms. "
    "MacLean et al. describe every high-dose session as blinded, but the 2006 report, as its checked card gives it, says 6 of "
    "its 36 volunteers had open-label psilocybin in a third session, and MacLean's 35 Study 1 volunteers would include at "
    "least five of them (editors' inference).")},
   "inconsistency": {"levels": 1, "note": (
    "In the trial that supplied 35 of the 52 volunteers, the randomized comparison found no difference in any personality "
    "factor (no values printed), while the pooled within-person analysis found a rise in Openness; and the two papers disagree "
    "on whether the change followed the experience (mystical score r = 0.42 in the volunteers; no peak-experience score related "
    "to Openness in the patients). Small groups and different designs may explain part of this; nothing resolves it.")},
   "indirectness": {"levels": 1, "note": (
    "The question is whether psilocybin changes personality; the evidence is self-ratings only, with no behaviour and no "
    "ratings of personality by others, in selected volunteers (high baseline Openness, spiritually active) and in patients with "
    "treatment-resistant depression, in supported clinical or laboratory settings.")},
   "imprecision": {"levels": 1, "note": (
    "52 and 19 people; the main change has p = 0.023 and the lasting change p = 0.0503 in a subgroup of 30; a few large "
    "individual rises carry much of the mean (about +1.3 without the three largest, editors' approximate calculation); the "
    "randomized comparison prints no values, so its precision cannot be judged.")},
   "publication_bias": {"levels": 0, "note": (
    "Not assessable: neither paper mentions a registration or analysis plan; the 2006 trial did publish its null personality "
    "result.")},
   "large_effect": {"levels": 0},
   "dose_response": {"levels": 0},
   "plausible_confounding": {"levels": 0}
  },
  "certainty": "very-low",
  "reasoning": (
   "The personality estimates are before-and-after changes within the same people, not comparisons between randomized "
   "conditions, so they are rated as observational and start low; rated down two levels for risk of bias and one each for "
   "inconsistency, indirectness and imprecision, which is below the floor: very low. Worded as insufficient evidence on "
   "whether psilocybin changes personality: that self-rated Openness was a few points higher after than before in these two "
   "samples is reported in the statement, not rated as an effect of the drug. Counted once: the 2006 trial supplied 35 of "
   "MacLean's 52 volunteers, so its null comparison and MacLean's rise come largely from the same people; the patient study "
   "is from a London team that includes MacLean's first author, and its Openness rise points the same way under different "
   "conditions. Status contested: the before-and-after rises point one way, and the one randomized comparison, the subgroup "
   "on which the lasting change rests and the two papers' disagreement about the experience point the other; the debate box "
   "sets out both sides. Neither paper checked a change against behaviour.")
 },
 "status": "contested",
 "debate": {
  "question": (
   "Does psilocybin change personality traits such as Openness, or do the before-and-after rises in self-ratings come from "
   "other things: expectations, improving mood, retesting or who volunteers?"),
  "evidence_yes": (
   "In 52 healthy volunteers pooled from two double-blind laboratory trials, self-rated Openness was 2.8 T points higher 1 to "
   "2 months after a high-dose psilocybin session (p = 0.023), while the other four domains, measured with the same "
   "questionnaire, retesting and setting, did not change detectably, and Openness did not change after a first session of "
   "placebo, methylphenidate or a low psilocybin dose (30 people, p = 0.48). The rise was larger the more mystical the session "
   "(r = 0.42) and concentrated in the 30 who had a 'complete mystical experience' (+5.7), whose screening Openness did not "
   "differ from the others', and in them it was still 4.2 points above screening at about 16 months (MacLean et al., 2011). "
   "Under different conditions, in 19 patients with treatment-resistant depression in an open-label study by a London team, "
   "Openness rose 4.9 points at 3 months; this rise did not differ between patients whose depression responded and those "
   "whose did not and did not correlate with depression change, which the authors read as an effect beyond improved mood, "
   "and it was more than three times the average change they computed from antidepressant trials (d 0.44 against 0.13), a "
   "comparison across separate studies (Erritzoe et al., 2018)."),
  "evidence_no": (
   "Neither study compared personality change with a control condition: MacLean et al. tested the change after the high-dose "
   "session and the change after a first session without it separately, never against each other, and Erritzoe et al. had no "
   "control group. In the trial that supplied 35 of MacLean's 52 volunteers, the randomized comparison (15 given psilocybin "
   "first against 15 given methylphenidate first) found no difference in any personality factor at 2 months, and the "
   "methylphenidate-first group did not change after its own psilocybin session (no values printed; Griffiths et al., 2006, as "
   "its checked study card reports). The lasting change rests on p = 0.0503 in a subgroup defined by what happened in the "
   "session, and the change for all participants at follow-up was not reported; about a third of individual changes were "
   "below zero, and without the three largest rises the mean would be about +1.3 (editors' approximate reading of the "
   "figure). The volunteers were unpaid, mostly spiritually active, highly educated people whose Openness was already about "
   "1.3 to 1.5 SDs above the norm, recruited by a study framed around sacramental use, who could probably tell when they had "
   "the high dose; expectations were not measured. In the patients, Neuroticism, Extraversion and Conscientiousness started "
   "far from the norms and moved towards them, as regression and lifting mood would predict, and the authors say it is hard to "
   "infer that these changes are traits rather than states. The two papers disagree on whether the change followed the "
   "experience."),
  "neither_can_show": (
   "Whether behaviour changed: all personality scores are self-reports, and no paper read related them to behaviour or to "
   "ratings by people who know the participants (the 2006 trial's observer ratings of behaviour and attitudes were not linked "
   "to personality scores). Whether changes last beyond about 16 months in the volunteers or 3 months in the patients. Whether "
   "the findings apply to people who are not volunteers for psilocybin research, to use outside a clinic or laboratory, or to "
   "other psychedelics: both studies gave psilocybin with preparation and support."),
  "editors_reading": (
   "Editors' reading (certainty: very low). After psilocybin with preparation and support, people rated themselves a few "
   "points more open to experience 1 to 3 months later, in two small studies, and patients with depression also rated "
   "themselves less anxious and more sociable as their mood improved. That psilocybin itself changed their personality is not "
   "shown: neither study compared the change with a control condition, the one randomized comparison in these trials found no "
   "difference, about a third of the volunteers scored lower afterwards, and no study read checked the scores against what "
   "people do. The rise more than a year later rests on a borderline result in a subgroup."),
  "what_would_settle_it": (
   "A randomized trial comparing psilocybin with an active placebo that people cannot easily tell apart, with personality, "
   "self-rated and rated by people who know the participant, as a pre-registered outcome at baseline and at 1, 6 and at least "
   "12 months, expectations measured beforehand, all five domains analysed for everyone randomized, depression change as a "
   "covariate in patients, and a measure of behaviour; repeated in people not selected for spiritual interest or high "
   "Openness.")
 },
 "verification": verification(
  "Theme 15. Adds three anchors from the checked card sc_griffiths_2006 (one contradicting, two qualifying), whose PDF is no "
  "longer on file: the editor should confirm this use. Not read: Griffiths et al. (2011, Study 2 of MacLean's analysis, cited "
  "in press), the trial reports behind the patient study (Carhart-Harris et al., 2016, Lancet Psychiatry; 2018, "
  "Psychopharmacology), and the LSD studies Erritzoe et al. describe (Carhart-Harris et al., 2016, Psychological Medicine 46, "
  "1379–1390, a small Openness rise at 2 weeks; Schmid & Liechti, 2018, Psychopharmacology 235, 535–545, no rise at 1 and 12 "
  "months); no DOIs are printed for these. The answer on mystical experiences says that personality questionnaires did not "
  "change in the 2006 trial; this answer agrees and says how both findings can stand."),
 "version": "0.1.0",
 "changelog": changelog("MacLean et al. (2011) and Erritzoe et al. (2018), with three anchors from the checked study card "
                        "of Griffiths et al. (2006), whose PDF is not on file"),
}

# ---------------------------------------------------------------------------------------------------------------
# 3. Geometric visuals: a model
# ---------------------------------------------------------------------------------------------------------------
c3 = {
 "id": "cl_xc_visual_patterns",
 "substance": "lsd",
 "section": 4,
 "statement": (
  "Evidence is insufficient to say whether the simple geometric visions seen on psychedelics come from spontaneous patterns "
  "of activity in the primary visual cortex (V1): a mathematical model proposes that they do, the paper tests it against no "
  "measurement in people on a drug (Bressloff et al., 2001), and no such test has been read for this answer. The model "
  "starts from Klüver's sorting of reported geometric "
  "hallucinations into four classes of 'form constants': gratings, lattices, fretworks, filigrees, honeycombs and "
  "chequer-boards; cobwebs; tunnels, funnels, alleys, cones and vessels; and spirals. The paper says such images are seen "
  "after flickering light, certain anaesthetics, deep pressure on the eyeballs, on waking or falling asleep, and shortly "
  "after drugs such as LSD and marijuana, and, citing earlier reports, that they are also seen by blind people and in sealed "
  "dark rooms and keep their positions relative to each other as the eyes move, so that they arise in the brain rather than "
  "the eyes. The model rests on the map from retina to V1, which away from the centre of gaze works like a complex logarithm, "
  "so that circles in the visual field fall on V1 as vertical lines, rays as horizontal lines and logarithmic spirals as "
  "oblique lines, making tunnels, funnels and spirals simple stripes of activity across V1; and on the wiring of V1, with "
  "cells tuned to the orientation of edges, connections within each local patch, and long lateral connections that link "
  "patches of the same orientation preference along the axis of that preference, measured mainly in cats, macaques, owl "
  "monkeys and tree shrews and scaled to human V1 (hypercolumns about 1.33 to 2 mm apart, about 1,300 per hemisphere); it "
  "extends an earlier model by the corresponding author and a colleague (Ermentrout & Cowan, 1979), which had no orientation "
  "tuning and could not produce lattice tunnels, honeycombs, some chequer-boards or cobwebs. When the model's resting state is "
  "made unstable, by raising "
  "excitability or lowering inhibition, which the authors describe as thought to be one possible effect of hallucinogens, a "
  "limited set of repeating patterns can arise: with weak inhibition between neighbouring orientation patches, light-and-dark "
  "patterns that map back to tunnels, funnels and spirals, and with strong inhibition, lattices of oriented edges that map "
  "back to honeycombs, chequer-boards and cobwebs. Its limits: the drug appears only as an abstract excitability setting, "
  "with no receptor, drug or dose, and the same mechanism is offered for flickering light; the match with "
  "hallucinations was judged by eye against a few drawings redrawn from secondary sources; the contour-forming patterns that "
  "match seen form constants needed lateral connections spreading more than 45 degrees from the orientation axis, wider than "
  "the anatomy that motivated the model, whose strict form gave patterns without continuous contours; the expected size of "
  "the patterns rests on an unsourced figure of 30 to 40 repetitions around the visual field (2.4 to 3.2 mm in V1); and some "
  "reported images, including a complex image after LSD, cannot be explained by the simple model, the authors say. The paper "
  "offers predictions, such as orientation changes detectable by optical imaging near the horizontal meridian, that it did "
  "not test. Certainty: very low. Status: single study."),
 "plain": (
  "Why do psychedelic visuals look like tunnels, spirals and honeycombs? A mathematical model suggests the visual brain's own "
  "wiring may shape them. The simple geometric visions people report, after LSD or cannabis but also with flickering light "
  "or on falling asleep, were sorted long ago into four types: lattices such as honeycombs and chequerboards, cobwebs, "
  "tunnels and funnels, and spirals. The wiring from the eye to the brain's first visual area turns a tunnel, a funnel or a "
  "spiral into simple stripes across that area. In the model, when the area becomes too excitable, stripes and lattices of "
  "activity form on their own, shaped by how its cells are connected, and mapped back to what a person would see they look "
  "like all four types. But it is only a model: the drug is just an excitability setting, the wiring was measured mostly in "
  "animals, the match was judged by eye against a few drawings, the best-matching patterns needed wider connections than the "
  "anatomy it was built on, and some complex visions do not fit it. The paper did not test it against brain activity "
  "measured in people on a drug."),
 "population": (
  "No participants: a mathematical model of human primary visual cortex (V1), built from anatomical and physiological "
  "findings in cats, macaques, owl monkeys and tree shrews (partly unpublished, cited as personal communications) and from "
  "estimates of human V1 size and hypercolumn spacing, and compared with published drawings and descriptions of geometric "
  "hallucinations."),
 "exposure": (
  "In the model, a rise in network excitability (stronger global coupling, or a steeper neural response through a steady "
  "input) or a fall in local inhibition, which the authors describe as one possible effect of hallucinogens and also apply "
  "to flickering light; no drug, receptor or dose is modelled."),
 "comparator": (
  "The model's uniform resting state, and the earlier Ermentrout–Cowan model without orientation tuning; for the "
  "hallucinations, comparison by eye with a few drawings."),
 "outcome": (
  "Which repeating (doubly periodic) patterns of V1 activity can emerge when the resting state becomes unstable, which of "
  "them are stable, and what they would look like in the visual field after an inverse retinocortical map; resemblance to "
  "Klüver's four classes of form constants, judged by eye."),
 "relation": "insufficient-evidence",
 "magnitude": (
  "No statistical estimates. Retinocortical map constants w0 = 0.087 and epsilon = 0.051 (estimated from Drasdo, 1977); "
  "orientation preference repeating about every 300 µm in cat V1 and 0.5 mm in macaque V1; 20% of lateral connections ending "
  "on inhibitory cells; human V1 about 3,500 mm² per hemisphere, hypercolumn spacing about 1.33–2 mm, about 1,300 "
  "hypercolumns; critical wavelength given as about 2.66 mm (2π × 0.400 / qc at qc = 1 gives 2.51 mm, editors' calculation); "
  "30–40 repetitions around the visual field for commonly reported hallucinations (unsourced), corresponding to 2.4–3.2 mm in "
  "V1; contour-forming (even) patterns need lateral spread beyond 45 degrees (theta0 > π/4)."),
 "evidence": [
  anchor("bressloff_2001", "sc_bressloff_2001", "pp. 299–300",
   "Abstract, 1st and 3rd paragraphs (p. 299) and last paragraph (p. 300)",
   "The paper takes Klüver's four classes of form constants ((i) gratings, lattices, fretworks, filigrees, honeycombs and "
   "chequer-boards; (ii) cobwebs; (iii) tunnels, funnels, alleys, cones and vessels; (iv) spirals) and investigates "
   "mathematically the assumption that the retina-to-V1 map and V1's local and lateral circuits determine their geometry. It "
   "studies the patterns that emerge when the model's dynamics become unstable under the presumed action of hallucinogens or "
   "flickering lights and, given the authors' interpretation of the correspondence between V1 patterns and percepts, finds "
   "representatives of all the form constants; the results are sensitive to the detailed specification of the lateral "
   "connectivity, and the authors present a link to the processing of edges and contours as an interesting possibility if the "
   "mechanism is sited mainly in V1.",
   "supports", SRC_B),
  anchor("bressloff_2001", "sc_bressloff_2001", "pp. 300–301",
   "1. Introduction › (a) Form constants and visual imagery: paragraphs on the conditions, on Klüver's classes and on blind "
   "subjects (p. 300) and the last paragraph (p. 300, continuing on p. 301)",
   "Geometric visual hallucinations are described as seen after flickering lights, certain anaesthetics, on waking or falling "
   "asleep, after deep binocular pressure on the eyeballs, and shortly after drugs such as LSD and marijuana; patterns that "
   "may be hallucinatory are found in petroglyphs and cave paintings. Citing earlier reports (Krill et al., 1963; Klüver, "
   "1966), the paper says such images are seen by blind subjects and in sealed dark rooms and move with the eyes while "
   "keeping their positions relative to each other, suggesting they are generated in the brain rather than the eyes; in the "
   "authors' view, in V1, stabilized by V2 and elsewhere. The premise that all observers report Klüver's form constants or "
   "variations carries no source; continuity across the midline and stability in the visual field are deferred to a later "
   "study.",
   "qualifies", SRC_B),
  anchor("bressloff_2001", "sc_bressloff_2001", "pp. 302–303",
   "1. Introduction › (b) The human retinocortical map (p. 302); (c) Form constants as spontaneous cortical patterns, 1st "
   "and 2nd paragraphs, and (d) Orientation tuning in V1, 1st paragraph (p. 303); Figures 6 and 7 (p. 303)",
   "Away from the fovea the retina-to-V1 map is a scaled complex logarithm (constants w0 = 0.087 and epsilon = 0.051 from "
   "Drasdo, 1977): circles in the visual field become vertical lines in V1, rays horizontal lines and logarithmic spirals "
   "oblique lines, so tunnel, funnel and spiral form constants correspond to stripes of activity at various angles in V1. "
   "Ermentrout & Cowan (1979) proposed that such stripes form spontaneously under hallucinogens through a Turing-like "
   "instability in a sheet of excitatory and inhibitory neurons; without orientation tuning, that model cannot produce lattice "
   "tunnels, honeycombs, certain chequer-boards or cobwebs.",
   "supports", SRC_B),
  anchor("bressloff_2001", "sc_bressloff_2001", "pp. 303–305",
   "1. Introduction › (d) Orientation tuning in V1, from the 2nd paragraph to the end of the subsection (pp. 303–304); "
   "Figures 8–10 (pp. 304–305); 2. A model of V1 › (a) The model, left column (p. 305)",
   "Orientation preference repeats about every 300 µm in cat V1 and about every 0.5 mm in macaque V1; cells less than 0.5 mm "
   "apart connect roughly isotropically, while long horizontal axons in layers II and III contact patches of similar "
   "orientation about every 0.5 mm along the axis of their orientation preference (owl monkey and tree shrew images, partly "
   "a personal communication); these come almost entirely from excitatory neurons, 20% ending on inhibitory cells. Some "
   "anatomical and psychophysical evidence puts human hypercolumn spacing at about 1.33–2 mm; with a human V1 of about "
   "3,500 mm² per hemisphere and hypercolumns of about 2.67 mm², about 1,300 hypercolumns. The model assumes all orientations "
   "at every position and a continuum, although many hallucination patterns have wavelengths of about twice the hypercolumn "
   "spacing.",
   "supports", SRC_B),
  anchor("bressloff_2001", "sc_bressloff_2001", "p. 311",
   "3. Linear stability analysis › (c) Marginal stability › (i) Choosing the bifurcation parameter",
   "The instability is induced by raising the global coupling parameter or, equivalently, the slope of the neural output "
   "function through a steady input, which changes network excitability, described as thought to be one of the possible "
   "effects of hallucinogens; hallucinogens might also act indirectly on the relative levels of inhibition. No receptor, drug "
   "or dose enters the model.",
   "qualifies", SRC_B),
  anchor("bressloff_2001", "sc_bressloff_2001", "pp. 312, 324",
   "3. Linear stability analysis › (d) The Ermentrout–Cowan model revisited (p. 312); 7. Discussion, item (i) of the second "
   "list (p. 324)",
   "If inhibition between neighbouring orientation patches is weak, V1 behaves without intrinsic orientation tuning and "
   "non-contoured patterns (contrasting regions of light and dark) arise, corresponding to tunnels, funnels and spirals; if it "
   "is strong, contoured patterns (lattices of oriented edges) arise, corresponding to honeycombs, chequer-boards and "
   "cobwebs. All but the square patterns are stable; the authors say hallucinations resembling square patterns exist and may "
   "be transitional forms.",
   "supports", SRC_B),
  anchor("bressloff_2001", "sc_bressloff_2001", "pp. 311, 317, 324",
   "3(c), right-column paragraph beginning 'An interesting question', and Figure 17 (p. 311); 5(b) Planforms in the visual "
   "field, last paragraph (p. 317); 7. Discussion, item (ii) of the second list (p. 324)",
   "With lateral connections running strictly along the axis of orientation preference and acting as inhibitory, the 'odd' "
   "contoured patterns are selected, and these do not form continuous contours; the contour-completing 'even' patterns, which "
   "recover the form constants missing from the earlier model, appear when the lateral connections spread more than 45 "
   "degrees (theta0 > π/4) from that axis.",
   "qualifies", SRC_B),
  anchor("bressloff_2001", "sc_bressloff_2001", "pp. 301–302, 317",
   "Figures 1–4 and captions (pp. 301–302); 5(b) Planforms in the visual field, right column, text after equation (45) and "
   "last paragraph (p. 317)",
   "The hallucination images used for comparison are drawings redrawn from secondary sources: a pressure phosphene (Tyler, "
   "1978), a honeycomb attributed to marijuana (Clottes & Lewis-Williams, 1998), funnels and spirals attributed to LSD (Oster, "
   "1970; Siegel, 1977) and a cobweb petroglyph (Patterson, 1992). The reader is invited to compare, for example, the pressure "
   "phosphene with one model pattern and the cobweb with another; no measure of fit is given. Commonly reported hallucination "
   "patterns are said to show 30–40 repetitions around the visual field, corresponding to 2.4–3.2 mm in V1, the range expected "
   "for the model's critical wavelength; this figure has no source.",
   "qualifies", SRC_B),
  anchor("bressloff_2001", "sc_bressloff_2001", "pp. 323–324",
   "7. Discussion, 1st paragraph (p. 323) and item (ii) of the second list (p. 324)",
   "The authors present the model as showing that common hallucinatory images can be generated by a biologically plausible "
   "architecture, with the instability presumed to occur shortly after hallucinogens act on brain-stem nuclei that control "
   "cortical excitability; the Discussion concludes that V1 circuits normally involved in detecting oriented edges and "
   "processing contours are also responsible for generating the form constants, a firmer wording than the abstract's "
   "'interesting possibility'.",
   "qualifies", SRC_B),
  anchor("bressloff_2001", "sc_bressloff_2001", "pp. 312, 325–326",
   "4. Doubly periodic planforms, 1st paragraph (p. 312); 7. Discussion, item (iv) of the second list (pp. 325–326)",
   "Restricting the solutions to doubly periodic patterns is standard but, the authors write, has no formal justification. "
   "Many variants of the form constants cannot be understood in terms of the simple model: a tunnel with reversed "
   "magnification (possibly involving circuits beyond V1, such as dorsal MSTd), a lattice-tunnel attributed to marijuana "
   "(possibly a mismatch with a disordered cortical lattice) and a complex image after LSD, which does not fit a form constant "
   "well and may involve two length-scales, beyond the scope of the model.",
   "qualifies", SRC_B),
  anchor("bressloff_2001", "sc_bressloff_2001", "pp. 324–325",
   "7. Discussion, item (ii) of the first list (p. 324) and the paragraph on two further scenarios after item (ii) of the "
   "second list (p. 324, continuing on p. 325)",
   "Predictions offered for testing: if V1 implements the double retinocortical map, cells tuned to the same relative angle "
   "should be preferentially connected, and orientation changes should be relatively large and detectable with optical "
   "imaging near the horizontal meridian; reports that a bright white light at the centre of the visual field expands into a "
   "hallucination in about 3 seconds after LSD and similar drugs would correspond to activity spreading across V1 at about "
   "2.4 cm per second. None is tested in the paper.",
   "qualifies", SRC_B),
 ],
 "grade": {
  "starting_level": "low",
  "domains": {
   "risk_of_bias": {"levels": 1, "note": (
    "No validated instrument exists for a theoretical model; on the card's checklist the comparison with hallucinations is "
    "high risk: it is by eye, against a few drawings redrawn from secondary sources (popular-science articles, a petroglyph, "
    "cave-art illustrations), with no measure of fit; two premises have no source (that all observers report Klüver's form "
    "constants, and the 30 to 40 repetitions that set the expected scale); and the results are sensitive to the assumed "
    "lateral connectivity, the contour-forming patterns appearing only with lateral spread wider than the anatomy that "
    "motivated the model. The mathematics itself is printed in full.")},
   "inconsistency": {"levels": 0, "note": "One model; no competing model is developed or compared."},
   "indirectness": {"levels": 1, "note": (
    "No measurement in people, and none during drug use: the drug enters only as an abstract rise in excitability or fall in "
    "inhibition, the same mechanism the paper offers for flickering light, and the anatomy comes mainly from "
    "cats, macaques, owl monkeys and tree shrews (partly unpublished), scaled to human V1.")},
   "imprecision": {"levels": 0, "note": "No estimates; not applicable."},
   "publication_bias": {"levels": 0, "note": "Not applicable to a single theoretical paper."},
   "large_effect": {"levels": 0},
   "dose_response": {"levels": 0},
   "plausible_confounding": {"levels": 0}
  },
  "certainty": "very-low",
  "reasoning": (
   "A theoretical model is not evidence from measurement and starts low; rated down one level for risk of bias (the fit to "
   "hallucinations judged by eye against a few redrawn images, unsourced premises, sensitivity to the assumed connectivity) "
   "and one for indirectness (no human or drug data; the drug as an abstract parameter; animal anatomy), which is below the "
   "floor: very low. Worded as insufficient evidence on whether psychedelic geometric visuals arise this way: what the model "
   "proposes, what it rests on and what it predicts are reported as such, not rated as findings about the brain. Status single "
   "study: one modelling paper; it extends the corresponding author's earlier model (Ermentrout & Cowan, 1979), which is not "
   "counted as independent support, and no empirical test of its predictions has been read.")
 },
 "status": "single-study",
 "verification": verification(
  "Theme 35. Not read: Klüver (1966), the source of the four classes; Ermentrout & Cowan (1979); Bressloff et al. (2000b), "
  "to which the fuller stability analysis is deferred; and any study that imaged visual cortex during geometric "
  "hallucinations (for example the LSD brain-imaging study named in the demand file, Carhart-Harris et al., 2016), which "
  "would be the first test in people. No DOIs are printed in the paper for these. The card and the PDF agree on every "
  "number used."),
 "version": "0.1.0",
 "changelog": changelog("Bressloff et al. (2001)"),
}

claims = [c1, c2, c3]

# ---------------------------------------------------------------------------------------------------------------
# Plain lines
# ---------------------------------------------------------------------------------------------------------------
V = "0.1.0"
simple = {
 "claims": {
  "cl_xc_psychedelic_beliefs": {
   "q": "Do trips show you the truth, or just change your beliefs?",
   "pages": ["psilocybin", "lsd", "dmt-ayahuasca", "general"],
   "short": ("These studies can't say if it's the truth. But beliefs do shift a bit, towards ideas like other worlds and a "
             "conscious universe. The shift was still there 6 months later."),
   "but": "There was no comparison group, and only 122 of over 800 people answered every survey. Most already leaned that way.",
   "how": [
    ("People answered questions a week before a psychedelic retreat or ceremony, then 4 weeks and 6 months after. In the "
     "122 who answered all three, belief in things like other worlds rose a little."),
    ("First-timers shifted more. In one exploratory analysis, the shift went with feeling in tune with the group, not "
     "clearly with how mystical or visual the trip felt."),
    ("In a trial in depression, beliefs shifted after psilocybin. They shifted a little after a standard antidepressant too, "
     "and the gap was too small to be sure of."),
    ("A survey asked 1,606 people whose beliefs had changed to look back, about 8 years on average. 26 in 100 recalled "
     "thinking plants could be conscious before, and 61 in 100 after. Superstitions, like black cats bringing bad luck, "
     "didn't rise."),
   ],
   "how_src": [["timmermann_2021"], ["timmermann_2021"], ["timmermann_2021"], ["nayak_2022"]],
   "rate": ("Mostly one study with no comparison group, where most people stopped answering, plus a small trial and a survey "
            "of people chosen because their beliefs had changed. None can say whether the beliefs are true."),
   "v": V,
  },
  "cl_psi_personality": {
   "q": "Can psilocybin change your personality?",
   "pages": ["psilocybin", "general"],
   "short": ("Not proven. After psilocybin, people rated themselves about 3 to 5 points more 'open' 1 to 3 months later, on "
             "a scale where the average adult scores 50."),
   "but": ("These were people rating themselves, before and after. The one test against another drug found no difference. "
           "Neither study checked how people acted."),
   "how": [
    ("52 healthy volunteers, new to psychedelics and mostly religious or spiritual, rated themselves 2.8 points more open 1 "
     "to 2 months after their psilocybin session. Their other four traits didn't clearly change."),
    ("The rise came from the 30 who had a full mystical experience, and about a third of all the volunteers scored lower "
     "afterwards. Over a year later, that group was still about 4 points up, a result right on the edge of chance."),
    ("Most of them came from one trial. There, 15 people who got psilocybin first and 15 who got a stimulant first scored "
     "no differently on personality 2 months later."),
    ("In 19 patients with hard-to-treat depression, openness rose 4.9 points by 3 months, and they rated themselves less "
     "anxious and more sociable. The researchers say mood may explain those last two changes."),
   ],
   "how_src": [["maclean_2011"], ["maclean_2011"], ["griffiths_2006"], ["erritzoe_2018"]],
   "rate": ("Two small before-and-after studies of selected volunteers and patients rating themselves. The one test against "
            "another drug found no difference. Both sides are below."),
   "v": V,
  },
  "cl_xc_visual_patterns": {
   "q": "Why do psychedelic visuals look like tunnels, spirals and honeycombs?",
   "pages": ["lsd", "psilocybin", "mescaline", "dmt-ayahuasca"],
   "short": ("Maybe the visual brain's own wiring. A maths model shows how tunnels, spirals, cobwebs and honeycombs could "
             "arise there. It wasn't tested in people on a drug."),
   "but": ("It's only maths: the drug is just a setting for how excitable the brain is. The match was judged by eye against "
           "a few drawings."),
   "how": [
    ("People see simple shapes after LSD or cannabis. They also come with flickering light or when falling asleep. Long "
     "ago, these were sorted into four types: lattices and honeycombs, cobwebs, tunnels, and spirals."),
    ("The wiring from eye to brain turns a tunnel or a spiral into plain stripes. These run across the brain's first area "
     "for sight."),
    ("In the model, when that area gets too excitable, stripes and lattices of activity form by themselves, shaped by how "
     "its cells connect. Mapped back to what you'd see, they look like all four types."),
    ("The wiring data came mostly from cats and monkeys. The best matches needed wider connections than that anatomy shows, "
     "and some complex visions don't fit the model."),
   ],
   "how_src": [["bressloff_2001"], ["bressloff_2001"], ["bressloff_2001"], ["bressloff_2001"]],
   "rate": ("One maths model, built on brain wiring measured mostly in animals and checked by eye against a few drawings. "
            "It wasn't tested against brain activity in people on a drug."),
   "v": V,
  },
 },
 "tf": {
  "general": [
   {"claim": "cl_xc_psychedelic_beliefs",
    "statement": "Beliefs can shift after a psychedelic retreat and still be shifted 6 months on.",
    "answer": True, "v": V,
    "why": ("In one study, belief in things like other worlds rose a little and was still up 6 months on. But only 122 of "
            "over 800 people answered every survey, and most already leaned that way.")},
   {"claim": "cl_psi_personality",
    "statement": "It's been shown that psilocybin can change your personality.",
    "answer": False, "v": V,
    "why": ("Not proven. People rated themselves a little more open after, but the one test against another drug found no "
            "difference.")},
  ],
  "lsd": [
   {"claim": "cl_xc_psychedelic_beliefs",
    "statement": "People whose beliefs change after a trip start to believe in bad luck too.",
    "answer": False, "v": V,
    "why": ("In a survey of 1,606 such people, belief in bad luck from black cats didn't rise. Belief that plants can be "
            "conscious did, as they recalled it years later.")},
   {"claim": "cl_xc_visual_patterns",
    "statement": "The simple shapes people see on LSD have been sorted into just four types.",
    "answer": True, "v": V,
    "why": ("Lattices and honeycombs, cobwebs, tunnels, and spirals. Similar visions also come with flickering light or when "
            "falling asleep.")},
  ],
  "psilocybin": [
   {"claim": "cl_psi_personality",
    "statement": "In a lab study, all who took psilocybin came out more 'open'.",
    "answer": False, "v": V,
    "why": "About a third of the volunteers scored lower afterwards. On average, scores rose by under 3 points."},
  ],
  "mescaline": [
   {"claim": "cl_xc_visual_patterns",
    "statement": "It's proven that trip tunnels and spirals come from the brain's wiring.",
    "answer": False, "v": V,
    "why": "A maths model suggests it, but it wasn't tested in people on a drug."},
  ],
 },
}


# ---------------------------------------------------------------------------------------------------------------
# Checks and output
# ---------------------------------------------------------------------------------------------------------------
def syl(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    m = re.findall(r"[aeiouy]{1,2}", w)
    return len(m) if m else 1


def grade(t):
    words = [x for x in t.split() if x]
    sents = max(1, len(re.findall(r"[.!?]+", t)))
    sy = sum(syl(w) for w in words)
    return 0.39 * len(words) / sents + 11.8 * sy / len(words) - 15.59


if __name__ == "__main__":
    out_claims = ROOT + "/data/claims/_incoming/pdf1114_w681.json"
    out_simple = ROOT + "/data/verification/pdf-2026-11-14/681_simple.json"
    for c in claims:
        for f in ("statement", "plain", "population", "exposure", "comparator", "outcome", "magnitude"):
            if re.search(r"\b(non-)?users?\b", c[f].lower()):
                print("WARN user(s) in", c["id"], f)
        q = [e.get("quote") for e in c["evidence"] if e.get("quote")]
        print(c["id"], "anchors", len(c["evidence"]), "statement words", len(c["statement"].split()),
              "plain words", len(c["plain"].split()))
    for cid, s in simple["claims"].items():
        print(cid, "| q words", len(s["q"].split()), "| short words", len(s["short"].split()),
              "grade %.1f" % grade(s["short"]), "| but grade %.1f" % grade(s["but"]),
              "| rate words", len(s["rate"].split()))
        for i, h in enumerate(s["how"]):
            print("   how[%d] grade %.1f words %d" % (i, grade(h), len(h.split())))
        assert len(s["how"]) == len(s["how_src"])
    for page, items in simple["tf"].items():
        for it in items:
            print("tf", page, it["claim"], "grade %.1f" % grade(it["statement"]), "words", len(it["statement"].split()))
    if "--write" in sys.argv:
        with open(out_claims, "w", encoding="utf-8") as fh:
            json.dump(claims, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        with open(out_simple, "w", encoding="utf-8") as fh:
            json.dump(simple, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        print("written", out_claims, out_simple)
