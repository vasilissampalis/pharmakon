# Gelberg statistical follow-up, reader 408, 9 November 2026

The printed benzodiazepine probabilities imply two disjoint rounding ranges
for cumulative odds ratios: 3.391–3.918 and 5.260–5.311. Neither contains
19.918, and neither is a valid replacement common proportional odds ratio.

A reproducible hypothetical common-OR 19.918 model reproduces all six printed
probability cells when probabilities are averaged first. This demonstrates
that a wrong coefficient cannot be inferred from those cells alone. The paper
instead describes applying a logistic function to least-square means. The
actual calculation remains unreconciled without its model and prediction code.

The **unapplied** replacement proposal `354d_patch.json` removes the proposed
corrected stimulant-first ordering. It retains printed estimates and qualifies
their relationship. Only Gelberg statistical passages change from the original
354 proposal; all other content passes through unchanged. Numerical checks,
scope guards and the patch dry run pass. Completed cards are unchanged, and
their checks and global validation were not repeated.

Gelberg anchor 30 (zero-based, after application) remains `ai-located` for a
fresh independent reader. Reader 408 is the same ChatGPT conversation as 401.
No patch applied, rating changed, author contacted, checkpoint archive created
or site published. Detailed derivation and executable checks are in
`handoff/scratchpad/pdf1101/a408/`.
