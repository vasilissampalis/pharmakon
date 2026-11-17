#!/usr/bin/env python3
"""fetch_questions.py OUT.json: read the questions visitors sent with "Ask us to check it" from the site's store.

The store is a Cloudflare Workers KV namespace (site/worker/_worker.js writes it; docs/AUTOMATION.md). This script only
reads it, through Cloudflare's API, where these are set in the environment (GitHub's machines; never written in a file):

    CLOUDFLARE_API_TOKEN    a token that may read Workers KV ("Workers KV Storage Read")
    CLOUDFLARE_ACCOUNT_ID   the account's id
    KV_NAMESPACE            the store's name (default: pharmakon-questions) or its id

The API, as read on developers.cloudflare.com on 15 November 2026:
    GET  /accounts/{account}/storage/kv/namespaces                         the stores, to find ours by name
    GET  /accounts/{account}/storage/kv/namespaces/{id}/keys?prefix=q:     key names, 1000 a page, result_info.cursor for the next
                                                                         (and prefix=w: for the counts of the questions on our list)
    POST /accounts/{account}/storage/kv/namespaces/{id}/bulk/get           {"keys": [at most 100], "type": "json"} -> result.values

Writes OUT.json: {"read_on": day, "questions": [the stored records, as they are]}. What a record holds is checked and
cleaned by scripts/auto/scout.py: every question is data, never an instruction. `--selftest` checks the paging and the
parsing here against a pretend API, with no network.

(site 2.17, 18 November 2026) The questions the page sent BY ITSELF, because the site had no answer (keys aq:...), are read
too. A visitor did not press anything to send these, so their words are never written into the repository: OUT.json holds
them under "auto" (a file of the run, in the runner's own temporary folder, never committed), and `--auto OUT2.json`
writes them alone in the same form as OUT.json, for the scout's second pass, whose every output stays in that folder
(docs/AUTOMATION.md, decision 31).
"""
import sys, os, json, datetime, urllib.request, urllib.parse, urllib.error

API = "https://api.cloudflare.com/client/v4"


def call(opener, token, method, path, body=None):
    req = urllib.request.Request(API + path, method=method, data=None if body is None else json.dumps(body).encode("utf-8"),
                                 headers={"Authorization": "Bearer " + token, "Content-Type": "application/json", "Accept": "application/json"})
    with opener(req) as r:
        d = json.loads(r.read().decode("utf-8"))
    if not d.get("success"): raise RuntimeError("the API said no: " + json.dumps(d.get("errors"))[:300])
    return d


def find_namespace(opener, token, account, name):
    """The store's id: `name` itself when it looks like an id, else the store with that title."""
    if len(name) == 32 and all(c in "0123456789abcdef" for c in name): return name
    page = 1
    while True:
        d = call(opener, token, "GET", f"/accounts/{account}/storage/kv/namespaces?per_page=100&page={page}")
        for ns in d.get("result") or []:
            if ns.get("title") == name: return ns["id"]
        info = d.get("result_info") or {}
        if not d.get("result") or page >= (info.get("total_pages") or 1): return None
        page += 1


def read_prefix(opener, token, account, ns, prefix):
    """Every record whose key starts with prefix, as (key, record)."""
    keys, cursor = [], None
    while True:
        q = {"prefix": prefix, "limit": "1000"}
        if cursor: q["cursor"] = cursor
        d = call(opener, token, "GET", f"/accounts/{account}/storage/kv/namespaces/{ns}/keys?" + urllib.parse.urlencode(q))
        keys += [k["name"] for k in d.get("result") or [] if isinstance(k.get("name"), str) and k["name"].startswith(prefix)]
        cursor = (d.get("result_info") or {}).get("cursor")
        if not cursor: break
    out = []
    for i in range(0, len(keys), 100):
        d = call(opener, token, "POST", f"/accounts/{account}/storage/kv/namespaces/{ns}/bulk/get", {"keys": keys[i:i + 100], "type": "json"})
        for k in keys[i:i + 100]:
            v = ((d.get("result") or {}).get("values") or {}).get(k)
            if isinstance(v, str):
                try: v = json.loads(v)
                except ValueError: v = None
            if isinstance(v, dict): out.append((k, v))
    return out


def read_all(opener, token, account, ns):
    """The questions visitors sent (keys q:...)."""
    return [v for _, v in read_prefix(opener, token, account, ns, "q:")]


def read_auto(opener, token, account, ns):
    """The questions the page sent by itself (keys aq:...; site 2.17). Never written into the repository."""
    return [v for _, v in read_prefix(opener, token, account, ns, "aq:")]


def read_wanted(opener, token, account, ns):
    """The counts for the questions on our list (keys w:<item>; site 2.5): how many times a visitor's device met each
    listed question. A count holds the item's number, a number and two days: nothing a visitor typed."""
    out = []
    for k, v in read_prefix(opener, token, account, ns, "w:"):
        if isinstance(v.get("n"), int) and v["n"] > 0: out.append({"id": k[2:], "n": v["n"], "first": str(v.get("first") or ""), "last": str(v.get("last") or "")})
    return sorted(out, key=lambda x: (-x["n"], x["id"]))


