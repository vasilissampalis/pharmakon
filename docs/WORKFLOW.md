# Working procedure (one substance, start to finish)

Roles: **VS** = Vasilis Sampalis (senior author). **AI** = Claude (co-editor). **AI reader 2** = an independent AI reader
that checks the first reader's work without seeing it first (METHODS §5.5).

| Step | Who | What | Output |
|---|---|---|---|
| 1 | AI | Writes the search strings (METHODS §2.2) and runs them: PubMed through the E-utilities interface, Crossref and OpenAlex; screens titles and abstracts; snowballs; builds the evidence map | `search-logs/<Folder>_search-log.md`, `search-logs/<Folder>_DOI-LIST.md` |
| 2 | AI | Checks every listed DOI against Crossref (author, year, title, retraction and correction links) | `search-logs/_VERIFICATION-SWEEP_<date>.md` |
| 3 | AI | Finds which papers are free to read (PubMed Central, open access at the publisher) | `data/access/pmc-index.txt`, `data/access/publisher-oa.txt`, `docs/READ-MYSELF-LIST.md` |
| 4 | VS | Saves only the papers the AI cannot open: paywalled ones, and free ones on ScienceDirect, which refuses the app's browser. Ten at a time, in the order of `docs/PDF-REQUEST-LIST.md`, into `PDFs/<Folder>/` under the filename given; then says "batch N done" | PDFs |
| 5 | AI | Builds the reference records from Crossref (never typed by hand; documented corrections only, in `data/access/metadata-overrides.json`) | `data/references/<substance>.json` |
| 6 | AI reader 1 | Reads each paper in full (the PDFs, or the free full text) and writes the study card: design, sample, risk of bias, key findings with page and locator, reporting issues, interpretation gap | `data/study-cards/<substance>.json` (status `first-pass`) |
| 7 | AI reader 1 | Writes the claims: PECO statement, plain-language sentence, evidence anchors (page, locator, data in its own words, role), GRADE with reasons, status, debate box when contested | `data/claims/<substance>.json`; anchors `ai-located` |
| 8 | AI reader 2 | Reads the same sources blind to reader 1's anchors, extracts the evidence for each claim, gives a verdict on each claim, then checks each study card | `data/verification/<round>/out/*.json` |
| 9 | AI | Reconciles the two readers. Matching anchors become `ai-checked` (blind); every disagreement is listed for VS | `data/verification/<round>/report.md` |
| 9a | AI reader 2 | Targeted checks: anchors the blind reading did not re-find, or that the editor added later, are checked at the stated place (METHODS §5.5) | `data/verification/<round>/…`; anchors `ai-checked`, `check_mode: targeted` |
| 9b | AI adjudicator | Settles reader 2's findings on each study card against the source and logs every change on the card (`docs/ADJUDICATION-BRIEF.md`); a card becomes `ai-checked` when the readers agree on the overall risk-of-bias judgment | Corrected cards in `data/study-cards/_incoming/` |
| 9c | AI methodologists | Independent review of every claim against its evidence and the protocol (`docs/REVIEW-BRIEF*.md`), adjudicated against the sources (`docs/ADJUDICATION-BRIEF-R2.md`) and applied as claim patches (`scripts/claim_patch.py`) | `data/verification/review*/` |
| 9d | AI | Merges checked study cards (`scripts/merge_cards.py`) and staged claims whose references and cards exist (`scripts/merge_claims.py`), then adds each merged claim to its monograph section | `data/study-cards/<substance>.json`, `data/claims/<substance>.json` |
| 9e | AI readers 1 and 2 | Identity section (section 2): first pass from official pages (`docs/IDENTITY-BRIEF.md`, checked with `scripts/check_identity.py`), then a blind second reading and comparison (`docs/IDENTITY-CHECK-BRIEF.md`) | `data/identity/<slug>.json` (`draft` → `ai-checked`) |
| 10 | VS | Opens **Review** on the site: answers the open decisions at the top of the tab (protocol and single claims; `data/site/decisions.json`, rendered to `docs/SENIOR-DECISIONS.md` by `scripts/render_decisions.py`); ticks each anchor after checking it against the source (link or PDF filename shown), marks each study card read after reading it against its source, then approves, approves with edits, or flags each claim with a note | Decisions stored in the site's database |
| 11 | AI | Reads the decisions back (`scripts/apply_senior_review.py`): ticked anchors become `senior-verified`; cards marked read become `appraised`; a claim whose anchors are all senior-verified becomes `anchor-verified`, `appraised` when every card it cites is appraised, and `senior-reviewed` when VS approved its current version. A flag is recorded with its note and the claim is reworked and goes back to step 10 | Claim and card files |
| 12 | VS | Authors section 7 (routes and practical risk reduction) if and when legal review permits. Decision `p-ways-of-taking` (proposed 18 October): the AI may draft section 7 comparisons of forms and routes as findings only, through the usual two readings; `site/build.js` leaves every such claim out of the page until VS approves that version, recorded in `data/verification/senior-gate.json` (`scripts/validate.py` warns on each one still waiting). Practical risk-reduction advice stays his alone | Section 7 content |
| 13 | AI | Validates (schemas, citation integrity, GRADE arithmetic, status ladder, language), builds and publishes the page | Rendered monograph |
| 14 | VS | Opens the page, clicks every citation, approves publication | Status `published`, version 1.0.0 |

