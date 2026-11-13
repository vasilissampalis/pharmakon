# Independent check of the three group 354 adjudication anchors

> Completed by fresh reader 409 on 9 November 2026; results are in
> `out_reader409.json` and have been applied. This is the retained task brief,
> not an outstanding review. See `../354f_completion.json`.

This task is ready for a fresh reader who did not write these anchors or the
findings behind them. The current ChatGPT conversation (readers 401–408) must
not carry out this check. No independent reader has yet been assigned.

PROJECT is the `pharmakon-project` folder containing this brief. In the current
workspace it is `/workspace/scratch/d1ee8d93ce58/pharmakon-project`.
UPLOADS is `/workspace/scratch/d1ee8d93ce58/pharmakon-uploads`; each task's
`pdf_path` is relative to UPLOADS. These are supplied PDFs; no web access,
downloads or author contact is needed or authorized.

Read `tasks.json`. For context, only `claims.json` is needed; do not read other
reviewers' reports, the adjudication log or prior calculation code before
forming your own findings. This is a targeted round-2 check, not a new review
of the whole claim or of either completed study card.

For each of the three tasks:

1. Read the specified source pages, extract text yourself, and inspect the
   rendered pages. Use 150 dpi for text and 300 dpi for tables and figures.
2. Verify every statement, number, comparison, interval, locator and role in
   `extracted`. For editors' calculations, calculate them independently from
   the printed cells. Keep the two cumulative cutpoints distinct.
3. For the Gelberg task, distinguish an inverse-link of a linear least-square
   mean from an average of probabilities. Assess the stated same-model,
   same-weight assumptions. The anchor must not identify a wrong coefficient,
   a replacement adjusted effect or the authors' actual prediction procedure
   without source evidence. It must not assert a corrected subgroup ranking.
4. Return one verdict: `confirmed`, `corrected`, `wrong-location` or
   `not-found`. A correction may supply `corrected_extracted`,
   `corrected_page` and `corrected_locator`. Give a short explanation and
   report any numerical correction explicitly.

Write only `out_reader409.json` beside this brief, using this schema:

```json
{
  "reader": "AI reader 409 (independent round-2 checker; identify the actual model/provider)",
  "date": "YYYY-MM-DD",
  "results": [
    {"n": 1, "claim_id": "cl_benzo_harm_reduction_services", "anchor_index": 25,
     "verdict": "confirmed", "note": "What was checked at the source."}
  ]
}
```

Include all three results, retaining each task's number, claim id and anchor
index. Do not edit claims, cards, reference metadata, grades or statuses. Do not
apply the results. A later editor will verify the tasks still match the current
anchors, then use `scripts/apply_targeted.py` and the normal guarded patch flow.
If a source fact cannot be resolved, identify exactly what is missing; do not
invent a correction or mark the anchor checked.

The name `409` is a suggested unused reader number, not evidence that a review
has happened. The output must name the actual fresh reader who performs it.
