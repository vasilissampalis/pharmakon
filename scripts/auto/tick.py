#!/usr/bin/env python3
"""tick.py: every half hour, what is there to do? (docs/AUTOMATION.md; .github/workflows/auto.yml)

The senior author, 15 November 2026: "automatically deployed every 30 minutes"; "everything we can find automated and
free ... every 30 minutes when github will be regenerated".

    python3 -I scripts/auto/tick.py plan       on the smallest machine: decides, writes $GITHUB_OUTPUT (scout, lane, deploy)
    python3 -I scripts/auto/tick.py after      after the work: has what the site is built from changed? ($GITHUB_OUTPUT deploy)
    python3 -I scripts/auto/tick.py inputs     prints the fingerprint of everything the site is built from
    python3 -I scripts/auto/tick.py did lane|deploy    counts one run of that kind today
    python3 -I scripts/auto/tick.py --selftest

It looks every half hour and works only when there is work, because this repository is private and GitHub gives a private
repository 12 US dollars of machine time a month (about 2,000 minutes of the standard machine; read on 15 November 2026):
a look on the one-core machine costs a fifth of a cent; a run that writes answers costs 2 to 3 cents and a publishing a
little over one cent (two minutes, measured on 15 November 2026). So a day holds at most LANE_A_DAY runs that write and
DEPLOY_A_DAY that publish (requests by the editor count too): 48 looks, six writing runs and eight publishings come to
about 35 cents a day, inside the 40 that a month of 12 dollars gives. On a public repository there would be no such limit.

  scout   the question store has changed since the scout last read it (scripts/auto/look.py)
  lane    a listed question's turn has come (never tried; written by an older lane; the second look: not complete and
          the finders have found something since; no answer for a week), today's free model allowance has room for at
          least one answer, and fewer than LANE_A_DAY such runs were made today
  deploy  what the site is built from is not what was last published (data/auto/deploy/deployed.json), and fewer than
          DEPLOY_A_DAY publishings were made today
"""
import sys, os, json, hashlib, pathlib, datetime, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
TICK = ROOT / "data" / "auto" / "tick.json"
DEPLOYED = ROOT / "data" / "auto" / "deploy" / "deployed.json"
LANE_A_DAY, DEPLOY_A_DAY = 6, 8
ROOM = 1200             # neurons one answer may take: the lane starts only when today's allowance has this much left
RETRY_DAYS = 7
# everything the site is built from (site/build.js and site/build_public.py read these); the machine lane's answers are counted apart
BUILT_FROM = ["site/src", "site/build.js", "site/build_public.py", "site/public-assets", "site/worker", "site/insight/model.json", "site/insight/scope.json", "site/insight/vendor", "site/photos",
              "data/auto/lane/policy.json", "data/auto/lane/lines.json",
              "data/site", "data/claims", "data/references", "data/study-cards", "data/epidemiology", "data/legal", "data/identity", "data/monographs",
              "data/verification/senior-gate.json", "data/evidence-maps.json", "data/doi-index.json", "scripts/insight/build_index.py"]


def today(): return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def load(p, d):
    try: return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError): return d


def inputs():
    """One fingerprint of everything the site is built from: git's own fingerprints of those folders and files, and the
    machine lane's answers that the site shows (the published ones, and the list of answers taken down)."""
    h = hashlib.sha256()
    for p in BUILT_FROM:
        r = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--verify", "-q", "HEAD:" + p], capture_output=True, text=True)
        h.update((p + "=" + (r.stdout.strip() or "none") + "\n").encode())
    shown = []
    for f in sorted((ROOT / "data" / "auto" / "answers").glob("au_*.json")):
        a = load(f, {})
        if a.get("status") == "published": shown.append([a.get("id"), a.get("lane"), a.get("kind"), [[p.get("text"), p.get("quote"), p.get("who"), p.get("what")] for p in a.get("parts") or []], [(s.get("ref") or {}).get("id") for s in a.get("sources") or []], a.get("complete"), (a.get("made") or {}).get("from")])
    h.update(json.dumps(shown, sort_keys=True, ensure_ascii=False).encode()); h.update(json.dumps(load(ROOT / "data" / "auto" / "held.json", {}), sort_keys=True).encode())
    return h.hexdigest()[:24]


def counts():
    t = load(TICK, {})
    if t.get("day") != today(): t = {"day": today(), "lane": 0, "deploy": 0, "looks": 0}
    return t


def lane_has_work(state, items, ledger_left, t):
    """(yes or no, why)"""
    if t["lane"] >= LANE_A_DAY: return False, f"{t['lane']} writing runs today already"
    if ledger_left < ROOM: return False, f"today's free model allowance has {ledger_left:.0f} neurons left: not enough for one answer"
    if load(ROOT / "data" / "auto" / "lane" / "policy.json", {}).get("pause"): return False, "the editor has paused the lane (data/auto/lane/policy.json, pause)"
    import lane as L
    todo = [w["id"] for w in items if L.turn_of(w, state.get("items") or {}) is not None]
    return (True, f"{len(todo)} listed questions are to be worked on") if todo else (False, "every listed question has been worked on")


