# W2 report: Indonesia's national lists (narcotics and psychotropics classes)

Read on 2026-10-17 by AI reader W2. Output: `/home/claude/drug-encyclopedia/data/legal/_incoming/indonesia.json`. It has 76 rows under the 25 drug-page keys. Ayahuasca is named, so it has a row. Peyote or San Pedro is not named, so it has none.

## 1. The lists

**Legal frame (each provision read twice, once in each of two official copies)**
- **Narcotics.** Law No. 35 of 2009 on Narcotics, Pasal 6(2)–(3):
  - the first classification is the law's Lampiran I;
  - changes of classification are "diatur dengan Peraturan Menteri" (made by Ministerial regulation).
- **Psychotropics.** Law No. 5 of 1997 on Psychotropics, Pasal 2(3)–(4):
  - the types in Golongan I–IV were first set in the law's annex;
  - "penetapan dan perubahan" (setting and changing) them is "diatur oleh Menteri" (for the Minister).

**The current lists**
1. **Narcotics: Permenkes No. 15 Tahun 2025 tentang Perubahan Penggolongan Narkotika** (Health Minister Regulation 15/2025 on Changes to the Classification of Narcotics).
   - Signed 21 Nov 2025; promulgated 28 Nov 2025, Berita Negara 2025 No. 989.
   - In force on promulgation (Pasal 4). Revokes Permenkes 7/2025 (Pasal 3).
   - Pasal 2(1): the Minister sets the classes "sebagaimana tercantum dalam Lampiran" (as set out in the annex).
   - Its Lampiran "PENGGOLONGAN NARKOTIKA" restates the whole classification from entry 1 (the opium poppy): A. Golongan I, 219 entries; B. Golongan II, 91; C. Golongan III, 15.
2. **Psychotropics: Permenkes No. 14 Tahun 2025 tentang Penetapan dan Perubahan Penggolongan Psikotropika.**
   - Signed 21 Nov 2025; promulgated 28 Nov 2025, Berita Negara 2025 No. 988. Revokes Permenkes 6/2025.
   - Its Lampiran "PENGGOLONGAN PSIKOTROPIKA" has A. Golongan I, 12 entries; B. Golongan II, 6; C. Golongan III, 8; D. Golongan IV, 62.
   - Long-standing medicines (diazepam, phenobarbital and others) appear in it, so it reads as a full list, not only the changes.

**Currency.** BPK's legal database shows both regulations as "Berlaku" (in force), with no "Dicabut dengan" (revoked by). Each is the last link of its chain:
- Narcotics: … 4/2021 → 9/2022 → 36/2022 … 30/2023 → 7/2025 → 15/2025.
- Psychotropics: 9/2015 → 3/2017 … 57/2017 → 49/2018 → 23/2020 → 2/2021 → 10/2022 … 31/2023 → 6/2025 → 14/2025. The links shown as "…" were not printed in the listings read.

Web searches for a 2026 Health Ministry regulation on either list found none.

**Class definitions (Pasal 1, read twice; used for `medical_use`)**

| Class | What Pasal 1 says |
|---|---|
| Narkotika Golongan I | "hanya dapat digunakan untuk tujuan pengembangan ilmu pengetahuan dan tidak digunakan dalam terapi" (science only, not therapy) |
| Narkotika Golongan II | "berkhasiat pengobatan yang digunakan sebagai pilihan terakhir" (therapeutic, used as a last resort) |
| Narkotika Golongan III | "berkhasiat pengobatan dan banyak digunakan dalam terapi" (therapeutic and widely used in therapy) |
| Psikotropika Golongan I | science only, not therapy |
| Psikotropika Golongan II and III | "berkhasiat pengobatan dan banyak digunakan dalam terapi" |
| Psikotropika Golongan IV | "berkhasiat pengobatan dan sangat luas digunakan dalam terapi" (very widely used in therapy) |

