#!/usr/bin/env python3
"""Risk-of-bias vocabulary by instrument (METHODS §5.3).

Each instrument has its own words. Mixing them (a ROBINS-I "serious" inside a ROBINS-E rating, an RoB 1 "unclear"
inside RoB 2) makes the rating unreadable, so the validator and check_card.py refuse it. For the tools that build
an overall judgment from domains (RoB 2, ROBINS-E, ROBINS-I and the editors' narrative-review checklist), the overall
judgment can be no less severe than the worst domain.

Editors' extensions, documented in METHODS §5.3:
  AMSTAR 2 item "no-information"  — the item can only be judged from a supplement that has not been read; the overall
                                    confidence rating is then provisional and the card says so.
  JBI "partial-yes"                — an item met in part; the card gives the reason. JBI itself offers yes, no, unclear
                                    and not applicable, and has no overall algorithm; the editors summarise as low,
                                    moderate or high risk.

Usage
  rob_vocab.py            list problems in all merged and incoming cards
  rob_vocab.py --fix      apply only the mechanical corrections below, logging each in verification.editorial_corrections:
                            ROBINS-E: moderate -> some-concerns, serious -> high, critical -> very-high
                            RoB 2: unclear -> some-concerns
                            overall less severe than the worst domain -> raised to the worst domain
"""
import json, sys, glob, pathlib, datetime, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
TODAY = datetime.date.today().isoformat()

VOCAB = {
    "RoB 2": ({"low", "some-concerns", "high"}, {"low", "some-concerns", "high"}),
    "ROBINS-E": ({"low", "some-concerns", "high", "very-high"}, {"low", "some-concerns", "high", "very-high"}),
    "ROBINS-I": ({"low", "moderate", "serious", "critical", "no-information"},
                 {"low", "moderate", "serious", "critical", "no-information"}),
    "AMSTAR 2": ({"yes", "partial-yes", "no", "no-meta-analysis", "no-information"},
                 {"high-confidence", "moderate-confidence", "low-confidence", "critically-low"}),
    "SYRCLE": ({"low", "high", "unclear"}, {"low", "high", "unclear"}),
    "QUADAS-2": ({"low", "high", "unclear"}, {"low", "high", "unclear"}),
    "JBI-prevalence": ({"yes", "partial-yes", "no", "unclear", "not-applicable"}, {"low", "moderate", "high"}),
    "none-applicable": ({"low", "some-concerns", "high"}, {"low", "some-concerns", "high"}),
    # the editors' qualitative checklist (domains adapted from CASP: design, sampling, data collection, reflexivity,
    # ethics, rigour of analysis, grounding of findings, transferability), METHODS §5.3
    "editors-qualitative": ({"low", "some-concerns", "high"}, {"low", "some-concerns", "high"}),
    # the editors' checklist for evidence reports by public bodies (Surgeon General, IARC, National Academies, government
    # reviews), decision p-public-reports, METHODS §5.3
    "editors-report": ({"low", "some-concerns", "high"}, {"low", "some-concerns", "high"}),
}
SEVERITY = {
    "RoB 2": {"low": 0, "some-concerns": 1, "high": 2},
    "ROBINS-E": {"low": 0, "some-concerns": 1, "high": 2, "very-high": 3},
    "ROBINS-I": {"low": 0, "moderate": 1, "serious": 2, "critical": 3},
    "none-applicable": {"low": 0, "some-concerns": 1, "high": 2},
    "editors-qualitative": {"low": 0, "some-concerns": 1, "high": 2},
    "editors-report": {"low": 0, "some-concerns": 1, "high": 2},
}
MECHANICAL = {
    "ROBINS-E": {"moderate": "some-concerns", "serious": "high", "critical": "very-high"},
    "RoB 2": {"unclear": "some-concerns"},
}


def problems(card):
    rb = card.get("risk_of_bias") or {}
    inst = rb.get("instrument")
    if inst not in VOCAB:
        return [f"unknown instrument '{inst}'"]
    dv, ov = VOCAB[inst]
    out = []
    for i, d in enumerate(rb.get("domains", [])):
        if d.get("judgment") not in dv:
            out.append(f"{inst} domain {i} '{d.get('domain', '')[:50]}': '{d.get('judgment')}' is not {inst} vocabulary ({', '.join(sorted(dv))})")
    if rb.get("overall") not in ov:
        out.append(f"{inst} overall '{rb.get('overall')}' is not {inst} vocabulary ({', '.join(sorted(ov))})")
    sev = SEVERITY.get(inst)
    if sev and rb.get("overall") in sev:
        worst = max([sev.get(d.get("judgment"), -1) for d in rb.get("domains", [])] + [-1])
        if sev[rb["overall"]] < worst:
            out.append(f"{inst} overall '{rb['overall']}' is less severe than the worst domain")
    return out



