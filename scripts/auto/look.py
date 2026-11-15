#!/usr/bin/env python3
"""look.py: the scout's short first step (docs/AUTOMATION.md): is there anything new in the question store?

It runs every time the scout wakes, on the smallest machine, and must finish in well under a minute, because on a private
repository every started minute is paid from the month's free machine time. It reads the store (fetch_questions.py),
makes one short signature of what is there (each question's words and count), and compares it with the signature of the
last finished run, kept in data/auto/state.json. The heavy work (building the index, ranking, the report) starts only when
the two differ.

What it writes:
  $GITHUB_OUTPUT        new=true|false, and why= one of: new, same, setup, tried, forced, error
  data/auto/state.json  only when something is worth a commit: a new signature about to be worked on (so that a run that
                        keeps failing is tried three times and then left until the questions change), the first look of
                        a day (a sign of life, once a day), or a change of state (set up or not, readable or not)
  $GITHUB_STEP_SUMMARY  one plain line

No secret and no question is ever printed. `--selftest` checks the decisions with no network.
"""
import sys, os, json, hashlib, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
STATE = ROOT / "data" / "auto" / "state.json"
MAX_TRIES = 3


def signature(records):
    """One short string for what the store holds: every question's words and count, in a fixed order."""
    rows = sorted((str(r.get("q", "")).strip().lower(), int(r.get("n") or 1)) for r in records if isinstance(r, dict))
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False).encode("utf-8")).hexdigest()[:24]


def decide(state, sig, today, forced=False, problem=None):
    """What to do and what to remember. Returns (new, why, state to keep, commit it?)."""
    s = dict(state or {}); before = json.dumps(s, sort_keys=True)
    first_today = s.get("looked_on") != today
    if problem:   # not set up, or the store could not be read: say so once, then once a day
        changed = s.get("status") != problem
        s.update({"status": problem, "looked_on": today})
        return False, problem, s, changed or first_today
    s["status"] = "ok"; s["looked_on"] = today
    if sig == s.get("done") and not forced:
        return False, "same", s, first_today or json.loads(before).get("status") != "ok"
    if s.get("trying") == sig: tries = int(s.get("tries") or 0)
    else: tries = 0
    if tries >= MAX_TRIES and not forced:
        return False, "tried", s, first_today
    s.update({"trying": sig, "tries": 0 if forced and tries >= MAX_TRIES else tries + 1})
    return True, "forced" if forced and sig == s.get("done") else "new", s, True


def finished(state, sig, today, questions):
    """After the heavy work has ended well: this signature is done."""
    s = dict(state or {}); s.update({"status": "ok", "done": sig, "done_on": today, "questions": questions, "tries": 0}); s.pop("trying", None)
    return s


def selftest():
    t = "2026-11-16"
    new, why, s, commit = decide({}, None, t, problem="setup"); assert (new, why, commit) == (False, "setup", True) and s["status"] == "setup"
    new, why, s2, commit = decide(s, None, t, problem="setup"); assert (new, why, commit) == (False, "setup", False)          # said once a day
    new, why, s2, commit = decide(s, None, "2026-11-17", problem="setup"); assert commit is True
    new, why, s, commit = decide(s, "aaa", t); assert (new, why, commit) == (True, "new", True) and s["tries"] == 1 and s["trying"] == "aaa"
    new, why, s, commit = decide(s, "aaa", t); assert new and s["tries"] == 2                                                # the work failed: tried again
    new, why, s, commit = decide(s, "aaa", t); assert new and s["tries"] == 3
    new, why, s4, commit = decide(s, "aaa", t); assert (new, why, commit) == (False, "tried", False)                         # three times, then left alone
    new, why, s5, commit = decide(s, "aaa", t, forced=True); assert new and s5["tries"] == 0                                 # until someone asks by hand
    new, why, s6, commit = decide(s, "bbb", t); assert new and s6["tries"] == 1                                              # or the questions change
    d = finished(s, "aaa", t, 12); assert d["done"] == "aaa" and "trying" not in d and d["questions"] == 12
    new, why, s7, commit = decide(d, "aaa", t); assert (new, why, commit) == (False, "same", False)                          # nothing new: nothing written
    new, why, s8, commit = decide(d, "aaa", "2026-11-17"); assert (new, why, commit) == (False, "same", True)                # one sign of life a day
    new, why, s9, commit = decide(d, "aaa", t, forced=True); assert (new, why) == (True, "forced")
    a = [{"q": "Can you overdose on LSD?", "n": 2}, {"q": "is it addictive", "n": 1}]
    assert signature(a) == signature(list(reversed(a))) and signature(a) != signature([dict(a[0], n=3), a[1]]) and signature([]) == signature([])
    print("look selftest: ok")


def main():
    if "--selftest" in sys.argv: return selftest()
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import fetch_questions as fq, urllib.request
    today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    state = json.load(open(STATE, encoding="utf-8")) if STATE.exists() else {}
    forced = "--force" in sys.argv
    token, account = (os.environ.get("CLOUDFLARE_API_TOKEN") or "").strip(), (os.environ.get("CLOUDFLARE_ACCOUNT_ID") or "").strip()   # a secret pasted with a line break after it is the same secret
    sig, n, problem = None, 0, None
    if "--done" in sys.argv:   # the heavy work ended well: remember the signature it worked on
        recs = json.load(open(sys.argv[sys.argv.index("--done") + 1], encoding="utf-8"))["questions"]
        state = finished(state, signature(recs), today, len(recs))
        STATE.parent.mkdir(parents=True, exist_ok=True); json.dump(state, open(STATE, "w", encoding="utf-8"), indent=1); print("look: done, " + str(len(recs)) + " questions"); return
    if not token or not account: problem = "setup"
    else:
        try:
            ns = fq.find_namespace(urllib.request.urlopen, token, account, os.environ.get("KV_NAMESPACE") or "pharmakon-questions")
            if not ns: problem = "no-store"
            else: recs = fq.read_all(urllib.request.urlopen, token, account, ns); sig, n = signature(recs), len(recs)
        except Exception as e:   # the reason is kept short and holds no secret (the API's own error codes at most)
            problem = "error"; print("look: the store could not be read (" + type(e).__name__ + ")")
    new, why, state, commit = decide(state, sig, today, forced, problem)
    if sig is not None: state["seen"] = n
    if commit:
        STATE.parent.mkdir(parents=True, exist_ok=True); json.dump(state, open(STATE, "w", encoding="utf-8"), indent=1)
    line = {"setup": "The scout is not set up yet: the two secrets are missing (docs/AUTOMATION.md, the setup).", "no-store": "No store named pharmakon-questions in this account.",
            "error": "The question store could not be read.", "same": f"Nothing new: {n} questions, as at the last run.", "tried": "The same questions failed three times; waiting for a change or a run by hand.",
            "new": f"Something new: {n} questions. The work starts.", "forced": f"Run by hand: {n} questions. The work starts."}[why]
    print("look: " + line)
    for var, text in (("GITHUB_OUTPUT", f"new={'true' if new else 'false'}\nwhy={why}\ncommit={'true' if commit else 'false'}\n"), ("GITHUB_STEP_SUMMARY", line + "\n")):
        if os.environ.get(var):
            with open(os.environ[var], "a", encoding="utf-8") as f: f.write(text)


if __name__ == "__main__":
    main()
