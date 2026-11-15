#!/usr/bin/env python3
"""probe.py: is everything the automatic work needs within reach? (docs/AUTOMATION.md)

Run on GitHub's machine with the repository's two secrets. It asks each model the lane might use for one word and for one
small JSON object, reads how many records the question store holds, and writes what answered into
data/auto/lane/probe.json. No key and no visitor's question is ever printed or written.
"""
import sys, os, json, time, pathlib, datetime, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import llm, fetch_questions as fq

MODELS = ["@cf/qwen/qwen3-30b-a3b-fp8", "@cf/meta/llama-3.3-70b-instruct-fp8-fast", "@cf/google/gemma-4-26b-a4b-it", "@cf/mistralai/mistral-small-3.1-24b-instruct",
          "@cf/openai/gpt-oss-120b", "@cf/openai/gpt-oss-20b", "@cf/zai-org/glm-4.7-flash", "@cf/meta/llama-4-scout-17b-16e-instruct"]


def main():
    out = {"_note": "Made by scripts/auto/probe.py on GitHub's machine: what answered. No key is written here.", "on": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "models": {}, "store": {}}
    for m in MODELS:
        t0 = time.time(); r = {}
        try:
            a = llm.chat(m, [{"role": "user", "content": "Reply with the single word: ready"}], 60)
            b = llm.chat(m, [{"role": "system", "content": "You answer with JSON only."}, {"role": "user", "content": 'Copy exactly, as JSON: {"quote": "between 9% and 27% met criteria", "n": 2}'}], 120)
            j = llm.as_json(b)
            r = {"ok": True, "word": a[:40], "json": j == {"quote": "between 9% and 27% met criteria", "n": 2}, "json_raw": b[:120], "seconds": round(time.time() - t0, 1)}
        except (llm.Budget, llm.Unavailable) as e: r = {"ok": False, "why": str(e)[:300]}
        out["models"][m] = r; print("probe:", m, "ok" if r.get("ok") else "NOT ok", r.get("why", ""))
    token, account = (os.environ.get("CLOUDFLARE_API_TOKEN") or "").strip(), (os.environ.get("CLOUDFLARE_ACCOUNT_ID") or "").strip()   # a secret pasted with a line break after it is the same secret
    try:
        ns = fq.find_namespace(urllib.request.urlopen, token, account, os.environ.get("KV_NAMESPACE") or "pharmakon-questions")
        if not ns: out["store"] = {"ok": False, "why": "no store named pharmakon-questions"}
        else: out["store"] = {"ok": True, "questions": len(fq.read_all(urllib.request.urlopen, token, account, ns)), "listed_items_counted": len(fq.read_wanted(urllib.request.urlopen, token, account, ns))}
    except Exception as e: out["store"] = {"ok": False, "why": type(e).__name__ + ": " + str(e)[:200]}
    out["neurons_today"] = llm.ledger()["neurons"]
    p = ROOT / "data" / "auto" / "lane" / "probe.json"; p.parent.mkdir(parents=True, exist_ok=True); json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("probe: store", "ok" if out["store"].get("ok") else "NOT ok", {k: v for k, v in out["store"].items() if k != "ok"})


if __name__ == "__main__":
    main()
