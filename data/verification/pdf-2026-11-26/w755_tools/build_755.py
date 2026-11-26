"""Claim writer 755 (round pdf-2026-11-26): builds the two new claims and their plain lines.

Writes data/claims/_incoming/pdf1126_w755.json and data/verification/pdf-2026-11-26/755_simple.json.
Run from the repository root: python3 -I data/verification/pdf-2026-11-26/w755_tools/build_755.py
Every number was read on the rendered PDF pages; the counts from Brunetti et al. (2021), Table 1, come from
parse_table1b.py + classify_deaths.py + opioid_counts.py in this folder (run them on the PDF to redo them).
"""
import json

D = "2026-11-26"
WHO = "AI reader 755 (claim writer), from the PDF"

SR_WOOD = ("PDF (version of record), Clinical Toxicology 2015;53(2):85-92, all 8 pages; Tables 1-3 and the page of every "
           "number used checked on 110-dpi renderings")
SR_CARP = ("PDF (online-first version, DOI 10.1080/15563650.2018.1510502; PDF p. 1 is the publisher's cover page and PDF pp. 2-6 "
           "the article, whose page numbers differ from the print issue, Clin Toxicol 2019;57(4):282-286), all 6 pages; Tables 1-4 "
           "checked on 120-dpi renderings")
SR_BRUN = ("PDF (version of record), Pharmaceuticals 2021;14:560, all 46 pages; all 30 pages of Table 1 (pp. 5-34) rendered at "
           "100 dpi; every death row counted with a parse of the table's ruled rows (w755_tools in this round's folder), checked "
           "against the rendered pages")


def A(ref, card, page, loc, ext, role, sr, quote=None):
    a = {"reference": ref, "study_card": card, "page": page, "locator": loc, "extracted": ext, "role": role,
         "anchor_status": "ai-located", "located_by": WHO, "located_on": D, "source_read": sr}
    if quote:
        a["quote"] = quote
    return a


def W(page, loc, ext, role, quote=None):
    return A("wood_2015", "sc_wood_2015", page, loc, ext, role, SR_WOOD, quote)


def C(page, loc, ext, role):
    return A("carpenter_2019", "sc_carpenter_2019", page, loc, ext, role, SR_CARP)


def B(page, loc, ext, role, quote=None):
    return A("brunetti_2021", "sc_brunetti_2021", page, loc, ext, role, SR_BRUN, quote)