**Generic clauses.** A script searched all 413 agreed rows; the chemical names were read for the matched entries.
- **Salts:** the last entry of each narcotics class is "Garam-garam dari Narkotika dalam golongan tersebut di atas" (salts of the narcotics in this class): I-219, II-91, III-13. The psychotropics annex has no salts entry (two readings).
- **Isomers and stereoisomers:**
  - THC: I-9 is "Tetrahydrocannabinol, dan semua isomer serta semua bentuk stereo kimianya". I-10 is "Delta 9 tetrahydrocannabinol, dan semua bentuk stereo kimianya". These decide the dronabinol row.
  - Per-entry "termasuk campuran rasemat dan semua stereoisomernya" (including the racemate and all stereoisomers): seen in MDPV, mephedrone, 2-MMC, 3-MMC and MDMB-4en-PINACA, and in psychotropics I-1 and I-6.
  - "sebagai isomer" in the MDA-19 entries.
- **Esters and derivatives:** ecgonine and its esters and derivatives (II-28); pentavalent-nitrogen morphine derivatives (II-60).
- **Preparations and mixtures:** opium preparations (I-64); difenoxin and difenoxylate mixtures (III-14, III-15).
- **Plants:** opium poppy (I-1); coca (I-4, I-5); cannabis (I-8); khat (I-140); *Banisteriopsis caapi* and *Psychotria viridis* "nama lain AYAHUASCA" (I-141); *Mimosa tenuiflora* (I-142).
- **Not present:** no analogue or derivative clause of general reach, and no fungus or cactus.

**Two further official lists read**
- **BPOM Regulation 12/2025 on "Obat-Obat Tertentu yang Sering Disalahgunakan"** (certain drugs often misused):
  - Promulgated 2 May 2025, Berita Negara 2025 No. 300; in force.
  - It defines them as drugs "selain narkotika dan psikotropika" (other than narcotics and psychotropics).
  - Pasal 2 lists: a. tramadol, b. triheksifenidil, c. klorpromazin, d. amitriptilin, e. haloperidol, f. ketamin, g. dekstrometorfan.
  - It is outside the two lists the editor named (see section 7).
- **Permenkes 29/2023 on precursors:** Tabel I has 25 entries and Tabel II has 8. It was used only to check GHB, GBL and 1,4-butanediol, which are absent from it.

## 2. Sources

| Source | URL | Version | Used for | Read |
|---|---|---|---|---|
| Permenkes 15/2025 (narcotics), JDIH Kemenkes | https://jdih.kemkes.go.id/storage/documents/pdfs/2025permenkes015.pdf | BN 2025/989, in force | All three narcotics classes; Pasal 1–4 | Every chunk twice; 3 disputed points a third time |
| Same regulation, cross-check copies | https://peraturan.go.id/files/permenkes-no-15-tahun-2025.pdf ; https://peraturan.bpk.go.id/Download/407027/permenkes-no-15-tahun-2025.pdf | Same text | Counts 219/91/15; spot entries I-140, 141, 182, 193, 212, 213, II-43, II-89, III-11; the "RANCANGAN" label | Once each |
| Permenkes 14/2025 (psychotropics), JDIH Kemenkes | https://jdih.kemkes.go.id/storage/documents/pdfs/2025permenkes014.pdf | BN 2025/988, in force | All four classes; Pasal 1–4 | Every chunk twice; 5 disputed points a third time |
| BPOM Regulation 12/2025 | https://peraturan.go.id/files/peraturan-bpom-no-12-tahun-2025.pdf ; https://peraturan.bpk.go.id/Download/381859/peraturan-bpom-no-12-tahun-2025.pdf | BN 2025/300, in force | Pasal 1 angka 3; Pasal 2 | Twice (one per copy), plus a third reading |
| Permenkes 29/2023 (precursors) | https://jdih.kemkes.go.id/common/dokumen/2023permenkes029.pdf | BN 2023/642, in force | Absence of GHB, GBL and 1,4-butanediol | Twice |
| Law 35/2009 on Narcotics | https://peraturan.go.id/files/uu35-2009.pdf ; https://peraturan.bpk.go.id/Download/28105/UU%20Nomor%2035%20Tahun%202009.pdf | In force; Pasal 111–126 revoked by Law 1/2023; amended by the Job Creation laws (all per BPK) | Pasal 6 | Pasal 6(2)–(3) twice |
| Law 5/1997 on Psychotropics | https://peraturan.go.id/files/uu5-1997.pdf ; https://peraturan.bpk.go.id/Download/34479/UU%20Nomor%205%20Tahun%201997.pdf | In force (BPK) | Pasal 2 | Pasal 2(3)–(4) twice |
| BPK JDIH detail pages and search listings | peraturan.bpk.go.id/Details/343789, 343788, 322670, 322556, 320222, 275558, 38776, 45926 and searches | As shown on 2026-10-17 | Status, dates and revocation chains | Detail page and search listing |

