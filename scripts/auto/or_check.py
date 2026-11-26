#!/usr/bin/env python3
"""or_check.py: which OpenRouter key the system's runs use, and what it may spend (26 November 2026; docs/OPENROUTER.md).

The senior author's dashboard shows one key (its last three characters) that was "never" used, while OpenRouter's activity
showed the system's calls. This asks OpenRouter, with the secret OPENROUTER_API_KEY that the runs use, about that key itself
(GET /api/v1/key) and its account's credit (GET /api/v1/credits, where the key may ask), and reads the public list of models
for the ids, prices and providers this system names (data/auto/lane/pay.json). None of these calls costs anything.

It writes data/auto/or-check.json and prints a short line. NEVER the key, never the key's label whole: whether the key ends
as the dashboard's (the request's "dashboard_key_ends", three characters the dashboard itself shows), the label's last three
characters, and the numbers OpenRouter gives (the limit, what is left of it, what was used, whether credit was ever bought).

    python3 -I scripts/auto/or_check.py        (data/auto/requests/orcheck-*.json: {"dashboard_key_ends": "abc"})
"""
import json, os, pathlib, re, time, urllib.error, urllib.parse, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = "https://openrouter.ai/api/v1/"


def get(path, key=None, timeout=40):
    h = {"User-Agent": "pharmakon-lane/1 (+https://pharmakon.world)"}
    if key: h["Authorization"] = "Bearer " + key
    try:
        with urllib.request.urlopen(urllib.request.Request(BASE + path, headers=h), timeout=timeout) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e: return e.code, None
    except Exception as e: return 0, type(e).__name__


def plain(d):
    """Only numbers, yes/no and short words: never a long string (a key could be one), never the label."""
    out = {}
    for k, v in (d or {}).items():
        if k == "label": continue
        if v is None or isinstance(v, (bool, int, float)): out[k] = v
        elif isinstance(v, str) and len(v) <= 24 and "sk-" not in v: out[k] = v
        elif isinstance(v, dict): out[k] = plain(v)
    return out


def per_m(x):
    try: return round(float(x) * 1e6, 4)
    except (TypeError, ValueError): return None


def main():
    key = (os.environ.get("OPENROUTER_API_KEY") or "").strip()
    want = ""
    for f in sorted((ROOT / "data" / "auto" / "requests").glob("orcheck-*.json")):
        try: want = str(json.load(open(f, encoding="utf-8")).get("dashboard_key_ends") or "")[:4] or want
        except ValueError: pass
    pay = json.load(open(ROOT / "data" / "auto" / "lane" / "pay.json", encoding="utf-8")).get("openrouter") or {}
    out = {"_note": "Made by scripts/auto/or_check.py on GitHub's machines: which OpenRouter key the runs use (never the key itself) and what it may spend; the ids and prices of the models this system names. Nothing here costs anything.",
           "when": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    if not key:
        out["key"] = {"set": False}
    else:
        st, j = get("key", key)
        d = (j or {}).get("data") if isinstance(j, dict) else None
        label = str((d or {}).get("label") or "")
        out["key"] = {"set": True, "status": st, "ends_as_dashboard": (key.endswith(want) if want else None), "dashboard_key_ends": want,
                      "label_ends": label[-3:], "label_looks_like_a_key": label.startswith("sk-or-"), "label_ends_as_dashboard": (label.endswith(want) if want and label else None),
                      **plain(d)}
        st2, j2 = get("credits", key)
        out["credits"] = {"status": st2, **plain((j2 or {}).get("data") if isinstance(j2, dict) else {})}
    st3, j3 = get("models")
    ms = (j3 or {}).get("data") if isinstance(j3, dict) else None
    named = set((pay.get("models") or {}).keys())
    for f in [ROOT / "data" / "auto" / "lane" / "models.json"] + sorted((ROOT / "data" / "auto" / "requests").glob("*.json")) + sorted((ROOT / "data" / "auto" / "requests-prepared").glob("*.json")):
        try: t = f.read_text(encoding="utf-8")
        except OSError: continue
        named |= set(re.findall(r'"openrouter:([A-Za-z0-9_.\-/:]+)"', t))
    found = {}
    if isinstance(ms, list):
        ids = {m.get("id"): m for m in ms if isinstance(m, dict)}
        for n in sorted(named):
            m = ids.get(n)
            base = n.split(":")[0]; fam = base.rsplit("-", 1)[0] if "-" in base.split("/")[-1] else base
            near = sorted(i for i in ids if i and i != n and (i.startswith(base) or i.startswith(fam)))[:12]   # the same model's other ids, and its family's
            found[n] = {"listed": bool(m), "near": near}
            if m:
                pr = m.get("pricing") or {}
                found[n].update({"in": per_m(pr.get("prompt")), "out": per_m(pr.get("completion")), "context": m.get("context_length"),
                                 "reasoning": "reasoning" in (m.get("supported_parameters") or []), "ceiling": (pay.get("models") or {}).get(n, {}).get("max")})
                st4, j4 = get("models/" + urllib.parse.quote(n, safe="/:") + "/endpoints")
                eps = ((j4 or {}).get("data") or {}).get("endpoints") if isinstance(j4, dict) else None
                if isinstance(eps, list):
                    cap = found[n]["ceiling"] or [None, None]; rows = []
                    for e in eps:
                        p2 = e.get("pricing") or {}; i_, o_ = per_m(p2.get("prompt")), per_m(p2.get("completion"))
                        rows.append({"provider": e.get("provider_name"), "in": i_, "out": o_, "quantization": e.get("quantization"), "max_out": e.get("max_completion_tokens"),
                                     "status": e.get("status"), "under_ceiling": (cap[0] is not None and i_ is not None and o_ is not None and i_ <= cap[0] and o_ <= cap[1])})
                    found[n]["providers"] = rows
    out["models"] = {"status": st3, "named": found}
    t = json.dumps(out, ensure_ascii=False, indent=1)
    if key and len(key) >= 6: t = t.replace(key, "***")   # (it is never written above; this only makes sure)
    (ROOT / "data" / "auto" / "or-check.json").write_text(t + "\n", encoding="utf-8")
    k = out["key"]
    print("or_check: key set:", k.get("set"), "| status:", k.get("status"), "| ends as the dashboard's:", k.get("ends_as_dashboard"), "| label ends as it:", k.get("label_ends_as_dashboard"),
          "| bought credit before (not free tier):", (None if k.get("is_free_tier") is None else not k.get("is_free_tier")), "| limit:", k.get("limit"), "| left:", k.get("limit_remaining"),
          "| credits status:", (out.get("credits") or {}).get("status"), "| models listed:", sum(1 for v in found.values() if v.get("listed")), "of", len(found))


if __name__ == "__main__":
    main()
