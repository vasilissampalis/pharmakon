# EU-wide control (Annex of Framework Decision 2004/757/JHA), 2026-10-16

- First reading: the editor, through WebFetch and WebSearch (`first-reading-log.md`).
- Second reading: AI reader 2, blind (it saw only `second/tasks.json`: five source URLs and the questions), 35 calls,
  no refusals (`second/results.json`, `second/calls.jsonl`).
- Comparison (editor): every fact used in the new rows was found by both readings: the Annex as inserted by Directive (EU)
  2017/2103 (point 3: 2C-I, 2C-T-2, 2C-T-7, TMA-2; point 5: mephedrone; point 8: MDPV with 25I-NBOMe, AH-7921 and
  methoxetamine; point 10: alpha-PVP; point 12: acryloylfentanyl); Delegated Directive (EU) 2019/369 (furanylfentanyl and
  four others); (EU) 2021/802 (MDMB-4en-PINACA, 4F-MDMB-BICA); 3-MMC and 3-CMC by the act of 18 March 2022; (EU) 2025/2062
  of 14 October 2025 (2-MMC, 4-BMC, NEP; in force 12 January 2026; national control by 12 July 2026).
- One difference between sources, not between readers: the Commission's report COM(2022) 251 prints the 18 March 2022
  act as "(EU) 2022/1552"; the EUDA Drugs Library and the Publications Office give (EU) 2022/1326, and the Council cover
  note 7430/22 shows the Commission's document number C(2022) 1552. The rows use (EU) 2022/1326.
- Facts read by one reader only are not used (e.g. the date of Directive (EU) 2017/2103, the 18 February 2023 deadline
  of (EU) 2022/1326).
- Applied with `rows.py --apply "(EU) 2022/1326"`: new ai-checked EU rows on 2c-x, synthetic-cathinones,
  synthetic-cannabinoids and fentanyl-and-analogues; on the other pages the general EU row now says that none of the
  substances named on the page is in the Annex as read.
