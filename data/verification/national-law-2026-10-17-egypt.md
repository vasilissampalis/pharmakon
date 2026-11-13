# W2 report: Egypt's own lists of controlled substances

Read on 2026-10-17 by AI reader W2. Output: `/home/claude/drug-encyclopedia/data/legal/_incoming/egypt.json`, with **no rows**. Egypt's current tables of controlled substances could not be read online, so nothing was matched and nothing was guessed.

## 1. Result in brief

- **The current list.** Egypt lists its controlled substances in the tables annexed to **Law No. 182 of 1960** on combating narcotics and regulating their use and trafficking.
  - Ministry of Health and Population **Decree No. 44 of 2026** replaced all of those tables (17 Feb 2026).
  - **Decree No. 242 of 2026** then amended them (Gazette of 17 Aug 2026).
- **Why nothing could be read.** The only official copies online are the Egyptian Drug Authority's PDFs of the two Gazette issues, and both print the tables as scanned images with no text layer. WebFetch cannot read images, and the brief allows no browser and no shell download.
- **What is recorded:**
  - `entries` is empty.
  - `not_found` is empty, because no list was read, so no item can be called "not found".
  - All 77 items are named under `unsettled`.
- **A second, separate official list was read.** This is the Drug Authority's annex of products and substances "that may be misused", made under the Authority Chairman's Decree No. 375 of 2026 (pharmacy law). It names only five generics, and none of the 77 items is among them. It is not the narcotics tables, so its silence proves nothing, and no row was made from it (see section 2).
- **Merging.** The merge script (`scripts/merge_national_law.py`) will report 0 rows on 0 drug pages for Egypt, and no drug page has an existing Egypt row.

## 2. The Egyptian instruments: what could be read

**Decree No. 44 of 2026.** Two readings, identical apart from format:
- Title: "قرار رقم 44 لسنة 2026 بشأن استبدال الجداول الملحقة بالقانون رقم 182 لسنة 1960". Gloss: Decree No. 44 of 2026 replacing the tables annexed to Law No. 182 of 1960.
- Issued by the Minister of Health and Population, Prof. Dr. Khaled Atef Abdel Ghaffar, "صدر فى 17/2/2026" (issued 17 Feb 2026).
- Published in al-Waqa'i' al-Misriyya No. 39 (continued) (C), 17 February 2026. The decree is on printed pp. 2-3 and the tables on pp. 4-35.
- **Art. 1:** "تستبدل الجداول المرافقة لهذا القرار، بالجداول الملحقة بالقانون رقم 182 لسنة 1960". Gloss: the tables attached to this decree replace those annexed to Law 182 of 1960. So every earlier version of the tables is superseded.
- **Art. 2:** published in al-Waqa'i' al-Misriyya, in force from the date of publication.
- **Preamble.** It cites:
  - Law 127 of 1955 (pharmacy practice), Law 182 of 1960, Law 71 of 2009 (mental-health patient care) and Law 151 of 2019 (which set up the Unified Procurement Authority and the Drug Authority);
  - the 1961, 1971 and 1988 UN conventions;
  - Presidential Decree 242 of 1996, which organizes the Ministry;
  - the Supreme Constitutional Court judgment in case No. (33) of judicial year 47 (Constitutional), session of 16/2/2026;
  - the proposal of the head of the Egyptian Drug Authority.
- **Number order.** The text layer prints numbers in reversed order, for example "١٩٦٠ لسنة ١٨٢" and "٢٠٢٦ لسنة ٤٤قرار رقم". The reading order was restored from Decree 242's text, which is not reversed and cites the same law and decree.

**Decree No. 242 of 2026.** Two readings, identical:
- Title: "قرار رقم 242 لسنة 2026 بشأن تعديل الجداول الملحقة بالقانون رقم 182 لسنة 1960". It goes on: "والمستبدلة بقرار وزير الصحة والسكان رقم 44 لسنة 2026" (as replaced by Decree No. 44 of 2026).
- Issued "صدر فى 2026/7/20" (20 Jul 2026), same minister.
- Published in al-Waqa'i' al-Misriyya No. 179, 17 August 2026, printed pp. 9-12.
- **Art. 1:** "يستبدل بنص البند (12) الوارد بالجدول رقم (1) - القسم الأول (ب)". Gloss: the text of item (12) in Table (1), Part One (B), is replaced by the text that follows. That text is on p. 11, which has no text layer.
- **Art. 2:** in force from the day after publication.
- This is the only fact about the tables' layout that could be read: there is a Table (1) with a Part One (B) that has an item (12).

