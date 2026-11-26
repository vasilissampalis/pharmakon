#!/usr/bin/env python3
"""First reader 741 (round pdf-2026-11-26): the editors' calculations behind sc_varshneya_2022 and sc_williams_2020.

Pure arithmetic on numbers printed in the papers (no files are read). Run: python3 -I 741_calculations.py

Varshneya et al. (2022), author manuscript, Table 1 (PDF pp. 7-8) and Figure 1 (PDF p. 6): the paper does not name the
reference category of its logistic regression. Unadjusted 2x2 comparisons against the group whose shortest wait after
fentanyl was "within 1 month" reproduce every printed odds ratio, 95% CI and p value, using the Table 1 group sizes, the
printed severe counts for "within 24 h" (152) and "within 48 h" (55), and severe counts of 25, 13 and 5 for "within 72 h",
"within 1 wk" and "within 1 mo" (methadone 23, 2, 2, 1, 2). These counts add up to the printed totals (250 and 30) and
match the Figure 1 bars measured on the page rendered at 300 dpi (buprenorphine 22.15, 7.99, 3.63, 1.87, 0.72% of 685;
methadone 11.5, 1.0, 1.0, 0.49, 1.0% of 199).

Williams et al. (2020), AJP in Advance, Figure 3 (PDF p. 5): bar heights measured on the page rendered at 300 dpi and
calibrated on the 60%, 40% and 30% gridlines (13.4 px per percentage point); the printed values they can be checked
against (41.2, 48.6, 11.3, 13.9, 19.1, 25.9) are recovered within about 0.15 points.
"""
import math

def wilson(k, n, z=1.96):
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return 100 * p, 100 * (c - h), 100 * (c + h)

def phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

print("Varshneya 2022: severe withdrawal by shortest wait after fentanyl")
groups = ["within 24 h", "within 48 h", "within 72 h", "within 1 wk", "within 1 mo (reference)"]
data = {
    "buprenorphine": [(339, 152), (160, 55), (97, 25), (52, 13), (37, 5)],
    "methadone": [(135, 23), (22, 2), (21, 2), (13, 1), (8, 2)],
}
printed = {
    "buprenorphine": [(5.202, 1.979, 13.675, 0.001), (3.352, 1.237, 9.089, 0.017), (2.222, 0.780, 6.329, 0.135), (2.133, 0.687, 6.620, 0.190)],
    "methadone": [(0.616, 0.117, 3.247, 0.568), (0.300, 0.035, 2.606, 0.275), (0.316, 0.036, 2.750, 0.297), (0.250, 0.019, 3.342, 0.295)],
}
for drug, rows in data.items():
    n_all = sum(n for n, _ in rows); k_all = sum(k for _, k in rows)
    p, lo, hi = wilson(k_all, n_all)
    print(f"  {drug}: {k_all}/{n_all} severe = {p:.1f}% (Wilson 95% CI {lo:.1f}-{hi:.1f})")
    n_ref, k_ref = rows[-1]
    for i, (g, (n, k)) in enumerate(zip(groups, rows)):
        p, lo, hi = wilson(k, n)
        line = f"    {g:24s} {k}/{n} = {p:.1f}% within group (Wilson {lo:.1f}-{hi:.1f}); {100 * k / n_all:.2f}% of all {n_all}"
        if i < 4:
            orr = (k / (n - k)) / (k_ref / (n_ref - k_ref))
            se = math.sqrt(1 / k + 1 / (n - k) + 1 / k_ref + 1 / (n_ref - k_ref))
            l, u = math.exp(math.log(orr) - 1.96 * se), math.exp(math.log(orr) + 1.96 * se)
            pv = 2 * (1 - phi(abs(math.log(orr)) / se))
            line += f" | OR {orr:.3f} ({l:.3f}-{u:.3f}) p={pv:.3f}; printed {printed[drug][i]}"
        print(line)
print("  both medications (n=152): buprenorphine 69 = %.1f%%, methadone 20 = %.1f%%" % (100 * 69 / 152, 100 * 20 / 152))
print("  denominators: 339/1163 = %.1f%% (printed 29.1%% as 339/685 = %.1f%%); 135/1163 = %.1f%% (printed 11.6%% as 135/200 = %.1f%%)"
      % (100 * 339 / 1163, 100 * 339 / 685, 100 * 135 / 1163, 100 * 135 / 200))
print("  250 of all 1,163 = %.1f%%; 1,163 - 421 never - 57 within 1 yr = %d" % (100 * 250 / 1163, 1163 - 421 - 57))

print("\nWilliams 2020")
print("  overdose 464/8,996: %.1f%% (Wilson %.1f-%.1f)" % wilson(464, 8996))
print("  excluded for incomplete enrolment 3,940/12,936 = %.1f%%; not stopped 10,481/26,576 = %.1f%%" % (100 * 3940 / 12936, 100 * 10481 / 26576))
print("  Table 1 totals: psychiatric %.1f%%, alcohol use disorder %.1f%%, non-opioid drug use disorder %.1f%%"
      % (100 * 2777 / 8996, 100 * 430 / 8996, 100 * 1951 / 8996))
print("  15-18 vs 6-9 months, percentage points: ED %.1f, inpatient %.1f, opioid prescription %.1f" % (48.6 - 41.2, 13.9 - 11.3, 25.9 - 19.1))
n = [4126, 2440, 1499, 931]
rx = [25.93, 25.19, 22.95, 19.22]   # Figure 3 bars, opioid prescription, 6-9, 9-12, 12-15, 15-18 months
ed = [48.47, 46.98, 44.22, 41.23]   # Figure 3 bars, emergency services
print("  weighted averages from Figure 3: opioid prescription %.1f%%, emergency visits %.1f%%"
      % (sum(a * b for a, b in zip(n, rx)) / sum(n), sum(a * b for a, b in zip(n, ed)) / sum(n)))
