# What each drug is, in a few lines (first reader 703; second reader 704)

Read `BRIEF-common.md` in this folder first. The senior author (15 November 2026): "i think each drug page should have a
description for each drug that makes you understand what it is and its sources are validated". The description is the
first thing on a drug's page, above a menu of sections; today most pages show one line about the drug's family
(`data/site/families-plain.json`).

## Reader 703

For each of the 30 drugs in `data/site/substances.json` (`slug`, `name`, `cls` = family), write **two to four lines**
that let someone who has only heard the name understand what it is:
1. what it is and where it comes from (a plant, a medicine, a chemical made in labs; what family it belongs to, in a
   plain word such as stimulant or opioid);
2. what people take it for, or what it does, in a few plain words, as the sources put it (hedged as they hedge:
   "people can feel…");
3. how it comes and is known (the forms and the best-known other names), only if the sources say;
4. whether it is also a medicine, and for what, only if the sources say.
- These are identity lines. No risks, no warnings, no "highly addictive", no deaths, no law: those have their own
  checked answers on the page. No amounts, no routes compared, nothing on how to take it. Neutral words: "people who use
  it", never "abusers" or "addicts"; the drug's name, never "narcotic".
- Sources: the drug's own page at ADF (adf.org.au/drug-facts), EUDA/EMCDDA drug profiles, NIDA, WHO fact sheets, NHS,
  FRANK, Health Canada, The Level (NZ Drug Foundation), MedlinePlus for medicines. Two independent publishers per drug
  where they exist; every line anchored as `BRIEF-common.md` says. Pages group some drugs (2C-x, synthetic cathinones,
  synthetic cannabinoids, prescription opioids, methadone and buprenorphine, alkyl nitrites and inhalants, DMT and
  ayahuasca, GHB and GBL, fentanyl and its analogues): describe the group as the page's title names it.
- Where the sources do not support a line, leave it out and say so in `gaps`.

Output `data/verification/pages-2026-11-15/descriptions_703.json`:
`{"reader": "AI reader 703", "date": "2026-11-15", "drugs": {"<slug>": {"lines": [{"line": "...", "anchors": [...]}],
"gaps": "..."}}}`. Save after every drug; commit and push after every 10 drugs. Final message under 150 words: drugs
done, publishers used, gaps.

## Reader 704 (and readers 715 and 716: the 30 drugs are shared between three second readers, ten each)

Your drugs and your output file's name are in your instructions; the shape of the file is the one below, with your own
reader name. An anchor whose page cannot be opened (an approval that is not answered, an error) gets the verdict
`not-checked` with the reason in `note`: do not retry it and do not look for the passage elsewhere.

Check every anchor and line of `descriptions_703.json` as `BRIEF-common.md` says, and also:
- is each line an identity line (no risk, warning, amount or how-to)?
- is each line in our own words? A line that follows one source's sentence so closely that it is that page's wording
  (about six or more of its words in a row, or its sentence with a word or two changed) is `fix`: give a line that says
  the same and no more in plain words of our own. The same turn of phrase must not be repeated from drug to drug
  because one publisher uses it on every page (for example a family sentence about "messages travelling between the
  brain and the body"): say what the family word means in our own short words, as the sources support it.
- would someone who has only heard the drug's name understand what it is after these lines? If the first line does not
  do that, say so in `note`. Output `data/verification/pages-2026-11-15/descriptions_check_704.json`:
`{"reader": "AI reader 704 (second reader)", "date": "2026-11-15", "drugs": {"<slug>": [{"index": 0, "line_verdict":
"ok", "line": "<corrected line if fix>", "anchors": [{"index": 0, "verdict": "confirmed", "quote": "", "where": ""}],
"note": ""}]}}`. Final message under 150 words: counts by verdict and every line you fixed or dropped.
