#!/usr/bin/env python3
"""llm.py: the models the machine lane may use, and the count of what each call costs (docs/AUTOMATION.md).

The senior author: "no i don't want my claude plan to use tokens! we have to automate the ai!", "i want it to be free".
So the lane's readers, writer and checker are open models run by Cloudflare Workers AI, inside its free allowance:
10,000 "neurons" a day (read from Cloudflare's pricing page on 15 November 2026; over the allowance a free account's
calls fail, they are not charged). GitHub's own free models were retired on 30 July 2026 (its documentation says so).

    chat(model, messages, max_tokens)  ->  the model's words

  - One endpoint for every model: POST /accounts/{account}/ai/v1/chat/completions (Cloudflare's OpenAI-compatible form).
  - It needs CLOUDFLARE_API_TOKEN (Workers AI: Read and Edit) and CLOUDFLARE_ACCOUNT_ID, the repository's two secrets.
    No key and no answer is ever printed.
  - The ledger (data/auto/lane/usage.json): neurons spent today, by model. A call that would take the day past OUR_LIMIT
    is not made (Budget is raised): the lane stops for the day and goes on tomorrow. So the lane cannot cost money even
    on an account that would be charged.
  - A model's words are data. Nothing a model writes is ever run, and nothing it writes is published without passing the
    lane's gates (scripts/auto/lane.py).
"""
import sys, os, re, json, time, pathlib, datetime, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEDGER = ROOT / "data" / "auto" / "lane" / "usage.json"
API = "https://api.cloudflare.com/client/v4/accounts/{account}/ai/v1/chat/completions"
FREE_A_DAY = 10000      # Cloudflare's free allocation of neurons a day
OUR_LIMIT = 9000        # where the lane stops by itself
# neurons per million tokens, in and out (Cloudflare's pricing page, 15 November 2026); a model not listed is counted dear
PRICE = {"@cf/meta/llama-3.3-70b-instruct-fp8-fast": (26668, 204805), "@cf/meta/llama-3.1-8b-instruct-fp8-fast": (4119, 34868), "@cf/meta/llama-4-scout-17b-16e-instruct": (24545, 77273),
         "@cf/mistralai/mistral-small-3.1-24b-instruct": (31876, 50488), "@cf/google/gemma-3-12b-it": (31371, 50560), "@cf/google/gemma-4-26b-a4b-it": (9091, 27273),
         "@cf/qwen/qwen3-30b-a3b-fp8": (4625, 30475), "@cf/qwen/qwq-32b": (60000, 90909), "@cf/openai/gpt-oss-120b": (31818, 68182), "@cf/openai/gpt-oss-20b": (18182, 27273),
         "@cf/zai-org/glm-4.7-flash": (5500, 36400), "@cf/zai-org/glm-5.3-flash": (13636, 45455), "@cf/deepseek-ai/deepseek-v4.1-flash-1017": (27273, 109091),
         "@cf/ibm-granite/granite-4.0-h-micro": (1542, 10158), "@cf/nvidia/nemotron-3-120b-a12b": (45455, 136364)}
DEAR = (130000, 450000)


class Budget(Exception):
    """Today's free allowance is used up (or would be by this call)."""


class Unavailable(Exception):
    """No key, or the service cannot be used now."""


def today(): return datetime.datetime.now(datetime.timezone.utc).date().isoformat()   # the allowance resets at 00:00 UTC


def ledger():
    try: d = json.load(open(LEDGER, encoding="utf-8"))
    except (OSError, ValueError): d = {}
    if d.get("day") != today(): d = {"day": today(), "neurons": 0.0, "calls": 0, "by_model": {}}
    return d


def spend(model, tokens_in, tokens_out, save=True):
    """Write one call into the ledger; returns the neurons it cost."""
    pi, po = PRICE.get(model, DEAR); n = tokens_in * pi / 1e6 + tokens_out * po / 1e6
    d = ledger(); d["neurons"] = round(d["neurons"] + n, 2); d["calls"] += 1
    m = d["by_model"].setdefault(model, {"calls": 0, "in": 0, "out": 0, "neurons": 0.0}); m["calls"] += 1; m["in"] += tokens_in; m["out"] += tokens_out; m["neurons"] = round(m["neurons"] + n, 2)
    if save:
        LEDGER.parent.mkdir(parents=True, exist_ok=True); json.dump(d, open(LEDGER, "w", encoding="utf-8"), indent=1)
    return n


def left(): return max(0.0, OUR_LIMIT - ledger()["neurons"])


def rough_tokens(text): return int(len(text) / 3.6) + 8   # for the estimate before a call; the service's own count is used after it


def clean(text):
    """A model's words without the thinking some models print first."""
    text = re.sub(r"<think>.*?</think>", "", text or "", flags=re.S)
    if "</think>" in text: text = text.split("</think>", 1)[1]
    return text.strip()


