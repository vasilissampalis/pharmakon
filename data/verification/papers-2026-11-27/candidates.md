# Papers for the next round, most-asked questions first

Paper finder, 27 November 2026. 32 papers for 15 questions; the full records are in `candidates.json` (same order). ★ = save
first for that question. No paper was read; none is in the library (`data/references/*.json`, the 59 files of
`papers-2026-11-26/manifest.json`, the study cards), checked by DOI and by title.

**Order.** Questions are ranked by their theme's share of all questions asked (`data/verification/demand-themes.md`, the
basis of `data/site/demand.json`), then by the question's own forum views or the number of times it appears in the 400
forum questions of the gold sample. "Unanswered" means still on the public list in the build of 27 November
(`site/dist/data/insight.json`: 33 of the 52 items in `wanted.json`), or on forums.md's list of the most-read unanswered
questions. Questions 3 and 13 already have draft answers that wait for a paper the writers asked for.

**Checks.** Crossref was not reachable from this session (the proxy refused api.crossref.org, HTTP 403), so no Crossref
record was fetched. Every detail was seen in WebSearch results (titles and links only) or in the Europe PMC records that
the machine lane keeps in `data/auto/`. The `confirmed` field of each record says what was seen where. "Not seen" marks a
detail written from the paper's usual citation that no result showed (mostly pages and later authors): check those
against Crossref when the PDFs arrive. Six papers have no DOI here because none was seen, and none was guessed: Kurtz
2011, Zeifman 2022, Odell 2015, Cone 1991, and the two CDC reports (given by their CDC links). Retractions were not
checked (Crossref blocked); one correction was seen: Zeifman 2022 has a published corrigendum.

## By question

**1. What is 6-APB (Benzo Fury) like, how does it compare with MDMA, and how risky is it?**
Demand: research chemicals are the most-asked theme the site answers (3.7% of all questions, only 2 answers); on
Bluelight the 6-APB thread has 2.0 million views and 5-MAPB 535,000 (megathreads inflate these). Nothing on benzofurans
is on file.
- ★ Kamour et al. (2014), *Clinical Toxicology*: UK poisons-service enquiries about people unwell after benzofurans; the
  only series in people found.
- Rickli et al. (2015), *British Journal of Pharmacology*: how benzofurans act beside MDMA (cell studies, not people).
- Nugteren-van Lonkhuyzen et al. (2015), *Drug and Alcohol Dependence*: review of benzofurans, 2C-B and 4-FA (effects,
  poisonings, deaths). It serves the 2C-x page too.

**2. What is 1P-LSD, and how does it compare with LSD?**
Demand: research chemicals again; 1P-LSD 588,000 views, other LSD analogues 224,000 to 356,000 each, new tryptamines such
as 4-AcO-DMT 330,000. Nothing on file.
- ★ Grumann et al. (2020), *Drug Testing and Analysis*: 1P-LSD given to people: whether the body turns it into LSD, and
  what they felt. Use only that: its comparison of oral and injected use belongs to section 7.
- Mallaroni et al. (2022), *Psychopharmacology*: how people describe new lysergamides, tryptamines and phenethylamines
  beside LSD and mushrooms.

**3. Can a pill's logo or look tell you what's in it?** (answered, very low)
Demand: theme 4, 3.4% of questions. Writer 754, checker 782 and the editor asked for this one paper.
- ★ Cole et al. (2002), *Addiction*: how much the contents of tablets with the same look varied (DOI found:
  10.1046/j.1360-0443.2002.00222.x).

**4. How is MDMA different from meth or speed?**
Demand: theme 5, 3.0% of questions; on the public list. On file: only Bedi 2010.
- ★ Kirkpatrick et al. (2012), *Psychopharmacology*: Carl Hart's laboratory gave the same people MDMA and methamphetamine,
  blind.
