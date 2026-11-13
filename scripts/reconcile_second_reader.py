#!/usr/bin/env python3
"""Reconcile AI reader 2's blind extractions with reader 1's evidence anchors (METHODS §5.5, §6.2).

Reads data/verification/<round>/out/*.json (format: docs/VERIFICATION-BRIEF.md) and the claims. An anchor of reader 1 is
matched to an anchor of reader 2 for the same claim and source when they point to the same place (same printed page, or
overlapping locator words for web full texts) and agree on the numbers (at least 60% of reader 1's numbers appear in
reader 2's extraction, rounding allowed). Matched anchors on claims that reader 2 judged supported or partly supported
become 'ai-checked'; everything else stays 'ai-located' and is listed for the editor and the senior author.

Usage: reconcile_second_reader.py ROUND [--apply] [--claims FILE] [--cards FILE|DIR]
Writes data/verification/ROUND/report.md and report.json; with --apply, updates anchor statuses, claim statuses
(ai-anchored when every anchor is ai-checked or better) and card statuses (ai-checked when reader 2 confirmed every key
finding and agreed on risk of bias).
"""
import json, re, sys, glob, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[1]
rnd = sys.argv[1]; apply = "--apply" in sys.argv
TODAY = datetime.date.today().isoformat()
OUT = ROOT / "data" / "verification" / rnd

NUM = re.compile(r"(?<![\w.])[−-]?\d+(?:[.,]\d+)?(?![\w])")
def nums(t):
    out = []
    for m in NUM.findall(t or ""):
        x = m.replace("−", "-").replace(",", "")
        try:
            out.append((float(x.lstrip("-")), len(x.split(".")[1]) if "." in x else 0))
        except ValueError:
            pass
    return out
def pages(p):
    return set(int(x) for x in re.findall(r"\d+", p or "")) if re.search(r"\d", p or "") and "HTML" not in (p or "") else set()
STOP = set("the a an of and in on to for with by at from vs versus results table figure paragraph section".split())
def words(t):
    return set(w for w in re.findall(r"[a-z]{3,}", (t or "").lower()) if w not in STOP)

def num_agreement(a_text, b_text):
    A = [n for n in nums(a_text) if not (n[1] == 0 and n[0] < 10)]
    if not A:
        return None
    B = nums(b_text)
    hit = 0
    for x, dec in A:
        tol = 0.5 * 10 ** (-dec) + 1e-9
        if any(abs(x - y) <= tol or abs(round(y, dec) - x) <= tol for y, _ in B):
            hit += 1
    return hit / len(A)

def match(a, cands):
    best, best_s = None, -1.0
    for b in cands:
        pa, pb = pages(a["page"]), pages(b.get("page", ""))
        same_place = bool(pa & pb) if pa and pb else bool(words(a["locator"]) & words(b.get("locator", "")))
        na = num_agreement(a["extracted"], b.get("extracted", ""))
        if na is None:
            score = len(words(a["extracted"]) & words(b.get("extracted", ""))) / max(1, len(words(a["extracted"])))
            ok = same_place and score >= 0.3
        else:
            score = na
            ok = same_place and na >= 0.6 or (na >= 0.85 and len(nums(a["extracted"])) >= 3)
        if ok and score > best_s:
            best, best_s = b, score
    return best, best_s

def _arg(flag, default):
    return pathlib.Path(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else default
# --claims FILE and --cards FILE|DIR reconcile staged (incoming) claims and cards before they are merged
claims_path = _arg("--claims", ROOT / "data" / "claims" / "methamphetamine.json")
claims = json.load(open(claims_path, encoding="utf-8"))
cards_arg = _arg("--cards", ROOT / "data" / "study-cards" / "methamphetamine.json")
if cards_arg.is_dir():
    card_files = {json.load(open(f, encoding="utf-8"))["id"]: pathlib.Path(f) for f in sorted(glob.glob(str(cards_arg / "*.json")))}
    cards = [json.load(open(f, encoding="utf-8")) for f in card_files.values()]
else:
    card_files = None
    cards = json.load(open(cards_arg, encoding="utf-8"))
card_by = {c["id"]: c for c in cards}
outs = {pathlib.Path(f).stem: json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob(str(OUT / "out" / "*.json")))}

