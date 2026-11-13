"""Independent reader412 arithmetic from the two permitted original PDFs.

The numbers below were transcribed independently from original-source text
and page renders. Counts are compatible reconstructions, not supplied raw data.
Run this script in place to regenerate arithmetic_reader412.json.
"""
from decimal import Decimal
import hashlib
import json
from math import erfc, sqrt
from pathlib import Path
from statistics import NormalDist

HERE = Path(__file__).resolve().parent
z = NormalDist().inv_cdf(0.975)


def compatible_counts(percent, denominator, decimal_places=1):
    printed = Decimal(str(percent))
    half_unit = Decimal(5) * Decimal(10) ** (-decimal_places - 1)
    return [x for x in range(denominator + 1)
            if printed - half_unit <= Decimal(100) * x / denominator
            < printed + half_unit]


def wilson(x, n):
    p = x / n
    divisor = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / divisor
    half_width = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / divisor
    lower, upper = 100 * (centre - half_width), 100 * (centre + half_width)
    return {
        "count": x, "denominator": n, "percent": 100 * p,
        "wilson95_percent": [lower, upper],
        "wilson95_rounded_one_decimal": [round(lower, 1), round(upper, 1)],
        "half_width_percentage_points": 100 * half_width,
        "lower_distance_from_estimate_points": 100 * p - lower,
        "upper_distance_from_estimate_points": upper - 100 * p,
    }


def pearson_2x2(table):
    rows = [sum(r) for r in table]
    cols = [sum(table[i][j] for i in range(2)) for j in range(2)]
    n = sum(rows)
    statistic = sum((table[i][j] - rows[i] * cols[j] / n) ** 2 /
                    (rows[i] * cols[j] / n) for i in range(2) for j in range(2))
    return {"compatible_table_rows_yes_no": table, "n": n,
            "pearson_chi_square_df1_no_continuity_correction": statistic,
            "p_df1": erfc(sqrt(statistic / 2))}


entries = [
    ("ever_preloaded", 41.4, 116, 48, "Results 3.1 p. 170; Results 3.4 p. 172"),
    ("ever_postloaded", 47.4, 116, 55, "Results 3.1 p. 170; Results 3.4 p. 172"),
    ("5HTP_preloading_listing", 41.3, 46, 19, "Table 5 p. 172"),
    ("reduce_comedown_reason", 45.5, 55, 25, "Table 6 p. 173"),
]
wilson_results = []
for label, printed, n, x, location in entries:
    candidates = compatible_counts(printed, n)
    assert candidates == [x], (label, candidates)
    row = {"label": label, "printed_percent": printed,
           "source_location": location,
           "compatible_integer_counts_given_denominator": candidates}
    row.update(wilson(x, n))
    wilson_results.append(row)

reason_results = []
for label, printed in [
    ("reduce_comedown", 45.5), ("reduce_brain_damage_or_neurotoxicity", 32.7),
    ("increase_pleasurable_effects", 21.8), ("reduce_negative_side_effects", 18.2),
    ("prevent_fatigue_illness_or_feeling_run_down", 14.5),
    ("worth_a_try", 3.6), ("other", 14.5),
]:
    candidates = compatible_counts(printed, 55)
    assert len(candidates) == 1
    reason_results.append({"label": label, "printed_percent": printed,
                           "denominator": 55, "compatible_count": candidates[0],
                           "reconstructed_percent": 100 * candidates[0] / 55})

focal_variables = ["age", "gender", "education", "years of ecstasy use",
                   "frequency of ecstasy use", "total occasions of ecstasy use",
                   "average ecstasy dose per occasion", "highest ecstasy dose",
                   "recency of ecstasy use", "place of ecstasy use"]
outcomes = ["changed ecstasy use in response to dislikes", "preloading", "postloading"]
extra_gender = ["highest dose", "public place of use", "more than 50 occasions"]
extra_correlations = ["age with years of use", "typical with highest dose",
                      "highest dose with years of use"]

checks = {
    "preloading_by_total_occasions_high_then_low": pearson_2x2([[29, 24], [19, 44]]),
    "postloading_by_total_occasions_high_then_low": pearson_2x2([[32, 21], [23, 40]]),
    "postloading_by_monthly_or_more_then_less": pearson_2x2([[33, 26], [20, 35]]),
}

approved_inputs = [
    HERE / "BRIEF.md", HERE / "tasks_reader412.json", HERE / "claims_reader412.json",
    Path("/workspace/scratch/d1ee8d93ce58/pharmakon-uploads/PDFs/Alkyl-nitrites-and-inhalants/Bass_1970_SuddenSniffingDeath.pdf"),
    Path("/workspace/scratch/d1ee8d93ce58/pharmakon-uploads/PDFs/MDMA/Allott_2006_HarmReductionPreloading.pdf"),
]

report = {
    "reader": "AI reader412 (ChatGPT/OpenAI; fresh isolated context)",
    "date": "2026-11-09", "z": z,
    "method": "Wilson score 95%, no continuity correction; p=x/n; centre=(p+z^2/(2n))/(1+z^2/n); half-width=z*sqrt(p*(1-p)/n+z^2/(4*n^2))/(1+z^2/n).",
    "scope": "Original PDFs only. All counts reconstructed from printed percentages and stated or expressly assumed denominators; no participant-level data or external calculation ledger accessed.",
    "wilson_checks": wilson_results,
    "table6_reason_checks": reason_results,
    "source_shares_no_stated_denominator": {
        "Internet": 34, "supermarket": 32.1, "pharmacy": 30.2, "health_store": 28.3,
        "note": "These match Results 3.4 p. 172. Product-source response denominator is not stated; no raw counts inferred here."
    },
    "compatible_association_reconstruction": checks,
    "minimum_test_count": {
        "source": "Methods 2.4 p. 170; Results 3.2 pp. 170-171 and 3.4 pp. 171,173",
        "variables": focal_variables, "outcomes": outcomes,
        "focal_comparisons": len(focal_variables) * len(outcomes),
        "additional_explicit_gender_comparisons": extra_gender,
        "additional_explicit_correlations": extra_correlations,
        "focal_plus_distinct_explicit_additional_analyses": 36,
        "qualification": "The 30 is an editorial lower-bound reconstruction from the stated 10-variable by 3-outcome analyses, not a count printed by the authors. Methods says only significant gender differences are reported, so the complete total of additional tests cannot be recovered. Alpha 0.025 on violation of normality is not described as a multiplicity correction; none is reported."
    },
    "bass_table_sum": {"source": "Table p. 2078", "cells": [3,2,2,2,2,2,2,1,1,1], "sum": 18,
                       "qualification": "Not an independent comparison group; eight dashing deaths overlap the narrated cases and cannot be added to them as separate deaths."},
    "input_sha256": {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in approved_inputs},
}
(HERE / "arithmetic_reader412.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
for row in wilson_results:
    print(row["label"], row["count"], row["denominator"], row["percent"],
          row["wilson95_percent"], row["wilson95_rounded_one_decimal"],
          "half-width", row["half_width_percentage_points"])
for label, row in checks.items():
    print(label, row)
print("Focal comparisons:", len(focal_variables) * len(outcomes))
