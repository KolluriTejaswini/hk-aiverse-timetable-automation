# 2. Problem and estimated scale

**Problem.** A timetable that satisfies many fixed rules (labs, industry days, HoD first hour, 16-18 h workload, room capacity) is built by hand by two faculty, checked by eye, and revised after clashes are found. Each semester it is repeated [O E07].

**Scale (what the files show).**
- ~234 course-section rows, 50 course codes, 19 year/programme blocks in the master sheet [O, approximate, E05].
- 4 workbooks to keep consistent: master, section grids, individual timetables, lab slots [O E01-E04].
- 2 people do the work manually each semester [R E08].

**Estimated effort.** Placeholder estimate of 60 person-hours per semester [A] in `calculations/time_assumptions.csv`. It must be replaced with figures from the coordinators (E10). The net-saving result is shown with sensitivity so the conclusion does not depend on one guess.

**Risks of the current method.** Double-booking of a faculty, section, or room is possible [A: logical consequence of manual checking]; workload balance is hard to verify across ~100+ instructors [O E05 gives up to ~131 distinct instructor strings, may overcount due to spelling variants].
