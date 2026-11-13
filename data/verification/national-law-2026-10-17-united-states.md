# W2 report: the United States' own (federal) lists of controlled substances

Read on 2026-10-17 by AI reader W2. Output: `/home/claude/drug-encyclopedia/data/legal/_incoming/united-states.json` (76 rows under the 25 drug-page keys; the "if named" item ayahuasca has no row because no list names it).

## 1. The US federal lists

- **Schedules I-V of the Controlled Substances Act**, kept by the Drug Enforcement Administration (DEA) in 21 CFR 1308.11 to 1308.15. Each schedule is divided into lettered paragraphs. For example, Schedule I has (b) opiates, (c) opium derivatives, (d) hallucinogenic substances, (e) depressants, (f) stimulants, (g) cannabimimetic agents and (h) temporary listings. Every entry carries a DEA Controlled Substances Code Number (CSCN).
- **Temporary scheduling orders** (21 U.S.C. 811(h)) are codified in 1308.11(h).
- **Related texts read:**
  - 21 CFR 1300.01: definitions of isomer, positional isomer, marijuana and state medical marijuana license.
  - 1307.31: Native American Church peyote exemption.
  - 1308.22: excluded over-the-counter products.
  - 1310.02: List I and List II chemicals. These are regulated chemicals, not controlled substances.
  - 21 U.S.C. 802: statutory definitions.
- **The DEA's own published lists.** DEA's Diversion Control Division publishes "Lists of: Scheduling Actions, Controlled Substances, Regulated Chemicals" (August 2026). From it I read "Controlled Substances - Alphabetical Order" and "Scheduling Actions - Alphabetical Order", both dated 27-Aug-26.

Federal law only; state law was not read.

## 2. Sources read (all official)

| Source | URL | Version printed | Used for |
|---|---|---|---|
| eCFR 21 CFR 1308.11 Schedule I | https://www.ecfr.gov/current/title-21/section-1308.11 | "up to date as of 10/15/2026"; Title 21 last amended 10/14/2026; section version of 2026-10-09 | (a)-(d)(99) |
| eCFR 1308.12, 1308.13, 1308.14, 1308.15 (Schedules II-V) | https://www.ecfr.gov/current/title-21/section-1308.12 (and .13, .14, .15) | same | all Schedule II-V rows |
| eCFR 1300.01, 1307.31, 1308.22, 1310.02 | https://www.ecfr.gov/current/title-21/section-1300.01 (etc.) | same | definitions, peyote exemption, levmetamfetamine inhalers, GBL |
| eCFR search API, current text of part 1308 (versions modified on or after 2026-10-01, i.e. 2026-10-06 and 2026-10-09) | https://www.ecfr.gov/api/search/v1/results | version of 2026-10-09 | entry numbers after (d)(99); searches for the names of items not found |
| DEA, Controlled Substances - Alphabetical Order | https://www.deadiversion.usdoj.gov/schedules/orangebook/c_cs_alpha.pdf | 27-Aug-26, 24 pages | the complete list: code, schedule, other names, positional-isomer notes |
| DEA, Scheduling Actions - Alphabetical Order | https://www.deadiversion.usdoj.gov/schedules/orangebook/a_sched_alpha.pdf | 27-Aug-26 | temporary/permanent history of 12 substances |
| Federal Register final rules (GovInfo HTML) | see JSON `sources` | as published | see the list below |
| Federal Register notice of intent 91 FR 65370 (14 Oct 2026) and temporary order 91 FR 54948 (26 Aug 2026) | federalregister.gov and govinfo.gov | as published | kratom alkaloids |
| 21 U.S.C. 802, U.S. Code 2024 ed. | https://www.govinfo.gov/link/uscode/21/802?link-type=html | 2024 Edition, through Pub. L. 118-189 | marihuana and hemp; DXM not mentioned; analogue definition |
| Federal Register API document list, 21 CFR part 1308, 1 Jan 2025 to 14 Oct 2026 | federalregister.gov/api/v1/documents.json | 52 documents | finding aid only |

