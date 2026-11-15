// worker_test.mjs: the question endpoint (site/worker/_worker.js) against a store kept in memory. usage: node scripts/ux/worker_test.mjs
import worker, { readQuestion } from "../../site/worker/_worker.js";
const kv = () => { const m = new Map(); return { m, get: async (k, how) => { const v = m.get(k); return v == null ? null : how === "json" ? JSON.parse(v) : v; }, put: async (k, v) => { m.set(k, v); } }; };
let pass = 0, fail = 0; const ok = (name, cond, extra) => { if (cond) pass++; else { fail++; console.log("FAIL", name, extra || ""); } };
const call = async (env, method, body, headers, path) => { const r = await worker.fetch(new Request("https://pharmakon.world" + (path || "/api/ask"), { method, headers: Object.assign({ "content-type": "application/json" }, headers || {}), body: body == null ? undefined : typeof body === "string" ? body : JSON.stringify(body) }), env); let j = null; try { j = await r.clone().json(); } catch (e) {} return { status: r.status, j, r }; };
const assets = { fetch: async () => new Response("the page", { status: 200 }) };
{ const env = { ASSETS: assets }; let x = await call(env, "GET"); ok("GET without the store answers 200 with ok false (a state, not an error)", x.status === 200 && x.j.ok === false);
  x = await call(env, "POST", { q: "can you overdose on lsd" }); ok("POST without the store is 503", x.status === 503); }
{ const s = kv(), env = { ASSETS: assets, QUESTIONS: s };
  let x = await call(env, "GET"); ok("GET with the store says ok", x.status === 200 && x.j.ok === true);
  x = await call(env, "POST", { q: "  Can you overdose   on LSD? ", d: "lsd", v: "2.4.0" }); ok("a question is kept", x.status === 200 && x.j.ok === true && !x.j.again);
  const keys = [...s.m.keys()], item = JSON.parse(s.m.get(keys.find(k => k.startsWith("q:"))));
  ok("what is kept: the words, the page, the version, the day, a count, and nothing else", item.q === "Can you overdose on LSD?" && item.d[0] === "lsd" && item.v === "2.4.0" && item.n === 1 && item.dn === 1 && Object.keys(item).sort().join() === "d,dn,first,last,n,q,v", JSON.stringify(item));
  x = await call(env, "POST", { q: "can you overdose on lsd?", d: "mdma" }); ok("the same question again is counted, not stored twice", x.j.again === true && [...s.m.keys()].filter(k => k.startsWith("q:")).length === 1);
  const again = JSON.parse(s.m.get(keys.find(k => k.startsWith("q:")))); ok("its count and pages grow", again.n === 2 && again.dn === 2 && again.d.join() === "lsd,mdma");
  { const writes = () => s.m.get("count:" + new Date().toISOString().slice(0, 10)); for (let i = 0; i < 30; i++) x = await call(env, "POST", { q: "Can you overdose on LSD?" });
    const many = JSON.parse(s.m.get(keys.find(k => k.startsWith("q:")))); ok("one question is counted at most 20 times a day, and the rest write nothing", x.status === 200 && x.j.again === true && many.n === 20 && many.dn === 20 && writes() === "20", JSON.stringify(many) + " " + writes());
    const old = Object.assign({}, many, { last: "2026-01-01" }); s.m.set(keys.find(k => k.startsWith("q:")), JSON.stringify(old)); x = await call(env, "POST", { q: "Can you overdose on LSD?" });
    const next = JSON.parse(s.m.get(keys.find(k => k.startsWith("q:")))); ok("on another day it counts again, from one", next.n === 21 && next.dn === 1 && next.last === new Date().toISOString().slice(0, 10), JSON.stringify(next)); }
  for (const [q, why] of [["hi", "too short"], ["cocaine", "too short"], ["see http://x.example for more", "no links"], ["mail me at someone@example.com please", "no links"], ["call me on +30 210 1234567 now", "no long numbers"], ["12345678 9", "too short"], ["<script>alert(1)</script> hello there", "no links"]]) {
    x = await call(env, "POST", { q }); ok("refused: " + q, x.status === 422 && x.j.error.startsWith(why.split(" ")[0] === "no" ? "no" : "too"), JSON.stringify(x.j)); }
  x = await call(env, "POST", "{not json"); ok("bad JSON is 400", x.status === 400);
  x = await call(env, "POST", { q: "x".repeat(3000) }); ok("a body that is too long is 413", x.status === 413);
  x = await call(env, "POST", { q: "is it safe to mix alcohol and ghb" }, { origin: "https://evil.example" }); ok("another site's page cannot send", x.status === 403);
  x = await call(env, "POST", { q: "is it safe to mix alcohol and ghb" }, { origin: "https://pharmakon.world" }); ok("this site's page can", x.status === 200);
  x = await call(env, "PUT", { q: "is it safe to mix alcohol and ghb" }); ok("other methods are 405", x.status === 405);
  x = await call(env, "GET", null, null, "/api/other"); ok("another /api address is 404", x.status === 404);
  x = await call(env, "GET", null, null, "/index.html"); ok("every other address is the site's own file", x.status === 200 && (await x.r.text()) === "the page");
  const long = await call(env, "POST", { q: "why " + "really ".repeat(60) + "does this happen" }); const stored = [...s.m.entries()].filter(([k]) => k.startsWith("q:")).map(([, v]) => JSON.parse(v)).find(v => v.q.startsWith("why really"));
  ok("a long question is cut at 200 characters", long.status === 200 && stored && stored.q.length <= 200);
  s.m.set("count:" + new Date().toISOString().slice(0, 10), "400"); x = await call(env, "POST", { q: "a brand new question about ketamine" }); ok("the daily cap holds for a new question", x.status === 429);
  x = await call(env, "POST", { q: "is it safe to mix alcohol and ghb" }); ok("and for one asked before", x.status === 429);
  ok("no key holds anything but questions and the day's count", [...s.m.keys()].every(k => /^(q:[0-9a-f]{20}|count:\d{4}-\d\d-\d\d)$/.test(k))); }
ok("readQuestion keeps Greek", readQuestion({ q: "είναι ασφαλές το αλκοόλ με κοκαΐνη" }).q.length > 10);
console.log(fail ? fail + " of " + (pass + fail) + " checks failed" : "All " + pass + " checks passed"); process.exit(fail ? 1 : 0);