def chat(model, messages, max_tokens=700, opener=None, tries=3):
    """The model's answer to messages ([{"role", "content"}]). Raises Budget before a call that today's allowance cannot
    hold, Unavailable when there is no key or the service refuses."""
    token, account = (os.environ.get("CLOUDFLARE_API_TOKEN") or "").strip(), (os.environ.get("CLOUDFLARE_ACCOUNT_ID") or "").strip()   # a secret pasted with a line break after it is the same secret
    if not token or not account: raise Unavailable("no key (the repository's two secrets are not set)")
    if not re.fullmatch(r"[0-9a-fA-F]{32}", account) and account != "ACC": raise Unavailable("the account number in the secret CLOUDFLARE_ACCOUNT_ID is not a Cloudflare account ID (32 letters a-f and digits)")
    pi, po = PRICE.get(model, DEAR); est_in = sum(rough_tokens(m["content"]) for m in messages)
    if est_in * pi / 1e6 + max_tokens * po / 1e6 > left(): raise Budget(f"today's free allowance cannot hold this call ({ledger()['neurons']:.0f} of {OUR_LIMIT} neurons used)")
    body = json.dumps({"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0}).encode("utf-8")
    opener = opener or urllib.request.urlopen
    for k in range(tries):
        req = urllib.request.Request(API.format(account=account), data=body, method="POST", headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
        try:
            with opener(req, timeout=180) as r: d = json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = ""
            try: detail = e.read().decode("utf-8", "replace")[:300]
            except Exception: pass
            if e.code == 429 and re.search(r"allocation|quota|neurons|daily", detail, re.I): raise Budget("Cloudflare says today's free allowance is used up")
            if e.code in (429, 500, 502, 503, 504) and k + 1 < tries: time.sleep(4 * (k + 1) if opener is urllib.request.urlopen else 0); continue
            raise Unavailable(f"the model service answered {e.code}" + (": " + re.sub(r"\s+", " ", detail) if detail else ""))
        except (urllib.error.URLError, TimeoutError, ConnectionError, ValueError) as e:
            if k + 1 < tries: time.sleep(3 if opener is urllib.request.urlopen else 0); continue
            raise Unavailable("the model service could not be reached: " + str(e)[:200])
        ch = (d.get("choices") or [{}])[0].get("message") or {}
        text = ch.get("content") or ""
        if isinstance(text, list): text = "".join(p.get("text", "") for p in text if isinstance(p, dict))
        u = d.get("usage") or {}
        spend(model, int(u.get("prompt_tokens") or est_in), int(u.get("completion_tokens") or rough_tokens(text)))
        return clean(text)
    raise Unavailable("the model service gave no answer")


def as_json(text):
    """The JSON object in a model's words, or None. Takes the outermost braces; mends a trailing comma."""
    if not text: return None
    a, b = text.find("{"), text.rfind("}")
    if a < 0 or b <= a: return None
    raw = text[a:b + 1]
    for cand in (raw, re.sub(r",\s*([}\]])", r"\1", raw)):
        try:
            v = json.loads(cand)
            return v if isinstance(v, dict) else None
        except ValueError: continue
    return None


def selftest():
    import tempfile
    global LEDGER
    keep = LEDGER; LEDGER = pathlib.Path(tempfile.mkdtemp()) / "usage.json"
    os.environ["CLOUDFLARE_API_TOKEN"] = "T\n"; os.environ["CLOUDFLARE_ACCOUNT_ID"] = "ACC\n\n"; seen = []   # pasted with line breaks after them, as it happened
    class Resp:
        def __init__(self, d): self.d = d
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return json.dumps(self.d).encode()
    def opener(req, timeout=0):
        seen.append(req); b = json.loads(req.data.decode())
        assert req.full_url.endswith("/accounts/ACC/ai/v1/chat/completions") and req.get_header("Authorization") == "Bearer T" and b["temperature"] == 0
        return Resp({"choices": [{"message": {"content": "<think>hm</think>{\"ok\": true,}"}}], "usage": {"prompt_tokens": 1000, "completion_tokens": 100}})
    out = chat("@cf/qwen/qwen3-30b-a3b-fp8", [{"role": "user", "content": "x" * 400}], 200, opener)
    assert out == '{"ok": true,}' and as_json(out) == {"ok": True}, out
    d = ledger(); assert d["calls"] == 1 and abs(d["neurons"] - (1000 * 4625 + 100 * 30475) / 1e6) < 0.01, d
    spend("@cf/qwen/qwen3-30b-a3b-fp8", 0, 0); spend("unknown/model", 60000, 0)        # an unlisted model is counted dear: 7,800 neurons
    try: chat("@cf/meta/llama-3.3-70b-instruct-fp8-fast", [{"role": "user", "content": "y" * 4000}], 8000, opener); raise AssertionError("no Budget")
    except Budget: pass
    assert len(seen) == 1                                                             # the call that would pass the limit was never sent
    del os.environ["CLOUDFLARE_API_TOKEN"]
    try: chat("m", [{"role": "user", "content": "x"}], 10, opener); raise AssertionError("no Unavailable")
    except Unavailable: pass
    assert as_json("no json here") is None and as_json('before {"a": [1, 2,], "b": "}"} after') == {"a": [1, 2], "b": "}"}
    LEDGER = keep
    print("llm selftest: ok (one call counted in neurons by the service's own token counts; a call the day's allowance cannot hold is not sent; no key, no call)")


if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    else: print(json.dumps(ledger(), indent=1))
