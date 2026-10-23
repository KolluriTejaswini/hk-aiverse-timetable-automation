"""Runs the five required synthetic cases (+1 bonus validator self-test) and writes tests/ results."""
import os, json, shutil
import pandas as pd
from common import load_input, copy_data
from pipeline import run_pipeline
from validator import validate
from excel_io import write_workbook

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TESTS = os.path.join(BASE, "tests")
base_data = load_input(os.path.join(BASE, "data", "synthetic_input.xlsx"))
CR_COLS = ["request_id", "requested_by", "approved_by", "change_type", "target", "value", "note"]
results = []


def save_case(name, desc, data, res, expected, passed, recovery):
    d = os.path.join(TESTS, name); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    with pd.ExcelWriter(os.path.join(d, "case_input.xlsx")) as w:
        for k, df in data.items():
            df.to_excel(w, sheet_name=k, index=False)
    pd.DataFrame(res["issues"] + res["log"]).to_csv(os.path.join(d, "issues_and_log.csv"), index=False)
    if res["schedule"] is not None:
        write_workbook(os.path.join(d, "generated_timetable.xlsx"), res["schedule"], res["violations"], res["message"])
    results.append(dict(case=name, description=desc, expected=expected, actual_status=res["status"],
                        actual_message=res["message"], recovery=recovery, result="PASS" if passed else "FAIL"))
    print(("PASS " if passed else "FAIL "), name, "->", res["status"])


# ---- 1 NORMAL
data = copy_data(base_data)
res = run_pipeline(data)
save_case("case1_normal", "Valid synthetic data, no change requests", data, res,
          "status OK, 0 violations, 156 teaching periods placed",
          res["status"] == "OK" and len(res["schedule"]) == 156,
          "n/a - no failure. Faculty then reviews the workbook.")

# ---- 2 MISSING INFORMATION
data = copy_data(base_data)
i = data["Assignments"].index[(data["Assignments"]["section"] == "C") & (data["Assignments"]["subject"] == "DAA")][0]
data["Assignments"].loc[i, "faculty_id"] = ""
res = run_pipeline(data)
codes = [x["code"] for x in res["issues"]]
save_case("case2_missing_info", "Section C / DAA has no faculty assigned", data, res,
          "status REJECTED, MISSING_FACULTY listed for C/DAA, no timetable produced",
          res["status"] == "REJECTED" and "MISSING_FACULTY" in codes and res["schedule"] is None,
          "Coordinator fills the faculty ID in the Assignments sheet and resubmits (no partial timetable is released).")

# ---- 3 DUPLICATE
data = copy_data(base_data)
dup = data["Assignments"].iloc[[0]].copy()
data["Assignments"] = pd.concat([data["Assignments"], dup], ignore_index=True)
res = run_pipeline(data)
codes = [x["code"] for x in res["issues"]]
save_case("case3_duplicate", "First assignment row entered twice (same faculty)", data, res,
          "DUPLICATE_MERGED warning, duplicate dropped, status OK, 0 violations (no double-counted hours)",
          res["status"] == "OK" and "DUPLICATE_MERGED" in codes and len(res["schedule"]) == 156,
          "Automatic: duplicate merged and logged. A CONFLICTING duplicate (different faculty) would be an ERROR for the HoD.")

# ---- 4 UNAUTHORIZED REQUEST
data = copy_data(base_data)
data["ChangeRequests"] = pd.DataFrame([["CR-1", "Faculty member", "Self", "ALLOW_HOD_FIRST_HOUR", "F01", "", "wants S1 slots"]], columns=CR_COLS)
res = run_pipeline(data)
codes = [x["code"] for x in res["log"]]
hod_s1 = res["schedule"] is not None and ((res["schedule"]["faculty_id"] == "F01") & (res["schedule"]["period"] == 1)).any()
save_case("case4_unauthorized", "Request to lift the HoD first-hour block, approved_by='Self'", data, res,
          "UNAUTHORIZED_REQUEST logged, rule unchanged, F01 has no period-1 class, status OK",
          res["status"] == "OK" and "UNAUTHORIZED_REQUEST" in codes and not hod_s1,
          "Request ignored and logged; requester must get HoD approval and resubmit.")