**Rule for every exchange:** AI gives VS one step at a time with exact text to paste or exact actions to take, and names
the exact file to save and where. VS never has to search inside files.

## File naming

- PDFs: `PDFs/<Folder>/<FirstAuthor>_<Year>_<ShortTitle>.pdf` (e.g. `PDFs/Methamphetamine/Hart_2012_CognitiveFunctioning.pdf`).
  Two papers by the same first author in one year: add `a`, `b` after the year. A doubled `.pdf.pdf` from a save dialog is
  harmless; the reference records follow the actual filename.

## What the AI can and cannot reach (checked 2026-10-15)

- Through the app's browser: Crossref, PubMed (E-utilities), PubMed Central, Europe PMC, OpenAlex, Unpaywall, ClinicalTrials.gov,
  most publisher article pages (Wiley, SAGE, Springer, Lancet journals, Frontiers, BMC). JAMA Network sometimes shows a bot
  check; the AI waits and retries later and never tries to solve it.
- Not reachable: ScienceDirect (all Elsevier journals except the Lancet family) refuses the app's browser, so those papers go
  to VS's list even when they are free. Paywalled full texts are never obtained by any route other than VS's own access.
- The AI never downloads files in the browser, never opens PDF links there, never uses shadow libraries, and never touches
  VS's own browser tabs.
- Without the app's browser (computer asleep or offline), only WebFetch reaches the web. It answers through a small model
  that summarizes pages and declines to reproduce article text, so it is never used to read papers for study cards; it is
  used for short metadata lookups, and any record it transcribes is compared with a second fetch or the browser before
  use (on 2026-10-16 it dropped a Frontiers record's journal name and issue date). The shell cannot reach Crossref,
  PubMed Central or publishers at all (proxy policy).
- Crossref through WebFetch (learned by the evidence-map agents, 2026-10-16): keep URLs under about 250 characters;
  `&sort=relevance` makes requests fail, while `select=DOI,title,container-title,issued,author` works and allows 25–30
  rows per request; at most three DOIs per `filter=doi:` request; pace 90–130 seconds between calls and 150–300 seconds
  after a refusal (HTTP 429). A topic search with `filter=type:journal-article,has-update:true` is a one-request screen
  for retractions, corrections and expressions of concern, and belongs in every search.
- A Crossref failure that looks like success: `works?filter=doi:A,doi:B` sometimes ignores the filter and returns
  arbitrary records from the whole index (`total-results` in the hundreds of millions). Always check that `total-results`
  equals the number of DOIs asked for, and that every returned DOI is one of them; otherwise the request failed.
  `query.bibliographic` with a long title can likewise return unrelated records instead of nothing.
- From the protocol-reference check (2026-10-16): WebFetch shortens values over about 125 characters (a 202-character
  title came back in pieces); ask for long titles in consecutive pieces under 100 characters and join them by script.
  Even at 138–181 s spacing, 3 of 18 Crossref calls drew HTTP 429 from the proxy, which then refuses that exact URL; the
  plain `works?filter=doi:<DOI>` form (no `select`) works as the second transcription. UNODC: the 'Findings in brief'
  and report pages were readable, the press release and the PDF booklet were not (client errors).
- More from the evidence-map agents (2026-10-16): a literal comma inside a query term (for example `1,4-butanediol`)
  makes WebFetch refuse the URL as robots-disallowed; Crossref weights journal titles heavily, so topic words alone
  can return a page of hits from one journal on unrelated topics (a nicotine query returned 23 of 25 from *Nicotine &
  Tobacco Research*), while author surnames plus exact title fragments work; when `works/<DOI>` is rate-limited, a DOI
  copied verbatim from a works-search record returned in the same session counts as verified, and one successful
  search can verify several papers. Retraction and correction links still need a `works/<DOI>` check per item.
- Learned by the stimulants evidence-map agent (2026-10-16): add `updated-by` to the search `select` so every hit carries
  its retraction and correction links in the same call (the Cocaine, MDMA and Amphetamine searches ran before this and
  need a retraction sweep); `query.container-title` combines with `query.bibliographic` (it found the *Nature Medicine*
  MDMA trials). Crossref answered HTTP 429 to about one call in three even at 200–450 s spacing when several agents
  shared the limit, so run one Crossref agent at a time.
- OpenAlex through WebFetch (learned by the access-check agent, 2026-10-16): `filter=doi:` accepts at most three
  DOIs joined by `%7C` per request (four fail even in short URLs); `select=doi,ids,open_access,is_retracted` gives the
  PubMed Central id, open-access status and a retraction flag in one call; pace 40 s with `scratchpad/openalex_pace.sh`.
- Legal sources through WebFetch (2026-10-16): readable — the Ministry of Health's consolidated tables (only Tables Α΄–Γ΄;
  the extracted text has no table headings and stops at Γ΄ 135), the UN 1971 schedules on documents.un.org, the INCB
  Yellow List and 2025 additions (EUDA copies), legislation.gov.uk (UK law and its copies of EU acts, e.g. the Annex of
  Directive (EU) 2017/2103), Council documents on data.consilium.europa.eu (PDF), Publications Office records
  (op.europa.eu), EUDA news and Drugs Library pages, EUR-Lex ELI `/oj` pages (metadata only, and not all of them).
  Not readable: EUR-Lex text pages (`legal-content/.../TXT/HTML`) and some ELI pages (robots rule); NCBI E-utilities
  (robots rule); Europe PMC, including its REST search on www.ebi.ac.uk (HTTP 429). Two Ministry of Health documents gave
  the Gazette issue of ν. 4139/2013 (Α΄ 74); e-nomothesia.gr is closed to automated readers.
