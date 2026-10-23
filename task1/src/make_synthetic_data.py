"""Creates data/synthetic_input.xlsx : fully synthetic, no real names, IDs, marks or fees.
Structure mirrors the real process (faculty + subjects + sections + rooms + rules)."""
import os
import pandas as pd

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "synthetic_input.xlsx")

faculty = pd.DataFrame([
    ["F01", "Regular", "Y", "Mon,Tue,Wed,Thu,Fri"],   # F01 plays the HoD role (no class in first hour)
    ["F02", "Regular", "N", "Mon,Tue,Wed,Thu,Fri"],
    ["F03", "Regular", "N", "Mon,Tue,Wed,Thu,Fri"],
    ["F04", "Regular", "N", "Mon,Tue,Wed,Thu,Fri"],
    ["F05", "Regular", "N", "Mon,Tue,Wed,Thu,Fri"],
    ["F06", "Regular", "N", "Mon,Tue,Wed,Thu,Fri"],
    ["F07", "Regular", "N", "Mon,Tue,Wed,Thu,Fri"],
    ["F08", "Regular", "N", "Mon,Tue,Wed,Thu,Fri"],
    ["F09", "Industry", "N", "Tue,Thu"],              # industry faculty come only on fixed days
], columns=["faculty_id", "role", "is_hod", "allowed_days"])

# theory_hrs = lecture periods/week ; lab_blocks = number of 2-hour lab blocks/week
subjects = pd.DataFrame([
    ["IOT", "Internet of Things (synthetic)", 3, 0, ""],
    ["TOC", "Theory of Computation (synthetic)", 3, 0, ""],
    ["DAA", "Design & Analysis of Algorithms (synthetic)", 3, 0, ""],
    ["EEM", "Engineering Economics (synthetic)", 3, 0, ""],
    ["DM", "Discrete Mathematics (synthetic)", 3, 0, ""],
    ["ITPS", "IT Problem Solving (synthetic)", 3, 0, ""],
    ["OOP", "Object Oriented Programming (synthetic)", 2, 2, "Lab"],
    ["PS1", "Power Skills-I (synthetic)", 0, 1, "Lab"],
], columns=["subject", "title", "theory_hrs", "lab_blocks", "lab_room_type"])

strengths = [60, 62, 64, 66, 68, 70]
sections = pd.DataFrame(
    [[s, strengths[i], f"R-{101 + i}"] for i, s in enumerate("ABCDEF")],
    columns=["section", "strength", "home_room"])

rooms = pd.DataFrame(
    [[f"R-{101 + i}", "Class", cap] for i, cap in enumerate([70, 70, 72, 72, 75, 75])] +
    [[f"LAB-{i}", "Lab", 70] for i in (1, 2, 3)],
    columns=["room_id", "room_type", "capacity"])

# HoD decides who teaches what (matches the manual process). 9 hrs/subject-group => 18 hrs per regular faculty.
pairs = {
    "F01": [("IOT", "ABC"), ("TOC", "ABC")], "F02": [("IOT", "DEF"), ("TOC", "DEF")],
    "F03": [("DAA", "ABC"), ("EEM", "ABC")], "F04": [("DAA", "DEF"), ("EEM", "DEF")],
    "F05": [("DM", "ABC"), ("ITPS", "ABC")], "F06": [("DM", "DEF"), ("ITPS", "DEF")],
    "F07": [("OOP", "ABC")], "F08": [("OOP", "DEF")],
    "F09": [("PS1", "ABCDEF")],
}
rows = [[sec, subj, fid] for fid, lst in pairs.items() for subj, secs in lst for sec in secs]
assign = pd.DataFrame(rows, columns=["section", "subject", "faculty_id"]).sort_values(["section", "subject"])

rule_df = pd.DataFrame([
    ["workload_min", 16, "weekly teaching periods, regular faculty (from process description)"],
    ["workload_max", 18, "same"],
    ["max_section_periods_per_day", 6, "ASSUMPTION - adjust to college norm"],
    ["max_faculty_periods_per_day", 6, "ASSUMPTION - adjust to college norm"],
    ["hod_blocked_period", 1, "HoD does rounds in the first hour (from process description)"],
], columns=["key", "value", "note"])

changes = pd.DataFrame(columns=["request_id", "requested_by", "approved_by", "change_type", "target", "value", "note"])

if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with pd.ExcelWriter(OUT) as w:
        for name, df in [("Faculty", faculty), ("Subjects", subjects), ("Sections", sections), ("Rooms", rooms),
                         ("Assignments", assign), ("Rules", rule_df), ("ChangeRequests", changes)]:
            df.to_excel(w, sheet_name=name, index=False)
    print("written", os.path.abspath(OUT))
