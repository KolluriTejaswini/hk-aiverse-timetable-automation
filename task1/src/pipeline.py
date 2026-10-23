"""End-to-end flow: input -> change requests -> input checks -> generate -> validate -> fallback."""
import pandas as pd
from common import load_input
from input_checks import apply_change_requests, check_input, has_errors
from generator import generate
from validator import validate


def run_pipeline(data, time_limit=60):
    res = {"status": None, "log": [], "issues": [], "schedule": None, "violations": None, "message": ""}
    data, log = apply_change_requests(data)
    res["log"] = log
    data, issues = check_input(data)
    res["issues"] = issues
    res["data_used"] = data
    if has_errors(issues):
        res["status"] = "REJECTED"
        res["message"] = "Input rejected. Fix the listed ERRORs and resubmit. Nothing was generated."
        return res
    sched, info = generate(data, time_limit=time_limit)
    res["solver"] = info
    if sched is None:
        res["status"] = "FALLBACK_MANUAL"
        causes = [i for i in issues if i["level"] == "DIAGNOSTIC"]
        res["message"] = ("No feasible timetable under the current rules. MANUAL REVIEW NEEDED. "
                          + ("Probable causes: " + " | ".join(c["detail"] for c in causes) if causes
                             else "No single cause identified by the capacity pre-check; relax one rule at a time."))
        return res
    viol = validate(sched, data)
    res["schedule"], res["violations"] = sched, viol
    res["status"] = "OK" if viol.empty else "GENERATED_WITH_VIOLATIONS"
    res["message"] = "Timetable generated and independently validated: 0 violations." if viol.empty else \
        f"Timetable generated but validator found {len(viol)} violation(s): HoD review required."
    return res
