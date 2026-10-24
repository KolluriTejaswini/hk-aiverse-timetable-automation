"""Independent computation of FCFS, non-preemptive SJF and Round Robin (q=3)."""
P = {"P1": (0, 8), "P2": (1, 4), "P3": (2, 9), "P4": (3, 5), "P5": (4, 2)}

def report(name, finish, gantt):
    print(f"\n{name}\n  Gantt: {gantt}")
    w = {p: finish[p] - P[p][0] - P[p][1] for p in P}
    for p in P: print(f"  {p}: waiting {w[p]}")
    print(f"  average waiting = {sum(w.values())/len(w):.2f}")

def fcfs():
    t, fin, g = 0, {}, []
    for p in sorted(P, key=lambda k: (P[k][0], k)):
        t = max(t, P[p][0]); g.append((p, t, t + P[p][1])); t += P[p][1]; fin[p] = t
    return fin, g

def sjf():
    t, fin, g, left = 0, {}, [], set(P)
    while left:
        ready = [p for p in left if P[p][0] <= t] or [min(left, key=lambda k: P[k][0])]
        p = min(ready, key=lambda k: (P[k][1], P[k][0], k)); t = max(t, P[p][0])
        g.append((p, t, t + P[p][1])); t += P[p][1]; fin[p] = t; left.remove(p)
    return fin, g

def rr(q=3):
    rem = {p: P[p][1] for p in P}; t, fin, g, queue, seen = 0, {}, [], [], set()
    def admit():
        for p in sorted(P, key=lambda k: (P[k][0], k)):
            if P[p][0] <= t and p not in seen: queue.append(p); seen.add(p)
    admit()
    while len(fin) < len(P):
        if not queue:
            t = min(P[p][0] for p in P if p not in seen); admit(); continue
        p = queue.pop(0); run = min(q, rem[p]); g.append((p, t, t + run)); t += run; rem[p] -= run
        admit()                                 # arrivals during the slice enter the queue first
        if rem[p] > 0: queue.append(p)
        else: fin[p] = t
    return fin, g

for name, f in (("FCFS", fcfs), ("SJF (non-preemptive)", sjf), ("Round Robin q=3", rr)):
    report(name, *f())
