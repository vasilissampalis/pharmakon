# W2 report: Iran (Islamic Republic of)

Checked on 2026-10-17 by AI reader W2, using WebSearch and WebFetch only (no browser, no shell downloads).

- **Output:** `/home/claude/drug-encyclopedia/data/legal/_incoming/iran.json`.
- **Records:** 75 rows under the 25 drug-page keys. All 75 are **draft**.
  - 7 rows are named in the law text: cannabis, coca leaf, cocaine, heroin, morphine, codeine and methadone.
  - 68 rows are "Not found in the lists read".
  - The two "if named" items (ayahuasca; peyote or San Pedro) are not named, so they have no row. They are in `not_found` with the 68.
- **The main limit.** The official current lists could not be read. Iran's law defines "narcotic" by pointing to a 1338 Cabinet list (as amended) and to Ministry of Health announcements. WebFetch refused every official host that carries those lists or the current consolidated law.
- **What was read.** The only readable text is the Anti-Narcotics Law as amended in 1376 (1997). It was read on FAOLEX, the UN Food and Agriculture Organization's legal database, which holds a 2016 print of the dastour.ir legislation portal page.
- **How the gap is recorded.** As instructed for Iran, every item the law text does not name is recorded as "Not found in the lists read". Each such row says which lists were searched and which could not be read. **These rows do not show that an item is uncontrolled in Iran.**

## 1. How Iran lists controlled substances (as far as could be read)

The 1376 text of the law has no schedule. It works in two ways:
- it names a few substances and plants in its offence articles;
- it defines "narcotic" by pointing to outside lists.

**The definition (Art. 1, note).**
- Art. 1 opens «اعمال زير جرم است» (the following acts are crimes). Its note (تبصره) defines narcotics for the whole law.
- Narcotics are the substances listed in «تصويب نامه راجع به فهرست مواد مخدر مصوب ۱۳۳۸ و اصلاحات بعدي آن». Gloss: the Cabinet resolution on the list of narcotic substances, approved 1338 (1959), and its later amendments.
- They are also any substance that is «توسط وزارت بهداشت، درمان و آموزش پزشكي به عنوان مخدر شناخته و اعلام ميگردد». Gloss: recognised and announced as narcotic by the Ministry of Health, Treatment and Medical Education.
- So the decisive lists are outside the law. Neither could be read (section 4).

**Substances the 1376 text names.** Each was read twice; the readings agree after settling (section 6).

