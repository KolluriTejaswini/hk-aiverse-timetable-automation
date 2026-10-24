"""Tests the AI's has_cycle(head) from ai_solution.py (needs class Node(val) with .next)."""
import importlib, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    m = importlib.import_module("ai_solution")
except ModuleNotFoundError:
    sys.exit("Save the AI's code as verify/ai_solution.py first.")
Node, has_cycle = m.Node, m.has_cycle

def build(n, cycle_to=None):
    nodes = [Node(i) for i in range(n)]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if cycle_to is not None and n:
        nodes[-1].next = nodes[cycle_to]
    return nodes[0] if nodes else None

cases = [("empty list", build(0), False), ("one node, no cycle", build(1), False),
         ("one node pointing to itself", build(1, 0), True), ("5 nodes, no cycle", build(5), False),
         ("5 nodes, tail -> head", build(5, 0), True), ("6 nodes, tail -> middle", build(6, 3), True),
         ("2 nodes, tail -> head", build(2, 0), True), ("1000 nodes, no cycle", build(1000), False)]
ok = True
for name, head, want in cases:
    got = has_cycle(head)
    print(("PASS" if got == want else "FAIL"), name, "expected", want, "got", got)
    ok &= got == want
print("ALL PASS" if ok else "SOME FAILED")
