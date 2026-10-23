"""Step 4 of the proposed process: independent clash / rule checker.
It only needs a long-format schedule (section, day, period, subject, faculty_id, room, type, block_id),
so it can check a generated timetable OR a manually prepared one converted to this format."""
import pandas as pd
from common import DAYS, PERIODS, PAIRS, LUNCH, rules, faculty_days, is_hod, is_industry


def v(check, severity, detail):
    return {"check": check, "severity": severity, "detail": detail}


def validate(sched, data):
    out = []
    rl = rules(data)
    fdays = faculty_days(data)
    subj = data["Subjects"].set_index("subject")
    secs = data["Sections"].set_index("section")
    rooms = data["Rooms"].set_index("room_id")
    fac_ids = set(data["Faculty"]["faculty_id"])
    s = sched.copy()
    s["period"] = s["period"].astype(int)

    # reference checks
    for _, r in s[~s["faculty_id"].isin(fac_ids)].iterrows():
        out.append(v("UNKNOWN_FACULTY", "ERROR", f"{r['section']} {r['day']} P{r['period']}: faculty '{r['faculty_id']}'"))
    for _, r in s[~s["room"].isin(rooms.index)].iterrows():
        out.append(v("UNKNOWN_ROOM", "ERROR", f"{r['section']} {r['day']} P{r['period']}: room '{r['room']}'"))
    for _, r in s[~s["period"].isin(PERIODS)].iterrows():
        what = "lunch period used" if r["period"] == LUNCH else "invalid period"
        out.append(v("BAD_PERIOD", "ERROR", f"{r['section']} {r['day']} P{r['period']}: {what}"))
    for _, r in s[~s["day"].isin(DAYS)].iterrows():
        out.append(v("BAD_DAY", "ERROR", f"{r['section']} day '{r['day']}'"))

    # clashes
    for col, name in (("faculty_id", "FACULTY_CLASH"), ("section", "SECTION_CLASH"), ("room", "ROOM_CLASH")):
        g = s.groupby([col, "day", "period"]).size()
        for (who, d, p), cnt in g[g > 1].items():
            rows = s[(s[col] == who) & (s["day"] == d) & (s["period"] == p)]
            what = "; ".join(f"{r.section}/{r.subject}" for r in rows.itertuples())
            out.append(v(name, "ERROR", f"{who} has {cnt} bookings on {d} P{p}: {what}"))

    # hours per subject per section + assignment match
    a = data["Assignments"]
    for _, r in a.iterrows():
        sub = s[(s["section"] == r["section"]) & (s["subject"] == r["subject"])]
        th, lb = int(subj.loc[r["subject"], "theory_hrs"]), int(subj.loc[r["subject"], "lab_blocks"])
        got_t, got_l = (sub["type"] == "Theory").sum(), (sub["type"] == "Lab").sum()
        if got_t != th or got_l != 2 * lb:
            out.append(v("HOURS_MISMATCH", "ERROR",
                         f"{r['section']}/{r['subject']}: theory {got_t}/{th}, lab periods {got_l}/{2*lb}"))
        wrong = sub[sub["faculty_id"] != r["faculty_id"]]
        if len(wrong):
            out.append(v("WRONG_FACULTY", "ERROR", f"{r['section']}/{r['subject']}: assigned {r['faculty_id']} "
                         f"but scheduled with {sorted(set(wrong['faculty_id']))}"))

    # theory repeated on same day
    t = s[s["type"] == "Theory"].groupby(["section", "subject", "day"]).size()
    for (sec, sub, d), cnt in t[t > 1].items():
        out.append(v("THEORY_REPEAT_SAME_DAY", "ERROR", f"{sec}/{sub} has {cnt} theory periods on {d}"))

    # lab blocks must be an allowed consecutive pair in one room
    for bid, g in s[s["type"] == "Lab"].groupby("block_id"):
        ps = tuple(sorted(g["period"]))
        if ps not in PAIRS or g["room"].nunique() != 1 or g["day"].nunique() != 1:
            out.append(v("LAB_BLOCK_INVALID", "ERROR", f"block {bid}: periods {ps}, rooms {sorted(set(g['room']))}"))
    for _, r in s[(s["type"] == "Lab") & (s["room"].isin(rooms.index))].iterrows():
        if rooms.loc[r["room"], "room_type"] != "Lab":
            out.append(v("LAB_IN_CLASSROOM", "ERROR", f"{r['section']}/{r['subject']} {r['day']} P{r['period']} in {r['room']}"))

    # capacity
    for _, r in s[s["room"].isin(rooms.index) & s["section"].isin(secs.index)].drop_duplicates(["section", "room"]).iterrows():
        if int(secs.loc[r["section"], "strength"]) > int(rooms.loc[r["room"], "capacity"]):
            out.append(v("ROOM_TOO_SMALL", "ERROR", f"section {r['section']} ({secs.loc[r['section'],'strength']}) in {r['room']} "
                                                    f"(cap {rooms.loc[r['room'],'capacity']})"))

    # faculty rules
    for f in sorted(set(s["faculty_id"]) & fac_ids):
        fs = s[s["faculty_id"] == f]
        if is_hod(data, f):
            for _, r in fs[fs["period"] == rl["hod_blocked_period"]].iterrows():
                out.append(v("HOD_FIRST_HOUR", "ERROR", f"{f} teaches {r['section']}/{r['subject']} on {r['day']} P{r['period']}"))
        for _, r in fs[~fs["day"].isin(fdays.get(f, []))].iterrows():
            out.append(v("FACULTY_DAY_NOT_ALLOWED", "ERROR", f"{f} on {r['day']} (allowed {fdays.get(f)}) {r['section']}/{r['subject']}"))
        if not is_industry(data, f):
            hrs = len(fs)
            if not (rl["workload_min"] <= hrs <= rl["workload_max"]):
                out.append(v("WORKLOAD", "ERROR", f"{f} has {hrs} h/week (target {rl['workload_min']}-{rl['workload_max']})"))
        for d, cnt in fs.groupby("day").size().items():
            if cnt > rl["max_faculty_periods_per_day"]:
                out.append(v("FACULTY_DAILY_LIMIT", "ERROR", f"{f} has {cnt} periods on {d}"))
    for (sec, d), cnt in s.groupby(["section", "day"]).size().items():
        if cnt > rl["max_section_periods_per_day"]:
            out.append(v("SECTION_DAILY_LIMIT", "ERROR", f"section {sec} has {cnt} periods on {d}"))
    return pd.DataFrame(out, columns=["check", "severity", "detail"])