**Facts from other sites.** None. Commercial and private sites (hukumonline, pasal.id, paralegal.id, literasihukum) appeared in search results but were not opened.

**Pages that could not be read**
- Lampiran I of Law 35/2009:
  - the peraturan.go.id text ends in Pasal 111 (72,364 characters; offsets beyond return nothing);
  - the BPK copy ends in Pasal 121 at every offset;
  - the Kemenkes copy (`UU No. 35 Th 2009 ttg Narkotika.pdf`) failed to fetch twice;
  - the farmalkes.kemkes.go.id page has no working download link;
  - the peraturan.go.id file `uu35-2009pjl.pdf` is only the Penjelasan (elucidation).
- Pasal 153 of Law 35/2009 was not reached.
- The annex of Law 5/1997 is in neither official copy.

## 3. How I searched

- **Finding the lists.**
  - WebSearch for the latest "Perubahan Penggolongan Narkotika" and "Penetapan dan Perubahan Penggolongan Psikotropika" regulations, then for 2026 successors (none found).
  - Then the BPK JDIH detail pages for status, and BPK searches for the revocation chains.
- **Reading the lists.** Each list was read from the issuing ministry's own portal (JDIH Kemenkes). For Permenkes 15/2025, this copy prints the promulgation date and Berita Negara number legibly; the peraturan.go.id and BPK copies print them as glyphs ("Д", "Ж").
- **Out-of-scope lists.** After finding that ketamine, tramadol and dextromethorphan are in neither list, I searched for BPOM's list of "Obat-Obat Tertentu", found Regulation 12/2025 (in force) and read its Pasal 1–2. For GHB, GBL and 1,4-butanediol I also read the precursor tables (Permenkes 29/2023).
- **Limits of the summarizer.**
  - WebFetch's summarizer would not quote passages longer than 125 characters.
  - So the long descriptive entries (opium, coca, cannabis) were read in full once (reading A).
  - Their decisive phrases were then confirmed one by one with YES/NO questions in a second, differently worded reading. Rows 9 and 10 (THC) were quoted whole in both readings.

## 4. Method of reading and comparison

- **Reading A** asked for "number | name exactly as printed". **Reading B** asked to "transcribe rows … character for character". Chemical names of every matched entry were read separately, twice, with differently worded prompts.
- **Script comparison** (Python, readings pasted inline, no files saved):

| Chunk | Exact agreement | Other outcome |
|---|---|---|
| Narcotics I, entries 1–80 | 71 | 9 where B gave only the head name of a long descriptive entry; content agrees; decisive phrases confirmed separately |
| Narcotics I, entries 81–219 | 137 | 2 differences |
| Narcotics II | 90 | 1 difference |
| Narcotics III | 5 | 10 where A added the chemical name; names agree; chemical names of 5 and 11 re-read twice |
| Psychotropics I–IV | 84 | 4 differences |
| Chemical names of matched entries | 52 of 52 | One flagged pair was my own paste slip (a stray character); both outputs were identical |
| Pasal 1–4 (both regulations) | All agree | Except "dan" in Permenkes 14/2025 Pasal 2(1) |
| Law 35/2009 Pasal 6(2)–(3); Law 5/1997 Pasal 2(3)–(4) | Agree | — |
| BPOM Regulation 12/2025 | List and letters agree | One word of the definition differs (see section 5) |