# ---------------------------------------------------------------- cl_lsd_nbome
nbome = {
    "id": "cl_lsd_nbome",
    "substance": "lsd",
    "section": 6,
    "statement": (
        "As described in one narrative review of reports up to 2014 (Wood et al., 2015), so that its figures are second-hand and come "
        "from published case reports and case series (several known only from conference abstracts), one US poison-centre series, "
        "cases and deaths reported to European agencies and a news report, none of them appraised: NBOMes (N-2-methoxybenzyl "
        "relatives of the 2C phenethylamines, among them 25I-, 25B- and 25C-NBOMe; the review describes 25I-NBOMe as a very potent "
        "agonist of the serotonin 5-HT2A receptor) were typically sold on blotters, and also as powder and liquid, and 8 of the 10 "
        "first detections of an NBOMe in Europe, from January 2011 to June 2013, were on blotters, alone or with powder (editors' "
        "count from the review's table). In several reported cases people believed they had taken LSD: a woman at a US festival had "
        "taken 'acid' on blotters whose remains held mainly 25C-NBOMe (her own samples were not tested); three people in Belgium who "
        "said they had taken 'synthetic LSD' had 25I-NBOMe, and no other drug, in their urine; and among the deaths, a 21-year-old "
        "man in Houston who had taken two 'hits of acid' had 25I-NBOMe, with cannabis metabolites, in post-mortem samples, a person "
        "in Belgium had used a blotter they thought held LSD, in which no LSD was found (whether an NBOMe was tested for is not "
        "reported), and in Richmond, Virginia, a 19-year-old died while 'trip sitting' friends who were using 'acid' blotters, and an "
        "unused blotter from the case held 25I-NBOMe, which was also found in his own samples. How often blotters sold as LSD hold an NBOMe was not measured. In the 29 published poisoning cases (25I-NBOMe "
        "23, 25B-NBOMe 3, 25C-NBOMe 3; aged 14 to 31, and 17 of the 19 whose sex is given were men, editors' count), the review "
        "reports a fast heart rate in 96.6%, high blood pressure in 62.0%, agitation or aggression in 48.2%, seizures in 37.9% and a "
        "high body temperature in 27.6%, and acute kidney injury in 5 people; these features are not defined, and the review's own "
        "case descriptions do not reproduce all of the shares (by the editors' count, seizures in 12 of the 29 and kidney injury in "
        "6), so they are approximate. The severe courses described include continuous seizures (status epilepticus), muscle "
        "breakdown with kidney injury treated with dialysis or blood filtration in 3 people, lung injury needing a long period on a "
        "ventilator, and 38 days in intensive care for a man who injected a liquid labelled 25I-NBOMe (he left hospital after 43 "
        "days with normal kidney function); five of seven men in one English series went home from the emergency department within "
        "a day. Published cases favour severe ones: in 25 cases reported to Texas poison centres in 2012-2013 (no other substance "
        "reported in 21), seizures were recorded in 4% (1 of 25, editors' calculation), against 38% across the published cases, and "
        "the commonest effects were a fast heart rate (52%), agitation or irritability (48%), hallucinations (32%) and high blood "
        "pressure (32%). Eight deaths had been reported with 25I-NBOMe (in one with 25C-NBOMe too), and the review's abstract says "
        "it was detected in all eight, but its text reports laboratory detection in five (two in Houston, one in Richmond, one in "
        "Belgium whose death was reported as due to natural causes, and one in the UK, a 22-year-old man who drowned, with "
        "25C-NBOMe and five other substances also found) and none reported for three (an Australian news report, the Belgian death "
        "after a blotter thought to hold LSD, and a Polish death). Several deaths followed disturbed behaviour, such as falls from "
        "balconies, or self-injury and aggression before collapse, and the review says the role of NBOMes in the deaths had often "
        "not been determined. By the editors' count, the NBOMe was found in the person's own samples in 15 of the 29 published "
        "poisoning cases, only in the remaining product in 2, and in no sample linked to the person in 12, and other drugs were "
        "found or reported in many cases; the review's authors read the reported features as serotonin toxicity together with "
        "stimulant-like (sympathomimetic) toxicity, much like MDMA, some amphetamines and mephedrone. These reports count no one who "
        "used an NBOMe without harm, so they cannot give the risk of harm from a use, and no source here compares NBOMes with LSD; "
        "in two non-representative 2013 surveys aimed at people who go clubbing (one of them by two of the review's authors), NBOMe "
        "use was much less common than LSD or mephedrone use (ever used: 2.6% against 39.4% for LSD among 22,289 respondents of the "
        "Global Drugs Survey). Nothing after 2014 is covered. How often people seek emergency treatment after taking LSD is a "
        "separate answer. Certainty: very low. Status: single study."
    ),
    "plain": (
        "What are NBOMes, and are they sold as LSD? NBOMes are lab-made drugs related to the 2C drugs, and they were usually sold on "
        "blotters. One review of reports up to 2014, whose figures are second-hand, describes several cases in which people who got "
        "sick or died thought they had taken LSD or 'acid'; nobody measured how often blotters sold as LSD hold an NBOMe. In 29 "
        "published cases of poisoning, nearly all people had a racing heart, about 6 in 10 high blood pressure, about 4 in 10 "
        "seizures and about 3 in 10 a high temperature, and some needed intensive care, a breathing machine or dialysis. Published "
        "cases tend to be the worst ones: among 25 cases reported to poison centres in Texas, 4 in 100 had seizures. Eight deaths had "
        "been reported with one NBOMe, 25I-NBOMe, and a laboratory found it in five; some of these people had taken other drugs too, "
        "and the review says the drug's role in the deaths was often not settled. These reports cannot say how risky one use is, and "
        "nobody compared NBOMes with LSD."
    ),
    "population": (
        "People with reported poisoning or death after NBOMe use, 2010-2014, as gathered in one narrative review: 29 published "
        "poisoning cases (several known only from conference abstracts), 25 cases reported to Texas poison centres in 2012-2013, 25 "
        "non-fatal cases reported to the EU Early Warning System, and 8 reported deaths (forensic reports, the EU Early Warning "
        "System and a news report); first detections of NBOMes in Europe, 2011-2013"
    ),
    "exposure": (
        "NBOMe drugs (mostly 25I-NBOMe; also 25B- and 25C-NBOMe), reported by the person or found by laboratory analysis of the "
        "person's samples or of the product, often with other drugs; the forms in which they were found or taken (blotters, powder, "
        "liquid, capsules), including blotters taken as LSD or 'acid'"
    ),
    "comparator": (
        "None: case reports and one poison-centre series with no comparison group; the review sets the published cases beside the "
        "poison-centre series; no comparison with LSD"
    ),
    "outcome": (
        "Clinical features, severe complications and deaths as reported, whether the drug was confirmed by laboratory analysis, and "
        "cases in which people believed they had taken LSD"
    ),
    "relation": "describes",
    "magnitude": (
        "Wood et al. (2015), second-hand: first detections in Europe 2011-2013, 8 of 10 on blotters (editors' count, Table 1). 29 "
        "published poisoning cases (25I 23, 25B 3, 25C 3): tachycardia 96.6%, hypertension 62.0%, agitation/aggression 48.2%, "
        "seizures 37.9%, hyperthermia 27.6%, acute kidney injury 5 patients (as printed; editors' count from the case descriptions: "
        "seizures 12 of 29, kidney injury 6); NBOMe found in the person's own samples in 15 of 29, product only 2, no linked analysis "
        "12 (editors' count). Texas poison centres 2012-2013, 25 cases: tachycardia 52%, agitation/irritability 48%, hallucinations "
        "32%, hypertension 32%, confusion 24%, mydriasis 20%, seizures 4% (1 of 25, editors' calculation) against 38% in published "
        "cases. Deaths: 8 reported with 25I-NBOMe (abstract: detected in all 8); laboratory detection in 5, none reported for 3. "
        "Global Drugs Survey 2013 (22,289; non-representative): ever used an NBOMe 2.6%, LSD 39.4%. No denominators of people who "
        "used NBOMes; no rates or intervals."
    ),
    "evidence": [
        W("pp. 85-86",
          "Abstract › Methods (p. 85); Methods, single paragraph (p. 85, continued on p. 86)",
          "Narrative review by two clinical toxicologists in London and two staff of the EU drugs agency (EMCDDA): PubMed searched for 'NBOMe' and the names of ten NBOMe compounds, 1966-2014; abstracts of two clinical "
          "toxicology congresses (2010-2014 and 2010-2013); the EU information system and database on new drugs; a Google search "
          "for grey literature; each paper kept if it related to prevalence of use or acute toxicity. No other eligibility criteria, "
          "selection procedure or appraisal of the reports is described.",
          "qualifies"),
        W("pp. 85-86",
          "Introduction, 1st paragraph (p. 85); Table 1 (p. 86)",
          "NBOMes are N-2-methoxybenzyl analogues of the 2C-X substituted phenethylamines; they are typically sold in blotters, and "
          "are also available as powder and liquid; 25I-NBOMe is described as a very potent 5-HT2A receptor agonist. Table 1 (EU "
          "Early Warning System): first detections of ten NBOMes in Europe, January 2011 to June 2013, by police or customs: 8 of "
          "the 10 on blotters, alone or with powder (25N-, 25E-, 25G-, 25D-, 25I-, 25B- and 25H-NBOMe and 25B-N(BOMe)2), and 2 as "
          "powder only (25C- and 25iP-NBOMe) (editors' count).",
          "supports"),
        W("pp. 88-91",
          "25C-NBOMe, 3rd paragraph (p. 88); 25I-NBOMe acute toxicity cases from the EMCDDA Risk Assessment Report, single "
          "paragraph (p. 89, continued on p. 90); NBOMe-related deaths, 3rd and 5th paragraphs (p. 90), 6th paragraph (p. 90, "
          "continued on p. 91) and 8th paragraph (p. 91)",
          "Cases in which people believed they had taken LSD: a 24-year-old woman at the Burning Man festival had taken 'acid' on "
          "blotter paper, whose remains held mainly 25C-NBOMe and a very small amount of 25I-NBOMe; her own samples were not "
          "analysed. Three people in Belgium, brought to hospital from the same party, reported using 'synthetic LSD'; 25I-NBOMe was "
          "confirmed in their urine, with no other drugs detected. A 21-year-old man in Houston who had taken two 'hits of acid' and "
          "smoked cannabis hallucinated, injured himself and attacked a friend, and was found unresponsive; 25I-NBOMe and cannabis "
          "metabolites were found in his post-mortem heart blood and urine. A 19-year-old in Richmond, Virginia, 'trip sitting' "
          "friends who were reportedly using 'acid', behaved strangely and was found after probably jumping or falling from a balcony; "
          "a case-related sample of unused blotter paper held 25I-NBOMe and targeted analysis found it in his blood, urine, brain, "
          "liver and bile; his friends did not know he had taken anything, and those who took the 'acid' blotters showed no similar "
          "symptoms. In Belgium a person had used a blotter at a party that they thought contained LSD; no LSD was found, and "
          "analytical confirmation of 25I-NBOMe was not reported.",
          "supports"),
        W("pp. 85, 87, 91",
          "Abstract › Acute toxicity (p. 85); Acute toxicity, 1st paragraph (p. 87); Conclusions, 1st paragraph (p. 91)",
          "29 published cases of acute toxicity associated with an NBOMe: 25I-NBOMe 23, 25B-NBOMe 3, 25C-NBOMe 3; no information on "
          "acute toxicity for six other NBOMes. Commonly reported features: tachycardia 96.6%, hypertension 62.0%, "
          "agitation/aggression 48.2%, seizures 37.9% and hyperthermia 27.6%; five patients were reported to have developed acute "
          "kidney injury. No definitions or thresholds are given. Editors' count from the review's case descriptions (pp. 87-90): "
          "seizures in 12 of the 29 (37.9% is 11 of 29), acute kidney injury in 6; ages 14 to 31 where given; 17 of the 19 whose "
          "sex is given were men.",
          "supports"),
        W("pp. 87-89",
          "25B-NBOMe, 3rd paragraph (p. 87); 25C-NBOMe, 1st paragraph (p. 87, continued on p. 88); 25I-NBOMe, 2nd paragraph (p. 88, "
          "continued on p. 89) and 6th paragraph (p. 89); Table 2 (p. 88)",
          "Severe courses: a 19-year-old man in Richmond (25B-NBOMe confirmed) in status epilepticus with a rectal temperature of "
          "40°C, then rhabdomyolysis and acute kidney injury, fully alert by day 6; a 19-year-old man in Germany (self-reported "
          "25C-NBOMe, no analysis) with rhabdomyolysis and acute kidney injury needing haemofiltration, then acute lung injury "
          "needing a prolonged period of invasive ventilation, recovered by day 13; in Grand Rapids, three of four men with "
          "prolonged seizures needing sedation and intubation, and one with rhabdomyolysis (creatine kinase 30,000 IU/L) and acute "
          "kidney injury needing haemodialysis. In the Hill series of seven men, case 1, who injected a liquid labelled '25I-NBOMe' "
          "bought from a drug dealer, spent 38 days in intensive care (acute kidney injury needing haemodialysis, lung abscesses, "
          "acute respiratory distress syndrome) and was discharged after 43 days with normal kidney function; cases 3-7 were "
          "discharged from the emergency department after a short period of observation (stays of 15 h to under 24 h, Table 2) "
          "without long-term sequelae.",
          "supports"),
        W("p. 90",
          "NBOMe-drug-related toxicity reported to poison centres, single paragraph",
          "Texas Poison Centers, 2012-2013: 25 NBOMe cases (8 in 2012, 17 in 2013); 19 (76%) 25I-NBOMe, 3 (12%) 25C-NBOMe, 3 an "
          "unidentified NBOMe; no other substance used in 21 (84%); commonest effects tachycardia 52%, agitation/irritability 48%, "
          "hallucinations 32%, hypertension 32%, confusion 24% and mydriasis 20%; seizures reported in 4% (1 of 25, editors' "
          "calculation), against an overall frequency of 38% in the published case reports.",
          "qualifies"),
        W("pp. 85, 90-91",
          "Abstract › NBOMe-related deaths (p. 85); NBOMe-related deaths, all ten paragraphs (pp. 90-91)",
          "The abstract says 25I-NBOMe was detected in eight fatalities, in one with 25C-NBOMe, and that its role was not determined "
          "in all cases. The text reports analytical detection in five: two people after a rave party in Houston (post-mortem heart "
          "blood and urine, with cannabis metabolites; the post-mortem examinations showed only external injuries), a 19-year-old in "
          "Richmond (blood, urine, vitreous humour, brain, liver and bile), a man in Belgium whose death was reported as due to "
          "natural causes (matrix and method not specified), and a 22-year-old man in the UK who drowned (25I- and 25C-NBOMe, with "
          "amphetamine, ketamine, lidocaine, 5-methoxy-diisopropyltryptamine and 2,5-dimethoxy-4-iodoamphetamine). No analytical "
          "confirmation was reported for three: a 17-year-old in Australia known from a media report, who acted erratically and "
          "jumped from a third-floor balcony; a Belgian who had used a blotter thought to contain LSD; and a Polish death.",
          "supports",
          quote="25I-NBOMe has been detected in eight fatalities"),
        W("pp. 87-91",
          "25B-NBOMe, 25C-NBOMe and 25I-NBOMe sections (pp. 87-89); Tables 2 and 3 (pp. 88, 90); Conclusions, 1st paragraph (p. 91)",
          "Editors' count from the case descriptions: the NBOMe was found in the patient's own samples, with the result linked to "
          "the patient, in 15 of the 29 published cases (both Hong Kong cases, the Richmond 25B-NBOMe case, the seven Hill cases, "
          "the Richmond 25I-NBOMe case, the St Paul case and three of the four Grand Rapids cases); only the product was analysed in "
          "2 (Detroit, Burning Man); no analysis linked to the patient was reported in 12 (the German 25C-NBOMe case, the ten "
          "Richmond patients, whose two analysed serum samples could not be linked to patients, and one Grand Rapids patient). "
          "Other drugs found or reported include amphetamine and methamphetamine in six of the seven Hill cases, ketamine in the "
          "second Hong Kong case, caffeine in three Grand Rapids cases, a phencyclidine analogue in the Detroit eye dropper, and "
          "co-use reported by four of the ten Richmond patients. The Conclusions say only some reports included analytical "
          "confirmation, read the features as both serotonin syndrome and sympathomimetic toxicity, much like MDMA, certain other "
          "amphetamines and mephedrone, and say the significance of post-mortem detection for the deaths has often not been "
          "determined.",
          "qualifies"),
        W("pp. 86-87, 91",
          "Prevalence of use, 2nd-4th paragraphs (p. 86, the 4th continued on p. 87); Declaration of interest (p. 91)",
          "No national or international surveys of NBOMe use exist; the only data are two non-representative surveys targeting "
          "people who frequent nightclubs. Global Drugs Survey 2013 (22,289 respondents, mainly from the UK and USA): 582 (2.6%) had "
          "ever used 25B-, 25C- or 25I-NBOMe; 8,774 (39.4%) had ever used LSD. South East London nightclub survey, 2013 (397 "
          "participants): ever used an NBOMe 4.8% against 76.6% for mephedrone; this survey is a congress abstract by Lovett, "
          "Measham, Dargan and Wood (reference 19), two of them authors of the review. Two authors are advisers to or members of the "
          "UK Advisory Council on the Misuse of Drugs and the EMCDDA and attended the EMCDDA risk-assessment meeting on 25I-NBOMe; "
          "the other two report no declarations.",
          "qualifies"),
    ],
    "grade": {
        "starting_level": "low",
        "domains": {
            "risk_of_bias": {"levels": 1, "note": (
                "Published case reports select severe, unusual or analytically interesting cases (seizures in about 38% of them against "
                "4% in the one poison-centre series); the NBOMe was found in the person's own samples in only 15 of the 29 published "
                "cases (editors' count) and other drugs were often present; the features are not defined and the pooled shares cannot "
                "all be reproduced from the review's case descriptions; the review is not systematic and does not appraise its sources "
                "(card sc_wood_2015: some concerns).")},
            "inconsistency": {"levels": 0, "note": (
                "The published cases and the poison-centre series differ in how often seizures were recorded, a difference the "
                "statement gives and that selection explains; the reports agree on the kind of features.")},
            "indirectness": {"levels": 1, "note": (
                "Second-hand: the case reports, the poison-centre series and the European reports were not read; everything is as "
                "described by one narrative review (METHODS §6.3).")},
            "imprecision": {"levels": 0, "note": (
                "Counts of reports, not rates; the shares rest on 29 and 25 cases, which the statement gives.")},
            "publication_bias": {"levels": 0, "note": (
                "The selection of published cases is counted under risk of bias and not twice.")},
            "large_effect": {"levels": 0},
            "dose_response": {"levels": 0},
            "plausible_confounding": {"levels": 0},
        },
        "certainty": "very-low",
        "reasoning": (
            "Descriptive (what was reported, and in which kind of data): starts low as case reports and record series seen through a "
            "narrative review; downgraded one level for risk of bias (selected, partly unconfirmed cases, often with other drugs) and "
            "one for indirectness (second-hand), bounded at very low; never upgraded. Because every supporting anchor cites one "
            "narrative review, the claim stays a draft and its statement says that its figures are second-hand. Status single study: "
            "one review; the primary reports it gathers come from different teams but were not read here, so they are not counted as "
            "independent replications. The statement gives the review's printed shares, not the editors' recount, and says that they "
            "are approximate; it reports deaths with the drug found or reported, not deaths caused by it. Nothing here measures how "
            "often blotters sold as LSD hold an NBOMe, the risk of harm from a use, or harm compared with LSD."
        ),
    },
    "status": "single-study",
    "verification": {
        "status": "draft",
        "drafted_by": "AI reader 755 (claim writer)",
        "drafted_on": D,
        "flag_note": (
            "Question 7 of round pdf-2026-11-26 (forum theme: research chemicals; 'Is a blotter sold as LSD really LSD, or a more "
            "dangerous NBOMe?', 190,000 views; the 25I- and 25C-NBOMe threads, 482,000 and 430,000). Not read: the primary reports the "
            "review summarizes (Hill et al., 2013, Clin Toxicol 51:487-492; Forrester, 2014, J Addict Dis 33:196-201; Walterscheid et "
            "al., 2014, Am J Forensic Med Pathol 35:20-25; Poklis et al., 2014, Forensic Sci Int 234:e14-20; Armenian and Gerona, 2014, "
            "doi 10.1016/j.ajem.2014.04.047, the only DOI the review prints), the EMCDDA risk assessment of 25I-NBOMe (2014) and Lawn "
            "et al. (2014, J Psychopharmacol 28:780-788). Only drug-checking data on blotters sold as LSD could say how often they hold "
            "an NBOMe. Pages: lsd and 2c-x (the 2C-x page is planned, not yet published)."
        ),
    },
    "version": "0.1.0",
    "changelog": [{"version": "0.1.0", "date": D, "change": (
        "Drafted by AI reader 755 (claim writer) from Wood et al. (2015), read in full from the PDF; anchors ai-located; round "
        "pdf-2026-11-26, question 7.")}],
}

