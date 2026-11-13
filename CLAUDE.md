# Pharmakon: working rules for this repository

Pharmakon (https://pharmakon.world) is an evidence-graded drug encyclopedia. Senior author: Vasilis Sampalis. The AI
co-editor decides and he reviews. Site version and protocol version: `data/site/version.json`.

## Save everything, at once

- This repository on GitHub (`vasilissampalis/pharmakon`, branch `main`) is the only safe copy. The cloud workspace can
  be reset at any time, and on 13 November 2026 a reset wiped the earlier working copy (see `docs/STATUS.md`).
- Commit and push after every step that changes files: `git add -A && git commit -m "..." && git push -q origin main`.
  Never end a turn with uncommitted or unpushed work.
- Keep tools, briefs, task files and readers' outputs inside the repository (`scripts/editor/`, `data/verification/`),
  never only in temporary folders. Large scratch files (page images, PDF text dumps) may stay outside it.
- Never commit PDFs of papers (copyright) or built output (`site/dist`, `site/public`, zips).

## Demand first (senior author, 13 November 2026)

- Prioritize what people actually want to learn, not what we think they want: questions come from real sources (Reddit
  pages and forums he pastes, search questions, the site's own visitors), ranked by how much people ask them
  (`data/verification/questions-*/`, scores in `data/site/demand.json`). Safety facts go inside the answers people ask for.
- Write each question in people's words and lead each short answer with what they want to know. Nothing too clinical or
  boring at the top of a page: clinical answers stay, checked, but lower down. No answer exists only because a paper does.

## Evidence rules (METHODS.md has the full protocol)

- Nothing unverified. Every statement rests on anchors: a passage found by one reader and checked at the source by
  another who wrote none of it. Second readers do not open `data/claims` or first readers' files, except the claim
  named for context.
- APA 7; Crossref records for reference metadata, never typed by hand (overrides need a cited source).
- Simple language; Carl Hart's critical eye; practical safety first; a safe, non-judging space; person-first language.
- Quotations at most 15 words, at most one per claim. No copyrighted content. Photos: public domain, CC0 or CC BY.
- No dosing, administration or potentiation guidance anywhere. The doses section is the senior author's own text.
- Section 7 (forms and routes compared) is shown only in a version he approved (`data/verification/senior-gate.json`).
  Never record an approval he did not give.
- Quiz and myth-or-fact items: useful, surprising research facts; never amounts, doses, timing, routes compared for
  strength, or reaching or strengthening effects; mixing only as risk facts.
- If an automatic filter stops a step, do not retry or reword it.

## Pipeline

First readers write study cards; claim writers write patches (`scripts/claim_patch.py`); round-2 readers check new
anchors and cards; the editor adjudicates and merges (`scripts/merge_cards.py`); plain lines and quiz items are
blind-checked; `scripts/snapshot_published.py`; `python3 -I scripts/validate.py` (0 hard failures); `node site/build.js`;
`python3 -I site/build_public.py`; the zip goes to the senior author's folder, and he deploys it on Cloudflare Pages.
- Deliver the zip with SendUserFile, then write it to his folder by that file's id (`device_commit_files` with `fileUuid`), never
  by an outputs path: on 13 November a path-based write put an older zip in his folder. Stage it back and compare SHA-256.
