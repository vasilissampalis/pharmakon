#!/usr/bin/env python3
"""local_llm.py: open models of our own, run on GitHub's machines (docs/AUTOMATION.md, decision 38).

The senior author, 19 November 2026, 20:20 Athens: "this should never happen ... our ai has to be unstoppable and always working";
20:50, of "a model of our own on GitHub's machines, used when the free allowances run out": "yes it has to work like an LLM ... so
NOTHING NEVER UNSTOPPABLY runs out". The repository is public, so GitHub's machines cost nothing and have no daily allowance: a model
that runs ON the machine has no limit but the machine's speed (four processor cores, 16 GB of memory, no graphics card).

    python3 -I scripts/auto/local_llm.py serve NAME [--port 8088]    fetch the model (once: GitHub's cache keeps it) and start its server in the
                                                                     background; returns when it answers (OpenAI's form, as llm.py asks every service)
    python3 -I scripts/auto/local_llm.py bench [--request FILE]      each model of the request: start it, measure how fast it reads and writes on
                                                                     this machine, sit the lane's exam (optional), stop it; data/auto/exam/local-bench.json
    python3 -I scripts/auto/local_llm.py find                        the open models in GGUF form that the model hub lists most (name, size, licence),
                                                                     for choosing the next to try; data/auto/exam/local-find.json
    python3 -I scripts/auto/local_llm.py --selftest

MODELS: our name -> where its weights are (Hugging Face repositories, tried in order, and the file's pattern) and its licence. Only models
whose licence allows any use (Apache 2.0, MIT) and that anyone may download without signing in. What a model writes is data, never run,
and nothing it writes is published without the lane's gates (scripts/auto/lane.py), as for every other model. Nothing leaves the machine.
"""
import sys, os, re, json, time, fnmatch, hashlib, pathlib, subprocess, urllib.request, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
EXAM = ROOT / "data" / "auto" / "exam"
CACHE = pathlib.Path(os.environ.get("LOCAL_LLM_CACHE") or (pathlib.Path.home() / ".cache" / "pharmakon-models"))

MODELS = {   # file: the patterns of the weights' file, tried in order (the first that a repository has is taken)
    "qwen3-4b": {"repos": ["unsloth/Qwen3-4B-Instruct-2507-GGUF", "lmstudio-community/Qwen3-4B-Instruct-2507-GGUF", "bartowski/Qwen_Qwen3-4B-Instruct-2507-GGUF"],
                 "file": ["*Q4_K_M.gguf"], "licence": "Apache-2.0", "ctx": 12288},
    "phi4-mini": {"repos": ["unsloth/Phi-4-mini-instruct-GGUF", "bartowski/microsoft_Phi-4-mini-instruct-GGUF", "lmstudio-community/Phi-4-mini-instruct-GGUF"],
                  "file": ["*Q4_K_M.gguf"], "licence": "MIT", "ctx": 12288},
    # (a model of 30 billion weights of which 3 work for each word: as fast as a small one, nearer a large one; squeezed to about 3 bits a weight to fit the machine's 16 GB)
    "qwen3-30b-a3b": {"repos": ["unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF", "bartowski/Qwen_Qwen3-30B-A3B-Instruct-2507-GGUF", "lmstudio-community/Qwen3-30B-A3B-Instruct-2507-GGUF"],
                      "file": ["*UD-IQ3_XXS.gguf", "*IQ3_XXS.gguf", "*Q3_K_S.gguf"], "licence": "Apache-2.0", "ctx": 12288, "big": True},
    "gpt-oss-20b": {"repos": ["ggml-org/gpt-oss-20b-GGUF", "unsloth/gpt-oss-20b-GGUF"], "file": ["*mxfp4*.gguf"], "licence": "Apache-2.0", "ctx": 12288, "big": True},
}
PERMISSIVE = {"apache-2.0", "mit"}


def log(*a): print("local:", *a, flush=True)


