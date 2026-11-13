"""Build the public website (pharmakon.world) from the built page in site/dist.

usage: python3 -I site/build_public.py

site/dist/index.html is written for the claude.ai viewer, which wraps it in a document and loads its fonts from Google.
The public site needs a whole document of its own: this script adds the document head (title, description, link
preview, icons, a content security policy), serves the fonts from the site itself, and writes the files a static
host needs (robots.txt, sitemap.xml, 404.html, _headers). Output: site/public/, ready to publish as it is.
"""
import json
import pathlib
import re
import shutil
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
DIST, ASSETS, OUT = HERE / "dist", HERE / "public-assets", HERE / "public"
DOMAIN = "pharmakon.world"
URL = "https://" + DOMAIN + "/"
TITLE = "Pharmakon: what the research says about drugs"
DESC = ("Plain answers about drugs, from the research: what each drug does, what can go wrong, how to stay safer, "
        "and how sure the evidence is. Free, with every source cited.")
ACCENT, INK, BG = "#0a6a5b", "#101813", "#f2f5f1"
LOGO = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
        '<path fill="%s" d="M13.2 27.8a6.8 6.8 0 0 1-9.6-9.6L10 11.8l9.6 9.6z"/>'
        '<path fill="#ffffff" stroke="%s" stroke-width="2" d="M10 11.8l6.4-6.4a6.8 6.8 0 0 1 9.6 9.6l-6.4 6.4z"/></svg>') % (ACCENT, INK)

