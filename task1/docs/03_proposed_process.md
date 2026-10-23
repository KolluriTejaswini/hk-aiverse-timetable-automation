# 3. Proposed process (assisted, human-approved)

**Accountable owner:** the HoD (or timetable coordinator named by the HoD). The tool never publishes anything.

## Inputs (one Excel workbook, 7 sheets)
Faculty (id, role, HoD flag, allowed days) | Subjects (theory hours, lab blocks, lab room type) | Sections (strength, home room) | Rooms (type, capacity) | Assignments (section, subject, faculty) | Rules (workload range, daily limits, HoD blocked period) | ChangeRequests (who asked, who approved, what).

## Statuses
`DRAFT INPUT` -> `INPUT REJECTED` (errors listed) or `INPUT ACCEPTED` -> `GENERATED` -> `VALIDATED (0 violations)` or `GENERATED WITH VIOLATIONS` or `FALLBACK: MANUAL REVIEW` -> `HoD APPROVED` -> `PUBLISHED`. The code sets everything up to the validation status; `HoD APPROVED` and `PUBLISHED` are human steps.

## Approval boundaries
| Action | Tool may do it? |
|---|---|
| Merge exact duplicate rows | Yes, logged |
| Change faculty assignments, rules, availability | **No** - only via a ChangeRequest with `approved_by = HoD` |
| Release a timetable to faculty/students | **No** - human sign-off |
| Resolve conflicting duplicates | **No** - HoD decides |

## Fallback
If the solver finds no feasible timetable, the tool stops, produces no partial timetable, prints probable causes (e.g. "F09 needs 6 lab blocks but only 4 block slots exist on allowed days"), and the coordinators continue manually or ask the HoD to approve a rule change and rerun.

## Mapping to code
`src/input_checks.py` (change requests + input checks) -> `src/generator.py` (solver) -> `src/validator.py` (independent checker) -> `src/excel_io.py` (workbooks) -> `src/pipeline.py` (fallback logic).

## Why the validator is separate
It only needs a long-format schedule, so it can also check a manually prepared timetable once converted. Converting the college's grid format is **not** implemented (see limitations).
