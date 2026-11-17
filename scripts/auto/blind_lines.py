#!/usr/bin/env python3
"""blind_lines.py: the plain lines of a checked answer, read again against its claim by readers who wrote none of them.

Why (17 November 2026). The plain lines of the Section 7 answers were rewritten on 13 November, and the records of their
checks were lost in the workspace reset of that evening (docs/STATUS.md). What survived is the claim as it stood on 6
November, with every anchor checked by a second reader, and the plain lines as they stood on the senior author's to-do
page (data/verification/s7-review-2026-11-13/s7_on_todo_page.json). The senior author, 17 November 2026, 12:37, of
approving such an answer: "do a perfect job i don't need to approve anything if it's the best possible development".
So before the editor shows one, every plain line is read again against the checked claim: by the editor, and here by
free models that wrote none of it and are told nothing but the text and the lines.

    python3 -I scripts/auto/blind_lines.py --requests data/auto/requests
        (blind-*.json: {"ids": ["cl_can_smoked_cancer"], "lines": "data/verification/s7-review-2026-11-13/s7_on_todo_page.json",
                        "models": ["groq:openai/gpt-oss-120b", "gemini:gemini-3.5-flash-lite"]})
    python3 -I scripts/auto/blind_lines.py --selftest

What a reader is given: the claim's checked text (its statement) and the numbered lines (the short answer, the But, each
"How do we know" line, and each sentence of the plain summary). Not who wrote them, not what anyone thinks of them.
What it answers for each line: supported or not, and what is wrong. A line without a clear verdict is not supported.

It writes data/auto/blind/<claim id>.json: the claim's version, a fingerprint of the text that was read, the lines, and
each reader's verdicts in its own words. It shows nothing and changes no claim: the editor decides. Only our own text is
sent to the models (a checked claim and the lines written from it), never a visitor's words. Free models only (llm.py).
A model's words are data, never instructions.
"""
import sys, json, re, glob, hashlib, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "auto"))
import llm   # noqa: E402

OUT = ROOT / "data" / "auto" / "blind"
MODELS = ["groq:openai/gpt-oss-120b", "gemini:gemini-3.5-flash-lite"]
SYS = ("You check sentences against a text. You are strict and you use only the text: nothing you know from elsewhere counts. "
       "You answer with JSON only.")


