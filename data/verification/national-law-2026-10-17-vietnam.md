# W2 report: Viet Nam's own lists of controlled substances

Checked on 2026-10-17 by AI reader W2, using WebSearch and WebFetch only (no browser, no shell downloads).

Output: `/home/claude/drug-encyclopedia/data/legal/_incoming/vietnam.json`, with **no rows**. Viet Nam's current lists could not be read online, so nothing was matched and nothing was guessed.

## 1. Result in brief

- **The current lists.** Viet Nam lists its controlled substances in the four Danh mục (lists) annexed to **Nghị định số 28/2026/NĐ-CP quy định các danh mục chất ma túy và tiền chất** (Government Decree No. 28/2026/ND-CP setting the lists of narcotic substances and precursors).
  - Dated 19-01-2026 and in force 19-01-2026. Signed by Phạm Minh Chính.
  - Published in Công báo (the Official Gazette) No. 82 of 4 Feb 2026, from printed p. 3.
  - No amendment was found as of 17 Oct 2026.
- **Why nothing could be read.**
  - Every official copy that WebFetch can reach is a scan with no text layer:
    - the decree PDF on vanban.chinhphu.vn;
    - the four list PDFs linked from the Government newspaper.
  - The only copies likely to have text are the Gazette's DOCX and PDF. They are served from g7.cdnchinhphu.vn, which bars WebFetch by robots.txt.
  - The Ministry of Justice database (vbpl.vn) lists the decree, but its search and document pages return errors.
- **What is recorded.**
  - `entries` is empty.
  - `not_found` is empty: no list was read, so no item can be called "not found".
  - All 77 items are named under `unsettled`.
- **A second official list, under the pharmacy law, could not be read either.** This is Ministry of Health Circular 18/2026/TT-BYT (in force 16 Jul 2026). Its text is also on the blocked Gazette CDN only (§2).
- **Merging.**
  - The merge script (`scripts/merge_national_law.py`) will report 0 rows on 0 drug pages for Viet Nam.
  - No drug page has an existing Viet Nam row: a search of `data/legal/*.json` for "vietnam" or "viet nam" found none.

## 2. The instruments: what could be read

Only the official document pages could be read: their metadata, read twice each. No list entry, article or annex text of any instrument could be read.

**Decree 28/2026/NĐ-CP (the lists).**
- vanban.chinhphu.vn (docid 216717):
  - Số ký hiệu 28/2026/NĐ-CP; ngày ban hành 19-01-2026; ngày có hiệu lực 19-01-2026.
  - Loại văn bản Nghị định; cơ quan ban hành Chính phủ; người ký Phạm Minh Chính.
  - Trích yếu (title): "Quy định các danh mục chất ma túy và tiền chất".
  - One attachment, 28-cp.signed.pdf. It is a scan: probed twice, no text.
- Official Gazette page:
  - ngày ban hành 19/01/2026; hiệu lực 19/01/2026; Công báo số 82, 2026-02-04.
  - Its relationship chart (Lược đồ) shows no linked document.
  - Two downloads, `2026_82_28/2026/NĐ-CP.docx` and `.pdf`. Both are on g7.cdnchinhphu.vn, which refused (ROBOTS_DISALLOWED, robots.txt included).
  - The issue page puts the decree at printed p. 3.
- **Reported but not read.** The Government newspaper (baochinhphu.vn, 20 Jan 2026) and the Hưng Yên provincial portal (13 Feb 2026) give the lists' structure. These are news items, so none of this is recorded as fact:
  - Danh mục I: substances absolutely banned from medicine and social life, 58, in IA and IB;
  - Danh mục II: 476, in IIA and IIB;
  - Danh mục III: 81;
  - Danh mục IV: 79 precursors, in IVA (31), IVB (30) and IVC (18).
  - They, and Cần Thơ's legal-dissemination portal, also report that the decree ends Decree 57/2022/NĐ-CP (25 Aug 2022) and Decree 90/2024/NĐ-CP (17 Jul 2024).
