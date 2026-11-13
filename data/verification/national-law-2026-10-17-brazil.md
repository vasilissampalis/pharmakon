# W2 report: Brazil's own list of controlled drugs

Checked on 2026-10-17 by AI reader W2, using WebSearch and WebFetch only.

Output: `/home/claude/drug-encyclopedia/data/legal/_incoming/brazil.json`. It has 77 records for 76 items; THC has two records. The "if named" item ayahuasca is not recorded because no list names it.

## 1. The official list and its sources

Brazil's list is **Anexo I of Portaria SVS/MS nº 344, de 12 de maio de 1998**. Anvisa keeps it up to date with resolutions of its Collegiate Board (RDC), and each update republishes the whole annex under a running number ("ATUALIZAÇÃO N.").

| Source | URL | Version | Used for |
|---|---|---|---|
| RDC Anvisa nº 1.036, de 9 de julho de 2026, on AnvisaLegis (Anvisa's legislation portal) | https://anvisalegis.datalegis.net/action/ActionDatalegis.php?acao=abrirTextoAto&link=S&tipo=RDC&numeroAto=00001036&seqAto=000&valorAno=2026&orgao=RDC/DC/ANVISA/MS&codTipo=&desItem=&desItemFim=&cod_modulo=293&cod_menu=8499 | Atualização N. 101, current. Art. 2 puts it in force on publication. | All lists A1 to F1 and their adendos, list headings, F2 a) items 1 to 122 |
| RDC Anvisa nº 999, de 24 de novembro de 2025, PDF on gov.br/anvisa | https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/controlados/RDC9992025.pdf/@@display-file/file | Atualização N. 97 | F2 a) items 100 to 184, F2 b) class headings, F2 c) clauses 1 to 1.4.1 |
| RDC nº 767, de 8 de dezembro de 2022, PDF on gov.br/anvisa | https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/controlados/RDC7671.pdf/@@display-file/file | Atualização N. 83 (2022) | Only for F2 c) clauses 1.4 to 1.5.1, F2 d) and F2 adendo clauses 1 to 9, which no current copy reaches |
| RDCs Anvisa nº 1.011, 1.017, 1.021 and 1.023 of 2026, articles before the annex (AnvisaLegis; same URL pattern with numeroAto 00001011, 00001017, 00001021, 00001023) | see JSON `sources` | Atualizações N. 98, "98" (sic), 99 and 100 | The changes made after Atualização N. 97 |
| EUDA initial reports on NEP and 2-MMC | https://www.euda.europa.eu/node/32745_fi ; https://www.euda.europa.eu/publications/initial-reports/initial-report-2-mmc_en | web pages | Only the two substances' IUPAC names, used to match them |

Two non-official sites helped me find the texts, and no fact was taken from them. LegisWeb gave the RDC numbers for Atualizações 97, 100 and 101 and showed that each update republishes the whole annex. An Atlas Público news item gave the DOU link for RDC 1.023.

## 2. How the current version was established

- The DOU (in.gov.br, pesquisa.in.gov.br) is closed to WebFetch by robots.txt, so I used Anvisa's own legislation portal, AnvisaLegis.
- AnvisaLegis's "Extrato DOU Anvisa" page listed acts published up to 16 October 2026.
- **RDC 1.036/2026 (Atualização N. 101)** is the latest annex update. I opened every RDC numbered from 1.037 to 1.045/2026. None updates Anexo I; they cover reference medicines, airports, laboratories, saneantes, medical gases, simplified registration, clinical-analysis services, BA/BE studies and artisanal cosmetics. Numbers 1.046 to 1.048 return the same "Este ato está sendo processado" message as the non-existent number 9999, so they are not in the database.
- Updates since Atualização N. 97 (RDC 999/2025):
  - RDC 1.011 of 30 January 2026 (N. 98) added C1 adendo 15 and E adendos 13 to 15, on Cannabis with up to 0.3% THC.
  - RDC 1.017 of 20 February 2026 also prints "ATUALIZAÇÃO N. 98". It added fenfluramina to A3 and cenobamato to C1, removed fenfluramina from F4, and altered A3 adendo 4.
  - RDC 1.021 of 9 April 2026 (N. 99) added protodesnitazeno to F1, desalquilgidazepam and NMDMSB to F2, and fenibut to F4, and altered F2 adendo 16.
  - RDC 1.023 of 11 May 2026 (N. 100) changed adendos only. Its items 2.4 to 2.7 took effect on 4 August 2026.
  - RDC 1.036 of 9 July 2026 (N. 101) added MMDPPA to D1 and dimetocaína to F1.
  - Each of these articles was read twice, and the two readings agree.
