#!/usr/bin/env python3
"""panel.py: which judges, together, let the fewest wrong sentences through? (docs/AUTOMATION.md, decisions 21 and 23)

    python3 -I scripts/auto/panel.py                 (both exams: every judge alone, and every two and three together)
    python3 -I scripts/auto/panel.py --most 2        (alone and in twos only)
    python3 -I scripts/auto/panel.py --selftest

No judge we have is good enough alone: each sat the exam and each lets wrong cards through. But they are different kinds
of reader (rules in code, large open models at three services, a small model of our own that we run ourselves), and what
one misses another may catch. A sentence is kept only if EVERY judge of a panel accepts it. This file counts, from the
results on file and without asking any model anything, what each panel would have done on the items all its judges saw:
how many wrong ones it would have let through, and how many good ones it would have stopped.

The judges it knows:
  rules            the lane's rules in code (lane.says_more_text and lane.hedges), computed here
  model files      data/auto/exam/model-<name>.json (the cards) and model-<name>-lane.json (the lane's own sentences)
  our own models   data/auto/own/candidates/<name>.scores.json, at the threshold the candidate carries

Two exams: the cards (data/auto/exam/cards.json) and the lane's own sentences (lane-sentences.json: the real task, small).
For the cards it also says how many of the wrong cards a panel caught are ones whose fault a sentence-reader can see at
all (cards-where.json): a catch of one of the others is luck.

It decides nothing. The editor reads the table and names the panel in data/auto/lane/models.json; the reason is written
in docs/STATUS.md with these numbers.
"""
import sys, re, json, pathlib, itertools

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
EXAM = ROOT / "data" / "auto" / "exam"
OWN = ROOT / "data" / "auto" / "own" / "candidates"


def load(p, default=None):
    try: return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError): return default


def true_part(card):
    why = [x.strip() for x in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9“\"'(\[])", re.sub(r"^(?:true|false|myth|fact)[.!:]?\s+", "", card.get("why") or "", flags=re.I)) if x.strip()]
    return ([card["statement"]] if card["answer"] else []) + why


def rules_judge(cards, sents):
    """The lane's rules in code as a judge: {item id: let through} for the cards (their true part) and for the lane's sentences."""
    import lane
    def ok(ours, src): return not lane.says_more_text(ours, src) and not lane.hedges([{"part": "x", "text": ours, "uses": ["A"]}], {"A": {"quote": src, "passage_text": ""}})
    lines = lambda L: " ".join(t for t in [L.get("short") or "", L.get("but") or ""] + list(L.get("how") or []) if t)
    return ({i["id"]: all(ok(s, lines(i["lines"])) for s in true_part(i["card"])) for i in cards},
            {i["id"]: ok(i["sentence"], " ".join(i["rests_on"])) for i in sents})


def judges(cards, sents, exam=None, own=None):
    """{judge's name: ({card id: through}, {sentence id: through})} from what is on file."""
    out = {"rules": rules_judge(cards, sents)}
    for f in sorted((exam or EXAM).glob("model-*.json")):
        d = load(f) or {}
        if d.get("how") == "pieces" or not isinstance(d.get("cards"), dict): continue
        name = str(d.get("model") or f.stem) + ("" if not d.get("effort") or f.stem.endswith("-lane") or not re.search(r"-(low|medium|high)$", f.stem) else " (" + d["effort"] + ")")
        got = {k: bool(v.get("through")) for k, v in d["cards"].items() if v.get("clear")}          # no clear word is no verdict: such an item is not counted for this judge
        c, s = out.setdefault(name, ({}, {}))
        (s if f.stem.endswith("-lane") else c).update(got)
    for f in sorted((own or OWN).glob("*.scores.json")):
        rec = load(f.with_name(f.name.replace(".scores.json", ".json"))) or {}; d = load(f) or {}; t = rec.get("threshold")
        if not isinstance(t, (int, float)): continue
        out[f.name.replace(".scores.json", "") + f" (ours, at {t})"] = ({r["id"]: all(x >= t for x in r["scores"]) for r in d.get("items") or [] if r.get("scores")},
                                                                    {r["id"]: all(x >= t for x in r["scores"]) for r in d.get("lane") or [] if r.get("scores")})
    return out


def count(panel, verdicts, items):
    """What a panel (names) does on the items all its judges saw: a dict of counts, or None when they share too few items."""
    seen = [i for i in items if all(i["id"] in verdicts[j] for j in panel)]
    bad = [i for i in seen if not i["good"]]; good = [i for i in seen if i["good"]]
    if not bad or not good: return None
    through = lambda i: all(verdicts[j][i["id"]] for j in panel)
    return {"panel": list(panel), "wrong_seen": len(bad), "wrong_through": sum(through(i) for i in bad), "good_seen": len(good), "good_stopped": sum(not through(i) for i in good),
            "wrong_through_ids": [i["id"] for i in bad if through(i)]}


