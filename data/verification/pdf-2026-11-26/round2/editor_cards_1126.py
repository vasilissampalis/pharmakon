"""editor_cards_1126.py: the AI co-editor's fixes to this round's new cards, from the round-2 readers' notes (26 November 2026).

adj_r2.py applied the readers' item-by-item corrections. This applies what their notes on the risk-of-bias and interpretation-gap
judgments say and the card's other fields need: two interpretation gaps raised to substantial (readers 773 and 777 disagreed, with
reasons the editor accepts), and wording that said more than the paper (each fix names the reader's note it follows). Every change
is logged in the card's verification.disagreements. Each old text must occur exactly once, or the script stops before writing.
"""
import glob, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
FIX = [
 ("sc_griffiths_1997", "interpretation_gap.gap_assessment", "minor", "substantial",
  "Reader 773: the central claim that drug history is the most important determinant rests on cross-study comparisons in which drug-experienced people got far higher doses, which the review never discusses. The editor adopts substantial."),
 ("sc_efron_1997", "interpretation_gap.gap_assessment", "minor", "substantial",
  "Reader 777: the abstract's conclusion that pre-existing complaints improve with stimulant treatment, and its statements that the drugs caused appetite loss and insomnia, rest on before-after contrasts without placebo. The editor adopts substantial."),
 ("sc_koski_2003", "sample.selection_effects", "the alcohol-only group is a decade older", "the alcohol-only group is about seven years older (53 against 46)",
  "Reader 773: 53 against 46 years is about seven years, not a decade."),
 ("sc_koski_2003", "interpretation_gap.claimed", "(a decade younger, more often women", "(about seven years younger, more often women",
  "Reader 773: about seven years, not a decade."),
 ("sc_koski_2003", "interpretation_gap.claimed", "(81-96% in six of the nine groups)", "(81-96% in five of the nine groups)",
  "Reader 773: concentrations above the therapeutic range reach 81-96% in five groups (Key finding 5), not six."),
 ("sc_koski_2003", "interpretation_gap.claimed", "comes from 31 deaths in a group the paper itself describes as people prescribed promazine for alcohol withdrawal",
  "comes from 31 deaths among people taking a drug the paper describes as predominantly prescribed in Finland to people with alcohol problems to relieve withdrawal (p. 286)",
  "Reader 773: the paper describes Finnish prescribing in general (p. 286), not the group itself."),
 ("sc_koski_2003", "risk_of_bias.domains[0].note", "For promazine the group is explicitly people prescribed it for alcohol withdrawal.",
  "For promazine, the paper describes the drug as predominantly prescribed in Finland to people with alcohol problems to relieve withdrawal (p. 286); the group itself is not described.",
  "Reader 773: the promazine group is not explicitly people prescribed it for withdrawal."),
 ("sc_senay_2003", "interpretation_gap.results_show", "reporting rates were at most about 2–3 cases per 100,000 estimated patients per quarter in the first year and below 1 later",
  "the reporting rate peaked at about 2.5–3.0 cases per 100,000 patients 12–15 months after launch (the paper gives no time unit for it) and fell below 1 later",
  "Reader 773: the paper gives no time unit, and the peak came 12–15 months after launch."),
 ("sc_maust_2019", "interpretation_gap.claimed", "and prescribed stimulant use with no difference (AOR 0.90, 0.74–1.09)",
  "and prescribed stimulant use was not significantly associated with it (AOR 0.90, 0.74–1.09)",
  "Reader 778: not significantly associated, not 'no difference'."),
 ("sc_maust_2019", "outcomes.multiplicity_correction", "28 counts the two regression outcomes (any use; misuse against use as prescribed) and the 26 younger-against-older comparisons in Table 3",
  "27 counts the two regression outcomes (any use; misuse against use as prescribed) and the 25 younger-against-older comparisons in Table 3 (26 rows; none is tested for theft from a health care setting)",
  "Reader 778: Table 3 has 26 rows but 25 tests."),
 ("sc_maust_2019", "risk_of_bias.domains[7].note", "26 uncorrected age comparisons", "25 uncorrected age comparisons",
  "Reader 778: 25 tests."),
 ("sc_nitro_2022", "interpretation_gap.claimed", "(4) The statement that stigma leads to late presentation and loss to follow-up (p. 3265) rests on one citation",
  "(4) The suggestion that the lack of follow-up data may be partly due to stigma, with late presentation and loss to follow-up as its consequences (p. 3265), rests on one citation",
  "Reader 777: keep the source's hedge ('may be partially due to')."),
 ("sc_vogels_2009", "interpretation_gap.claimed", "The abstract and the closing summary say DIMS gives an accurate reflection",
  "The abstract and the closing summary say that DIMS appears to be a market monitor giving an accurate reflection",
  "Reader 771: the abstract and the closing summary hedge with 'appears to be a market monitor'."),
 ("sc_boutron_2010", "design_detail", "Proportions with exact 95% CIs (pp. 2059–2060).",
  "Proportions with 95% CIs (pp. 2059–2060); the paper does not name the method, and the editors' recalculation reproduces them as exact (Clopper–Pearson) intervals.",
  "Reader 774: the paper never says its CIs are exact; that is the editors' finding."),
 ("sc_boutron_2010", "analysis.effect_sizes", "Spin among 72 reports (exact 95% CIs):",
  "Spin among 72 reports (95% CIs, reproduced as exact intervals by the editors):",
  "Reader 774: the paper never says its CIs are exact."),
 ("sc_boutron_2010", "risk_of_bias.domains[7].note", "Proportions with exact 95% CIs, reproduced by the editors' recalculation (p. 2060; Tables 1–3).",
  "Proportions with 95% CIs (p. 2060; Tables 1–3), which the editors' recalculation reproduces as exact intervals; the paper does not name the method.",
  "Reader 774: the paper never says its CIs are exact."),
 ("sc_heyman_2013", "interpretation_gap.claimed", "The abstract and summary points say addiction is not a chronic relapsing disease, that most people",
  "The summary points say addiction is not a chronic relapsing disease (Summary Point 1; also p. 37), and the abstract and summary points that most people",
  "Reader 772: 'not a chronic relapsing disease' is in Summary Point 1 and p. 37, not the abstract."),
 ("sc_farhat_2025", "risk_of_bias.domains[6].judgment", "yes", "no-information",
  "Reader 776: under METHODS §5.3 (the documented extension for unread supplements), item 7 is 'no information' while the excluded list stands only in the unread appendix; the overall rating is provisional until it is read."),
 ("sc_farhat_2025", "risk_of_bias.domains[6].note", "the appendix was not read.",
  "the appendix was not read, so the item is recorded as no information (METHODS §5.3) and the overall rating stays provisional until it is read.",
  "Reader 776: the rating marked provisional."),
]


