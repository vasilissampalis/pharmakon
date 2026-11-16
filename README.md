# Pharmakon (φάρμακον)

**https://pharmakon.world** · an evidence-graded encyclopedia of psychoactive drugs. Every statement on a checked page
rests on passages of sources that one reader found and another checked. Senior author: Vasilis Sampalis, MSc (clinical
neuropsychologist). AI co-editor: Claude (Anthropic). Not medical advice.

This is the project's whole working repository: the methods, the data, the code that builds and publishes the site, and
the record of what was decided and why. It is open to read; see [NOTICE.md](NOTICE.md) for what may be reused.

- **How we check**: `docs/METHODS.md` (the protocol; its changelog is at its end). What is done and what waits: `docs/STATUS.md`.
- **Two lanes, always kept apart.** *The checked lane*: claims with graded evidence, each read by two readers and the
  editors (`data/claims`, `data/study-cards`, `data/verification`). *The machine lane*: answers the system writes by
  itself from papers and official pages, published with the line "Written by our system. Not yet checked by a person."
  (`scripts/auto/`, `data/auto/`, `docs/AUTOMATION.md`; METHODS §12.2). The system also lists questions by itself and
  starts pages for drugs that have none; such pages say so.
- **Information, never advice**: no guidance on dosing, on ways of taking a drug or on making an effect stronger
  (METHODS says exactly what may stand where), and nothing a source's own words do not carry.
- **Keys and visitors**: no key or password is kept here (they are repository secrets), and no visitor's words are stored here.

## Where things are

- `docs/METHODS.md` — editorial protocol (authoritative; its version is at its top; v0.1.0 was written before any content)
- `docs/TIER1.md` — substance registry; `docs/WORKFLOW.md` — who does what and the pipeline; `docs/STATUS.md` — what is done and what waits; `docs/EVIDENCE-MAP-BRIEF.md` — how evidence maps are built; `docs/PDF-REQUEST-LIST.md` — master list of PDFs to obtain
- Briefs for AI readers: `docs/STUDY-CARD-BRIEF.md`, `docs/VERIFICATION-BRIEF.md`, `docs/ADJUDICATION-BRIEF.md`, `docs/REVIEW-BRIEF*.md`, `docs/ADJUDICATION-BRIEF-R2.md`, `docs/IDENTITY-BRIEF.md`, `docs/IDENTITY-CHECK-BRIEF.md`
- `docs/SENIOR-DECISIONS.md` — the decisions only the senior author can take (also at the top of the site's Review tab)
- `schema/` — JSON schemas (reference, study card, claim, monograph, epidemiology figure, identity, legal)
- `data/` — content as structured data: references (Crossref-verified), study cards, claims, monographs, epidemiology, identity, legal, site tables, verification rounds and access lists
- `search-logs/` — per-substance DOI lists and search logs (PRISMA)
- `scripts/` — validation (`validate.py`, `rob_vocab.py`, `check_card.py`, `check_identity.py`, `check_citations.js`, `quote_limits.js`), merging (`merge_cards.py`, `merge_claims.py`), patching (`claim_patch.py`, `apply_senior_review.py`), data building and reading rounds (see the pipeline in `docs/WORKFLOW.md`)
- `site/` — the prototype generator (`build.js`) and its source; `site/dist/index.html` is the published page (not kept in Git; rebuild with `node site/build.js`)
- Full texts of papers are never kept here (copyright); the senior author keeps them.
- History: this repository's own (METHODS §11).