- No update after N. 97 excludes anything from Lista F2.
- These RDCs are not annex updates: 1.001 to 1.009 (2025/2026), 1.014, 1.016, 1.018 to 1.020, 1.022 and 1.024 to 1.035. RDC 1.010 could not be opened under either year. RDCs 1.012, 1.013 and 1.015/2026, which the List E adendo cites as the Cannabis rules, were not opened. Because the annex numbers run 97, 98, "98", 99, 100, 101 across RDCs 999, 1.011, 1.017, 1.021, 1.023 and 1.036, no annex update is missing.
- The currency checks were single readings of each act's ementa, not of list text.

## 3. What could and could not be read

WebFetch's copy of every full annex text is cut off before the end of the annex.

- **AnvisaLegis, RDC 1.036.** The page text is 88,776 characters and ends at F2 a) item 122 at every offset. I tried `offset` values of 40,000, 60,000 and 80,000, the `link=N` variant and a `desItem` view; all end at the same place. The public permalink view is cut even earlier, inside the C3 adendo. The pages of RDC 1.011, 1.017, 1.021 and 1.023 end between F2 a) items 106 and 125.
- **gov.br PDFs.**
  - RDC 999/2025 ends inside F2 c) clause 1.4.1.
  - RDC 985/2025 ends at F2 a) item 179.
  - RDC 767/2022 ends at F2 adendo clause 9.
  - On antigo.anvisa.gov.br, RDC 784/2023 ends in F2 b), and RDC 877/2024 and 936/2024 end in F2 a).
  - Anvisa's English translation of RDC 970/2025 ends in F2 Addendum 1.2. I did not use it.
- **Read in the current text**, entries in every case and adendos where listed:
  - A1, A2, A3, B1, B2, C1, D1, D2, E and F1, with their adendos;
  - C2, C3 and C5, entries only;
  - F2 a) items 1 to 122;
  - the list headings.
- **Read in Atualização N. 97:** F2 a) items 100 to 184 (the end of a)), the F2 b) class headings, and F2 c) clauses 1 to 1.4.1.
- **Read only in the 2022 text (N. 83):** F2 c) clauses 1.4 to 1.5.1, F2 d), and F2 adendo clauses 1 to 9.
- **Not read in any version:** the current F2 adendo (it has at least 16 clauses, since RDC 1.021 altered clause 16), Lista F3 and Lista F4.

## 4. Method

- **Readings.** Each chunk was read in two WebFetch calls with differently worded prompts and output formats: `LIST | number | name` in one, `number ;; name` in the other.
- **Summariser limits.** WebFetch's summariser will not quote more than 125 characters at a time.
  - Entry names came back exactly.
  - Long systematic chemical names were cut, at different points in the two readings.
  - Adendo clauses came back as close paraphrases in both readings. I compared them by eye on every substance, number and exception they name.
  - Where the wording decides an answer, I asked separately for the opening words (15 words at most). Those quotations were given identically in two readings.
