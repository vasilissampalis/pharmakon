#!/usr/bin/env python3
"""tick.py: every five minutes (until 18 November 2026: every half hour), what is there to do? (docs/AUTOMATION.md; .github/workflows/auto.yml)

The senior author, 15 November 2026: "automatically deployed every 30 minutes"; "everything we can find automated and
free ... every 30 minutes when github will be regenerated".

    python3 -I scripts/auto/tick.py plan       on the smallest machine: decides, writes $GITHUB_OUTPUT (scout, lane, deploy)
    python3 -I scripts/auto/tick.py after [--asked FILE]     after the work: has what the site is built from changed? ($GITHUB_OUTPUT deploy)
    python3 -I scripts/auto/tick.py publish    asks GitHub to start the publishing run now (in the middle of a run, as soon as a sent question has its answer)
    python3 -I scripts/auto/tick.py inputs     prints the fingerprint of everything the site is built from
    python3 -I scripts/auto/tick.py did lane|deploy    counts one run of that kind today
    python3 -I scripts/auto/tick.py --selftest

It looks every half hour and works only when there is work, because this repository is private and GitHub gives a private
repository 12 US dollars of machine time a month (about 2,000 minutes of the standard machine; read on 15 November 2026):
a look on the one-core machine costs a fifth of a cent; a run that writes answers costs 2 to 3 cents and a publishing a
little over one cent (two minutes, measured on 15 November 2026). So a day holds at most LANE_A_DAY runs that write and
DEPLOY_A_DAY that publish (requests by the editor count too): 48 looks, six writing runs and eight publishings come to
about 35 cents a day, inside the 40 that a month of 12 dollars gives. On a public repository there would be no such limit.
(16 November 2026, 22:13 Athens time: the senior author made the repository public. Machine time is free now; the ceilings
below were lifted the same hour, and what limits a day is the models' free allowances.)

  scout   the question store has changed since the scout last read it (scripts/auto/look.py)
  lane    a listed question's turn has come (never tried; written by an older lane; the second look: not complete and
          the finders have found something since; no answer since the day before), today's free model allowance has room for at
          least one answer, and fewer than LANE_A_DAY such runs were made today
  deploy  what the site is built from is not what was last published (data/auto/deploy/deployed.json), and fewer than
          DEPLOY_A_DAY publishings were made today
"""
import sys, os, json, hashlib, pathlib, datetime, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
TICK = ROOT / "data" / "auto" / "tick.json"
DEPLOYED = ROOT / "data" / "auto" / "deploy" / "deployed.json"
LANE_A_DAY, DEPLOY_A_DAY = 240, 96    # (18 November 2026, lane 19: the look comes every five minutes and a writing run is short, so that a sent question is begun within minutes; what limits a day is the models' free allowances (lane.team) and, for publishing, one every quarter of an hour on average. Until that day: 24 and 24.)   # (16 November 2026, 22:13: the senior author made the repository public, so GitHub's machine time is free and no longer limits a day. What limits it now is the models' free allowances: a writing run starts only when a team has room (lane.team), so this number is a ceiling, not a plan. Before that day: 4 and 8, for the paid machine time of a private repository.)
ROOM = 1200             # neurons one answer may take: the lane starts only when today's allowance has this much left
RETRY_DAYS = 1     # (17 November 2026: a question without an answer is tried again the next day, not the next week: "this should be done as fast and good as possible")
# everything the site is built from (site/build.js and site/build_public.py read these); the machine lane's answers are counted apart
BUILT_FROM = ["site/src", "site/build.js", "site/build_public.py", "site/public-assets", "site/worker", "site/insight/model.json", "site/insight/scope.json", "site/insight/places.json", "site/insight/vendor", "data/auto/language/learned.json", "site/photos",
              "data/auto/lane/policy.json", "data/auto/lane/lines.json", "data/auto/names/learned.json",   # (2.9.3) the names the system learned by looking them up: a new one is a reason to publish
              "data/auto/pages.json", "data/auto/wanted-auto.json", "data/auto/filing.json", "data/auto/pictures.json", "site/photos-auto",   # (2.12) the pages people asked about: their questions, their names, their pictures
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


def lane_has_work(state, items, ledger_left, t, paused=None, kept=None):
    """(yes or no, why)"""
    if t["lane"] >= LANE_A_DAY: return False, f"{t['lane']} writing runs today already"
    if ledger_left < ROOM: return False, f"today's free model allowance has {ledger_left:.0f} neurons left: not enough for one answer"
    if (load(ROOT / "data" / "auto" / "lane" / "policy.json", {}).get("pause") if paused is None else paused): return False, "the editor has paused the lane (data/auto/lane/policy.json, pause)"
    import lane as L
    todo = [w["id"] for w in items if L.turn_of(w, state.get("items") or {}) is not None and not (L.kept_for_sent if kept is None else kept)(w)]      # (what is left of a day's allowance is kept for the questions people send: lane.kept_for_sent)
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
    scout = False; st = load(look.STATE, {}); tell = False
    if token and account:
        try:
            ns = fq.find_namespace(urllib.request.urlopen, token, account, os.environ.get("KV_NAMESPACE") or "pharmakon-questions")
            # (19 November 2026) the same records the scout signs when it has read them (look.py, --done: the questions people chose to send and the ones the page
            # sent by itself). Until then this line signed other records (the counts of listed questions, and not the questions the page sent), so the two
            # never agreed: every look said "the store has changed" and every look started the scout
            recs = fq.read_all(urllib.request.urlopen, token, account, ns) + fq.read_auto(urllib.request.urlopen, token, account, ns) if ns else []
            sig = look.signature(recs); scout = bool(ns) and sig != st.get("done"); why["scout"] = "the store has changed" if scout else "the store is as the scout last read it"
            # (19 November 2026, site 2.23) a sent question the system has decided on, whose key the state file for waiting readers does not hold yet
            # (data/auto/live.json): a run writes the file, and nothing else, so that the reader's page can say what became of the question
            try:
                import live as LV
                done = load(ROOT / "data" / "auto" / "asked.json", {}).get("done") or {}; known = load(LV.LIVE, {}).get("q") or {}
                cut = (datetime.datetime.now(datetime.timezone.utc).date() - datetime.timedelta(days=LV.KEEP_DAYS)).isoformat()
                lacks = [1 for r in recs if isinstance(r.get("q"), str) and str(r.get("last") or "9") >= cut and LV.decided((done.get(LV.finger(r["q"])) or {}).get("what")) and LV.key_of(r["q"]) not in known]
                tell = bool(lacks); why["live"] = f"{len(lacks)} sent question(s) are not yet in the state file for the readers who wait" if tell else "every sent question the system has read is in the state file"
            except Exception as e: why["live"] = "the state file could not be looked at (" + type(e).__name__ + ")"
        except Exception as e: why["scout"] = "the store could not be read (" + type(e).__name__ + ")"
    else: why["scout"] = "no key"
    import papers
    items = papers.listed()
    try:
        import lane as L; room = ROOM if L.team() else 0            # (16 November 2026) with a second free service the lane has room when any team of models has; (18 November 2026) and only then: a run that finds no team writes nothing
    except Exception: room = llm.left()
    lane, why["lane"] = lane_has_work(load(ROOT / "data" / "auto" / "lane" / "state.json", {"items": {}}), items, room, t) if token and account else (False, "no key")
    dep, why["deploy"] = deploy_needed(t, inputs(), load(DEPLOYED, {}))
    t["last"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"); t["why"] = why
    TICK.parent.mkdir(parents=True, exist_ok=True); json.dump(t, open(TICK, "w", encoding="utf-8"), indent=1)
    # the look is kept in the repository when something is to be done, and once a day as a sign of life
    out(scout=scout, lane=lane, work=scout or lane or tell, deploy=dep and not (scout or lane), keep=(scout or lane or tell or dep or t["looks"] == 1))
    print("tick:", "; ".join(f"{k}: {v}" for k, v in why.items()))


def after(asked=None):
    """asked: a file that holds the fingerprint a publishing was already asked for in the middle of this run (auto.yml, keep_now): nothing more has changed
    since, so the end of the run does not ask a second time."""
    t = counts(); now = inputs(); dep, why = deploy_needed(t, now, load(DEPLOYED, {}))
    try: already = bool(asked) and open(asked, encoding="utf-8").read().strip() == now
    except OSError: already = False
    if dep and already: dep, why = False, "a publishing of exactly this was asked for a few minutes ago, in the middle of this run"
    out(deploy=dep); print("tick, after the work:", why)


def publish():
    """Ask GitHub to start the publishing run (deploy.yml) now. The token is the run's own (GH_TOKEN); a push made by a run starts no workflow, a request does."""
    import urllib.request
    repo, token = (os.environ.get("GITHUB_REPOSITORY") or "").strip(), (os.environ.get("GH_TOKEN") or "").strip()
    if not repo or not token: print("tick: no repository or no token here: a publishing cannot be asked for"); return
    req = urllib.request.Request("https://api.github.com/repos/" + repo + "/actions/workflows/deploy.yml/dispatches", data=json.dumps({"ref": "main"}).encode(), method="POST",
                                 headers={"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "pharmakon-auto"})
    try: print("tick: the publishing run was asked for:", urllib.request.urlopen(req, timeout=30).status)
    except Exception as e: print("tick: the publishing run could not be asked for (" + type(e).__name__ + "); the end of this run asks again")


def settle_pick(ours, theirs, was):
    """Whose record of an answer stays when two runs wrote the same answer at the same time: "ours" (this run's) or "theirs" (the one another run has kept on
    main meanwhile). was: the record as it stood when this run began. (18 November 2026: a run asked for by name and the run of the clock both wrote "Do
    mothers worry about their children taking drugs?". The clock's answer passed every gate and was published at 15:56; twenty minutes later the other run
    kept its own failed draft over it, by the rule "what a run found wins", and the answer would have left the site.) The lane's rule for a second look holds
    between runs too: an answer that is published is not replaced by a draft that is not; where both runs published one, the one already on main stays."""
    if not isinstance(ours, dict) or not isinstance(theirs, dict) or theirs == was or theirs == ours: return "ours"      # nobody else wrote it meanwhile
    if theirs.get("status") == "published" and int(theirs.get("lane") or 0) >= int(ours.get("lane") or 0): return "theirs"
    return "ours"


def settle(root=None):
    """Before a run keeps its records: where another run has kept an answer on main since this run began, settle_pick says whose stays; theirs is put back as
    it stands on main, with its line in the lane's state. Returns the questions put back. Never a reason for a run to fail: any fault leaves things as they were."""
    root = pathlib.Path(root or ROOT); import re
    git = lambda *a: subprocess.run(["git", *a], cwd=root, capture_output=True, text=True)
    def show(rev, path):
        r = git("show", f"{rev}:{path}")
        try: return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None
        except ValueError: return None
    back = []
    try:
        if git("fetch", "-q", "origin", "main").returncode != 0: print("settle: main could not be fetched; nothing settled"); return back
        base = git("merge-base", "HEAD", "origin/main").stdout.strip()
        if not base: print("settle: no common point with main; nothing settled"); return back
        theirs_state = None
        for path in git("diff", "--name-only", base, "origin/main", "--", "data/auto/answers").stdout.split():
            if not re.fullmatch(r"data/auto/answers/au_w_[a-z0-9_]{1,40}\.json", path): continue
            f = root / path
            try: ours = json.load(open(f, encoding="utf-8"))
            except (OSError, ValueError): continue                               # this run holds no record of it: main's comes with the pull
            theirs = show("origin/main", path)
            if settle_pick(ours, theirs, show(base, path)) != "theirs": continue
            f.write_text(git("show", f"origin/main:{path}").stdout, encoding="utf-8")
            wid = str(theirs.get("from") or path.rsplit("au_", 1)[1][:-5])
            if theirs_state is None: theirs_state = (show("origin/main", "data/auto/lane/state.json") or {}).get("items") or {}
            sf = root / "data" / "auto" / "lane" / "state.json"
            try: st = json.load(open(sf, encoding="utf-8"))
            except (OSError, ValueError): st = None
            if st and wid in theirs_state: st.setdefault("items", {})[wid] = theirs_state[wid]; json.dump(st, open(sf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            back.append(wid)
    except Exception as e: print("settle: left as it was (" + type(e).__name__ + ")")
    print("settle:", (", ".join(back) + ": another run published an answer meanwhile; it stays, and this run's draft is not kept over it") if back else "nothing to settle")
    return back


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
    st["items"]["w_2"]["n"] = 2                                                                                           # (lane 19) w_2 has had its two tries of today
    assert lane_has_work(st, items, 5000, t, False, kept=lambda w: False) == (True, "1 listed questions are to be worked on")                    # w_3 was never tried
    st["items"]["w_3"] = {"status": "waiting", "last": new, "lane": L.LANE, "for": "editor"}; assert lane_has_work(st, items, 5000, t, False, kept=lambda w: False)[0] is False      # tried twice today, or waiting for an editor
    st["items"]["w_2"]["n"] = 1; assert lane_has_work(st, items, 5000, t, False, kept=lambda w: False)[0] is True                               # (lane 19) one try today gave no answer: once more the same day, by another team
    st["items"]["w_3"]["for"] = "again"; st["items"]["w_2"]["n"] = 2; assert lane_has_work(st, items, 5000, t, False, kept=lambda w: False)[0] is True      # (lane 19) an answer that waits for a reader that could not be asked is worked on again by itself
    st["items"]["w_3"]["for"] = "editor"; st["items"]["w_2"]["last"] = old; assert lane_has_work(st, items, 5000, t, False, kept=lambda w: False)[0] is True                              # no answer a day or more ago: tried again
    assert lane_has_work(st, items, 800, t, False, kept=lambda w: False)[0] is False and lane_has_work(st, items, 5000, dict(t, lane=LANE_A_DAY), False, kept=lambda w: False)[0] is False  # no room in the allowance; the day's runs are used
    st["items"]["w_2"] = {"status": "published", "last": new, "lane": L.LANE - 1}; assert lane_has_work(st, items, 5000, t, False, kept=lambda w: False)[0] is True         # written by an older lane: written again
    assert deploy_needed(t, "abc", {"inputs": "abc"})[0] is False and deploy_needed(t, "abd", {"inputs": "abc"})[0] is True and deploy_needed(dict(t, deploy=DEPLOY_A_DAY), "abd", {"inputs": "abc"})[0] is False
    a = inputs(); assert len(a) == 24 and a == inputs()
    # two runs, one answer: a published answer on main is not replaced by this run's draft that is not; anything else is kept as this run found it
    pub, non = {"status": "published", "lane": 19, "made": {"run": "1"}}, {"status": "none", "lane": 19, "made": {"run": "2"}}
    assert settle_pick(non, pub, None) == "theirs" and settle_pick(non, pub, {"status": "waiting", "lane": 18}) == "theirs" and settle_pick(dict(pub, made={"run": "2"}), pub, None) == "theirs"
    assert settle_pick(pub, non, None) == "ours" and settle_pick(non, dict(non, made={"run": "1"}), None) == "ours" and settle_pick(non, pub, pub) == "ours" and settle_pick(non, None, None) == "ours"
    assert settle_pick(dict(non, lane=20), pub, None) == "ours"                                                                                  # a newer lane's word stands over an older lane's answer
    import tempfile
    with tempfile.TemporaryDirectory() as td:                                      # the same in a real repository: main moves on while a run works
        up, me, other = pathlib.Path(td) / "up.git", pathlib.Path(td) / "me", pathlib.Path(td) / "other"
        g = lambda where, *a_: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.org", "-c", "init.defaultBranch=main", *a_], cwd=where, capture_output=True, text=True, check=True)
        subprocess.run(["git", "-c", "init.defaultBranch=main", "init", "-q", "--bare", str(up)], capture_output=True, check=True); g(td, "clone", "-q", str(up), str(me))
        (me / "data/auto/answers").mkdir(parents=True); (me / "data/auto/lane").mkdir(parents=True)
        wj = lambda where, rel, obj: (where / rel).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
        wj(me, "data/auto/answers/au_w_a1.json", {"from": "w_a1", "status": "none", "lane": 19, "made": {"run": "0"}}); wj(me, "data/auto/answers/au_w_a2.json", {"from": "w_a2", "status": "none", "lane": 19, "made": {"run": "0"}})
        wj(me, "data/auto/lane/state.json", {"items": {"w_a1": {"status": "none"}, "w_a2": {"status": "none"}}})
        g(me, "checkout", "-q", "-b", "main"); g(me, "add", "-A"); g(me, "commit", "-q", "-m", "start"); g(me, "push", "-q", "-u", "origin", "main"); g(td, "clone", "-q", str(up), str(other))
        wj(other, "data/auto/answers/au_w_a1.json", {"from": "w_a1", "status": "published", "lane": 19, "made": {"run": "1"}}); wj(other, "data/auto/lane/state.json", {"items": {"w_a1": {"status": "published", "why": "passed every gate"}, "w_a2": {"status": "none"}}})
        g(other, "add", "-A"); g(other, "commit", "-q", "-m", "the other run published one"); g(other, "push", "-q")
        wj(me, "data/auto/answers/au_w_a1.json", {"from": "w_a1", "status": "none", "lane": 19, "made": {"run": "2"}}); wj(me, "data/auto/answers/au_w_a2.json", {"from": "w_a2", "status": "published", "lane": 19, "made": {"run": "2"}})
        wj(me, "data/auto/lane/state.json", {"items": {"w_a1": {"status": "none", "why": "no draft passed"}, "w_a2": {"status": "published"}}})
        assert settle(me) == ["w_a1"]
        st2 = json.load(open(me / "data/auto/lane/state.json", encoding="utf-8"))["items"]
        assert json.load(open(me / "data/auto/answers/au_w_a1.json", encoding="utf-8"))["made"]["run"] == "1" and st2["w_a1"] == {"status": "published", "why": "passed every gate"} and st2["w_a2"] == {"status": "published"}
        assert json.load(open(me / "data/auto/answers/au_w_a2.json", encoding="utf-8"))["status"] == "published" and settle(me) == []     # this run's own answer is kept; settled once, nothing more to settle
    assert lane_has_work(st, items, 5000, t, "the editor's reason", kept=lambda w: False)[0] is False                                         # the editor's pause stops it
    print(f"tick selftest: ok (the lane starts for a question never tried, written by an older lane or without an answer since the day before, with room in the allowance and fewer than {LANE_A_DAY} runs today; the site is published when what it is built from has changed, {DEPLOY_A_DAY} times a day at most)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest()
    elif a[:1] == ["plan"]: plan()
    elif a[:1] == ["after"]: after(a[a.index("--asked") + 1] if "--asked" in a and a.index("--asked") + 1 < len(a) else None)
    elif a[:1] == ["publish"]: publish()
    elif a[:1] == ["settle"]: settle()
    elif a[:1] == ["inputs"]: print(inputs())
    elif a[:1] == ["did"] and a[1:2] and a[1] in ("lane", "deploy"): did(a[1])
    else: sys.exit(__doc__)
