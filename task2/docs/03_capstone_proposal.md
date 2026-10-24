# Proposed capstone lab: "Rule-checked scheduling assistant" (built on Task 1)

**Where it fits:** SP301 Special Project (Sem VI, 0-0-6, 3 credits, change C07) and as the lab part of NEW-03 Software Engineering & Testing (Sem V) and NEW-04 MLOps & Deployment (Sem VI).

**Idea.** Teams take one real campus workflow (e.g. timetable preparation, lab-slot allocation, exam invigilation duty) and deliver a small assistant that: collects structured inputs, generates a draft with a solver or model, validates it with an **independent checker**, escalates exceptions to a named human owner, and logs approvals. The Task 1 timetable tool is the worked example.

**Why this is a good capstone.** It needs requirements gathering with permission, data handling with synthetic data, a testable design (five test cases: normal, missing information, duplicate, unauthorized request, failed step), deployment and monitoring, and honest reporting of limits.

## 12-week plan (6 contact hours/week)
| Weeks | Output | Skills |
|---|---|---|
| 1-2 | Process map, evidence log, scale estimate | requirements, ethics of data |
| 3-4 | Input schema, synthetic data, rule list with owner | data modelling, SQL |
| 5-7 | Generator + validator, unit tests | Python, testing, Git |
| 8-9 | Five-case test report, fault-injection tests | QA |
| 10 | Package and deploy (container or cloud function), logging | MLOps |
| 11 | Net-time-saved study with review and support effort | evaluation |
| 12 | Demo, limitations, AI-use record | communication, responsible AI |

## Assessment (suggested)
Process study 15% | Design and approval boundaries 15% | Working tool and tests 30% | Verification of AI-assisted parts 15% | Deployment 10% | Report and limitations 15%.

## Prerequisites
CS201, CS206, DS202; NEW-03 for the Sem VI version. **Resources:** free tools only, synthetic data, no live college systems. **Risk:** projects that touch private data; mitigate with the same rule used here (synthetic or permitted data only, no names, IDs, marks or fees).