- **Comparison by script.** Python, run from the shell with the readings pasted in, so that no files other than the two outputs were written. A row counts as agreed if the two readings are identical. It also counts if the primary names are identical and the rest matches after whitespace and dashes are normalised, comparing only the common prefix where one reading was cut.
- **Matching.**
  - One script searched all 774 agreed entries with accent-insensitive patterns for each of the 77 items, covering the Portuguese INNs, code names and chemical names.
  - I checked every hit by eye. The false positives I discarded:
    - 2C-I-NBF, for 2C-I
    - Lisdexanfetamina, for dexamfetamine
    - "BUTIRIL FENTANIL", for fentanyl
    - Tetrahidrofuranilfentanil, for furanylfentanyl
    - "1-CICLOPROPIONIL LSD", for LSD
    - "N-ETIL MDA", the MDEA synonym, for MDA
    - "BK-MDEA" (etilona), for MDEA
    - the methadone intermediate, for methadone
    - 4-MEAPP, for NEP
  - Two items were identified by printed chemical name: NEP (EUDA's IUPAC name 2-(Ethylamino)-1-phenylpentan-1-one equals F2 a) item 84 'ALFA-EAPP') and 2-MMC (see section 7).

## 5. Results

**Found: 74 items.** 73 are named in a list; 2-MMC is covered by a structural class only, marked draft.
**Not found: 2** (dextromethorphan, 1,4-butanediol).
**Not recorded: 1** "if named" item that no list names (ayahuasca).
**Unsettled: 3 points** (section 7).

In the table, N. 97 numbers are marked; the current number is that plus one or two (see section 7).

| Page | Item | Brazil |
|---|---|---|
| 2c-x | 2C-B, 2C-I, 2C-E, 2C-C, 2C-T-7 | F2 a) items 6, 11, 9, 7, 13 |
| 5-meo-dmt | 5-MeO-DMT | F2 a) 52 |
| amphetamine | amfetamine, dexamfetamine, lisdexamfetamine | A3 items 1, 4, 11 |
| benzodiazepines | diazepam, alprazolam, clonazepam, lorazepam, bromazepam, etizolam, flualprazolam, flubromazolam | B1 items 31, 3, 21, 57, 10, 39, 42, 43 |
| cannabis | cannabis | E 1 (*Cannabis sativa* L.). Resin is covered by E adendo 14; up to 0.3% THC is excepted to C1 (E adendo 13, C1 adendo 15). |
| cannabis | THC | A3 5 (Dronabinol, synthetic only per A3 adendo 6) and F2 a) 178 (N. 97) 'TETRAHIDROCANNABINOL ou THC' |
| cannabis | CBD | C1 25 'Canabidiol (CBD)', synthetic only (C1 adendo 13) |
| cocaine | cocaine, coca leaf | F1 22; E 4 (*Erythroxylum coca* Lam., the plant; the leaf is not named) |
| dmt-ayahuasca | DMT | F2 a) 113. Ayahuasca is not named, so not recorded. |
| dxm | dextromethorphan | Not found; excepted from the A1 isomers clause (A1 adendo 1.1 and 1.2) |
| fentanyl-and-analogues | fentanyl, sufentanil, remifentanil | A1 42, 88, 87 |
| fentanyl-and-analogues | carfentanil, acetylfentanyl, furanylfentanyl | F1 19, 8, 32 (F1 adendo 3 allows veterinary carfentanil) |
| ghb-gbl | GHB, GBL | B1 49, 48 |
| ghb-gbl | 1,4-butanediol | Not found |
| heroin | heroin | F1 33 'HEROÍNA ou DIACETILMORFINA' |
| ketamine | ketamine, esketamine | B1 17 'Cetamina', 33 'Escetamina' |
| kratom | *Mitragyna speciosa* | E 6 |
| kratom | mitragynine, 7-hydroxymitragynine | F1 38, 6 |
| lsd | LSD | F2 a) 1 '(+) – LISÉRGIDA ou LSD; LSD-25' |
| mdma | MDMA, MDA, MDEA | F2 a) 149, 176 'TENANFETAMINA ou MDA', 148 'MDE ou MDEA' (all N. 97) |
| mescaline | mescaline | F2 a) 152 (N. 97) |
| mescaline | peyote | E 5 *Lophophora williamsii* Coult.; E adendo 3 calls it "cacto peyote". San Pedro is not named. |
| methadone-buprenorphine | methadone, buprenorphine | A1 58, 17 |
| methamphetamine | methamphetamine | F2 a) 154 (N. 97); levometanfetamina is a separate entry, 138 (N. 97) |
| methylphenidate | methylphenidate | A3 12 |
| pcp | PCP | A3 7 'Fenciclidina' |
| prescription-opioids | morphine, oxycodone, hydrocodone, tapentadol | A1 65, 77, 44, 89 |
| prescription-opioids | codeine, tramadol | A2 2, 13 |
| psilocybin | psilocybin, psilocin | F2 a) 170, 171 (N. 97) |
| salvia-divinorum | *Salvia divinorum* | E 9 |
| salvia-divinorum | salvinorin A | F2 a) 174 (N. 97) |
| synthetic-cannabinoids | JWH-018, MDMB-4en-PINACA | F2 a) 126, 142 (N. 97) |
| synthetic-cannabinoids | AM-2201, 5F-MDMB-PINACA, ADB-BUTINACA | F2 a) 89, 41 (printed '5F-ADB'), 77 |
| synthetic-cathinones | cathinone | F2 a) 98 |
| synthetic-cathinones | cathine | A3 2 |
| synthetic-cathinones | mephedrone | F2 a) 151 (N. 97) 'MEFEDRONA' |
| synthetic-cathinones | MDPV | F1 35 |
| synthetic-cathinones | alpha-PVP, 3-MMC, 3-CMC, 4-CMC | F2 a) 87, 19, 16, 25 |
| synthetic-cathinones | NEP | F2 a) 84 'ALFA-EAPP', matched by chemical name |
| synthetic-cathinones | 2-MMC | Not named; F2 c) structural class (draft) |
| synthetic-cathinones | 4-BMC | F2 a) 23 |

