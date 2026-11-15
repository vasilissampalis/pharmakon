# Each seller's own page for each drug's test kit (finder 705; verifier 706)

Read `BRIEF-common.md` in this folder first (its rules on reading pages apply; here the pages are shops, read only for
what they sell, never for health facts). Each drug page lists sellers of drug-checking tests that ship to the reader's
country (`data/site/tests-world.json` → `sellers`: 11 sellers with `name` and `url`). All links go to the shop's front
page. The senior author (15 November 2026) clicked Bunk Police from the cannabis page and landed on a general front
page: "there is nothing about cannabis in the link this is generalized and difficult to use if a user wants to buy
something they should be able to buy it immediately ... the links should be individualized for each drug page". Bunk
Police, for one, has "Shop By Substance" pages (Amphetamine, Cannabis, Cocaine, DMT, Fent, Heroin, Ketamine, LSD, MDMA,
Mescaline, Methamphetamine, Nitazene, Psilocybin, Xyl test kits) and "How to test …" guides.

## Finder 705

For each of the 11 sellers and each of the 30 drugs in `data/site/substances.json`, find the seller's own page that
sells the test for that drug: a by-substance category page where the seller has one, otherwise the product page of the
kit the seller itself names for that drug. Start from the seller's shop page and menus (WebFetch; ask for the links
with their exact URLs and link texts). Record only URLs you have opened and seen to be about that drug on that seller's
site; never build a URL by guessing its pattern. No page for a drug at a seller: leave it out. For the opioid pages
(heroin, fentanyl and its analogues, prescription opioids, methadone and buprenorphine) and benzodiazepines, the
seller's fentanyl (and where sold, nitazene or xylazine) test page counts, labelled as what it is.

Output `data/verification/pages-2026-11-15/kit_links_705.json`:
`{"finder": "AI reader 705", "date": "2026-11-15", "sellers": {"<seller name as in tests-world.json>": {"home":
"<shop URL>", "drugs": {"<slug>": {"url": "...", "label": "<what the page sells, in the seller's words, at most 6
words, e.g. 'Cannabis test kits'>", "seen": "<page title or heading, word for word>", "read_on": "2026-11-15", "via":
"WebFetch"}}}}}`. Final message under 150 words: per seller, how many drugs have a page; sellers that could not be read.

## Verifier 706

Open every URL of `kit_links_705.json` yourself. Verdict: `confirmed` (the page loads, is on the seller's own site, and
sells a test for that drug or the stated thing), `wrong` (say why), `dead`. Output
`data/verification/pages-2026-11-15/kit_links_check_706.json`: `{"verifier": "AI reader 706", "date": "2026-11-15",
"checks": [{"seller": "...", "slug": "...", "verdict": "confirmed", "note": ""}]}`. Final message under 100 words.
