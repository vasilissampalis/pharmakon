"""make_preview.py BUILD_DIR PREVIEW_DIR: refresh the redesign preview's files from a build (site/dist of the redesign
worktree). The page is the built index.html with the title "Pharmakon preview"; photos (img/) and study-card files (data/) are
copied only when changed. Prints the changed files, to pass in the Artifact publish's `files` (unchanged ones are kept there).
The preview artifact: https://claude.ai/artifact/Pps2qG53aCyQrv9ZDGiDTi (publish PREVIEW_DIR/index.html to that url)."""
import sys, os, hashlib, shutil, json
D, P = sys.argv[1], sys.argv[2]
h = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
page = open(os.path.join(D, "index.html"), encoding="utf-8").read()
if page.count("<title>Pharmakon</title>") != 1: sys.exit("the built page's title is not the expected one")
os.makedirs(P, exist_ok=True)
open(os.path.join(P, "index.html"), "w", encoding="utf-8").write(page.replace("<title>Pharmakon</title>", "<title>Pharmakon preview</title>", 1))
changed = []
for sub in ("img", "data"):
    os.makedirs(os.path.join(P, sub), exist_ok=True)
    for f in sorted(os.listdir(os.path.join(D, sub))):
        src, dst = os.path.join(D, sub, f), os.path.join(P, sub, f)
        if not os.path.exists(dst) or h(src) != h(dst): shutil.copyfile(src, dst); changed.append(sub + "/" + f)
gone = [sub + "/" + f for sub in ("img", "data") for f in os.listdir(os.path.join(P, sub)) if not os.path.exists(os.path.join(D, sub, f))]
print(json.dumps({"page_mb": round(len(page.encode()) / 1e6, 2), "changed": changed, "no_longer_built": gone}, indent=1))
