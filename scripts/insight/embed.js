// embed.js IN.json OUT.f32: Insight's vectors made by the page's own runtime (site 2.2.0). Called by build_index.py with the
// token ids of each text (made in Python by the tokenizers library, as the page's tokenizer makes them: parity.js checks it);
// runs all-MiniLM-L6-v2 with the same ONNX Runtime Web files the page loads (site/insight/vendor, WebAssembly, one thread,
// the same graph optimizations), one text at a time as the page runs a question, averages the last layer over the tokens and
// scales to unit length; writes the vectors as float32, one row per text. Under Node the WebAssembly gives bit-identical
// numbers to the browser's, which the Python onnxruntime on a PC does not quite do (its int8 kernels round differently: cosine
// 0.994 to 1 against the page; scripts/insight/parity.js reports both).
const fs = require("fs"), path = require("path");
const VENDOR = path.resolve(__dirname, "..", "..", "site", "insight", "vendor");
(async () => {
  const [inp, out] = process.argv.slice(2);
  const ids = JSON.parse(fs.readFileSync(inp, "utf8")).ids;
  const ort = require(path.join(VENDOR, "ort.wasm.min.js"));
  ort.env.wasm.numThreads = 1; ort.env.wasm.proxy = false; ort.env.wasm.wasmPaths = "file://" + VENDOR + "/"; ort.env.logLevel = "error";
  const s = await ort.InferenceSession.create(new Uint8Array(fs.readFileSync(path.join(VENDOR, "all-MiniLM-L6-v2-q8.onnx"))), { executionProviders: ["wasm"], graphOptimizationLevel: "all" });
  let all = null;
  for (let k = 0; k < ids.length; k++) {
    const t = ids[k], n = t.length;
    const feeds = { input_ids: new ort.Tensor("int64", BigInt64Array.from(t, x => BigInt(x)), [1, n]), attention_mask: new ort.Tensor("int64", new BigInt64Array(n).fill(1n), [1, n]) };
    if (s.inputNames.includes("token_type_ids")) feeds.token_type_ids = new ort.Tensor("int64", new BigInt64Array(n), [1, n]);
    const h = (await s.run(feeds))[s.outputNames[0]].data, d = h.length / n, v = new Float32Array(d);
    if (!all) all = new Float32Array(ids.length * d);
    for (let i = 0; i < n; i++) for (let j = 0; j < d; j++) v[j] += h[i * d + j];
    let q = 0; for (let j = 0; j < d; j++) { v[j] /= n; q += v[j] * v[j]; }
    const sc = 1 / Math.max(Math.sqrt(q), 1e-9); for (let j = 0; j < d; j++) all[k * d + j] = v[j] * sc;
  }
  fs.writeFileSync(out, Buffer.from((all || new Float32Array(0)).buffer));
})().catch(e => { console.error("embed.js: " + (e && e.stack || e)); process.exit(1); });