def get(o, path):
    import re
    for part in re.findall(r"[^.\[\]]+|\[\d+\]", path):
        o = o[int(part[1:-1])] if part.startswith("[") else o[part]
    return o


def put(o, path, value):
    import re
    parts = re.findall(r"[^.\[\]]+|\[\d+\]", path)
    for part in parts[:-1]: o = o[int(part[1:-1])] if part.startswith("[") else o[part]
    last = parts[-1]
    if last.startswith("["): o[int(last[1:-1])] = value
    else: o[last] = value


cards = {}
for cid, path, old, new, why in FIX:
    if cid not in cards:
        fp = glob.glob(str(ROOT / "data" / "study-cards" / "_incoming" / "*" / f"{cid}.json"))
        assert len(fp) == 1, cid
        cards[cid] = (fp[0], json.load(open(fp[0], encoding="utf-8")))
    fp, c = cards[cid]; cur = get(c, path)
    if cur == old: put(c, path, new)
    else:
        assert isinstance(cur, str) and cur.count(old) == 1, f"{cid} {path}: the old text is not there exactly once"
        put(c, path, cur.replace(old, new))
    c["verification"].setdefault("disagreements", []).append({"field": path, "first_pass": old, "reviewer": new, "resolution": "The AI co-editor's fix, 26 November 2026, from the round-2 reader's note: " + why})
if "--dry" not in sys.argv:
    for fp, c in cards.values(): json.dump(c, open(fp, "w", encoding="utf-8"), ensure_ascii=False, indent=1); open(fp, "a").write("\n")
print("fixed:", len(FIX), "in", len(cards), "cards")
