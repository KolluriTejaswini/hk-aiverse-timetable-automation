# Net time saved per semester (person-hours)

Source of inputs: `time_assumptions.csv`. Rows labelled ASSUMPTION are placeholders until confirmed with the coordinating faculty.

| Item | Side | Hours | Label |
|---|---|---:|---|
| Collect subjects/faculty/sections and allot rooms | manual | 6 | ASSUMPTION |
| Draft master + odd-semester timetable (labs and industry faculty first) | manual | 24 | ASSUMPTION |
| Derive individual faculty timetables | manual | 12 | ASSUMPTION |
| Clash check + revision rounds (3 rounds x 6 h) | manual | 18 | ASSUMPTION |
| Fill the 7-sheet input workbook | tool | 5 | ASSUMPTION |
| Run generator + validator | tool | 0.1 | OBSERVED |
| Human review of draft + fix exceptions (HoD/coordinator) | tool | 8 | ASSUMPTION |
| Support effort (rule changes; data fixes; helping staff) | tool | 6 | ASSUMPTION |
| One-time setup/training (amortised) | tool | 3.33 | ASSUMPTION |

**Manual total:** 60 h  
**Tool total (setup+entry+run+review+support):** 22.43 h  
**Net time saved = 60 - 22.43 = 37.57 h per semester** (63% of manual effort)

Review + support effort is already included above (14 h).

## Sensitivity (what if my assumptions are wrong?)

| Scenario | Manual h | Tool h | Net saved h |
|---|---:|---:|---:|
| Base | 60 | 22.43 | 37.57 |
| Manual is 50% of assumed | 30 | 22.43 | 7.57 |
| Manual is 150% of assumed | 90 | 22.43 | 67.57 |
| Review+support double | 60 | 36.43 | 23.57 |
| Worst: manual 50% AND review+support double | 30 | 36.43 | -6.43 |

Break-even: the tool pays off as long as real manual effort is above 22.43 h per semester (37% of the assumed 60 h).
