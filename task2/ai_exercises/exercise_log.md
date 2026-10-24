# AI-Assisted Exercise Log

**Record date:** 2026-10-24  
**Tool for the answers recorded below:** ChatGPT  
**Model label:** GPT-6 (confirm against the model label shown in the interface)  
**Time:** Not recorded  
**Prompt changes:** The five prompts in `prompts.md` are the reference prompts. The answers below were generated in this ChatGPT conversation; they are not claimed to be Claude's original answers.

## 1. Data Structures (CS102) — Linked-list cycle detection

- **Date:** 2026-10-24
- **Tool/model:** ChatGPT; model label to be confirmed against the interface.
- **Prompt used:** `prompts.md`, prompt 1. The prompt asks for a `Node` class, Floyd's cycle-detection algorithm, complexity, and explanation.
- **Full ChatGPT answer:**

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

def has_cycle(head):
    slow = head
    fast = head

    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            return True

    return False
```

**Time complexity:** O(n), where n is the number of nodes visited.  
**Auxiliary space complexity:** O(1), because only two pointers are maintained.

**Explanation:** The slow pointer advances one node per iteration and the fast pointer advances two. If a cycle exists, both pointers eventually enter it. Within the cycle, the fast pointer gains one node on the slow pointer per iteration, so their relative positions must eventually coincide. If there is no cycle, the fast pointer or its next pointer becomes `None`, and the function returns `False`.

- **How I verified it:** Ran `python task2\ai_exercises\verify\v1_test_cycle.py`.
- **Observed result:** All 8 tests passed: empty list, one node without a cycle, self-cycle, five-node list without a cycle, tail-to-head cycle, tail-to-middle cycle, two-node cycle, and a 1,000-node list without a cycle.
- **What matched:** The implementation passed every listed test.
- **Mistakes or weak points:** The tests cover several important cases but do not prove correctness for every possible list. The function assumes a well-formed linked list and does not validate arbitrary objects.
- **Conclusion:** I would use this standard implementation for cycle detection, with additional tests if it were part of a larger application.

## 2. Database Management Systems (CS206) — SQL aggregation

- **Date:** 2026-10-24
- **Tool/model:** ChatGPT; model label to be confirmed against the interface.
- **Prompt used:** `prompts.md`, prompt 2. The prompt requests department-wise DBMS enrollment counts and average marks, a minimum of three distinct students, and a specified ordering.
- **Full ChatGPT answer:**

```sql
SELECT
    d.dept_name,
    COUNT(DISTINCT s.student_id) AS student_count,
    ROUND(AVG(e.marks), 2) AS average_marks
FROM departments AS d
JOIN students AS s
    ON s.dept_id = d.dept_id
JOIN enrollments AS e
    ON e.student_id = s.student_id
