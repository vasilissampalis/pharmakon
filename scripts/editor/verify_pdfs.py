"""verify_pdfs.py REQUESTED.json STAGING.tsv UPLOAD_ROOT: check that each requested PDF the senior author saved is the right
paper, before any reader opens it. For each entry of REQUESTED (k, folder, name, apa with its DOI): finds the staged file
(UPLOAD_ROOT/PDFs/<folder>/<name>, also with a doubled ".pdf.pdf", or in any folder), reads the text of its first two
pages, and compares it with the paper's Crossref record in STAGING (title words and first author's surname). Also flags
two files with the same SHA-256 (the same PDF saved twice under two names). Prints one line per paper:
ok / check (weak match: look at it) / missing / duplicate."""
import json, sys, os, re, glob, hashlib, subprocess
req, tsv, root = sys.argv[1], sys.argv[2], sys.argv[3]
R = json.load(open(req, encoding="utf-8"))
CR = {}
for line in open(tsv, encoding="utf-8"):
    if "\t" not in line: continue
    sha, js = line.rstrip("\n").split("\t", 1)
    try: rec = json.loads(js)
    except Exception: continue
    CR[rec["DOI"].lower()] = rec
words = lambda s: [w for w in re.findall(r"[a-z]{4,}", (s or "").lower()) if w not in {"with", "from", "that", "this", "their", "after", "into", "among", "about", "versus", "study", "using"}]
allpdf = glob.glob(os.path.join(root, "PDFs", "**", "*.pdf"), recursive=True)
seen, out = {}, []
for x in R:
    doi = re.search(r"doi\.org/(\S+)", x.get("apa", "") or x.get("url", ""))
    doi = doi.group(1).rstrip(".").lower() if doi else None
    rec = CR.get(doi) if doi else None
    cands = [os.path.join(root, "PDFs", x["folder"], x["name"]), os.path.join(root, "PDFs", x["folder"], x["name"] + ".pdf")]
    cands += [p for p in allpdf if os.path.basename(p) in (x["name"], x["name"] + ".pdf")]
    path = next((p for p in cands if os.path.exists(p)), None)
    if not path: out.append(("missing", x["k"], "", "")); continue
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    dup = seen.get(h); seen[h] = x["k"]
    try: txt = subprocess.run(["pdftotext", "-l", "2", path, "-"], capture_output=True, text=True, timeout=60).stdout
    except Exception: txt = ""
    tw = set(words(txt)); title = (rec or {}).get("title") or ""
    want = words(title); hit = sum(w in tw for w in want) / max(1, len(want))
    au = ((rec or {}).get("au") or [[None]])[0][0] or ""
    au_ok = bool(au) and au.lower().split()[-1] in txt.lower()
    verdict = "duplicate of " + dup if dup else ("ok" if hit >= 0.7 and au_ok else "check")
    out.append((verdict, x["k"], f"title words {hit:.0%}, first author {'found' if au_ok else 'not found'}" + ("" if rec else " (no Crossref record)") + ("" if txt.strip() else " (no text layer)"), os.path.relpath(path, root)))
for v, k, note, p in out: print(f"{v:<22} {k:<55} {note}  {p}")
print("ok:", sum(v == "ok" for v, *_ in out), "check:", sum(v == "check" for v, *_ in out), "missing:", sum(v == "missing" for v, *_ in out), "duplicates:", sum(v.startswith("duplicate") for v, *_ in out))