# ---- 5 FAILED STEP (+ recovery)
data = copy_data(base_data)
data["Faculty"].loc[data["Faculty"]["faculty_id"] == "F09", "allowed_days"] = "Tue"   # industry faculty only 1 day
res = run_pipeline(data)
diag = " ".join(x["detail"] for x in res["issues"] if x["level"] == "DIAGNOSTIC")
ok_fail = res["status"] == "FALLBACK_MANUAL" and "F09" in res["message"]
# recovery: HoD-approved change adds Thursday
rec = copy_data(data)
rec["ChangeRequests"] = pd.DataFrame([["CR-2", "Timetable coordinator", "HoD", "SET_FACULTY_DAYS", "F09", "Tue,Thu", "HoD agreed Thu as well"]], columns=CR_COLS)
res2 = run_pipeline(rec)
rec_ok = res2["status"] == "OK"
save_case("case5_failed_step", "Industry faculty F09 available only Tue but needs 6 two-hour blocks (4 block slots exist)", data, res,
          "solver INFEASIBLE -> FALLBACK_MANUAL naming F09 / lab-block capacity; after HoD-approved CR-2 (Tue,Thu) the rerun succeeds",
          ok_fail and rec_ok,
          f"Fallback: manual review message names the cause. Recovery run with HoD-approved change CR-2 -> status {res2['status']}.")
if res2["schedule"] is not None:
    write_workbook(os.path.join(TESTS, "case5_failed_step", "recovery_timetable.xlsx"), res2["schedule"], res2["violations"], res2["message"])
    pd.DataFrame(res2["issues"] + res2["log"]).to_csv(os.path.join(TESTS, "case5_failed_step", "recovery_log.csv"), index=False)

# ---- BONUS: does the validator catch faults injected into a good timetable?
good = run_pipeline(copy_data(base_data))["schedule"].copy()
bad = good.copy()
f01 = bad[(bad["faculty_id"] == "F01") & (bad["type"] == "Theory")]
a, b = f01.iloc[0], f01[f01["section"] != f01.iloc[0]["section"]].iloc[0]
bad.loc[a.name, ["day", "period"]] = [b["day"], b["period"]]                       # fault 1: faculty double-booked
c = bad[(bad["faculty_id"] == "F01") & (bad["type"] == "Theory") & (bad["period"] != 1)].iloc[-1]
bad.loc[c.name, "period"] = 1                                                      # fault 2: HoD in first hour
e = bad[bad["faculty_id"] == "F09"].iloc[0]
bad.loc[bad["block_id"] == e["block_id"], "day"] = "Wed"                           # fault 3: industry faculty on Wed
viol = validate(bad, base_data)
found = set(viol["check"])
need = {"FACULTY_CLASH", "HOD_FIRST_HOUR", "FACULTY_DAY_NOT_ALLOWED"}
ok = need <= found
d = os.path.join(TESTS, "bonus_validator_selftest"); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
viol.to_csv(os.path.join(d, "violations_found.csv"), index=False)
write_workbook(os.path.join(d, "faulty_timetable_with_report.xlsx"), bad, viol, "Faults injected on purpose")
results.append(dict(case="bonus_validator_selftest", description="3 faults injected into a good timetable (double-booking, HoD at S1, industry faculty on Wed)",
                    expected="validator reports FACULTY_CLASH, HOD_FIRST_HOUR, FACULTY_DAY_NOT_ALLOWED",
                    actual_status="CAUGHT " + ",".join(sorted(found & need)), actual_message=f"{len(viol)} violations listed in total",
                    recovery="Coordinator fixes the listed cells and re-validates.", result="PASS" if ok else "FAIL"))
print(("PASS " if ok else "FAIL "), "bonus_validator_selftest ->", sorted(found))

df = pd.DataFrame(results)
df.to_csv(os.path.join(TESTS, "test_results.csv"), index=False)
with open(os.path.join(TESTS, "test_results.md"), "w") as f:
    f.write("# Task 1 - synthetic test results\n\nGenerated by `src/run_tests.py` (all data synthetic).\n\n")
    f.write("| Case | What was fed in | Expected | Actual status | Result |\n|---|---|---|---|---|\n")
    for r in results:
        f.write(f"| {r['case']} | {r['description']} | {r['expected']} | {r['actual_status']} | **{r['result']}** |\n")
    f.write("\n## Messages and recovery\n\n")
    for r in results:
        f.write(f"**{r['case']}**\n- Message: {r['actual_message']}\n- Recovery: {r['recovery']}\n\n")
print(df["result"].value_counts().to_dict())
