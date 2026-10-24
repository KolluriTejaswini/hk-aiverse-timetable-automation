"""Runs the AI's SQL (verify/ai_query.sql) on a small synthetic DB and compares with a pandas answer."""
import os, sys, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sql_data import make_db
db = make_db()
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai_query.sql")
if not os.path.exists(path):
    sys.exit("Save the AI's query as verify/ai_query.sql first.")
got = pd.read_sql_query(open(path).read().strip().rstrip(";"), db)
d, s, e = (pd.read_sql_query(f"select * from {t}", db) for t in ("departments", "students", "enrollments"))
x = e[e.course == "DBMS"].merge(s, on="student_id").merge(d, on="dept_id")
want = (x.groupby("dept_name").agg(n=("student_id", "nunique"), avg=("marks", "mean")).reset_index())
want = want[want.n >= 3].assign(avg=lambda t: t.avg.round(2)).sort_values(["avg", "dept_name"], ascending=[False, True]).reset_index(drop=True)
print("Expected (pandas):\n", want, "\n\nAI query result:\n", got)
vals_ok = len(got) == len(want) and [round(float(v), 2) for v in got.iloc[:, 2]] == list(want.avg) and list(got.iloc[:, 0]) == list(want.dept_name) and [int(v) for v in got.iloc[:, 1]] == list(want.n)
print("\nMATCH" if vals_ok else "\nDIFFERENT - find out why (distinct count? a student enrolled twice? ordering?)")
