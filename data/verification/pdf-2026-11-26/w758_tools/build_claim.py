"""Builds data/claims/_incoming/pdf1126_w758.json (claim writer 758, round pdf-2026-11-26)."""
import json, sys

OUT = sys.argv[1]

EVOY_SRC = ("PDF PDFs/_Cross-cutting/Evoy_2021_GabapentinoidMisuseSRUpdate.pdf (Springer online-first version, "
            "no journal page numbers; the issue version, Drugs 81(1):125–156, not seen): all text pages read; the "
            "Table 1 rows used checked on 200-dpi renderings of PDF pp. 4, 9, 10, 12, 13 and 15–19; reference list "
            "PDF pp. 30–31")
BON17_SRC = ("PDF PDFs/_Cross-cutting/Bonnet_2017_HowAddictiveGabapentinoidsSR.pdf (Elsevier article-in-press "
             "version with its own pages 1–31; the issue version, 27(12):1185–1215, not seen): text pp. 1–4, 13 and "
             "21–26 read on 100-dpi renderings and as text; the Table 1 and Table 3 rows used checked on 200-dpi "
             "renderings of PDF pp. 5–7, 16–17 and 19–20")
BON21_SRC = ("PDF PDFs/_Cross-cutting/Bonnet_2021_CommentGabapentinoidSR.pdf (version of record, Drugs "
             "2021;81:611–614): all four pages read on rendered pages and as text")
LB = "AI reader 758 (claim writer), from the PDF"


def a(ref, card, page, locator, extracted, role, src, located_by=LB, quote=None):
    d = {"reference": ref, "study_card": card, "page": page, "locator": locator, "extracted": extracted,
         "role": role, "anchor_status": "ai-located", "located_by": located_by, "source_read": src}
    if quote:
        d["quote"] = quote
    return d


E, B, L = "evoy_2021", "bonnet_2017", "bonnet_2021"
EC, BC, LC = "sc_evoy_2021", "sc_bonnet_2017", "sc_bonnet_2021"

