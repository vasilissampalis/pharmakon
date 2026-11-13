# DrugEncyclopedia — project repository

Working title **Pharmakon** (φάρμακον). An evidence encyclopedia of psychoactive drugs: every finding a graded, sourced claim.

- `docs/METHODS.md` — editorial protocol (authoritative; v0.2.5; v0.1.0 written before any content)
- `docs/TIER1.md` — substance registry; `docs/WORKFLOW.md` — who does what and the pipeline; `docs/STATUS.md` — what is done and what waits; `docs/EVIDENCE-MAP-BRIEF.md` — how evidence maps are built; `docs/PDF-REQUEST-LIST.md` — master list of PDFs to obtain
- Briefs for AI readers: `docs/STUDY-CARD-BRIEF.md`, `docs/VERIFICATION-BRIEF.md`, `docs/ADJUDICATION-BRIEF.md`, `docs/REVIEW-BRIEF*.md`, `docs/ADJUDICATION-BRIEF-R2.md`, `docs/IDENTITY-BRIEF.md`, `docs/IDENTITY-CHECK-BRIEF.md`
- `docs/SENIOR-DECISIONS.md` — the decisions only the senior author can take (also at the top of the site's Review tab)
- `schema/` — JSON schemas (reference, study card, claim, monograph, epidemiology figure, identity, legal)
- `data/` — content as structured data: references (Crossref-verified), study cards, claims, monographs, epidemiology, identity, legal, site tables, verification rounds and access lists
- `search-logs/` — per-substance DOI lists and search logs (PRISMA)
- `scripts/` — validation (`validate.py`, `rob_vocab.py`, `check_card.py`, `check_identity.py`, `check_citations.js`, `quote_limits.js`), merging (`merge_cards.py`, `merge_claims.py`), patching (`claim_patch.py`, `apply_senior_review.py`), data building and reading rounds (see the pipeline in `docs/WORKFLOW.md`)
- `site/` — the prototype generator (`build.js`) and its source; `site/dist/index.html` is the published page (not kept in Git; rebuild with `node site/build.js`)
- `PDFs/<Substance>/` (on the senior author's computer) — full texts, one folder per substance
- History: a local Git repository in the working copy (METHODS §11); exported as `DrugEncyclopedia-history.bundle` to the senior author's computer when it is linked
