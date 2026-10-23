# Limitations (honest list)

1. **Synthetic prototype.** 6 sections, 8 subjects, 9 faculty, 3 lab rooms. The real master sheet is far larger (~234 rows) and was not used as solver input.
2. **Not tested on real data.** Real files contain private names and were not committed. Converting the college's grid/master layout into the tool's input format is not implemented.
3. **Simplifications:** one faculty per subject-section; one lab room per lab block (the college sometimes uses two rooms/batches at once); fixed home classroom per section; no electives, no merged classes, no faculty preferences.
4. **Assumed rules** (not confirmed with the HoD): max 6 periods/day for sections and faculty; theory max once/day/section; industry faculty exempt from 16-18 h; the HoD is modelled as one faculty ID.
5. **Workload is fixed by the HoD's assignment**, not optimised. The tool can only check it.
6. **Time estimates** in `calculations/time_assumptions.csv` are placeholders until the coordinators give figures (evidence E10). Net saving can be negative in the worst-case row.
7. **Solver:** SciPy HiGHS with a 5% optimality gap and a 60 s limit. Timetables are valid, not optimal; a different random seed gives a different valid timetable.
8. **Validator scope:** checks only the rules coded in `validator.py`. A passing report means "no known rule broken", not "the timetable is good".
9. **Permission:** confirmation from the coordinating faculty is pending (E11). Student work, not an official college process change.
