"""export_mix.py MODELS_DIR STATE.pt ALPHA OUT.onnx: write an encoder file for the site from a fine-tuned state, mixed with the
original weights: weights = (1 - ALPHA) x original + ALPHA x fine-tuned (ALPHA 1 = the fine-tuned model as it is). Mixing
keeps what the original knows about ordinary language while taking what the training taught about this site's questions;
the gold set's dev half chooses ALPHA. Writes OUT.onnx as int8 with the inputs and output the site loads."""
import sys, pathlib, hashlib, tempfile
import numpy as np, torch, onnx
from onnx import numpy_helper
from transformers import BertConfig, BertModel
M_DIR, state, alpha, out = pathlib.Path(sys.argv[1]), sys.argv[2], float(sys.argv[3]), pathlib.Path(sys.argv[4])
FP32 = M_DIR / "_maycombhq_embed-model/package/model.onnx"
m = onnx.load(str(FP32)); init = {i.name: numpy_helper.to_array(i) for i in m.graph.initializer}
cfg = BertConfig(vocab_size=30522, hidden_size=384, num_hidden_layers=6, num_attention_heads=12, intermediate_size=1536, max_position_embeddings=512, type_vocab_size=2, hidden_act="gelu", layer_norm_eps=1e-12)
model = BertModel(cfg, add_pooling_layer=False)
sd = {k: torch.tensor(v.copy()) for k, v in init.items() if not k.startswith("onnx::") and k != "embeddings.position_ids"}
for n in m.graph.node:
    if n.op_type == "MatMul" and n.input[1] in init: sd[n.output[0].split("/MatMul")[0].strip("/").replace("/", ".") + ".weight"] = torch.tensor(init[n.input[1]].T.copy())
ft = torch.load(state)
mix = {k: (1 - alpha) * v + alpha * ft[k] if v.dtype.is_floating_point else v for k, v in sd.items()}
missing, unexpected = model.load_state_dict(mix, strict=False); assert not unexpected
model.eval()
class Wrap(torch.nn.Module):
    def __init__(self, m): super().__init__(); self.m = m
    def forward(self, input_ids, attention_mask, token_type_ids): return self.m(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids).last_hidden_state
ii = torch.tensor([[101, 1037, 2460, 2742, 102, 0, 0], [101, 2178, 1010, 3621, 2936, 2742, 102]]); am = (ii != 0).long()
with tempfile.TemporaryDirectory() as td:
    fp = pathlib.Path(td) / "fp32.onnx"
    torch.onnx.export(Wrap(model), (ii, am, torch.zeros_like(ii)), str(fp), input_names=["input_ids", "attention_mask", "token_type_ids"], output_names=["last_hidden_state"],
                      dynamic_axes={k: {0: "batch", 1: "sequence"} for k in ("input_ids", "attention_mask", "token_type_ids", "last_hidden_state")}, opset_version=14, do_constant_folding=True, dynamo=False)
    from onnxruntime.quantization import quantize_dynamic, QuantType
    quantize_dynamic(str(fp), str(out), weight_type=QuantType.QUInt8)
print(out.name, out.stat().st_size, "bytes, SHA-256", hashlib.sha256(out.read_bytes()).hexdigest())
