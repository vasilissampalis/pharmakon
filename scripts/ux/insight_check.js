// Insight (site 2.2.0, 14 November 2026), checked in a real browser at 390 x 844 and 1280 x 800, with the site served as
// Cloudflare Pages serves it (the file types, revalidated caching, and the security policy of site/public/_headers): every
// published file is under 25 MiB; the start page fetches none of Insight's files; the cursor in the search box fetches them,
// from the site itself only, with no cache-busting; three real questions get their checked answer among the closest checked
// answers at the top of the results, under the quiet line; nothing typed leaves the page (no request carries it) or is
// stored; an answer with a myth-or-fact statement asks the guess first, then shows the reveal and the next questions, its
// evidence comes back to it, and after four answers in a row comes the calm end; a safety answer opens at once with the
// emergency line; a question with no close checked answer says so, and Ask us carries the words typed; a second visit
// downloads nothing again; on a connection that saves data nothing is fetched until the reader taps the line that offers it;
// no "AI" words; no console errors; no sideways scroll; the reveal's one movement stays still for readers who prefer less
// motion. Prints the time each search takes (median and slowest).
// Usage: node scripts/ux/insight_check.js [--shots DIR] [--port N]   (build first: node site/build.js && python3 -I site/build_public.py)
const http = require("http"), fs = require("fs"), path = require("path"), os = require("os");
const { chromium } = require("playwright");
const ROOT = path.resolve(__dirname, "..", "..", "site", "public");
const arg = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const SHOTS = arg("--shots"), PORT = +(arg("--port") || 0);
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".mjs": "text/javascript", ".wasm": "application/wasm", ".json": "application/json", ".css": "text/css",
  ".webp": "image/webp", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".txt": "text/plain; charset=utf-8", ".xml": "application/xml" };
// three questions the site answers, as people type them, and the answer each should find
const REAL = [["does ecstasy damage your brain permanently", "cl_mdma_neurotoxicity_contested"], ["can you fail a drug test from secondhand weed smoke", "cl_can_secondhand_test"],
  ["how long does ketamine stay in your blood", "cl_ket_halflife_norketamine"]];
const SAFETY = ["what does an opioid overdose look like", "cl_opi_overdose_recognition"];
const NONE = "what is the capital of mongolia";
const AI_WORDS = /\b(AI|A\.I\.|artificial intelligence|machine learning|neural|algorithm|language model|chatbot|GPT)\b/i;
const results = [], errors = [], times = [];
const ok = (name, pass, detail) => { results.push(!!pass); console.log((pass ? "PASS " : "FAIL ") + name + (detail ? "  (" + detail + ")" : "")); };
if (!fs.existsSync(path.join(ROOT, "index.html"))) { console.error("No site/public/index.html: build first."); process.exit(2); }
const csp = (fs.readFileSync(path.join(ROOT, "_headers"), "utf8").match(/Content-Security-Policy: (.*)/) || [])[1];
// as Cloudflare Pages does: an ETag, and "revalidate before use", so a file already in the browser's cache comes back as 304
const served = [];
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]); if (p.endsWith("/")) p += "index.html";
  const f = path.join(ROOT, path.normalize(p)); if (!f.startsWith(ROOT)) { res.writeHead(403); res.end(); return; }
  fs.stat(f, (err, st) => { if (err || !st.isFile()) { res.writeHead(404); res.end("not found"); return; }
    const tag = '"' + st.size.toString(36) + "-" + Math.floor(st.mtimeMs).toString(36) + '"';
    const head = Object.assign({ "Content-Type": TYPES[path.extname(f)] || "application/octet-stream", "X-Content-Type-Options": "nosniff", ETag: tag, "Cache-Control": "public, max-age=0, must-revalidate" }, csp ? { "Content-Security-Policy": csp } : {});
    if (req.headers["if-none-match"] === tag) { served.push({ p, status: 304, bytes: 0 }); res.writeHead(304, head); res.end(); return; }
    fs.readFile(f, (e2, buf) => { if (e2) { res.writeHead(500); res.end(); return; } served.push({ p, status: 200, bytes: buf.length }); res.writeHead(200, head); res.end(buf); }); });
});
// every file the site publishes stays under Cloudflare Pages' limit of 25 MiB a file
{ const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [[path.join(d, e.name), fs.statSync(path.join(d, e.name)).size]]);
  const files = walk(ROOT).sort((a, b) => b[1] - a[1]);
  ok("every published file is under 25 MiB", files[0][1] < 25 * 1024 * 1024, files.slice(0, 2).map(([f, n]) => path.relative(ROOT, f) + " " + (n / 1048576).toFixed(1) + " MiB").join(", ")); }
