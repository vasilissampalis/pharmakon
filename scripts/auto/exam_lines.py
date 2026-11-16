#!/usr/bin/env python3
"""exam_lines.py: the exam of plain lines (docs/AUTOMATION.md, decision 23): a technical source, a plain line, and a
blind checker's verdict. This is the lane's own kind of task, made of work our readers already did.

    python3 -I scripts/auto/exam_lines.py build      (makes data/auto/exam/lines.json from our own records)
    python3 -I scripts/auto/exam_lines.py --selftest

Where it comes from. When an answer's plain lines were written (the short answer, the But, the How-do-we-know points), a
blind checker who had written none of them read each line against the checked claim: its statement, who was studied, what
was compared, what was measured, the figures, and the reasons for its certainty (data/verification/*/tasks_check*.json,
"lines"; the verdicts in check_out*.json). The checker passed a line or rewrote it and said why.

  good items   lines the checker left as written, and the lines the checker rewrote (the corrected versions)
  bad items    lines as first written that the checker changed because they said something the claim does not carry
               (data/auto/exam/labels-lines.json: every changed line, sorted by the editor from the checker's own
               reason): a hedge dropped, a self-report said as a fact, a word that is not in the claim, a finding said
               of more than was studied, a figure set against the wrong one
  left out     lines changed for form only (two sentences joined, a clearer word, an order, something added that was
               missing): as first written they are neither right nor wrong

A judge reads a line beside the claim's own fields (the "premise" of a claim, kept once for each claim). The exam can show
that a judge is not good enough; it cannot show that one is. It grows with every blind check of plain lines.
"""
import sys, os, re, json, glob, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
EXAM = ROOT / "data" / "auto" / "exam"
VER = ROOT / "data" / "verification"
FIELDS = [("statement", "THE CLAIM"), ("population", "WHO WAS STUDIED"), ("exposure", "WHAT THEY TOOK OR DID"), ("comparator", "COMPARED WITH"), ("outcome", "WHAT WAS MEASURED"), ("magnitude", "THE FIGURES"), ("reasoning", "HOW SURE, AND WHY")]


def premise(task):
    """The claim as the blind checker saw it: [(label, text)] for the fields that hold something."""
    return [(label, re.sub(r"\s+", " ", str(task[k])).strip()) for k, label in FIELDS if task.get(k)]


def checks(ver=None):
    """[(where, the task, the checker's answer)] for every blind check of plain lines on file, in a fixed order."""
    out = []
    for tf in sorted(glob.glob(str((ver or VER) / "*" / "tasks_check*.json"))):
        if tf.endswith("_key.json"): continue
        of = os.path.join(os.path.dirname(tf), "check_out" + os.path.basename(tf)[len("tasks_check"):])
        if not os.path.exists(of): continue
        try: T = {x["id"]: x for x in json.load(open(tf, encoding="utf-8")).get("lines", [])}; O = json.load(open(of, encoding="utf-8")).get("lines", [])
        except (ValueError, KeyError, TypeError): continue
        where = os.path.basename(os.path.dirname(tf)) + "/" + os.path.basename(tf)[len("tasks_check"):-len(".json")]
        out += [(where, T[o["id"]], o) for o in O if o.get("id") in T]
    return out


def lines_of(task):
    """A task's lines as [(key, text)]: short, but, how1, how2, ..."""
    L = task.get("lines") or {}
    return [(k, L[k]) for k in ("short", "but") if L.get(k)] + [(f"how{n}", t) for n, t in enumerate(L.get("how") or [], 1) if t]


def changed(task, answer):
    """{key: the checker's line} for the lines the checker changed (short, but, how1, ...): only lines that existed before."""
    old = dict(lines_of(task)); new = {}; f = answer.get("fields") or {}
    for k in ("short", "but"):
        if isinstance(f.get(k), str) and old.get(k) and f[k] != old[k]: new[k] = f[k]
    if isinstance(f.get("how"), list):
        for n, t in enumerate(f["how"], 1):
            if old.get(f"how{n}") and t and t != old[f"how{n}"]: new[f"how{n}"] = t
    return new