The Federal Register final rules read are:
- 88 FR 86266 (13 Dec 2023): ADB-BUTINACA, α-PiHP, 3-MMC.
- 90 FR 51102 (17 Nov 2025): 4-CMC.
- 91 FR 2297 (20 Jan 2026): cannabimimetic agents; JWH-018 and AM2201 moved to (d).
- 91 FR 9985 (2 Mar 2026): clonazolam, diclazepam, etizolam, flualprazolam, flubromazolam.
- 91 FR 21958 (24 Apr 2026): MDMB-4en-PINACA.
- 91 FR 22714 (28 Apr 2026): FDA-approved and state-licensed marijuana products moved to Schedule III.

## 3. How I searched, and what could not be read

**The Schedule I page is cut off.** The eCFR page for 21 CFR 1308.11 ends mid-entry at (d)(99), whatever offset is used. I tried three other routes:
- The eCFR API text routes (`/api/versioner/v1/full/`, `/api/renderer/v1/content/`) are refused under robots.txt.
- The latest annual CFR edition on GovInfo (revised 1 Apr 2025) is old, and it too is cut off, at (h)(76).
- The other Schedule pages (1308.12-1308.15) read complete.

**How the rest of Schedule I was established:**
- **The DEA alphabetical list** was read in full. It contains every controlled substance with its code and schedule, as of 27-Aug-26.
- **The Federal Register rules** that placed the relevant entries were read. Their amendatory instructions give the paragraph numbers.
- **The current eCFR text** was read for each entry through the eCFR search API. Its excerpts show the entry number and the neighbouring entries. The filter `last_modified_on_or_after=2026-10-01` was used because the `date` filter returned 2025 versions. With that filter, only the versions of 2026-10-06 and 2026-10-09 come back.
- **Changes after the DEA list's date.** The Federal Register list for part 1308 was read up to 14 Oct 2026. The rules after 27 Aug 2026 are:
  - a temporary order for 5,6-dichloro brorphine and three related substances;
  - cipepofol (Schedule IV);
  - diphenidine (Schedule I);
  - a correction on O-desmethyltramadol;
  - the removal of exemption status for inactive butalbital products.

  None of them touches the 77 items.
- **Names of items not found** were searched in the current text, twice each (17 searches). A positive control (bromazolam, a current temporary listing) was found.

**Not used, as facts:**
- The part-level eCFR versions summary. It wrongly gave 2026-06-24 as the last change to 1308.11, and 2023 as the last change to 1308.14. The section-level list and the text itself contradict it.
- Any law firm, Wikipedia or news page. None was opened.
- Penalties and quantity rules.

**Noted but not used to decide any row:** the controlled substance analogue definition (21 U.S.C. 802(32)).

## 4. Method of reading

- **Two readings.** Every chunk was read twice through WebFetch, with differently worded prompts and different output formats and orders, for example "(b)(N) | name | code" against "c;;N;;name;;code" with the paragraphs in reverse order.
- **The eCFR summarizer will not quote long passages.** It gave short names and codes. Wording that decides a row was asked for in short quotations, twice.
- **Script comparison.** The two readings were compared by Python scripts, with both readings pasted inline. Numbers and codes were compared strictly, and names after normalisation. The DEA list chunks were aligned with `difflib` so that a row missing from one reading is isolated.
- **No reading files were saved**, because the caller asked for only the two output files.
- **Chunks read:**
  - Schedule I: 3 chunks.
  - Schedules II, III, IV and V: one chunk each.
  - 1310.02.
  - DEA alphabetical list: 8 chunks of 3 pages, about 630 rows.
  - DEA scheduling actions: 26 rows.
  - The FR rules.
  - 12 entry excerpts.
  - 17 name searches plus a positive control.
