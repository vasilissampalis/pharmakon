# Second-reader brief (AI reader 2)

First written for round 1 (methamphetamine); the same procedure was used in round 2. Paths below name round 1; use
`data/verification/<round>/…` with the round named in your task.

You are the **second, independent reader** in the encyclopedia's three-reader rule (METHODS §5.5): AI reader 1 drafted study
cards and evidence anchors; you check them without seeing reader 1's anchors; the senior author decides.

Project root: `/home/claude/drug-encyclopedia`. Read `docs/METHODS.md` §4.5, §5, §6 first (15 minutes, once).

## What you are given

For each source assigned to you there is a task file `data/verification/round1/tasks/<reference>.json`. It lists the
claims that cite that source: each claim's id, statement and magnitude, and how many anchors reader 1 took from this
source with what roles (supports / contradicts / qualifies). It does **not** contain reader 1's pages, locators or extracted
data. **Do not open `data/claims/*.json`** before you have finished step 1 for that source: that file contains reader 1's
anchors, and seeing them first defeats the purpose.

## Step 1 — blind extraction (per source)

Read the source in full (see "Where to read"). For every claim in the task file:

1. Find every place in the source that supports, contradicts or qualifies the claim **as the claim is worded**. Record each
   as an anchor: printed page (or `PMC HTML` / `publisher HTML` for web full texts), locator (section › paragraph, table,
   figure), the data in your own words (numbers, n, intervals, test statistics, conditions), and its role.
2. Give a verdict on the claim **as far as this source is concerned**: `supported`, `partly-supported` (say which part is
   not), `not-supported`, or `contradicted`. Check every number in the statement and magnitude that comes from this source.
   If a number is a derived "editors' calculation", recompute it and say whether you get the same.
3. Say whether the claim's wording overstates the source (causal language, generalization beyond the sample, "normal",
   "recovery", "impairment" and similar words) or understates it.

## Step 2 — check reader 1's study card (unblinded, after step 1)

Now open the card for that source in `data/study-cards/methamphetamine.json` (id `sc_<reference>`, hyphens become
underscores). For each key finding and each reporting issue: `confirmed`, `corrected` (give the correction),
`wrong-location` (give the right one) or `not-found`. Say whether you agree with the risk-of-bias judgment and the
interpretation-gap assessment, and list anything important the card missed.

## Output

One file per source: `data/verification/round1/out/<reference>.json`:

```json
{
  "reference": "volkow_2001a",
  "reader": "AI reader 2",
  "read_on": "2026-10-16",
  "source_read": "PDF, pp. 377–382 (all pages; Table 2 and Figures 2–4 checked on rendered pages)",
  "claims": [
    {"claim_id": "cl_meth_dat_lower", "verdict": "supported", "overstatement": "", "note": "",
     "anchors": [{"page": "p. 379", "locator": "Table 2", "extracted": "…", "role": "supports"}]}
  ],
  "card_check": {
    "key_findings": [{"index": 0, "verdict": "confirmed", "correction": ""}],
    "reporting_issues": [{"index": 0, "verdict": "confirmed", "note": ""}],
    "risk_of_bias": {"verdict": "agree", "note": ""},
    "interpretation_gap": {"verdict": "agree", "note": ""},
    "missed": []
  }
}
```

`index` is the 0-based position in the card's `key_findings` / `reporting_issues` arrays. Validate your JSON with
`python3 -c "import json,sys; json.load(open(sys.argv[1]))" <file>` before moving on.

## Where to read

- **PDF sources** (`pdf_path` in the task file): the PDF is at `/mnt/user-data/uploads/DrugEncyclopedia/<pdf_path>`. Extract
  text with `pdftotext -layout` into your own scratch folder; render pages with `pdftoppm -r 110` and look at them for
  tables and figures. Printed page = the journal's page number, not the PDF page index.
- **PMC sources**: `https://pmc.ncbi.nlm.nih.gov/articles/<PMCID>/` in **your own browser tab** (create it with the
  browser-pane `tabs_create` tool; use only that tab id).
- **Publisher HTML sources** (Wiley, SAGE, JAMA Network): the DOI link, in your own tab. JAMA's site sometimes shows a
  Cloudflare check: wait and retry later, never try to solve it.

## Rules (hard)

- Use only the browser tab you created. Never touch, read, navigate or close any other tab; other tabs belong to the
  senior author or to other readers.
- Never download files, never open PDF URLs in the browser, never attempt a CAPTCHA or bot check, never use shadow
  libraries (Sci-Hub and similar). If a page will not open, record that and move on.
- Never reproduce passages. Extracted data are in your own words; if wording itself matters, at most one quotation of
  15 words or fewer per claim.
- Person-first language (METHODS §9). No dosing, administration or potentiation guidance of any kind; doses appear only
  as study conditions.
- Do not edit any project file other than your own outputs in `data/verification/round1/out/`. Do not change the claims,
  cards or references; the editor reconciles.
- Do not message the user. When finished, report: sources done, verdicts that are not `supported`, card findings that
  are `corrected`/`wrong-location`/`not-found`, and anything you could not read.

**Locator convention for web full texts (PubMed Central, publisher HTML).** Count only paragraphs of running text within the named section or subsection: headings, figure and table captions, figure legends, footnotes and boxed 'key points' are not paragraphs. Give the section path as printed (Results › Characteristics of the sample, 2nd paragraph). For tables, name the table and the row or column. This keeps two readers' locators comparable.

## Targeted checks (METHODS §5.5; added 2026-10-16)

After the blind round, anchors the blind reading did not re-find, and anchors the editor added later, are checked one by
one at the stated place. For each anchor in the round's targeted task file, open the source at the stated page and
locator and answer `confirmed` / `corrected` (give the corrected text) / `wrong-location` (give the locator) /
`not-found`, with a short note of what you compared. The editor then sets `anchor_status: ai-checked` with
`check_mode: targeted`. You must not check an anchor you wrote yourself, or one whose matching card finding you added.
