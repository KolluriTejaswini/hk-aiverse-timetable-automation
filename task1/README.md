# Task 1 - Master timetable preparation: process study and assisted redesign

Student work (not an official college process). Everything in this folder uses **synthetic data**. No names, IDs, marks, fees or private messages are included.

## Run it
```bash
pip install -r requirements.txt
python src/make_synthetic_data.py   # creates data/synthetic_input.xlsx
python src/run_demo.py              # -> output/generated_timetable.xlsx
python src/run_tests.py             # five cases + bonus -> tests/test_results.md
python calculations/net_time_saved.py
```

## Read in this order
1. `docs/01_process_as_is.md` - steps, handoffs, approvals, exceptions
2. `docs/02_problem_and_scale.md` - the problem and its size
3. `evidence/evidence_log.md` - dated log: Observed / Estimate / Assumption
4. `docs/03_proposed_process.md` - inputs, statuses, owner, approval boundaries, fallback
5. `docs/04_test_plan.md` and `tests/test_results.md` - five synthetic cases
6. `calculations/net_time_saved.md` - net time after review and support effort
7. `docs/05_limitations.md`, `docs/06_ai_use_and_contribution.md`

## Result of the latest run
Normal case: 156 periods placed in ~2 s, 0 clashes, regular faculty at 18 h each, HoD never in S1. All 5 required cases and the bonus validator test pass.