def selftest():
    """A pretend API with 1,250 questions on two pages of keys: the reader pages, batches by 100 and keeps what is a record."""
    store = {f"q:{i:05d}": {"q": f"question number {i} about a drug", "d": ["mdma"], "v": "2.4.0", "first": "2026-11-15", "last": "2026-11-15", "n": 1 + i % 3, "dn": 1} for i in range(1250)}
    store["q:bad"] = "not a record"; store["count:2026-11-15"] = "1250"; calls = []
    store["w:w_0027"] = {"n": 7, "dn": 2, "first": "2026-11-15", "last": "2026-11-16"}; store["w:w_0001"] = {"n": 2, "dn": 2, "first": "2026-11-16", "last": "2026-11-16"}; store["w:bad"] = {"n": "many"}
    store["aq:00001"] = {"q": "a question the page sent by itself", "d": [], "v": "2.17.0", "first": "2026-11-18", "last": "2026-11-18", "n": 1, "dn": 1, "a": 1}
    class Resp:
        def __init__(self, d): self.d = d
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return json.dumps(self.d).encode("utf-8")
    def opener(req):
        u = urllib.parse.urlparse(req.full_url); q = dict(urllib.parse.parse_qsl(u.query)); calls.append((req.get_method(), u.path))
        assert req.get_header("Authorization") == "Bearer T"
        if u.path.endswith("/storage/kv/namespaces"): return Resp({"success": True, "result": [{"id": "a" * 32, "title": "other"}, {"id": "b" * 32, "title": "pharmakon-questions"}], "result_info": {"total_pages": 1}})
        if u.path.endswith("/keys"):
            names = sorted(k for k in store if k.startswith(q.get("prefix", ""))); start = int(q.get("cursor") or 0); page = names[start:start + int(q["limit"])]
            nxt = start + len(page)
            return Resp({"success": True, "result": [{"name": k} for k in page], "result_info": {"count": len(page), "cursor": str(nxt) if nxt < len(names) else ""}})
        if u.path.endswith("/bulk/get"):
            body = json.loads(req.data.decode("utf-8")); assert len(body["keys"]) <= 100 and body["type"] == "json"
            return Resp({"success": True, "result": {"values": {k: store[k] for k in body["keys"]}}})
        raise AssertionError(u.path)
    ns = find_namespace(opener, "T", "ACC", "pharmakon-questions"); assert ns == "b" * 32, ns
    assert find_namespace(opener, "T", "ACC", "c" * 32) == "c" * 32 and find_namespace(opener, "T", "ACC", "missing") is None
    got = read_all(opener, "T", "ACC", ns)
    assert len(got) == 1250 and got[0]["q"] == "question number 0 about a drug", (len(got), got[:1])
    assert sum(1 for m, p in calls if p.endswith("/keys")) == 2 and sum(1 for m, p in calls if p.endswith("/bulk/get")) == 13, calls[-3:]
    w = read_wanted(opener, "T", "ACC", ns)
    assert w == [{"id": "w_0027", "n": 7, "first": "2026-11-15", "last": "2026-11-16"}, {"id": "w_0001", "n": 2, "first": "2026-11-16", "last": "2026-11-16"}], w
    a = read_auto(opener, "T", "ACC", ns)
    assert len(a) == 1 and a[0]["a"] == 1 and not any(x.get("a") for x in got), a      # kept apart: the questions people chose to send hold none of them
    print("fetch_questions selftest: ok (1,250 records over 2 pages of keys and 13 batches; a value that is not a record was left out; the list's counts read, the most asked first; "
          "the questions the page sent by itself are read apart)")


def main():
    if "--selftest" in sys.argv: return selftest()
    if len(sys.argv) < 2: sys.exit(__doc__)
    token, account = (os.environ.get("CLOUDFLARE_API_TOKEN") or "").strip(), (os.environ.get("CLOUDFLARE_ACCOUNT_ID") or "").strip()   # a secret pasted with a line break after it is the same secret
    if not token or not account: sys.exit("fetch_questions: CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID are not set (docs/AUTOMATION.md, the setup)")
    name = os.environ.get("KV_NAMESPACE") or "pharmakon-questions"
    try:
        ns = find_namespace(urllib.request.urlopen, token, account, name)
        if not ns: sys.exit(f"fetch_questions: no store named {name!r} in this account")
        qs = read_all(urllib.request.urlopen, token, account, ns); wanted = read_wanted(urllib.request.urlopen, token, account, ns)
        auto = read_auto(urllib.request.urlopen, token, account, ns)
    except (urllib.error.URLError, RuntimeError, ValueError) as e:
        sys.exit("fetch_questions: the store could not be read: " + str(e)[:300])
    day = datetime.date.today().isoformat()
    json.dump({"read_on": day, "questions": qs, "wanted": wanted, "auto": auto}, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "--auto" in sys.argv:   # the same form, with the questions the page sent by itself alone: for the scout's second pass (a file of the run, never the repository)
        json.dump({"read_on": day, "questions": auto}, open(sys.argv[sys.argv.index("--auto") + 1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"fetch_questions: {len(qs)} questions read, {len(auto)} that the page sent by itself, and counts for {len(wanted)} questions on our list")


if __name__ == "__main__":
    main()