**Is this current?** On 2026-10-17, the Drug Authority's laws page, in English and in Arabic, lists only three narcotics items:
- Law 182 of 1960 (05/06/1960);
- Decree 44 of 2026 (17/02/2026);
- Decree 242 of 2026 (20/07/2026).

The Authority's 2026 chairman decrees:
- Nos. 157, 158, 235, 239, 354 and 379: their titles do not concern the tables.
- Nos. 375 and 376: listed only as "Arabic version", so both were opened. No. 376 is about laboratory licensing; No. 375 is described below.

Searches for later decrees amending the tables found none.

**A separate pharmacy-law list: substances that may be misused.**
- **The decree.** Drug Authority Chairman's Decree No. 375 of 2026 (dated 28/6/2026; al-Waqa'i' al-Misriyya No. 139 bis (A), 29 June 2026) regulates the import, tracking of circulation, export and dispensing of "المواد التي قد يساء استخدامها" (substances that may be misused).
  - Its preamble cites Law 127 of 1955 (pharmacy practice), the industrial-licensing law (printed "(15) لسنة 2027" in the text layer, one reading), Law 151 of 2019 and Presidential Decree 28 of 2026 (the Authority's board).
  - It does not cite Law 182 of 1960, and the word "المخدرات" (narcotics) does not occur.
  - Art. 2 requires a regulatory guide on the Authority's website with an annexed table of the substances.
- **The guide and its annex.** Both are posted on the guidelines page of the Authority's inspection administration ("06/2026 | Version 01"; the guide's file name carries 30-6-2026). The guide's URL is too long for WebFetch.
- **What the annex lists.** It is a table of registered products ("Trade_name Dosage_form Generics") under five substance headings: eszopiclone, gabapentin (also gabapentin enacarbil), cyclopentolate (some products with phenylephrine), tropicamide and clozapine. None of the 77 items appears.
- **Why it adds no rows.** This list sits under the pharmacy law, beside the narcotics tables. That an item is absent from it shows nothing about the item's status.

## 3. Sources read (all official)

| Source | URL | Version printed | Used for | Readings |
|---|---|---|---|---|
| MoHP Decree No. 44 of 2026 with its tables, al-Waqa'i' al-Misriyya No. 39 (cont.) (C), Drug Authority copy | https://edaegypt.gov.eg/media/dkjooww3/%D9%82%D8%B1%D8%A7%D8%B1-%D9%88%D8%B2%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D8%B5%D8%AD%D8%A9-%D9%88%D8%A7%D9%84%D8%B3%D9%83%D8%A7%D9%86-%D8%B1%D9%82%D9%85-44-%D9%84%D8%B3%D9%86%D8%A9-2026-ar-2026_.pdf | issued 17/2/2026; Gazette 17 Feb 2026 | decree text; check of the table pages | decree text twice; table pages 4 probes |
| MoHP Decree No. 242 of 2026, al-Waqa'i' al-Misriyya No. 179, Drug Authority copy | https://edaegypt.gov.eg/media/lydpgqi5/%D9%84%D9%85%D9%83%D8%A7%D9%81%D8%AD%D8%A9-%D8%A7%D9%84%D9%85%D8%AE%D8%AF%D8%B1%D8%A7%D8%AA_2026_242-%D9%88%D8%B2%D9%8A%D8%B1-%D8%A7%D9%84%D8%B5%D8%AD%D8%A9.pdf | issued 20/7/2026; Gazette 17 Aug 2026 | what it amends; check of p. 11 | twice |
| Drug Authority, Laws and Executive Regulations (English and Arabic pages) | https://edaegypt.gov.eg/en/the-regulatory-reference-of-the-egyptian-drug-authority-eda/laws-and-executive-regulations/ | as displayed | which instruments are in force | once each (they agree) |
| Law No. 182 of 1960 and its amendments, Drug Authority copy | https://edaegypt.gov.eg/media/ekgifxb3/1960-182.pdf | none readable | text layer check | twice: "empty or contains no machine-readable text" |
| Drug Authority Chairman's Decree No. 375 of 2026 (substances that may be misused) | https://edaegypt.gov.eg/media/twwd4hs3/375-2026_ar.pdf | dated 28/6/2026; Gazette 29 June 2026 | shows the annex is a pharmacy-law list, not the narcotics tables | three (two summaries, one verbatim reading of the preamble) |
| Annex of products and substances with misuse potential (Drug Authority) | https://edaegypt.gov.eg/media/kgnfy0p5/%D9%85%D9%84%D8%AD%D9%82-%D8%A7%D9%84%D9%85%D8%B3%D8%AA%D8%AD%D8%B6%D8%B1%D8%A7%D8%AA_2026-ar.pdf | no date printed; listed as "06/2026, Version 01" | the generics it names | twice |