evidence = [
    # ---- Evoy et al. (2021), systematic review update ----
    a(E, EC, "PDF pp. 1–3",
      "Abstract (Methods, Results) (PDF p. 1); 2.1; 2.2, 1st and 2nd paragraphs; 2.3; 3 Results, 1st paragraph (PDF p. 2); Fig. 1 (PDF p. 3)",
      "Update of the authors' 2017 review: PubMed searched for studies published 29 July 2016 to 31 August 2020, with "
      "ClinicalTrials.gov, the Cochrane Library and reference lists; English-language studies with original data on "
      "gabapentinoid abuse, misuse or overdose; 55 included (46 observational studies and 10 case reports or series, "
      "one manuscript in both; 29 from North America, 28 of them from the USA, 17 Europe, 6 Asia, 3 Australia; 20 on "
      "gabapentin only, 18 pregabalin only, 17 both). The synthesis is qualitative only: bias was assessed "
      "qualitatively in a limitations column of Table 1, with no appraisal tool and no pooling.",
      "qualifies", EVOY_SRC),
    a(E, EC, "PDF pp. 9, 12, 13, 16, 19, 21",
      "Table 1: Dahlman et al. [17] (PDF p. 9), Ianni et al. [27] (PDF p. 12), Mutschler et al. [30] (PDF p. 13), "
      "Sason et al. [35] (PDF p. 16), Wagner et al. [44] (PDF p. 19); 4.1, 2nd paragraph (PDF p. 21)",
      "People in opioid maintenance treatment: non-prescribed pregabalin in 17.7% of 300 in Israel (one urine test per "
      "patient, 2017); pregabalin in 18.8% and gabapentin in 1% of 388 in two German centres (oral-fluid screening; "
      "Table 1 says tested positive, the text says non-prescribed); pregabalin in 10.7% of 140 Italian patients not "
      "prescribed it (hair testing; 4.29% of 140 people using drugs outside treatment, p = 0.041); none of 109 in "
      "Switzerland (self-report and hair); lifetime non-medical pregabalin use reported by 21% of 73 in Sweden (36% "
      "reported any lifetime use).",
      "supports", EVOY_SRC),
    a(E, EC, "PDF pp. 17, 20–21, 27",
      "Table 1, Snellgrove et al. [38] (PDF p. 17); 3.1.2, 1st paragraph (PDF pp. 3, 20); 4.1, 2nd paragraph (PDF p. 21); "
      "4.5, 4th paragraph (PDF p. 27)",
      "German detoxification ward for people using illicit drugs (253 patients, August 2012 to July 2013): 56% had used "
      "pregabalin at least once, 92% of them obtaining it illegally; use in the past year 47% and in the past 10 days "
      "23%; 11% of those using pregabalin met DSM-IV criteria for dependence (Table 1; the text says study criteria); "
      "main reasons relieving opioid withdrawal (61.7% in Table 1, 67.1% in the Discussion) and augmenting other "
      "substances (51.9%). Listed limitations: a subgroup especially at risk; criteria for misuse not validated; "
      "dependence hard to assess in people using several drugs.",
      "supports", EVOY_SRC),
    a(E, EC, "PDF pp. 9, 24",
      "4.2, 2nd and 3rd paragraphs (PDF p. 24); Table 1, Dahlman et al. [17] (PDF p. 9)",
      "In qualitative interview studies, euphoria and improved sociability were the non-therapeutic effects most often "
      "sought; others used gabapentinoids to ease withdrawal from or craving for other drugs, to come down from other "
      "drugs, to ease pain or anxiety, or to sleep. In Swedish opioid treatment, the reasons given for non-prescribed "
      "pregabalin were relieving emotional problems (65%), recreation (27%; getting high, in the text) and relieving "
      "physical problems (12%); among US people with opioid use disorder, the commonest reason for first misusing "
      "gabapentin was a desire to get high (58.1%).",
      "qualifies", EVOY_SRC),
    a(E, EC, "PDF pp. 15, 18, 20, 25",
      "Table 1, Peckham et al. [33] (PDF p. 15) and Van Baelen et al. [42] (PDF p. 18); 3.1.2, 1st paragraph (PDF p. 20); "
      "4.3, 1st and 2nd paragraphs (PDF p. 25)",
      "US commercial insurance claims, 2013–2015: sustained gabapentin overuse in 2.0% of 44,148 people prescribed "
      "gabapentin without opioids and 11.7% of 15,335 prescribed it with opioids (OR 6.32, 95% CI 5.80–6.89); listed "
      "limitations include the lack of established dose thresholds to signal misuse. Belgian treatment-demand and "
      "health-insurance data, 2008–2014 (30,905 people): 10% of people treated for a substance use disorder who "
      "obtained gabapentin had at least one instance of a quantity possibly indicating abuse, against 9.8% of other "
      "patients (from defined daily doses, not an observed measure). The review calls past or current opioid use "
      "disorder the greatest risk factor.",
      "supports", EVOY_SRC),
    a(E, EC, "PDF pp. 4, 18, 21, 25, 27–28",
      "3.2.1 (PDF p. 21); 4.4, 2nd paragraph (PDF p. 25); 4.5, 4th paragraph (PDF pp. 27–28); Table 1, Al-Husseini et al. "
      "[10] (PDF p. 4) and Vickers Smith et al. [43] (PDF p. 18)",
      "Physical dependence and withdrawal widely reported. Jordan, semi-structured interviews with 11 men in treatment "
      "who had misused pregabalin: several described profound dependence and withdrawal on stopping (exhaustion, "
      "headaches, anxiety, depression, joint and muscle pains, shivering, lethargy, insomnia, sweating, avoiding "
      "others). USA, focus groups with 33 people in rural Kentucky who also misused prescription opioids: most had "
      "started gabapentin on a valid prescription, and several had had gabapentin withdrawal, described as similar "
      "to, but shorter than, withdrawal from opioids or depressants. Three gabapentin case reports described "
      "withdrawal including seizures. All 6 misuse case reports (median age 39) were of people with at least one "
      "substance use disorder (one nicotine only), 4 of them with opioid use disorder.",
      "supports", EVOY_SRC),
    a(E, EC, "PDF pp. 13, 16, 28",
      "Table 1, Lyndon et al. [28] (PDF p. 13) and Slavova et al. [36] (PDF p. 16); 4.5.1, 1st paragraph (PDF p. 28)",
      "Post-mortem toxicology in five US jurisdictions, 2015: gabapentin in 22% of 4,169 overdose deaths (931), from 4% "
      "in Northeast Tennessee, where it was not tested automatically, to 41% in Kentucky; every one with at least one "
      "other drug (opioids 94%, benzodiazepines 64.1%, in the text). UK deaths involving gabapentinoids rose from 1 in "
      "2009 to 137 in 2015, 79% of them involving opioids. The review says gabapentinoids are increasingly detected in "
      "overdose deaths, though rarely as the only substance present.",
      "supports", EVOY_SRC),
    a(E, EC, "PDF pp. 10, 27",
      "Table 1, Dart et al. [19] (PDF p. 10); 4.5, 2nd paragraph (PDF p. 27)",
      "US National Poison Data System, June 2006 to December 2014: 4,152 gabapentin or pregabalin abuse cases; the rate "
      "rose 4.3-fold (0.0144 to 0.0618 per 100,000); 31.9% involved a single substance; severe outcomes were "
      "infrequent but included death (0.4%) and major effects (6.1%).",
      "supports", EVOY_SRC),
    a(E, EC, "PDF pp. 4, 13, 20, 27, 30",
      "Table 1, Abrahamsson et al. [9] (PDF p. 4) and Macleod et al. [29] (PDF p. 13); 3.1.3 (PDF p. 20); 4.5, 3rd "
      "paragraph (PDF p. 27); reference 29 (PDF p. 30)",
      "Swedish register cohort of 4,501 people in opioid maintenance treatment, July 2005 to December 2012 (999 with "
      "pregabalin, 1,458 with benzodiazepine and 1,836 with Z-hypnotic prescriptions): pregabalin with overdose death "
      "HR 2.82 (95% CI 1.79–4.43) and all-cause mortality 2.01 (1.38–2.91), not with other deaths 1.16 (0.60–2.25); "
      "Z-hypnotics with overdose death 1.60 (1.07–2.39); benzodiazepines with other deaths 2.02 (1.29–3.18) but not "
      "overdose death 1.49 (0.97–2.29); listed limitations: causal relationships cannot be determined; mostly people "
      "dependent on heroin, aged 18–50. 12,118 people in opioid agonist treatment (called US in Table 1 and the text; "
      "UK Clinical Practice Research Datalink and Office for National Statistics data by reference 29): gabapentinoids "
      "with all-cause mortality HR 1.71 (1.33–2.20) but not drug-related poisoning 1.54 (0.60–3.98). The text restates "
      "the Swedish benzodiazepine and Z-hypnotic hazard ratios wrongly (PDF pp. 20, 27), and the review does not say "
      "whether any estimate was adjusted.",
      "supports", EVOY_SRC),
    a(E, EC, "PDF pp. 15, 27",
      "Table 1, Peckham et al. [6] (PDF p. 15); 4.5, 2nd paragraph (PDF p. 27)",
      "US commercial insurance claims, 2013–2015 (796,330 people aged 16–64), against gabapentin without overuse: "
      "sustained gabapentin overuse without opioid overuse, all-cause hospital admission OR 1.366 (95% CI 1.055–1.769) "
      "and drug-related admission 1.440 (1.010–2.053); with sustained opioid overuse as well, all-cause admission 4.083 "
      "(2.582–6.457) and emergency or inpatient care for respiratory depression 4.106 (1.753–9.619). Listed limitations "
      "include possible residual confounding and claims that may not reflect consumption; adjustment is not described.",
      "supports", EVOY_SRC),
    a(E, EC, "PDF pp. 27, 31",
      "4.5, 3rd paragraph (PDF p. 27); reference 68 (PDF p. 31)",
      "A Swedish population-based cohort (Molero et al., 2019, BMJ), not among the 55 included studies: the risk of "
      "unintentional overdose rose after people were prescribed gabapentinoids (HR 1.24, 95% CI 1.19–1.28), with no "
      "difference once people with substance use disorders were excluded (0.99, 0.91–1.08). The same paragraph says "
      "that the studies linking gabapentinoids to opioid overdose death were not specifically of people misusing them.",
      "qualifies", EVOY_SRC),
    a(E, EC, "PDF pp. 1, 28, 29",
      "Abstract (Conclusion) (PDF p. 1); 4.6, 1st paragraph (PDF p. 28); 4.7 and 5 Conclusion (PDF p. 29)",
      "The abstract concludes that gabapentinoid misuse is a growing trend causing significant patient harm, and the "
      "Conclusion calls the trend alarming; the Discussion says the harm seen with gabapentinoids taken with opioids "
      "was not limited to people with substance use disorders or to misuse. Limitations: highly heterogeneous studies, "
      "hence a qualitative synthesis only; small, single-site samples focused on substance use disorders or overdose "
      "rather than the general population; retrospective designs; reliance on surrogate markers of misuse and harm; "
      "and the assumption that findings for one gabapentinoid apply to the other.",
      "qualifies", EVOY_SRC),
    a(E, EC, "PDF pp. 2, 30",
      "1 Introduction, 2nd paragraph (PDF p. 2); reference 5 (PDF p. 30)",
      "The introduction gives a lifetime prevalence of gabapentinoid misuse of 2.5% in the general population from a UK "
      "study of 2013; its reference 5 is Kapil et al. (2014), a letter on misuse of baclofen, gabapentin and "
      "pregabalin in the UK, the survey for which the 2017 review gives 1.1% for gabapentin and 0.5% for pregabalin "
      "(editors' reading: the 2.5% apparently counts baclofen too).",
      "qualifies", EVOY_SRC),
    # ---- Bonnet & Scherbaum (2017), systematic review ----
    a(B, BC, "PDF p. 3",
      "2.1, 1st to 3rd paragraphs; 2.2; Figure 1",
      "PubMed and Scopus searched from market introduction (gabapentin 1997, pregabalin 2004) to 31 March 2017, with "
      "reference lists; both authors screened independently; 106 articles included (Figure 1). The framework weighs "
      "rewarding effects, ICD-10 dependence criteria in clinical studies and case reports, relapse, treatment seeking, "
      "social harm and overdose toxicity, and takes behavioural dependence in people with no earlier history of "
      "substance use as the best sign of a drug's own power to cause dependence.",
      "qualifies", BON17_SRC),
    a(B, BC, "PDF pp. 1, 4",
      "Abstract (PDF p. 1); 3.1, 1st to 4th paragraphs (PDF p. 4)",
      "17 publications on rewarding effects, mostly animal studies: gabapentin did not produce a conditioned place "
      "preference in rodents and pregabalin did so in one set of experiments only; no animal study of gabapentin "
      "self-administration alone was found; pregabalin was not reinforcing, or only weakly with the effect fading within "
      "the first week, in monkeys trained to self-administer barbiturates; in healthy volunteers pregabalin did not change liking or the "
      "desire to take the drug. The authors read this as no relevant rewarding effect for gabapentin and a low one for "
      "pregabalin. The abstract rests its finding of no convincing evidence of a strong power to cause dependence on "
      "these limited rewarding effects, few notes on relapse, the 4 cases without an earlier history and the absence "
      "of published treatment seeking.",
      "qualifies", BON17_SRC),
    a(B, BC, "PDF pp. 4–7, 22",
      "3.2, 1st and 2nd paragraphs (PDF p. 4); Table 1, Snellgrove (2016) and Mutschler et al. (PDF p. 7); 4.2, 2nd "
      "paragraph (PDF p. 22)",
      "In people in opioid substitution programmes or dependent on prescription opioids, non-medical use within up to 6 "
      "months was 15–22% for gabapentin and 3–26% for pregabalin; all patients found to misuse or be dependent on "
      "gabapentinoids in the clinical studies were dependent on at least one other substance, mostly opioids. In Table "
      "1 the 26% is pregabalin use in the past 30 days in a German detoxification ward (253 patients, all dependent on "
      "other substances, mostly opioids or benzodiazepines; lifetime use 56%), where the point and 24-month "
      "prevalences of pregabalin dependence were 3% and 7%; a Swiss methadone programme (109 patients) found no "
      "pregabalin use by self-report or hair testing.",
      "supports", BON17_SRC),
    a(B, BC, "PDF pp. 6–7",
      "Table 1, Bastiaens et al. (2016)",
      "250 former prisoners living in a correctional community centre in Pittsburgh (written questionnaire): 16% (41) "
      "had misused gabapentin; 26% of the 145 with opioid use disorder against 4% of the 105 without it (p < 0.0001); "
      "1 of 30 people with cocaine use disorder and no opioid use disorder; every participant had at least one further "
      "substance use disorder.",
      "supports", BON17_SRC),
    a(B, BC, "PDF pp. 4, 5, 22",
      "4.2, 1st paragraph (PDF p. 22); Table 1, Kapil et al. (2014) and Cossmann et al. (2016) (PDF p. 5); 3.2, 2nd "
      "paragraph (PDF p. 4)",
      "No epidemiological survey had measured gabapentinoid misuse or dependence in the general population. Online "
      "survey of 1,500 people aged 16–59 who used the internet, in England and Wales: lifetime misuse of gabapentin 1.1% (17), "
      "pregabalin 0.5% (8), baclofen 1.3% (19); other substance use not known. Structured DSM-IV interviews (SKID-I) "
      "of 400 inpatients aged 65 or more in a German general hospital, 2013: lifetime prevalence of gabapentinoid abuse "
      "and dependence 0.25% (one man with transient gabapentin dependence, previously and currently dependent on an "
      "opioid painkiller), 12-month prevalence 0%, no case with pregabalin (section 3.2 calls the 0.25% a 12-month "
      "prevalence); how many of the 400 took gabapentinoids is not given.",
      "supports", BON17_SRC),
    a(B, BC, "PDF p. 13",
      "3.3, 1st, 2nd, 4th and 5th paragraphs",
      "36 gabapentin and 19 pregabalin case presentations, scored against the six ICD-10 dependence criteria: "
      "tolerance and withdrawal symptoms (physical dependence) in 27 of 36 (75%) and 16 of 19 (84%); behavioural "
      "dependence (craving, loss of control, drug seeking) in 3 of 36 (8%) and 15 of 19 (79%); three or more criteria "
      "in 5 of 36 (14%) and 13 of 19 (68%); a move from prescribed doses to self-administration in 10 of 36 and 16 of "
      "19. Most cases with self-administration had a history of alcohol, benzodiazepine or opioid dependence; only 4 "
      "patients, all with pregabalin, showed behavioural dependence without a history of other substance use "
      "disorders apart from nicotine.",
      "supports", BON17_SRC),
    a(B, BC, "PDF p. 13",
      "3.3, 3rd paragraph",
      "The withdrawal symptoms described in the case presentations resembled those of benzodiazepines, including "
      "withdrawal seizures and delirium, or of SSRI antidepressants.",
      "supports", BON17_SRC),
    a(B, BC, "PDF pp. 13, 22",
      "3.3, 6th and 7th paragraphs, and 3.2, 5th paragraph (PDF p. 13); 4 Discussion, 1st paragraph (PDF p. 22)",
      "Information was missing for 177 of the 330 ICD-10 items (54%): 122 of 216 for gabapentin (56%) and 55 of 114 for "
      "pregabalin (48%); the authors judge it more likely that a missing criterion was absent than present but "
      "unreported. No report was found of anyone seeking treatment for gabapentinoid misuse or dependence, or of "
      "social harm attributable to gabapentinoids alone.",
      "qualifies", BON17_SRC),
    a(B, BC, "PDF pp. 19–22",
      "3.4, 3rd, 5th and 7th paragraphs (PDF pp. 21–22); Table 3, Mowry et al. 2013 to 2016 (PDF pp. 19–20)",
      "Nine register studies (Finland, Sweden, Germany, the UK, European pharmacovigilance) all pointed to rising "
      "deaths involving gabapentinoids, mainly pregabalin, nearly always with other drugs, mostly opioids, "
      "benzodiazepines, alcohol and antidepressants. US poison-centre annual reports: fatality records involving a "
      "gabapentinoid 38 of 2,576 (1.5%) in 2012, 41 of 2,113 (1.9%) in 2013, 41 of 1,408 (2.9%) in 2014 and 59 of "
      "1,371 (4.3%) in 2015; pregabalin-related deaths always with other medicines; in each of 2013–2015 one record "
      "(0.05–0.07% of all fatality records), always gabapentin, attributed to a gabapentinoid alone, with no "
      "information on blood levels or autopsy. The authors sum up pure overdoses as relatively safe but able to become "
      "lethal in mixtures, mostly with opioids and sedatives.",
      "supports", BON17_SRC),
    a(B, BC, "PDF p. 23",
      "4.4, 1st paragraph",
      "The authors write that analysing large registers is well suited to uncovering trends but less helpful for "
      "verifying causal relationships, and that the rising deaths involving gabapentinoids might mainly reflect their "
      "increasing use alongside other potentially lethal substance use, mostly of opioids.",
      "qualifies", BON17_SRC),
    a(B, BC, "PDF p. 26",
      "5 Conclusion and recommendations; 4.6, 3rd paragraph",
      "Conclusion: in patients without another current or past substance use disorder the risk of developing "
      "dependence on gabapentinoids is very low, while for patients with such a history, especially opioid use "
      "disorder, the authors advise avoidance or strict monitoring; prospective studies comparing patients with and "
      "without other substance use disorders are missing. In 4.6 the 4 cases without such a history are set against "
      "the number of published cases of a rare syndrome (gut fermentation), a comparison that gives no rate (editors' "
      "note).",
      "qualifies", BON17_SRC,
      quote="the risk to develop a dependence on gabapentinoids is very low"),
    # ---- Bonnet, McAnally & Scherbaum (2021), letter ----
    a(L, LC, "p. 611",
      "Letter, 1st to 3rd paragraphs",
      "The letter, by the two authors of the 2017 review and a pain specialist, accepts the limits the review itself "
      "states (small samples, mostly retrospective designs, homogeneous groups of people dependent on opioids and other "
      "substances) and says clinical studies of people without past or present substance use disorders are lacking; "
      "argues that the reported outcomes are often surrogate and relatively rare and that the authors know of only a "
      "minuscule number of people worldwide seeking treatment for gabapentinoid misuse; says they know of no study that "
      "accounted for predictors and confounders well enough to support a causal link between gabapentinoid use or "
      "misuse and harms including psychological dependence and death (a PubMed search for mediation analyses found no "
      "human studies) and that very few of the review's 46 observational studies were prospective; and calls for "
      "well-powered, controlled prospective studies.",
      "qualifies", BON21_SRC),
    a(L, LC, "pp. 612–613",
      "Letter, 6th paragraph (p. 612) and 8th paragraph (p. 613); Declarations (p. 613)",
      "The letter proposes that gabapentinoids might protect people who use opioids by replacing riskier drugs, adding "
      "that this has not been investigated (6th paragraph); it acknowledges that they may raise the risk of adverse "
      "outcomes in people using other substances through combined depression of the nervous system and perhaps of "
      "breathing, which it says has not been proven mechanistically or clinically (8th paragraph). Declarations: the "
      "authors had written two reviews on the subject, and one author received honoraria from several pharmaceutical "
      "companies.",
      "qualifies", BON21_SRC),
    # ---- older, checked study cards (no PDF on file) ----
    a("gomes_2017", "sc_gomes_2017", "PMC HTML",
      "Abstract (Methods and findings); Results, 3rd paragraph; Fig 2 (forest plot)",
      "Ontario public-drug-plan recipients of opioid painkillers, 1997–2013 (nested case–control study): gabapentin "
      "dispensed in the previous 120 days to 155 of 1,256 people who died an accidental opioid-related death (12.3%) "
      "and 313 of 4,619 matched controls (6.8%); adjusted odds ratio 1.49 (95% CI 1.18–1.88), adjusted for opioid "
      "dose, other sedating medicines, alcohol use disorder and other factors.",
      "qualifies",
      "Study card sc_gomes_2017, key finding 7 (written by AI reader 47 from the PMC full text PMC5626029); the same "
      "figures are ai-checked anchors of the answer on gabapentin and pregabalin with opioids; no PDF on file",
      located_by="AI reader 758 (claim writer), from the study card sc_gomes_2017"),
    a("launiainen_2014", "sc_launiainen_2014", "PMC HTML",
      "Table 2, gabapentin and pregabalin rows; Materials and methods › Forensic toxicology in Finland, 1st and 2nd "
      "paragraphs; Data refining, 3rd paragraph (as the study card gives them)",
      "Finnish medico-legal autopsy cases with comprehensive toxicology, 2000–2010 (57,903 cases analysed in one "
      "national laboratory; deaths selected by police and forensic pathologists for investigation): pregabalin was "
      "found in femoral blood in 380 cases, of which 12% were certified by the pathologist as fatal poisonings with "
      "pregabalin as the main finding; gabapentin in 135 cases, 8%. The paper does not report which other drugs were "
      "present in these deaths.",
      "qualifies",
      "Study card sc_launiainen_2014 (ai-checked; key findings 1 and 7, from the PMC full text PMC4237191, whose Table 2 "
      "the first and second readers checked row by row); no PDF on file",
      located_by="AI reader 758 (claim writer), from the study card sc_launiainen_2014"),
]