def fetch(name):
    """The model's file on this machine: {"path", "repo", "file", "revision", "bytes", "sha256"}. Taken from the first repository that has a file of
    the pattern; GitHub's cache keeps the folder between runs, so it is downloaded once. Raises RuntimeError where no repository has it."""
    from huggingface_hub import HfApi, hf_hub_download
    m = MODELS[name]; api = HfApi(); why = []
    for repo in m["repos"]:
        try:
            info = api.model_info(repo, files_metadata=False)
            files = [s.rfilename for s in (info.siblings or [])]
            pick = next((sorted(f for f in files if fnmatch.fnmatch(f.lower(), pat.lower()) and "/" not in f) for pat in m["file"] if any(fnmatch.fnmatch(f.lower(), pat.lower()) and "/" not in f for f in files)), [])
            if not pick: why.append(f"{repo}: no file like {' or '.join(m['file'])}"); continue
            f = pick[0]; t = time.time()
            path = hf_hub_download(repo, f, revision=info.sha, cache_dir=str(CACHE))
            size = os.path.getsize(path); h = hashlib.sha256()
            with open(path, "rb") as fh:
                for chunk in iter(lambda: fh.read(1 << 24), b""): h.update(chunk)
            log(f"{name}: {repo}/{f} ({size / 1e9:.2f} GB) ready in {time.time() - t:.0f} s")
            return {"path": path, "repo": repo, "file": f, "revision": info.sha, "bytes": size, "sha256": h.hexdigest()}
        except Exception as e: why.append(f"{repo}: {type(e).__name__}: {str(e)[:120]}")
    raise RuntimeError(f"{name} could not be fetched: " + "; ".join(why))


def serve(name, port=8088, wait=600):
    """Start the model's server in the background (llama-cpp-python's, in OpenAI's form) and wait until it answers. Returns (process, what fetch() gave)."""
    m = MODELS[name]; got = fetch(name)
    cmd = [sys.executable, "-m", "llama_cpp.server", "--model", got["path"], "--model_alias", name, "--host", "127.0.0.1", "--port", str(port),
           "--n_ctx", str(m.get("ctx", 8192)), "--n_threads", str(os.cpu_count() or 4), "--n_batch", "512"]
    out = open(ROOT / "data" / "auto" / "exam" / f"_local-{name}-server.log", "w", encoding="utf-8") if os.environ.get("LOCAL_LLM_SERVER_LOG") else subprocess.DEVNULL
    p = subprocess.Popen(cmd, stdout=out, stderr=subprocess.STDOUT); t = time.time()
    while time.time() - t < wait:
        if p.poll() is not None: raise RuntimeError(f"{name}: the server stopped at once (exit {p.returncode})")
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/v1/models", timeout=5) as r:
                if r.status == 200: log(f"{name}: answering on port {port} after {time.time() - t:.0f} s"); return p, got
        except Exception: time.sleep(2)
    p.terminate(); raise RuntimeError(f"{name}: the server did not answer in {wait} s")


