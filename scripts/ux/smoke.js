// Smoke test of the built public site (site/public) in a real browser at 390 x 844 and 1280 x 800: the main views render
// (site 2.3: each drug has one page, and the research page's old address opens it), a section opens from a drug page's
// menu and an answer opens in it, the quiz answers a tap, and no step shows horizontal scroll or a console or page error.
// Rewritten on 13 November 2026 after the workspace reset (the first smoke test lived in a temporary folder and was lost).
// Usage: node scripts/ux/smoke.js [--port N]   (build first: node site/build.js && python3 -I site/build_public.py)
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const ROOT = path.resolve(__dirname, "..", "..", "site", "public");
const PORT = +((process.argv.indexOf("--port") > 0 && process.argv[process.argv.indexOf("--port") + 1]) || 0);
const TYPES = { ".html": "text/html; charset=utf-8", ".json": "application/json", ".webp": "image/webp", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".css": "text/css" };
const results = [], errors = [];
const ok = (name, pass, detail) => { results.push(!!pass); console.log((pass ? "PASS " : "FAIL ") + name + (detail ? "  (" + detail + ")" : "")); };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]); if (p.endsWith("/")) p += "index.html";
  if (p === "/api/ask") { res.writeHead(200, { "Content-Type": "application/json" }); res.end('{"ok":false}'); return; }   // as the site's worker answers before its store is set up
  const f = path.join(ROOT, path.normalize(p)); if (!f.startsWith(ROOT)) { res.writeHead(403); res.end(); return; }
  fs.readFile(f, (err, buf) => { if (err) { res.writeHead(404); res.end(); return; } res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" }); res.end(buf); });
});
(async () => {
  if (!fs.existsSync(path.join(ROOT, "index.html"))) { console.error("No site/public/index.html: build first."); process.exit(2); }
  await new Promise(r => server.listen(PORT, "127.0.0.1", r));
  const BASE = "http://127.0.0.1:" + server.address().port + "/#";
  const browser = await chromium.launch({ args: ["--no-proxy-server"] });
  for (const w of [390, 1280]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: w < 700 ? 844 : 800 } });
    const p = await ctx.newPage();
    p.on("pageerror", e => errors.push(w + " page error: " + String(e).slice(0, 200)));
    p.on("console", m => { if (m.type() === "error") errors.push(w + " console error: " + m.text().slice(0, 200)); });
    const hs = async step => { const [sw, cw] = await p.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]); if (sw > cw) errors.push(w + " horizontal scroll at " + step + ": " + sw + " > " + cw); };
    await p.goto(BASE + "home"); await p.waitForTimeout(1200); await hs("home");
    const views = [["home", "view-home"], ["quiz", "view-quiz"], ["s-cannabis", "view-drug"], ["s-lsd", "view-drug"], ["s-mdma", "view-drug"], ["s-heroin", "view-drug"],
      ["s-fentanyl-and-analogues", "view-drug"], ["facts", "view-facts"], ["checking/kits", "view-checking"], ["interactions", "view-interactions"], ["emergency", "view-emergency"],
      ["s-cannabis/evidence", "view-drug"], ["s-cannabis/part-d-help", "view-drug"], ["s-mdma/part-d-kits", "view-drug"], ["howto", "view-howto"], ["a/lsd/cl_lsd_chromosomes", "view-shared"]];
    const wrong = [];
    for (const [h, v] of views) { await p.evaluate(x => { location.hash = x; }, "#" + h); await p.waitForTimeout(450); await hs(h);
      const a = await p.evaluate(() => (document.querySelector(".view.active") || {}).id); if (a !== v) wrong.push(h + " -> " + a); }
    ok(w + ": main views render", !wrong.length, wrong.join("; "));
    // a drug page: nothing but its menu at first; a row opens its section alone, and an answer opens in it
    await p.evaluate(() => { location.hash = "#s-lsd"; }); await p.waitForTimeout(600);
    const menu = await p.evaluate(() => ({ rows: document.querySelectorAll("#secmenu .sm-b").length, shown: [...document.querySelectorAll("#drug2 .secs > .sec")].filter(x => !x.hidden).length }));
    await p.click("#secmenu .sm-b"); await p.waitForTimeout(700); await hs("section open");
    const sec = await p.evaluate(() => [...document.querySelectorAll("#drug2 .secs > .sec")].filter(x => !x.hidden).map(x => x.id));
    ok(w + ": a drug page shows its menu of sections, and a row opens its section alone", menu.rows > 4 && menu.shown === 0 && sec.length === 1, menu.rows + " rows; open: " + sec.join());
    await p.click("#drug2 .secs > .sec:not([hidden]) details.ask > summary"); await p.waitForTimeout(700);
    const opened = await p.evaluate(() => { const d = document.querySelector("#drug2 .secs > .sec:not([hidden]) details.ask"); return !!d && d.open && d.getBoundingClientRect().top >= 0; });
    await hs("answer open"); ok(w + ": an answer opens", opened === true, String(opened));
    // the quiz answers a tap
    await p.evaluate(() => { location.hash = "#quiz"; }); await p.waitForTimeout(700);
    const before = await p.evaluate(() => document.querySelector("#view-quiz").innerText.length);
    const btn = await p.$("#quizpage .qz2-o:not([disabled])");   // (site 2.4: the page's first buttons choose a drug)
    if (btn) { await btn.click(); await p.waitForTimeout(500); }
    const after = await p.evaluate(() => document.querySelector("#view-quiz").innerText.length);
    await hs("quiz"); ok(w + ": the quiz answers a tap", !!btn && after !== before, before + " -> " + after);
    await ctx.close();
  }
  ok("no horizontal scroll, no console or page errors", !errors.length, errors.slice(0, 5).join(" | "));
  await browser.close(); server.close();
  const failed = results.filter(x => !x).length;
  console.log("\n" + (results.length - failed) + " of " + results.length + " checks passed");
  process.exit(failed ? 1 : 0);
})();
