#!/usr/bin/env python3
"""Make the web copies of the drug photos listed in data/site/photos.json.

For each photo: open the original from the senior author's Images folder, turn it upright,
crop it if the record says so, and write two WebP copies without any metadata (no EXIF, so no
camera or GPS data): <id>-m.webp (up to 800 px on the long side, for the drug page) and
<id>-t.webp (up to 400 px, for tiles and galleries). Writes site/photos/manifest.json with each
copy's width, height and size, which the build embeds so the page can reserve the space.

Usage: python3 scripts/build_photos.py [IMAGES_DIR]
"""
import json, os, sys
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/uploads/DrugEncyclopedia/Images"
OUT = os.path.join(ROOT, "site", "photos")
SIZES = {"m": (800, 74), "t": (400, 70)}  # long side in px, WebP quality

def main():
    doc = json.load(open(os.path.join(ROOT, "data", "site", "photos.json")))
    os.makedirs(OUT, exist_ok=True)
    manifest, missing = {}, []
    for p in doc["photos"]:
        src = os.path.join(SRC, p["file"])
        if not os.path.exists(src):
            missing.append(p["file"]); continue
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        if p.get("crop"):
            x0, y0, x1, y1 = p["crop"]; W, H = im.size
            im = im.crop((round(x0 * W), round(y0 * H), round(x1 * W), round(y1 * H)))
        manifest[p["id"]] = {}
        for k, (side, q) in SIZES.items():
            c = im.copy(); c.thumbnail((side, side), Image.LANCZOS)
            f = os.path.join(OUT, p["id"] + "-" + k + ".webp")
            c.save(f, "WEBP", quality=q, method=6)  # no exif= argument: nothing from the original's metadata is kept
            manifest[p["id"]][k] = [c.size[0], c.size[1], os.path.getsize(f)]
    # web copies of photos no longer listed are removed, so they are not published
    keep = {p["id"] + "-" + k + ".webp" for p in doc["photos"] for k in SIZES}
    gone = [f for f in os.listdir(OUT) if f.endswith(".webp") and f not in keep]
    for f in gone: os.remove(os.path.join(OUT, f))
    if gone: print("removed old web copies:", ", ".join(sorted(gone)))
    json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
    total = sum(v[k][2] for v in manifest.values() for k in v)
    print(len(manifest), "photos,", round(total / 1024), "KB in all;", "missing:", missing or "none")
    if missing: sys.exit(1)

if __name__ == "__main__":
    main()