# ---------------------------------------------------------------- cl_benzo_designer
benzo = {
    "id": "cl_benzo_designer",
    "substance": "benzodiazepines",
    "section": 6,
    "statement": (
        "Evidence is insufficient to say whether designer benzodiazepines (benzodiazepines and close relatives sold on the illicit "
        "market, such as etizolam, clonazolam, flualprazolam, flubromazolam and phenazepam, of which etizolam and phenazepam are "
        "licensed medicines in a few countries) are more dangerous than prescribed benzodiazepines: no source read here compares them, and neither source counts the people who used them without coming to "
        "attention, so neither gives a risk per use. In US poison-centre records (the National Poison Data System), 474 exposures to "
        "designer benzodiazepines were reported from 2014 to 2017; the 234 intentional exposures to one of 11 coded designer "
        "benzodiazepines and no other substance were analysed, while the reports involving other substances, about half, were neither collected nor "
        "analysed (Carpenter et al., 2019). The 234 were mostly etizolam (162) and clonazolam (50); the median age was 25, 86% were "
        "men, and 42 (18 in 100) were coded as suspected suicide. Drowsiness or lethargy was coded in 152 (65 in 100), slurred "
        "speech in 40 (17), confusion in 32 (14), agitation or irritability in 22 (9), a fast heart rate in 20 (9), low blood "
        "pressure in 19 (8) and coma in 10 (4), as the table gives them (the text gives 14% for agitation and 8% for coma), and 7 "
        "people (3 in 100) were intubated. Of the 224 whose care was recorded (editors' sum), 92 (41 in 100) were treated and "
        "released, 31 (14 in 100) admitted to a non-critical-care ward, 49 (22 in 100) to critical care and 36 (16 in 100) to a "
        "psychiatric facility; 9 (4 in 100) had a major effect, and one man, aged 29, died after a reported intentional ingestion of etizolam (1 of 234, 0.4%); effects "
        "lasted less than a day in 151 of the 178 with a recorded duration (85 in 100; editors' sum of the table's rows). The drug in "
        "each report is the one named by the caller and coded by poison-centre staff, with no laboratory confirmation, and the "
        "authors say people may have taken other compounds than those coded; they expect people without significant symptoms to "
        "have gone unreported, so that the reports undercount exposures and overstate severity; and a death after flubromazolam, "
        "coded under the general 'benzodiazepine' code, was missing from the data. Reports rose from 26 in 2014 to 112 in 2017, "
        "a 330% increase that the abstract reads as rising incidence, but only etizolam had its own code before 2016: etizolam alone went from "
        "26 to 60 reports. In published case reports and forensic series up to March 2021, as compiled in a review that did not "
        "appraise them (Brunetti et al., 2021; so these figures are second-hand), 12 designer benzodiazepines appear in 141 death "
        "entries, 63 cases of impaired driving and 44 emergency admissions, from eight countries; the deaths were mostly with "
        "phenazepam (60), flualprazolam (38) and etizolam (34). By the editors' count of the review's table, 115 of the 141 death "
        "entries also list at least one opioid (methadone in 51, morphine or 6-acetylmorphine in 49), 2 more list loperamide or its "
        "metabolite, and 3 list no other drug; at least four people appear to be listed twice, all four with an opioid, and counting "
        "each of them once gives 111 of 137 (editors' calculation), about 8 in 10 either way. The two deaths in which, by the "
        "review's text, phenazepam alone was listed as the cause list alcohol in one and diazepam with dihydrocodeine in the other. In the emergency cases "
        "the review describes mostly sedation (depression of the central nervous system), and agitation and delirium in a few "
        "(editors' summary of its drug-by-drug text); its authors say that because several drugs are usually present, a death often "
        "cannot be assigned to one of them, and that blood levels overlapped between drivers judged impaired and drivers judged not "
        "impaired, and were similar in drivers and in deaths. The review's introduction says that, compared with classical "
        "benzodiazepines, these drugs produce strong sedation and amnesia and raise the risk of breathing depression and death with "
        "other depressants, citing two papers (a review of how to find information on their potency, and a study of prescribed "
        "benzodiazepines taken with opioids by people starting dialysis), and presents no comparison of its own. It also reports, "
        "from agency sources, counterfeit Xanax (alprazolam) tablets holding etizolam, flualprazolam or phenazepam seized in the US, "
        "Australia, Singapore and Malaysia, flubromazolam first identified in tablets labelled 'XANAX', seven young people treated "
        "in emergency departments after taking what they thought was alprazolam (flualprazolam, not confirmed in three), and "
        "products holding variable amounts or other drugs, generally without the buyer knowing. What drug checking found in pills "
        "and powders sold as something else is in the answers on fake pills and on benzodiazepine test strips. Certainty: very low. "
        "Status: replicated."
    ),
    "plain": (
        "Are designer benzos like etizolam more dangerous? Nobody has compared them with prescription benzos, and the reports below "
        "count only people who got into trouble, not everyone who used them. In 234 reports to US poison centres in 2014 to 2017 that "
        "named a designer benzo and no other drug, mostly etizolam, 65 in 100 people were drowsy, 4 in 100 were in a coma and 3 in 100 needed a "
        "breathing tube; of those whose care was recorded, 22 in 100 went to intensive care, and one man died. For 85 in 100 of "
        "those with a recorded duration, the effects were over within a day. Nobody tested in a laboratory which drug these people "
        "had really taken. In published reports of deaths up to 2021, gathered second-hand by a review, almost all involved other "
        "drugs as well: 115 of 141 death entries also listed an opioid, and only 3 listed no other drug; a few people seem to be "
        "listed twice. Reports to US poison centres rose from 26 to 112 a year, partly because new codes were added in 2016; "
        "etizolam alone went from 26 to 60. Designer benzos have also turned up in fake Xanax pills."
    ),
    "population": (
        "People reported to US poison centres after an intentional exposure to a single coded designer benzodiazepine, 2014-2017 "
        "(234 reports); people in published case reports and forensic series up to March 2021, as compiled in one review (141 death "
        "entries, 63 impaired drivers and 44 emergency admissions; Finland, Germany, Japan, Norway, Poland, Sweden, the UK and the USA)"
    ),
    "exposure": (
        "Designer benzodiazepines (mostly etizolam, clonazolam, flualprazolam, flubromazolam and phenazepam), as named by callers and "
        "coded (poison centres) or found by forensic analysis (case reports), alone or with other drugs"
    ),
    "comparator": (
        "None: no comparison with prescribed benzodiazepines or with people who used designer benzodiazepines without harm; within "
        "the review's table, death entries with and without other drugs (editors' count)"
    ),
    "outcome": (
        "Clinical effects, treatments, level of care, graded outcome, duration and deaths coded by poison centres; deaths, impaired "
        "driving and emergency admissions in published reports, with the other drugs found"
    ),
    "relation": "insufficient-evidence",
    "magnitude": (
        "Carpenter et al. (2019), NPDS 2014-2017: 474 exposures; 234 intentional single-agent exposures analysed (etizolam 162, "
        "clonazolam 50, flubromazolam 13, diclazepam 4, flubromazepam 3, meclonazepam 1, norflurazepam 1); per year 26, 30, 66, 112 "
        "(etizolam alone 26, 30, 46, 60; other agents coded only from 2016); median age 25 (13-63); men 86%; suspected suicide 42 "
        "(18%). Of 234: drowsiness/lethargy 152 (65%), slurred speech 40 (17%), confusion 32 (14%), agitated/irritable 22 (9%; text "
        "14%), ataxia 21 (9%), tachycardia 20 (9%), hypotension 19 (8%), coma 10 (4%; text 8%), bradycardia 9 (4%); intubation 7 "
        "(3%). Disposition, 224 recorded (editors' sum): treated and released 92 (41%), non-critical admission 31 (14%), critical "
        "care 49 (22%), psychiatric facility 36 (16%), lost to follow-up or left 16 (7%). Outcome: major effect 9 (4%), death 1 "
        "(0.4%). Duration under 24 h 151 of 178 (84.8%, editors' sum; text 85%). No intervals; no laboratory confirmation. Brunetti "
        "et al. (2021), published reports to March 2021: 254 cases (141 deaths, 63 DUID, 44 ED, 3 outpatient, 2 self-administration, "
        "1 drug offence); deaths phenazepam 60, flualprazolam 38, etizolam 34, flubromazolam 4, five others 1 each. Editors' count "
        "of the Table 1 death entries: any opioid 115 of 141 (81.6%; etizolam 29 of 34, flualprazolam 27 of 38, phenazepam 53 of "
        "60, flubromazolam 3 of 4, others 3 of 5; methadone 51, morphine or 6-acetylmorphine 49), loperamide or its metabolite 2, "
        "no other substance 3; four apparent double entries, all with an opioid: 111 of 137 (81.0%) counting each once."
    ),
    "evidence": [
        C("PDF pp. 2-3",
          "Methods, 1st paragraph (PDF p. 2, continued on PDF p. 3) and 2nd paragraph (PDF p. 3)",
          "National Poison Data System records of reports by members of the public and health-care providers to US poison centres, "
          "coded by Specialists in Poison Information; forensic testing to confirm the reported exposure is not routinely performed. "
          "Retrieved: all intentional single-agent exposures to 11 designer benzodiazepines (adinazolam, clonazolam, cloniprazepam, "
          "diclazepam, etizolam, flubromazepam, flubromazolam, meclonazepam, nifoxipam, norflurazepam, pyrazolam), 1 January 2014 "
          "to 31 December 2017, all routes; accidental ingestions and exposures to more than one substance excluded. Etizolam had "
          "been tracked since 2007, but specific codes for all the other agents were added only in 2016; agents without a specific "
          "code could not be retrieved.",
          "qualifies"),
        C("PDF pp. 2-4",
          "Abstract › Results (PDF p. 2); Results, 1st paragraph (PDF p. 3); Table 1 and Table 2 with its footnote (PDF p. 4)",
          "474 designer benzodiazepine exposures were reported to poison centres in 2014-2017, of which 234 single-agent exposures met "
          "the inclusion criteria; 26 in 2014 and 112 in 2017, which the abstract calls a 330% increase; etizolam 162 (69%), "
          "clonazolam 50 (21%), flubromazolam 13, diclazepam 4, flubromazepam 3, meclonazepam 1, norflurazepam 1. Table 2: etizolam "
          "26, 30, 46 and 60 in 2014-2017, the other agents only in 2016-2017 (footnote: before 2016, data were collected only for "
          "etizolam). Table 1: median age 25 (range 13-63); 201 men (86%) and 32 women (14%); reason 'Abuse' 138 (59%), suspected "
          "suicide 42 (18%), 'Misuse' 31 (13%), intentional-unknown 23 (10%).",
          "supports"),
        C("PDF pp. 3-5",
          "Results, 2nd paragraph (PDF p. 3, continued on PDF p. 4); Table 3 (PDF p. 5)",
          "Table 3, the ten most common clinical effects and therapies among the 234: drowsiness/lethargy 152 (65%), slurred speech "
          "40 (17%), confusion 32 (14%), agitated/irritable 22 (9%), ataxia 21 (9%), tachycardia 20 (9%), hypotension 19 (8%), coma "
          "10 (4%), bradycardia 9 (4%); intubation 7 (3%), ventilator 5 (2%). The text gives agitation/irritability as 14% and coma "
          "as 8%, which match no count in the table, and adds respiratory depression (3%), respiratory arrest (0.4%) and cardiac "
          "arrest (0.4%); 224 (95%) of the exposures were by ingestion.",
          "supports"),
        C("PDF pp. 4-5",
          "Results, 3rd paragraph (PDF p. 4); Table 4 (PDF p. 5)",
          "Table 4: treated/evaluated and released 92 (41%), admitted to a non-critical care unit 31 (14%), to a critical care unit 49 "
          "(22%), to a psychiatric facility 36 (16%), lost to follow-up or left against medical advice 16 (7%) (editors' sum of the "
          "disposition rows: 224); outcome no effect 18 (8%), minor 101 (44%), moderate 76 (33%), major 9 (4%), death 1 (0.4%); "
          "duration under 2 h 8, 2-8 h 57, 8-24 h 86, 24 h-3 days 19, 3 days-1 week 7, over 1 week 1 (editors' sum 178, of which 151 "
          "under 24 h, 84.8%; the text says 85% of cases with clinical effects). The one death was a 29-year-old man after a "
          "reportedly intentional ('abuse') ingestion of etizolam, quantity unknown; one etizolam case had symptoms for more than a "
          "month, with kidney failure needing haemodialysis.",
          "supports"),
        C("PDF pp. 2, 4-6",
          "Abstract › Conclusions (PDF p. 2); Discussion, 1st and 2nd paragraphs (PDF p. 4, the 2nd continued on PDF p. 5), 4th "
          "paragraph (PDF p. 5) and 6th paragraph (PDF p. 6); Conclusions (PDF p. 6)",
          "A death after acute flubromazolam exposure described in the 2016 NPDS annual report was coded as 'Benzodiazepine' and so "
          "not retrieved; 234 of the 474 reports (49%) involved several agents and were neither collected nor analysed; no laboratory "
          "data confirmed the exposures, people likely bought the drug from an unregulated source and may have taken other compounds "
          "than those coded, and confirmatory testing is unavailable to most US clinicians; reporting is voluntary, effects may go "
          "unrecognised and be mis-coded, and only etizolam was tracked before 2016; people exposed without significant symptoms were "
          "probably not reported, so the authors expect totals to be under-reported and severity over-reported. The authors conclude "
          "that the incidence of exposures is rising and will likely keep rising, that effects are generally consistent with a "
          "sedative-hypnotic toxidrome and mostly resolve within 24 h, and that severe effects, including death, are infrequent.",
          "qualifies"),
        B("pp. 1, 3-4, 39-40",
          "Abstract (p. 1); 2. Results, 1st-3rd paragraphs (pp. 3-4); 4. Materials and Methods, single paragraph (p. 39); Funding "
          "(p. 40)",
          "Scoping review by forensic toxicologists in Ancona and Philadelphia, partly funded by the Italian government's Department "
          "of Antidrug Policy: 31 designer benzodiazepines considered; PubMed, Scopus, Google Scholar and Web of Science searched to "
          "March 2021, with agency reports; references reviewed for relevance by one author; included were reports in which a "
          "designer benzodiazepine was the sole or explicit contributory cause of poisoning, driving impairment or death; of 372 "
          "potentially relevant reports, 324 were excluded and 49 included, on 12 drugs; 254 cases reported 2008-2021: 1 drug "
          "offence, 2 self-administration studies, 3 outpatient admissions, 44 emergency-department admissions, 63 DUID and 141 "
          "deaths, tabulated in Table 1. Most patients and decedents were young, of both sexes, often with a history of substance "
          "use and mental illness; cases came from Finland, Germany, Japan, Norway, Poland, Sweden, the UK and the USA. The included "
          "reports are not appraised.",
          "qualifies"),
        B("pp. 5-34",
          "Table 1, rows with Study 'Death' (Compound and Co-Exposure columns)",
          "Editors' count of Table 1 (one row per ruled cell of the Concentration column; 254 rows in all, matching the review's 141 "
          "deaths, 63 DUID, 44 ED, 3 outpatient, 2 self-administration and 1 drug offence): death entries phenazepam 60, "
          "flualprazolam 38, etizolam 34, flubromazolam 4, and adinazolam, deschloroetizolam, diclazepam, flubromazepam and pyrazolam "
          "1 each. 115 of the 141 death entries list at least one opioid in the Co-Exposure column: methadone or EDDP 51, morphine or "
          "6-acetylmorphine 49, codeine 19, fentanyl, norfentanyl, acetylfentanyl or 4-ANPP 16, dihydrocodeine 12, buprenorphine or "
          "norbuprenorphine 9, brorphine 6, tramadol 5, hydrocodone 4, U-47700 3, isotonitazene 3, tapentadol 1; by drug, etizolam "
          "29 of 34, flualprazolam 27 of 38, phenazepam 53 of 60, flubromazolam 3 of 4, the other five 3 of 5. Two more list "
          "loperamide (p. 18) or desmethyl-loperamide with ethanol (p. 20); 3 list no other substance: an etizolam death recorded as "
          "suicide, with only etizolam metabolites (p. 7), and two flualprazolam deaths (p. 18). Counted per entry; the review gives "
          "no such count.",
          "supports"),
        B("pp. 10-13, 22, 26-27, 31",
          "Table 1, death rows: etizolam (pp. 10-13), flualprazolam (p. 22), flubromazolam (pp. 26-27), phenazepam (p. 31)",
          "Four apparent double entries (the same age and identical concentrations of several drugs, listed under two designer "
          "benzodiazepines): a 39-year-old man (p. 12 under etizolam; p. 26 under flubromazolam, with etizolam among the "
          "co-exposures; the morphine values differ); a 49-year-old man (p. 11 under etizolam, with flubromazepam among the "
          "co-exposures; p. 26 under flubromazolam, with etizolam; the morphine and pregabalin values differ); a 33-year-old "
          "(p. 13 under etizolam, male, with flubromazolam; p. 27 under flubromazolam, female, with etizolam); a 37-year-old man "
          "(p. 10 under etizolam; p. 22 under flualprazolam, with etizolam). All four pairs list an opioid. Two identical "
          "phenazepam entries on p. 31 may be a fifth. Editors' calculation counting each of the four once: 111 of 137 entries "
          "with an opioid.",
          "qualifies"),
        B("pp. 29, 36-38",
          "2.5 Etizolam and 2.6 Flualprazolam, single paragraphs (p. 36); 2.10 Phenazepam and 3-Hydroxyphenazepam, single paragraph "
          "(p. 37, continued on p. 38); Table 1, phenazepam death rows 'Phenazepam intoxication' (p. 29)",
          "Text: of 34 etizolam deaths, 33 had the cause recorded as accidental overdose due to polydrug toxicity, in people known to "
          "use drugs or with a history of mental disorders, and 1 was a suicide; all 38 flualprazolam deaths involved multiple drugs, "
          "36 recorded as accidental multiple drug toxicity and 2 ruled intentional flualprazolam poisonings; of 60 phenazepam deaths, "
          "phenazepam alone was listed as the sole cause in 2 and the rest were attributed to accidental polydrug overdose. Table 1 "
          "lists those two ('Phenazepam intoxication') with ethanol (a 46-year-old man) and with diazepam and dihydrocodeine "
          "(a 26-year-old man). Etizolam is used as a medicine in India, Italy, Japan and Korea and is not "
          "approved elsewhere (2.5); phenazepam is used as a medicine in the former USSR (2.10).",
          "qualifies"),
        B("pp. 35-37",
          "2.2 Clonazolam (p. 35); 2.4 Diclazepam (p. 35, continued on p. 36); 2.5 Etizolam and 2.6 Flualprazolam (p. 36); "
          "2.7 Flubromazepam and 2.8 Flubromazolam (p. 37)",
          "Emergency cases as the drug-by-drug text describes them: clonazolam, primary adverse effect CNS depression (two of six not "
          "confirmed, amounts self-reported); diclazepam, 2 of 3 in a severe state of agitation and disorientation with stimulants "
          "and dissociatives also detected, the third with CNS depression and a withdrawal syndrome; etizolam, three children drowsy "
          "and wobbly after eating coloured pills thought to be sweets (confirmed in one) and a man found unconscious next to a "
          "syringe of heroin; flualprazolam, seven young people after a benzodiazepine thought to be alprazolam, three sedated with "
          "verbal impairment, two with CNS depression and two without symptoms, flualprazolam not confirmed in three; flubromazepam, "
          "four in profound agitation and delirium followed by rigidity and CNS depression; flubromazolam, 18 in a severe state of "
          "CNS depression with functional and motor impairment, the sole drug detected in 16. Flubromazolam was first identified in "
          "Sweden in 10 seized white tablets labelled 'XANAX'.",
          "supports"),
        B("p. 39",
          "3. Discussion, 4th paragraph",
          "Few pharmacokinetic studies exist, so concentrations cannot yet be related to effects; diclazepam, etizolam and "
          "phenazepam blood concentrations overlapped in impaired and non-impaired drivers, and etizolam and flualprazolam "
          "concentrations were similar in DUID cases and deaths (the authors suggest differences in tolerance); because polypharmacy "
          "is the rule, causation often cannot be assigned to a single drug; many people exposed may never develop significant "
          "adverse events (citing Carpenter et al.); many cases go undetected for lack of analytical methods or awareness; the newest "
          "drugs may cross-react with common benzodiazepine immunoassays, which often cannot tell designer from prescribed "
          "benzodiazepines; how pathologists and toxicologists attribute the role of these drugs in deaths is largely unknown.",
          "qualifies",
          quote="polypharmacy is the rule rather than the exception"),
        B("pp. 2-3, 38",
          "1. Introduction, 3rd paragraph and 4th paragraph (p. 2, the 4th continued on p. 3); 3. Discussion, 1st-2nd paragraphs "
          "(p. 38)",
          "The authors state that, compared with classical benzodiazepines, these compounds produce strong sedation and amnesia and "
          "raise the risk of respiratory depression and death when combined with other CNS depressants, citing a review of how to "
          "find information on their potency and a study of prescribed benzodiazepines co-dispensed with opioids in people starting "
          "haemodialysis (references 41 and 42); no comparative data are presented. They are illegally manufactured, sometimes made "
          "to look like legal medicines, and bought cheaply online; according to the UNODC, bulk materials are processed in Europe "
          "and sold as fake alprazolam or diazepam; counterfeit Xanax (alprazolam) and erimin-5 (nimetazepam) tablets containing "
          "etizolam, flualprazolam and phenazepam were seized in the US, Australia, Singapore and Malaysia; products may hold "
          "variable amounts of active ingredient or contaminants such as novel synthetic opioids, generally without the buyer "
          "knowing; they are sold online as blotters, liquids, pills, powders and tablets; etizolam, flualprazolam and flubromazolam "
          "were found in counterfeit Xanax tablets in Canada.",
          "qualifies"),
    ],
    "grade": {
        "starting_level": "low",
        "domains": {
            "risk_of_bias": {"levels": 1, "note": (
                "Poison-centre reports: the drug is the caller's report as coded, never confirmed in a laboratory; voluntary reporting "
                "favours people with symptoms; half of all reports (those with other substances) were excluded; codes changed in "
                "2016; two percentages in the text contradict the table (card sc_carpenter_2019: JBI, moderate as a description, high "
                "as evidence of what a named drug does). Published cases: severe and detected cases, chosen by one author with no "
                "stated rule for judging contribution, not appraised, with some people apparently listed twice (card "
                "sc_brunetti_2021: high).")},
            "inconsistency": {"levels": 0, "note": (
                "The two sources agree in direction: the reported effects are mostly sedation, and deaths without other drugs are rare "
                "in both (1 death among 234 single-substance poison-centre reports; 3 of 141 death entries in the review's table list "
                "no other drug).")},
            "indirectness": {"levels": 1, "note": (
                "The deaths are known only through a review's compilation of case reports, which were not read (second-hand); the "
                "poison-centre data cover single-substance reports only, while most deaths involved other drugs; neither source "
                "compares designer with prescribed benzodiazepines, which is why the claim is worded as insufficient evidence for "
                "that comparison.")},
            "imprecision": {"levels": 0, "note": (
                "Counts of reports; the one death among 234 single-substance reports is a single event, which the statement gives "
                "as a count.")},
            "publication_bias": {"levels": 0, "note": (
                "The selection of published cases is counted under risk of bias, not twice.")},
            "large_effect": {"levels": 0},
            "dose_response": {"levels": 0},
            "plausible_confounding": {"levels": 0},
        },
        "certainty": "very-low",
        "reasoning": (
            "Insufficient evidence for the comparison the question asks about: no source read compares designer with prescribed "
            "benzodiazepines, and neither has a count of the people who used them, so neither gives a risk per use. The descriptive "
            "findings start low (poison-centre records and case reports), are downgraded one level for risk of bias and one for "
            "indirectness (bounded at very low), and are never upgraded. Status replicated: two independent sources, a national US "
            "poison-centre series and a review of case reports from eight countries that does not include that series, agree in "
            "direction (mostly sedation; deaths without other drugs rare); each figure comes from one source, and the review cites "
            "the poison-centre study only for the point that many people exposed may have no serious effects. The share of death "
            "entries listing an opioid is the editors' count of the review's table (115 of 141; 111 of 137 counting each apparent "
            "double entry once), which the review itself does not give; it describes which drugs were found together in reported "
            "deaths, not whether the combination caused them."
        ),
    },
    "status": "replicated",
    "verification": {
        "status": "draft",
        "drafted_by": "AI reader 755 (claim writer)",
        "drafted_on": D,
        "flag_note": (
            "Question 8 of round pdf-2026-11-26 (forum theme: research chemicals; 'etizolam vs xanax', 132,000 views). Not read: the "
            "reports compiled in Brunetti's Table 1 (for example Papsun et al., 2021, J Anal Toxicol 45:226-232, flualprazolam in 197 "
            "forensic cases; Kriikku et al., 2020, Forensic Sci Int 307:110101; Shearer et al., 2015, Forensic Sci Int 254:197-204, "
            "phenazepam deaths in South Scotland; Hikin et al., 2021, Med Sci Law 61:122-129, etizolam in post-mortem cases), the "
            "UNODC reports the review cites, the 2016 NPDS annual report (Gummin et al., 2017, Clin Toxicol 55:1072-1254; the "
            "flubromazolam death) and Carpenter's online supplement (the Poisindex codes); neither PDF prints DOIs for them. No study "
            "read here compares designer with prescribed benzodiazepines, or designer benzodiazepines with opioids against either "
            "alone. Pages: benzodiazepines."
        ),
    },
    "version": "0.1.0",
    "changelog": [{"version": "0.1.0", "date": D, "change": (
        "Drafted by AI reader 755 (claim writer) from Carpenter et al. (2019) and Brunetti et al. (2021), each read in full from the "
        "PDF; Brunetti's Table 1 death entries recounted; anchors ai-located; round pdf-2026-11-26, question 8.")}],
}