# The instrument must match the design (METHODS §5.3). Designs with no listed instrument (case series, case reports,
# registry descriptions, modelling, in-vitro) are not checked: the card states the design's limits instead.
DESIGN_INSTRUMENT = {
    "narrative-review": {"none-applicable"},
    "meta-analysis": {"AMSTAR 2"}, "systematic-review": {"AMSTAR 2"},
    "rct": {"RoB 2"}, "crossover-rct": {"RoB 2"},
    # placebo-controlled within-person laboratory studies with randomized or counterbalanced order (METHODS §6.3)
    "human-laboratory": {"RoB 2"},
    "prospective-cohort": {"ROBINS-E", "ROBINS-I"}, "retrospective-cohort": {"ROBINS-E", "ROBINS-I"},
    "case-control": {"ROBINS-E", "ROBINS-I"},
    # a cross-sectional comparison of two ways of delivering an intervention (e.g. take-home against on-site drug checking) is a
    # non-randomized study of interventions: ROBINS-I, as METHODS §5.3 says for observational studies of interventions (27 October)
    "cross-sectional": {"ROBINS-E", "ROBINS-I", "JBI-prevalence"},
    "survey": {"JBI-prevalence"},
    "preclinical-animal": {"SYRCLE"},
    # a test compared with a reference method or known content, e.g. drug-checking strips (METHODS 0.3.1, §5.3)
    "test-accuracy": {"QUADAS-2"},
    "qualitative": {"editors-qualitative"},
    # a report by a public body that states how it weighs evidence and was externally reviewed; AMSTAR 2 where it states a systematic search
    "evidence-report": {"editors-report", "AMSTAR 2"},
}
LABEL = {"none-applicable": "the editors\u2019 narrative-review checklist (none-applicable)",
         "editors-qualitative": "the editors\u2019 qualitative checklist (editors-qualitative)",
         "editors-report": "the editors\u2019 evidence-report checklist (editors-report)"}


def design_problems(card):
    want = DESIGN_INSTRUMENT.get(card.get("design"))
    have = (card.get("risk_of_bias") or {}).get("instrument")
    if want and have not in want:
        label = " or ".join(LABEL.get(w, w) for w in sorted(want))
        return [f"design '{card.get('design')}' calls for {label}, but the card uses {have}"]
    return []


# AMSTAR 2 offers "partial yes" only for items 2, 4, 7, 8 and 9, and "no meta-analysis conducted" only for items 11, 12
# and 15 (Shea et al., 2017); every other item is yes or no. "no-information" is the editors' extension (METHODS §5.3).
AMSTAR_PARTIAL = {2, 4, 7, 8, 9}
AMSTAR_NOMA = {11, 12, 15}


def amstar_item_problems(card):
    rb = card.get("risk_of_bias") or {}
    if rb.get("instrument") != "AMSTAR 2":
        return []
    out = []
    for d in rb.get("domains", []):
        m = re.match(r"\s*(\d{1,2})\b", d.get("domain", ""))
        if not m:
            continue
        item, j = int(m.group(1)), d.get("judgment")
        if j == "partial-yes" and item not in AMSTAR_PARTIAL:
            out.append(f"AMSTAR 2 item {item} is judged 'partial yes', which AMSTAR 2 offers only for items 2, 4, 7, 8 and 9")
        if j == "no-meta-analysis" and item not in AMSTAR_NOMA:
            out.append(f"AMSTAR 2 item {item} is judged 'no meta-analysis', which applies only to items 11, 12 and 15")
    return out

def fix(card):
    rb = card.get("risk_of_bias") or {}
    inst = rb.get("instrument")
    log = card.setdefault("verification", {}).setdefault("editorial_corrections", [])
    changed = 0
    m = MECHANICAL.get(inst, {})
    for i, d in enumerate(rb.get("domains", [])):
        if d.get("judgment") in m:
            new = m[d["judgment"]]
            log.append({"date": TODAY, "field": f"risk_of_bias.domains[{i}].judgment", "from": d["judgment"], "to": new,
                        "reason": f"{inst} vocabulary: '{d['judgment']}' belongs to another tool; the judgment itself is unchanged (METHODS §5.3)."})
            d["judgment"] = new; changed += 1
    if rb.get("overall") in m:
        new = m[rb["overall"]]
        log.append({"date": TODAY, "field": "risk_of_bias.overall", "from": rb["overall"], "to": new,
                    "reason": f"{inst} vocabulary: '{rb['overall']}' belongs to another tool; the judgment itself is unchanged (METHODS §5.3)."})
        rb["overall"] = new; changed += 1
    sev = SEVERITY.get(inst)
    if sev and rb.get("overall") in sev:
        ranked = [(sev.get(d.get("judgment"), -1), d.get("judgment")) for d in rb.get("domains", [])]
        if ranked:
            worst_level, worst_word = max(ranked)
            if sev[rb["overall"]] < worst_level:
                log.append({"date": TODAY, "field": "risk_of_bias.overall", "from": rb["overall"], "to": worst_word,
                            "reason": f"{inst}: the overall judgment can be no less severe than the worst domain, which is '{worst_word}'. Domain judgments unchanged; the senior author may revisit the domain (METHODS §5.3)."})
                rb["overall"] = worst_word; changed += 1
    if not log:
        card["verification"].pop("editorial_corrections")
    return changed


def card_files():
    yield ROOT / "data" / "study-cards" / "methamphetamine.json", True
    for f in sorted(glob.glob(str(ROOT / "data" / "study-cards" / "*.json"))):
        if not f.endswith("methamphetamine.json"):
            yield pathlib.Path(f), True
    for f in sorted(glob.glob(str(ROOT / "data" / "study-cards" / "_incoming" / "*" / "*.json"))):
        yield pathlib.Path(f), False


def main():
    do_fix = "--fix" in sys.argv
    total = 0
    for path, is_list in card_files():
        data = json.load(open(path, encoding="utf-8"))
        cards = data if is_list else [data]
        changed = 0
        for c in cards:
            if do_fix:
                changed += fix(c)
            for p in problems(c):
                print(f"{c.get('id')}: {p}"); total += 1
        if do_fix and changed:
            path.write_text(json.dumps(data if is_list else cards[0], indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"  fixed {changed} judgments in {path.relative_to(ROOT)}")
    print(f"{total} problems remain")


if __name__ == "__main__":
    main()
