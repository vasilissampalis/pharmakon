/* Pharmakon's one small piece of server (site 2.4, 15 November 2026): the question a reader chooses to send with
   "Ask us to check it". Cloudflare Pages runs this file for /api/* only (_routes.json beside it); every other address
   of the site is a fixed file, served as before, and never reaches this code.

   Kept, in the Workers KV store bound as QUESTIONS: the question's words (at most 200 characters), the drug pages it was
   asked on, the site version, the first and last day it was asked, and how many times (in all, and on that last day). Not kept and not logged: the
   address a request came from, the browser, any cookie (the site sets none). A question that holds a link, an email
   address or a long run of digits is refused, so that nobody's contact details are stored by mistake.

   GET  /api/ask            -> {"ok": true}  when the store is bound; {"ok": false} when it is not (the page asks once,
                               to know whether it can send; without the store it falls back to its email form)
   POST /api/ask {q, d, v}  -> {"ok": true}  the question is kept (or counted again when it was already there);
                               503 without the store
   POST /api/want {id}      -> {"ok": true}  one more person asked a question that is on the site's public list of
                               questions not answered yet (site 2.5). Only the list item's number arrives ("w_0041"):
                               never the person's words. Kept: the number, a count, the last day.
   An address with a slash at its end ("/api/ask/") is taken as the same address. */
// The free store takes 1,000 writes a day and a question kept or counted costs two, so at most 400 are taken in a day.
// One question is counted at most 20 times a day: nobody is known here, so this is what keeps one sender from making a
// question look much asked (the scout orders its list by these counts).
const MAX_Q = 200, MAX_A_DAY = 400, MAX_SAME_A_DAY = 20;
// Counts for the list (/api/want) share the day's 400 and stop at 300, so that they can never crowd out a question
// someone chose to send; one list item is counted at most 60 times a day.
const MAX_WANT_UNTIL = 300, MAX_WANT_SAME_A_DAY = 60;
const json = (o, status) => new Response(JSON.stringify(o), { status: status || 200, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
const clean = s => String(s == null ? "" : s).normalize("NFKC").replace(/[\u0000-\u001f\u007f]/g, " ").replace(/\s+/g, " ").trim();
async function keyOf(text) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, "0")).join("").slice(0, 20);
}
export function readQuestion(body) {
  const q = clean(body && body.q).slice(0, MAX_Q);
  const d = clean(body && body.d).toLowerCase().replace(/[^a-z0-9-]/g, "").slice(0, 40), v = clean(body && body.v).replace(/[^0-9.]/g, "").slice(0, 12);
  if (q.length < 8 || q.split(" ").length < 2 || !/\p{L}{2}/u.test(q)) return { error: "too short" };
  if (/https?:\/\/|www\.|[^\s@]+@[^\s@]+\.[a-z]{2,}|<\s*[a-z!/]/i.test(q)) return { error: "no links or addresses" };
  if (/\d[\d\s().+-]{7,}\d/.test(q)) return { error: "no long numbers" };
  return { q, d, v };
}
// one more person asked a question that is on the public list: the item's number, counted
async function want(request, url, store) {
  if (request.method !== "POST") return json({ ok: false, error: "method" }, 405);
  if (!store) return json({ ok: false, error: "no store" }, 503);
  const origin = request.headers.get("origin");
  if (origin) { let host = ""; try { host = new URL(origin).host; } catch (e) { host = ""; } if (host !== url.host) return json({ ok: false, error: "origin" }, 403); }
  let body = null;
  try { const t = await request.text(); if (t.length > 200) return json({ ok: false, error: "too long" }, 413); body = JSON.parse(t); } catch (e) { return json({ ok: false, error: "json" }, 400); }
  const id = String((body && body.id) || "");
  if (!/^w_[a-z0-9_]{1,40}$/.test(id)) return json({ ok: false, error: "id" }, 422);
  try {
    const day = new Date().toISOString().slice(0, 10), key = "w:" + id, had = await store.get(key, "json");
    if (had && had.last === day && (had.dn || 1) >= MAX_WANT_SAME_A_DAY) return json({ ok: true });   // counted enough for today: nothing is written
    const ck = "count:" + day, n = parseInt((await store.get(ck)) || "0", 10) || 0;
    if (n >= MAX_WANT_UNTIL) return json({ ok: true, full: true });   // the day's room is kept for questions people send
    await store.put(ck, String(n + 1), { expirationTtl: 3 * 86400 });
    const rec = had ? { n: (had.n || 1) + 1, dn: had.last === day ? (had.dn || 1) + 1 : 1, first: had.first || day, last: day } : { n: 1, dn: 1, first: day, last: day };
    await store.put(key, JSON.stringify(rec));
    return json({ ok: true });
  } catch (e) { return json({ ok: false, error: "store" }, 503); }
}
export default {
  async fetch(request, env) {
    const url = new URL(request.url), at = url.pathname.replace(/\/+$/, "");   // "/api/ask/" is "/api/ask"
    if (at !== "/api/ask" && at !== "/api/want") return url.pathname.startsWith("/api/") ? json({ ok: false, error: "not found" }, 404) : env.ASSETS.fetch(request);
    const store = env.QUESTIONS;
    if (at === "/api/want") return want(request, url, store);
    if (request.method === "GET") return json({ ok: !!store });   // 200 either way: a missing store is a state, not an error in the reader's console
    if (request.method !== "POST") return json({ ok: false, error: "method" }, 405);
    if (!store) return json({ ok: false, error: "no store" }, 503);
    // only this site's own pages may send
    const origin = request.headers.get("origin");
    if (origin) { let host = ""; try { host = new URL(origin).host; } catch (e) { host = ""; } if (host !== url.host) return json({ ok: false, error: "origin" }, 403); }
    let body = null;
    try { const t = await request.text(); if (t.length > 2000) return json({ ok: false, error: "too long" }, 413); body = JSON.parse(t); } catch (e) { return json({ ok: false, error: "json" }, 400); }
    const r = readQuestion(body); if (r.error) return json({ ok: false, error: r.error }, 422);
    try {
      const day = new Date().toISOString().slice(0, 10), key = "q:" + (await keyOf(r.q.toLowerCase()));
      const had = await store.get(key, "json");
      if (had && had.last === day && (had.dn || 1) >= MAX_SAME_A_DAY) return json({ ok: true, again: true });   // counted enough for today: nothing is written
      const ck = "count:" + day, n = parseInt((await store.get(ck)) || "0", 10) || 0;
      if (n >= MAX_A_DAY) return json({ ok: false, error: "full for today" }, 429);
      await store.put(ck, String(n + 1), { expirationTtl: 3 * 86400 });
      if (had) {
        had.n = (had.n || 1) + 1; had.dn = had.last === day ? (had.dn || 1) + 1 : 1; had.last = day;
        if (r.d && !(had.d || []).includes(r.d)) had.d = (had.d || []).concat(r.d).slice(0, 5);
        await store.put(key, JSON.stringify(had)); return json({ ok: true, again: true });
      }
      await store.put(key, JSON.stringify({ q: r.q, d: r.d ? [r.d] : [], v: r.v, first: day, last: day, n: 1, dn: 1 }));
      return json({ ok: true });
    } catch (e) { return json({ ok: false, error: "store" }, 503); }
  }
};