def ask(port, name, messages, max_tokens):
    body = {"model": name, "messages": messages, "max_tokens": max_tokens, "temperature": 0}
    t = time.time()
    with urllib.request.urlopen(urllib.request.Request(f"http://127.0.0.1:{port}/v1/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=900) as r:
        d = json.loads(r.read().decode())
    u = d.get("usage") or {}
    return time.time() - t, int(u.get("prompt_tokens") or 0), int(u.get("completion_tokens") or 0), ((d.get("choices") or [{}])[0].get("message") or {}).get("content") or ""


def passage(words=1800):
    """Text of our own to read (docs/METHODS.md: public, ours), about as long as what the lane gives a reader."""
    t = re.sub(r"\s+", " ", (ROOT / "docs" / "METHODS.md").read_text(encoding="utf-8"))
    return " ".join(t.split(" ")[:words])


def speed(port, name, no_think=False):
    """Seconds and tokens a second on this machine: reading (the prompt) and writing (the answer), on a prompt the size of a lane reader's."""
    sys_ = "You read a passage and answer in JSON only." + (" /no_think" if no_think else "")
    q = passage() + "\n\nQuestion: does the passage say who checks each sentence? Answer as JSON: {\"yes\": true or false, \"words\": \"the passage's own words, at most 15\"}"
    a = ask(port, name, [{"role": "system", "content": sys_}, {"role": "user", "content": q}], 1)            # (the prompt alone: reading)
    b = ask(port, name, [{"role": "system", "content": sys_ + " "}, {"role": "user", "content": q}], 200)    # (one space more: the prompt is read again, then up to 200 tokens written)
    read_s, read_tok = a[0], a[1]; write_tok = max(1, b[2]); write_s = max(0.01, b[0] - read_s)
    return {"prompt_tokens": read_tok, "read_seconds": round(read_s, 1), "read_per_second": round(read_tok / max(read_s, 0.01), 1),
            "wrote_tokens": write_tok, "write_seconds": round(write_s, 1), "write_per_second": round(write_tok / write_s, 1), "answer_starts": b[3][:160]}


def find(top=40):
    """The model hub's most downloaded GGUF models of the makers we trust, with their licence (for choosing the next to try; nothing is downloaded)."""
    from huggingface_hub import HfApi
    api = HfApi(); rows = []
    for author in ("Qwen", "ggml-org", "unsloth", "lmstudio-community", "bartowski", "microsoft", "ibm-granite", "HuggingFaceTB", "mistralai"):
        try:
            try: found = list(api.list_models(author=author, search="GGUF", sort="downloads", limit=25, cardData=True))
            except TypeError: found = list(api.list_models(author=author, search="GGUF", sort="downloads", limit=25))
            for mi in found:
                lic = str(((getattr(mi, "card_data", None) or {}) or {}).get("license") or "") if getattr(mi, "card_data", None) else ""
                rows.append({"id": mi.id, "downloads": int(getattr(mi, "downloads", 0) or 0), "licence": lic, "created": str(getattr(mi, "created_at", "") or "")[:10]})
        except Exception as e: rows.append({"author": author, "error": type(e).__name__ + ": " + str(e)[:100]})
    rows = sorted([r for r in rows if "id" in r], key=lambda r: -r["downloads"])[:top * 3]
    out = {"_note": "scripts/auto/local_llm.py find: the model hub's most downloaded GGUF models of trusted makers (names only; nothing downloaded).", "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "models": rows}
    json.dump(out, open(EXAM / "local-find.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1); log(f"{len(rows)} models listed in data/auto/exam/local-find.json")


def bench(request=None):
    """Each model of the request: fetched, served, timed, and (exam: true) the lane's own exam sat as its checker; then stopped. The results are kept as they come."""
    r = json.load(open(request, encoding="utf-8")) if request else {}
    names = [n for n in (r.get("models") or ["qwen3-4b", "phi4-mini", "qwen3-30b-a3b"]) if n in MODELS]
    until = time.time() + 60 * float(r.get("minutes") or 300)
    outf = EXAM / "local-bench.json"
    try: out = json.load(open(outf, encoding="utf-8"))
    except (OSError, ValueError): out = {"_note": "scripts/auto/local_llm.py bench: open models run on GitHub's own machine (4 cores, 16 GB, no graphics card): how fast they read and write there, and their exam as the lane's checker. Nothing leaves the machine.", "runs": []}
    run = {"at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "cores": os.cpu_count(), "models": {}}
    out["runs"] = (out.get("runs") or [])[-9:] + [run]
    def keep(): json.dump(out, open(outf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for i, n in enumerate(names):
        if time.time() > until - 120: run["models"][n] = {"skipped": "no time left in this run"}; keep(); continue
        m = MODELS[n]; port = 8088 + i; row = run["models"][n] = {"licence": m["licence"]}
        if m["licence"].lower() not in PERMISSIVE: row["skipped"] = "its licence does not allow any use"; keep(); continue
        try:
            p, got = serve(n, port); row.update({k: got[k] for k in ("repo", "file", "revision", "bytes", "sha256")})
        except Exception as e: row["failed"] = str(e)[:300]; keep(); continue
        try:
            row["speed"] = speed(port, n, m.get("no_think")); keep(); log(f"{n}: {row['speed']}")
            if r.get("exam"):
                import llm, exam_models as X
                os.environ["LOCAL_LLM_KEY"] = "local"; os.environ["LOCAL_LLM_PORTS"] = json.dumps({n: port})
                model = "local:" + n; f = EXAM / ("model-" + X.slug(model) + "-lane.json")
                t = time.time(); X.sit(model, 10 ** 6, cards=X.lane_cards(), file=f, until=until - 60)
                try: res = json.load(open(f, encoding="utf-8")); row["exam_lane"] = {k: res.get(k) for k in ("wrong_cards_seen", "wrong_caught", "good_cards_seen", "good_stopped", "no_clear_verdict")}
                except (OSError, ValueError): row["exam_lane"] = {"failed": "no result was written"}
                row["exam_minutes"] = round((time.time() - t) / 60, 1); keep(); log(f"{n}: exam {row['exam_lane']} in {row['exam_minutes']} minutes")
        except Exception as e: row["failed"] = (type(e).__name__ + ": " + str(e))[:300]
        finally:
            p.terminate()
            try: p.wait(timeout=30)
            except Exception: p.kill()
            keep()
    log("bench done:", json.dumps({n: {k: v for k, v in x.items() if k in ("speed", "exam_lane", "failed", "skipped")} for n, x in run["models"].items()})[:1500])


def selftest():
    assert all(m["licence"].lower() in PERMISSIVE for m in MODELS.values()), "only models whose licence allows any use"
    assert all(re.fullmatch(r"[a-z0-9.-]{3,40}", n) for n in MODELS) and all(m["repos"] and m["file"] and all(f.endswith(".gguf") for f in m["file"]) for m in MODELS.values())
    import llm
    os.environ["LOCAL_LLM_PORTS"] = json.dumps({"phi4-mini": 8089})
    assert llm.local_url("phi4-mini") == "http://127.0.0.1:8089/v1/chat/completions" and llm.local_url("qwen3-4b") == "http://127.0.0.1:8088/v1/chat/completions" and llm.local_url("x", "models").endswith("/v1/models")
    assert llm.service_of("local:qwen3-4b") == ("local", "qwen3-4b") and not llm.never_paid("local:qwen3-4b")
    os.environ.pop("LOCAL_LLM_KEY", None); assert not llm.has("local:qwen3-4b"); os.environ["LOCAL_LLM_KEY"] = "local"; assert llm.has("local:qwen3-4b")
    # a call goes to the model's own port, with the long time limit of a model that runs on the machine
    seen = {}
    class R:
        def __init__(s, d): s.d = d
        def __enter__(s): return s
        def __exit__(s, *a): return False
        def read(s): return json.dumps(s.d).encode()
    def op(req, timeout=None):
        seen.update(url=req.full_url, timeout=timeout, body=json.loads(req.data.decode())); return R({"choices": [{"message": {"content": "{\"ok\": true}"}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 10, "completion_tokens": 3}})
    import tempfile
    was = llm.LEDGER; llm.LEDGER = pathlib.Path(tempfile.mkdtemp()) / "usage.json"
    try: assert llm.chat("local:phi4-mini", [{"role": "user", "content": "answer in JSON"}], 50, opener=op) == "{\"ok\": true}"
    finally: llm.LEDGER = was
    assert seen["url"] == "http://127.0.0.1:8089/v1/chat/completions" and seen["timeout"] == 900 and seen["body"]["model"] == "phi4-mini" and seen["body"]["response_format"] == {"type": "json_object"}, seen
    import lane
    assert lane.base("local:qwen3-4b") == "qwen3-4b"
    print("local_llm selftest: ok (only models whose licence allows any use; a local model is asked on its own port with a long time limit, as llm.py asks every service; no key, no call)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a: selftest()
    elif a[:1] == ["serve"] and a[1:2] and a[1] in MODELS:
        p, got = serve(a[1], int(a[a.index("--port") + 1]) if "--port" in a else 8088); print(json.dumps({"pid": p.pid, **{k: got[k] for k in ("repo", "file", "bytes")}}))
    elif a[:1] == ["bench"]: bench(a[a.index("--request") + 1] if "--request" in a else None)
    elif a[:1] == ["find"]: find()
    else: sys.exit(__doc__)