# ---------------------------------------------------------------- plain lines
V = "0.1.0"
simple = {
    "claims": {
        "cl_lsd_nbome": {
            "v": V,
            "q": "What are NBOMes, and are they sold as LSD?",
            "pages": ["lsd", "2c-x"],
            "short": ("Yes, sometimes. NBOMes are lab-made drugs, mostly sold on blotters. In case reports up to 2014, several people "
                      "who got sick or died thought they'd taken LSD."),
            "but": ("Nobody has counted how often 'LSD' blotters hold NBOMes. And these are reports of people who got sick, so they "
                    "can't say how risky one use is."),
            "how": [
                ("NBOMes are lab-made relatives of the 2C drugs. Of the first 10 found in Europe, from 2011 to 2013, 8 were on "
                 "blotters. In some cases, blotters taken as 'acid' turned out to hold an NBOMe."),
                ("In 29 published cases of poisoning, nearly all had a racing heart and about 4 in 10 had seizures. Some needed "
                 "intensive care, a breathing machine or dialysis."),
                ("Published cases are often the worst ones. Of 25 cases reported to Texas poison centres, 4 in 100 had seizures, "
                 "against about 38 in 100 published cases."),
                ("By 2014, eight deaths had been reported with 25I-NBOMe, and a lab found it in five. Some had taken other drugs too. "
                 "The review says its role in the deaths was often unclear."),
            ],
            "how_src": [["wood_2015"], ["wood_2015"], ["wood_2015"], ["wood_2015"]],
            "rate": ("One review of case reports up to 2014. Case reports pick out people who got very sick, only about half had the "
                     "drug found in their own samples, and nobody counted everyone who used NBOMes."),
        },
        "cl_benzo_designer": {
            "v": V,
            "q": "Are designer benzos like etizolam more dangerous?",
            "pages": ["benzodiazepines"],
            "short": ("Nobody has tested that. Of 141 deaths with a designer benzo in published reports, 115 also listed an opioid, "
                      "and only 3 listed no other drug."),
            "but": ("These reports only count people who got into trouble, not everyone who used. So they can't say how risky one "
                    "use is."),
            "how": [
                ("US poison centres, 2014 to 2017: in 234 reports naming a designer benzo and no other drug, mostly etizolam, 65 in "
                 "100 people were drowsy and 3 in 100 needed a breathing tube. One man died."),
                ("Nobody lab-tested which drug these people took. Reports rose from 26 to 112 a year, partly because new drugs got "
                 "their own codes in 2016."),
                ("A review of published cases to 2021 found 141 death entries, mostly phenazepam, flualprazolam and etizolam. 115 "
                 "also listed an opioid, and only 3 listed no other drug. A few people seem to be listed twice."),
                ("Designer benzos have turned up in fake Xanax pills, and buyers often don't know what's in them."),
            ],
            "how_src": [["carpenter_2019"], ["carpenter_2019"], ["brunetti_2021"], ["brunetti_2021"]],
            "rate": ("Reports of people who got sick or died, with no count of everyone who used. The poison-centre drugs were never "
                     "lab-checked, and the deaths come from a review of case reports."),
        },
    },
    "tf": {
        "lsd": [
            {"claim": "cl_lsd_nbome", "v": V, "statement": "Blotters taken as LSD always hold LSD.", "answer": False,
             "why": "In some reported cases, blotters taken as 'acid' held an NBOMe instead. Nobody has counted how often this happens."},
            {"claim": "cl_lsd_nbome", "v": V, "statement": "Published NBOMe cases had far more seizures than poison centre cases.",
             "answer": True,
             "why": ("About 38 in 100 published cases had seizures, against 4 in 100 of 25 cases at Texas poison centres. Published "
                     "cases are often the worst ones.")},
        ],
        "benzodiazepines": [
            {"claim": "cl_benzo_designer", "v": V, "statement": "Most deaths linked to designer benzos involved no other drug.",
             "answer": False,
             "why": "In a review of published cases, 115 of 141 death entries also listed an opioid, and only 3 listed no other drug."},
            {"claim": "cl_benzo_designer", "v": V, "statement": "Designer benzos have been shown to be riskier than prescribed benzos.",
             "answer": False,
             "why": ("Nobody has compared them. The reports only count people who got into trouble, so they can't say how risky one "
                     "use is.")},
        ],
    },
}