statement = (
    "In studies published up to August 2020 and gathered by two systematic reviews (Bonnet & Scherbaum, 2017, searched "
    "to March 2017; Evoy et al., 2021, July 2016 to August 2020), most of them of people with opioid use disorder or "
    "other substance use disorders or of death, poison-centre and insurance records, non-medical use of gabapentin or "
    "pregabalin (one brand is Lyrica) was found mainly in people who also used opioids or other drugs, and more often "
    "than in others wherever the two were compared, with one exception; dependence and withdrawal were described "
    "mainly in case reports; and the deaths recorded with these medicines nearly always involved other drugs, mostly "
    "opioids. None of these studies shows that the medicines caused the harms recorded with them, and the reviews' "
    "figures are second-hand here (the primary studies were not read). "
    "In people in opioid substitution treatment or dependent on prescription opioids, the 2017 review gives non-medical "
    "use within up to 6 months of 15% to 22% for gabapentin and 3% to 26% for pregabalin (the 26% is pregabalin use in "
    "the past 30 days, prescribed or not, in a German detoxification ward), and says that everyone found to misuse or be dependent on "
    "these medicines in the clinical studies was dependent on at least one other substance, mostly opioids; the 2021 "
    "review adds non-prescribed pregabalin in 17.7% of 300 people in Israeli methadone treatment (one urine test), "
    "pregabalin in 18.8% and gabapentin in 1% of 388 people in two German opioid-treatment centres (oral fluid), "
    "pregabalin in 10.7% of 140 Italian patients not prescribed it (hair), none in 109 people in Swiss methadone "
    "treatment, and lifetime non-medical use of pregabalin reported by 21% of 73 people in Swedish opioid treatment; "
    "in the German ward (253 people, all dependent on other substances), 56% had ever used pregabalin, 92% of them "
    "obtaining it without a prescription. Within one sample of 250 former prisoners in Pittsburgh, all with at least "
    "one substance use disorder, 26% of the 145 with opioid use disorder reported misusing gabapentin against 4% of "
    "the 105 without it; in US commercial insurance claims, sustained gabapentin 'overuse' (prescription fills, not "
    "observed misuse) was found in 2.0% of 44,148 people prescribed gabapentin without opioids and 11.7% of 15,335 "
    "prescribed it with opioids; but in Belgian insurance data, people treated for a substance use disorder who "
    "obtained gabapentin received quantities possibly indicating misuse about as often as other patients (10% against "
    "9.8%). For the general population, the 2017 review says no epidemiological survey had measured misuse or "
    "dependence and offers two rough estimates: in one online survey of 1,500 adults aged 16 to 59 in England and "
    "Wales, 1.1% (17 people) reported ever misusing gabapentin and 0.5% (8) pregabalin (the 2021 review cites the same "
    "survey as 2.5% for gabapentinoids, a figure that, by the editors' reading, also counts baclofen), and among 400 "
    "hospital inpatients aged 65 or more in Germany, one man, "
    "also dependent on an opioid painkiller, had had a passing dependence on gabapentin (0.25% of all 400, none in "
    "the past year; how many took gabapentinoids is not given). In interview studies the effects most often sought "
    "were euphoria and feeling more sociable; others took these medicines to ease withdrawal from other drugs, "
    "anxiety, pain or sleeplessness (in the Swedish group, 65% named relief of emotional problems and 27% recreation). "
    "In 55 case presentations published to March 2017 (36 gabapentin, 19 pregabalin), which the 2017 review scored "
    "against the six ICD-10 dependence criteria, tolerance and withdrawal symptoms (physical dependence) were "
    "described in 27 of 36 and 16 of 19, behavioural dependence (craving, loss of control, drug seeking) in 3 of 36 "
    "and 15 of 19, and three or more criteria in 5 of 36 and 13 of 19; the withdrawal described resembled that of "
    "benzodiazepines, including seizures and delirium, or of SSRI antidepressants; and only 4 people, all taking "
    "pregabalin, showed behavioural dependence without a history of other substance use disorders apart from "
    "nicotine. Information was missing for 177 of the 330 criterion ratings (six criteria for each of 55 cases; 54%), "
    "which the reviewers judged more likely absent than unreported, and case reports have no denominator; the "
    "review's conclusion that for people without a substance use disorder \"the risk to develop a dependence on "
    "gabapentinoids is very low\" rests on these case counts, on finding no published report of anyone seeking "
    "treatment for gabapentinoid dependence, on weak rewarding effects in mostly animal studies and on one survey of "
    "older inpatients, none of which measures a rate. In the German detoxification ward, 11% of those who had used "
    "pregabalin met DSM-IV dependence criteria by the 2021 review's table (the 2017 review gives point and 24-month "
    "prevalences of 3% and 7%, apparently of all 253 patients); in interview studies, several of 11 men in treatment "
    "in Jordan described dependence on and withdrawal from pregabalin (exhaustion, headaches, anxiety, low mood, "
    "aches, shivering, sleeplessness and sweating, among others), and several of 33 people in rural Kentucky "
    "described gabapentin withdrawal as similar to, but shorter than, withdrawal from opioids or depressants; all 6 "
    "misuse case reports in the 2021 review were of people with at least one substance use disorder (one nicotine "
    "only). "
    "Gabapentin was found in 22% of 4,169 overdose deaths in five US jurisdictions in 2015 (4% where it was not "
    "tested automatically, 41% in Kentucky), always with at least one other drug (opioids in 94%); UK deaths "
    "involving gabapentinoids rose from 1 in 2009 to 137 in 2015, 79% with opioids; of 4,152 reports of gabapentinoid "
    "abuse to US poison centres (2006–2014), 31.9% involved one substance only, 0.4% ended in death and 6.1% in "
    "'major effects'; and in US poison-centre fatality records, gabapentinoids were involved in 38 to 59 deaths a "
    "year in 2012–2015, almost all with other substances, with one death a year in 2013–2015, always gabapentin and "
    "without blood levels or autopsy results, attributed to a gabapentinoid alone. In Finnish medico-legal autopsies "
    "with toxicology (2000–2010), 12% of the 380 deaths in which pregabalin was found and 8% of the 135 with "
    "gabapentin were certified as fatal poisonings with that drug as the main finding (Launiainen & Ojanperä, 2014; "
    "the 2017 review gives these shares as counts, 12 and 8 deaths). Among 4,501 people in Swedish opioid maintenance "
    "treatment (2005–2012), a pregabalin prescription was associated with overdose death (hazard ratio 2.82, 95% CI "
    "1.79 to 4.43), as were Z-hypnotic sleeping pills (1.60, 1.07 to 2.39), while benzodiazepines were associated "
    "with other deaths but not clearly with overdose death (1.49, 0.97 to 2.29); among 12,118 people in UK opioid "
    "treatment, a gabapentinoid prescription was associated with death from all causes (1.71, 1.33 to 2.20) but not "
    "clearly with drug-poisoning death (1.54, 0.60 to 3.98); and in US insurance claims, gabapentin overuse was "
    "associated with hospital admission (odds ratio 1.366 without and 4.083 with sustained opioid overuse, against "
    "gabapentin without overuse). The 2021 review does not say whether or how these estimates were adjusted, calls "
    "the UK study American and restates the Swedish comparisons wrongly in its text. In a Swedish population cohort "
    "described in its Discussion (Molero et al., 2019; not among its included studies and not read here), "
    "unintentional overdoses were more frequent after a gabapentinoid prescription (hazard ratio 1.24, 1.19 to 1.28) "
    "but not once people with substance use disorders were left out (0.99, 0.91 to 1.08). Whether gabapentin or "
    "pregabalin prescribed with opioid painkillers goes with more opioid deaths is a separate answer (in Ontario, an "
    "adjusted odds ratio of 1.49 for gabapentin; see the answer on gabapentin and pregabalin with opioids). "
    "Neither review appraised the studies it included (both are critically low by AMSTAR 2), most samples were "
    "selected for drug problems or deaths, and misuse was measured by different stand-ins (self-report, urine, "
    "oral-fluid or hair tests, prescription fills); the 2021 review's abstract concludes that misuse is causing "
    "significant harm to patients, while its own Discussion says the studies of opioid deaths were not of people "
    "misusing the medicines. A published letter by the two authors of the 2017 review and a pain specialist argues, "
    "without new studies, that these observational studies cannot show that gabapentinoids cause dependence or death, "
    "that no study adjusted well enough for other factors to support a causal link, that the samples were mostly "
    "people dependent on opioids and that the outcomes were often stand-ins and rare, and adds that its authors know "
    "of very few people worldwide seeking treatment for gabapentinoid misuse (Bonnet et al., 2021). Certainty: very "
    "low. Status: replicated."
)