## 6. Disagreements between readings and how they were settled

1. **D1 items 1 and 2.** Reading 1 gave "1-boc-4-AP" and "1-boc-4-piperidona"; reading 2 gave "1.1-boc-4-AP" and "1.1-boc-4-piperidona". A third reading showed the item number fused to the name: the entries are printed "1." and "2." followed by "1-boc-…". Settled for reading 1. None of the 77 items is affected.
2. **A1 adendo clause 1 (isomers).** Reading 1 said only that "certain named isomers are excluded". Reading 2 named dextromethorphan and dextrorphan. A third reading named them too and quoted "exceto os isômeros dextrometorfano, (+)3-metoxi-N-metilmorfinan, e o Dextrorfano". Settled by readings 2 and 3.
3. **F2 a) items 1 to 122 (current text).** 96 rows are identical. 26 rows differ only in spacing, dash type, or the point where the summariser cut a long chemical name: items 3, 4, 5, 28, 31, 38, 40, 43, 44, 50, 64, 69 to 72, 74, 76, 78, 79, 82, 89, 92, 96, 101, 113 and 119. No substantive disagreement.
4. **F2 a) items 100 to 184 (N. 97).** 52 rows identical and 33 equal on the common prefix after cutting. No substantive disagreement.
5. **Format differences that are not disagreements.**
   - D1/D2 reading 1 printed the literal word "LIST" as the list code. I relabelled the rows by where the numbering restarts: D1 has 35 items and D2 has 13.
   - F1 reading 1 reported in a note that item 54 is missing and item 55 is printed twice; reading 2 wrote "54 ;; ABSENT". The comparison used one row for 54 in both.
   - B1 reading 1 was entered into the script as its 95 names in printed order; its numbering in the tool output was 1 to 95 with no gaps.