(async () => {
  await new Promise(r => server.listen(PORT, "127.0.0.1", r));
  const ORIGIN = "http://127.0.0.1:" + server.address().port, BASE = ORIGIN + "/#";
  if (SHOTS) fs.mkdirSync(SHOTS, { recursive: true });
  const browser = await chromium.launch({ args: ["--no-proxy-server"] });
  for (const w of [390, 1280]) {
    const H = w < 700 ? 844 : 800;
    const ctx = await browser.newContext({ viewport: { width: w, height: H }, deviceScaleFactor: 1, hasTouch: w < 700, isMobile: w < 700 }), p = await ctx.newPage();
    p.on("pageerror", e => errors.push(w + " page error: " + String(e).slice(0, 200)));
    p.on("console", m => { if (m.type() === "error") errors.push(w + " console error: " + m.text().slice(0, 200)); });
    const reqs = [], sent = []; p.on("request", r => { reqs.push(r.url()); sent.push(r.url() + " " + (r.postData() || "")); });
    const typed = [];   // every question typed, to make sure none leaves the page
    const shot = async name => { const [sw, cw] = await p.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]); if (sw > cw) errors.push(w + " horizontal scroll at " + name);
      if (SHOTS) await p.screenshot({ path: path.join(SHOTS, w + "-insight-" + name + ".png") }); };
    const ins = u => /\/data\/insight\.json|\/insight\//.test(u);
    // ask a question; wait for Insight's block for exactly these words
    const ask = async q => {
      typed.push(q); await p.fill("#search", q);
      await p.waitForFunction(q => { const b = document.querySelector("#search-results > .sr-fit, #search-results > .sr-fit-none"); return b && b.dataset.q === q; }, q, { timeout: 20000 }).catch(() => {});
      return p.evaluate(() => { const box = document.getElementById("search-results"), f = box.querySelector(".sr-fit");
        return { fit: f ? [...f.querySelectorAll("a[data-insight]")].map(a => ({ id: a.dataset.insight, q: a.querySelector(".t").textContent, a: a.querySelector(".a").textContent })) : [], none: (box.querySelector(".sr-fit-none") || {}).textContent || "",
          note: (box.querySelector(".sr-note") || {}).textContent || "", head: f ? f.querySelector(".sr-fit-h").textContent : "", first: box.firstElementChild && box.firstElementChild.className, open: !box.hidden }; });
    };
    const uiText = () => p.evaluate(() => [...document.querySelectorAll(".sr-note, .sr-fit-h, .sr-fit-none, .ins-k, .ins-skip, .ins-end, .ins-next .rn-k, .ins-eye")].map(e => e.textContent).join(" | "));
    let ui = "";

    // the start page: nothing of Insight's fetched
    await p.goto(BASE + "home"); await p.waitForTimeout(2500);
    ok(w + ": the start page fetches none of Insight's files", !reqs.some(ins), reqs.filter(ins).join(", ") || "none");
    // the cursor in the search box: the files come, from the site itself, and the quiet line shows once ready
    const t0 = Date.now(); await p.focus("#search");
    const ready = await p.waitForFunction(() => window.pkInsight && pkInsight.state() === "ready", null, { timeout: 120000 }).then(() => true, () => false);
    const loadMs = Date.now() - t0; await p.waitForTimeout(300);
    const got = reqs.filter(ins).map(u => u.replace(/^.*\//, "")), outside = reqs.filter(u => !u.startsWith(ORIGIN) && !u.startsWith("data:") && !u.startsWith("blob:"));
    const need = ["insight.json", "ort.wasm.min.js", "ort-wasm-simd-threaded.mjs", "ort-wasm-simd-threaded.wasm", "all-MiniLM-L6-v2-q8.onnx", "vocab.txt"];
    ok(w + ": the cursor in the search box fetches Insight's files from the site itself, with no cache-busting, and it gets ready", ready && need.every(f => got.includes(f)) && !outside.length && !got.some(f => /jsep|webgpu/i.test(f)) && !reqs.filter(ins).some(u => u.includes("?")),
      "ready in " + loadMs + " ms; fetched " + got.join(", ") + (outside.length ? "; OUTSIDE: " + outside.join(", ") : ""));
    const sug = await p.evaluate(() => { const b = document.getElementById("search-results"); return { note: (b.querySelector(":scope > .sr-note") || {}).textContent || "", sug: b.querySelectorAll("a.sr-sug").length }; });
    ok(w + ": once ready, one quiet line under the box says it runs on the device", /^Runs on your (phone|computer)\. Nothing you type leaves it\.$/.test(sug.note.trim()) && sug.sug > 0, JSON.stringify(sug));
    await shot("ready");
    // three real questions: the answer that fits at the top
    for (const [q, want] of REAL) {
      const r = await ask(q); ui += " " + await uiText();
      const at = r.fit.findIndex(x => x.id === want);
      ok(w + ": “" + q + "” finds its answer among the closest checked answers", r.open && at >= 0 && r.first === "sr-note" && r.head === "Closest checked answers", (at >= 0 ? "#" + (at + 1) + " " : "missing; got ") + r.fit.map(x => x.id + " (" + x.q + ")").join("; "));
    }
    await shot("answers-that-fit");
    // the first: a guess, then the reveal, then the next questions
    await ask(REAL[0][0]);
    await p.click('#search-results a[data-insight="' + REAL[0][1] + '"]'); await p.waitForTimeout(300);
    const g = await p.evaluate(() => { const s = document.querySelector("#evsheet.open .ins"); return s ? { guess: !!s.querySelector(".ins-guess"), opts: [...s.querySelectorAll("[data-ins-guess]")].map(b => b.textContent).join(","), skip: !!s.querySelector("[data-ins-skip]"), q: (s.querySelector(".ins-q") || {}).textContent || "", title: document.getElementById("ev-title").textContent, searchOpen: !document.getElementById("search-results").hidden } : null; });
    ui += " " + await uiText(); await shot("guess");
    ok(w + ": an answer with a myth-or-fact statement asks the guess first (Myth or Fact, or skip)", g && g.guess && g.opts === "Myth,Fact" && g.skip && g.q.length > 10 && !g.searchOpen, JSON.stringify(g));
    await p.click("#evsheet [data-ins-guess=fact]"); await p.waitForTimeout(400);
    const rv = await p.evaluate(() => { const s = document.querySelector("#evsheet.open .ins"); if (!s) return null; const v = s.querySelector(".ins-verdict");
      return { verdict: v && v.querySelector(".mf-v").textContent.trim(), said: !!(v && v.querySelector(".mf-said")), why: !!(v && v.querySelector(".qz2-why")), short: !!s.querySelector(".ins-ans .ask-short"), bars: !!s.querySelector(".ins-ans .ask-foot .meter, .ins-ans .ask-foot [class*=meter]"),
        ev: !!s.querySelector('.ins-ans a.ask-ev[href^="#cl_"]'), next: s.querySelectorAll(".ins-next a[data-insight-next]").length, focus: document.activeElement && document.activeElement.className, anim: v ? getComputedStyle(v).animationName : "" }; });
    await shot("reveal");
    ok(w + ": the reveal shows the verdict, the statement and why, the short answer, the bars and the evidence, then up to 3 next questions", rv && /^(Fact|Myth) (Right!|Not quite\.)$/.test(rv.verdict) && rv.said && rv.why && rv.short && rv.bars && rv.ev && rv.next >= 1 && rv.next <= 3 && rv.focus === "mf-v" && rv.anim === "ins-in", JSON.stringify(rv));
    // the evidence, and back to the answer
    await p.click("#evsheet .ins-ans a.ask-ev"); await p.waitForFunction(() => document.querySelector("#evsheet.open") && !document.querySelector("#evsheet .ins") && !document.querySelector("#evsheet .loading"), null, { timeout: 15000 }).catch(() => {});
    await p.click("#evsheet .ev-back"); await p.waitForTimeout(300);
    const back = await p.evaluate(() => ({ open: !!document.querySelector("#evsheet.open"), ins: !!document.querySelector("#evsheet .ins .ins-ans"), verdict: !!document.querySelector("#evsheet .ins-verdict") }));
    ok(w + ": the evidence opened from the answer comes back to it with Back", back.open && back.ins && back.verdict, JSON.stringify(back));
    // next questions, until the calm end after four answers in a row
    const run = [];
    for (let i = 0; i < 3; i++) {
      const nx = await p.evaluate(() => { const a = document.querySelector("#evsheet .ins-next a[data-insight-next]"); return a ? a.dataset.insightNext : null; }); if (!nx) break;
      await p.click('#evsheet .ins-next a[data-insight-next="' + nx + '"]'); await p.waitForTimeout(250);
      const st = await p.evaluate(() => ({ guess: !!document.querySelector("#evsheet .ins-guess"), safety: !!document.querySelector("#evsheet .ins-sos") }));
      if (st.guess) { await p.click("#evsheet [data-ins-skip]"); await p.waitForTimeout(250); }
      run.push(nx + (st.guess ? " (guess skipped)" : ""));
    }
    const end = await p.evaluate(() => { const e = document.querySelector("#evsheet .ins-end"); return e ? { t: e.querySelector(".ins-end-t").textContent, ask: !!e.querySelector("[data-ins-ask]"), more: !!e.querySelector("[data-ins-more]"), next: document.querySelectorAll("#evsheet .ins-next").length } : null; });
    ui += " " + await uiText(); await shot("end");
    ok(w + ": after four answers in a row, a calm end (Ask something else, or Keep reading)", run.length === 3 && end && end.t === "You’ve read 4 answers" && end.ask && end.more && !end.next, run.join(" > ") + "; " + JSON.stringify(end));
    await p.click("#evsheet [data-ins-ask]"); await p.waitForTimeout(300);
    const after = await p.evaluate(() => ({ closed: !document.querySelector("#evsheet.open"), focus: document.activeElement && document.activeElement.id, value: document.getElementById("search").value }));
    ok(w + ": Ask something else closes the answer and puts the cursor in an empty search box", after.closed && after.focus === "search" && after.value === "", JSON.stringify(after));
    // a safety answer opens at once, with the emergency line
    const sr = await ask(SAFETY[0]); const sAt = sr.fit.findIndex(x => x.id === SAFETY[1]);
    if (sAt >= 0) { await p.click('#search-results a[data-insight="' + SAFETY[1] + '"]'); await p.waitForTimeout(300); }
    const sf = await p.evaluate(() => { const s = document.querySelector("#evsheet.open .ins"); return s ? { guess: !!s.querySelector(".ins-guess"), sos: (s.querySelector(".ins-sos") || {}).textContent || "", ans: !!s.querySelector(".ins-ans .ask-short") } : null; });
    await shot("safety");
    ok(w + ": a safety answer (“" + SAFETY[0] + "”) opens at once, no guess, with the emergency line", sAt >= 0 && sf && !sf.guess && sf.ans && /Emergency/.test(sf.sos), "found at #" + (sAt + 1) + "; " + JSON.stringify(sf));
    await p.click("#evsheet .ev-back"); await p.waitForTimeout(200);
    // a question the site has not checked: said plainly, and Ask us carries the words
    await p.focus("#search"); const nr = await ask(NONE); ui += " " + await uiText(); await shot("not-checked");
    ok(w + ": a question with no close checked answer says “No checked answer fits this closely. Ask us”, with no answers offered", nr.fit.length === 0 && /^No checked answer fits this closely\. Ask us$/.test(nr.none.trim()), JSON.stringify(nr));
    await p.click("#search-results .sr-fit-none button"); await p.waitForTimeout(400);
    const pn = await p.evaluate(() => ({ open: document.getElementById("report").classList.contains("open"), msg: document.getElementById("report-message").value, mode: (document.querySelector('.fb-opt[aria-pressed="true"]') || { dataset: {} }).dataset.mode }));
    ok(w + ": its Ask us opens Ask a question with the words typed", pn.open && pn.msg === NONE && pn.mode === "feedback", JSON.stringify(pn));
    await p.keyboard.press("Escape"); await p.waitForTimeout(200);
    ok(w + ": no “AI” words in what Insight shows", ui.trim().length > 50 && !AI_WORDS.test(ui), (ui.match(AI_WORDS) || ["none"])[0]);
    // the promise under the box: nothing typed is sent anywhere, or kept (Ask us sends nothing either: it opens a form)
    const forms = q => [q, encodeURIComponent(q), q.replace(/ /g, "+"), q.replace(/ /g, "%20")];
    const leaked = sent.filter(x => typed.some(q => forms(q).some(f => x.includes(f))));
    const kept = await p.evaluate(qs => { const all = []; for (const st of [localStorage, sessionStorage]) for (let i = 0; i < st.length; i++) all.push(st.getItem(st.key(i)) || ""); return qs.filter(q => all.some(v => v.includes(q))); }, typed);
    ok(w + ": nothing typed leaves the page or is kept on the device (" + typed.length + " questions, " + sent.length + " requests)", typed.length >= 5 && !leaked.length && !kept.length, (leaked.concat(kept).join(" | ") || "none").slice(0, 200));
    times.push(...await p.evaluate(() => pkInsight.times()));
    await ctx.close();
  }
  // a second visit, in a browser with a profile of its own as people have (a test context keeps no disk cache): the files
  // come back from the browser's cache, revalidated (304), and nothing is downloaded again
  { const dir = fs.mkdtempSync(path.join(os.tmpdir(), "pk-insight-"));
    const ctx = await chromium.launchPersistentContext(dir, { args: ["--no-proxy-server"], viewport: { width: 390, height: 844 } }), p = ctx.pages()[0] || await ctx.newPage();
    p.on("pageerror", e => errors.push("second-visit page error: " + String(e).slice(0, 200)));
    const visit = async again => { await p.goto(BASE + "home"); if (again) await p.reload(); await p.waitForTimeout(600); await p.focus("#search");
      return p.waitForFunction(() => window.pkInsight && pkInsight.state() === "ready", null, { timeout: 120000 }).then(() => true, () => false); };
    const first = await visit(false), mark = served.length, second = await visit(true);
    const big = served.slice(mark).filter(x => /\/insight\//.test(x.p)), bytes = big.reduce((a, x) => a + x.bytes, 0);
    ok("a second visit downloads the model and runtime nothing again (the browser's cache, revalidated)", first && second && big.some(x => /\.onnx$/.test(x.p)) && big.some(x => /\.wasm$/.test(x.p)) && bytes === 0,
      big.map(x => x.p.replace(/^.*\//, "") + " " + x.status).join(", ") || "not requested");
    await ctx.close(); fs.rmSync(dir, { recursive: true, force: true }); }
  // saving data: nothing fetched on focus; one quiet line offers it, and the word search works meanwhile
  { const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
    await ctx.addInitScript(() => { try { Object.defineProperty(Navigator.prototype, "connection", { configurable: true, get: () => ({ saveData: true, effectiveType: "4g", addEventListener() {} }) }); } catch (e) {} });
    const p = await ctx.newPage();
    p.on("pageerror", e => errors.push("save-data page error: " + String(e).slice(0, 200)));
    p.on("console", m => { if (m.type() === "error") errors.push("save-data console error: " + m.text().slice(0, 200)); });
    const reqs = []; p.on("request", r => reqs.push(r.url()));
    const ins = u => /\/data\/insight\.json|\/insight\//.test(u);
    await p.goto(BASE + "home"); await p.waitForTimeout(800); await p.focus("#search"); await p.fill("#search", REAL[1][0]); await p.waitForTimeout(1500);
    const s1 = await p.evaluate(() => { const b = document.getElementById("search-results"); return { get: (b.querySelector(":scope > .sr-get") || {}).textContent || "", last: !!(b.lastElementChild && b.lastElementChild.matches(".sr-get")), words: b.querySelectorAll("a.sr-ans").length, fit: !!b.querySelector(".sr-fit") }; });
    if (SHOTS) await p.screenshot({ path: path.join(SHOTS, "390-insight-save-data.png") });
    ok("390, saving data: nothing of Insight's fetched on focus or typing; the word search answers; one quiet line under the results offers it", !reqs.some(ins) && s1.get === "Understand questions in your own words (downloads about 38 MB once)" && s1.last && s1.words > 0 && !s1.fit, JSON.stringify(s1) + "; fetched " + (reqs.filter(ins).join(", ") || "none"));
    await p.click("#search-results [data-ins-get]");
    const ready = await p.waitForFunction(() => window.pkInsight && pkInsight.state() === "ready", null, { timeout: 120000 }).then(() => true, () => false);
    await p.waitForFunction(id => document.querySelector('#search-results a[data-insight="' + id + '"]'), REAL[1][1], { timeout: 20000 }).catch(() => {});
    const s2 = await p.evaluate(() => ({ fit: [...document.querySelectorAll("#search-results .sr-fit a[data-insight]")].map(a => a.dataset.insight), get: !!document.querySelector("#search-results .sr-get") }));
    ok("390, saving data: tapping the line downloads it, and the question gets its closest checked answers", ready && reqs.some(ins) && s2.fit.includes(REAL[1][1]) && !s2.get, JSON.stringify(s2));
    await ctx.close(); }
  // less motion: the verdict appears without moving
  { const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: "reduce" }), p = await ctx.newPage();
    p.on("pageerror", e => errors.push("reduced-motion page error: " + String(e).slice(0, 200)));
    p.on("console", m => { if (m.type() === "error") errors.push("reduced-motion console error: " + m.text().slice(0, 200)); });
    await p.goto(BASE + "home"); await p.waitForTimeout(800); await p.focus("#search");
    await p.waitForFunction(() => window.pkInsight && pkInsight.state() === "ready", null, { timeout: 120000 }).catch(() => {});
    await p.fill("#search", REAL[0][0]);
    await p.waitForFunction(id => document.querySelector('#search-results a[data-insight="' + id + '"]'), REAL[0][1], { timeout: 20000 }).catch(() => {});
    await p.click('#search-results a[data-insight="' + REAL[0][1] + '"]').catch(() => {}); await p.waitForTimeout(200);
    await p.click("#evsheet [data-ins-guess=myth]").catch(() => {}); await p.waitForTimeout(200);
    const anim = await p.evaluate(() => { const v = document.querySelector("#evsheet .ins-verdict.just"); return v ? getComputedStyle(v).animationName : "missing"; });
    ok("390, less motion: the verdict appears without moving", anim === "none", "animation " + anim);
    await ctx.close(); }
  await browser.close(); server.close();
  const s = times.slice().sort((a, b) => a - b), med = s.length ? s[Math.floor(s.length / 2)] : NaN;
  console.log("Time per search (question to numbers to ranked answers, " + s.length + " searches): median " + med.toFixed(1) + " ms, slowest " + (s[s.length - 1] || NaN).toFixed(1) + " ms");
  ok("no console errors or sideways scroll", !errors.length, errors.slice(0, 6).join(" | "));
  const failed = results.filter(x => !x).length;
  console.log(failed ? failed + " of " + results.length + " checks failed" : "All " + results.length + " checks passed");
  process.exit(failed ? 1 : 0);
})().catch(e => { console.error(e); server.close(); process.exit(1); });
