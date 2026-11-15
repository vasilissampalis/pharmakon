#!/usr/bin/env python3
"""exam.py: the exam a machine checker must pass before any machine-written line is shown (docs/AUTOMATION.md).

    python3 -I scripts/auto/exam.py build              make data/auto/exam/cards.json from our own records
    python3 -I scripts/auto/exam.py run [CANDIDATE]    measure a candidate on it; writes data/auto/exam/result-<candidate>.json

The exam is made of work our readers already did. Each item is one Myth or fact? card (a statement, Myth or Fact, and a
one- or two-sentence why) that a writer wrote from an answer's checked plain lines, together with those lines, and the
decision of a blind checker who had written none of it (data/verification/*/tasks_check*.json and check_out*.json). The
checker's task was the checker's task we want a machine to do: does the card say only what the lines say?

  good items   cards passed as written, and the cards the checkers rewrote (their corrected versions)
  bad items    cards the checker found to say something the lines do not support (data/auto/exam/labels-cards.json: the
               checkers' reasons, sorted by the editor): a word, a number or a cause the lines do not hold, a finding said
               of more people than were studied, a report said as a fact
  left out     cards changed for form only (length, clarity, a trick) and second wordings of one card: they are neither
               right nor wrong sentences; cards refused for a content rule (timing, amounts) go to the rules' own test

A candidate is a function (the lines, the card) -> pass or stop. The bar (the senior author's rule for the machine lane,
15 November 2026): of everything a candidate lets through, at most 1 item in 50 may be a bad one. The exam also says how
many good items it stops, because a checker that stops everything is perfectly safe and useless.

The exam is small (see the counts it prints): it can show that a candidate is NOT good enough; passing it once is not
proof, which is why the result carries its range, and why the exam grows with every blind check our readers do.

Candidates here: "none" (lets everything through: the base rate), "numbers" (gate 2 alone: every number in the card is
in the lines). Model candidates are added by scripts that write their decisions as {item id: true|false} and call score().
"""
import sys, json, re, glob, os, pathlib, math

ROOT = pathlib.Path(__file__).resolve().parents[2]
EXAM = ROOT / "data" / "auto" / "exam"
BAR = 1 / 50