def table(js, which, items, most=3, least_wrong=8, least_good=8):
    rows = []; names = [n for n in js if js[n][which]]
    v = {n: js[n][which] for n in names}
    for k in range(1, most + 1):
        for panel in itertools.combinations(names, k):
            r = count(panel, v, items)
            if r and r["wrong_seen"] >= least_wrong and r["good_seen"] >= least_good: rows.append(r)
    rows.sort(key=lambda r: (r["wrong_through"] / r["wrong_seen"], r["good_stopped"] / r["good_seen"], len(r["panel"])))
    return rows


def show(rows, title, visible=None, top=14):
    print(title)
    singles = [r for r in rows if len(r["panel"]) == 1]
    for label, part in (("each judge alone", singles), (f"the {top} best panels (fewest wrong let through, then fewest good stopped)", [r for r in rows if len(r["panel"]) > 1][:top])):
        print("  " + label + ":")
        for r in part:
            extra = ""
            if visible is not None:
                caught = r["wrong_seen"] - r["wrong_through"]; cv = sum(1 for i in visible["seen"](r) if i not in r["wrong_through_ids"] and visible["is"](i))
                extra = f"  [of the {caught} caught, {cv} are faults a sentence-reader can see]"
            print(f"    lets {r['wrong_through']:>2} of {r['wrong_seen']:>2} wrong through, stops {r['good_stopped']:>3} of {r['good_seen']:>3} good ({100 * r['good_stopped'] / r['good_seen']:.0f} in 100): " + " + ".join(r["panel"]) + extra)


def selftest():
    items = [{"id": "w1", "good": False}, {"id": "w2", "good": False}, {"id": "g1", "good": True}, {"id": "g2", "good": True}, {"id": "g3", "good": True}]
    v = {"a": {"w1": True, "w2": False, "g1": True, "g2": True, "g3": False}, "b": {"w1": False, "w2": True, "g1": True, "g2": False, "g3": True}, "c": {"w1": True, "g1": True}}
    assert count(["a"], v, items) == {"panel": ["a"], "wrong_seen": 2, "wrong_through": 1, "good_seen": 3, "good_stopped": 1, "wrong_through_ids": ["w1"]}
    r = count(["a", "b"], v, items); assert r["wrong_through"] == 0 and r["good_stopped"] == 2                       # kept only if every judge accepts: what one misses the other catches, and both stop some good ones
    r = count(["a", "c"], v, items); assert r["wrong_seen"] == 1 and r["good_seen"] == 1 and r["wrong_through"] == 1     # only the items all the judges of a panel saw
    assert count(["c"], {"c": {"g1": True}}, items) is None
    rows = table({"a": (v["a"], {}), "b": (v["b"], {})}, 0, items, most=2, least_wrong=2, least_good=2)
    assert rows[0]["panel"] == ["a", "b"] and len(rows) == 3
    assert true_part({"statement": "It is so.", "answer": False, "why": "False. It is not. One study said so."}) == ["It is not.", "One study said so."]
    print("panel selftest: ok (a sentence is kept only if every judge of a panel accepts it; a panel is counted on the items all its judges saw; panels are ordered by wrong let through, then good stopped)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest(); sys.exit(0)
    most = int(a[a.index("--most") + 1]) if "--most" in a else 3
    cards = (load(EXAM / "cards.json") or {}).get("items") or []; sents = (load(EXAM / "lane-sentences.json") or {}).get("items") or []
    where = (load(EXAM / "cards-where.json") or {}).get("cards") or {}
    js = judges(cards, sents)
    print("judges on file:", "; ".join(f"{n} ({len(c)} cards, {len(s)} of the lane's sentences)" for n, (c, s) in js.items()))
    vis = {"is": lambda cid: bool((where.get(cid) or {}).get("at")), "seen": lambda r: [i["id"] for i in cards if not i["good"] and all(i["id"] in js[j][0] for j in r["panel"])]} if where else None
    show(table(js, 0, cards, most), f"\nTHE CARDS ({sum(not i['good'] for i in cards)} wrong, {sum(i['good'] for i in cards)} good; {sum(1 for w in where.values() if w.get('at'))} of the wrong ones have a fault a sentence-reader can see)", vis)
    show(table(js, 1, sents, most, least_wrong=5, least_good=5), f"\nTHE LANE'S OWN SENTENCES ({sum(not i['good'] for i in sents)} not good, {sum(i['good'] for i in sents)} good)")