| Article | Names as printed | Gloss |
|---|---|---|
| 1, item 1 | «كشت خشخاش و كوكا مطلقًا و كشت شاهدانه به منظور توليد مواد مخدر» | cultivation of poppy and coca, absolutely, and of cannabis for producing narcotics |
| 2, 24 | خشخاش، كوكا، شاهدانه | poppy, coca, cannabis (plants) |
| 3 | «بذر يا گرز خشخاش يا بذر يا برگ كوكا و يا بذر شاهدانه» | poppy seed or capsule, coca seed or leaf, cannabis seed (covers keeping, hiding or carrying them) |
| 4 | «هركس بنگ، چرس، ترياك، شيره، سوخته و يا تفاله ترياك را» | bhang, charas, opium, opium sap, burnt opium, opium residue |
| 5 | ترياك | opium |
| 8 | «هركس هروئين، مرفين، كوكائين، و ديگر مشتقات شيميائي مرفين و كوكائين را» | heroin, morphine, cocaine and other chemical derivatives of morphine and cocaine |
| 40 (added) | انيدريد استيك، اسيد انتر اتيليك، اسيد فنيل استيك، كلرور استيل، plus the other substances in Tables I and II annexed to Art. 12 of the 1988 UN Convention | acetic anhydride, an acid printed «اسيد انتر اتيليك» (probably anthranilic acid; the reader's gloss), phenylacetic acid, acetyl chloride |
| 40 (added) | «همچنين نسبت به ورود، خريد، فروش، ساخت، مصرف، نگهداري يا صدور كدئين و متادون» | and also the import, purchase, sale, manufacture, use, keeping or export of codeine and methadone |

**Generic clauses** (each read twice):
- **Art. 1 note:** the definition by reference, above. It decides the answer for almost every item, and its lists were not read.
- **Art. 8:** «و ديگر مشتقات شيميائي مرفين و كوكائين» (and other chemical derivatives of morphine and cocaine). Whether this reaches oxycodone, hydrocodone or buprenorphine is not stated. Those three are recorded as not found, with a note.
- **Art. 40:** "and the other substances in Tables I and II annexed to Art. 12 of the 1988 Convention and its later amendments". No site item is a precursor of that kind.

**Other provisions:**
- **Art. 40's opening:** «هركس عالمًا عامداً به قصد تبديل يا توليد مواد مخدر» (anyone who knowingly and deliberately, to convert or produce narcotics). Whether this intent also governs the codeine and methadone clause is a penal question outside the brief. The rows record only that both are named.
- **Art. 41:** exempts making, trade, keeping, import, export, use and carriage of «مواد ممنوع» (prohibited substances), as the case may be, «براي مصارف پزشكي، تحقيقاتي و صنعتي» (for medical, research and industrial uses), with a Ministry of Health permit. This is general, so `medical_use` is null in every row.

**Words that do not occur in the 1376 text.** One check of 22 terms found none of these, and neither names reading lists them:
- cannabis terms: حشيش (hashish), گراس (grass);
- named drugs: LSD, amphetamine, methamphetamine, ecstasy, ketamine, tramadol, buprenorphine, mescaline, psilocybin;
- street and general terms: crack, شيشه (crystal), قرص (pill).

**The original 1367 text** (FAOLEX, read once, superseded, no row rests on it). Its Art. 8 named codeine, methadone, «عصاره شيميايي حشيش» (chemical extract of hashish) and «روغن حشيش» (hashish oil) beside heroin, morphine and cocaine. In the 1376 text, Art. 8 names only heroin, morphine and cocaine, and codeine and methadone appear in the added Art. 40.

## 2. Sources read

| # | Text | URL | Version printed | Host | Readings |
|---|---|---|---|---|---|
| 1 | قانون اصلاح قانون مبارزه با مواد مخدر و الحاق موادي به آن مصوب ۳/۸/۱۳۶۷ مجمع تشخيص مصلحت نظام (Law amending the Anti-Narcotics Law of 3/8/1367 and adding articles to it), Expediency Council | https://faolex.fao.org/docs/pdf/ira167838.pdf | Final approval 'در تاريخ۱۷/۸/۱۳۷۶' (8 Nov 1997); 42 articles, 25 notes; 10, 17, 18, 35 'حذف شد'; 39, 40 'الحاقي'; signed 'رئيس مجمع تشخيص مصلحت نظام ـ اكبر هاشمي رفسنجاني'. Print header '9/26/2016 www.dastour.ir/Print/?lid=175711', 13 pages. No 1389 or 1396 text in it. FAOLEX's record (leap.unep.org) cites Official Journal No. 15590, 6 Sep 1998 | FAOLEX (FAO); a print of a dastour.ir page whose operator the print does not name | 2 readings of every decisive passage, plus 3rd and 4th where needed (section 5) |
| 2 | قانون مبارزه با مواد مخدر (Anti-Narcotics Law, 3/8/1367, original, 35 articles) | https://faolex.fao.org/docs/pdf/ira167862.pdf | Print header '9/26/2016 www.dastour.ir/Print/?lid=133515', 11 pages; superseded by #1 | FAOLEX | 1 (context only) |
| 3 | FAOLEX records for #1 and #2 | https://leap.unep.org/en/countries/ir/national-legislation/amendment-and-supplementary-provisions-counter-narcotics-law ; https://leap.unep.org/en/countries/ir/national-legislation?page=30 | As displayed | UNEP/FAO | 1 each (metadata only) |

**Opened for orientation only** (no fact in the JSON rests on them):
- **shmu.ac.ir/fdo:** the food and drug deputy of Shahroud University of Medical Sciences. Its narcotics-unit, controlled-substances and regulations pages hold no list. They link only three PDFs: pharmacy regulations and two evaluation guidelines.
- **darman.sums.ac.ir:** a regulation on addiction treatment centres under the law, which lists no substances.
- **digitallibrary.un.org, E/NL.1972/45-46:** Iran's 1972 communication of narcotics laws to the UN. Record only; it is not current.
- **ensani.ir:** an academic article. It names no list.

## 3. What could not be read

WebFetch returned "robots disallowed" for nearly every Iranian official host. A few front pages loaded; deep pages did not.

| Host (body) | Pages tried | Result |
|---|---|---|
| qavanin.ir (national laws and regulations portal) | front page; `?CAPTION=` search; /Law/TreeText/164499 (the 1338 list, title from search results «تصويبنامه راجع به فهرست مواد مخدره»); /Law/TreeText/84416; /Law/PrintText/118572; www. variant | Front page loaded (a list of recent texts, the latest dated 1401/06/29). Every other page was refused. |
| rc.majlis.ir (Majlis Research Center law database) | /fa/law, /fa/law/search (both loaded: listings of 1393-1394 items); /fa/law/show/…, /fa/law/print_version/…, ?q= search, site root | Law pages refused |
| dastour.ir (legislation portal printed in the FAOLEX copies) | root; /Print/?lid=133515 | Refused |
| dotic.ir | root; /news/5619 (title in search results: «قانون مربوط به مواد روان‌گردان (پسيكوتروپ)»); /news/5620 (title: «تصويبنامه راجع‌به فهرست موادمخدر») | Refused |
| rrk.ir (Official Gazette) | root; /Shop/ShowProduct.aspx?Code=164 | Refused |
| dchq.ir, news.dchq.ir (Drug Control Headquarters) | root; news.dchq.ir/3/?p=15107 (title in search results: «فهرست داروهای مخدر تصویب شد/ تعیین مجازات حمل موادمخدر مطابق فهرست جدید») | Refused |
| fda.gov.ir, irc.fda.gov.ir (Food and Drug Administration) | front page (loaded: five announcements, no links); /item/4176 (www and bare host); irc.fda.gov.ir | Deep pages refused |
| Other official hosts | behdasht.gov.ir (front page loaded: a news page); majlis.ir; maslahat.ir (Expediency Council); irna.ir; epl.irica.ir and irica.ir (Customs); switzerland.mfa.gov.ir PDF; dolat.ir (front page only) | Refused, or front page only |
| University food-and-drug deputies | fda.ajums.ac.ir (narcotics distribution instruction 1391, PDF); old-fda.tbzmed.ac.ir (controlled-drugs unit PDF); arakmu.ac.ir regulation pages 276 (title «قانون مربوط به مواد روان گردان») and 4397; fdo.sums.ac.ir; fda.jums.ac.ir | Refused |
| UNODC SHERLOC | https://www.unodc.org/cld/uploads/res/document/irn/anti-narcotics-law_html/iran-THE_ANTI_NARCOTICS_LAW.pdf (an English text; not an Iranian host) and a SHERLOC document page | Client error, twice |

**Private sites.** These carry copies of the lists or of the current law, but they are not official, so nothing was taken from them:
- refused WebFetch: ekhtebar.ir, solh.ir, edalatsara.com, wikihoghoogh.net;
- read only as pointers: law-ir.ir (it files «تصویب نامه راجع به فهرست مواد مخدره مصوب 1338 با اصلاحات بعدی» under the 1338 poppy and opium law); lawyerir.com (it names a 1354 psychotropic-substances law);
- found in search results but not opened: davoudabadi.ir, farasai.com, shenasname.ir ("with the latest amendments to 1396/7/12");
- found broken: gafghahi.com, which returned a spam page.

**Currency.** Search results point to later amendments of the law, none of which could be read:
- an Expediency Council amendment of 1389 (2010), which news and law-firm pages say added industrial non-medical psychotropics (روان‌گردان‌های صنعتی غیردارویی);
- an article (Art. 45) added by Parliament in 1396 (2017).

One law-firm page (lawyerir.com) describes the current Art. 8 as covering LSD, ecstasy and crystal, which the 1376 text does not name, so Art. 8 at least has probably changed since 1376. News headlines in the results (not opened) also mention a bill on new psychoactive substances and a permission to grow hemp. None of this was used for a fact.

## 4. How I searched

**WebSearch** (standard and extended), in Persian and English, for:
- the law and its 1376, 1389 and 1396 amendments on qavanin.ir, rc.majlis.ir, dastour.ir, dotic.ir and rrk.ir;
- "فهرست مواد روان‌گردان صنعتی غیردارویی" and Drug Control Headquarters resolutions;
- the 1338 list ("فهرست مواد مخدره");
- the psychotropic-substances law ("قانون مربوط به مواد روان‌گردان (پسیکوتروپ)");
- Food and Drug Administration lists of narcotic and controlled medicines;
- Ministry of Health announcements;
- FAOLEX, UNODC SHERLOC and the UN Digital Library (E/NL series).

**Finding aids** (never used for facts):
- iranhr.net gave two qavanin.ir links;
- law-ir.ir and lawyerir.com named the 1338 list and a 1354 psychotropic-substances law.

**The decisive pointer was in the law itself:** the Art. 1 note (read twice), which names the 1338 list and the Ministry of Health announcements.

## 5. Method of reading

- **Two readings.** Each decisive passage was read in two WebFetch calls with differently worded prompts and layouts:
  - names per article as `ماده n | تبصره | name` lines, against a JSON array with fragments;
  - numbered verbatim fragments, against labelled short quotes (Q1-Q4, S1-S5, X/Y, T1-T3, JSON fields).
- **Third and fourth readings** were taken for Art. 40, where the summariser refused a long verbatim copy, and for the Art. 1 note.
- **Comparison by script.** Python ran inline from the shell, with the readings pasted into the script, and compared each pair. Normalisation:
  - NFKC;
  - zero-width non-joiner and tatweel removed;
  - Arabic ي/ك mapped to Persian ی/ک;
  - whitespace and quotation marks ignored.

  Per-article name sets were compared as sets.
- **Final check.** A last script checked that every Persian quotation in the JSON (14 distinct) is found in the settled readings and is at most 15 words. All pass, and all 75 rows carry every field of the brief.
- **Summariser limit.** The summariser quotes at most about 125 characters at a time, so long passages were read in short fragments. Its paraphrases were never used as readings.
- **Files.** No reading files were saved. The JSON was written by a small build script in the scratchpad, which was deleted afterwards.

| Passage | Readings | Result |
|---|---|---|
| Names per article, Arts 1-42 and notes | A (lines), B (JSON) | Agree except two items, both settled (section 6) |
| Art. 1 note (definition) | A (4 fragments), B (refused, paraphrase), C (X/Y quotes) | A and C identical |
| Art. 1 opening and its 9 items | A, B | Identical |
| Art. 1 item 1; Art. 3; Art. 4 | A, B | Identical |
| Art. 8 | A, B | Identical on the common span (B adds «وارد كند») |
| Art. 40: precursors | A, B | Identical on the common span |
| Art. 40: codeine and methadone | B (Q3), C (S3), D (words after «بنمايد») | Identical on the common span |
| Art. 40: «روانگردان» phrase; opening words | R1/R2, the 22-term check | Agree |
| Art. 41 | A (T1-T3), B (JSON) | Agree |
| Header, final approval date, deleted and added articles | Structure reading, S4/S5, second structure check | Identical |

## 6. Disagreements between readings, and how each was settled

1. **Art. 8.** Reading A listed «مشتقات شيميائي مرفين و كوكائين» as a separate name. Reading B instead listed مرفين and كوكائين a second time. Both verbatim fragments give «و ديگر مشتقات شيميائي مرفين و كوكائين». Settled: it is a generic clause (other chemical derivatives of morphine and cocaine), not a named substance.
2. **Art. 40.** Reading A listed «داروهاي روانگردان» (psychotropic drugs) as a name; reading B did not. Two further readings place the words inside the title of the 1988 UN Convention: «مبارزه با قاچاق مواد مخدر و داروهاي روانگردان مصوب ميلادي ۱۹۸۸». Settled: a convention title, not a controlled class.
3. **Spans.** Some readings quoted longer spans than others (Art. 8; both Art. 40 clauses). They agree on the common span. This is a difference of format only.
4. **Refusals.** Reading B of the Art. 1 note, and a reading of Art. 40 in pieces, were refused and replaced by a paraphrase. The paraphrases were not used, and short-quote readings replaced them (C and S3 above).

No disagreement of content remained.

## 7. Matching

- **By script.** A script searched the names printed in the law (both readings) with Persian and Latin search keys for all 77 items. Six items hit; cocaine was confirmed with a corrected key.
- **By eye.** Every hit was checked by eye.
- **False positives discarded:**
  - coca leaf against «كوكائين» (Art. 8);
  - morphine and cocaine against the generic «مشتقات شيميائي …» clause. That clause is recorded as a generic clause, not as a match.
- **Named (7 rows, all draft):**
  - **Cannabis and cannabis resin:** Art. 4 (بنگ, چرس); Art. 1 item 1 and Art. 3 (شاهدانه).
  - **Coca leaf:** Art. 3 (برگ كوكا); Art. 1 item 1 (coca cultivation).
  - **Cocaine:** Art. 8.
  - **Heroin:** Art. 8.
  - **Morphine:** Art. 8.
  - **Codeine and methadone:** Art. 40.
- **Not found in the lists read (68 rows, all draft).** These are every other item. Each row's note gives three things:
  - the definition by reference;
  - the lists searched;
  - the lists that could not be read.

  The oxycodone, hydrocodone and buprenorphine rows also note Art. 8's generic clause.
- **"If named" items.** Ayahuasca and peyote or San Pedro are not named; they have no row.

## 8. Unsettled: for the editor

1. **The official current lists are needed before Iran can have reliable rows.** In order of importance:
   - the 1338 Cabinet list «تصويبنامه راجع به فهرست مواد مخدره» with all its amendments (qavanin.ir/Law/TreeText/164499);
   - the Ministry of Health announcements of narcotics;
   - the 1389 amendment of the law, with any list of industrial non-medical psychotropics made under it;
   - the psychotropic-substances law «قانون مربوط به مواد روان‌گردان (پسيكوتروپ)».

   All sit on hosts that refuse WebFetch. A human reader, or a browser session that can open qavanin.ir, is needed. Until then, the 68 "not found" rows say only that the 1376 law text does not name the item.
2. **Should the "not found" rows be shown at all?** They follow this country's instruction. They could mislead a reader who takes "not found" to mean "legal", for example for methamphetamine, MDMA or tramadol. The editor may prefer to hide them, as was done for Egypt and the DRC, until the lists are read.
3. **Host and currency.** The text read is FAOLEX's copy of a 2016 print of the 1376 text. dastour.ir's operator could not be confirmed, and the later amendments were not read. All seven named rows are therefore draft, and may be out of date: the 1389 amendment may have changed Arts 4 and 8.
4. **Generic clause.** Does Art. 8's «ديگر مشتقات شيميائي مرفين» (other chemical derivatives of morphine) reach oxycodone, hydrocodone or buprenorphine? A chemist or lawyer should decide.
5. **Art. 40's intent clause.** Whether the opening intent "to convert or produce narcotics" qualifies the codeine and methadone clause is a penal reading. The rows only record that both are named.
6. **Glosses.** بنگ is glossed "bhang" (cannabis herb) and چرس "charas" (cannabis resin). Both glosses are the reader's; the law defines neither.
7. **medical_use** is null throughout. Art. 41's exemption for medical, research and industrial uses with a Ministry of Health permit is general.