**Also opened, for orientation only** (none supplied a fact in the JSON):
- the Drug Authority's page of amendments to Law 182 of 1960, which lists amending laws from 1960 to Law 19 of 2020 and no table decrees;
- its Arabic ministerial-decrees index and its 2026 chairman decrees page;
- its EDA Chairman Decree index (English) and its inspection administration's guidelines page;
- its Periodic Lists and Databases pages, neither of which holds a controlled-substances list;
- Drug Authority chairman's Decree 376 of 2026 (laboratory licensing);
- a Cairo Governorate English news item (cairo.gov.eg), which links to no document.

**Not used for any fact:**
- news sites (Ahram Gate, Masrawy, Maspero, Al Arabiya, Daily News Egypt, Mada Masr, Almal News, Akhbar El Yom, Parlmany). Only one Daily News Egypt page and one Akhbar El Yom page were opened. They showed only that a court ruling, a replacement decree and a misuse guide existed;
- manshurat.org, a private legal database that appears in search results for these decrees (not opened);
- dspace.id.com.eg, a repository of Gazette issues. Its operator is not shown, it is not a gov.eg site, and its files sit behind "request-a-copy". Two item pages were opened; neither is the 2026 issue;
- UNODC SHERLOC's French copy of the 1960 law (not opened).

## 4. How I searched

**Searches.** I used WebSearch in Arabic and English. The queries covered:
- Law 182 of 1960 and its tables on gov.eg;
- the Drug Authority's decrees on the tables;
- "44 لسنة 2026" and "242 لسنة 2026", with the exact phrase Decree 242 uses for the current tables;
- any later decree amending the tables (Aug-Oct 2026);
- the 2026 constitutional ruling;
- the Gazette issues (No. 39 of 17 Feb 2026, No. 179 of 17 Aug 2026) and the Amiri Press;
- an official legislation portal;
- the Fund for Drug Control and Treatment of Addiction;
- the Drug Authority's English pages for an English version.

**Sites tried:**
- **edaegypt.gov.eg** (Drug Authority): laws page (English and Arabic), amendments page, ministerial-decrees and 2026 decree pages, Periodic Lists, Databases, and its inspection administration's guidelines page (which holds the misuse guide and its annex). This is the only official host of the two decrees found.
- **mohp.gov.eg, ppo.gov.eg, cc.gov.eg and sccourt.gov.eg**: site-restricted searches returned no page from these domains.
- **cairo.gov.eg**: a news item only.

**Finding.** No official copy of the 2026 tables with a text layer was found.

## 5. Method of reading

- **Two readings.** Each document was read twice with WebFetch, using differently worded prompts and formats:
  - reading 1: numbered verbatim segments of at most 100 characters;
  - reading 2: labelled fields (masthead, number, title, each recital, each article, issue date, signatory).
