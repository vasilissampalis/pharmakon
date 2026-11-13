"""Load and save data/site/simple.json in the project's format (indent 1, UTF-8, trailing newline)."""
import json, pathlib
P = pathlib.Path(__file__).resolve().parents[2] / "data" / "site" / "simple.json"
def load():
    return json.load(open(P, encoding="utf-8"))
def save(S):
    with open(P, "w", encoding="utf-8") as f:
        json.dump(S, f, ensure_ascii=False, indent=1); f.write("\n")
