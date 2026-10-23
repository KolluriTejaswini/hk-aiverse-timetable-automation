"""Step 1-2 of the proposed process: apply HoD-approved change requests, then check input quality."""
from common import DAYS, PERIODS, PAIRS, copy_data, rules, faculty_days, is_hod, is_industry

ALLOWED_CHANGES = {"ALLOW_HOD_FIRST_HOUR", "SET_FACULTY_DAYS"}


def issue(level, code, detail):
    return {"level": level, "code": code, "detail": detail}


def apply_change_requests(data):
    """Only requests approved by the HoD are applied. Everything is logged."""
    data = copy_data(data)
    log = []
    cr = data["ChangeRequests"]
    for _, r in cr.iterrows():
        rid = r["request_id"] or "?"
        if r["approved_by"].strip().upper() != "HOD":
            log.append(issue("REJECTED", "UNAUTHORIZED_REQUEST",
                             f"{rid}: '{r['change_type']}' on {r['target']} requested by {r['requested_by']} "
                             f"but approved_by='{r['approved_by']}' (only HoD may approve). Ignored."))
            continue
        if r["change_type"] not in ALLOWED_CHANGES:
            log.append(issue("REJECTED", "UNSUPPORTED_REQUEST", f"{rid}: unknown change_type '{r['change_type']}'."))
            continue
        fac = data["Faculty"]
        if r["target"] not in set(fac["faculty_id"]):
            log.append(issue("REJECTED", "UNKNOWN_TARGET", f"{rid}: faculty '{r['target']}' not found."))
            continue
        idx = fac.index[fac["faculty_id"] == r["target"]][0]
        if r["change_type"] == "ALLOW_HOD_FIRST_HOUR":
            data["Faculty"].loc[idx, "is_hod"] = "N"
        else:  # SET_FACULTY_DAYS
            data["Faculty"].loc[idx, "allowed_days"] = r["value"]
        log.append(issue("APPLIED", "HOD_APPROVED_CHANGE", f"{rid}: {r['change_type']} {r['target']} -> {r['value']}"))
    return data, log


def check_input(data):
    """Returns (clean_data, issues). Any issue with level ERROR means: reject, do not generate."""
    data = copy_data(data)
    issues = []
    fac_ids = set(data["Faculty"]["faculty_id"])
    subj = data["Subjects"].set_index("subject")
    secs = data["Sections"].set_index("section")
    rooms = data["Rooms"].set_index("room_id")
    a = data["Assignments"]

    # --- duplicates (exact duplicates are merged, conflicting ones are errors)
    key = a["section"] + "|" + a["subject"]
    dup_mask = key.duplicated(keep="first")
    for i in a.index[dup_mask]:
        first = a[key == key[i]].iloc[0]
        if first["faculty_id"] == a.loc[i, "faculty_id"]:
            issues.append(issue("WARNING", "DUPLICATE_MERGED",
                                f"Row for section {a.loc[i,'section']} / {a.loc[i,'subject']} appears twice; duplicate removed."))
        else:
            issues.append(issue("ERROR", "DUPLICATE_CONFLICT",
                                f"Section {a.loc[i,'section']} / {a.loc[i,'subject']} listed with two different faculty "
                                f"({first['faculty_id']} vs {a.loc[i,'faculty_id']}). HoD must decide."))
    a = a[~dup_mask].copy()
    data["Assignments"] = a

    # --- missing / unknown fields
    for i, r in a.iterrows():
        label = f"section {r['section']} / {r['subject']}"
        if r["faculty_id"] == "":
            issues.append(issue("ERROR", "MISSING_FACULTY", f"{label}: no faculty assigned."))
        elif r["faculty_id"] not in fac_ids:
            issues.append(issue("ERROR", "UNKNOWN_FACULTY", f"{label}: faculty '{r['faculty_id']}' not in Faculty sheet."))
        if r["subject"] not in subj.index:
            issues.append(issue("ERROR", "UNKNOWN_SUBJECT", f"{label}: subject not in Subjects sheet."))
        if r["section"] not in secs.index:
            issues.append(issue("ERROR", "UNKNOWN_SECTION", f"{label}: section not in Sections sheet."))
    # every section must have every subject
    have = set(zip(a["section"], a["subject"]))
    for s in secs.index:
        for sj in subj.index:
            if (s, sj) not in have:
                issues.append(issue("ERROR", "MISSING_ASSIGNMENT", f"section {s} has no row for subject {sj}."))

    # --- room capacity
    for s, r in secs.iterrows():
        room = r["home_room"]
        if room not in rooms.index:
            issues.append(issue("ERROR", "UNKNOWN_ROOM", f"section {s}: home room {room} not in Rooms."))
        elif int(r["strength"]) > int(rooms.loc[room, "capacity"]):
            issues.append(issue("ERROR", "ROOM_TOO_SMALL",
                                f"section {s}: strength {r['strength']} > capacity {rooms.loc[room,'capacity']} of {room}."))

    # --- capacity diagnostics (probable causes if the solver later fails)
    rl = rules(data)
    fdays = faculty_days(data)
    load, blocks = {}, {}
    for _, r in a.iterrows():
        if r["subject"] not in subj.index or r["faculty_id"] not in fac_ids:
            continue
        th, lb = int(subj.loc[r["subject"], "theory_hrs"]), int(subj.loc[r["subject"], "lab_blocks"])
        load[r["faculty_id"]] = load.get(r["faculty_id"], 0) + th + 2 * lb
        blocks[r["faculty_id"]] = blocks.get(r["faculty_id"], 0) + lb
    for f, hrs in load.items():
        days = fdays.get(f, [])
        avail = len(days) * len(PERIODS) - (len(days) if is_hod(data, f) else 0)
        avail_pairs = len(days) * len(PAIRS)
        if hrs > avail:
            issues.append(issue("DIAGNOSTIC", "FACULTY_OVERLOADED_FOR_DAYS",
                                f"{f} needs {hrs} periods but only {avail} slots exist on allowed days {days}."))
        if blocks.get(f, 0) > avail_pairs:
            issues.append(issue("DIAGNOSTIC", "NOT_ENOUGH_LAB_PAIRS",
                                f"{f} needs {blocks[f]} two-hour lab blocks but only {avail_pairs} block slots exist "
                                f"on allowed days {days}."))
        if hrs > len(days) * rl["max_faculty_periods_per_day"]:
            issues.append(issue("DIAGNOSTIC", "DAILY_LIMIT_EXCEEDED",
                                f"{f} needs {hrs} periods but daily limit allows {len(days)*rl['max_faculty_periods_per_day']}."))
        if not is_industry(data, f) and not (rl["workload_min"] <= hrs <= rl["workload_max"]):
            issues.append(issue("WARNING", "WORKLOAD_OUT_OF_RANGE",
                                f"{f} assigned {hrs} h/week; target {rl['workload_min']}-{rl['workload_max']}. HoD may rebalance."))
    lab_rooms = [r for r, x in rooms.iterrows() if x["room_type"] == "Lab"]
    total_blocks = sum(blocks.values())
    if total_blocks > len(lab_rooms) * len(DAYS) * len(PAIRS):
        issues.append(issue("DIAGNOSTIC", "NOT_ENOUGH_LAB_ROOM_SLOTS",
                            f"{total_blocks} lab blocks needed, only {len(lab_rooms)*len(DAYS)*len(PAIRS)} lab-room slots exist."))
    return data, issues


def has_errors(issues):
    return any(i["level"] == "ERROR" for i in issues)
