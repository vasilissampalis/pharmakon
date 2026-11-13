# W2 report: Russian Federation

Checked on 2026-10-17 by AI reader W2. Output: `/home/claude/drug-encyclopedia/data/legal/_incoming/russia.json` (77 rows, keyed by the site's drug pages).

## 1. Sources

| Source | URL | Version printed |
|---|---|---|
| Постановление Правительства РФ от 30.06.1998 № 681 with the Перечень наркотических средств, психотропных веществ и их прекурсоров, подлежащих контролю в Российской Федерации (Lists I–IV, Notes 1–6). Copy posted by Росздравнадзор (Roszdravnadzor, the federal medicines regulator) | https://roszdravnadzor.gov.ru/i/upload/images/2026/3/30/1774879151.29078-1-3386659.pdf | «ред. от 11.06.2025», printed on Roszdravnadzor's page for the act (https://roszdravnadzor.gov.ru/drugs/documents/167, dated 30.03.2026) and again on https://www.roszdravnadzor.gov.ru/drugs/licensingdrugs. The PDF's pages carry the stamp "11-195(09)/26ВН" and "27.03.2026" |
| Постановление Правительства РФ от 27.11.2010 № 934 (plants list), operative text only, in Российская газета (official gazette), No. 280 (5359), 10.12.2010 | https://rg.ru/documents/2010/12/10/rasteniya-dok.html | original text; the annexed plant list is not on the page |

All facts in the JSON come from the first source. The second only shows that a separate official plants list exists.

## 2. How I searched

Official portals tried first, all refused by WebFetch (robots or site block):
- pravo.gov.ru (proxy/ips, /ips), ips.pravo.gov.ru, publication.pravo.gov.ru: ROBOTS_DISALLOWED.
- government.ru and static.government.ru: ROBOTS_DISALLOWED.
- мвд.рф (regional page): ROBOTS_DISALLOWED. web.archive.org: blocked.

Other official pages:
- minzdrav.gov.ru page for Resolution 681: published and last updated 08.04.2008, so out of date. Not used.
- Roszdravnadzor: current copy of Resolution 681 (above). Used.

Currency. As a finding aid only, the ConsultantPlus page for Resolution 681 showed «ред. от 11.06.2025» on 2026-10-17. ConsultantPlus legal news of 6 Feb 2026 reported an MVD draft to add 16 positions; I found no sign that it was adopted. Neither is used as a fact. See unsettled.

Plants list (Resolution 934). I searched Roszdravnadzor (documents, licensing and import pages), Minzdrav, FSVPS, Rossiyskaya Gazeta and FAOLEX. Only commercial databases (ConsultantPlus, Garant, Kontur, Kodeks) and a municipal copy of a 2012 Kodeks edition (gubkin.city) carry the annex; none of them is official.
- Rossiyskaya Gazeta prints only the operative text of Resolutions 934 (2010) and 1002 (2012).
- Its publication of Resolution 827 of 12.07.2017 (https://rg.ru/2017/07/31/narkotiki-dok.html, read once, used here only as corroboration) gives the amendment text. That text adds «Мимоза хостилис (растение вида Mimosa tenuiflora)» to the plants list, adds etizolam and fluorobromazolam to List III, and adds furanylfentanyl to List I. This agrees with the readings below.
- I found no official pages for the later amending acts 1041 (2019), 1140 (2020) and 135 (2024).

Potent-substances list (Resolution 964 of 29.12.2007). I know it only from search results and found no official copy. Roszdravnadzor's import page links a different act (Resolution 930 of 1996) as a .docx file, which WebFetch could not read.

Finding aids consulted, never used for facts: consultant.ru, kontur-extern.ru (Kontur.Normativ), gubkin.city, pharmznanie.ru, s-standard.ru, gxpnews.net, and two FAOLEX files that turned out to be unrelated acts.

## 3. How the list was read

WebFetch's summarizer refuses long verbatim copying (it caps each quotation at 125 characters). So every part of the Perechen was read as a name index:
- Reading A asked for numbered lines "n. name +П", where +П marks «и его/их производные».
- Reading B, worded differently, asked for "n ;; name ;; derivatives: yes/no".

Each chunk was read in two separate WebFetch calls. The whole PDF fits in one WebFetch window (no `offset` was needed), so chunks were set by entry position.

| Part | Positions | Chunks | Agreement on first comparison |
|---|---|---|---|
| List I, narcotic drugs | 401 | 6 (1–70, 71–140, 141–210, 211–280, 281–350, 351–401) | 397 rows identical; 4 disagreements |
| List I, psychotropic substances | 20 | 1 | 20/20 |
| List I, precursors | 55 | 1 | 55/55 |
| List II, narcotic drugs | 77 | 2 | 76/77 |
| List II, psychotropic substances + general provisions | 15 | 1 | 15/15; provisions see §4 |
| List III | 108 | 2 | 107 rows identical; glyph issues, see §4 |
| List IV, Table I | 106 | 2 | 105/106 |
| List IV, Tables II and III | 37 and 22 | 1 | 37/37 and 22/22 |
| General provisions after List I; Notes 1–6 | 4 + 6 | 1 | 10/10 identical |
| Headings of Lists I–IV and of the Перечень | – | 1 | identical |

How the comparison worked:
- A Python script compared each pair of readings, with the readings passed on stdin so that no extra files were written.
- The script normalised both readings first: Cyrillic/Latin look-alike letters, whitespace and dashes, and the «и его производные, за исключением…» clause.
- It then aligned the two readings with difflib and compared names and derivative flags (List IV: names and concentration thresholds).
- Rows on which both readings agree are recorded as ai-checked.

## 4. Every disagreement and how it was settled

1. **List I, RTI-126.** A: «8-Метил-2-(3-метил-1,2,4-оксадиазол-5-ил)-3-фенил-8-азабицикло[3.2.1]октан (RTI-126)». B put "RTI-126" first. A third reading found that the printed entry begins "8-Метил-2-", so A is right.
2. **List I, 5-MeO-MIPT.** A: «…пропан-2-амин5-MeO-MIPT)». B: «… (5-MeO-MIPT)». A third reading found the entry printed with no space and no opening parenthesis (a typo in the source), so A is right.
3. **List I, JWH-194 and JWH-197.** A: «2-Метил-1-пентил-1H-индол-3-ил-(4-метил-1-нафтил)метан (JWH-194)» and «…(4-метокси-1-нафтил)метан (JWH-197)». B began both with «(4-Метил/Метоксинафталин-1-ил)…». A third reading found that both begin "2-Метил-1-пентил-1H-индол-3-ил-", so A is right.
4. **List I, the line «(введено Постановлением Правительства РФ от 29.07.2017 N 903)».** A counted it as entry 232; B left it out. A third reading found it is an amendment note between RH-34 and 5-MeO-DIBF, not a position. So the part has 401 positions, and A's numbering in that chunk was one too high.
5. **List II, dihydrothebaine entry.** A truncated the long chemical name; B gave the ending. A third reading found that it ends «(18),14-тетраен(дигидротебаин)», so B is right.
6. **List II, general provisions.** A quoted only their opening words, because of its quotation limit; B gave them in full. A third reading confirmed B's full text: isomers, stereoisomers and salts.
7. **List III, GHB entries.** A wrote «…соли γ-оксимасляной кислоты» and said it had restored the γ. B wrote «…соли -оксимасляной кислоты» and also returned a lone line "γ" between Клоксазолам and Клоназепам. A third reading confirmed that in the text layer the γ is attached to neither entry («- оксимасляная кислота», «…-оксимасляной кислоты») and that a lone "γ" stands after "Клоксазолам". Settled as follows:
   - The two entries are recorded as «[γ]-оксимасляная кислота» and «4-гидроксибутират натрия и другие соли [γ]-оксимасляной кислоты», with a note on the displaced glyph.
   - The stray γ is not a position. List III has 108 positions.
8. **List III, the closing provision «Соли веществ, перечисленных в данном списке, если существование таких солей возможно».** A listed it as entry 109; B gave it as a general provision. It is a general provision.
9. **List IV, Table I, the MAPA entry.** A: «метил- -фенилацетоацетат»; B: «метил-α-фенилацетоацетат». A third reading found the Greek letter missing in the text layer. This is not one of the items, so it was left as is.
10. **Look-ups.** One placed «1-(5-Фторпентил)-1H-индол-2,3-дион» in List IV; the other look-up and both full readings place it among the List I precursors. List I precursors is right (not one of the items).

Numbering-only differences had no effect on content: A renumbered Table I from 1 in its second chunk, and A left one List I chunk unnumbered.

## 5. Matching

- **Script match.** The 77 items were matched by Russian and Latin name patterns against all 704 settled entries of Lists I–III and List IV Table II, then against all 126 active rows of List IV Tables I and III. Every hit was checked by eye. These hits were false positives and were discarded: bk-2C-B and 2C-B-AR (for 2C-B); DOC and DOET (for amphetamine); 3-furanylfentanyl (for furanylfentanyl); the methadone intermediate (for methadone); the norpseudoephedrine precursor, which expressly excludes cathine (for cathine). Harmine (List II) is recorded only as context on the ayahuasca row.
- **Absences.** Two differently worded look-ups over the whole document, covering 60 search strings, agreed on every string. They also found the excluded position «Позиция исключена с 1 января 2013 года. d-Лизергид (ЛСД, ЛСД-25)».
- **Wording and placement.** The exact wording of the 15 «…и его производные» entries quoted in the JSON was read twice more. The list and part of 26 key entries were checked once more and matched the full readings.
- **Numbers.** The Перечень prints no entry numbers, so none are recorded.

## 6. Results

**51 items named (ai-checked):**
- List I, narcotic drugs: 2C-B, 2C-T-7, cannabis and cannabis resin, Δ9-THC (via «Тетрагидроканнабинолы (все изомеры) и их производные»), coca leaf, DMT, acetylfentanyl, furanylfentanyl, heroin (printed twice), mitragynine, 7-hydroxymitragynine, MDMA, MDA, MDEA, mescaline, methadone, methamphetamine, PCP, hydrocodone, psilocybin, psilocin, salvinorin A, JWH-018, mephedrone, MDPV.
- List I, psychotropic substances: amfetamine (and its derivatives), methylphenidate, cathinone, cathine.
- List II, narcotic drugs: cocaine, fentanyl, carfentanil, sufentanil, remifentanil, buprenorphine, morphine, oxycodone, codeine.
- List II, psychotropic substances: ketamine.
- List III: diazepam, alprazolam, clonazepam, lorazepam, bromazepam, etizolam, flualprazolam, flubromazolam (as «Фторбромазолам»), dextromethorphan, GHB, GBL.
- List IV, Table II (15 % or more): 1,4-butanediol. Butyrolactone and its isomers are also listed there.

**19 items not named but possibly covered by a generic clause (draft):** 2C-I, 2C-E, 2C-C, 5-MeO-DMT, LSD, AM-2201, 5F-MDMB-PINACA, MDMB-4en-PINACA, ADB-BUTINACA, alpha-PVP, 3-MMC, 3-CMC, 4-CMC, NEP, 2-MMC, 4-BMC and lisdexamfetamine fall under the derivative clause (Note 6); dexamfetamine (List I) and esketamine (List II) under the isomer clauses.

**7 items not found in the lists read:**
- Cannabidiol is ai-checked.
- Tramadol, tapentadol, Mitragyna speciosa, Salvia divinorum, ayahuasca and peyote/San Pedro are draft, because official lists I could not read probably decide them.

**Points a reader may not expect:** hydrocodone and methadone are in List I (circulation prohibited); carfentanil is in List II; methylphenidate is in List I; dextromethorphan is in List III; LSD has had no position of its own since 1 January 2013.

## 7. Unsettled (for the editor)

1. **Currency.** The Roszdravnadzor copy is «ред. от 11.06.2025», posted 30.03.2026. I could not check for amendments made after March 2026 from an official source, because the official portals refuse automated fetching. Confirm on pravo.gov.ru in a browser.
2. **Plants list (Resolution 934) not read.** Commercial databases, used only as leads, show it naming Mitragyna speciosa, Salvia divinorum, mescaline-containing cacti (Lophophora williamsii and other species), Banisteriopsis caapi and Psychotria viridis. This decides four rows: kratom plant, Salvia divinorum, peyote/San Pedro, ayahuasca.
3. **Potent-substances list (Resolution 964) not read.** A news report, used only as a lead, says Resolution No. 667 of 27.05.2019 added tapentadol to it from 1 December 2019. I found no lead for tramadol.
4. **Derivative and isomer clauses** for the 19 items above. Whether each counts as a "derivative" under Note 6 is a chemical judgement that the list does not make.
5. **Flubromazolam is matched by name only:** the list prints «Фторбромазолам» with no chemical name.
6. **Other possible national lists were not searched.** For example, anything kept on the Ministry of Internal Affairs site, which refuses automated fetching.
