"""Step 3 of the proposed process: generate a clash-free draft timetable.
Method: 0/1 integer programme solved with SciPy's HiGHS (free, pip-installable).
Hard rules are constraints; 'avoid last period' is a soft preference in the objective."""
import numpy as np
import pandas as pd
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
from common import DAYS, PERIODS, PAIRS, rules, faculty_days, is_hod


def generate(data, time_limit=60, seed=1):
    rl = rules(data)
    fdays = faculty_days(data)
    subj = data["Subjects"].set_index("subject")
    secs = data["Sections"].set_index("section")
    rooms = data["Rooms"].set_index("room_id")
    items = []
    for _, r in data["Assignments"].iterrows():
        items.append(dict(sec=r["section"], sub=r["subject"], fac=r["faculty_id"],
                          th=int(subj.loc[r["subject"], "theory_hrs"]),
                          lb=int(subj.loc[r["subject"], "lab_blocks"]),
                          rtype=subj.loc[r["subject"], "lab_room_type"]))

    var, ub, cost = [], [], []     # var[k] = ('T', item, d, p) or ('L', item, d, pair_idx, room)

    def add(v, upper, c):
        var.append(v); ub.append(upper); cost.append(c)

    for i, it in enumerate(items):
        hod = is_hod(data, it["fac"])
        for d, day in enumerate(DAYS):
            ok_day = day in fdays.get(it["fac"], [])
            for p in PERIODS:
                if it["th"] > 0:
                    blocked = (not ok_day) or (hod and p == rl["hod_blocked_period"])
                    add(("T", i, d, p), 0 if blocked else 1, 1.0 if p == 9 else 0.0)
            if it["lb"] > 0:
                for k, pr in enumerate(PAIRS):
                    for room, rr in rooms.iterrows():
                        if rr["room_type"] != it["rtype"] or int(rr["capacity"]) < int(secs.loc[it["sec"], "strength"]):
                            continue
                        blocked = (not ok_day) or (hod and rl["hod_blocked_period"] in pr)
                        add(("L", i, d, k, room), 0 if blocked else 1, 2.0 if pr == (8, 9) else 0.0)

    n = len(var)
    rng = np.random.default_rng(seed)
    c = np.array(cost) + rng.uniform(0, 1e-3, n)       # tiny noise => varied but reproducible timetables
    rows_lo, rows_hi, entries = [], [], []

    def row(coefs, lo, hi):
        entries.append(coefs); rows_lo.append(lo); rows_hi.append(hi)

    idx = {v: k for k, v in enumerate(var)}
    byitem_T = {i: [] for i in range(len(items))}
    byitem_L = {i: [] for i in range(len(items))}
    cover = {}                                           # (kind,key,d,p) -> list of var idx
    for k, v in enumerate(var):
        if v[0] == "T":
            _, i, d, p = v; byitem_T[i].append(k)
            periods = [p]; rooms_used = [secs.loc[items[i]["sec"], "home_room"]]
        else:
            _, i, d, kk, room = v; byitem_L[i].append(k)
            periods = list(PAIRS[kk]); rooms_used = [room]
        it = items[i]
        for p in periods:
            cover.setdefault(("sec", it["sec"], d, p), []).append(k)
            cover.setdefault(("fac", it["fac"], d, p), []).append(k)
            cover.setdefault(("room", rooms_used[0], d, p), []).append(k)

    for i, it in enumerate(items):
        if it["th"] > 0:
            row({k: 1 for k in byitem_T[i]}, it["th"], it["th"])
            for d in range(5):                           # a theory subject at most once a day per section
                row({idx[("T", i, d, p)]: 1 for p in PERIODS}, 0, 1)
        if it["lb"] > 0:
            row({k: 1 for k in byitem_L[i]}, it["lb"], it["lb"])
            for d in range(5):                           # at most one lab block per day per subject per section
                row({k: 1 for k in byitem_L[i] if var[k][2] == d}, 0, 1)
    for key, ks in cover.items():                        # no clashes for section / faculty / room
        row({k: 1 for k in ks}, 0, 1)
    for d in range(5):                                   # daily load limits
        for who, lim, field in (("sec", rl["max_section_periods_per_day"], "sec"),
                                ("fac", rl["max_faculty_periods_per_day"], "fac")):
            groups = {}
            for k, v in enumerate(var):
                it = items[v[1]]
                if v[2] == d:
                    groups.setdefault(it[field], {})[k] = 1 if v[0] == "T" else 2
            for g, co in groups.items():
                row(co, 0, lim)

    A = lil_matrix((len(entries), n))
    for r_i, co in enumerate(entries):
        for k, val in co.items():
            A[r_i, k] = val
    res = milp(c, constraints=LinearConstraint(A.tocsr(), rows_lo, rows_hi), integrality=np.ones(n),
               bounds=Bounds(np.zeros(n), np.array(ub, dtype=float)),
               options={"time_limit": time_limit, "mip_rel_gap": 0.05, "disp": False})
    if res.x is None:
        return None, {"solver_status": int(res.status), "message": res.message}

    out = []
    for k, v in enumerate(var):
        if res.x[k] < 0.5:
            continue
        it = items[v[1]]
        if v[0] == "T":
            _, i, d, p = v
            out.append([it["sec"], DAYS[d], p, it["sub"], it["fac"], secs.loc[it["sec"], "home_room"], "Theory", ""])
        else:
            _, i, d, kk, room = v
            bid = f"{it['sec']}-{it['sub']}-{DAYS[d]}-{PAIRS[kk][0]}"
            for p in PAIRS[kk]:
                out.append([it["sec"], DAYS[d], p, it["sub"], it["fac"], room, "Lab", bid])
    sched = pd.DataFrame(out, columns=["section", "day", "period", "subject", "faculty_id", "room", "type", "block_id"])
    sched["d"] = sched["day"].map({d: i for i, d in enumerate(DAYS)})
    sched = sched.sort_values(["section", "d", "period"]).drop(columns="d").reset_index(drop=True)
    return sched, {"solver_status": int(res.status), "message": res.message}
