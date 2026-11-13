# W2 report: China (People's Republic of China, mainland)

Checked on 2026-10-17 by AI reader W2, using WebSearch and WebFetch only.

Output: `/home/claude/drug-encyclopedia/data/legal/_incoming/china.json`. It has 75 rows under the 25 drug-page keys. The two "if named" items (ayahuasca, peyote/San Pedro) are not named in any list, so they have no row.

## 1. The lists

**Legal frame.** Article 3 of the 麻醉药品和精神药品管理条例 (Regulations on Narcotic Drugs and Psychotropic Substances) was amended by State Council Decree No. 797 (6 Dec 2024, in force 20 Jan 2025). It was read twice and both readings agree. It says:
- controlled substances are those in the catalogues, which are split into 药用类 (medicinal) and 非药用类 (non-medicinal);
- medicinal psychotropics are split into 第一类 (Class I) and 第二类 (Class II);
- the drug regulator (NMPA), with the MPS and the health ministry (NHC), makes the medicinal catalogue;
- the MPS, with the NMPA and NHC, makes the non-medicinal catalogue;
- a non-medicinal substance found to have medical use moves to the medicinal catalogue.

So China now has three lists, plus the separate precursor list.

| List | Issued by | Version | Size |
|---|---|---|---|
| 药用类麻醉药品目录（2025年版） (Catalogue of Medicinal Narcotic Drugs) | NMPA, MPS, NHC, Announcement 2025 No. 55, Annex 1 | dated 21 Jul 2025, in force on publication (posted 28 Jul 2025) | 32 entries |
| 药用类精神药品目录（2025年版） (Catalogue of Medicinal Psychotropic Substances) | same, Annex 2 | same; Class II amended by 2026 No. 58 (dated 6 Jul 2026, in force 1 Oct 2026: methoxyethyl etomidate, lorotomidate, solriamfetol) | Class I 18; Class II 78 (+3) |
| 非药用类麻醉药品和精神药品目录 (Catalogue of Non-medicinal Narcotic Drugs and Psychotropic Substances) | MPS, NHC, NMPA | issued 21 Jul 2025, in force on publication. Later changes: 16 substances from 1 Jul 2026 (not read); 奥啡类物质 (orphine-type) class, signed 18 Sep 2026, in force 1 Oct 2026 (read) | 396 entries + fentanyl, synthetic-cannabinoid and nitazene classes |
| 易制毒化学品的分类和品种目录 (precursor chemicals), annex to the 易制毒化学品管理条例 | State Council; additions by State Council letters and multi-ministry announcements | 2018 annex + additions of 2017, 2021, 2024 and 2025 read | Categories 1–3 |

The MPS text that issues the non-medicinal catalogue (read twice) says it is made up of three parts:
- 231 items from the abolished 2015 supplementary catalogue;
- 91 items split off from the 2013 narcotic catalogue;
- 74 items split off from the 2013 psychotropic catalogue (no longer divided into classes).

It also says etizolam was moved to the psychotropic catalogue, and chemical names were revised to IUPAC rules.

**Generic clauses (each read twice, identical):**
- **Medicinal narcotic catalogue.** 注1: salts and single-ingredient preparations are included. 注2: stereoisomers, esters and ethers are included. 注3: * marks "我国生产及使用的品种" (varieties produced and used in China).
- **Medicinal psychotropic catalogue.** The notes are printed only after the Class II table. 注1: salts and single-ingredient preparations. 注2: stereoisomers. 注3: the same * note.
- **Non-medicinal catalogue.** 注1: salts, stereoisomers and their salts. 注2: entries 305–396 also include their esters and ethers.
- **Class definitions.** The fentanyl-type class has four structural conditions measured against fentanyl. Its last sentence keeps fentanyls "already in 《麻醉药品品种目录》" under that catalogue (the pre-2025 name, as printed). The synthetic-cannabinoid class is a general formula with R1–R5, X, Y and Z defined; the diagram itself is not readable as text. The nitazene class has four conditions measured against etonitazene.

`medical_use` is filled only for entries in the medicinal (药用类) catalogues. It says whether the entry carries the * that note 3 defines.

## 2. Sources