- **Matching.** The 77 items were matched by script, with name variants, against 543 DEA rows (the 86 anabolic-steroid rows, code 4000, were left out) and 83 CFR rows. Every hit was checked by eye.

## 5. Disagreements between readings, and how each was settled

None of the disagreements concerns one of the 77 items.

- **Schedule I (b)-(c), 144 rows: all codes agree.**
  - (b)(42), (b)(77)-(80) and (c)(10) differed in which name was given.
  - A third reading showed that both names are printed, and that (c)(10) reads "Etorphine (except hydrochloride salt)".
- **Schedule I (d)(1)-(99), Schedule II (72 rows), Schedule IV (82), Schedule V (17), 1310.02 (53):** no disagreement.
- **Schedule III:**
  - The 38 coded rows and 86 steroid names agree.
  - Three rows were paraphrased differently: (b)(1), (c)(3) and (c)(6).
  - (c)(6) (GHB products) was settled by two exact-quote readings.
- **1308.22:** one reading counted 15 table rows and the other 16. Both find the same two levmetamfetamine inhalers. This was not pursued, because only those two rows are used.
- **DEA alphabetical list:**
  - **Pages 1-3.** Reading B left out four positional-isomer notes (2C-E, 2C-T-4, 2C-T-7, DOET). A third reading showed that they are printed. Four short names sat in different columns, which needed no change.
  - **Pages 4-6.** Reading B printed a stray "8001" row and withdrew it itself. It was excluded.
  - **Pages 7-9.** Brivaracetam's chemical name was placed in a different column.
  - **Pages 10-12.** Reading A missed Ethylmethylthiambutene (9623). It is present, confirmed by a third reading and by eCFR (b)(41).
  - **Pages 13-15.** Flubromazolam's alternative chemical name was garbled by line wrap in reading B. Its code and schedule agree.
  - **Pages 19-21.**
    - Reading B missed Noracymethadol (9633). It is present (third reading; eCFR (b)(73)).
    - Reading A missed "Opium poppy" (9650, II). It is present (third reading).
    - One pentedrone synonym is missing in reading B.
  - **Pages 22-24.** Reading B gave no synonyms for phenyl fentanyl, thiofuranyl fentanyl and valeryl fentanyl.
- **FR rules, entry excerpts, 1300.01, 1307.31, 21 U.S.C. 802, scheduling actions:** no disagreement.
- **Details read only once were left out or replaced.** These were one extension's end date, the threshold figures in the 7-hydroxymitragynine notice, a page citation, and a paraphrase of the new cannabimimetic-agents definition. The August 2026 kratom-derivative order was confirmed in the order itself.

**False matches rejected by eye:**
- Lisdexamfetamine and MDA, for amfetamine and dexamfetamine.
- 5-MeO-DMT, and psilocyn's positional-isomer note, for DMT.
- Levomethorphan and racemethorphan, for DXM.
- Fentanyl analogues, for fentanyl, acetylfentanyl and furanylfentanyl.
- PEPAP and MPPP ("synthetic heroin"), for heroin.
- Ecgonine, for cocaine.
- Lysergic acid and lysergic acid amide, for LSD.
- The 2C-B row ("sold as Ecstasy"), for MDMA.
- MMDA, N-hydroxy MDA and N-ethyl MDA, for MDA.
- Ethylone (bk-MDEA), for MDEA.
- Aminorex, for methamphetamine.
- Precursors and 3-MeO-PCP, for PCP.
- Mitragynine pseudoindoxyl, MGM-15 and MGM-16, for mitragynine and 7-hydroxymitragynine.
- MAM-2201 and EAM-2201, for AM-2201.
- 4-chloro-α-PVP, for α-PVP.
- 4-MEAP, for NEP.
- O-desmethyltramadol, for tramadol.

## 6. Result