- **Transitional dates (news only).** The newspaper reports two:
  - carisoprodol and etomidate (not items): controlled from 1 Jun 2026;
  - 1,4-butanediol: lawful businesses must meet the precursor rules before 31 Dec 2026.
  - The second suggests that **1,4-butanediol** (ghb-gbl page) is now a listed precursor. It must be confirmed in Danh mục IV before it is recorded.

**Luật Phòng, chống ma túy No. 120/2025/QH15 (the law the lists serve).**
- vanban.chinhphu.vn (docid 216502): adopted 10-12-2025; ngày có hiệu lực 01-07-2026; Quốc hội; signed by Trần Thanh Mẫn.
- The Ministry of Public Security database (vanban.bocongan.gov.vn) shows "Còn hiệu lực" (in force) from 01/07/2026.
- The Gazette page (Công báo số 36, 2026-01-21) prints hiệu lực as "07/01/2026". Read twice; both readings agree. This conflicts with the two other pages. The law's own effect clause could not be read, and the point does not affect any item.
- **Not read.** Both official PDFs (vanban.chinhphu.vn, MPS) are scans, and the Gazette copies are on the blocked CDN. So the law's definitions could not be read. Nor could it be checked whether the law points to any further list, for example of plants.

**Nghị định số 163/2026/NĐ-CP (detailing the law).**
- vanban.chinhphu.vn (docid 218256): dated 15-05-2026, in force 01-07-2026, signed by Phạm Thị Thanh Trà.
- Its three attachments (163-ndcp.signed.pdf, 163-2.pdf, 163-3.pdf) are all scans.

**Thông tư số 18/2026/TT-BYT (pharmacy law: medicines under special control).**
- Gazette page: Bộ Y tế; signed by Nguyễn Tri Thức; ngày ban hành 01/06/2026; hiệu lực 16/07/2026; Công báo số 329, 2026-06-14.
- Downloads only on the blocked CDN.
- Not found on vanban.chinhphu.vn. Docids 218316-218400 were checked one by one; 218317 is the Ministry's previous circular, 17/2026/TT-BYT.
- **Finding aids (not used for facts).**
  - A Lạng Sơn Department of Health dispatch (soyt.langson.gov.vn, June 2026) says the circular replaces Circulars 20/2017/TT-BYT and 27/2024/TT-BYT.
  - Bạc Liêu General Hospital posts a text copy of an **unsigned** version, with number and date left blank: https://bvdkbaclieu.gov.vn/upload/1000079/20260613/771_Thong-tu-18-2026-TT-BYT_5f0ad354fb.pdf
    - It was opened only to see its shape. It appears to hold Phụ lục I (dược chất gây nghiện, narcotic drug substances, about 42 rows), II (dược chất hướng thần, psychotropic drug substances, about 72) and III (tiền chất dùng làm thuốc, precursors used as medicines, about 8).
    - Its preamble cites Decree 28/2026/NĐ-CP. Its Article 1 ties the annexes to the Pharmacy Law, not to the decree's Danh mục.
    - No row was made from it: a hospital is not the publisher, and the version is unsigned.
    - Even if read, this list could only add medical-use detail. It cannot stand in for the decree's lists, because many items (for example heroin, LSD, MDMA) would sit only in the decree.

## 3. Sources