- **Matching.** Regular expressions with Indonesian spellings and aliases (e.g. KOKAINA, DEKSAMFETAMINA, KLONAZEPAM, KARFENTANIL, MEFEDRON, 4-KLOROMETKATINONA) were run over all agreed rows, 420 including the BPOM list. Every hit was checked by eye.
- **False hits rejected:**
  - ETIL AMFETAMINA (psychotropics IV-13) and DESKLOROETIZOLAM (psychotropics I-9);
  - fentanyl analogues (narcotics I-143, 149, 150, 161, 162) and 1P-LSD (I-197);
  - MDA-19 entries, N-HIDROKSI MDA and ETILON "bk-MDEA";
  - 3-MeO-PCP and the halogenated α-PVPs (I-132 to I-134);
  - METADONA INTERMEDIATE;
  - morphine and codeine N-oxides (II-59, II-60);
  - DESKLORO-N-ETIL KETAMIN.
- **Identified by chemical name, not by the item's name:**
  - "N-ETIL MDA" (I-42) is MDEA: (±)-N-ethyl-α-methyl-3,4-(methylenedioxy)phenethylamine.
  - "5-FLUORO-ADB" (I-95) is 5F-MDMB-PINACA: methyl 2-{[1-(5-fluoropentyl)-1H-indazole-3-carbonyl]amino}-3,3-dimethylbutanoate.

## 5. Disagreements between readings, and how each was settled

| # | Where | Reading A | Reading B | Settled by | Result | Bears on an item? |
|---|---|---|---|---|---|---|
| 1 | Narcotics I-188 (APP-BINACA alias) | 1H-INDAZOL | 1HINDAZOL | Third reading | "1HINDAZOL" | No |
| 2 | Narcotics I-209 (BZP) | N-BENZILPIPERAZIN | NBENZILPIPERAZIN | Third reading | "NBENZILPIPERAZIN" | No |
| 3 | Narcotics II-60 | kodeina-N-oksida | kodeina-Noksida | Third reading | "kodeina-Noksida" | No (codeine is III-5) |
| 4 | Psychotropics I-2 | comma before "2-FIuoro" | no comma | Third reading | No comma | No |
| 5 | Psychotropics I-6 | chemical name omitted | chemical name included | Third reading | Chemical name printed before the racemate clause | No |
| 6 | Psychotropics I-9 | comma before "nama lain" | no comma | Third reading | No comma | No |
| 7 | Psychotropics I-11 | comma before "nama lain" | no comma | Third reading | No comma | No |
| 8 | Permenkes 14/2025 Pasal 2(1) | no "dan" | "dan" before Golongan IV | Third reading | "dan" printed | No |
| 9 | BPOM 12/2025 Pasal 1 angka 3 | "selanjutnya disebut" (peraturan.go.id copy) | "selanjutnya disingkat" (BPK copy) | Third reading of the peraturan.go.id copy: "disebut" | Not settled across the two copies | No (that part is not quoted) |

**Other points that were not disagreements of content**
- In the reading of chemical names, reading A labelled the cocaine row "1". Its content ("Kokaina, metil ester-1-bensoil ekgonina.") is row 7 in reading B and in both name readings.
- For ADB-BUTINACA, both readings of the Kemenkes copy print the alias "ADBBINACA"; a spot reading of the peraturan.go.id copy gave "ADB-BINACA". This looks like a line-break hyphen.

## 6. Result

**Listed: 59 rows** (all ai-checked)