- Holze et al. (2020), *Neuropsychopharmacology*: MDMA beside d-amphetamine (and LSD) in one crossover.
- Bershad et al. (2016), *Journal of Psychopharmacology*: review of whether MDMA's social effects differ from other
  stimulants'.

**5. What happens if you take Xanax with coke or Adderall?**
Demand: theme 7 (risky mixes), 2.8%; 616,000 views (with cocaine) and 421,000 (with Adderall) on Bluelight; writer 759:
the most-read part of the mixing question, and nothing on file studies the two together.
- ★ Votaw et al. (2019), *Drug and Alcohol Dependence*: systematic review of who misuses benzodiazepines, why, and with
  which other drugs.
- Rush et al. (2004), *Journal of Clinical Psychopharmacology*: the one controlled study found of alprazolam given with
  an amphetamine. Its finding must be written as a risk fact (one drug hiding the other), never as a way to take the edge
  off.
- Kurtz et al. (2011), *Drug and Alcohol Dependence*: benzodiazepine dependence among young adults in the club scene who
  use several drugs. No DOI seen. The same team's 2017 paper (*Journal of Psychoactive Drugs*, 49(1),
  10.1080/02791072.2016.1269978, DOI seen) is an alternative.
- Kleinman & Weiss (2022), *Journal of General Internal Medicine*: US deaths involving benzodiazepines, 2000–2019, and the
  other drugs involved. The reader checks whether stimulants are counted apart. Not found: a laboratory study of a
  benzodiazepine with cocaine.

**6. Can psychedelics ease anxiety and depression in people with cancer or another serious illness?**
Demand: theme 13, 2.1%; on the public list. The Cochrane review (Schipper 2024) is in the library; its trials are not.
- ★ Griffiths et al. (2016), *Journal of Psychopharmacology*: double-blind trial in life-threatening cancer, six months.
- Ross et al. (2016), *Journal of Psychopharmacology*: the second trial, against an active placebo, with crossover.

**7. Can psilocybin therapy make depression or suicidal thoughts worse?**
Demand: theme 13; on the public list. On file: Goodwin 2022 and comments on it, but no meta-analysis.
- ★ Hinkle et al. (2024), *JAMA Psychiatry*: meta-analysis of adverse events in classic-psychedelic studies, serious ones
  included.
- Zeifman et al. (2022), *Journal of Clinical Psychiatry*: individual data pooled across trials on suicidal thoughts
  (save the corrigendum with it; no DOI seen).

**8. Does cannabis make sex better?**
Demand: theme 14, 2.0%, with only one answer (on MDMA); the senior author asked it on the site on 17 November.
- ★ Pizzol et al. (2019), *American Journal of Men's Health*: systematic review and meta-analysis on cannabis and erectile
  dysfunction.
- Moser et al. (2023), *Journal of Cannabis Research*: the newest study found on cannabis and desire, orgasm and
  satisfaction (the reader states its design).
- Lynn et al. (2019), *Sexual Medicine*: women at one clinic who used cannabis before sex, beside those who did not.

