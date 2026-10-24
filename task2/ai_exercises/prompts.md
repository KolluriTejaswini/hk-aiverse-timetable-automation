# The 5 prompts (copy exactly, paste into the AI tool you use)

Use the **same wording** so your record is reproducible. Write down the model name shown by the tool and today's date.

## 1. Data Structures (CS102)
```
In Python, define class Node with attributes val and next. Write a function has_cycle(head) that returns True if a singly linked list has a cycle, using Floyd's tortoise-and-hare method. State the time and space complexity and explain why the two pointers must meet if a cycle exists.
```
Save the AI's code as `verify/ai_solution.py`, then run `python verify/v1_test_cycle.py`.

## 2. Database Management Systems (CS206)
```
Schema (SQLite): departments(dept_id, dept_name); students(student_id, dept_id, year); enrollments(student_id, course, marks). Write one SQL query that returns, for each department, dept_name, the number of distinct students enrolled in the course 'DBMS', and the average DBMS marks rounded to 2 decimals, only for departments with at least 3 such students, ordered by average marks descending then dept_name. Explain each clause.
```
Save the AI's query as `verify/ai_query.sql`, then run `python verify/v2_sql_check.py`.

## 3. Operating Systems (CS302)
```
Five processes (arrival time, burst time): P1 (0, 8), P2 (1, 4), P3 (2, 9), P4 (3, 5), P5 (4, 2). Compute the waiting time of each process and the average waiting time for FCFS, non-preemptive SJF, and Round Robin with time quantum 3. Show a Gantt chart for each.
```
Compare the AI's numbers with `python verify/v3_os_scheduling.py`.

## 4. Machine Learning (DS304)
```
Using scikit-learn on the Iris dataset, write code that makes a stratified 80/20 train-test split with random_state=42, trains a logistic regression (max_iter=200), reports test accuracy and macro F1, and also reports 5-fold cross-validated accuracy on the full data. Explain what overfitting would look like here and why this dataset is unlikely to show it.
```
Run the AI's code yourself, then compare with `python verify/v4_ml_baseline.py` (needs scikit-learn).

## 5. Computer Networks (CS306)
```
Divide 192.168.10.0/24 into 4 equal subnets. For each subnet give the subnet mask, network address, first usable host, last usable host, broadcast address and number of usable hosts. Explain how you chose the prefix length.
```
Compare with `python verify/v5_subnet.py`.

---
**Rule for the record:** paste the AI's *full* output, then write what you checked, what matched, and **every mistake or weak explanation you found** (even small ones). If everything matched, say how you know it is not luck (e.g. you also tried 3 extra inputs).