plain = (
    "Can you become dependent on gabapentin or pregabalin (Lyrica), and how risky are they? It happens, but almost "
    "everything known comes from people who also use opioids or other drugs. In studies of people with opioid "
    "problems, between none and about 20 in 100 had used these medicines without a prescription, depending on the "
    "study. Among 250 "
    "former prisoners in the US, 26 in 100 people with an opioid problem said they had misused gabapentin, against 4 "
    "in 100 without one. In one online survey in England and Wales, about 1 in 100 adults had ever misused gabapentin "
    "and 1 in 200 pregabalin. Published case reports often describe tolerance and withdrawal, sometimes with "
    "seizures, and in a German detox ward 11 in 100 people who had used pregabalin met the criteria for dependence. "
    "Only 4 published cases, all on pregabalin, showed craving or loss of control in people with no earlier drug "
    "problem, but case reports cannot show how often that happens. Deaths with these medicines nearly always "
    "involved other drugs, mostly opioids, and a Swedish study found no rise in overdoses after a prescription once "
    "people with drug problems were left out. None of these studies shows that the medicines caused the deaths, and "
    "the two reviews behind these figures did not check the quality of the studies they gathered."
)

magnitude = (
    "Non-medical use, as each study defined it. Opioid substitution or prescription-opioid samples, within up to 6 "
    "months: gabapentin 15–22%, pregabalin 3–26% (Bonnet & Scherbaum, 2017; the 26% is any use in the past 30 days "
    "in a detoxification ward). Opioid maintenance (Evoy et al., 2021): non-prescribed pregabalin 17.7% of 300 "
    "(Israel, urine); pregabalin 18.8% and gabapentin 1% of 388 (Germany, oral fluid); 10.7% of 140 not prescribed it "
    "(Italy, hair); 0 of 109 (Switzerland); lifetime 21% of 73 (Sweden). German detoxification ward (n = 253): ever "
    "used pregabalin 56%, 92% of them without a prescription. Former prisoners (n = 250): gabapentin misuse 26% of 145 "
    "with opioid use disorder against 4% of 105 without (p < 0.0001). US claims: sustained gabapentin overuse 2.0% of "
    "44,148 without opioids, 11.7% of 15,335 with opioids, OR 6.32 (95% CI 5.80–6.89). Belgium: possibly excessive "
    "gabapentin quantities in 10% of people treated for a substance use disorder against 9.8% of others. General "
    "population: lifetime misuse of gabapentin 1.1% (17 of 1,500) and pregabalin 0.5% (8 of 1,500), one online "
    "survey; lifetime gabapentinoid dependence 0.25% (1 of 400 inpatients aged 65 or more; 12-month 0%). "
    "Dependence: case presentations to March 2017, physical dependence 27/36 (gabapentin) and 16/19 (pregabalin), "
    "behavioural dependence 3/36 and 15/19, three or more ICD-10 criteria 5/36 and 13/19; behavioural dependence "
    "without another substance use history 4 (all pregabalin); criteria not reported 177/330 (54%). German "
    "detoxification ward: DSM-IV pregabalin dependence 11% of those who used it (Evoy, Table 1); point 3% and "
    "24-month 7% (Bonnet, Table 1). Deaths: gabapentin in 22% of 4,169 overdose deaths, five US jurisdictions, 2015 "
    "(4% to 41%), all with at least one other drug, opioids 94%; UK gabapentinoid deaths 1 (2009) to 137 (2015), 79% "
    "with opioids; US poison-centre abuse reports (n = 4,152, 2006–2014): one substance only 31.9%, death 0.4%, major "
    "effects 6.1%; US poison-centre fatality records involving a gabapentinoid 38/2,576 (1.5%, 2012), 41/2,113 "
    "(1.9%), 41/1,408 (2.9%), 59/1,371 (4.3%, 2015), one a year attributed to gabapentin alone (2013–2015); Finnish "
    "autopsies 2000–2010, certified as poisoning with the drug as the main finding: 12% of 380 pregabalin and 8% of "
    "135 gabapentin cases. Associations (adjustment not stated by the review): Swedish opioid maintenance (n = 4,501), "
    "pregabalin and overdose death HR 2.82 (1.79–4.43), all-cause 2.01 (1.38–2.91); Z-hypnotics and overdose death "
    "1.60 (1.07–2.39); benzodiazepines and overdose death 1.49 (0.97–2.29); UK opioid treatment (n = 12,118), "
    "gabapentinoids and all-cause death HR 1.71 (1.33–2.20), drug-related poisoning 1.54 (0.60–3.98); US claims, "
    "gabapentin overuse and all-cause hospital admission OR 1.366 (1.055–1.769), with sustained opioid overuse 4.083 "
    "(2.582–6.457), against gabapentin without overuse. Swedish population cohort (second-hand, from the 2021 "
    "review's Discussion): unintentional overdose HR 1.24 (1.19–1.28); 0.99 (0.91–1.08) without people with "
    "substance use disorders. Ontario (the answer on gabapentin and pregabalin with opioids): adjusted OR 1.49 "
    "(1.18–1.88)."
)

