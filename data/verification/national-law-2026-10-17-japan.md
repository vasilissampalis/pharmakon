# W2 report: Japan

Checked on 2026-10-17 by AI reader W2, using WebSearch and WebFetch only (no browser, no shell downloads).

Output: `/home/claude/drug-encyclopedia/data/legal/_incoming/japan.json`. It has 75 rows under the 25 drug-page keys. The two "if named" items (ayahuasca; peyote/San Pedro) are not named in any list, so they have no row.

## 1. The lists

Japan has no single schedule. Four regimes list substances, all on e-Gov (the government's consolidated law database run by the Digital Agency):

| Regime | Where the substances are listed | Size read |
|---|---|---|
| 麻薬 (narcotics) | 麻薬及び向精神薬取締法 (Act No. 14 of 1953) Art. 2(1)(i): 麻薬 = 別表第一 + 大麻. 別表第一 item 77 hands further designation to Cabinet Order No. 238 of 1990, Art. 1. Art. 2(2) and Cabinet Order Art. 6 deem THC acids narcotics. | 別表第一 78 items; Cabinet Order Art. 1, 171 items; Art. 6, 2 items |
| 麻薬原料植物 (narcotic raw-material plants) | 別表第二, and Cabinet Order Art. 3 | 4 + 2 (psilocybin and psilocin mushrooms) |
| 向精神薬 (psychotropics) | 別表第三, and Cabinet Order Art. 4 (designated under 別表第三 item 11). Classes come from Act Art. 50-9: 第一種 (Class I) = Enforcement Order Art. 3; 第二種 (Class II) = Enforcement Order Art. 4; 第三種 (Class III) = every other psychotropic. | 12 + 80; Class I 9 items, Class II 10 items |
| 麻薬向精神薬原料 (raw materials) | 別表第四, and Cabinet Order Art. 5 | 10 + 26 |
| 覚醒剤 (stimulants) and 覚醒剤原料 (stimulant raw materials) | 覚醒剤取締法 (Act No. 252 of 1951) Art. 2(1) and 別表; 覚醒剤原料を指定する政令 (Cabinet Order No. 23 of 1996) | Art. 2(1) items i-iii; 別表 9; order 14 |
| 大麻 (cannabis) | Defined in 大麻草の栽培の規制に関する法律 Art. 2(1)-(2). This is the former 大麻取締法. The Narcotics Act makes cannabis a narcotic. | 2 definitions |
| 指定薬物 (designated substances) | PMD Act Art. 2(15). The definition excludes stimulants, narcotics, psychotropics, opium and poppy straw. The list itself is MHLW Ordinance No. 14 of 2007, Art. 1. | 366 items. Items 360-365 are generic (包括指定) designations; item 366 covers products, with Salvia divinorum and Mitragyna speciosa named in its proviso. |

**Generic clauses (each read twice; the readings were identical):**
- **Salts.** Almost every entry ends 及びその塩類 ("and its salts"). Some entries add esters or ethers (e.g. 別表第一 items 6, 15, 16, 22).
- **Isomers.** There is no general isomer clause. Particular isomers are excluded by name instead:
  - 右旋性のものを除く (dextrorotatory form excluded): 別表第一 items 50, 55, 56 and 71. Item 71 is what keeps dextromethorphan out.
  - 左旋性のものを除く (levorotatory form excluded): the cathine entry (Cabinet Order Art. 4 item 62; Enforcement Order Art. 4 item 7).
- **別表第一 item 78.** Anything containing items 1-77 or cannabis is a narcotic, with four exceptions:
  - イ: preparations with 1% or less of codeine or dihydrocodeine (千分中十分以下). Act Art. 2(1)(v) calls these 家庭麻薬 (household narcotics).
  - ロ: products not in plant form whose Δ9-THC is at or below the Cabinet Order Art. 2 limits: 10 ppm for oils and powders, 0.1 ppm for aqueous solutions, 1 ppm for others.
  - ハ: seed and mature-stalk products containing items 42-43, unless THC was added artificially.
  - ニ: plants other than 麻薬原料植物 and 大麻草.
- **別表第三 item 12.** Anything containing a psychotropic is a psychotropic.
- **Designated-substance generic items.**
  - 360-361: naphthoylindoles.
  - 362: cathinones. Its three-column table is set out under item 362 in §6.
  - 363-365: THC, Δ8-THC and HHC homologues with C3-C8 side chains.
  - Each excludes narcotics. 360-362 also exclude stimulants and psychotropics.
  - 366: products containing items 1-365. Plants are excluded, except Salvia divinorum and Mitragyna speciosa in forms "immediately usable on the human body".

`medical_use` is null in every row. None of these lists states a medical use for an entry.

## 2. Sources

All e-Gov texts were read through the e-Gov Law API v2 (XML). The revision ID e-Gov prints is the version record.

| Source | URL read | Version printed |
|---|---|---|
| 麻薬及び向精神薬取締法: Art. 2, Art. 50-9, 別表第一-第四 | https://laws.e-gov.go.jp/api/2/law_data/328AC0000000014 (elm=AppdxTable, AppdxTable[2], [3], [4], MainProvision-Article_2, MainProvision-Article_50_9) | 328AC0000000014_20261001_507AC0000000087. Amended by 令和七年法律第八十七号, in force 1 Oct 2026, CurrentEnforced. Later amendments are promulgated for 1 Mar 2027 and 20 May 2027 (UnEnforced, not read). |
| Cabinet Order No. 238 of 1990 (麻薬、麻薬原料植物、向精神薬、麻薬向精神薬原料等を指定する政令), Arts 1-6 | https://laws.e-gov.go.jp/api/2/law_data/402CO0000000238 (elm=MainProvision-Article_1 … _6) | 402CO0000000238_20260906_508CO0000000258. Amended by 令和八年政令第二百五十八号 (promulgated 7 Aug 2026), in force 6 Sep 2026. No later revision is listed. |
| 麻薬及び向精神薬取締法施行令, Arts 3-4 | https://laws.e-gov.go.jp/api/2/law_data/328CO0000000057 (elm=MainProvision-Article_3, _4) | 328CO0000000057_20260408_508CO0000000130 (in force 8 Apr 2026) |
| 覚醒剤取締法, Art. 2 and 別表 | https://laws.e-gov.go.jp/api/2/law_data/326AC0100000252 (elm=MainProvision-Article_2; AppdxTable) | 326AC0100000252_20250601_504AC0000000068 (in force 1 Jun 2025). No later revision is listed. |
| 覚醒剤原料を指定する政令 | https://laws.e-gov.go.jp/api/2/law_data/408CO0000000023 | 408CO0000000023_20240830_506CO0000000258 (in force 30 Aug 2024) |
| 大麻草の栽培の規制に関する法律, Art. 2 | https://laws.e-gov.go.jp/api/2/law_data/323AC0000000124 (elm=MainProvision-Article_2) | 323AC0000000124_20250601_504AC0000000068 (in force 1 Jun 2025) |
| PMD Act (医薬品医療機器等法), Art. 2(15) | https://laws.e-gov.go.jp/api/2/law_data/335AC0000000145 (elm=MainProvision-Article_2-Paragraph_15) | 335AC0000000145_20260521_505AC0000000063 (in force 21 May 2026) |
| MHLW Ordinance No. 14 of 2007 (指定薬物省令), Art. 1 | https://laws.e-gov.go.jp/api/2/law_data/419M60000100014 (items 1-250 via elm=MainProvision-Article_1; items 251-366 via elm=…-Paragraph_1-Item_n, one per call) | 419M60000100014_20260906_508M60000100135. Amended by 令和八年厚生労働省令第百三十五号 (promulgated 27 Aug 2026), in force 6 Sep 2026. |
| MHLW 指定薬物一覧 (designated-substance list with 通称等, the common names) | https://www.mhlw.go.jp/content/11120000/001743040.pdf | No date printed. Cut off at 省令番号 318 in WebFetch. Used only for common names (rows 75, 110, 120, 290, 291). |
| MHLW notice of 30 Aug 2023 (seven substances moved from 指定薬物 to 麻薬 from 29 Sep 2023) | https://www.yakubutsu.mhlw.go.jp/social/2023/20230830.html | Read once. Confirms the names ADB-BUTINACA and 3-MMC. |
| MHLW news list; notice of 7 Aug 2026 (three substances made narcotics from 6 Sep 2026) | https://www.yakubutsu.mhlw.go.jp/social/index.html ; https://www.yakubutsu.mhlw.go.jp/social/2026/20260807.html | Latest item 13 Oct 2026. Read once, for currency only. |

## 3. How I searched

- **Finding the texts.**
  - MHLW's 関係法令 page (https://www.mhlw.go.jp/seisakunitsuite/bunya/kenkou_iryou/iyakuhin/yakubutsuranyou_taisaku/hourei/index.html) links each Act to e-Gov.
  - The e-Gov viewer (laws.e-gov.go.jp/document?lawid=…) is a JavaScript page; WebFetch got only its header.
  - So I used the e-Gov Law API, whose documentation (laws.e-gov.go.jp/docs/…/law-api-v1) was found by WebSearch:
    - law IDs came from the v2 title search (`/api/2/laws?law_title=…`);
    - revision histories from `/api/2/law_revisions/{id}`;
    - single articles, tables and items from the `elm` parameter.
- **Two limits of WebFetch shaped the method.**
  - **Page cap.** A page is cut off at about 67,500 characters:
    - the whole-law XML of the Act stops around Art. 24;
    - the designated-substance ordinance stops at item 250 (item 256 without `elm`);
    - so items 251-366 were read one item per call, two calls per item.
  - **Quotation limit.** The summarizing model refused or paraphrased long verbatim passages (it cites a 125-character limit). I then asked for labelled fragments or a different layout. A paraphrase was never used as a reading.
- **Currency.**
  - e-Gov marks every instrument read as CurrentEnforced.
  - MHLW's drug-control news list (latest item 13 Oct 2026) shows no designation after the notices of 7 Aug 2026 (narcotics, from 6 Sep 2026) and 18 Aug 2026 (designated substances, from 28 Aug 2026). Both are already in the e-Gov texts read.
- **Two MHLW designated-substance PDFs.**
  - 001739360.pdf is linked from MHLW's drug site as "令和８年８月18日現在" (as of 18 Aug 2026). Its row numbers differ from the current e-Gov text: its 75 is EDMB-PINACA, which is e-Gov item 74.
  - 001743040.pdf matches the current e-Gov numbering for every row checked. I used it, for common names only.
- **Finding aids, never used for facts.**
  - Search results only (not read): sn-hoki.co.jp (a legal publisher), japaneselawtranslation.go.jp (MOJ translations, not current), and prefectural and municipal PDFs.
  - Read only for the e-Gov API syntax: a Qiita article and a jsDelivr type file.
- **Not read.**
  - あへん法 (the Opium Act); no item is opium itself.
  - Enforcement Order Art. 7 (psychotropic preparations exempt from some provisions).
  - The MHLW designation of mushrooms excluded from Cabinet Order Art. 3.
  - The rest of the Enforcement Regulations (麻薬及び向精神薬取締法施行規則). Its table of contents and Arts 1-24 show only procedural provisions.
  - The two future amendments to the Act.

## 4. Method, and every disagreement

- **Readings.** Each chunk was read in two WebFetch calls with different prompts and layouts:
  - reading A: `number<TAB>text`;
  - reading B: a JSON object, a Markdown table, `n :: text`, or fragment lists;
  - per-item reads of designated substances 251-366: A in `Num<TAB>text`, B as JSON `{"num","name"}`.
- **Comparison.** A Python script, run from the shell with both readings pasted inline, compared every entry by number. No reading files were saved. Normalisation:
  - NFKC;
  - whitespace ignored;
  - surrounding quote marks stripped.
- **Matching.** A second script searched every settled row for each of the 77 items. It used normalised Japanese patterns: kanji numerals turned into digits, ― into -, ・ into a comma. Patterns covered 別名 aliases, katakana INNs and chemical-name fragments. Every hit was checked by eye.
- **Final check.** All 63 printed entry texts in the JSON were compared again by script with the settled readings: no mismatch.

| Part | Rows | Chunks | Result |
|---|---|---|---|
| Act 別表第一, items 1-77 | 77 | 1 | 77/77 identical. Item 30: B added column marks [第1欄]/[第2欄]; equal once removed. |
| Act 別表第一, item 78 and イ-ニ | 5 strings | 1 | A refused verbatim (paraphrase). A third reading (JSON) was compared with B: identical. |
| Act 別表第二, 第三, 第四 | 4 / 12 / 10 | 1 each | identical |
| Act Art. 2(1) (7 definitions) and Art. 2(2) | 8 | 1 | identical (B ran term and definition together) |
| Act Art. 50-9 | 3 defining phrases | 1 | A gave only the defining phrases (quotation limit); the script found them verbatim in B's paragraphs |
| Cabinet Order Art. 1 | 171 | 3 (1-60, 61-120, 121-171) | 171/171 identical |
| Cabinet Order Art. 2 | 4 strings | 1 | identical once B's split items were joined |
| Cabinet Order Arts 3, 5, 6 | 3 / 27 / 3 | 1 each | identical |
| Cabinet Order Art. 4 | 80 | 2 (1-40, 41-80) | 80/80 identical |
| Enforcement Order Arts 3-4 | 10 / 11 | 1 each | identical |
| 覚醒剤取締法 Art. 2 | 5 strings | 1 | Both first readings refused verbatim (paraphrases). Two more readings with short-string prompts: identical. |
| 覚醒剤取締法 別表 | 9 | 1 | identical |
| 覚醒剤原料を指定する政令 | 15 | 1 | identical |
| 大麻草の栽培の規制に関する法律 Art. 2(1)-(2) | 2 | 1 | identical |
| PMD Act Art. 2(15) | 4 fragments | 1 | identical once joined |
| Designated substances 1-50 | 50 | 1 | B (JSON) refused; re-read as a Markdown table: 50/50 |
| Designated substances 51-100 | 50 | 1 | 50/50 (B numbered rows in kanji; converted by script) |
| Designated substances 101-150 | 50 | 1 | 50/50 |
| Designated substances 151-200 | 50 | 1 | 50/50 (B numbered rows 1-50; offset by 150; all 50 aligned) |
| Designated substances 201-250 | 50 | 1 | 50/50 |
| Designated substances 251-359 | 109 | one item per call | 109/109. Item 358: A printed an ASCII "("; width only. |
| Designated substances 360-366 (generic items) | 7 items in parts | per item | All identical. Item 360's proviso and table were read twice more. Item 362's JSON reading refused, and was re-read as fragments. |
| MHLW 指定薬物一覧, rows 75, 110, 120, 290, 291 | 5 | 1 | identical in common name and designation date |

**Disagreements.** None. Every difference between readings was one of format: quote marks, row numbering, splits, column marks, character width. No third reading was needed to settle content. Third readings were taken only to replace refusals and paraphrases, as listed above.

## 5. Matching: false positives discarded

| Pattern | Discarded hits |
|---|---|
| Fentanyl | alfentanil, thiofentanyl, β-hydroxy- and 3-methyl-fentanyls, crotonyl-, valeryl- and para-fluorofentanyl, α-methylfentanyls (Cabinet Order Art. 1 items 21, 70, 87, 88, 101, 104, 114, 136, 137, 145-147) |
| Acetylfentanyl | methoxyacetyl analogues (items 113, 164) |
| Furanylfentanyl | the tetrahydrofuran analogue (item 100) |
| 2C-B | the NBOMe (118), DOB (120) and bk-2C-B, NBF and NBOH types (designated items 41, 260, 261) |
| 2C-C | DOC (Cabinet Order item 31) and NBOMe/NBOH types (Cabinet Order item 32; designated items 111-113) |
| 2C-E | the NBOMe and NBOH types (designated items 76-77) |
| 2C-I | NBOMe (170), DOI (designated 353) and other N-benzyl types (247, 354, 355) |
| 2C-T-7 | the 4-isopropylthio phenethylamine (Cabinet Order item 65) and the amphetamine (designated item 52) |
| DMT and 5-MeO-DMT | 4-AcO-DMT, Boc-DMT, 4-PrO-DMT and 5-MeO-2-Me-DMT (designated items 13, 166, 259, 348); 5-MeO-DIPT (Cabinet Order item 42) |
| MDA and MDEA | N-hydroxy MDA and MMDA (items 159, 168) |
| Amfetamine | DOET, DMA, TMA-2, TMA, PMA and DOB ("α-methylphenethylamine" fragment) |
| Cathinone and mephedrone | methcathinone (128); 3-methoxy analogue (designated item 347) |
| α-PVP and MDPV | the 4-methyl-pentanone analogues (Cabinet Order item 143; designated item 320) |
| ADB-BUTINACA | the APP and 5-bromo analogues (designated items 27, 34) |
| MDMB-4en-PINACA | the amide (designated 38) and the indole MMB-4en (designated 318) |
| 5F-MDMB-PINACA | MDMB-CHMICA, 4F-MDMB-BINACA, MDMB-FUBINACA and 5F-MDMB-PICA (Cabinet Order items 134, 149, 150, 154) |
| THC | DMHP and other THC isomers and homologues (Cabinet Order items 63, 76-79, 122-124) |
| Morphine and codeine | acetorphine and etorphine (Cabinet Order items 1, 55); dihydrocodeine and nicocodine (別表第一 items 23, 46) |
| Methadone | the methadone intermediate, normethadone and isomethadone (別表第一 items 18, 32, 38) |
| Mitragynine | 7-hydroxymitragynine (designated 290), which shares the skeleton |

Items found only under a printed chemical name, without the site's name (MHLW confirmation where found):
- 2C-B, 2C-I, 2C-T-7.
- amfetamine and methamphetamine (フエニル(メチル)アミノプロパン); lisdexamfetamine.
- flualprazolam, flubromazolam.
- carfentanil, acetylfentanyl, furanylfentanyl.
- JWH-018, AM-2201, 5F-MDMB-PINACA, MDMB-4en-PINACA, ADB-BUTINACA (MHLW 2023 notice).
- cathinone, cathine, mephedrone, MDPV, α-PVP, 3-MMC (MHLW 2023 notice), 3-CMC.
- 2C-E, 2C-C, mitragynine and 7-hydroxymitragynine (MHLW 指定薬物一覧 通称等).

## 6. Results

**Listed, 65 rows (ai-checked):**
- **覚醒剤 (stimulants), 覚醒剤取締法 Art. 2(1)(i):** amfetamine and methamphetamine.
- **覚醒剤原料 (stimulant raw material):** lisdexamfetamine, 覚醒剤原料を指定する政令 item 4.
- **麻薬 (narcotics), 別表第一:**
  - cocaine 13, coca leaf 14;
  - codeine 15, heroin 16, hydrocodone 22, oxycodone 25, methadone 36, morphine 72;
  - Δ9-THC 42.
- **麻薬 by definition:** cannabis (Act Art. 2(1)(i) with the cultivation act Art. 2(2)); resin not named.
- **麻薬, Cabinet Order Art. 1:**
  - phenethylamines and tryptamines: 2C-B 119, 2C-I 169, 2C-T-7 67; DMT 58; psilocybin 59, psilocin 60; mescaline 82;
  - MDMA 64, MDA 158, MDEA 25; LSD 171; PCP 91; ketamine 34; GHB 90;
  - fentanyl 96, carfentanil 148, acetylfentanyl 98, furanylfentanyl 103, sufentanil 166, remifentanil 161, tapentadol 61;
  - synthetic cannabinoids: JWH-018 85, AM-2201 116, 5F-MDMB-PINACA 152, MDMB-4en-PINACA 135, ADB-BUTINACA 4;
  - cathinones: cathinone 7, mephedrone 131, MDPV 160, α-PVP 95, 3-MMC 130, 3-CMC 35, 4-CMC 36.
- **向精神薬 (psychotropics):**
  - methylphenidate, 別表第三 item 9 (Class I);
  - buprenorphine, Cabinet Order Art. 4 item 50 (Class II);
  - cathine, item 62 (Class II);
  - Class III: diazepam (別表第三 item 3), alprazolam 45, clonazepam 34, lorazepam 13, bromazepam 68, etizolam 32, flualprazolam 43, flubromazolam 70.
- **指定薬物 (designated substances), MHLW Ordinance No. 14 of 2007 Art. 1:**
  - 2C-E 75, 2C-C 110, 5-MeO-DMT 332;
  - salvinorin A 120, mitragynine 291, 7-hydroxymitragynine 290;
  - Salvia divinorum and Mitragyna speciosa, named in the proviso of item 366.

**Not named, possibly covered (5, draft):**
- **Dexamfetamine and esketamine.** There is no isomer clause, so cover depends on reading the unqualified names to include their enantiomers.
- **NEP, 2-MMC and 4-BMC.** These fall under generic designated-substance item 362 on a structural reading. The base is 2-amino-1-phenylpropan-1-one (cathinone), and each entity may carry one substituent from each column of the table:

| Position | Substituent allowed (one) |
|---|---|
| amino group at C2 | unchanged, or replaced by methyl-, ethyl-, dimethyl-, diethyl- or methylethylamino or 1-pyrrolidinyl |
| C3 | hydrogen, or a straight-chain C1-C7 alkyl |
| benzene ring | none, or methyl, ethyl, methoxy, methylenedioxy, F, Cl, Br or I at position 2, 3 or 4 |

- How each fits:
  - NEP: ethylamino, with ethyl on C3.
  - 2-MMC: methylamino, with 2-methyl on the ring.
  - 4-BMC: methylamino, with 4-bromo on the ring.

**Not found in the lists read (5, ai-checked):**
- **CBD.**
- **Dextromethorphan.** 別表第一 item 71 lists 3-methoxy-N-methylmorphinan but excludes the dextrorotatory form.
- **GBL and 1,4-butanediol.** Not on the raw-material lists either.
- **Tramadol.** Its O-desmethyl metabolite is designated item 165 (by chemical name).

**No row:** ayahuasca and peyote/San Pedro are not named. 別表第一 item 78ニ excludes undesignated plants from "substances containing narcotics".

**Points a reader may not expect:**
- Several items are 指定薬物 under the PMD Act, not narcotics: 5-MeO-DMT, 2C-E, 2C-C, salvinorin A, mitragynine and 7-hydroxymitragynine. Kratom and Salvia divinorum are too, but only in ready-to-use form.
- GHB and ketamine are narcotics.
- Buprenorphine and cathine are Class II psychotropics, and methylphenidate is Class I.
- Lisdexamfetamine is a stimulant raw material, not a stimulant.
- Codeine preparations of 1% or less are exempt as 家庭麻薬.
- THC limits: products not in plant form are narcotics only above 10 ppm (oils and powders), 0.1 ppm (aqueous) or 1 ppm (others) Δ9-THC.

## 7. Unsettled (for the editor)

1. **Generic cathinone designation (draft): NEP, 2-MMC and 4-BMC.**
   - None is named.
   - Cover rests on a structural reading of item 362's printed table.
   - A chemist should confirm.
2. **Esketamine and dexamfetamine (draft).**
   - Neither is named, and no isomer clause is printed.
   - Other entries exclude particular isomers by name, which suggests unqualified names cover all isomers. That is an inference.
   - Decide how to present them.
3. **Cannabis resin.**
   - Not named. A product without plant form falls outside 大麻.
   - It is a narcotic only through its Δ9-THC content (別表第一 items 78 and 42) above the Cabinet Order Art. 2 limits.
   - The row is ai-checked for cannabis itself; the resin point is the reader's application.
4. **Identification by chemical name.**
   - 23 listed items appear only under chemical names; see §5.
   - MHLW pages confirm six of them; the rest were matched by eye. A chemist may want to spot-check.
5. **Not read.** The Opium Act; Enforcement Order Art. 7; the MHLW mushroom designation under Cabinet Order Art. 3; the rest of the Enforcement Regulations; the two 2027 amendments to the Act.
6. **medical_use** is null throughout. The designated-substance ordinance (Art. 2) lists permitted uses only in general, and MHLW's list prints 医療等の用途区分 codes without a key.
7. **Currency.**
   - There is no single "current to" page; the e-Gov revision IDs are the version record.
   - MHLW news shows no designation after 18 Aug 2026 (checked 17 Oct 2026).
   - MHLW's drug site still links the older list PDF (001739360.pdf, "as of 18 Aug 2026"). Its numbering differs from the current e-Gov text.
