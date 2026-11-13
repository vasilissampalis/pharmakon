# _Tolerance — search log (PRISMA 2020)

Protocol: METHODS.md §2; brief of 2026-10-17 (tolerance evidence map, every drug page). Run by AI reader 30 on 2026-10-17.

**Source.** PubMed through the E-utilities interface (`esearch.fcgi?db=pubmed`, `esummary.fcgi`; `efetch.fcgi` abstracts only where a title was ambiguous), fetched from a tab of the app's browser at about one request per second. Hit counts are PubMed's `count` on 2026-10-17. Screening: titles and journals (abstracts where needed) against the five questions of the brief; kept items are named by PMID with their number in `_Tolerance_DOI-LIST.md`. Every listed DOI was then fetched from Crossref `works/<DOI>` in a second tab (title, year, first author, `updated-by`). Where PubMed has no DOI, a Crossref `query.bibliographic` search (title + first author + year, 3 rows) located it before the `works/<DOI>` fetch; these are marked "DOI via Crossref search".

Field tags: `[tiab]` title/abstract, `[ti]` title, `[MeSH Terms]`. `humans[MeSH Terms]` was used as a filter where the literature is large; it drops pre-1966 records without MeSH, so the classic psychedelic studies were searched without it.

---

## 1. Alcohol

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| A1 | `(ethanol[tiab] OR alcohol[tiab]) AND ("acute tolerance"[tiab] OR Mellanby[tiab] OR "chronic tolerance"[tiab] OR "acquired tolerance"[tiab] OR "behavioral tolerance"[tiab] OR "behavioural tolerance"[tiab] OR "functional tolerance"[tiab]) AND humans[MeSH Terms]` | 181 | 28277803→1; 33631255→2; 8214406→3; 28280882→4; 18540784→7; 5565850→8; 22023021→10; 35701549→12; 18619740→13; 12877310→24. Not kept: animal and cell studies indexed as human, single acute-tolerance laboratory studies already covered by the reviews (#1, #7), driving-decision studies, studies of other drugs. |
| A2 | `(alcohol[ti] OR ethanol[ti]) AND (tolerance[ti] OR "cross-tolerance"[ti]) AND humans[MeSH Terms] NOT (glucose[ti] OR lactose[ti] OR immun*[ti] OR exercise[ti] OR "distress tolerance"[ti] OR intolerance[ti])` | 312 (136 new) | 31950152→6; 32212746→29; 7182673→9; 22763668→11; 21862534→14; 9514287→15; 7587972→20; 10807215→21; 35792050→22; 32873498→23; 3511175→25; 6264608→27; 21049267 (→ Cannabis); 6432093 (→ Benzodiazepines). Not kept: hand-rub skin tolerance, zero-tolerance laws, invertebrate and rodent models, non-English items without abstract. |
| A3 | `("Alcoholism"[MeSH Terms] OR "alcohol dependence"[tiab] OR "alcohol use disorder"[tiab] OR alcoholics[tiab]) AND (abstinence[tiab] OR detoxification[tiab] OR abstinent[tiab]) AND ("Positron-Emission Tomography"[MeSH Terms] OR "Tomography, Emission-Computed, Single-Photon"[MeSH Terms]) AND (receptor*[tiab]) AND (recovery[tiab] OR normaliz*[tiab] OR longitudinal[tiab] OR "time course"[tiab] OR "follow-up"[tiab] OR weeks[tiab])` | 22 | 16061765→5; 25453062→16; 32919411→17; 24553924→18; 28108358→19. Not kept: cross-sectional receptor studies without a time course. |
| A4 | `(alcohol[tiab] OR ethanol[tiab]) AND ("cross-tolerance"[tiab] OR "cross tolerance"[tiab] OR "cross-tolerant"[tiab]) AND humans[MeSH Terms]` | 56 (49 new) | 7072468→28. Not kept: withdrawal-management reviews that mention cross-tolerance only as the rationale for benzodiazepine treatment, rodent studies. |
| A5 | `("alcohol poisoning"[tiab] OR "ethanol poisoning"[tiab] OR "fatal alcohol"[tiab] OR "acute alcohol intoxication"[tiab]) AND (tolerance[tiab] OR tolerant[tiab]) AND ("blood alcohol"[tiab] OR "blood ethanol"[tiab] OR "blood-alcohol"[tiab] OR "blood-ethanol"[tiab])` | 10 (7 new) | 6375435→26. |

DOIs via Crossref search: Jones & Holmgren 2003 (10.1520/jfs2002420), Perper 1986 (10.1520/jfs11873j). Not found in Crossref and not listed: Khanna & Mayer 1982, "An analysis of cross-tolerance among ethanol, other general depressants and opioids" (Subst Alcohol Actions Misuse; no DOI); Vogel-Sprott 1997, "Is behavioral tolerance learned?" (Alcohol Health Res World; PMC6826826, no DOI).

## 2. Benzodiazepines

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| B1 | `(benzodiazepine*[tiab] OR diazepam[tiab] OR lorazepam[tiab] OR alprazolam[tiab] OR clonazepam[tiab] OR triazolam[tiab] OR temazepam[tiab] OR midazolam[tiab] OR chlordiazepoxide[tiab]) AND (tolerance[ti] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab] OR "tolerance development"[tiab]) AND humans[MeSH Terms]` | 209 (185 new) | 23515374→30; 6134543→31; 10193652→32; 10529072→34; 23617374→36; 1670787→37; 6661348→38; 4036631→39; 2868609→40; 7862837→41; 3720528→42; 7334143→44; 6440434→45; 2908405→46; 33957437→47; 1675689→51; 2858077→52; 26733466→54; 41748921→55. Not kept: "tolerance" of procedures (endoscopy, bronchoscopy), ICU sedation and neonatal opioid papers, case reports, non-English trials of drug "tolerance" (= tolerability). |
| B2 | `(benzodiazepine*[tiab]) AND (flumazenil[tiab] OR iomazenil[tiab] OR "Ro15-4513"[tiab]) AND ("Positron-Emission Tomography"[MeSH Terms] OR "Tomography, Emission-Computed, Single-Photon"[MeSH Terms]) AND ("long-term"[tiab] OR chronic[tiab] OR dependence[tiab] OR dependent[tiab] OR withdrawal[tiab] OR tolerance[tiab] OR users[tiab])` | 36 (33 new) | None new (stroke, brain injury and alcohol-dependence imaging; Fujita 1999 already from B1). No PET/SPECT study of people taking benzodiazepines long term apart from #32. |
| B3 | `(benzodiazepine*[ti] OR hypnotic*[ti] OR anxiolytic*[ti]) AND ("long-term"[ti] OR chronic[ti] OR prolonged[ti]) AND (efficacy[tiab] OR tolerance[tiab] OR cognitive[ti] OR cognition[ti]) AND ("Meta-Analysis"[pt] OR "Systematic Review"[pt] OR "Review"[pt])` | 32 (30 new) | 14731058→33; 31274696→48; 29244060→49; 15033227→50. |
| B4 | `(benzodiazepine*[ti]) AND (tolerance[ti]) AND ("Review"[pt] OR "Systematic Review"[pt] OR "Meta-Analysis"[pt]) AND 2005:2026[dp]` | 4 (2 new) | 29872302→53. |
| B5 | Known-item check: `Vinkers CH[au] AND tolerance[ti] AND benzodiazepine*[ti]` | 1 | 22536226→35. |
| — | From A2 (Alcohol) | — | 6432093→43. |

DOI note: Soldatos et al. 1999 has no DOI in PubMed; a Crossref search returned two records with identical metadata (vol 14, issue 5, pp 287–304): 10.1097/00004850-199909000-00004 (listed) and 10.1097/00004850-199914050-00004. Both resolve in Crossref; neither has `updated-by`.

## 3. GHB / GBL

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| G1 (first form, discarded) | `("gamma-hydroxybutyrate"[tiab] OR "gamma-hydroxybutyric acid"[tiab] OR "hydroxybutyrate"[ti] OR GHB[tiab] OR "sodium oxybate"[tiab] OR "gamma-butyrolactone"[tiab] OR GBL[tiab] OR butanediol[tiab] OR "Sodium Oxybate"[MeSH Terms]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab] OR tolerant[tiab])` | 313 | Too broad (microbial "solvent tolerance", 2,3-butanediol, glucose tolerance); replaced by G1. |
| G1 | `("gamma-hydroxybutyrate"[tiab] OR "gamma-hydroxybutyric acid"[tiab] OR "4-hydroxybutyrate"[tiab] OR GHB[tiab] OR "sodium oxybate"[tiab] OR "gamma-butyrolactone"[tiab] OR GBL[tiab] OR "1,4-butanediol"[tiab]) AND (tolerance[ti] OR "cross-tolerance"[tiab] OR "tolerance development"[tiab] OR tachyphylaxis[tiab] OR (tolerance[tiab] AND (dependence[tiab] OR withdrawal[tiab] OR abuse[tiab] OR recreational[tiab])))` | 64 | 26074743→59; 11579621→57; 14723976→66; 7737330→70; 14744611→71; 17026996→72; 12837642→73; 12831503→74. |
| G2 | `(GHB[tiab] OR "gamma-hydroxybutyrate"[tiab] OR "gamma-hydroxybutyric acid"[tiab] OR GBL[tiab] OR "gamma-butyrolactone"[tiab]) AND (dependence[tiab] OR dependent[tiab] OR detoxification[tiab] OR withdrawal[tiab]) AND (relapse[tiab] OR coma[tiab] OR overdose[tiab] OR "frequency of use"[tiab] OR daily[tiab] OR cohort[tiab] OR "follow-up"[tiab]) AND humans[MeSH Terms]` | 137 | 28004314→60; 27923198→58; 20925687→61; 33417072→62; 26855327→63; 20166080→65; 12733850→68. Not kept: case reports of withdrawal, sodium oxybate trials for alcohol dependence, records matched through "GHb" (glycated haemoglobin). |
| G3 | `(GHB[ti] OR "gamma-hydroxybutyrate"[ti] OR "gamma-hydroxybutyric acid"[ti] OR "sodium oxybate"[ti]) AND (dependence[ti] OR tolerance[tiab]) AND ("Review"[pt] OR "Systematic Review"[pt] OR "long-term"[ti] OR "12-month"[ti] OR extension[ti])` | 27 (12 new) | 27003176→56; 19968016→64; 12627729→69. |
| G4 | Known-item check for the correction to #64: `sodium oxybate[ti] AND correction[ti] AND safety[ti]` (an exact-title form returned 0) | 1 | 21897784→67. |

DOIs via Crossref search: U.S. Xyrem Multicenter Study Group 2003, Sleep (10.1093/sleep/26.1.31); Wang et al. 2009 (10.5664/jcsm.27549). The same search surfaced the 2011 correction (10.5664/jcsm.1214), which `updated-by` on the 2009 record does not carry. A DOI tried for Kamal et al. 2016 before reading the PubMed record (10.1159/000446225) resolved to an unrelated paper and was dropped; the PubMed DOI (10.1159/000443173) was fetched and matches.

## 4. Caffeine

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| C1 | `caffeine[ti] AND (tolerance[ti] OR "complete tolerance"[tiab] OR "partial tolerance"[tiab] OR "tolerance develop*"[tiab] OR "withdrawal reversal"[tiab] OR tachyphylaxis[tiab] OR "cross-tolerance"[tiab]) NOT (glucose[ti] OR insulin[ti] OR "exercise tolerance"[ti] OR orthostatic[ti])` | 114 | 7009653→75; 1410146→76; 14967827→77; 16001109→78; 30673725→79; 5638095→80; 2772103→81; 2060564→82; 8422743→83; 12392588→84; 15882556→85; 19241060→86; 27762662→87; 31900579→88; 32708555→89; 12601503→90; 20520601→91; 23108937→92; 9989559→95; 9989558→98; 6888193→99; 3807640→100. Not kept: yeast, plant and insect "caffeine tolerance", letters in Circulation 2003, most rodent studies. |
| C2 | `caffeine[tiab] AND ("adenosine A1"[tiab] OR "A1 adenosine"[tiab] OR "A2A"[tiab] OR "adenosine receptor*"[tiab]) AND ("Positron-Emission Tomography"[MeSH Terms] OR PET[tiab] OR "receptor availability"[tiab] OR "receptor occupancy"[tiab]) AND humans[MeSH Terms]` | 15 | None: receptor-occupancy and sleep-deprivation PET studies, no study of receptor change with regular intake. |
| C3 | `caffeine[ti] AND (habitual[ti] OR regular[ti] OR "daily intake"[ti] OR chronic[ti] OR "low consumers"[tiab] OR "non-consumers"[tiab] OR nonconsumers[tiab] OR "caffeine-naive"[tiab] OR "caffeine naive"[tiab]) AND ("blood pressure"[tiab] OR performance[tiab] OR alertness[tiab] OR sleep[tiab] OR anxiety[tiab] OR "cerebral blood flow"[tiab]) AND humans[MeSH Terms]` | 114 (103 new) | None beyond C1 (sports-supplement trials comparing habitual and non-habitual consumers were left to the Caffeine monograph's own list). |
| C4 | Known-item checks: `(caffeine[ti]) AND ((Weibel J[au] AND adaptation[tiab]) OR (Varani K[au] AND platelets[tiab]) OR (Juliano LM[au] AND withdrawal[ti]) OR ("adenosine receptor*"[ti] AND (chronic[ti] OR consumption[ti]) AND humans[MeSH Terms]))` | 9 | 31866308→94; 15448977→93; 10330379→96; 10899090→97. |

## 5. Nicotine and tobacco

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| N1 | `(nicotine[ti] OR smoking[ti] OR smokers[ti] OR tobacco[ti] OR cigarette*[ti]) AND (tolerance[ti] OR "acute tolerance"[tiab] OR "chronic tolerance"[tiab] OR tachyphylaxis[tiab] OR "cross-tolerance"[tiab]) AND humans[MeSH Terms] NOT (glucose[ti] OR exercise[ti] OR "distress tolerance"[ti] OR "pain tolerance"[ti] OR "zero tolerance"[ti])` | 120 (111 new) | 8071855→102; 11685379→103; 2587748→106; 7617803→107; 1797521→108; 2498949→109; 11105943→110; 2392509→111; 3680508→112; 3131804→113; 8033495→114; 12090675→115; 11181916→116; 18452252→121. Not kept: Fagerström Tolerance Questionnaire psychometrics (a dependence scale, not tolerance), transgenic tobacco plants, transplant "tolerance". 12521400→101 came from A1 (Alcohol). |
| N2 | `(nicotinic[tiab]) AND (smokers[tiab] OR smoking[tiab] OR tobacco[tiab]) AND (abstinence[tiab] OR abstinent[tiab] OR "quit"[tiab] OR cessation[tiab]) AND ("Positron-Emission Tomography"[MeSH Terms] OR "Tomography, Emission-Computed, Single-Photon"[MeSH Terms] OR "receptor availability"[tiab] OR upregulation[tiab])` | 65 (64 new) | 19487632→104; 16928859→105; 17942810→117; 18794265→118; 24360979→119; 23429692→120. Not kept: rodent and cell upregulation studies. |
| N3 | `Perkins KA[au] AND (tolerance[tiab] OR "acute tolerance"[tiab] OR sensitivity[ti]) AND nicotine[tiab]` | 29 (13 new) | None new (initial-sensitivity studies in people who do not smoke). |
| N4 | `"green tobacco sickness"[tiab] AND (nonsmokers[tiab] OR "non-smokers"[tiab] OR "smoking status"[tiab] OR tolerance[tiab]) AND (systematic[tiab] OR review[pt] OR cohort[tiab] OR prevalence[tiab])` | 3 | None (checked for tolerance as protection against nicotine toxicity). |

DOIs via Crossref search: Perkins et al. 1994 (10.1016/s0022-3565(25)22421-1) and Perkins et al. 2001, JPET (10.1016/s0022-3565(24)38826-3). Crossref spells #107's title "tolerence"; same paper.

## 6. Cocaine

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| K1 | `(cocaine[ti] OR crack[ti]) AND (tolerance[ti] OR "acute tolerance"[tiab] OR tachyphylaxis[tiab] OR "cross-tolerance"[tiab] OR "chronic tolerance"[tiab] OR "tolerance develop*"[tiab] OR sensitization[ti]) AND humans[MeSH Terms]` | 84 (77 new) | 4078729→122; 9509494→123; 20001286→124; 3390996→127; 2019989→128; 15159138→129; 3234239→130; 3386392→131; 9298515→132; 11822993→133; 8981391→134; 18720516→135. Not kept: rodent sensitization studies indexed as human, NIDA monograph chapters without DOI (Ambre 1989–1991, Fischman 1981), "crack tolerance" in materials science. |
| K2 | `cocaine[tiab] AND (abstinence[tiab] OR abstinent[tiab] OR detoxified[tiab] OR withdrawal[tiab]) AND ("dopamine transporter*"[tiab] OR "D2 receptor*"[tiab] OR "D2/D3"[tiab] OR "D2/3"[tiab] OR "mu-opioid"[tiab] OR "serotonin transporter"[tiab] OR "kappa opioid"[tiab]) AND ("Positron-Emission Tomography"[MeSH Terms] OR "Tomography, Emission-Computed, Single-Photon"[MeSH Terms]) AND (recovery[tiab] OR longitudinal[tiab] OR weeks[tiab] OR months[tiab] OR "follow-up"[tiab] OR duration[tiab])` | 12 | 15953495→140; 18762918→141; 21054687→142. |
| K3 | Known-item check for the imaging landmarks: `cocaine[ti] AND ((Volkow ND[au] AND (dopamine[ti] OR dopaminergic[ti]) AND (detoxified[tiab] OR abstinence[tiab] OR "D2 receptor"[ti])) OR (Martinez D[au] AND "dopamine release"[ti]) OR (Malison RT[au] AND transporter*[ti]))` | 18 (17 new) | 28297025→125; 24912491→126; 17403976→136; 9126741→137; 8101394→138; 9619159→139. |
| K4 | Known-item check (surfaced by a Crossref search while working on Methamphetamine): `"repeated dosing with oral cocaine in humans"[ti] OR (cocaine[ti] AND oral[ti] AND repeated[ti] AND humans[ti])` | 1 | 19653786→143 (renumbered in the final list). |

DOIs via Crossref search: Fischman et al. 1985 (10.1016/s0022-3565(25)24216-1); Foltin & Fischman 1991 (10.1016/s0022-3565(25)24787-5). Abstracts read (efetch) to confirm the time-course notes for #138 and #140.

## 7. Amphetamine

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| AM1 | `(amphetamine[ti] OR dextroamphetamine[ti] OR "d-amphetamine"[ti] OR lisdexamfetamine[ti] OR dexamphetamine[ti] OR amphetamines[ti]) AND (tolerance[tiab] OR tachyphylaxis[tiab] OR "acute tolerance"[tiab] OR sensitization[ti] OR "cross-tolerance"[tiab] OR "repeated administration"[ti] OR "repeated doses"[ti]) AND humans[MeSH Terms]` | 88 | 8834422→144; 11557168→145; 10780242→148; 8896773→149; 9836021→150; 2057510→151; 7220674→152; 32559027→155; 14085622 (→ LSD). Not kept: rodent sensitization studies indexed as human, forensic blood-concentration papers. |
| AM2 | `(stimulant*[ti] OR amphetamine*[ti] OR lisdexamfetamine[ti] OR methylphenidate[ti] OR psychostimulant*[ti]) AND (tolerance[ti] OR tachyphylaxis[ti] OR "acute tolerance"[tiab] OR "loss of efficacy"[tiab] OR "maintenance of efficacy"[tiab] OR "randomized withdrawal"[tiab]) AND (ADHD[tiab] OR "attention deficit"[tiab] OR narcolepsy[tiab])` (shared with Methylphenidate) | 26 (25 new) | 35892400→146; 24839883→153; 22780921→154; 29580130→157; methylphenidate items → Methylphenidate section. |
| AM3 | `(amphetamine[tiab]) AND (sensitization[ti] OR "repeated"[ti]) AND (raclopride[tiab] OR "dopamine release"[tiab]) AND ("Positron-Emission Tomography"[MeSH Terms] OR PET[tiab] OR SPECT[tiab]) AND humans[MeSH Terms]` | 2 | 17146013→147; 26905412→156. |

Year note: #152 is 1980 in PubMed and 1981 (print) in Crossref; the Crossref print year is used (METHODS §4.2). #157: species confirmed as rats from the abstract.

## 8. Methamphetamine

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| MA1 | `(methamphetamine[ti] OR methylamphetamine[ti] OR metamfetamine[ti]) AND (tolerance[tiab] OR "acute tolerance"[tiab] OR tachyphylaxis[tiab] OR "cross-tolerance"[tiab] OR sensitization[ti] OR "repeated"[ti] OR "binge"[ti]) AND humans[MeSH Terms]` | 69 (66 new) | 11441429→158; 1913701→159; 1362938→160; 15542728→164; 21748253→165; 28589263→166. Not kept: rodent sensitization studies indexed as human, HIV/sexual-behaviour "binge" papers. |
| MA2 | `(methamphetamine[tiab]) AND (abstinence[tiab] OR abstinent[tiab] OR detoxification[tiab] OR detoxified[tiab]) AND ("dopamine transporter*"[tiab] OR "D2"[tiab] OR "glucose metabolism"[tiab] OR "serotonin transporter"[tiab] OR "D3"[tiab]) AND ("Positron-Emission Tomography"[MeSH Terms] OR "Tomography, Emission-Computed, Single-Photon"[MeSH Terms]) AND (recovery[tiab] OR protracted[tiab] OR longitudinal[tiab] OR months[tiab] OR "follow-up"[tiab])` | 7 (6 new) | None kept (cross-sectional; the recovery studies were not retrieved by this string). |
| MA3 | Known-item check: `methamphetamine[ti] AND (Volkow ND[au] OR Wang GJ[au]) AND (abstinence[ti] OR recovers[ti] OR recovery[ti] OR detoxification[ti])` | 3 (2 new) | 11717374→161; 14754772→162; 26208874→163 (also in K2). |

DOI via Crossref search: Cook et al. 1992 (10.1016/s0090-9556(25)08806-3). Abstracts read for #158, #159 and #161 (the design note for #161 was taken from its abstract).

## 9. Methylphenidate

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| MP1 | `(methylphenidate[ti] OR dexmethylphenidate[ti]) AND (tolerance[tiab] OR "acute tolerance"[tiab] OR tachyphylaxis[tiab] OR sensitization[tiab] OR "cross-tolerance"[tiab]) AND humans[MeSH Terms] NOT (tolerability[ti])` | 43 (36 new) | 2585214→171. Not kept: tolerability reports, case reports, rodent sensitization; Winsberg 1987 (Psychopharmacol Bull, no DOI). |
| MP2 | `(methylphenidate[tiab] OR psychostimulant*[tiab] OR stimulant*[tiab]) AND ("dopamine transporter"[tiab] OR "dopamine transporters"[tiab]) AND (ADHD[tiab] OR "attention deficit"[tiab]) AND ("long-term"[tiab] OR chronic[tiab] OR "12 months"[tiab] OR "1 year"[tiab] OR "Meta-Analysis"[pt]) AND ("Positron-Emission Tomography"[MeSH Terms] OR "Tomography, Emission-Computed, Single-Photon"[MeSH Terms] OR "Meta-Analysis"[pt])` | 11 | 23696790→168; 22294258→169; 16139732→170; 22805600→174; 22805599→175. |
| — | From AM2 (Amphetamine) | — | 10511066→167; 12578439→172; 14624806→173. |

Crossref `updated-by` on #175 lists an erratum (10.1038/npp.2013.15). Abstracts read for #168 and #172 to confirm the notes; #170 has no abstract in PubMed.

## 10. Synthetic cathinones

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| SC1 | `(cathinone*[tiab] OR mephedrone[tiab] OR "4-MMC"[tiab] OR "3-MMC"[tiab] OR MDPV[tiab] OR methylenedioxypyrovalerone[tiab] OR "alpha-PVP"[tiab] OR "α-PVP"[tiab] OR methylone[tiab] OR eutylone[tiab] OR "bath salts"[tiab]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab] OR redosing[tiab] OR "re-dosing"[tiab] OR binge[tiab] OR "repeated doses"[tiab] OR "repeated administration"[tiab] OR "two doses"[tiab] OR "consecutive doses"[tiab])` (no humans filter, to see the animal literature) | 114 | 21592252→176; 32087112→177; 22257011→178; 27681583→180; 28753045→181; 22342322→182; 3749220→183; 7086694→184; 1971444→185; 31934604→186. Not kept: rodent binge/sensitization neurotoxicity studies, khat papers (Tier 2 page), analytical chemistry. |
| SC2 | `(mephedrone[tiab] OR cathinone*[tiab] OR "bath salts"[tiab] OR MDPV[tiab] OR "alpha-PVP"[tiab] OR "3-MMC"[tiab]) AND (dependence[tiab] OR craving[tiab] OR compulsive[tiab] OR withdrawal[tiab] OR tolerance[tiab]) AND (survey[tiab] OR users[tiab] OR "people who use"[tiab] OR interview*[tiab]) AND humans[MeSH Terms]` | 31 (22 new) | 27371497→179. Not kept: single-dose human pharmacology (Papaseit 2016; Olesti 2019), chemsex qualitative studies without tolerance data. |

DOI via Crossref search: Foltin & Schuster 1982 (10.1016/s0022-3565(25)33163-0). Species for #183 and #186 confirmed from abstracts.

## 11. MDMA

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| MD1 | `(MDMA[tiab] OR ecstasy[tiab] OR "3,4-methylenedioxymethamphetamine"[tiab]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab] OR "repeated doses"[tiab] OR "repeated administration"[tiab] OR "second dose"[tiab] OR "two doses"[tiab] OR redosing[tiab] OR booster[tiab] OR "supplemental dose"[tiab]) AND humans[MeSH Terms]` | 74 (58 new) | 15671132→187; 15071716→188; 23142957→189; 26073279→192; 42243076→193; 19836170→200. Not kept: immune-function repeated-dose papers (Pacifici 2001/2002), forensic and analytical papers, efavirenz "tolerance", rodent studies; Raznahan 2013 (no DOI; see Known gaps). |
| MD2 | `(MDMA[tiab] OR ecstasy[tiab]) AND ("serotonin transporter"[tiab] OR SERT[tiab] OR "5-HT2A"[tiab] OR DASB[tiab] OR McN5652[tiab] OR "beta-CIT"[tiab] OR "5-HT transporter"[tiab]) AND (abstinence[tiab] OR abstinent[tiab] OR "ex-users"[tiab] OR former[tiab] OR recovery[tiab] OR abstention[tiab] OR reversib*[tiab]) AND ("Positron-Emission Tomography"[MeSH Terms] OR "Tomography, Emission-Computed, Single-Photon"[MeSH Terms])` | 19 (18 new) | 27568200→191; 11741626→190; 16133393→194; 19336788→195; 21646575→196; 22353758→197; 11850153→198; 16510479→199. Not kept: rat model studies, cortisol and cognition correlates. |

Raznahan et al. 2013 (Psychiatr Danub; PMID 23793283): no DOI in PubMed; a Crossref search returned no matching record. Abstracts read for #188 and #190 to confirm the notes.

## 12. LSD

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| L0 (first form, discarded) | `(LSD OR lysergide) AND (tolerance OR cross-tolerance) AND humans[MeSH Terms]` | 142 | Untagged "LSD" matched lysosomal storage diseases (Gaucher, Pompe, Niemann-Pick) and "tolerance" matched tolerability; replaced by L1. |
| L1 | `("lysergic acid diethylamide"[MeSH Terms] OR "lysergic acid diethylamide"[tiab] OR lysergide[tiab]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab] OR "Drug Tolerance"[MeSH Terms])` (no humans filter: the classic human studies predate MeSH indexing) | 141 | 13371962→201; 13717955→202; 13486057→203; 13497364→206; 14405871→207; 13796179→208; 14159265→209; 13295823→210; 828469→211; 35900876→214; 25513973→215; 15756304→216; 14007904, 13796178 (→ Mescaline); 14138757 (→ DMT); 14085622, 5350620 (→ Cross-cutting). Not kept: more than 60 animal studies (cats, rats, dogs, monkeys) of the 1960s–1980s, receptor-binding studies without a DOI (Buckholtz 1990), off-topic pharmacology. |
| L2 | `("lysergic acid diethylamide"[tiab] OR LSD[ti] OR lysergide[tiab]) AND (microdos*[tiab] OR "repeated low dose*"[tiab] OR "repeated dos*"[tiab] OR "repeated administration"[tiab]) AND humans[MeSH Terms]` | 60 (58 new) | 35106880→204; 31853557→205; 40105807→212; 31303095→213. Not kept: microdosing surveys and trials that report mood or cognition but not change in response over repeated doses; protocols. |
| L3 | `(psychedelic*[ti] OR hallucinogen*[ti] OR serotonergic[ti]) AND (tolerance[ti] OR "cross-tolerance"[ti] OR tachyphylaxis[ti])` | 19 (18 new) | 4844244, 25271256, 34032876 (→ 2C-x). No human review of psychedelic tolerance was found. |

DOIs via Crossref search (volume, issue and first page matched to PubMed): Isbell et al. 1956 (10.1001/archneurpsyc.1956.02330290012002) and Abramson et al. 1958 (10.1001/archneurpsyc.1958.02340020081015); Crossref splits their titles into title and subtitle.

## 13. Psilocybin

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| P1 | `(psilocybin[tiab] OR psilocin[tiab] OR Psilocybe[tiab]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab]) NOT (tolerability[ti])` | 23 (13 new) | None new (13717955 already listed as #202). Not kept: a trial protocol (Kothiwala 2026), rodent studies, reviews mentioning tolerance in passing. |
| P2 | `(psilocybin[tiab] OR psilocin[tiab]) AND ("5-HT2A"[tiab] OR "serotonin 2A"[tiab] OR "5-HT(2A)"[tiab]) AND ("Positron-Emission Tomography"[MeSH Terms] OR PET[tiab]) AND humans[MeSH Terms]` | 14 | 32146028→217; 30685771→218. |
| P3 | `(psilocybin[ti] OR "magic mushrooms"[ti] OR Psilocybe[ti]) AND (microdos*[tiab] OR "repeated dos*"[tiab] OR "two doses"[tiab] OR "second dose"[tiab] OR "consecutive"[tiab] OR "dose-escalation"[tiab] OR "repeated administration"[tiab]) AND humans[MeSH Terms] AND ("Clinical Trial"[pt] OR "Randomized Controlled Trial"[pt] OR placebo[tiab])` | 23 (22 new) | 41825921→219; 35918311→220. Not kept: therapeutic trials with one or two sessions (no repeated-dose response data), the two-dose migraine trial (doses a week apart; abstract read). |

Crossref `updated-by` on #218 lists a correction (10.1038/s41386-019-0360-5). Abstracts read for #217 and #219.

## 14. DMT and ayahuasca

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| D1 (discarded) | `("N,N-dimethyltryptamine"[tiab] OR DMT[tiab] OR ayahuasca[tiab] OR dimethyltryptamine[tiab] OR "Banisteriopsis caapi"[tiab]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab] OR "repeated doses"[tiab] OR "repeated administration"[tiab] OR "two doses"[tiab] OR "continuous infusion"[tiab] OR "extended"[ti] OR "long-term"[ti] OR "regular use"[tiab])` | 238 | "DMT" also abbreviates disease-modifying therapy (multiple sclerosis), discrete multitone (optics) and 2′,6′-dimethyltyrosine (opioid peptides); replaced by D2. Kept from it: 21842159→222; 37897244→227; 39702577→228. |
| D2 | `("N,N-dimethyltryptamine"[tiab] OR dimethyltryptamine[ti] OR ayahuasca[ti] OR hoasca[ti] OR (DMT[ti] AND (psychedelic*[tiab] OR hallucinogen*[tiab] OR tryptamine*[tiab]))) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab] OR "closely spaced"[tiab] OR repeated[tiab] OR "regular use"[tiab] OR "long-term use"[tiab] OR "platelet"[tiab]) NOT ("multiple sclerosis"[tiab])` | 102 (79 new) | 8731519→221; 7892432→224; 8596116→225; 8788488→226; 3979433 (→ 5-MeO-DMT); 40659913, 29708042 (→ 5-MeO-DMT). Not kept: rodent ayahuasca studies, mental-health outcome surveys of ritual users. |
| — | From L1 (LSD) | — | 14138757→223; 1064726→229. |

DOI via Crossref search (volume, issue and pages matched to PubMed): Kovacic & Domino 1976 (10.1016/s0022-3565(25)30534-3). Not found in Crossref: Gillin et al. 1973 (PMID 4519415).

## 15. 5-MeO-DMT

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| M5 | `("5-MeO-DMT"[tiab] OR "5-methoxy-N,N-dimethyltryptamine"[tiab] OR GH001[tiab] OR "Bufo alvarius"[tiab] OR "Incilius alvarius"[tiab] OR mebufotenin[tiab]) AND (tolerance[tiab] OR repeated[tiab] OR "individualized dosing"[tiab] OR "individualised dosing"[tiab] OR "multiple doses"[tiab] OR "three doses"[tiab] OR "cross-tolerance"[tiab] OR "dose-escalation"[tiab])` | 58 (9 new; most were rodent 5-MeO-DMT studies already screened in D2) | 37409159→230; 35149998→231. |
| — | From D2 (DMT) | — | 40659913→232; 29708042→233; 3979433→234. |

Abstract read for #230 (dosing design note).

## 16. Mescaline

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| ME1 | `(mescaline[tiab] OR peyote[tiab] OR "San Pedro"[tiab] OR Lophophora[tiab] OR Trichocereus[tiab] OR Echinopsis[tiab]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab] OR "repeated"[tiab] OR "long-term"[tiab] OR "regular use"[tiab])` | 88 (65 new) | 16271313→237; 5998418→238; 5067530→239. "San Pedro" matched place names (ecology, air quality); not kept: rabbit and mouse studies, reviews. |
| — | From L1 (LSD) | — | 14007904→235; 13796178→236. |

## 17. 2C-x

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| X1 | `("2C-B"[tiab] OR "4-bromo-2,5-dimethoxyphenethylamine"[tiab] OR "2C-I"[tiab] OR "2C-E"[tiab] OR "2C-T-7"[tiab] OR NBOMe[tiab] OR "25I-NBOMe"[tiab] OR "25B-NBOMe"[tiab] OR "25C-NBOMe"[tiab] OR "25CN-NBOH"[tiab] OR "2,5-dimethoxy-4-methylamphetamine"[tiab] OR "2,5-dimethoxy-4-iodoamphetamine"[tiab] OR DOI[ti] OR DOM[ti]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab] OR "repeated administration"[tiab] OR "repeated doses"[tiab])` | 46 (37 new) | 29467649→242; 10435391→244. "DOI"/"DOM" in titles matched errata, author names and unrelated words; not kept: other DOI-receptor pharmacology in rodents. |
| — | From L3 (LSD) | — | 4844244→240; 25271256→241; 34032876→243. |

Abstracts read: #241 (species and compounds), #243 (species); #240 has no abstract.

## 18. Ketamine

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| KE1 | `(ketamine[ti] OR esketamine[ti] OR arketamine[ti]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab]) AND humans[MeSH Terms] NOT (opioid*[ti] OR morphine[ti] OR remifentanil[ti] OR hyperalgesia[ti] OR fentanyl[ti] OR "pain tolerance"[tiab] OR postoperative[ti])` (the NOT clause removes ketamine used against opioid tolerance) | 96 (95 new) | 36244360→248; 11476262→254; 7469110→255; 26317449→256. Not kept: "tolerance" meaning tolerability in sedation and pain trials, single pediatric case letters (Khan 1988, MacLennan 1982, Stevens 1981), a tachyphylaxis case letter (Cavalcanti 2024). |
| KE2 | `ketamine[tiab] AND (frequent[tiab] OR chronic[tiab] OR regular[tiab] OR recreational[tiab] OR "long-term"[tiab]) AND (users[tiab] OR "people who use"[tiab] OR abusers[tiab]) AND (tolerance[tiab] OR dependence[tiab] OR "dose escalation"[tiab] OR binge*[tiab]) AND humans[MeSH Terms]` | 38 (36 new) | 31470241→257; 34176409→258. Not kept: biomarker and imaging studies of people dependent on ketamine without tolerance data, perioperative studies. |
| KE3 | `(ketamine[ti] OR esketamine[ti]) AND (repeated[ti] OR serial[ti] OR maintenance[ti] OR "long-term"[ti] OR "six infusions"[tiab] OR "repeated infusions"[tiab]) AND depress*[tiab] AND (tolerance[tiab] OR tachyphylaxis[tiab] OR "loss of response"[tiab] OR "diminish*"[tiab] OR "attenuat*"[tiab])` | 17 (13 new) | None (rodent studies, effectiveness reports without tolerance data). |
| KE4 | Known-item check: `ketamine[ti] AND ((Morgan CJ[au] AND (longitudinal[ti] OR review[ti] OR frequent[ti] OR "3-year"[ti] OR "1-year"[ti])) OR (Krystal JH[au] AND (ethanol[tiab] OR alcohol[tiab]) AND (recovering[tiab] OR dependent[tiab])) OR (Narendran R[au] AND recreational[ti]))` | 11 (10 new) | 21777321→245; 19919593→246; 16330601→249; 15500598→250; 19133891→251. |
| KE5 | Known-item check: `Krystal JH[au] AND (recovering[ti] OR "ethanol-like"[tiab] OR "ethanol-dependent"[ti] OR alcoholics[ti]) AND (NMDA[ti] OR ketamine[tiab] OR "glutamate receptor antagonist"[ti])` | 4 (3 new) | 12888778→247; 9554431→252; 19028835→253. |

Crossref `updated-by` on #246 lists an erratum (10.1111/j.1360-0443.2010.02984.x). Crossref's title for #254 has OCR errors ("Ketamlne"); same paper. Abstract read for #249.

## 19. Phencyclidine

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| PC1 | `(phencyclidine[tiab] OR "3-MeO-PCP"[tiab] OR "angel dust"[tiab]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab] OR "chronic use"[tiab] OR "chronic users"[tiab] OR "long-term use"[tiab]) NOT (pneumocystis[tiab] OR "Pneumocystis"[MeSH Terms])` (no humans filter) | 135 (125 new) | 7304511→259; 6514253→260; 7241405→261; 2198784→262; 7117133→263; 113826→264; 6864526→265; 6294678→266. Not kept: PCP as an animal model of schizophrenia, NMDA antagonists and opioid tolerance, JPET and NIDA monograph items without DOI (Spain 1985, Flint 1980, Balster 1980). |

DOI via Crossref search (volume, issue and pages matched to PubMed): Wenger 1983 (10.1016/s0022-3565(25)33642-6). Abstracts read for #259 and #263.

## 20. Dextromethorphan

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| DX1 | `(dextromethorphan[ti] OR DXM[ti]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR dependence[tiab] OR "chronic use"[tiab] OR "long-term use"[tiab] OR abuse[ti] OR misuse[ti] OR recreational[ti]) NOT (morphine[ti] OR opioid*[ti] OR "opioid tolerance"[tiab])` | 92 (91 new) | 30903576→267; 27288091→268; 20737060→269; 16318953→270; 3092943→271; 19289333→272. Not kept: poison-centre trend reports, single toxicity cases without tolerance data, dextromethorphan–bupropion pharmacovigilance, "tolerance" meaning tolerability in clinical trials. |

## 21. Nitrous oxide

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| NO1 (discarded) | `("nitrous oxide"[ti] OR N2O[ti]) AND (tolerance[tiab] OR "acute tolerance"[tiab] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab] OR "chronic use"[tiab] OR "recreational"[tiab]) NOT (emission*[ti] OR soil[ti] OR wastewater[ti] OR nitrification[tiab])` | 379 (first 200 screened) | The "recreational" term returned mainly B12/myeloneuropathy case reports; replaced by NO2. Kept from it: 37904333→279. |
| NO2 | `("nitrous oxide"[tiab] OR N2O[ti]) AND ("acute tolerance"[tiab] OR tolerance[ti] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab] OR "chronic tolerance"[tiab] OR (Ramsay DS[au])) NOT (emission*[ti] OR soil[ti] OR wastewater[ti] OR nitrification[tiab] OR denitrif*[tiab] OR plant*[ti])` | 82 (79 new) | 15733627→273; 1491863→274; 8743615→275; 8761985→276; 4061009→277; 2316879→278; 15778887→280; 17216156→281; 22247586→282; 484891→283. Not kept: "patient tolerance" of procedures under nitrous oxide sedation, suxamethonium tachyphylaxis, rodent mechanism studies. |

## 22. Cannabis

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| CA1 | `(cannabis[ti] OR marijuana[ti] OR marihuana[ti] OR THC[ti] OR tetrahydrocannabinol[ti] OR dronabinol[ti] OR nabilone[ti] OR cannabinoid*[ti]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab]) AND humans[MeSH Terms] NOT ("distress tolerance"[tiab] OR "pain tolerance"[ti] OR synthetic[ti] OR "tolerance to frustration"[tiab])` | 383 (most recent 200 retrieved; 196 new) | 30056176→284; 32014378→285; 27225696→289; 25745105→292; 28407543→295; 24373053→300; 31865628→301; 37329730→302; 36595624→303; 35692186→304; 25270679→305; 37348821→306; 30861005→307. Older records were reached through CA4 instead of a second page. Not kept: pain, sleep and medical-cannabis trials, CB2 and allosteric-modulator pharmacology, driving-policy papers. |
| CA2 | `(cannabis[tiab] OR marijuana[tiab]) AND (CB1[tiab] OR "cannabinoid receptor*"[tiab] OR "CB(1)"[tiab]) AND ("Positron-Emission Tomography"[MeSH Terms] OR PET[tiab]) AND (abstinence[tiab] OR downregulation[tiab] OR "down-regulation"[tiab] OR reversible[tiab] OR availability[tiab]) AND humans[MeSH Terms]` | 10 (7 new) | 21747398→287. |
| CA3 (discarded) | `(cannabis[ti] OR marijuana[ti] OR marihuana[ti] OR THC[ti] OR tetrahydrocannabinol[ti] OR cannabinoid*[ti]) AND (tolerance[ti] OR "cross-tolerance"[ti] OR blunted[ti] OR "CB1"[ti] OR "CB(1)"[ti]) AND humans[MeSH Terms] AND 1960:2016[dp]` | 450 | "CB1"[ti] returned receptor pharmacology; nothing kept. |
| CA4 | Known-item check: `(D'Souza DC[au] AND (blunted[ti] OR rapid[ti]) AND (cannabis[tiab] OR tetrahydrocannabinol[tiab])) OR (Ramaekers JG[au] AND (heavy[ti] OR occasional[ti] OR tolerance[ti]) AND (THC[tiab] OR cannabis[tiab])) OR (Babor TF[au] AND marihuana[ti]) OR (Jones RT[au] AND (cannabis[ti] OR marihuana[ti]) AND (tolerance[ti] OR dependence[ti]))` | 22 (16 new) | 18185500→286; 27585721→290; 18719045→291; 21975580→293; 22553980→294; 798533→297; 6271820→298; 29560896→299. |
| — | From A2 (Alcohol) and N1 (Nicotine) | — | 21049267→288; 23074216→296. |

Crossref `updated-by` on #289 lists its erratum (#290, 10.1038/srep31939). Abstracts read for #287 and #299 (time-course notes).

## 23. Synthetic cannabinoids

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| SY1 | `("synthetic cannabinoid*"[tiab] OR spice[ti] OR K2[ti] OR "JWH-018"[tiab] OR "AB-FUBINACA"[tiab] OR "MDMB-4en-PINACA"[tiab] OR AKB48[tiab] OR "5F-ADB"[tiab] OR "synthetic cannabinoid receptor agonist*"[tiab] OR SCRA[tiab] OR SCRAs[tiab]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR dependence[tiab] OR withdrawal[tiab] OR "repeated"[tiab])` (no humans filter) | 348 (most recent 150 retrieved; 143 new) | 38915848→308; 34533608→312; 40570820→313; 34311790→314; 35640052→315; 33115642→316; 30833484→317; 32688070→318. "spice" and "K2" matched cooking spices, vitamin K2, bacterial serotypes and the SPICE circuit simulator; not kept: rodent toxicity studies, analytical and wastewater papers. |
| SY2 | `("JWH-018"[ti] OR "synthetic cannabinoid"[ti] OR "synthetic cannabinoids"[ti]) AND (volunteers[tiab] OR participants[tiab] OR "placebo-controlled"[tiab] OR survey[tiab] OR "frequent cannabis users"[tiab]) AND (tolerance[tiab] OR "repeated"[tiab] OR dependence[tiab] OR "cannabis users"[tiab]) AND humans[MeSH Terms]` | 14 (9 new) | 33497715→311; 27074934→309; 21835562→310. |

Abstracts read for #311 and #316.

## 24. Heroin

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| H1 | `(heroin[ti] OR diamorphine[ti] OR diacetylmorphine[ti] OR opiate*[ti]) AND (tolerance[tiab] OR "cross-tolerance"[tiab]) AND (overdose[tiab] OR death*[tiab] OR fatal*[tiab] OR "loss of tolerance"[tiab] OR "reduced tolerance"[tiab] OR users[tiab] OR "people who"[tiab]) AND humans[MeSH Terms] NOT ("pain tolerance"[tiab] OR "cold pressor"[tiab])` | 51 (48 new) | 12727768→319; 9654260→320; 16564148→321; 39930592→322; 11487418→323; 12791795→324; 21353406→327; 11964108→328; 38126706→329; 35737700→330; 16105259→331; 14969742→332; 7200260→335. Not kept: opioid-transition and market papers, gene-association studies, a Swedish case series without DOI (Rajs 2000). 28493329 is on the Interactions list already. |
| H5 | `(hair[tiab]) AND (heroin[tiab] OR morphine[tiab] OR opiate*[tiab] OR methadone[tiab]) AND (overdose[tiab] OR fatal[tiab] OR deaths[tiab]) AND (tolerance[tiab] OR "abstinence"[tiab] OR "recent use"[tiab] OR "use history"[tiab])` | 8 (3 new) | None new (methadone-death hair study, 25622032, considered under Methadone). |
| H6 | `(Siegel S[au] AND (overdose[tiab] OR "drug-associated"[tiab] OR tolerance[ti])) OR ("conditioned tolerance"[tiab] AND (heroin[tiab] OR opioid*[tiab] OR morphine[tiab]) AND humans[MeSH Terms])` | 42 (39 new) | 1384078→325; 12233979→326. Not kept: rat conditioning studies other than #335. |
| — | From MB3 and MB5 (Methadone and buprenorphine), added after the first write-up of the section | — | 9279497→334 (MB3); 17602127→333 (MB5). |

The cross-cutting searches (release from prison, after treatment, naltrexone) are logged under Cross-cutting.


## 25. Fentanyl and analogues

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| F1 | `(fentanyl[ti] OR carfentanil[ti] OR nitazene*[tiab] OR sufentanil[ti] OR remifentanil[ti] OR alfentanil[ti]) AND (tolerance[ti] OR "acute tolerance"[tiab] OR "cross-tolerance"[tiab] OR tachyphylaxis[tiab] OR "opioid tolerance"[ti]) AND humans[MeSH Terms] NOT (hyperalgesia[ti] OR ketamine[ti] OR "patient tolerance"[tiab])` | 62 | 9620525→339; 11973194→341; 10490157→343; 12518→353; 23792280→354; 30379379→351 (added after the first write-up of the section). Not kept: perioperative dosing trials and opioid-induced hyperalgesia studies. |
| F2 | `fentanyl[tiab] AND (tolerance[tiab] OR "opioid-naive"[tiab] OR "opioid naive"[tiab] OR "non-tolerant"[tiab] OR "nontolerant"[tiab]) AND (overdose[tiab] OR "people who use"[tiab] OR unregulated[tiab] OR illicit[tiab] OR "street"[tiab]) AND humans[MeSH Terms]` | 66 | 41642634→337; 38383903→338; 2066723→345 (DOI 10.1520/jfs13045j found by Crossref bibliographic search); 30778596→347; 42302710→349; 39182110→350. Not kept: a trial protocol without results (40731024), a single case report (33973925), drug-checking and market papers. |
| F3 | `(fentanyl[tiab] OR remifentanil[tiab]) AND ("respiratory depression"[tiab] OR ventilation[tiab]) AND (tolerance[tiab] OR "opioid-tolerant"[tiab] OR "chronic opioid"[tiab] OR "opioid-naive"[tiab] OR "opioid-naïve"[tiab] OR "high-dose opioid users"[tiab]) AND humans[MeSH Terms]` | 114 (91 new) | 32865832→336; 19135798→340; 12598253→342; 16037150→344; 19918162→346. Held for Methadone and buprenorphine: 35316224, 35085249, 34601272. Not kept: intensive-care sedation, sleep apnoea and new-ligand studies. |
| F4 | `fentanyl[ti] AND (transdermal[tiab] OR patch*[tiab]) AND ("opioid-naive"[tiab] OR "opioid naive"[tiab] OR "opioid-naïve"[tiab] OR "non-opioid-tolerant"[tiab] OR "opioid-tolerant"[tiab]) AND (death*[tiab] OR safety[tiab] OR "respiratory depression"[tiab] OR overdose[tiab])` | 22 (16 new) | 25477566→348. Not kept: patch efficacy trials in cancer pain and a single fatal case report. |

Abstracts read for #336–340, #342, #344, #346, #348, #349 and #354.

## 26. Prescription opioids

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| PO1 | `(oxycodone[ti] OR morphine[ti] OR hydrocodone[ti] OR tramadol[ti] OR codeine[ti] OR hydromorphone[ti] OR oxymorphone[ti] OR tapentadol[ti] OR "opioid therapy"[ti] OR "long-term opioid"[ti] OR "chronic opioid"[ti] OR "opioid analgesic"[ti] OR "opioid analgesics"[ti]) AND (tolerance[ti] OR "cross-tolerance"[tiab] OR "opioid tolerance"[tiab]) AND humans[MeSH Terms] NOT ("patient tolerance"[tiab] OR "glucose tolerance"[tiab] OR hyperalgesia[ti])` | 433 (most recent 250 retrieved; 227 new) | 2594396→367; 3926042→366; 8121693→365; 8768738→368 (DOI 10.1016/s0022-3565(25)20670-x found by Crossref bibliographic search); 20609129→363; 32293684→372 (also in F2). Held for Methadone and buprenorphine: 34216862, 12745417. Most hits were animal mechanism studies indexed with humans; "tolerance" also matched exercise, cold-pressor and drug tolerability; no-DOI reviews (e.g. 8564998) not kept. |
| PO1b | Known-item and trial check: `(Chu LF[au] AND tolerance[ti]) OR (Martin WR[au] AND Jasinski DR[au] AND (tolerance[tiab] OR abstinence[ti])) OR (("chronic pain"[tiab] OR "cancer pain"[tiab] OR "low back pain"[tiab]) AND (morphine[ti] OR oxycodone[ti] OR opioid*[ti]) AND ("analgesic tolerance"[tiab] OR "opioid tolerance"[ti] OR "dose escalation"[ti]) AND (randomized[tiab] OR prospective[tiab] OR cohort[tiab] OR "systematic review"[tiab]))` (needed because PO1 excluded titles with "hyperalgesia") | 29 (27 new) | 22704854→355; 5352850→356; 32006699→360; 16414554→361; 17977662→362; 25529548→364; 24847273→352 (Fentanyl). Not kept: dose-escalation cohorts without a tolerance measure, a methylation study, a duplicate 1970 digest reprint without DOI (5454815). |
| PO2 | `("opioid rotation"[tiab] OR "opioid switching"[tiab] OR "opioid switch"[tiab] OR "opioid conversion"[tiab] OR equianalgesic[tiab]) AND ("cross-tolerance"[tiab] OR "incomplete cross-tolerance"[tiab] OR "cross tolerance"[tiab])` | 21 (17 new) | 30853505→380. Not kept: equianalgesic tables, single cases, new-ligand pharmacology. |
| PO3 | `(opioid*[tiab]) AND (taper*[ti] OR discontinu*[ti] OR stopping[ti] OR "dose variability"[ti] OR cessation[ti]) AND (overdose[tiab]) AND ("long-term opioid"[tiab] OR "chronic opioid"[tiab] OR "prescribed opioid"[tiab] OR "prescribed opioids"[tiab] OR "opioid prescription"[tiab] OR "opioid prescriptions"[tiab] OR "opioid therapy"[tiab]) AND (cohort[tiab] OR "systematic review"[tiab] OR "case-control"[tiab] OR registry[tiab])` | 20 | 34342618→359; 36454732→374 (its correction, 36944161, noted in the row); 35960518→375; 35696163→376; 31468341→377; 31002325→378; 33145689→379. Held for Methadone and buprenorphine: 31786933. Not kept: newer cohorts in older adults and policy studies (2025–2026) that repeat the design of those kept. |
| PO4 | `(opioid*[ti] OR oxycodone[ti] OR methadone[ti] OR "long-acting"[ti] OR "extended-release"[ti]) AND (overdose[ti] OR poisoning[ti] OR "respiratory depression"[ti] OR mortality[ti] OR death*[ti]) AND ("opioid-naive"[tiab] OR "opioid naive"[tiab] OR "opioid-naïve"[tiab] OR "opioid tolerance"[tiab] OR "opioid-tolerant"[tiab] OR "first 2 weeks"[tiab] OR "initiation"[ti] OR "duration of action"[ti]) AND humans[MeSH Terms]` | 71 (64 new) | 25686208→371; 18333735→373; 29888409→357 (also in F2). Held for Methadone and buprenorphine: 12144602, 21696913, 26234389, 29179255, 31419306, 20081524. Held for Cross-cutting: 30024795, 39034384, 31082666, 33258068, 29807248. Not kept: post-surgical prescribing cohorts without a tolerance measure, letters on 25686208, a retracted anaesthesia cohort (37474420). |
| PO5 | Known-item check: `(Oliva EM[au] AND stopping[ti]) OR (Webster LR[au] AND rotation[ti]) OR (Fine PG[au] AND rotation[ti]) OR (Quigley C[au] AND switching[ti])` | 9 | 32131996→358; 19735903→369; 22458884→370. Not kept: the Cochrane review on opioid switching (15266542), withdrawn in 2013 (24142865); an expert-panel paper centred on conversion practice (19735902). |

Abstracts read for #351–352, #357, #360, #362–363, #371, #373–375 and #378.

## 27. Methadone and buprenorphine

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| MB1 | `(methadone[ti] OR buprenorphine[ti] OR "opioid agonist treatment"[ti] OR "opioid substitution"[ti] OR "opioid maintenance"[ti] OR "methadone-maintained"[ti]) AND (tolerance[tiab] OR "cross-tolerance"[tiab]) AND (analgesi*[tiab] OR respiratory[tiab] OR "receptor occupancy"[tiab] OR "receptor availability"[tiab] OR PET[tiab] OR "opioid-naive"[tiab] OR "opioid naive"[tiab]) AND humans[MeSH Terms] NOT ("glucose tolerance"[tiab] OR "patient tolerance"[tiab])` | 105 (84 new) | 16427197→386; 29514333→388; 30418214→389; 9085402→395; 16547090→399; 22565115→417; 35500444→418 (also MB4); 25622032→416 (also H5, MB4). From earlier searches: 34601272→381 (F3); 34216862→390 and 12745417→391 (PO1); 35085249→400 (F3). Not kept: methadone and buprenorphine as analgesics in cancer and chronic pain, perioperative case reports, a second modelling paper on the data of #400 (35316224). |
| MB2 | `(methadone[tiab] OR buprenorphine[tiab] OR "opioid agonist"[tiab] OR "opioid substitution"[tiab]) AND (mortality[ti] OR death*[ti] OR overdose[ti] OR poisoning[ti]) AND (induction[tiab] OR "first 2 weeks"[tiab] OR "first two weeks"[tiab] OR "first 4 weeks"[tiab] OR "first four weeks"[tiab] OR "leaving treatment"[tiab] OR "after treatment"[tiab] OR "off treatment"[tiab] OR "out of treatment"[tiab] OR cessation[tiab] OR discontinu*[tiab]) AND ("systematic review"[tiab] OR "meta-analysis"[tiab] OR cohort[tiab])` | 56 (49 new) | 28446428→383; 34076676→384; 12144602→405 (also PO4); 26384619→407; 20978062→408; 26452239→409; 21696913→410 (also PO4); 32034837→412; 31786933→413 (also PO3); 36173629→414. From PO4: 29179255→411. Held for Cross-cutting: 18031430, 32969097, 28160345, 36305669, 24694626, 21438941, 17931824. Not kept: cohorts on retention, comorbidity, take-home doses and benzodiazepine co-prescription; a second primary care cohort (29672985) and a non-fatal overdose cohort (36034051) that repeat the design of #408–410. |
| MB3 | Known-item check: `(Doverty M[au] AND methadone[tiab]) OR (Greenwald MK[au] AND ("receptor availability"[tiab] OR "receptor occupancy"[tiab])) OR (Caplehorn JR[au] AND (deaths[ti] OR mortality[ti])) OR (Zador D[au] AND deaths[ti]) OR (Kreek MJ[au] AND tolerance[ti] AND methadone[tiab])` | 21 | 11427327→387; 12902992→382; 10942856→396; 25179217→398; 16203464→401; 10065120→402; 12188991→403; 10723832→385; 9279497→334 (Heroin). Not kept: commentaries and editorials, a study of hyperalgesia rather than tolerance (11166974), earlier heroin-death series (8604187, 10940541, 9251698). |
| MB4 | `methadone[ti] AND (death*[ti] OR fatal*[ti] OR poisoning[ti] OR toxicity[ti] OR mortality[ti]) AND (tolerance[tiab] OR "opioid-naive"[tiab] OR "opioid naive"[tiab] OR "opioid-naïve"[tiab] OR "non-tolerant"[tiab] OR "nontolerant"[tiab] OR induction[tiab] OR "first two weeks"[tiab] OR "first 2 weeks"[tiab])` | 31 (16 new) | 1288269→404; 19563562→406; 23891033→415; 20087676→419. Not kept: regional death series without a tolerance measure, a pharmacogenetic study, a neonatal case. |
| MB5 | `("opioid dependence"[tiab] OR "opioid-dependent"[tiab] OR heroin[tiab] OR "opiate dependence"[tiab] OR "opiate-dependent"[tiab] OR methadone[tiab] OR "opioid use disorder"[tiab]) AND ("positron emission tomography"[tiab] OR PET[tiab]) AND ("mu-opioid receptor"[tiab] OR "μ-opioid receptor"[tiab] OR "opioid receptor binding"[tiab] OR "opioid receptor availability"[tiab] OR diprenorphine[tiab] OR carfentanil[tiab]) AND (abstinence[tiab] OR abstinent[tiab] OR detoxification[tiab] OR withdrawal[tiab])` | 6 (3 new) | 16950210→397; 17602127→333 (Heroin). Not kept: a review protocol. |

Abstracts read for #334, #381, #383–384, #400, #406, #410–411 and #415–418. PubMed lists three errata for #384 that Crossref `updated-by` does not show; they are given in the row.

## 28. Kratom

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| KR1 | `(kratom[tiab] OR mitragynine[tiab] OR "Mitragyna speciosa"[tiab] OR "7-hydroxymitragynine"[tiab] OR "7-OH-mitragynine"[tiab]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR "dose escalation"[tiab] OR "increasing doses"[tiab])` (no humans filter, so that animal work could be seen) | 54 (52 new) | 41486478→423; 38788532→421; 38441236→424; 35220331→425; 38217374→422; 16169018→428; 35341571→429. Not kept: case reports, social-media and narrative studies, a "pain tolerance" trial without DOI (32607084), a rodent study of mitragynine given with morphine (23292329), a retracted rat study (37058820). |
| KR2 | `(kratom[ti] OR mitragynine[ti] OR "Mitragyna speciosa"[ti] OR ketum[ti] OR krathom[ti]) AND (dependence[ti] OR withdrawal[ti] OR "regular users"[tiab] OR "regular kratom"[tiab] OR "long-term"[ti] OR "daily"[ti]) AND humans[MeSH Terms]` | 59 (50 new) | 42144893→420; 24698080→426; 40762659→427. Not kept: case reports of treatment with buprenorphine, biomarker studies in people who use kratom regularly, a withdrawal-scale validation. |

Abstracts read (searched for tolerance and repeated-dose findings) for #420–427 and #428–429. Crossref `updated-by` on #422 lists a correction.

## 29. Alkyl nitrites and inhalants

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| AN1 | `("amyl nitrite"[tiab] OR "isobutyl nitrite"[tiab] OR "butyl nitrite"[tiab] OR "alkyl nitrite"[tiab] OR "alkyl nitrites"[tiab] OR poppers[tiab] OR "isopropyl nitrite"[tiab]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR repeated[tiab] OR "chronic use"[tiab])` | 58 | 1904032→439; 34087382→438. Most hits were organic chemistry using tert-butyl nitrite as a reagent; also case reports of poisoning and maculopathy. |
| AN2 | `(toluene[ti] OR solvent[ti] OR solvents[ti] OR inhalant[ti] OR inhalants[ti] OR "volatile substance"[ti] OR "volatile solvent"[ti] OR butane[ti] OR trichloroethane[ti] OR "glue sniffing"[tiab]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR "acute tolerance"[tiab]) AND humans[MeSH Terms] NOT ("glucose tolerance"[tiab] OR "solvent-free"[tiab])` | 52 (50 new) | 3651728→430; 6542228→440. Discarded as a strategy: "inhalant" matched inhalant allergy and "solvent" matched solvent tolerance in bacteria and enzymes; replaced by AN2b. |
| AN2b | `(inhalant[ti] OR inhalants[ti] OR "solvent abuse"[tiab] OR "solvent misuse"[tiab] OR "volatile substance"[tiab] OR "glue sniffing"[tiab] OR toluene[ti]) AND (tolerance[tiab] OR "dependence syndrome"[tiab] OR "inhalant use disorder"[tiab] OR "inhalant dependence"[tiab]) AND humans[MeSH Terms] NOT (allerg*[tiab] OR immunotherapy[tiab] OR asthma[tiab])` | 54 (38 new) | 25134040→435; 20553671→436; 19267939→437. Not kept: case reports (including a single report of rising use of propane, 10695032), prevalence surveys without a tolerance measure, treatment case reports. |
| AN3 | `(sevoflurane[ti] OR isoflurane[ti] OR desflurane[ti] OR halothane[ti] OR enflurane[ti] OR "volatile anesthetic"[ti] OR "volatile anaesthetic"[ti] OR "volatile anesthetics"[ti] OR "inhaled anesthetic"[ti] OR "anesthetic requirement"[ti] OR MAC[ti]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR "acute tolerance"[tiab] OR alcoholic*[tiab] OR "chronic alcohol"[tiab] OR "repeated exposure"[tiab] OR "repeated administration"[tiab]) AND humans[MeSH Terms] NOT ("glucose tolerance"[tiab] OR "exercise tolerance"[tiab] OR "ischemic tolerance"[tiab] OR preconditioning[tiab])` | 104 (98 new) | 18077105→431 (also in A4 and AN5; first seen under Alcohol); 8387735→433; 402782→432. "MAC" also matched an alcoholism scale and a liver-fibrosis marker; not kept: hepatitis after repeated halothane, neonatal neurotoxicity in animals, anaesthetic technique trials. |
| AN4 | `("nitrate tolerance"[ti] OR "nitroglycerin tolerance"[ti] OR "nitrate cross-tolerance"[tiab]) AND (review[pt] OR "systematic review"[tiab])` | 58 | 16195486→441 (one review chosen as the indirect source for nitrite tolerance). |
| AN5 | Known-item and gap check: `(Han YH[au] AND alcoholics[ti]) OR (Zacny JP[au] AND (sevoflurane[tiab] OR isoflurane[tiab] OR halothane[tiab])) OR ((amyl[ti] OR nitrite[ti] OR nitrites[ti]) AND tolerance[ti])` | 40 (37 new) | 20982390→434; 17893272→442. The 1969 study on anaesthetic needs in people with alcohol dependence (Han) was not found in PubMed under this author form. Most "nitrite tolerance" hits were aquaculture and microbiology. |

Abstracts read (searched for tolerance findings) for #430–434, #438–439 and #442.

## 30. Salvia divinorum

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| SA1 | `(salvinorin*[tiab] OR "Salvia divinorum"[tiab] OR "S. divinorum"[tiab]) AND (tolerance[tiab] OR "cross-tolerance"[tiab] OR repeated[tiab] OR "reverse tolerance"[tiab] OR sensitization[tiab])` (no humans filter) | 27 (26 new) | 26058662→444. Not kept: analogue chemistry, allergy and cerebrovascular studies, rodent studies of salvinorin A given repeatedly before cocaine (21757186, 18246329), which address cocaine responses rather than tolerance to salvinorin A. |
| SA2 | `("Salvia divinorum"[tiab] OR salvinorin*[tiab]) AND (humans[MeSH Terms]) AND (survey[tiab] OR users[tiab] OR volunteers[tiab] OR participants[tiab] OR "placebo-controlled"[tiab])` | 47 | 21131142→443. Abstracts of the laboratory studies (23135605, 21901316) and surveys (20627425, 16720081, 20937616, 17703708) were searched for tolerance findings; none reported any. Not kept: prevalence surveys, YouTube and forum studies, toxicology methods. |
| SA3 | `salvinorin*[tiab] AND (desensitization[tiab] OR desensitisation[tiab] OR internalization[tiab] OR "receptor downregulation"[tiab] OR tachyphylaxis[tiab] OR "acute tolerance"[tiab] OR "chronic administration"[tiab] OR "chronic treatment"[tiab])` | 13 | 15383632→445. Not kept: analogue pharmacology and reviews. |

## 31. Cross-cutting

| # | String | Hits | Kept (PMID → list #) |
|---|---|---|---|
| CC1 | Loss of tolerance and overdose: `(overdose[ti] OR "drug-related death"[ti] OR "drug-related deaths"[ti] OR "drug related deaths"[ti] OR mortality[ti] OR death[ti] OR deaths[ti]) AND (opioid*[tiab] OR heroin[tiab] OR "drug users"[tiab] OR "people who use drugs"[tiab] OR "people who inject drugs"[tiab]) AND ((release[tiab] AND (prison*[tiab] OR jail*[tiab] OR incarcerat*[tiab])) OR detoxification[tiab] OR "residential treatment"[tiab] OR "inpatient treatment"[tiab] OR "hospital discharge"[tiab] OR "discharge from hospital"[tiab] OR "loss of tolerance"[tiab] OR "reduced tolerance"[tiab] OR "lowered tolerance"[tiab]) AND ("systematic review"[tiab] OR "meta-analysis"[tiab] OR cohort[tiab] OR "record linkage"[tiab] OR "record-linkage"[tiab] OR "case-crossover"[tiab] OR "case-control"[tiab])` | 93 | 20579009→446 (also CC4); 33773635→449; 9492665→454; 24189594→457; 28319291→458; 28160345→459; 24612249→460; 38942554→461; 35080937→462; 17280803→467; 32096908→468; 22925008→469; 32969097→471; 31520924→472. From earlier searches: 18031430→466 (MB2); 29807248→473 (PO4). Not kept: cohorts on infections, surgery and pregnancy; policy and cost-effectiveness models; further regional post-release cohorts that repeat the design of those kept (e.g. 36821990, 39024534, 37164452, 42135928); a second Scottish hospital-discharge study (26539701) and a detoxification follow-up (20650614) that repeat #469 and #467. |
| CC2 | Naltrexone: `naltrexone[tiab] AND (overdose[ti] OR mortality[ti] OR death[ti] OR deaths[ti] OR fatal[ti]) AND (tolerance[tiab] OR "after cessation"[tiab] OR "after treatment"[tiab] OR discontinu*[tiab] OR "loss of tolerance"[tiab] OR cohort[tiab] OR "adverse events"[tiab])` | 46 (42 new) | 9179515→474; 22487087→476; 29560596→477 (Crossref `updated-by` lists a correction); 31082666→478 (also PO4); 10707430→453 (no DOI in PubMed; 10.1046/j.1360-0443.1999.9479612.x found by Crossref bibliographic search, as on the Interactions list). Not kept: medication-for-OUD cohorts without a naltrexone stopping period, a pharmacovigilance series (33258068), a 2008 naltrexone-implant cohort (17931824) and a 2002 review (11982544) covered by #476 and #477. |
| CC3 | Cross-tolerance between classes: `("cross-tolerance"[ti] OR "cross tolerance"[ti] OR "cross-tolerant"[ti]) AND humans[MeSH Terms]` | 101 | 14085622→450; 5350620→451; 32677699→452; 5061865→479. For Methadone and buprenorphine: 627883→392; 5289287→393; 38326506→394. Already listed: 21049267 (#288), 16427197 (#386), 11427327 (#387), 2594396 (#367), 6134543 and 4036631 (Benzodiazepines), 6264608 (#27), 35900876 (LSD). Most hits were immunology ("endotoxin cross-tolerance"), plant stress and nitrate pharmacology; no-DOI items (6762674, 17373407, 9580575) not kept. |
| CC4 | Known-item check: `(Binswanger IA[au] AND "release from prison"[ti]) OR (Farrell M[au] AND Marsden J[au] AND prisoners[ti]) OR (Zlodre J[au]) OR (Bird SM[au] AND Hutchinson SJ[au] AND release[ti]) OR (Ravndal E[au] AND mortality[ti]) OR (Lewer D[au] AND hospital[ti] AND overdose[ti]) OR (Brinkley-Rubinstein L[au] AND fentanyl[ti]) OR (Digiusto E[au] AND naltrexone[tiab]) OR (Gibson AE[au] AND naltrexone[ti]) OR (Kelty E[au] AND overdose[ti])` | 27 (26 new) | 23078476→447; 17215533→448; 12534423→455; 18199304→456; 29459328→463; 22966409→464; 20022184→465; 15049745→475. Not kept: a case report of overdose with a naltrexone implant (17309406), a 2017 comparison of three treatments (28609749) covered by #476, unrelated papers by the same authors. |
| CC4b | `(Lewer D[au] AND (hospital*[ti] OR discharge*[ti])) OR (Gibson A[au] AND Degenhardt L[au] AND naltrexone[ti])` (the case-crossover study title has "overdoses", which CC4 missed) | 18 (17 new) | 34610017→470. The 2007 Gibson and Degenhardt naltrexone mortality comparison was not found in PubMed. |

The E-utilities tab had to be replaced twice near the end (after SA2 and after SA3), so the "new" counts for SA3 and for CC1–CC4b are relative only to the searches run in the replacement tab.

## Overlap with other DOI lists

Papers on `_Tolerance_DOI-LIST.md` whose DOI also appears on another list in `search-logs/` (checked by DOI on 2026-10-17).

| # | First author(s) | DOI | Also on |
|---|---|---|---|
| 58 | Dijkstra et al. | 10.1016/j.drugalcdep.2016.11.014 | `GHB-GBL_DOI-LIST.md` |
| 60 | Kamal et al. | 10.1007/s40263-016-0402-z | `GHB-GBL_DOI-LIST.md` |
| 78 | James & Rogers | 10.1007/s00213-005-0084-6 | `Caffeine_DOI-LIST.md` |
| 92 | Rogers et al. | 10.1007/s00213-012-2889-4 | `Caffeine_DOI-LIST.md` |
| 93 | Juliano & Griffiths | 10.1007/s00213-004-2000-x | `Caffeine_DOI-LIST.md` |
| 124 | Small et al. | 10.3109/10826080902961179 | `Cocaine_DOI-LIST.md` |
| 125 | Ashok et al. | 10.1001/jamapsychiatry.2017.0135 | `Amphetamine_DOI-LIST.md`, `Cocaine_DOI-LIST.md`, `methamphetamine_DOI-LIST.md` |
| 130 | Foltin et al. | 10.1016/0376-8716(88)90015-4 | `Cocaine_DOI-LIST.md` |
| 148 | Wachtel & de Wit | 10.1097/00008877-199905000-00004 | `Amphetamine_DOI-LIST.md` |
| 161 | Volkow et al. | 10.1523/JNEUROSCI.21-23-09414.2001 | `methamphetamine_DOI-LIST.md` |
| 162 | Wang et al. | 10.1176/appi.ajp.161.2.242 | `methamphetamine_DOI-LIST.md` |
| 176 | Winstock et al. | 10.1111/j.1360-0443.2011.03502.x | `Synthetic-cathinones_DOI-LIST.md` |
| 177 | Mead & Parrott | 10.1016/j.brainres.2020.146740 | `Synthetic-cathinones_DOI-LIST.md` |
| 178 | Freeman et al. | 10.1111/j.1360-0443.2011.03719.x | `Synthetic-cathinones_DOI-LIST.md` |
| 179 | Jones et al. | 10.1177/0269881116653106 | `Synthetic-cathinones_DOI-LIST.md` |
| 188 | Farré et al. | 10.1007/s00213-004-1789-7 | `MDMA_DOI-LIST.md` |
| 204 | de Wit et al. | 10.1111/adb.13143 | `LSD_DOI-LIST.md` |
| 207 | Isbell et al. | 10.1007/BF00409110 | `LSD_DOI-LIST.md` |
| 221 | Strassman et al. | 10.1016/0006-3223(95)00200-6 | `DMT-Ayahuasca_DOI-LIST.md` |
| 222 | Dos Santos et al. | 10.1007/s00213-011-2434-x | `DMT-Ayahuasca_DOI-LIST.md` |
| 226 | Strassman | 10.1016/0166-4328(96)00081-2 | `DMT-Ayahuasca_DOI-LIST.md` |
| 231 | Reckweg et al. | 10.1111/jnc.15587 | `5-MeO-DMT_DOI-LIST.md` |
| 233 | Davis et al. | 10.1177/0269881118769063 | `5-MeO-DMT_DOI-LIST.md` |
| 237 | Halpern et al. | 10.1016/j.biopsych.2005.06.038 | `Mescaline_DOI-LIST.md` |
| 245 | Morgan & Curran | 10.1111/j.1360-0443.2011.03576.x | `Ketamine_DOI-LIST.md` |
| 246 | Morgan et al. | 10.1111/j.1360-0443.2009.02761.x | `Ketamine_DOI-LIST.md` |
| 249 | Narendran et al. | 10.1176/appi.ajp.162.12.2352 | `Ketamine_DOI-LIST.md` |
| 250 | Morgan et al. | 10.1111/j.1360-0443.2004.00879.x | `Ketamine_DOI-LIST.md` |
| 251 | Morgan et al. | 10.1111/j.1360-0443.2008.02394.x | `Ketamine_DOI-LIST.md` |
| 252 | Krystal et al. | 10.1001/archpsyc.55.4.354 | `_Interactions_DOI-LIST.md` |
| 253 | Dickerson et al. | 10.1177/0269881108098612 | `Ketamine_DOI-LIST.md` |
| 268 | Stanciu et al. | 10.1111/ajad.12389 | `DXM_DOI-LIST.md` |
| 270 | Miller | 10.1080/13556210500352410 | `DXM_DOI-LIST.md` |
| 275 | Yajnik et al. | 10.1016/0091-3057(95)02278-3 | `Nitrous-oxide_DOI-LIST.md` |
| 279 | Back et al. | 10.1111/add.16380 | `Nitrous-oxide_DOI-LIST.md` |
| 309 | Cooper | 10.1007/s11920-016-0694-1 | `Synthetic-cannabinoids_DOI-LIST.md` |
| 310 | Vandrey et al. | 10.1016/j.drugalcdep.2011.07.011 | `Synthetic-cannabinoids_DOI-LIST.md` |
| 323 | Warner-Smith et al. | 10.1046/j.1360-0443.2001.96811135.x | `_Interactions_DOI-LIST.md` |
| 337 | van Lemmen et al. | 10.1097/ALN.0000000000005931 | `Fentanyl-and-analogues_DOI-LIST.md` |
| 345 | Henderson | 10.1520/jfs13045j | `Fentanyl-and-analogues_DOI-LIST.md` |
| 346 | Jumbelic | 10.1097/PAF.0b013e31818738b8 | `Fentanyl-and-analogues_DOI-LIST.md` |
| 352 | Kim et al. | 10.3389/fphar.2014.00108 | `Prescription-opioids_DOI-LIST.md` |
| 359 | Agnoli et al. | 10.1001/jama.2021.11013 | `Prescription-opioids_DOI-LIST.md` |
| 374 | Kennedy et al. | 10.1371/journal.pmed.1004123 | `Prescription-opioids_DOI-LIST.md` |
| 375 | Larochelle et al. | 10.1001/jamanetworkopen.2022.26523 | `Prescription-opioids_DOI-LIST.md` |
| 376 | Fenton et al. | 10.1001/jamanetworkopen.2022.16726 | `Prescription-opioids_DOI-LIST.md` |
| 383 | Sordo et al. | 10.1136/bmj.j1550 | `Heroin_DOI-LIST.md`, `Methadone-Buprenorphine_DOI-LIST.md`, `_Harm-reduction_DOI-LIST.md` |
| 384 | Santo et al. | 10.1001/jamapsychiatry.2021.0976 | `Heroin_DOI-LIST.md`, `Methadone-Buprenorphine_DOI-LIST.md` |
| 406 | Bell et al. | 10.1111/j.1360-0443.2009.02627.x | `Heroin_DOI-LIST.md`, `Methadone-Buprenorphine_DOI-LIST.md` |
| 408 | Cornish et al. | 10.1136/bmj.c5475 | `Heroin_DOI-LIST.md`, `Methadone-Buprenorphine_DOI-LIST.md` |
| 426 | Singh et al. | 10.1016/j.drugalcdep.2014.03.017 | `Kratom_DOI-LIST.md` |
| 427 | Vadiei et al. | 10.1007/s11920-025-01631-7 | `Kratom_DOI-LIST.md` |
| 437 | Howard & Perron | 10.1186/1471-244X-9-8 | `Alkyl-nitrites-and-inhalants_DOI-LIST.md` |
| 443 | Johnson et al. | 10.1016/j.drugalcdep.2010.11.005 | `Salvia-divinorum_DOI-LIST.md` |
| 453 | White & Irvine | 10.1046/j.1360-0443.1999.9479612.x | `_Interactions_DOI-LIST.md` |
| 457 | Binswanger et al. | 10.7326/0003-4819-159-9-201311050-00005 | `Heroin_DOI-LIST.md` |
| 458 | Bukten et al. | 10.1111/add.13803 | `Heroin_DOI-LIST.md` |
| 461 | Bukten & Stavseth | 10.1016/S2468-2667(24)00098-7 | `Heroin_DOI-LIST.md`, `Methadone-Buprenorphine_DOI-LIST.md` |