**Listed in Schedules I-V: 63 of the 77 items.**
- 61 are named.
- Dexamfetamine and esketamine are covered by the entries' own isomer wording: "optical isomers" in 1308.12(d)(1), and "isomers" in 1308.13(c)(7).

**Listed elsewhere:** GBL is a List I chemical (1310.02(a)(25)). It is regulated, not scheduled.

**Draft, covered only as positional isomers:** 2-MMC (of mephedrone, (d)(36)) and 3-CMC (of 4-CMC, (d)(106)).

**Not found: 10 items, plus ayahuasca ("if named", no row).**
- CBD and DXM are draft, because a generic clause may matter.
- The others are ai-checked: 1,4-butanediol, kratom, mitragynine, 7-hydroxymitragynine, Salvia divinorum, salvinorin A, NEP and 4-BMC.

**Rows:** 76, of which 72 are ai-checked and 4 draft.

**Notable current facts:**
- The April 2026 order (91 FR 22714) put marijuana "in a U.S. Food and Drug Administration approved product or subject to a state medical marijuana license" in Schedule III (1308.13(g)(2)-(4)). Other marihuana stays in Schedule I (d)(23).
- Etizolam, flualprazolam and flubromazolam became permanent Schedule I depressants on 1 Apr 2026, at (e)(3)-(5). GHB was renumbered (e)(6).
- JWH-018 and AM2201 moved to (d)(107) and (d)(108) on 19 Feb 2026.
- MDMB-4en-PINACA became permanent at (d)(110) on 27 Apr 2026.
- 4-CMC was added at (d)(106) on 17 Dec 2025.
- No item of the 77 is held only by a temporary order.

**Medical use** is recorded only where an entry itself names FDA approval or a state medical marijuana license: cannabis, delta-9-THC (dronabinol) and GHB.

## 7. Unsettled: for the editor

1. **The eCFR cut-off.** The Schedule I numbers after (d)(99) come from the FR rules, the search-API excerpts and DEA's list. They are ADB-BUTINACA (d)(102), 3-MMC (d)(104), 4-CMC (d)(106), JWH-018 (d)(107), AM2201 (d)(108), MDMB-4en-PINACA (d)(110), etizolam, flualprazolam and flubromazolam (e)(3)-(5), GHB (e)(6) and cathinone (f)(4). (h), (g) and (i) were not read in full. Please confirm in a browser.
2. **Codes for the new Schedule III cannabis entries.** eCFR prints "XXXX", as published. DEA's list gives 7362 (marijuana), 7353 (marijuana extract) and 7386 (naturally derived delta-9-THC). Which should the page show?
3. **2-MMC and 3-CMC.** Should they be stated as Schedule I positional isomers? This is a chemical application of 21 CFR 1300.01 for paragraph (d). DEA's 2023 rule says positional isomers of mephedrone have been controlled since 9 Jul 2012, but it names only 3-MMC.
4. **CBD.** It is not named. Whether it is covered depends on its source: it may fall under the marihuana or marihuana-extract definitions, while hemp is excluded. Please decide how to present it.
5. **DXM.** No text read excludes it by name. 1308.12(c) excepts only dextrorphan and levopropoxyphene, while extending control to the isomers of the listed levomethorphan and racemethorphan. DEA's list does not list DXM. Please decide whether to state that it is not federally controlled.
6. **7-hydroxymitragynine.** It is not controlled now. A notice of intent of 14 Oct 2026 announces a temporary Schedule I order on or after 13 Nov 2026. Re-check after that date.
7. **Medical use.** Schedules II-V imply accepted medical use under 21 U.S.C. 812(b), which was not read, but the lists do not state it. The field is left null for those rows.
8. **GBL.** It is a List I chemical, not a controlled substance. How should the page show it?
9. **Ayahuasca and San Pedro.** Neither is named. DMT and mescaline are listed, and (d) covers any material containing them. Peyote is named. The Native American Church exemption in 1307.31 is recorded in the peyote row.
