"""Net time saved = manual effort - (tool effort incl. review + support). Reads time_assumptions.csv."""
import os, pandas as pd
here = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(here, "time_assumptions.csv"))
man = df[df.side == "manual"].hours_per_semester.sum()
tool = df[df.side == "tool"].hours_per_semester.sum()
review_support = df[df.item.str.contains("review|Support", case=False)].hours_per_semester.sum()
net = man - tool
lines = ["# Net time saved per semester (person-hours)", "",
         "Source of inputs: `time_assumptions.csv`. Rows labelled ASSUMPTION are placeholders until confirmed with the coordinating faculty.", "",
         "| Item | Side | Hours | Label |", "|---|---|---:|---|"]
for r in df.itertuples():
    lines.append(f"| {r.item} | {r.side} | {r.hours_per_semester:g} | {r.label} |")
lines += ["", f"**Manual total:** {man:g} h  ", f"**Tool total (setup+entry+run+review+support):** {tool:g} h  ",
          f"**Net time saved = {man:g} - {tool:g} = {net:g} h per semester** ({net/man:.0%} of manual effort)", "",
          f"Review + support effort is already included above ({review_support:g} h).", "",
          "## Sensitivity (what if my assumptions are wrong?)", "",
          "| Scenario | Manual h | Tool h | Net saved h |", "|---|---:|---:|---:|"]
for name, mf, tf in [("Base", 1, 1), ("Manual is 50% of assumed", .5, 1), ("Manual is 150% of assumed", 1.5, 1),
                     ("Review+support double", 1, None), ("Worst: manual 50% AND review+support double", .5, None)]:
    m = man * mf
    t = tool if tf == 1 else tool + review_support
    lines.append(f"| {name} | {m:g} | {t:g} | {m - t:g} |")
be = tool / man
lines += ["", f"Break-even: the tool pays off as long as real manual effort is above {tool:g} h per semester "
          f"({be:.0%} of the assumed {man:g} h)."]
open(os.path.join(here, "net_time_saved.md"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
