"""Independent reader417 calculations from own transcription of original PDFs.

No project claims, cards, ledgers or previous calculations are imported.
Sumnall inputs are rounded Table 1 values and randomized group header counts;
they cannot exactly reconstruct the analytic sample or the published MANOVA.
"""
import json
import math
from pathlib import Path

output_directory = Path(__file__).parent
z = 1.959963984540054


def wilson(x, n):
    p = x / n
    d = 1 + z * z / n
    center = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return {"x": x, "n": n, "percent": 100 * p,
            "wilson_95_percent": [100 * (center - half), 100 * (center + half)]}


n = [158, 155, 155, 154, 155, 158, 156, 157]
harm_mean = [22.9, 22.4, 23.1, 23.5, 24.0, 23.8, 22.9, 23.6]
harm_sd = [5.1, 5.7, 5.4, 4.0, 4.6, 4.7, 5.2, 4.5]
stigma_mean = [38.6, 41.0, 43.7, 46.2, 43.5, 45.4, 47.7, 50.1]
N = sum(n)
sse = sum((ni - 1) * sd ** 2 for ni, sd in zip(n, harm_sd))
mse = sse / (N - len(n))


def collapse(indices):
    total = sum(n[i] for i in indices)
    mean = sum(n[i] * harm_mean[i] for i in indices) / total
    var = sum((n[i] - 1) * harm_sd[i] ** 2 +
              n[i] * (harm_mean[i] - mean) ** 2 for i in indices) / (total - 1)
    return {"n": total, "mean": mean, "sd": math.sqrt(var)}


collapsed = {key: collapse(indices) for key, indices in {
    "younger": [0, 1, 2, 3], "older": [4, 5, 6, 7],
    "younger_ecstasy": [0, 1], "older_ecstasy": [4, 5],
    "younger_heroin": [2, 3], "older_heroin": [6, 7],
    "woman": [0, 2, 4, 6], "man": [1, 3, 5, 7],
}.items()}


def contrast(coefficients):
    estimate = sum(c * m for c, m in zip(coefficients, harm_mean))
    variance = mse * sum(c * c / ni for c, ni in zip(coefficients, n))
    return {"coefficients": coefficients, "estimate": estimate,
            "variance": variance, "approximate_F": estimate ** 2 / variance}


contrasts = {key: contrast(coefficients) for key, coefficients in {
    "age_equal_marginals": [-.25, -.25, -.25, -.25, .25, .25, .25, .25],
    "age_by_drug_equal_marginals": [-.5, -.5, .5, .5, .5, .5, -.5, -.5],
    "age_within_ecstasy_equal_marginals": [-.5, -.5, 0, 0, .5, .5, 0, 0],
    "age_within_heroin_equal_marginals": [0, 0, -.5, -.5, 0, 0, .5, .5],
}.items()}

young, old = collapsed["younger"], collapsed["older"]
age_pooled_sd = math.sqrt(((young["n"] - 1) * young["sd"] ** 2 +
                           (old["n"] - 1) * old["sd"] ** 2) / (N - 2))
result = {
    "reader": "reader417",
    "transcription": {
        "sumnall_table_1_condition_order": [
            "Jane/younger/ecstasy", "John/younger/ecstasy",
            "Jane/younger/heroin", "John/younger/heroin",
            "Jane/older/ecstasy", "John/older/ecstasy",
            "Jane/older/heroin", "John/older/heroin"],
        "sumnall_table_1_header_n": n,
        "sumnall_table_1_harm_mean": harm_mean,
        "sumnall_table_1_harm_sd": harm_sd,
        "sumnall_table_1_stigma_mean": stigma_mean,
        "hancock_table_1": {"suspected": {"drug_final": 2454, "other_final": 265},
                            "not_suspected": {"drug_final": 115, "other_final": 122}},
        "smiley_table_1": {"internal": 78, "external": 1012,
                           "none": 148, "not_needed": 82, "total": 1320},
        "zaychik_table_4_estimate_se": [[-.02, .04], [-.03, .05], [-.02, .06]],
    },
    "sumnall": {
        "header_N": N,
        "header_counts_imply_univariate_residual_df": N - 8,
        "printed_univariate_residual_df": 1230,
        "printed_df_implied_N_under_full_eight_cell_model": 1230 + 8,
        "sample_size_limit": "Header counts sum to 1248, but the printed residual df imply 1238 under the stated full eight-cell model. Missingness/exclusions cannot be recovered from the article alone.",
        "within_eight_cell_sse": sse,
        "within_eight_cell_mse_using_header_n": mse,
        "within_eight_cell_pooled_sd": math.sqrt(mse),
        "weighted_collapses": collapsed,
        "approximate_equal_marginal_contrasts": contrasts,
        "age_harm_d_from_weighted_collapses": (old["mean"] - young["mean"]) / age_pooled_sd,
        "stigma_d_from_printed_marginals_equal_weight_pooled_sd": {
            "man_minus_woman": (45.6 - 43.4) / math.sqrt((12.1 ** 2 + 12.6 ** 2) / 2),
            "older_minus_younger": (46.7 - 42.3) / math.sqrt((11.8 ** 2 + 12.7 ** 2) / 2),
            "heroin_minus_ecstasy": (46.9 - 42.1) / math.sqrt((11.5 ** 2 + 12.8 ** 2) / 2),
        },
        "stigma_regression_N_from_F_17_850": 17 + 850 + 1,
        "stigma_final_R2_sum_from_table_2": .068 + .016 + .234 + .251,
        "interpretation_limit": "F approximations use rounded cell summaries and the overall table header counts. They are an editorial diagnostic, not a reanalysis of individual observations or proof that the printed F=4.8 labels a particular test.",
    },
    "hancock": {
        "non_drug_among_suspected": wilson(265, 2719),
        "drug_among_not_suspected": wilson(115, 237),
        "sensitivity": wilson(2454, 2569),
        "specificity": wilson(122, 387),
        "source_defined_false_negative_fraction": wilson(115, 2569),
    },
    "smiley": {
        "access_percent": (78 + 1012) / 1320 * 100,
        "internal_percent": 78 / 1320 * 100,
        "external_percent": 1012 / 1320 * 100,
        "none_percent": 148 / 1320 * 100,
        "not_needed_percent": 82 / 1320 * 100,
        "screening_percent": 715 / 1326 * 100,
        "confirmation_percent": 674 / 709 * 100,
    },
    "zaychik": {
        "before_system_counts_in_seven_analysed_states": {
            "justices_of_peace": 2, "coroner": 2, "physician_coroner": 1,
            "locally_appointed_physician": 1, "magistrate_coroner": 1},
        "editorial_normal_95_intervals_from_rounded_estimates_and_SE": [
            {"estimate": b, "se": se, "interval": [b - z * se, b + z * se]}
            for b, se in [(-.02, .04), (-.03, .05), (-.02, .06)]],
        "interval_limit": "Conditional calculations from published rounded standard errors; no correction for repeated state observations can be reconstructed. Neither exact corrected precision nor its direction is established by these calculations.",
    },
}
(output_directory / "calculations_reader417.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"written": str(output_directory / "calculations_reader417.json"),
                  "sumnall_F": {k: v["approximate_F"] for k, v in contrasts.items()}}, indent=2))