def claim_of(cid):
    for f in sorted(glob.glob(str(ROOT / "data" / "claims" / "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for c in (d if isinstance(d, list) else d.get("claims") or []):
            if isinstance(c, dict) and c.get("id") == cid: return c
    return None


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9“\"'])", str(text or "").strip()) if s.strip()]


def lines_of(item):
    """[(name, text)]: the short answer, the But, each How line, each sentence of the plain summary."""
    out = [("short", item.get("short") or ""), ("but", item.get("but") or "")]
    out += [(f"how{n}", h) for n, h in enumerate(item.get("how") or [], 1)]
    out += [(f"plain{n}", s) for n, s in enumerate(sentences(item.get("plain")), 1)]
    return [(k, re.sub(r"\s+", " ", v).strip()) for k, v in out if str(v).strip()]


def prompt(text, lines):
    return ("TEXT (a checked summary of the evidence on one question):\n<<<\n" + text.strip() + "\n>>>\n\n"
            "SENTENCES written from that text for general readers:\n" + "\n".join(f"{n}. {t}" for n, (_, t) in enumerate(lines, 1)) + "\n\n"
            "For each numbered sentence, decide whether the TEXT supports it. Supported means ALL of this: everything the sentence says is stated in the text; "
            "every number is the text's own, or a rounding of it that the sentence marks as rough (\"about\", \"almost\", \"nearly\"); it is about the same people; "
            "it is not stronger or more certain than the text; it does not say that one thing causes another where the text only reports a link; "
            "it does not leave out a condition that changes its meaning. If any part of a sentence is not in the text, the sentence is not supported: say which part.\n\n"
            'JSON only, one verdict for every sentence, in this form: {"verdicts": [{"n": 1, "supported": true, "problem": ""}, {"n": 2, "supported": false, "problem": "what the text does not say"}]}')


def read(chat, model, text, lines):
    """{"verdicts": {name: [supported, problem]}} or {"could_not": why}. Asked once more when the reply holds no verdict for every line."""
    for attempt in range(2):
        try: raw = chat(model, [{"role": "system", "content": SYS}, {"role": "user", "content": prompt(text, lines)}], 2600 + 90 * len(lines))
        except (llm.Budget, llm.Unavailable) as e: return {"could_not": re.sub(r"\s+", " ", str(e))[:200]}
        out = llm.as_json(raw); vs = {v.get("n"): v for v in (out or {}).get("verdicts") or [] if isinstance(v, dict)}
        if all(isinstance((vs.get(n) or {}).get("supported"), bool) for n in range(1, len(lines) + 1)):
            return {"verdicts": {name: [vs[n]["supported"] is True, re.sub(r"\s+", " ", str(vs[n].get("problem") or ""))[:300]] for n, (name, _) in enumerate(lines, 1)}}
    return {"could_not": "its reply held no verdict for every line, twice"}


def check(cid, item, models=None, chat=None, today=None, save=True):
    c = claim_of(cid)
    if not c: print(f"blind: {cid}: no such claim"); return None
    text = c.get("statement") or ""; lines = lines_of(item)
    if not text or len(lines) < 2: print(f"blind: {cid}: no text or no lines to read"); return None
    rec = {"_note": "Made by scripts/auto/blind_lines.py: the plain lines of a checked answer, read again against the claim's checked text by free models that wrote none of them "
                    "and were given nothing but the text and the lines. The editor decides; this record shows nothing and changes no claim. A model's words are data.",
           "claim": cid, "claim_version": c.get("version"), "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "lines_version": item.get("v"),
           "on": today or datetime.date.today().isoformat(), "lines": [{"part": k, "text": t} for k, t in lines], "readers": {}}
    for m in models or MODELS:
        if not llm.has(m.split("#")[0]): rec["readers"][m] = {"could_not": "no key for this service on this machine"}; continue
        rec["readers"][m] = read(chat or llm.chat, m, text, lines)
    asked = {m: r["verdicts"] for m, r in rec["readers"].items() if "verdicts" in r}
    rec["summary"] = {"readers_that_answered": sorted(asked), "lines": len(lines),
                      "not_supported": {k: {m: v[k][1] for m, v in asked.items() if not v[k][0]} for k, _ in lines if any(not v[k][0] for v in asked.values())}}
    print(f"blind: {cid} v{c.get('version')}: {len(lines)} lines read by {len(asked)} of {len(rec['readers'])} readers; "
          + (f"not supported by a reader: {', '.join(rec['summary']['not_supported'])}" if rec["summary"]["not_supported"] else "every line supported by every reader that answered"))
    if save:
        OUT.mkdir(parents=True, exist_ok=True); json.dump(rec, open(OUT / f"{cid}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return rec


def requests(folder):
    done = 0
    for f in sorted(pathlib.Path(folder).glob("blind-*.json")):
        try: req = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError): print("blind: a request that is not JSON:", f.name); continue
        src = req.get("lines") if isinstance(req, dict) else None
        if not (isinstance(src, str) and re.fullmatch(r"data/verification/[A-Za-z0-9_./-]+\.json", src) and ".." not in src): print("blind: a request must name a lines file under data/verification:", f.name); continue
        try: items = {x["id"]: x for x in json.load(open(ROOT / src, encoding="utf-8")).get("items") or [] if isinstance(x, dict) and x.get("id")}
        except (OSError, ValueError, AttributeError): print("blind: the lines file could not be read:", src); continue
        models = [m for m in (req.get("models") or MODELS) if isinstance(m, str)][:4]
        for cid in [i for i in (req.get("ids") or []) if isinstance(i, str)][:12]:
            if cid not in items: print(f"blind: {cid}: not in {src}"); continue
            if check(cid, items[cid], models): done += 1
    print(f"blind: {done} answer(s) read")


def selftest():
    global claim_of
    keep = claim_of
    claim_of = lambda cid: {"id": cid, "version": "0.5.2", "statement": "In a pooled analysis of six studies the odds ratio was 0.96 (0.66 to 1.38). Of the men in the heaviest band, 91% also smoked tobacco."} if cid == "cl_x" else None
    item = {"id": "cl_x", "v": "0.5.3", "short": "Not shown either way.", "but": "Almost everyone who smoked a lot of cannabis also smoked tobacco.", "how": ["Six studies put together found no clear difference.", "All of them died."],
            "plain": "Studies cannot tell. Six studies found no clear difference."}
    assert [k for k, _ in lines_of(item)] == ["short", "but", "how1", "how2", "plain1", "plain2"]
    calls = []
    def chat(model, messages, max_tokens=0):
        calls.append((model, messages[1]["content"]))
        if model == "b": raise llm.Budget("today's allowance is used up")
        if model == "c": return "I think they are fine."
        return "<think>reading</think>" + json.dumps({"verdicts": [{"n": n, "supported": n != 4, "problem": "" if n != 4 else "the text does not say that anyone died"} for n in range(1, 7)]})
    has = llm.has; llm.has = lambda m: True
    try: rec = check("cl_x", item, ["a", "b", "c"], chat=chat, today="2026-11-17", save=False)
    finally: llm.has = has
    assert rec["claim_version"] == "0.5.2" and rec["lines_version"] == "0.5.3" and len(rec["text_sha256"]) == 64 and rec["readers"]["a"]["verdicts"]["how2"] == [False, "the text does not say that anyone died"] and rec["readers"]["a"]["verdicts"]["short"][0] is True
    assert "allowance" in rec["readers"]["b"]["could_not"] and rec["readers"]["c"]["could_not"].startswith("its reply held no verdict") and len([c for c in calls if c[0] == "c"]) == 2
    assert rec["summary"] == {"readers_that_answered": ["a"], "lines": 6, "not_supported": {"how2": {"a": "the text does not say that anyone died"}}}
    p = calls[0][1]; assert "1. Not shown either way." in p and "4. All of them died." in p and "pooled analysis of six studies" in p and "0.5.3" not in p and "editor" not in p.lower()      # the reader is given the text and the lines, nothing else
    assert check("cl_none", item, ["a"], chat=chat, save=False) is None
    claim_of = keep
    print("blind_lines selftest: ok (every plain line and every sentence of the plain summary is read against the claim's text; a reader is given nothing but the text and the lines; "
          "a reader that cannot be asked or gives no verdict twice is said so and decides nothing; what each reader said of each line is kept in its own words)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest()
    elif "--requests" in a: requests(a[a.index("--requests") + 1])
    else: sys.exit(__doc__)