- Ask short questions (under about 400 characters) of euda.europa.eu pages: long prompts there were refused before.

## Pipeline (as built, 2026-10-16)

Source of truth is `data/` (JSON validated against `schema/`). The site is generated from it; nothing is typed into the site
by hand.

| Step | Command (run by AI) | What it does |
|---|---|---|
| Check a card | `python3 -I scripts/check_card.py <card.json>` | Schema, placeholders, quotation length, stigma terms, pages on key findings |
| Merge cards | `python3 -I scripts/merge_cards.py [ids]` | Moves checked cards from `_incoming/` into the substance file; keeps superseded versions |
| References | `python3 -I scripts/build_references.py` | Crossref cache → APA reference records; adds PMCIDs; applies documented overrides |
| Number check | `python3 -I scripts/check_anchor_numbers.py <text-dir>` | Every number in a PDF anchor must appear on the page it names |
| Second reader | `python3 -I scripts/reconcile_second_reader.py round1 [--apply]` | Matches reader 2 to reader 1; upgrades statuses; writes the disagreement report |
| Claim patches | `python3 -I scripts/claim_patch.py PATCH.json [--dry-run]` | Applies an editor's patch file to claims (fields, exact replacements, anchors), bumps versions, writes changelog entries, steps a claim down the ladder when new anchors are unchecked |
| Blind tasks | `python3 -I scripts/make_blind_tasks.py ROUND [--refs a,b]` | Writes the second reader's task files (claims only, no anchors) |
| Vocabulary | `python3 -I scripts/rob_vocab.py [--fix]` | Risk-of-bias words per instrument; design–instrument match (also run by the validator) |
| Senior review | `python3 -I scripts/apply_senior_review.py <export-dir>` | Applies VS's decisions exported from the site's database |
| DOI sweep | `python3 -I scripts/crossref_sweep.py fetch-list / add / report` | Crossref check of every DOI in every list |
| Compile PDF list | `python3 -I scripts/compile_pdf_list.py` | Splits the lists into VS's list (paywalled or ScienceDirect) and the AI's list (free) |
| Validate | `python3 -I scripts/validate.py` | Schemas; citation integrity; GRADE arithmetic; status ladder; language; counts what is not yet senior-verified |
| Build | `node site/build.js` | Injects `data/` into `site/dist/index.html` |
| Publish | Artifact tool | Same URL every time |

The site's database holds four things: VS's review decisions (`reviews/<claim>`), VS's anchor checks (`anchors/<claim>`) and
VS's card readings (`cards/<card>`), all writable only by the owner, and readers' error reports
(`reports/<viewer>/items/<id>`), readable only by editors.

- Learned in batch 2 (2026-10-17): in two-column PDFs, `pdftotext -layout` shows where pages break; second readers' page and paragraph claims need spot checks (several were wrong); notes attached to "confirmed" verdicts sometimes hide real fixes, so the adjudicator sweeps them too; `check_card.py`'s quotation count can be fooled by two short double-quoted phrases in one string.
- Learned in the drug-checking round (2026-10-26/27): first readers wrote cards only and two claim writers then wrote the claims from all the cards together, which kept one topic's numbers consistent; `scripts/check_anchor_numbers.py` had been skipping every anchor whose `source_read` named a PDF path (only the bare word "PDF" was recognized) and now reads both forms and "AM p." pages; an adjudicator's new anchor must be checked by a reader who raised neither it nor the finding behind it, so the targeted checks of new anchors go to readers of other sources; figures on publisher web pages cannot be checked without the app's browser, so a saved PDF is the better record for any paper whose figures carry numbers.
