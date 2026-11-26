"""Claim writer 763 (round pdf-2026-11-26): editors' counts from Goodwin et al. (2008), Table II (pp. 565-566).

Transcribed from the rendered PDF pages: per participant, time of the first negative screen, time of the last positive
screen and length of observation, all in days from admission (screen: immunoassay, 50 ng/mL). None = the dagger or
section-mark rows (never screened positive / never screened negative). Run: python3 -I 763_counts.py
"""
G = {
    "0-50": [  # subject: (first negative, last positive, observation)
        ("A", 1.7, 4.3, 4.8), ("B", 0.3, 1.5, 6.9), ("C", 1.6, 3.8, 4.4), ("E", 0.0, 2.2, 5.1), ("H", 1.4, 1.2, 2.8),
        ("L", 0.3, 0.0, 29.9), ("AA", 0.0, 0.7, 5.8), ("BB", 0.0, None, 2.9), ("DD", 0.0, None, 9.5), ("EE", 1.4, 3.3, 16.3),
        ("GG", 0.3, 2.4, 11.8), ("LL", 0.1, 21.8, 21.8), ("MM", 0.0, None, 0.6), ("OO", 1.2, 5.6, 5.7), ("RR", 0.9, 3.8, 3.8),
        ("TT", 0.0, None, 1.7), ("ZZ", 2.2, 8.6, 29.5), ("DDD", 0.0, None, 20.6), ("FFF", 0.0, None, 12.0)],
    "51-150": [
        ("D", 0.5, 4.3, 4.5), ("F", 1.0, 3.1, 2.2), ("G", None, 1.8, 1.8), ("J", 1.3, 11.6, 26.3), ("K", 7.9, 8.3, 9.6),
        ("N", 0.9, 3.3, 5.8), ("R", 7.8, 10.1, 20.8), ("S", 2.4, 3.7, 20.4), ("V", 2.9, 8.9, 22.4), ("W", 2.8, 2.6, 29.0),
        ("Y", 6.7, 16.0, 29.2), ("CC", 1.2, 3.8, 13.5), ("FF", 2.2, 25.3, 25.7), ("HH", None, 11.0, 11.0), ("JJ", None, 11.0, 11.0),
        ("NN", 3.7, 12.1, 18.6), ("QQ", 1.2, 10.7, 24.6), ("WW", 8.3, 20.9, 30.4), ("XX", 0.0, 17.0, 27.9), ("CCC", 1.7, 5.0, 29.3),
        ("HHH", 5.7, 13.3, 22.6)],
    ">150": [
        ("I", 0.8, 12.7, 12.7), ("M", 1.4, 6.0, 7.3), ("O", 1.6, 3.6, 11.0), ("P", None, 8.2, 8.2), ("Q", 0.8, 3.6, 5.7),
        ("T", 2.5, 29.8, 29.8), ("U", 15.2, 29.3, 29.7), ("X", 5.8, 14.7, 29.6), ("Z", 4.9, 6.3, 29.7), ("II", None, 11.0, 11.0),
        ("KK", None, 11.0, 11.0), ("PP", 1.2, 6.7, 6.7), ("SS", 3.0, 8.8, 28.5), ("UU", 5.6, 18.9, 20.8), ("VV", 3.7, 27.3, 27.3),
        ("YY", 6.1, 29.2, 29.7), ("AAA", 2.1, 28.5, 28.5), ("BBB", 16.1, 29.8, 29.8), ("EEE", None, 12.0, 12.0), ("GGG", None, 11.0, 11.0)],
}


def mean(xs):
    return sum(xs) / len(xs)


def positive_at_end(last, obs):
    # still positive on the last day of observation: last positive on the same calendar day as the end of observation
    # (the rule that reproduces the paper's 13 of 20, mean 19 days, 4 on day 30, in the highest group)
    return last is not None and int(last) == int(obs)


allrows = [r for g in G.values() for r in g]
print("participants", len(allrows), {k: len(v) for k, v in G.items()})
for k, rows in G.items():
    lp = [r[2] for r in rows if r[2] is not None]
    fn = [r[1] if r[1] is not None else 0.0 for r in rows]  # rows never negative are not in the paper's first-negative mean
    fn_paper = [r[1] for r in rows if r[1] is not None]
    end = [r for r in rows if positive_at_end(r[2], r[3])]
    print(f"{k}: mean last positive {mean(lp):.2f} (n={len(lp)}); mean first negative {mean(fn_paper):.2f} (n={len(fn_paper)});"
          f" positive on last day {len(end)} of {len(rows)}, mean last day {mean([r[3] for r in end]):.1f},"
          f" on day 30 (29.x) {sum(1 for r in end if r[3] >= 29.5)}")
never_pos = [r[0] for r in allrows if r[2] is None]
print("never screened positive:", len(never_pos), never_pos)
ever_pos = [r for r in allrows if r[2] is not None]
print("ever positive:", len(ever_pos), "; still positive at end of observation:", sum(1 for r in ever_pos if positive_at_end(r[2], r[3])))
long_obs = [r for r in allrows if r[3] >= 27]
print("observed 27 days or more:", len(long_obs), "; still positive at end:", [r[0] for r in long_obs if positive_at_end(r[2], r[3])])
print("their last positives:", sorted(r[2] for r in long_obs if positive_at_end(r[2], r[3])))
print("others' last positives range:", min(r[2] for r in long_obs if not positive_at_end(r[2], r[3])), "to",
      max(r[2] for r in long_obs if not positive_at_end(r[2], r[3])))
both = [r for r in allrows if r[1] is not None and r[2] is not None]
after = [r for r in both if r[2] > r[1]]
print("had both a negative and a positive screen:", len(both), "; a positive after the first negative:", len(after),
      "; not:", [r[0] for r in both if r[2] <= r[1]])
print("  without row F (impossible: last positive after the end of observation):",
      len([r for r in both if r[0] != "F"]), len([r for r in after if r[0] != "F"]))
print("last positive range", min(r[2] for r in ever_pos), max(r[2] for r in ever_pos),
      "; first negative range", min(r[1] for r in allrows if r[1] is not None), max(r[1] for r in allrows if r[1] is not None))
print("last positive at 10 days or more:", sum(1 for r in ever_pos if r[2] >= 10))