| Source | URL read | Version printed | Result |
|---|---|---|---|
| Decree 28/2026/NĐ-CP, vanban.chinhphu.vn | https://vanban.chinhphu.vn/?docid=216717&pageid=27160 | dated and in force 19-01-2026 | page read twice; PDF (https://datafiles.chinhphu.vn/cpp/files/vbpq/2026/01/28-cp.signed.pdf) probed twice: no text |
| Decree 28/2026/NĐ-CP, Official Gazette No. 82 | https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-28-2026-nd-cp-468827/62134.htm ; issue page https://congbao.chinhphu.vn/cong-bao/cong-bao-so-82-ngay-04-02-2026-46980.htm | Công báo số 82, 4 Feb 2026, p. 3 | page read twice; DOCX/PDF refused by robots.txt |
| Danh mục I-IV as four PDFs (Government newspaper) | bcp.cdnchinhphu.vn …signed-trang-3/4/5/6….pdf (full URLs in the JSON) | scans of the signed decree | each probed: no text |
| Law 120/2025/QH15, vanban.chinhphu.vn | https://vanban.chinhphu.vn/?pageid=27160&docid=216502&classid=1&orggroupid=1 | adopted 10-12-2025; in force 01-07-2026 | page read twice; PDF probed: no text |
| Law 120/2025/QH15, Official Gazette No. 36 | https://congbao.chinhphu.vn/van-ban/luat-so-120-2025-qh15-468574.htm | prints hiệu lực 07/01/2026 | page read twice (dates); downloads on the blocked CDN |
| Law 120/2025/QH15, MPS database | https://vanban.bocongan.gov.vn/co-so-du-lieu-van-ban/luat-phong-chong-ma-tuy-1768903233?tab=attributes | Còn hiệu lực; in force 01/07/2026 | read once; PDF on bocongan.gov.vn/media probed: no text |
| Decree 163/2026/NĐ-CP, vanban.chinhphu.vn | https://vanban.chinhphu.vn/?pageid=27160&docid=218256 | dated 15-05-2026; in force 01-07-2026 | page read twice; three PDFs probed: no text |
| Circular 18/2026/TT-BYT, Official Gazette No. 329 | https://congbao.chinhphu.vn/van-ban/thong-tu-so-18-2026-tt-byt-469674.htm | dated 01/06/2026; in force 16/07/2026 | page read twice; downloads on the blocked CDN |

## 4. How I searched

- **Finding the decree.**
  - WebSearch found news of Decree 28/2026 at once.
  - The vanban.chinhphu.vn search is an ASP.NET postback form, so a `keyword` in the URL is ignored. An extended WebSearch returned the decree's docid (216717).
  - The Government newspaper's article linked the four list PDFs.
  - The Gazette's search loads by script. Instead I opened issue pages by their sequential issue ID:
    - ID 47050 = No. 150 (17 Mar 2026);
    - 46940 = No. 42 (22 Jan);
    - 46950, 46960, 46970 = Nos. 52, 62, 72;
    - 46980 = No. 82 (4 Feb 2026), which holds the decree.
- **Hosts tried, and what happened.**

| Host | Outcome |
|---|---|
| vanban.chinhphu.vn, datafiles.chinhphu.vn | reachable; every relevant file is a scan (the decree, the law, Decree 163) |
| baochinhphu.vn, bcp.cdnchinhphu.vn | reachable; the four list PDFs are scans |
| congbao.chinhphu.vn | reachable for metadata. g7.cdnchinhphu.vn (all downloads): ROBOTS_DISALLOWED, robots.txt included |
| vbpl.vn | listing pages reachable but carry no links. Search page and document pages (vbpq-toanvan, vbpq-thuoctinh): CLIENT_ERROR. vbpl.moj.gov.vn: ROBOTS_DISALLOWED |
| moj.gov.vn, phapdien.moj.gov.vn | ROBOTS_DISALLOWED |
| phapluat.gov.vn | CLIENT_ERROR |
| bocongan.gov.vn | /van-ban: CLIENT_ERROR; articles reachable. vanban.bocongan.gov.vn: the law's entry is reachable; lists load by script ("Không có dữ liệu"); the decree's entry was not found |
| dav.gov.vn (Drug Administration) | ROBOTS_DISALLOWED |
| congan.daklak.gov.vn | ROBOTS_DISALLOWED |
| hungyen.gov.vn, pbgdpl.cantho.gov.vn | news summaries, no attachment |
| hcc.nghean.gov.vn | serves the same signed scans (checked on its Decree 57/2022 page) |
| moit.gov.vn; cuchoachat.gov.vn | MOIT posts its own documents only. Cục Hóa chất's TCTN.pdf is a guide built on the repealed Decree 57/2022 |
| customs.gov.vn | home page loads by script; no hit in search |

