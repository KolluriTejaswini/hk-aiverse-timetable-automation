"""Credit audit: current vs proposed by semester, balance check, % of programme credits affected."""
import os, json
import pandas as pd
here = os.path.dirname(os.path.abspath(__file__))
cur = pd.read_csv(os.path.join(here, "..", "data", "courses_current.csv"), dtype={"sem": str})
chg = pd.read_csv(os.path.join(here, "..", "data", "changes.csv"), dtype={"sem": str})
cur["credits"] = cur["credits"].astype(int)
counted = cur[cur.counted_in_165 == "Y"]
total_cur = counted.credits.sum()
by_sem = counted.groupby("sem")["credits"].sum()

delta = (chg.new_credits - chg.old_credits).groupby(chg["sem"]).sum()
prop_sem = by_sem.add(delta, fill_value=0).astype(int)
total_prop = int(prop_sem.sum())

upd = chg[chg.tag == "UPDATE"].old_credits.sum()
red = (chg[chg.tag == "REDUCE"].old_credits - chg[chg.tag == "REDUCE"].new_credits).sum()
add = (chg[chg.tag == "ADD"].new_credits - chg[chg.tag == "ADD"].old_credits).sum()
affected = upd + red + add
pct = affected / total_cur * 100

# every UPDATE/REDUCE code must exist in the current table
codes = set(cur.code)
missing = [c for c in chg[chg.tag.isin(["UPDATE", "REDUCE"])].code if c not in codes]
assert not missing, missing
assert total_prop == total_cur, (total_prop, total_cur)
assert 20 <= pct <= 25, pct
assert red == add, (red, add)
assert all(prop_sem[s] == by_sem[s] for s in by_sem.index), "semester loads changed"

lines = ["# Credit audit (B.Tech Artificial Intelligence, 2023-24 handbook, section 4.7.1)", "",
         "| Semester | Current credits | Proposed credits |", "|---|---:|---:|"]
for s in by_sem.index:
    lines.append(f"| {s} | {by_sem[s]} | {prop_sem[s]} |")
lines += [f"| **Total** | **{total_cur}** | **{total_prop}** |", "",
          f"- Handbook grand total: 165. Sum of listed courses: {total_cur}. Match: {'yes' if total_cur == 165 else 'NO'}.",
          "- Handbook prints Semester III total as 23, but the listed courses add to 24; only 24 reconciles with the grand total of 165.",
          "- Summer internship IP201 (3 credits) is not in the 165 total (assumption, verify).", "",
          "## How 'programme credits affected' is counted",
          f"UPDATE courses (full credits of each course whose content changes): {upd}",
          f"REDUCE (credits removed): {red}",
          f"ADD (credits added): {add}",
          f"**Affected = {upd} + {red} + {add} = {affected} of {total_cur} = {pct:.1f}%** (target 20-25%).", "",
          f"Balance check: credits removed ({red}) = credits added ({add}) -> programme total unchanged at {total_prop}. Semester loads unchanged: yes.", ""]
open(os.path.join(here, "credit_balance.md"), "w").write("\n".join(lines))
print("\n".join(lines))
json.dump({"current": json.loads(cur.fillna("").to_json(orient="records")),
           "changes": json.loads(chg.fillna("").to_json(orient="records"))},
          open(os.path.join(here, "..", "tool", "data.json"), "w"))