grade = {
    "starting_level": "low",
    "domains": {
        "risk_of_bias": {"levels": 1, "note": (
            "Both reviews are critically low by AMSTAR 2 (cards sc_evoy_2021 and sc_bonnet_2017): neither appraised the "
            "studies it included; the samples were selected for drug problems or deaths (opioid treatment and "
            "detoxification, former prisoners, decedents, spontaneous reports); misuse was measured by different "
            "stand-ins (self-report, a single urine test, oral-fluid or hair tests, prescription fills); the case "
            "reports are a selection driven by what gets published, with 54% of the dependence criteria unreported; and "
            "the 2021 review does not say whether the death and hospital associations were adjusted, or for what. The "
            "letter (sc_bonnet_2021) is cited only for its arguments.")},
        "inconsistency": {"levels": 0, "note": (
            "Non-medical use ranges from none (one Swiss clinic) to 26% within up to 6 months, and to 56% lifetime in "
            "one detoxification ward, and one Belgian prescription study found no difference between people with and "
            "without a substance use disorder; both reviews relate the spread to samples, tests and time windows, the "
            "statement gives the range and the exception, and nothing is pooled. Not downgraded.")},
        "indirectness": {"levels": 1, "note": (
            "The figures are second-hand: none of the primary studies was read; the general-population figures come "
            "from one online survey and one survey of older inpatients, both known only from the 2017 review's table; "
            "the Swedish population result comes from one paragraph of a Discussion; and misuse and dependence mean "
            "different things in different studies (DSM-IV interviews, ICD-10 criteria scored on case reports by the "
            "reviewers, prescription quantities).")},
        "imprecision": {"levels": 0, "note": (
            "Not downgraded for the pattern, which several samples of hundreds to tens of thousands of people show; "
            "the general-population figures rest on 17 and 8 people and one man, and the case counts are small, which "
            "the statement says.")},
        "publication_bias": {"levels": 0, "note": (
            "Not assessable; the selection of case reports by what gets published is counted under risk of bias, not "
            "twice.")},
        "large_effect": {"levels": 0, "note": "Not applicable to a descriptive claim."},
        "dose_response": {"levels": 0},
        "plausible_confounding": {"levels": 0},
    },
    "certainty": "very-low",
    "reasoning": (
        "Descriptive claim (how often misuse and dependence were found, in whom, and what was recorded with deaths), "
        "with the death and hospital findings stated as associations. Observational evidence starts low; downgraded "
        "once for risk of bias and once for indirectness, which gives very low (the floor); not upgraded, as "
        "descriptive claims never are. Status replicated: the central pattern, non-medical use found far more often in "
        "people who also use opioids or have other substance use disorders, appears in several independent samples in "
        "several countries as the reviews describe them (former prisoners in Pittsburgh, 26% against 4%; US insurance "
        "claims, 11.7% against 2.0%; opioid-treatment and detoxification samples in Germany, Israel, Italy and Sweden); "
        "the two reviews overlap only from July 2016 to March 2017 and no study is counted twice here; one Belgian "
        "prescription study and one Swiss clinic point the other way or found none, which the statement says. The "
        "case-report counts, the two general-population surveys and the Swedish population result are single "
        "sources. Not marked contested: the reviews and the letter disagree about whether gabapentinoids cause harm "
        "and how worried prescribers should be, but this claim states only what was counted and the associations "
        "reported, which neither side disputes, and takes from the letter its points of method (association, not "
        "cause), not its safety conclusions, which rest on the authors' opinion and their own data; whether "
        "gabapentinoids cause the deaths they are found in is not claimed. The 2017 review's conclusion of a very low "
        "risk without a substance use disorder is quoted as its authors' reading of case counts, not as a measured "
        "rate. The 2021 review's pregnancy findings (a case series of 19 infants; a relative risk that cannot be "
        "derived from its own percentages) and the letter's own hospital figures (whose counts differ from the 2017 "
        "review's account of what seems the same sample) are left out.")
}

