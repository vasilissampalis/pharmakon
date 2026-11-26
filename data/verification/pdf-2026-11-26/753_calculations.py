"""Claim writer 753, round pdf-2026-11-26: editors' calculations for Siegel et al. (1982), Table 1 (p. 436) and the p values in the text (p. 437).

Recomputes: the whole-number counts behind the printed percentages, the DT-vs-ST risk difference and risk ratio,
and chi-square / Fisher tests for the comparisons printed only as bare p values.
"""
from math import log, exp, sqrt
from scipy.stats import chi2_contingency, fisher_exact, binomtest

groups = {"ST": (37, 32.4), "DT": (42, 64.3), "Control": (28, 96.4)}
counts = {}
for g, (n, pct) in groups.items():
    fits = [k for k in range(n + 1) if round(100 * k / n, 1) == pct]
    counts[g] = fits[0]
    print(f"{g}: n={n}, printed {pct}% -> whole numbers that round to it: {fits} ({fits[0]}/{n} = {100*fits[0]/n:.2f}%)")

st, dt, ct = counts["ST"], counts["DT"], counts["Control"]
nst, ndt, nct = 37, 42, 28

# DT against ST
rd = dt / ndt - st / nst
rr = (dt / ndt) / (st / nst)
se = sqrt(1 / dt - 1 / ndt + 1 / st - 1 / nst)
lo, hi = exp(log(rr) - 1.96 * se), exp(log(rr) + 1.96 * se)
print(f"DT vs ST: risk difference {100*rd:.1f} points; risk ratio {rr:.2f} (Katz 95% CI {lo:.2f} to {hi:.2f})")
tab = [[dt, ndt - dt], [st, nst - st]]
c2, p, _, _ = chi2_contingency(tab, correction=False)
c2y, py, _, _ = chi2_contingency(tab, correction=True)
_, pf = fisher_exact(tab)
print(f"DT vs ST: Pearson chi2 {c2:.2f}, p {p:.4f}; Yates chi2 {c2y:.2f}, p {py:.4f}; Fisher two-sided p {pf:.4f}")
print("  printed in the paper: P < .001")

# three groups
tab3 = [[st, nst - st], [dt, ndt - dt], [ct, nct - ct]]
c3, p3, dof3, _ = chi2_contingency(tab3, correction=False)
print(f"three groups: chi2 {c3:.1f}, df {dof3}, p {p3:.2e}  (printed P < .001)")

# each heroin-experienced group against control
for g, k, n in (("ST", st, nst), ("DT", dt, ndt)):
    t = [[k, n - k], [ct, nct - ct]]
    c, pp, _, _ = chi2_contingency(t, correction=False)
    _, ppf = fisher_exact(t)
    print(f"{g} vs control: Pearson chi2 {c:.2f}, p {pp:.2e}; Fisher p {ppf:.2e}  (printed P < .002 for both)")
pooled = [[st + dt, nst + ndt - st - dt], [ct, nct - ct]]
c, pp, _, _ = chi2_contingency(pooled, correction=False)
print(f"ST+DT pooled vs control: chi2 {c:.2f}, p {pp:.2e}")

# six replications all in the same direction
print(f"six of six replications in one direction: one-sided binomial p = {binomtest(6, 6, 0.5, alternative='greater').pvalue:.4f}; two-sided {binomtest(6, 6, 0.5).pvalue:.4f}  (printed P < .02)")

# out of 100
for g, k, n in (("ST", st, nst), ("DT", dt, ndt), ("Control", ct, nct)):
    print(f"{g}: about {round(100*k/n)} in 100 died ({k} of {n})")
