# Protocol references: Crossref metadata through WebFetch (2026-10-16)

Checker: an AI metadata reader (WebFetch only). Staged lines appended to `data/access/crossref-webfetch-verified.jsonl`;
records built with `scripts/build_references.py` into `data/references/protocol-and-site.json` (Lopez-Quintero 2011 was
already in `methamphetamine.json`).

## Method

Two independent WebFetch transcriptions per article: (a) `api.crossref.org/works/<DOI>`; (b)
`api.crossref.org/works?filter=doi:<DOI>` (total-results 1 and the same DOI each time). A script compared 16 fields (DOI,
type, title, subtitle, authors in order, container-title, volume, issue, page, article-number, published-print,
published-online, issued, update-to, updated-by, publisher). Every field agreed for every article; no update-to or
updated-by relation appeared (no retraction or correction).

## Results

| Reference | DOI | Result |
|---|---|---|
| Hooijmans et al. (2014) | 10.1186/1471-2288-14-43 | verified; article number 43 from Crossref's article-number field |
| Sterne et al. (2016), ROBINS-I | 10.1136/bmj.i4919 | verified; no volume in Crossref, volume 355 from the publisher's page (editor, 2026-10-16) |
| Whiting et al. (2011), QUADAS-2 | 10.7326/0003-4819-155-8-201110180-00009 | verified (DOI found by Crossref search); group author "the QUADAS-2 Group*" given as "QUADAS-2 Group" |
| Munn et al. (2015) | 10.1097/xeb.0000000000000054 | verified (DOI found by Crossref search; the only 2015 IJEBH paper with Munn first on prevalence) |
| Lopez-Quintero et al. (2011) | 10.1016/j.drugalcdep.2010.11.004 | verified; title's survey name kept as a proper noun (override `title_apa`) |
| Iorio et al. (2015) | 10.1136/bmj.h870 | verified; issue "mar16 7" (publisher code) dropped, e-locator h870 as article number; byline read on the publisher's page prints "Kujpers" and "Schunemann", kept as printed |
| GRADE Handbook (Schünemann et al., Eds., 2013) | none | official page read once (https://gdt.gradepro.org/app/handbook/handbook.html, "Updated October 2013"); draft until the senior author checks it |

## Calls

18 Crossref calls between 03:01 and 03:59 UTC; 15 answered. Three were refused by the WebFetch proxy with HTTP 429
(rate limit): the first QUADAS-2 search, and the `filter=doi:` request with a `select` parameter for QUADAS-2 and for
Munn 2015. None of those URLs was fetched again; the plain `filter=doi:` form served as the second transcription.
Pacing: at least 138 s between calls and 275 s after a refusal.

## Notes for the reachability record (WORKFLOW)

- WebFetch shortens values over about 125 characters (a 202-character title came back in pieces); asking for the title
  in consecutive pieces under 100 characters, joined by script, recovers it.
- Even at 138–181 s spacing, 3 of 18 Crossref calls drew HTTP 429 from the proxy, which then refuses that URL.

## Editor's additions (2026-10-16)

- Publisher pages read by the editor through WebFetch: https://www.bmj.com/content/355/bmj.i4919 ("Cite this as: BMJ
  2016;355:i4919", reached by the DOI resolver's redirect) and https://www.bmj.com/content/350/bmj.h870 (byline and "Cite
  this as: BMJ 2015;350:h870").
- The site's APA code now splits run-together initials ("PT", "W.S.") into one initial per letter; this changed only the
  three new records with such names (checked by rendering every reference before and after).
- Casing rule: an all-capital compound keeps every part (ROBINS-I, QUADAS-2); re-titling all records changed only
  ROBINS-I and the quotation marks of Harding et al. (2022), which Crossref prints as curly quotes.