claim = {
    "id": "cl_gen_gabapentinoids",
    "substance": "general",
    "section": 8,
    "statement": statement,
    "plain": plain,
    "population": (
        "People studied for gabapentin or pregabalin misuse, dependence and harms in studies published up to August "
        "2020 and compiled by two systematic reviews (to March 2017; July 2016 to August 2020): mostly people with "
        "opioid use disorder or other substance use disorders (opioid treatment, detoxification, former prisoners), "
        "decedents, and poison-centre, adverse-event and insurance records; general-population figures from one online "
        "survey of 1,500 adults (England and Wales) and one survey of 400 older hospital inpatients (Germany); 55 "
        "published case presentations; and Finnish medico-legal autopsies with toxicology, 2000–2010"),
    "exposure": "Use of gabapentin or pregabalin, prescribed or not",
    "comparator": (
        "Within some studies, people without opioid use disorder (former prisoners), without opioid prescriptions (US "
        "claims) or without a substance use disorder (Belgian records; the Swedish population cohort); otherwise none "
        "(descriptive)"),
    "outcome": (
        "Non-medical use as each study defined it (self-report; urine, oral-fluid or hair tests; prescription fills "
        "above a threshold); dependence (DSM-IV interviews; ICD-10 criteria scored on case reports) and withdrawal; "
        "deaths, overdoses and hospital care recorded with gabapentinoids"),
    "relation": "describes",
    "magnitude": magnitude,
    "evidence": evidence,
    "grade": grade,
    "status": "replicated",
    "verification": {
        "status": "draft",
        "drafted_by": "AI reader 758 (claim writer)",
        "drafted_on": "2026-11-26",
        "flag_note": (
            "Question 12 of round pdf-2026-11-26. Not read: the review authors' reply to the letter "
            "(10.1007/s40265-021-01495-0) and the primary studies behind the key figures, above all Bastiaens et al. "
            "2016 (Psychiatr Q 87, 763–767), Kapil et al. 2014 (Br J Clin Pharmacol 78, 190–191), Snellgrove et al. "
            "2017 (10.1007/s40263-017-0467-3), Abrahamsson et al. 2017 (10.1016/j.drugalcdep.2017.01.013), Molero et "
            "al. 2019 (10.1136/bmj.l2147), Slavova et al. 2018 (10.1016/j.drugalcdep.2018.01.018) and Bonnet, Strasser "
            "and Scherbaum 2019 (Addict Behav 90, 265–271). Pages general and prescription-opioids, as the brief asks; "
            "there is no gabapentin or pregabalin page."),
    },
    "version": "0.1.0",
    "changelog": [
        {"version": "0.1.0", "date": "2026-11-26",
         "change": ("Round pdf-2026-11-26: drafted by AI reader 758 (claim writer) from the PDFs of Evoy et al. (2021), "
                    "Bonnet & Scherbaum (2017) and Bonnet et al. (2021), with two anchors from the study cards of "
                    "Gomes et al. (2017) and Launiainen & Ojanperä (2014); anchors ai-located.")}
    ],
}

json.dump([claim], open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(OUT, "a", encoding="utf-8").write("\n")
print("written", OUT, "anchors", len(evidence))