| Source | URL | Version printed | Used for |
|---|---|---|---|
| Medicinal catalogues 2025 (Annexes 1–2, Announcement 2025 No. 55), in the HKSAR Trade and Industry Department's Trade Circular 659/2025 (30 Jul 2025). The copy states it is excerpted from the NMPA website. | https://www.tid.gov.hk/en/tradecircular/files/2025/ci6592025a.pdf (original https://www.nmpa.gov.cn/xxgk/ggtg/ypggtg/ypqtggtg/20250728092519123.html) | 2025 editions, dated 21 Jul 2025 | all medicinal rows, notes, announcement |
| Announcement 2025 No. 55, repost "来源：国家药品监督管理局网站" | https://yjj.sh.gov.cn/qtgzwj/20250728/80ad6017cd9d41daa4181ddb4a044c9c.html ; https://www.ccfdie.org/cn/yjxx/yphzp/webinfo/2025/07/1753824812291834.htm | posted 28–29 Jul 2025 | operative text, dates (attachments are .doc) |
| Non-medicinal catalogue 2025, TID Trade Circular 658/2025 (30 Jul 2025). The copy states it is excerpted from the MPS website. | https://www.tid.gov.hk/en/tradecircular/files/2025/ci6582025a.pdf (original https://www.mps.gov.cn/n6557558/c10150600/content.html) | issued 21 Jul 2025 | all non-medicinal rows, class definitions, notes, announcement |
| 2026 No. 58 (TID Trade Circular 598/2026; Shanghai MPA repost) | https://www.tid.gov.hk/en/tradecircular/files/2026/ci5982026a.pdf ; https://yjj.sh.gov.cn/qtgzwj/20260707/64dce663535f4569bb81419b58a680bd.html | dated 6 Jul 2026, in force 1 Oct 2026 | currency |
| Orphine-class announcement (Shanghai MPA repost from NMPA) | https://yjj.sh.gov.cn/qtgzwj/20260923/7987417abd544288bdf9b81e08921a67.html | signed 18 Sep 2026, in force 1 Oct 2026 | currency |
| State Council Decree No. 797, amending Art. 3 of the Regulations (Shanghai MPA) | https://yjj.sh.gov.cn/xzfg/20241219/f3065819ad624b08abafb65fe93624d2.html | 6 Dec 2024, in force 20 Jan 2025 | legal frame |
| 易制毒化学品管理条例 and annex (Shanghai MPA) | https://yjj.sh.gov.cn/xzfg/20220301/0e01490cc34149b28fb0538732a06362.html | Decree 445 as revised by Decree 703 (18 Sep 2018) | precursor base list |
| 国办函〔2021〕58号 (gov.cn) | https://www.gov.cn/zhengce/zhengceku/2021-06/07/content_5615890.htm | dated 28 May 2021 | GBL, Category 3 |
| 国办函〔2017〕120号 (gov.cn) | https://www.gov.cn/zhengce/zhengceku/2017-12/05/content_5244588.htm | dated 6 Nov 2017 | 1,4-butanediol check |
| Six-ministry announcement of 2 Aug 2024 (MOFCOM) | https://www.mofcom.gov.cn/zcfb/dwmygl/art/2024/art_7fff82096a874989b21b2215ec53d952.html | in force 1 Sep 2024 | CBD, Category 2 |
| Six-ministry announcement of 20 Jun 2025 (Shanghai MPA) | https://yjj.sh.gov.cn/qtgzwj/20250625/3106ce6fa2884f85be2024a33fbcde4d.html | in force 20 Jul 2025 | 1,4-butanediol check |
| NMPA/MPS/NNCC notice 2026 No. 11 (Shanghai MPA) | https://yjj.sh.gov.cn/qtgzwj/20260422/80e65f492ae049dc801b852beb18a4cd.html | signed 13 Apr 2026 | context for DXM (management only, no listing) |

**On the TID copies.** The TID is a department of the HKSAR Government. Each copy names its mainland source and URL. They are used because the mainland originals could not be read (§3). The operative texts of the medicinal announcement and of 2026 No. 58 were also read on mainland official reposts, and they agree. Whether these copies are acceptable is for the editor to decide (see §7).

## 3. How I searched, and what could not be read