def deploy_needed(t, fingerprint, deployed):
    if deployed.get("inputs") == fingerprint: return False, "what is published is what the site is built from now"
    if t["deploy"] >= DEPLOY_A_DAY: return False, f"{t['deploy']} publishings today already; the change waits for tomorrow"
    return True, "what the site is built from has changed since it was last published"


def out(**kv):
    line = "".join(f"{k}={'true' if v is True else 'false' if v is False else v}\n" for k, v in kv.items())
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f: f.write(line)
    print(line, end="")


def plan():
    import llm, look, fetch_questions as fq, urllib.request
    t = counts(); t["looks"] = t.get("looks", 0) + 1; why = {}
    # the question store
    token, account = (os.environ.get("CLOUDFLARE_API_TOKEN") or "").strip(), (os.environ.get("CLOUDFLARE_ACCOUNT_ID") or "").strip()
    scout = False; st = load(look.STATE, {})
    if token and account:
        try:
            ns = fq.find_namespace(urllib.request.urlopen, token, account, os.environ.get("KV_NAMESPACE") or "pharmakon-questions")
            recs = fq.read_all(urllib.request.urlopen, token, account, ns) + [{"q": "w:" + w["id"], "n": w["n"]} for w in fq.read_wanted(urllib.request.urlopen, token, account, ns)] if ns else []
            sig = look.signature(recs); scout = bool(ns) and sig != st.get("done"); why["scout"] = "the store has changed" if scout else "the store is as the scout last read it"
        except Exception as e: why["scout"] = "the store could not be read (" + type(e).__name__ + ")"
    else: why["scout"] = "no key"
    import papers
    items = papers.listed()
    lane, why["lane"] = lane_has_work(load(ROOT / "data" / "auto" / "lane" / "state.json", {"items": {}}), items, llm.left(), t) if token and account else (False, "no key")
    dep, why["deploy"] = deploy_needed(t, inputs(), load(DEPLOYED, {}))
    t["last"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"); t["why"] = why
    TICK.parent.mkdir(parents=True, exist_ok=True); json.dump(t, open(TICK, "w", encoding="utf-8"), indent=1)
    # the look is kept in the repository when something is to be done, and once a day as a sign of life
    out(scout=scout, lane=lane, work=scout or lane, deploy=dep and not (scout or lane), keep=(scout or lane or dep or t["looks"] == 1))
    print("tick:", "; ".join(f"{k}: {v}" for k, v in why.items()))


def after():
    t = counts(); dep, why = deploy_needed(t, inputs(), load(DEPLOYED, {}))
    out(deploy=dep); print("tick, after the work:", why)


def did(kind):
    t = counts(); t[kind] = t.get(kind, 0) + 1; TICK.parent.mkdir(parents=True, exist_ok=True); json.dump(t, open(TICK, "w", encoding="utf-8"), indent=1)
    if kind == "deploy":
        d = load(DEPLOYED, {}); d["inputs"] = inputs(); DEPLOYED.parent.mkdir(parents=True, exist_ok=True); json.dump(d, open(DEPLOYED, "w", encoding="utf-8"), indent=1)


def selftest():
    t = {"day": today(), "lane": 0, "deploy": 0}
    items = [{"id": "w_1"}, {"id": "w_2"}, {"id": "w_3"}]
    old = (datetime.date.today() - datetime.timedelta(days=8)).isoformat(); new = datetime.date.today().isoformat()
    import lane as L
    st = {"items": {"w_1": {"status": "published", "last": old, "lane": L.LANE}, "w_2": {"status": "none", "last": new, "lane": L.LANE}}}
    assert lane_has_work(st, items, 5000, t) == (True, "1 listed questions are to be worked on")                    # w_3 was never tried
    st["items"]["w_3"] = {"status": "waiting", "last": new, "lane": L.LANE}; assert lane_has_work(st, items, 5000, t)[0] is False      # tried, waiting or too recent
    st["items"]["w_2"]["last"] = old; assert lane_has_work(st, items, 5000, t)[0] is True                              # no answer a week ago: tried again
    assert lane_has_work(st, items, 800, t)[0] is False and lane_has_work(st, items, 5000, dict(t, lane=LANE_A_DAY))[0] is False  # no room in the allowance; the day's runs are used
    st["items"]["w_2"] = {"status": "published", "last": new, "lane": L.LANE - 1}; assert lane_has_work(st, items, 5000, t)[0] is True         # written by an older lane: written again
    assert deploy_needed(t, "abc", {"inputs": "abc"})[0] is False and deploy_needed(t, "abd", {"inputs": "abc"})[0] is True and deploy_needed(dict(t, deploy=DEPLOY_A_DAY), "abd", {"inputs": "abc"})[0] is False
    a = inputs(); assert len(a) == 24 and a == inputs()
    print(f"tick selftest: ok (the lane starts for a question never tried, written by an older lane or without an answer for a week, with room in the allowance and fewer than {LANE_A_DAY} runs today; the site is published when what it is built from has changed, {DEPLOY_A_DAY} times a day at most)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest()
    elif a[:1] == ["plan"]: plan()
    elif a[:1] == ["after"]: after()
    elif a[:1] == ["inputs"]: print(inputs())
    elif a[:1] == ["did"] and a[1:2] and a[1] in ("lane", "deploy"): did(a[1])
    else: sys.exit(__doc__)