6. **Adendos with differently split clauses.** The A2, A3, B1, B2, C1 and F1 adendos were split into sub-clauses differently in the two readings, for example 1 and 1.2 against 1.1 and 1.2. Reading 2 of the E adendo left out clauses 10 and 11, which reading 1 shows as "(Excluído)". In every case the content agrees.
7. **A1 adendo 5.** Only reading 2 gave the oxycodone dose limit (40 mg per unit). It is not recorded.
8. **RDC 1.011's entry-into-force date.** Only reading 1 gave it (4 August 2026). The JSON uses instead RDC 1.023 Art. 6, which both readings give as 4 August 2026 for its items 2.4 to 2.7.

Rows agreed in all lists:

| List | Rows agreed |
|---|---|
| A1 | 94 |
| A2 | 13 |
| A3 | 14 |
| B1 | 95 |
| B2 | 8 |
| C1 | 213 (numbering contiguous) |
| C2, C3, C5 | 5, 3, 31 |
| D1 | 35 (after the third reading) |
| D2 | 13 |
| E | 9 |
| F1 | 56 |
| List headings | 15 |

## 7. Unsettled: for the editor

1. **2-MMC (draft).** 2-MMC is not named. I recorded it as covered by F2 c), the structural class of synthetic cathinones.
   - Clause 1 reads "Qualquer substância que apresente uma estrutura 2-aminopropan-1-ona (estrutura C1)".
   - The match uses EUDA's IUPAC name for 2-MMC.
   - Clauses 1 to 1.4 come from N. 97; clauses 1.4.1 to 1.5.1 and adendo clauses 7 and 8 come only from the 2022 text.
   - The structural reading is mine. Please decide whether to show it, or to show "Not named (possibly covered by the structural class)".
2. **F2 adendo, F3 and F4 could not be read.** The not-found results for dextromethorphan and 1,4-butanediol do not cover them. What the amending acts say about these parts:
   - F4 now includes fenibut (RDC 1.021/2026) and no longer includes fenfluramina (RDC 1.017/2026).
   - F2 adendo 16 was altered in 2026; its new wording is not printed in the amending article.
   - The 2022 F2 adendo excepted Anvisa-registered THC medicines (clause 6) and named six THC isomers (clause 1.2). The current wording is unknown.
   - The editor may want to read the DOU of 13 July 2026, or Anvisa's own PDF of RDC 1.036 if it can be obtained, for these parts.
3. **Item numbers after F2 a) item 122.** These 13 items carry their N. 97 numbers: JWH-018, MDMB-4en-PINACA, MDEA, MDMA, mephedrone, mescaline, methamphetamine, psilocybin, psilocin, salvinorin A, MDA, and the THC entry.
   - RDC 1.021/2026 inserted desalquilgidazepam at item 103, so numbers shift by +1 from DET onward. A single reading of RDC 1.021's page also shows Eutilona at 123, one above its N. 97 number of 122.
   - It also inserted NMDMSB, whose position could not be read. Numbers after it shift by +2.
   - Each JSON note gives both possible current numbers.

## 8. Other observations

- Two different RDCs (1.011 and 1.017 of 2026) print "ATUALIZAÇÃO N. 98" on their annexes. Both were read twice.
- Several items are not in the proscribed List F:
  - PCP is in A3, with the 'A' prescription notification.
  - Etizolam, flualprazolam and flubromazolam are in B1, with the 'B' notification.
  - Ketamine, esketamine, GHB and GBL are also in B1.
- MDPV is in F1 (the proscribed narcotics), not F2.
- A3 item 14 prints "Tanfetamina". It was not matched to MDA, which F2 prints as "TENANFETAMINA ou MDA".
- `medical_use` records what the list itself prints. For lists A1 to C1 that is the prescription type in the list heading, for example 'Sujeitas à Notificação de Receita "A"'. Adendo clauses on medicines are added where they exist: ketamine and esketamine only in health establishments, buprenorphine patches, codeine and tramadol preparations up to 100 mg per dose, registered Cannabis medicines, and veterinary carfentanil.
- AnvisaLegis does not print the DOU publication dates of these RDCs, so no publication date is recorded. LegisWeb's dates were not used.