- **Refused or failing.**
  - NMPA pages (three URLs): "client error".
  - NHC: client error.
  - Refused by robots.txt: www.mps.gov.cn and m.mps.gov.cn; the gov.cn search API; hunan.gov.cn; sz.gov.cn and ga.sz.gov.cn; a county police site (jaxga.jianxian.gov.cn); a Sanmenxia bureau; the nncc626.com article; the CNCSDR listing.
  - The Guangdong Emergency Management page: server error.
- **Unreadable files.** NMPA and Shanghai MPA attachments are .doc/.docx; WebFetch returns "binary data".
- **Readable.** TID PDFs; Shanghai MPA (yjj.sh.gov.cn) HTML pages; gov.cn policy-library pages; the MOFCOM page; CCFDIE.
- **Finding aids, never used for facts.** News (Xinhua, Sina, QQ, Hebei Health Commission's repost of Xinhua, and others); CIRS ChemRadar and hgt.cirs-group; Allbright Law; pharnexcloud; the Scitegrity blog; shanghaiinvest.com; cpi.ac.cn; CNCSDR (a society, not a government body).
- **Currency.**
  - Shanghai MPA's repost column was read on pages index, index_2 and index_3 (latest item 15 Oct 2026); index_1 does not exist.
  - Site searches of yjj.sh.gov.cn found the medicinal announcements 2025 No. 55, 2025 No. 110 (customs codes), 2026 No. 58 and 2026 No. 84 (customs codes), and the non-medicinal 2024 and orphine announcements.
  - No other medicinal-catalogue change was found.
  - The June 2026 non-medicinal addition was found only as a title in search results (MPS) and in news. I checked TID circulars 530–552/2026 one by one (dated 17–26 Jun 2026); none covers it.
- **The summarizer's own glosses were sometimes wrong.** For example, it glossed 溴啡 as "bromazolam", but the catalogue prints 溴啡 = Brorphine (entry 174). It also glossed 替来他明 as "tenamfetamine". Only the English names printed in the catalogues were used.

## 4. Method, and every disagreement

- **Readings.** Each chunk was read in two WebFetch calls with differently worded prompts and layouts:
  - Reading A: `n | 中文名 | 英文名 | CAS号 | 备注`.
  - Reading B, for the medicinal tables: `n ;; English ;; Chinese ;; CAS ;; remarks`.
  - Reading B, for the non-medicinal table: `n ;; English ;; CAS ;; remarks ;; Chinese`.
- **Comparison.** A Python script, run from the shell with both readings pasted inline, compared every field by entry number. No reading files were saved. Normalisation:
  - NFKC and whitespace;
  - "-", "none" and blank treated as empty;
  - cells cut by the reader ("…") compared on their common prefix;
  - differences of whitespace only reported separately.
- **Matching.** A second script searched all 524 settled rows for each of the 77 items. It used English, Chinese, abbreviation and chemical-name patterns. Every hit was checked by eye.

| Part | Rows | Chunks | Result of first comparison |
|---|---|---|---|
| Medicinal narcotic (Annex 1) | 32 | 1 | 32/32 identical |
| Medicinal psychotropic Class I | 18 | 1 | 18/18 |
| Medicinal psychotropic Class II | 78 | 2 (1–40, 41–78) | 78/78 |
| Notes to Annexes 1–2; announcement 2025 No. 55 | – | 1 | identical |
| Non-medicinal 1–50 | 50 | 1 | 50/50 |
| Non-medicinal 51–100 | 50 | 1 | 48/50 (2 disagreements) |
| Non-medicinal 101–150 | 50 | 1 | 50/50 |
| Non-medicinal 151–200 | 50 | 1 | 49/50 (1) |
| Non-medicinal 201–250 | 50 | 1 | 47/50 (3); 4 cut cells agree on prefix |
| Non-medicinal 251–305 | 55 | 1 | 53/55 (2); entries 252 and 253 whitespace only; entry 282 cut cell agrees on prefix |
| Non-medicinal 306–355 | 50 | 1 | 50/50 |
| Non-medicinal 356–396 | 41 | 1 | 41/41 |
| Class definitions and 注1–注2 | 21 sentences | 1 | identical apart from whitespace and quotation marks |
| 2026 No. 58 attachment | 3 | 1 | identical |

**Disagreements and how they were settled.** All were cells where one reading had a hyphen that the other lacked. A third reading asked about each cell specifically. None of them is in a field that decides an item's status.
1. Entry 55 (JWH-203), English: "1H-indol" (A) vs "1Hindol" (B). Third reading: "1Hindol". B.
2. Entry 60 (MDMB-FUBINACA), Chinese: "吲唑-3-甲酰胺" vs "吲唑3-甲酰胺". Third: "吲唑3". B.
3. Entry 199 (DMXE), English ending: "cyclohexanone" (A) vs "cyclohexan-1-one" (B). Third: "cyclohexanone". A.
4. Entry 231 (hexahydrocannabinol), English: "chromen-1-ol" vs "chromen1-ol". Third: "chromen1-ol". B.
5. Entry 245 (DMHP), Chinese: "6H-苯并" vs "6H苯并". Third: "6H苯并". B.
6. Entry 246 (Δ9-THC, an item), English: "chromen-1-ol" vs "chromen1-ol". Third: "chromen1-ol". B. Recorded "as in the text layer" in the JSON.
7. Entry 262 (JWH-250), English: "pentyl-1H" vs "pentyl1H". Third: "pentyl1H". B.
8. Entry 264 (MDMA, an item), English: "-N-methylpropan" vs "-Nmethylpropan". Third: "-Nmethylpropan". B. Recorded "as in the text layer".

Other points:
- **Source typos kept as printed.** Entry 11 (2C-T-7) prints "dimethox-phenethylamine". Entries 319/320 print English names that look swapped against their abbreviations. Neither entry 319 nor 320 is an item.
- **Orphine announcement date.** Both readings of the Shanghai MPA copy give a signature date of 18 Sep 2026. A non-official repost (CNCSDR) gives 23 Sep, which is the posting date.
- **2025 precursor announcement.** Neither reading finds a category stated for 4-piperidone or 1-Boc-4-piperidone. This does not affect any item.

## 5. Matching: false positives discarded

- 2C-B-NBOMe, 2C-I-NBOMe and 2C-C-NBOMe (for 2C-B, 2C-I and 2C-C).
- 2C-T-4 (for 2C-T-7).
- 5-MeO-DMT and 4-AcO-DMT (for DMT).
- Fludiazepam, flualprazolam, delorazepam and flubromazepam (for diazepam, alprazolam, lorazepam and bromazepam).
- Ethcathinone, methcathinone and ethchlorvynol (substring "THC").
- 6-Br-MDMA and 6-Cl-MDMA (MDMA).
- MMDA, N-hydroxy MDA, MDAI and dimdazenil (MDA).
- 1P-, 1V- and 1cP-LSD (LSD).
- THF-F (furanylfentanyl).
- NENK and 2-FDCK (ketamine).
- Isomethadone, the methadone intermediate and normethadone (methadone).
- Thebacon (hydrocodone).
- Dihydrocodeine, acetyldihydrocodeine, nicocodine and norcodeine (codeine).
- FUB-JWH-018 (JWH-018).
- EAM-2201 and MAM-2201 (AM-2201).
- 5F-ADBICA, 5F-AMB, 5F-AB-PINACA, 5F-APINACA and PX-2 (5F-ADB).
- Valiloxybate (GHB pattern "oxybate").
- N-ethylpentylone, 4-MEAPP, 4-Cl-EAPP and amineptine (NEP).
- Ring-substituted α-PVPs (α-PVP).
- The many "苯丙胺" and "卡西酮" substring hits.

Items found by printed name or abbreviation without the site's INN:
- 5F-MDMB-PINACA appears as "5F-ADB" (entry 149).
- Mephedrone appears as "4-MMC".
- 4-CMC and 4-BMC appear without "clephedrone" or "brephedrone".
- Heroin appears without "diacetylmorphine".
- MDA appears without "tenamfetamine".

## 6. Results

**Listed, 67 rows (ai-checked):**
- **Medicinal narcotic catalogue (8), all marked \*:**
  - fentanyl (13), sufentanil (29), remifentanil (28);
  - methadone (17);
  - morphine (18), oxycodone (21), hydrocodone (14), codeine (5).
  - Compound oral preparations of oxycodone and hydrocodone are psychotropic Class I or II depending on the dose per unit. Codeine compound oral liquids are Class II (75).
- **Medicinal psychotropic Class I (7):** amfetamine (2\*), dexamfetamine (5), buprenorphine (4\*), GHB (6\*), ketamine (7\*), methylphenidate (11\*), tapentadol (14\*).
- **Medicinal psychotropic Class II (9):** diazepam (24\*), alprazolam (2\*), clonazepam (17\*), lorazepam (39\*), bromazepam (5), etizolam (30), dextromethorphan (22\*), tramadol (68\*), cathine (13).
- **Non-medicinal catalogue (41):**
  - phenethylamines and tryptamines: 2C-B 234, 2C-I 241, 2C-E 6, 2C-C 2, 2C-T-7 11; 5-MeO-DMT 97; DMT 244; mescaline 257;
  - benzodiazepines: flualprazolam 169, flubromazolam 171;
  - cannabis 325, Δ9-THC/dronabinol 246;
  - cocaine 328, coca leaf 327; heroin 347;
  - carfentanil 118, acetylfentanyl 107, furanylfentanyl 119;
  - kratom (Mitragyna speciosa) 214, mitragynine 215, 7-hydroxymitragynine 216;
  - LSD 255; MDMA 264, MDA 280, MDEA 271; methamphetamine 259; PCP 274;
  - psilocybin 278, psilocin 277;
  - synthetic cannabinoids: JWH-018 273, AM-2201 253, 5F-ADB 149;
  - cathinones: cathinone 237, mephedrone 268, MDPV 266, α-PVP 91, 3-MMC 71, 3-CMC 69, 4-CMC 73, 2-MMC 67, 4-BMC 72.
- **Precursor list (2):** CBD, Category 2 (from 1 Sep 2024); GBL, Category 3 (国办函〔2021〕58号).

**Not named, possibly covered (3, draft):**
- esketamine, through the stereoisomer clause;
- MDMB-4en-PINACA and ADB-BUTINACA, through the synthetic-cannabinoid class.

**Not found in the lists read (5):**
- lisdexamfetamine, 1,4-butanediol, Salvia divinorum and salvinorin A (ai-checked);
- NEP (draft, see §7).

The "if named" items ayahuasca and peyote/San Pedro have no row.

**Points a reader may not expect:**
- Dronabinol, cannabis, cocaine, heroin, LSD, MDMA and psilocybin are all in the non-medicinal catalogue.
- GHB, ketamine, methylphenidate, buprenorphine, tapentadol and amfetamine are medicinal Class I psychotropics.
- Dextromethorphan, etizolam and cathine are Class II.
- The kratom plant itself is an entry.
- CBD is controlled only as a Category 2 precursor chemical.

## 7. Unsettled (for the editor)

1. **TID copies.**
   - The tables were read in HKSAR TID reproductions of the NMPA and MPS pages, because the mainland originals could not be fetched.
   - Decide whether these copies are acceptable, or check them against the originals in a browser.
2. **June 2026 addition of 16 substances (in force 1 Jul 2026).**
   - Not read from any official source. The MPS page is https://www.mps.gov.cn/n6557558/c10498264/content.html.
   - Non-official leads say it includes NEP (2-乙氨基-1-苯基-1-戊酮). NEP is recorded as not found, as draft.
   - Read the announcement in a browser, and update NEP and, if needed, the other not-found items.
3. **Esketamine (draft).**
   - It is not named.
   - The stereoisomer note is printed after the Class II table, and it is the reader's application to treat it as covering ketamine (Class I).
4. **MDMB-4en-PINACA and ADB-BUTINACA (draft).**
   - Neither is named.
   - Whether they fit the synthetic-cannabinoid general formula needs a chemist, because the formula diagram could not be read.
5. **Lisdexamfetamine.** It is not named. The printed clauses (salts, single-ingredient preparations, stereoisomers) do not reach it. Decide how to present it.
6. **Precursor list.**
   - No official consolidated current list was found.
   - The 2012 and 2014 additions and the MPS implementing announcement for the 2021 additions were not read, so GBL's effective date is not established.
7. **Currency.**
   - China publishes no consolidated "current to" page.
   - Currency rests on the Shanghai MPA repost column and on searches, as of 17 Oct 2026.
8. **The fentanyl-class sentence** cites 《麻醉药品品种目录》, the pre-2025 name, as printed.