- **Script comparison.** Python compared each pair, with both readings pasted inline into the script. No reading files were saved, because only the two output files were to be written. Text was normalized (tatweel and whitespace removed, Persian yeh mapped to Arabic yeh), joined, and diffed with difflib.
- **Table pages of Decree 44.** These were probed four times:
  1. a general probe;
  2. a Latin-script and full-page probe of pp. 3, 4, 5 and 35;
  3. a probe asking for any characters, even garbled, after the masthead on pp. 6, 10, 20 and 30;
  4. a page-by-page table of pp. 4-35.

  All four agree: each page holds only the masthead and its page number.
- **Annex of products with misuse potential.** It was read twice: first the table groups and first entries, then every distinct generic name with a yes/no check of 26 names. A script compared the two sets of substance headings and matched all 77 items, with synonyms (INN and common names, plant genera for the "if named" items), against every generic either reading gives. There were no hits.
- **Matching.** Against the narcotics tables, not done: no entry of the tables was read.

## 6. Disagreements between readings, and how each was settled

- **Decree 44, printed pp. 2-3.** The joined texts were 1,053 and 1,008 characters with spaces removed (similarity 0.978). The only differences are three format lines:
  - reading 1 kept the line "وزير الصحة والسكان" above the preamble, and the headings "(المادة الأولى)" and "(المادة الثانية)";
  - reading 2 used labels for the articles and gave the minister's title with the signature.

  Every recital, both articles, the issue date and the signatory are identical. Settled with no change.
- **Decree 44, printed pp. 4-35.** The four probes agree that there is no body text. No disagreement.
- **Decree 242.** The two readings are identical (1,157 characters each, similarity 1.000). Both find no text after the colon of Art. 1, and both find only the masthead on p. 11.
- **Law 182 PDF.** Both readings return the same "no machine-readable text" message.
- **Drug Authority laws page.** The English and Arabic readings agree on the three narcotics items and their dates. The Arabic reading's summary called Decree 44 a "Law No. (44)"; the decree's own text (two readings) prints "قرار رقم" (decree), which settles it.
- **Annex of products with misuse potential.**
  - The five substance headings agree.
  - Reading 2 also names gabapentin enacarbil (2 rows) and phenylephrine (a second ingredient in 2 cyclopentolate rows).
  - The row counts differ: reading 1 gave cyclopentolate 10 and an inconsistent gabapentin total, while reading 2 gave eszopiclone 18, gabapentin 62 plus 2, cyclopentolate 9, tropicamide 9 and clozapine 11.

  Row counts are not used for anything, and no reading names any of the 77 items, so this was settled with no change.
- **Decree 375.** The three readings agree on its number, date, Gazette issue, signatory and subject. The verbatim reading confirms the pharmacy-law basis and finds neither "182 لسنة 1960" nor "المخدرات" in the text.

## 7. Unsettled: for the editor

1. **The scanned tables.** The tables in force are those attached to Decree 44 of 2026, as amended by Decree 242 of 2026, and they could not be read. The candidates are:
   - an OCR or browser reading of the Drug Authority's PDF of Decree 44 (printed pp. 4-35) and of Decree 242 (p. 11), which is outside this brief's rules;
   - a human reading of those 33 pages.

   Until one of these is done, Egypt has no national rows, and all 77 items stay unread, not "not found".
2. **Item (12) of Table (1), Part One (B)** was replaced by Decree 242 of 2026. Its substance is not legible.
3. **Earlier texts were not used.** Searches return earlier Drug Authority chairman decrees on the tables (for example 4/2020, 442/2021, 480/2021, 481/2021, 272/2022, 697/2022, 586/2023). They were not opened: Decree 44 of 2026 replaced all the tables, and it recites the Supreme Constitutional Court judgment of 16/2/2026 (case 33, judicial year 47), which was itself not read. Decide whether a clearly labelled historical note is wanted. If so, it needs its own reading.
4. **The Law's own text.** The Drug Authority's PDF of Law 182 of 1960 has no text layer, so its articles on the tables (who may amend them, and any generic clauses) were not read.
5. **The list of products with misuse potential** (Decree 375 of 2026 and its annex) is a pharmacy-law control list. It covers eszopiclone, gabapentin, cyclopentolate, tropicamide and clozapine, none of which is a site item. Decide whether a drug page should ever mention it. It does not bear on any of the 77 items now.
