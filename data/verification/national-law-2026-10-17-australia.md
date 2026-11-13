# W2 report: Australia's national scheduling (the Poisons Standard)

Read on 2026-10-17 by AI reader W2. Output: `/home/claude/drug-encyclopedia/data/legal/_incoming/australia.json` (75 rows under the 25 drug-page keys; the two "if named" items are not named, so they have no row).

## 1. The list

Australia schedules substances nationally in the **Poisons Standard**. The current one is the *Therapeutic Goods (Poisons Standard—October 2026) Instrument 2026* (F2026L01327). Section 1(2) says it may also be cited as the *Standard for the Uniform Scheduling of Medicines and Poisons No. 51*.

- **Version.** As made (28 Sep 2026), registered 30 Sep 2026. The whole instrument commences on 1 Oct 2026 (s 2). It repeals the June 2026 Standard (F2026L00633), with transitional provisions (s 4).
- **Current?** Yes. Three FRL readings agree that it is "In force" with compilation number 0 and no amendments:
  - the versions page;
  - the API version record (start 30 Sep 2026; isCurrent and isLatest true);
  - the API title record.

  Of the 83 FRL titles with "Poisons Standard" in their name, this is the only Poisons Standard instrument in force. (The 2008 amending Act is also in force, but it is an Act, not a Standard.)
