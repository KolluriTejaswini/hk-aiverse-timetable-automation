"""Shared constants and helpers for the Task 1 timetable tool (synthetic data only)."""
import pandas as pd

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
PERIODS = [1, 2, 3, 4, 6, 7, 8, 9]          # period 5 = LUNCH (never used)
LUNCH = 5
PAIRS = [(1, 2), (3, 4), (6, 7), (8, 9)]    # a 2-hour lab block never spans lunch

SHEETS = ["Faculty", "Subjects", "Sections", "Rooms", "Assignments", "Rules", "ChangeRequests"]


def load_input(path):
    """Read the input workbook into a dict of DataFrames (all text)."""
    x = pd.read_excel(path, sheet_name=None, dtype=str)
    data = {}
    for k in SHEETS:
        df = x.get(k, pd.DataFrame()).fillna("")
        data[k] = df.apply(lambda c: c.astype(str).str.strip()) if len(df.columns) else df
    return data


def copy_data(data):
    return {k: v.copy() for k, v in data.items()}


def rules(data):
    r = {row["key"]: row["value"] for _, row in data["Rules"].iterrows()}
    return {
        "workload_min": int(r.get("workload_min", 16)),
        "workload_max": int(r.get("workload_max", 18)),
        "max_section_periods_per_day": int(r.get("max_section_periods_per_day", 6)),
        "max_faculty_periods_per_day": int(r.get("max_faculty_periods_per_day", 6)),
        "hod_blocked_period": int(r.get("hod_blocked_period", 1)),
    }


def faculty_days(data):
    out = {}
    for _, f in data["Faculty"].iterrows():
        days = [d.strip() for d in f["allowed_days"].split(",") if d.strip()]
        out[f["faculty_id"]] = [d for d in days if d in DAYS]
    return out


def is_hod(data, fid):
    f = data["Faculty"]
    row = f[f["faculty_id"] == fid]
    return (not row.empty) and row.iloc[0]["is_hod"].upper() == "Y"


def is_industry(data, fid):
    f = data["Faculty"]
    row = f[f["faculty_id"] == fid]
    return (not row.empty) and row.iloc[0]["role"].lower() == "industry"
