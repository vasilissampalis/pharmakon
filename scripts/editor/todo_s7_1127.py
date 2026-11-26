"""todo_s7_1127.py PAGE.html: the section 7 answers on the senior author's to-do page, from their checked lines (27 November 2026).

Writes into the page's DATA.s7 (in place): the answers waiting for his approval, each at its current version with its plain lines
(data/site/simple.json, written shorter as he asked on 12 and 13 November and checked blind twice), the myth-or-fact cards that go
with it, and a note: what the reset of 13 November did to it, and where a checker thought a reader might take a finding as advice.
The answers he approved stay as they are, at the end. cl_alc_nac_hangover is left off, as he said on 12 November. Also replaces the
section's note. Run from the repository root."""
import glob, json, re, sys

page = sys.argv[1]
t = open(page, encoding="utf-8").read()
m = re.search(r"const DATA\s*=\s*(\{.*?\});\s*\n", t, re.S)
D = json.loads(m.group(1))
C = {}
for f in glob.glob("data/claims/*.json"):
    for c in json.load(open(f, encoding="utf-8")): C[c["id"]] = c
S = json.load(open("data/site/simple.json", encoding="utf-8"))
G = json.load(open("data/verification/senior-gate.json", encoding="utf-8"))
lost = {it["id"]: it["v"] for it in json.load(open("data/verification/s7-review-2026-11-13/s7_on_todo_page.json", encoding="utf-8"))["items"]}
key = lambda x: tuple(int(q) for q in x.split("."))
OFF = {"cl_alc_nac_hangover"}   # his comment of 12 November: "this unecessary"
NOTE = json.load(open("data/verification/s7-simple-2026-11-27/notes_for_him.json", encoding="utf-8"))
# his comments of 12 and 13 November on these answers (the page's database, given to writers 801 to 804 in their task files): the new lines answer them.
# Their claim versions did not change, so the page would show his old "Change asked" on lines written since: each item carries the day its lines were
# written ("lv"), and a decision saved for other lines does not count for these (the page's sState).
COMMENTED = {}
for f in glob.glob("data/verification/s7-simple-2026-11-27/tasks_writer80*.json"):
    for x in json.load(open(f, encoding="utf-8"))["claims"]:
        if x.get("senior_author_comment"): COMMENTED[x["id"]] = x["senior_author_comment"]
LV = "2026-11-27"
REG = {"cl_can_smoked_vs_vaped": "Your 13 November version (two trials and two machine tests) was lost in the reset; this one has one trial. The fuller one will be rebuilt from papers in your folder and come back to you.",
       "cl_can_edibles_labels": "Your 13 November version (with a Colorado test of 2023 to 2024) was lost in the reset; this one has the 2014 test only. The fuller one will be rebuilt from papers in your folder and come back to you.",
       "cl_alc_water_dehydration": "You approved its 13 November version, which the reset lost; this is the current checked version, with new lines."}
page_item = {x["id"]: x for x in D["s7"]}
s7ids = [cid for cid, c in C.items() if c.get("section") == 7]
approved = [cid for cid in s7ids if isinstance(G.get(cid), dict) and G[cid].get("version") == C[cid]["version"] and str(G[cid].get("decision", "")).startswith("approved")]
waiting = [cid for cid in s7ids if cid not in approved and cid not in OFF]
order = [x["id"] for x in D["s7"]]
pos = lambda cid: order.index(cid) if cid in order else len(order)
tf = {}
for slug, its in S.get("tf", {}).items():
    for it in its: tf.setdefault(it["claim"], []).append(it)
items = []
LATER = {"cl_can_smoked_vs_vaped", "cl_can_edibles_labels"}   # they come back with the studies they lost: shown after the answers that are final
for cid in sorted(waiting, key=lambda c: (c in LATER, pos(c))):
    c = C[cid]; e = S["claims"][cid]; assert e.get("v") == c["version"], (cid, e.get("v"), c["version"])
    note = []
    if cid in REG: note.append(REG[cid])
    elif cid in lost and key(lost[cid]) > key(c["version"]): note.append("Your 13 November version of this answer was lost in the reset; this one rests on the same sources.")
    if cid in COMMENTED:
        d = COMMENTED[cid].get("date") or ""
        note.insert(0, "Your comment of " + ("12" if d.endswith("-12") else "13" if d.endswith("-13") else "") + " November is answered in these lines.")
    if NOTE.get(cid): note.append(NOTE[cid])
    cards = [{"statement": x["statement"], "answer": x["answer"], "why": x.get("why", "")} for x in tf.get(cid, []) if x.get("v") == c["version"]]
    items.append({"id": cid, "v": c["version"], "page": page_item.get(cid, {}).get("page", "Alcohol"), "q": e["q"], "short": e["short"], "but": e.get("but", ""), "how": e.get("how", []),
                  "certainty": c["grade"]["certainty"], "new": cid not in page_item, "rewritten": False, "note": " ".join(note), "tf": cards, "lv": LV})
for cid in sorted(approved, key=pos):
    x = dict(page_item[cid]); assert x["v"] == C[cid]["version"]; x.update({"note": "", "tf": [], "rewritten": False, "new": False}); items.append(x)
D["s7"] = items
t = t[:m.start(1)] + json.dumps(D, ensure_ascii=False) + t[m.end(1):]
old_s = 'const sState = x => { const v = SS[x.id] || local["s:" + x.id]; return v && v.v === x.v ? v : null; };'
new_s = 'const sState = x => { const v = SS[x.id] || local["s:" + x.id]; return v && v.v === x.v && (v.lv || "") === (x.lv || "") ? v : null; };'
if old_s in t: t = t.replace(old_s, new_s)
assert new_s in t, "sState not found"
old_v = 'const v = { decision: decision, note: note || "", v: x.v, at: new Date().toISOString() };'
new_v = 'const v = { decision: decision, note: note || "", v: x.v, lv: x.lv || "", at: new Date().toISOString() };'
if old_v in t: t = t.replace(old_v, new_v)
assert new_v in t, "saveS7 not found"
a = re.search(r'<p class="note"><b>(?:Paused: please don&rsquo;t approve these for now\.|Ready for you again: \d+ answers\.)</b>.*?</p>', t, re.S)
assert a, "the section's note was not found"
n = len(waiting)
note = (f'<p class="note"><b>Ready for you again: {n} answers.</b> Each is written for its current version and shorter, as you asked on 12 and 13 November '
        '(the answer first, the drug named, only what matters), and checked blind twice by readers who wrote none of it; the myth-or-fact cards that '
        'come with it are under it. The reset of 13 November took 16 of them back to the versions before your comments; where your comment was about '
        'what an answer says, the new lines answer it. Two of them (smoked against vaped cannabis, edible labels) and the answer on hangover cures will '
        'come back to you with the studies they lost, rebuilt from papers already in your folder. The answer on NAC for hangovers is off the list, as you '
        'said. None of these lines tells anyone what to do; where a checker thought a reader might still take a finding as advice, it says so under the '
        'answer. The 8 answers you approved before are at the end, unchanged.</p>')
t = t[:a.start()] + note + t[a.end():]
open(page, "w", encoding="utf-8").write(t)
print(n, "waiting,", len(approved), "approved;", sum(1 for x in items if x.get("note")), "with a note;", sum(len(x["tf"]) for x in items), "cards")
