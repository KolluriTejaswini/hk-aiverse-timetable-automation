# 4. Five synthetic cases: expected results and recovery

Results actually produced are in `tests/test_results.md` (run `python src/run_tests.py`).

| Case | Input | Expected result | Recovery |
|---|---|---|---|
| Normal | valid data | OK, 156 periods placed, 0 violations, every regular faculty at 18 h | none needed |
| Missing information | C/DAA has no faculty | REJECTED with MISSING_FACULTY; no timetable | fill the cell, resubmit |
| Duplicate | one row entered twice | duplicate merged and logged; 156 periods (no double counting) | automatic; a conflicting duplicate is an ERROR for the HoD |
| Unauthorized request | lift HoD first-hour block, approved_by = Self | request ignored and logged; F01 has no S1 class | requester gets HoD approval and resubmits |
| Failed step | industry faculty available only Tue | solver infeasible -> FALLBACK_MANUAL naming F09 | HoD-approved change adding Thu -> rerun succeeds |
| Bonus | 3 faults injected into a good timetable | validator reports faculty clash, HoD at S1, industry faculty on Wed | fix flagged cells |
