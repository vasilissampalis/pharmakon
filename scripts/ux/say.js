// say.js: what the page says to a question, as a reader would get it (the editor's tool; site 2.9, 17 November 2026).
// The senior author: "we have to include our site responding perfectly to every circumstance this is what smartness is about".
// Usage: node scripts/ux/say.js "do gay people" "can i die from" ...      (build first: node site/build.js && python3 -I site/build_public.py)
//        node scripts/ux/say.js --file questions.txt [--drug cannabis]      (one question a line; --drug: asked on that drug's page)
// For each question: the line under it (note), why it is not finished (unf), the routes, how many best matches and related answers, a
// word read as a drug's name, an unknown word, and the words a screen reader hears.
const http = require("http"), fs = require("fs"), path = require("path");
const { chromium } = require("playwright");
const ROOT = path.resolve(__dirname, "..", "..", "site", "public");
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".mjs": "text/javascript", ".wasm": "application/wasm", ".json": "application/json", ".css": "text/css", ".txt": "text/plain; charset=utf-8" };
const a = process.argv.slice(2), arg = k => { const i = a.indexOf(k); return i >= 0 ? a[i + 1] : null; };
const drug = arg("--drug"), file = arg("--file");
const qs = (file ? fs.readFileSync(file, "utf8").split("\n").map(s => s.trim()).filter(Boolean) : a.filter((x, i) => !x.startsWith("--") && a[i - 1] !== "--drug" && a[i - 1] !== "--file"));
if (!qs.length) { console.error("say.js: give questions, or --file FILE"); process.exit(2); }
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]); if (p.endsWith("/")) p += "index.html";
  if (p === "/api/ask" || p === "/api/want") { res.writeHead(200, { "Content-Type": "application/json" }); res.end('{"ok":false}'); return; }
  const f = path.join(ROOT, path.normalize(p)); if (!f.startsWith(ROOT)) { res.writeHead(403); res.end(); return; }
  fs.readFile(f, (err, buf) => { if (err) { res.writeHead(404); res.end(); return; } res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" }); res.end(buf); });
});
(async () => {
  await new Promise(ok => server.listen(0, "127.0.0.1", ok));
  const browser = await chromium.launch({ args: ["--no-proxy-server"] }), p = await browser.newPage();
  await p.goto("http://127.0.0.1:" + server.address().port + "/#home"); await p.waitForTimeout(400);
  if (!await p.evaluate(() => pkInsight.load())) { console.error("Insight did not load"); process.exit(1); }
  const out = await p.evaluate(async ({ qs, drug }) => { const rows = [];
    for (const q of qs) { const r = await pkInsight.rank(q, drug ? { drug } : {});
      rows.push({ q, note: r.note || "-", unf: r.unf || "", routes: r.routes.map(x => x.kind).join("+"), best: r.best.length, related: r.related.length, read: (r.read || []).map(x => x.join(">")).join(","), stranger: r.stranger || "", says: pkInsight.say ? pkInsight.say(q, drug ? { drug } : {}) : "" }); }
    return Promise.all(rows.map(async x => Object.assign(x, { says: await x.says }))); }, { qs, drug });
  for (const r of out) console.log([r.q.padEnd(44), ("note " + r.note + (r.unf ? ":" + r.unf : "")).padEnd(22), ("routes " + (r.routes || "-")).padEnd(16), "best " + r.best, "related " + r.related, r.read ? "read " + r.read : "", r.stranger ? "unknown " + r.stranger : "", r.says ? "| " + r.says : ""].filter(Boolean).join("  "));
  await browser.close(); server.close();
})().catch(e => { console.error(e); server.close(); process.exit(1); });