page = (DIST / "index.html").read_text(encoding="utf-8")
# the claude.ai viewer's own tags and the Google Fonts links go; the fonts come from this site
page = page.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
page = re.sub(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\n?', "", page)
page = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/[^"]+">\n?', "", page)
assert "fonts.googleapis" not in page and "fonts.gstatic" not in page, "a Google Fonts reference is left"
page = re.sub(r"^<title>[^<]*</title>\n?", "", page)
i = page.index("</style>") + len("</style>")
style, body = page[:i], page[i:]
style = style.replace("<style>", "<style>\n" + (ASSETS / "fonts.css").read_text(encoding="utf-8"), 1)

csp = ("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
       "font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests")
head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="theme-color" content="{ACCENT}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pharmakon">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{URL}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Pharmakon: what the research says about drugs, and how sure it is.">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
"""
doc = head + style + "\n</head>\n<body>" + body.rstrip() + "\n</body>\n</html>\n"

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
(OUT / "index.html").write_text(doc, encoding="utf-8")
for d in ("data", "img"):
    shutil.copytree(DIST / d, OUT / d)
shutil.copytree(ASSETS / "fonts", OUT / "fonts")
(OUT / "favicon.svg").write_text(LOGO, encoding="utf-8")
# security headers, read by Cloudflare Pages and Netlify (GitHub Pages ignores the file; the page carries its own policy)
(OUT / "_headers").write_text("/*\n"
    "  Strict-Transport-Security: max-age=31536000\n"
    "  X-Content-Type-Options: nosniff\n"
    "  X-Frame-Options: DENY\n"
    "  Referrer-Policy: strict-origin-when-cross-origin\n"
    "  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()\n"
    "  Content-Security-Policy: " + csp.replace("upgrade-insecure-requests", "frame-ancestors 'none'; upgrade-insecure-requests") + "\n", encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {URL}sitemap.xml\n", encoding="utf-8")
ver = json.loads((HERE.parent / "data/site/version.json").read_text(encoding="utf-8"))
build_date = re.search(r'<span id="build-date">([^<]+)</span>', doc)
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                 f"  <url><loc>{URL}</loc></url>\n</urlset>\n", encoding="utf-8")
(OUT / "404.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found · Pharmakon</title><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>{(ASSETS / "fonts.css").read_text(encoding="utf-8")}
body {{ margin: 0; min-height: 100vh; display: grid; place-items: center; background: {BG}; color: {INK}; font-family: "Atkinson Hyperlegible", Verdana, sans-serif; }}
main {{ max-width: 30rem; padding: 24px 16px; }} h1 {{ font-family: Overpass, Arial, sans-serif; font-weight: 800; }}
a {{ color: {ACCENT}; }} svg {{ width: 56px; height: 56px; }}</style></head>
<body><main>{LOGO}<h1>This page doesn't exist</h1><p>The address may be mistyped, or the page may have moved.</p>
<p><a href="/">Go to Pharmakon's start page</a></p></main></body></html>
""", encoding="utf-8")

# the link preview picture and the icons, drawn from the site's own logo and fonts
import base64
font_data = lambda f: "data:font/woff2;base64," + base64.b64encode((ASSETS / "fonts" / f).read_bytes()).decode()
og = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Overpass; font-weight: 900; src: url({font_data('overpass-latin-900-normal.woff2')}); }}
@font-face {{ font-family: Atk; font-weight: 400; src: url({font_data('atkinson-hyperlegible-latin-400-normal.woff2')}); }}
@font-face {{ font-family: Mono; font-weight: 600; src: url({font_data('overpass-mono-latin-600-normal.woff2')}); }}
html, body {{ margin: 0; }}
.card {{ width: 1200px; height: 630px; box-sizing: border-box; padding: 76px 84px; background: {BG}; color: {INK}; position: relative; overflow: hidden; }}
.card::after {{ content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 14px; background: {ACCENT}; }}
.logo {{ width: 112px; height: 112px; }}
h1 {{ margin: 26px 0 0; font: 900 118px/1 Overpass, sans-serif; letter-spacing: -2px; }}
p {{ margin: 26px 0 0; max-width: 1000px; font: 400 44px/1.25 Atk, sans-serif; text-wrap: balance; }}
.foot {{ position: absolute; left: 84px; right: 84px; bottom: 62px; display: flex; align-items: flex-end; justify-content: space-between; }}
.bars {{ display: flex; align-items: flex-end; gap: 9px; }}
.bars i {{ display: block; width: 22px; border-radius: 4px; background: {ACCENT}; }}
.url {{ font: 600 34px/1 Mono, monospace; color: {ACCENT}; }}
</style></head><body><div class="card">{LOGO.replace('<svg ', '<svg class="logo" ')}
<h1>Pharmakon</h1><p>What the research says about drugs, and how sure it is.</p>
<div class="foot"><div class="bars"><i style="height:22px"></i><i style="height:36px"></i><i style="height:50px"></i><i style="height:64px"></i></div><span class="url">{DOMAIN}</span></div>
</div></body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content(og)
    pg.evaluate("() => document.fonts.ready")
    pg.wait_for_timeout(300)
    pg.screenshot(path=str(OUT / "og.png"))
    for size, name in ((32, "favicon-32.png"), (180, "apple-touch-icon.png")):
        pad = 0 if size == 32 else 22
        bg = "transparent" if size == 32 else BG
        pg.set_viewport_size({"width": size, "height": size})
        pg.set_content(f'<html><body style="margin:0;background:{bg}"><div style="width:{size}px;height:{size}px;box-sizing:border-box;padding:{pad}px">'
                       + LOGO.replace("<svg ", f'<svg width="{size - 2 * pad}" height="{size - 2 * pad}" ') + "</div></body></html>")
        pg.screenshot(path=str(OUT / name), omit_background=(size == 32))
    b.close()

# one zip with the site at its root, for a drag-and-drop upload
zpath = HERE / "pharmakon-site.zip"
if zpath.exists():
    zpath.unlink()
shutil.make_archive(str(zpath.with_suffix("")), "zip", root_dir=OUT)
n = sum(1 for _ in OUT.rglob("*") if _.is_file())
size = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
print(f"public site: {n} files, {size / 1e6:.1f} MB in {OUT} (version {ver['site']}); zip {zpath.stat().st_size / 1e6:.1f} MB")