import re

KEEP = {"drafted_on", "located_on", "date", "id", "reference", "study_card", "relation", "status", "anchor_status", "role",
        "substance", "starting_level", "certainty", "version", "v", "claim", "pages", "how_src"}


def dash(s):
    """En dashes for number ranges (pages, years, ages, durations); ISO dates, the round id and chemical names keep hyphens."""
    keep = {}
    def hold(m):
        keep[f"\x00{len(keep)}\x00"] = m.group(0)
        return f"\x00{len(keep) - 1}\x00"
    s = re.sub(r"pdf-\d{4}-\d{2}-\d{2}|\b\d{4}-\d{2}-\d{2}\b|\d+\.\d+/[\w.()/-]+", hold, s)
    s = re.sub(r"(?<=\d)-(?=\d)", "–", s)
    s = re.sub(r"(?<=\d(st|nd|rd|th))-(?=\d)", "–", s)
    s = s.replace(" h-3 days", " h–3 days").replace("days-1 week", "days–1 week").replace(
        "intentional-unknown", "intentional–unknown")
    for k, v in keep.items():
        s = s.replace(k, v)
    return s


def fix(o, key=None):
    if isinstance(o, dict):
        return {k: (v if k in KEEP else fix(v, k)) for k, v in o.items()}
    if isinstance(o, list):
        return [fix(x, key) for x in o]
    if isinstance(o, str):
        return dash(o)
    return o


nbome, benzo, simple = fix(nbome), fix(benzo), fix(simple)

if __name__ == "__main__":
    json.dump([nbome, benzo], open("data/claims/_incoming/pdf1126_w755.json", "w"), indent=1, ensure_ascii=False)
    open("data/claims/_incoming/pdf1126_w755.json", "a").write("\n")
    json.dump(simple, open("data/verification/pdf-2026-11-26/755_simple.json", "w"), indent=1, ensure_ascii=False)
    open("data/verification/pdf-2026-11-26/755_simple.json", "a").write("\n")
    print("written")