| List | Items |
|---|---|
| Narcotics Golongan I (37) | 2C-B 68, 2C-I 121, 2C-E 196, 2C-C 122, amfetamine 53, dexamfetamine 54, cannabis 8, THC 10 (and 9), cocaine 7, coca leaf 5, DMT 31, ayahuasca 141, carfentanil 144, acetylfentanyl 108, furanylfentanyl 147, heroin 19, LSD 36, MDMA 37, MDA 50, MDEA 42, mescaline 38, metamfetamine 61, PCP 57, psilocybin 47, psilocin 46, JWH-018 73, AM-2201 107, 5F-MDMB-PINACA 95, MDMB-4en-PINACA 182, ADB-BUTINACA 193, cathinone 35, mephedrone 75, MDPV 74, α-PVP 110, 3-MMC 213, 4-CMC 104, 2-MMC 212 |
| Narcotics Golongan II (7) | fentanyl 43, sufentanil 81, remifentanil 89, methadone 50, morphine 61, oxycodone 68, hydrocodone 33 |
| Narcotics Golongan III (2) | codeine 5, buprenorphine 11 |
| Psychotropics Golongan I (2) | flubromazolam 3, flualprazolam 4 |
| Psychotropics Golongan II (2) | methylphenidate 2, etizolam 5 |
| Psychotropics Golongan III (1) | cathine 5 |
| Psychotropics Golongan IV (5) | alprazolam 2, bromazepam 7, diazepam 11, clonazepam 30, lorazepam 36 |
| BPOM "Obat-Obat Tertentu" (3) | tramadol (a), ketamine (f), dextromethorphan (g); not narcotics or psychotropics |

**Not found: 17 rows, plus 1 "if named" item**
- **Not found (17):** 2C-T-7, 5-MeO-DMT, lisdexamfetamine, CBD, GHB, GBL, 1,4-butanediol, esketamine, *Mitragyna speciosa* (kratom), mitragynine, 7-hydroxymitragynine, tapentadol, *Salvia divinorum*, salvinorin A, 3-CMC, NEP, 4-BMC.
- **Draft rows (2):** CBD and esketamine are not named, but whether a clause covers them is open (section 7). The other 15 are ai-checked: both readings of every list agree that the name is absent.
- **"If named" item:** no cactus is named (searched: peyote, Lophophora, San Pedro, Trichocereus, Echinopsis, kaktus), so peyote or San Pedro has no row. It is listed in `not_found`.

**`medical_use`.** For every listed row this comes from the class definition in Pasal 1 (section 1); for the three BPOM rows, from BPOM's Pasal 1 angka 3. It is null for not-found rows.

## 7. Unsettled: for the editor

1. **Scope of the BPOM list.** Tramadol, ketamine and dextromethorphan are in neither the narcotics nor the psychotropics list. They are named by BPOM Regulation 12/2025, a list of drugs defined as "selain narkotika dan psikotropika" (other than narcotics and psychotropics). It lies outside the two lists you named. I recorded it, labelled "Listed outside the narcotics and psychotropics lists". If you rule it out of scope, these three rows become "Not found in the lists read".
2. **CBD.** Not named. Narcotics I-8 covers "hasil olahan tanaman ganja" (products made from the cannabis plant). Whether CBD extracted from the plant, or made synthetically, falls under it is not stated. The row is kept draft.
3. **Esketamine.** Not named. BPOM 12/2025 names "ketamin" with no salts or isomer clause (two readings). Whether esketamine is covered is for you. The row is kept draft.
4. **"RANCANGAN" label.**
   - The first page of Permenkes 15/2025 prints "RANCANGAN" (draft) in all three official copies, and the Kemenkes copy of Permenkes 14/2025 prints it too.
   - Yet the copies carry the signing and promulgation lines and Berita Negara numbers, and BPK lists both as in force. I read them as the promulgated texts.
   - You may wish to confirm against the Berita Negara.
5. **Base annexes unread.** The annexes of Law 35/2009 (Lampiran I) and Law 5/1997 could not be read (section 2). The current lists come from the 2025 regulations, whose annexes restate every class from entry 1.
6. **Minor, not decisive.**
   - The BPOM definition reads "disebut" in one copy and "disingkat" in the other.
   - BPOM Pasal 13 (a six-month transition for ketamine) was read once only.
