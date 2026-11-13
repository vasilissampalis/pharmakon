// How fast the start page opens, measured in a real browser (speed work, 13 November 2026; the senior author: "every time I
// open the website… a few seconds pass"). Serves a built site (default site/public) with brotli compression as a real host
// does, then loads the start page twice: a desktop on a fast network, and a mid-range phone (CPU slowed 4 times, a 9 Mbps 4G
// link with 60 ms latency; Chrome throttles the decoded bytes, so this is pessimistic: real phones are faster).
// It reports first paint, when the start page is usable (the script has run and drawn the drug grid), and the page's size.
// Usage: node scripts/ux/perf.js [site dir] [--runs N]   (build first: node site/build.js && python3 -I site/build_public.py)
const http = require("http"), fs = require("fs"), path = require("path"), zlib = require("zlib");
const { chromium } = require("playwright");
const args = process.argv.slice(2), runsAt = args.indexOf("--runs"), RUNS = runsAt >= 0 ? +args[runsAt + 1] : 1;
const ROOT = path.resolve(args.find((a, i) => !a.startsWith("--") && args[i - 1] !== "--runs") || path.join(__dirname, "..", "..", "site", "public"));
const TYPES = { ".html": "text/html; charset=utf-8", ".json": "application/json", ".webp": "image/webp", ".woff2": "font/woff2", ".png": "image/png", ".svg": "image/svg+xml" };
const BR = {};
const brotli = f => (BR[f] = BR[f] || zlib.brotliCompressSync(fs.readFileSync(f), { params: { [zlib.constants.BROTLI_PARAM_QUALITY]: 5 } }));
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]); if (p.endsWith("/")) p += "index.html";
  const f = path.join(ROOT, path.normalize(p)); if (!f.startsWith(ROOT) || !fs.existsSync(f)) { res.writeHead(404); res.end(); return; }
  const type = TYPES[path.extname(f)] || "application/octet-stream";
  if (/html|json|svg/.test(type)) { res.writeHead(200, { "Content-Type": type, "Content-Encoding": "br" }); res.end(brotli(f)); }
  else { res.writeHead(200, { "Content-Type": type }); res.end(fs.readFileSync(f)); }
});
(async () => {
  await new Promise(r => server.listen(0, "127.0.0.1", r));
  brotli(path.join(ROOT, "index.html"));
  const url = "http://127.0.0.1:" + server.address().port + "/#home", browser = await chromium.launch({ args: ["--no-proxy-server"] });
  console.log("index.html: " + (fs.statSync(path.join(ROOT, "index.html")).size / 1e6).toFixed(2) + " MB, " + (BR[path.join(ROOT, "index.html")].length / 1e6).toFixed(2) + " MB compressed (" + ROOT + ")");
  for (const [label, cpu, kbps] of [["desktop, fast network", 1, 50000], ["mid phone (CPU 4x slower), 4G 9 Mbps", 4, 9000]]) {
    const all = [];
    for (let run = 0; run < RUNS; run++) {
      const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } }), page = await ctx.newPage(), cdp = await ctx.newCDPSession(page);
      await cdp.send("Network.enable");
      await cdp.send("Network.emulateNetworkConditions", { offline: false, latency: 60, downloadThroughput: kbps * 1024 / 8, uploadThroughput: kbps * 1024 / 8 });
      await cdp.send("Emulation.setCPUThrottlingRate", { rate: cpu });
      const t0 = Date.now(); await page.goto(url, { waitUntil: "commit" });
      await page.waitForFunction(() => { const v = document.querySelector("#view-home"); return v && v.classList.contains("active") && !!document.querySelector("#dgrid a.dcard"); }, { timeout: 180000, polling: 50 });
      const usable = Date.now() - t0;
      const m = await page.evaluate(() => { const fcp = performance.getEntriesByName("first-contentful-paint")[0], nav = performance.getEntriesByType("navigation")[0];
        return { fcp: fcp ? Math.round(fcp.startTime) : null, dom: Math.round(nav.domInteractive), transfer: nav.transferSize, decoded: nav.decodedBodySize }; });
      all.push(Object.assign(m, { usable }));
      await ctx.close();
    }
    const med = k => all.map(x => x[k]).sort((a, b) => a - b)[Math.floor(all.length / 2)];
    console.log(label + ": first paint " + med("fcp") + " ms, start page usable " + med("usable") + " ms (DOM interactive " + med("dom") + " ms); page transferred " + (all[0].transfer / 1e6).toFixed(2) + " MB of " + (all[0].decoded / 1e6).toFixed(2) + " MB" + (RUNS > 1 ? " (median of " + RUNS + ")" : ""));
  }
  await browser.close(); server.close();
})().catch(e => { console.error(e); process.exit(1); });