- **Authority and administration.** Made under para 52D(2)(b) of the *Therapeutic Goods Act 1989*. Administered by the Department of Health, Disability and Ageing.
- **The Schedules.** These are the lists, and their titles were read twice (PDF table of contents and Reader's guide):
  - Schedule 2: Pharmacy medicines
  - Schedule 3: Pharmacist only medicines
  - Schedule 4: Prescription only medicines and prescription animal remedies
  - Schedules 5 to 7: Caution, Poisons, and Dangerous poisons
  - Schedule 8: Controlled drugs
  - Schedule 9: Prohibited substances
  - Schedule 10: Substances of such danger to health as to warrant prohibition of supply and use
  - Appendices A to M, then an Index
- **State and territory laws.** The Reader's guide says scheduling "is implemented through relevant State and Territory legislation". State and territory laws were not read.
- **The Index has no legal force.** Section 5(2) says: "The Index is not part of this instrument."
- **Generic clause (s 7, read twice, identical).** Unless the contrary intention appears, a reference to a substance includes:
  - (a) the substance whether prepared from natural sources or artificially;
  - (b) a plant (other than one in Schedule 8 or 9), or any part of it, when packed or prepared for therapeutic use;
  - (c) "every salt, active principle or derivative of the substance, including esters and ethers";
  - (d) alkaloids;
  - (e) stereoisomers;
  - (f) recombinant forms;
  - (g) preparations and admixtures.

  The Reader's guide adds that a substance counts as a derivative only "if it is not individually listed elsewhere". That is decided by a balanced consideration of factors, which this reading cannot apply.

## 2. Sources

| Source | URL | Version | Used for | Read |
|---|---|---|---|---|
| The instrument (FRL HTML from the EPUB, and the authorised PDF) | https://www.legislation.gov.au/F2026L01327/asmade/text | As made; in force; compilation 0 | Reader's guide; ss 1–7; table of contents | twice |
| FRL API full-text search | `https://api.prod.legislation.gov.au/v1/titles/search(criteria='text("…",nameAndText,contains)')?$filter=id eq 'F2026L01327'` | Indexed text of F2026L01327 | Every Index line | decisive phrases twice |
| FRL API Versions and Documents | `https://api.prod.legislation.gov.au/v1/Versions?$filter=titleId eq 'F2026L01327'` | — | Compilation status; files (PDF 677 pp., EPUB with one HTML file) | once each, plus the versions page |
| Explanatory Statement | https://www.legislation.gov.au/F2026L01327/asmade/2026-09-30/es/original/pdf | 8 pp. | Testing the method only | once |
| Two small FRL amendment instruments | F2021L00070 (boric acid Index entry); F2021L01253 (ivermectin Index entry) | as made, 2021 | Learning the Index layout only (no facts taken) | once |
| NIST Chemistry WebBook (US Department of Commerce) | https://webbook.nist.gov/cgi/cbook.cgi?ID=… | online | Identity of four CAS numbers printed in the Index: 66142-81-2, 110-63-4, 591-81-1, 520-52-5 | once each |

**Facts from other sites.** No fact was taken from Wikipedia, law firms, news or AustLII.

**Pages that could not be read:**
- TGA pages: refused under robots rules.
- PubChem: refused under robots rules.
- NIST lookups for 69587-11-7 and 96-48-0: refused (HTTP 429). As the proxy instructed, they were not retried.

## 3. How I searched, and what could not be read

- **The Schedules and the Index could not be read as text.** The HTML (the only HTML file in a 280 KB EPUB) gives WebFetch only the first 84,879 characters, ending in s 47(2). The PDF gives 89,425 characters, ending in s 34, just after printed p. 21 of 677. The Word file comes back as binary. The previous session found the same. Schedules 8–10 are on pp. 280–298 and the Index starts on p. 369.
- **Workaround: exact-phrase search of the official text.** The FRL's own search API searches the indexed full text of the instrument. Filtered to F2026L01327, a query returns 1 or 0, so each query answers one yes/no question about a phrase. Tests showed that:
  - search is case-insensitive and ignores punctuation;
  - matching is an exact phrase: "methylamphetamine schedule 9" returns 0 although all three words occur in the text;
  - the indexed text runs to the end of the Index ("zolpidem schedule" returns 1).
- **Testing against known facts.** The method was checked against new entries named in the Explanatory Statement:
  - "spidoxamat schedule 5" = 1 and "spidoxamat schedule 4" = 0;
  - "teplizumab schedule 4" = 1;
  - "… No. 51" = 1 and "… No. 52" = 0.
- **Index layout.** Learned from small official FRL amendment instruments (2021). Each Index entry runs:
  1. the name;
  2. sometimes a line "cross reference: …" (synonyms, related names, or CAS numbers);
  3. "Schedule N" lines in descending order;
  4. "Appendix …" lines.

  An Index line was "read" by chaining phrases. For example, "codeine schedule 8 schedule 4 appendix" = 1 and "codeine schedule 8 schedule 4 schedule" = 0.
- **Line ends and alternatives.**
  - Every line end was tested: is another Schedule or an Appendix next?
  - Every name was tested for its own cross-reference line. Where a name has one, a match of "name Schedule N" can come from another entry's cross-reference list (this is what happened with THC).
  - All schedule numbers 2–10 were excluded with grouped OR queries.
- **CAS numbers as search keys.** For cross-reference entries and for names absent from the text, CAS numbers were tried only as search keys. A CAS number counts only when the official text contains it in the line found. Its identity is stated only where NIST confirms it.
- **Limits.**
  - The proxy rejects URLs longer than about 250 characters, so OR groups held 2–3 phrases.
  - About 800 queries were made. Near the end the FRL API began returning server errors on every request, including the Versions endpoint. The FRL's reuse page warns that heavy automated use is blocked automatically. I stopped querying.

## 4. Method of reading and comparison

- **Reading 1.** Lowercase, unpunctuated phrases, built step by step, with prompt A ("Report only the integer after @odata.count…").
- **Reading 2.** Each decisive phrase re-sent as a separate query:
  - in printed form, uppercase and punctuated;
  - with different `$select` parameters;
  - with prompt B ("How many records does this JSON say it contains…").

  Negative checks were re-sent as OR pairs.
- **Script comparison.** A Python script, with every reading pasted inline, compared the two readings. No reading files were saved.
  - 55 positive phrases: all agree.
  - 57 negative checks: all agree.
  - 7 checks were read once only (see section 7).
- **Front matter.** The Reader's guide and ss 1–7 were read twice with different prompts and compared by script. Section 5(2) and s 7(a)–(g) are identical in both readings. Sections 1(2), 2, 3 and 4(1) agree on the key fact (summary against verbatim).
- **Matching to the 77 items.** Each item was searched under every printed name variant (INN, Australian name, common name, code, chemical name), 136 names plus group words. Every hit was checked by eye.
- **What the matches show.**
  - The Standard's names are METHYLAMPHETAMINE, AMFETAMINE (cross-referenced to AMPHETAMINE), DEXAMFETAMINE (cross-referenced to DEXAMPHETAMINE), HEROIN, LYSERGIDE, PSILOCYBINE and PSILOCINE.
  - These names do not occur: diacetylmorphine, LSD, psilocin, dimethyltryptamine.

## 5. Disagreements between readings, and how each was settled

**No two readings of the same phrase disagreed.** The following points are corrections of my own interpretation, not disagreements between readings:

1. **THC and kratom.** These names first matched "name Schedule N", but each has its own cross-reference line. So those matches came from other entries' cross-reference lists that end in the name.
   - For THC: "…tetrahydrocannabinols schedule 4 schedule 3" was shown to be the CANNABIDIOL entry. The "…tetrahydrocannabinols schedule 9 schedule 8" line belongs to an entry not identified. THC is therefore left unsettled.
   - For kratom: its own line was read in full ("mitragyna speciosa cross reference kratom mitragynine cas no 4098-40-2 schedule 9").
2. **CBD.** An OR pair returned 1, and I first credited the wrong phrase. Single queries showed the hit was "nabiximols tetrahydrocannabinols". The CBD line was then confirmed in full.
3. **Psilocybine.** The search key 520-53-6 failed. The Index prints "psilocybin cas no 520-52-5", and NIST gives 520-52-5 as psilocybine. The official text and NIST agree.
4. **MDMA hydrochloride.** The search key 64057-70-3 failed. Testing the last digit found "64057 70 1", and the full line was then read twice.
5. **Ambiguous OR results.** Some OR results mixed a likely-true phrase with the one being tested (for example, methylphenidate 7 with methadone 8). These were re-run singly.
6. **Tool errors.**
   - URL-length rejections: re-run as smaller groups.
   - Final FRL server errors: two second-reading checks were lost (see section 7).

## 6. Result

**Listed: 45 rows**

- **Schedule 8 (18):**
  - stimulants: amfetamine, dexamfetamine, lisdexamfetamine, methylamphetamine, methylphenidate;
  - alprazolam and cocaine;
  - opioids: fentanyl, sufentanil, remifentanil, methadone, buprenorphine, morphine, oxycodone, hydrocodone, tapentadol;
  - ketamine and esketamine.
- **Schedule 8 and Schedule 4:** codeine.
- **Schedule 9 and Schedule 8:** MDMA and psilocybin.
- **Schedule 9 (14):**
  - coca leaf, heroin, LSD, DMT, MDA, PCP;
  - kratom (Mitragyna speciosa) and mitragynine;
  - Salvia divinorum and salvinorin A;
  - mephedrone, flubromazolam, GHB, and 2C-B (by CAS number).
- **Schedule 4 (6):** diazepam, clonazepam, lorazepam, bromazepam, tramadol, cathine.
- **Schedule 4 and Schedule 3:** CBD.
- **Schedule 4 and Schedule 2:** dextromethorphan.
- **Schedule 10 (2):** GBL, and 1,4-butanediol (by CAS number).
- **Sodium oxybate** has a separate Schedule 8 line.

**Not found: 20 rows, plus the 2 "if named" items**

- **Not found (20):** 2C-E, 2C-C, 5-MeO-DMT, etizolam, flualprazolam, carfentanil, acetylfentanyl, furanylfentanyl, 7-hydroxymitragynine, AM-2201, 5F-MDMB-PINACA, MDMB-4en-PINACA, ADB-BUTINACA, cathinone, 3-MMC, 3-CMC, 4-CMC, NEP, 2-MMC, 4-BMC.
- **"If named" items:** neither ayahuasca nor peyote or San Pedro is named. These words were searched and none occurs: ayahuasca, Banisteriopsis, Psychotria, Lophophora, peyote, Trichocereus, Echinopsis, San Pedro.

**Unsettled: 10 rows**

- **Named, but the line was not resolved:** cannabis (and resin), THC/dronabinol, mescaline, psilocin, MDPV.
- **CAS line ending in Schedule 9, identity not confirmed:** 2C-I, 2C-T-7, JWH-018.
- **CAS number present, no Schedule found after it:** MDEA, alpha-PVP.

**Verification.** All rows are **draft** (see section 7, point 1). No `medical_use` is recorded: the lines read do not state one.

## 7. Unsettled: for the editor

1. **Method.** No Schedule entry was read. Every status comes from Index lines confirmed by exact-phrase search, and the Index is not part of the instrument (s 5(2)). Two agreeing searches back each listed status, but I kept every row draft.
   - Decide whether such rows may count as ai-checked.
   - Better still, have Schedules 4, 8, 9 and 10 and the Index read in a browser. The Schedule entries also carry conditions that were not read (for CBD in Schedules 3 and 4, DXM in Schedule 2, codeine in Schedule 4, MDMA and psilocybine in Schedule 8, and GBL and 1,4-butanediol in Schedule 10).
2. **Named, but no Schedule lines reached.**
   - Cannabis: its entry begins "cannabis cross reference cannabis sativa hemp …".
   - THC and dronabinol.
   - Mescaline: followed by none of Schedule, cross reference, Appendix or CAS.
   - Psilocin: PSILOCINE has a cross-reference line whose targets were not found.
   - MDPV.
3. **Entry name not read.** These statuses rest on a cross-reference list inside an entry whose own name was not read: DMT, MDMA, MDA, salvinorin A, mephedrone, GHB, 2C-B and 1,4-butanediol.
4. **CAS identities.**
   - 2C-I (69587-11-7), 2C-T-7 (207740-26-9) and JWH-018 (209414-07-3) each have a CAS number followed by "Schedule 9", but the identities were not confirmed officially: NIST refused one lookup (429) and has no record of the other two.
   - For MDEA (82801-81-8) and alpha-PVP (14530-33-7), the CAS numbers occur but no Schedule was found after them.
5. **Group entries.** These are indexed but their text was not read: "…cannabinomimetics" (Schedule 9) and "…cathinones" (Schedule 9). The words "phenethylamine", "phenylethylamine" and "benzodiazepine" also occur. Together with s 7(c), they may cover the not-found synthetic cannabinoids, cathinones (including cathinone itself, whose singular name does not occur), 2C-E and 2C-C, 5-MeO-DMT, etizolam and flualprazolam, the fentanyl analogues and 7-hydroxymitragynine.
6. **Read once only.**
   - The absence tests behind the 20 not-found rows: the FRL API stopped answering before the second reading.
   - The Schedule 9 exclusion for amfetamine.
   - The line ends for 1,4-butanediol and for the Appendix after methylamphetamine, dexamfetamine and DXM.
   - The exclusion of the minor Schedules (2, 3, 5, 6, 7 and 10) for each drug.
7. **Possible relevance for the site.** Schedule 10, not Schedule 9, holds GBL and 1,4-butanediol, and Schedule 4, not Schedule 8, holds diazepam, clonazepam, lorazepam, bromazepam and tramadol. Both depend on the Index; confirm them against the Schedules before publishing.