**9. What happens after naloxone (Narcan): withdrawal, and can the overdose come back?**
Demand: theme 16, 1.8%; on the public list. On file: McDonald 2016 (withdrawal counts), White 1999 (no figures on
overdose coming back).
- ★ Willman et al. (2017), *Clinical Toxicology*: systematic review of how often poisoning came back after naloxone in
  heroin overdose (a letter and the authors' reply followed in 55(4)).
- Neale & Strang (2015), *Addiction*: the withdrawal and other harms people describe after naloxone.

**10. Is sugar really as addictive as cocaine?**
Demand: theme 19 (myths), 1.5%; on the public list. On file: one rat study (Lenoir 2007).
- ★ Westwater et al. (2016), *European Journal of Nutrition*: review of the evidence in animals and in people.
- Markus et al. (2017), *Appetite*: a human study of whether addiction-like eating is about sugar or about eating.

**11. How long does weed stay in your system?**
Demand: theme 20, 1.4%; the listed question asked most often in the forum sample (6 times in 400). Writer 763: Goodwin
2008's averages are minimums.
- ★ Ellis et al. (1985), *Clinical Pharmacology & Therapeutics*: heavy users watched after their last use; the longest
  windows reported.
- Odell et al. (2015), *Forensic Science International*: heavy users after stopping: blood, urine and saliva (no DOI
  seen).
- Lead, not listed: a 2026 systematic review, "Urinary Δ9-tetrahydrocannabinol and metabolite concentrations following
  cannabis use" (*Pharmacological Research*; PubMed 41707818). No search result showed its authors or DOI. Once the
  editor has its record, it should be saved first for this question.

**12. How long does heroin show up on a drug test?**
Demand: theme 20; its most-viewed question (Bluelight). The existing answer gives heroin's marker only from reviews.
- ★ Cone et al. (1991), *Journal of Analytical Toxicology*: volunteers given heroin under study conditions: how long
  6-acetylmorphine stayed in urine (no DOI seen). Not found in any search: Smith et al. (2001), the later study of heroin
  marker profiles, so it is not listed.

**13. Can medicines cause a false positive on a drug test?** (answered, draft)
Demand: theme 20; 19 forum questions on false positives. The two reviews disagree on efavirenz.
- ★ Blank et al. (2009), *Clinical Infectious Diseases*: efavirenz and benzodiazepine screens (DOI found: 10.1086/599109).

**14. How can you die from alcohol?**
Demand: theme 42, 0.8%; on the public list; the senior author's own question. No paper on alcohol poisoning on file.
- ★ Kanny et al. (2015), *MMWR*: US deaths from alcohol poisoning itself, 2010–2012 (a CDC report, no DOI).
- Esser et al. (2024), *MMWR*: US deaths caused by drinking, 2016–2021, by cause (CDC link given; DOI not seen).
- Vonghia et al. (2008), *European Journal of Internal Medicine*: what alcohol poisoning does in the body. Findings only:
  no blood-alcohol levels written as amounts.

**15. Can antidepressants like amitriptyline get you high, and is it risky?**
Demand: theme 59, 0.6%, with no answer at all; amitriptyline 381,000 views, fluoxetine 277,000, citalopram 241,000.
- ★ Evans & Sullivan (2014), *Substance Abuse and Rehabilitation*: review of antidepressant misuse, who, why and harms.

## Not on this list, and why

- **Already in the library:** Anthony 1994 (the heroin dependence figure writer 752 wants) and Moeller 2017 (heroin
  detection) are on file and need no saving.
- **Answerable from cards already on file** (gap finder 711), so they need no new paper: fake Xanax bars (one card's PDF,
  Morrison 2025, is not on file: re-save it), how often drugs are mis-sold, how an opioid overdose kills, whether a
  heroin overdose leaves time, overamping, which drug is most addictive, kratom's side effects.
- **Waiting for the senior author:** coming off antipsychotic depot injections (4.3 million views; his decision); "Does
  cannabis cause cancer?" (`cl_can_smoked_cancer`, his section 7 approval); the four questions about amounts (machine
  lane only).
- **No paper found:** why cannabis makes some people shake (430,000 views; a search found only general reviews; the
  anxiety part is in cards on file); whether 5-HTP or vitamins protect after MDMA (no trial in people known).
- **Next in line if there is room:** "Can you overdose on LSD?" (Nichols & Grob 2018, *Forensic Science International*,
  10.1016/j.forsciint.2018.01.006, from the lane's Europe PMC record); Halberstadt et al. (2020), *Neuropharmacology*,
  on 1P-LSD and ALD-52 as forms the body turns into LSD (no DOI seen); Greene et al. (2019), *Emergency Medicine
  Journal*, 36(4), deaths after "treat and release" (no DOI seen); kratom dependence in clinical samples; ego death
  (nothing on file).
