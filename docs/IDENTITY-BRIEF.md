# Identity sections — brief for the first reader

Written 2026-10-16. Section 2 of each monograph ("Identity and nomenclature") is a set of **sourced facts** (METHODS
§10.3), not graded claims: names, identifiers, forms, street names and drug-checking findings, each tied to the official
page it comes from. Files validate against `schema/identity.schema.json` and are written to
`data/identity/_incoming/<slug>.json`; the editor reviews them and moves them into `data/identity/`. A second reader then
checks them (`docs/IDENTITY-CHECK-BRIEF.md`).

## Sources

Official or monitoring bodies only: EUDA (drug profiles, European Drug Report, risk assessments, EMCDDA reports), WHO
(ATC/DDD Index; Expert Committee on Drug Dependence critical and pre-review reports), UNODC and INCB, the US DEA
(Diversion Control Division drug and chemical information sheets; DEA fact sheets), NIDA, AIHW, the NIST Chemistry
WebBook, DailyMed, FDA, EMA, national legislation pages. Not Wikipedia, PubChem summaries of other sites, vendors or
forums. Never a paper read through WebFetch (METHODS §12.1): drug-checking findings from papers are left for a full-text
reading; drug-checking facts on official pages (for example EUDA's) may be used.

## How to read

- WebFetch and WebSearch only, with open prompts that ask for items **exactly as printed** (numbers digit by digit,
  names in the page's spelling, lists complete and in page order). At least 60 seconds between two calls to the same
  domain; never retry a refused or failed page; no browser, no downloads, no CAPTCHAs, no PubChem pages (they load by
  script and have returned bot checks).
- Every number (CAS number, formula, molar mass) is **read twice**: a second, narrower fetch of the same page, or a second
  source. Record which in the source's `note`. Where two sources disagree, give both, as printed, and say which is
  which; a CAS number must pass its check digit (`scripts/check_identity.py` tests it).
- Each source records `read_via: "WebFetch"`, the page date as the page gives it (`date`) and `accessed`.
- A page that could not be read, or a lookup that found nothing, is **not** a source: list it in your final report.

## What to write

- `names`: INN (WHO ATC name or the source's explicit INN statement; otherwise say "INN status not confirmed"), IUPAC or
  systematic name, CAS numbers (each as "number: what it identifies (source)"), formula, molar mass, synonyms.
- `members` (pages that cover a class of substances): one entry per member the page covers, each with name, INN if any,
  CAS, formula, molar mass, synonyms and `source_ids`.
- `forms`: salts, physical forms, products and preparations as documented, in the sources' words. Describe forms, never
  how to prepare, take, dose or combine anything; a product size or a seizure amount is fine, a dose is not.
- `street_names`: names exactly as documented, with the region and period the source gives; never invent a region.
- `compiled_by`: who compiled it and how ("Claude (AI co-editor), first pass from official pages read through WebFetch on
  <date>; numbers marked 'read twice' were re-read …; not yet checked by a second reader or by the senior author").
- `verification`: `draft`.

Person-first wording; quotations at most 15 words. Run `python3 -I scripts/check_identity.py <file>` until it reports OK.
Do not edit any other project file.
