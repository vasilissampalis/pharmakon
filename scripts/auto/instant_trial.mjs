// instant_trial.mjs: the answer within seconds (site/worker/_worker.js, /api/answer), tried with the REAL model and the REAL index of
// papers, on the editor's own questions, where a key is held (GitHub's machines; .github/workflows/lane.yml, requests instant-*.json).
//
//   node scripts/auto/instant_trial.mjs REQUESTS_DIR OUT_DIR USAGE.json
//
// Why: the editor's workspace can reach neither the site nor the model, and on the site the model answers only once the senior author
// has bound it. This runs the very code the site's server runs (the same file, imported), with three stand-ins for what Cloudflare gives
// it there: the model, asked through Cloudflare's own API with the repository's key (the same model, the same account, the same free
// allowance); a store kept in memory; and the network as it is (Europe PMC). So what the model really writes, what the code's checks
// keep and refuse, and how long it takes are seen before a reader ever meets it.
// A request: {"questions": [{"q": "...", "names": ["..."], "words": ["..."]}], "most_neurons": 1200}. The questions are the editor's own
// (never a visitor's). What is written (OUT_DIR/trial-<time>.json): for each question the server's reply, the sentences kept, the ones
// refused with the reason, the model's raw words, the papers' titles (never their summaries), the time taken and the neurons used.
// No key is printed: the account's number is taken out of anything the service says. Usage is written for the lane's ledger (USAGE.json).
import fs from "node:fs";
import path from "node:path";
import worker, { IA } from "../../site/worker/_worker.js";

const [dir, outDir, usageFile] = process.argv.slice(2);
const token = (process.env.CLOUDFLARE_API_TOKEN || "").trim(), account = (process.env.CLOUDFLARE_ACCOUNT_ID || "").trim();
const hide = s => String(s).split(account || "\u0000").join("***").split(token || "\u0000").join("***").replace(/(accounts\/)[0-9a-fA-F]{32}/g, "$1***");
if (!dir || !outDir) { console.log("usage: node scripts/auto/instant_trial.mjs REQUESTS_DIR OUT_DIR [USAGE.json]"); process.exit(2); }
const files = fs.existsSync(dir) ? fs.readdirSync(dir).filter(f => /^instant-.*\.json$/.test(f)).sort() : [];
if (!files.length) { console.log("instant trial: no request"); process.exit(0); }
if (!token || !account) { console.log("instant trial: no key here: nothing is asked"); process.exit(0); }
let left = Number(process.env.NEURONS_LEFT); if (!Number.isFinite(left)) left = 0;
console.log("instant trial: " + files.length + " request(s); the lane's ledger leaves " + Math.round(left) + " neurons today");

const asked = [];   // every call to the model: time, tokens, raw words
const ai = { run: async (model, input) => {
  const t0 = Date.now();
  const r = await fetch("https://api.cloudflare.com/client/v4/accounts/" + account + "/ai/run/" + model, { method: "POST", headers: { authorization: "Bearer " + token, "content-type": "application/json" }, body: JSON.stringify(input) });
  let j = null; try { j = await r.json(); } catch (e) { j = null; }
  if (!r.ok || !j || j.success === false || !j.result) { const said = hide(JSON.stringify((j && j.errors) || r.status)).slice(0, 300); asked.push({ ms: Date.now() - t0, failed: said, form: !!input.response_format }); throw new Error(said); }
  const res = j.result, raw = typeof res.response === "string" ? res.response : JSON.stringify(res.response);
  asked.push({ ms: Date.now() - t0, usage: res.usage || null, form: !!input.response_format, keys: Object.keys(res), raw: hide(String(raw)).slice(0, 2000), given: String(input.messages[1].content).split("\n").filter(l => /^\[\d+\] \(/.test(l)).map(l => l.slice(0, 200)) });
  return res; } };
const store = (() => { const m = new Map(); return { m, get: async (k, how) => { const v = m.get(k); return v == null ? null : how === "json" ? JSON.parse(v) : v; }, put: async (k, v) => { m.set(k, v); } }; })();
const env = { ASSETS: { fetch: async () => new Response("", { status: 404 }) }, QUESTIONS: store, AI: ai };
const neuronsOf = c => (c.usage ? (Number(c.usage.prompt_tokens) || 0) * IA.price[0] / 1e6 + (Number(c.usage.completion_tokens) || 0) * IA.price[1] / 1e6 : 0);

let used = 0, usage = { model: IA.writer, in: 0, out: 0 };
fs.mkdirSync(outDir, { recursive: true });
for (const f of files) {
  let req = null; try { req = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8")); } catch (e) { console.log("instant trial: " + f + " is not JSON"); continue; }
  const most = Math.min(Number(req.most_neurons) || 1200, Math.max(0, left - 300)), items = [];
  for (const q of Array.isArray(req.questions) ? req.questions.slice(0, 40) : []) {
    if (used + 160 > most) { items.push({ q: q.q, skipped: "the neurons this trial may use are used (" + Math.round(used) + " of " + Math.round(most) + ")" }); continue; }
    const before = asked.length, t0 = Date.now();
    let reply = null, status = 0;
    try { const r = await worker.fetch(new Request("https://pharmakon.world/api/answer", { method: "POST", headers: { "content-type": "application/json", origin: "https://pharmakon.world" }, body: JSON.stringify({ q: q.q, names: q.names, words: q.words }) }), env); status = r.status; reply = await r.json(); }
    catch (e) { reply = { error: hide(String(e && e.message)).slice(0, 200) }; }
    const calls = asked.slice(before), key = [...store.m.keys()].filter(k => k.startsWith("ia:")).pop(), kept = key ? JSON.parse(store.m.get(key)) : null;
    for (const c of calls) { used += neuronsOf(c); if (c.usage) { usage.in += Number(c.usage.prompt_tokens) || 0; usage.out += Number(c.usage.completion_tokens) || 0; } }
    items.push({ q: q.q, names: q.names, words: q.words, status, ms: Date.now() - t0, reply, kept: kept && calls.length ? { lines: kept.lines, drop: kept.drop || [], why: kept.why || "" } : null, model: calls });
    console.log("instant trial: " + JSON.stringify(q.q) + ": " + (reply && reply.answer ? reply.answer.lines.length + " sentence(s) kept" : reply && reply.none ? "nothing shown (" + reply.why + ")" : JSON.stringify(reply).slice(0, 120)) + (kept && kept.drop ? ", " + kept.drop.length + " refused" : "") + ", " + (Date.now() - t0) + " ms");
  }
  const stamp = new Date().toISOString().replace(/[-:]/g, "").slice(0, 13), outFile = path.join(outDir, "trial-" + stamp + "-" + f.replace(/^instant-|\.json$/g, "") + ".json");
  fs.writeFileSync(outFile, JSON.stringify({ _note: "Made by scripts/auto/instant_trial.mjs: the answer within seconds (site/worker/_worker.js, /api/answer) tried with the real model and the real index of papers on the editor's own questions. Nothing here is shown on the site. kept.lines: what a reader would see; kept.drop: what the model wrote that the code's checks refused, and why; model: every call, with its raw words.", made: new Date().toISOString(), why: String(req.why || "").slice(0, 300), writer: IA.writer, v: IA.v, neurons: Math.round(used * 10) / 10, items }, null, 1));
  console.log("instant trial: written " + outFile + " (" + Math.round(used) + " neurons so far)");
}
if (usageFile) fs.writeFileSync(usageFile, JSON.stringify([usage]));
