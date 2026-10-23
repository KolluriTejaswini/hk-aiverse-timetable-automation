"""Generate the normal-case timetable from data/synthetic_input.xlsx into output/."""
import os, sys, time
from common import load_input
from pipeline import run_pipeline
from excel_io import write_workbook

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
t = time.time()
res = run_pipeline(load_input(os.path.join(base, "data", "synthetic_input.xlsx")))
print(res["status"], "-", res["message"], f"({time.time()-t:.1f}s)")
if res["schedule"] is not None:
    os.makedirs(os.path.join(base, "output"), exist_ok=True)
    write_workbook(os.path.join(base, "output", "generated_timetable.xlsx"), res["schedule"], res["violations"], res["message"])
    print("written output/generated_timetable.xlsx")