WHERE e.course = 'DBMS'
GROUP BY d.dept_id, d.dept_name
HAVING COUNT(DISTINCT s.student_id) >= 3
ORDER BY average_marks DESC, d.dept_name ASC;
```

**Clause explanation:**
- `SELECT` returns the department name, distinct-student count, and rounded average.
- `FROM` starts with the departments table.
- `JOIN` connects departments to students and students to their enrollments.
- `WHERE` keeps only enrollments for the course named `DBMS`.
- `GROUP BY` calculates the results separately for each department.
- `HAVING` keeps departments with at least three distinct students enrolled in DBMS.
- `ORDER BY` sorts by average marks from highest to lowest, then by department name alphabetically.
- `COUNT(DISTINCT s.student_id)` avoids counting the same student multiple times in the student count.
- `ROUND(AVG(e.marks), 2)` rounds the average marks to two decimal places.

- **How I verified it:** Ran `python task2\ai_exercises\verify\v2_sql_check.py`.
- **Observed result:** The query output matched the expected pandas output:
  - CSE: 4 students, average marks 76.25
  - AI: 4 students, average marks 72.25
  The verification script reported `MATCH`.
- **What matched:** Department counts, averages, and output ordering matched the verifier's expected result.
- **Mistakes or weak points:** The query assumes the schema and course name are correct. If a student can have multiple DBMS enrollment records, `AVG(e.marks)` averages enrollment rows, not one pre-aggregated mark per student. The schema does not state whether that situation is possible.
- **Conclusion:** The query passed the supplied synthetic-data check. I would verify the enrollment uniqueness rules before using it on real institutional data.

## 3. Operating Systems (CS302) — Scheduling algorithms

- **Date:** 2026-10-24
- **Tool/model:** ChatGPT; model label to be confirmed against the interface.
- **Prompt used:** `prompts.md`, prompt 3. The prompt gives five processes and requests waiting times and Gantt charts for FCFS, non-preemptive SJF, and Round Robin with quantum 3.
- **Full ChatGPT answer:**

### FCFS

Gantt chart:

```text
0 | P1 | 8 | P2 | 12 | P3 | 21 | P4 | 26 | P5 | 28
```

| Process | Arrival | Burst | Waiting |
|---|---:|---:|---:|
| P1 | 0 | 8 | 0 |
| P2 | 1 | 4 | 7 |
| P3 | 2 | 9 | 10 |
| P4 | 3 | 5 | 18 |
| P5 | 4 | 2 | 22 |

Average waiting time = (0 + 7 + 10 + 18 + 22) / 5 = **11.40**.

### Non-preemptive SJF

At time 0, P1 is the only available process. After P1 completes, the shortest available job is selected each time.

Gantt chart:

```text
0 | P1 | 8 | P5 | 10 | P2 | 14 | P4 | 19 | P3 | 28
```

| Process | Arrival | Burst | Waiting |
|---|---:|---:|---:|
| P1 | 0 | 8 | 0 |
| P2 | 1 | 4 | 9 |
| P3 | 2 | 9 | 17 |
| P4 | 3 | 5 | 11 |
| P5 | 4 | 2 | 4 |

Average waiting time = (0 + 9 + 17 + 11 + 4) / 5 = **8.20**.

### Round Robin, quantum = 3

Gantt chart:

```text
0 | P1 | 3 | P2 | 6 | P3 | 9 | P4 | 12 |
P1 | 15 | P5 | 17 | P2 | 18 | P3 | 21 |
P4 | 23 | P1 | 25 | P3 | 28
```

| Process | Arrival | Burst | Waiting |
|---|---:|---:|---:|
| P1 | 0 | 8 | 17 |
| P2 | 1 | 4 | 13 |
| P3 | 2 | 9 | 17 |
| P4 | 3 | 5 | 15 |
| P5 | 4 | 2 | 11 |

Average waiting time = (17 + 13 + 17 + 15 + 11) / 5 = **14.60**.

Waiting time can be calculated as completion time minus arrival time minus burst time. Round Robin's order depends on the stated ready-queue convention when a process arrives at the same instant that a time slice ends.

- **How I verified it:** Ran `python task2\ai_exercises\verify\v3_os_scheduling.py`.
- **Observed result:** The script reported FCFS average waiting 11.40, SJF 8.20, and Round Robin 14.60, with the waiting times and Gantt schedules shown above.
- **What matched:** The displayed calculations matched the verification script's reported values.
- **Mistakes or weak points:** A Gantt chart should make time boundaries unambiguous. For Round Robin, the ready-queue convention at simultaneous arrival and quantum expiry should be documented because it can affect the order in other implementations.
- **Conclusion:** The numbers matched the supplied verifier. I would keep the process inputs, queue convention, and completion times alongside the result to make it easier to audit.

## 4. Machine Learning (DS304) — Iris classification baseline

- **Date:** 2026-10-24
- **Tool/model:** ChatGPT; model label to be confirmed against the interface.
- **Prompt used:** `prompts.md`, prompt 4. The prompt requests a stratified 80/20 split, logistic regression, test accuracy, macro F1, and 5-fold cross-validation.
- **Full ChatGPT answer:**

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("test accuracy:", round(accuracy_score(y_test, y_pred), 4))
print("test macro F1:", round(f1_score(y_test, y_pred, average="macro"), 4))

cv_scores = cross_val_score(
    LogisticRegression(max_iter=200),
    X,
    y,
    cv=5,
    scoring="accuracy"
)
print("5-fold CV accuracy:", round(cv_scores.mean(), 4))
```

