// Trim verbatim quotations to at most 15 words around the figure they support (METHODS §4.5).
// The data files keep the full sentence each figure was checked against (the verification record); the site shows at
// most 15 consecutive words of it, centred on the figure, with ellipses. Used by site/build.js.
const MAXW = 15;
function windowAround(words, value) {
  // index of the first word containing the value (as printed), else of the first word with a digit
  const vs = value == null ? [] : [String(value), String(value).replace(/\B(?=(\d{3})+(?!\d))/g, ","), String(value).replace(/\B(?=(\d{3})+(?!\d))/g, " ")];
  let i = words.findIndex(w => vs.some(v => v && w.includes(v)));
  if (i < 0) i = words.findIndex(w => /\d/.test(w));
  if (i < 0) i = 0;
  let start = Math.max(0, i - 6), end = Math.min(words.length, start + MAXW);
  start = Math.max(0, end - MAXW);
  return (start > 0 ? "…" : "") + words.slice(start, end).join(" ") + (end < words.length ? "…" : "");
}
function trimQuotes(text, value) {
  if (!text) return text;
  const fix = (body) => { const w = body.trim().split(/\s+/); return w.length > MAXW ? windowAround(w, value) : body; };
  let out = text.replace(/“([^”]+)”/g, (m, b) => "“" + fix(b) + "”").replace(/"([^"]+)"/g, (m, b) => '"' + fix(b) + '"');
  out = out.replace(/(^|[\s(:])'([^']{10,}?)'(?=[\s);,.:]|$)/g, (m, pre, b) => pre + "'" + fix(b) + "'");
  return out;
}
function longQuotes(text) {
  const found = [];
  for (const re of [/“([^”]+)”/g, /"([^"]+)"/g, /(?:^|[\s(:])'([^']{10,}?)'(?=[\s);,.:]|$)/g]) { let m; while ((m = re.exec(text || ""))) { const n = m[1].trim().split(/\s+/).length; if (n > MAXW) found.push(n + ": " + m[1].slice(0, 80)); } }
  return found;
}
module.exports = { trimQuotes, longQuotes };
if (require.main === module) {
  // node scripts/quote_limits.js — report quotations over 15 words that the site would still show after trimming
  const fs = require("fs"), path = require("path"); const ROOT = path.join(__dirname, "..");
  let n = 0, bad = 0;
  for (const f of ["europe", "global", "greece", "us"]) {
    const p = path.join(ROOT, "data/epidemiology", f + ".json"); if (!fs.existsSync(p)) continue;
    for (const r of JSON.parse(fs.readFileSync(p, "utf8"))) for (const k of ["page_or_table", "measure_definition"]) {
      const t = trimQuotes(r[k], r.value); if (t !== r[k]) n++;
      const lq = longQuotes(t); if (lq.length) { bad++; console.log("STILL LONG", r.id, k, lq); }
    }
  }
  for (const dir of ["legal", "identity"]) {
    const d = path.join(ROOT, "data", dir); if (!fs.existsSync(d)) continue;
    for (const f of fs.readdirSync(d).filter(x => x.endsWith(".json"))) {
      const walk = (o, at) => { if (typeof o === "string") { const lq = longQuotes(o); if (lq.length) { bad++; console.log("LONG QUOTE", dir + "/" + f, at, lq); } } else if (o && typeof o === "object") for (const [k, v] of Object.entries(o)) walk(v, at + "/" + k); };
      walk(JSON.parse(fs.readFileSync(path.join(d, f), "utf8")), "");
    }
  }
  console.log("statistics fields trimmed for display:", n, "· quotations still over 15 words:", bad);
  process.exit(bad ? 1 : 0);
}