report = {"round": rnd, "date": TODAY, "anchors": [], "claims": [], "cards": []}
for c in claims:
    for i, a in enumerate(c["evidence"]):
        o = outs.get(a["reference"])
        if not o or a["anchor_status"] == "unchecked":
            continue
        ce = next((x for x in o.get("claims", []) if x.get("claim_id") == c["id"]), None)
        if not ce:
            report["anchors"].append({"claim": c["id"], "reference": a["reference"], "i": i, "result": "claim not covered by reader 2"}); continue
        b, s = match(a, ce.get("anchors", []))
        verdict = ce.get("verdict", "")
        ok = b is not None and verdict in ("supported", "partly-supported")
        report["anchors"].append({"claim": c["id"], "reference": a["reference"], "i": i, "page": a["page"], "locator": a["locator"],
                                  "result": "matched" if b else "no match", "score": round(s, 2) if b else None,
                                  "reader2_page": b.get("page") if b else None, "reader2_locator": b.get("locator") if b else None,
                                  "claim_verdict": verdict, "upgrade": ok})
        if ok and apply and a["anchor_status"] == "ai-located":
            a["anchor_status"] = "ai-checked"; a["checked_by"] = "AI reader 2"; a["checked_on"] = o.get("read_on", TODAY)
    for ref, o in outs.items():
        ce = next((x for x in o.get("claims", []) if x.get("claim_id") == c["id"]), None)
        if ce and (ce.get("verdict") not in ("supported",) or ce.get("overstatement")):
            report["claims"].append({"claim": c["id"], "reference": ref, "verdict": ce.get("verdict"),
                                     "overstatement": ce.get("overstatement", ""), "note": ce.get("note", "")})
    # the ladder is cumulative: a claim reaches ai-anchored only from metadata-verified (references checked first)
    if apply and all(e["anchor_status"] in ("ai-checked", "senior-verified") for e in c["evidence"]) and c["verification"]["status"] == "metadata-verified":
        c["verification"]["status"] = "ai-anchored"

for ref, o in outs.items():
    cid = "sc_" + ref.replace("-", "_")
    if o.get("card_check", {}) is None:  # the card was second-read in an earlier round: no card step this time
        continue
    cc = o.get("card_check") or {}
    kf = cc.get("key_findings", []); ri = cc.get("reporting_issues", [])
    bad_kf = [x for x in kf if x.get("verdict") not in ("confirmed",)]
    bad_ri = [x for x in ri if x.get("verdict") not in ("confirmed",)]
    rob = (cc.get("risk_of_bias") or {}).get("verdict", "")
    gap = (cc.get("interpretation_gap") or {}).get("verdict", "")
    card = card_by.get(cid)
    clean = (card is not None and not bad_kf and not bad_ri and rob == "agree" and gap in ("agree", "")
             and not cc.get("missed") and len(kf) >= len(card.get("key_findings", [])))
    report["cards"].append({"card": cid, "key_findings_flagged": bad_kf, "reporting_issues_flagged": bad_ri,
                            "risk_of_bias": cc.get("risk_of_bias"), "interpretation_gap": cc.get("interpretation_gap"),
                            "missed": cc.get("missed", []), "upgrade": clean})
    if apply and clean and card["verification"]["status"] == "first-pass":
        card["verification"]["status"] = "ai-checked"; card["verification"]["checked_by"] = "AI reader 2"
        card["verification"]["checked_on"] = o.get("read_on", TODAY)

if apply:
    json.dump(claims, open(claims_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False); open(claims_path, "a").write("\n")
    if card_files:
        for c in cards:
            card_files[c["id"]].write_text(json.dumps(c, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        json.dump(cards, open(cards_arg, "w", encoding="utf-8"), indent=1, ensure_ascii=False); open(cards_arg, "a").write("\n")
json.dump(report, open(OUT / "report.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

A = report["anchors"]
lines = [f"# Second-reader reconciliation — {rnd}", "", f"Run {TODAY}. Sources read by reader 2: {len(outs)}.", "",
         f"Anchors compared: {len(A)} · matched: {sum(1 for x in A if x['result'] == 'matched')} · upgraded to ai-checked: {sum(1 for x in A if x.get('upgrade'))}", "",
         "## Claim verdicts other than 'supported', or flagged wording", ""]
for x in report["claims"]:
    lines.append(f"- **{x['claim']}** · {x['reference']} · {x['verdict']}" + (f" · overstatement: {x['overstatement']}" if x['overstatement'] else "") + (f" — {x['note']}" if x['note'] else ""))
lines += ["", "## Anchors not matched", ""]
for x in A:
    if x["result"] != "matched":
        lines.append(f"- {x['claim']} · {x['reference']} · {x.get('page','')} · {x.get('locator','')} — {x['result']}")
lines += ["", "## Study cards", ""]
for x in report["cards"]:
    flag = "upgraded to ai-checked" if x["upgrade"] else "kept first-pass"
    lines.append(f"- **{x['card']}** — {flag}; key findings flagged: {len(x['key_findings_flagged'])}; reporting issues flagged: {len(x['reporting_issues_flagged'])}; risk of bias: {(x['risk_of_bias'] or {}).get('verdict','?')}")
    for k in x["key_findings_flagged"]:
        lines.append(f"  - finding {k.get('index')}: {k.get('verdict')} — {k.get('correction','')}")
    for k in x["reporting_issues_flagged"]:
        lines.append(f"  - reporting issue {k.get('index')}: {k.get('verdict')} — {k.get('note','')}")
    for m in x["missed"]:
        lines.append(f"  - missed: {m}")
(OUT / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines[:8]))