**Overfitting explanation:** Overfitting would be suggested by training performance that is substantially better than performance on unseen test data or cross-validation folds. The Iris dataset is small and relatively simple, and logistic regression is a comparatively simple model, so severe overfitting is less likely than with a highly flexible model. However, overfitting is not impossible, and evaluation results should still be checked.

- **How I verified it:** Ran `python task2\ai_exercises\verify\v4_ml_baseline.py`.
- **Observed result:** Test accuracy 0.9667; test macro F1 0.9666; training accuracy 0.9750; five-fold CV accuracy 0.9733. The script notes that scikit-learn versions can change the last few decimal places.
- **What matched:** The recorded baseline results are the results printed by the verification script.
- **Mistakes or weak points:** The code reports the requested metrics but does not print individual fold scores. The exact output can depend on the library version. The test score and cross-validation score are estimates, not proof that the model will perform equally well on new real-world data.
- **Conclusion:** This is a useful baseline for the supplied dataset. I would record the scikit-learn version and inspect class-level errors before drawing stronger conclusions.

## 5. Computer Networks (CS306) — Subnetting

- **Date:** 2026-10-24
- **Tool/model:** ChatGPT; model label to be confirmed against the interface.
- **Prompt used:** `prompts.md`, prompt 5. The prompt requests four equal subnets from `192.168.10.0/24`.
- **Full ChatGPT answer:**

A `/24` network has 256 addresses. To divide it into four equal subnets, borrow two host bits because 2² = 4. The new prefix is `/26`, leaving 6 host bits per subnet. Each subnet has 64 total addresses and 62 usable host addresses after excluding the network and broadcast addresses.

Subnet mask for all four subnets: `255.255.255.192`.

| Subnet | Network address | First usable | Last usable | Broadcast | Usable hosts |
|---|---|---|---|---|---:|
| 1 | 192.168.10.0/26 | 192.168.10.1 | 192.168.10.62 | 192.168.10.63 | 62 |
| 2 | 192.168.10.64/26 | 192.168.10.65 | 192.168.10.126 | 192.168.10.127 | 62 |
| 3 | 192.168.10.128/26 | 192.168.10.129 | 192.168.10.190 | 192.168.10.191 | 62 |
| 4 | 192.168.10.192/26 | 192.168.10.193 | 192.168.10.254 | 192.168.10.255 | 62 |

The block size in the last octet is 64, so the subnet network addresses begin at 0, 64, 128, and 192.

- **How I verified it:** Ran `python task2\ai_exercises\verify\v5_subnet.py`.
- **Observed result:** The script printed the four `/26` networks with mask `255.255.255.192`, the expected first and last usable addresses, broadcast addresses, and 62 usable hosts each.
- **What matched:** All four printed subnet ranges matched the table.
- **Mistakes or weak points:** This calculation assumes conventional IPv4 subnetting and excludes the network and broadcast addresses from usable hosts. It does not discuss special-purpose address reservations or deployment-specific network policies.
- **Conclusion:** The subnet calculation matched the verification script and is suitable for the stated exercise.

## Overall reflection

I ran the five supplied verification scripts and recorded their observed results. Passing these scripts is evidence that the answers match the tested cases; it is not proof that every possible edge case has been tested. I have documented assumptions and limitations rather than claiming extra manual tests that were not recorded.
