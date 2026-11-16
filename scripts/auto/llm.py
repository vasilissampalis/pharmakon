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

A second free service, off until its key exists (the secret GROQ_API_KEY; the senior author's to decide): Groq. A model
named "groq:<its id>" is asked there (https://api.groq.com/openai/v1/chat/completions, the same form). Its free plan,
read on Groq's own page on 15 November 2026 (console.groq.com/docs/rate-limits): for each of openai/gpt-oss-120b,
openai/gpt-oss-20b and qwen/qwen3.8-27b, 30 requests and 8,000 tokens a minute, 1,000 requests and 200,000 tokens a day.
The ledger counts tokens for each of its models and a call that today's free tokens cannot hold is not made (Budget);
between calls it waits so that a minute never holds more than the plan allows. A free account is not charged.
"""
import sys, os, io, re, json, time, pathlib, datetime, urllib.request, urllib.error

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
GROQ = "https://api.groq.com/openai/v1/chat/completions"
GROQ_FREE = {"openai/gpt-oss-120b": {"tpm": 8000, "tpd": 200000, "rpd": 1000}, "openai/gpt-oss-20b": {"tpm": 8000, "tpd": 200000, "rpd": 1000}, "qwen/qwen3.8-27b": {"tpm": 8000, "tpd": 200000, "rpd": 1000}}
GROQ_SHARE = 0.9        # of a day's free tokens, where we stop by ourselves
_minute = {}            # model -> [(when, tokens)] of the last minute


class Budget(Exception):
    """Today's free allowance is used up (or would be by this call)."""


class Unavailable(Exception):
    """No key, or the service cannot be used now."""


def today(): return datetime.datetime.now(datetime.timezone.utc).date().isoformat()   # the allowance resets at 00:00 UTC


def ledger():
    try: d = json.load(open(LEDGER, encoding="utf-8"))
    except (OSError, ValueError): d = {}
    if d.get("day") != today(): d = dict({"day": today(), "neurons": 0.0, "calls": 0, "by_model": {}}, **({"groq_rolling": d["groq_rolling"]} if isinstance(d.get("groq_rolling"), dict) else {}))   # (Groq's day does not begin at midnight: see groq_level)
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


# ---------- more services (16 November 2026) ----------
# The senior author, 21:11: "we have to make this as perfect as possible as claude to how Fable 5.2 would generate answers". The exam
# says the free models we have catch about half of what a careful reader catches, so stronger readers are tried: three services
# with a free plan (Mistral's free mode, Google AI Studio's free tier, OpenRouter's free models) and, only if he chooses to pay, a
# top model through its own interface. A model is named "service:its name" ("mistral:mistral-large-latest"). Nothing here is used
# by the lane until a model has sat the exam (exam_models.py) and data/auto/lane/models.json names it.
#   key: the name of the repository secret; gap: seconds between two calls (the free plans count calls a minute);
#   calls: calls in a day (UTC) where we stop by ourselves; paid: a service that costs money for every call.
# What may be sent to any of them: our own wording of a question and passages of public papers and official pages. Never a
# visitor's words (those go to Cloudflare alone).
SERVICES = {
    "mistral": {"url": "https://api.mistral.ai/v1/chat/completions", "models": "https://api.mistral.ai/v1/models", "key": "MISTRAL_API_KEY", "gap": 1.5, "calls": 1500, "json": True},
    "gemini": {"url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", "models": "https://generativelanguage.googleapis.com/v1beta/openai/models", "key": "GEMINI_API_KEY", "gap": 7.0, "calls": 180, "json": True},
    "openrouter": {"url": "https://openrouter.ai/api/v1/chat/completions", "models": "https://openrouter.ai/api/v1/models", "key": "OPENROUTER_API_KEY", "gap": 3.5, "calls": 45, "json": False},
    "claude": {"url": "https://api.anthropic.com/v1/messages", "models": "https://api.anthropic.com/v1/models", "key": "ANTHROPIC_API_KEY", "gap": 0.4, "calls": 4000, "paid": True},
}
PRICES = ROOT / "data" / "auto" / "lane" / "prices.json"      # what a paid model costs, as read from its maker's own page, and the most that may be spent in a day and in a month
FREE = ROOT / "data" / "auto" / "lane" / "free-limits.json"   # what each free plan allows each model (calls a minute, calls a day), as read on the service's own page
OF_A_DAY = 0.9                                                 # where we stop by ourselves: nine tenths of the calls a free plan allows a model in a day
_last_call = {}
_minute = {}                                                   # model -> [(when, tokens)] of this run's calls in the last minute (for a plan that counts tokens a minute)


def service_of(model):
    """("mistral", "mistral-large-latest") for "mistral:mistral-large-latest"; (None, model) for Cloudflare's and Groq's models."""
    svc, _, name = model.partition(":")
    return (svc, name) if svc in SERVICES and name else (None, model)


def svc_used(svc, d=None):
    """What was used of a service: {"day", "calls", "in", "out", "usd", "month", "usd_month"} (a day and a month by UTC)."""
    u = dict(((d if d is not None else ledger()).get("svc") or {}).get(svc) or {})
    if u.get("day") != today(): u.update(day=today(), calls=0, usd=0.0, models={}, **{"in": 0, "out": 0})
    if u.get("month") != today()[:7]: u.update(month=today()[:7], usd_month=0.0)
    return u


def prices():
    try: return json.load(open(PRICES, encoding="utf-8"))
    except (OSError, ValueError): return {}


def usd_left(svc="claude"):
    """Dollars a paid service may still be asked for today (the smaller of what is left of the day's and of the month's limit in prices.json; 0 where no limit is written)."""
    p = prices(); u = svc_used(svc)
    return max(0.0, min(float(p.get("usd_a_day") or 0) - u["usd"], float(p.get("usd_a_month") or 0) - u["usd_month"]))


def free_limits():
    try: return json.load(open(FREE, encoding="utf-8"))
    except (OSError, ValueError): return {}


def limits_of(model):
    """What its free plan allows one model of a service: {"gap": seconds between two calls, "calls": calls in a day where we
    stop by ourselves, "tpm": tokens a minute or None}. From data/auto/lane/free-limits.json (the first pattern of the
    service's list that matches the model's name, else the service's "else"); where the file says nothing, the service's own
    cautious numbers above. (The senior author, 16 November 2026: Google gives its models very different free allowances, from
    20 calls a day to 14,400.)"""
    svc, name = service_of(model); S = SERVICES[svc]; f = free_limits().get(svc) or {}
    row = next((r for r in f.get("models") or [] if isinstance(r, dict) and re.search(str(r.get("match") or "$^"), name)), None) or (f.get("else") if isinstance(f.get("else"), dict) else None)
    if not row: return {"gap": S["gap"], "calls": S["calls"], "tpm": None}
    rpm, rpd = float(row.get("rpm") or 60.0 / S["gap"]), float(row.get("rpd") or S["calls"] / OF_A_DAY)
    return {"gap": round(60.0 / max(rpm, 0.1) * 1.1, 2), "calls": int(rpd * OF_A_DAY), "tpm": (int(row["tpm"]) if row.get("tpm") else None)}


def calls_left(x):
    """Calls still open today: for a model of a service ("gemini:gemma-...": its own free allowance), or for a whole service by its name."""
    svc, name = service_of(x)
    if svc: return max(0, min(limits_of(x)["calls"] - int((svc_used(svc).get("models") or {}).get(name) or 0), SERVICES[svc]["calls"] - svc_used(svc)["calls"] if not (free_limits().get(svc) or {}) else 10 ** 9))
    return max(0, SERVICES[x]["calls"] - svc_used(x)["calls"])


def calls_fit(by_model):
    """Can these calls ({a service's model: how many}) all still be made today? Each model against its own allowance; and where
    a service counts all its models together (no list of its own in free-limits.json: OpenRouter's free models), their sum."""
    by_svc = {}
    for m, n in by_model.items():
        if n > calls_left(m): return False
        svc = service_of(m)[0]; by_svc[svc] = by_svc.get(svc, 0) + n
    return all(bool(free_limits().get(svc)) or n <= calls_left(svc) for svc, n in by_svc.items())


def never_paid(model):
    """Why a model may not be asked because it could cost money, or "" (the senior author, 16 November 2026: "Pharmakon must use
    only free API models, with no billing, paid subscriptions, credit purchases or unexpected charges"). This is code, not a
    setting: at OpenRouter only a model whose name ends in ":free" costs nothing, so no other is ever asked there."""
    svc, name = service_of(model)
    if svc == "openrouter" and not name.endswith(":free"): return f"{name} is not one of the models OpenRouter gives for free (their names end in “:free”): never asked"
    return ""


def cost(model, tokens_in, tokens_out):
    """Dollars for a call of a paid model, by data/auto/lane/prices.json ($ per million tokens: [in, out]); None when its price is not written there."""
    p = (prices().get("models") or {}).get(model)
    return None if not p else tokens_in * p[0] / 1e6 + tokens_out * p[1] / 1e6


def has(model):
    """Can this model be asked at all on this machine (is its service's key there)?"""
    svc, _ = service_of(model)
    if svc: return bool((os.environ.get(SERVICES[svc]["key"]) or "").strip()) and not never_paid(model)
    return bool((os.environ.get("GROQ_API_KEY") or "").strip()) if model.startswith("groq:") else bool((os.environ.get("CLOUDFLARE_API_TOKEN") or "").strip())


def chat_service(model, messages, max_tokens, opener=None, tries=3):
    """A call to one of SERVICES. Mistral, Google and OpenRouter take the same request (the form OpenAI made common); Claude's
    own interface takes the system text apart from the messages. A paid service is never asked beyond the limits written in
    data/auto/lane/prices.json, and never for a model whose price is not written there."""
    svc, name = service_of(model); S = SERVICES[svc]
    key = (os.environ.get(S["key"]) or "").strip()
    if not key: raise Unavailable(f"no key for {svc} (the repository secret {S['key']} is not set)")
    if never_paid(model): raise Unavailable(never_paid(model))
    lim = limits_of(model)
    if calls_left(model) <= 0: raise Budget(f"{svc}: today's calls for {name} are used ({lim['calls']} is where we stop)")
    est_in = sum(rough_tokens(m["content"]) for m in messages)
    if S.get("paid"):
        c = cost(model, est_in, max_tokens)
        if c is None: raise Unavailable(f"{model} costs money and its price is not in data/auto/lane/prices.json: not asked")
        if c > usd_left(svc): raise Budget(f"{svc}: the spending limit cannot hold this call (${svc_used(svc)['usd']:.2f} spent today, ${svc_used(svc)['usd_month']:.2f} this month)")
    if svc == "claude":
        system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
        body = {"model": name, "max_tokens": max_tokens, "temperature": 0, "messages": [{"role": m["role"], "content": m["content"]} for m in messages if m["role"] != "system"]}
        if system: body["system"] = system
        eff = EFFORT.get(name)                                              # an exam's or a trial's own choice: the model thinks before it answers
        if eff in ("low", "medium", "high"):
            budget = {"low": 1500, "medium": 4000, "high": 10000}[eff]; body.update(max_tokens=max_tokens + budget, thinking={"type": "enabled", "budget_tokens": budget}); body.pop("temperature")
        headers = {"x-api-key": key, "anthropic-version": "2023-06-01", "Content-Type": "application/json", "User-Agent": "pharmakon-lane/1 (+https://pharmakon.world)"}
    else:
        body = {"model": name, "messages": messages, "max_tokens": max_tokens, "temperature": 0}
        if S.get("json") and any("json" in m["content"].lower() for m in messages): body["response_format"] = {"type": "json_object"}
        if EFFORT.get(name) in ("low", "medium", "high") and svc == "gemini": body["reasoning_effort"] = EFFORT[name]
        headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json", "User-Agent": "pharmakon-lane/1 (+https://pharmakon.world)"}
        if svc == "openrouter": headers.update({"HTTP-Referer": "https://pharmakon.world", "X-Title": "Pharmakon"})
    op = opener or urllib.request.urlopen; last = None
    for k in range(tries):
        wait = lim["gap"] - (time.time() - _last_call.get(model, 0))                 # (each model has its own calls a minute)
        if lim["tpm"]:                                                              # a plan that counts tokens a minute: this run's own calls of the last minute are counted before the next is sent
            now = time.time(); mine = _minute[model] = [(w, n) for w, n in _minute.get(model, []) if now - w < 60]
            if mine and sum(n for _, n in mine) + est_in + max_tokens > OF_A_DAY * lim["tpm"]: wait = max(wait, 60 - (now - mine[0][0]) + 1)
        if wait > 0 and not opener: time.sleep(wait)
        _last_call[model] = time.time(); _minute.setdefault(model, []).append((time.time(), est_in + max_tokens))
        try:
            with op(urllib.request.Request(S["url"], data=json.dumps(body).encode("utf-8"), headers=headers), timeout=180) as r: d = json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            whole = e.read().decode("utf-8", "replace")[:6000] if hasattr(e, "read") else ""; detail = whole[:400]; last = f"{svc} answered {e.code}: {detail}"
            if e.code == 429 or (e.code == 529 and svc == "claude"):
                a_day = re.search(r"per[ _-]?day|daily|free-models-per-day", whole, re.I); a_minute = re.search(r"per[ _-]?(?:minute|second)|\bRPM\b|\bTPM\b", whole, re.I)
                if a_day or (not a_minute and re.search(r"quota|RESOURCE_EXHAUSTED|credit balance|insufficient|exceeded your current", whole, re.I)):
                    L = ledger(); used = svc_used(svc, L); used.setdefault("models", {})[name] = max(int(used["models"].get(name) or 0), lim["calls"]); L.setdefault("svc", {})[svc] = used      # the service's own word is believed: this model is done for today
                    LEDGER.parent.mkdir(parents=True, exist_ok=True); json.dump(L, open(LEDGER, "w", encoding="utf-8"), indent=1)
                    raise Budget(f"{svc} says the allowance is used up: {detail[:160]}")
                ra = str((e.headers or {}).get("Retry-After") or "").strip(); rd = re.search(r'"retryDelay":\s*"(\d+(?:\.\d+)?)s?"', whole)
                secs = min(65, int(float(ra)) + 1) if re.fullmatch(r"\d+(?:\.\d+)?", ra) else min(65, int(float(rd.group(1))) + 1) if rd else 25
                if k + 1 < tries: time.sleep(0 if opener else secs); continue
            if e.code in (500, 502, 503, 504) and k + 1 < tries: time.sleep(0 if opener else 4 * (k + 1)); continue
            if e.code in (400, 401, 402, 403, 404, 413, 422): raise Unavailable(last)
            continue
        except (urllib.error.URLError, TimeoutError, ConnectionError, ValueError) as e:
            last = f"{svc} could not be reached: {str(e)[:160]}"
            if k + 1 < tries: time.sleep(0 if opener else 4); continue
            break
        if svc == "claude":
            text = "".join(b.get("text", "") for b in d.get("content") or [] if b.get("type") == "text"); u = d.get("usage") or {}
            t_in, t_out, finish = int(u.get("input_tokens") or est_in), int(u.get("output_tokens") or rough_tokens(text)), d.get("stop_reason")
            reasoned = sum(len(b.get("thinking", "")) for b in d.get("content") or [] if b.get("type") == "thinking")
        else:
            ch = (d.get("choices") or [{}])[0]; msg = ch.get("message") or {}; text = msg.get("content") or ""; u = d.get("usage") or {}
            if isinstance(text, list): text = "".join(x.get("text", "") for x in text if isinstance(x, dict))
            t_in, t_out, finish = int(u.get("prompt_tokens") or est_in), int(u.get("completion_tokens") or rough_tokens(text)), ch.get("finish_reason")
            reasoned = len(msg.get("reasoning") or msg.get("reasoning_content") or "")
        L = ledger(); used = svc_used(svc, L); used["calls"] += 1; used["in"] += t_in; used["out"] += t_out
        used.setdefault("models", {})[name] = int(used["models"].get(name) or 0) + 1
        c = cost(model, t_in, t_out) if S.get("paid") else 0.0
        used["usd"] = round(used["usd"] + (c or 0.0), 6); used["usd_month"] = round(used["usd_month"] + (c or 0.0), 6)
        L.setdefault("svc", {})[svc] = used
        LEDGER.parent.mkdir(parents=True, exist_ok=True); json.dump(L, open(LEDGER, "w", encoding="utf-8"), indent=1)
        LAST.clear(); LAST.update({"finish": finish, "in": t_in, "out": t_out, "reasoned": reasoned, "wrote": len(text)})
        return clean(text)
    raise Unavailable(last or f"{svc} gave no answer")


def models_of(svc, opener=None):
    """The names of the models a service offers this key (its own list), or the reason it gave none. No key is ever returned."""
    S = SERVICES[svc]; key = (os.environ.get(S["key"]) or "").strip()
    if not key: return None, "no key"
    headers = {"x-api-key": key, "anthropic-version": "2023-06-01"} if svc == "claude" else {"Authorization": "Bearer " + key}
    try:
        with (opener or urllib.request.urlopen)(urllib.request.Request(S["models"], headers=dict(headers, **{"User-Agent": "pharmakon-lane/1 (+https://pharmakon.world)"})), timeout=60) as r: d = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e: return None, f"answered {e.code}"
    except (urllib.error.URLError, TimeoutError, ConnectionError, ValueError) as e: return None, "could not be reached: " + str(e)[:120]
    rows = d.get("data") if isinstance(d, dict) else d
    return sorted({str(x.get("id") or x.get("name") or "").replace("models/", "") for x in rows or [] if isinstance(x, dict)} - {""}), ""


def groq_level(name, d=None, now=None):
    """(tokens, calls) of one of Groq's models that count against its free plan right now, by our own count. Groq's day is
    not a calendar day: what was used comes back bit by bit over the next 24 hours (its refusals say "try again in 8m"),
    so the count drains at one day's allowance in 24 hours. (Until 16 November 2026 this file began every model anew at
    00:00 UTC; a batch just after midnight would have been promised tokens that Groq had not given back yet.)"""
    lim = GROQ_FREE.get(name); r = ((d if d is not None else ledger()).get("groq_rolling") or {}).get(name) or {}
    if not lim: return 0.0, 0.0
    dt = max(0.0, (now or time.time()) - float(r.get("at") or 0))
    return max(0.0, float(r.get("tokens") or 0) - lim["tpd"] * dt / 86400), max(0.0, float(r.get("calls") or 0) - lim["rpd"] * dt / 86400)


def groq_left(name, now=None):
    """Tokens of Groq's free plan that one of its models can still take now, by our own count (we stop at GROQ_SHARE of it)."""
    lim = GROQ_FREE.get(name)
    if not lim: return 0
    tokens, calls = groq_level(name, now=now)
    return 0 if calls >= lim["rpd"] * GROQ_SHARE else max(0, int(lim["tpd"] * GROQ_SHARE - tokens))


def groq_count(name, used, calls=1, full=False):
    """Write a call at Groq into the ledger: the day's count (for the record) and the draining count (for what is left).
    full: Groq itself said the day's plan is used up, so the draining count is set to the whole allowance."""
    L = ledger(); now = time.time(); lim = GROQ_FREE[name]
    g = L.setdefault("groq", {}).setdefault(name, {"calls": 0, "tokens": 0}); g["calls"] += calls; g["tokens"] += used
    tokens, n = groq_level(name, L, now)
    L.setdefault("groq_rolling", {})[name] = {"at": round(now), "tokens": lim["tpd"] if full else round(tokens + used), "calls": round(n + calls, 2)}
    LEDGER.parent.mkdir(parents=True, exist_ok=True); json.dump(L, open(LEDGER, "w", encoding="utf-8"), indent=1)


def chat_groq(model, messages, max_tokens, opener=None, tries=3):
    name = model[5:]; token = (os.environ.get("GROQ_API_KEY") or "").strip()
    if not token: raise Unavailable("no key for Groq (the secret GROQ_API_KEY is not set)")
    lim = GROQ_FREE.get(name)
    if not lim: raise Unavailable(f"{name} is not on the list of Groq's free models that this file knows")
    est = sum(rough_tokens(m["content"]) for m in messages) + max_tokens
    if est > lim["tpm"]: raise Unavailable(f"this call is larger than Groq's free plan allows in a minute ({est} of {lim['tpm']} tokens)")
    if est > groq_left(name): raise Budget(f"today's free tokens at Groq cannot hold this call for {name}")
    now = time.time(); recent = [(t, n) for t, n in _minute.get(name, []) if now - t < 61]
    while recent and sum(n for _, n in recent) + est > lim["tpm"]:                       # wait for the minute to have room
        wait = 61 - (now - recent[0][0])
        if opener is None and wait > 0: time.sleep(min(wait, 61))
        recent = recent[1:]; now = time.time()
    body = {"model": name, "messages": messages, "max_completion_tokens": max_tokens, "temperature": 0}
    # how each model reasons at Groq (console.groq.com/docs/reasoning, read 16 November 2026): gpt-oss takes reasoning_effort low, medium or high and
    # returns its reasoning apart from its answer (reasoning_format is not for it); qwen3.8-27b does not reason unless an effort is set, and with
    # reasoning_format "hidden" its answer comes without its reasoning. The larger gpt-oss writes and checks (medium); the smaller only reads (low).
    # (Until 16 November 2026, 19:40 this line asked "20b" in name, which "gpt-oss-120b" also holds: the larger model wrote plans and checked with LOW
    # effort in lanes 7 to 9 and in its first exam. EFFORT: an exam's or a trial's own choice for a model.)
    if name.startswith("openai/gpt-oss"): body["reasoning_effort"] = EFFORT.get(name) or ("low" if name.endswith("gpt-oss-20b") else "medium")
    elif name.startswith("qwen/qwen3"):                                # Groq's free plan gives it 1,000 output tokens a minute (its refusal of 16 November 2026: "output tokens per minute (OTPM): Limit 1000"): it answers without reasoning first, and never more than 900 tokens
        body["reasoning_effort"] = "none"; body["max_completion_tokens"] = min(max_tokens, 900)
    op = opener or urllib.request.urlopen
    for k in range(tries):
        req = urllib.request.Request(GROQ, data=json.dumps(body).encode("utf-8"), method="POST", headers={"Authorization": "Bearer " + token, "Content-Type": "application/json", "User-Agent": "Pharmakon (https://pharmakon.world; mailto:contact@pharmakon.world)"})
        try:
            with op(req, timeout=180) as r: d = json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = ""
            try: detail = e.read().decode("utf-8", "replace")[:300]
            except Exception: pass
            if e.code == 429 and re.search(r"per day|TPD|RPD|daily", detail, re.I):
                groq_count(name, 0, 0, full=True)                        # our count was too low: Groq's own word is taken, and the next team is chosen without this model
                raise Budget("Groq says today's free plan is used up for " + name)
            if e.code in (429, 500, 502, 503, 504) and k + 1 < tries: time.sleep(0 if opener else 20 * (k + 1)); continue
            raise Unavailable(f"Groq answered {e.code}" + (": " + re.sub(r"\s+", " ", detail) if detail else ""))
        except (urllib.error.URLError, TimeoutError, ConnectionError, ValueError) as e:
            if k + 1 < tries: time.sleep(0 if opener else 3); continue
            raise Unavailable("Groq could not be reached: " + str(e)[:200])
        text = ((d.get("choices") or [{}])[0].get("message") or {}).get("content") or ""; u = d.get("usage") or {}
        used = int(u.get("total_tokens") or (int(u.get("prompt_tokens") or est - max_tokens) + int(u.get("completion_tokens") or rough_tokens(text))))
        groq_count(name, used)
        _minute[name] = recent + [(time.time(), used)]
        return clean(text)
    raise Unavailable("Groq gave no answer")


EFFORT = {}   # {"openai/gpt-oss-120b": "high"}: how hard one of Groq's reasoning models is asked to think, where a run sets it (an exam, a trial); otherwise as chat_groq says
LAST = {}   # about the last answer: why it ended, the service's token counts, how long the model reasoned before it wrote (for the trials; never an answer's words)


def chat(model, messages, max_tokens=700, opener=None, tries=3, extra=None):
    """The model's answer to messages ([{"role", "content"}]). Raises Budget before a call that today's allowance cannot
    hold, Unavailable when there is no key or the service refuses. extra: more fields for the request (a trial's)."""
    if model.startswith("groq:"): return chat_groq(model, messages, max_tokens, opener, tries)
    if service_of(model)[0]: return chat_service(model, messages, max_tokens, opener, tries)
    token, account = (os.environ.get("CLOUDFLARE_API_TOKEN") or "").strip(), (os.environ.get("CLOUDFLARE_ACCOUNT_ID") or "").strip()   # a secret pasted with a line break after it is the same secret
    if not token or not account: raise Unavailable("no key (the repository's two secrets are not set)")
    if not re.fullmatch(r"[0-9a-fA-F]{32}", account) and account != "ACC": raise Unavailable("the account number in the secret CLOUDFLARE_ACCOUNT_ID is not a Cloudflare account ID (32 letters a-f and digits)")
    pi, po = PRICE.get(model, DEAR); est_in = sum(rough_tokens(m["content"]) for m in messages)
    if est_in * pi / 1e6 + max_tokens * po / 1e6 > left(): raise Budget(f"today's free allowance cannot hold this call ({ledger()['neurons']:.0f} of {OUR_LIMIT} neurons used)")
    body = json.dumps(dict({"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0}, **(extra or {}))).encode("utf-8")
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
        LAST.clear(); LAST.update({"finish": (d.get("choices") or [{}])[0].get("finish_reason"), "in": u.get("prompt_tokens"), "out": u.get("completion_tokens"),
                                   "reasoned": len(str(ch.get("reasoning_content") or ch.get("reasoning") or "")), "wrote": len(text or "")})
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
    # the second service: off without its key; with it, the same form, tokens counted for each model, a call the day cannot hold is not sent
    had = os.environ.pop("GROQ_API_KEY", None)                       # (on the machine that has the key, this test must still see what happens without it)
    assert not has("groq:openai/gpt-oss-120b")
    try: chat("groq:openai/gpt-oss-120b", [{"role": "user", "content": "x"}], 10, opener); raise AssertionError("no Unavailable")
    except Unavailable: pass
    os.environ["GROQ_API_KEY"] = "G\n"; sent = []
    def gopener(req, timeout=0):
        b = json.loads(req.data.decode()); sent.append(b)
        assert req.full_url == GROQ and req.get_header("Authorization") == "Bearer G" and b["model"] in ("openai/gpt-oss-120b", "openai/gpt-oss-20b") and b["reasoning_effort"] == ("low" if b["model"].endswith("-20b") else EFFORT.get(b["model"], "medium"))
        return Resp({"choices": [{"message": {"content": "{\"ok\": 1}"}}], "usage": {"total_tokens": 1200}})
    assert has("groq:openai/gpt-oss-120b") and chat("groq:openai/gpt-oss-120b", [{"role": "user", "content": "x" * 400}], 200, gopener) == '{"ok": 1}'
    assert ledger()["groq"]["openai/gpt-oss-120b"] == {"calls": 1, "tokens": 1200} and 180000 - 1200 <= groq_left("openai/gpt-oss-120b") <= 180000 - 1195
    # Groq's day drains: half a day later half a day's allowance has come back, and midnight changes nothing
    later = time.time() + 43200
    assert groq_left("openai/gpt-oss-120b", now=later) == 180000 and groq_level("openai/gpt-oss-120b", now=later) == (0.0, 0.0)
    L = ledger(); L["groq_rolling"]["openai/gpt-oss-120b"] = {"at": round(time.time()), "tokens": 150000, "calls": 100}; L["day"] = "2001-01-01"; json.dump(L, open(LEDGER, "w"))
    assert "groq" not in ledger() and 29990 <= groq_left("openai/gpt-oss-120b") <= 30010 and 129000 <= groq_left("openai/gpt-oss-120b", now=later) <= 131000
    L = ledger(); L["groq_rolling"]["openai/gpt-oss-120b"]["tokens"] = 179900; json.dump(L, open(LEDGER, "w"))
    for m, err in (("groq:openai/gpt-oss-120b", Budget), ("groq:some/other-model", Unavailable)):
        try: chat(m, [{"role": "user", "content": "x" * 400}], 200, gopener); raise AssertionError("no " + err.__name__)
        except err: pass
    try: chat("groq:qwen/qwen3.8-27b", [{"role": "user", "content": "x" * 40000}], 200, gopener); raise AssertionError("a call larger than a minute allows was sent")
    except Unavailable: pass
    assert len(sent) == 1
    # the smaller model reads with little effort, the larger with medium unless a run says otherwise; Groq's own "used up for the day" is believed
    chat("groq:openai/gpt-oss-20b", [{"role": "user", "content": "x"}], 50, gopener); EFFORT["openai/gpt-oss-120b"] = "high"
    L = ledger(); L["groq_rolling"]["openai/gpt-oss-120b"]["tokens"] = 1000; json.dump(L, open(LEDGER, "w"))
    chat("groq:openai/gpt-oss-120b", [{"role": "user", "content": "x"}], 50, gopener); assert sent[-1]["reasoning_effort"] == "high" and sent[-2]["reasoning_effort"] == "low"; EFFORT.clear()
    def full(req, timeout=0): raise urllib.error.HTTPError(GROQ, 429, "Too Many Requests", {}, io.BytesIO(b'{"error": {"message": "Rate limit reached on tokens per day (TPD): Limit 200000, Used 199000. Please try again in 8m"}}'))
    try: chat("groq:openai/gpt-oss-120b", [{"role": "user", "content": "x"}], 50, full); raise AssertionError("no Budget")
    except Budget: pass
    assert groq_left("openai/gpt-oss-120b") == 0 and groq_left("openai/gpt-oss-120b", now=time.time() + 6 * 3600) > 29000
    del os.environ["GROQ_API_KEY"]
    # ---- more services: each is off without its key; a call is counted; the common form and Claude's own form; a paid model is never asked without its price and its limit
    global PRICES
    assert not has("mistral:mistral-large-latest") and service_of("mistral:mistral-large-latest") == ("mistral", "mistral-large-latest") and service_of("@cf/openai/gpt-oss-120b") == (None, "@cf/openai/gpt-oss-120b") and service_of("groq:x/y")[0] is None
    try: chat("mistral:mistral-large-latest", [{"role": "user", "content": "x"}], 50, lambda *a, **k: (_ for _ in ()).throw(AssertionError("called without a key"))); raise AssertionError("no Unavailable")
    except Unavailable: pass
    os.environ["MISTRAL_API_KEY"] = "M\n"; os.environ["OPENROUTER_API_KEY"] = "O"; os.environ["ANTHROPIC_API_KEY"] = "A"; seen = []
    def sopener(req, timeout=0):
        b = json.loads(req.data.decode("utf-8")); seen.append((req.full_url, dict(req.header_items()), b))
        if "anthropic" in req.full_url: return Resp({"content": [{"type": "thinking", "thinking": "hm"}, {"type": "text", "text": '{"ok": true}'}], "usage": {"input_tokens": 1000, "output_tokens": 200}, "stop_reason": "end_turn"})
        return Resp({"choices": [{"message": {"content": '{"ok": true}'}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 900, "completion_tokens": 100}})
    assert has("mistral:mistral-large-latest") and as_json(chat("mistral:mistral-large-latest", [{"role": "system", "content": "JSON only"}, {"role": "user", "content": "x"}], 50, sopener)) == {"ok": True}
    u, h, b = seen[-1]; assert u == SERVICES["mistral"]["url"] and h["Authorization"] == "Bearer M" and b["model"] == "mistral-large-latest" and b["response_format"] == {"type": "json_object"} and b["messages"][0]["role"] == "system"
    assert svc_used("mistral")["calls"] == 1 and svc_used("mistral")["in"] == 900 and calls_left("mistral") == SERVICES["mistral"]["calls"] - 1 and svc_used("mistral")["usd"] == 0
    chat("openrouter:nvidia/some-model:free", [{"role": "user", "content": "answer in json"}], 50, sopener)
    u, h, b = seen[-1]; assert u == SERVICES["openrouter"]["url"] and b["model"] == "nvidia/some-model:free" and "response_format" not in b and h.get("X-title") == "Pharmakon"
    L = ledger(); L["svc"]["openrouter"]["calls"] = SERVICES["openrouter"]["calls"]; json.dump(L, open(LEDGER, "w"))
    try: chat("openrouter:nvidia/some-model:free", [{"role": "user", "content": "x"}], 50, sopener); raise AssertionError("a call beyond the day's calls")
    except Budget: pass
    PRICES = pathlib.Path(tempfile.mkdtemp()) / "prices.json"
    try: chat("claude:claude-haiku-5-5", [{"role": "user", "content": "x"}], 50, sopener); raise AssertionError("a paid model asked without its price")
    except Unavailable as e: assert "price" in str(e)
    json.dump({"usd_a_day": 0.5, "usd_a_month": 20, "models": {"claude:claude-haiku-5-5": [0.10, 0.50], "claude:claude-sonnet-5-5": [2, 10]}}, open(PRICES, "w"))
    n = len(seen); assert as_json(chat("claude:claude-haiku-5-5", [{"role": "system", "content": "JSON only"}, {"role": "user", "content": "x"}], 50, sopener)) == {"ok": True}
    u, h, b = seen[-1]; assert u == SERVICES["claude"]["url"] and h["X-api-key"] == "A" and h["Anthropic-version"] == "2023-06-01" and b["system"] == "JSON only" and [m["role"] for m in b["messages"]] == ["user"] and b["max_tokens"] == 50
    assert abs(svc_used("claude")["usd"] - (1000 * 0.10 + 200 * 0.50) / 1e6) < 1e-9 and abs(usd_left("claude") - (0.5 - 0.0002)) < 1e-6 and LAST["reasoned"] == 2
    L = ledger(); L["svc"]["claude"]["usd"] = 0.4999; json.dump(L, open(LEDGER, "w"))
    try: chat("claude:claude-sonnet-5-5", [{"role": "user", "content": "x" * 4000}], 900, sopener); raise AssertionError("a call beyond the day's spending limit")
    except Budget as e: assert "spending limit" in str(e)
    assert len(seen) == n + 1
    def quota(req, timeout=0): raise urllib.error.HTTPError(req.full_url, 429, "Too Many Requests", {}, io.BytesIO(b'{"error": {"message": "You exceeded your current quota: free tier requests per day"}}'))
    try: chat("mistral:mistral-large-latest", [{"role": "user", "content": "x"}], 50, quota); raise AssertionError("no Budget")
    except Budget: pass
    names, why = models_of("mistral", lambda req, timeout=0: Resp({"data": [{"id": "mistral-large-latest"}, {"id": "mistral-small-latest"}]})); assert names == ["mistral-large-latest", "mistral-small-latest"] and why == ""
    # ---- only free models, by code: at OpenRouter a model that is not marked free is never asked, whatever a file names
    n = len(seen)
    try: chat("openrouter:openai/some-paid-model", [{"role": "user", "content": "x"}], 50, sopener); raise AssertionError("a model that costs money was asked at OpenRouter")
    except Unavailable as e: assert "free" in str(e) and len(seen) == n
    assert never_paid("openrouter:x/y") and not never_paid("openrouter:x/y:free") and not never_paid("gemini:gemma-4-31b-it") and not has("openrouter:x/y") and has("openrouter:x/y:free")
    assert not calls_fit({"openrouter:a/b:free": 1}) and calls_fit({"mistral:mistral-medium-latest": 100, "mistral:mistral-small-latest": 100}) and not calls_fit({"mistral:mistral-medium-latest": 1000, "mistral:mistral-small-latest": 600})   # (OpenRouter's day was used up above; a service that counts all its models together: their sum)
    assert calls_left("mistral:mistral-large-latest") == 0 and not calls_fit({"mistral:mistral-large-latest": 1})          # (the service itself said this model's day was used up, just above: believed)
    # ---- each model of a service has its own free allowance, read from a file: its calls a day (we stop at nine tenths), its calls a minute
    global FREE
    keep_free = FREE; FREE = pathlib.Path(tempfile.mkdtemp()) / "free-limits.json"
    json.dump({"gemini": {"models": [{"match": "^gemma-4-", "rpm": 30, "rpd": 14400}, {"match": "flash-lite", "rpm": 15, "rpd": 500, "tpm": 250000}], "else": {"rpm": 5, "rpd": 20}}}, open(FREE, "w"))
    os.environ["GEMINI_API_KEY"] = "G"
    assert limits_of("gemini:gemma-4-31b-it") == {"gap": 2.2, "calls": 12960, "tpm": None} and limits_of("gemini:gemini-3.5-flash-lite")["calls"] == 450 and limits_of("gemini:gemini-4-hydrogen") == {"gap": 13.2, "calls": 18, "tpm": None}
    assert limits_of("mistral:mistral-large-latest") == {"gap": SERVICES["mistral"]["gap"], "calls": SERVICES["mistral"]["calls"], "tpm": None}          # a service the file says nothing of keeps its own cautious numbers
    chat("gemini:gemini-4-hydrogen", [{"role": "user", "content": "x"}], 50, sopener)
    assert calls_left("gemini:gemini-4-hydrogen") == 17 and calls_left("gemini:gemma-4-31b-it") == 12960 and seen[-1][2]["model"] == "gemini-4-hydrogen"
    assert calls_fit({"gemini:gemma-4-31b-it": 9000, "gemini:gemma-4-26b-it": 9000, "gemini:gemini-4-hydrogen": 17}) and not calls_fit({"gemini:gemini-4-hydrogen": 18})          # each of Google's models has its own day
    L = ledger(); L["svc"]["gemini"]["models"]["gemini-4-hydrogen"] = 18; json.dump(L, open(LEDGER, "w"))
    try: chat("gemini:gemini-4-hydrogen", [{"role": "user", "content": "x"}], 50, sopener); raise AssertionError("a call beyond one model's day")
    except Budget: pass
    chat("gemini:gemma-4-31b-it", [{"role": "user", "content": "x"}], 50, sopener)                                    # another model of the same service has its own day
    # Google's own refusals: "a minute" is waited out and asked again; "a day" ends that model's day by our count too
    state = {"n": 0}
    def minute_then_ok(req, timeout=0):
        state["n"] += 1
        if state["n"] == 1: raise urllib.error.HTTPError(req.full_url, 429, "Too Many Requests", {}, io.BytesIO(b'{"error": {"code": 429, "message": "You exceeded your current quota", "status": "RESOURCE_EXHAUSTED", "details": [{"quotaId": "GenerateRequestsPerMinutePerProjectPerModel-FreeTier"}, {"retryDelay": "34s"}]}}'))
        return sopener(req)
    assert as_json(chat("gemini:gemma-4-31b-it", [{"role": "user", "content": "x"}], 50, minute_then_ok)) == {"ok": True} and state["n"] == 2
    def day(req, timeout=0): raise urllib.error.HTTPError(req.full_url, 429, "Too Many Requests", {}, io.BytesIO(b'{"error": {"code": 429, "status": "RESOURCE_EXHAUSTED", "details": [{"quotaId": "GenerateRequestsPerDayPerProjectPerModel-FreeTier"}]}}'))
    try: chat("gemini:gemma-4-31b-it", [{"role": "user", "content": "x"}], 50, day); raise AssertionError("no Budget")
    except Budget: pass
    assert calls_left("gemini:gemma-4-31b-it") == 0 and calls_left("gemini:gemini-3.5-flash-lite") == 450
    FREE = keep_free; del os.environ["GEMINI_API_KEY"]
    for k in ("MISTRAL_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY"): del os.environ[k]
    if had: os.environ["GROQ_API_KEY"] = had
    LEDGER = keep
    print("llm selftest: ok (one call counted in neurons by the service's own token counts; a call the day's allowance cannot hold is not sent; no key, no call; the second service is off without its key and counted by tokens with it)")


if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    else: print(json.dumps(ledger(), indent=1))
