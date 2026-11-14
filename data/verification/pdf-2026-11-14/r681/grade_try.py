import sys, importlib.util
spec = importlib.util.spec_from_file_location("b", __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "build_w681.py"))
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
for line in sys.stdin:
    t = line.strip()
    if t: print("%.1f | %d | %s" % (b.grade(t), len(t.split()), t))