def build(ver=None, labels=None, out=None):
    labels = labels if labels is not None else json.load(open(EXAM / "labels-lines.json", encoding="utf-8"))["labels"]
    claims, items, unsorted = {}, [], []
    for where, task, ans in checks(ver):
        key = where + ":" + task["id"]; ch = changed(task, ans) if ans.get("verdict") != "ok" else {}
        mine = labels.get(key) or {}
        if set(ch) != set(mine): unsorted.append((key, sorted(ch), sorted(mine))); continue
        claims[key] = premise(task); why = re.sub(r"\s+", " ", str(ans.get("reason") or ""))[:700]
        for k, text in lines_of(task):
            if k not in ch: items.append({"id": f"{key}#{k}", "claim": key, "good": True, "from": "passed as written", "line": text}); continue
            if mine[k] == "bad": items.append({"id": f"{key}#{k}~was", "claim": key, "good": False, "from": "changed by the checker for what it said", "line": text, "what": why, "now": ch[k]})
            items.append({"id": f"{key}#{k}", "claim": key, "good": True, "from": "the checker's corrected line", "line": ch[k]})
    if unsorted: sys.exit("exam_lines: lines a checker changed that the editor has not sorted (data/auto/exam/labels-lines.json): " + "; ".join(f"{k}: changed {c}, sorted {m}" for k, c, m in unsorted[:6]))
    seen = set()
    for it in items: assert it["id"] not in seen, it["id"]; seen.add(it["id"])
    good = sum(i["good"] for i in items); bad = len(items) - good
    doc = {"_note": "The exam of plain lines, made by scripts/auto/exam_lines.py build from the blind checks of plain lines on file. An item is one plain line beside the checked claim it was written from ('claims': the claim as the blind checker saw it). "
                    "good: the checker left the line as written, or it is the checker's corrected line; not good: the line as first written, which the checker changed because it said something the claim does not carry ('what': the checker's reason; 'now': the corrected line). "
                    "Lines changed for form only are left out.",
           "good": good, "bad": bad, "claims": {k: [list(x) for x in v] for k, v in claims.items()}, "items": items}
    if out is not False: json.dump(doc, open(out or EXAM / "lines.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"exam of plain lines: {len(items)} items from {len(claims)} checked claims: {good} good ({sum(1 for i in items if i['from'] == 'passed as written')} passed as written, {sum(1 for i in items if i['from'].startswith('the checker'))} corrected by a checker), "
          f"{bad} that say something the claim does not carry")
    return doc


def premise_text(doc, claim):
    """A claim's premise as one text (for a model that reads a passage and a sentence)."""
    return " ".join(t for _, t in doc["claims"][claim])


def selftest():
    import tempfile
    v = pathlib.Path(tempfile.mkdtemp()); d = v / "check-x"; d.mkdir()
    json.dump({"lines": [{"id": "cl_a", "statement": "People SAID desire often rose.", "population": "20 men", "lines": {"q": "?", "short": "Desire often goes up.", "but": "It is one survey. It was small.", "how": ["20 men were asked.", "Most were young."]}},
                         {"id": "cl_b", "statement": "S", "lines": {"short": "Fine.", "but": "Also fine.", "how": ["Good."]}}]}, open(d / "tasks_check7.json", "w"))
    json.dump({"lines": [{"id": "cl_a", "verdict": "fix", "reason": "Short stated a recollection as a fact. But joined.", "fields": {"short": "People say desire often goes up.", "but": "It is one small survey.", "how": ["20 men were asked.", "Most were young.", "A new point."]}},
                         {"id": "cl_b", "verdict": "ok", "reason": "", "fields": {}}]}, open(d / "check_out7.json", "w"))
    json.dump({"quiz_key": []}, open(d / "tasks_check7_key.json", "w"))
    t = checks(v)[0][1]
    assert changed(t, checks(v)[0][2]) == {"short": "People say desire often goes up.", "but": "It is one small survey."}                # a point the checker added is not a changed line
    assert premise(t) == [("THE CLAIM", "People SAID desire often rose."), ("WHO WAS STUDIED", "20 men")]
    doc = build(v, {"check-x/7:cl_a": {"short": "bad", "but": "form"}}, out=False)
    ids = {i["id"]: i for i in doc["items"]}
    assert not ids["check-x/7:cl_a#short~was"]["good"] and ids["check-x/7:cl_a#short~was"]["line"] == "Desire often goes up." and ids["check-x/7:cl_a#short"]["line"] == "People say desire often goes up."
    assert "check-x/7:cl_a#but~was" not in ids and ids["check-x/7:cl_a#but"]["line"] == "It is one small survey." and ids["check-x/7:cl_a#how2"]["from"] == "passed as written"      # a line changed for form: only its corrected version is an item
    assert doc["good"] == 7 and doc["bad"] == 1 and premise_text(doc, "check-x/7:cl_a") == "People SAID desire often rose. 20 men"
    try: build(v, {}, out=False); raise AssertionError("lines nobody sorted were used")
    except SystemExit as e: assert "has not sorted" in str(e)
    print("exam_lines selftest: ok (a line the checker changed for what it said is a wrong item and its corrected version a good one; a line changed for form is only its corrected version; a changed line nobody sorted stops the build)")


if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    elif len(sys.argv) > 1 and sys.argv[1] == "build": build()
    else: sys.exit(__doc__)
