"""Claim writer 754 (round pdf-2026-11-26): editors' calculations for cl_dc_pill_logo, redoable by a second reader.

Source: Vrolijk, Brunt, Vreeker & Niesink (2017), Addiction 112, 94-100 (PDF, version of record):
site totals p. 95 (Pillreports 218, Partyflock 253); Table 1, Table 4 and Table 5 on p. 97.
Only printed numbers are used. Run: python3 -I 754_calculations.py
"""
import math
from math import comb

N_PILL, N_PARTY = 218, 253
N = N_PILL + N_PARTY  # 471

# Table 1, percentages by site
SPREAD = (67.9, 64.8)      # 'spread inclusion' (a range of amounts given)
DANGER = (14.7, 15.8)      # 'dangerous'

with_range = round(SPREAD[0] / 100 * N_PILL) + round(SPREAD[1] / 100 * N_PARTY)   # 148 + 164
no_range = N - with_range                                                       # 159
dangerous = round(DANGER[0] / 100 * N_PILL) + round(DANGER[1] / 100 * N_PARTY)  # 32 + 40
print(f"with a range {with_range}, without {no_range}, 'dangerous' {dangerous} (Table 1 total 15.3% of 471 = {0.153 * N:.1f})")


def pearson_chi2(a, n1, b, n2):
    """2x2 Pearson chi-square: a of n1 'dangerous' (no range) against b of n2 (range)."""
    tot, d = n1 + n2, a + b
    cells = [(a, n1 * d / tot), (n1 - a, n1 * (tot - d) / tot), (b, n2 * d / tot), (n2 - b, n2 * (tot - d) / tot)]
    return sum((o - e) ** 2 / e for o, e in cells)


# Which split of the 72 'dangerous' reports reproduces Table 4's Pearson chi-square of 6.890?
hits = [a for a in range(dangerous + 1)
        if a <= no_range and dangerous - a <= with_range
        and abs(pearson_chi2(a, no_range, dangerous - a, with_range) - 6.890) < 0.0005]
print("splits reproducing chi2 = 6.890:", hits)
a = hits[0]
b = dangerous - a
p1, p2 = a / no_range, b / with_range
print(f"no range: {a}/{no_range} = {100 * p1:.1f}%; range: {b}/{with_range} = {100 * p2:.1f}%")
print(f"ratio of proportions {p1 / p2:.3f}; odds ratio {(a / (no_range - a)) / (b / (with_range - b)):.3f}; "
      f"1/Exp(b) from Table 5 = 1/0.511 = {1 / 0.511:.3f}")

# Share of reports within 10 mg of the database (or giving no amount): not printed; at most
print(f"within 10 mg or no amount: at most {100 - 39.7 - 17.6:.1f}% (100 - 39.7 - 17.6)")

# Table 4's printed P values against its chi-square values (1 df, two-sided), and one-sided Fisher tests
for x in (0.040, 6.890, 0.116):
    print(f"chi2 {x}: two-sided P = {math.erfc(math.sqrt(x / 2)):.4f}")


def fisher_upper(a, n1, b, n2):
    tot, k = n1 + n2, a + b
    return sum(comb(k, x) * comb(tot - k, n1 - x) for x in range(a, min(k, n1) + 1)) / comb(tot, n1)


print(f"one-sided Fisher, range row: P = {fisher_upper(a, no_range, b, with_range):.4f} (printed 0.007)")
print(f"one-sided Fisher, website row (Pillreports 32/218 vs Partyflock 40/253, lower tail): "
      f"P = {1 - fisher_upper(33, N_PILL, 39, N_PARTY):.4f} (printed 0.417)")

# Table 3: the interval for 'unreported substance dangerous' is not symmetric on the log scale
est, lo, hi = 1.514, 0.477, 7.225
print(f"log distances: lower {math.log(est / lo):.3f}, upper {math.log(hi / est):.3f}; "
      f"symmetric upper limit {est ** 2 / lo:.2f}")
se = math.log(est / lo) / 1.959964
print(f"two-sided Wald P from the lower limit: {math.erfc(abs(math.log(est) / se) / math.sqrt(2)):.3f} (printed 0.481)")