- **Text-layer searches.** Searches for phrases that only a text copy would contain found no government-hosted text copy of the decree: "Danh mục IVC", the transitional sentence, the effect clause and file-name variants.
- **Finding aids, never used for facts.**
  - thuvienphapluat.vn: amendment status, which shows none.
  - luatvietnam.vn, tapchitoaan.vn.
  - thoibaotaichinhvietnam.vn: Customs dispatch 13040/CHQ-GSQL implementing the decree.
  - viettimes.vn.
  - enviliance.com and chemical.chemlinked.com: the lead to Decree 163/2026.
  - vietnamlawmagazine.vn; khoaduoc.pnt.edu.vn.
  - The Lạng Sơn dispatch and the Bạc Liêu hospital copy (§2).

## 5. Method, and every disagreement

- **Readings.** No list chunk could be read. Each official document page was read twice with different prompts: first prose fields, then JSON or `field :: value` lines.
- **Comparison.** A Python script, run with both readings pasted inline, compared every field. No reading files were saved. Normalisation: NFKC, whitespace, case.

| Page | Fields | Result |
|---|---|---|
| vanban 216717 (Decree 28/2026) | 8 | identical |
| Gazette 62134 (Decree 28/2026) | 9 | identical |
| Gazette 469674 (Circular 18/2026) | 9 | 8 identical, 1 equal after case ("Bộ Y tế" / "BỘ Y TẾ") |
| vanban 216502 (Law 120/2025) | 6 | identical |
| Gazette 468574 (Law 120/2025), dates | 2 | identical |
| vanban 218256 (Decree 163/2026) | 7 | identical |

- **Disagreements between readings.** None.
- **Disagreement between sources.** The law's effect date: 01-07-2026 on vanban.chinhphu.vn and 01/07/2026 in the MPS database, against 07/01/2026 on the Gazette page. It is unsettled, but it does not touch any item.
- **Matching.** Not done: there were no entries to match.

## 6. Results

- **Listed:** 0 rows.
- **Not found:** none recorded; no list was read.
- **Unsettled:** all 77 items, by drug page, in the JSON.
- **Lead for one item (unverified):** 1,4-butanediol as a precursor (§2).

## 7. Unsettled (for the editor)

1. **The scanned lists need a reading that WebFetch cannot give.**
   - **Needed from Vasilis:** save the Official Gazette copies (PDF, or DOCX) from these three pages:
     - Decree 28/2026/NĐ-CP: https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-28-2026-nd-cp-468827/62134.htm
     - Circular 18/2026/TT-BYT: https://congbao.chinhphu.vn/van-ban/thong-tu-so-18-2026-tt-byt-469674.htm
     - Law 120/2025/QH15: https://congbao.chinhphu.vn/van-ban/luat-so-120-2025-qh15-468574.htm
   - The Gazette copies are likely to carry text, since one is a DOCX. This could not be checked, because they could not be opened.
   - A reader could then read the lists from the saved files. That needs the editor's leave, since this brief allows only WebFetch.
   - Otherwise a human or OCR reading of the scanned lists on vanban.chinhphu.vn is needed.
2. **Circular 18/2026/TT-BYT.** Decide whether the Bạc Liêu General Hospital copy, an unsigned version, may be used. It should at least be checked against the Gazette copy. Even read, it adds medical-use detail only.
3. **Plants.** Whether any official list names plants could not be checked; it rests on the law and Decree 163/2026, both unread. This matters for coca leaf, cannabis, kratom, Salvia divinorum, peyote/San Pedro and the ayahuasca plants.
4. **Currency.**
   - No amendment of Decree 28/2026 was found on 17 Oct 2026. The vanban.chinhphu.vn page lists none, the Gazette chart shows no linked document, and searches found none.
   - Whoever reads the lists should still check the Gazette from 4 Feb 2026 onward.
5. **Until then** Viet Nam has no national rows, and the drug pages keep only the UN treaty layer.