def build():
    labels = json.load(open(EXAM / "labels-cards.json", encoding="utf-8"))["labels"]
    items, seen = [], set()
    for out in sorted(glob.glob(str(ROOT / "data" / "verification" / "*" / "check_out*.json"))):
        d = os.path.dirname(out); n = os.path.basename(out)[len("check_out"):-len(".json")]; tf = os.path.join(d, "tasks_check" + n + ".json")
        if not os.path.exists(tf): continue
        tasks = {x["n"]: x for x in json.load(open(tf, encoding="utf-8")).get("quiz", [])}
        for x in json.load(open(out, encoding="utf-8")).get("quiz", []):
            t = tasks.get(x["n"])
            if not t or t.get("kind") != "tf" or not t.get("lines"): continue
            key = os.path.basename(d) + "/" + n + "#" + str(x["n"])
            lines = {k: t["lines"].get(k) for k in ("short", "but", "how")}
            card = lambda it: {"statement": it["statement"], "answer": bool(it["answer"]), "why": it.get("why", "")}
            if x["verdict"] == "ok": items.append({"id": key, "good": True, "from": "passed as written", "claim": t["item"].get("claim"), "lines": lines, "card": card(t["item"])})
            else:
                lab = labels.get(key)
                if lab is None: sys.exit("exam: a card that was not passed has no label yet (data/auto/exam/labels-cards.json): " + key)
                if lab["label"] == "support": items.append({"id": key, "good": False, "from": "stopped by the checker", "what": lab["what"], "claim": t["item"].get("claim"), "lines": lines, "card": card(t["item"])})
                fx = x.get("item") or {}
                if x["verdict"] == "fix" and fx.get("statement") and "answer" in fx: items.append({"id": key + "+fixed", "good": True, "from": "the checker's corrected card", "claim": t["item"].get("claim"), "lines": lines, "card": card(fx)})
    for it in items:
        assert it["id"] not in seen, it["id"]; seen.add(it["id"])
    good = sum(1 for i in items if i["good"]); bad = len(items) - good
    json.dump({"_note": "The exam's items, made by scripts/auto/exam.py build from the blind checks on file. good: the card says only what the lines say; not good: a blind checker found it to say something the lines do not support.",
               "good": good, "bad": bad, "items": items}, open(EXAM / "cards.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"exam: {len(items)} items: {good} good ({sum(1 for i in items if i['from'] == 'passed as written')} passed as written, {sum(1 for i in items if i['from'].startswith('the checker'))} corrected by a checker), {bad} that say something the lines do not support")


def wilson(k, n, z=1.96):
    """The range a true share can lie in when k of n were seen (95 in 100 times)."""
    if n == 0: return (0.0, 1.0)
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def score(name, decisions, note=""):
    """decisions: {item id: True (let through) | False (stopped)}. Prints and writes the result."""
    items = json.load(open(EXAM / "cards.json", encoding="utf-8"))["items"]
    missing = [i["id"] for i in items if i["id"] not in decisions]
    if missing: sys.exit(f"exam: {len(missing)} items have no decision, for example {missing[0]}")
    through = [i for i in items if decisions[i["id"]]]; bad_through = [i for i in through if not i["good"]]
    good = [i for i in items if i["good"]]; bad = [i for i in items if not i["good"]]
    good_stopped = [i for i in good if not decisions[i["id"]]]
    share = len(bad_through) / len(through) if through else 0.0; lo, hi = wilson(len(bad_through), len(through))
    res = {"candidate": name, "note": note, "items": len(items), "good": len(good), "bad": len(bad), "let_through": len(through), "wrong_let_through": len(bad_through),
           "wrong_share": round(share, 4), "wrong_share_range": [round(lo, 4), round(hi, 4)], "bar": BAR,
           "passes": bool(through) and hi <= BAR, "under_the_bar_as_counted": bool(through) and share <= BAR,
           "bad_caught": len(bad) - len(bad_through), "good_stopped": len(good_stopped), "good_stopped_share": round(len(good_stopped) / len(good), 4) if good else 0.0,
           "wrong_let_through_ids": [i["id"] for i in bad_through][:60]}
    json.dump(res, open(EXAM / ("result-" + re.sub(r"[^a-z0-9-]", "-", name.lower()) + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"exam, candidate \"{name}\": lets {len(through)} of {len(items)} through, {len(bad_through)} of them wrong: {100 * share:.1f} in 100 (range {100 * lo:.1f} to {100 * hi:.1f}; the bar is 2.0)."
          f" It catches {res['bad_caught']} of the {len(bad)} wrong cards and stops {len(good_stopped)} of the {len(good)} good ones ({100 * res['good_stopped_share']:.0f} in 100)."
          f" {'PASSES' if res['passes'] else 'Under the bar as counted, but the range is too wide to call it passed' if res['under_the_bar_as_counted'] else 'Does not pass'}.")
    return res


# ---- candidates that need no model ----
NUM = re.compile(r"\d+(?:[.,]\d+)*")
WORDS = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10", "half": "half", "twice": "twice", "double": "double", "third": "third", "quarter": "quarter"}


def numbers(text):
    t = text.lower().replace(",", "")
    return set(NUM.findall(t)) | {WORDS[w] for w in re.findall(r"[a-z]+", t) if w in WORDS}


def cand_numbers(lines, card):
    """Gate 2 alone: every number in the card (statement and why) is in the lines."""
    src = numbers(" ".join([lines.get("short") or "", lines.get("but") or ""] + list(lines.get("how") or [])))
    return numbers(card["statement"] + " " + card["why"]) <= src


def run(name):
    items = json.load(open(EXAM / "cards.json", encoding="utf-8"))["items"]
    if name == "none": return score("none", {i["id"]: True for i in items}, "lets everything through: how many wrong cards there are to catch")
    if name == "numbers": return score("numbers", {i["id"]: cand_numbers(i["lines"], i["card"]) for i in items}, "gate 2 alone: every number in the card is in the lines")
    sys.exit("exam: no candidate named " + name)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "build": build()
    elif cmd == "run":
        for c in (sys.argv[2:] or ["none", "numbers"]): run(c)
    else: sys.exit(__doc__)
